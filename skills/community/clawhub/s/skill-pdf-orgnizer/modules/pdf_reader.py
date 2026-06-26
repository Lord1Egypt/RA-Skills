"""
PDF Reader Module
Extracts text and metadata from PDF files
"""

import PyPDF2
from pathlib import Path
from typing import Dict, Optional, Tuple


class PDFReader:
    """Handles reading and extracting content from PDF files"""

    def __init__(self, max_chars: int = 10000):
        """
        Initialize PDF reader

        Args:
            max_chars: Maximum characters to extract for analysis
        """
        self.max_chars = max_chars

    def read_pdf(self, pdf_path: Path) -> Tuple[str, Dict[str, str]]:
        """
        Extract text and metadata from a PDF file

        Args:
            pdf_path: Path to the PDF file

        Returns:
            Tuple of (extracted_text, metadata_dict)

        Raises:
            Exception: If PDF cannot be read
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)

                # Extract metadata
                metadata = self._extract_metadata(pdf_reader)

                # Extract text from all pages
                text_content = self._extract_text(pdf_reader)

                return text_content, metadata

        except Exception as e:
            raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")

    def _extract_metadata(self, pdf_reader: PyPDF2.PdfReader) -> Dict[str, str]:
        """Extract metadata from PDF"""
        metadata = {}

        if pdf_reader.metadata:
            info = pdf_reader.metadata
            metadata['title'] = info.get('/Title', '').strip()
            metadata['author'] = info.get('/Author', '').strip()
            metadata['subject'] = info.get('/Subject', '').strip()
            metadata['creator'] = info.get('/Creator', '').strip()
            metadata['producer'] = info.get('/Producer', '').strip()

        metadata['page_count'] = str(len(pdf_reader.pages))

        return metadata

    def _extract_text(self, pdf_reader: PyPDF2.PdfReader) -> str:
        """Extract text from PDF pages"""
        text_content = []

        for page in pdf_reader.pages:
            try:
                page_text = page.extract_text()
                if page_text:
                    text_content.append(page_text)

                    # Stop if we've reached the character limit
                    if sum(len(t) for t in text_content) >= self.max_chars:
                        break
            except Exception as e:
                # Continue even if a page fails to extract
                continue

        # Join all text and clean it
        full_text = '\n'.join(text_content)

        # Clean up text
        full_text = self._clean_text(full_text)

        # Truncate to max_chars if needed
        if len(full_text) > self.max_chars:
            full_text = full_text[:self.max_chars]

        return full_text

    def _clean_text(self, text: str) -> str:
        """Clean extracted text"""
        # Remove excessive whitespace
        text = ' '.join(text.split())

        # Remove common PDF artifacts
        text = text.replace('\x00', '')
        text = text.replace('\x0c', '')

        return text

    def can_read(self, pdf_path: Path) -> bool:
        """
        Check if a file can be read as a PDF

        Args:
            pdf_path: Path to the file

        Returns:
            True if file is a readable PDF
        """
        try:
            if not pdf_path.exists():
                return False

            if pdf_path.suffix.lower() != '.pdf':
                return False

            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                # Try to read first page to verify it's a valid PDF
                if len(pdf_reader.pages) > 0:
                    return True

        except Exception:
            return False

        return False
