#!/usr/bin/env python3
# Copyright (c) 2026 Beijing Volcano Engine Technology Co., Ltd.
# SPDX-License-Identifier: MIT
"""Rank local API wiki hits with one rg recall pass."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


API_BASE = "https://api.volcengine.com/api/common"
GENERIC_QUERY_WORDS = {
    "api",
    "apis",
    "sdk",
    "code",
    "demo",
    "sample",
    "example",
    "test",
}

WEIGHTS = {
    "service": 120,
    "resource": 100,
    "action": 80,
    "alias_target": 240,
    "default_version": 1,
    "version": 240,
    "intent": 60,
    "original": 45,
    "extra": 20,
}

FIELD_WEIGHTS = {
    "action": 4,
    "name_cn": 4,
    "api_group": 3,
    "service_code": 3,
    "api_version": 4,
    "keywords": 3,
    "description": 1,
    "usage_scenario": 1,
}

GROUP_FIELDS = {
    "service": ("service_code",),
    "action": ("action",),
    "version": ("api_version",),
    "resource": ("action", "name_cn", "api_group", "keywords", "description", "usage_scenario"),
}

COMMON_SERVICE_CODES = {
    "alb": "alb",
    "apig": "apig",
    "ark": "ark",
    "cdn": "CDN",
    "cen": "cen",
    "clb": "clb",
    "cr": "cr",
    "dcdn": "dcdn",
    "ecs": "ecs",
    "ga": "ga",
    "iam": "iam",
    "kafka": "Kafka",
    "mongodb": "mongodb",
    "mysql": "rds_mysql",
    "pg": "rds_postgresql",
    "pgsql": "rds_postgresql",
    "postgres": "rds_postgresql",
    "postgresql": "rds_postgresql",
    "pssql": "rds_postgresql",
    "rabbitmq": "RabbitMQ",
    "rds": "rds",
    "redis": "Redis",
    "rocketmq": "RocketMQ",
    "slb": "clb",
    "sts": "sts",
    "tos": "tos",
    "vefaas": "vefaas",
    "vke": "vke",
    "vpc": "vpc",
    "vpn": "vpn",
}


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def default_wiki_path() -> Path:
    return skill_root() / "references" / "api_wiki.jsonl"


def default_alias_path() -> Path:
    return skill_root() / "references" / "query_aliases.json"


def split_terms(value: str | None) -> list[str]:
    if not value:
        return []
    return [part.strip() for part in value.split("|") if part.strip()]


def uniq(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(value)
    return result


def wiki_keys(path: Path) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    if not path.exists():
        return keys
    with path.open(encoding="utf-8") as file:
        for line in file:
            record = parse_record(line)
            if not record:
                continue
            service_code = record.get("service_code")
            api_version = record.get("api_version")
            action = record.get("action")
            if service_code and api_version and action:
                keys.add((str(service_code), str(api_version), str(action)))
    return keys


def validate_alias_targets(aliases: list[dict[str, Any]], wiki_path: Path) -> None:
    keys = wiki_keys(wiki_path)
    if not keys:
        return
    missing: list[str] = []
    for alias in aliases:
        target = alias.get("target")
        if not isinstance(target, dict):
            continue
        key = (
            str(target.get("service_code")),
            str(target.get("api_version")),
            str(target.get("action")),
        )
        if key not in keys:
            missing.append(f"{alias.get('id', '<unknown>')}: {'#'.join(key)}")
    if missing:
        raise ValueError(
            "alias target not found in api_wiki.jsonl with exact ServiceCode/api_version/action: "
            + "; ".join(missing[:10])
        )


def load_aliases(path: Path | None = None, *, wiki_path: Path | None = None) -> list[dict[str, Any]]:
    path = path or default_alias_path()
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    aliases = data if isinstance(data, list) else []
    validate_alias_targets(aliases, wiki_path or default_wiki_path())
    return aliases


def match_aliases(query: str | None, aliases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not query:
        return []
    normalized_query = re.sub(r"\s+", " ", query).strip().lower()
    compact_query = re.sub(r"\s+", "", query).lower()
    date_re = re.compile(r"\s*20\d{2}-\d{2}-\d{2}\s*")
    normalized_no_version = date_re.sub(" ", normalized_query).strip()
    compact_no_version = re.sub(r"20\d{2}-\d{2}-\d{2}", "", compact_query)
    hits: list[dict[str, Any]] = []
    for alias in aliases:
        patterns = alias.get("patterns") or []
        for pattern in patterns:
            normalized_pattern = re.sub(r"\s+", " ", str(pattern)).strip().lower()
            compact_pattern = re.sub(r"\s+", "", str(pattern)).lower()
            if (
                normalized_pattern
                and alias_pattern_matches(normalized_query, normalized_pattern)
            ) or (
                compact_pattern
                and alias_pattern_matches(compact_query, compact_pattern)
            ) or (
                normalized_pattern
                and normalized_no_version
                and alias_pattern_matches(normalized_no_version, normalized_pattern)
            ) or (
                compact_pattern
                and compact_no_version
                and alias_pattern_matches(compact_no_version, compact_pattern)
            ):
                hits.append(alias)
                break
    return hits


def is_ascii_word_char(value: str) -> bool:
    return bool(re.match(r"[a-z0-9_]", value, re.IGNORECASE))


def alias_pattern_matches(compact_query: str, compact_pattern: str) -> bool:
    start = compact_query.find(compact_pattern)
    while start >= 0:
        end = start + len(compact_pattern)
        prev_char = compact_query[start - 1] if start > 0 else ""
        next_char = compact_query[end] if end < len(compact_query) else ""
        starts_with_ascii = is_ascii_word_char(compact_pattern[0])
        ends_with_ascii = is_ascii_word_char(compact_pattern[-1])
        has_left_boundary = not (starts_with_ascii and prev_char and is_ascii_word_char(prev_char))
        has_right_boundary = not (ends_with_ascii and next_char and is_ascii_word_char(next_char))
        if has_left_boundary and has_right_boundary:
            return True
        start = compact_query.find(compact_pattern, start + 1)
    return False


def alias_terms(alias_hits: list[dict[str, Any]], field: str) -> list[str]:
    values: list[str] = []
    for alias in alias_hits:
        raw = alias.get(field) or []
        if isinstance(raw, str):
            values.append(raw)
        elif isinstance(raw, list):
            values.extend(str(item) for item in raw if item)
    return uniq(values)


def camel_words(value: str) -> list[str]:
    spaced = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)
    return [part for part in re.split(r"[^A-Za-z0-9_]+", spaced) if len(part) > 1]


def infer_original_terms(query: str | None) -> list[str]:
    if not query:
        return []
    if is_pure_generic_query(query.strip()):
        return []
    terms = [query.strip()]
    compact = re.sub(r"\s+", "", query)
    if compact and compact != query:
        terms.append(compact)
    if "宽带" in query:
        terms.append(query.replace("宽带", "带宽"))
    return uniq([term for term in terms if term])


def is_pure_generic_query(term: str) -> bool:
    if not term:
        return False
    if any(ord(char) > 127 for char in term):
        return False
    tokens = camel_words(term)
    return bool(tokens) and all(token.lower() in GENERIC_QUERY_WORDS for token in tokens)


def infer_intents(query: str | None) -> list[str]:
    if not query:
        return []
    pairs = {
        "创建": "Create",
        "列出": "List|Describe",
        "查询": "Describe|List|Get",
        "获取": "Get|Describe|List",
        "列表": "List",
        "更新": "Update|Modify",
        "修改": "Modify|Update",
        "替换": "Replace",
        "绑定": "Bind|Associate",
        "解绑": "Unbind|Disassociate",
        "删除": "Delete",
        "移除": "Remove|Delete|Disassociate",
        "释放": "Release|Delete",
        "销毁": "Delete|Terminate",
        "启动": "Start",
        "停止": "Stop",
        "重启": "Reboot|Restart",
        "重置": "Reset",
        "扩容": "Scale|Expand|Resize",
        "退订": "Terminate",
        "续费": "Renew",
    }
    terms: list[str] = []
    for zh, en in pairs.items():
        if zh in query:
            terms.append(zh)
            terms.extend(split_terms(en))
    return uniq(terms)


def infer_resource_terms(query: str | None) -> list[str]:
    if not query:
        return []
    terms: list[str] = []
    if "宽带包" in query or "带宽包" in query:
        terms.extend(["宽带包", "带宽包", "BandwidthPackage", "BandwidthPkg"])
    if "公网" in query:
        terms.extend(["公网", "Public"])
    if "私有网络" in query or "vpc" in query.lower():
        terms.extend(["私有网络", "VPC", "Vpc"])
    if "辅助网" in query or "辅助网段" in query or "辅助cidr" in query.lower():
        terms.extend(
            [
                "辅助网",
                "辅助网段",
                "辅助CIDR",
                "CidrBlock",
                "VpcCidrBlock",
                "SecondaryCidr",
                "DisassociateVpcCidrBlock",
            ]
        )
    if "角色扮演" in query:
        terms.extend(["角色扮演", "AssumeRole"])
    if "api网关" in query.lower() or "api gateway" in query.lower() or "apig" in query.lower():
        terms.extend(["API网关", "api网关", "网关", "Gateway", "GatewayService"])
    if "云服务器" in query:
        terms.extend(["云服务器", "ECS", "Instance"])
    if "缓存数据库" in query or "redis" in query.lower():
        terms.extend(["Redis", "缓存数据库", "DBInstance"])
    if "消息队列" in query or "kafka" in query.lower():
        terms.extend(["Kafka", "消息队列", "Instance"])
    if "mysql" in query.lower() or "云数据库" in query:
        terms.extend(["MySQL", "云数据库", "DBInstance"])
    if any(term in query.lower() for term in ("postgresql", "postgres", "pgsql", "pssql")):
        terms.extend(["PostgreSQL", "postgresql", "postgres", "pgsql", "pssql", "DBInstance"])
    if "内容分发" in query or "cdn" in query.lower():
        terms.extend(["CDN", "内容分发", "加速域名", "CdnDomain"])
    if "方舟" in query or "大模型" in query or "ark" in query.lower():
        terms.extend(["ark", "方舟", "大模型"])
    if "应用负载均衡" in query or "alb" in query.lower():
        terms.extend(["ALB", "应用负载均衡", "LoadBalancer"])
    if "传统负载均衡" in query or "经典负载均衡" in query or "slb" in query.lower() or "clb" in query.lower():
        terms.extend(["CLB", "SLB", "负载均衡", "LoadBalancer"])
    if "waf" in query.lower():
        terms.extend(["WAF", "域名", "网站"])
    for word in camel_words(query):
        if word.lower() not in GENERIC_QUERY_WORDS:
            terms.append(word)
    return uniq(terms)


def infer_service_terms(query: str | None) -> list[str]:
    if not query:
        return []
    terms: list[str] = []
    for word in camel_words(query):
        service_code = COMMON_SERVICE_CODES.get(word.lower())
        if service_code:
            terms.append(service_code)
    if "私有网络" in query:
        terms.append("vpc")
    if "云服务器" in query:
        terms.append("ecs")
    if "缓存数据库" in query:
        terms.append("Redis")
    if "消息队列" in query or "kafka" in query.lower():
        terms.append("Kafka")
    if "云数据库" in query and "mysql" in query.lower():
        terms.append("rds_mysql")
    if any(term in query.lower() for term in ("postgresql", "postgres", "pgsql", "pssql")):
        terms.append("rds_postgresql")
    if "内容分发" in query or "cdn" in query.lower():
        terms.append("CDN")
    if "方舟" in query or "大模型" in query:
        terms.append("ark")
    if "api网关" in query.lower() or "api gateway" in query.lower() or "apig" in query.lower():
        terms.append("apig")
    if "应用负载均衡" in query:
        terms.append("alb")
    if "传统负载均衡" in query or "经典负载均衡" in query:
        terms.append("clb")
    return uniq(terms)


def infer_version_terms(query: str | None) -> list[str]:
    if not query:
        return []
    return uniq(re.findall(r"20\d{2}-\d{2}-\d{2}\b", query))


def compile_group(name: str, terms: list[str]) -> tuple[str, list[re.Pattern[str]]]:
    patterns = [re.compile(re.escape(term), re.IGNORECASE) for term in terms if term]
    return name, patterns


def build_groups(args: argparse.Namespace) -> dict[str, list[str]]:
    alias_hits = getattr(args, "alias_hits", [])
    groups = {
        "original": split_terms(args.original) or infer_original_terms(args.query),
        "resource": (split_terms(args.resource) or infer_resource_terms(args.query)) + alias_terms(alias_hits, "resource"),
        "intent": (split_terms(args.intent) or infer_intents(args.query)) + alias_terms(alias_hits, "intent"),
        "service": (split_terms(args.service) or infer_service_terms(args.query)) + alias_terms(alias_hits, "service"),
        "action": split_terms(args.action) + alias_terms(alias_hits, "action"),
        "version": infer_version_terms(args.query),
        "extra": split_terms(args.extra),
    }
    return {name: uniq(terms) for name, terms in groups.items() if terms}


def recall_pattern(groups: dict[str, list[str]]) -> str:
    terms = uniq([term for terms in groups.values() for term in terms])
    return "|".join(re.escape(term) for term in terms)


def run_rg(path: Path, pattern: str) -> list[tuple[int, str]]:
    rg = shutil.which("rg")
    if not rg:
        return python_scan(path, pattern)
    cmd = [rg, "-n", "-i", "--no-heading", "--color", "never", "-e", pattern, "--", str(path)]
    proc = subprocess.run(cmd, text=True, capture_output=True, check=False)
    if proc.returncode not in (0, 1):
        raise RuntimeError(proc.stderr.strip() or f"rg exited with {proc.returncode}")
    results: list[tuple[int, str]] = []
    for raw in proc.stdout.splitlines():
        match = re.match(r"^(\d+):(.*)$", raw)
        if not match:
            continue
        results.append((int(match.group(1)), match.group(2)))
    return results


def python_scan(path: Path, pattern: str) -> list[tuple[int, str]]:
    compiled = re.compile(pattern, re.IGNORECASE)
    results: list[tuple[int, str]] = []
    with path.open(encoding="utf-8") as file:
        for line_no, line in enumerate(file, start=1):
            line = line.rstrip("\n")
            if compiled.search(line):
                results.append((line_no, line))
    return results


def field_text(record: dict[str, Any], field: str) -> str:
    value = record.get(field)
    if isinstance(value, list):
        return " ".join(str(item) for item in value)
    return "" if value is None else str(value)


def score_record(
    record: dict[str, Any],
    line: str,
    compiled_groups: dict[str, list[re.Pattern[str]]],
    alias_hits: list[dict[str, Any]] | None = None,
) -> tuple[int, dict[str, int], int]:
    group_scores: dict[str, int] = {}
    total_hits = 0
    for group_name, patterns in compiled_groups.items():
        best_group_field_weight = 0
        group_hits = 0
        matched_terms = 0
        for pattern in patterns:
            hit_count = 0
            fields = GROUP_FIELDS.get(group_name) or tuple(FIELD_WEIGHTS)
            for field in fields:
                field_weight = FIELD_WEIGHTS[field]
                text = field_text(record, field)
                hits = pattern.findall(text)
                if hits:
                    hit_count += len(hits)
                    best_group_field_weight = max(best_group_field_weight, field_weight)
            if hit_count:
                matched_terms += 1
                group_hits += hit_count
        if best_group_field_weight:
            if group_name == "resource":
                term_bonus = min(max(matched_terms - 1, 0), 4)
            else:
                term_bonus = 0
            group_scores[group_name] = WEIGHTS.get(group_name, WEIGHTS["extra"]) * (
                best_group_field_weight + term_bonus
            )
            total_hits += group_hits
    for alias in alias_hits or []:
        target = alias.get("target") if isinstance(alias.get("target"), dict) else {}
        if (
            target
            and str(record.get("service_code")) == str(target.get("service_code"))
            and str(record.get("api_version")) == str(target.get("api_version"))
            and str(record.get("action")) == str(target.get("action"))
        ):
            group_scores[f"alias:{alias.get('id', 'target')}"] = WEIGHTS["alias_target"] * 4
        elif alias_terms([alias], "action") and str(record.get("action")) in alias_terms([alias], "action"):
            group_scores[f"alias:{alias.get('id', 'action')}"] = WEIGHTS["alias_target"]
    return sum(group_scores.values()), group_scores, total_hits


def parse_record(line: str) -> dict[str, Any] | None:
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None
    return data if isinstance(data, dict) else None


def explicit_version_requested(groups: dict[str, list[str]]) -> bool:
    for terms in groups.values():
        for term in terms:
            if re.search(r"\b20\d{2}-\d{2}-\d{2}\b", term):
                return True
    return False


def apply_default_version_boost(
    ranked: list[dict[str, Any]],
    *,
    explicit_version: bool,
) -> None:
    if explicit_version:
        return
    items_by_api: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for item in ranked:
        record = item.get("record") or {}
        service_code = record.get("service_code")
        action = record.get("action")
        api_version = record.get("api_version")
        if not service_code or not action or not api_version:
            continue
        key = (str(service_code), str(action))
        items_by_api.setdefault(key, []).append(item)

    for (_service_code, _action), items in items_by_api.items():
        versions = {str((item.get("record") or {}).get("api_version", "")) for item in items}
        if len(versions) <= 1:
            continue
        default_items = [
            item
            for item in items
            if (item.get("record") or {}).get("is_default_version") is True
        ]
        if not default_items:
            continue
        best_score = max(int(item.get("score", 0)) for item in items)
        item = default_items[0]
        current_score = int(item.get("score", 0))
        delta = max(best_score - current_score + 1, 1)
        group_scores = item.setdefault("group_scores", {})
        group_scores["default_version"] = delta
        item["score"] = sum(group_scores.values())
        item["group_count"] = len(group_scores)


def http_json(url: str, *, timeout: int = 8) -> dict[str, Any]:
    headers = {
        "Accept": "application/json, text/plain, */*",
        "x-language": "zh",
        "User-Agent": "volcengine-make-code-skill/rg-rank",
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def remote_search(query: str, *, limit: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode(
        {
            "Query": query,
            "Channel": "api",
            "Limit": max(limit, 1),
            "Offset": 0,
        }
    )
    data = http_json(f"{API_BASE}/search/all?{params}")
    items = data.get("Result", {}).get("List", [])
    results: list[dict[str, Any]] = []
    for idx, item in enumerate(items, start=1):
        biz = item.get("BizInfo") or {}
        service_code = biz.get("ServiceCode")
        version = biz.get("Version")
        action = biz.get("Action")
        if not service_code or not version or not action:
            continue
        highlights = item.get("Highlight") or []
        name_cn = ""
        description_parts = []
        for highlight in highlights:
            if not isinstance(highlight, dict):
                continue
            summary = re.sub(r"</?em>", "", str(highlight.get("Summary", "")))
            if highlight.get("Field") in {"title", "abstract"} and not name_cn:
                name_cn = summary
            if summary:
                description_parts.append(summary)
        record = {
            "key": f"{service_code}#{version}#{action}",
            "service_code": service_code,
            "api_version": version,
            "action": action,
            "api_group": "",
            "name_cn": name_cn,
            "description": " ".join(description_parts),
            "usage_scenario": "",
            "attentions": "",
            "operation_type": 0,
            "online_status": 0,
            "keywords": [service_code, action, name_cn],
            "source": "remote_search",
        }
        results.append(
            {
                "line": None,
                "score": 0,
                "group_count": 0,
                "hit_count": 0,
                "group_scores": {},
                "source": "remote_search",
                "remote_rank": idx,
                "record": record,
            }
        )
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Rank Volcengine API wiki hits using one rg pass.")
    parser.add_argument("--query", help="Original user query.")
    parser.add_argument("--resource", help="Resource terms separated by |.")
    parser.add_argument("--intent", help="Intent terms separated by |.")
    parser.add_argument("--service", help="Service/product terms separated by |.")
    parser.add_argument("--action", help="Action terms separated by |.")
    parser.add_argument("--original", help="Original/normalized phrase terms separated by |.")
    parser.add_argument("--extra", help="Extra recall terms separated by |.")
    parser.add_argument("--aliases", default=str(default_alias_path()))
    parser.add_argument("--wiki", default=str(default_wiki_path()))
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--format", choices=("json", "jsonl", "text"), default="json")
    parser.add_argument("--remote-search", action="store_true", help="Force remote API search in addition to local ranking; use sparingly.")
    parser.add_argument("--no-remote-fallback", action="store_true", help="Disable automatic remote search when local ranking has zero results.")
    args = parser.parse_args()
    path = Path(args.wiki).expanduser()
    aliases = load_aliases(Path(args.aliases).expanduser(), wiki_path=path)
    args.alias_hits = match_aliases(args.query, aliases)

    groups = build_groups(args)
    if not groups:
        if args.query and not args.no_remote_fallback:
            try:
                ranked = remote_search(args.query, limit=args.limit)
                source = "remote_search"
                remote_fallback_reason = "no_local_hits"
            except Exception as exc:
                ranked = []
                source = "remote_search"
                remote_fallback_reason = f"no_local_hits: {exc}"
            return print_ranked_output(
                args,
                ranked,
                pattern="",
                groups={},
                alias_hits=args.alias_hits,
                total_hits=0,
                source=source,
                remote_fallback_reason=remote_fallback_reason,
            )
        message = "provide --query or term groups"
        if args.format == "text":
            print(f"error: empty_query: {message}")
        else:
            print(json.dumps({"error": "empty_query", "message": message}, ensure_ascii=False))
        return 2

    pattern = recall_pattern(groups)
    hits = run_rg(path, pattern)
    compiled_groups = dict(compile_group(name, terms) for name, terms in groups.items())

    ranked: list[dict[str, Any]] = []
    for line_no, line in hits:
        record = parse_record(line)
        if not record:
            continue
        score, group_scores, total_hits = score_record(record, line, compiled_groups, args.alias_hits)
        if score <= 0:
            continue
        ranked.append(
            {
                "line": line_no,
                "score": score,
                "group_count": len(group_scores),
                "hit_count": total_hits,
                "group_scores": group_scores,
                "record": record,
            }
        )

    apply_default_version_boost(
        ranked,
        explicit_version=explicit_version_requested(groups),
    )
    ranked.sort(key=lambda item: (-item["score"], -item["group_count"], -item["hit_count"], item["line"]))
    ranked = ranked[: max(args.limit, 0)]
    source = "local"
    remote_fallback_reason = ""

    should_remote = bool(args.query) and (
        args.remote_search or (not ranked and not args.no_remote_fallback)
    )
    if should_remote:
        remote_fallback_reason = "forced" if args.remote_search else "no_local_hits"
        try:
            remote_results = remote_search(args.query, limit=args.limit)
        except Exception as exc:
            remote_results = []
            remote_fallback_reason = f"{remote_fallback_reason}: {exc}"
        if args.remote_search and ranked:
            ranked.extend(remote_results)
            source = "mixed"
            if args.limit >= 0:
                ranked = ranked[: args.limit]
        elif remote_results:
            ranked = remote_results[: max(args.limit, 0)]
            source = "remote_search"
        elif not ranked:
            source = "remote_search"

    return print_ranked_output(
        args,
        ranked,
        pattern=pattern,
        groups=groups,
        alias_hits=args.alias_hits,
        total_hits=len(hits),
        source=source,
        remote_fallback_reason=remote_fallback_reason,
    )


def print_ranked_output(
    args: argparse.Namespace,
    ranked: list[dict[str, Any]],
    *,
    pattern: str,
    groups: dict[str, list[str]],
    alias_hits: list[dict[str, Any]],
    total_hits: int,
    source: str,
    remote_fallback_reason: str,
) -> int:
    if args.format == "jsonl":
        for item in ranked:
            print(json.dumps(item, ensure_ascii=False))
    elif args.format == "text":
        for idx, item in enumerate(ranked, start=1):
            record = item["record"]
            item_source = item.get("source") or record.get("source") or "local"
            line = item.get("line")
            line_part = f"line={line}" if line is not None else f"remote_rank={item.get('remote_rank')}"
            print(
                f"{idx}. [{item_source}] score={item['score']} {line_part} "
                f"{record.get('name_cn', '')} | {record.get('service_code')} "
                f"{record.get('api_version')} {record.get('action')}"
            )
    else:
        print(
            json.dumps(
                {
                    "pattern": pattern,
                    "groups": groups,
                    "alias_hits": [alias.get("id") for alias in alias_hits],
                    "total_hits": total_hits,
                    "source": source,
                    "remote_fallback_reason": remote_fallback_reason,
                    "results": ranked,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({"error": "exception", "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(1)
