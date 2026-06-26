#!/usr/bin/env python3
"""
submit_song.py - Submit a song workflow to ComfyUI AceStep API.

Usage:
    python submit_song.py --lyrics "..." --tags "[Style tags...]" [options]

Or import as a module:
    from submit_song import submit
    submit(lyrics="...", tags="...", ...)

⚠️ lyrics 参数不要包含"歌名：《XXX》"前缀，会被 AceStep 唱出来。
"""

import json
import os
import random
import re
import requests
import shutil
import sys
import time
from datetime import datetime

COMFYUI_API = "http://127.0.0.1:8188"
WORKFLOW_PATH = os.path.expanduser(
    "~/ai/ComfyUI/user/default/workflows/api工作流/audio_ace_step1_5_xl_sft.json"
)
OUTPUT_BASE = os.path.expanduser("~/ai/ComfyUI/output")
WORKSPACE_BASE = os.path.expanduser("~/.openclaw/workspace/output")


def _clean_lyrics(text: str) -> str:
    """移除歌词中可能存在的"歌名：《XXX》"前缀，防止被 AceStep 唱出来"""
    text = text.lstrip()
    lines = text.split("\n")
    while lines and re.match(r'^歌名[：:]', lines[0].strip()):
        lines = lines[1:]  # 去掉歌名行
    # 去掉歌名行后的空行
    while lines and lines[0].strip() == "":
        lines = lines[1:]
    return "\n".join(lines).strip()


def submit(
    lyrics: str,
    tags: str,
    song_name: str = "unknown",
    bpm: int = 78,
    key: str = "Eb major",
    duration: int = 220,
    temperature: float = 0.75,
    top_p: float = 0.88,
    cfg: float = 5.5,
    language: str = "zh",
    wait: bool = True,
):
    """
    Submit a song generation workflow to ComfyUI.

    Args:
        lyrics: 歌词正文（自动清洗"歌名："前缀）
        tags: 风格标签（英文）
        song_name: 歌曲名（用于输出文件名）
        bpm: BPM 速度
        key: 调性 (e.g. "D minor", "G major")
        duration: 时长（秒，建议 185 稳定上限）
        temperature: 温度
        top_p: Top-P
        cfg: CFG scale（默认 7 已验证稳定）
        language: 语言（默认 zh）
        wait: 是否等待完成

    Returns: MP3 文件路径，或 None
    """
    # 自动清洗歌词
    lyrics = _clean_lyrics(lyrics)

    # Read workflow
    with open(WORKFLOW_PATH) as f:
        wf = json.load(f)

    # Configure text encoding node (94) - 只改需要改的字段
    node = wf["94"]["inputs"]
    node["tags"] = tags
    node["lyrics"] = lyrics
    node["bpm"] = bpm
    node["keyscale"] = key
    node["duration"] = duration
    node["temperature"] = temperature
    node["top_p"] = top_p
    node["cfg_scale"] = cfg
    node["language"] = language
    node["seed"] = random.randint(0, 999999999)
    # ⚠️ 不要修改 node["clip"] — 保持节点引用 ["105", 0] 不变
    # ⚠️ 不要修改 node["timesignature"], node["generate_audio_codes"],
    #    node["top_k"], node["min_p"] — 保持工作流默认值

    # Configure latent audio duration (node 98)
    wf["98"]["inputs"]["seconds"] = duration

    # Build filename prefix with date
    date_str = datetime.now().strftime("%Y%m%d")
    prefix = f"{date_str}/audio/{song_name}"
    wf["107"]["inputs"]["filename_prefix"] = prefix

    # Submit
    resp = requests.post(f"{COMFYUI_API}/api/prompt", json={"prompt": wf})
    data = resp.json()
    prompt_id = data.get("prompt_id")
    errors = data.get("node_errors", {})
    if errors:
        print(f"Validation errors: {errors}", file=sys.stderr)
        return None

    print(f"Submitted: {prompt_id}")

    if not wait:
        return prompt_id

    # Poll until completion
    for i in range(600):
        try:
            resp = requests.get(f"{COMFYUI_API}/api/history/{prompt_id}")
            h = resp.json().get(prompt_id, {})
            if h.get("status", {}).get("completed"):
                break
        except Exception:
            pass
        if i % 6 == 0:
            print(f"Waiting... ({i*10}s)")
        time.sleep(10)
    else:
        print("TIMEOUT", file=sys.stderr)
        return None

    print("Completed!")

    # Find output file
    outputs = h.get("outputs", {})
    for node_id, node_out in outputs.items():
        for audio_info in node_out.get("audio", []):
            filename = audio_info["filename"]
            subfolder = audio_info["subfolder"]
            src = os.path.join(OUTPUT_BASE, subfolder, filename)
            if os.path.exists(src):
                dst_dir = os.path.join(WORKSPACE_BASE, date_str, "audio")
                os.makedirs(dst_dir, exist_ok=True)
                dst = os.path.join(dst_dir, f"{song_name}.mp3")
                shutil.move(src, dst)
                print(f"Output: {dst}")

                output_dir = os.path.join(OUTPUT_BASE, subfolder)
                if os.path.exists(output_dir) and not os.listdir(output_dir):
                    os.rmdir(output_dir)

                return dst

    print("Output file not found!", file=sys.stderr)
    return None


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Submit song to ComfyUI AceStep")
    parser.add_argument("--lyrics", required=True, help="完整歌词（不含歌名行）")
    parser.add_argument("--tags", required=True, help="Style tags（英文，逗号分隔）")
    parser.add_argument("--name", default="song", help="歌曲名")
    parser.add_argument("--bpm", type=int, default=78)
    parser.add_argument("--key", default="C major")
    parser.add_argument("--duration", type=int, default=185,
                        help="时长秒数（建议 185 稳定上限）")
    parser.add_argument("--temperature", type=float, default=0.85)
    parser.add_argument("--top-p", type=float, default=0.92, dest="top_p")
    parser.add_argument("--cfg", type=float, default=7.0)
    parser.add_argument("--lang", default="zh")
    args = parser.parse_args()

    path = submit(
        lyrics=args.lyrics,
        tags=args.tags,
        song_name=args.name,
        bpm=args.bpm,
        key=args.key,
        duration=args.duration,
        temperature=args.temperature,
        top_p=args.top_p,
        cfg=args.cfg,
        language=args.lang,
    )
    if path:
        print(f"\nMEDIA:{path}")


if __name__ == "__main__":
    main()
