#!/usr/bin/env python3
"""
审稿管线产物完整性校验 — 确保每个环节都产生了对应的分析产物

用法：
  python3 validate_pipeline.py docs/reviews/<article-dir>/

返回码：
  0 — 全部通过
  1 — 产物缺失/不完整
  2 — 参数错误

检查项：
  1. review.md 存在且有内容
  2. 环节标记存在（每个 stage 是否被引用）
  3. 素材对照结果存在（如有 sources/ 目录）
  4. 事实风险清单存在
  5. 逐句模拟输出存在
  6. 结构评估输出存在
  7. 听众带走什么分析存在
  8. 修复跟踪存在（仅多轮迭代时）
"""

import os
import sys
import re
import json
from pathlib import Path


# ── 颜色 ──
def red(t): return f"\033[31m{t}\033[0m"
def green(t): return f"\033[32m{t}\033[0m"
def yellow(t): return f"\033[33m{t}\033[0m"
def cyan(t): return f"\033[36m{t}\033[0m"


# ── 检查项 ──

# 每个 stage 在 review.md 中应有的关键词标记
STAGE_MARKERS = {
    "素材对照": [
        "素材对照", "素材事实清单", "素材对照结果",
        "素材中", "素材文件", "sources",
    ],
    "事实风险": [
        "事实核查", "事实风险", "事实风险清单",
        "6 类风险", "6类风险",
        "数字精确性", "绝对化表述", "记忆模糊",
        "应然vs实然", "技术概念", "风险类型",
    ],
    "概念频率": [
        "概念频率", "概念频率热力图", "跨幕重叠",
        "出现次数", "出现幕数", "概念名称",
        "🔴 重复", "判定", "callback",
    ],
    "读者模拟": [
        "读者模拟", "逐句", "脑内弹幕",
        "🎯", "😴", "🔥", "🤔",
        "反应标记", "读者反应",
    ],
    "结构评估": [
        "结构完整性", "人性洞察", "市场洞察",
        "传播力", "反AI味",
        "评分", "五维度", "总评",
    ],
    "听众带走": [
        "听众带走", "一句话带走", "一句话定题",
        "认知框架", "未解疑惑", "离场情绪", "行动转化",
        "带走什么", "带走",
    ],
    "风格检查": [
        "风格一致性", "Voice", "voice",
        "解释段", "不必要升维", "结尾拔高",
        "二元对立", "反AI味检测",
    ],
    "修复跟踪": [
        "修复跟踪", "已修", "未修", "新发现",
        "修复率", "回归率", "版本对比",
        "修复情况", "修改情况",
    ],
    "GPT审稿": [
        "ChatGPT", "GPT", "次审", "gpt-review",
    ],
}


def check_review_md_exists(review_dir):
    """检查 review.md 是否存在"""
    path = review_dir / "review.md"
    if not path.exists():
        return False, f"review.md 不存在: {path}"
    size = path.stat().st_size
    if size < 100:
        return False, f"review.md 内容过短 ({size} bytes)"
    return True, f"review.md 存在 ({size} bytes)"


def check_stage_markers(review_dir):
    """检查每个 stage 在 review.md 中是否有关键词标记"""
    path = review_dir / "review.md"
    if not path.exists():
        return [], "review.md 不存在，跳过阶段标记检查"

    content = path.read_text(encoding="utf-8")
    results = []

    for stage, markers in STAGE_MARKERS.items():
        found = []
        for m in markers:
            if m.lower() in content.lower():
                found.append(m)

        if found:
            results.append((stage, True, f"✓ 找到标记: {found[0]}"))
        else:
            results.append((stage, False, f"✗ 未找到任何匹配关键词"))

    return results, None


def check_source_material_result(review_dir, project_dir=None):
    """检查是否有素材对照结果"""
    # 先看 review.md 里有没有素材对照章节
    path = review_dir / "review.md"
    if not path.exists():
        return False, "review.md 不存在"

    content = path.read_text(encoding="utf-8")

    # 检查素材对照标记
    markers = ["素材对照", "素材事实清单", "✅ 一致", "❓ 素材中未找到"]
    for m in markers:
        if m in content:
            return True, f"素材对照已完成（找到标记: {m}）"

    # 如果有 sources 目录但没有素材对照 → 风险
    if project_dir:
        sources_dir = Path(project_dir) / "sources"
        if sources_dir.exists() and any(sources_dir.iterdir()):
            return False, "项目有 sources/ 目录但 review 中未包含素材对照结果 ⚠️"

    return True, "无素材文件（或素材对照已包含在其它分析中）"


def check_output_format(review_dir):
    """检查 review.md 输出格式是否规范"""
    path = review_dir / "review.md"
    if not path.exists():
        return False, "review.md 不存在"

    content = path.read_text(encoding="utf-8")
    issues = []

    # 检查是否有明显的硬伤/建议分层 (支持多种格式)
    priority_found = (
        bool(re.search(r'🔴|📌|✍️|🔧', content)) or           # emoji 标记
        bool(re.search(r'🟡|🟢', content)) or                  # 严重度标记
        bool(re.search(r'严重风险|中等风险|轻微风险', content)) or  # 事实风险格式
        bool(re.search(r'必须改|建议改|可选|推荐修改', content))    # 文字格式
    )
    if not priority_found:
        issues.append("未找到问题优先级标记（🔴📌✍️🔧 或 严重/中等/轻微 分层）")

    # 检查是否有位置标注（多种格式）
    location_found = (
        bool(re.search(r'第.*[^。]*幕|位置|段落|原文|第.*段|摘录|稿位置|草稿位置|草稿原文|章节|文中|草稿', content)) or
        bool(re.search(r'\|\s*原始建议\s*\|', content)) or   # 版本对比表: | 原始建议 | 来源 | ...
        bool(re.search(r'\|\s*原文摘录\s*\|', content)) or    # 事实风险表: | 原文摘录 | 风险类型 | ...
        bool(re.search(r'\|\s*草稿位置\s*\|', content))       # 素材对照表: | 草稿位置 | 草稿原文 | ...
    )
    if not location_found:
        issues.append("未找到位置/原文引用的标注")

    # 检查是否有修改建议
    if not re.search(r'建议|改为|修改|修复|修法|修正|方向|改法|调整', content):
        issues.append("未找到修改建议")

    return len(issues) == 0, issues if issues else ["输出格式基本完整"]


def check_archive(review_dir):
    """检查是否有归档目录，多轮迭代时应有"""
    archive_dir = review_dir / "archive"
    if archive_dir.exists():
        archives = list(archive_dir.glob("*.md"))
        return True, f"已归档 {len(archives)} 个历史版本"
    return None, "无归档目录（首轮审稿默认无归档）"


def check_gpt_review(review_dir):
    """检查是否存在 GPT 审稿记录"""
    path = review_dir / "gpt-review.md"
    if path.exists():
        size = path.stat().st_size
        if size > 500:
            return True, f"GPT审稿记录存在 ({size} bytes)"
        else:
            return False, f"GPT审稿记录过短 ({size} bytes)"
    return None, "无 GPT 审稿记录（可选次审）"


def main():
    if len(sys.argv) < 2:
        print(f"用法: python3 {sys.argv[0]} <review-dir> [project-dir]")
        print(f"示例: python3 {sys.argv[0]} docs/reviews/llm-wiki-todo")
        print(f"      python3 {sys.argv[0]} docs/reviews/llm-wiki-todo docs/projects/llm-wiki-todo")
        sys.exit(2)

    review_dir = Path(sys.argv[1])
    if not review_dir.exists() or not review_dir.is_dir():
        print(red(f"错误: 目录不存在: {review_dir}"))
        sys.exit(2)

    project_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    passed_all = True

    print(f"\n{'='*60}")
    print(f"📋 审稿管线产物完整性校验")
    print(f"   审稿目录: {review_dir}")
    if project_dir:
        print(f"   项目目录: {project_dir}")
    print(f"{'='*60}")

    # ---- 1. review.md 存在性 ----
    print(f"\n{'─'*40}")
    print(f"  1️⃣  基础文件检查")
    ok, msg = check_review_md_exists(review_dir)
    status = green("✅") if ok else red("❌")
    print(f"  {status} {msg}")
    if not ok:
        passed_all = False

    # ---- 2. 阶段标记完整性 ----
    print(f"\n{'─'*40}")
    print(f"  2️⃣  审稿阶段覆盖检查")
    stage_results, err = check_stage_markers(review_dir)
    if err:
        print(f"  {red('❌')} {err}")
        passed_all = False
    else:
        covered = sum(1 for _, ok, _ in stage_results if ok)
        total = len(stage_results)
        for stage, ok, detail in stage_results:
            icon = green("✓") if ok else yellow("⚠")
            # 修复跟踪、GPT审稿、听众带走是可选阶段
            OPTIONAL_STAGES = {"修复跟踪", "GPT审稿", "听众带走"}
            is_optional = stage in OPTIONAL_STAGES
            if not ok:
                if is_optional:
                    icon = yellow("○")
                else:
                    icon = red("✗")
                    passed_all = False
            print(f"  {icon} {stage}: {detail}")
        print(f"  {'─'*30}")
        info_color = green if covered >= total - 2 else yellow
        print(f"  {info_color(f'覆盖: {covered}/{total} 个阶段')}" +
              (" (修复跟踪/GPT审稿/听众带走为可选)" if total - covered > 0 else ""))

    # ---- 3. 素材对照 ----
    print(f"\n{'─'*40}")
    print(f"  3️⃣  素材对照检查")
    ok, msg = check_source_material_result(review_dir, project_dir)
    icon = green("✅") if ok else red("⚠️")
    print(f"  {icon} {msg}")
    if not ok:
        passed_all = False

    # ---- 4. 输出格式 ----
    print(f"\n{'─'*40}")
    print(f"  4️⃣  输出格式检查")
    ok, issues = check_output_format(review_dir)
    if ok:
        print(f"  {green('✅')} {issues[0]}")
    else:
        for issue in issues:
            print(f"  {yellow('⚠')} {issue}")

    # ---- 5. 归档 ----
    print(f"\n{'─'*40}")
    print(f"  5️⃣  版本归档检查")
    ok, msg = check_archive(review_dir)
    if ok is None:
        print(f"  ⚪ {msg}")
    elif ok:
        print(f"  {green('✅')} {msg}")
    else:
        print(f"  {yellow('⚠')} {msg}")

    # ---- 6. GPT审稿 ----
    print(f"\n{'─'*40}")
    print(f"  6️⃣  GPT副审记录")
    ok, msg = check_gpt_review(review_dir)
    if ok is None:
        print(f"  ⚪ {msg}")
    elif ok:
        print(f"  {green('✅')} {msg}")
    else:
        print(f"  {yellow('⚠')} {msg}")

    # ---- 汇总 ----
    print(f"\n{'='*60}")
    if passed_all:
        print(f"  {green('✅ 全部通过')}")
        sys.exit(0)
    else:
        print(f"  {red('❌ 存在未通过项，请补充后再发布')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
