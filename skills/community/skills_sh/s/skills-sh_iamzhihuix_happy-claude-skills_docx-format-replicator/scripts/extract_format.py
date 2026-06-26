#!/usr/bin/env python3
"""
Extract format information from a Word document (.docx).
This script analyzes the OOXML structure and extracts reusable format information.
"""

import sys
import json
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET
from collections import defaultdict

# OOXML namespaces
NAMESPACES = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
}

def extract_styles(styles_xml):
    """Extract style definitions from styles.xml"""
    tree = ET.parse(styles_xml)
    root = tree.getroot()

    styles = {}
    for style in root.findall('.//w:style', NAMESPACES):
        style_id = style.get(f"{{{NAMESPACES['w']}}}styleId")
        style_type = style.get(f"{{{NAMESPACES['w']}}}type")

        name_elem = style.find('w:name', NAMESPACES)
        style_name = name_elem.get(f"{{{NAMESPACES['w']}}}val") if name_elem is not None else None

        # Extract font info
        rpr = style.find('.//w:rPr', NAMESPACES)
        fonts = {}
        if rpr is not None:
            font_elem = rpr.find('w:rFonts', NAMESPACES)
            if font_elem is not None:
                fonts = {
                    'ascii': font_elem.get(f"{{{NAMESPACES['w']}}}ascii"),
                    'hAnsi': font_elem.get(f"{{{NAMESPACES['w']}}}hAnsi"),
                    'eastAsia': font_elem.get(f"{{{NAMESPACES['w']}}}eastAsia"),
                }

            # Font size
            sz_elem = rpr.find('w:sz', NAMESPACES)
            if sz_elem is not None:
                fonts['size'] = sz_elem.get(f"{{{NAMESPACES['w']}}}val")

        # Extract paragraph properties
        ppr = style.find('.//w:pPr', NAMESPACES)
        para_props = {}
        if ppr is not None:
            jc_elem = ppr.find('w:jc', NAMESPACES)
            if jc_elem is not None:
                para_props['alignment'] = jc_elem.get(f"{{{NAMESPACES['w']}}}val")

            spacing_elem = ppr.find('w:spacing', NAMESPACES)
            if spacing_elem is not None:
                para_props['spacing'] = {
                    'line': spacing_elem.get(f"{{{NAMESPACES['w']}}}line"),
                    'lineRule': spacing_elem.get(f"{{{NAMESPACES['w']}}}lineRule"),
                }

        styles[style_id] = {
            'id': style_id,
            'name': style_name,
            'type': style_type,
            'fonts': fonts,
            'paragraph': para_props,
        }

    return styles

def extract_numbering(numbering_xml):
    """Extract numbering definitions from numbering.xml"""
    if not numbering_xml.exists():
        return {}

    tree = ET.parse(numbering_xml)
    root = tree.getroot()

    numbering = {}
    for num in root.findall('.//w:num', NAMESPACES):
        num_id = num.get(f"{{{NAMESPACES['w']}}}numId")
        abstract_num_id = num.find('w:abstractNumId', NAMESPACES)
        if abstract_num_id is not None:
            numbering[num_id] = {
                'abstractNumId': abstract_num_id.get(f"{{{NAMESPACES['w']}}}val")
            }

    return numbering

def extract_table_structure(doc_xml):
    """Extract table structure from document.xml"""
    tree = ET.parse(doc_xml)
    root = tree.getroot()

    tables = []
    for idx, tbl in enumerate(root.findall('.//w:tbl', NAMESPACES)):
        tbl_pr = tbl.find('w:tblPr', NAMESPACES)

        table_info = {
            'index': idx,
            'rows': len(tbl.findall('w:tr', NAMESPACES)),
            'properties': {}
        }

        if tbl_pr is not None:
            # Table width
            tbl_w = tbl_pr.find('w:tblW', NAMESPACES)
            if tbl_w is not None:
                table_info['properties']['width'] = {
                    'value': tbl_w.get(f"{{{NAMESPACES['w']}}}w"),
                    'type': tbl_w.get(f"{{{NAMESPACES['w']}}}type"),
                }

            # Table style
            tbl_style = tbl_pr.find('w:tblStyle', NAMESPACES)
            if tbl_style is not None:
                table_info['properties']['style'] = tbl_style.get(f"{{{NAMESPACES['w']}}}val")

        # Extract grid columns
        grid = tbl.find('w:tblGrid', NAMESPACES)
        if grid is not None:
            cols = grid.findall('w:gridCol', NAMESPACES)
            table_info['columns'] = [
                col.get(f"{{{NAMESPACES['w']}}}w") for col in cols
            ]

        tables.append(table_info)

    return tables

def extract_headers_footers(docx_path):
    """Extract header and footer information"""
    headers = []
    footers = []

    with zipfile.ZipFile(docx_path, 'r') as zf:
        for name in zf.namelist():
            if name.startswith('word/header'):
                headers.append({
                    'file': name,
                    'exists': True
                })
            elif name.startswith('word/footer'):
                footers.append({
                    'file': name,
                    'exists': True
                })

    return {'headers': headers, 'footers': footers}

def extract_format(docx_path, output_path):
    """Main function to extract format from a docx file"""
    docx_path = Path(docx_path)
    output_path = Path(output_path)

    if not docx_path.exists():
        print(f"Error: File not found: {docx_path}")
        return 1

    # Create temporary directory to unpack docx
    import tempfile
    import shutil

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Unpack docx
        with zipfile.ZipFile(docx_path, 'r') as zf:
            zf.extractall(tmpdir)

        word_dir = tmpdir / 'word'

        # Extract various format components
        format_info = {
            'source_document': str(docx_path.name),
            'styles': {},
            'numbering': {},
            'tables': [],
            'headers_footers': {}
        }

        # Extract styles
        styles_path = word_dir / 'styles.xml'
        if styles_path.exists():
            format_info['styles'] = extract_styles(styles_path)

        # Extract numbering
        numbering_path = word_dir / 'numbering.xml'
        if numbering_path.exists():
            format_info['numbering'] = extract_numbering(numbering_path)

        # Extract table structures
        doc_path = word_dir / 'document.xml'
        if doc_path.exists():
            format_info['tables'] = extract_table_structure(doc_path)

        # Extract headers/footers info
        format_info['headers_footers'] = extract_headers_footers(docx_path)

    # Save to output file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(format_info, f, indent=2, ensure_ascii=False)

    print(f"✅ Format extracted successfully!")
    print(f"   Source: {docx_path}")
    print(f"   Output: {output_path}")
    print(f"\nExtracted:")
    print(f"   - {len(format_info['styles'])} styles")
    print(f"   - {len(format_info['numbering'])} numbering definitions")
    print(f"   - {len(format_info['tables'])} tables")
    print(f"   - {len(format_info['headers_footers']['headers'])} headers")
    print(f"   - {len(format_info['headers_footers']['footers'])} footers")

    return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: extract_format.py <input.docx> [output.json]")
        print("\nExtract format information from a Word document.")
        print("\nArguments:")
        print("  input.docx   - Path to the Word document to analyze")
        print("  output.json  - Path for output JSON file (default: format.json)")
        return 1

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "format.json"

    return extract_format(input_path, output_path)

if __name__ == '__main__':
    sys.exit(main())
