# /// script
# requires-python = ">=3.14"
# ///

from __future__ import annotations

import argparse
import json
import time

from common import (
    OUTPUT_ROOT,
    create_song_task,
    default_output_path,
    download_file,
    extract_audio_url,
    get_trace_id,
    log_params,
    pretty_json,
    setup_logging,
    wait_for_song_task,
)

setup_logging()

DEFAULT_MODEL = "TemPolor v4.5"
DEFAULT_PROMPT = (
    "中文流行抒情歌曲，中慢速节奏（70-85 BPM），钢琴与柔和合成器开场，"
    "副歌加入弦乐与鼓组增强情绪。旋律有记忆点，副歌朗朗上口。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="天谱乐歌曲生成并下载到本地")
    parser.add_argument("--prompt", default=DEFAULT_PROMPT, help="音乐描述提示词")
    parser.add_argument("--name", default="", help="文件名描述，不超过 10 个中文字")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="模型名称")
    parser.add_argument("--lyrics", default=None, help="自定义歌词（为空时自动生成）")
    parser.add_argument("--voice-id", default=None, help="演唱声音 ID")
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=15,
        help="轮询间隔秒数，默认 15",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=900,
        help="超时秒数，默认 900",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    pipeline_start = time.monotonic()
    log_params("歌曲生成开始", model=args.model, prompt=args.prompt, voice_id=args.voice_id, name=args.name)
    create_response = create_song_task(
        prompt=args.prompt,
        model=args.model,
        lyrics=args.lyrics,
        voice_id=args.voice_id,
    )
    item_id = create_response["data"]["item_ids"][0]
    log_params("歌曲任务已创建", item_id=item_id)
    print(f"歌曲任务已创建: {item_id}")

    item = wait_for_song_task(
        item_id,
        poll_interval=args.poll_interval,
        timeout=args.timeout,
    )
    log_params("歌曲生成成功", item_id=item_id)
    audio_url = extract_audio_url(item)
    local_path = default_output_path("songs", item_id, ".mp3", name=args.name)
    download_file(audio_url, local_path)

    total_elapsed = round(time.monotonic() - pipeline_start, 3)
    log_params("歌曲生成完成", item_id=item_id, total_elapsed=total_elapsed)
    result = {
        "type": "song",
        "provider": "tianpuyue",
        "item_id": item_id,
        "local_path": str(local_path.relative_to(OUTPUT_ROOT)),
        "source_url": audio_url,
        "title": item.get("title", ""),
        "style": item.get("style", ""),
        "duration": item.get("duration"),
        "model": item.get("model", ""),
        "lyrics": item.get("lyrics", ""),
        "task_info": item,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
