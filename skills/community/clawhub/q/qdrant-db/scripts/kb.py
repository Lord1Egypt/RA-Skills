#!/usr/bin/env python3
"""OpenClaw Qdrant knowledge-base CLI."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

# 配置文件随 skill 走：<skill根>/.env（scripts/ 的上一级），shell 风格 KEY=VALUE
# 代码不内置默认值：配置统一从 真实环境变量 > .env 读取，模板见 env.example
ENV_FILE = Path(__file__).resolve().parent.parent / ".env"


def eprint(*args: Any) -> None:
    print(*args, file=sys.stderr)


def load_env_file(path: Path) -> dict[str, str]:
    """解析 shell 风格 .env：KEY=VALUE、export 前缀、单/双引号、# 注释、空行。
    不做变量展开/行内注释，保持简单可预期。"""
    out: dict[str, str] = {}
    if not path.exists():
        return out
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except Exception as err:
        eprint(f"warning: cannot read {path}: {err}")
        return out
    for lineno, raw in enumerate(lines, 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        if "=" not in line:
            eprint(f"warning: {path}:{lineno}: skipped malformed line (no '=')")
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if not key or not key.replace("_", "").replace("-", "").isalnum() or key[0].isdigit():
            eprint(f"warning: {path}:{lineno}: skipped invalid key '{key}'")
            continue
        # 去引号（单/双引号都可，不做内部展开）
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        out[key] = val
    return out


def settings_from_env() -> dict[str, Any]:
    """所有配置统一从环境变量读取，代码不内置默认值。

    注入顺序（setdefault，不覆盖已存在的真实 env）：
    1. 真实环境变量（最高优先）
    2. <skill根>/.env
    缺 QDRANT_URL / QDRANT_COLLECTION 直接报错并提示复制 env.example；
    Embedding 配置允许为空，留给 embed_texts 按需报错（如 migrate-sqlite 不需要）。
    """
    kc = load_env_file(ENV_FILE)
    for name, val in kc.items():
        os.environ.setdefault(name, val)

    missing = [
        key
        for key in ("QDRANT_URL", "QDRANT_COLLECTION")
        if not os.environ.get(key, "").strip()
    ]
    if missing:
        raise SystemExit(
            "Missing env config: "
            + ", ".join(missing)
            + f"\nCopy {ENV_FILE.parent / 'env.example'} to {ENV_FILE} and fill in values."
        )

    try:
        dims = int(os.environ.get("EMBEDDING_DIMS") or 0)
    except ValueError:
        raise SystemExit(f"Invalid EMBEDDING_DIMS: {os.environ['EMBEDDING_DIMS']!r}")

    return {
        "qdrant_url": os.environ["QDRANT_URL"].rstrip("/"),
        "qdrant_api_key": os.environ.get("QDRANT_API_KEY", ""),
        "collection": os.environ["QDRANT_COLLECTION"].strip(),
        "embed_base": os.environ.get("EMBEDDING_BASE_URL", "").rstrip("/"),
        "embed_key": os.environ.get("EMBEDDING_API_KEY", ""),
        "embed_model": os.environ.get("EMBEDDING_MODEL", ""),
        "dims": dims,
    }


def http_json(
    url: str,
    *,
    method: str = "GET",
    body: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 60.0,
) -> Any:
    data = None if body is None else json.dumps(body).encode("utf-8")
    hdrs = {"Accept": "application/json"}
    if body is not None:
        hdrs["Content-Type"] = "application/json"
    if headers:
        hdrs.update(headers)
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", "replace")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as err:
        detail = err.read().decode("utf-8", "replace")
        raise SystemExit(f"HTTP {err.code} {method} {url}\n{detail}") from err
    except urllib.error.URLError as err:
        raise SystemExit(f"URL error {method} {url}: {err}") from err


def qdrant_headers(cfg: dict[str, Any]) -> dict[str, str]:
    h: dict[str, str] = {}
    if cfg.get("qdrant_api_key"):
        h["api-key"] = cfg["qdrant_api_key"]
    return h


def embed_texts(cfg: dict[str, Any], texts: list[str]) -> list[list[float]]:
    missing_embed = [
        name
        for name, val in (
            ("EMBEDDING_BASE_URL", cfg.get("embed_base")),
            ("EMBEDDING_API_KEY", cfg.get("embed_key")),
            ("EMBEDDING_MODEL", cfg.get("embed_model")),
        )
        if not val
    ]
    if missing_embed:
        raise SystemExit(
            "Missing embedding config: "
            + ", ".join(missing_embed)
            + f". Fill them in {ENV_FILE} (see env.example)."
        )
    url = cfg["embed_base"] + "/embeddings"
    body = {"model": cfg["embed_model"], "input": texts if len(texts) > 1 else texts[0]}
    headers = {"Authorization": f"Bearer {cfg['embed_key']}"}
    data = http_json(url, method="POST", body=body, headers=headers, timeout=120.0)
    items = data.get("data") or []
    if not items:
        raise SystemExit(f"Empty embedding response: {json.dumps(data)[:500]}")
    # OpenAI-style may return unsorted; sort by index when present
    items = sorted(items, key=lambda x: x.get("index", 0))
    vectors = [list(map(float, it["embedding"])) for it in items]
    if len(vectors) != len(texts):
        raise SystemExit(f"Embedding count mismatch: got {len(vectors)} want {len(texts)}")
    dim = len(vectors[0])
    if dim != cfg["dims"]:
        eprint(f"warning: embedding dim {dim} != configured {cfg['dims']}; using actual dim")
        cfg["dims"] = dim
    return vectors


def ensure_collection(cfg: dict[str, Any], dims: int | None = None) -> None:
    coll = cfg["collection"]
    base = cfg["qdrant_url"]
    try:
        http_json(f"{base}/collections/{coll}", headers=qdrant_headers(cfg))
        return
    except SystemExit:
        # 可能 404（不存在）或瞬时错误：再列一次确认，避免把鉴权/网络错误当"不存在"直接建库
        listed = http_json(f"{base}/collections", headers=qdrant_headers(cfg))
        names = {c.get("name") for c in (listed.get("result") or {}).get("collections") or []}
        if coll in names:
            return
    http_json(
        f"{base}/collections/{coll}",
        method="PUT",
        body={"vectors": {"size": int(dims or cfg["dims"]), "distance": "Cosine"}},
        headers=qdrant_headers(cfg),
    )


def chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> list[str]:
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    # split by markdown headings / blank lines first
    parts = re.split(r"\n(?=#{1,6}\s)|\n{2,}", text)
    parts = [p.strip() for p in parts if p and p.strip()]
    chunks: list[str] = []
    buf = ""
    for part in parts:
        if len(part) <= max_chars:
            if buf and len(buf) + 2 + len(part) > max_chars:
                chunks.append(buf.strip())
                buf = part
            else:
                buf = f"{buf}\n\n{part}".strip() if buf else part
            continue
        # hard wrap long part
        if buf:
            chunks.append(buf.strip())
            buf = ""
        start = 0
        while start < len(part):
            end = min(len(part), start + max_chars)
            chunks.append(part[start:end].strip())
            if end >= len(part):
                break
            start = max(0, end - overlap)
    if buf.strip():
        chunks.append(buf.strip())
    return [c for c in chunks if c]


def cmd_ensure(cfg: dict[str, Any]) -> None:
    # probe embedding dims
    vecs = embed_texts(cfg, ["dimension probe"])
    ensure_collection(cfg, dims=len(vecs[0]))
    print(json.dumps({"ok": True, "collection": cfg["collection"], "dims": len(vecs[0])}, ensure_ascii=False))


def cmd_collections(cfg: dict[str, Any]) -> None:
    data = http_json(f"{cfg['qdrant_url']}/collections", headers=qdrant_headers(cfg))
    print(json.dumps(data.get("result") or data, ensure_ascii=False, indent=2))


def cmd_info(cfg: dict[str, Any]) -> None:
    coll = cfg["collection"]
    data = http_json(f"{cfg['qdrant_url']}/collections/{coll}", headers=qdrant_headers(cfg))
    safe_cfg = {
        "qdrant_url": cfg["qdrant_url"],
        "collection": coll,
        "embed_base": cfg["embed_base"],
        "embed_model": cfg["embed_model"],
        "dims": cfg["dims"],
        "has_embed_key": bool(cfg.get("embed_key")),
    }
    print(json.dumps({"config": safe_cfg, "collection": data.get("result") or data}, ensure_ascii=False, indent=2))


def qdrant_point_id(raw_id: str) -> str:
    """Qdrant accepts UUID or unsigned int; map arbitrary ids to 32-hex."""
    s = str(raw_id).strip()
    if re.fullmatch(r"[0-9a-fA-F]{32}", s):
        return s.lower()
    if re.fullmatch(
        r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}",
        s,
    ):
        return s.lower()
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:32]


def put_points(cfg: dict[str, Any], body_points: list[dict[str, Any]]) -> int:
    if not body_points:
        return 0
    ensure_collection(cfg, dims=len(body_points[0]["vector"]))
    upserted = 0
    for i in range(0, len(body_points), 32):
        batch = body_points[i : i + 32]
        http_json(
            f"{cfg['qdrant_url']}/collections/{cfg['collection']}/points?wait=true",
            method="PUT",
            body={"points": batch},
            headers=qdrant_headers(cfg),
            timeout=120.0,
        )
        upserted += len(batch)
    return upserted


def upsert_points(cfg: dict[str, Any], points: list[dict[str, Any]]) -> dict[str, Any]:
    if not points:
        return {"status": "ok", "upserted": 0}
    texts = [p["payload"]["text"] for p in points]
    vectors = embed_texts(cfg, texts)
    body_points = []
    for p, vec in zip(points, vectors):
        body_points.append({"id": p["id"], "vector": vec, "payload": p["payload"]})
    upserted = put_points(cfg, body_points)
    return {"status": "ok", "upserted": upserted, "collection": cfg["collection"]}


def cmd_upsert(cfg: dict[str, Any], args: argparse.Namespace) -> None:
    text = args.text
    if args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    if not text or not str(text).strip():
        raise SystemExit("empty text")
    source = args.source or (args.file or "manual")
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    pid = args.id or qdrant_point_id(f"{source}\n{text.strip()}")
    payload = {
        "text": text.strip(),
        "source": source,
        "tags": tags,
        "created_at": int(time.time()),
    }
    if args.meta:
        extra = json.loads(args.meta)
        if not isinstance(extra, dict):
            raise SystemExit("--meta must be a JSON object")
        payload.update(extra)
    result = upsert_points(cfg, [{"id": pid, "payload": payload}])
    result["id"] = pid
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_upsert_file(cfg: dict[str, Any], args: argparse.Namespace) -> None:
    path = Path(args.path)
    raw = path.read_text(encoding="utf-8")
    chunks = chunk_text(raw, max_chars=args.max_chars, overlap=args.overlap)
    if not chunks:
        raise SystemExit("no chunks from file")
    source = args.source or str(path)
    tags = [t.strip() for t in (args.tags or "").split(",") if t.strip()]
    points = []
    for i, ch in enumerate(chunks):
        pid = hashlib.sha256(f"{source}#{i}\n{ch}".encode("utf-8")).hexdigest()[:32]
        points.append(
            {
                "id": pid,
                "payload": {
                    "text": ch,
                    "source": source,
                    "chunk": i,
                    "tags": tags,
                    "created_at": int(time.time()),
                },
            }
        )
    result = upsert_points(cfg, points)
    result["chunks"] = len(chunks)
    result["source"] = source
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_search(cfg: dict[str, Any], args: argparse.Namespace) -> None:
    query = args.query
    vec = embed_texts(cfg, [query])[0]
    ensure_collection(cfg, dims=len(vec))
    body: dict[str, Any] = {
        "vector": vec,
        "limit": args.top_k,
        "with_payload": True,
        "with_vector": False,
    }
    if args.score_threshold is not None:
        body["score_threshold"] = args.score_threshold
    data = http_json(
        f"{cfg['qdrant_url']}/collections/{cfg['collection']}/points/search",
        method="POST",
        body=body,
        headers=qdrant_headers(cfg),
    )
    hits = data.get("result") or []
    out = []
    for h in hits:
        payload = h.get("payload") or {}
        out.append(
            {
                "id": h.get("id"),
                "score": h.get("score"),
                "source": payload.get("source"),
                "chunk": payload.get("chunk"),
                "tags": payload.get("tags"),
                "text": payload.get("text"),
            }
        )
    print(json.dumps({"query": query, "collection": cfg["collection"], "hits": out}, ensure_ascii=False, indent=2))


def cmd_delete(cfg: dict[str, Any], args: argparse.Namespace) -> None:
    body = {"points": [args.id]}
    data = http_json(
        f"{cfg['qdrant_url']}/collections/{cfg['collection']}/points/delete?wait=true",
        method="POST",
        body=body,
        headers=qdrant_headers(cfg),
    )
    print(json.dumps({"id": args.id, "result": data.get("result") or data}, ensure_ascii=False, indent=2))


def cmd_migrate_sqlite(cfg: dict[str, Any], args: argparse.Namespace) -> None:
    db_path = Path(
        args.db
        or os.environ.get(
            "OPENCLAW_MEMORY_DB",
            str(Path.home() / ".openclaw/agents/main/agent/openclaw-agent.sqlite"),
        )
    )
    if not db_path.exists():
        raise SystemExit(f"sqlite not found: {db_path}")

    import sqlite3

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    rows = list(
        conn.execute(
            "SELECT id, path, source, start_line, end_line, hash, model, text, embedding, updated_at "
            "FROM memory_index_chunks"
        )
    )
    if not rows:
        print(json.dumps({"status": "ok", "migrated": 0, "reason": "no chunks"}, ensure_ascii=False))
        return

    body_points: list[dict[str, Any]] = []
    skipped = 0
    models: dict[str, int] = {}
    paths: dict[str, int] = {}
    dims_seen: set[int] = set()

    for r in rows:
        text = (r["text"] or "").strip()
        emb_raw = r["embedding"]
        if not text or not emb_raw:
            skipped += 1
            continue
        try:
            vec = json.loads(emb_raw)
        except Exception:
            skipped += 1
            continue
        if not isinstance(vec, list) or not vec:
            skipped += 1
            continue
        vec = [float(x) for x in vec]
        dims_seen.add(len(vec))
        model = r["model"] or cfg["embed_model"]
        models[model] = models.get(model, 0) + 1
        path = r["path"] or ""
        paths[path] = paths.get(path, 0) + 1
        origin_id = r["id"]
        pid = qdrant_point_id(origin_id)
        payload = {
            "text": text,
            "source": r["source"] or "memory",
            "path": path,
            "start_line": r["start_line"],
            "end_line": r["end_line"],
            "hash": r["hash"],
            "model": model,
            "origin_id": origin_id,
            "origin": "openclaw-sqlite",
            "updated_at": r["updated_at"],
            "migrated_at": int(time.time()),
            "tags": ["migrated", "sqlite", "memory"],
        }
        body_points.append({"id": pid, "vector": vec, "payload": payload})

    if len(dims_seen) != 1:
        raise SystemExit(f"inconsistent embedding dims in sqlite: {sorted(dims_seen)}")
    dim = next(iter(dims_seen))
    cfg["dims"] = dim

    if args.reembed:
        # optional: recompute vectors with current embedding endpoint
        texts = [p["payload"]["text"] for p in body_points]
        new_vecs: list[list[float]] = []
        for i in range(0, len(texts), 16):
            new_vecs.extend(embed_texts(cfg, texts[i : i + 16]))
        for p, v in zip(body_points, new_vecs):
            p["vector"] = v
            p["payload"]["model"] = cfg["embed_model"]
            p["payload"]["reembedded"] = True

    migrated = put_points(cfg, body_points)
    # verify count
    info = http_json(
        f"{cfg['qdrant_url']}/collections/{cfg['collection']}",
        headers=qdrant_headers(cfg),
    )
    points_count = (info.get("result") or {}).get("points_count")
    out = {
        "status": "ok",
        "db": str(db_path),
        "collection": cfg["collection"],
        "sqlite_chunks": len(rows),
        "migrated": migrated,
        "skipped": skipped,
        "dims": dim,
        "reembed": bool(args.reembed),
        "models": models,
        "paths": paths,
        "qdrant_points_count": points_count,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="OpenClaw Qdrant knowledge base")
    p.add_argument("--collection", default=None, help="override collection name")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("ensure", help="ensure collection exists")
    sub.add_parser("collections", help="list collections")
    sub.add_parser("info", help="show collection + safe config")

    sp = sub.add_parser("search", help="semantic search")
    sp.add_argument("query")
    sp.add_argument("--top-k", type=int, default=5)
    sp.add_argument("--score-threshold", type=float, default=None)

    up = sub.add_parser("upsert", help="upsert one text point")
    up.add_argument("--text", default=None)
    up.add_argument("--file", default=None, help="read text from file (single point)")
    up.add_argument("--id", default=None)
    up.add_argument("--source", default=None)
    up.add_argument("--tags", default="")
    up.add_argument("--meta", default=None, help="extra JSON object merged into payload")

    uf = sub.add_parser("upsert-file", help="chunk and upsert a file")
    uf.add_argument("path")
    uf.add_argument("--source", default=None)
    uf.add_argument("--tags", default="")
    uf.add_argument("--max-chars", type=int, default=1200)
    uf.add_argument("--overlap", type=int, default=150)

    d = sub.add_parser("delete", help="delete point by id")
    d.add_argument("--id", required=True)

    ms = sub.add_parser(
        "migrate-sqlite",
        help="migrate OpenClaw memory_index_chunks from sqlite into Qdrant",
    )
    ms.add_argument(
        "--db",
        default=None,
        help="path to openclaw-agent.sqlite (default: ~/.openclaw/agents/main/agent/openclaw-agent.sqlite)",
    )
    ms.add_argument(
        "--reembed",
        action="store_true",
        help="recompute embeddings instead of reusing sqlite vectors",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    cfg = settings_from_env()
    if args.collection:
        cfg["collection"] = args.collection
    cmd = args.cmd
    if cmd == "ensure":
        cmd_ensure(cfg)
    elif cmd == "collections":
        cmd_collections(cfg)
    elif cmd == "info":
        cmd_info(cfg)
    elif cmd == "search":
        cmd_search(cfg, args)
    elif cmd == "upsert":
        cmd_upsert(cfg, args)
    elif cmd == "upsert-file":
        cmd_upsert_file(cfg, args)
    elif cmd == "delete":
        cmd_delete(cfg, args)
    elif cmd == "migrate-sqlite":
        cmd_migrate_sqlite(cfg, args)
    else:
        parser.error(f"unknown cmd {cmd}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
