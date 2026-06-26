"""
usage_analyzer.py — 使用价值评估（6大数据源）

从 Mem0 记忆、每日记忆、MEMORY.md、HEARTBEAT.md、Session 日志、AGENTS.md
六个数据源收集证据，评估每个已安装 Skill 的实际使用情况。
"""

import subprocess
import json
from pathlib import Path
from collections import defaultdict
from datetime import datetime

from utils import (
    HOME, SKILL_PATHS, GENERIC_KEYWORDS,
    MEMORY_MD, HEARTBEAT_MD, AGENTS_MD, MEMORY_DIR, SESSIONS_DIR,
    run_cmd, find_skill_dirs, parse_skill_md, build_skill_keywords,
    read_file_safe, count_keyword_hits,
)


def load_mem0_memories() -> str:
    """加载 Mem0 记忆数据（可选依赖，缺失时返回空）"""
    # 方法1：通过 list.py 脚本
    mem0_script = HOME / ".openclaw/skills/mem0/list.py"
    if mem0_script.is_file():
        try:
            result = subprocess.run(
                ["python3", str(mem0_script)],
                capture_output=True, text=True, timeout=15
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout
        except Exception:
            pass

    # 方法2：直接查找数据文件
    mem0_dir = HOME / ".openclaw/skills/mem0"
    if mem0_dir.is_dir():
        for ext in ("*.json", "*.db", "*.sqlite"):
            for f in mem0_dir.glob(ext):
                if f.name in ("package.json", "README.md"):
                    continue
                content = read_file_safe(f)
                if content:
                    return content

    return ""


def load_daily_memories() -> str:
    """加载每日记忆文件"""
    if not MEMORY_DIR.is_dir():
        return ""

    texts = []
    for md_file in sorted(MEMORY_DIR.glob("*.md")):
        content = read_file_safe(md_file)
        if content:
            texts.append(content)

    return "\n".join(texts)


def load_session_logs() -> str:
    """
    加载 Session 日志中用户消息的纯文本。
    严格过滤系统消息、元数据、子代理消息。
    """
    if not SESSIONS_DIR.is_dir():
        return ""

    user_texts = []

    for session_file in sorted(SESSIONS_DIR.glob("*.jsonl")):
        try:
            content = session_file.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for line in content.strip().split("\n"):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except (json.JSONDecodeError, ValueError):
                continue

            if obj.get("type") != "message":
                continue

            msg = obj.get("message", {})
            if msg.get("role") != "user":
                continue

            raw = msg.get("content", "")

            # content 可能是 list（OpenClaw 格式）
            if isinstance(raw, list):
                texts = []
                for item in raw:
                    if isinstance(item, dict) and item.get("type") == "text":
                        texts.append(item.get("text", ""))
                    elif isinstance(item, str):
                        texts.append(item)
                raw = "\n".join(texts)

            if not isinstance(raw, str) or len(raw) <= 10:
                continue

            # 过滤系统消息和元数据
            filtered_lines = []
            in_metadata = False
            in_code_block = False

            for ln in raw.split("\n"):
                ln_stripped = ln.strip()

                # 跳过代码块
                if ln_stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                # 跳过元数据块
                if ln_stripped.startswith("[") and any(kw in ln_stripped.lower() for kw in [
                    "metadata", "cron:", "subagent", "system:", "inter-session",
                    "queued message", "internal task", "heartbeat",
                    "current time:", "subagent context",
                ]):
                    in_metadata = True
                    continue
                if in_metadata and ln_stripped == "]":
                    in_metadata = False
                    continue

                # 跳过 JSON schema 行
                if ln_stripped.startswith("{") and "schema" in ln_stripped:
                    continue

                # 跳过已知系统消息
                if any(kw in ln_stripped.lower() for kw in [
                    "subagent task is ready",
                    "convert the result above",
                    "return your summary as plain text",
                    "you are a subagent",
                    "your final response should include",
                    "complete this task",
                    "do not initiate",
                    "no user conversations",
                    "no heartbeats",
                ]):
                    continue

                if not in_metadata and ln_stripped:
                    filtered_lines.append(ln)

            filtered_text = "\n".join(filtered_lines).strip()
            if len(filtered_text) > 5:
                user_texts.append(filtered_text)

    return "\n".join(user_texts)


def check_usage() -> str:
    """
    评估每个已安装 Skill 的使用情况。
    从多个数据源收集证据，给出使用评分。
    """
    lines = []
    lines.append("# 📊 Skill 使用价值评估")
    lines.append(f"\n> 生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append("")

    # ── 收集所有 Skill ──
    all_skills = []
    for source, skill_dir in find_skill_dirs():
        skill_md = skill_dir / "SKILL.md"
        info = parse_skill_md(skill_md)
        info["source"] = source
        all_skills.append(info)

    if not all_skills:
        lines.append("⚠️ 未找到任何已安装的 Skill。")
        return "\n".join(lines)

    # ── 加载数据源 ──
    lines.append("## 数据源扫描")
    lines.append("")

    # 加载所有可选数据源
    data_source_configs = [
        ("Mem0 记忆", load_mem0_memories(), "向量记忆系统（可选）"),
        ("每日记忆", load_daily_memories(), "memory/*.md 日记"),
        ("MEMORY.md", read_file_safe(MEMORY_MD), "核心配置"),
        ("HEARTBEAT.md", read_file_safe(HEARTBEAT_MD), "定期任务"),
        ("Session 日志", load_session_logs(), "用户对话"),
        ("AGENTS.md", read_file_safe(AGENTS_MD), "工作规则"),
    ]

    for name, text, desc in data_source_configs:
        if text:
            lines.append(f"- ✅ {name}（{len(text)} 字符）")

    available_count = sum(1 for _, t, _ in data_source_configs if t)
    lines.append("")
    if available_count == 0:
        lines.append("⚠️ 未检测到任何数据源，评估结果可能不准确。")
        lines.append("")
    lines.append(f"共扫描 **{len(all_skills)}** 个 Skill。")
    lines.append("")

    # ── 构建关键词映射 & 统计命中 ──
    data_sources = [(name, text) for name, text, _ in data_source_configs]

    skill_usage = []  # list of dicts

    for skill in all_skills:
        name = skill["name"]
        keywords = build_skill_keywords(skill)

        # 在各数据源中搜索
        source_hits = {}  # source_name -> hit dict
        total_name_hits = 0       # 精确 name 匹配总数
        total_keyword_hits = 0    # description 关键词匹配总数
        sources_with_name = 0     # 有 name 精确匹配的数据源数
        sources_with_any = 0      # 有任何匹配的数据源数

        for src_name, src_text in data_sources:
            if not src_text:
                continue
            hits = count_keyword_hits(src_text, keywords)
            if hits["total"] > 0:
                source_hits[src_name] = hits
                total_name_hits += hits["name_hits"]
                total_keyword_hits += hits["keyword_hits"]
                sources_with_any += 1
                if hits["name_hits"] > 0:
                    sources_with_name += 1

        # ── 计算评分（严格模式）──
        # 核心原则：只有精确 name 匹配才算真正使用
        # description 关键词只作为辅助证据，不能单独提升评分
        #
        # 注意：MEMORY.md 的 Skill 索引表会列出几乎所有已安装 Skill，
        # 所以单独 MEMORY.md name 命中不能算"核心配置"，
        # 需要结合其他数据源的证据。

        # 核心配置 = name 在 MEMORY.md + 至少1个其他数据源中出现
        memory_name = source_hits.get("MEMORY.md", {}).get("name_hits", 0)
        heartbeat_name = source_hits.get("HEARTBEAT.md", {}).get("name_hits", 0)
        other_name_sources = 0
        for src_name in ["Session", "每日记忆", "Mem0", "AGENTS.md"]:
            if source_hits.get(src_name, {}).get("name_hits", 0) > 0:
                other_name_sources += 1

        in_core_config = False
        if (memory_name >= 1 and heartbeat_name >= 1) or \
           (memory_name >= 1 and other_name_sources >= 1) or \
           (heartbeat_name >= 1 and other_name_sources >= 1):
            in_core_config = True

        # 如果没有任何 name 精确匹配，最高只能到低频
        if total_name_hits == 0:
            if sources_with_any >= 3 and total_keyword_hits >= 5:
                rating = "low"       # 🟡 低频：仅关键词在多处出现
            elif sources_with_any >= 1:
                rating = "low"       # 🟡 低频：仅关键词偶尔出现
            else:
                rating = "unused"    # 🔴 未使用
        else:
            # 有 name 精确匹配
            if in_core_config or (total_name_hits >= 5) or \
               (sources_with_name >= 3) or \
               (total_name_hits >= 2 and sources_with_name >= 2):
                rating = "high"      # 🔵 高频
            elif (total_name_hits >= 2) or \
                 (sources_with_name >= 2) or \
                 (total_name_hits >= 1 and total_keyword_hits >= 3):
                rating = "medium"    # 🟢 中频
            else:
                rating = "low"       # 🟡 低频：name 仅出现1次

        # 构建证据摘要（优先显示 name 精确匹配）
        evidence_parts = []
        for src_name in ["MEMORY.md", "HEARTBEAT.md", "Session", "每日记忆", "Mem0", "AGENTS.md"]:
            if src_name in source_hits:
                hits = source_hits[src_name]
                if hits["name_hits"] > 0:
                    evidence_parts.append(f"{src_name}提及{hits['name_hits']}次")
                elif hits["keyword_hits"] > 0:
                    # 显示具体命中了哪些关键词（最多3个）
                    top_kws = sorted(hits["keyword_details"], key=lambda x: -x[1])[:3]
                    kw_str = ", ".join(f"`{kw}`" for kw, _ in top_kws)
                    evidence_parts.append(f"{src_name}({kw_str})")

        evidence = " + ".join(evidence_parts) if evidence_parts else "无命中"

        skill_usage.append({
            "name": name,
            "description": skill.get("description", ""),
            "source": skill["source"],
            "rating": rating,
            "sources_with_any": sources_with_any,
            "sources_with_name": sources_with_name,
            "total_name_hits": total_name_hits,
            "total_keyword_hits": total_keyword_hits,
            "total_hits": total_name_hits + total_keyword_hits,
            "evidence": evidence,
            "source_hits": source_hits,
        })

    # ── 评分统计 ──
    rating_counts = defaultdict(int)
    for su in skill_usage:
        rating_counts[su["rating"]] += 1

    total = len(skill_usage)
    lines.append("## 概览")
    lines.append("")
    lines.append("| 评分 | 数量 | 占比 |")
    lines.append("|------|------|------|")
    for rating, emoji_label in [("high", "🔵 高频"), ("medium", "🟢 中频"),
                                 ("low", "🟡 低频"), ("unused", "🔴 未使用")]:
        count = rating_counts.get(rating, 0)
        pct = f"{count / total * 100:.0f}%" if total > 0 else "0%"
        lines.append(f"| {emoji_label} | {count} | {pct} |")
    lines.append("")

    # ── 按评分分组输出 ──
    rating_order = ["high", "medium", "low", "unused"]
    rating_titles = {
        "high": "🔵 高频使用 (核心工具)",
        "medium": "🟢 中频使用",
        "low": "🟡 低频使用",
        "unused": "🔴 未使用",
    }

    for rating in rating_order:
        items = [su for su in skill_usage if su["rating"] == rating]
        if not items:
            continue

        # 按总命中数降序排列（name 精确匹配权重更高）
        items.sort(key=lambda x: (x["total_name_hits"] * 10 + x["total_keyword_hits"]), reverse=True)

        lines.append(f"## {rating_titles[rating]}")
        lines.append("")

        src_icons = {"bundled": "📦", "workspace": "🧩", "managed": "⚙️"}

        for item in items:
            icon = src_icons.get(item["source"], "📁")
            desc_short = item["description"][:80] if item["description"] else ""
            lines.append(f"- {icon} **`{item['name']}`** [{item['source']}]")
            if desc_short:
                lines.append(f"  - {desc_short}")
            lines.append(f"  - 📋 {item['evidence']}")
            lines.append("")

    # ── 清理建议 ──
    unused_items = [su for su in skill_usage if su["rating"] == "unused"]
    low_items = [su for su in skill_usage if su["rating"] == "low"]

    lines.append("## 💡 清理建议")
    lines.append("")

    if unused_items:
        lines.append(f"### 🔴 从未使用（{len(unused_items)} 个）")
        lines.append("")
        lines.append("以下 Skill 在所有数据源中均未被发现使用，建议评估是否保留：")
        lines.append("")
        for item in unused_items:
            icon = src_icons.get(item["source"], "📁")
            desc_short = item["description"][:80] if item["description"] else ""
            lines.append(f"- {icon} `{item['name']}` [{item['source']}] — {desc_short}")
        lines.append("")

    if low_items:
        lines.append(f"### 🟡 使用频率低（{len(low_items)} 个）")
        lines.append("")
        lines.append("以下 Skill 偶尔被使用，可根据实际需求决定是否保留：")
        lines.append("")
        for item in low_items:
            icon = src_icons.get(item["source"], "📁")
            desc_short = item["description"][:80] if item["description"] else ""
            lines.append(f"- {icon} `{item['name']}` [{item['source']}] — {item['evidence']}")
        lines.append("")

    if not unused_items and not low_items:
        lines.append("🎉 所有 Skill 均有使用记录，无需清理！")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("> 📋 **评分说明**：")
    lines.append("> - 🔵 **高频**：name 在 MEMORY.md + 其他数据源中频繁出现，或在每日记忆中大量提及")
    lines.append("> - 🟢 **中频**：name 在 2+ 数据源中出现，或 name + 关键词组合匹配")
    lines.append("> - 🟡 **低频**：仅通过关键词匹配（非 name），或 name 仅出现 1 次")
    lines.append("> - 🔴 **未使用**：所有数据源中均未发现相关关键词")
    lines.append("")
    lines.append("> ⚠️ 基于关键词匹配推断，非精确统计。MEMORY.md 的 Skill 索引表会列出所有已安装 Skill，")
    lines.append("> 单独出现不作为高频依据，需要结合其他数据源证据。")

    return "\n".join(lines)
