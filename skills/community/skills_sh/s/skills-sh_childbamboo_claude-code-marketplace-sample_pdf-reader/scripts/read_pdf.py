#!/usr/bin/env python3
"""
PDF Reader Script
Extracts text content from PDF files and converts to Markdown format.
"""

import sys
import os

try:
    import pdfplumber
except ImportError:
    print("Error: pdfplumber is not installed.")
    print("Please install it with: pip install pdfplumber")
    sys.exit(1)


def read_pdf(file_path):
    """
    Read PDF file and extract text content.

    Args:
        file_path (str): Path to the PDF file

    Returns:
        str: Extracted text content in Markdown format
    """
    try:
        markdown_content = []

        with pdfplumber.open(file_path) as pdf:
            # Add document title
            markdown_content.append(f"# {os.path.basename(file_path)}\n")
            markdown_content.append(f"**Total Pages:** {len(pdf.pages)}\n")
            markdown_content.append("---\n")

            # Extract text from each page
            for page_num, page in enumerate(pdf.pages, start=1):
                markdown_content.append(f"## Page {page_num}\n")

                # Extract text
                text = page.extract_text()
                if text:
                    markdown_content.append(text)
                else:
                    markdown_content.append("*(No text content on this page)*")

                # Extract tables
                tables = page.extract_tables()
                if tables:
                    markdown_content.append("\n### Tables\n")
                    for table_num, table in enumerate(tables, start=1):
                        markdown_content.append(f"\n**Table {table_num}:**\n")
                        markdown_content.append(format_table_as_markdown(table))

                markdown_content.append("\n---\n")

        return '\n'.join(markdown_content)

    except FileNotFoundError:
        return f"Error: File not found: {file_path}"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def format_table_as_markdown(table):
    """
    Format a table as Markdown.

    Args:
        table (list): Table data as list of lists

    Returns:
        str: Markdown formatted table
    """
    if not table or not table[0]:
        return ""

    markdown_table = []

    # Header row
    header = table[0]
    markdown_table.append("| " + " | ".join(str(cell) if cell else "" for cell in header) + " |")

    # Separator row
    markdown_table.append("| " + " | ".join("---" for _ in header) + " |")

    # Data rows
    for row in table[1:]:
        markdown_table.append("| " + " | ".join(str(cell) if cell else "" for cell in row) + " |")

    return "\n".join(markdown_table)


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print("Usage: python read_pdf.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        sys.exit(1)

    if not file_path.lower().endswith('.pdf'):
        print("Warning: File does not have .pdf extension")

    content = read_pdf(file_path)
    print(content)


if __name__ == "__main__":
    main()
