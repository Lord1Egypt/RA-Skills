#!/usr/bin/env python3
"""
Setup script for PDF Organizer
Creates necessary directories and helps with initial configuration
"""

import json
import os
from pathlib import Path


def main():
    print("=" * 60)
    print("PDF Organizer - Setup")
    print("=" * 60)
    print()

    # Create directories
    print("Creating directories...")
    directories = [
        'input_pdfs',
        'organized_pdfs',
        'modules',
        'examples'
    ]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  [OK] {directory}/")

    # Check config
    print("\nChecking configuration...")
    config_path = Path('config.json')

    if not config_path.exists():
        print("  [X] config.json not found")
        print("  Creating config.json from template...")
        template = {
            "openai_api_key": "your-api-key-here",
            "input_folder": "./input_pdfs",
            "output_folder": "./organized_pdfs",
            "model": "gpt-3.5-turbo",
            "dry_run": False,
            "incremental": True,
            "max_chars": 10000,
            "custom_topics": {
                "Artificial Intelligence": "Technology",
                "Machine Learning": "Technology",
                "Investment": "Finance"
            }
        }

        with open(config_path, 'w') as f:
            json.dump(template, f, indent=2)
        print("  [OK] config.json created")
    else:
        print("  [OK] config.json found")

        # Check if API key is set
        with open(config_path, 'r') as f:
            config = json.load(f)
            api_key = config.get('openai_api_key', '')

            if not api_key or api_key in ['your-api-key-here', 'your-api-key']:
                print("\n  [!] Warning: OpenAI API key not set!")
                print("  Please edit config.json and set your API key")
            else:
                print("  [OK] API key is configured")

    # Install dependencies
    print("\nChecking dependencies...")
    requirements_path = Path('requirements.txt')

    if requirements_path.exists():
        print("  To install dependencies, run:")
        print("    pip install -r requirements.txt")
    else:
        print("  [X] requirements.txt not found")

    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit config.json and set your OpenAI API key")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Place PDF files in the input_pdfs/ folder")
    print("4. Run: python pdf_organizer.py")
    print("\nFor dry-run mode (preview without moving files):")
    print("  python pdf_organizer.py --dry-run")
    print()


if __name__ == '__main__':
    main()
