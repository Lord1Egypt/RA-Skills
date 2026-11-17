#!/usr/bin/env python3
"""Read-only local issue audit for installed skills and plugin skill sources."""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Allow direct execution and fixture loading without installing this skill as a package.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from collect_codex_display_candidates import (
    collect,
    frontmatter,
    logical_items,
    inventory_summary,
    unresolved_visible_items,
)
from recommendation_contract import enrich_report, render_actions, render_footer
from scan_state import plan_scan, finish_scan, digest_paths


def issue(item: dict, code: str, severity: str, message: str, remediation: str, evidence: list[str]) -> dict:
    return {
        "id": item.get("id"),
        "source_type": item.get("source_type"),
        "severity": severity,
        "code": code,
        "message": message,
        "remediation": remediation,
        "evidence": evidence,
        "editable": item.get("editable", False),
    }


def audit_item(item: dict) -> list[dict]:
    issues: list[dict] = []
    source_paths = [Path(value) for value in item.get("source_paths", [])]
    skill_paths = sorted({path for path in source_paths if path.name == "SKILL.md"})
    if item.get("fact_status") != "observed":
        return [issue(item, "SOURCE_UNAVAILABLE", "critical", "技能来源无法解析", "修复或重新安装来源后再审查。", [str(path) for path in source_paths])]

    if item.get("source_conflict"):
        conflict_paths = sorted({path for peer in item.get("source_candidates", []) for path in peer.get("source_paths", [])} | {str(path) for path in source_paths})
        issues.append(issue(item, "SOURCE_DIVERGENCE", "critical", "同一技能 ID 的安装来源内容不同。", "先用 UI 证据确认实际来源；只读插件交由上游更新，不直接修改 cache。", conflict_paths))
    elif item.get("source_resolution_status") == "equivalent_sources":
        issues.append(issue(item, "DUPLICATE_EQUIVALENT_SOURCE", "info", "检测到内容一致的多个来源。", str(item.get("source_resolution_plan") or "按已安装来源优先级选择当前来源；等价副本不阻断使用。"), [str(path) for path in source_paths]))

    if item.get("inventory_scope") == "visible" and item.get("translation_quality") != "ready":
        issues.append(issue(item, "DESCRIPTION_NEEDS_REFINEMENT", "warning", "技能展示说明仍需人工精炼。", "按翻译质量规则生成候选，保留 ID 和 display_name 后回读验证。", [str(path) for path in source_paths]))

    for skill_path in skill_paths:
        meta = frontmatter(skill_path)
        missing = [field for field in ("name", "description") if not str(meta.get(field) or "").strip()]
        if missing:
            issues.append(issue(item, "METADATA_MISSING", "warning", "SKILL.md frontmatter 缺少: " + ", ".join(missing), "补齐 frontmatter；系统或插件来源通过上游包更新，不直接改 cache。", [str(skill_path)]))
        ui_path = skill_path.parent / "agents" / "openai.yaml"
        if not ui_path.exists():
            issues.append(issue(item, "UI_METADATA_FALLBACK", "info", "未找到 agents/openai.yaml，将回退到 SKILL.md frontmatter。", "用户 skill 可补充 UI metadata；系统/插件 skill 保持只读并通过上游发布更新。", [str(skill_path)]))
        text = skill_path.read_text(encoding="utf-8-sig", errors="replace")
        references = sorted(set(re.findall(r"(?:references|scripts|agents)/[A-Za-z0-9_.\-/]+", text)))
        for reference in references:
            cleaned = reference.rstrip(".,;:)")
            roots = [skill_path.parent, *list(skill_path.parents)[1:5]]
            candidates = [root / cleaned for root in roots]
            if not any(target.exists() for target in candidates):
                editable = bool(item.get("editable"))
                code = "REFERENCE_MISSING" if editable else "REFERENCE_UNRESOLVED_READONLY"
                severity = "warning" if editable else "info"
                message = f"技能引用不存在: {reference}" if editable else f"只读来源中的引用未在包内解析: {reference}"
                remediation = (
                    f"在 {skill_path.parent} 下补齐 {cleaned}，或修正 SKILL.md 中的相对引用；修后重新运行审查。"
                    if editable else
                    "记录为上游包问题；不要修改 cache，升级对应插件或系统技能后重新审查。"
                )
                issues.append(issue(item, code, severity, message, remediation, [str(skill_path), *[str(target) for target in candidates]]))
    return issues


def load_profile(profile_path: Path | None) -> tuple[str, str]:
    if profile_path is None or not profile_path.exists():
        return "", "unavailable"
    try:
        return profile_path.read_text(encoding="utf-8-sig", errors="replace"), "observed"
    except OSError:
        return "", "unavailable"


def terms(text: str) -> set[str]:
    result = {token.lower() for token in re.findall(r"[A-Za-z][A-Za-z0-9+.-]{2,}", text)}
    stopwords = {"当前", "使用", "用于", "进行", "支持", "用户", "技能", "功能", "问题", "相关", "可以", "主要"}
    for chunk in re.findall(r"[\u4e00-\u9fff]{2,}", text):
        if chunk not in stopwords:
            result.add(chunk)
        for size in (2, 3, 4):
            for index in range(0, len(chunk) - size + 1):
                token = chunk[index:index + size]
                if token not in stopwords:
                    result.add(token)
    return result


def item_terms(item: dict) -> set[str]:
    return terms(" ".join([
        str(item.get("id", "")),
        str(item.get("command_palette", {}).get("original", "")),
        str(item.get("sidebar", {}).get("original", "")),
        str(item.get("sidebar", {}).get("short_description", "")),
    ]))


def trigger_terms(item: dict) -> set[str]:
    description = str(item.get("sidebar", {}).get("short_description") or item.get("sidebar", {}).get("original", ""))
    trigger = description.split("→", 1)[0] if "→" in description else ""
    raw = "|".join([str(item.get("command_palette", {}).get("original", "")), trigger])
    extracted = {token.strip().lower() for token in re.split(r"[|/·、,;]+", raw) if len(token.strip()) >= 2}
    return extracted or terms(str(item.get("id", "")))


def capability_terms(item: dict) -> set[str]:
    description = str(item.get("sidebar", {}).get("short_description") or item.get("sidebar", {}).get("original", ""))
    capability = description.split("→", 1)[1] if "→" in description else description
    return terms(capability)


def version_info(item: dict) -> dict:
    for raw_path in item.get("source_paths", []):
        path = Path(raw_path)
        for parent in (path.parent, *path.parents):
            version_file = parent / "VERSION"
            if version_file.exists():
                value = version_file.read_text(encoding="utf-8-sig", errors="replace").strip()
                match = re.search(r"\d+(?:\.\d+)+", value)
                if match:
                    return {"status": "observed", "version": match.group(0), "source": str(version_file)}
        for part in path.parts:
            if re.fullmatch(r"\d+(?:\.\d+)+", part):
                return {"status": "observed", "version": part, "source": str(path)}
    return {"status": "unavailable", "version": None, "source": None}


def score_items(items: list[dict], item_issues: list[dict], profile_text: str, profile_status: str) -> list[dict]:
    by_id: dict[str, list[dict]] = {}
    for entry in item_issues:
        by_id.setdefault(entry["id"], []).append(entry)
    profile_terms = terms(profile_text)
    results: list[dict] = []
    for item in items:
        codes = {entry["code"] for entry in by_id.get(item["id"], [])}
        dimensions = {
            "existence": 0 if "SOURCE_UNAVAILABLE" in codes else 10,
            "metadata": 4 if "METADATA_MISSING" in codes else 10,
            "source": 0 if "SOURCE_DIVERGENCE" in codes else 10,
            "description": (6 if "DESCRIPTION_NEEDS_REFINEMENT" in codes else 10) if item.get("inventory_scope") == "visible" else None,
            "version": 10 if version_info(item)["status"] == "observed" else None,
        }
        available = [value for value in dimensions.values() if value is not None]
        score = round(sum(available) / len(available), 1) if available else 0
        if profile_status == "observed":
            overlap = item_terms(item) & profile_terms
            alignment = {"status": "inferred", "score": round(min(10.0, len(overlap) * 2.0), 1), "matched_terms": sorted(overlap)}
        else:
            alignment = {"status": "unavailable", "score": None, "matched_terms": []}
        results.append({"id": item["id"], "health_score": score, "dimensions": dimensions, "profile_alignment": alignment, "version": version_info(item)})
    return results


def relationships(items: list[dict], scores: list[dict]) -> tuple[list[dict], dict[str, int]]:
    profile_map = {entry["id"]: set(entry["profile_alignment"].get("matched_terms", [])) for entry in scores}
    result: list[dict] = []
    counts = {"conflict": 0, "complementary": 0, "unrelated": 0}
    for index, left in enumerate(items):
        left_triggers = trigger_terms(left)
        left_capabilities = capability_terms(left)
        for right in items[index + 1:]:
            right_triggers = trigger_terms(right)
            right_capabilities = capability_terms(right)
            trigger_union = left_triggers | right_triggers
            trigger_overlap = left_triggers & right_triggers
            trigger_ratio = round(len(trigger_overlap) / len(trigger_union), 3) if trigger_union else 0.0
            generic_triggers = {"创建", "审查", "查询", "文档", "技能", "通用技能", "分析", "使用", "生成", "控制", "工具", "create", "review", "use"}
            def meaningful_contains(a: str, b: str) -> bool:
                shorter, longer = (a, b) if len(a) <= len(b) else (b, a)
                if shorter in generic_triggers:
                    return False
                if re.fullmatch(r"[\u4e00-\u9fff]+", shorter):
                    return len(shorter) >= 3 and shorter in longer
                # Identifier substrings such as summarize/skills-summarize-audit or
                # figma-use/figma-use-motion are distinct invocation IDs, not trigger conflicts.
                return False
            contains_trigger = any(meaningful_contains(a, b) for a in left_triggers for b in right_triggers)
            if contains_trigger:
                trigger_ratio = max(trigger_ratio, 0.6)
            capability_union = left_capabilities | right_capabilities
            capability_overlap = left_capabilities & right_capabilities
            capability_ratio = round(len(capability_overlap) / len(capability_union), 3) if capability_union else 0.0
            complement_profile_terms = {"知识", "写作", "调研", "视频", "网页", "历史", "小说", "图像", "游戏", "投资", "安全", "测试", "自动化", "研究"}
            shared_profile = (profile_map.get(left["id"], set()) & profile_map.get(right["id"], set())) & complement_profile_terms
            if trigger_ratio >= 0.5:
                relationship = "conflict"
                reason = "触发词或描述高度重叠"
            elif trigger_ratio < 0.3 and capability_ratio <= 0.15 and shared_profile:
                relationship = "complementary"
                reason = "服务同一画像需求，但触发词与能力边界不同"
            else:
                relationship = "unrelated"
                reason = "当前证据不足以判定冲突或互补"
            counts[relationship] += 1
            if relationship != "unrelated":
                result.append({"left": left["id"], "right": right["id"], "relationship": relationship, "trigger_overlap": trigger_ratio, "capability_overlap": capability_ratio, "shared_profile_terms": sorted(shared_profile), "reason": reason})
    return result, counts


def recommendations(scores: list[dict], item_issues: list[dict], relationship_items: list[dict]) -> list[dict]:
    by_id: dict[str, list[dict]] = {}
    for entry in item_issues:
        by_id.setdefault(entry["id"], []).append(entry)
    result: list[dict] = []
    for scored in scores:
        entries = by_id.get(scored["id"], [])
        severities = {entry["severity"] for entry in entries}
        if "critical" in severities:
            decision, reason = "升级/修复", "存在 critical 来源或解析问题"
        elif "warning" in severities:
            decision, reason = "优化", "存在元数据或说明质量问题"
        elif scored["health_score"] >= 8 and (scored["profile_alignment"].get("score") or 0) > 0:
            decision, reason = "保留", "健康分达标且与用户画像有匹配证据"
        elif scored["health_score"] >= 8:
            decision, reason = "观察", "健康分达标但当前画像匹配证据不足"
        else:
            decision, reason = "观察", "健康分或证据不足，暂不做安装/归档结论"
        result.append({"target": scored["id"], "decision": decision, "reason": reason, "evidence": [entry["code"] for entry in entries]})
    for relation in relationship_items:
        if relation["relationship"] == "conflict":
            result.append({"target": f"{relation['left']} + {relation['right']}", "decision": "边界调整", "reason": relation["reason"], "evidence": [f"trigger_overlap={relation['trigger_overlap']}"]})
        elif relation["relationship"] == "complementary":
            result.append({"target": f"{relation['left']} + {relation['right']}", "decision": "共存", "reason": relation["reason"], "evidence": [f"capability_overlap={relation['capability_overlap']}", "shared_profile=" + ",".join(relation["shared_profile_terms"])]})
    return result


def bundle_name(item: dict) -> str:
    """Return the installed source group without treating cache entries as UI-visible skills."""
    paths = "|".join(str(path).replace("\\", "/") for path in item.get("source_paths", []))
    for name in ("openai-templates", "figma", "github", "browser", "computer-use", "visualize"):
        if f"/{name}/" in paths:
            return name
    if item.get("source_type") == "codex_runtime_plugin":
        return "runtime"
    if item.get("source_type") == "codex_system_skill":
        return "system"
    return "global"


def inventory_analysis(items: list[dict], scores: list[dict], recommendation_items: list[dict], profile_status: str) -> dict:
    """Summarize installed sources, suitability, and inferred pressure without claiming usage data."""
    score_by_id = {entry["id"]: entry for entry in scores}
    recommendation_by_id = {entry["target"]: entry for entry in recommendation_items if " + " not in entry["target"]}
    bundles: dict[str, list[dict]] = defaultdict(list)
    source_counts = Counter()
    decision_counts = Counter()
    repair_candidates = []
    for item in items:
        bundle = bundle_name(item)
        bundles[bundle].append(item)
        source_counts[item.get("source_type", "unavailable")] += 1
        score = score_by_id.get(item["id"], {})
        alignment = score.get("profile_alignment", {})
        fit_score = alignment.get("score")
        suitability = "unavailable" if alignment.get("status") not in {"observed", "inferred"} else ("高" if (fit_score or 0) >= 4 else "中" if (fit_score or 0) >= 2 else "低")
        decision = recommendation_by_id.get(item["id"], {}).get("decision", "观察")
        decision_counts[decision] += 1
        if decision in {"优化", "升级/修复"}:
            repair_candidates.append({
                "id": item["id"], "bundle": bundle, "source_type": item.get("source_type"),
                "health_score": score.get("health_score"), "suitability": suitability,
                "decision": decision, "usage": "unavailable",
            })
    bundle_rows = []
    candidates = list(repair_candidates)
    for name, members in sorted(bundles.items(), key=lambda entry: (-len(entry[1]), entry[0])):
        plugin_group = name not in {"global", "system", "runtime"}
        low_fit = 0
        for item in members:
            alignment = score_by_id.get(item["id"], {}).get("profile_alignment", {})
            if alignment.get("status") in {"observed", "inferred"} and (alignment.get("score") or 0) == 0:
                low_fit += 1
        pressure = "高" if len(members) >= 12 else "中" if len(members) >= 5 else "低"
        advice = "暂不变更，补充使用证据" if plugin_group else "按任务保留"
        bundle_rows.append({
            "bundle": name, "items": len(members), "source_types": sorted({item.get("source_type") for item in members}),
            "low_suitability_items": low_fit, "context_pressure": pressure,
            "pressure_status": "inferred", "advice": advice,
        })
    return {
        "usage_evidence": "unavailable: 未取得可归因的结构化 session/tool-call 事件",
        "profile_status": profile_status,
        "source_counts": dict(sorted(source_counts.items())),
        "decision_counts": dict(sorted(decision_counts.items())),
        "bundles": bundle_rows,
        "action_candidates": candidates,
        "context_pressure_note": "按安装项数量推断来源组的潜在发现/选择噪声；不等同于实际注入 prompt token。",
    }


def audit(root: Path, catalog_dir: Path, runtime_dir: Path, staging_dir: Path | None, user_skill_dir: Path | None, scope: str, visible_ids: list[str], profile_path: Path | None = None, baseline: dict | None = None, scan_mode: str = "auto") -> tuple[dict, list[Path]]:
    items, watched = collect(root, catalog_dir, runtime_dir, staging_dir, user_skill_dir)
    selected = logical_items(items, scope, visible_ids if scope == "visible" else None)
    context = {"scope": scope, "visible_ids": sorted(visible_ids),
               "roots": [str(p.resolve()) if p else None for p in (root, catalog_dir, runtime_dir, staging_dir, user_skill_dir)],
               "inputs": digest_paths([profile_path] if profile_path else []),
               "engine": digest_paths(Path(__file__).parent.glob("*.py"))}
    scan, reused, snapshot = plan_scan(selected, context, baseline, scan_mode)
    issues = [entry for item in selected for entry in (reused[item["id"]] if item["id"] in reused else audit_item(item))]
    finish_scan(scan, snapshot, issues)
    profile_text, profile_status = load_profile(profile_path)
    scores = score_items(selected, issues, profile_text, profile_status)
    by_severity = {severity: sum(entry["severity"] == severity for entry in issues) for severity in ("critical", "warning", "info")}
    relationship_candidates = [item for item in selected if item.get("source_type") != "codex_plugin_manifest"]
    relationship_scores = [entry for entry in scores if any(item["id"] == entry["id"] for item in relationship_candidates)]
    relationship_items, relationship_counts = relationships(relationship_candidates, relationship_scores)
    recommendation_items = recommendations(scores, issues, relationship_items)
    inventory = inventory_analysis(selected, scores, recommendation_items, profile_status)
    report = {
        "schema_version": 1,
        "mode": "read_only",
        "scope": scope,
        "summary": {"items_scanned": len(selected), "issues": len(issues), "by_severity": by_severity},
        "unresolved_items": unresolved_visible_items(selected) if scope == "visible" else [],
        "issues": issues,
        "profile": {"status": profile_status, "source": str(profile_path) if profile_status == "observed" else None},
        "skill_scores": scores,
        "relationships": relationship_items,
        "relationship_counts": relationship_counts,
        "recommendations": recommendation_items,
        "inventory_analysis": inventory,
        "discovery_summary": inventory_summary(items),
        "external_candidate_status": "unavailable: 未取得本次联网同意",
        "items": selected,
        "watched_source_count": len(watched),
        "scan": scan,
        "baseline": snapshot,
    }
    return enrich_report(report), watched


# ============================================================================
# v9.0.0 新增：生态综合评估（ecosystem scope）
# ============================================================================


def load_mcp_tool_counts(reasonix_dir: Path) -> dict[str, int]:
    """从 Reasonix mcp/*.json 提取每个 server 的真实 tool_count。

    返回 {server_name_normalized: tool_count}。
    名称规范化：取文件名去掉 .json 后缀，保持原样。
    """
    result: dict[str, int] = {}
    if not reasonix_dir.exists():
        return result
    for json_file in reasonix_dir.glob("*.json"):
        try:
            data = json.loads(json_file.read_text(encoding="utf-8"))
            tools = data.get("tools", [])
            result[json_file.stem] = len(tools)
        except Exception:
            pass
    return result


def load_mcp_config(config_path: Path) -> dict:
    """加载 ZCode MCP 配置。"""
    if not config_path.exists():
        return {}
    try:
        with open(config_path, encoding="utf-8") as f:
            data = json.load(f)
        # ZCode 格式：{mcp: {servers: {...}}} 或标准 {mcpServers: {...}}
        servers = data.get("mcp", {}).get("servers", {})
        if not servers:
            servers = data.get("mcpServers", {})
        return servers
    except Exception:
        return {}


def estimate_token_count(text: str) -> int:
    """粗估 token 数：中文 chars/1.8，英文 chars/4。"""
    zh_chars = len(re.findall(r"[\u4e00-\u9fa5]", text))
    en_chars = len(text) - zh_chars
    return int(zh_chars / 1.8 + en_chars / 4)


def assess_mcp_health(mcp_config: dict, signals: dict) -> list[dict]:
    """评估每个 MCP server 的六维健康分。详见 mcp-health-checklist.md。"""
    results = []
    observed_servers = {m["mcp_server"]: m for m in signals.get("mcp_usage_evidence", [])}

    for server_name, cfg in mcp_config.items():
        dims = {}

        # 维度 1: 配置完整性
        has_command = bool(cfg.get("command") or cfg.get("url"))
        has_args = isinstance(cfg.get("args"), list) or cfg.get("url")
        dims["config"] = {"status": "pass" if (has_command and has_args) else "fail",
                          "reason": "" if (has_command and has_args) else "缺少 command 或 args"}

        # 维度 2: 启动可达性（简化：仅检查 command 存在，实际启动测试由 agent 执行）
        dims["startup"] = {"status": "unavailable", "reason": "配置存在不证明可启动；本扫描不执行 MCP 命令"}

        # 维度 3: 权限边界
        env = cfg.get("env", {})
        exposed = []
        for k, v in env.items():
            if re.search(r"(?i)(token|key|secret|password|api[_-]?key)", k) and v and not str(v).startswith("${"):
                exposed.append({"field": k})
        url = cfg.get("url", "")
        is_https = url.startswith("https://") if url else True
        dims["permissions"] = {"status": "warn" if not is_https else "unavailable" if exposed else "pass",
                               "exposed_fields": exposed, "https": is_https,
                               "reason": "含凭据字段；尚未核验权限、Git 跟踪与日志暴露，不能判定泄漏或安全" if exposed else "仅检查配置字段及传输声明，非安全认证"}

        # 维度 4: Schema 健康（简化：从 Reasonix mcp/*.json 读取 tool_count，否则标 unavailable）
        dims["schema"] = {"status": "unavailable", "reason": "tool_count 需读取 Reasonix mcp/*.json 或实际 list_tools"}

        # 维度 5: 实际调用证据
        obs = observed_servers.get(server_name)
        if obs:
            calls = obs.get("tool_calls")
            valid_calls = isinstance(calls, int) and not isinstance(calls, bool) and calls >= 0
            known_usage = valid_calls and (calls > 0 or (obs.get("coverage_complete") is True and obs.get("status") == "observed"))
            if obs.get("status") == "configured_never_observed" or not known_usage:
                dims["usage"] = {"status": "unavailable", "calls": None, "reason": "configured; no attributable calls in scanned records"}
            else:
                dims["usage"] = {"status": "pass", "calls": calls, "last_used": obs.get("last_used")}
        else:
            dims["usage"] = {"status": "unavailable", "calls": None, "reason": "no signals data"}

        # 维度 6: 跨客户端一致（标 unavailable，需扫描多客户端配置）
        dims["consistency"] = {"status": "unavailable", "reason": "需扫描多客户端配置"}

        # 综合健康分（权重见 mcp-health-checklist.md）
        weights = {"startup": 0.25, "config": 0.15, "permissions": 0.20, "schema": 0.10, "usage": 0.20, "consistency": 0.10}
        score_map = {"pass": 10, "warn": 5, "fail": 0}
        total_weight = 0
        weighted_sum = 0
        for dim, w in weights.items():
            status = dims[dim]["status"]
            if status in score_map:
                weighted_sum += score_map[status] * w
                total_weight += w
        health_score = round(weighted_sum / total_weight, 1) if total_weight else 0
        grade = "partial" if any(d["status"] == "unavailable" for d in dims.values()) else ("healthy" if health_score >= 8 else "ok" if health_score >= 6 else "needs_attention" if health_score >= 4 else "unhealthy")

        # v9.1.0: Pass through related_python_package and headroom proxy info from signals
        related_python = None
        working_mode = None
        status_note = None
        if obs:
            related_python = obs.get("related_python_package")
            working_mode = obs.get("working_mode")
            status_note = obs.get("status_note")
            # Proxy activity is independent evidence, not an MCP invocation count.
            if working_mode == "proxy_active":
                dims["usage"]["proxy_active"] = True
                dims["usage"]["proxy_note"] = "proxy 通道活跃；不能替代可归因 MCP 调用或证明完整采集覆盖"

        results.append({
            "server": server_name,
            "health_score": health_score,
            "grade": grade,
            "dimensions": dims,
            "config": {"transport": "remote" if cfg.get("url") else "stdio", "env_fields": sorted(env), "has_command": bool(cfg.get("command"))},
            "exposure": {
                "executes_local_commands": {"status": "observed", "value": bool(cfg.get("command"))},
                "requires_network": {"status": "observed" if cfg.get("url") else "unavailable", "value": True if cfg.get("url") else None},
                "requires_token": {"status": "inferred" if any(re.search(r"(?i)(token|key|secret)", k) for k in env) else "unavailable", "value": True if any(re.search(r"(?i)(token|key|secret)", k) for k in env) else None},
                "arbitrary_shell": {"status": "unavailable", "value": None},
                "offline_review": {"status": "observed", "value": True},
                "upstream_overwrite": {"status": "unavailable", "value": None},
            },
            "data_source": {"config_path": "observed", "signals_source": "extract_usage_signals.py" if signals else "unavailable"},
            "related_python_package": related_python,
            "working_mode": working_mode,
            "status_note": status_note,
        })
    return results


def load_agent_capabilities(yaml_path: Path) -> dict:
    """从 capability-dimensions.yaml 的 agent_tools 节加载 agent 能力矩阵。

    返回: {"agent_name": {"dimension_id": level, ...}, ...} 以及元信息。
    如果 yaml 不可用或解析失败，回退到 fallback_builtin。
    """
    fallback = {
        "general-purpose": {"reasoning": 7, "file-ops": 8, "code-analysis": 6, "research": 7},
        "Explore": {"research": 8, "file-ops": 7, "web-search": 6},
        "data-worker": {"file-ops": 8, "integration": 6},
        "docs-worker": {"file-ops": 7, "reasoning": 5},
        "implementation-worker": {"code-analysis": 8, "file-ops": 7, "reasoning": 6},
        "test-worker": {"code-analysis": 7, "file-ops": 6},
        "quality-expert": {"skill-audit": 8, "code-analysis": 7, "reasoning": 8},
        "security-expert": {"skill-audit": 7, "reasoning": 8},
        "solution-architect": {"reasoning": 9, "code-analysis": 7, "research": 7},
        "research-worker": {"research": 9, "web-search": 8, "file-ops": 6},
        "glm-adversarial-reviewer": {"reasoning": 8, "skill-audit": 7, "code-analysis": 6},
    }
    if not yaml_path or not yaml_path.exists():
        return {"capabilities": fallback, "source": "fallback_builtin", "reason": "yaml_path not found or not provided"}
    try:
        import yaml
        with open(yaml_path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
        agent_tools = data.get("agent_tools", [])
        if not agent_tools:
            return {"capabilities": fallback, "source": "fallback_builtin", "reason": "agent_tools section empty or missing"}
        result = {}
        for entry in agent_tools:
            name = entry.get("name")
            caps = entry.get("capabilities", {})
            if not name:
                continue
            result[name] = {}
            for dim_id, dim_info in caps.items():
                if isinstance(dim_info, dict):
                    result[name][dim_id] = dim_info.get("level", 5)
                elif isinstance(dim_info, (int, float)):
                    result[name][dim_id] = int(dim_info)
        if not result:
            return {"capabilities": fallback, "source": "fallback_builtin", "reason": "parsed agent_tools yielded zero entries"}
        return {"capabilities": result, "source": "observed_yaml", "reason": "loaded from " + str(yaml_path)}
    except ImportError:
        return {"capabilities": fallback, "source": "fallback_builtin", "reason": "PyYAML not installed"}
    except Exception as e:
        return {"capabilities": fallback, "source": "fallback_builtin", "reason": f"yaml parse error: {e}"}


def assess_agent_dispatch(signals: dict, agents_dir: Path | None = None, capabilities_yaml: Path | None = None) -> dict:
    """评估 sub-agent 调用歧义。详见 agent-dispatch-ambiguity.md。

    新增 capabilities_yaml 参数：如果提供，从 capability-dimensions.yaml 的 agent_tools 加载真实能力矩阵。
    """
    # 加载 agent 能力矩阵
    caps_result = load_agent_capabilities(capabilities_yaml) if capabilities_yaml else {"capabilities": {}, "source": "fallback_builtin", "reason": "no capabilities_yaml provided"}
    agent_capabilities = caps_result["capabilities"]
    caps_source = caps_result["source"]

    # 如果加载结果为空，使用 fallback
    if not agent_capabilities:
        agent_capabilities = {
            "general-purpose": {"reasoning": 7, "file-ops": 8, "code-analysis": 6, "research": 7},
            "Explore": {"research": 8, "file-ops": 7, "web-search": 6},
            "data-worker": {"file-ops": 8, "integration": 6},
            "docs-worker": {"file-ops": 7, "reasoning": 5},
            "implementation-worker": {"code-analysis": 8, "file-ops": 7, "reasoning": 6},
            "test-worker": {"code-analysis": 7, "file-ops": 6},
            "quality-expert": {"skill-audit": 8, "code-analysis": 7, "reasoning": 8},
            "security-expert": {"skill-audit": 7, "reasoning": 8},
            "solution-architect": {"reasoning": 9, "code-analysis": 7, "research": 7},
            "research-worker": {"research": 9, "web-search": 8, "file-ops": 6},
            "glm-adversarial-reviewer": {"reasoning": 8, "skill-audit": 7, "code-analysis": 6},
        }
        caps_source = "fallback_builtin"

    # 调用频次分布
    dispatch_stats = {s["profile_id"]: s for s in signals.get("agent_dispatch_stats", [])}
    total_dispatches = sum(s["dispatch_count"] for s in dispatch_stats.values()) or 1

    # 两两 overlap 计算
    profile_ids = list(agent_capabilities.keys())
    overlap_pairs = []
    for i, a in enumerate(profile_ids):
        for b in profile_ids[i + 1:]:
            caps_a = agent_capabilities[a]
            caps_b = agent_capabilities[b]
            common = set(caps_a) & set(caps_b)
            union = set(caps_a) | set(caps_b)
            jaccard = len(common) / len(union) if union else 0
            # 加权 overlap（考虑 level 相似度）
            if common:
                diffs = [abs(caps_a[d] - caps_b[d]) for d in common]
                similarity = 1 - (sum(diffs) / len(diffs)) / 10
                weighted = jaccard * similarity
            else:
                weighted = 0

            # 风险等级
            freq_a = dispatch_stats.get(a, {}).get("dispatch_count", 0) / total_dispatches
            freq_b = dispatch_stats.get(b, {}).get("dispatch_count", 0) / total_dispatches
            freq_diff = abs(freq_a - freq_b)
            if jaccard >= 0.7 and freq_diff >= 0.3:
                risk = "critical"
                reason = f"能力重叠 {jaccard:.0%}，调用频次差异 {freq_diff:.0%}"
            elif jaccard >= 0.5 and freq_diff >= 0.2:
                risk = "warning"
                reason = f"能力部分重叠 {jaccard:.0%}，建议明确边界"
            else:
                continue  # 不输出 ok 对

            overlap_pairs.append({
                "agent_a": a,
                "agent_b": b,
                "overlap": round(jaccard, 2),
                "weighted_overlap": round(weighted, 2),
                "shared_dimensions": sorted(common),
                "freq_a": round(freq_a, 3),
                "freq_b": round(freq_b, 3),
                "risk_level": risk,
                "risk_reason": reason,
            })

    overlap_pairs.sort(key=lambda x: x["overlap"], reverse=True)

    # unmapped: signals 中出现但 capabilities 字典中没有的 agent，标 unmapped=true 以避免假阳性判断
    unmapped_set = {pid for pid in dispatch_stats if pid not in agent_capabilities}

    return {
        "status": "inferred" if dispatch_stats else "unavailable",
        "reason": "按声明能力与历史频次推断，不证明实际误派单" if dispatch_stats else "未提供可归因派单记录，不能将零风险对解释为正常",
        "capability_matrix": [{"profile_id": k, "capabilities": v} for k, v in agent_capabilities.items()],
        "overlap_pairs": overlap_pairs,
        "dispatch_distribution": {
            pid: {
                "count": s["dispatch_count"],
                "share": round(s["dispatch_count"] / total_dispatches, 3),
                "avg_tokens": s["avg_tokens"],
                **({"unmapped": True} if pid in unmapped_set else {}),
            }
            for pid, s in dispatch_stats.items()
        },
        "capabilities_source": caps_source,
        "unmapped_agents": sorted(unmapped_set),
        "data_source": {
            "capabilities": caps_source,
            "signals": "extract_usage_signals.py (observed)",
            "yaml_path": str(capabilities_yaml) if capabilities_yaml else None,
        },
    }


def assess_context_pressure(user_skill_dir: Path, mcp_config: dict, agents_dir: Path | None = None, reasonix_dir: Path | None = None) -> dict:
    """评估上下文压力。详见 context-pressure-assessment.md。

    新增 reasonix_dir 参数：如果提供，从 Reasonix mcp/*.json 读取真实的 tool_count。
    """
    context_window = 200000  # 假设值

    # Skills 注入估算
    skill_tokens = {}
    if user_skill_dir.exists():
        for skill_md in user_skill_dir.glob("*/SKILL.md"):
            try:
                desc = str(frontmatter(skill_md).get("description") or "")
                tokens = estimate_token_count(desc) + 10
                skill_tokens[skill_md.parent.name] = tokens
            except Exception:
                pass

    skills_total = sum(skill_tokens.values())

    # 加载 Reasonix 真实 tool_count（如果提供了 reasonix_dir）
    reasonix_counts = load_mcp_tool_counts(reasonix_dir) if reasonix_dir else {}

    # MCP schema 注入估算
    mcp_per_server = {}
    mcp_total = 0
    tool_count_source_summary: dict[str, int] = {"observed_reasonix": 0, "estimated_default": 0}
    for server in mcp_config:
        # 尝试精确名匹配
        tool_count = reasonix_counts.get(server)
        if tool_count is not None:
            tool_count_source = "observed_reasonix"
            tool_count_source_summary["observed_reasonix"] += 1
        else:
            # 尝试模糊匹配：检查 server 名是否包含在 reasonix 文件名中，或反过来
            for rx_name, rx_count in reasonix_counts.items():
                if server.lower() in rx_name.lower() or rx_name.lower() in server.lower():
                    tool_count = rx_count
                    tool_count_source = "observed_reasonix"
                    tool_count_source_summary["observed_reasonix"] += 1
                    break
            else:
                # 找不到则 fallback 到默认值 10
                tool_count = 10
                tool_count_source = "estimated_default"
                tool_count_source_summary["estimated_default"] += 1
        server_tokens = tool_count * 300
        mcp_per_server[server] = {"tools": tool_count, "tokens": server_tokens, "tool_count_source": tool_count_source}
        mcp_total += server_tokens

    # Agent profile 注入估算
    agent_tokens = {}
    agents_total = 0
    agent_status = "unavailable"
    agent_reason = ""
    if agents_dir and agents_dir.exists():
        # 优先扫描 *.md（传统 profile 文件）
        for profile_md in agents_dir.glob("*.md"):
            try:
                text = profile_md.read_text(encoding="utf-8")
                tokens = estimate_token_count(text)
                agent_tokens[profile_md.stem] = tokens
                agents_total += tokens
                agent_status = "observed"
            except Exception:
                pass
        # 如果没有 .md 文件，递归查找 sess_*/agent_*/metadata.json
        if not agent_tokens:
            metadata_files = sorted(agents_dir.glob("sess_*/agent_*/metadata.json"))
            if metadata_files:
                seen_profiles: dict[str, str] = {}
                for meta_path in metadata_files:
                    try:
                        data = json.loads(meta_path.read_text(encoding="utf-8"))
                        snap = data.get("profileSnapshot", {})
                        name = snap.get("name", meta_path.parent.name)
                        desc = snap.get("description", "")
                        if name not in seen_profiles:
                            seen_profiles[name] = desc
                    except Exception:
                        pass
                for name, desc in seen_profiles.items():
                    tokens = estimate_token_count(desc) + 10  # 附加 frontmatter 开销
                    agent_tokens[name] = tokens
                    agents_total += tokens
                if agent_tokens:
                    agent_status = "observed"
            else:
                agent_reason = "无 profile.md 且无 metadata.json 可推断"
    else:
        agent_reason = "agents_dir 不存在或未指定"

    total = skills_total + mcp_total + agents_total
    pressure_percent = round(total / context_window * 100, 2)
    grade = "low_pressure" if pressure_percent < 5 else "moderate_pressure" if pressure_percent < 10 else "high_pressure" if pressure_percent < 20 else "critical_pressure"

    return {
        "total_injection_tokens": total,
        "context_window_assumed": context_window,
        "pressure_percent": pressure_percent,
        "grade": grade,
        "breakdown": {
            "skills": {"total_tokens": skills_total, "count": len(skill_tokens), "per_skill": skill_tokens},
            "mcp": {"total_tokens": mcp_total, "count": len(mcp_config), "per_server": mcp_per_server, "tool_count_source_summary": tool_count_source_summary},
            "agents": {"total_tokens": agents_total, "count": len(agent_tokens), "per_agent": agent_tokens, "status": agent_status, "reason": agent_reason},
        },
        "data_source": {
            "skills": "observed (SKILL.md frontmatter)",
            "mcp": "observed (Reasonix mcp/*.json tool_count) / estimated_default if unmatched",
            "agents": "observed (profile.md / metadata.json)" if agent_status == "observed" else f"unavailable: {agent_reason}" if agent_reason else "unavailable",
            "context_window": "assumed (200K, not measured)",
        },
    }


def valid_signals_payload(signals: object) -> bool:
    """Validate fields consumed by ecosystem scoring and health output."""
    if not isinstance(signals, dict):
        return False
    record_specs = (
        ("mcp_usage_evidence", "mcp_server", "tool_calls"),
        ("skill_invocation_evidence", "skill_id", "invocations"),
        ("agent_dispatch_stats", "profile_id", "dispatch_count"),
    )
    for key, identifier, count_key in record_specs:
        entries = signals.get(key, [])
        if not isinstance(entries, list):
            return False
        for entry in entries:
            if not isinstance(entry, dict) or not isinstance(entry.get(identifier), str) or not entry[identifier]:
                return False
            if count_key in entry and (not isinstance(entry[count_key], int) or isinstance(entry[count_key], bool) or entry[count_key] < 0):
                return False
            if "coverage_complete" in entry and not isinstance(entry["coverage_complete"], bool):
                return False
            if key == "mcp_usage_evidence" and entry.get("status") == "observed" and count_key not in entry:
                return False
    summary = signals.get("scan_summary", {})
    if not isinstance(summary, dict):
        return False
    if isinstance(summary, dict):
        if "coverage_complete" in summary and not isinstance(summary["coverage_complete"], bool):
            return False
        if "agents_scanned" in summary and (not isinstance(summary["agents_scanned"], int) or summary["agents_scanned"] < 0):
            return False
        if "clients_scanned" in summary and (not isinstance(summary["clients_scanned"], list) or not all(isinstance(c, str) for c in summary["clients_scanned"])):
            return False
    return True


def audit_ecosystem(
    user_skill_dir: Path,
    zcode_config_path: Path,
    agents_dir: Path | None,
    signals_path: Path | None = None,
    profile_path: Path | None = None,
    root: Path | None = None,
    catalog_dir: Path | None = None,
    runtime_dir: Path | None = None,
    staging_dir: Path | None = None,
    reasonix_dir: Path | None = None,
    capabilities_yaml: Path | None = None,
    market_evidence: dict | None = None,
    baseline: dict | None = None,
    scan_mode: str = "auto",
    signals_data: dict | None = None,
) -> dict:
    """v9.0.0 生态综合评估主函数（MCP + Agent + Skill 三层）。"""
    # 加载 MCP 配置
    mcp_config = load_mcp_config(zcode_config_path)

    # 不隐式扫描会话；未提供 signals 时在报告中明确补采集。
    signals = {}
    signals_status = "unavailable: 未提供 signals；请运行 extract_usage_signals.py 后使用 --signals-path"
    if signals_path and not signals_path.exists():
        signals_status = "unavailable: 指定的 signals 文件不存在"
    if signals_path and signals_path.exists():
        try:
            with open(signals_path, encoding="utf-8") as f:
                signals = json.load(f)
            if not isinstance(signals, dict):
                signals = {}
                signals_status = "unavailable: signals 必须是 JSON object"
            elif not valid_signals_payload(signals):
                signals = {}
                signals_status = "unavailable: signals 记录结构不符合契约"
            else:
                signals_status = "observed"
        except (OSError, ValueError) as exc:
            signals_status = f"unavailable: signals 无法读取 ({type(exc).__name__})"

    if signals_data is not None:
        if valid_signals_payload(signals_data):
            signals, signals_status = signals_data, "observed"
        else:
            signals, signals_status = {}, "unavailable: signals_data 记录结构不符合契约"

    # 执行三项评估：MCP、Agent、Context Pressure
    mcp_health = assess_mcp_health(mcp_config, signals)
    agent_dispatch = assess_agent_dispatch(signals, agents_dir, capabilities_yaml=capabilities_yaml)
    context_pressure = assess_context_pressure(user_skill_dir, mcp_config, agents_dir, reasonix_dir=reasonix_dir)

    # Skill 层评估：调用 audit() 获取技能审查数据
    skill_layer: dict = {"status": "unavailable", "reason": "未提供 root/catalog_dir 等参数"}
    if root:
        try:
            cat_dir = catalog_dir or (root / "cache" / "remote_plugin_catalog")
            run_dir = runtime_dir or (Path.home() / ".cache" / "codex-runtimes")
            stag_dir = staging_dir or (root / ".tmp" / "bundled-marketplaces")
            if not stag_dir.exists():
                stag_dir = None
            skill_report, _ = audit(
                root=root,
                catalog_dir=cat_dir,
                runtime_dir=run_dir,
                staging_dir=stag_dir,
                user_skill_dir=user_skill_dir,
                scope="installed",
                visible_ids=[],
                profile_path=profile_path,
                baseline=baseline, scan_mode=scan_mode,
            )
            skill_layer = {
                "status": "observed",
                "skill_scores": skill_report.get("skill_scores", []),
                "relationships": [r for r in skill_report.get("relationships", []) if r.get("relationship") in ("conflict", "complementary")],
                "issues_critical": sum(1 for i in skill_report.get("issues", []) if i["severity"] == "critical"),
                "issues_warning": sum(1 for i in skill_report.get("issues", []) if i["severity"] == "warning"),
                "items_scanned": skill_report.get("summary", {}).get("items_scanned", 0),
                "issues": skill_report.get("issues", []),
                "discovery_summary": skill_report.get("discovery_summary", {}),
            }
        except Exception as e:
            skill_layer = {"status": "unavailable", "reason": f"audit() 调用失败: {e}"}

    # v9.0.0 B3 修复：计算配置优化建议（value_score + 三层分层）
    optimization = compute_optimization_layer(
        skill_layer=skill_layer,
        mcp_health=mcp_health,
        signals=signals,
        market_evidence=market_evidence,
    )

    report = {
        "schema_version": 2,
        "mode": "read_only",
        "scope": "ecosystem",
        "ecosystem_assessment": {
            "skill_layer": skill_layer,
            "mcp_health": mcp_health,
            "agent_dispatch": agent_dispatch,
            "context_pressure": context_pressure,
            "optimization": optimization,
        },
        "signals_source": "in_memory (显式统计输入)" if signals_data is not None else str(signals_path) if signals_path else "unavailable (需先运行 extract_usage_signals.py)",
        "signals_status": signals_status,
        "usage_coverage": signals.get("scan_summary", {}),
        "scope_sources": {"skills": str(root.resolve()) if root else None,
                          "user_skills": str(user_skill_dir.resolve()),
                          "mcp_config": str(zcode_config_path.resolve()),
                          "agents": str(agents_dir.resolve()) if agents_dir else None},
        "scan_status": "complete" if skill_layer["status"] == "observed" else "partial",
        "assessment_status": "partial",
        "module_coverage": {"local_sources": skill_layer["status"], "usage": signals_status,
                            "agent_dispatch": agent_dispatch.get("status", "unavailable"),
                            "context": "estimated", "runtime": "unavailable",
                            "upstream_versions": "unavailable", "security": "unavailable",
                            "ui_visibility": "unavailable", "market": "input_supplied_unverified" if market_evidence else "unavailable"},
        "data_contract": {
            "mcp_health_score": "inferred (基于配置 + signals)",
            "agent_overlap": "inferred (基于 capability-dimensions 基线)",
            "context_pressure": "estimated (基于 token 估算公式)",
            "dispatch_count": "observed (从 transcript 计数)",
            "skill_layer": "observed (基于 audit() 审查)" if skill_layer["status"] == "observed" else f"unavailable ({skill_layer.get('reason', 'N/A')})",
            "optimization": "inferred only with complete evidence; missing dimensions unavailable",
        },
    }
    if root and skill_layer["status"] == "observed":
        report["scan"], report["baseline"] = skill_report["scan"], skill_report["baseline"]
        finish_scan(report["scan"], report["baseline"], skill_report["issues"], optimization["summary"].get("evidence_coverage"))
    enrich_report(report)
    for rec in optimization.get("mcp_recommendations", []):
        health = next((m for m in mcp_health if m["server"] == rec["target"]), {})
        rec["action_plan"]["exposure"].update(health.get("exposure", {}))
    return report


def compute_optimization_layer(skill_layer: dict, mcp_health: list[dict], signals: dict, market_evidence: dict | None = None) -> dict:
    """
    v9.0.0 B3 修复：计算生态优化建议。
    使用独立的 compute_value_scores 模块，避免污染 audit_skill_plugin_issues 主逻辑。
    """
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        from compute_value_scores import (
            assess_skills_optimization,
            assess_mcp_optimization,
            ecosystem_optimization_summary,
        )
    except ImportError:
        return {
            "status": "unavailable",
            "reason": "compute_value_scores.py 模块不可用",
            "recommendations": [],
            "summary": {},
        }

    # 从 signals 提取使用证据
    skill_usage_list = signals.get("skill_invocation_evidence", [])
    skill_usage_dict = {s["skill_id"]: s for s in skill_usage_list}
    mcp_usage_list = signals.get("mcp_usage_evidence", [])

    # Skill 层
    if skill_layer.get("status") == "observed":
        skill_recs = assess_skills_optimization(
            skill_scores=skill_layer.get("skill_scores", []),
            skill_usage=skill_usage_dict,
            market_evidence=market_evidence,
        )
    else:
        skill_recs = []

    # MCP 层
    mcp_recs = assess_mcp_optimization(
        mcp_health=mcp_health,
        mcp_usage=mcp_usage_list,
        market_evidence=market_evidence,
    )

    summary = ecosystem_optimization_summary(skill_recs, mcp_recs)

    return {
        "status": "partial" if summary["pending_evidence"] else "inferred",
        "summary": summary,
        "skill_recommendations": skill_recs,
        "mcp_recommendations": mcp_recs,
        "agent_recommendations": [],  # v9.0.0 暂不对 agent 做 value_score（agent 无画像匹配维度）
        "data_source": {
            "skill_usage": "observed" if skill_usage_list else "unavailable (signals 缺失)",
            "mcp_usage": "observed" if mcp_usage_list else "unavailable (signals 缺失)",
            "market_signal": "provided; validated per item" if market_evidence else "unavailable (需联网补全)",
        },
    }


def render_human_report(report: dict, detail: bool = False) -> str:
    """Render the compact, action-first terminal report; keep --json as the full contract."""
    summary = report["summary"]
    severities = summary["by_severity"]
    issues = report["issues"]
    actionable = [entry for entry in issues if entry["severity"] in {"critical", "warning"}]
    relationships = report["relationships"]
    inventory = report["inventory_analysis"]
    lines = [
        "技能/插件审查",
        f"状态: complete | 范围: {report['scope']} | 模式: {report['mode']}",
        f"结论: 扫描 {summary['items_scanned']} 项；需处理 {len(actionable)} 项（critical {severities['critical']} / warning {severities['warning']}）。",
        f"适用度: {inventory['profile_status']} | 使用频率: unavailable（未取得可归因调用证据）。",
    ]
    lines.append(render_actions(report, detail))
    lines.extend(["", "安装全景", "| 来源组 | 项数 | 低适用项 | 上下文压力 | 建议 |", "| --- | ---: | ---: | --- | --- |"])
    for bundle in inventory["bundles"]:
        lines.append(f"| {bundle['bundle']} | {bundle['items']} | {bundle['low_suitability_items']} | {bundle['context_pressure']} (inferred) | {bundle['advice']} |")
    lines.extend(["", "评分与证据边界", "| 维度 | 含义 |", "| --- | --- |", "| 健康分 | 来源、元数据与版本可解析性；不代表常用或适用。 |", "| 适用度 | 仅按用户画像词命中计算；高/中/低为 observed，缺画像则 unavailable。 |", "| 使用频率 | " + inventory["usage_evidence"] + " |", "| 上下文压力 | " + inventory["context_pressure_note"] + " |"])
    if actionable:
        lines.extend(["", "问题证据"])
        for index, entry in enumerate(actionable, 1):
            evidence = entry["evidence"][0] if entry["evidence"] else "unavailable"
            lines.extend([
                f"{index}. [{entry['severity'].upper()}] {entry['id']} - {entry['code']}",
                f"   问题: {entry['message']}",
                f"   证据: {evidence}",
                f"   建议: {entry['remediation']}",
            ])
    else:
        lines.extend(["", "问题证据", "无。"])
    if relationships:
        lines.extend(["", "边界与协同"])
        for relation in relationships:
            overlap = relation["trigger_overlap"] if relation["relationship"] == "conflict" else relation["capability_overlap"]
            action = "明确触发边界" if relation["relationship"] == "conflict" else "保留并按能力分工"
            lines.append(f"- {relation['left']} + {relation['right']}: {relation['relationship']}（重叠 {overlap}）；{action}。")
    candidates = inventory["action_candidates"]
    lines.extend(["", "优化建议", "| 对象 | 来源组 | 健康 | 适用度 | 使用频率 | 建议 |", "| --- | --- | ---: | --- | --- | --- |"])
    if candidates:
        for candidate in candidates:
            decision = "先维修" if candidate["decision"] in {"优化", "升级/修复"} else "[需确认] 评估禁用/卸载"
            lines.append(f"| {candidate['id']} | {candidate['bundle']} | {candidate['health_score']} | {candidate['suitability']} | {candidate['usage']} | {decision} |")
    else:
        lines.append("| 无 | - | - | - | - | 无足够证据建议卸载。 |")
    if detail:
        score_by_id = {entry["id"]: entry for entry in report["skill_scores"]}
        recommendation_by_id = {entry["target"]: entry for entry in report["recommendations"] if " + " not in entry["target"]}
        lines.extend(["", "完整安装清单", "| 技能/插件 | 来源组 | 健康 | 适用度 | 使用频率 | 决策 |", "| --- | --- | ---: | --- | --- | --- |"])
        for item in sorted(report["items"], key=lambda value: (bundle_name(value), value["id"])):
            score = score_by_id.get(item["id"], {})
            alignment = score.get("profile_alignment", {})
            fit = alignment.get("score")
            suitability = "unavailable" if alignment.get("status") not in {"observed", "inferred"} else ("高" if (fit or 0) >= 4 else "中" if (fit or 0) >= 2 else "低")
            decision = recommendation_by_id.get(item["id"], {}).get("decision", "观察")
            lines.append(f"| {item['id']} | {bundle_name(item)} | {score.get('health_score')} | {suitability} | unavailable | {decision} |")
    unavailable = []
    if report["profile"]["status"] != "observed":
        unavailable.append("用户画像")
    if report["external_candidate_status"].startswith("unavailable"):
        unavailable.append("外部候选数据")
    if unavailable:
        lines.extend(["", "未获取数据", "、".join(unavailable) + "；未用默认值补齐。"])
    info_count = severities["info"]
    if info_count:
        lines.extend(["", f"附注: 已折叠 {info_count} 条非阻断提示；使用 --json 查看完整证据。"])
    return "\n".join(lines) + render_footer(report)


def format_coverage(coverage: dict) -> str:
    available, total = coverage.get("available", 0), coverage.get("total", 0)
    return f"{available}/{total} 个评分维度（{available / total:.0%}）" if total else "unavailable（无可评分对象）"


def render_ecosystem_report(report: dict, detail: bool = False) -> str:
    """Render the ecosystem assessment as a human-readable terminal report.

    Defensive: uses .get() on all access; never raises KeyError.
    """
    ea = report.get("ecosystem_assessment", {})
    sl = ea.get("skill_layer", {})
    mcp_health = ea.get("mcp_health", [])
    agent_dispatch = ea.get("agent_dispatch", {})
    context_pressure = ea.get("context_pressure", {})
    optimization = ea.get("optimization", {})

    # -- helpers --
    def grade_emoji(grade: str) -> str:
        mapping = {
            "healthy": "\U0001F7E2",        # 🟢
            "ok": "\U0001F7E1",             # 🟡
            "needs_attention": "\U0001F7E0", # 🟠
            "unhealthy": "\U0001F534",      # 🔴
        }
        return mapping.get(grade, "\u2753")

    def pressure_emoji(grade: str) -> str:
        mapping = {
            "low_pressure": "\U0001F7E2",
            "moderate_pressure": "\U0001F7E1",
            "high_pressure": "\U0001F7E0",
            "critical_pressure": "\U0001F534",
        }
        return mapping.get(grade, "\u2753")

    def risk_emoji(level: str) -> str:
        mapping = {
            "critical": "\U0001F534",  # 🔴
            "warning": "\U0001F7E1",   # 🟡
        }
        return mapping.get(level, "")

    sl_status = sl.get("status", "unavailable")
    sl_items = sl.get("items_scanned", 0)
    sl_crit = sl.get("issues_critical", 0)
    sl_warn = sl.get("issues_warning", 0)

    signals_source = str(report.get("signals_source", "unavailable"))
    report_scope = report.get("scope", "ecosystem")
    report_mode = report.get("mode", "read_only")

    lines = [
        "技能/插件推荐操作 — 生态证据",
        f"扫描状态: {report.get('scan_status', 'partial')} | 评估状态: {report.get('assessment_status', 'partial')} | 范围: {report_scope} | {report_mode}",
        f"扫描方式: {report.get('scan', {}).get('mode', 'unavailable')}；完整扫描不等于工具全部可运行。",
        f"信号源: {signals_source}",
        "",
        f"Skill 层: {sl_status} (扫描 {sl_items} 项；critical {sl_crit} / warning {sl_warn})",
        f"评分证据覆盖: {format_coverage(optimization.get('summary', {}).get('evidence_coverage', {}))}；"
        f"待补证据 {optimization.get('summary', {}).get('pending_evidence', 0)} 项，暂不变更。",
    ]
    sources = report.get("scope_sources", {})
    usage_coverage = report.get("usage_coverage", {})
    if usage_coverage:
        lines.append(f"调用证据范围: 客户端 {', '.join(usage_coverage.get('clients_scanned', []))}；记录 {usage_coverage.get('agents_scanned', 0)}；时间 {usage_coverage.get('time_range')}；覆盖完整={usage_coverage.get('coverage_complete', False)}。")
    lines.append(f"MCP 配置来源: {sources.get('mcp_config', 'unavailable')}（不代表所有客户端）")
    discovered = sl.get("discovery_summary", {})
    if discovered:
        lines.append(f"发现范围: 已安装去重 {discovered.get('installed_unique_items', 0)} 项；仅缓存 {discovered.get('cached_only_source_records', 0)} 条；市场目录 {discovered.get('catalog_only_source_records', 0)} 条（不计入已安装）。")
    lines.append("未验证模块: 实际运行、上游版本新鲜度、完整安全检查、UI 可见性；市场输入由 Agent 核验，CLI 不认证来源真实性。")

    # MCP 健康分布
    lines.append(render_actions(report, detail))
    mcp_total = len(mcp_health)
    mcp_healthy = sum(1 for m in mcp_health if m.get("grade") == "healthy")
    mcp_ok = sum(1 for m in mcp_health if m.get("grade") == "ok")
    mcp_need = sum(1 for m in mcp_health if m.get("grade") == "needs_attention")
    lines.append(
        f"MCP 层: 评估 {mcp_total} 个服务器；"
        f"健康分分布（healthy {mcp_healthy} / ok {mcp_ok} / needs_attention {mcp_need} / partial {sum(m.get('grade') == 'partial' for m in mcp_health)}）"
    )

    # Agent 歧义对计数
    pairs = agent_dispatch.get("overlap_pairs", [])
    critical_count = sum(1 for p in pairs if p.get("risk_level") == "critical")
    warning_count = sum(1 for p in pairs if p.get("risk_level") == "warning")
    if agent_dispatch.get("status") == "unavailable":
        lines.append("Agent 层: unavailable，缺少可归因派单记录；未发现风险对不表示已验证正常。")
    elif critical_count + warning_count:
        lines.append(f"Agent 层: {critical_count + warning_count} 个 critical+warning 风险对（critical {critical_count} / warning {warning_count}）")
    else:
        lines.append("Agent 层: 未发现可归因的 critical/warning 风险对；不代表已验证正常。")

    # == MCP 健康表 ==
    mcp_rows = []
    for m in mcp_health:
        hscore = m.get("health_score", 0)
        usage_dim = m.get("dimensions", {}).get("usage", {})
        calls = usage_dim.get("calls")
        # 仅显示 health_score < 8 或调用次数为 0 的项
        if not detail and m.get("grade") != "partial" and hscore >= 8 and isinstance(calls, (int, float)) and calls > 0:
            continue
        server = m.get("server", "?")
        grade = m.get("grade", "")
        emoji = grade_emoji(grade)
        # 关键问题简述
        dims = m.get("dimensions", {})
        problems = []
        for dkey in ("startup", "config", "permissions", "schema", "usage", "consistency"):
            d = dims.get(dkey, {})
            ds = d.get("status", "")
            if ds == "fail":
                problems.append(d.get("reason", dkey))
            elif ds == "warn":
                problems.append(dkey)
            elif ds == "unavailable":
                problems.append(f"{dkey}: unavailable")
        call_label = f"{calls} [observed]" if usage_dim.get("status") == "pass" and isinstance(calls, int) and not isinstance(calls, bool) and calls >= 0 else "unavailable"

        # v9.1.0: Add related_python_package note and headroom proxy mode to problems
        rpp = m.get("related_python_package")
        if rpp and rpp.get("note"):
            problems.append(rpp["note"])

        wm = m.get("working_mode")
        sn = m.get("status_note")
        if wm == "proxy_active":
            problems.append(f"proxy 模式工作中{'; ' + sn if sn else ''}")
        elif wm == "proxy_unconfirmed":
            problems.append(sn if sn else "proxy 模式检测不可用")

        prob_str = "; ".join(problems) if problems else "无"
        available_dims = sum(d.get("status") != "unavailable" for d in dims.values())
        mcp_rows.append(f"| {server} | {hscore}（{available_dims}/{len(dims)} 维） | {grade} {emoji} | {call_label} | {prob_str} |")

    if mcp_rows:
        lines.extend(["", "## MCP 局部检查（分数仅覆盖已检查维度，不代表运行通过）", "", "| 服务器 | 局部分数/覆盖 | 等级 | 调用次数 | 关键问题 |", "| --- | ---: | :---: | ---: | --- |"] + mcp_rows)

    # == Agent 调用歧义 ==
    risk_pairs = [p for p in pairs if p.get("risk_level") in ("critical", "warning")]
    if risk_pairs:
        lines.extend(["", "## Agent 调用歧义", "| Agent A | Agent B | Overlap | 频次差 | 风险 |", "| --- | --- | ---: | ---: | :---: |"])
        for p in risk_pairs:
            a = p.get("agent_a", "?")
            b = p.get("agent_b", "?")
            overlap = p.get("overlap", 0)
            freq_diff = round(abs(p.get("freq_a", 0) - p.get("freq_b", 0)), 3)
            risk = risk_emoji(p.get("risk_level", ""))
            lines.append(f"| {a} | {b} | {overlap} | {freq_diff} | {risk} |")

    # == 上下文压力 ==
    cp_breakdown = context_pressure.get("breakdown", {})
    skills_bd = cp_breakdown.get("skills", {})
    mcp_bd = cp_breakdown.get("mcp", {})
    agents_bd = cp_breakdown.get("agents", {})
    total_tokens = context_pressure.get("total_injection_tokens", 0)
    window = context_pressure.get("context_window_assumed", 200000)
    pressure_pct = context_pressure.get("pressure_percent", 0)
    pressure_grade = context_pressure.get("grade", "")

    lines.extend(["", "## 上下文压力（estimated，非实际注入量）", "| 来源 | 工具数 | 估算 token | 占假定窗口 |", "| --- | ---: | ---: | ---: |"])
    lines.insert(len(lines) - 2, "")

    sk_count = skills_bd.get("count", 0)
    sk_tokens = skills_bd.get("total_tokens", 0)
    sk_pct = round(sk_tokens / window * 100, 2) if window else 0
    lines.append(f"| Skills | {sk_count} | {sk_tokens} | {sk_pct}% |")

    mcp_count = mcp_bd.get("count", 0)
    mcp_tokens = mcp_bd.get("total_tokens", 0)
    mcp_pct = round(mcp_tokens / window * 100, 2) if window else 0
    lines.append(f"| MCP schemas | {mcp_count} | {mcp_tokens} | {mcp_pct}% |")

    agents_status = agents_bd.get("status", "unavailable")
    ag_count = agents_bd.get("count", 0)
    ag_tokens = agents_bd.get("total_tokens", 0)
    ag_pct = round(ag_tokens / window * 100, 2) if window else 0
    status_tag = f" [{agents_status}]" if agents_status != "observed" else ""
    lines.append(f"| Agent profiles | {ag_count} | {ag_tokens} | {ag_pct}%{status_tag} |")

    total_pct = round(total_tokens / window * 100, 2) if window else 0
    pemoji = pressure_emoji(pressure_grade)
    lines.append(f"| 合计 | - | {total_tokens} | {total_pct}% |")
    lines.append(f"等级: {pemoji} [{pressure_grade}]")
    lines.append(f"估算边界: Skills 仅取 {sources.get('user_skills', '指定用户目录')} 的一级技能，不含全部插件/系统技能；窗口假设 {window:,} tokens；MCP 缺少 schema 时按每服务 10 工具×300 tokens。不能据此决定卸载。")

    # == 配置优化总览 ==
    opt_summary = optimization.get("summary", {})
    keep_n = opt_summary.get("keep", 0)
    watch_n = opt_summary.get("watch", 0)
    hide_n = opt_summary.get("hide", 0)
    uninstall_n = opt_summary.get("uninstall_candidates", 0)

    lines.extend(["", "## 配置优化总览", "", "| 层级 | 数量 | 说明 |", "| --- | ---: | --- |",
                  f"| 保留 (value>=7) | {keep_n} | 高频高匹配 |",
                  f"| 观察 (4-7) | {watch_n} | 30 天复查 |",
                  f"| 隐藏 (2-4) | {hide_n} | 命令栏隐藏 |",
                  f"| 卸载候选 (<2) | {uninstall_n} | 需完整证据及依赖检查 |",
                  f"| 证据不足 | {opt_summary.get('pending_evidence', 0)} | 补采集，暂不变更 |",
                  f"证据覆盖: {format_coverage(opt_summary.get('evidence_coverage', {}))}",
                  f"使用信号: {report.get('signals_status', 'unavailable')}"])

    # == 高价值工具（Top 5）==
    skill_recs = optimization.get("skill_recommendations", [])
    mcp_recs = optimization.get("mcp_recommendations", [])
    all_recs = sorted(
        skill_recs + mcp_recs,
        key=lambda x: x.get("value_score") if x.get("value_score") is not None else -1,
        reverse=True,
    )
    top5 = [r for r in all_recs if r.get("value_score") is not None][:5]
    if top5:
        lines.extend(["", "## 高价值工具（Top 5）", "| 对象 | 类型 | value | 层级 | 证据 |", "| --- | --- | ---: | --- | --- |"])
        for rec in top5:
            target = rec.get("target", "?")
            rtype = rec.get("type", "?")
            vs = rec.get("value_score", 0)
            layer = rec.get("layer", "?")
            evidence_rec = rec.get("evidence", {})
            ev_parts = []
            if evidence_rec.get("has_local_evidence"):
                ev_parts.append(f"调用 {evidence_rec.get('usage_count', 0)} 次")
            if evidence_rec.get("market_evidence") and "unavailable" not in str(evidence_rec.get("market_evidence", "")):
                ev_parts.append("有市场证据")
            ev_str = "; ".join(ev_parts) if ev_parts else "证据不足"
            lines.append(f"| {target} | {rtype} | {vs} | {layer} | {ev_str} |")

    # == 待卸载/隐藏候选 ==
    hide_cands = [
        r for r in all_recs
        if r.get("layer") in ("hide", "hide_review", "uninstall_candidate")
    ]
    if hide_cands:
        lines.extend(["", "## 待卸载/隐藏候选", "| 对象 | 类型 | value | 使用 | 匹配 | 建议 |", "| --- | --- | ---: | ---: | ---: | --- |"])
        for r in hide_cands:
            target = r.get("target", "?")
            rtype = r.get("type", "?")
            vs = r.get("value_score", 0)
            bd = r.get("breakdown", {})
            usage_norm = bd.get("usage", 0)
            alignment = bd.get("alignment", 0)
            layer = r.get("layer", "?")
            suggestion = "uninstall_candidate" if layer == "uninstall_candidate" else "hide"
            lines.append(f"| {target} | {rtype} | {vs} | {usage_norm} | {alignment} | {suggestion} |")

    # == 数据缺口 ==
    data_gaps = opt_summary.get("data_gaps", [])
    if data_gaps:
        lines.extend(["", "数据缺口:"])
        for gap in data_gaps:
            lines.append(f"- {gap}")

    # == 下一步 ==
    mcp_unhealthy = sum(1 for m in mcp_health if m.get("grade") in ("needs_attention", "unhealthy"))
    lines.extend(["", "下一步:", ""])
    if sl_crit or sl_warn:
        lines.append(f"- 优先复核 {sl_crit + sl_warn} 项技能/插件来源问题，按上方建议逐项验证。")
    if mcp_unhealthy:
        lines.append(f"- 复核 {mcp_unhealthy} 个 MCP 的具体失败维度。")
    if critical_count + warning_count:
        lines.append(f"- 复核 {critical_count + warning_count} 个 Agent 重叠候选，不把频次差异直接解释为误派。")
    if opt_summary.get('pending_evidence'):
        lines.append("- 按当前需求选择优先目标补证；需要市场比较时，经授权仅选 2–3 个同类项目，不全量联网补分。")
    if not report.get("actions"):
        lines.append("- 暂无有证据支持的变更；运行与 UI 项目仍需单独验收。")

    return "\n".join(lines) + render_footer(report)


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    parser = argparse.ArgumentParser(description="Audit local skill/plugin issues without writing files.")
    parser.add_argument("--root", type=Path, default=Path(__import__("os").environ.get("CODEX_HOME", Path.home() / ".codex")))
    parser.add_argument("--catalog-dir", type=Path)
    parser.add_argument("--runtime-dir", type=Path, default=Path.home() / ".cache" / "codex-runtimes")
    parser.add_argument("--staging-dir", type=Path)
    parser.add_argument("--user-skill-dir", type=Path, default=Path.home() / ".agents" / "skills")
    parser.add_argument("--profile", type=Path, default=None, help="用户画像文件；缺失时 profile_alignment=unavailable。")
    parser.add_argument("--zcode-config", type=Path, default=Path.home() / ".zcode" / "cli" / "config.json", help="ZCode 配置文件路径（仅 ecosystem 模式使用）。")
    parser.add_argument("--agents-dir", type=Path, default=Path.home() / ".zcode" / "cli" / "agents", help="ZCode agent profile 目录（仅 ecosystem 模式使用）。")
    parser.add_argument("--signals-path", type=Path, default=None, help="extract_usage_signals.py 输出的信号 JSON 路径（仅 ecosystem 模式使用）。")
    parser.add_argument("--market-path", type=Path, help="带来源、日期与评分依据的市场证据 JSON；不自动联网。")
    parser.add_argument("--baseline", type=Path, help="上次 --json 报告；未提供或失效则全景扫描。")
    parser.add_argument("--scan-mode", choices=("auto", "full", "incremental"), default="auto")
    parser.add_argument("--output", type=Path, help="明确导出到新文件；默认只输出报告，不保存基线。")
    parser.add_argument("--reasonix-dir", type=Path, default=Path.home() / "AppData/Local/Reasonix/mcp", help="Reasonix MCP 配置目录（仅 ecosystem 模式使用，用于真实 tool_count）。")
    parser.add_argument("--scope", choices=("installed", "visible", "all", "ecosystem"), default="installed")
    parser.add_argument("--visible-id", action="append", default=[])
    parser.add_argument("--fail-on", choices=("none", "info", "warning", "critical"), default="none")
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--detail", action="store_true", help="人类可读输出中包含每项安装资产；默认只显示来源组和行动候选。")
    args = parser.parse_args()
    baseline = None
    if args.baseline:
        try:
            previous = json.loads(args.baseline.read_text(encoding="utf-8-sig"))
            baseline = previous.get("baseline", previous) if isinstance(previous, dict) else {"invalid": True}
        except (OSError, ValueError):
            baseline = {"invalid": True}
    market = {}
    if args.market_path:
        try:
            market = json.loads(args.market_path.read_text(encoding="utf-8-sig"))
            if not isinstance(market, dict) or any(not isinstance(v, dict) for v in market.values()):
                parser.error("--market-path 必须是以 skill:<id>/mcp:<server> 为键的证据对象")
        except (OSError, ValueError) as exc:
            parser.error(f"市场证据无法读取: {exc}")

    def emit(report, renderer):
        output = json.dumps(report, ensure_ascii=False, indent=2) if args.as_json else renderer(report, args.detail)
        if args.output:
            # Export is explicit and cannot overwrite source files or prior reports.
            try:
                with args.output.open("x", encoding="utf-8") as stream:
                    stream.write(output + "\n")
            except OSError as exc:
                parser.error(f"导出失败（不覆盖已有文件）: {exc}")
        else:
            print(output)

    # ecosystem scope: 生态评估，不走标准 audit 流程
    if args.scope == "ecosystem":
        catalog_dir = args.catalog_dir or args.root / "cache" / "remote_plugin_catalog"
        staging_dir = args.staging_dir or args.root / ".tmp" / "bundled-marketplaces"
        report = audit_ecosystem(
            args.user_skill_dir,
            args.zcode_config,
            args.agents_dir,
            args.signals_path,
            args.profile,
            root=args.root,
            catalog_dir=catalog_dir,
            runtime_dir=args.runtime_dir,
            staging_dir=staging_dir if staging_dir.exists() else None,
            reasonix_dir=args.reasonix_dir,
            capabilities_yaml=(Path(__file__).resolve().parent.parent / "references" / "capability-dimensions.yaml"),
            market_evidence=market, baseline=baseline, scan_mode=args.scan_mode,
        )
        emit(report, render_ecosystem_report)
        severity = {"none": 0, "info": 1, "warning": 2, "critical": 3}
        findings = report["ecosystem_assessment"].get("skill_layer", {}).get("issues", [])
        return int(args.fail_on != "none" and any(severity[i["severity"]] >= severity[args.fail_on] for i in findings))

    catalog_dir = args.catalog_dir or args.root / "cache" / "remote_plugin_catalog"
    staging_dir = args.staging_dir or args.root / ".tmp" / "bundled-marketplaces"
    report, _ = audit(
        args.root,
        catalog_dir,
        args.runtime_dir,
        staging_dir if staging_dir.exists() else None,
        args.user_skill_dir,
        args.scope,
        args.visible_id,
        args.profile,
        baseline=baseline, scan_mode=args.scan_mode,
    )
    emit(report, render_human_report)
    order = {"info": 1, "warning": 2, "critical": 3, "none": 0}
    if args.fail_on != "none" and any(order[entry["severity"]] >= order[args.fail_on] for entry in report["issues"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
