#!/usr/bin/env python3
"""
Sentinel Restore — Recovery tool for corrupted or lost files
Part of Sentinel — AI Agent State Guardian

Author: Shadow Rose
License: MIT
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Tuple

# Import config
try:
    import sentinel_config as config
except ImportError:
    print("ERROR: sentinel_config.py not found. Copy config_example.py to sentinel_config.py and configure it.")
    sys.exit(1)


class RestoreTool:
    """File restoration from backups."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.workspace = Path(config_obj.WORKSPACE_ROOT).resolve()
        self.backup_root = Path(config_obj.BACKUP_DIR).resolve()
        self.state_file = Path(config_obj.STATE_FILE).resolve()
    
    def list_backups(self, filepath: Optional[Path] = None) -> List[Tuple[datetime, Path]]:
        """List all available backups, optionally filtered by file."""
        backups = []
        
        try:
            # Get all timestamped backup directories
            backup_dirs = sorted([d for d in self.backup_root.iterdir() if d.is_dir()], reverse=True)
            
            for backup_dir in backup_dirs:
                # Parse timestamp from directory name
                try:
                    timestamp = datetime.strptime(backup_dir.name, "%Y%m%d_%H%M%S")
                except ValueError:
                    continue
                
                if filepath:
                    # Check if this backup contains the specific file
                    rel_path = filepath.relative_to(self.workspace)
                    backup_file = backup_dir / rel_path
                    if backup_file.exists():
                        backups.append((timestamp, backup_file))
                else:
                    # List all files in this backup
                    for backup_file in backup_dir.rglob('*'):
                        if backup_file.is_file():
                            backups.append((timestamp, backup_file))
            
            return backups
        except Exception as e:
            print(f"Error listing backups: {e}")
            return []
    
    def find_latest_backup(self, filepath: Path) -> Optional[Path]:
        """Find the most recent backup of a specific file."""
        try:
            rel_path = filepath.relative_to(self.workspace)
            
            backup_dirs = sorted([d for d in self.backup_root.iterdir() if d.is_dir()], reverse=True)
            
            for backup_dir in backup_dirs:
                candidate = backup_dir / rel_path
                if candidate.exists() and candidate.is_file():
                    return candidate
            
            return None
        except Exception as e:
            print(f"Error finding backup: {e}")
            return None
    
    def find_backup_at_time(self, filepath: Path, target_time: datetime) -> Optional[Path]:
        """Find the backup closest to a specific time."""
        try:
            rel_path = filepath.relative_to(self.workspace)
            
            backup_dirs = sorted([d for d in self.backup_root.iterdir() if d.is_dir()])
            
            closest_backup = None
            min_diff = float('inf')
            
            for backup_dir in backup_dirs:
                try:
                    timestamp = datetime.strptime(backup_dir.name, "%Y%m%d_%H%M%S")
                    diff = abs((timestamp - target_time).total_seconds())
                    
                    candidate = backup_dir / rel_path
                    if candidate.exists() and diff < min_diff:
                        min_diff = diff
                        closest_backup = candidate
                except ValueError:
                    continue
            
            return closest_backup
        except Exception as e:
            print(f"Error finding backup at time: {e}")
            return None
    
    def restore_file(self, filepath: Path, backup_path: Path, create_backup: bool = True) -> bool:
        """Restore a file from backup."""
        try:
            # Create safety backup of current file if it exists
            if create_backup and filepath.exists():
                safety_backup = filepath.parent / f"{filepath.name}.before-restore.bak"
                shutil.copy2(filepath, safety_backup)
                print(f"Safety backup created: {safety_backup}")
            
            # Restore
            filepath.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_path, filepath)
            print(f"✓ Restored: {filepath}")
            print(f"  From: {backup_path}")
            
            return True
        except Exception as e:
            print(f"✗ Restore failed: {e}")
            return False
    
    def verify_backup(self, backup_path: Path) -> Tuple[bool, str]:
        """Verify a backup file is valid."""
        try:
            if not backup_path.exists():
                return False, "Backup file does not exist"
            
            if not backup_path.is_file():
                return False, "Backup path is not a file"
            
            stat = backup_path.stat()
            if stat.st_size == 0:
                return False, "Backup file is empty (0 bytes)"
            
            # Try to read first few bytes
            try:
                with open(backup_path, 'rb') as f:
                    f.read(1024)
            except Exception as e:
                return False, f"Cannot read backup file: {e}"
            
            return True, "OK"
        except Exception as e:
            return False, f"Verification failed: {e}"
    
    def interactive_restore(self, filepath: Path):
        """Interactive restoration with backup selection."""
        print(f"\n=== Restore: {filepath} ===\n")
        
        # Check if file exists in workspace
        if filepath.exists():
            stat = filepath.stat()
            print(f"Current file:")
            print(f"  Size: {stat.st_size} bytes")
            print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime)}")
            print()
        else:
            print("Current file: DOES NOT EXIST\n")
        
        # Find backups
        backups = self.list_backups(filepath)
        
        if not backups:
            print("✗ No backups found for this file")
            return
        
        print(f"Available backups ({len(backups)}):\n")
        
        for idx, (timestamp, backup_path) in enumerate(backups, 1):
            stat = backup_path.stat()
            is_valid, msg = self.verify_backup(backup_path)
            status = "✓" if is_valid else "✗"
            print(f"{idx}. {status} {timestamp} | {stat.st_size} bytes | {backup_path}")
        
        print(f"\n0. Cancel")
        
        # Get user choice
        try:
            choice = input("\nSelect backup to restore (0 to cancel): ").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                print("Restore cancelled")
                return
            
            if choice_num < 1 or choice_num > len(backups):
                print("Invalid selection")
                return
            
            selected_backup = backups[choice_num - 1][1]
            
            # Verify backup
            is_valid, msg = self.verify_backup(selected_backup)
            if not is_valid:
                print(f"\n✗ Cannot restore: {msg}")
                return
            
            # Confirm
            confirm = input(f"\nRestore {filepath} from {selected_backup}? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Restore cancelled")
                return
            
            # Restore
            self.restore_file(filepath, selected_backup)
        
        except (ValueError, KeyboardInterrupt):
            print("\nRestore cancelled")
    
    def restore_latest(self, filepath: Path, auto: bool = False):
        """Restore the latest backup of a file."""
        print(f"\n=== Restore latest: {filepath} ===\n")
        
        backup_path = self.find_latest_backup(filepath)
        
        if backup_path is None:
            print("✗ No backup found")
            return
        
        # Verify backup
        is_valid, msg = self.verify_backup(backup_path)
        if not is_valid:
            print(f"✗ Backup invalid: {msg}")
            return
        
        stat = backup_path.stat()
        print(f"Latest backup: {backup_path}")
        print(f"  Size: {stat.st_size} bytes")
        print(f"  Modified: {datetime.fromtimestamp(stat.st_mtime)}")
        
        if not auto:
            confirm = input("\nRestore this backup? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("Restore cancelled")
                return
        
        self.restore_file(filepath, backup_path)
    
    def list_all_backups(self):
        """List all backups in the backup directory."""
        print("\n=== All Backups ===\n")
        
        try:
            backup_dirs = sorted([d for d in self.backup_root.iterdir() if d.is_dir()], reverse=True)
            
            if not backup_dirs:
                print("No backups found")
                return
            
            for backup_dir in backup_dirs:
                try:
                    timestamp = datetime.strptime(backup_dir.name, "%Y%m%d_%H%M%S")
                    file_count = len(list(backup_dir.rglob('*')))
                    total_size = sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
                    
                    print(f"{timestamp} | {file_count} files | {total_size:,} bytes | {backup_dir}")
                except ValueError:
                    print(f"[invalid timestamp] {backup_dir}")
        
        except Exception as e:
            print(f"Error listing backups: {e}")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sentinel Restore — Recovery tool")
    parser.add_argument('--file', type=str, help='File path to restore (relative to workspace)')
    parser.add_argument('--latest', action='store_true', help='Restore latest backup')
    parser.add_argument('--interactive', action='store_true', help='Interactive backup selection')
    parser.add_argument('--list', action='store_true', help='List all backups')
    parser.add_argument('--auto', action='store_true', help='Skip confirmation prompts')
    
    args = parser.parse_args()
    
    tool = RestoreTool(config)
    
    if args.list:
        tool.list_all_backups()
        return
    
    if not args.file:
        print("ERROR: --file required (unless using --list)")
        print("Example: python3 sentinel_restore.py --file memory/2026-02-21.md --latest")
        sys.exit(1)
    
    filepath = tool.workspace / args.file
    
    if not filepath.is_relative_to(tool.workspace):
        print("ERROR: File path must be relative to workspace")
        sys.exit(1)
    
    if args.latest:
        tool.restore_latest(filepath, auto=args.auto)
    elif args.interactive:
        tool.interactive_restore(filepath)
    else:
        print("ERROR: Specify --latest or --interactive")
        sys.exit(1)


if __name__ == '__main__':
    main()
