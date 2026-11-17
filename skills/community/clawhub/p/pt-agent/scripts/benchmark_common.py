#!/usr/bin/env python3
"""Run safe, repeatable pt-agent common-operation benchmarks."""

from __future__ import annotations

import argparse
import json
import os
import statistics
import subprocess
import sys
import tempfile
import threading
import time
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "scripts" / "pt_runtime.py"
STORE = ROOT / "scripts" / "pt_store.py"
sys.dont_write_bytecode = True
sys.path.insert(0, str(ROOT / "scripts"))
import pt_store  # noqa: E402


PayloadCheck = Callable[[dict[str, Any]], bool]


class FixtureHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def send_bytes(self, body: bytes, content_type: str = "text/plain; charset=utf-8") -> None:
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/v2/app/version":
            self.send_bytes(b"v5.0.3")
            return
        if parsed.path == "/api/v2/sync/maindata":
            payload = {
                "server_state": {"free_space_on_disk": 500 * 1024**3, "dl_info_speed": 2048, "up_info_speed": 1024},
                "torrents": {
                    "a": {"state": "downloading", "progress": 0.5, "dlspeed": 2048, "upspeed": 0},
                    "b": {"state": "stalledUP", "progress": 1, "dlspeed": 0, "upspeed": 1024},
                },
            }
            self.send_bytes(json.dumps(payload).encode(), "application/json")
            return
        if parsed.path == "/api/v2/torrents/info":
            self.send_bytes(b"[]", "application/json")
            return
        if parsed.path == "/download.php":
            self.send_response(200)
            body = b"d8:announce13:http://local4:infod4:name7:fixtureee"
            self.send_header("Content-Type", "application/x-bittorrent")
            self.send_header("Content-Disposition", 'attachment; filename="fixture.torrent"')
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/torrents.php":
            keyword = urllib.parse.parse_qs(parsed.query).get("search", [""])[0]
            if "庆余年" in keyword:
                rows = [("庆余年 S01 1080p", "TV", "12.0 GB", 88, "")]
            else:
                rows = [
                    (f"{keyword or '周星驰'} 电影 2160p", "Movie", "24.0 GB", 120, "pro_free"),
                    (f"{keyword or '周星驰'} 花絮 1080p", "Movie", "4.0 GB", 40, ""),
                ]
            body_rows = "".join(
                "<tr class='torrent-row {tag}'><td>{category}</td>"
                "<td><a href='details.php?id={index}' title='{title}'>{title}</a>"
                "<a href='download.php?id={index}'>download</a></td>"
                "<td>{size}</td><td>{seeders}</td><td>2</td><td>50</td></tr>".format(
                    tag=tag,
                    category=category,
                    index=index,
                    title=title,
                    size=size,
                    seeders=seeders,
                )
                for index, (title, category, size, seeders, tag) in enumerate(rows, start=1)
            )
            html = (
                "<html><table><tr><th>Category</th><th>Name</th><th>Size</th>"
                "<th>Seeders</th><th>Leechers</th><th>Completed</th></tr>"
                f"{body_rows}</table></html>"
            )
            self.send_bytes(html.encode("utf-8"), "text/html; charset=utf-8")
            return
        stats = "分享率: 7.813 上传量: 2.481 TB 下载量: 325.22 GB 魔力值: 5,196,765.0"
        self.send_bytes(stats.encode("utf-8"), "text/html; charset=utf-8")

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length") or 0)
        if content_length:
            self.rfile.read(content_length)
        self.send_bytes(b"Ok.")

    def log_message(self, _format: str, *_args: Any) -> None:
        return


def run_case(
    name: str,
    program: Path,
    args: list[str],
    timeout: int,
    repeats: int,
    env: dict[str, str],
    check: PayloadCheck,
) -> dict[str, Any]:
    timings: list[float] = []
    payload: dict[str, Any] = {}
    return_code = 1
    error_code: str | None = None
    for _index in range(repeats):
        started = time.monotonic()
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as output:
            try:
                completed = subprocess.run(
                    [sys.executable, str(program), *args],
                    stdout=output,
                    stderr=subprocess.DEVNULL,
                    timeout=timeout,
                    env=env,
                    check=False,
                )
                elapsed = (time.monotonic() - started) * 1000
                output.seek(0)
                payload = json.load(output)
                return_code = completed.returncode
                error_code = (payload.get("error") or {}).get("code") or (
                    ((payload.get("failures") or [{}])[0].get("error") or {}).get("code")
                )
                timings.append(elapsed)
            except (subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
                error_code = "timeout" if isinstance(exc, subprocess.TimeoutExpired) else "invalid_json"
                break
    payload_valid = bool(payload) and check(payload)
    successful = len(timings) == repeats and return_code == 0 and payload.get("ok", True) is not False and payload_valid
    return {
        "name": name,
        "ok": successful,
        "medianMs": round(statistics.median(timings)) if timings else None,
        "minMs": round(min(timings)) if timings else None,
        "maxMs": round(max(timings)) if timings else None,
        "returnCode": return_code,
        "errorCode": error_code,
        "validationError": None if payload_valid else "unexpected_payload",
        "total": payload.get("total"),
        "dryRun": payload.get("dryRun", False),
    }


def tracker_record(tracker_id: str, base_url: str) -> dict[str, Any]:
    return {
        "id": tracker_id,
        "displayName": tracker_id,
        "adapterId": "nexusphp",
        "authMode": "cookie",
        "baseUrl": base_url,
        "secretRefs": {"cookie": "env://PT_AGENT_BENCHMARK_COOKIE"},
        "status": "configured",
    }


def field_equals(path: str, expected: Any) -> PayloadCheck:
    keys = path.split(".")

    def check(payload: dict[str, Any]) -> bool:
        current: Any = payload
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return False
            current = current[key]
        return current == expected

    return check


def field_count(path: str, expected: int) -> PayloadCheck:
    keys = path.split(".")

    def check(payload: dict[str, Any]) -> bool:
        current: Any = payload
        for key in keys:
            if not isinstance(current, dict) or key not in current:
                return False
            current = current[key]
        return isinstance(current, (list, dict)) and len(current) == expected

    return check


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark safe pt-agent common operations")
    parser.add_argument("--live", action="store_true", help="include read-only checks against the configured store")
    parser.add_argument("--tracker", help="tracker id or alias; defaults to the configured search tracker")
    parser.add_argument("--movie-query", default="周星驰的电影")
    parser.add_argument("--tv-query", default="庆余年电视剧")
    parser.add_argument("--timeout", type=int, default=15)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    repeats = max(1, min(args.repeats, 20))

    server = ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler)
    server_thread = threading.Thread(target=server.serve_forever, daemon=True)
    server_thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PT_AGENT_BENCHMARK_COOKIE": "session=fixture"}

    try:
        with tempfile.TemporaryDirectory(prefix="pt-agent-benchmark-") as temp_dir:
            fixture_path = Path(temp_dir) / "store.json"
            fixture = pt_store.empty_store()
            fixture["trackers"] = {
                "benchmark-a": tracker_record("benchmark-a", base_url),
                "benchmark-b": tracker_record("benchmark-b", base_url),
            }
            fixture["downloaders"] = {
                "benchmark-qb": {
                    "id": "benchmark-qb",
                    "type": "qbittorrent",
                    "baseUrl": base_url,
                    "enabled": True,
                    "status": "configured",
                }
            }
            fixture["defaultSearchSolutionId"] = "benchmark-a"
            fixture["defaultDownloaderId"] = "benchmark-qb"
            pt_store.atomic_write(fixture_path, fixture)
            store_args = ["--store", str(fixture_path)]
            magnet = "magnet:?xt=urn:btih:0000000000000000000000000000000000000000"
            first_site = json.loads((ROOT / "references" / "site-preset-catalog.json").read_text())["sites"][0]["id"]

            cases: list[tuple[str, Path, list[str], PayloadCheck]] = [
                ("store-location", STORE, [*store_args, "location"], field_equals("exists", True)),
                ("store-summary", STORE, [*store_args, "summary"], field_count("trackers", 2)),
                ("store-doctor", STORE, [*store_args, "doctor"], field_equals("counts.trackers", 2)),
                ("store-audit-secrets", STORE, [*store_args, "audit-secrets"], field_count("rawSecretLikePaths", 0)),
                ("store-find-tracker", STORE, [*store_args, "find-tracker", "benchmark-a"], field_equals("found", True)),
                ("store-set-state", STORE, [*store_args, "set-state", "--json", '{"lastView":"overview"}'], field_equals("interactionState.lastView", "overview")),
                ("store-upsert-stats", STORE, [*store_args, "upsert-stats", "--tracker", "benchmark-a", "--json", '{"status":"ok","ratio":2.5}'], field_equals("record.ratio", 2.5)),
                ("site-presets", RUNTIME, ["site-presets", first_site], field_equals("total", 1)),
                ("adapter-presets", RUNTIME, ["adapter-presets", "nexusphp"], lambda payload: payload.get("adapters", [{}])[0].get("id") == "nexusphp"),
                ("first-run", RUNTIME, [*store_args, "first-run"], field_equals("summary.enabledTrackers", 2)),
                ("overview-cached", RUNTIME, [*store_args, "overview"], field_count("trackers", 2)),
                ("validate-tracker", RUNTIME, [*store_args, "validate-tracker", "--tracker", "benchmark-a"], field_equals("status", "statically_valid")),
                ("health-check", RUNTIME, [*store_args, "health-check", "--tracker", "benchmark-a"], field_equals("status", "authenticated_or_public")),
                ("user-stats-persist", RUNTIME, [*store_args, "user-stats", "--tracker", "benchmark-a", "--persist"], field_equals("stats.ratio", 7.813)),
                ("search", RUNTIME, [*store_args, "search", "周星驰", "--tracker", "benchmark-a", "--limit", "5"], field_equals("total", 2)),
                ("movie-search-default", RUNTIME, [*store_args, "media-search", args.movie_query, "--kind", "movie", "--limit", "5"], lambda payload: payload.get("total") == 2 and "回复：下载第 1 个" in payload.get("display", {}).get("text", "")),
                ("tv-search", RUNTIME, [*store_args, "media-search", args.tv_query, "--kind", "tv", "--limit", "5"], field_equals("total", 1)),
                ("movie-free-4k", RUNTIME, [*store_args, "media-search", args.movie_query, "--kind", "movie", "--free-only", "--resolution", "4k", "--limit", "5"], lambda payload: payload.get("total") == 1 and payload.get("filters", {}).get("resolution") == "2160p"),
                ("movie-search-multisite", RUNTIME, [*store_args, "media-search", args.movie_query, "--all-trackers", "--kind", "movie", "--limit", "5"], lambda payload: payload.get("total") == 4 and len(payload.get("trackerIds", [])) == 2),
                ("overview-refresh", RUNTIME, [*store_args, "overview", "--refresh"], lambda payload: payload.get("refreshed") is True and payload.get("persisted") is True and len(payload.get("trackers", [])) == 2),
                ("downloader-status", RUNTIME, [*store_args, "downloader-status"], lambda payload: payload.get("version") == "v5.0.3" and payload.get("counts", {}).get("active") == 2),
                ("torrent-list-empty", RUNTIME, [*store_args, "list-torrents", "--filter", "paused", "--limit", "5"], lambda payload: "没有暂停的任务" in payload.get("display", {}).get("text", "")),
                ("magnet-dry-run", RUNTIME, [*store_args, "add-magnet", "--magnet", magnet, "--paused", "--dry-run"], field_equals("dryRun", True)),
                ("magnet-add", RUNTIME, [*store_args, "add-magnet", "--magnet", magnet, "--paused"], field_equals("status", "added")),
                ("torrent-dry-run", RUNTIME, [*store_args, "download-torrent", "--tracker", "benchmark-a", "--torrent-id", "12345", "--paused", "--dry-run"], field_equals("dryRun", True)),
                ("torrent-download", RUNTIME, [*store_args, "download-torrent", "--tracker", "benchmark-a", "--torrent-id", "12345", "--paused"], lambda payload: payload.get("status") == "added" and payload.get("filename") == "fixture.torrent"),
            ]
            results = [
                run_case(name, program, command, max(2, args.timeout), repeats, env, check)
                for name, program, command, check in cases
            ]

            if args.live:
                live_store_path, _source = pt_store.resolve_store_path()
                live_store = pt_store.load_store(live_store_path)
                selected_tracker = args.tracker or live_store.get("defaultSearchSolutionId")
                tracker_args = ["--tracker", str(selected_tracker)] if selected_tracker else []
                live_cases = [
                    ("live-health-check", RUNTIME, ["health-check", *tracker_args], lambda payload: "statusCode" in payload),
                    ("live-user-stats", RUNTIME, ["user-stats", *tracker_args], lambda payload: "stats" in payload),
                    ("live-movie-search", RUNTIME, ["media-search", args.movie_query, *tracker_args, "--kind", "movie", "--limit", "5"], lambda payload: "results" in payload),
                    ("live-tv-search", RUNTIME, ["media-search", args.tv_query, *tracker_args, "--kind", "tv", "--limit", "5"], lambda payload: "results" in payload),
                    ("live-downloader-status", RUNTIME, ["downloader-status"], lambda payload: "healthy" in payload),
                ]
                results.extend(
                    run_case(name, program, command, max(2, args.timeout), 1, env, check)
                    for name, program, command, check in live_cases
                )
    finally:
        server.shutdown()
        server.server_close()
        server_thread.join(timeout=2)

    payload = {"ok": all(result.get("ok") for result in results), "live": args.live, "repeats": repeats, "results": results}
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
