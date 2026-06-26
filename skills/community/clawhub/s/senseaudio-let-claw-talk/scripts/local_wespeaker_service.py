#!/usr/bin/env python3
import argparse
import contextlib
import io
import json
import os
import signal
import sys
import threading
import warnings
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import numpy as np

warnings.filterwarnings("ignore")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Background WeSpeaker service for VoiceClaw.")
    subparsers = parser.add_subparsers(dest="command", required=True)
    serve = subparsers.add_parser("serve")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=18567)
    serve.add_argument("--state-dir", required=True)
    serve.add_argument("--model", default="chinese")
    serve.add_argument("--threshold", type=float, default=0.72)
    return parser.parse_args()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


class WeSpeakerStore:
    def __init__(self, state_dir: Path):
        self.state_dir = state_dir
        self.profiles_dir = self.state_dir / "profiles"
        self.meta_dir = self.state_dir / "meta"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.meta_dir.mkdir(parents=True, exist_ok=True)

    def embedding_path(self, profile_name: str) -> Path:
        return self.profiles_dir / f"{profile_name}.npy"

    def meta_path(self, profile_name: str) -> Path:
        return self.profiles_dir / f"{profile_name}.json"

    def load_embeddings(self, profile_name: str) -> np.ndarray:
        path = self.embedding_path(profile_name)
        if not path.exists():
            return np.zeros((0, 256), dtype=np.float32)
        data = np.load(path)
        if data.ndim == 1:
            data = data.reshape(1, -1)
        return data.astype(np.float32)

    def save_embeddings(self, profile_name: str, embeddings: np.ndarray) -> None:
        path = self.embedding_path(profile_name)
        np.save(path, embeddings.astype(np.float32))
        meta = {
            "profile_name": profile_name,
            "sample_count": int(embeddings.shape[0]),
            "updated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
        write_json(self.meta_path(profile_name), meta)

    def clear_profile(self, profile_name: str) -> None:
        for path in [self.embedding_path(profile_name), self.meta_path(profile_name)]:
            if path.exists():
                path.unlink()

    def profile_status(self, profile_name: str) -> dict:
        embeddings = self.load_embeddings(profile_name)
        meta = {}
        meta_path = self.meta_path(profile_name)
        if meta_path.exists():
            with contextlib.suppress(Exception):
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
        return {
            "profile_name": profile_name,
            "exists": bool(embeddings.size),
            "sample_count": int(embeddings.shape[0]) if embeddings.size else 0,
            "meta": meta if isinstance(meta, dict) else {},
        }


class WeSpeakerRuntime:
    def __init__(self, state_dir: Path, model_name: str, threshold: float):
        self.state_dir = state_dir
        self.model_name = model_name
        self.threshold = float(threshold)
        self.store = WeSpeakerStore(state_dir)
        self.pid_path = state_dir / "service.pid"
        self.status_path = state_dir / "service_status.json"
        os.environ.setdefault("WESPEAKER_HOME", str((state_dir / "models").resolve()))
        self.model = self._load_model()
        self._write_status()

    def _load_model(self):
        import wespeaker

        with contextlib.redirect_stdout(io.StringIO()):
            model = wespeaker.load_model(self.model_name)
        return model

    def _write_status(self) -> None:
        payload = {
            "pid": os.getpid(),
            "model": self.model_name,
            "threshold": self.threshold,
            "state_dir": str(self.state_dir),
            "updated_at": __import__("time").strftime("%Y-%m-%dT%H:%M:%S%z"),
        }
        write_json(self.status_path, payload)
        self.pid_path.write_text(str(os.getpid()) + "\n", encoding="utf-8")

    def extract_embedding(self, audio_path: str) -> np.ndarray:
        embedding = self.model.extract_embedding(audio_path)
        if embedding is None:
            raise RuntimeError("这段音频里有效人声太少，暂时没法提取声纹。")
        return embedding.detach().cpu().numpy().astype(np.float32).reshape(1, -1)

    def enroll(self, audio_path: str, profile_name: str, reset: bool, max_samples: int) -> dict:
        embedding = self.extract_embedding(audio_path)
        if reset:
            embeddings = embedding
        else:
            existing = self.store.load_embeddings(profile_name)
            embeddings = np.vstack([existing, embedding]) if existing.size else embedding
        max_samples = max(1, int(max_samples))
        if embeddings.shape[0] > max_samples:
            embeddings = embeddings[-max_samples:]
        self.store.save_embeddings(profile_name, embeddings)
        return {
            "ok": True,
            "profile_name": profile_name,
            "sample_count": int(embeddings.shape[0]),
        }

    def verify(self, audio_path: str, profile_name: str, threshold: float) -> dict:
        embeddings = self.store.load_embeddings(profile_name)
        if not embeddings.size:
            raise RuntimeError("当前还没有录入可用的声音档案。")
        probe = self.extract_embedding(audio_path).reshape(-1)
        probe_norm = np.linalg.norm(probe)
        if probe_norm <= 1e-6:
            raise RuntimeError("当前声纹特征不稳定，暂时无法比对。")
        ref_norms = np.linalg.norm(embeddings, axis=1)
        valid_mask = ref_norms > 1e-6
        if not np.any(valid_mask):
            raise RuntimeError("当前声纹特征不稳定，暂时无法比对。")
        valid_embeddings = embeddings[valid_mask]
        valid_norms = ref_norms[valid_mask]
        cosine_scores = np.dot(valid_embeddings, probe) / (valid_norms * probe_norm)
        normalized_scores = (cosine_scores + 1.0) / 2.0
        best_score = float(np.max(normalized_scores))
        mean_score = float(np.mean(normalized_scores))
        top_scores = np.sort(normalized_scores)[-min(2, normalized_scores.shape[0]):]
        consensus_score = float(np.mean(top_scores))
        effective_threshold = float(threshold)
        match = bool(best_score >= effective_threshold or consensus_score >= (effective_threshold - 0.03))
        return {
            "ok": True,
            "profile_name": profile_name,
            "score": best_score,
            "mean_score": mean_score,
            "consensus_score": consensus_score,
            "threshold": effective_threshold,
            "match": match,
            "sample_count": int(embeddings.shape[0]),
        }


class Handler(BaseHTTPRequestHandler):
    runtime: WeSpeakerRuntime = None
    shutdown_event: threading.Event = None

    def log_message(self, _format, *_args):
        return

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0") or "0")
        if length <= 0:
            return {}
        body = self.rfile.read(length).decode("utf-8")
        return json.loads(body or "{}")

    def _send(self, code: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/health":
            self._send(
                200,
                {
                    "ok": True,
                    "pid": os.getpid(),
                    "model": self.runtime.model_name,
                    "threshold": self.runtime.threshold,
                },
            )
            return
        if parsed.path == "/profile":
            name = parse_qs(parsed.query).get("name", ["default"])[0]
            self._send(200, self.runtime.store.profile_status(name))
            return
        self._send(404, {"ok": False, "error": "not_found"})

    def do_POST(self):
        try:
            payload = self._read_json()
            if self.path == "/enroll":
                result = self.runtime.enroll(
                    payload["audio_path"],
                    payload.get("profile_name", "default"),
                    bool(payload.get("reset")),
                    int(payload.get("max_samples", 3)),
                )
                self._send(200, result)
                return
            if self.path == "/verify":
                threshold = float(payload.get("threshold", self.runtime.threshold))
                result = self.runtime.verify(
                    payload["audio_path"],
                    payload.get("profile_name", "default"),
                    threshold,
                )
                self._send(200, result)
                return
            if self.path == "/clear_profile":
                name = payload.get("profile_name", "default")
                self.runtime.store.clear_profile(name)
                self._send(200, {"ok": True, "profile_name": name})
                return
            if self.path == "/shutdown":
                self._send(200, {"ok": True})
                self.shutdown_event.set()
                return
            self._send(404, {"ok": False, "error": "not_found"})
        except Exception as exc:
            self._send(500, {"ok": False, "error": str(exc)})


def serve(args: argparse.Namespace) -> int:
    state_dir = Path(args.state_dir).expanduser().resolve()
    state_dir.mkdir(parents=True, exist_ok=True)
    runtime = WeSpeakerRuntime(state_dir=state_dir, model_name=args.model, threshold=args.threshold)
    shutdown_event = threading.Event()
    Handler.runtime = runtime
    Handler.shutdown_event = shutdown_event
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    server.daemon_threads = True

    def stop_handler(_signum, _frame):
        shutdown_event.set()

    signal.signal(signal.SIGTERM, stop_handler)
    signal.signal(signal.SIGINT, stop_handler)

    worker = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.5}, daemon=True)
    worker.start()
    while not shutdown_event.is_set():
        shutdown_event.wait(0.5)
    server.shutdown()
    server.server_close()
    with contextlib.suppress(Exception):
        runtime.pid_path.unlink()
    return 0


def main() -> int:
    args = parse_args()
    if args.command == "serve":
        return serve(args)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
