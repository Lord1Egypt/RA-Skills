#!/usr/bin/env python3
"""
Sentinel — AI Agent State Guardian
Automated backup, integrity monitoring, and self-healing for AI agent workspaces.

Author: Shadow Rose
License: MIT
"""

import os
import sys
import json
import hashlib
import shutil
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple

# Import config
try:
    import sentinel_config as config
except ImportError:
    print("ERROR: sentinel_config.py not found. Copy config_example.py to sentinel_config.py and configure it.")
    sys.exit(1)


class SentinelLogger:
    """Centralized logging with configurable outputs."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.logger = logging.getLogger("Sentinel")
        self.logger.setLevel(logging.DEBUG if config_obj.DEBUG else logging.INFO)
        
        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
        self.logger.addHandler(console)
        
        # File handler if configured
        if config_obj.LOG_FILE:
            try:
                file_handler = logging.FileHandler(config_obj.LOG_FILE)
                file_handler.setLevel(logging.DEBUG)
                file_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.warning(f"Could not create log file: {e}")
    
    def info(self, msg): self.logger.info(msg)
    def warning(self, msg): self.logger.warning(msg)
    def error(self, msg): self.logger.error(msg)
    def debug(self, msg): self.logger.debug(msg)
    
    def alert(self, level: str, message: str):
        """Send alert via configured channels."""
        alert_msg = f"[{level.upper()}] {message}"
        
        if level in ['CRITICAL', 'ERROR']:
            self.logger.error(alert_msg)
        elif level == 'WARNING':
            self.logger.warning(alert_msg)
        else:
            self.logger.info(alert_msg)
        
        # Write to alert file if configured
        if self.config.ALERT_FILE:
            try:
                with open(self.config.ALERT_FILE, 'a') as f:
                    f.write(f"{datetime.now().isoformat()} {alert_msg}\n")
            except Exception as e:
                self.logger.error(f"Failed to write alert file: {e}")


class FileHasher:
    """Compute and verify file hashes."""
    
    @staticmethod
    def hash_file(filepath: Path) -> Optional[str]:
        """Compute SHA-256 hash of a file."""
        try:
            sha256 = hashlib.sha256()
            with open(filepath, 'rb') as f:
                while chunk := f.read(8192):
                    sha256.update(chunk)
            return sha256.hexdigest()
        except Exception as e:
            return None
    
    @staticmethod
    def hash_matches(filepath: Path, expected_hash: str) -> bool:
        """Verify file hash matches expected value."""
        actual = FileHasher.hash_file(filepath)
        return actual == expected_hash if actual else False


class ProcessDetector:
    """Detect running processes and their open files."""
    
    @staticmethod
    def is_file_in_use(filepath: Path) -> bool:
        """Check if file is currently in use by a process."""
        try:
            # Try to rename to itself (will fail if file is locked on Windows)
            if os.name == 'nt':
                try:
                    os.rename(filepath, filepath)
                    return False
                except OSError:
                    return True
            else:
                # On Unix, check if we can get exclusive access
                try:
                    with open(filepath, 'r+b') as f:
                        import fcntl
                        fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
                    return False
                except (IOError, OSError, ImportError):
                    # If fcntl not available or file is locked, assume in use
                    return True
        except Exception:
            # If we can't determine, assume it's in use (safer)
            return True


class StateManifest:
    """Manage file state manifests."""
    
    def __init__(self, manifest_file: Path):
        self.manifest_file = manifest_file
        self.manifest: Dict[str, Dict] = {}
    
    def load(self) -> bool:
        """Load manifest from disk."""
        try:
            if self.manifest_file.exists():
                with open(self.manifest_file, 'r') as f:
                    self.manifest = json.load(f)
                return True
        except Exception:
            pass
        return False
    
    def save(self) -> bool:
        """Save manifest to disk."""
        try:
            self.manifest_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.manifest_file, 'w') as f:
                json.dump(self.manifest, f, indent=2)
            return True
        except Exception:
            return False
    
    def update_file(self, filepath: Path, file_hash: str, size: int, mtime: float):
        """Update manifest entry for a file."""
        key = str(filepath)
        self.manifest[key] = {
            'hash': file_hash,
            'size': size,
            'mtime': mtime,
            'last_checked': time.time()
        }
    
    def get_file_state(self, filepath: Path) -> Optional[Dict]:
        """Get stored state for a file."""
        return self.manifest.get(str(filepath))
    
    def remove_file(self, filepath: Path):
        """Remove file from manifest."""
        key = str(filepath)
        if key in self.manifest:
            del self.manifest[key]


class BackupManager:
    """Handle file backups."""
    
    def __init__(self, backup_root: Path, logger: SentinelLogger):
        self.backup_root = backup_root
        self.logger = logger
    
    def backup_file(self, filepath: Path, workspace_root: Path) -> Optional[Path]:
        """Create timestamped backup of a file."""
        try:
            # Create backup path preserving directory structure
            rel_path = filepath.relative_to(workspace_root)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_root / timestamp / rel_path
            
            # Create parent directories
            backup_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file
            shutil.copy2(filepath, backup_path)
            self.logger.debug(f"Backed up: {filepath} -> {backup_path}")
            return backup_path
        except Exception as e:
            self.logger.error(f"Backup failed for {filepath}: {e}")
            return None
    
    def get_latest_backup(self, filepath: Path, workspace_root: Path) -> Optional[Path]:
        """Find most recent backup of a file."""
        try:
            rel_path = filepath.relative_to(workspace_root)
            
            # Find all timestamped backup directories
            backup_dirs = sorted([d for d in self.backup_root.iterdir() if d.is_dir()], reverse=True)
            
            for backup_dir in backup_dirs:
                candidate = backup_dir / rel_path
                if candidate.exists():
                    return candidate
            
            return None
        except Exception:
            return None


class IntegrityChecker:
    """Verify file integrity."""
    
    def __init__(self, logger: SentinelLogger):
        self.logger = logger
    
    def check_file(self, filepath: Path, expected_state: Dict) -> Tuple[bool, List[str]]:
        """Check file integrity against expected state."""
        issues = []
        
        try:
            if not filepath.exists():
                issues.append("File does not exist")
                return False, issues
            
            # Check if empty
            stat = filepath.stat()
            if stat.st_size == 0:
                issues.append("File is empty (0 bytes)")
            
            # Check size change
            if 'size' in expected_state:
                expected_size = expected_state['size']
                if stat.st_size != expected_size:
                    issues.append(f"Size mismatch: expected {expected_size}, got {stat.st_size}")
            
            # Check hash
            if 'hash' in expected_state:
                expected_hash = expected_state['hash']
                actual_hash = FileHasher.hash_file(filepath)
                if actual_hash != expected_hash:
                    issues.append(f"Hash mismatch: file modified unexpectedly")
            
            return len(issues) == 0, issues
        
        except Exception as e:
            issues.append(f"Check failed: {e}")
            return False, issues


class Sentinel:
    """Main Sentinel monitoring and backup engine."""
    
    def __init__(self, config_obj):
        self.config = config_obj
        self.logger = SentinelLogger(config_obj)
        self.workspace = Path(config_obj.WORKSPACE_ROOT).resolve()
        self.backup_manager = BackupManager(Path(config_obj.BACKUP_DIR), self.logger)
        self.integrity_checker = IntegrityChecker(self.logger)
        self.manifest = StateManifest(Path(config_obj.STATE_FILE))
        
        # Load existing manifest
        self.manifest.load()
    
    def scan_critical_files(self) -> List[Path]:
        """Discover all critical files to monitor."""
        critical_files = []
        
        for pattern in self.config.CRITICAL_FILES:
            if '*' in pattern or '?' in pattern:
                # Glob pattern
                try:
                    matches = list(self.workspace.glob(pattern))
                    critical_files.extend(matches)
                except Exception as e:
                    self.logger.warning(f"Failed to glob pattern {pattern}: {e}")
            else:
                # Exact path
                filepath = self.workspace / pattern
                if filepath.exists():
                    critical_files.append(filepath)
        
        return list(set(critical_files))  # Remove duplicates
    
    def monitor_file(self, filepath: Path) -> bool:
        """Monitor a single file for changes and integrity."""
        try:
            # Skip if file is in use
            if ProcessDetector.is_file_in_use(filepath):
                self.logger.debug(f"Skipping {filepath}: file in use")
                return True
            
            # Get current state
            stat = filepath.stat()
            current_hash = FileHasher.hash_file(filepath)
            if current_hash is None:
                self.logger.warning(f"Could not hash {filepath}")
                return False
            
            # Get previous state
            previous_state = self.manifest.get_file_state(filepath)
            
            if previous_state is None:
                # First time seeing this file
                self.logger.info(f"New file tracked: {filepath}")
                self.manifest.update_file(filepath, current_hash, stat.st_size, stat.st_mtime)
                self.backup_manager.backup_file(filepath, self.workspace)
            else:
                # Check for changes
                if current_hash != previous_state['hash']:
                    self.logger.info(f"Change detected: {filepath}")
                    
                    # Create backup before updating manifest
                    backup_path = self.backup_manager.backup_file(filepath, self.workspace)
                    if backup_path:
                        self.logger.info(f"Backup created: {backup_path}")
                    
                    # Update manifest
                    self.manifest.update_file(filepath, current_hash, stat.st_size, stat.st_mtime)
                    
                    self.logger.alert('INFO', f"File changed: {filepath}")
            
            # Check integrity
            is_ok, issues = self.integrity_checker.check_file(filepath, previous_state or {})
            if not is_ok:
                self.logger.warning(f"Integrity issues in {filepath}: {', '.join(issues)}")
                self.logger.alert('WARNING', f"Integrity issue: {filepath} - {', '.join(issues)}")
                
                # Auto-restore if configured and file is corrupted
                if self.config.AUTO_RESTORE_ON_CORRUPTION and 'empty' in ' '.join(issues).lower():
                    self.attempt_restore(filepath)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Monitor failed for {filepath}: {e}")
            return False
    
    def attempt_restore(self, filepath: Path) -> bool:
        """Attempt to restore file from backup."""
        try:
            self.logger.info(f"Attempting auto-restore: {filepath}")
            
            # Find latest backup
            backup_path = self.backup_manager.get_latest_backup(filepath, self.workspace)
            if backup_path is None:
                self.logger.error(f"No backup found for {filepath}")
                self.logger.alert('ERROR', f"Auto-restore failed: no backup for {filepath}")
                return False
            
            # Verify backup is not empty
            if backup_path.stat().st_size == 0:
                self.logger.error(f"Backup is empty: {backup_path}")
                return False
            
            # Restore
            shutil.copy2(backup_path, filepath)
            self.logger.info(f"Restored from backup: {backup_path} -> {filepath}")
            self.logger.alert('INFO', f"Auto-restored {filepath} from {backup_path}")
            
            # Update manifest
            stat = filepath.stat()
            new_hash = FileHasher.hash_file(filepath)
            self.manifest.update_file(filepath, new_hash, stat.st_size, stat.st_mtime)
            
            return True
        
        except Exception as e:
            self.logger.error(f"Restore failed for {filepath}: {e}")
            self.logger.alert('ERROR', f"Auto-restore failed for {filepath}: {e}")
            return False
    
    def run_once(self):
        """Run one monitoring cycle."""
        self.logger.info("=== Sentinel monitoring cycle started ===")
        
        critical_files = self.scan_critical_files()
        self.logger.info(f"Monitoring {len(critical_files)} critical files")
        
        success_count = 0
        failure_count = 0
        
        for filepath in critical_files:
            if self.monitor_file(filepath):
                success_count += 1
            else:
                failure_count += 1
        
        # Save manifest
        if self.manifest.save():
            self.logger.debug("State manifest saved")
        else:
            self.logger.error("Failed to save state manifest")
        
        self.logger.info(f"=== Cycle complete: {success_count} ok, {failure_count} failed ===")
    
    def run_continuous(self):
        """Run continuous monitoring loop."""
        self.logger.info("Sentinel starting in continuous mode")
        self.logger.info(f"Check interval: {self.config.CHECK_INTERVAL_SECONDS}s")
        
        try:
            while True:
                self.run_once()
                time.sleep(self.config.CHECK_INTERVAL_SECONDS)
        except KeyboardInterrupt:
            self.logger.info("Sentinel stopped by user")


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Sentinel — AI Agent State Guardian")
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--continuous', action='store_true', help='Run continuous monitoring')
    parser.add_argument('--status', action='store_true', help='Show current status')
    
    args = parser.parse_args()
    
    sentinel = Sentinel(config)
    
    if args.status:
        print(f"Workspace: {sentinel.workspace}")
        print(f"Backup dir: {sentinel.backup_manager.backup_root}")
        print(f"State file: {sentinel.manifest.manifest_file}")
        print(f"Tracked files: {len(sentinel.manifest.manifest)}")
        return
    
    if args.continuous:
        sentinel.run_continuous()
    else:
        sentinel.run_once()


if __name__ == '__main__':
    main()
