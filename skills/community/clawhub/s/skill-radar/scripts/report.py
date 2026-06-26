"""
report.py — 智能推荐 + 完整报告生成

包含基于历史对话的智能推荐（含 ClawHub 实时搜索 + 安全扫描）
和完整报告的执行摘要生成。
"""

import json
from pathlib import Path
from datetime import datetime

from utils import (
    HOME, MEMORY_MD, HEARTBEAT_MD, AGENTS_MD,
    RECOMMENDATION_RULES,
    find_skill_dirs, parse_skill_md, read_file_safe,
    build_skill_keywords, count_keyword_hits,
)
from scanner import search_clawhub, security_scan_skill
from usage_analyzer import load_mem0_memories, load_daily_memories, load_session_logs
from checks import parse_skills_list, parse_clawhub_list, inspect_clawhub_version


# ─── 智能推荐 ───────────────────────────────────────────────────────────────

def _parse_user_messages_from_sessions(session_files):
    """从 session 日志中提取用户消息（过滤系统消息）"""
    all_user_messages = []
    for sf in session_files:
        try:
            content = sf.read_text(encoding="utf-8", errors="replace")
            for line in content.strip().split("\n"):
                if not line.strip():
                    continue
                try:
                    obj = json.loads(line)
                    if obj.get("type") == "message":
                        msg = obj.get("message", {})
                        if msg.get("role") == "user":
                            raw = msg.get("content", "")
                            if isinstance(raw, list):
                                texts = []
                                for item in raw:
                                    if isinstance(item, dict) and item.get("type") == "text":
                                        texts.append(item.get("text", ""))
                                    elif isinstance(item, str):
                                        texts.append(item)
                                raw = "\n".join(texts)
                            if isinstance(raw, str) and len(raw) > 10:
                                actual_lines = []
                                in_metadata = False
                                skip_block = False
                                in_code_block = False
                                for ln in raw.split("\n"):
                                    ln_stripped = ln.strip()
                                    if ln_stripped.startswith("```"):
                                        in_code_block = not in_code_block
                                        continue
                                    if in_code_block:
                                        continue
                                    if ln_stripped.startswith("[") and any(kw in ln_stripped.lower() for kw in [
                                        "metadata", "cron:", "subagent", "system:", "inter-session",
                                        "queued message", "internal task", "heartbeat", "current time:"
                                    ]):
                                        in_metadata = True
                                        continue
                                    if ln_stripped.startswith("{") and "schema" in ln_stripped:
                                        in_metadata = True
                                        continue
                                    if in_metadata and ln_stripped == "]":
                                        in_metadata = False
                                        continue
                                    if "subagent task is ready" in ln_stripped.lower() or \
                                       "convert the result above" in ln_stripped.lower() or \
                                       "return your summary as plain text" in ln_stripped.lower():
                                        skip_block = True
                                        continue
                                    if not in_metadata and ln_stripped and not skip_block:
                                        actual_lines.append(ln)
                                actual_text = "\n".join(actual_lines).strip()
                                if len(actual_text) > 5:
                                    all_user_messages.append(actual_text)
                except (json.JSONDecodeError, KeyError):
                    pass
        except Exception:
            pass
    return all_user_messages


def _collect_user_context(session_files):
    """收集用户消息 + 工作空间配置"""
    all_user_messages = _parse_user_messages_from_sessions(session_files)

    workspace_files = [
        HOME / ".openclaw/workspace/MEMORY.md",
        HOME / ".openclaw/workspace/USER.md",
        HOME / ".openclaw/workspace/HEARTBEAT.md",
    ]
    for wf in workspace_files:
        if wf.is_file():
            try:
                text = wf.read_text(encoding="utf-8", errors="replace")
                if len(text) > 10:
                    all_user_messages.append(f"[config] {text}")
            except Exception:
                pass

    return all_user_messages


def _get_installed_skills():
    """获取已安装 Skill 名称集合"""
    installed = set()
    for source, path in find_skill_dirs():
        info = parse_skill_md(path / "SKILL.md")
        if info.get("name"):
            installed.add(info["name"].lower())
    return installed


def check_recommend() -> str:
    """基于历史对话分析需求缺口，推荐 Skill"""
    lines = []
    lines.append("# 💡 智能推荐")
    lines.append("")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    sessions_dir = HOME / ".openclaw/agents/main/sessions"
    if not sessions_dir.is_dir():
        lines.append("⚠️ 未找到 session 日志目录，无法分析。")
        return "\n".join(lines)

    session_files = sorted(sessions_dir.glob("*.jsonl"), reverse=True)
    if not session_files:
        lines.append("⚠️ 未找到 session 日志文件。")
        return "\n".join(lines)

    all_user_messages = _collect_user_context(session_files)

    if not all_user_messages:
        lines.append("⚠️ 未找到用户对话记录。")
        return "\n".join(lines)

    lines.append(f"📊 分析了 **{len(all_user_messages)}** 条历史对话记录")
    lines.append(f"📁 扫描了 **{len(session_files)}** 个 session 文件")
    lines.append("")

    all_text = "\n".join(all_user_messages).lower()
    installed_skills = _get_installed_skills()

    matched = []
    for rule in RECOMMENDATION_RULES:
        hits = [kw for kw in rule["keywords"] if kw.lower() in all_text]
        if hits:
            query = rule.get("search_query", rule["keywords"][0])
            clawhub_skills = search_clawhub(query, limit=3)
            recommended = []
            for sk in clawhub_skills:
                if sk["name"].lower() not in installed_skills:
                    recommended.append(sk)

            matched.append({
                "scene": rule["scene"],
                "hit_keywords": hits,
                "hit_count": sum(all_text.count(kw.lower()) for kw in hits),
                "recommended": recommended,
            })

    matched.sort(key=lambda x: x["hit_count"], reverse=True)

    if not matched:
        lines.append("🎉 你的 Skill 覆盖度很好，暂未发现明显缺口！")
        lines.append("")
        lines.append("> 💡 提示：推荐结果基于历史对话关键词分析，随着使用场景增多会越来越精准。")
        return "\n".join(lines)

    lines.append("## 🔥 高优先级推荐（频繁出现的需求）")
    lines.append("")

    # 安全扫描
    lines.append("🔒 正在对推荐 Skill 进行安全扫描...")
    lines.append("")

    all_recommended_skills = []
    for m in matched:
        for sk in m["recommended"][:3]:
            if sk["name"].lower() not in {s["name"] for s in all_recommended_skills}:
                all_recommended_skills.append(sk)

    security_results = {}
    for sk in all_recommended_skills:
        sec = security_scan_skill(sk["name"])
        security_results[sk["name"].lower()] = sec

    safe_count = sum(1 for s in security_results.values() if s["risk"] == "safe")
    warn_count = sum(1 for s in security_results.values() if s["risk"] == "warning")
    danger_count = sum(1 for s in security_results.values() if s["risk"] == "danger")
    meta_count = sum(1 for s in security_results.values() if s.get("files_checked", 0) == 0 and s.get("meta"))

    lines.append(f"扫描结果：🟢 安全 {safe_count} | 🟡 注意 {warn_count} | 🔴 高风险 {danger_count} | 📋 元数据检查 {meta_count}")
    lines.append("")

    high_priority = [m for m in matched if m["hit_count"] >= 5]
    if high_priority:
        for m in high_priority:
            lines.append(f"### {m['scene']}")
            lines.append(f"- 📈 需求频率：**{m['hit_count']}** 次提及")
            lines.append(f"- 🔑 触发关键词：{', '.join(f'`{k}`' for k in m['hit_keywords'][:8])}")
            if m["recommended"]:
                safe_recs = []
                for sk in m["recommended"][:5]:
                    sec = security_results.get(sk["name"].lower(), {})
                    if sec.get("risk") == "danger":
                        continue
                    safe_recs.append((sk, sec))
                if safe_recs:
                    lines.append("- 💡 推荐安装（来自 ClawHub 实时搜索，已通过安全检查）：")
                    for sk, sec in safe_recs[:3]:
                        is_code_scan = sec.get("files_checked", 0) > 0
                        if sec.get("risk") == "safe":
                            risk_icon = "🟢" if is_code_scan else "📋"
                        elif sec.get("risk") == "warning":
                            risk_icon = "🟡"
                        else:
                            risk_icon = "📋"
                        desc_suffix = ""
                        if sec.get("risk") == "warning" and sec.get("yellow_flags"):
                            top_flag = sec["yellow_flags"][0]["rule"]
                            desc_suffix = f" *⚠️ {top_flag}*"
                        elif not is_code_scan and sec.get("meta"):
                            author = sec["meta"].get("author", "未知")
                            desc_suffix = f" — 作者: {author}"
                        lines.append(f"  - {risk_icon} [`{sk['name']}`](https://clawhub.com/skills/{sk['name']}) — {sk['description']}{desc_suffix}")
                else:
                    lines.append("- ⛔ 所有搜索到的 Skill 均未通过安全检查，建议手动搜索替代品")
            else:
                lines.append("- ✅ 相关 Skill 已安装，无需额外推荐")
            lines.append("")
    else:
        lines.append("*暂无高频需求*")
        lines.append("")

    lines.append("## 📋 其他发现的潜在需求")
    lines.append("")

    low_priority = [m for m in matched if m["hit_count"] < 5]
    if low_priority:
        for m in low_priority:
            lines.append(f"### {m['scene']}")
            lines.append(f"- 📈 需求频率：**{m['hit_count']}** 次提及")
            lines.append(f"- 🔑 触发关键词：{', '.join(f'`{k}`' for k in m['hit_keywords'][:5])}")
            if m["recommended"]:
                safe_recs = []
                for sk in m["recommended"][:5]:
                    sec = security_results.get(sk["name"].lower(), {})
                    if sec.get("risk") == "danger":
                        continue
                    safe_recs.append((sk, sec))
                if safe_recs:
                    lines.append("- 💡 推荐安装：")
                    for sk, sec in safe_recs[:3]:
                        risk_icon = "🟢" if sec.get("risk") == "safe" else "🟡" if sec.get("risk") == "warning" else "⚪"
                        lines.append(f"  - {risk_icon} [`{sk['name']}`](https://clawhub.com/skills/{sk['name']}) — {sk['description']}")
                else:
                    lines.append("- ⛔ 未通过安全检查")
            else:
                lines.append("- ✅ 相关 Skill 已安装")
            lines.append("")
    else:
        lines.append("*暂无*")
        lines.append("")

    if danger_count > 0:
        lines.append("## ⛔ 被安全扫描拦截的 Skill")
        lines.append("")
        lines.append("以下 Skill 存在安全风险，已自动从推荐中移除：")
        lines.append("")
        for sk in all_recommended_skills:
            sec = security_results.get(sk["name"].lower(), {})
            if sec.get("risk") == "danger":
                lines.append(f"- `{sk['name']}` — {sk['description']}")
                for flag in sec.get("red_flags", []):
                    lines.append(f"  - 🚨 {flag['rule']}")
                lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("> 💡 **说明**：")
    lines.append("> - 推荐基于历史对话关键词分析 + ClawHub 实时搜索 + 安全扫描")
    lines.append("> - 🔒 安全扫描基于 skill-vetter 协议：已安装Skill做代码级检查（🟢），未安装Skill做元数据检查（📋）")
    lines.append("> - 🟡 需注意（有黄旗） / 🔴 高风险（已拦截）")
    lines.append("> - 安装后自动升级为代码级安全扫描（缓存7天）")
    lines.append("> - 高危 Skill 已自动从推荐列表移除，建议安装前再做人工审查")

    return "\n".join(lines)


# ─── 完整报告 ───────────────────────────────────────────────────────────────

def generate_summary() -> str:
    """生成执行摘要，汇总所有检查的关键发现"""
    lines = []
    lines.append("# 📡 Skill Radar — 执行摘要")
    lines.append("")
    lines.append(f"> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # ── 1. 状态概览 ──
    skills = parse_skills_list()
    if not skills:
        lines.append("⚠️ 无法获取 Skill 列表。")
        return "\n".join(lines)

    ready = [s for s in skills if s["status"] == "ready"]
    missing = [s for s in skills if s["status"] == "missing"]
    total = len(skills)

    lines.append("## 📊 一、整体状况")
    lines.append("")
    lines.append(f"共 **{total}** 个 Skill，其中 **{len(ready)}** 个就绪，**{len(missing)}** 个缺失。")
    lines.append("")

    # ── 2. 使用评估摘要 ──
    all_skills = []
    for source, path in find_skill_dirs():
        info = parse_skill_md(path / "SKILL.md")
        if info.get("name"):
            info["source"] = source
            all_skills.append(info)

    data_sources = [
        ("Mem0", load_mem0_memories()),
        ("每日记忆", load_daily_memories()),
        ("MEMORY.md", read_file_safe(MEMORY_MD)),
        ("HEARTBEAT.md", read_file_safe(HEARTBEAT_MD)),
        ("Session", load_session_logs()),
        ("AGENTS.md", read_file_safe(AGENTS_MD)),
    ]

    rating_counts = {"high": 0, "medium": 0, "low": 0, "unused": 0}
    for skill in all_skills:
        keywords = build_skill_keywords(skill)

        total_name_hits = 0
        sources_with_name = 0
        sources_with_any = 0
        total_keyword_hits = 0

        memory_name = 0
        heartbeat_name = 0
        other_name_sources = 0

        for src_name, src_text in data_sources:
            if not src_text:
                continue
            hits = count_keyword_hits(src_text, keywords)
            if hits["total"] > 0:
                sources_with_any += 1
                total_name_hits += hits["name_hits"]
                total_keyword_hits += hits["keyword_hits"]
                if hits["name_hits"] > 0:
                    sources_with_name += 1
                if src_name == "MEMORY.md":
                    memory_name = hits["name_hits"]
                elif src_name == "HEARTBEAT.md":
                    heartbeat_name = hits["name_hits"]
                elif src_name in ["Session", "每日记忆", "Mem0", "AGENTS.md"]:
                    if hits["name_hits"] > 0:
                        other_name_sources += 1

        in_core_config = (
            (memory_name >= 1 and heartbeat_name >= 1) or
            (memory_name >= 1 and other_name_sources >= 1) or
            (heartbeat_name >= 1 and other_name_sources >= 1)
        )

        if total_name_hits == 0:
            rating = "low" if sources_with_any >= 1 else "unused"
        elif in_core_config or total_name_hits >= 5 or sources_with_name >= 3 or (total_name_hits >= 2 and sources_with_name >= 2):
            rating = "high"
        elif total_name_hits >= 2 or sources_with_name >= 2 or (total_name_hits >= 1 and total_keyword_hits >= 3):
            rating = "medium"
        else:
            rating = "low"

        rating_counts[rating] += 1

    lines.append("## 📊 二、使用评估")
    lines.append("")
    total_rated = sum(rating_counts.values())
    lines.append(f"在 **{total_rated}** 个可评估的 Skill 中：")
    lines.append("")
    lines.append("| 评分 | 数量 | 占比 | 说明 |")
    lines.append("|------|------|------|------|")
    for rating, label, desc in [
        ("high", "🔵 高频", "核心工具，频繁使用"),
        ("medium", "🟢 中频", "经常使用"),
        ("low", "🟡 低频", "偶尔使用"),
        ("unused", "🔴 未使用", "从未被提及"),
    ]:
        count = rating_counts.get(rating, 0)
        pct = f"{count / total_rated * 100:.0f}%" if total_rated > 0 else "0%"
        lines.append(f"| {label} | {count} | {pct} | {desc} |")
    lines.append("")

    active_count = rating_counts["high"] + rating_counts["medium"]
    health_pct = active_count / total_rated * 100 if total_rated > 0 else 0
    if health_pct >= 60:
        health_emoji, health_label = "✅", "健康"
    elif health_pct >= 40:
        health_emoji, health_label = "⚠️", "一般"
    else:
        health_emoji, health_label = "🔴", "需优化"

    lines.append(f"**活跃率**：{active_count}/{total_rated}（{health_pct:.0f}%）{health_emoji} — 状态：**{health_label}**")
    lines.append("")

    # ── 3. 版本检查摘要 ──
    local_versions = parse_clawhub_list()
    needs_update_count = 0
    if local_versions:
        lines.append("## 🔄 三、版本状态")
        lines.append("")
        checked = 0
        for name in list(local_versions.keys())[:10]:
            remote = inspect_clawhub_version(name)
            checked += 1
            if remote and remote != local_versions[name]:
                needs_update_count += 1

        if checked > 0:
            estimated = int(needs_update_count / checked * len(local_versions))
            if needs_update_count > 0:
                lines.append(f"抽样检查 **{checked}** 个 Skill，发现 **{needs_update_count}** 个需要更新。")
                lines.append(f"预估 **{len(local_versions)}** 个 ClawHub Skill 中约有 **{estimated}** 个待更新。")
            else:
                lines.append(f"抽样检查 **{checked}** 个 Skill，均为最新版本。")
        lines.append("")

    # ── 4. 智能推荐摘要 ──
    sessions_dir = HOME / ".openclaw/agents/main/sessions"
    session_files = sorted(sessions_dir.glob("*.jsonl"), reverse=True) if sessions_dir.is_dir() else []

    all_user_messages = _collect_user_context(session_files)
    all_text = "\n".join(all_user_messages).lower()
    installed_skill_names = {s["name"].lower() for s in all_skills}

    recommend_matched = []
    for rule in RECOMMENDATION_RULES:
        hits = [kw for kw in rule["keywords"] if kw.lower() in all_text]
        if hits:
            hit_count = sum(all_text.count(kw.lower()) for kw in hits)
            query = rule.get("search_query", rule["keywords"][0])
            clawhub_skills = search_clawhub(query, limit=3)
            recommended = [sk for sk in clawhub_skills if sk["name"].lower() not in installed_skill_names]
            recommend_matched.append({
                "scene": rule["scene"],
                "hit_count": hit_count,
                "recommended": recommended,
            })
    recommend_matched.sort(key=lambda x: x["hit_count"], reverse=True)

    if recommend_matched:
        lines.append("## 💡 四、智能推荐")
        lines.append("")
        lines.append(f"基于 {len(all_user_messages)} 条历史记录 + 工作空间配置 + ClawHub 实时搜索，发现以下需求缺口：")
        lines.append("")

        high_rec = [m for m in recommend_matched if m["hit_count"] >= 5]
        low_rec = [m for m in recommend_matched if m["hit_count"] < 5]

        if high_rec:
            lines.append("**🔥 高优先级（频繁需求）：**")
            lines.append("")
            for m in high_rec:
                lines.append(f"- {m['scene']} — 提及 **{m['hit_count']}** 次")
                if m["recommended"]:
                    for sk in m["recommended"][:2]:
                        lines.append(f"  - 📦 `{sk['name']}` — {sk['description']}")
                else:
                    lines.append(f"  - ✅ 相关 Skill 已安装")
                lines.append("")

        if low_rec:
            lines.append("**📋 潜在需求：**")
            lines.append("")
            for m in low_rec:
                lines.append(f"- {m['scene']} — 提及 **{m['hit_count']}** 次")
                if m["recommended"]:
                    for sk in m["recommended"][:2]:
                        lines.append(f"  - 📦 `{sk['name']}` — {sk['description']}")
            lines.append("")
    else:
        lines.append("## 💡 四、智能推荐")
        lines.append("")
        lines.append("🎉 你的 Skill 覆盖度很好，暂未发现明显缺口！")
        lines.append("")

    # ── 5. 关键发现 & 行动建议 ──
    lines.append("## 🎯 五、关键发现与建议")
    lines.append("")

    suggestions = []

    if health_pct < 40:
        suggestions.append((
            "🧹 **清理闲置 Skill**",
            f"活跃率仅 {health_pct:.0f}%，有 {rating_counts['unused']} 个 Skill 从未使用、{rating_counts['low']} 个低频使用。"
            f"建议评估是否卸载，减少 token 消耗和认知负担。"
        ))
    elif rating_counts["unused"] > 5:
        suggestions.append((
            "🧹 **关注未使用 Skill**",
            f"有 {rating_counts['unused']} 个 Skill 在所有数据源中均未被提及，建议逐一评估是否需要保留。"
        ))

    if needs_update_count > 0:
        suggestions.append((
            "🔄 **更新过期 Skill**",
            f"部分 Skill 版本落后，建议运行 `npx clawhub sync` 一键更新。"
        ))

    if len(missing) > 20:
        bundled_missing = [s for s in missing if s["source"] == "openclaw-bundled"]
        if bundled_missing:
            suggestions.append((
                "📦 **清理 Bundled Missing**",
                f"有 {len(bundled_missing)} 个自带 Skill 处于 missing 状态（依赖未安装），"
                f"建议更新 OpenClaw 或确认不需要。"
            ))

    if health_pct >= 60:
        suggestions.append((
            "✅ **Skill 生态健康**",
            f"活跃率 {health_pct:.0f}%，大部分 Skill 都在被有效使用。继续保持！"
        ))

    if not suggestions:
        suggestions.append((
            "✅ **一切正常**",
            "未发现明显问题，你的 Skill 生态管理得不错！"
        ))

    for title, desc in suggestions:
        lines.append(f"### {title}")
        lines.append("")
        lines.append(desc)
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("> 📋 以下为各项检查的详细报告，如需深入了解请继续阅读。")
    lines.append("")

    return "\n".join(lines)
