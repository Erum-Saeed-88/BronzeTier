"""
Orchestrator - Master process that triggers Qwen Code to process tasks.

The orchestrator:
1. Monitors the Needs_Action folder for new items
2. Triggers Qwen Code to process pending tasks
3. Updates the Dashboard with recent activity
4. Manages the overall workflow

For Bronze Tier: Simple polling-based orchestrator that triggers Qwen Code
when new items are detected in Needs_Action folder.
"""

import time
import logging
import subprocess
import shutil
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


class Orchestrator:
    """
    Main orchestrator for the AI Employee system.

    Coordinates between watchers, Qwen Code, and the vault.
    """
    
    def __init__(self, vault_path: str, check_interval: int = 30):
        """
        Initialize the orchestrator.
        
        Args:
            vault_path: Path to the Obsidian vault root
            check_interval: Seconds between checks (default: 30)
        """
        self.vault_path = Path(vault_path).resolve()
        self.check_interval = check_interval
        self.logger = logging.getLogger('Orchestrator')
        
        # Vault folders
        self.needs_action = self.vault_path / 'Needs_Action'
        self.done = self.vault_path / 'Done'
        self.plans = self.vault_path / 'Plans'
        self.logs = self.vault_path / 'Logs'
        self.dashboard = self.vault_path / 'Dashboard.md'
        
        # Ensure folders exist
        for folder in [self.needs_action, self.done, self.plans, self.logs]:
            folder.mkdir(parents=True, exist_ok=True)
        
        # State tracking
        self.processed_files = set()
        self.qwen_available = self._check_qwen_code()

        self.logger.info(f'Vault path: {self.vault_path}')
        self.logger.info(f'Qwen Code available: {self.qwen_available}')
    
    def _check_qwen_code(self) -> bool:
        """Check if Qwen Code is installed and available."""
        try:
            # On Windows, use shell=True to find commands in PATH
            import os
            use_shell = os.name == 'nt'
            
            result = subprocess.run(
                ['qwen', '--version'],
                capture_output=True,
                text=True,
                timeout=10,
                shell=use_shell
            )
            self.logger.info(f'Qwen Code version: {result.stdout.strip()}')
            return result.returncode == 0
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            self.logger.warning(f'Qwen Code not found or not responding: {e}')
            return False
    
    def get_pending_items(self) -> list:
        """
        Get list of pending .md files in Needs_Action folder.
        
        Returns:
            List of Path objects for pending files
        """
        if not self.needs_action.exists():
            return []
        
        pending = []
        for f in self.needs_action.glob('*.md'):
            if str(f) not in self.processed_files:
                pending.append(f)
        
        return pending
    
    def update_dashboard(self, action: str, details: str = ''):
        """
        Update the Dashboard.md with recent activity.
        
        Args:
            action: Description of the action taken
            details: Additional details
        """
        if not self.dashboard.exists():
            return
        
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        entry = f'- [{timestamp}] {action}'
        
        try:
            content = self.dashboard.read_text()
            
            # Find the "Recent Activity" section and add entry
            if '## Recent Activity' in content:
                lines = content.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if line == '## Recent Activity':
                        new_lines.append(entry)
                
                content = '\n'.join(new_lines)
            else:
                # Append to end if section not found
                content += f'\n\n## Recent Activity\n{entry}\n'
            
            self.dashboard.write_text(content)
            self.logger.info(f'Dashboard updated: {action}')
            
        except Exception as e:
            self.logger.error(f'Error updating dashboard: {e}')
    
    def log_action(self, action_type: str, details: dict):
        """
        Log an action to the logs folder.
        
        Args:
            action_type: Type of action (e.g., 'file_processed', 'claude_triggered')
            details: Dictionary of action details
        """
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = self.logs / f'{today}.jsonl'
        
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'action_type': action_type,
            'actor': 'orchestrator',
            'details': details
        }
        
        try:
            with open(log_file, 'a') as f:
                import json
                f.write(json.dumps(log_entry) + '\n')
        except Exception as e:
            self.logger.error(f'Error writing log: {e}')
    
    def trigger_qwen_code(self, task_description: str) -> bool:
        """
        Trigger Qwen Code to process tasks.

        For Bronze Tier: This is a placeholder that logs the intent.
        In practice, user would run Qwen Code manually or via script.

        Args:
            task_description: Description of the task for Qwen

        Returns:
            True if Qwen was triggered successfully
        """
        self.logger.info(f'Triggering Qwen Code: {task_description}')

        # For Bronze Tier: Create a prompt file that user can reference
        prompt_file = self.vault_path / '_qwen_prompt.md'
        prompt_content = f'''# Qwen Code Task

**Generated:** {datetime.now().isoformat()}

**Task:** {task_description}

## Instructions for User
Run the following command in your terminal:

```bash
cd "{self.vault_path}"
qwen "Process all files in /Needs_Action folder. Read each file, determine required actions, create plans if needed, and move completed items to /Done. Follow the Company_Handbook.md rules."
```

## Context
- Vault: {self.vault_path}
- Pending items: {len(self.get_pending_items())}
- Company Handbook: {self.vault_path / 'Company_Handbook.md'}

---
*This prompt was auto-generated by the Orchestrator*
'''

        try:
            prompt_file.write_text(prompt_content)
            self.log_action('qwen_prompt_created', {
                'task': task_description,
                'prompt_file': str(prompt_file)
            })
            self.update_dashboard(f'Qwen prompt created: {task_description[:50]}...')
            return True
        except Exception as e:
            self.logger.error(f'Error creating Qwen prompt: {e}')
            return False
    
    def mark_complete(self, file_path: Path):
        """
        Mark a file as complete by moving it to Done folder.
        
        Args:
            file_path: Path to the completed file
        """
        try:
            dest = self.done / file_path.name
            shutil.move(str(file_path), str(dest))
            self.processed_files.add(str(file_path))
            self.logger.info(f'Moved to Done: {file_path.name}')
        except Exception as e:
            self.logger.error(f'Error moving file to Done: {e}')
    
    def run(self):
        """
        Main orchestrator loop.
        """
        self.logger.info('Starting Orchestrator')
        self.logger.info(f'Check interval: {self.check_interval}s')

        if not self.qwen_available:
            self.logger.warning('Qwen Code not available - running in limited mode')

        try:
            while True:
                # Check for pending items
                pending = self.get_pending_items()

                if pending:
                    self.logger.info(f'Found {len(pending)} pending item(s)')

                    for item in pending:
                        self.log_action('pending_item_detected', {
                            'file': str(item),
                            'size': item.stat().st_size
                        })

                        # Trigger Qwen Code
                        self.trigger_qwen_code(f'Process {item.name}')

                        # Mark as processed (user will move to Done after Qwen)
                        self.processed_files.add(str(item))

                time.sleep(self.check_interval)

        except KeyboardInterrupt:
            self.logger.info('Orchestrator stopped by user')
        except Exception as e:
            self.logger.error(f'Fatal error: {e}')
            raise


def main():
    """Main entry point."""
    import sys
    
    # Default vault path (can be overridden via command line)
    vault_path = sys.argv[1] if len(sys.argv) > 1 else '../Vault'
    vault_path = Path(vault_path).resolve()
    
    # Create and run orchestrator
    orchestrator = Orchestrator(str(vault_path), check_interval=30)
    orchestrator.run()


if __name__ == '__main__':
    main()
