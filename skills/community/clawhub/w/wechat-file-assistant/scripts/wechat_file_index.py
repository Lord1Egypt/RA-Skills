#!/usr/bin/env python3
"""Read-only WeChat file catalog with a local SQLite index."""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET

TEXT_EXTENSIONS = {
    ".txt", ".md", ".csv", ".tsv", ".json", ".xml", ".yaml", ".yml",
    ".log", ".ini", ".py", ".js", ".ts", ".html", ".css", ".sql",
}
OFFICE_EXTENSIONS = {".docx", ".xlsx"}
PDF_EXTENSIONS = {".pdf"}
EXTRACTABLE_EXTENSIONS = TEXT_EXTENSIONS | OFFICE_EXTENSIONS | PDF_EXTENSIONS
MAX_CONTENT_CHARS = 200_000


def emit(payload: dict, exit_code: int = 0) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(exit_code)


def default_db_path() -> Path:
    base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
    return base / "Codex" / "wechat-file-finder" / "index.sqlite3"


def canonical(path: str | Path) -> str:
    return os.path.normcase(os.path.abspath(os.fspath(path)))


def discover_roots(explicit: list[str] | None = None) -> list[Path]:
    candidates: list[Path] = []
    if explicit:
        candidates.extend(Path(item).expanduser() for item in explicit)
    else:
        configured = os.environ.get("WECHAT_FILE_ROOTS", "")
        if configured:
            candidates.extend(Path(item) for item in configured.split(";") if item.strip())
        documents = Path.home() / "Documents"
        candidates.extend([documents / "WeChat Files", documents / "xwechat_files"])
        for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            drive = Path(f"{letter}:\\")
            if not drive.exists():
                continue
            candidates.extend([
                drive / "xwechat_files",
                drive / "WeChat Files",
                drive / "wechat" / "WeChat Files",
                drive / "weixin" / "WeChat Files",
            ])
    result: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        try:
            if not candidate.is_dir():
                continue
            key = canonical(candidate)
            if key not in seen:
                seen.add(key)
                result.append(Path(os.path.abspath(candidate)))
        except OSError:
            continue
    return result


def content_directories(root: Path, explicit: bool) -> list[Path]:
    """Narrow known WeChat layouts; custom roots remain fully searchable."""
    result: list[Path] = []
    if root.name.lower() == "xwechat_files":
        for account in root.iterdir():
            if not account.is_dir():
                continue
            for relative in (("msg", "file"), ("msg", "attach")):
                candidate = account.joinpath(*relative)
                if candidate.is_dir():
                    result.append(candidate)
    elif root.name.lower() == "wechat files":
        for account in root.iterdir():
            if not account.is_dir():
                continue
            for relative in (("FileStorage", "File"), ("Files",)):
                candidate = account.joinpath(*relative)
                if candidate.is_dir():
                    result.append(candidate)
    return result or [root]


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA foreign_keys=ON")
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS files (
            path TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            extension TEXT NOT NULL,
            size_bytes INTEGER NOT NULL,
            mtime_ns INTEGER NOT NULL,
            last_write_time TEXT NOT NULL,
            root TEXT NOT NULL,
            account_hint TEXT,
            sha256 TEXT,
            content TEXT,
            content_status TEXT NOT NULL,
            sender TEXT,
            sent_at TEXT,
            chat TEXT,
            metadata_source TEXT,
            scan_id TEXT NOT NULL,
            indexed_at TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_files_name ON files(name COLLATE NOCASE);
        CREATE INDEX IF NOT EXISTS idx_files_extension ON files(extension);
        CREATE INDEX IF NOT EXISTS idx_files_mtime ON files(mtime_ns DESC);
        CREATE INDEX IF NOT EXISTS idx_files_sha256 ON files(sha256);
        CREATE INDEX IF NOT EXISTS idx_files_root ON files(root);
        CREATE TABLE IF NOT EXISTS index_info (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )
    return connection


def decode_text_file(path: Path) -> tuple[str, str]:
    data = path.read_bytes()[: 4 * 1024 * 1024]
    for encoding in ("utf-8-sig", "utf-8", "gb18030", "utf-16"):
        try:
            return data.decode(encoding)[:MAX_CONTENT_CHARS], "extracted"
        except UnicodeDecodeError:
            continue
    return "", "decode_failed"


def extract_docx(path: Path) -> tuple[str, str]:
    with zipfile.ZipFile(path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    parts = [node.text for node in root.iter() if node.tag.endswith("}t") and node.text]
    return "\n".join(parts)[:MAX_CONTENT_CHARS], "extracted"


def extract_xlsx(path: Path) -> tuple[str, str]:
    parts: list[str] = []
    with zipfile.ZipFile(path) as archive:
        names = archive.namelist()
        if "xl/sharedStrings.xml" in names:
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            parts.extend(node.text for node in root.iter() if node.tag.endswith("}t") and node.text)
        for name in names:
            if re.fullmatch(r"xl/worksheets/sheet\d+\.xml", name):
                root = ET.fromstring(archive.read(name))
                parts.extend(node.text for node in root.iter() if node.text and node.tag.endswith(("}v", "}t")))
                if sum(len(item) for item in parts) >= MAX_CONTENT_CHARS:
                    break
    return "\n".join(parts)[:MAX_CONTENT_CHARS], "extracted"


def extract_pdf(path: Path) -> tuple[str, str]:
    try:
        with path.open("rb") as handle:
            if handle.read(5) != b"%PDF-":
                return "", "invalid_pdf_header"
    except OSError:
        return "", "extract_failed:OSError"
    try:
        from pypdf import PdfReader  # type: ignore

        reader = PdfReader(str(path))
        parts: list[str] = []
        for page in reader.pages:
            parts.append(page.extract_text() or "")
            if sum(len(item) for item in parts) >= MAX_CONTENT_CHARS:
                break
        text = "\n".join(parts)[:MAX_CONTENT_CHARS]
        return text, "extracted" if text.strip() else "no_text_or_scanned_pdf"
    except ImportError:
        return "", "pdf_dependency_unavailable"


def extract_content(path: Path) -> tuple[str, str]:
    extension = path.suffix.lower()
    if extension not in EXTRACTABLE_EXTENSIONS:
        return "", "unsupported_type"
    try:
        if extension in TEXT_EXTENSIONS:
            return decode_text_file(path)
        if extension == ".docx":
            return extract_docx(path)
        if extension == ".xlsx":
            return extract_xlsx(path)
        if extension == ".pdf":
            return extract_pdf(path)
    except Exception as exc:
        return "", f"extract_failed:{type(exc).__name__}"
    return "", "unsupported_type"


def hash_file(path: Path, max_bytes: int) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except OSError:
        return None


def account_hint(path: Path, root: Path) -> str | None:
    try:
        relative = path.relative_to(root)
    except ValueError:
        return None
    first = relative.parts[0] if relative.parts else ""
    if first.lower() in {"msg", "filestorage", "files"}:
        return root.parent.name or None
    return first if re.match(r"^(wxid_|Q\d|[A-Za-z0-9_-]+_[A-Fa-f0-9]{4,})", first) else None


def iter_files(directories: Iterable[Path]) -> Iterable[Path]:
    for directory in directories:
        for current, dirnames, filenames in os.walk(directory):
            dirnames[:] = [name for name in dirnames if name.lower() not in {"cache", "temp", "thumb", "thumbnail"}]
            for filename in filenames:
                yield Path(current) / filename


def build_index(args: argparse.Namespace) -> None:
    roots = discover_roots(args.root)
    if not roots:
        emit({"status": "no_roots", "roots": [], "database": str(args.database)})
    connection = connect(args.database)
    scan_id = f"{int(time.time())}-{os.getpid()}"
    counters = {"scanned": 0, "added": 0, "updated": 0, "unchanged": 0, "errors": 0, "removed": 0}
    max_hash_bytes = args.hash_max_mb * 1024 * 1024
    explicit = bool(args.root)

    for root in roots:
        directories = content_directories(root, explicit)
        for path in iter_files(directories):
            if args.max_files and counters["scanned"] >= args.max_files:
                break
            counters["scanned"] += 1
            try:
                stat = path.stat()
                absolute = canonical(path)
                row = connection.execute(
                    "SELECT size_bytes, mtime_ns, content, content_status, sha256 FROM files WHERE path = ?",
                    (absolute,),
                ).fetchone()
                unchanged = row and row["size_bytes"] == stat.st_size and row["mtime_ns"] == stat.st_mtime_ns
                if unchanged:
                    content, status, digest = row["content"], row["content_status"], row["sha256"]
                    counters["unchanged"] += 1
                else:
                    content, status = extract_content(path)
                    digest = hash_file(path, max_hash_bytes)
                    counters["updated" if row else "added"] += 1
                timestamp = dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc).astimezone().isoformat()
                connection.execute(
                    """
                    INSERT INTO files(path,name,extension,size_bytes,mtime_ns,last_write_time,root,account_hint,
                                      sha256,content,content_status,scan_id,indexed_at)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(path) DO UPDATE SET
                        name=excluded.name, extension=excluded.extension, size_bytes=excluded.size_bytes,
                        mtime_ns=excluded.mtime_ns, last_write_time=excluded.last_write_time, root=excluded.root,
                        account_hint=excluded.account_hint, sha256=excluded.sha256, content=excluded.content,
                        content_status=excluded.content_status, scan_id=excluded.scan_id, indexed_at=excluded.indexed_at
                    """,
                    (absolute, path.name, path.suffix.lower(), stat.st_size, stat.st_mtime_ns, timestamp,
                     canonical(root), account_hint(path, root), digest, content, status, scan_id,
                     dt.datetime.now(dt.timezone.utc).isoformat()),
                )
                if counters["scanned"] % 250 == 0:
                    connection.commit()
            except (OSError, sqlite3.Error):
                counters["errors"] += 1
        if args.max_files and counters["scanned"] >= args.max_files:
            break

    if not args.max_files:
        for root in roots:
            cursor = connection.execute("DELETE FROM files WHERE root = ? AND scan_id <> ?", (canonical(root), scan_id))
            counters["removed"] += cursor.rowcount
    connection.execute("INSERT OR REPLACE INTO index_info(key,value) VALUES('last_build',?)", (dt.datetime.now().astimezone().isoformat(),))
    connection.execute("INSERT OR REPLACE INTO index_info(key,value) VALUES('roots',?)", (json.dumps([str(root) for root in roots], ensure_ascii=False),))
    connection.commit()
    total = connection.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    connection.close()
    emit({"status": "ok", "database": str(args.database), "roots": [str(root) for root in roots], "total_indexed": total, **counters})


def parse_date(value: str | None, end: bool = False) -> int | None:
    if not value:
        return None
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.astimezone()
    if end and len(value) == 10:
        parsed += dt.timedelta(days=1)
    return int(parsed.timestamp() * 1_000_000_000)


def search_index(args: argparse.Namespace) -> None:
    if not args.database.exists():
        emit({"status": "index_missing", "database": str(args.database), "hint": "run build first"})
    connection = connect(args.database)
    clauses: list[str] = []
    params: list[object] = []
    query = (args.query or "").strip()
    if query:
        if args.exact_name:
            clauses.append("name = ? COLLATE NOCASE")
            params.append(query)
        elif args.content_only:
            clauses.append("instr(lower(COALESCE(content,'')), lower(?)) > 0")
            params.append(query)
        else:
            clauses.append("(instr(lower(name), lower(?)) > 0 OR instr(lower(COALESCE(content,'')), lower(?)) > 0)")
            params.extend([query, query])
    if args.extension:
        extension = args.extension.lower()
        if not extension.startswith("."):
            extension = "." + extension
        clauses.append("extension = ?")
        params.append(extension)
    since = parse_date(args.since)
    before = parse_date(args.before, end=False)
    if since is not None:
        clauses.append("mtime_ns >= ?")
        params.append(since)
    if before is not None:
        clauses.append("mtime_ns < ?")
        params.append(before)
    if args.min_size is not None:
        clauses.append("size_bytes >= ?")
        params.append(args.min_size)
    if args.max_size is not None:
        clauses.append("size_bytes <= ?")
        params.append(args.max_size)
    where = " WHERE " + " AND ".join(clauses) if clauses else ""
    rows = connection.execute(
        "SELECT * FROM files" + where + " ORDER BY mtime_ns DESC, name COLLATE NOCASE LIMIT ?",
        (*params, args.limit),
    ).fetchall()
    results = []
    lowered = query.lower()
    for row in rows:
        content = row["content"] or ""
        position = content.lower().find(lowered) if lowered else -1
        snippet = None
        if position >= 0:
            snippet = re.sub(r"\s+", " ", content[max(0, position - 80):position + len(query) + 120]).strip()
        results.append({
            "name": row["name"], "path": row["path"], "extension": row["extension"],
            "size_bytes": row["size_bytes"], "last_write_time": row["last_write_time"],
            "last_write_time_source": "filesystem", "account_hint": row["account_hint"],
            "content_status": row["content_status"], "content_match_snippet": snippet,
            "sha256": row["sha256"], "sender": row["sender"], "sent_at": row["sent_at"],
            "chat": row["chat"], "metadata_source": row["metadata_source"],
        })
    connection.close()
    emit({"status": "ok", "database": str(args.database), "query": query, "match_count_returned": len(results), "results": results})


def duplicate_groups(args: argparse.Namespace) -> None:
    if not args.database.exists():
        emit({"status": "index_missing", "database": str(args.database)})
    connection = connect(args.database)
    groups = connection.execute(
        """SELECT sha256, size_bytes, COUNT(*) AS count
           FROM files WHERE sha256 IS NOT NULL
           GROUP BY sha256, size_bytes HAVING COUNT(*) > 1
           ORDER BY size_bytes * COUNT(*) DESC LIMIT ?""",
        (args.limit,),
    ).fetchall()
    payload = []
    for group in groups:
        files = connection.execute("SELECT path,last_write_time FROM files WHERE sha256=? ORDER BY mtime_ns DESC", (group["sha256"],)).fetchall()
        payload.append({"sha256": group["sha256"], "size_bytes": group["size_bytes"], "count": group["count"], "files": [dict(row) for row in files]})
    connection.close()
    emit({"status": "ok", "duplicate_group_count": len(payload), "groups": payload})


def import_metadata(args: argparse.Namespace) -> None:
    if not args.database.exists():
        emit({"status": "index_missing", "database": str(args.database)})
    source_path = args.input
    if source_path.suffix.lower() == ".csv":
        with source_path.open("r", encoding="utf-8-sig", newline="") as handle:
            records = list(csv.DictReader(handle))
    elif source_path.suffix.lower() in {".jsonl", ".ndjson"}:
        records = [json.loads(line) for line in source_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    else:
        parsed = json.loads(source_path.read_text(encoding="utf-8"))
        records = parsed if isinstance(parsed, list) else [parsed]
    connection = connect(args.database)
    matched = 0
    for record in records:
        path = record.get("path")
        if not path:
            continue
        cursor = connection.execute(
            "UPDATE files SET sender=?,sent_at=?,chat=?,metadata_source=? WHERE path=?",
            (record.get("sender"), record.get("sent_at"), record.get("chat"), record.get("source") or str(source_path), canonical(path)),
        )
        matched += cursor.rowcount
    connection.commit()
    connection.close()
    emit({"status": "ok", "records_read": len(records), "records_matched": matched, "source": str(source_path)})


def status(args: argparse.Namespace) -> None:
    if not args.database.exists():
        emit({"status": "index_missing", "database": str(args.database), "discovered_roots": [str(item) for item in discover_roots()]})
    connection = connect(args.database)
    total = connection.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    extracted = connection.execute("SELECT COUNT(*) FROM files WHERE content_status='extracted'").fetchone()[0]
    metadata = connection.execute("SELECT COUNT(*) FROM files WHERE metadata_source IS NOT NULL").fetchone()[0]
    last_build_row = connection.execute("SELECT value FROM index_info WHERE key='last_build'").fetchone()
    connection.close()
    emit({"status": "ok", "database": str(args.database), "total_indexed": total, "content_extracted": extracted, "verified_metadata_records": metadata, "last_build": last_build_row[0] if last_build_row else None})


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Incremental local index for WeChat files")
    result.add_argument("--database", type=Path, default=default_db_path())
    commands = result.add_subparsers(dest="command", required=True)

    build = commands.add_parser("build")
    build.add_argument("--root", action="append")
    build.add_argument("--hash-max-mb", type=int, default=100)
    build.add_argument("--max-files", type=int, default=0, help="Test/debug limit; disables stale-row cleanup")
    build.set_defaults(handler=build_index)

    search = commands.add_parser("search")
    search.add_argument("query", nargs="?", default="")
    search.add_argument("--exact-name", action="store_true")
    search.add_argument("--content-only", action="store_true")
    search.add_argument("--extension")
    search.add_argument("--since")
    search.add_argument("--before")
    search.add_argument("--min-size", type=int)
    search.add_argument("--max-size", type=int)
    search.add_argument("--limit", type=int, default=20)
    search.set_defaults(handler=search_index)

    duplicates = commands.add_parser("duplicates")
    duplicates.add_argument("--limit", type=int, default=20)
    duplicates.set_defaults(handler=duplicate_groups)

    metadata = commands.add_parser("import-metadata")
    metadata.add_argument("input", type=Path)
    metadata.set_defaults(handler=import_metadata)

    inspect = commands.add_parser("status")
    inspect.set_defaults(handler=status)
    return result


def main() -> None:
    args = parser().parse_args()
    args.database = Path(args.database).expanduser()
    args.handler(args)


if __name__ == "__main__":
    main()
