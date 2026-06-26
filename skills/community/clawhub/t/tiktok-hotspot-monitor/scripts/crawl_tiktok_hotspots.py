from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "tiktok_hotspot_sources.json"
SOURCE_TYPES = {"keyword", "hashtag", "creator", "music"}
PROVIDER_TYPES = {"tiktok_mcp", "apify"}


@dataclass(frozen=True)
class CrawlWindow:
    name: str
    label: str
    weight: int
    input_overrides: dict[str, Any]


@dataclass(frozen=True)
class Source:
    type: str
    value: str
    limit: int
    enabled: bool = True


@dataclass(frozen=True)
class CrawlRequest:
    source: Source
    window: CrawlWindow | None
    limit: int


@dataclass(frozen=True)
class CrawlerConfig:
    market: str
    output_base_dir: Path
    snapshots_dir: Path
    logs_dir: Path
    schedule_enabled: bool
    interval_minutes: int
    provider_type: str
    tiktok_mcp_command: str
    tiktok_mcp_args: list[str]
    tiktok_mcp_cwd: Path | None
    tiktok_mcp_timeout_seconds: int
    tiktok_mcp_reject_simulated: bool
    tiktok_mcp_env: dict[str, str]
    apify_actor_id: str | None
    apify_token_env: str
    apify_input_defaults: dict[str, Any]
    apify_input_templates: dict[str, Any]
    apify_crawl_windows: dict[str, list[CrawlWindow]]
    sources: list[Source]


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def load_dotenv(path: Path = PROJECT_ROOT / ".env") -> None:
    if not path.exists():
        return

    with path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            if key and key not in os.environ:
                os.environ[key] = value.strip().strip('"').strip("'")


def load_config(path: Path) -> CrawlerConfig:
    with path.open("r", encoding="utf-8") as file:
        raw = json.load(file)

    output = raw.get("output", {})
    schedule = raw.get("schedule", {})
    provider = raw.get("provider", {})
    tiktok_mcp = raw.get("tiktok_mcp", {})
    apify = raw.get("apify", {})
    apify_input = apify.get("input", {})
    apify_input_defaults = as_mapping(apify_input.get("defaults", {}), "apify.input.defaults")
    apify_input_templates = as_mapping(apify_input.get("per_source", {}), "apify.input.per_source")
    apify_crawl_windows = parse_crawl_windows(apify_input.get("crawl_windows", {}))
    defaults = raw.get("defaults", {})

    base_dir = resolve_project_path(output.get("base_dir", "data/tiktok_hotspots"))
    snapshots_dir = resolve_output_path(base_dir, output.get("snapshots_dir", "snapshots"))
    logs_dir = resolve_output_path(base_dir, output.get("logs_dir", "logs"))

    provider_type = str(provider.get("type", "tiktok_mcp")).strip().lower()
    if provider_type not in PROVIDER_TYPES:
        raise ValueError(f"provider.type must be one of {sorted(PROVIDER_TYPES)}")

    default_limit = positive_int(defaults.get("limit", 10), "defaults.limit")
    interval_minutes = positive_int(schedule.get("interval_minutes", 60), "schedule.interval_minutes")
    tiktok_mcp_timeout_seconds = positive_int(tiktok_mcp.get("timeout_seconds", 120), "tiktok_mcp.timeout_seconds")
    tiktok_mcp_command = optional_string(tiktok_mcp.get("command")) or "python"
    tiktok_mcp_args = as_string_list(tiktok_mcp.get("args", ["-m", "tiktok_mcp_service.main"]), "tiktok_mcp.args")
    tiktok_mcp_cwd = optional_path(tiktok_mcp.get("cwd"))
    tiktok_mcp_env = {key: str(value) for key, value in as_mapping(tiktok_mcp.get("env", {}), "tiktok_mcp.env").items()}

    apify_actor_id = optional_string(provider.get("actor_id")) or optional_string(apify.get("actor_id"))
    if provider_type == "apify" and not apify_actor_id:
        raise ValueError("apify.actor_id is required when provider.type is apify")

    sources = [parse_source(item, default_limit, index) for index, item in enumerate(raw.get("sources", []), start=1)]
    enabled_sources = [source for source in sources if source.enabled]
    if not enabled_sources:
        raise ValueError("At least one enabled source is required")

    return CrawlerConfig(
        market=str(raw.get("market", "US")),
        output_base_dir=base_dir,
        snapshots_dir=snapshots_dir,
        logs_dir=logs_dir,
        schedule_enabled=bool(schedule.get("enabled", False)),
        interval_minutes=interval_minutes,
        provider_type=provider_type,
        tiktok_mcp_command=tiktok_mcp_command,
        tiktok_mcp_args=tiktok_mcp_args,
        tiktok_mcp_cwd=tiktok_mcp_cwd,
        tiktok_mcp_timeout_seconds=tiktok_mcp_timeout_seconds,
        tiktok_mcp_reject_simulated=bool(tiktok_mcp.get("reject_simulated", True)),
        tiktok_mcp_env=tiktok_mcp_env,
        apify_actor_id=apify_actor_id,
        apify_token_env=str(apify.get("token_env", "APIFY_TOKEN")),
        apify_input_defaults=apify_input_defaults,
        apify_input_templates=apify_input_templates,
        apify_crawl_windows=apify_crawl_windows,
        sources=sources,
    )


def parse_source(raw: dict[str, Any], default_limit: int, index: int) -> Source:
    source_type = str(raw.get("type", "")).strip().lower()
    if source_type not in SOURCE_TYPES:
        raise ValueError(f"sources[{index}].type must be one of {sorted(SOURCE_TYPES)}")

    enabled = bool(raw.get("enabled", True))
    value = str(raw.get("value", "")).strip()
    if enabled and not value:
        raise ValueError(f"sources[{index}].value is required when enabled")

    return Source(
        type=source_type,
        value=value,
        limit=positive_int(raw.get("limit", default_limit), f"sources[{index}].limit"),
        enabled=enabled,
    )



def parse_crawl_windows(raw: Any) -> dict[str, list[CrawlWindow]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("apify.input.crawl_windows must be an object")

    windows_by_type: dict[str, list[CrawlWindow]] = {}
    for source_type, items in raw.items():
        source_type = str(source_type).strip().lower()
        if source_type not in SOURCE_TYPES and source_type != "default":
            raise ValueError(f"apify.input.crawl_windows.{source_type} must target a known source type or default")
        if not isinstance(items, list):
            raise ValueError(f"apify.input.crawl_windows.{source_type} must be a list")
        windows_by_type[source_type] = [parse_crawl_window(item, source_type, index) for index, item in enumerate(items, start=1)]
    return windows_by_type


def parse_crawl_window(raw: Any, source_type: str, index: int) -> CrawlWindow:
    if not isinstance(raw, dict):
        raise ValueError(f"apify.input.crawl_windows.{source_type}[{index}] must be an object")
    name = optional_string(raw.get("name"))
    if not name:
        raise ValueError(f"apify.input.crawl_windows.{source_type}[{index}].name is required")
    return CrawlWindow(
        name=name,
        label=optional_string(raw.get("label")) or name,
        weight=positive_int(raw.get("weight", 1), f"apify.input.crawl_windows.{source_type}[{index}].weight"),
        input_overrides=as_mapping(raw.get("input", {}), f"apify.input.crawl_windows.{source_type}[{index}].input"),
    )


def positive_int(value: Any, name: str) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{name} must be a positive integer") from exc
    if parsed <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return parsed


def optional_string(value: Any) -> str | None:
    if value is None:
        return None
    parsed = str(value).strip()
    return parsed or None



def as_mapping(value: Any, name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    return value


def as_string_list(value: Any, name: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")
    return [str(item) for item in value]


def optional_path(value: Any) -> Path | None:
    parsed = optional_string(value)
    return resolve_project_path(parsed) if parsed else None


def resolve_project_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else PROJECT_ROOT / path


def resolve_output_path(base_dir: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else base_dir / path


def build_target(source: Source) -> str:
    if source.type == "keyword":
        return source.value
    if source.type == "hashtag":
        return f"#{source.value.lstrip('#')}"
    if source.type == "creator":
        handle = source.value.lstrip("@")
        return f"https://www.tiktok.com/@{handle}"
    return source.value


def fetch_source(config: CrawlerConfig, request: CrawlRequest) -> tuple[list[dict[str, Any]], str | None]:
    if config.provider_type == "apify":
        return fetch_source_apify(config, request)
    return fetch_source_tiktok_mcp(config, request)


def build_tiktok_mcp_search_term(source: Source) -> str:
    if source.type == "keyword":
        return source.value
    if source.type == "hashtag":
        return f"#{source.value.lstrip('#')}"
    raise ValueError(f"tiktok_mcp provider only supports keyword and hashtag sources, got {source.type}")


def fetch_source_tiktok_mcp(config: CrawlerConfig, request: CrawlRequest) -> tuple[list[dict[str, Any]], str | None]:
    try:
        records, response = asyncio.run(call_tiktok_mcp_search(config, request))
    except ImportError:
        return [], "mcp is not installed; run python -m pip install -r requirements.txt"
    except ValueError as exc:
        return [], str(exc)
    except Exception as exc:
        return [], f"TikTok MCP search failed: {exc}"

    transformations = response.get("transformations") if isinstance(response, dict) else None
    if transformations and config.tiktok_mcp_reject_simulated:
        return [], "TikTok MCP returned simulated results; rejected by tiktok_mcp.reject_simulated"

    errors = response.get("errors") if isinstance(response, dict) else None
    if errors:
        return records, json.dumps(errors, ensure_ascii=False)
    return records, None


async def call_tiktok_mcp_search(config: CrawlerConfig, request: CrawlRequest) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    search_term = build_tiktok_mcp_search_term(request.source)
    server_params = StdioServerParameters(
        command=config.tiktok_mcp_command,
        args=config.tiktok_mcp_args,
        env={**os.environ, **config.tiktok_mcp_env},
        cwd=config.tiktok_mcp_cwd,
        encoding_error_handler="replace",
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await asyncio.wait_for(session.initialize(), timeout=config.tiktok_mcp_timeout_seconds)
            result = await asyncio.wait_for(
                session.call_tool("search_videos", arguments={"search_terms": [search_term], "count": request.limit}),
                timeout=config.tiktok_mcp_timeout_seconds,
            )

    response = parse_mcp_tool_response(result)
    term_records = response.get("results", {}).get(search_term, [])
    if not isinstance(term_records, list):
        raise ValueError("TikTok MCP returned an invalid results payload")
    return [normalize_tiktok_mcp_raw_record(item, search_term) for item in term_records if isinstance(item, dict)], response


def parse_mcp_tool_response(result: Any) -> dict[str, Any]:
    structured = getattr(result, "structuredContent", None)
    if isinstance(structured, dict):
        return structured

    content = getattr(result, "content", [])
    for item in content:
        item_type = getattr(item, "type", None)
        item_text = getattr(item, "text", None)
        if item_type == "text" and item_text:
            parsed = json.loads(item_text)
            if isinstance(parsed, dict):
                return parsed
    raise ValueError("TikTok MCP did not return JSON content")


def normalize_tiktok_mcp_raw_record(raw: dict[str, Any], search_term: str) -> dict[str, Any]:
    normalized = dict(raw)
    stats = raw.get("stats") if isinstance(raw.get("stats"), dict) else {}
    normalized["search_query"] = search_term
    normalized["webpage_url"] = raw.get("url")
    normalized["title"] = raw.get("description")
    normalized["view_count"] = parse_optional_int(stats.get("views"))
    normalized["like_count"] = parse_optional_int(stats.get("likes"))
    normalized["share_count"] = parse_optional_int(stats.get("shares"))
    normalized["comment_count"] = parse_optional_int(stats.get("comments"))
    normalized["uploader"] = raw.get("author")
    normalized["video_id"] = extract_tiktok_video_id(raw.get("url"))
    return normalized


def extract_tiktok_video_id(url: Any) -> str | None:
    if not isinstance(url, str):
        return None
    marker = "/video/"
    if marker not in url:
        return None
    return url.split(marker, 1)[1].split("?", 1)[0].strip("/") or None


def parse_optional_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(str(value).replace(",", ""))
    except ValueError:
        return None


def fetch_source_apify(config: CrawlerConfig, request: CrawlRequest) -> tuple[list[dict[str, Any]], str | None]:
    token = optional_string(os.environ.get(config.apify_token_env))
    if not token:
        return [], f"Apify token environment variable is not set: {config.apify_token_env}"

    try:
        from apify_client import ApifyClient
    except ImportError:
        return [], "apify-client is not installed; run python -m pip install -r requirements.txt"

    try:
        run_input = build_apify_run_input(config, request)
    except ValueError as exc:
        return [], str(exc)

    try:
        client = ApifyClient(token)
        actor_run = client.actor(config.apify_actor_id).call(run_input=run_input)
        dataset_id = actor_run.get("defaultDatasetId") if actor_run else None
        if not dataset_id:
            return [], "Apify actor run did not return a defaultDatasetId"
        items = client.dataset(dataset_id).list_items().items
    except Exception as exc:
        return [], f"Apify actor failed: {exc}"

    records = [item for item in items if isinstance(item, dict) and not item.get("error") and not item.get("errorCode")]
    errors = [item for item in items if isinstance(item, dict) and (item.get("error") or item.get("errorCode"))]
    if errors:
        message = first_value(errors[0], ["error", "errorCode"]) or "Apify dataset contains error items"
        return records, str(message)
    return records, None


def build_apify_run_input(config: CrawlerConfig, request: CrawlRequest) -> dict[str, Any]:
    source = request.source
    run_input = render_template(config.apify_input_defaults, config, request)
    if not isinstance(run_input, dict):
        raise ValueError("apify.input.defaults must render to an object")

    source_template = config.apify_input_templates.get(source.type) or config.apify_input_templates.get("default")
    if source_template is None:
        source_input = {
            "source_type": source.type,
            "source_value": source.value,
            "source_target": build_target(source),
            "limit": request.limit,
            "market": config.market,
        }
    else:
        source_input = render_template(source_template, config, request)
        if not isinstance(source_input, dict):
            raise ValueError(f"apify.input.per_source.{source.type} must render to an object")

    window_input: dict[str, Any] = {}
    if request.window is not None:
        rendered_window = render_template(request.window.input_overrides, config, request)
        if not isinstance(rendered_window, dict):
            raise ValueError(f"apify.input.crawl_windows.{source.type}.{request.window.name}.input must render to an object")
        window_input = rendered_window

    return {**run_input, **source_input, **window_input}


def render_template(value: Any, config: CrawlerConfig, request: CrawlRequest) -> Any:
    source = request.source
    context = {
        "market": config.market,
        "source_type": source.type,
        "source_value": source.value,
        "source_value_without_prefix": source.value.lstrip("#@"),
        "source_target": build_target(source),
        "limit": request.limit,
        "source_limit": source.limit,
        "crawl_window": request.window.name if request.window else "default",
        "crawl_window_label": request.window.label if request.window else "Default",
    }
    if isinstance(value, str):
        if value == "{limit}":
            return request.limit
        if value == "{source_limit}":
            return source.limit
        return value.format_map(context)
    if isinstance(value, list):
        return [render_template(item, config, request) for item in value]
    if isinstance(value, dict):
        return {key: render_template(item, config, request) for key, item in value.items()}
    return value


def normalize_record(raw: dict[str, Any], request: CrawlRequest, crawl_timestamp: str) -> dict[str, Any]:
    source = request.source
    return {
        "crawl_timestamp": crawl_timestamp,
        "source_type": source.type,
        "source_value": source.value,
        "crawl_window": request.window.name if request.window else "default",
        "crawl_window_label": request.window.label if request.window else "Default",
        "crawl_window_limit": request.limit,
        "video_id": first_value(raw, ["id", "video_id", "videoId", "awemeId", "itemInfo.itemStruct.id"]),
        "webpage_url": first_value(raw, ["webpage_url", "url", "webVideoUrl", "shareUrl", "itemInfo.itemStruct.shareInfo.shareUrl"]),
        "title": first_value(raw, ["title", "description", "desc", "text"]),
        "description": first_value(raw, ["description", "desc", "text", "title"]),
        "text_language": first_value(raw, ["textLanguage", "text_language", "descLanguage"]),
        "uploader": first_value(raw, ["uploader", "authorMeta.name", "authorMeta.nickName", "author.nickname", "author.uniqueId"]),
        "uploader_id": first_value(raw, ["uploader_id", "authorMeta.id", "authorMeta.profileUrl", "author.id", "author.uniqueId"]),
        "uploader_profile_url": first_value(raw, ["authorMeta.profileUrl", "author.profileUrl", "author.url"]),
        "uploader_follower_count": first_value(raw, ["authorMeta.fans", "authorMeta.followerCount", "author.followerCount", "author.stats.followerCount"]),
        "uploader_like_count": first_value(raw, ["authorMeta.heart", "authorMeta.heartCount", "author.heartCount", "author.stats.heartCount"]),
        "upload_date": first_value(raw, ["upload_date", "createTimeISO", "createTime"]),
        "timestamp": first_value(raw, ["timestamp", "createTime", "createTimestamp"]),
        "duration": first_value(raw, ["duration", "videoMeta.duration", "video.duration"]),
        "view_count": first_value(raw, ["view_count", "playCount", "stats.playCount", "itemInfo.itemStruct.stats.playCount"]),
        "like_count": first_value(raw, ["like_count", "diggCount", "stats.diggCount", "itemInfo.itemStruct.stats.diggCount"]),
        "comment_count": first_value(raw, ["comment_count", "commentCount", "stats.commentCount", "itemInfo.itemStruct.stats.commentCount"]),
        "share_count": first_value(raw, ["share_count", "shareCount", "stats.shareCount", "itemInfo.itemStruct.stats.shareCount"]),
        "repost_count": first_value(raw, ["repost_count", "repostCount", "stats.repostCount"]),
        "collect_count": first_value(raw, ["collect_count", "collectCount", "stats.collectCount", "itemInfo.itemStruct.stats.collectCount"]),
        "hashtags": extract_hashtags(raw),
        "mentions": first_value(raw, ["mentions", "detailedMentions"]),
        "is_ad": first_value(raw, ["isAd", "is_ad"]),
        "is_slideshow": first_value(raw, ["isSlideshow", "is_slideshow"]),
        "is_pinned": first_value(raw, ["isPinned", "is_pinned"]),
        "search_query": first_value(raw, ["searchQuery", "search_query"]),
        "cover_url": first_value(raw, ["videoMeta.coverUrl", "video.cover", "coverUrl"]),
        "media_urls": first_value(raw, ["mediaUrls", "media_urls"]),
        "music": extract_music(raw),
        "raw_metadata": raw,
    }


def extract_hashtags(raw: dict[str, Any]) -> list[str] | None:
    hashtags = first_value(raw, ["hashtags", "challenges", "itemInfo.itemStruct.challenges"])
    if not isinstance(hashtags, list):
        return None

    names: list[str] = []
    for item in hashtags:
        if isinstance(item, str) and item:
            names.append(item.lstrip("#"))
        elif isinstance(item, dict):
            name = first_value(item, ["name", "title", "hashtagName"])
            if name:
                names.append(str(name).lstrip("#"))
    return names


def extract_music(raw: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": first_value(raw, ["musicMeta.musicId", "music.id", "musicInfo.music.id"]),
        "track": first_value(raw, ["track", "musicMeta.musicName", "music.title", "musicInfo.music.title"]),
        "artist": first_value(raw, ["artist", "musicMeta.musicAuthor", "music.authorName", "musicInfo.music.authorName"]),
        "album": first_value(raw, ["album", "music.album"]),
        "is_original": first_value(raw, ["musicMeta.musicOriginal", "music.original", "musicInfo.music.original"]),
        "play_url": first_value(raw, ["musicMeta.playUrl", "music.playUrl", "musicInfo.music.playUrl"]),
        "cover_url": first_value(raw, ["musicMeta.coverMediumUrl", "music.coverMediumUrl", "musicInfo.music.coverMediumUrl"]),
    }


def first_value(raw: dict[str, Any], paths: list[str]) -> Any:
    for path in paths:
        value = nested_value(raw, path)
        if value not in (None, ""):
            return value
    return None


def nested_value(raw: dict[str, Any], path: str) -> Any:
    value: Any = raw
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return None
        value = value[part]
    return value



def crawl_windows_for(config: CrawlerConfig, source: Source) -> list[CrawlWindow]:
    return config.apify_crawl_windows.get(source.type) or config.apify_crawl_windows.get("default") or []


def build_crawl_requests(config: CrawlerConfig, max_sources: int | None = None) -> list[CrawlRequest]:
    enabled_sources = [source for source in config.sources if source.enabled]
    if max_sources is not None:
        enabled_sources = enabled_sources[:max_sources]

    requests: list[CrawlRequest] = []
    for source in enabled_sources:
        windows = crawl_windows_for(config, source)
        if not windows or config.provider_type != "apify":
            requests.append(CrawlRequest(source=source, window=None, limit=source.limit))
            continue
        for window, limit in split_limit_by_weight(source.limit, windows):
            requests.append(CrawlRequest(source=source, window=window, limit=limit))
    return requests


def split_limit_by_weight(limit: int, windows: list[CrawlWindow]) -> list[tuple[CrawlWindow, int]]:
    if limit < len(windows):
        selected = sorted(enumerate(windows), key=lambda item: (-item[1].weight, item[0]))[:limit]
        windows = [window for _, window in sorted(selected, key=lambda item: item[0])]

    total_weight = sum(window.weight for window in windows)
    allocations: list[tuple[CrawlWindow, int, float]] = []
    allocated = 0
    for window in windows:
        exact = limit * window.weight / total_weight
        window_limit = max(1, int(exact))
        allocations.append((window, window_limit, exact - int(exact)))
        allocated += window_limit

    while allocated < limit:
        index = max(range(len(allocations)), key=lambda item: allocations[item][2])
        window, window_limit, remainder = allocations[index]
        allocations[index] = (window, window_limit + 1, remainder)
        allocated += 1

    while allocated > limit and len(allocations) > 1:
        candidates = [index for index, (_, window_limit, _) in enumerate(allocations) if window_limit > 1]
        if not candidates:
            break
        index = min(candidates, key=lambda item: allocations[item][2])
        window, window_limit, remainder = allocations[index]
        allocations[index] = (window, window_limit - 1, remainder)
        allocated -= 1

    return [(window, window_limit) for window, window_limit, _ in allocations]


def request_key(request: CrawlRequest) -> tuple[str, str]:
    return (request.source.type, request.source.value)


def request_window_name(request: CrawlRequest) -> str:
    return request.window.name if request.window else "default"


def request_window_label(request: CrawlRequest) -> str:
    return request.window.label if request.window else "Default"


def crawl_plan_metrics(requests: list[CrawlRequest]) -> dict[str, Any]:
    return {
        "enabled_source_count": len({request_key(request) for request in requests}),
        "crawl_window_count": len({request_window_name(request) for request in requests}),
        "planned_run_count": len(requests),
        "requested_total_limit": sum(request.limit for request in requests),
    }


def run_once(config: CrawlerConfig, max_sources: int | None = None) -> tuple[Path, Path, dict[str, Any]]:
    crawl_timestamp = utc_timestamp()
    config.snapshots_dir.mkdir(parents=True, exist_ok=True)
    config.logs_dir.mkdir(parents=True, exist_ok=True)

    snapshot_path = config.snapshots_dir / f"tiktok_hotspots_{crawl_timestamp}.jsonl"
    log_path = config.logs_dir / f"tiktok_hotspots_{crawl_timestamp}.jsonl"
    requests = build_crawl_requests(config, max_sources)
    summary: dict[str, Any] = {
        "crawl_timestamp": crawl_timestamp,
        "event": "crawl_round_summary",
        "provider": config.provider_type,
        **crawl_plan_metrics(requests),
        "completed_run_count": 0,
        "failed_run_count": 0,
        "raw_record_count": 0,
        "cost_model_note": "Apify cost depends on Actor pricing, planned runs, returned results, compute duration, memory, proxy usage, retries, add-ons, and account plan; verify exact cost in the Apify usage dashboard.",
        "windows": {},
    }

    with snapshot_path.open("w", encoding="utf-8") as snapshot_file, log_path.open("w", encoding="utf-8") as log_file:
        for request in requests:
            source = request.source
            started_at = datetime.now(timezone.utc).isoformat()
            raw_records, error = fetch_source(config, request)
            normalized_records = [normalize_record(raw, request, crawl_timestamp) for raw in raw_records]
            for record in normalized_records:
                snapshot_file.write(json.dumps(record, ensure_ascii=False) + "\n")
            window_name = request_window_name(request)
            window_summary = summary["windows"].setdefault(
                window_name,
                {
                    "label": request_window_label(request),
                    "planned_run_count": 0,
                    "completed_run_count": 0,
                    "failed_run_count": 0,
                    "requested_limit": 0,
                    "raw_record_count": 0,
                },
            )
            summary["raw_record_count"] += len(normalized_records)
            summary["failed_run_count" if error else "completed_run_count"] += 1
            window_summary["planned_run_count"] += 1
            window_summary["requested_limit"] += request.limit
            window_summary["raw_record_count"] += len(normalized_records)
            window_summary["failed_run_count" if error else "completed_run_count"] += 1
            log_entry = {
                "crawl_timestamp": crawl_timestamp,
                "started_at": started_at,
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "provider": config.provider_type,
                "source_type": source.type,
                "source_value": source.value,
                "source_limit": source.limit,
                "crawl_window": window_name,
                "crawl_window_label": request_window_label(request),
                "crawl_window_limit": request.limit,
                "status": "failed" if error else "success",
                "record_count": len(normalized_records),
                "error": error,
            }
            log_file.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
            log_file.flush()
            snapshot_file.flush()

        log_file.write(json.dumps(summary, ensure_ascii=False) + "\n")

    video_ids = set()
    for line in snapshot_path.read_text(encoding="utf-8").splitlines():
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        video_id = record.get("video_id") if isinstance(record, dict) else None
        if video_id:
            video_ids.add(str(video_id))
    summary["unique_video_count"] = len(video_ids)
    summary["duplicate_rate"] = 0.0 if not summary["raw_record_count"] else round(1 - len(video_ids) / summary["raw_record_count"], 4)

    lines = log_path.read_text(encoding="utf-8").splitlines()
    lines[-1] = json.dumps(summary, ensure_ascii=False)
    log_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return snapshot_path, log_path, summary



def run_schedule(config: CrawlerConfig) -> None:
    while True:
        snapshot_path, log_path, summary = run_once(config)
        print(
            f"crawl complete: records={summary['raw_record_count']} failed_runs={summary['failed_run_count']}/{summary['planned_run_count']} "
            f"snapshot={snapshot_path} log={log_path}",
            flush=True,
        )
        time.sleep(config.interval_minutes * 60)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Crawl TikTok hotspot candidate metadata snapshots.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--once", action="store_true", help="Run one crawl and exit.")
    mode.add_argument("--schedule", action="store_true", help="Run continuously with the configured interval.")
    parser.add_argument("--max-sources", type=int, default=None, help="Limit enabled sources for smoke tests.")
    return parser.parse_args()


def main() -> int:
    load_dotenv()
    args = parse_args()
    try:
        config = load_config(args.config)
        if args.schedule:
            run_schedule(config)
            return 0
        snapshot_path, log_path, summary = run_once(config, args.max_sources)
    except ValueError as exc:
        print(f"configuration error: {exc}", file=sys.stderr)
        return 2

    print(f"snapshot: {snapshot_path}")
    print(f"log: {log_path}")
    print(f"records: {summary['raw_record_count']}")
    print(f"unique_videos: {summary.get('unique_video_count', 'unknown')}")
    print(f"planned_runs: {summary['planned_run_count']}")
    print(f"completed_runs: {summary['completed_run_count']}")
    print(f"failed_runs: {summary['failed_run_count']}")
    print(f"requested_total_limit: {summary['requested_total_limit']}")
    return 1 if summary["planned_run_count"] and summary["failed_run_count"] == summary["planned_run_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
