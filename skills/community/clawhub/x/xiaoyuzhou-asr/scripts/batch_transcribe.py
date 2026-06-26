#!/usr/bin/env python3
"""
批量转录编排脚本
搜索小宇宙上 LLM/AI 相关播客，自动下载转录。

用法:
  python3 scripts/batch_transcribe.py                    # 完整流程
  python3 scripts/batch_transcribe.py --discover-only    # 只搜索，不转录
  python3 scripts/batch_transcribe.py --resume            # 从检查点恢复
  python3 scripts/batch_transcribe.py --min-plays 5000   # 降低播放量阈值
"""

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from transcribe_podcast import (
    TranscriptionError,
    TokenExpiredError,
    episode_file_stem,
    format_output,
    get_all_episodes,
    resolve_setting,
    search_all_podcasts,
    transcribe_episode,
    _detect_asr_bin,
    _detect_model_dir,
)

# --- Config ---

DEFAULT_KEYWORDS = [
    "LLM",
    "AI Agent",
    "大模型",
    "GPT",
    "Claude",
    "ChatGPT",
    "OpenAI",
    "Anthropic",
    "AI应用",
    "AI创业",
]

# Skip podcasts whose title matches these (traditional ML/DL)
EXCLUDE_PATTERNS = ["机器学习", "深度学习", "Deep Learning", "Machine Learning", "ML入门"]

DEFAULT_MIN_PLAYS = 10000
DEFAULT_OUTPUT_DIR = Path.home() / "xiaoyuzhou-transcripts"
CHECKPOINT_FILE = "batch-checkpoint.json"


def default_checkpoint() -> dict:
    return {"discovered_podcasts": [], "discovered_episodes": [], "completed": [], "failed": []}


def _atomic_write(path: Path, data: dict) -> None:
    """Atomic JSON write: write to tmp, fsync, rename."""
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    tmp.replace(path)


def load_checkpoint(output_dir: Path) -> dict:
    path = output_dir / CHECKPOINT_FILE
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            checkpoint = default_checkpoint()
            checkpoint.update(data)
            return checkpoint
    return default_checkpoint()


def save_checkpoint(output_dir: Path, checkpoint: dict) -> None:
    _atomic_write(output_dir / CHECKPOINT_FILE, checkpoint)


def is_excluded(title: str) -> bool:
    lower = title.lower()
    return any(p.lower() in lower for p in EXCLUDE_PATTERNS)


def discover_podcasts(token: str, keywords: list[str], min_plays: int) -> list[dict]:
    """Search for podcasts across all keywords, deduplicate, filter."""
    seen_pids = set()
    all_podcasts = []

    for kw in keywords:
        print(f"\n搜索关键词: {kw}")
        podcasts = search_all_podcasts(token, kw, max_pages=3)
        for p in podcasts:
            pid = p.get("pid")
            if not pid or pid in seen_pids:
                continue
            title = p.get("title", "")
            if is_excluded(title):
                print(f"  跳过 (传统ML/DL): {title}")
                continue
            seen_pids.add(pid)
            all_podcasts.append(p)
            sub_count = p.get("subscriptionCount", 0)
            ep_count = p.get("episodeCount", 0)
            print(f"  发现: {title} (订阅: {sub_count:,}, 集数: {ep_count})")

    print(f"\n共发现 {len(all_podcasts)} 个播客 (去重后)")
    return all_podcasts


def discover_episodes(token: str, podcasts: list[dict], min_plays: int) -> list[dict]:
    """Get all episodes from podcasts, filter by play count."""
    all_episodes = []
    seen_eids = set()

    for p in podcasts:
        pid = p.get("pid")
        if not isinstance(pid, str) or not pid:
            print(f"\n跳过无效播客记录: {p.get('title', '?')}")
            continue

        title = p.get("title", "")
        print(f"\n获取播客单集: {title} ({pid})")

        episodes = get_all_episodes(token, pid, max_pages=50)
        qualifying = []

        for ep in episodes:
            eid = ep.get("eid")
            if not eid or eid in seen_eids:
                continue
            seen_eids.add(eid)

            play_count = ep.get("playCount", 0)
            ep_title = ep.get("title", "")
            duration = ep.get("duration", 0)

            if play_count < min_plays:
                continue
            if duration < 60:
                continue

            qualifying.append(ep)

        print(f"  共 {len(episodes)} 集, {len(qualifying)} 集符合条件 (>={min_plays:,} 播放, >1min)")
        all_episodes.extend(qualifying)

    all_episodes.sort(key=lambda e: e.get("playCount", 0), reverse=True)
    print(f"\n总计 {len(all_episodes)} 集待转录")
    return all_episodes


def batch_transcribe(
    token: str,
    episodes: list[dict],
    checkpoint: dict,
    output_dir: Path,
    model_dir: str,
    asr_bin: str,
    keep_audio: bool = False,
) -> None:
    """Transcribe episodes with checkpoint resume."""
    completed_eids = set(checkpoint.get("completed", []))
    failed = checkpoint.get("failed", [])
    remaining = [e for e in episodes if e["eid"] not in completed_eids]

    if not remaining:
        print("所有单集已完成转录。")
        return

    print(f"\n待转录: {len(remaining)} 集 (已完成: {len(completed_eids)}, 失败: {len(failed)})")

    for i, ep in enumerate(remaining):
        eid = ep["eid"]
        title = ep.get("title", "未知")
        play_count = ep.get("playCount", 0)
        print(f"\n{'='*50}")
        print(f"[{i+1}/{len(remaining)}] {title}")
        print(f"  播放: {play_count:,}")
        print(f"{'='*50}")

        safe = episode_file_stem(ep, fallback=eid)
        out_path = output_dir / f"{safe}.md"

        if out_path.exists() and out_path.stat().st_size > 0:
            print(f"  跳过 (文件已存在): {out_path}")
            checkpoint["completed"].append(eid)
            save_checkpoint(output_dir, checkpoint)
            continue

        try:
            episode, transcript, timings = transcribe_episode(
                token, eid, model_dir, asr_bin, keep_audio,
            )
            output = format_output(episode, transcript, timings)
            output_dir.mkdir(parents=True, exist_ok=True)
            out_path.write_text(output, encoding="utf-8")
            print(f"  已保存: {out_path}")

            checkpoint["completed"].append(eid)
            save_checkpoint(output_dir, checkpoint)

        except TokenExpiredError:
            print("\n  Token 过期，请重新登录后使用 --resume 恢复")
            sys.exit(1)
        except (TranscriptionError, Exception) as e:
            print(f"  失败: {e}")
            failed.append({"eid": eid, "title": title, "error": str(e)})
            checkpoint["failed"] = failed
            save_checkpoint(output_dir, checkpoint)
            continue


def main():
    parser = argparse.ArgumentParser(description="批量转录小宇宙 LLM/AI 播客")
    parser.add_argument("--keywords", nargs="+", default=None,
                        help="搜索关键词 (默认使用内置列表)")
    parser.add_argument("--min-plays", type=int, default=DEFAULT_MIN_PLAYS,
                        help=f"最低播放量 (默认 {DEFAULT_MIN_PLAYS:,})")
    parser.add_argument("--output-dir", type=str, default=str(DEFAULT_OUTPUT_DIR),
                        help=f"输出目录 (默认 {DEFAULT_OUTPUT_DIR})")
    parser.add_argument("--discover-only", action="store_true",
                        help="只搜索和发现，不转录")
    parser.add_argument("--transcribe-only", action="store_true",
                        help="从检查点恢复，直接开始转录 (跳过搜索)")
    parser.add_argument("--resume", action="store_true",
                        help="从检查点恢复 (等同于 --transcribe-only)")
    parser.add_argument("--keep-audio", action="store_true",
                        help="保留下载的音频文件")
    parser.add_argument("--model-dir", help="Qwen3-ASR 模型目录")
    parser.add_argument("--asr-bin", help="qwen3-asr-rs 路径")
    parser.add_argument("--token", help="Access token")
    args = parser.parse_args()

    token = resolve_setting(args.token, "XYZ_ACCESS_TOKEN", "token") or ""
    if not token:
        print("错误: 需要 access token，请先运行: python3 scripts/transcribe_podcast.py --login")
        sys.exit(1)

    model_dir = resolve_setting(args.model_dir, "QWEN3_ASR_MODEL_DIR", "model_dir") or _detect_model_dir()
    asr_bin = resolve_setting(args.asr_bin, "QWEN3_ASR_BIN", "asr_bin") or _detect_asr_bin()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    keywords = args.keywords or DEFAULT_KEYWORDS

    print("=" * 50)
    print("小宇宙播客批量转录")
    print(f"关键词: {', '.join(keywords)}")
    print(f"最低播放量: {args.min_plays:,}")
    print(f"输出目录: {output_dir}")
    print("=" * 50)

    checkpoint = load_checkpoint(output_dir)

    # --- Discover phase ---
    if not args.transcribe_only and not args.resume:
        # Step 1: Discover podcasts
        if checkpoint.get("discovered_podcasts") and not args.discover_only:
            print(f"\n检查点中已有 {len(checkpoint['discovered_podcasts'])} 个播客，跳过搜索")
            print("  (使用 --transcribe-only 或删除检查点以重新搜索)")
            podcasts = checkpoint["discovered_podcasts"]
        else:
            podcasts = discover_podcasts(token, keywords, args.min_plays)
            checkpoint["discovered_podcasts"] = podcasts

        # Step 2: Discover episodes
        if checkpoint.get("discovered_episodes") and not args.discover_only:
            print(f"\n检查点中已有 {len(checkpoint['discovered_episodes'])} 个单集，跳过枚举")
            episodes = checkpoint["discovered_episodes"]
        else:
            episodes = discover_episodes(token, podcasts, args.min_plays)
            checkpoint["discovered_episodes"] = episodes

        save_checkpoint(output_dir, checkpoint)

        if args.discover_only:
            # Print summary
            print(f"\n{'='*50}")
            print(f"发现摘要:")
            print(f"  播客数: {len(podcasts)}")
            print(f"  符合条件的单集数: {len(episodes)}")
            print(f"\nTop 10 单集 (按播放量):")
            for i, ep in enumerate(episodes[:10]):
                podcast_title = ep.get("podcast", {}).get("title", "?")
                print(f"  {i+1}. [{ep.get('playCount', 0):>8,} 播放] {ep.get('title', '?')} — {podcast_title}")
            return

    # --- Transcribe phase ---
    episodes = checkpoint.get("discovered_episodes", [])
    if not episodes:
        print("没有待转录的单集。请先不带 --resume 运行以搜索。")
        sys.exit(1)

    batch_transcribe(
        token, episodes, checkpoint, output_dir, model_dir, asr_bin, args.keep_audio,
    )

    # Final summary
    checkpoint = load_checkpoint(output_dir)
    completed = len(checkpoint.get("completed", []))
    failed = len(checkpoint.get("failed", []))
    total = len(checkpoint.get("discovered_episodes", []))
    print(f"\n{'='*50}")
    print(f"完成: {completed}/{total}, 失败: {failed}")
    if failed:
        print("失败列表:")
        for f in checkpoint["failed"]:
            print(f"  - {f.get('title', '?')}: {f.get('error', '?')[:80]}")
    print(f"输出目录: {output_dir}")


if __name__ == "__main__":
    main()
