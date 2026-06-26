#!/usr/bin/env python3
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional, Tuple


def _bootstrap_shared_senseaudio_env() -> None:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / "_shared" / "senseaudio_env.py"
        if candidate.exists():
            candidate_dir = str(candidate.parent)
            if candidate_dir not in sys.path:
                sys.path.insert(0, candidate_dir)
            from senseaudio_env import ensure_senseaudio_env
            ensure_senseaudio_env()
            return


_bootstrap_shared_senseaudio_env()

from senseaudio_api_guard import ensure_runtime_api_key


API_URL = "https://api.senseaudio.cn/v1/t2a_v2"


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9_-]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "line"


def parse_sse_audio(response) -> Tuple[bytes, Optional[str], Optional[dict], int]:
    audio_parts = []
    trace_id = None
    extra_info = None
    chunk_count = 0
    for raw_line in response:
        line = raw_line.decode("utf-8", "replace").strip()
        if not line or not line.startswith("data: "):
            continue
        chunk_count += 1
        payload = json.loads(line[6:])
        base_resp = payload.get("base_resp") or {}
        if base_resp.get("status_code") not in (None, 0):
            raise RuntimeError(base_resp.get("status_msg") or "SenseAudio returned an error.")
        trace_id = payload.get("trace_id") or trace_id
        if payload.get("extra_info"):
            extra_info = payload["extra_info"]
        data = payload.get("data") or {}
        audio_hex = data.get("audio")
        if audio_hex:
            audio_parts.append(bytes.fromhex(audio_hex))
    return b"".join(audio_parts), trace_id, extra_info, chunk_count


def candidate_models(voice_id: str) -> list[str]:
    if voice_id.startswith("vc-"):
        return ["SenseAudio-TTS-1.5", "SenseAudio-TTS-1.0"]
    return ["SenseAudio-TTS-1.0"]


def synthesize(text: str, voice_id: str, api_key: str) -> Tuple[bytes, Optional[str], Optional[dict], int, str]:
    last_error = ""
    for model in candidate_models(voice_id):
        payload = {
            "model": model,
            "text": text,
            "stream": True,
            "voice_setting": {"voice_id": voice_id},
            "audio_setting": {"format": "mp3", "sample_rate": 32000},
        }
        request = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "Codex-SenseAudio-Game-NPC/1.0",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                audio_bytes, trace_id, extra_info, chunk_count = parse_sse_audio(response)
                return audio_bytes, trace_id, extra_info, chunk_count, model
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", "replace")
            last_error = f"HTTP {exc.code}: {body}"
            if voice_id.startswith("vc-") and "model does not support this capability" in last_error.lower():
                continue
            raise RuntimeError(last_error) from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Network error: {exc}") from exc
    raise RuntimeError(last_error or "No compatible TTS model found.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Batch synthesize an NPC scene manifest.")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--outdir", required=True)
    parser.add_argument("--voice-id", default="")
    parser.add_argument("--voice-source", choices=["system", "clone"], default="system")
    parser.add_argument("--api-key-env", default="SENSEAUDIO_API_KEY")
    args = parser.parse_args()

    api_key = ensure_runtime_api_key(os.getenv(args.api_key_env), args.api_key_env, purpose="tts")

    manifest = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
    voice_id = args.voice_id or manifest["npc_profile"]["voice_id"]
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    results = []
    for item in manifest["lines"]:
        audio_bytes, trace_id, extra_info, chunk_count, model_used = synthesize(item["text"], voice_id, api_key)
        filename = f"{item['line_id']}_{slugify(item['event_type'])}_{slugify(item['relationship'])}.mp3"
        out_path = outdir / filename
        out_path.write_bytes(audio_bytes)
        results.append(
            {
                "line_id": item["line_id"],
                "voice_id": voice_id,
                "out_path": str(out_path),
                "trace_id": trace_id,
                "bytes": len(audio_bytes),
                "extra_info": extra_info,
                "model_used": model_used,
                "tts_stream": True,
                "tts_stream_chunk_count": chunk_count,
                "voice_source": args.voice_source,
                "text": item["text"],
            }
        )

    summary = {
        "npc_name": manifest["npc_profile"]["npc_name"],
        "voice_id": voice_id,
        "voice_source": args.voice_source,
        "scene": manifest["scene"],
        "output_dir": str(outdir),
        "count": len(results),
        "results": results,
    }
    summary_path = outdir / "scene_tts_results.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    json.dump(summary, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
