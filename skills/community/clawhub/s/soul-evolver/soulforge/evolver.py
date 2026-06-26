"""
SoulForge SoulEvolver
Safely updates workspace files with discovered patterns.
"""

import os
import re
import logging
import shutil
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Any

from soulforge.analyzer import DiscoveredPattern

logger = logging.getLogger(__name__)


class SoulEvolver:
    """
    Safely evolves workspace files by applying discovered patterns.

    Safety features:
    - Incremental updates (appends, never overwrites)
    - Backup before write
    - Provenance tracking
    - Dry-run mode
    """

    def __init__(self, workspace: str, config):
        """
        Initialize the evolver.

        Args:
            workspace: Path to workspace directory
            config: SoulForgeConfig instance
        """
        self.workspace = Path(workspace)
        self.config = config
        self._changes_made: List[Dict] = []

    def apply_updates(
        self,
        patterns: List[DiscoveredPattern],
        dry_run: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Apply discovered patterns to target files.

        Args:
            patterns: List of DiscoveredPattern objects to apply
            dry_run: If True, don't actually write (default from config)

        Returns:
            Dict with results summary
        """
        if dry_run is None:
            dry_run = self.config.is_dry_run

        self._changes_made = []
        results = {
            "dry_run": dry_run,
            "patterns_attempted": len(patterns),
            "patterns_applied": 0,
            "patterns_skipped": 0,
            "errors": [],
            "files_updated": [],
        }

        # Group patterns by target file
        by_file: Dict[str, List[DiscoveredPattern]] = {}
        for pattern in patterns:
            target = pattern.target_file
            if target not in by_file:
                by_file[target] = []
            by_file[target].append(pattern)

        # Process each target file
        for filename, file_patterns in by_file.items():
            try:
                result = self._apply_to_file(filename, file_patterns, dry_run)
                if result["applied"] > 0:
                    results["files_updated"].append(filename)
                    results["patterns_applied"] += result["applied"]
                results["patterns_skipped"] += result["skipped"]
                if result.get("error"):
                    results["errors"].append({filename: result["error"]})
            except Exception as e:
                logger.error(f"Failed to update {filename}: {e}")
                results["errors"].append({filename: str(e)})

        results["changes"] = self._changes_made
        return results

    def _apply_to_file(
        self,
        filename: str,
        patterns: List[DiscoveredPattern],
        dry_run: bool
    ) -> Dict[str, Any]:
        """
        Apply patterns to a single file.

        Args:
            filename: Target file name (relative to workspace)
            patterns: Patterns to apply
            dry_run: Whether to actually write

        Returns:
            Dict with applied/skipped counts and any error
        """
        file_path = self.workspace / filename
        result = {"applied": 0, "skipped": 0, "error": None}

        # Load existing content
        if file_path.exists():
            existing_content = file_path.read_text(encoding="utf-8")
        else:
            existing_content = ""
            # Create empty file with basic structure
            file_path.parent.mkdir(parents=True, exist_ok=True)
            logger.info(f"File doesn't exist, will create: {filename}")

        # Check for duplicates
        patterns_to_apply = self._filter_duplicates(patterns, existing_content)

        if not patterns_to_apply:
            result["skipped"] = len(patterns)
            logger.info(f"All patterns already exist in {filename}, skipping")
            return result

        # Create backup
        if not dry_run and self.config.get("backup_enabled", True):
            self._create_backup(file_path)

        # Apply each pattern
        for pattern in patterns_to_apply:
            update_block = pattern.to_markdown_block()

            if dry_run:
                logger.info(f"[DRY RUN] Would add to {filename}: {pattern.summary}")
                result["applied"] += 1
                self._changes_made.append({
                    "file": filename,
                    "action": "would_add",
                    "pattern": pattern.summary,
                    "content_preview": pattern.content[:100],
                })
            else:
                # Append to file
                try:
                    with open(file_path, "a", encoding="utf-8") as f:
                        f.write("\n" + update_block)

                    logger.info(f"Updated {filename}: {pattern.summary}")
                    result["applied"] += 1
                    self._changes_made.append({
                        "file": filename,
                        "action": "added",
                        "pattern": pattern.summary,
                    })
                except Exception as e:
                    result["error"] = str(e)
                    logger.error(f"Failed to write to {filename}: {e}")

        return result

    def _filter_duplicates(
        self,
        patterns: List[DiscoveredPattern],
        existing_content: str
    ) -> List[DiscoveredPattern]:
        """
        Filter out patterns that are already present in the file.

        Args:
            patterns: Patterns to check
            existing_content: Current file content

        Returns:
            Patterns that should be applied (not duplicates)
        """
        if not existing_content:
            return patterns

        filtered = []
        for pattern in patterns:
            # Check if similar content already exists
            content_snippet = pattern.content[:50].lower()
            summary_snippet = pattern.summary[:50].lower()

            # Look for the summary or content in existing file
            if content_snippet in existing_content.lower():
                logger.debug(f"Skipping duplicate pattern: {pattern.summary}")
                continue
            if summary_snippet in existing_content.lower():
                logger.debug(f"Skipping similar pattern: {pattern.summary}")
                continue

            # Check for SoulForge update blocks with same summary
            if re.search(
                rf"<!--\s*SoulForge.*-->\s*##\s*{re.escape(pattern.summary)}",
                existing_content,
                re.IGNORECASE
            ):
                logger.debug(f"Skipping already-updated pattern: {pattern.summary}")
                continue

            filtered.append(pattern)

        return filtered

    def _create_backup(self, file_path: Path) -> None:
        """
        Create a timestamped backup of the file.

        Args:
            file_path: Path to file to backup
        """
        if not file_path.exists():
            return

        backup_dir = Path(self.config.backup_dir)
        backup_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.name}.{timestamp}.bak"
        backup_path = backup_dir / backup_name

        shutil.copy2(file_path, backup_path)
        logger.info(f"Backup created: {backup_path}")

        # Clean up old backups (keep last 10)
        self._cleanup_old_backups(backup_dir, file_path.name, keep=10)

    def _cleanup_old_backups(self, backup_dir: Path, original_name: str, keep: int = 10) -> None:
        """Remove old backups, keeping only the most recent N."""
        backups = sorted(
            backup_dir.glob(f"{original_name}.*.bak"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        for old_backup in backups[keep:]:
            old_backup.unlink()
            logger.debug(f"Removed old backup: {old_backup}")

    def get_backup_list(self, filename: str) -> List[Dict[str, str]]:
        """
        Get list of backups for a file.

        Args:
            filename: Original file name

        Returns:
            List of dicts with path and timestamp
        """
        backup_dir = Path(self.config.backup_dir)
        if not backup_dir.exists():
            return []

        backups = sorted(
            backup_dir.glob(f"{filename}.*.bak"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        return [
            {
                "path": str(b),
                "timestamp": datetime.fromtimestamp(b.stat().st_mtime).isoformat(),
            }
            for b in backups
        ]

    def restore_from_backup(self, filename: str, backup_path: str) -> bool:
        """
        Restore a file from backup.

        Args:
            filename: Target file name
            backup_path: Path to backup file

        Returns:
            True if successful
        """
        try:
            backup = Path(backup_path)
            target = self.workspace / filename

            if not backup.exists():
                logger.error(f"Backup not found: {backup_path}")
                return False

            # Create backup of current file before restoring
            if target.exists():
                self._create_backup(target)

            shutil.copy2(backup, target)
            logger.info(f"Restored {filename} from {backup_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore: {e}")
            return False

    def summarize_changes(self) -> str:
        """Generate a human-readable summary of changes made."""
        if not self._changes_made:
            return "No changes made."

        lines = ["SoulForge Update Summary:", ""]
        by_file: Dict[str, List] = {}
        for change in self._changes_made:
            f = change["file"]
            if f not in by_file:
                by_file[f] = []
            by_file[f].append(change)

        for filename, changes in by_file.items():
            lines.append(f"  {filename}:")
            for c in changes:
                action = "Added" if c["action"] == "added" else c["action"]
                lines.append(f"    - {action}: {c['pattern']}")
            lines.append("")

        return "\n".join(lines)
