#!/usr/bin/env python3
"""
Test File Manager for Skills-Coach

Automatically downloads or generates test files needed for skill testing.
"""

import os
import json
import urllib.request
from pathlib import Path
from typing import Dict, List, Optional


class TestFileManager:
    """Manages test files for skill testing."""

    # Public test files that can be downloaded
    TEST_FILE_URLS = {
        'pdf_simple': 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf',
        'pdf_form': 'https://www.irs.gov/pub/irs-pdf/fw9.pdf',  # IRS W-9 form (fillable)
        'pdf_multipage': 'https://www.africau.edu/images/default/sample.pdf',
        'image_png': 'https://www.w3.org/Graphics/PNG/alphatest.png',
        'image_jpg': 'https://www.w3.org/Graphics/JPEG/jfif3.jpg',
    }

    def __init__(self, workspace_dir: Path, prefer_local: bool = False):
        self.workspace_dir = workspace_dir
        self.workspace_dir.mkdir(parents=True, exist_ok=True)
        self.prefer_local = prefer_local  # If True, generate local files instead of downloading

    def prepare_files_for_command(self, command: str, script_path: str) -> Dict[str, str]:
        """
        Analyze command and prepare necessary test files.

        Returns:
            Dict mapping filename to file content (for text files) or file path (for binary files)
        """
        files = {}

        # Extract filenames from command
        import re
        # Find all .pdf, .json, .png, .jpg files mentioned in command
        pdf_files = re.findall(r'(\w+\.pdf)', command)
        json_files = re.findall(r'(\w+\.json)', command)
        png_files = re.findall(r'(\w+\.png)', command)
        jpg_files = re.findall(r'(\w+\.jpe?g)', command)

        # Analyze what files are needed based on command
        if 'fill_fillable_fields.py' in command or 'fillable' in command:
            # Need: input PDF (fillable form), fields JSON, output path
            if pdf_files:
                # Use the first PDF as input
                input_pdf = pdf_files[0]
                files[input_pdf] = self._download_or_get('pdf_form', input_pdf)
            if json_files:
                # Generate fields JSON with the actual filename
                fields_json = json_files[0]
                files[fields_json] = self._generate_pdf_fields_json(script_path, fields_json)
            # output.pdf will be created by the script

        elif 'convert_pdf_to_images' in command:
            # Need: input PDF
            if pdf_files:
                input_pdf = pdf_files[0]
                files[input_pdf] = self._download_or_get('pdf_simple', input_pdf)

        elif 'extract_form' in command:
            # Need: PDF with form
            if pdf_files:
                input_pdf = pdf_files[0]
                files[input_pdf] = self._download_or_get('pdf_form', input_pdf)

        elif 'extract' in command and 'pdf' in command.lower():
            # Need: any PDF
            if pdf_files:
                input_pdf = pdf_files[0]
                files[input_pdf] = self._download_or_get('pdf_simple', input_pdf)

        elif 'merge' in command or 'combine' in command:
            # Need: multiple PDFs
            if len(pdf_files) >= 2:
                files[pdf_files[0]] = self._download_or_get('pdf_simple', pdf_files[0])
                files[pdf_files[1]] = self._download_or_get('pdf_multipage', pdf_files[1])

        elif 'split' in command:
            # Need: multi-page PDF
            if pdf_files:
                input_pdf = pdf_files[0]
                files[input_pdf] = self._download_or_get('pdf_multipage', input_pdf)

        elif pdf_files:
            # Generic PDF operation - use first PDF mentioned
            input_pdf = pdf_files[0]
            files[input_pdf] = self._download_or_get('pdf_simple', input_pdf)

        # Handle image files
        for png_file in png_files:
            files[png_file] = self._download_or_get('image_png', png_file)
        for jpg_file in jpg_files:
            files[jpg_file] = self._download_or_get('image_jpg', jpg_file)

        return files

    def _download_or_get(self, file_key: str, target_filename: str = None) -> str:
        """Download test file if not exists, or generate locally if prefer_local is True."""
        if file_key not in self.TEST_FILE_URLS:
            return f"<{file_key}>"

        # Use target filename if provided, otherwise use default
        if target_filename:
            filename = target_filename
        else:
            # Determine filename from key
            ext_map = {
                'pdf_simple': 'simple.pdf',
                'pdf_form': 'form.pdf',
                'pdf_multipage': 'multipage.pdf',
                'image_png': 'test.png',
                'image_jpg': 'test.jpg',
            }
            filename = ext_map.get(file_key, f"{file_key}.bin")

        filepath = self.workspace_dir / filename

        # If file already exists, return it
        if filepath.exists():
            return str(filepath)

        # If prefer_local, try to generate locally first
        if self.prefer_local:
            if self._generate_local_file(file_key, filepath):
                return str(filepath)

        # Otherwise download from URL
        url = self.TEST_FILE_URLS[file_key]
        try:
            print(f"  Downloading {filename} from {url[:50]}...")
            urllib.request.urlretrieve(url, filepath)
            print(f"  ✓ Downloaded {filename}")
        except Exception as e:
            print(f"  ✗ Failed to download {filename}: {e}")
            # Try to generate locally as fallback
            if self._generate_local_file(file_key, filepath):
                return str(filepath)
            return f"<{filename}>"

        return str(filepath)

    def _generate_local_file(self, file_key: str, filepath: Path) -> bool:
        """Generate a local test file without downloading."""
        try:
            if file_key.startswith('pdf_'):
                return self._generate_local_pdf(file_key, filepath)
            elif file_key.startswith('image_'):
                return self._generate_local_image(file_key, filepath)
            return False
        except Exception as e:
            print(f"  ✗ Failed to generate local file: {e}")
            return False

    def _generate_local_pdf(self, file_key: str, filepath: Path) -> bool:
        """Generate a simple PDF file locally using reportlab."""
        try:
            from reportlab.pdfgen import canvas
            from reportlab.lib.pagesizes import letter

            print(f"  Generating local PDF: {filepath.name}")

            c = canvas.Canvas(str(filepath), pagesize=letter)
            width, height = letter

            if file_key == 'pdf_simple':
                # Simple single-page PDF
                c.drawString(100, height - 100, "Test PDF Document")
                c.drawString(100, height - 130, "This is a simple test PDF generated locally.")
                c.drawString(100, height - 160, "It contains basic text content for testing.")

            elif file_key == 'pdf_multipage':
                # Multi-page PDF
                for page_num in range(1, 4):
                    c.drawString(100, height - 100, f"Page {page_num}")
                    c.drawString(100, height - 130, f"This is page {page_num} of a multi-page document.")
                    c.drawString(100, height - 160, "Content for testing PDF operations.")
                    if page_num < 3:
                        c.showPage()

            elif file_key == 'pdf_form':
                # Simple form-like PDF (not fillable, but has form-like content)
                c.drawString(100, height - 100, "Sample Form")
                c.drawString(100, height - 130, "Name: _______________________")
                c.drawString(100, height - 160, "Email: ______________________")
                c.drawString(100, height - 190, "Date: _______________________")
                c.drawString(100, height - 220, "Comments: ___________________")

            c.save()
            print(f"  ✓ Generated local PDF: {filepath.name}")
            return True

        except ImportError:
            print(f"  ⚠ reportlab not available, cannot generate local PDF")
            return False
        except Exception as e:
            print(f"  ✗ Failed to generate PDF: {e}")
            return False

    def _generate_local_image(self, file_key: str, filepath: Path) -> bool:
        """Generate a simple image file locally using PIL."""
        try:
            from PIL import Image, ImageDraw, ImageFont

            print(f"  Generating local image: {filepath.name}")

            # Create a simple test image
            if file_key == 'image_png':
                img = Image.new('RGB', (200, 100), color='white')
                draw = ImageDraw.Draw(img)
                draw.rectangle([10, 10, 190, 90], outline='black', width=2)
                draw.text((50, 40), "Test PNG", fill='black')
                img.save(filepath, 'PNG')

            elif file_key == 'image_jpg':
                img = Image.new('RGB', (200, 100), color='lightblue')
                draw = ImageDraw.Draw(img)
                draw.rectangle([10, 10, 190, 90], outline='darkblue', width=2)
                draw.text((50, 40), "Test JPG", fill='darkblue')
                img.save(filepath, 'JPEG')

            print(f"  ✓ Generated local image: {filepath.name}")
            return True

        except ImportError:
            print(f"  ⚠ PIL not available, cannot generate local image")
            return False
        except Exception as e:
            print(f"  ✗ Failed to generate image: {e}")
            return False

    def _generate_pdf_fields_json(self, script_path: str, target_filename: str = "fields.json") -> str:
        """Generate a sample fields.json for PDF form filling."""
        # Try to extract field info from the script's directory
        script_dir = Path(script_path).parent

        # Generate fields JSON with actual W-9 form field names
        # These are the real field IDs from the IRS W-9 PDF form (extracted via extract_form_field_info.py)
        fields_data = [
            {
                "field_id": "topmostSubform[0].Page1[0].f1_01[0]",
                "page": 1,
                "value": "John Doe"
            },
            {
                "field_id": "topmostSubform[0].Page1[0].f1_02[0]",
                "page": 1,
                "value": "Acme Corporation"
            },
            {
                "field_id": "topmostSubform[0].Page1[0].Boxes3a-b_ReadOrder[0].c1_1[0]",
                "page": 1,
                "value": "/1"
            }
        ]

        fields_path = self.workspace_dir / target_filename
        with open(fields_path, 'w') as f:
            json.dump(fields_data, f, indent=2)

        return str(fields_path)

    def copy_to_workspace(self, source_path: str, dest_name: str) -> str:
        """Copy a file to workspace."""
        import shutil
        dest_path = self.workspace_dir / dest_name
        shutil.copy2(source_path, dest_path)
        return str(dest_path)
