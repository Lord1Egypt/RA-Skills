#!/usr/bin/env python3
"""semantic_media.py — semantic search over an ACTIVE storage folder.

Part of the smart-storage-triage skill. Archives are NOT embedded — they stay on
tree-snapshot search (archive_find.py). Meaning-based search uses a LOCAL
multimodal EmbeddingGemma2 model (768d) served by an OpenAI-compatible embeddings
router (default http://127.0.0.1:18794). The router can fail over between backends
(e.g. a desktop PC -> a Raspberry Pi) running the SAME checkpoint: vectors are
interchangeable, so failover costs speed only — never quality — and never requires
reindexing. This is NOT a cloud Gemini API: everything runs on local hardware.

What gets indexed:
  image — jpg/jpeg/png/webp/heic/gif/bmp: content vector (1024px downscale);
  video — mp4/mov/mkv/avi/webm/m4v: 6 evenly spaced ffmpeg frames -> mean-pool;
  doc   — every other file: "filename | folder" text vector (search by NAME;
          full-text content search stays with storage_find.py).

Dedup by sha1 (images: full bytes; videos: first 1 MB + size). Incremental:
resume by size+mtime, errors stored and retried on the next run. The file list
comes from a gzip tree snapshot — no blind disk walks.

Configuration (resolution order: CLI > env > workspace-local > global config > defaults):
  Workspace-local binding: .smart-storage-triage.json (section "media") in the
  current directory or in an ancestor directory of the script copy (up to the
  workspace root). Lets each agent workspace bind its OWN storage root/tree/db
  without touching the shared global config; first match wins.
  Global: ~/.config/smart-storage-triage/config.json, section "media":
    root    — storage root (required), e.g. "/path/to/storage"
    active  — active-folder prefix relative to root, e.g. "ActiveFolder/"
              ("" = whole root; requires explicit --allow-broad confirmation)
    tree    — gzip tree snapshot path (default: <root>/tree.json.gz)
    router  — embeddings router base URL (default: http://127.0.0.1:18794).
              SECURITY: only LOOPBACK routers are accepted by default. A
              non-loopback router requires the explicit --allow-external-router
              flag (or STORAGE_MEDIA_ALLOW_EXTERNAL_ROUTER=1); a discovered
              workspace config can never silently redirect embeddings outside.
    db      — index DB path (default: ~/.local/share/semantic-media/index.db)
  Env overrides: STORAGE_MEDIA_ROOT / _ACTIVE / _TREE / _ROUTER / _DB.

Scope guards: tree-snapshot paths are validated to stay INSIDE the storage root
(no absolute paths, no '..', symlinks resolving outside are skipped), and the
secret denylist is applied to symlink RESOLVED targets as well as alias names.

Usage:
  python3 semantic_media.py search "query" [--limit 10] [--kind image|video|doc] [--json]
  python3 semantic_media.py index [--area SUBSTR] [--kind image|video|doc] [--force] [--max N]
  python3 semantic_media.py status

Indexing needs PIL + pillow-heif (HEIC photos); search needs only numpy.
The index DB is a local rebuildable cache; the storage itself is read-only.
"""
import argparse
import base64
import hashlib
import io
import ipaddress
import json
import os
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

MODEL = "embeddinggemma-2"
DIMS = 768
QUERY_PREFIX = "task: search result | query: "
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".gif", ".bmp"}
VID_EXT = {".mp4", ".mov", ".mkv", ".avi", ".webm", ".m4v"}
MAX_IMG_SIDE = 1024
JPEG_Q = 88
VIDEO_FRAMES = 6
DOC_BATCH = 32
HTTP_TIMEOUT = 300
# DENYLIST (exclusion list), NOT credential access: these names/patterns are
# skipped by the indexer so secret files are never read, embedded or listed.
SECRET_NAMES = {".env", "credentials.json", "token.json", "auth.json",
                "secrets.json", "id_rsa", "id_ed25519"}
SENSITIVE_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".pkcs12", ".kdbx"}
SENSITIVE_DIRS = {".ssh", ".aws", ".gnupg", ".azure", ".kube", ".secrets", "secrets"}

# Resolved by resolve_config() before any command runs.
ROOT = None
ACTIVE_PREFIX = ""
TREE_PATH = None
DB_PATH = None
DB_DIR = None
ROUTER = None
ALLOW_BROAD = False


def _local_media_config():
    """Per-workspace binding file .smart-storage-triage.json (section "media").

    Checked in CWD first, then in the script's ancestor directories (a skill
    copy lives inside its agent workspace). First match wins; this lets each
    agent bind its own storage root/tree/db while sharing one global default.
    """
    name = ".smart-storage-triage.json"
    candidates = [Path.cwd() / name]
    candidates += [p / name for p in Path(__file__).resolve().parents[:4]]
    for f in candidates:
        try:
            if f.is_file():
                data = json.loads(f.read_text(encoding="utf-8")) or {}
                return data.get("media", {}) or {}
        except Exception:
            continue
    return {}


def resolve_config(args=None):
    global ROOT, ACTIVE_PREFIX, TREE_PATH, DB_PATH, DB_DIR, ROUTER, ALLOW_BROAD
    cfg = {}
    cfg_file = Path.home() / ".config/smart-storage-triage/config.json"
    if cfg_file.exists():
        try:
            cfg = (json.loads(cfg_file.read_text(encoding="utf-8")) or {}).get("media", {}) or {}
        except Exception:
            cfg = {}
    # Broad-scope confirmation is honored ONLY from the user-owned global
    # config (or CLI/env) — never from an auto-discovered workspace file.
    ALLOW_BROAD = bool(cfg.get("allow_broad"))
    local = _local_media_config()
    if local:
        cfg = {**cfg, **local}

    def pick(cli, env, key, default=None):
        v = getattr(args, cli, None) if args is not None else None
        return v or os.environ.get(env) or cfg.get(key) or default

    ROOT = pick("root", "STORAGE_MEDIA_ROOT", "root")
    ACTIVE_PREFIX = pick("active", "STORAGE_MEDIA_ACTIVE", "active", "")
    TREE_PATH = pick("tree", "STORAGE_MEDIA_TREE", "tree")
    router_base = pick("router", "STORAGE_MEDIA_ROUTER", "router",
                       "http://127.0.0.1:18794")
    # SECURITY: embedding requests carry private media content and search
    # queries. Only LOOPBACK endpoints are accepted by default; an external
    # endpoint requires an explicit operator opt-in (--allow-external-router
    # or STORAGE_MEDIA_ALLOW_EXTERNAL_ROUTER=1). A workspace-discovered
    # .smart-storage-triage.json can NEVER silently enable an external router.
    parts = urllib.parse.urlsplit(router_base)
    if parts.scheme not in ("http", "https") or not parts.hostname:
        print("Invalid embeddings router URL: %r (http/https required)" % router_base,
              flush=True)
        sys.exit(2)
    host = parts.hostname
    # Strict loopback test: parse IP literals with ipaddress (a hostname like
    # "127.evil.example" is NOT loopback even though it starts with "127.");
    # only the exact name "localhost" is accepted as a non-IP loopback alias.
    try:
        is_loopback = ipaddress.ip_address(host).is_loopback
    except ValueError:
        is_loopback = host == "localhost"
    allow_ext = bool(getattr(args, "allow_external_router", False)) or \
        os.environ.get("STORAGE_MEDIA_ALLOW_EXTERNAL_ROUTER") == "1"
    if not is_loopback and not allow_ext:
        print("SECURITY: refusing non-loopback embeddings router %r.\n"
              "Private media/query data would leave this host. If this is truly\n"
              "intended, pass --allow-external-router explicitly (or set\n"
              "STORAGE_MEDIA_ALLOW_EXTERNAL_ROUTER=1)." % router_base, flush=True)
        sys.exit(2)
    ROUTER = router_base.rstrip("/") + "/v1/embeddings"
    db = pick("db", "STORAGE_MEDIA_DB", "db")
    DB_PATH = Path(db).expanduser() if db else Path.home() / ".local/share/semantic-media/index.db"
    DB_DIR = DB_PATH.parent
    if not ROOT:
        print("media.root is not configured. Set the 'media' section in "
              "~/.config/smart-storage-triage/config.json (root/active/tree/router/db) "
              "or env STORAGE_MEDIA_ROOT.", flush=True)
        sys.exit(2)
    if not TREE_PATH:
        TREE_PATH = os.path.join(ROOT, "tree.json.gz")


def log(msg):
    print(msg, flush=True)


def now_iso():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


# ---------- tree ----------

def path_of(it):
    if isinstance(it, str):
        return it
    if "path" in it:
        return it["path"]
    d = (it.get("d") or "").strip("/")
    f = it.get("f") or ""
    return f"{d}/{f}" if d else f


def _sensitive_rel(rel):
    """Denylist check on a relative path (alias OR resolved symlink target)."""
    name = rel.rsplit("/", 1)[-1].lower()
    if name.startswith(".") or name in SECRET_NAMES:
        return True
    if name.startswith(".env") or name.endswith(".env"):
        return True
    if any(name.endswith(s) for s in SENSITIVE_SUFFIXES):
        return True
    dirs = {p.lower() for p in Path(rel).parts[:-1]}
    return bool(dirs & SENSITIVE_DIRS)


def safe_abs_path(rel):
    """Resolve a tree-snapshot relative path strictly INSIDE the storage root.

    SECURITY: tree snapshots are data, not trust. Absolute paths, '..'
    traversal and symlinks resolving outside ROOT are rejected, so a crafted
    snapshot entry cannot make the indexer read (and embed) out-of-scope files.
    Returns the resolved absolute path, or None when out of boundary.
    """
    if not rel or rel.startswith("/") or rel.startswith("\\"):
        return None
    if ".." in Path(rel).parts:
        return None
    root_real = os.path.realpath(ROOT)
    ap = os.path.realpath(os.path.join(ROOT, rel))
    if ap != root_real and not ap.startswith(root_real + os.sep):
        return None
    return ap


def load_active_paths():
    import gzip
    with open(TREE_PATH, "rb") as fh:
        data = json.loads(gzip.open(fh, "rt").read())
    files = data.get("files") if isinstance(data, dict) else data
    out = []
    skipped_scope = 0
    root_real = os.path.realpath(ROOT)
    for it in files:
        p = path_of(it)
        if ACTIVE_PREFIX and not p.startswith(ACTIVE_PREFIX):
            continue
        if _sensitive_rel(p):
            continue
        ap = safe_abs_path(p)
        if ap is None:
            skipped_scope += 1
            continue
        # Symlink-alias protection: apply the denylist to the RESOLVED target
        # too, so notes.txt -> .env inside the root cannot bypass exclusion.
        try:
            rel_resolved = os.path.relpath(ap, root_real)
        except ValueError:
            skipped_scope += 1
            continue
        if _sensitive_rel(rel_resolved):
            continue
        out.append(p)
    if skipped_scope:
        log("[scope] skipped %d out-of-boundary tree entries" % skipped_scope)
    return sorted(out)


def classify(path):
    e = Path(path).suffix.lower()
    if e in IMG_EXT:
        return "image"
    if e in VID_EXT:
        return "video"
    return "doc"


# ---------- db ----------

def db_connect():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH), timeout=30)
    con.execute("PRAGMA journal_mode=WAL")
    con.execute("""CREATE TABLE IF NOT EXISTS items(
        path TEXT PRIMARY KEY, kind TEXT NOT NULL, ext TEXT,
        size INTEGER, mtime INTEGER, hash TEXT, vec BLOB,
        error TEXT, indexed_at TEXT)""")
    con.execute("CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v TEXT)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_items_hash ON items(hash)")
    con.execute("CREATE INDEX IF NOT EXISTS idx_items_kind ON items(kind)")
    return con


def vec_to_blob(v):
    import numpy as np
    a = np.asarray(v, dtype=np.float32)
    n = float(np.linalg.norm(a))
    if n > 0:
        a = a / n
    return a.tobytes()


def blob_to_vec(b):
    import numpy as np
    return np.frombuffer(b, dtype=np.float32)


# ---------- embeddings ----------

def embed_post(items, retries=2):
    body = json.dumps({"input": items, "model": MODEL}).encode("utf-8")
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(
                ROUTER, data=body, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                out = json.loads(r.read())
            data = sorted(out["data"], key=lambda d: d["index"])
            import numpy as np
            return np.array([d["embedding"] for d in data], dtype=np.float32)
        except urllib.error.HTTPError as e:
            last = "HTTP %s: %s" % (e.code, e.read()[:300])
        except Exception as e:
            last = "%s: %s" % (type(e).__name__, e)
        if attempt < retries:
            time.sleep(3)
    raise RuntimeError("embed failed: %s" % last)


def register_heif():
    try:
        import pillow_heif
        pillow_heif.register_heif_opener()
        return True
    except ImportError:
        return False


def image_bytes_to_data_url(raw):
    from PIL import Image
    im = Image.open(io.BytesIO(raw))
    im = im.convert("RGB")
    im.thumbnail((MAX_IMG_SIDE, MAX_IMG_SIDE))
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=JPEG_Q)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def sha1_bytes(raw):
    return hashlib.sha1(raw).hexdigest()


def video_frame_urls(abs_path):
    """6 evenly spaced frames via ffmpeg (fast seek), each -> data URL.

    SECURITY: fixed argv lists, shell=False; abs_path was validated by
    safe_abs_path() to stay inside the configured storage root. No user input
    can alter the command structure -> no command injection.
    """
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "json", abs_path],
        capture_output=True, timeout=60)
    if probe.returncode != 0:
        raise RuntimeError("ffprobe: %s" % probe.stderr.decode()[:200])
    dur = float(json.loads(probe.stdout)["format"]["duration"])
    if dur <= 0:
        raise RuntimeError("zero duration")
    urls = []
    for i in range(VIDEO_FRAMES):
        t = dur * (i + 0.5) / VIDEO_FRAMES
        fr = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", "%.3f" % t, "-i", abs_path,
             "-frames:v", "1", "-f", "image2", "-vcodec", "mjpeg", "pipe:1"],
            capture_output=True, timeout=180)
        if fr.returncode != 0 or not fr.stdout:
            raise RuntimeError("ffmpeg frame %d: %s" % (i, fr.stderr.decode()[:200]))
        urls.append(image_bytes_to_data_url(fr.stdout))
    return urls


def mean_pool(vecs):
    import numpy as np
    m = vecs.mean(axis=0)
    n = float(np.linalg.norm(m))
    return m / n if n > 0 else m


# ---------- index ----------

def cmd_index(args):
    import numpy as np
    # SECURITY: an empty active prefix means the WHOLE storage root would be
    # indexed and sent to the embeddings router. Require explicit confirmation
    # (CLI flag, env, or the user-owned global config) before proceeding.
    if not ACTIVE_PREFIX:
        allow_broad = bool(getattr(args, "allow_broad", False)) or \
            os.environ.get("STORAGE_MEDIA_ALLOW_BROAD") == "1" or ALLOW_BROAD
        if not allow_broad:
            log("SECURITY: active prefix is empty — the whole storage root would be "
                "indexed. Confirm the scope explicitly: pass --allow-broad, set "
                "media.allow_broad=true in the GLOBAL config, or "
                "STORAGE_MEDIA_ALLOW_BROAD=1.")
            sys.exit(2)
    heif_ok = register_heif()
    paths = load_active_paths()
    if args.area:
        paths = [p for p in paths if args.area in p]
    if args.kind:
        paths = [p for p in paths if classify(p) == args.kind]
    con = db_connect()
    existing = {r[0]: r for r in con.execute(
        "SELECT path,size,mtime,hash,vec IS NOT NULL,error FROM items")}
    dedup = {}
    for h, v in con.execute(
            "SELECT hash,vec FROM items WHERE vec NOT NULL AND hash NOT NULL"):
        dedup.setdefault(h, v)
    stats = {"indexed": 0, "skipped": 0, "dedup": 0, "errors": 0, "missing": 0}
    t0 = time.time()
    processed = 0

    def upsert(path, kind, size, mtime, h, vec, error):
        con.execute(
            "INSERT INTO items(path,kind,ext,size,mtime,hash,vec,error,indexed_at) "
            "VALUES(?,?,?,?,?,?,?,?,?) ON CONFLICT(path) DO UPDATE SET "
            "kind=excluded.kind,ext=excluded.ext,size=excluded.size,"
            "mtime=excluded.mtime,hash=excluded.hash,vec=excluded.vec,"
            "error=excluded.error,indexed_at=excluded.indexed_at",
            (path, kind, Path(path).suffix.lower(), size, mtime, h,
             vec_to_blob(vec) if vec is not None else None, error, now_iso()))
        con.commit()

    def fresh(path, size, mtime):
        row = existing.get(path)
        return (not args.force and row and row[1] == size and row[2] == mtime
                and row[4] and not row[5])

    media = [p for p in paths if classify(p) in ("image", "video")]
    docs = [p for p in paths if classify(p) == "doc"]
    media.sort(key=lambda p: (classify(p) != "image", p))  # images first
    log("[index] root=%s active=%r files=%d (media=%d docs=%d) area=%r kind=%r force=%s"
        % (ROOT, ACTIVE_PREFIX, len(paths), len(media), len(docs),
           args.area, args.kind, args.force))

    for p in media:
        if args.max and processed >= args.max:
            break
        abs_path = safe_abs_path(p)
        if abs_path is None:
            stats["missing"] += 1
            continue
        kind = classify(p)
        try:
            st = os.stat(abs_path)
        except OSError:
            if p in existing:
                con.execute("DELETE FROM items WHERE path=?", (p,))
                con.commit()
            stats["missing"] += 1
            continue
        size, mtime = st.st_size, int(st.st_mtime)
        if fresh(p, size, mtime):
            stats["skipped"] += 1
            continue
        processed += 1
        try:
            if kind == "image":
                if p.lower().endswith(".heic") and not heif_ok:
                    raise RuntimeError("pillow-heif not installed")
                with open(abs_path, "rb") as fh:
                    raw = fh.read()
                h = sha1_bytes(raw)
                if h in dedup:
                    upsert(p, kind, size, mtime, h, blob_to_vec(dedup[h]), None)
                    stats["dedup"] += 1
                else:
                    url = image_bytes_to_data_url(raw)
                    v = embed_post([{"image": url}])[0]
                    upsert(p, kind, size, mtime, h, v, None)
                    dedup[h] = vec_to_blob(v)
                    stats["indexed"] += 1
            else:
                with open(abs_path, "rb") as fh:
                    head = fh.read(1024 * 1024)
                h = sha1_bytes(head + str(size).encode())
                if h in dedup:
                    upsert(p, kind, size, mtime, h, blob_to_vec(dedup[h]), None)
                    stats["dedup"] += 1
                else:
                    urls = video_frame_urls(abs_path)
                    vecs = embed_post([{"image": u} for u in urls])
                    v = mean_pool(vecs)
                    upsert(p, kind, size, mtime, h, v, None)
                    dedup[h] = vec_to_blob(v)
                    stats["indexed"] += 1
        except Exception as e:
            upsert(p, kind, size, mtime, None, None,
                   "%s: %s" % (type(e).__name__, str(e)[:300]))
            stats["errors"] += 1
            log("[index] ERROR %s: %s" % (p, str(e)[:200]))
        if processed % 20 == 0:
            el = time.time() - t0
            log("[index] media %d/%d done, %.0fs elapsed, %.1fs/item"
                % (processed, len(media), el, el / max(processed, 1)))
        if args.max and processed >= args.max:
            break

    # docs: batched by filename
    pending = []
    for p in docs:
        if args.max and processed >= args.max:
            break
        abs_path = safe_abs_path(p)
        if abs_path is None:
            stats["missing"] += 1
            continue
        try:
            st = os.stat(abs_path)
        except OSError:
            if p in existing:
                con.execute("DELETE FROM items WHERE path=?", (p,))
                con.commit()
            stats["missing"] += 1
            continue
        size, mtime = st.st_size, int(st.st_mtime)
        if fresh(p, size, mtime):
            stats["skipped"] += 1
            continue
        name = p.rsplit("/", 1)[-1]
        parent = str(Path(p).parent)
        text = "%s | folder: %s" % (name, parent)
        pending.append((p, size, mtime, text))
    for i in range(0, len(pending), DOC_BATCH):
        if args.max and processed >= args.max:
            break
        chunk = pending[i:i + DOC_BATCH]
        texts = [c[3] for c in chunk]
        try:
            vecs = embed_post(texts)
            for (p, size, mtime, text), v in zip(chunk, vecs):
                upsert(p, "doc", size, mtime, sha1_bytes(text.encode()), v, None)
                stats["indexed"] += 1
                processed += 1
        except Exception as e:
            for p, size, mtime, text in chunk:
                upsert(p, "doc", size, mtime, None, None,
                       "%s: %s" % (type(e).__name__, str(e)[:300]))
                stats["errors"] += 1
                processed += 1
            log("[index] DOC BATCH ERROR: %s" % str(e)[:200])
        log("[index] docs %d/%d" % (min(i + DOC_BATCH, len(pending)), len(pending)))

    el = time.time() - t0
    con.execute("INSERT INTO meta(k,v) VALUES('last_run',?) "
                "ON CONFLICT(k) DO UPDATE SET v=excluded.v", (now_iso(),))
    con.execute("INSERT INTO meta(k,v) VALUES('model',?) "
                "ON CONFLICT(k) DO UPDATE SET v=excluded.v", (MODEL,))
    con.commit()
    log("[index] DONE in %.0fs: %s" % (el, json.dumps(stats, ensure_ascii=False)))
    con.close()


# ---------- search ----------

def cmd_search(args):
    import numpy as np
    if not DB_PATH.exists():
        log("Index is empty. Run: python3 semantic_media.py index")
        sys.exit(1)
    con = db_connect()
    rows = list(con.execute(
        "SELECT path,kind,hash,mtime,vec FROM items WHERE vec NOT NULL"))
    con.close()
    if not rows:
        log("No vectors in the index. Run: python3 semantic_media.py index")
        sys.exit(1)
    M = np.stack([blob_to_vec(r[4]) for r in rows])
    qv = embed_post([QUERY_PREFIX + args.query])[0]
    scores = M @ qv
    order = np.argsort(-scores)
    seen = set()
    out = []
    for idx in order:
        path, kind, h, mtime, _ = rows[idx]
        if args.kind and kind != args.kind:
            continue
        if h and h in seen:
            continue
        if h:
            seen.add(h)
        out.append({"score": round(float(scores[idx]), 4), "kind": kind,
                    "path": os.path.join(ROOT, path), "rel": path,
                    "mtime": mtime})
        if len(out) >= args.limit:
            break
    if args.json:
        print(json.dumps({"query": args.query, "total_indexed": len(rows),
                          "results": out}, ensure_ascii=False, indent=1))
    else:
        icon = {"image": "🖼", "video": "🎬", "doc": "📄"}
        log("Query: %s  (%d files indexed)" % (args.query, len(rows)))
        for r in out:
            d = datetime.fromtimestamp(r["mtime"]).strftime("%d.%m.%Y") if r["mtime"] else "?"
            log("%.3f %s [%s] %s  (%s)" % (r["score"], icon.get(r["kind"], "?"),
                                           r["kind"], r["rel"], d))


# ---------- status ----------

def cmd_status(args):
    if not DB_PATH.exists():
        log("Index not created yet:", DB_PATH)
        return
    con = db_connect()
    counts = dict(con.execute(
        "SELECT kind, COUNT(*) FROM items WHERE vec NOT NULL GROUP BY kind"))
    errs = con.execute(
        "SELECT COUNT(*) FROM items WHERE error IS NOT NULL").fetchone()[0]
    uniq = con.execute(
        "SELECT COUNT(DISTINCT hash) FROM items WHERE vec NOT NULL").fetchone()[0]
    meta = dict(con.execute("SELECT k,v FROM meta"))
    con.close()
    tree_total = len(load_active_paths())
    indexed = sum(counts.values())
    log("DB: %s (%.1f MB)" % (DB_PATH, DB_PATH.stat().st_size / 1e6))
    log("Indexed: %d/%d active-folder files (%.0f%%)"
        % (indexed, tree_total, 100.0 * indexed / max(tree_total, 1)))
    log("By kind: %s | unique vectors: %d | errors: %d"
        % (json.dumps(counts, ensure_ascii=False), uniq, errs))
    log("Last run: %s | model: %s"
        % (meta.get("last_run", "?"), meta.get("model", "?")))
    if errs:
        con = db_connect()
        for p, e in con.execute(
                "SELECT path,error FROM items WHERE error IS NOT NULL LIMIT 10"):
            log("  ERR %s: %s" % (p, e[:120]))
        con.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", help="storage root (overrides config/env)")
    common.add_argument("--active", help="active-folder prefix relative to root")
    common.add_argument("--tree", help="gzip tree snapshot path")
    common.add_argument("--router", help="embeddings router base URL")
    common.add_argument("--db", help="index DB path")
    common.add_argument("--allow-external-router", action="store_true",
                        help="explicitly allow a NON-loopback embeddings router "
                             "(private media/query data would leave this host)")
    common.add_argument("--allow-broad", action="store_true",
                        help="explicitly confirm indexing the WHOLE storage root "
                             "when the active prefix is empty")
    sub = ap.add_subparsers(dest="cmd", required=True)
    pi = sub.add_parser("index", parents=[common], help="incremental indexing")
    pi.add_argument("--area", help="only paths containing this substring")
    pi.add_argument("--kind", choices=["image", "video", "doc"])
    pi.add_argument("--force", action="store_true", help="re-embed everything")
    pi.add_argument("--max", type=int, help="stop after N processed files")
    pi.set_defaults(fn=cmd_index)
    ps = sub.add_parser("search", parents=[common], help="semantic search")
    ps.add_argument("query")
    ps.add_argument("--limit", type=int, default=10)
    ps.add_argument("--kind", choices=["image", "video", "doc"])
    ps.add_argument("--json", action="store_true")
    ps.set_defaults(fn=cmd_search)
    pt = sub.add_parser("status", parents=[common], help="index state")
    pt.set_defaults(fn=cmd_status)
    args = ap.parse_args()
    resolve_config(args)
    args.fn(args)


if __name__ == "__main__":
    main()
