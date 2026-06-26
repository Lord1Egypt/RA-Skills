#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from super_memori_common import (  # noqa: E402
    EMBED_MODEL,
    QDRANT_COLLECTION,
    qdrant_request,
    get_embedding_model,
    now_iso,
    SEMANTIC_SCORE_THRESHOLD,
)

HOST = os.environ.get("SUPER_MEMORI_SEMANTIC_DAEMON_HOST", "127.0.0.1")
PORT = int(os.environ.get("SUPER_MEMORI_SEMANTIC_DAEMON_PORT", "8765"))
IDLE_TIMEOUT_SECONDS = int(os.environ.get("SUPER_MEMORI_SEMANTIC_DAEMON_IDLE_TIMEOUT", "60"))
LAST_ACTIVITY_AT = time.time()


def _touch() -> None:
    global LAST_ACTIVITY_AT
    LAST_ACTIVITY_AT = time.time()


def _embed_texts(texts: list[str], *, prefix: str) -> list[list[float]]:
    if not texts:
        return []
    model = get_embedding_model()
    prepared = [f"{prefix}: {text}" for text in texts]
    vectors = model.encode(prepared, normalize_embeddings=True)
    return [vector.tolist() for vector in vectors]


def semantic_search_via_qdrant(query: str, *, memory_type: str = "all", limit: int = 5, reviewed_only: bool = False) -> list[dict[str, Any]]:
    vector = _embed_texts([query], prefix="query")[0]
    must = []
    if memory_type != "all":
        must.append({"key": "memory_type", "match": {"value": memory_type}})
    if reviewed_only:
        must.append({"key": "reviewed", "match": {"value": 1}})
    payload: dict[str, Any] = {
        "vector": vector,
        "limit": max(limit, 1),
        "with_payload": True,
        "score_threshold": SEMANTIC_SCORE_THRESHOLD,
    }
    if must:
        payload["filter"] = {"must": must}
    data = qdrant_request(f"/collections/{QDRANT_COLLECTION}/points/search", method="POST", payload=payload, timeout=30)
    hits = data.get("result", [])
    results = []
    for hit in hits:
        point = hit.get("payload") or {}
        snippet = (point.get("snippet") or point.get("text") or "").strip().replace("\n", " ")
        results.append({
            "source_path": point.get("source_path", "?"),
            "memory_type": point.get("memory_type", "unknown"),
            "updated_at": point.get("updated_at"),
            "chunk_id": point.get("chunk_id") or hit.get("id"),
            "snippet": snippet[:280] + ("..." if len(snippet) > 280 else ""),
            "reviewed": point.get("reviewed", 1),
            "semantic_score": hit.get("score", 0.0),
            "rank": hit.get("score", 0.0),
            "relation_json": point.get("relation_json") or {},
            "conflict_status": point.get("conflict_status") or "none",
            "source_confidence": float(point.get("source_confidence") or 0.5),
        })
    return results


class Handler(BaseHTTPRequestHandler):
    server_version = "super-memori-semantic-daemon/0.1"

    def log_message(self, format: str, *args: object) -> None:
        return

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length > 0 else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def _send(self, code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        try:
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except BrokenPipeError:
            return

    def do_GET(self) -> None:
        _touch()
        if self.path == "/health":
            ready = True
            error = None
            try:
                get_embedding_model()
            except Exception as exc:
                ready = False
                error = str(exc)
            self._send(200 if ready else 503, {"status": "ok" if ready else "error", "model": EMBED_MODEL, "ready_at": now_iso(), "error": error})
            return
        self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        _touch()
        if self.path == "/embed":
            try:
                payload = self._read_json()
                texts = payload.get("texts") or []
                prefix = str(payload.get("prefix") or "query")
                vectors = _embed_texts([str(t) for t in texts], prefix=prefix)
                self._send(200, {"vectors": vectors})
            except Exception as exc:
                self._send(500, {"error": str(exc)})
            return
        if self.path == "/semantic-search":
            try:
                payload = self._read_json()
                results = semantic_search_via_qdrant(
                    str(payload.get("query") or ""),
                    memory_type=str(payload.get("memory_type") or "all"),
                    limit=int(payload.get("limit") or 5),
                    reviewed_only=bool(payload.get("reviewed_only")),
                )
                self._send(200, {"results": results})
            except Exception as exc:
                self._send(500, {"error": str(exc)})
            return
        self._send(404, {"error": "not found"})


def main() -> int:
    try:
        os.nice(10)
    except Exception:
        pass
    try:
        import torch
        torch.set_num_threads(1)
        if hasattr(torch, 'set_num_interop_threads'):
            torch.set_num_interop_threads(1)
    except Exception:
        pass
    server = HTTPServer((HOST, PORT), Handler)
    server.timeout = 1.0
    while True:
        server.handle_request()
        if time.time() - LAST_ACTIVITY_AT > IDLE_TIMEOUT_SECONDS:
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
