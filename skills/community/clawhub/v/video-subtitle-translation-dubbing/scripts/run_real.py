"""Real end-to-end runner for translation_dubbing_skill.

Usage:

    # 1) 导出凭证
    export TRANSLATION_CREDENTIAL=sk-minimax-xxx

    # 2) 仅翻译字幕
    python scripts/run_real.py \
        --video /path/to/input.mp4 \
        --subtitle /path/to/input.en.srt \
        --mode subtitle_only \
        --out-dir ./out

    # 3) 翻译 + 中文配音（Edge TTS，免费无凭证）
    python scripts/run_real.py \
        --video /path/to/input.mp4 \
        --mode subtitle_and_dubbing \
        --translation-provider llm \
        --translation-endpoint https://api.minimax.io/v1/text/chatcompletion_v2 \
        --translation-model MiniMax-M2 \
        --tts-provider edge \
        --voice-id zh-CN-XiaoxiaoNeural \
        --out-dir ./out

如果没有 --subtitle，脚本会从视频中提取内嵌的英文字幕轨。
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path

from translation_dubbing_skill import parse_manifest, run
from translation_dubbing_skill.models import ProgressEvent
from translation_dubbing_skill.progress import ProgressReporter


def _print_progress(event: ProgressEvent) -> None:
    """Simple stdout progress sink."""
    if event.completed is not None and event.total is not None:
        print(f"[{event.stage}] {event.message} ({event.completed}/{event.total})")
    else:
        print(f"[{event.stage}] {event.message}")
    if event.stage == "done" and event.extra:
        print(f"  output_video_path: {event.extra.get('output_video_path')}")
        print(f"  output_subtitle_path: {event.extra.get('output_subtitle_path')}")


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run translation_dubbing_skill on a real video.")
    p.add_argument("--video", required=True, help="Input video path (.mp4/.mkv/.mov/.webm)")
    p.add_argument("--subtitle", help="Optional external subtitle path (.srt/.vtt)")
    p.add_argument(
        "--mode",
        choices=["subtitle_only", "subtitle_and_dubbing"],
        default="subtitle_and_dubbing",
    )
    p.add_argument("--out-dir", default="./out", help="Output directory")

    # Translation provider
    p.add_argument("--translation-provider", default="llm", choices=["llm", "web"])
    p.add_argument(
        "--translation-endpoint",
        default="https://api.minimax.io/v1/text/chatcompletion_v2",
    )
    p.add_argument("--translation-model", default="MiniMax-M2")
    p.add_argument(
        "--translation-timeout-s",
        type=float,
        default=240.0,
    )

    # TTS provider (only when mode == subtitle_and_dubbing)
    p.add_argument(
        "--tts-provider",
        default="edge",
        choices=["llm", "web", "edge"],
    )
    p.add_argument("--tts-endpoint", default="", help="Ignored for edge provider")
    p.add_argument("--tts-model", default="", help="Optional model name for llm/web providers")
    p.add_argument("--voice-id", default="zh-CN-YunxiNeural")

    return p.parse_args()


async def _main() -> int:
    args = _parse_args()

    translation_credential = os.environ.get("TRANSLATION_CREDENTIAL")
    if not translation_credential:
        print("ERROR: 请通过环境变量 TRANSLATION_CREDENTIAL 提供翻译凭证", file=sys.stderr)
        return 2

    # Edge TTS is unauthenticated; everything else needs a credential.
    if args.mode == "subtitle_and_dubbing" and args.tts_provider != "edge":
        tts_credential = os.environ.get("TTS_CREDENTIAL")
        if not tts_credential:
            print(
                "ERROR: 非 edge 的 TTS 提供方需要环境变量 TTS_CREDENTIAL",
                file=sys.stderr,
            )
            return 2
    else:
        tts_credential = os.environ.get("TTS_CREDENTIAL", "none")

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # Assemble manifest parameters.
    manifest: dict = {
        "video_path": args.video,
        "processing_mode": args.mode,
        "translation_provider": args.translation_provider,
        "translation_endpoint": args.translation_endpoint,
        "translation_credential": translation_credential,
    }
    if args.translation_provider == "llm":
        manifest["translation_extra"] = {
            "model_name": args.translation_model,
            "reasoning_split": True,
            "timeout_s": args.translation_timeout_s,
        }
    if args.subtitle:
        manifest["subtitle_path"] = args.subtitle

    if args.mode == "subtitle_and_dubbing":
        tts_endpoint = args.tts_endpoint
        if args.tts_provider == "edge":
            # Edge doesn't use an endpoint — the library talks WebSockets
            # to Microsoft's service directly — but the manifest requires
            # a non-empty string, so pass a placeholder.
            tts_endpoint = tts_endpoint or "ws://edge-tts"
        tts_extra: dict = {"default_voice": args.voice_id}
        if args.tts_model:
            tts_extra["model_name"] = args.tts_model
        manifest.update(
            {
                "tts_provider": args.tts_provider,
                "tts_endpoint": tts_endpoint,
                "tts_credential": tts_credential,
                "tts_extra": tts_extra,
                "voice_id": args.voice_id,
            }
        )

    params = parse_manifest(manifest)
    reporter = ProgressReporter(_print_progress)

    result = await run(
        params,
        reporter=reporter,
        output_dir_factory=lambda: out_dir,
    )

    print()
    print(f"Video   : {result.output_video_path}")
    print(f"Subtitle: {result.output_subtitle_path}")
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(_main()))
