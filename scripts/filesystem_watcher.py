"""
File System Watcher - Monitors a drop folder for new files.

When files are added to the Inbox folder, this watcher copies them to
Needs_Action and creates metadata files for Claude to process.

This is the Bronze Tier watcher - simple, local, and requires no API setup.
"""

import time
import shutil
import hashlib
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

from base_watcher import BaseWatcher


class DropFolderHandler(FileSystemEventHandler):
    """Handles file system events for the drop folder."""
    
    def __init__(self, vault_path: str):
        """
        Initialize the handler.
        
        Args:
            vault_path: Path to the Obsidian vault root
        """
        self.vault_path = Path(vault_path)
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.processed_files = set()
        
        # Ensure folders exist
        self.inbox.mkdir(parents=True, exist_ok=True)
        self.needs_action.mkdir(parents=True, exist_ok=True)
    
    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return
        
        source = Path(event.src_path)
        
        # Skip if already processed
        if str(source) in self.processed_files:
            return
        
        # Skip hidden files and temp files
        if source.name.startswith('.') or source.suffix == '.tmp':
            return
        
        self.process_file(source)
    
    def process_file(self, source: Path):
        """
        Process a new file: copy to Needs_Action and create metadata.
        
        Args:
            source: Path to the source file
        """
        try:
            # Generate unique ID
            file_hash = hashlib.md5(str(source).encode()).hexdigest()[:8]
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # Copy file to Needs_Action
            dest_name = f'FILE_{timestamp}_{source.name}'
            dest = self.needs_action / dest_name
            shutil.copy2(source, dest)
            
            # Create metadata file
            self.create_metadata(source, dest)
            
            self.processed_files.add(str(source))
            print(f'✓ Processed: {source.name} -> {dest_name}')
            
        except Exception as e:
            print(f'✗ Error processing {source.name}: {e}')
    
    def create_metadata(self, source: Path, dest: Path):
        """
        Create a metadata .md file for the dropped file.
        
        Args:
            source: Original file path
            dest: Destination file path in Needs_Action
        """
        stat = source.stat()
        
        metadata_content = f'''---
type: file_drop
original_name: {source.name}
size: {stat.st_size}
created: {datetime.now().isoformat()}
source_path: {source.absolute()}
status: pending
---

# File Drop for Processing

**Original File:** `{source.name}`

**Size:** {stat.st_size} bytes

**Dropped At:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Instructions
This file was dropped into the Inbox folder for processing.
Please review and take appropriate action.

## Suggested Actions
- [ ] Review file content
- [ ] Determine required action
- [ ] Execute action or create plan
- [ ] Move to /Done when complete

---
*Created by File System Watcher*
'''
        
        meta_path = dest.with_suffix('.md')
        meta_path.write_text(metadata_content)


class FileSystemWatcher(BaseWatcher):
    """
    Watcher that monitors the Inbox folder for new files.
    
    Uses watchdog library for efficient file system monitoring.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 1):
        """
        Initialize the file system watcher.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Ignored for event-based watcher
        """
        super().__init__(vault_path, check_interval=1)
        self.handler = DropFolderHandler(vault_path)
        self.observer = None
    
    def check_for_updates(self) -> list:
        """
        Not used for event-based watcher.
        
        This method exists for API compatibility with BaseWatcher.
        """
        return []
    
    def create_action_file(self, item) -> Path:
        """
        Not used for event-based watcher.
        
        This method exists for API compatibility with BaseWatcher.
        """
        pass
    
    def run(self):
        """
        Run the file system watcher using event-based monitoring.
        """
        self.logger.info(f'Starting FileSystemWatcher')
        self.logger.info(f'Watching: {self.handler.inbox}')
        
        self.observer = Observer()
        self.observer.schedule(self.handler, str(self.handler.inbox), recursive=False)
        self.observer.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info('Stopping FileSystemWatcher')
            self.observer.stop()
        
        self.observer.join()
        self.logger.info('FileSystemWatcher stopped')


if __name__ == '__main__':
    import sys
    
    # Default vault path (can be overridden via command line)
    vault_path = sys.argv[1] if len(sys.argv) > 1 else '../Vault'
    
    # Resolve to absolute path
    vault_path = Path(vault_path).resolve()
    
    # Start the watcher
    watcher = FileSystemWatcher(str(vault_path))
    watcher.run()
