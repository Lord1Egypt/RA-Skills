#!/usr/bin/env python3
"""Compare one exact component ID across a few published package versions.

Online mode is deliberately limited to the official GitHub repository. Offline
mode accepts caller-provided version catalogues and uses the same parser, which
makes the query reproducible without bundling or caching historical databases.
"""

import argparse
import json
import math
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlparse
from urllib.request import HTTPRedirectHandler, Request, build_opener

import yaml

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


GITHUB_OWNER = "gongyu0918-debug"
GITHUB_REPOSITORY = "pc-build-assistant-skill"
GITHUB_API_HOST = "api.github.com"
GITHUB_RAW_HOST = "raw.githubusercontent.com"
COMPONENT_CATALOGUE = "data/components.yaml"
CASE_CATALOGUE = "data/cases.yaml"
ALLOWED_CATALOGUES = frozenset({COMPONENT_CATALOGUE, CASE_CATALOGUE})
MAX_VERSION_SEGMENT_DIGITS = 9
VERSION_SEGMENT_PATTERN = rf"(0|[1-9]\d{{0,{MAX_VERSION_SEGMENT_DIGITS - 1}}})"
TAG_PATTERN = re.compile(rf"^v{VERSION_SEGMENT_PATTERN}\.{VERSION_SEGMENT_PATTERN}\.{VERSION_SEGMENT_PATTERN}$")
COMMIT_PATTERN = re.compile(r"^[0-9a-f]{40}$")
DEFAULT_VERSION_COUNT = 5
DEFAULT_RECENT_COUNT = 3
DEFAULT_TIMEOUT_SECONDS = 10.0
DEFAULT_MAX_BYTES = 3_000_000
ABSOLUTE_MAX_BYTES = 16_000_000
MAX_VERSION_COUNT = 20
REDIRECT_STATUS_CODES = frozenset({301, 302, 303, 307, 308})


class RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, request, file_pointer, code, message, headers, new_url):
        raise HTTPError(request.full_url, code, "redirect rejected", headers, file_pointer)


NETWORK_OPENER = build_opener(RejectRedirects)


@dataclass
class QueryError(Exception):
    code: str
    message: str
    details: dict | None = None

    def as_result(self):
        result = {"ok": False, "reason": self.code, "message": self.message}
        if self.details:
            result.update(self.details)
        return result


@dataclass(frozen=True)
class ResolvedVersion:
    version: str
    commit_sha: str


def canonical_version(value):
    text = str(value or "").strip()
    if text and not text.startswith("v"):
        text = f"v{text}"
    if not TAG_PATTERN.fullmatch(text):
        raise QueryError("invalid_version", f"unsupported version: {value}")
    return text


def version_key(value):
    match = TAG_PATTERN.fullmatch(canonical_version(value))
    return tuple(int(part) for part in match.groups())


def catalogue_relative_path(item_id):
    return CASE_CATALOGUE if str(item_id).startswith("case-") else COMPONENT_CATALOGUE


def tags_api_url():
    return f"https://{GITHUB_API_HOST}/repos/{GITHUB_OWNER}/{GITHUB_REPOSITORY}/tags?per_page=100"


def tag_ref_api_url(version):
    tag = canonical_version(version)
    return f"https://{GITHUB_API_HOST}/repos/{GITHUB_OWNER}/{GITHUB_REPOSITORY}/git/ref/tags/{tag}"


def tag_object_api_url(tag_object_sha):
    sha = str(tag_object_sha or "").lower()
    if not COMMIT_PATTERN.fullmatch(sha):
        raise QueryError("invalid_commit", "GitHub returned an invalid tag object SHA")
    return f"https://{GITHUB_API_HOST}/repos/{GITHUB_OWNER}/{GITHUB_REPOSITORY}/git/tags/{sha}"


def raw_catalogue_url(commit_sha, item_id):
    sha = str(commit_sha or "").lower()
    if not COMMIT_PATTERN.fullmatch(sha):
        raise QueryError("invalid_commit", "GitHub returned an invalid commit SHA")
    relative = catalogue_relative_path(item_id)
    return f"https://{GITHUB_RAW_HOST}/{GITHUB_OWNER}/{GITHUB_REPOSITORY}/{sha}/{relative}"


def validate_remote_url(url):
    parsed = urlparse(url)
    try:
        port = parsed.port
    except ValueError as error:
        raise QueryError("remote_url_rejected", "remote URL is outside the fixed allowlist") from error
    if parsed.scheme != "https" or parsed.username or parsed.password or port or parsed.fragment:
        raise QueryError("remote_url_rejected", "remote URL is outside the fixed allowlist")
    if parsed.hostname == GITHUB_API_HOST:
        base = f"/repos/{GITHUB_OWNER}/{GITHUB_REPOSITORY}"
        if parsed.path == f"{base}/tags" and parse_qs(parsed.query) == {"per_page": ["100"]}:
            return
        if not parsed.query and not parsed.fragment:
            ref_prefix = f"{base}/git/ref/tags/"
            object_prefix = f"{base}/git/tags/"
            if parsed.path.startswith(ref_prefix) and TAG_PATTERN.fullmatch(parsed.path[len(ref_prefix):]):
                return
            if parsed.path.startswith(object_prefix) and COMMIT_PATTERN.fullmatch(parsed.path[len(object_prefix):]):
                return
        raise QueryError("remote_url_rejected", "GitHub API URL is outside the fixed allowlist")
    if parsed.hostname == GITHUB_RAW_HOST:
        prefix = f"/{GITHUB_OWNER}/{GITHUB_REPOSITORY}/"
        if not parsed.path.startswith(prefix) or parsed.query or parsed.fragment:
            raise QueryError("remote_url_rejected", "raw GitHub URL is outside the fixed allowlist")
        tail = parsed.path[len(prefix):]
        parts = tail.split("/", 1)
        if len(parts) != 2 or not COMMIT_PATTERN.fullmatch(parts[0]):
            raise QueryError("remote_url_rejected", "raw GitHub commit is outside the fixed allowlist")
        if parts[1] not in ALLOWED_CATALOGUES:
            raise QueryError("remote_url_rejected", "raw GitHub path is outside the fixed allowlist")
        return
    raise QueryError("remote_url_rejected", "remote host is outside the fixed allowlist")


def fetch_bytes(url, timeout=DEFAULT_TIMEOUT_SECONDS, max_bytes=DEFAULT_MAX_BYTES):
    validate_remote_url(url)
    request = Request(url, headers={"Accept": "application/json, text/plain", "User-Agent": "pc-build-assistant-price-history"})
    try:
        with NETWORK_OPENER.open(request, timeout=timeout) as response:
            declared = response.headers.get("Content-Length")
            if declared and int(declared) > max_bytes:
                raise QueryError("response_too_large", "remote response exceeded the configured size limit")
            payload = response.read(max_bytes + 1)
    except QueryError:
        raise
    except HTTPError as error:
        if error.code in REDIRECT_STATUS_CODES:
            raise QueryError(
                "redirect_rejected",
                "remote redirects are not allowed",
                {"http_status": error.code},
            ) from error
        raise QueryError("http_error", "remote version request failed", {"http_status": error.code}) from error
    except (URLError, TimeoutError, OSError, ValueError) as error:
        raise QueryError("network_error", "unable to read the fixed GitHub source") from error
    if len(payload) > max_bytes:
        raise QueryError("response_too_large", "remote response exceeded the configured size limit")
    return payload


def discover_versions(count, fetcher=fetch_bytes, timeout=DEFAULT_TIMEOUT_SECONDS, max_bytes=DEFAULT_MAX_BYTES):
    payload = fetcher(tags_api_url(), timeout=timeout, max_bytes=max_bytes)
    try:
        tags = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise QueryError("tag_response_invalid", "GitHub tag response was not valid JSON") from error
    if not isinstance(tags, list):
        raise QueryError("tag_response_invalid", "GitHub tag response had an unexpected shape")
    versions = set()
    for item in tags:
        if not isinstance(item, dict):
            continue
        version = str(item.get("name") or "")
        if TAG_PATTERN.fullmatch(version):
            versions.add(version)
    selected = sorted(versions, key=version_key, reverse=True)[:count]
    if not selected:
        raise QueryError("versions_not_found", "no supported semantic-version GitHub tags were found")
    return [
        resolve_version(version, fetcher, timeout, max_bytes)
        for version in sorted(selected, key=version_key)
    ]


def parse_json_mapping(payload, error_code, message):
    try:
        data = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise QueryError(error_code, message) from error
    if not isinstance(data, dict):
        raise QueryError(error_code, message)
    return data


def resolve_version(version, fetcher=fetch_bytes, timeout=DEFAULT_TIMEOUT_SECONDS, max_bytes=DEFAULT_MAX_BYTES):
    canonical = canonical_version(version)
    try:
        payload = fetcher(tag_ref_api_url(canonical), timeout=timeout, max_bytes=min(max_bytes, 1_000_000))
    except QueryError as error:
        if error.code == "http_error" and (error.details or {}).get("http_status") == 404:
            raise QueryError("version_not_found", f"GitHub tag was not found: {canonical}") from error
        raise
    ref = parse_json_mapping(payload, "tag_response_invalid", "GitHub tag reference response was invalid")
    if ref.get("ref") != f"refs/tags/{canonical}":
        raise QueryError("tag_response_invalid", "GitHub tag response did not match the requested version")
    target = ref.get("object") if isinstance(ref.get("object"), dict) else {}
    for _ in range(3):
        object_type = target.get("type")
        sha = str(target.get("sha") or "").lower()
        if not COMMIT_PATTERN.fullmatch(sha):
            raise QueryError("tag_response_invalid", "GitHub tag response did not contain a valid SHA")
        if object_type == "commit":
            return ResolvedVersion(canonical, sha)
        if object_type != "tag":
            raise QueryError("tag_target_invalid", "GitHub tag did not resolve to a commit")
        tag_payload = fetcher(tag_object_api_url(sha), timeout=timeout, max_bytes=min(max_bytes, 1_000_000))
        tag_object = parse_json_mapping(tag_payload, "tag_response_invalid", "GitHub annotated tag response was invalid")
        target = tag_object.get("object") if isinstance(tag_object.get("object"), dict) else {}
    raise QueryError("tag_depth_exceeded", "GitHub tag indirection exceeded the supported depth")


def parse_catalog_spec(value):
    if "=" not in str(value):
        raise QueryError("invalid_catalog", "catalog must use VERSION=PATH")
    version_text, path_text = str(value).split("=", 1)
    version = canonical_version(version_text)
    if not path_text.strip():
        raise QueryError("invalid_catalog_path", f"catalog path is empty for {version}")
    try:
        path = Path(path_text).expanduser().resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise QueryError("invalid_catalog_path", f"catalog path does not exist for {version}") from error
    if not path.is_file() and not path.is_dir():
        raise QueryError("invalid_catalog_path", f"catalog path is not a file or directory for {version}")
    return version, path


def resolve_local_catalogue(path, item_id):
    if path.is_file():
        return path
    relative = Path(catalogue_relative_path(item_id))
    candidates = (path / relative, path / relative.name)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise QueryError("catalog_file_missing", f"catalog directory does not contain {relative.as_posix()}")


def read_local_bytes(path, max_bytes):
    try:
        with path.open("rb") as handle:
            payload = handle.read(max_bytes + 1)
    except OSError as error:
        raise QueryError("catalog_read_error", "unable to read local catalog") from error
    if len(payload) > max_bytes:
        raise QueryError("catalog_too_large", "local catalog exceeded the configured size limit")
    return payload


def parse_catalogue(payload):
    try:
        data = yaml.safe_load(payload.decode("utf-8")) or {}
    except (UnicodeDecodeError, yaml.YAMLError) as error:
        raise QueryError("catalog_parse_error", "catalog was not valid UTF-8 YAML") from error
    if not isinstance(data, dict):
        raise QueryError("catalog_parse_error", "catalog root must be a mapping")
    return data


def exact_component(catalogue, item_id):
    matches = []
    for section, rows in catalogue.items():
        if not isinstance(rows, list):
            continue
        for row in rows:
            if isinstance(row, dict) and row.get("id") == item_id:
                matches.append((section, row))
    if len(matches) > 1:
        raise QueryError("duplicate_component_id", f"catalog contains duplicate exact ID: {item_id}")
    return matches[0] if matches else None


def sample_from_catalogue(version, catalogue, item_id, source_commit=None):
    match = exact_component(catalogue, item_id)
    if not match:
        return None, "component_not_found"
    section, item = match
    price = item.get("price_cny")
    if (
        item.get("price_status") == "needs_market_quote"
        or isinstance(price, bool)
        or not isinstance(price, (int, float))
        or not math.isfinite(price)
        or price <= 0
    ):
        return None, "price_not_available"
    metadata = catalogue.get("metadata") if isinstance(catalogue.get("metadata"), dict) else {}
    price_date = item.get("price_date") or item.get("price_sample_date") or metadata.get("price_date") or metadata.get("cutoff_date")
    sample = {
        "version": version,
        "id": item_id,
        "category": section,
        "model": item.get("model") or item_id,
        "price_cny": int(round(price)),
        "price_date": str(price_date or ""),
    }
    if source_commit:
        sample["source_commit"] = source_commit
    return sample, None


def validate_version_list(values):
    versions = [canonical_version(value) for value in values]
    if len(versions) != len(set(versions)):
        raise QueryError("duplicate_version", "each version may be queried only once")
    return sorted(versions, key=version_key)


def collect_local_samples(item_id, catalog_specs, max_bytes):
    parsed = [parse_catalog_spec(spec) for spec in catalog_specs]
    versions = [version for version, _ in parsed]
    validate_version_list(versions)
    samples, skipped = [], []
    for version, path in sorted(parsed, key=lambda entry: version_key(entry[0])):
        catalog_path = resolve_local_catalogue(path, item_id)
        catalogue = parse_catalogue(read_local_bytes(catalog_path, max_bytes))
        sample, reason = sample_from_catalogue(version, catalogue, item_id)
        if sample:
            samples.append(sample)
        else:
            skipped.append({"version": version, "reason": reason})
    return versions, samples, skipped


def collect_remote_samples(item_id, resolved_versions, fetcher, timeout, max_bytes):
    samples, skipped = [], []
    for resolved in resolved_versions:
        url = raw_catalogue_url(resolved.commit_sha, item_id)
        try:
            payload = fetcher(url, timeout=timeout, max_bytes=max_bytes)
        except QueryError as error:
            if error.code == "http_error" and (error.details or {}).get("http_status") == 404:
                skipped.append({"version": resolved.version, "source_commit": resolved.commit_sha, "reason": "catalog_not_found"})
                continue
            raise
        catalogue = parse_catalogue(payload)
        sample, reason = sample_from_catalogue(resolved.version, catalogue, item_id, resolved.commit_sha)
        if sample:
            samples.append(sample)
        else:
            skipped.append({"version": resolved.version, "source_commit": resolved.commit_sha, "reason": reason})
    return samples, skipped


def direction(change):
    if change > 0:
        return "up"
    if change < 0:
        return "down"
    return "flat"


def summarize(item_id, requested_versions, samples, skipped, recent_count, mode):
    samples = sorted(samples, key=lambda sample: version_key(sample["version"]))
    if not samples:
        return {
            "ok": False,
            "reason": "price_history_not_found",
            "message": "所查版本均未提供该精确 ID 的可用价格。",
            "id": item_id,
            "requested_versions": requested_versions,
            "skipped_versions": skipped,
        }
    recent = samples[-min(len(samples), recent_count):]
    if len(recent) >= 2:
        change = recent[-1]["price_cny"] - recent[0]["price_cny"]
        recent_direction = direction(change)
    else:
        change = None
        recent_direction = "insufficient"
    return {
        "ok": True,
        "id": item_id,
        "model": samples[-1]["model"],
        "mode": mode,
        "requested_versions": requested_versions,
        "sample_count": len(samples),
        "samples": samples,
        "skipped_versions": skipped,
        "recent_samples": recent,
        "recent_change_cny": change,
        "recent_direction": recent_direction,
    }


def query_history(
    item_id,
    catalog_specs=None,
    explicit_versions=None,
    version_count=DEFAULT_VERSION_COUNT,
    recent_count=DEFAULT_RECENT_COUNT,
    timeout=DEFAULT_TIMEOUT_SECONDS,
    max_bytes=DEFAULT_MAX_BYTES,
    fetcher=fetch_bytes,
):
    if not str(item_id or "").strip():
        raise QueryError("missing_id", "--id is required")
    if recent_count < 2 or recent_count > MAX_VERSION_COUNT:
        raise QueryError("invalid_recent_count", f"--recent must be between 2 and {MAX_VERSION_COUNT}")
    if timeout <= 0 or timeout > 60:
        raise QueryError("invalid_timeout", "--timeout must be greater than 0 and no more than 60 seconds")
    if max_bytes < 1024 or max_bytes > ABSOLUTE_MAX_BYTES:
        raise QueryError("invalid_size_limit", f"--max-bytes must be between 1024 and {ABSOLUTE_MAX_BYTES}")

    catalog_specs = list(catalog_specs or [])
    explicit_versions = list(explicit_versions or [])
    if catalog_specs and explicit_versions:
        raise QueryError("conflicting_inputs", "--catalog and --version cannot be combined")
    if catalog_specs:
        requested, samples, skipped = collect_local_samples(item_id, catalog_specs, max_bytes)
        return summarize(item_id, requested, samples, skipped, recent_count, "local_catalogs")

    if explicit_versions:
        versions = validate_version_list(explicit_versions)
        resolved_versions = [resolve_version(version, fetcher, timeout, max_bytes) for version in versions]
    else:
        if version_count < 2 or version_count > MAX_VERSION_COUNT:
            raise QueryError("invalid_version_count", f"--versions must be between 2 and {MAX_VERSION_COUNT}")
        resolved_versions = discover_versions(version_count, fetcher, timeout, min(max_bytes, 1_000_000))
        versions = [item.version for item in resolved_versions]
    samples, skipped = collect_remote_samples(item_id, resolved_versions, fetcher, timeout, max_bytes)
    return summarize(item_id, versions, samples, skipped, recent_count, "github_versions")


def human_direction(value):
    return {"up": "上涨", "down": "下降", "flat": "持平", "insufficient": "样本不足"}[value]


def format_human(result):
    if not result.get("ok"):
        return result.get("message", "未找到可用版本价格。")
    lines = [f"{result['model']}（{result['id']}）的已发布版本价格："]
    for sample in result["samples"]:
        date_text = f"，价格日期 {sample['price_date']}" if sample.get("price_date") else ""
        lines.append(f"- {sample['version']}：¥{sample['price_cny']}{date_text}")
    if result["recent_change_cny"] is None:
        lines.append("可用版本不足 2 个，暂不能判断涨跌。")
    else:
        lines.append(
            f"最近 {len(result['recent_samples'])} 个有价格的发布版本"
            f"{human_direction(result['recent_direction'])} ¥{abs(result['recent_change_cny'])}。"
        )
    if result["skipped_versions"]:
        skipped = "、".join(f"{item['version']}({item['reason']})" for item in result["skipped_versions"])
        lines.append(f"跳过：{skipped}。")
    lines.append("这是版本快照比较，不代表连续每日行情；下单前仍需核对当前价格。")
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compare an exact component ID across published package versions.")
    parser.add_argument("--id", required=True, help="精确组件 ID；不跨 SKU 合并")
    parser.add_argument("--catalog", action="append", default=[], metavar="VERSION=PATH", help="本地版本目录或单个 catalog 文件，可重复")
    parser.add_argument("--version", action="append", default=[], help="显式 GitHub vMAJOR.MINOR.PATCH tag，可重复")
    parser.add_argument("--versions", type=int, default=DEFAULT_VERSION_COUNT, help="未显式指定 tag 时读取最近几个 GitHub tag")
    parser.add_argument("--recent", type=int, default=DEFAULT_RECENT_COUNT, help="用最近几个有价格的版本比较涨跌")
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT_SECONDS)
    parser.add_argument("--max-bytes", type=int, default=DEFAULT_MAX_BYTES)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        result = query_history(
            args.id,
            catalog_specs=args.catalog,
            explicit_versions=args.version,
            version_count=args.versions,
            recent_count=args.recent,
            timeout=args.timeout,
            max_bytes=args.max_bytes,
        )
    except QueryError as error:
        result = error.as_result()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_human(result))
    return 0 if result.get("ok") else 2


if __name__ == "__main__":
    raise SystemExit(main())
