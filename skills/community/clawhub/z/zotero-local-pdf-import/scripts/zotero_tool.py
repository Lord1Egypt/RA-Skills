import argparse
import glob
import json
import os
import sqlite3
import subprocess
import sys
import time
import uuid
from typing import List, Optional

try:
    import requests
except Exception:
    requests = None

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
try:
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

os.environ.setdefault("PYTHONIOENCODING", "utf-8")
os.environ.setdefault("PYTHONUTF8", "1")


def _file_url(path: str) -> str:
    return "file:///" + os.path.abspath(path).replace("\\", "/")


def _zotero_headers() -> dict:
    return {"Zotero-API-Version": "3"}


def get_collections(port: int, timeout: int = 20) -> list:
    if requests is None:
        raise RuntimeError("requests not installed; run: python -m pip install requests")
    url = f"http://127.0.0.1:{port}/api/users/0/collections?limit=10000"
    r = requests.get(url, headers=_zotero_headers(), timeout=timeout)
    r.raise_for_status()
    return r.json()


def find_collection_key_by_name(name: str, port: int, timeout: int = 20) -> Optional[str]:
    cols = get_collections(port, timeout)
    for c in cols:
        if c.get("data", {}).get("name") == name:
            return c.get("key")
    low = name.lower()
    for c in cols:
        if c.get("data", {}).get("name", "").lower() == low:
            return c.get("key")
    return None


def _open_zotero_url(url: str):
    if sys.platform.startswith("win"):
        os.startfile(url)  # type: ignore[attr-defined]
    elif sys.platform == "darwin":
        subprocess.run(["open", url], check=True)
    else:
        subprocess.run(["xdg-open", url], check=True)
    time.sleep(1.2)


def select_collection_by_key(key: str):
    _open_zotero_url(f"zotero://select/library/collections/{key}")


def select_my_library():
    _open_zotero_url("zotero://select/library/items")


def import_one_pdf(pdf_path: str, port: int, timeout: int) -> tuple[int, str]:
    if requests is None:
        raise RuntimeError("requests not installed; run: python -m pip install requests")
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    metadata = {"sessionID": str(uuid.uuid4()), "url": _file_url(pdf_path)}
    headers = {"X-Metadata": json.dumps(metadata, ensure_ascii=True), "Content-Type": "application/pdf"}

    with open(pdf_path, "rb") as f:
        data = f.read()

    endpoint = f"http://127.0.0.1:{port}/connector/saveStandaloneAttachment"
    r = requests.post(endpoint, headers=headers, data=data, timeout=timeout)
    return r.status_code, r.text


def _normalize_pick_tokens(picks: Optional[List[str]]) -> List[str]:
    if not picks:
        return []
    out: List[str] = []
    for item in picks:
        parts = [p.strip() for p in item.split(",") if p.strip()]
        out.extend(parts)
    return out


def _pick_from_directory(directory: str, pick_tokens: List[str], recursive: bool) -> List[str]:
    if not pick_tokens:
        return []

    all_pdfs = glob.glob(os.path.join(directory, "**/*.pdf" if recursive else "*.pdf"), recursive=recursive)
    by_abs = {os.path.abspath(p): os.path.abspath(p) for p in all_pdfs}

    by_base: dict[str, List[str]] = {}
    for p in all_pdfs:
        by_base.setdefault(os.path.basename(p).lower(), []).append(os.path.abspath(p))

    selected: List[str] = []
    for token in pick_tokens:
        t = token.strip().strip('"').strip("'")
        if not t:
            continue

        if os.path.isabs(t):
            ap = os.path.abspath(t)
            if ap in by_abs:
                selected.append(ap)
                continue

        ap2 = os.path.abspath(os.path.join(directory, t))
        if ap2 in by_abs:
            selected.append(ap2)
            continue

        base_key = os.path.basename(t).lower()
        matched = by_base.get(base_key, [])
        if len(matched) == 1:
            selected.append(matched[0])
        elif len(matched) > 1:
            raise RuntimeError(f"ambiguous pick token: {token} (matched {len(matched)} files)")
        else:
            raise FileNotFoundError(f"pick file not found in dir: {token}")

    return selected


def gather_pdfs(pdf_list: Optional[List[str]], directory: Optional[str], recursive: bool, pick_tokens: Optional[List[str]] = None) -> List[str]:
    files: List[str] = []
    if pdf_list:
        files.extend(pdf_list)
    if directory:
        if pick_tokens:
            files.extend(_pick_from_directory(directory, pick_tokens, recursive=recursive))
        else:
            pattern = "**/*.pdf" if recursive else "*.pdf"
            files.extend(glob.glob(os.path.join(directory, pattern), recursive=recursive))

    seen = set()
    out: List[str] = []
    for f in files:
        af = os.path.abspath(f)
        if af not in seen:
            seen.add(af)
            out.append(af)
    return out


def check_recent_attachments(db_path: str, limit: int) -> list:
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"DB not found: {db_path}")
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro&immutable=1"
    con = sqlite3.connect(uri, uri=True)
    cur = con.cursor()
    q = """
    SELECT i.itemID, idv.value as title, ia.path, i.dateAdded
    FROM items i
    JOIN itemTypes t ON t.itemTypeID=i.itemTypeID AND t.typeName='attachment'
    LEFT JOIN itemAttachments ia ON ia.itemID=i.itemID
    LEFT JOIN itemData id ON id.itemID=i.itemID
      AND id.fieldID=(SELECT fieldID FROM fields WHERE fieldName='title')
    LEFT JOIN itemDataValues idv ON idv.valueID=id.valueID
    ORDER BY i.itemID DESC
    LIMIT ?
    """
    cur.execute(q, (limit,))
    rows = cur.fetchall()
    con.close()
    return rows


def cmd_import(args: argparse.Namespace) -> int:
    if args.collection:
        key = find_collection_key_by_name(args.collection, port=args.port, timeout=args.timeout)
        if not key:
            print("error=collection not found")
            return 3
        select_collection_by_key(key)
        print(f"info=selected collection: {args.collection} ({key})")
    else:
        select_my_library()
        print("info=selected target: 我的文库")

    picks = _normalize_pick_tokens(args.pick)
    pdfs = gather_pdfs(args.pdf, args.dir, args.recursive, pick_tokens=picks)
    if not pdfs:
        print("error=no PDF files found")
        return 4

    ok = 0
    fail = 0
    for p in pdfs:
        try:
            status, body = import_one_pdf(p, port=args.port, timeout=args.timeout)
            if status == 201:
                ok += 1
                print(f"ok={p}")
            else:
                fail += 1
                print(f"fail={p} status={status} body={(body or '')[:300]}")
        except Exception as e:
            fail += 1
            print(f"fail={p} error={e}")

    print(f"summary=ok:{ok} fail:{fail} total:{len(pdfs)}")
    return 0 if fail == 0 else 5


def cmd_check(args: argparse.Namespace) -> int:
    rows = check_recent_attachments(args.db, args.limit)
    for r in rows:
        print(r)
    return 0


def cmd_list_collections(args: argparse.Namespace) -> int:
    cols = get_collections(port=args.port, timeout=args.timeout)
    for c in cols:
        data = c.get("data", {})
        print(f"{c.get('key')}\t{data.get('name')}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    ok = True
    print(f"python_executable={sys.executable}")
    print(f"python_version={sys.version.split()[0]}")

    req_mod = requests
    if req_mod is None:
        print("dep_requests=missing")
        if args.auto_install_deps:
            print("dep_requests=installing")
            r = subprocess.run([sys.executable, "-m", "pip", "install", "requests>=2.31.0"], capture_output=True, text=True)
            if r.returncode != 0:
                print("dep_requests=install_failed")
                print((r.stderr or r.stdout or "").strip()[:500])
                return 10
            import importlib
            req_mod = importlib.import_module("requests")
            print(f"dep_requests=installed version={getattr(req_mod, '__version__', 'unknown')}")
        else:
            print("hint=run: python -m pip install requests>=2.31.0")
            return 10
    else:
        print(f"dep_requests=ok version={getattr(req_mod, '__version__', 'unknown')}")

    try:
        r = req_mod.get(f"http://127.0.0.1:{args.port}/connector/ping", timeout=5)
        print(f"connector_ping_status={r.status_code}")
        if r.status_code != 200:
            ok = False
            print("connector_ping=fail")
    except Exception as e:
        ok = False
        print(f"connector_ping=fail error={e}")

    try:
        if sys.platform.startswith("win"):
            print("url_opener=ok method=os.startfile")
        elif sys.platform == "darwin":
            r = subprocess.run(["which", "open"], capture_output=True, text=True)
            print("url_opener=ok method=open" if r.returncode == 0 else "url_opener=fail missing=open")
            ok = ok and (r.returncode == 0)
        else:
            r = subprocess.run(["which", "xdg-open"], capture_output=True, text=True)
            print("url_opener=ok method=xdg-open" if r.returncode == 0 else "url_opener=fail missing=xdg-open")
            ok = ok and (r.returncode == 0)
    except Exception as e:
        ok = False
        print(f"url_opener=fail error={e}")

    print("doctor=ok" if ok else "doctor=fail")
    return 0 if ok else 11


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Zotero local import/check tool (Python-only)")
    sub = p.add_subparsers(dest="command", required=True)

    p_doctor = sub.add_parser("doctor", help="Check Python/runtime/dependencies/connector availability")
    p_doctor.add_argument("--port", type=int, default=int(os.getenv("ZOTERO_PORT", "23119")), help="Zotero local port")
    p_doctor.add_argument("--auto-install-deps", action="store_true", help="Automatically install missing Python dependencies")
    p_doctor.set_defaults(func=cmd_doctor)

    p_import = sub.add_parser("import", help="Import one/multiple PDFs or a whole directory")
    p_import.add_argument("--pdf", action="append", help="PDF path (repeat this arg to pass multiple PDFs)")
    p_import.add_argument("--dir", help="directory containing PDFs")
    p_import.add_argument("--recursive", action="store_true", help="recursive when using --dir")
    p_import.add_argument("--pick", action="append", help="pick specific PDF(s) inside --dir (repeatable, comma-separated supported)")
    p_import.add_argument("--collection", help="target collection name (must already exist in local mode)")
    p_import.add_argument("--port", type=int, default=int(os.getenv("ZOTERO_PORT", "23119")), help="Zotero local port")
    p_import.add_argument("--timeout", type=int, default=90, help="HTTP timeout seconds")
    p_import.set_defaults(func=cmd_import)

    p_check = sub.add_parser("check", help="Check recent attachments in zotero.sqlite")
    p_check.add_argument("--db", default=os.path.join(os.path.expanduser("~"), "Zotero", "zotero.sqlite"), help="path to zotero.sqlite")
    p_check.add_argument("--limit", type=int, default=10)
    p_check.set_defaults(func=cmd_check)

    p_cols = sub.add_parser("list-collections", help="List available collections from local API")
    p_cols.add_argument("--port", type=int, default=int(os.getenv("ZOTERO_PORT", "23119")))
    p_cols.add_argument("--timeout", type=int, default=20)
    p_cols.set_defaults(func=cmd_list_collections)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "import":
        if (not args.pdf) and (not args.dir):
            print("error=for import, provide --pdf (one or more) or --dir")
            return 2
        if args.pdf and args.dir:
            print("error=choose one input source: (--pdf ... repeated) OR --dir")
            return 2
        if args.pick and (not args.dir):
            print("error=--pick only works with --dir")
            return 2

    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
