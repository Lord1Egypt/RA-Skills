#!/usr/bin/env python3
"""
triage_index.py - Universal smart indexer with dynamic age-based triage,
long path protection, multi-encoding resilience (Windows-1251, UTF-8 BOM, UTF-16, CP866),
and strict credential/secret exclusion.
"""

import gzip
import json
import os
import sqlite3
import sys
import time
from pathlib import Path

IGNORE_DIRS = {
    ".git", ".svn", ".hg", "node_modules", "venv", ".venv", "env",
    "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache",
    "dist", "build", "target", ".idea", ".vscode", ".next", ".nuxt",
    ".ssh", ".aws", ".gnupg", ".azure", ".kube", ".secrets", "secrets"
}

SENSITIVE_FILE_EXACT = {
    ".env", "credentials.json", "token.json", "auth.json", "secrets.json",
    "id_rsa", "id_ed25519", "id_ecdsa", "id_dsa"
}

SENSITIVE_SUFFIXES = {
    ".pem", ".key", ".pkcs12", ".pfx", ".p12", ".kdbx", ".cert", ".crt"
}

ARCHIVE_DIR_KEYWORDS = {"archive", "архив", "backup", "бэкап", "backups", "old"}

TEXT_EXTS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java", ".c", ".cpp",
    ".h", ".hpp", ".cs", ".php", ".rb", ".sh", ".bash", ".zsh", ".sql",
    ".html", ".css", ".scss", ".json", ".yaml", ".yml", ".toml", ".ini",
    ".md", ".markdown", ".txt", ".rst", ".csv", ".tsv", ".dockerfile"
}

DOC_EXTS = {".pdf", ".docx", ".xlsx"}

def is_sensitive_file(filename: str, rel_path: str) -> bool:
    """Checks if a file or path is a private credential or secret to prevent data leakage."""
    lower_name = filename.lower()
    if lower_name.startswith(".env"):
        return True
    if lower_name in SENSITIVE_FILE_EXACT:
        return True
    for sfx in SENSITIVE_SUFFIXES:
        if lower_name.endswith(sfx):
            return True
    parts = set(p.lower() for p in Path(rel_path).parts[:-1])
    if parts & {".ssh", ".aws", ".gnupg", ".azure", ".kube", ".secrets", "secrets"}:
        return True
    return False

def normalize_windows_path(p: Path) -> str:
    """Bypasses Windows MAX_PATH (260 chars) by adding \\\\?\\ prefix if needed."""
    s = str(p)
    if os.name == "nt" and len(s) > 240 and not s.startswith("\\\\?\\"):
        return "\\\\?\\" + os.path.abspath(s)
    return s

def safe_str(s: str) -> str:
    """Guarantees valid UTF-8 without surrogate encoding crashes."""
    if not isinstance(s, str):
        s = str(s)
    return s.encode("utf-8", errors="replace").decode("utf-8", errors="replace")

def smart_decode_bytes(b: bytes) -> str:
    """Auto-detects Windows (CP1251, CP866) and Unicode (UTF-8, UTF-8-BOM, UTF-16) encodings."""
    if not b:
        return ""
    if b.startswith(b"\xef\xbb\xbf"):
        return b.decode("utf-8-sig", errors="replace")
    if b.startswith(b"\xff\xfe") or b.startswith(b"\xfe\xff"):
        return b.decode("utf-16", errors="replace")

    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        pass

    try:
        return b.decode("cp1251")
    except UnicodeDecodeError:
        pass

    try:
        decoded = b.decode("cp866")
        if any(0x0400 <= ord(c) <= 0x04FF for c in decoded):
            return decoded
    except UnicodeDecodeError:
        pass

    return b.decode("utf-8", errors="replace")

def extract_text_file(path: Path):
    try:
        norm_path = normalize_windows_path(path)
        with open(norm_path, "rb") as f:
            raw = f.read(10 * 1024 * 1024)
        text = smart_decode_bytes(raw)
        lines = text.splitlines(keepends=True)
    except Exception:
        return []

    if not lines:
        return []

    chunks = []
    chunk_size = 40
    step = 30

    for i in range(0, len(lines), step):
        chunk_lines = lines[i:i + chunk_size]
        start_line = i + 1
        content = "".join(chunk_lines).strip()
        if content:
            chunks.append((start_line, content))
        if i + chunk_size >= len(lines):
            break

    return chunks

def extract_pdf_file(path: Path):
    try:
        import pypdf
        reader = pypdf.PdfReader(normalize_windows_path(path))
        chunks = []
        for idx, page in enumerate(reader.pages):
            txt = (page.extract_text() or "").strip()
            if txt:
                chunks.append((idx + 1, txt))
        return chunks
    except Exception:
        return []

def extract_docx_file(path: Path):
    try:
        from docx import Document
        doc = Document(normalize_windows_path(path))
        text = "\n".join([p.text for p in doc.paragraphs if p.text.strip()])
        return [(1, text)] if text else []
    except Exception:
        return []

def extract_xlsx_file(path: Path):
    try:
        import openpyxl
        wb = openpyxl.load_workbook(normalize_windows_path(path), read_only=True, data_only=True)
        chunks = []
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            rows_text = []
            for row in ws.iter_rows(values_only=True):
                r_vals = [str(v).strip() for v in row if v is not None and str(v).strip()]
                if r_vals:
                    rows_text.append(" | ".join(r_vals))
            sheet_content = "\n".join(rows_text).strip()
            if sheet_content:
                chunks.append((sheet, sheet_content[:20000]))
        return chunks
    except Exception:
        return []

def extract_document(path: Path, ext: str):
    if ext in TEXT_EXTS or path.name.lower() in ("dockerfile", "makefile"):
        return extract_text_file(path)
    elif ext == ".pdf":
        return extract_pdf_file(path)
    elif ext == ".docx":
        return extract_docx_file(path)
    elif ext == ".xlsx":
        return extract_xlsx_file(path)
    return []

def init_database(db_path: Path):
    conn = sqlite3.connect(str(db_path))
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS files_meta (
            rel_path TEXT PRIMARY KEY,
            mtime REAL,
            size INTEGER,
            indexed_at REAL
        )
    """)
    c.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
            file_name,
            rel_path,
            page_num,
            content,
            tokenize='porter unicode61'
        )
    """)
    conn.commit()
    return conn

def is_in_archive_folder(rel_path: str) -> bool:
    parts = set(p.lower() for p in Path(rel_path).parts[:-1])
    return bool(parts & ARCHIVE_DIR_KEYWORDS)

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__.strip())
        sys.exit(0)

    target_dir = Path(sys.argv[1]).resolve()
    if not target_dir.exists() or not target_dir.is_dir():
        print(f"❌ Target directory not found: {target_dir}")
        sys.exit(1)

    db_path = target_dir / "storage_rag.db"
    tree_path = target_dir / "tree.json.gz"
    force_rebuild = False
    full_workdir_mode = False
    allow_broad = False
    active_days = 365.0

    idx = 2
    while idx < len(sys.argv):
        arg = sys.argv[idx]
        if arg == "--db" and idx + 1 < len(sys.argv):
            db_path = Path(sys.argv[idx + 1]).resolve()
            idx += 2
        elif arg == "--tree" and idx + 1 < len(sys.argv):
            tree_path = Path(sys.argv[idx + 1]).resolve()
            idx += 2
        elif arg in ("--active-days", "--days") and idx + 1 < len(sys.argv):
            try:
                active_days = float(sys.argv[idx + 1])
            except ValueError:
                pass
            idx += 2
        elif arg in ("--full", "--workdir", "-w"):
            full_workdir_mode = True
            idx += 1
        elif arg in ("--allow-broad", "--force-broad"):
            allow_broad = True
            idx += 1
        elif arg == "--force":
            force_rebuild = True
            idx += 1
        else:
            idx += 1

    # Scope Guard: prevent broad accidental indexing of system root or home directory without explicit approval
    resolved_root = Path("/").resolve()
    resolved_home = Path.home().resolve()
    is_broad = (
        target_dir == resolved_root
        or target_dir == resolved_home
        or target_dir == Path("/home").resolve()
        or target_dir == Path("/root").resolve()
    )
    if is_broad and not allow_broad:
        print("❌ Safety Scope Guard: Direct indexing of root '/' or entire home '~' directory is restricted.", file=sys.stderr)
        print("   To index this broad scope, pass the explicit confirmation flag '--allow-broad'.", file=sys.stderr)
        sys.exit(1)

    print(f"📂 Target: {target_dir}")
    print(f"⚙️ Mode: {'FULL WORKDIR (all files fully indexed)' if full_workdir_mode else f'DYNAMIC TRIAGE (active: <{int(active_days)} days)'}")
    print(f"🗄️ Database: {db_path}")
    print(f"📦 Tree Snapshot: {tree_path}")

    conn = init_database(db_path)
    c = conn.cursor()

    if force_rebuild:
        c.execute("DELETE FROM chunks_fts")
        c.execute("DELETE FROM files_meta")
        conn.commit()

    existing_meta = {}
    for r in c.execute("SELECT rel_path, mtime, size FROM files_meta").fetchall():
        existing_meta[r[0]] = (r[1], r[2])

    now = time.time()
    all_files_for_tree = []
    all_dirs_for_tree = []
    active_indexed_count = 0
    archived_tree_only_count = 0
    skipped_unchanged_count = 0
    sensitive_skipped_count = 0
    chunks_added = 0

    t0 = time.time()
    print("⏳ Scanning storage with intelligent age triage & security denylist...")

    for root, dirs, files in os.walk(str(target_dir)):
        # Prune ignored directories and symlink directories to prevent escaping target boundaries or loops
        dirs[:] = [
            d for d in dirs
            if d not in IGNORE_DIRS
            and not d.startswith(".")
            and not d.lower().startswith(".env")
            and not (Path(root) / d).is_symlink()
        ]

        for d in dirs:
            dir_path = Path(root) / d
            rel_d = safe_str(str(dir_path.relative_to(target_dir)))
            all_dirs_for_tree.append(rel_d)

        for file in files:
            file_path = Path(root) / file

            # Symlink protection: ensure symlink files do not resolve outside target_dir
            if file_path.is_symlink():
                try:
                    resolved_file = file_path.resolve()
                    if not resolved_file.is_relative_to(target_dir):
                        continue
                except Exception:
                    continue

            rel_path = safe_str(str(file_path.relative_to(target_dir)))

            # Strict security denylist: exclude sensitive credentials/secrets from BOTH FTS and tree snapshot!
            if is_sensitive_file(file, rel_path):
                sensitive_skipped_count += 1
                continue

            all_files_for_tree.append(rel_path)

            ext = file_path.suffix.lower()
            if ext not in TEXT_EXTS and ext not in DOC_EXTS and file.lower() not in ("dockerfile", "makefile"):
                continue

            try:
                norm_p = normalize_windows_path(file_path)
                stat = os.stat(norm_p)
                mtime = stat.st_mtime
                size = stat.st_size
            except Exception:
                continue

            if size > 10 * 1024 * 1024:
                continue

            age_days = (now - mtime) / 86400.0
            is_archive = False
            if not full_workdir_mode:
                if age_days >= active_days or is_in_archive_folder(rel_path):
                    is_archive = True

            if is_archive:
                archived_tree_only_count += 1
                c.execute("DELETE FROM chunks_fts WHERE rel_path = ?", (rel_path,))
                c.execute("DELETE FROM files_meta WHERE rel_path = ?", (rel_path,))
                continue

            prev = existing_meta.get(rel_path)
            if prev and prev[0] == mtime and prev[1] == size:
                skipped_unchanged_count += 1
                continue

            c.execute("DELETE FROM chunks_fts WHERE rel_path = ?", (rel_path,))

            chunks = extract_document(file_path, ext)
            for page_or_line, content in chunks:
                c.execute("""
                    INSERT INTO chunks_fts (file_name, rel_path, page_num, content)
                    VALUES (?, ?, ?, ?)
                """, (safe_str(file), rel_path, str(page_or_line), safe_str(content)))
                chunks_added += 1

            c.execute("""
                INSERT OR REPLACE INTO files_meta (rel_path, mtime, size, indexed_at)
                VALUES (?, ?, ?, ?)
            """, (rel_path, mtime, size, now))

            active_indexed_count += 1

    conn.commit()
    conn.close()

    with gzip.open(tree_path, "wt", encoding="utf-8") as f:
        json.dump({"root": str(target_dir), "dirs": all_dirs_for_tree, "files": all_files_for_tree}, f)

    dt = time.time() - t0
    print(f"\n✅ Indexing finished in {dt:.2f}s!")
    print(f"   - Total dirs tracked in tree: {len(all_dirs_for_tree)}")
    print(f"   - Total files tracked in tree: {len(all_files_for_tree)}")
    print(f"   - Active files deeply indexed: {active_indexed_count} (skipped unchanged: {skipped_unchanged_count})")
    print(f"   - Archived files (> {int(active_days)}d untouched, tree-only): {archived_tree_only_count}")
    print(f"   - Sensitive/secret files excluded: {sensitive_skipped_count}")
    print(f"   - Total searchable chunks in FTS: {chunks_added}")
    print(f"   - Compressed tree snapshot size: {os.path.getsize(tree_path) / 1024:.1f} KB")

if __name__ == "__main__":
    main()
