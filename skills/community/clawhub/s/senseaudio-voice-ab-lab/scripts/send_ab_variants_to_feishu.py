#!/usr/bin/env python3
import argparse
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
for parent in SCRIPT_DIR.parents:
    candidate = parent / "_shared" / "audioclaw_paths.py"
    if candidate.exists():
        candidate_dir = str(candidate.parent)
        if candidate_dir not in sys.path:
            sys.path.insert(0, candidate_dir)
        break

from audioclaw_paths import get_config_path, get_workspace_root

DEFAULT_CONFIG_PATH = get_config_path()
DEFAULT_WORKSPACE = get_workspace_root()


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid json in {path}: {exc}") from exc


def load_helper_module(skill_name: str, script_name: str, alias: str) -> Any:
    current = Path(__file__).resolve()
    for parent in current.parents:
        candidate = parent / skill_name / "scripts" / script_name
        if candidate.exists():
            spec = importlib.util.spec_from_file_location(alias, candidate)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return module
    raise SystemExit(f"could not locate {skill_name}/scripts/{script_name}")


feishu_sender = load_helper_module("audioclaw-skills-voice-reply", "feishu_audio_sender.py", "audioclaw_feishu_sender")


def slugify(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "_" for ch in value)
    while "__" in cleaned:
        cleaned = cleaned.replace("__", "_")
    return cleaned.strip("_") or "voice_ab"


def resolve_ffmpeg_exe(explicit: str) -> str:
    if explicit:
        return str(Path(explicit).expanduser())
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        return ffmpeg_path
    try:
        import imageio_ffmpeg  # type: ignore

        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception as exc:
        raise SystemExit(
            "Feishu voice delivery needs ffmpeg. Install ffmpeg or `python3 -m pip install imageio-ffmpeg`."
        ) from exc


def transcode_to_ogg(source_path: Path, target_path: Path, *, ffmpeg_exe: str) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)
    command = [
        ffmpeg_exe,
        "-y",
        "-i",
        str(source_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "24000",
        "-c:a",
        "libopus",
        "-b:a",
        "48k",
        str(target_path),
    ]
    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as exc:
        stderr = (exc.stderr or "").strip()
        raise SystemExit(f"ffmpeg transcoding failed: {stderr or exc}") from exc
    os.chmod(target_path, 0o644)


def filter_results(results: list[dict], variant_ids: str, limit: int) -> list[dict]:
    selected = results
    if variant_ids.strip():
        wanted = {item.strip() for item in variant_ids.split(",") if item.strip()}
        selected = [item for item in selected if item.get("variant_id") in wanted]
    if limit > 0:
        selected = selected[:limit]
    return selected


def send_text_message(chat_id: str, text: str, tenant_token: str) -> dict:
    payload = {
        "receive_id": chat_id,
        "msg_type": "text",
        "content": json.dumps({"text": text}, ensure_ascii=False),
    }
    data = feishu_sender.http_json(
        "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id",
        payload,
        headers={"Authorization": f"Bearer {tenant_token}"},
    )
    if data.get("code") != 0:
        raise SystemExit(f"text send failed: {json.dumps(data, ensure_ascii=False)}")
    return data


def main() -> int:
    parser = argparse.ArgumentParser(description="Send generated Voice AB Lab variants to Feishu one by one as audio messages.")
    parser.add_argument("--tts-results", required=True)
    parser.add_argument("--workspace-root", default=str(DEFAULT_WORKSPACE))
    parser.add_argument("--config-path", default=str(DEFAULT_CONFIG_PATH))
    parser.add_argument("--chat-id", default="")
    parser.add_argument("--session-file", default="")
    parser.add_argument("--outdir", default="")
    parser.add_argument("--out-json", default="")
    parser.add_argument("--variant-ids", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--send-labels", action="store_true")
    parser.add_argument("--delay-ms", type=int, default=0)
    parser.add_argument("--ffmpeg-exe", default="")
    args = parser.parse_args()

    tts_results_path = Path(args.tts_results).expanduser().resolve()
    summary = load_json(tts_results_path)
    selected_results = filter_results(summary.get("results") or [], args.variant_ids, args.limit)
    if not selected_results:
        raise SystemExit("no variants selected for Feishu sending")

    workspace_root = Path(args.workspace_root).expanduser().resolve()
    config = feishu_sender.load_feishu_config(Path(args.config_path).expanduser())
    chat_id, session_path = feishu_sender.infer_chat_id(workspace_root, args.chat_id.strip(), args.session_file.strip())
    tenant_token = feishu_sender.fetch_tenant_token(config["app_id"], config["app_secret"])
    ffmpeg_exe = resolve_ffmpeg_exe(args.ffmpeg_exe.strip())

    if args.outdir.strip():
        prepared_dir = Path(args.outdir).expanduser().resolve()
    else:
        campaign_slug = slugify(summary.get("campaign_name") or tts_results_path.parent.parent.name)
        prepared_dir = workspace_root / "state" / "audio" / "voice_ab" / campaign_slug
    prepared_dir.mkdir(parents=True, exist_ok=True)

    deliveries = []
    for index, item in enumerate(selected_results, start=1):
        source_path = Path(str(item.get("out_path") or "")).expanduser().resolve()
        if not source_path.exists():
            raise SystemExit(f"missing synthesized audio file: {source_path}")
        target_name = f"{item.get('variant_id', f'V{index:02d}')}_{slugify(str(item.get('tone') or 'tone'))}_{slugify(str(item.get('regional_style') or 'style'))}.ogg"
        target_path = prepared_dir / target_name
        transcode_to_ogg(source_path, target_path, ffmpeg_exe=ffmpeg_exe)

        if args.send_labels:
            label = f"{item.get('variant_id', f'V{index:02d}')} {item.get('tone', '')}".strip()
            send_text = send_text_message(chat_id, label, tenant_token)
        else:
            send_text = None

        duration_ms = (((item.get("extra_info") or {}).get("audio_length")) or None)
        upload = feishu_sender.upload_audio(target_path, tenant_token, duration_ms)
        file_key = (((upload.get("data") or {}).get("file_key")) or "").strip()
        if not file_key:
            raise SystemExit(f"upload response missing file_key: {json.dumps(upload, ensure_ascii=False)}")
        send = feishu_sender.send_audio_message(chat_id, file_key, tenant_token)
        deliveries.append(
            {
                "variant_id": item.get("variant_id"),
                "tone": item.get("tone"),
                "regional_style": item.get("regional_style"),
                "source_audio_path": str(source_path),
                "feishu_audio_path": str(target_path),
                "duration_ms": duration_ms,
                "label_message": send_text,
                "upload": upload,
                "send": send,
            }
        )
        if args.delay_ms > 0 and index < len(selected_results):
            time.sleep(args.delay_ms / 1000)

    result = {
        "mode": "voice_ab_feishu_sequence_sent",
        "campaign_name": summary.get("campaign_name"),
        "chat_id": chat_id,
        "session_file": session_path,
        "prepared_dir": str(prepared_dir),
        "count": len(deliveries),
        "deliveries": deliveries,
    }
    result_path = Path(args.out_json).expanduser().resolve() if args.out_json.strip() else (prepared_dir / "feishu_send_results.json")
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
