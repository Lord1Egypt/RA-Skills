#!/usr/bin/env python3
"""
Zotero SQLite write script (ADD/TAG/UPDATE operations).
WARNING: Always backup the database before writing!

Usage:
  py -3 write_items.py --backup DB_PATH              # backup before writing
  py -3 write_items.py --add-tag KEY "tag1" ["tag2"...]
  py -3 write_items.py --add-note KEY "note content"
  py -3 write_items.py --set-field KEY fieldName "value"
  py -3 write_items.py --new-item typeName --title "Title" [--author "Name"...]
  py -3 write_items.py --list-fields                 # show available fields
  py -3 write_items.py --item-info KEY               # show full item details
"""

import sqlite3, argparse, sys, os, shutil, uuid
from datetime import datetime

DEFAULT_DB = r"E:\Refer.Hub\zotero.sqlite"
BACKUP_DIR = r"E:\Refer.Hub\backups"

def get_args():
    parser = argparse.ArgumentParser(description="Write to Zotero SQLite (ADD/TAG/UPDATE)")
    parser.add_argument("--db", default=DEFAULT_DB, help="Path to zotero.sqlite")
    parser.add_argument("--backup", metavar="PATH",
                        help="Backup the database to BACKUP_DIR before writing")
    parser.add_argument("--add-tag", nargs="+", metavar=("KEY", "TAG"),
                        help="Add tag(s) to item by key")
    parser.add_argument("--add-note", nargs=2, metavar=("KEY", "CONTENT"),
                        help="Add note to item by key")
    parser.add_argument("--set-field", nargs=3, metavar=("KEY", "FIELD", "VALUE"),
                        help="Set/update a field value on an item")
    parser.add_argument("--new-item", metavar="TYPE",
                         help="Create new item (type: journalArticle, book, etc.)")
    parser.add_argument("--title", help="Title for new item")
    parser.add_argument("--authors", nargs="+", metavar="NAME",
                        help="Author names (First Last)")
    parser.add_argument("--date", help="Publication date (YYYY or YYYY-MM-DD)")
    parser.add_argument("--journal", help="Journal name")
    parser.add_argument("--doi", help="DOI")
    parser.add_argument("--url", help="URL")
    parser.add_argument("--abstract", help="Abstract")
    parser.add_argument("--list-fields", action="store_true",
                        help="List all available field names")
    parser.add_argument("--item-info", metavar="KEY",
                        help="Show full item details including field IDs")
    return parser.parse_args()

# ─── Field name → fieldID map (cached) ───────────────────────────────────────
FIELD_CACHE = None

def get_field_id(cur, field_name):
    global FIELD_CACHE
    if FIELD_CACHE is None:
        cur.execute("SELECT fieldID, fieldName FROM fields")
        FIELD_CACHE = {row[1]: row[0] for row in cur.fetchall()}
    return FIELD_CACHE.get(field_name)

# ─── Item type name → itemTypeID ─────────────────────────────────────────────
TYPE_CACHE = None

def get_type_id(cur, type_name):
    global TYPE_CACHE
    if TYPE_CACHE is None:
        cur.execute("SELECT itemTypeID, typeName FROM itemTypes")
        TYPE_CACHE = {row[1]: row[0] for row in cur.fetchall()}
    return TYPE_CACHE.get(type_name)

# ─── Creator type name → creatorTypeID ────────────────────────────────────────
CREATOR_TYPE_CACHE = None

def get_creator_type_id(cur, type_name):
    global CREATOR_TYPE_CACHE
    if CREATOR_TYPE_CACHE is None:
        cur.execute("SELECT creatorTypeID, creatorType FROM creatorTypes")
        CREATOR_TYPE_CACHE = {row[1]: row[0] for row in cur.fetchall()}
    return CREATOR_TYPE_CACHE.get(type_name or "author")

# ─── Backup ────────────────────────────────────────────────────────────────────
def backup_db(db_path):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(BACKUP_DIR, f"zotero_{ts}.sqlite")
    shutil.copy2(db_path, backup_path)
    print(f"[BACKUP] Created: {backup_path}")
    return backup_path

# ─── Get itemID from key ──────────────────────────────────────────────────────
def get_item_id(cur, key):
    cur.execute("SELECT itemID FROM items WHERE key = ?", (key,))
    row = cur.fetchone()
    return row[0] if row else None

# ─── ValueID management ────────────────────────────────────────────────────────
def get_or_create_value(cur, value_text):
    """Return valueID for a text value, creating if necessary."""
    if not value_text:
        return None
    cur.execute("SELECT valueID FROM itemDataValues WHERE value = ?", (value_text,))
    row = cur.fetchone()
    if row:
        return row[0]
    cur.execute("INSERT INTO itemDataValues (value) VALUES (?)", (value_text,))
    return cur.lastrowid

# ─── Tag operations ────────────────────────────────────────────────────────────
def add_tags(cur, item_id, tag_names):
    """Add tags to an item."""
    added = 0
    for tag_name in tag_names:
        tag_name = tag_name.strip()
        if not tag_name:
            continue
        # Get or create tag
        cur.execute("SELECT tagID FROM tags WHERE name = ?", (tag_name,))
        row = cur.fetchone()
        if row:
            tag_id = row[0]
        else:
            cur.execute("INSERT INTO tags (name) VALUES (?)", (tag_name,))
            tag_id = cur.lastrowid

        # Link tag to item
        cur.execute("SELECT 1 FROM itemTags WHERE itemID = ? AND tagID = ? AND type = 1", (item_id, tag_id))
        if cur.fetchone():
            print(f"  [SKIP] Tag '{tag_name}' already on item")
            continue

        cur.execute("INSERT INTO itemTags (itemID, tagID, type) VALUES (?, ?, 1)", (item_id, tag_id))
        print(f"  [ADDED] Tag: {tag_name}")
        added += 1
    return added

# ─── Note operations ───────────────────────────────────────────────────────────
def add_note(cur, item_id, note_content):
    """Add a note to an item."""
    # Create note item
    note_key = uuid.uuid4().hex[:8].upper()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute("""
        INSERT INTO items (itemTypeID, key, libraryID, dateAdded, dateModified, clientDateModified, version, synced)
        VALUES (?, ?, 1, ?, ?, ?, 1, 0)
    """, (14, note_key, now, now))  # itemTypeID 14 = note
    note_item_id = cur.lastrowid

    # Link note to parent item
    cur.execute("SELECT itemID FROM itemNotes")
    # notes don't have a separate parent link - use itemNotes table
    cur.execute("INSERT INTO itemNotes (itemID, parentItemID, note) VALUES (?, ?, ?)",
                (note_item_id, item_id, note_content))
    print(f"  [ADDED] Note (key={note_key}, itemID={note_item_id}) linked to parent item {item_id}")
    return note_item_id

# ─── Field value operations ─────────────────────────────────────────────────────
def set_field(cur, item_id, field_name, value_text):
    """Set or update a field value on an item."""
    field_id = get_field_id(cur, field_name)
    if not field_id:
        print(f"  [ERROR] Unknown field: {field_name}")
        print("  Run with --list-fields to see all available fields.")
        return False

    # Check if field already has a value
    cur.execute("SELECT valueID FROM itemData WHERE itemID = ? AND fieldID = ?",
                (item_id, field_id))
    existing = cur.fetchone()

    value_id = get_or_create_value(cur, value_text)

    if existing:
        cur.execute("UPDATE itemData SET valueID = ? WHERE itemID = ? AND fieldID = ?",
                    (value_id, item_id, field_id))
        print(f"  [UPDATED] {field_name} = {value_text}")
    else:
        cur.execute("INSERT INTO itemData (itemID, fieldID, valueID) VALUES (?, ?, ?)",
                    (item_id, field_id, value_id))
        print(f"  [SET] {field_name} = {value_text}")
    return True

# ─── New item creation ────────────────────────────────────────────────────────
def new_item(conn, cur, item_type, title, authors=None, date=None,
             journal=None, doi=None, url=None, abstract=None):
    """Create a new item with metadata."""
    type_id = get_type_id(cur, item_type)
    if not type_id:
        print(f"  [ERROR] Unknown item type: {item_type}")
        print("  Common types: journalArticle, book, bookSection, conferencePaper, thesis, webpage")
        return None

    item_key = uuid.uuid4().hex[:8].upper()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cur.execute("""
        INSERT INTO items (itemTypeID, key, libraryID, dateAdded, dateModified, clientDateModified, version, synced)
        VALUES (?, ?, 1, ?, ?, ?, 1, 0)
    """, (type_id, item_key, now, now))
    item_id = cur.lastrowid
    print(f"  [CREATED] Item key={item_key}, itemID={item_id}, type={item_type}")

    # Set title (required for meaningful items)
    if title:
        set_field(cur, item_id, "title", title)

    # Set authors
    if authors:
        creator_type_id = get_creator_type_id(cur, "author")
        for i, name in enumerate(authors):
            name = name.strip()
            if not name:
                continue
            parts = name.rsplit(None, 1)
            if len(parts) == 2:
                first, last = parts
            else:
                first, last = "", parts[0]
            cur.execute("""
                INSERT INTO creators (firstName, lastName) VALUES (?, ?)
            """, (first, last))
            creator_id = cur.lastrowid
            cur.execute("""
                INSERT INTO itemCreators (itemID, creatorID, creatorTypeID, orderIndex)
                VALUES (?, ?, ?, ?)
            """, (item_id, creator_id, creator_type_id, i))
            print(f"  [AUTHOR] {first} {last}")

    # Set other fields
    for field_name, value in [
        ("date", date), ("publicationTitle", journal),
        ("DOI", doi), ("url", url), ("abstractNote", abstract)
    ]:
        if value:
            set_field(cur, item_id, field_name, value)

    conn.commit()
    print(f"\n  Item URL: zotero://select/items/{item_key}")
    return item_key

# ─── Item info ─────────────────────────────────────────────────────────────────
def item_info(cur, key):
    """Show full details of an item."""
    cur.execute("""
        SELECT items.itemID, items.key, items.itemTypeID, items.dateAdded,
               itemTypes.typeName
        FROM items JOIN itemTypes ON items.itemTypeID = itemTypes.itemTypeID
        WHERE items.key = ?
    """, (key,))
    row = cur.fetchone()
    if not row:
        print(f"Item not found: {key}")
        return

    item_id, item_key, type_id, date_added, type_name = row
    print(f"\n=== Item: {item_key} [{type_name}] ===")
    print(f"itemID: {item_id}  |  dateAdded: {date_added}")

    # Get all field values
    cur.execute("""
        SELECT fields.fieldName, itemDataValues.value
        FROM itemData
        JOIN fields ON itemData.fieldID = fields.fieldID
        JOIN itemDataValues ON itemData.valueID = itemDataValues.valueID
        WHERE itemData.itemID = ?
    """, (item_id,))
    for fname, fval in cur.fetchall():
        if fval:
            print(f"  {fname}: {fval[:200] if len(str(fval)) > 200 else fval}")

    # Get tags
    cur.execute("""
        SELECT tags.name FROM itemTags
        JOIN tags ON itemTags.tagID = tags.tagID
        WHERE itemTags.itemID = ?
    """, (item_id,))
    tags = [r[0] for r in cur.fetchall()]
    if tags:
        print(f"  Tags: {', '.join(tags)}")

    # Get attachments
    cur.execute("""
        SELECT items.key, itemAttachments.contentType, itemAttachments.linkMode
        FROM itemAttachments
        JOIN items ON itemAttachments.itemID = items.itemID
        WHERE itemAttachments.parentItemID = ?
    """, (item_id,))
    for att_key, ctype, lmode in cur.fetchall():
        print(f"  Attachment: key={att_key}, type={ctype}, mode={lmode}")

    print()

# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    args = get_args()

    if args.list_fields:
        conn = sqlite3.connect(args.db, timeout=30)
        cur = conn.cursor()
        cur.execute("SELECT fieldID, fieldName FROM fields ORDER BY fieldName")
        print("\nAvailable fields:")
        for fid, fname in cur.fetchall():
            print(f"  {fname} (ID={fid})")
        conn.close()
        return

    if args.item_info:
        conn = sqlite3.connect(args.db, timeout=30)
        item_info(conn.cursor(), args.item_info)
        conn.close()
        return

    # All write operations require backup
    has_write = any([args.add_tag, args.add_note, args.set_field, args.new_item])
    if has_write and not args.backup:
        print("ERROR: --backup DB_PATH is required before making any write changes.")
        print("Example: --backup \"E:\\Refer.Hub\\zotero.sqlite\"")
        sys.exit(1)

    # Backup
    if args.backup:
        backup_path = backup_db(args.backup)
        print(f"[WRITE MODE] Database: {args.db}")

    conn = sqlite3.connect(args.db, timeout=60)
    conn.execute("PRAGMA journal_mode=WAL")  # use WAL for safer writes
    cur = conn.cursor()

    try:
        if args.add_tag:
            key = args.add_tag[0]
            tags = args.add_tag[1:]
            item_id = get_item_id(cur, key)
            if not item_id:
                print(f"ERROR: Item not found: {key}")
                sys.exit(1)
            print(f"\nAdding tags to item {key} (itemID={item_id}):")
            n = add_tags(cur, item_id, tags)
            print(f"  Done: {n} tag(s) added.")
            conn.commit()

        elif args.add_note:
            key, content = args.add_note
            item_id = get_item_id(cur, key)
            if not item_id:
                print(f"ERROR: Item not found: {key}")
                sys.exit(1)
            print(f"\nAdding note to item {key} (itemID={item_id}):")
            add_note(cur, item_id, content)
            conn.commit()

        elif args.set_field:
            key, field, value = args.set_field
            item_id = get_item_id(cur, key)
            if not item_id:
                print(f"ERROR: Item not found: {key}")
                sys.exit(1)
            print(f"\nSetting field on item {key} (itemID={item_id}):")
            ok = set_field(cur, item_id, field, value)
            if ok:
                conn.commit()

        elif args.new_item:
            if not args.title:
                print("ERROR: --title is required when creating a new item.")
                sys.exit(1)
            print(f"\nCreating new item:")
            key = new_item(conn, cur, args.new_item, args.title,
                           authors=args.authors, date=args.date,
                           journal=args.journal, doi=args.doi,
                           url=args.url, abstract=args.abstract)
            if not key:
                sys.exit(1)

    except Exception as e:
        conn.rollback()
        print(f"\n[ERROR] Write failed, rolled back. Error: {e}")
        sys.exit(1)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
