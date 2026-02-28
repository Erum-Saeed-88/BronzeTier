"""
Verification script for Bronze Tier AI Employee.

Run this script to verify all components are working correctly.
"""

import sys
from pathlib import Path

def main():
    # Paths are relative to scripts folder
    vault_path = Path(__file__).parent.parent / 'Vault'
    scripts_path = Path(__file__).parent
    
    print("=" * 60)
    print("AI Employee - Bronze Tier Verification")
    print("=" * 60)
    print()
    
    all_passed = True
    
    # Check 1: Vault folder structure
    print("Checking Vault folder structure...")
    required_folders = [
        'Inbox',
        'Needs_Action', 
        'Done',
        'Pending_Approval',
        'Approved',
        'Plans',
        'Logs',
        'Briefings',
        'Accounting',
        'Invoices'
    ]
    
    for folder in required_folders:
        folder_path = vault_path / folder
        if folder_path.exists() and folder_path.is_dir():
            print(f"[PASS] {folder}/")
        else:
            print(f"[FAIL] {folder}/ - MISSING")
            all_passed = False
    
    print()
    
    # Check 2: Required Markdown files
    print("Checking required Markdown files...")
    required_files = [
        'Dashboard.md',
        'Company_Handbook.md',
        'Business_Goals.md'
    ]
    
    for file in required_files:
        file_path = vault_path / file
        if file_path.exists():
            print(f"[PASS] {file}")
        else:
            print(f"[FAIL] {file} - MISSING")
            all_passed = False
    
    print()
    
    # Check 3: Python scripts
    print("Checking Python scripts...")
    required_scripts = [
        'base_watcher.py',
        'filesystem_watcher.py',
        'orchestrator.py'
    ]
    
    for script in required_scripts:
        script_path = scripts_path / script
        if script_path.exists():
            print(f"[PASS] {script}")
        else:
            print(f"[FAIL] {script} - MISSING")
            all_passed = False
    
    print()
    
    # Check 4: Python dependencies
    print("Checking Python dependencies...")
    try:
        import watchdog
        print("[PASS] watchdog (installed)")
    except ImportError:
        print("[FAIL] watchdog - NOT INSTALLED")
        print("  Run: pip install watchdog")
        all_passed = False
    
    print()
    
    # Check 5: Claude Code availability
    print("Checking Claude Code...")
    import subprocess
    try:
        result = subprocess.run(
            ['claude', '--version'],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            print(f"[PASS] Claude Code: {result.stdout.strip()}")
        else:
            print("[WARN] Claude Code installed but not responding")
            all_passed = False
    except FileNotFoundError:
        print("[FAIL] Claude Code - NOT FOUND")
        print("  Install: npm install -g @anthropic/claude-code")
        all_passed = False
    except subprocess.TimeoutExpired:
        print("[WARN] Claude Code - TIMEOUT")
        all_passed = False
    
    print()
    print("=" * 60)
    
    if all_passed:
        print("[PASS] All checks passed! Bronze Tier is ready.")
        print()
        print("Next steps:")
        print("  1. Open Vault/ in Obsidian")
        print("  2. Run: python scripts/filesystem_watcher.py ../Vault")
        print("  3. Run: python scripts/orchestrator.py ../Vault")
        print("  4. Run: claude \"Process files in Needs_Action\"")
    else:
        print("[FAIL] Some checks failed. Please fix the issues above.")
        sys.exit(1)
    
    print("=" * 60)

if __name__ == '__main__':
    main()
