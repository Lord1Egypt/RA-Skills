#!/usr/bin/env python3
"""Repository-local validation for the pt-agent skill.

The checks are dependency-free so the skill can validate itself on a fresh
Codex install without PyYAML or project-specific tooling.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
MAX_SKILL_LINES = 500
MAX_DESCRIPTION_CHARS = 1024
FORBIDDEN_EXTRA_DOCS = {
    "AGENTS.md",
    "CHANGELOG.md",
    "INSTALLATION_GUIDE.md",
    "QUICK_REFERENCE.md",
}


class CheckResult:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def read_text(path: Path, result: CheckResult) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        result.error(f"{path.relative_to(ROOT)} unreadable: {exc}")
        return ""


def load_json(path: Path, result: CheckResult) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.error(f"{path.relative_to(ROOT)} invalid JSON at {exc.lineno}:{exc.colno}")
        return {}
    except OSError as exc:
        result.error(f"{path.relative_to(ROOT)} unreadable: {exc}")
        return {}
    if not isinstance(data, dict):
        result.error(f"{path.relative_to(ROOT)} root must be a JSON object")
        return {}
    return data


def parse_simple_frontmatter(text: str, result: CheckResult) -> dict[str, str]:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        result.error("SKILL.md must start with YAML frontmatter")
        return {}
    fields: dict[str, str] = {}
    for raw_line in match.group(1).splitlines():
        if not raw_line.strip():
            continue
        if ":" not in raw_line:
            result.error(f"SKILL.md frontmatter line is not key:value: {raw_line}")
            continue
        key, value = raw_line.split(":", 1)
        fields[key.strip()] = value.strip().strip('"')
    return fields


def check_skill_md(result: CheckResult) -> None:
    skill_path = ROOT / "SKILL.md"
    text = read_text(skill_path, result)
    if not text:
        return
    fields = parse_simple_frontmatter(text, result)
    unexpected = set(fields) - {"name", "description"}
    if unexpected:
        result.error(f"SKILL.md frontmatter has unexpected keys: {sorted(unexpected)}")
    name = fields.get("name")
    if name != "pt-agent":
        result.error("SKILL.md frontmatter name must be pt-agent")
    description = fields.get("description", "")
    if not description:
        result.error("SKILL.md frontmatter description is required")
    if len(description) > MAX_DESCRIPTION_CHARS:
        result.error(f"SKILL.md description exceeds {MAX_DESCRIPTION_CHARS} chars")
    if not {"tracker", "downloader", "PT"}.issubset(set(re.findall(r"PT|tracker|downloader", description))):
        result.warn("SKILL.md description should mention PT, tracker, and downloader")
    line_count = len(text.splitlines())
    if line_count > MAX_SKILL_LINES:
        result.error(f"SKILL.md has {line_count} lines; keep it under {MAX_SKILL_LINES}")

    referenced = sorted(set(re.findall(r"`((?:references|scripts)/[^`]+?)`", text)))
    for rel in referenced:
        if not (ROOT / rel).exists():
            result.error(f"SKILL.md references missing file: {rel}")


def check_openai_yaml(result: CheckResult) -> None:
    path = ROOT / "agents" / "openai.yaml"
    text = read_text(path, result)
    if not text:
        return
    for key in ("display_name", "short_description", "default_prompt"):
        if f"{key}:" not in text:
            result.error(f"agents/openai.yaml missing interface.{key}")
    if "$pt-agent" not in text:
        result.error("agents/openai.yaml default_prompt must mention $pt-agent")
    short_match = re.search(r'short_description:\s*"([^"]+)"', text)
    if short_match and not 25 <= len(short_match.group(1)) <= 64:
        result.warn("agents/openai.yaml short_description should be 25-64 characters")


def check_reference_shape(result: CheckResult) -> None:
    for path in sorted((ROOT / "references").glob("*.md")):
        text = read_text(path, result)
        if not text:
            continue
        if not text.startswith("# "):
            result.error(f"{path.relative_to(ROOT)} must start with an H1")
        if len(text.splitlines()) > 100 and "## Contents" not in text:
            result.warn(f"{path.relative_to(ROOT)} is over 100 lines and should include ## Contents")


def check_catalogs(result: CheckResult) -> None:
    adapter_catalog = load_json(ROOT / "references" / "adapter-catalog.json", result)
    site_catalog = load_json(ROOT / "references" / "site-preset-catalog.json", result)
    adapters = adapter_catalog.get("adapters") or []
    sites = site_catalog.get("sites") or []
    if not isinstance(adapters, list):
        result.error("adapter-catalog.json adapters must be a list")
        adapters = []
    if not isinstance(sites, list):
        result.error("site-preset-catalog.json sites must be a list")
        sites = []

    adapter_ids = {str(item.get("id")) for item in adapters if isinstance(item, dict) and item.get("id")}
    if len(adapter_ids) != len(adapters):
        result.error("adapter-catalog.json contains duplicate or missing adapter ids")

    site_ids: set[str] = set()
    for site in sites:
        if not isinstance(site, dict):
            result.error("site-preset-catalog.json contains a non-object site")
            continue
        site_id = site.get("id")
        if not site_id:
            result.error("site-preset-catalog.json site missing id")
            continue
        if site_id in site_ids:
            result.error(f"duplicate site preset id: {site_id}")
        site_ids.add(str(site_id))
        adapter_id = site.get("adapterId")
        if adapter_id not in adapter_ids:
            result.error(f"site preset {site_id} references unknown adapterId {adapter_id}")
    declared_count = site_catalog.get("count")
    if declared_count != len(sites):
        result.error(f"site-preset-catalog.json count={declared_count} but sites={len(sites)}")


def check_scripts(result: CheckResult) -> None:
    for path in sorted((ROOT / "scripts").glob("*.py")):
        source = read_text(path, result)
        if not source:
            continue
        try:
            compile(source, str(path), "exec")
        except SyntaxError as exc:
            result.error(f"{path.relative_to(ROOT)} syntax error at {exc.lineno}:{exc.offset}: {exc.msg}")


def check_secret_policy(result: CheckResult) -> None:
    module_path = ROOT / "scripts" / "pt_store.py"
    spec = importlib.util.spec_from_file_location("pt_agent_store_validation", module_path)
    if spec is None or spec.loader is None:
        result.error("scripts/pt_store.py could not be loaded for secret-policy validation")
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    unsafe_records = (
        {"secretRefs": {"cookie": "session_id=unsafe-example-value"}},
        {"credentialRef": "admin:unsafe-password"},
        {"apiKeyRef": "unsafe-api-key"},
    )
    for record in unsafe_records:
        try:
            module.load_json_arg(json.dumps(record))
        except module.StoreError as exc:
            if exc.payload.get("code") != "unsafe_secret_value":
                result.error(f"raw-secret rejection returned wrong error: {exc.payload.get('code')}")
        else:
            result.error(f"raw secret reference was accepted: {next(iter(record))}")

    safe_record = {
        "secretRefs": {"cookie": "env://PT_COOKIE"},
        "credentialRef": "secret://downloaders/main",
        "profileRef": "profile://trackers/main",
    }
    try:
        module.load_json_arg(json.dumps(safe_record))
    except module.StoreError as exc:
        result.error(f"safe secret references were rejected: {exc.payload.get('code')}")

    legacy = {"secretRefs": {"cookie": "session_id=unsafe-example-value"}, "credentialRef": "admin:unsafe-password"}
    paths = set(module.collect_raw_secret_paths(legacy))
    expected = {"secretRefs.cookie", "credentialRef"}
    if not expected.issubset(paths):
        result.error(f"secret audit missed legacy paths: {sorted(expected - paths)}")

    with tempfile.TemporaryDirectory(prefix="pt-agent-validation-") as temp_dir:
        legacy_store = module.empty_store()
        legacy_store["trackers"] = {"site-a": {"id": "site-a", "cookie": "session_id=unsafe-example-value"}}
        legacy_store["downloaders"] = {"qb": {"id": "qb", "username": "user", "password": "unsafe-password"}}
        migration = module.migrate_inline_secrets(legacy_store, Path(temp_dir) / ".env")
        try:
            module.reject_raw_secrets(legacy_store)
        except module.StoreError as exc:
            result.error(f"inline-secret migration left unsafe values: {exc.payload.get('fieldPath')}")
        if len(migration.get("migrated", [])) != 2:
            result.error("inline-secret migration did not migrate tracker and downloader credentials")
        categorized_root = Path(temp_dir) / ".hermes" / "skills" / "tools" / "pt-agent"
        if module._installed_host_home(categorized_root) != Path(temp_dir) / ".hermes":
            result.error("host-home detection does not support categorized skill directories")


def check_runtime_security(result: CheckResult) -> None:
    module_path = ROOT / "scripts" / "pt_runtime.py"
    source = read_text(module_path, result)
    for marker in ("CERT_NONE", "check_hostname = False"):
        if marker in source:
            result.error(f"scripts/pt_runtime.py disables TLS verification with {marker}")

    scripts_dir = str(module_path.parent)
    sys.path.insert(0, scripts_dir)
    try:
        spec = importlib.util.spec_from_file_location("pt_agent_runtime_validation", module_path)
        if spec is None or spec.loader is None:
            result.error("scripts/pt_runtime.py could not be loaded for security validation")
            return
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        try:
            module.resolve_ref("admin:unsafe-password", "downloader credential")
        except module.RuntimeErrorJson as exc:
            if exc.payload.get("code") != "unsafe_secret_ref":
                result.error(f"runtime raw-reference rejection returned wrong error: {exc.payload.get('code')}")
        else:
            result.error("scripts/pt_runtime.py accepted a raw credential instead of a reference")
        if module.normalize_media_query("搜一下周星驰的电影") != "周星驰":
            result.error("media-search did not normalize a common Chinese movie query")
        if module.adapter_index() is not module.adapter_index():
            result.error("adapter catalog is rebuilt instead of cached within a runtime process")
        if module.normalize_media_query(module.strip_tracker_phrase("用hh搜一下周星驰的电影", ["hh"])) != "周星驰":
            result.error("media-search did not remove an explicit tracker alias from the query")
        movie = {"title": "Example Movie 2024", "subtitle": "类型: 喜剧", "category": None}
        series = {"title": "Example Show S01", "subtitle": "全10集 真人秀", "category": None}
        if not module.media_kind_matches(movie, "movie") or module.media_kind_matches(series, "movie"):
            result.error("media-search movie filter does not exclude episodic results")
        if not module.media_kind_matches(series, "tv"):
            result.error("media-search TV filter does not retain episodic results")
        fixture_stats = module.parse_stats_text(
            "魔力值 [ 使用 ]: 5,196,765.0 邀请 [ 发送 ]: 4(0) 分享率: 7.813 上传量: 2.481 TB 下载量: 325.22 GB"
        )
        if fixture_stats.get("bonus") != 5196765.0:
            result.error("tracker stats parser confused bonus with a nearby account number")
        nexus_header_stats = module.parse_stats_text(
            "vastsa [分享率]: 2.781 [认领]: [0/200] [H&R]: [0/0/5] [邀请]: 0 43,916 [勋章] 4.511 TB 6 1.622 TB 0"
        )
        if nexus_header_stats.get("bonus") != 43916.0:
            result.error("NexusPHP header parser did not extract the account bonus")
        if nexus_header_stats.get("uploadedBytes") != module.parse_size("4.511 TB"):
            result.error("NexusPHP header parser did not extract uploaded bytes")
        if nexus_header_stats.get("downloadedBytes") != module.parse_size("1.622 TB"):
            result.error("NexusPHP header parser did not extract downloaded bytes")
        empty_overview = module.overview({"trackers": {}, "downloaders": {}, "trackerStats": {}}, False)
        if not empty_overview.get("ok") or empty_overview.get("refreshed"):
            result.error("cached overview does not return a safe read-only summary")
        if not hasattr(module, "qb_add_magnet"):
            result.error("scripts/pt_runtime.py is missing the qBittorrent magnet implementation")
        else:
            original_headers = module.qb_session_headers
            original_request = module.request
            try:
                module.qb_session_headers = lambda _downloader: {}
                module.request = lambda *_args, **_kwargs: (200, "http://downloader.invalid", b"Ok.", {})
                added = module.qb_add_magnet(
                    {"id": "qb", "type": "qbittorrent", "baseUrl": "http://downloader.invalid"},
                    "magnet:?xt=urn:btih:0000000000000000000000000000000000000000",
                    {"addPaused": True},
                )
                if not added.get("ok") or added.get("status") != "added":
                    result.error("qBittorrent magnet implementation failed its mocked add test")
            finally:
                module.qb_session_headers = original_headers
                module.request = original_request
        if not hasattr(module, "parse_promotion_state"):
            result.error("scripts/pt_runtime.py is missing promotion/discount parsing")
        else:
            css_false_free = """
            <div class='torrent-table-sub-info'>
              <style>.promotion-tag-free { color: teal; }.promotion-tag-2xfree { color: green; }</style>
              <a href='details.php?id=1'>Normal Movie 1080p</a>
              <span class='tag'>官方</span>
            </div>
            """
            real_free = """
            <div class='torrent-table-sub-info'>
              <a href='details.php?id=2'>Free Movie 2160p</a>
              <span class="promotion-tag promotion-tag-free">免费</span>
            </div>
            """
            false_state = module.parse_promotion_state(css_false_free)
            real_state = module.parse_promotion_state(real_free)
            if false_state.get("discount") != "unknown" or "Free" in (false_state.get("tags") or []):
                result.error("promotion parser false-positives Free from CSS class definitions")
            if real_state.get("discount") != "free" or "Free" not in (real_state.get("tags") or []):
                result.error("promotion parser misses real free badges")
        if not hasattr(module, "torrent_info_hash") or not hasattr(module, "summarize_torrent"):
            result.error("download path missing torrent hash/summary helpers")
        else:
            # minimal bencoded torrent-like payload: d4:infod4:name3:fooe e
            sample = b"d4:infod4:name3:fooee"
            digest = module.torrent_info_hash(sample)
            if not isinstance(digest, str) or len(digest) != 40:
                result.error("torrent_info_hash did not return a 40-char sha1")
            summary = module.summarize_torrent({
                "hash": "abc",
                "name": "demo",
                "state": "downloading",
                "progress": 0.5,
                "sizeBytes": 1024,
                "downloadRateBytesPerSec": 2048,
            })
            if not summary or summary.get("progressPercent") != 50.0:
                result.error("summarize_torrent did not normalize progress")
        if 'sub.add_parser("resume-torrents")' not in Path(scripts_dir, "pt_runtime.py").read_text(encoding="utf-8"):
            result.error("runtime must implement resume-torrents for paused download handoff")
    finally:
        sys.path.remove(scripts_dir)


def check_portable_script_paths(result: CheckResult) -> None:
    paths = [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))]
    for path in paths:
        text = read_text(path, result)
        if re.search(r"python3\s+scripts/", text):
            result.error(f"{path.relative_to(ROOT)} invokes scripts relative to the process working directory")


def check_fast_media_path(result: CheckResult) -> None:
    skill = read_text(ROOT / "SKILL.md", result)
    runtime = read_text(ROOT / "scripts" / "pt_runtime.py", result)
    if "media-search" not in skill or 'sub.add_parser("media-search")' not in runtime:
        result.error("movie/TV fast path must document and implement media-search")
    for command in ("overview --refresh", "downloader-status", "--dry-run", "--all-trackers"):
        if command not in skill:
            result.error(f"common-operation fast path is missing from SKILL.md: {command}")
    if 'sub.add_parser("overview")' not in runtime or 'p_downloader.add_argument("--downloader")' not in runtime:
        result.error("runtime must implement overview and default-downloader status fast paths")
    if 'choices=("4k", "2160p", "1080p", "720p")' not in runtime:
        result.error("media-search must accept the common 4k resolution alias")
    if "download-torrent" not in skill or "--start" not in skill:
        result.error("download fast path must document download-torrent --start")
    if "Never invent recommendations" not in skill or 'Interpret "优先免费"' not in skill or "never append a second" not in skill:
        result.error("search UX must forbid invented recommendations and distinguish free preference from free-only filtering")
    if "Critical Search Response Contract" not in skill or "copy titles verbatim" not in skill:
        result.error("search UX must keep the strict final-answer contract near the top of SKILL.md")
    if '"只看免费", "仅免费", "免费资源"' not in skill or "Run only one search" not in skill:
        result.error("search routing must enforce free-only semantics and forbid silent retry searches")
    if "Never expose CLI flags" not in skill:
        result.error("empty-state recovery must hide host/runtime implementation syntax")
    if "Critical Queue Response Contract" not in skill or "查看全部任务、搜索新资源" not in skill:
        result.error("queue UX must provide a concise empty state and next action")
    if "media_search_display_text" not in runtime or '"text": display_text' not in runtime:
        result.error("runtime must provide deterministic display.text for search and queue responses")
    if "Do **not** ask for confirmation" not in skill and "do not ask for confirmation" not in skill.lower():
        result.error("download fast path must skip confirmation for selected results")
    if not (ROOT / "scripts" / "benchmark_common.py").exists():
        result.error("common-operation benchmark script is missing")
    forbidden = ROOT / "references" / "nexusphp-direct-scraping.md"
    if forbidden.exists():
        result.error("unsafe direct-scraping fallback reference is present")
    markdown = "\n".join(read_text(path, result) for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md"))])
    for marker in ("raw cookie from store.json", "direct HTTP scraping with"):
        if marker in markdown:
            result.error(f"unsafe direct-scraping fallback is documented: {marker}")


def check_storage_policy(result: CheckResult) -> None:
    hermes_marker = "." + "hermes/"
    deprecated_store = hermes_marker + "pt-agent"
    allowed_legacy = hermes_marker + "pt-sites.json"
    for path in [ROOT / "SKILL.md", *sorted((ROOT / "references").glob("*.md")), *sorted((ROOT / "scripts").glob("*.py"))]:
        text = read_text(path, result)
        if deprecated_store in text:
            result.error(f"{path.relative_to(ROOT)} hardcodes deprecated Hermes pt-agent store")
        for match in re.finditer(re.escape(hermes_marker) + r"[^\s`'\"]+", text):
            if allowed_legacy not in match.group(0):
                result.warn(f"{path.relative_to(ROOT)} contains non-legacy .hermes reference: {match.group(0)}")


def check_no_generated_residue(result: CheckResult) -> None:
    for name in FORBIDDEN_EXTRA_DOCS:
        if (ROOT / name).exists():
            result.error(f"extraneous skill doc present: {name}")
    for path in ROOT.rglob("*"):
        if any(part in {".git", ".venv", ".cc-connect"} for part in path.parts):
            continue
        if path.name == "__pycache__" or path.suffix == ".pyc":
            result.warn(f"generated Python cache present: {path.relative_to(ROOT)}")


def main() -> int:
    result = CheckResult()
    check_skill_md(result)
    check_openai_yaml(result)
    check_reference_shape(result)
    check_catalogs(result)
    check_scripts(result)
    check_secret_policy(result)
    check_runtime_security(result)
    check_portable_script_paths(result)
    check_fast_media_path(result)
    check_storage_policy(result)
    check_no_generated_residue(result)

    payload = {
        "ok": not result.errors,
        "errors": result.errors,
        "warnings": result.warnings,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not result.errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
