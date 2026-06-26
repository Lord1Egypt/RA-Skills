from __future__ import annotations

import argparse
import sys
from typing import Any

from .cache import ResourceCache
from .common import dump_json, ensure_utf8_stdio, storage_root
from .core import ResourceHunterEngine, format_search_text, format_sources_text, parse_intent
from .video_core import VideoManager, format_video_text


def _resolve_kind(args: argparse.Namespace) -> str | None:
    if getattr(args, "kind", None):
        return args.kind
    for name in ("movie", "tv", "anime", "music", "software", "book", "general"):
        if getattr(args, name, False):
            return name
    return None


def _resolve_channel(args: argparse.Namespace) -> str:
    if getattr(args, "pan_only", False):
        return "pan"
    if getattr(args, "torrent_only", False):
        return "torrent"
    return getattr(args, "channel", "both")


def _format_doctor_text(payload: dict[str, Any]) -> str:
    lines = [
        "Resource Hunter doctor",
        f"Python: {payload['python']}",
        f"stdout_encoding: {payload['stdout_encoding']}",
        f"cache_db: {payload['cache_db']}",
        f"storage_root: {payload['storage_root']}",
        f"yt-dlp: {payload['binaries'].get('yt_dlp') or 'missing'}",
        f"ffmpeg: {payload['binaries'].get('ffmpeg') or 'missing'}",
    ]
    if payload.get("recent_sources"):
        lines.append("")
        lines.append("Recent source status:")
        for item in payload["recent_sources"]["sources"]:
            status = item["recent_status"]
            lines.append(
                f"- {item['source']} ({item['channel']}, p{item['priority']}): "
                f"ok={status['ok']} skipped={status['skipped']} degraded={status.get('degraded')} latency_ms={status.get('latency_ms')}"
            )
    if payload.get("recent_manifests"):
        lines.append("")
        lines.append("Recent video manifests:")
        for item in payload["recent_manifests"]:
            lines.append(f"- {item['url']} [{item.get('preset', '-')}]")
    return "\n".join(lines)


def _search(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    intent = parse_intent(
        query=args.query,
        explicit_kind=_resolve_kind(args),
        channel=_resolve_channel(args),
        quick=args.quick,
        wants_sub=args.sub,
        wants_4k=args.uhd,
    )
    if intent.is_video_url:
        video_manager = VideoManager(engine.cache)
        payload = video_manager.probe(intent.query)
        if args.json:
            print(dump_json(payload.to_dict()))
        else:
            print(format_video_text(payload, "probe"))
        return 0
    response = engine.search(intent, page=args.page, limit=args.limit, use_cache=not args.no_cache)
    effective_limit = min(args.limit, 4) if args.quick else args.limit
    response.setdefault("meta", {})
    response["meta"]["effective_limit"] = effective_limit
    response["meta"]["candidate_count"] = len(response.get("results", []))
    if args.json:
        print(dump_json(response))
    else:
        print(format_search_text(response, max_results=effective_limit))
    return 0


def _sources(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    payload = engine.source_catalog(probe=args.probe)
    if args.json:
        print(dump_json(payload))
    else:
        print(format_sources_text(payload))
    return 0


def _doctor(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    video_manager = VideoManager(engine.cache)
    payload = {
        "python": sys.executable,
        "stdout_encoding": getattr(sys.stdout, "encoding", None),
        "cache_db": str(engine.cache.db_path),
        "storage_root": str(storage_root()),
        "binaries": video_manager.doctor()["binaries"],
        "recent_sources": engine.source_catalog(probe=args.probe),
        "recent_manifests": video_manager.doctor()["recent_manifests"],
    }
    if args.json:
        print(dump_json(payload))
    else:
        print(_format_doctor_text(payload))
    return 0


def _video(engine: ResourceHunterEngine, args: argparse.Namespace) -> int:
    video_manager = VideoManager(engine.cache)
    if args.video_cmd == "info":
        payload = video_manager.info(args.url)
    elif args.video_cmd == "probe":
        payload = video_manager.probe(args.url)
    elif args.video_cmd == "download":
        payload = video_manager.download(args.url, preset=args.format, output_dir=args.dir)
    elif args.video_cmd == "subtitle":
        payload = video_manager.subtitle(args.url, lang=args.lang)
    else:
        raise RuntimeError(f"unsupported video command: {args.video_cmd}")
    if getattr(args, "json", False):
        print(dump_json(payload.to_dict()))
    else:
        print(format_video_text(payload, args.video_cmd))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resource Hunter v2")
    sub = parser.add_subparsers(dest="command")

    p_search = sub.add_parser("search", help="Search public pan/torrent resources")
    p_search.add_argument("query", help="keyword or public video url")
    p_search.add_argument("--kind", choices=["movie", "tv", "anime", "music", "software", "book", "general"])
    p_search.add_argument("--channel", choices=["both", "pan", "torrent"], default="both")
    p_search.add_argument("--movie", action="store_true")
    p_search.add_argument("--tv", action="store_true")
    p_search.add_argument("--anime", action="store_true")
    p_search.add_argument("--music", action="store_true")
    p_search.add_argument("--software", action="store_true")
    p_search.add_argument("--book", action="store_true")
    p_search.add_argument("--general", action="store_true")
    p_search.add_argument("--pan-only", action="store_true")
    p_search.add_argument("--torrent-only", action="store_true")
    p_search.add_argument("--page", type=int, default=1)
    p_search.add_argument("--limit", type=int, default=8)
    p_search.add_argument("--quick", action="store_true")
    p_search.add_argument("--sub", action="store_true")
    p_search.add_argument("--4k", action="store_true", dest="uhd")
    p_search.add_argument("--json", action="store_true")
    p_search.add_argument("--no-cache", action="store_true")

    p_sources = sub.add_parser("sources", help="Show configured resource sources")
    p_sources.add_argument("--probe", action="store_true")
    p_sources.add_argument("--json", action="store_true")

    p_doctor = sub.add_parser("doctor", help="Check dependencies and cached health")
    p_doctor.add_argument("--probe", action="store_true")
    p_doctor.add_argument("--json", action="store_true")

    p_video = sub.add_parser("video", help="Video workflow powered by yt-dlp")
    video_sub = p_video.add_subparsers(dest="video_cmd", required=True)

    p_info = video_sub.add_parser("info", help="Fetch video metadata")
    p_info.add_argument("url")
    p_info.add_argument("--json", action="store_true")

    p_probe = video_sub.add_parser("probe", help="Probe a video url without download")
    p_probe.add_argument("url")
    p_probe.add_argument("--json", action="store_true")

    p_download = video_sub.add_parser("download", help="Download a public video")
    p_download.add_argument("url")
    p_download.add_argument("format", nargs="?", default="best")
    p_download.add_argument("--dir")
    p_download.add_argument("--json", action="store_true")

    p_subtitle = video_sub.add_parser("subtitle", help="Extract subtitles")
    p_subtitle.add_argument("url")
    p_subtitle.add_argument("--lang", default="zh-Hans,zh,en")
    p_subtitle.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    argv = list(argv if argv is not None else sys.argv[1:])
    if argv and argv[0] not in {"search", "sources", "doctor", "video"}:
        argv = ["search"] + argv

    parser = build_parser()
    args = parser.parse_args(argv)
    cache = ResourceCache()
    engine = ResourceHunterEngine(cache=cache)

    try:
        if args.command == "search":
            return _search(engine, args)
        if args.command == "sources":
            return _sources(engine, args)
        if args.command == "doctor":
            return _doctor(engine, args)
        if args.command == "video":
            return _video(engine, args)
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    parser.print_help()
    return 0


def legacy_pansou_main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Legacy pan search wrapper")
    parser.add_argument("keyword")
    parser.add_argument("--types", nargs="+")
    parser.add_argument("--page", type=int, default=1)
    parser.add_argument("--page-size", type=int, default=20)
    parser.add_argument("--max", type=int, default=5)
    parser.add_argument("--fallback", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    engine = ResourceHunterEngine()
    intent = parse_intent(args.keyword, channel="pan")
    response = engine.search(intent, page=args.page, limit=args.max)
    if args.types:
        allowed = {item.lower() for item in args.types}
        response["results"] = [item for item in response["results"] if item["provider"].lower() in allowed]
    if args.json_output:
        print(dump_json(response))
    else:
        print(format_search_text(response, max_results=args.max))
    return 0


def legacy_torrent_main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    parser = argparse.ArgumentParser(description="Legacy torrent search wrapper")
    parser.add_argument("keyword")
    parser.add_argument("--engine", choices=["tpb", "nyaa", "yts", "eztv", "1337x", "all"], default="all")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--anime", action="store_true")
    parser.add_argument("--movie", action="store_true")
    parser.add_argument("--tv", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])
    explicit_kind = "anime" if args.anime else "movie" if args.movie else "tv" if args.tv else None
    engine = ResourceHunterEngine()
    intent = parse_intent(args.keyword, explicit_kind=explicit_kind, channel="torrent")
    response = engine.search(intent, limit=args.limit)
    if args.engine != "all":
        response["results"] = [item for item in response["results"] if item["source"] == args.engine]
    if args.json_output:
        print(dump_json(response))
    else:
        print(format_search_text(response, max_results=args.limit))
    return 0


def legacy_video_main(argv: list[str] | None = None) -> int:
    ensure_utf8_stdio()
    argv = list(argv if argv is not None else sys.argv[1:])
    return main(["video"] + argv)
