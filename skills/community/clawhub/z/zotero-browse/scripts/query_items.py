#!/usr/bin/env python3
"""
Zotero SQLite query script.
Usage: py -3 query_items.py [--db PATH] [--search TERM] [--all] [--summary] [--recent N]
"""

import sqlite3, argparse, sys, os

DEFAULT_DB = r"E:\Refer.Hub\zotero.sqlite"

def get_args():
    parser = argparse.ArgumentParser(description="Query Zotero SQLite database")
    parser.add_argument("--db", default=DEFAULT_DB, help="Path to zotero.sqlite")
    parser.add_argument("--search", help="Search papers by title keyword")
    parser.add_argument("--all", action="store_true", help="List all items")
    parser.add_argument("--summary", action="store_true", help="Show library summary")
    parser.add_argument("--recent", type=int, metavar="N", help="Show N most recent items")
    parser.add_argument("--key", help="Get item by Zotero key")
    return parser.parse_args()

def connect(db_path):
    if not os.path.exists(db_path):
        print(f"ERROR: Database not found: {db_path}", file=sys.stderr)
        print("Your Zotero storage DB is typically at E:\\Refer.Hub\\zotero.sqlite", file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(db_path, timeout=30)
    conn.execute("PRAGMA read_only=ON")
    return conn

def get_field_value(cur, item_id, field_name):
    cur.execute("""
        SELECT itemDataValues.value FROM itemData
        JOIN fields ON itemData.fieldID = fields.fieldID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        WHERE itemData.itemID = ? AND fields.fieldName = ?
    """, (item_id, field_name))
    row = cur.fetchone()
    return row[0] if row else ""

def get_attachments(cur, item_id):
    cur.execute("""
        SELECT items.key, itemAttachments.path, itemAttachments.storageHash,
               itemAttachments.linkMode, itemAttachments.contentType
        FROM itemAttachments
        JOIN items ON itemAttachments.itemID = items.itemID
        WHERE itemAttachments.parentItemID = ?
    """, (item_id,))
    return cur.fetchall()

def print_item(cur, item_id, item_key, item_type, verbose=True):
    title = get_field_value(cur, item_id, "title")
    authors = get_field_value(cur, item_id, "creators")
    date = get_field_value(cur, item_id, "date")
    journal = get_field_value(cur, item_id, "publicationTitle")
    doi = get_field_value(cur, item_id, "DOI")
    abstract = get_field_value(cur, item_id, "abstractNote")
    tags = get_field_value(cur, item_id, "tags")
    url = get_field_value(cur, item_id, "url")

    print(f"\n[{item_type}] {item_key}")
    print(f"  Title: {title}")
    if authors: print(f"  Authors: {authors}")
    if date: print(f"  Date: {date}")
    if journal: print(f"  Journal: {journal}")
    if doi: print(f"  DOI: {doi}")
    if abstract: print(f"  Abstract: {abstract[:300]}..." if len(abstract) > 300 else f"  Abstract: {abstract}")
    if tags: print(f"  Tags: {tags}")

    atts = get_attachments(cur, item_id)
    if atts:
        print(f"  Attachments ({len(atts)}):")
        for att_key, path, storage_hash, link_mode, ct in atts:
            mode = {0: "stored", 1: "linked", 2: "imported"}[link_mode] if link_mode in (0,1,2) else f"mode{link_mode}"
            print(f"    [{mode}] key={att_key}, hash={storage_hash[:8] if storage_hash else 'N/A'}")

def cmd_summary(conn):
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM items")
    total = cur.fetchone()[0]
    cur.execute("""
        SELECT itemTypes.typeName, COUNT(*) FROM items
        JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
        GROUP BY items.itemTypeID ORDER BY COUNT(*) DESC
    """)
    rows = cur.fetchall()
    print(f"\n=== Zotero Library Summary ===")
    print(f"Total items: {total}")
    print(f"\nBy type:")
    for name, count in rows:
        print(f"  {name}: {count}")
    print()

def cmd_search(conn, term):
    cur = conn.cursor()
    cur.execute("""
        SELECT items.key, itemTypes.typeName, items.itemID
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
    print(f"\n=== Search results for '{term}': {len(results)} found ===\n")
    for key, itype, iid in results:
        title = get_field_value(cur, iid, "title")
        date = get_field_value(cur, iid, "date")
        print(f"[{itype}] {key}")
        print(f"  Title: {title[:100]}..." if len(title) > 100 else f"  Title: {title}")
        if date: print(f"  Date: {date}")
        atts = get_attachments(cur, iid)
        if atts:
            stored = sum(1 for a in atts if a[3] == 0)
            print(f"  Attachments: {len(atts)} ({stored} stored PDF)")
        print()
    return results

def cmd_recent(conn, n):
    cur = conn.cursor()
    cur.execute("""
        SELECT items.key, itemTypes.typeName, items.itemID
        FROM items
        JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
        ORDER BY items.dateAdded DESC LIMIT ?
    """, (n,))
    results = cur.fetchall()
    print(f"\n=== {n} Most Recent Items ===\n")
    for key, itype, iid in results:
        title = get_field_value(cur, iid, "title")
        date = get_field_value(cur, iid, "date")
        print(f"[{itype}] {key} | {date}")
        print(f"  {title[:100]}..." if len(title) > 100 else f"  {title}")
        atts = get_attachments(cur, iid)
        if atts:
            print(f"  Attachments: {len(atts)}")
        print()
    return results

def cmd_all(conn):
    cur = conn.cursor()
    cur.execute("""
        SELECT items.key, itemTypes.typeName, items.itemID
        FROM items
        JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
        ORDER BY items.dateAdded DESC
    """)
    for key, itype, iid in cur:
        title = get_field_value(cur, iid, "title")
        print(f"[{itype}] {key} | {title[:80]}")

def cmd_by_key(conn, key):
    cur = conn.cursor()
    cur.execute("""
        SELECT items.key, itemTypes.typeName, items.itemID
        FROM items JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
        WHERE items.key = ?
    """, (key,))
    row = cur.fetchone()
    if not row:
        print(f"Item not found: {key}")
        return
    k, itype, iid = row
    print_item(cur, iid, k, itype)

def main():
    args = get_args()
    conn = connect(args.db)

    if args.summary:
        cmd_summary(conn)
    elif args.search:
        cmd_search(conn, args.search)
    elif args.recent:
        cmd_recent(conn, args.recent)
    elif args.all:
        cmd_all(conn)
    elif args.key:
        cmd_by_key(conn, args.key)
    else:
        cmd_summary(conn)
        print("Tip: --search TERM  or  --recent N  or  --all  or  --key KEY")

    conn.close()

if __name__ == "__main__":
    main()
