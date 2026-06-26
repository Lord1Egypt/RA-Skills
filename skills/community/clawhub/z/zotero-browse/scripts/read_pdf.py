#!/usr/bin/env python3
"""
Read PDF from Zotero storage by attachment key.
Usage: py -3 read_pdf.py <attachment_key> [--db PATH] [--pages N] [--output FILE]
       py -3 read_pdf.py --search "SEARCH TERM" [--db PATH] [--pages N]
"""

import sqlite3, argparse, sys, os

DEFAULT_DB = r"E:\Refer.Hub\zotero.sqlite"
STORAGE_BASE = r"E:\Refer.Hub\storage"

def get_args():
    parser = argparse.ArgumentParser(description="Read PDF from Zotero storage")
    parser.add_argument("key", nargs="?", help="Attachment key (e.g. ZL42EGES)")
    parser.add_argument("--search", "-s", help="Search for PDF by paper title keyword")
    parser.add_argument("--db", default=DEFAULT_DB, help="Path to zotero.sqlite")
    parser.add_argument("--pages", "-p", type=int, default=0,
                        help="Max pages to extract (0=all)")
    parser.add_argument("--output", "-o", help="Write extracted text to file")
    parser.add_argument("--info", "-i", action="store_true", help="Show PDF info only")
    return parser.parse_args()

def get_pdf_path(cur, key):
    """Get PDF file path from attachment key."""
    cur.execute("""
        SELECT items.key, itemAttachments.path, itemAttachments.storageHash
        FROM itemAttachments
        JOIN items ON itemAttachments.itemID = items.itemID
        WHERE items.key = ? AND itemAttachments.linkMode = 0
    """, (key,))
    row = cur.fetchone()
    if not row:
        return None, None
    att_key, path, storage_hash = row
    if not storage_hash:
        return None, path
    folder = os.path.join(STORAGE_BASE, storage_hash)
    if os.path.isdir(folder):
        files = [f for f in os.listdir(folder) if f.lower().endswith(".pdf")]
        if files:
            return os.path.join(folder, files[0]), path
    return None, path

def find_pdf_by_title(cur, term):
    """Search for PDF attachment by paper title."""
    cur.execute("""
        SELECT items.key, itemTypes.typeName, items.itemID,
               itemDataValues.value
        FROM items
        JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
        JOIN itemData ON items.itemID = itemData.itemID
        JOIN fields ON itemData.fieldID = fields.fieldID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        WHERE fields.fieldName = 'title'
        AND itemDataValues.value LIKE ?
        ORDER BY items.dateAdded DESC
    """, (f"%{term}%",))
    results = cur.fetchall()
    return results

def get_pdf_info(pdf_path):
    """Get PDF metadata using PyMuPDF."""
    import fitz
    doc = fitz.open(pdf_path)
    info = {
        "pages": len(doc),
        "title": doc.metadata.get("title", ""),
        "author": doc.metadata.get("author", ""),
        "subject": doc.metadata.get("subject", ""),
        "file_size": os.path.getsize(pdf_path),
    }
    return info, doc

def extract_text(pdf_path, max_pages=0):
    """Extract text from PDF using PyMuPDF."""
    import fitz
    doc = fitz.open(pdf_path)
    total = len(doc)
    limit = min(max_pages, total) if max_pages > 0 else total

    full_text = ""
    for i in range(limit):
        text = doc[i].get_text()
        full_text += f"\n=== Page {i+1}/{total} ===\n{text}"

    if max_pages == 0 or max_pages >= total:
        full_text += f"\n[Truncated at page {limit}/{total}]"
    doc.close()
    return full_text

def main():
    args = get_args()
    conn = sqlite3.connect(args.db, timeout=30)
    conn.execute("PRAGMA read_only=ON")

    if args.search:
        print(f"Searching for: {args.search}")
        results = find_pdf_by_title(conn, args.search)
        print(f"Found {len(results)} papers:\n")
        for key, itype, iid, title in results:
            print(f"  [{key}] {title[:80]}...")
        print()
        if not results:
            conn.close()
            return
        att_key = input("Enter attachment key to open: ").strip()
    else:
        att_key = args.key

    if not att_key:
        print("Usage: py -3 read_pdf.py <key>  or  py -3 read_pdf.py --search 'TERM'")
        conn.close()
        return

    pdf_path, db_path = get_pdf_path(conn.cursor(), att_key)
    conn.close()

    if not pdf_path:
        # Try finding by title in storage folder name
        print(f"PDF path not resolved for key={att_key}")
        print(f"DB path record: {db_path}")
        print("This may be a linked file, not a stored attachment.")
        return

    print(f"Opening: {pdf_path}")
    print(f"File size: {os.path.getsize(pdf_path) / 1024 / 1024:.1f} MB\n")

    if args.info:
        info, doc = get_pdf_info(pdf_path)
        print(f"Pages: {info['pages']}")
        print(f"Title: {info['title']}")
        print(f"Author: {info['author']}")
        print(f"Subject: {info['subject']}")
        return

    print(f"Extracting text (max_pages={args.pages or 'all'})...")
    text = extract_text(pdf_path, args.pages)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Text written to: {args.output}")
    else:
        print(text)

if __name__ == "__main__":
    main()
