"""
Folder Manager Module
Manages folder creation and organization structure
"""

import json
from pathlib import Path
from typing import Dict, List, Set, Optional


class FolderManager:
    """Manages folder creation and organization"""

    def __init__(self, output_folder: Path, dry_run: bool = False):
        """
        Initialize folder manager

        Args:
            output_folder: Root folder for organized PDFs
            dry_run: If True, don't actually create folders
        """
        self.output_folder = Path(output_folder)
        self.dry_run = dry_run
        self.created_folders: Set[Path] = set()

        # Load existing folder cache if available
        self.folder_cache: Dict[str, Path] = {}
        self._load_folder_cache()

    def _load_folder_cache(self):
        """Load existing folder structure into cache"""
        cache_file = self.output_folder / '.folder_cache.json'

        if cache_file.exists():
            try:
                with open(cache_file, 'r') as f:
                    self.folder_cache = json.load(f)
            except Exception:
                self.folder_cache = {}

        # Also scan existing folders
        if self.output_folder.exists():
            for folder in self.output_folder.iterdir():
                if folder.is_dir():
                    topic_name = folder.name
                    self.folder_cache[topic_name] = folder

    def _save_folder_cache(self):
        """Save folder cache to disk"""
        if not self.dry_run:
            cache_file = self.output_folder / '.folder_cache.json'

            try:
                # Convert Path objects to strings for JSON serialization
                cache_dict = {
                    topic: str(path)
                    for topic, path in self.folder_cache.items()
                }

                with open(cache_file, 'w') as f:
                    json.dump(cache_dict, f, indent=2)

            except Exception as e:
                print(f"Warning: Could not save folder cache: {e}")

    def normalize_topic_name(self, topic: str) -> str:
        """
        Normalize topic name to be folder-safe

        Args:
            topic: Original topic name

        Returns:
            Normalized topic name
        """
        # Remove special characters
        normalized = ''.join(
            c for c in topic
            if c.isalnum() or c in (' ', '-', '_')
        )

        # Replace spaces with underscores
        normalized = normalized.replace(' ', '_')

        # Remove multiple consecutive underscores
        while '__' in normalized:
            normalized = normalized.replace('__', '_')

        # Capitalize first letter
        normalized = normalized.capitalize()

        return normalized

    def get_or_create_topic_folder(self, topic: str) -> Path:
        """
        Get existing topic folder or create new one

        Args:
            topic: Topic name

        Returns:
            Path to topic folder
        """
        # Check cache first
        if topic in self.folder_cache:
            cached_path = Path(self.folder_cache[topic])
            if cached_path.exists():
                return cached_path

        # Normalize topic name
        folder_name = self.normalize_topic_name(topic)
        folder_path = self.output_folder / folder_name

        # Create folder if it doesn't exist
        if not folder_path.exists() and not self.dry_run:
            folder_path.mkdir(parents=True, exist_ok=True)
            self.created_folders.add(folder_path)
            print(f"Created folder: {folder_path}")

        # Update cache
        self.folder_cache[topic] = folder_path

        return folder_path

    def create_subtopic_folder(
        self,
        topic: str,
        subtopic: str
    ) -> Optional[Path]:
        """
        Create subtopic folder within topic folder

        Args:
            topic: Main topic
            subtopic: Subtopic name

        Returns:
            Path to subtopic folder, or None if not created
        """
        topic_folder = self.get_or_create_topic_folder(topic)

        # Normalize subtopic name
        subfolder_name = self.normalize_topic_name(subtopic)
        subfolder_path = topic_folder / subfolder_name

        # Create folder if it doesn't exist
        if not subfolder_path.exists() and not self.dry_run:
            subfolder_path.mkdir(parents=True, exist_ok=True)
            self.created_folders.add(subfolder_path)
            print(f"Created subfolder: {subfolder_path}")
            return subfolder_path

        return subfolder_path if subfolder_path.exists() else None

    def get_folder_for_pdf(self, analysis: Dict[str, any]) -> Path:
        """
        Get the appropriate folder for a PDF based on its analysis

        Args:
            analysis: Analysis result from ContentAnalyzer

        Returns:
            Path to destination folder
        """
        topic = analysis.get('topic', 'Other')
        subtopics = analysis.get('subtopics', [])

        # If there are subtopics, create a subfolder
        if subtopics:
            # Use the first subtopic
            subtopic_folder = self.create_subtopic_folder(topic, subtopics[0])
            if subtopic_folder:
                return subtopic_folder

        # Otherwise, use the main topic folder
        return self.get_or_create_topic_folder(topic)

    def organize_by_topic(
        self,
        pdf_analyses: List[tuple]
    ) -> Dict[str, Path]:
        """
        Organize PDFs by topic

        Args:
            pdf_analyses: List of (pdf_path, analysis) tuples

        Returns:
            Dictionary mapping pdf_path to destination folder
        """
        organization_map = {}

        for pdf_path, analysis in pdf_analyses:
            destination = self.get_folder_for_pdf(analysis)
            organization_map[str(pdf_path)] = destination

        # Save cache
        self._save_folder_cache()

        return organization_map

    def get_all_folders(self) -> List[Path]:
        """
        Get all topic folders

        Returns:
            List of folder paths
        """
        if not self.output_folder.exists():
            return []

        folders = []
        for item in self.output_folder.iterdir():
            if item.is_dir():
                folders.append(item)

        return folders

    def get_folder_stats(self) -> Dict[str, any]:
        """
        Get statistics about folder structure

        Returns:
            Dictionary with folder statistics
        """
        stats = {
            'total_folders': len(self.get_all_folders()),
            'created_this_session': len(self.created_folders),
            'folders': {}
        }

        for folder in self.get_all_folders():
            # Count files in folder
            file_count = sum(1 for _ in folder.glob('*.pdf'))
            stats['folders'][folder.name] = {
                'path': str(folder),
                'file_count': file_count
            }

        return stats

    def cleanup_empty_folders(self):
        """Remove empty folders"""
        if self.dry_run:
            return

        for folder in self.get_all_folders():
            # Check if folder is empty (no PDFs)
            pdf_files = list(folder.glob('*.pdf'))
            subfolders = [d for d in folder.iterdir() if d.is_dir()]

            if not pdf_files and not subfolders:
                try:
                    folder.rmdir()
                    print(f"Removed empty folder: {folder}")

                    # Remove from cache
                    topic_name = folder.name
                    if topic_name in self.folder_cache:
                        del self.folder_cache[topic_name]

                except Exception as e:
                    print(f"Could not remove folder {folder}: {e}")

        self._save_folder_cache()
