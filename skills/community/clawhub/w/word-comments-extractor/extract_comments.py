#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Word Comments Extractor v1.0
Extract comments, anchor text, and page numbers from Word documents.
Outputs JSON for agent-side semantic polishing.
"""

import xml.etree.ElementTree as ET
import html
import sys
import os
import json
import zipfile
import tempfile
import shutil

# XML namespaces
namespaces = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
}


def unpack_docx(docx_path, output_dir):
    """Unpack .docx (which is a zip archive) to extract XML files."""
    if not zipfile.is_zipfile(docx_path):
        print(f"Error: '{docx_path}' is not a valid .docx file.", file=sys.stderr)
        sys.exit(1)

    with zipfile.ZipFile(docx_path, 'r') as zf:
        zf.extractall(output_dir)

    comments_xml = os.path.join(output_dir, 'word', 'comments.xml')
    document_xml = os.path.join(output_dir, 'word', 'document.xml')

    if not os.path.exists(comments_xml):
        print("Error: No comments.xml found. This document may not contain any comments.", file=sys.stderr)
        sys.exit(1)
    if not os.path.exists(document_xml):
        print("Error: No document.xml found. Invalid .docx structure.", file=sys.stderr)
        sys.exit(1)

    return comments_xml, document_xml


def decode_unicode_text(text):
    if not text:
        return ""
    return html.unescape(text)


def extract_comments_from_xml(xml_path):
    """Extract comments from comments.xml."""
    tree = ET.parse(xml_path)
    root = tree.getroot()

    comments = []
    for comment in root.findall('.//w:comment', namespaces):
        comment_id = comment.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')

        text_parts = []
        for t in comment.findall('.//w:t', namespaces):
            if t.text:
                text_parts.append(t.text)
        comment_text = decode_unicode_text(''.join(text_parts))

        comments.append({
            'id': int(comment_id),
            'text': comment_text
        })
    return comments


def find_comment_anchor_text(doc_xml_path, comment_id):
    """Find the anchor text (highlighted content) for a comment."""
    tree = ET.parse(doc_xml_path)
    root = tree.getroot()

    for para in root.findall('.//w:p', namespaces):
        in_comment = False
        comment_texts = []

        for elem in para.iter():
            if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeStart':
                cid = elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                if cid and int(cid) == comment_id:
                    in_comment = True
                    continue

            if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}commentRangeEnd':
                cid = elem.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id')
                if cid and int(cid) == comment_id:
                    in_comment = False
                    break

            if in_comment and elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
                if elem.text:
                    comment_texts.append(elem.text)

        if comment_texts:
            return decode_unicode_text(''.join(comment_texts))
    return ""


def get_comment_pages_from_word(docx_path):
    """
    Get comment page numbers via Word COM interface.
    Returns dict: {sequential_index: page_number}
    """
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc = word.Documents.Open(os.path.abspath(docx_path))

        page_map = {}
        for comment in doc.Comments:
            sequential_idx = comment.Index
            page_num = comment.Scope.Information(3)
            page_map[sequential_idx] = page_num

        doc.Close()
        word.Quit()
        return page_map
    except Exception as e:
        print(f"Warning: Cannot get page numbers via Word COM: {e}", file=sys.stderr)
        return {}


def process_comments(docx_path):
    """Main processing: unpack docx, extract comments, match pages, output JSON."""

    # Unpack .docx to temp directory
    temp_dir = tempfile.mkdtemp(prefix='word_comments_')
    try:
        comments_xml, document_xml = unpack_docx(docx_path, temp_dir)

        # Extract comments
        comments = extract_comments_from_xml(comments_xml)
        comments.sort(key=lambda x: x['id'])

        # Get page numbers via Word COM
        page_map = get_comment_pages_from_word(docx_path)

        results = []
        for idx, comment in enumerate(comments, 1):
            anchor = find_comment_anchor_text(document_xml, comment['id'])
            page = page_map.get(idx, "unknown")

            results.append({
                'index': idx,
                'page': page,
                'comment_text': comment['text'],
                'anchor_text': anchor
            })

        return results
    finally:
        # Clean up temp directory
        shutil.rmtree(temp_dir, ignore_errors=True)


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_comments.py <docx_file_path>")
        print("Example: python extract_comments.py report.docx")
        sys.exit(1)

    docx_path = sys.argv[1]

    if not os.path.exists(docx_path):
        print(f"Error: File not found: {docx_path}")
        sys.exit(1)

    results = process_comments(docx_path)

    # Output JSON
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
