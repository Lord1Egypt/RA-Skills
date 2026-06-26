#!/usr/bin/env python3
"""
PDF Organizer - Main Entry Point
Organizes PDF files by topic using AI analysis
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

# Import modules
from modules.pdf_reader import PDFReader
from modules.content_analyzer import ContentAnalyzer
from modules.folder_manager import FolderManager
from modules.file_mover import FileMover


class PDFOrganizer:
    """Main PDF organizer class"""

    def __init__(self, config_path: str = "config.json"):
        """
        Initialize PDF organizer

        Args:
            config_path: Path to configuration file
        """
        self.config = self._load_config(config_path)

        # Validate configuration
        self._validate_config()

        # Initialize components
        self.pdf_reader = PDFReader(
            max_chars=self.config.get('max_chars', 10000)
        )

        self.content_analyzer = ContentAnalyzer(
            api_key=self.config['openai_api_key'],
            model=self.config.get('model', 'gpt-3.5-turbo'),
            api_provider=self.config.get('api_provider', 'openai')
        )

        # Set custom topic mappings if provided
        if 'custom_topics' in self.config:
            self.content_analyzer.set_custom_topic_mappings(
                self.config['custom_topics']
            )

        self.folder_manager = FolderManager(
            output_folder=Path(self.config['output_folder']),
            dry_run=self.config.get('dry_run', False)
        )

        self.file_mover = FileMover(
            dry_run=self.config.get('dry_run', False)
        )

        # Processing statistics
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'failed': 0,
            'skipped': 0,
            'topics': {},
            'start_time': None,
            'end_time': None
        }

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            print(f"Configuration loaded from: {config_path}")
            return config
        except FileNotFoundError:
            print(f"Error: Configuration file not found: {config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            sys.exit(1)

    def _validate_config(self):
        """Validate required configuration fields"""
        required_fields = ['openai_api_key', 'input_folder', 'output_folder']

        for field in required_fields:
            if field not in self.config:
                print(f"Error: Missing required configuration field: {field}")
                sys.exit(1)

        # Check if API key is set
        if not self.config['openai_api_key'] or self.config['openai_api_key'] == 'your-api-key-here':
            print("Error: Please set your API key in config.json")
            sys.exit(1)

        # Create input folder if it doesn't exist
        input_folder = Path(self.config['input_folder'])
        if not input_folder.exists():
            print(f"Creating input folder: {input_folder}")
            input_folder.mkdir(parents=True, exist_ok=True)

        # Create output folder if it doesn't exist
        output_folder = Path(self.config['output_folder'])
        if not output_folder.exists():
            print(f"Creating output folder: {output_folder}")
            output_folder.mkdir(parents=True, exist_ok=True)

    def get_pdf_files(self) -> List[Path]:
        """
        Get list of PDF files to process

        Returns:
            List of PDF file paths
        """
        input_folder = Path(self.config['input_folder'])
        pdf_files = list(input_folder.glob('*.pdf'))

        # Filter by incremental mode if enabled
        if self.config.get('incremental', False):
            pdf_files = self._filter_incremental(pdf_files)

        return sorted(pdf_files)

    def _filter_incremental(self, pdf_files: List[Path]) -> List[Path]:
        """
        Filter files for incremental processing

        Args:
            pdf_files: List of all PDF files

        Returns:
            List of files to process (new/modified only)
        """
        # Check for processed files log
        log_file = Path(self.config['output_folder']) / '.processed_files.json'

        processed_files = set()
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    processed = json.load(f)
                    processed_files = set(processed.get('files', []))
            except Exception:
                pass

        # Filter files
        filtered_files = []
        for pdf_file in pdf_files:
            file_str = str(pdf_file)
            if file_str not in processed_files:
                filtered_files.append(pdf_file)

        print(f"Incremental mode: Processing {len(filtered_files)} of {len(pdf_files)} files")

        return filtered_files

    def process_pdf(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Process a single PDF file

        Args:
            pdf_path: Path to PDF file

        Returns:
            Processing result
        """
        try:
            # Read PDF
            text_content, metadata = self.pdf_reader.read_pdf(pdf_path)

            # Analyze content
            analysis = self.content_analyzer.analyze_content(text_content, metadata)

            # Get destination folder
            destination = self.folder_manager.get_folder_for_pdf(analysis)

            # Prepare result
            result = {
                'pdf_path': str(pdf_path),
                'title': analysis['title'],
                'author': analysis['author'],
                'journal': analysis['journal'],
                'topic': analysis['topic'],
                'subtopics': analysis['subtopics'],
                'destination': str(destination),
                'confidence': analysis.get('confidence', 0.0),
                'success': True
            }

            return result

        except Exception as e:
            print(f"Error processing {pdf_path.name}: {str(e)}")
            return {
                'pdf_path': str(pdf_path),
                'error': str(e),
                'success': False
            }

    def run(self):
        """Run the PDF organizer"""
        print("\n" + "=" * 60)
        print("PDF Organizer - Starting")
        print("=" * 60 + "\n")

        self.stats['start_time'] = datetime.now()

        # Get PDF files
        pdf_files = self.get_pdf_files()
        self.stats['total_files'] = len(pdf_files)

        if not pdf_files:
            print("No PDF files found in input folder.")
            return

        print(f"Found {len(pdf_files)} PDF file(s) to process\n")

        # Process each PDF
        results = []
        for i, pdf_file in enumerate(pdf_files, 1):
            print(f"[{i}/{len(pdf_files)}] Processing: {pdf_file.name}")

            # Check if file is readable
            if not self.pdf_reader.can_read(pdf_file):
                print(f"  Skipping: Cannot read PDF file")
                self.stats['skipped'] += 1
                continue

            # Process PDF
            result = self.process_pdf(pdf_file)

            if result['success']:
                print(f"  Title: {result['title']}")
                print(f"  Author: {result['author']}")
                print(f"  Journal: {result['journal']}")
                print(f"  Topic: {result['topic']}")
                if result['subtopics']:
                    print(f"  Subtopics: {', '.join(result['subtopics'])}")
                print(f"  Destination: {Path(result['destination']).parent.name}")

                # Update topic statistics
                topic = result['topic']
                if topic not in self.stats['topics']:
                    self.stats['topics'][topic] = 0
                self.stats['topics'][topic] += 1

                self.stats['processed'] += 1

            else:
                print(f"  Error: {result.get('error', 'Unknown error')}")
                self.stats['failed'] += 1

            results.append(result)
            print()

        # Move files if not in dry run mode
        if not self.config.get('dry_run', False) and results:
            print("\nMoving files with enhanced naming...")

            # Prepare PDF analyses with results
            pdf_analyses = [
                (Path(result['pdf_path']), result)
                for result in results
                if result['success']
            ]

            move_results = self.file_mover.move_files_with_analysis(pdf_analyses)

            # Log processed files for incremental mode
            if self.config.get('incremental', False):
                self._save_processed_files(results)

        # Finalize
        self.stats['end_time'] = datetime.now()
        self._print_summary(results)

        # Export move log
        if not self.config.get('dry_run', False):
            log_file = Path(self.config['output_folder']) / 'move_log.json'
            self.file_mover.export_log(log_file)

    def _save_processed_files(self, results: List[Dict[str, Any]]):
        """Save list of processed files for incremental mode"""
        log_file = Path(self.config['output_folder']) / '.processed_files.json'

        # Load existing processed files
        processed_files = []
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    data = json.load(f)
                    processed_files = data.get('files', [])
            except Exception:
                pass

        # Add newly processed files
        new_files = [
            result['pdf_path']
            for result in results
            if result['success']
        ]

        processed_files.extend(new_files)

        # Save
        try:
            with open(log_file, 'w') as f:
                json.dump({'files': processed_files}, f)
        except Exception as e:
            print(f"Warning: Could not save processed files log: {e}")

    def _print_summary(self, results: List[Dict[str, Any]]):
        """Print processing summary"""
        print("\n" + "=" * 60)
        print("Processing Summary")
        print("=" * 60 + "\n")

        # Statistics
        duration = (self.stats['end_time'] - self.stats['start_time']).total_seconds()
        print(f"Total files: {self.stats['total_files']}")
        print(f"Processed: {self.stats['processed']}")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Duration: {duration:.1f} seconds\n")

        # Topics
        if self.stats['topics']:
            print("Topics found:")
            for topic, count in sorted(
                self.stats['topics'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                print(f"  {topic}: {count} file(s)")
            print()

        # Move summary
        if not self.config.get('dry_run', False):
            move_summary = self.file_mover.get_move_summary()
            print(f"Files moved: {move_summary['successful']}")
            print(f"Failed moves: {move_summary['failed']}")
        else:
            print("DRY RUN: No files were actually moved")

        print("\n" + "=" * 60 + "\n")


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Organize PDF files by topic using AI analysis'
    )
    parser.add_argument(
        '--config',
        default='config.json',
        help='Path to configuration file (default: config.json)'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without moving files'
    )

    args = parser.parse_args()

    # Create organizer
    organizer = PDFOrganizer(config_path=args.config)

    # Override dry-run if specified
    if args.dry_run:
        organizer.config['dry_run'] = True
        organizer.folder_manager.dry_run = True
        organizer.file_mover.dry_run = True
        print("DRY RUN MODE: No files will be moved\n")

    # Run organizer
    organizer.run()


if __name__ == '__main__':
    main()
