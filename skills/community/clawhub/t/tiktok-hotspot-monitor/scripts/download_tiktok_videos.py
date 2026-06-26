from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ANALYSIS_GLOB = "data/tiktok_hotspot_analysis/tiktok_hotspot_analysis_*.json"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "data" / "tiktok_videos"

def _read_crawl_timestamp(analysis_path: Path) -> str:
    try:
        report = json.loads(analysis_path.read_text(encoding="utf-8"))
        cm = report.get("crawl_metrics") or {}
        ts = cm.get("crawl_timestamp")
        if ts:
            return str(ts)
    except Exception:
        pass
    return ""

AGE_BUCKET_LABELS = {
    "within_1d": "近一天",
    "within_3d": "近三天",
    "within_7d": "近七天",
    "within_14d": "近两周",
    "older_than_14d": "两周以前",
    "age_unknown": "发布时间未知",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download hotspot videos organized by time buckets.")
    parser.add_argument("--analysis", type=Path, default=None, help="Analysis JSON. Defaults to latest.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--limit", type=int, default=10, help="Max videos per bucket (default: 10)")
    parser.add_argument("--dry-run", action="store_true", help="Print what would be downloaded without downloading")
    return parser.parse_args()


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else PROJECT_ROOT / path


def latest_analysis() -> Path:
    paths = sorted(PROJECT_ROOT.glob(DEFAULT_ANALYSIS_GLOB), key=lambda p: p.stat().st_mtime, reverse=True)
    if not paths:
        raise ValueError("No analysis JSON found")
    return paths[0]


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def sanitize_filename(name: str) -> str:
    safe = "".join(c if c.isalnum() or c in "._- " else "_" for c in name)
    return safe.strip() or "video"


def short_number(value: Any) -> str:
    if value is None:
        return "—"
    try:
        number = float(value)
    except (TypeError, ValueError):
        return str(value)
    if number >= 1_000_000_000:
        return f"{number / 1_000_000_000:.1f}B"
    if number >= 1_000_000:
        return f"{number / 1_000_000:.1f}M"
    if number >= 1_000:
        return f"{number / 1_000:.1f}K"
    return f"{number:,.0f}"


def write_metadata_md(video: dict[str, Any], md_path: Path) -> None:
    growth = video.get("growth") if isinstance(video.get("growth"), dict) else {}
    music = video.get("music") if isinstance(video.get("music"), dict) else {}
    hashtags = video.get("hashtags") or []

    lines = [
        "---",
        f"video_id: {video.get('video_id', '')}",
        f"url: {video.get('url', '')}",
        f"creator: {video.get('creator', video.get('uploader', ''))}",
        f"title: {video.get('title', '')}",
        f"views: {short_number(video.get('view_count'))}",
        f"likes: {short_number(video.get('like_count'))}",
        f"comments: {short_number(video.get('comment_count'))}",
        f"shares: {short_number(video.get('share_count'))}",
        f"hot_score: {short_number(video.get('hot_score'))}",
        f"engagement_rate: {video.get('engagement_rate', '')}",
        f"video_age_hours: {growth.get('video_age_hours', '')}",
        f"timeliness_label: {growth.get('timeliness_label', '')}",
        f"source_type: {video.get('source_type', '')}",
        f"source_value: {video.get('source_value', '')}",
        f"crawl_timestamp: {video.get('crawl_timestamp', '')}",
        f"downloaded_at: {datetime.now(timezone.utc).isoformat()}",
        "---",
        "",
        f"# {video.get('title', '未命名视频')}",
        "",
        f"**创作者**: @{video.get('creator', video.get('uploader', ''))}",
        f"**播放量**: {short_number(video.get('view_count'))}",
        f"**点赞**: {short_number(video.get('like_count'))}",
        f"**评论**: {short_number(video.get('comment_count'))}",
        f"**分享**: {short_number(video.get('share_count'))}",
        f"**热度分**: {short_number(video.get('hot_score'))}",
        f"**互动率**: {video.get('engagement_rate', '')}",
        f"**视频年龄**: {growth.get('video_age_hours', '')} 小时",
        f"**时效标签**: {growth.get('timeliness_label', '')}",
        "",
    ]
    if hashtags:
        lines.append("**标签**: " + " ".join(f"#{t}" for t in hashtags))
        lines.append("")
    if music.get("track") or music.get("artist"):
        lines.append(f"**音乐**: {music.get('track', '—')} — {music.get('artist', '—')}")
        lines.append("")
    lines.append(f"[在 TikTok 上打开]({video.get('url', '')})")
    lines.append("")

    md_path.write_text("\n".join(lines), encoding="utf-8")


def download_video(url: str, output_path: Path, dry_run: bool = False) -> bool:
    if dry_run:
        return True

    output_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_tmpl = output_path.with_suffix(".%(ext)s")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--no-playlist",
        "--no-warnings",
        "--no-part",  # avoid .part files
        "-o", str(tmp_tmpl),
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        print(f"  timeout: {url}")
        return False
    except Exception as exc:
        print(f"  error: {exc}")
        return False

    # Check for the expected .mp4 output
    if output_path.exists() and output_path.stat().st_size > 0:
        return True

    # Check other extensions
    for ext in [".mp4", ".webm", ".mkv"]:
        candidate = output_path.with_suffix(ext)
        if candidate.exists() and candidate.stat().st_size > 0:
            if ext != ".mp4":
                candidate.rename(output_path)
            return True

    # Check for .mp3 (audio only fallback) — treat as failed
    mp3 = output_path.with_suffix(".mp3")
    if mp3.exists():
        mp3.unlink()

    if result.stderr:
        err = result.stderr.strip()
        if not any(kw in err for kw in ["has no subtitles", "Writing video metadata"]):
            print(f"  yt-dlp: {err[:200]}")
    return False


def collect_videos(report: dict[str, Any], max_per_bucket: int) -> list[tuple[str, str, dict[str, Any]]]:
    collected: list[tuple[str, str, dict[str, Any]]] = []
    for group in report.get("recent_videos_by_age") or []:
        bucket_key = group.get("key", "unknown")
        bucket_label = group.get("label", AGE_BUCKET_LABELS.get(bucket_key, "未知"))
        for video in (group.get("items") or [])[:max_per_bucket]:
            collected.append((bucket_key, bucket_label, video))
    for video in (report.get("top_videos") or [])[:max_per_bucket]:
        collected.append(("top_cumulative", "累计热视频", video))
    return collected


def main() -> int:
    args = parse_args()
    try:
        report_path = resolve_path(args.analysis) if args.analysis else latest_analysis()
        report = load_json(report_path)
    except ValueError as exc:
        print(f"error: {exc}")
        return 2

    videos = collect_videos(report, args.limit)
    if not videos:
        print("no videos found in analysis report")
        return 1

    output_dir_root = resolve_path(args.output_dir)
    output_dir_root.mkdir(parents=True, exist_ok=True)
    existing_ids = set()
    for ts_dir in output_dir_root.iterdir():
        if not ts_dir.is_dir():
            continue
        for f in list(ts_dir.rglob("*.mp4")) + list(ts_dir.rglob("*.md")):
            parts = f.stem.split("_")
            if len(parts) >= 2 and parts[-1].isdigit():
                existing_ids.add(parts[-1])
    if existing_ids:
        print(f"already downloaded: {len(existing_ids)} unique videos")
    
    output_dir = output_dir_root
    parent_ts = _read_crawl_timestamp(report_path)
    if parent_ts:
        output_dir = output_dir / parent_ts
        print(f"parent timestamp: {parent_ts}")
    downloaded = 0
    skipped = 0
    failed = 0

    for bucket_key, bucket_label, video in videos:
        bucket_dir = output_dir / bucket_key
        bucket_dir.mkdir(parents=True, exist_ok=True)

        creator = sanitize_filename(str(video.get("creator", video.get("uploader", "unknown"))))
        video_id = str(video.get("video_id", ""))
        url = str(video.get("url", "") or video.get("webpage_url", ""))
        if not url or not video_id:
            continue

        stem = f"{creator}_{video_id}"
        mp4_path = bucket_dir / f"{stem}.mp4"
        md_path = bucket_dir / f"{stem}.md"

        # Always write / update the metadata .md
        if not args.dry_run:
            write_metadata_md(video, md_path)

        if video_id in existing_ids:
            skipped += 1
            continue

        if mp4_path.exists() and mp4_path.stat().st_size > 0:
            skipped += 1
            continue

        action = "[DRY-RUN]" if args.dry_run else "Downloading"
        print(f"{action} [{bucket_label}] {creator} ({video_id})")
        if args.dry_run:
            skipped += 1
            continue

        ok = download_video(url, mp4_path)
        if ok:
            downloaded += 1
        else:
            failed += 1

    total = downloaded + skipped
    print(f"\ndone: {downloaded} new, {skipped} already exist, {failed} failed (total {total})")
    if not args.dry_run:
        print(f"videos: {output_dir}")
    return 1 if failed > 0 else 0


if __name__ == "__main__":
    raise SystemExit(main())
