# -*- coding: utf-8 -*-
"""
safety-kb-import: Safety Review Knowledge Base Import Tool
==========================================================
Import regulations, standards, and policy documents into the safety-review
knowledge base. Supports multi-source text extraction, smart clause splitting,
and conflict detection.

Usage:
  python kb_import.py import --json <manifest.json>
  python kb_import.py extract-pdf <pdf_path>
  python kb_import.py split-clauses --text <content> [--pattern standard|policy]
  python kb_import.py validate <regulation_id>
  python kb_import.py schema

Manifest JSON format (for `import` command):
{
  "items": [
    {
      "title": "Standard Title",
      "document_number": "GB 16423-2020",
      "issuing_authority": "Agency Name",
      "authority_level": "national",  # national/ministerial/local
      "effective_date": "2021-09-01",
      "status": "current",           # current/superseded/draft/repealed
      "domains": "矿山安全",
      "category": "国标",
      "full_text": "...complete text...",
      "source_url": "",
      "page_count": 70,
      "clause_split_pattern": "standard"  # standard | policy | raw_lines
    }
  ]
}
"""

import sqlite3
import sys
import json
import os
import re
import argparse
from datetime import datetime

DEFAULT_DB_PATH = os.path.expanduser(
    r"~\.openclaw-autoclaw\skills\safety-review\db\knowledge.db"
)


def get_connection(db_path=None):
    path = db_path or os.environ.get("KB_PATH", DEFAULT_DB_PATH)
    if not os.path.exists(path):
        print(json.dumps({"error": f"Database not found at {path}"}), file=sys.stderr)
        sys.exit(1)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def detect_schema(conn):
    schema = {}
    for table in ["regulations", "clauses", "std_registry"]:
        try:
            cursor = conn.execute(f"PRAGMA table_info({table})")
            schema[table] = [row[1] for row in cursor.fetchall()]
        except sqlite3.OperationalError:
            schema[table] = []
    return schema


def detect_insert_columns(conn, table="regulations"):
    """Get column names needed for INSERT, excluding auto-generated ones."""
    cursor = conn.execute(f"PRAGMA table_info({table})")
    columns = [row[1] for row in cursor.fetchall()]
    # Exclude auto-increment primary key (usually 'id')
    if columns and columns[0] == "id":
        columns = columns[1:]
    return columns


def extract_pdf_text(pdf_path):
    """Extract text from PDF using pdfplumber."""
    try:
        import pdfplumber
    except ImportError:
        return {"success": False, "error": "pdfplumber not installed. Run: pip install pdfplumber"}

    if not os.path.exists(pdf_path):
        return {"success": False, "error": f"File not found: {pdf_path}"}

    text_parts = []
    total_chars = 0
    page_count = 0

    try:
        with pdfplumber.open(pdf_path) as pdf:
            page_count = len(pdf.pages)
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text() or ""
                if page_text.strip():
                    text_parts.append(page_text)
                    total_chars += len(page_text)

        full_text = "\n".join(text_parts)
        is_scan = total_chars == 0 and page_count > 0

        return {
            "success": True,
            "text": full_text,
            "char_count": total_chars,
            "page_count": page_count,
            "is_scan_only": is_scan,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def cmd_extract_pdf(args):
    """Extract text from a PDF file."""
    result = extract_pdf_text(args.pdf_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ============================================================
# Clause Splitting Strategies
# ============================================================

class ClauseSplitter:
    """
    Split full regulation text into individual clauses using pattern-matching.
    
    Supports three patterns:
    - 'standard': Chinese GB/AQ standards with numbered sections (第X章, X.X, X.X.X)
    - 'policy': Government policy documents with numbered articles (一、二、(一))
    - 'raw_lines': Simple line-by-line splitting (fallback)
    """

    @staticmethod
    def split_standard(text):
        """
        Split GB/AQ standard text by recognizing:
        - Chapters: 第X章 XXX / 第X节 XXX
        - Sections: X.X  Title
        - Articles: X.X.X  Content or numbered paragraphs
        """
        clauses = []
        lines = text.split("\n")
        current_chapter = ""
        current_section = ""

        # Pattern: 第N章/第N节
        chapter_pat = re.compile(r"^第[一二三四五六七八九十百零\d]+[章节]\s+(.+)$")
        # Pattern: N.N section heading like 4.5 紧急避险系统建设
        section_pat = re.compile(r"^(\d+\.\d+)\s+(.+)$")
        # Pattern: N.N.N detailed clause
        subsec_pat = re.compile(r"^(\d+\.\d+\.\d+)\s*(.*)$")
        # Pattern: Appendix
        appendix_pat = re.compile(r"^(附录\s*[A-Z\d]|附表\s*\d)")

        for line in lines:
            line = line.rstrip()
            if not line.strip():
                continue

            ch_match = chapter_pat.match(line.strip())
            sec_match = section_pat.match(line.strip())
            sub_match = subsec_pat.match(line.strip())

            if ch_match:
                current_chapter = line.strip()
                clauses.append({"article_number": current_chapter, "content": line.strip(), "chapter": current_chapter})
            elif sec_match:
                current_section = line.strip()
                clauses.append({"article_number": current_section, "content": line.strip(), "chapter": current_chapter})
            elif sub_match:
                num = sub_match.group(1).strip()
                content = sub_match.group(2).strip() or line.strip()
                clauses.append({
                    "article_number": num,
                    "content": content,
                    "chapter": current_section or current_chapter,
                })
            elif appendix_pat.match(line.strip()):
                current_chapter = line.strip()
                clauses.append({
                    "article_number": line.strip()[:30],
                    "content": line.strip(),
                    "chapter": line.strip(),
                })
            elif current_chapter or current_section:
                # Continuation line under a section
                if len(clauses) > 0 and len(line.strip()) > 2:
                    clauses.append({
                        "article_number": clauses[-1]["article_number"] + "+",
                        "content": line.strip(),
                        "chapter": current_chapter,
                    })

        return clauses

    @staticmethod
    def split_policy(text):
        """
        Split government policy documents by recognizing:
        - 一、二、三... (top-level numbering)
        - （一）（二）（三）... (sub-items)
        - 1. 2. 3... (numeric items)
        """
        clauses = []
        lines = text.split("\n")

        # Top-level: 一、二、三、（一）（二） etc.
        top_pat = re.compile(r"^[（(]?[一二三四五六七八九十]+[）、.]")
        # Numeric: 1. 2. 3. (1) (2)
        num_pat = re.compile(r"^\d+[.\．]")
        sub_num_pat = re.compile(r"^（\d+）")

        for line in lines:
            line = line.rstrip()
            if not line.strip():
                continue

            if top_pat.match(line.strip()) or num_pat.match(line.strip()) or sub_num_pat.match(line.strip()):
                article = line.strip()[:50]
                clauses.append({
                    "article_number": article,
                    "content": line.strip(),
                    "chapter": "",
                })

        # If no structured patterns found, fall back to meaningful paragraphs
        if not clauses:
            for para in text.split("\n\n"):
                para = para.strip()
                if len(para) > 10:
                    clauses.append({
                        "article_number": "",
                        "content": para[:500],
                        "chapter": "",
                    })

        return clauses

    @staticmethod
    def split_raw_lines(text):
        """Fallback: split by non-empty lines."""
        clauses = []
        for line in text.split("\n"):
            line = line.strip()
            if len(line) > 2:
                clauses.append({
                    "article_number": "",
                    "content": line[:500],
                    "chapter": "",
                })
        return clauses

    @classmethod
    def split(cls, text, pattern="standard"):
        """Dispatch to appropriate splitter based on pattern."""
        splitters = {
            "standard": cls.split_standard,
            "policy": cls.split_policy,
            "raw_lines": cls.split_raw_lines,
        }
        splitter = splitters.get(pattern, cls.split_raw_lines)
        return splitter(text)


def cmd_split_clauses(args):
    """Test clause splitting on given text."""
    text = args.text
    pattern = args.pattern

    clauses = ClauseSplitter.split(text, pattern)
    print(json.dumps({
        "pattern": pattern,
        "input_length": len(text),
        "clause_count": len(clauses),
        "sample_clauses": clauses[:10],
    }, ensure_ascii=False, indent=2))


def cmd_import(args):
    """Import regulations from a JSON manifest into the knowledge base."""
    manifest_path = args.json

    if not os.path.exists(manifest_path):
        print(json.dumps({"error": f"Manifest file not found: {manifest_path}"}))
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    items = manifest.get("items", [])
    conn = get_connection()
    schema = detect_schema(conn)
    reg_cols = schema.get("regulations", [])
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    results = []

    for item in items:
        result = import_single_item(conn, item, reg_cols, now)
        results.append(result)

    conn.commit()
    conn.close()

    summary = {
        "total": len(items),
        "imported": sum(1 for r in results if r["status"] == "created"),
        "updated": sum(1 for r in results if r["status"] == "updated"),
        "skipped": sum(1 for r in results if r["status"] == "skipped"),
        "failed": sum(1 for r in results if r["status"] == "error"),
        "details": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def import_single_item(conn, item, reg_cols, now):
    """Import a single regulation item into the database."""
    doc_no = item.get("document_number", "")
    title = item.get("title", "")
    full_text = item.get("full_text", "")
    pattern = item.get("clause_split_pattern", "standard")

    # Step 1: Check for existing record
    existing_id = None
    existing_row = None

    if doc_no:
        row = conn.execute(
            f"SELECT id, title, document_number, length(full_text) as tl "
            f"FROM regulations WHERE document_number LIKE ? LIMIT 1",
            (f"%{doc_no.split()[0]}%",) if doc_no and " " in str(doc_no) else (f"%{doc_no}%",),
        ).fetchone()
        if row:
            existing_id = row["id"]
            existing_row = dict(row)

    # Determine action
    action = "created"
    target_id = None

    try:
        if existing_id:
            # Check if existing data looks correct (title match)
            if existing_row and title and existing_row["title"] != title:
                short_title = (existing_row["title"] or "")[:40]
                if any(kw in short_title for kw in [doc_no.split()[0] if doc_no else "", title[:10]]):
                    pass  # Likely same standard different version
                else:
                    # Mismatch detected — update anyway but flag it
                    action = "updated_mismatch"

            # Update existing record
            cols = detect_insert_columns(conn, "regulations")
            set_clause = ", ".join([f"[{c}] = ?" for c in cols])
            values = [
                item.get("title"),
                item.get("document_number"),
                item.get("issuing_authority", ""),
                item.get("authority_level", ""),
                item.get("effective_date", ""),
                item.get("status", "current"),
                item.get("domains", ""),
                item.get("category", ""),
                full_text,
                f'imported/{(doc_no or "unknown").split()[0]}.pdf',
                item.get("source_url", ""),
                0, "", "",
                item.get("page_count", 0),
                now, now,
            ]
            # Trim values to match actual column count
            values = values[:len(cols)]
            conn.execute(f"UPDATE regulations SET {set_clause} WHERE id=?", values + [existing_id])
            target_id = existing_id

            # Delete old clauses and re-import
            conn.execute("DELETE FROM clauses WHERE regulation_id=?", (existing_id,))
        else:
            # Insert new record
            cols = detect_insert_columns(conn, "regulations")
            placeholders = ", ".join(["?"] * len(cols))
            values = [
                item.get("title"),
                item.get("document_number"),
                item.get("issuing_authority", ""),
                item.get("authority_level", ""),
                item.get("effective_date", ""),
                item.get("status", "current"),
                item.get("domains", ""),
                item.get("category", ""),
                full_text,
                f'imported/{(doc_no or "unknown").split()[0]}.pdf',
                item.get("source_url", ""),
                0, "", "",
                item.get("page_count", 0),
                now, now,
            ]
            values = values[:len(cols)]
            cursor = conn.execute(f"INSERT INTO regulations ({', '.join([f'[{c}]' for c in cols])}) VALUES ({placeholders})", values)
            target_id = cursor.lastrowid

        # Step 2: Split and insert clauses
        clause_count = 0
        if full_text:
            clauses = ClauseSplitter.split(full_text, pattern)
            clause_cols = detect_insert_columns(conn, "clauses")
            if clause_cols:
                clause_placeholders = ", ".join(["?"] * len(clause_cols))

                for cl in clauses:
                    # Map clause fields to expected columns
                    cl_values = []
                    for cc in clause_cols:
                        if cc == "regulation_id":
                            cl_values.append(target_id)
                        elif cc == "article_number":
                            cl_values.append(cl.get("article_number", "")[:100])
                        elif cc == "content":
                            cl_values.append(cl.get("content", ""))
                        elif cc == "chapter":
                            cl_values.append(cl.get("chapter", "")[:100])
                        else:
                            cl_values.append("")  # Other fields as empty default

                    try:
                        conn.execute(
                            f"INSERT INTO clauses ({', '.join([f'[{c}]' for c in clause_cols])}) VALUES ({clause_placeholders})",
                            cl_values,
                        )
                        clause_count += 1
                    except sqlite3.Error:
                        pass  # Skip malformed clause rows

        # Step 3: Register in std_registry if it's a standard (has document_number like GB/AQ)
        std_registered = False
        if doc_no and any(doc_no.startswith(pfx) for pfx in ["GB", "AQ/T", "AQ "]):
            try:
                std_cols = detect_insert_columns(conn, "std_registry")
                if std_cols:
                    # Check if already registered
                    exists = conn.execute(
                        "SELECT COUNT(*) FROM std_registry WHERE standard_no LIKE ?",
                        (f"{doc_no.split()[0]}%",),
                    ).fetchone()[0]

                    if exists == 0:
                        std_vals = []
                        for sc in std_cols:
                            if sc == "standard_no":
                                std_vals.append(doc_no)
                            elif sc == "name":
                                std_vals.append(title)
                            elif sc == "status":
                                std_vals.append(item.get("status", "current"))
                            elif sc == "effective_date":
                                std_vals.append(item.get("effective_date", ""))
                            elif sc == "category":
                                std_vals.append(item.get("category", ""))
                            elif sc.replace("_v", "").endswith("date") and "create" in sc.lower():
                                std_vals.append(now)
                            elif sc.replace("_v", "").endswith("date") and "update" in sc.lower():
                                std_vals.append(now)
                            else:
                                std_vals.append("")
                        std_vals = std_vals[:len(std_cols)]
                        conn.execute(
                            f"INSERT INTO std_registry ({', '.join([f'[{c}]' for c in std_cols])}) VALUES ({', '.join(['?']*len(std_cols))})",
                            std_vals,
                        )
                        std_registered = True
                    else:
                        std_registered = True  # Already there
            except sqlite3.Error:
                pass

        return {
            "status": action if action != "updated_mismatch" else "updated",
            "document_number": doc_no,
            "title": title[:60],
            "regulation_id": target_id,
            "clause_count": clause_count,
            "std_registry_registered": std_registered,
            "text_length": len(full_text),
        }

    except sqlite3.Error as e:
        return {
            "status": "error",
            "document_number": doc_no,
            "title": title[:60],
            "error": str(e),
        }


def cmd_validate(args):
    """Validate a specific regulation's data quality."""
    conn = get_connection()
    reg_id = args.regulation_id

    row = conn.execute("SELECT * FROM regulations WHERE id=?", (reg_id,)).fetchone()
    if not row:
        print(json.dumps({"error": f"Regulation ID {reg_id} not found"}))
        conn.close()
        return

    issues = []

    # Check 1: Has content?
    text_len = len(row["full_text"] or "")
    if text_len < 50:
        issues.append({"check": "content_length", "severity": "high", "value": text_len, "message": "Content too short or empty"})

    # Check 2: Has clauses?
    cc = conn.execute("SELECT COUNT(*) FROM clauses WHERE regulation_id=?", (reg_id,)).fetchone()[0]
    if cc == 0:
        issues.append({"check": "clause_count", "severity": "medium", "value": 0, "message": "No clauses found"})
    elif cc < 5:
        issues.append({"check": "clause_count", "severity": "low", "value": cc, "message": "Very few clauses, splitting may have failed"})

    # Check 3: Document number format
    doc_no = row["document_number"]
    if doc_no:
        valid_prefixes = ["GB", "AQ", "国发", "安监", "应急部", "T/AQ"]
        if not any(doc_no.startswith(p) for p in valid_prefixes):
            issues.append({"check": "document_format", "severity": "low", "value": doc_no, "message": "Unusual document number format"})

    # Check 4: Title-content consistency
    title = row["title"] or ""
    full_text = row["full_text"] or ""
    if title and len(title) > 5 and full_text and title[:10] not in full_text[:200]:
        issues.append({"check": "title_content_match", "severity": "medium", "message": "Title doesn't appear near start of content"})

    report = {
        "regulation_id": reg_id,
        "document_number": doc_no,
        "title": title[:60],
        "is_valid": len([i for i in issues if i["severity"] in ("high", "medium")]) == 0,
        "issue_count": len(issues),
        "issues": issues,
        "stats": {"text_length": text_len, "clause_count": cc},
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))
    conn.close()


def cmd_schema(_args):
    """Print schema info."""
    conn = get_connection()
    schema = detect_schema(conn)
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name").fetchall()
    output = {"tables": [t["name"] for t in tables], "columns": schema}
    print(json.dumps(output, ensure_ascii=False, indent=2))
    conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Safety Review Knowledge Base Import Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # import
    p_imp = subparsers.add_parser("import", help="Import regulations from JSON manifest")
    p_imp.add_argument("--json", required=True, help="Path to manifest JSON file")
    p_imp.set_defaults(func=cmd_import)

    # extract-pdf
    p_ext = subparsers.add_parser("extract-pdf", help="Extract text from PDF file")
    p_ext.add_argument("pdf_path", help="Path to PDF file")
    p_ext.set_defaults(func=cmd_extract_pdf)

    # split-clauses
    p_split = subparsers.add_parser("split-clauses", help="Test clause splitting strategy")
    p_split.add_argument("--text", required=True, help="Text content to split")
    p_split.add_argument("--pattern", choices=["standard", "policy", "raw_lines"], default="standard", help="Splitting pattern")
    p_split.set_defaults(func=cmd_split_clauses)

    # validate
    p_val = subparsers.add_parser("validate", help="Validate data quality of a regulation")
    p_val.add_argument("regulation_id", type=int, help="Regulation ID to validate")
    p_val.set_defaults(func=cmd_validate)

    # schema
    p_sch = subparsers.add_parser("schema", help="Show database schema")
    p_sch.set_defaults(func=cmd_schema)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
