"""
File Mover Module
Handles moving PDF files to their organized folders
"""

import shutil
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class FileMover:
    """Handles moving PDF files to organized folders"""

    def __init__(self, dry_run: bool = False):
        """
        Initialize file mover

        Args:
            dry_run: If True, don't actually move files
        """
        self.dry_run = dry_run
        self.move_log: List[Dict[str, any]] = []

    def move_file(
        self,
        source: Path,
        destination: Path,
        new_name: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Move a file from source to destination

        Args:
            source: Source file path
            destination: Destination folder
            new_name: Optional new filename (without extension)

        Returns:
            Tuple of (success, message)
        """
        try:
            # Ensure source exists
            if not source.exists():
                return False, f"Source file does not exist: {source}"

            # Create destination filename
            if new_name:
                dest_name = f"{new_name}{source.suffix}"
            else:
                dest_name = source.name

            dest_path = destination / dest_name

            # Handle filename conflicts
            dest_path = self._resolve_conflict(dest_path)

            # Log the move operation
            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'source': str(source),
                'destination': str(dest_path),
                'original_name': source.name,
                'new_name': dest_path.name,
                'success': False
            }

            if not self.dry_run:
                # Move the file
                shutil.move(str(source), str(dest_path))
                log_entry['success'] = True
                print(f"Moved: {source.name} -> {dest_path.parent.name}/{dest_path.name}")
            else:
                print(f"[DRY RUN] Would move: {source.name} -> {dest_path.parent.name}/{dest_path.name}")

            self.move_log.append(log_entry)
            return True, "File moved successfully"

        except Exception as e:
            error_msg = f"Error moving file {source}: {str(e)}"
            print(error_msg)

            log_entry = {
                'timestamp': datetime.now().isoformat(),
                'source': str(source),
                'destination': str(dest_path) if 'dest_path' in locals() else 'unknown',
                'error': str(e),
                'success': False
            }
            self.move_log.append(log_entry)

            return False, error_msg

    def _resolve_conflict(self, dest_path: Path) -> Path:
        """
        Resolve filename conflicts by adding a suffix

        Args:
            dest_path: Original destination path

        Returns:
            Resolved path without conflict
        """
        if not dest_path.exists():
            return dest_path

        # File exists, add numeric suffix
        base_name = dest_path.stem
        extension = dest_path.suffix
        counter = 1

        while True:
            new_name = f"{base_name}_{counter}{extension}"
            new_path = dest_path.parent / new_name

            if not new_path.exists():
                return new_path

            counter += 1

    def move_files_batch(
        self,
        move_map: Dict[str, Path]
    ) -> Dict[str, Tuple[bool, str]]:
        """
        Move multiple files in batch

        Args:
            move_map: Dictionary mapping source path to destination folder

        Returns:
            Dictionary mapping source path to (success, message) tuple
        """
        results = {}

        for source_str, destination in move_map.items():
            source = Path(source_str)
            success, message = self.move_file(source, destination)
            results[source_str] = (success, message)

        return results

    def move_files_with_analysis(
        self,
        pdf_analyses: List[Tuple[Path, Dict[str, any]]]
    ) -> Dict[str, Tuple[bool, str]]:
        """
        Move files based on analysis results

        Args:
            pdf_analyses: List of (pdf_path, analysis) tuples

        Returns:
            Dictionary mapping source path to (success, message) tuple
        """
        results = {}

        for pdf_path, analysis in pdf_analyses:
            # Create a descriptive filename based on title, author, and journal
            title = analysis.get('title', 'Untitled')
            author = analysis.get('author', 'Unknown_Author')
            journal = analysis.get('journal', 'Unknown_Venue')

            # Create filename in format: Title_Author_Journal.pdf (using only underscores)
            # Only preserve hyphens in author names, not in titles
            title_sanitized = self._sanitize_filename(title, preserve_hyphens=False)
            author_sanitized = self._sanitize_filename(author, preserve_hyphens=True)
            journal_sanitized = self._sanitize_filename(journal, preserve_hyphens=False)

            filename_parts = [
                title_sanitized,
                author_sanitized,
                journal_sanitized
            ]

            # Filter out empty or placeholder values
            filename_parts = [part for part in filename_parts if part and
                            part not in ['Untitled', 'Unknown_Author', 'Unknown_Venue']]

            # Join parts with underscores and remove consecutive underscores
            new_name = '_'.join(filename_parts) if filename_parts else title_sanitized

            # Clean up consecutive underscores
            while '__' in new_name:
                new_name = new_name.replace('__', '_')

            # Remove leading/trailing underscores
            new_name = new_name.strip('_')

            # Move to destination (destination will be determined by FolderManager)
            # For this method, we need the destination folder
            if 'destination' in analysis:
                destination = Path(analysis['destination'])
                success, message = self.move_file(pdf_path, destination, new_name)
                results[str(pdf_path)] = (success, message)

        return results

    def _sanitize_filename(self, filename: str, preserve_hyphens: bool = False) -> str:
        """
        Sanitize a string to be used as a filename

        Args:
            filename: Original filename
            preserve_hyphens: If True, preserve hyphens within words (e.g., author names)

        Returns:
            Sanitized filename
        """
        # Remove or replace invalid characters
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '')

        # Replace multiple spaces with single space
        while '  ' in filename:
            filename = filename.replace('  ', ' ')

        # Replace spaces with underscores
        filename = filename.replace(' ', '_')

        # Remove hyphens unless we're preserving them for names
        if not preserve_hyphens:
            filename = filename.replace('-', '_')

        # Limit length
        max_length = 100
        if len(filename) > max_length:
            filename = filename[:max_length]

        # Remove leading/trailing underscores and dots
        filename = filename.strip('._')

        return filename if filename else 'Untitled'

    def get_move_summary(self) -> Dict[str, any]:
        """
        Get summary of move operations

        Returns:
            Dictionary with move statistics
        """
        successful = sum(1 for log in self.move_log if log.get('success', False))
        failed = len(self.move_log) - successful

        return {
            'total_moves': len(self.move_log),
            'successful': successful,
            'failed': failed,
            'dry_run': self.dry_run,
            'moves': self.move_log
        }

    def export_log(self, log_file: Path):
        """
        Export move log to a file

        Args:
            log_file: Path to log file
        """
        import json

        summary = self.get_move_summary()

        with open(log_file, 'w') as f:
            json.dump(summary, f, indent=2)

        print(f"Move log exported to: {log_file}")

    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate MD5 hash of a file

        Args:
            file_path: Path to file

        Returns:
            MD5 hash as hex string
        """
        hash_md5 = hashlib.md5()

        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)

        return hash_md5.hexdigest()

    def find_duplicates(
        self,
        pdf_files: List[Path]
    ) -> Dict[str, List[Path]]:
        """
        Find duplicate files based on hash

        Args:
            pdf_files: List of PDF files to check

        Returns:
            Dictionary mapping hash to list of duplicate file paths
        """
        hash_map = {}

        for pdf_file in pdf_files:
            try:
                file_hash = self.calculate_file_hash(pdf_file)

                if file_hash not in hash_map:
                    hash_map[file_hash] = []

                hash_map[file_hash].append(pdf_file)

            except Exception as e:
                print(f"Error calculating hash for {pdf_file}: {e}")

        # Filter out non-duplicates
        duplicates = {
            h: files
            for h, files in hash_map.items()
            if len(files) > 1
        }

        return duplicates
