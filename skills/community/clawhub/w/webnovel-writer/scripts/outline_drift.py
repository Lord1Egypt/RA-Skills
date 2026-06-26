#!/usr/bin/env python3
"""
大纲偏差检测脚本
比较正文与大纲的差异，输出偏差评分和趋势。

用法:
  python3 outline_drift.py --outline <大纲文件> --chapters <正文章节目录>
  python3 outline_drift.py --outline <大纲文件> --chapter-list <章节列表文件> --chapters <正文章节目录>

支持两种大纲格式:
  1. 章节列表文件（20卷完整章节列表.md 格式）
  2. 完整大纲文件（完整大纲v4.md 格式，会从20卷章节列表提取结构）
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ── 工具函数 ──────────────────────────────────────────────

def strip_markdown(text: str) -> str:
    """去除 markdown 格式标记"""
    text = re.sub(r'[#*`_~\[\]()（），,。.!！？?\s]+', '', text)
    return text.strip()

def cn_num_to_int(s):
    """中文数字转阿拉伯数字（支持一到百）"""
    cn = '零一二三四五六七八九十'
    if s.isdigit():
        return int(s)
    result = 0
    if '百' in s:
        idx = s.index('百')
        prefix = s[:idx]
        result = (cn.index(prefix) if prefix in cn else 1) * 100
        s = s[idx+1:]
    if '十' in s:
        idx = s.index('十')
        prefix = s[:idx]
        result += (cn.index(prefix) if prefix else 1) * 10
        s = s[idx+1:]
    if s and s in cn:
        result += cn.index(s)
    return result or 0

def normalize_title(title: str) -> str:
    """标准化章节标题用于比较"""
    t = title.strip()
    # 去除章节号前缀
    t = re.sub(r'^第?\d+[章节卷]?\s*[.、)）]?\s*', '', t)
    t = re.sub(r'^\d+[.、)\s]+', '', t)
    return t.strip()

def char_similarity(a: str, b: str) -> float:
    """基于字符重叠的相似度"""
    a, b = strip_markdown(a), strip_markdown(b)
    if not a or not b:
        return 0.0
    set_a, set_b = set(a), set(b)
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0

def extract_keywords(text: str, top_n: int = 15) -> List[str]:
    """简单关键词提取：高频实词"""
    # 去除标点、数字、常见虚词
    stopwords = set('的了是在我有和就不人都一这中大为上个国也子时道说出会要没成好能对然她他它们你那被从把与而却已经将向给又很最只更比等但是因为所以如果虽然然后不过可以这个那个什么怎么为什么哪些自己别人事情知道看到听到感觉觉得发现突然终于居然竟然'.encode('utf-8').decode('utf-8'))
    # Actually use character-level stopwords
    stop_chars = set('的了是在我有和就不人都一这中大为上个国也子时道说出会要没成好能对然她他它们你那被从把与而却已经将向给又很最只更比等但是因为所以如果虽然然后不过可以这个那个什么怎么为什么哪些自己别人事情知道看到听到感觉觉得发现突然终于居然竟然一二三四五六七八九十百千万亿')

    # Extract 2-4 char words by sliding window (simple approach)
    # Better: just use characters that appear in meaningful nouns
    cleaned = "".join(c for c in text if "\u4e00" <= c <= "\u9fff")

    # Extract meaningful segments (2+ chars, skip single stop chars)
    words = []
    # Use simple 2-char and 3-char sliding window
    for i in range(len(cleaned) - 1):
        w2 = cleaned[i:i+2]
        if not (w2[0] in stop_chars and w2[1] in stop_chars):
            words.append(w2)
    for i in range(len(cleaned) - 2):
        w3 = cleaned[i:i+3]
        if sum(1 for c in w3 if c in stop_chars) <= 1:
            words.append(w3)

    counter = Counter(words)
    return [w for w, _ in counter.most_common(top_n)]

def find_character_names(text):
    """从文本中提取可能的人名（简单启发式）"""
    # 匹配常见中文姓名模式：2-3字，以常见姓氏开头
    common_surnames = '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏窦章苏潘葛范彭郎鲁韦昌马苗凤花方任袁柳唐罗薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄和穆萧尹'
    names = set()
    # 2-char names
    for m in re.finditer(rf'[{common_surnames}][\u4e00-\u9fff]', text):
        names.add(m.group())
    # 3-char names
    for m in re.finditer(rf'[{common_surnames}][\u4e00-\u9fff]{{1,2}}', text):
        if len(m.group()) >= 2:
            names.add(m.group())
    return names

# ── 解析大纲/章节列表 ─────────────────────────────────────

def parse_chapter_list(filepath: str) -> List[Dict[str, Any]]:
    """
    解析 20卷完整章节列表.md 格式
    返回: [{"vol": 卷号, "vol_title": 卷标题, "chapters": [{"num": 章节号, "title": 标题}]}]
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    volumes = []
    current_vol = None
    current_vol_title = ""

    for line in content.split('\n'):
        line = line.strip()
        # 匹配卷标题: # 第1卷 正常营业（第1-30章）
        m = re.match(r'#\s*第([一二三四五六七八九十百零\d]+)卷[：:\s]*(.+?)(?:（(.+?)）)?$', line)
        if m:
            if current_vol is not None:
                volumes.append(current_vol)
            current_vol = {
                "vol": cn_num_to_int(m.group(1)),
                "vol_title": m.group(2).strip(),
                "vol_range": m.group(3) or "",
                "chapters": []
            }
            current_vol_title = m.group(2).strip()
            continue

        # 匹配章节: 数字. 标题
        m = re.match(r'(\d+)\.\s*(.+)', line)
        if m and current_vol is not None:
            ch_num = int(m.group(1))
            ch_title = m.group(2).strip()
            current_vol["chapters"].append({
                "num": ch_num,
                "title": ch_title
            })

    if current_vol is not None:
        volumes.append(current_vol)

    return volumes

def parse_outline_keywords(filepath: str) -> List[Dict[str, Any]]:
    """
    从完整大纲提取每章的关键词和应出场角色
    返回: [{"vol": N, "chapters": [{"num": N, "title": "", "keywords": [], "characters": []}]}]
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    volumes = []
    current_vol = None

    for line in content.split('\n'):
        line = line.strip()
        m = re.match(r'#.*第([一二三四五六七八九十百零\d]+)卷', line)
        if m:
            if current_vol:
                volumes.append(current_vol)
            current_vol = {"vol": cn_num_to_int(m.group(1)), "chapters": []}
            continue

        # 匹配 Markdown 标题章节: # 第1章 标题
        m = re.match(r'#.*第(\d+)[章节]', line)
        if m and current_vol:
            current_vol["chapters"].append({
                "num": int(m.group(1)),
                "title": line,
                "keywords": extract_keywords(line + ' ' + line, 5),
                "characters": list(find_character_names(line))
            })
            continue

        # 匹配表格行: | 第001章 | 轮回影院 |
        m = re.match(r'\|\s*第(\d+)[章]\s*\|\s*(.+?)\s*\|', line)
        if m and current_vol:
            current_vol["chapters"].append({
                "num": int(m.group(1)),
                "title": m.group(2).strip(),
                "keywords": extract_keywords(m.group(2), 5),
                "characters": list(find_character_names(m.group(2)))
            })

    if current_vol:
        volumes.append(current_vol)

    return volumes

# ── 解析正文 ──────────────────────────────────────────────

def parse_chapters_dir(dirpath: str) -> List[Dict[str, Any]]:
    """
    解析正文目录中的章节文件
    返回: [{"num": 章节号, "title": 标题, "content": 正文内容, "filename": 文件名}]
    """
    chapters = []
    seen_nums = {}  # 章节号去重：同号只保留带标题的版本
    p = Path(dirpath)

    for f in sorted(p.glob('*.md')):
        filename = f.stem
        # 必须以"第"开头才视为正文章节（排除ch01.md等草稿）
        m = re.match(r'第(\d+)[章]', filename)
        if not m:
            continue

        ch_num = int(m.group(1))
        title = re.sub(r'^第\d+章\s*', '', filename).strip('_').strip()

        content = f.read_text(encoding='utf-8')
        first_line = content.split('\n')[0].strip()
        if first_line.startswith('#'):
            first_line = re.sub(r'^#+\s*', '', first_line)
            if first_line:
                title = first_line

        entry = {
            "num": ch_num,
            "title": title,
            "content": content,
            "filename": f.name,
            "char_count": len(content)
        }

        # 去重：同章节号，优先保留带标题的文件
        if ch_num in seen_nums:
            old_title = seen_nums[ch_num]["title"]
            if not old_title and title:
                seen_nums[ch_num] = entry
            # 都有标题时保留文件名更长的（通常更具体）
        else:
            seen_nums[ch_num] = entry

    chapters = sorted(seen_nums.values(), key=lambda x: x["num"])
    return chapters

# ── 偏差检测 ──────────────────────────────────────────────

def check_title_match(outline_chapters: List[Dict[str, Any]], actual_chapters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """章节标题匹配检测"""
    results = []

    # 建立索引
    outline_by_num = {c["num"]: c for c in outline_chapters}

    for ach in actual_chapters:
        num = ach["num"]
        if num in outline_by_num:
            och = outline_by_num[num]
            sim = char_similarity(ach["title"], och["title"])
            results.append({
                "num": num,
                "outline_title": och["title"],
                "actual_title": ach["title"],
                "similarity": round(sim, 3),
                "status": "匹配" if sim >= 0.3 else "偏差"
            })
        else:
            results.append({
                "num": num,
                "outline_title": "(大纲中无此章)",
                "actual_title": ach["title"],
                "similarity": 0.0,
                "status": "新增"
            })

    # 检查大纲中有但正文中没有的章节
    actual_nums = set(c["num"] for c in actual_chapters)
    for och in outline_chapters:
        if och["num"] not in actual_nums:
            results.append({
                "num": och["num"],
                "outline_title": och["title"],
                "actual_title": "(未写)",
                "similarity": 0.0,
                "status": "缺失"
            })

    return results

def check_keyword_coverage(outline_chapters, actual_chapters):
    """关键词覆盖率检测"""
    results = []
    actual_by_num = {c["num"]: c for c in actual_chapters}

    for och in outline_chapters:
        num = och["num"]
        keywords = och.get("keywords", [])

        if not keywords:
            continue

        if num not in actual_by_num:
            results.append({
                "num": num,
                "coverage": 0.0,
                "missing": keywords,
                "status": "未写"
            })
            continue

        content = actual_by_num[num]["content"]
        covered = [kw for kw in keywords if kw in content]
        coverage = len(covered) / len(keywords) if keywords else 0

        results.append({
            "num": num,
            "coverage": round(coverage, 3),
            "covered": covered,
            "missing": [kw for kw in keywords if kw not in content],
            "status": "良好" if coverage >= 0.4 else "偏离"
        })

    return results

def check_progress_drift(volumes, actual_chapters):
    """进度偏差检测"""
    results = []
    actual_nums = sorted(set(c["num"] for c in actual_chapters))
    max_actual = max(actual_nums) if actual_nums else 0

    total_outline = 0
    for vol in volumes:
        total_outline += len(vol["chapters"])

    for vol in volumes:
        vol_chapters = vol["chapters"]
        if not vol_chapters:
            continue

        ch_nums = [c["num"] for c in vol_chapters]
        start, end = min(ch_nums), max(ch_nums)

        # 统计该卷内实际写了几章
        written = [n for n in actual_nums if start <= n <= end]
        planned = len(vol_chapters)
        actual = len(written)

        drift = actual - planned

        results.append({
            "vol": vol["vol"],
            "vol_title": vol.get("vol_title", f"第{vol['vol']}卷"),
            "planned": planned,
            "actual": actual,
            "drift": drift,
            "status": "超前" if drift > 0 else ("滞后" if drift < 0 else "同步")
        })

    return results, total_outline, max_actual

def check_character_presence(outline_chapters, actual_chapters, known_characters=None):
    """角色出场偏差检测"""
    if known_characters is None:
        known_characters = []

    results = []
    actual_by_num = {c["num"]: c for c in actual_chapters}

    for och in outline_chapters:
        num = och["num"]
        expected_chars = och.get("characters", [])
        if not expected_chars:
            continue

        if num not in actual_by_num:
            results.append({
                "num": num,
                "expected": expected_chars,
                "missing": expected_chars,
                "status": "未写"
            })
            continue

        content = actual_by_num[num]["content"]
        present = [c for c in expected_chars if c in content]
        missing = [c for c in expected_chars if c not in content]

        results.append({
            "num": num,
            "expected": expected_chars,
            "present": present,
            "missing": missing,
            "status": "完整" if not missing else f"缺{len(missing)}人"
        })

    return results

def calculate_drift_trend(title_results, window=5):
    """计算偏差趋势：正文是否在逐渐偏离大纲"""
    # 只看有匹配结果的
    matched = [r for r in title_results if r["status"] in ("匹配", "偏差")]
    if len(matched) < 2:
        return "数据不足", []

    # 按章节号排序
    matched.sort(key=lambda x: x["num"])

    # 计算滑动平均相似度
    trend_points = []
    for i in range(len(matched)):
        start = max(0, i - window + 1)
        window_items = matched[start:i+1]
        avg_sim = sum(r["similarity"] for r in window_items) / len(window_items)
        trend_points.append({
            "num": matched[i]["num"],
            "similarity": matched[i]["similarity"],
            "avg": round(avg_sim, 3)
        })

    # 判断趋势
    if len(trend_points) < 3:
        return "数据不足", trend_points

    first_third = trend_points[:len(trend_points)//3]
    last_third = trend_points[-(len(trend_points)//3):]

    early_avg = sum(p["avg"] for p in first_third) / len(first_third)
    late_avg = sum(p["avg"] for p in last_third) / len(last_third)

    diff = late_avg - early_avg
    if diff > 0.05:
        trend = "✅ 趋于一致"
    elif diff < -0.05:
        trend = "⚠️ 逐渐偏离"
    else:
        trend = "📊 基本稳定"

    return trend, trend_points

# ── 汇总统计 ────────────────────────────────────────────

def compute_drift_score(num: int, title_results: List[Dict], keyword_results: List[Dict], character_results: List[Dict]) -> float:
    """计算单章偏差评分（0=完全一致，100=完全偏离）"""
    scores = []
    tr = next((r for r in title_results if r["num"] == num), None)
    if tr:
        scores.append((1 - tr["similarity"]) * 30)
    kr = next((r for r in keyword_results if r["num"] == num), None)
    if kr:
        scores.append((1 - kr.get("coverage", 0)) * 40)
    cr = next((r for r in character_results if r["num"] == num), None)
    if cr and cr.get("expected"):
        char_cov = len(cr.get("present", [])) / len(cr["expected"])
        scores.append((1 - char_cov) * 30)
    return min(100, sum(scores)) if scores else None

def generate_summary(title_results: List[Dict], keyword_results: List[Dict], character_results: List[Dict],
                     progress_results, actual_chapters, volumes):
    """
    生成汇总统计：平均偏差、偏差趋势、按卷摘要
    """
    # 1. 计算每章偏差评分
    written_nums = sorted(set(c["num"] for c in actual_chapters))
    chapter_scores = {}
    for num in written_nums:
        score = compute_drift_score(num, title_results, keyword_results, character_results)
        if score is not None:
            chapter_scores[num] = score

    # 2. 平均偏差
    if chapter_scores:
        avg_drift = round(sum(chapter_scores.values()) / len(chapter_scores), 1)
    else:
        avg_drift = 0.0

    # 3. 偏差趋势（最近5章）
    sorted_nums = sorted(chapter_scores.keys())
    recent_n = min(5, len(sorted_nums))
    if recent_n >= 2:
        recent = sorted_nums[-recent_n:]
        prev = sorted_nums[-2 * recent_n:-recent_n] if len(sorted_nums) >= 2 * recent_n else sorted_nums[:len(sorted_nums) - recent_n]
        recent_avg = sum(chapter_scores[n] for n in recent) / len(recent)
        prev_avg = sum(chapter_scores[n] for n in prev) / len(prev) if prev else recent_avg
        if recent_avg - prev_avg > 3:
            trend_direction = "上升（偏离增大）"
        elif recent_avg - prev_avg < -3:
            trend_direction = "下降（偏离减小）"
        else:
            trend_direction = "平稳"
    else:
        trend_direction = "数据不足"

    # 4. 按卷摘要
    vol_summary = []
    for vol in volumes:
        ch_nums = [c["num"] for c in vol.get("chapters", [])]
        if not ch_nums:
            continue
        start, end = min(ch_nums), max(ch_nums)
        vol_scores = {n: chapter_scores[n] for n in sorted_nums if start <= n <= end and n in chapter_scores}
        if not vol_scores:
            vol_summary.append({
                "vol": vol["vol"],
                "vol_title": vol.get("vol_title", f"第{vol['vol']}卷"),
                "avg_drift": None,
                "max_drift_chapter": None,
                "max_drift_score": None,
                "trend_direction": "未写",
                "written": 0,
                "planned": len(ch_nums)
            })
            continue
        avg = round(sum(vol_scores.values()) / len(vol_scores), 1)
        max_ch = max(vol_scores, key=vol_scores.get)
        # 卷内趋势
        vol_sorted = sorted(vol_scores.keys())
        vn = min(3, len(vol_sorted))
        if vn >= 2:
            vol_recent_avg = sum(vol_scores[n] for n in vol_sorted[-vn:]) / vn
            vol_prev_avg = sum(vol_scores[n] for n in vol_sorted[:vn]) / vn
            if vol_recent_avg - vol_prev_avg > 3:
                vol_trend = "上升"
            elif vol_recent_avg - vol_prev_avg < -3:
                vol_trend = "下降"
            else:
                vol_trend = "平稳"
        else:
            vol_trend = "数据不足"
        vol_summary.append({
            "vol": vol["vol"],
            "vol_title": vol.get("vol_title", f"第{vol['vol']}卷"),
            "avg_drift": avg,
            "max_drift_chapter": max_ch,
            "max_drift_score": vol_scores[max_ch],
            "trend_direction": vol_trend,
            "written": len(vol_scores),
            "planned": len(ch_nums)
        })

    return {
        "total_chapters": len(written_nums),
        "avg_drift": avg_drift,
        "trend_direction": trend_direction,
        "vol_summary": vol_summary,
        "chapter_scores": chapter_scores
    }

def format_summary_block(summary):
    """格式化汇总统计的控制台输出"""
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("  📊 汇总统计")
    lines.append("=" * 60)

    # 总览
    avg = summary["avg_drift"]
    avg_icon = "🟢" if avg < 20 else "🟡" if avg < 50 else "🔴"
    lines.append(f"\n  {avg_icon} 平均偏差评分: {avg} / 100")
    lines.append(f"  📈 最近5章偏差趋势: {summary['trend_direction']}")
    lines.append(f"  📝 已写章节数: {summary['total_chapters']}")

    # 按卷摘要
    lines.append("\n  ┌─ 按卷偏差摘要 ─────────────────────────────────┐")
    lines.append(f"  {'卷':>4s} | {'卷标题':<10s} | {'平均偏差':>6s} | {'最高偏差章':>8s} | {'趋势':>6s}")
    lines.append("  " + "-" * 54)
    for vs in summary["vol_summary"]:
        if vs["avg_drift"] is None:
            lines.append(f"  {vs['vol']:>3d}卷 | {vs['vol_title'][:10]:<10s} | {'(未写)':>6s} | {'---':>8s} | {vs['trend_direction']:>6s}")
        else:
            score_icon = "🟢" if vs["avg_drift"] < 20 else "🟡" if vs["avg_drift"] < 50 else "🔴"
            lines.append(f"  {vs['vol']:>3d}卷 | {vs['vol_title'][:10]:<10s} | {score_icon}{vs['avg_drift']:>5.1f} | 第{vs['max_drift_chapter']:>3d}章({vs['max_drift_score']:.0f}) | {vs['trend_direction']:>6s}")
    lines.append("  └" + "─" * 54 + "┘")
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

# ── 输出格式化 ────────────────────────────────────────────

def format_report(title_results, keyword_results, progress_results,
                  character_results, trend, trend_points, total_outline, max_actual):
    """格式化输出报告"""
    lines = []
    lines.append("=" * 60)
    lines.append("  大纲偏差检测报告")
    lines.append("=" * 60)

    # 总览
    lines.append(f"\n📋 总览")
    lines.append(f"   大纲计划: {total_outline} 章")
    lines.append(f"   实际完成: {max_actual} 章")
    lines.append(f"   趋势判断: {trend}")

    # 进度偏差
    lines.append(f"\n📖 进度偏差（按卷）")
    lines.append("-" * 50)
    for r in progress_results:
        status_icon = {"超前": "🟡", "滞后": "🔴", "同步": "🟢"}.get(r["status"], "⚪")
        lines.append(f"  {status_icon} 第{r['vol']:2d}卷 {r['vol_title'][:12]:<12s} "
                     f"计划{r['planned']:3d}章 实际{r['actual']:3d}章 {r['status']}")

    # 标题匹配
    lines.append(f"\n📝 标题匹配（相似度 < 0.3 标记为偏差）")
    lines.append("-" * 50)
    for r in sorted(title_results, key=lambda x: x["num"]):
        if r["status"] == "匹配":
            icon = "🟢"
        elif r["status"] == "偏差":
            icon = "🟡"
        elif r["status"] == "新增":
            icon = "🔵"
        elif r["status"] == "缺失":
            icon = "🔴"
        else:
            icon = "⚪"
        sim_str = f"{r['similarity']:.2f}" if r['similarity'] > 0 else "---"
        lines.append(f"  {icon} 第{r['num']:3d}章 [{sim_str}] {r['actual_title'][:20]} ← {r['outline_title'][:20]}")

    # 关键词覆盖
    if keyword_results:
        lines.append(f"\n🔑 关键词覆盖率")
        lines.append("-" * 50)
        for r in keyword_results:
            icon = "🟢" if r.get("coverage", 0) >= 0.4 else "🟡" if r.get("coverage", 0) > 0 else "🔴"
            cov_str = f"{r.get('coverage', 0):.0%}"
            lines.append(f"  {icon} 第{r['num']:3d}章 覆盖率{cov_str} {r.get('status', '')}")
            if r.get("missing"):
                lines.append(f"      缺失关键词: {', '.join(r['missing'][:8])}")

    # 角色出场
    if character_results:
        lines.append(f"\n👥 角色出场偏差")
        lines.append("-" * 50)
        for r in character_results:
            if r.get("missing"):
                icon = "🟡"
                lines.append(f"  {icon} 第{r['num']:3d}章 {r['status']} "
                           f"缺失: {', '.join(r['missing'])}")

    # 偏差趋势
    if trend_points and len(trend_points) > 2:
        lines.append(f"\n📈 偏差趋势（滑动平均相似度）")
        lines.append("-" * 50)
        # 只显示关键节点
        step = max(1, len(trend_points) // 10)
        for p in trend_points[::step]:
            bar_len = int(p["avg"] * 20)
            bar = "█" * bar_len + "░" * (20 - bar_len)
            lines.append(f"  第{p['num']:3d}章 {bar} {p['avg']:.2f}")

    # 每章偏差评分汇总
    lines.append(f"\n📊 每章偏差评分（0=完全一致，100=完全偏离）")
    lines.append("-" * 50)

    all_nums = sorted(set(
        [r["num"] for r in title_results] +
        [r["num"] for r in keyword_results] +
        [r["num"] for r in character_results]
    ))

    for num in all_nums:
        scores = []

        # 标题相似度贡献
        tr = next((r for r in title_results if r["num"] == num), None)
        if tr:
            scores.append((1 - tr["similarity"]) * 30)  # 权重30

        # 关键词覆盖贡献
        kr = next((r for r in keyword_results if r["num"] == num), None)
        if kr:
            scores.append((1 - kr.get("coverage", 0)) * 40)  # 权重40

        # 角色覆盖贡献
        cr = next((r for r in character_results if r["num"] == num), None)
        if cr and cr.get("expected"):
            char_cov = len(cr.get("present", [])) / len(cr["expected"])
            scores.append((1 - char_cov) * 30)  # 权重30

        if scores:
            total_score = min(100, sum(scores))
            if total_score < 20:
                icon = "🟢"
            elif total_score < 50:
                icon = "🟡"
            else:
                icon = "🔴"
            lines.append(f"  {icon} 第{num:3d}章 偏差评分: {total_score:5.1f}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

# ── 修复建议 ────────────────────────────────────────────────

def classify_drift_cause(tr, kr, cr, ach, outline_ch):
    """分类单章偏差原因"""
    causes = []
    if tr and tr["status"] == "偏差":
        causes.append("剧情转向")
    elif tr and tr["status"] == "新增":
        causes.append("扩写（新增章节）")
    if kr and kr.get("status") == "偏离":
        causes.append("关键词偏离")
    if cr and cr.get("missing"):
        causes.append(f"角色缺失({','.join(cr['missing'][:3])})")
    # 字数偏差
    if ach:
        expected_len = 2500  # 默认期望字数
        ratio = ach["char_count"] / expected_len if expected_len > 0 else 1
        if ratio > 1.5:
            causes.append("扩写（字数过多）")
        elif ratio < 0.5:
            causes.append("压缩（字数不足）")
    return causes or ["未检测到明显偏差"]

def generate_fix_suggestions(title_results, keyword_results, character_results,
                             progress_results, summary, volumes, actual_chapters, outline_flat):
    """生成修复建议"""
    suggestions = []
    actual_by_num = {c["num"]: c for c in actual_chapters}
    outline_by_num = {c["num"]: c for c in outline_flat}
    chapter_scores = summary.get("chapter_scores", {})

    # 找出偏差较大的章节（评分>=30）
    drifted_chapters = sorted(
        [(num, score) for num, score in chapter_scores.items() if score >= 30],
        key=lambda x: x[1], reverse=True
    )

    # 按卷分组
    vol_map = {}
    for vol in volumes:
        ch_nums = [c["num"] for c in vol.get("chapters", [])]
        if not ch_nums:
            continue
        for n in ch_nums:
            vol_map[n] = vol

    # 缺失章节
    missing = [r for r in title_results if r["status"] == "缺失"]
    # 新增章节
    added = [r for r in title_results if r["status"] == "新增"]

    # 逐章建议
    chapter_suggestions = []
    for num, score in drifted_chapters:
        tr = next((r for r in title_results if r["num"] == num), None)
        kr = next((r for r in keyword_results if r["num"] == num), None)
        cr = next((r for r in character_results if r["num"] == num), None)
        ach = actual_by_num.get(num)
        och = outline_by_num.get(num)

        causes = classify_drift_cause(tr, kr, cr, ach, och)

        # 生成建议
        if score >= 60:
            action = "修改大纲" if any("新增" in c or "转向" in c for c in causes) else "回归大纲"
        else:
            action = "回归大纲"

        vol = vol_map.get(num, {})
        vol_title = vol.get("vol_title", "未知卷")

        specific_advice = []
        if kr and kr.get("missing"):
            specific_advice.append(f"补充关键词: {', '.join(kr['missing'][:5])}")
        if cr and cr.get("missing"):
            specific_advice.append(f"安排角色出场: {', '.join(cr['missing'][:5])}")
        if tr and tr["status"] == "新增":
            specific_advice.append("此章不在大纲中，考虑：\n  a) 删除/合并到相邻章节\n  b) 在大纲中补充此章")
        if not specific_advice:
            specific_advice.append("检查剧情走向，对齐大纲描述")

        chapter_suggestions.append({
            "num": num,
            "score": score,
            "vol": vol_title,
            "causes": causes,
            "action": action,
            "advice": specific_advice
        })

    # 缺失章节建议
    missing_suggestions = []
    for r in missing:
        vol = vol_map.get(r["num"], {})
        missing_suggestions.append({
            "num": r["num"],
            "outline_title": r["outline_title"],
            "vol": vol.get("vol_title", "未知"),
            "advice": "尽快补充此章，或在前后章节中覆盖其内容"
        })

    # 新增章节建议
    added_suggestions = []
    for r in added:
        added_suggestions.append({
            "num": r["num"],
            "actual_title": r["actual_title"],
            "advice": "决定：\n  a) 保留并更新大纲\n  b) 合并到相邻大纲章节\n  c) 删除"
        })

    # 按卷汇总建议
    vol_suggestions = []
    for vs in summary.get("vol_summary", []):
        if vs.get("avg_drift") is not None and vs["avg_drift"] >= 30:
            vol_suggestions.append({
                "vol": vs["vol"],
                "vol_title": vs["vol_title"],
                "avg_drift": vs["avg_drift"],
                "advice": "该卷整体偏差较大，建议逐章检查并调整"
            })

    return {
        "total_drifted": len(drifted_chapters),
        "chapter_suggestions": chapter_suggestions,
        "missing_suggestions": missing_suggestions,
        "added_suggestions": added_suggestions,
        "vol_suggestions": vol_suggestions
    }

def format_fix_suggestions(suggestions):
    """格式化修复建议输出"""
    lines = []
    lines.append("\n" + "=" * 60)
    lines.append("  🔧 偏差修复建议")
    lines.append("=" * 60)
    lines.append(f"\n  共检测到 {suggestions['total_drifted']} 个偏差章节")

    # 逐章建议
    cs = suggestions["chapter_suggestions"]
    if cs:
        lines.append("\n  ┌─ 逐章修复建议 ────────────────────────────────┐")
        for s in cs:
            action_icon = "📝" if s["action"] == "修改大纲" else "🔄"
            lines.append(f"  {action_icon} 第{s['num']:3d}章 ({s['vol']}) 偏差{s['score']:.0f}分")
            lines.append(f"     原因: {', '.join(s['causes'])}")
            lines.append(f"     建议: {s['action']}")
            for adv in s["advice"]:
                lines.append(f"     → {adv}")
        lines.append("  └" + "─" * 48 + "┘")

    # 缺失章节
    ms = suggestions["missing_suggestions"]
    if ms:
        lines.append("\n  ┌─ 缺失章节 ────────────────────────────────────┐")
        for s in ms:
            lines.append(f"  🔴 第{s['num']:3d}章《{s['outline_title'][:20]}》({s['vol']})")
            lines.append(f"     → {s['advice']}")
        lines.append("  └" + "─" * 48 + "┘")

    # 新增章节
    ads = suggestions["added_suggestions"]
    if ads:
        lines.append("\n  ┌─ 新增章节（大纲外） ──────────────────────────┐")
        for s in ads:
            lines.append(f"  🔵 第{s['num']:3d}章《{s['actual_title'][:20]}》")
            lines.append(f"     → {s['advice']}")
        lines.append("  └" + "─" * 48 + "┘")

    # 按卷汇总
    vs = suggestions["vol_suggestions"]
    if vs:
        lines.append("\n  ┌─ 按卷汇总 ────────────────────────────────────┐")
        for s in vs:
            lines.append(f"  ⚠️ 第{s['vol']:2d}卷 {s['vol_title']} 平均偏差{s['avg_drift']:.0f}")
            lines.append(f"     → {s['advice']}")
        lines.append("  └" + "─" * 48 + "┘")

    if not cs and not ms and not ads:
        lines.append("\n  ✅ 未检测到明显偏差，大纲一致性良好！")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

# ── 主流程 ────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='大纲偏差检测')
    parser.add_argument('--outline', required=True, help='完整大纲文件路径')
    parser.add_argument('--chapter-list', help='章节列表文件路径（20卷章节列表格式）')
    parser.add_argument('--chapters', required=True, help='正文章节目录路径')
    parser.add_argument('--json', action='store_true', help='输出JSON格式')
    parser.add_argument('--known-characters', nargs='*', help='已知角色名列表')
    parser.add_argument('--fix-suggest', action='store_true', help='检测偏差后给出修复建议')
    parser.add_argument('--version', action='version', version='outline_drift v2.1.0 (novel-writer skill)')
    args = parser.parse_args()

    # 解析大纲：自动检测文件格式
    # 先尝试当章节列表解析，如果解析出卷和章节则当作章节列表
    volumes = []
    try:
        test_vols = parse_chapter_list(args.outline)
        if test_vols and any(v["chapters"] for v in test_vols):
            volumes = test_vols
    except Exception:
        pass

    # 解析大纲关键词（如果没通过章节列表获取到volumes，或需要补充关键词）
    outline_data = parse_outline_keywords(args.outline)

    # 解析额外章节列表（如果提供）
    if args.chapter_list:
        volumes = parse_chapter_list(args.chapter_list)

    # 如果没有章节列表，从大纲构建简化版
    if not volumes:
        for vol in outline_data:
            volumes.append({
                "vol": vol["vol"],
                "vol_title": f"第{vol['vol']}卷",
                "chapters": vol["chapters"]
            })

    # 展平大纲章节
    outline_flat = []
    for vol in volumes:
        for ch in vol["chapters"]:
            # 从大纲数据补充关键词
            odata = None
            for ov in outline_data:
                for oc in ov["chapters"]:
                    if oc["num"] == ch["num"]:
                        odata = oc
                        break
            entry = {
                "num": ch["num"],
                "title": ch["title"],
                "keywords": odata["keywords"] if odata else extract_keywords(ch["title"], 8),
                "characters": odata["characters"] if odata else list(find_character_names(ch["title"]))
            }
            outline_flat.append(entry)

    # 解析正文
    actual_chapters = parse_chapters_dir(args.chapters)
    if not actual_chapters:
        print("❌ 未找到正文章节文件", file=sys.stderr)
        sys.exit(1)

    # 执行检测
    title_results = check_title_match(outline_flat, actual_chapters)
    keyword_results = check_keyword_coverage(outline_flat, actual_chapters)
    progress_results, total_outline, max_actual = check_progress_drift(volumes, actual_chapters)
    character_results = check_character_presence(outline_flat, actual_chapters, args.known_characters)
    trend, trend_points = calculate_drift_trend(title_results)

    # 生成汇总统计
    summary = generate_summary(title_results, keyword_results, character_results,
                               progress_results, actual_chapters, volumes)

    # --fix-suggest 模式
    if args.fix_suggest:
        fix_suggestions = generate_fix_suggestions(
            title_results, keyword_results, character_results,
            progress_results, summary, volumes, actual_chapters, outline_flat
        )
        if args.json:
            report["fix_suggestions"] = fix_suggestions
        else:
            print(format_fix_suggestions(fix_suggestions))

    if args.json:
        report = {
            "summary": {
                "total_outline": total_outline,
                "total_actual": max_actual,
                "trend": trend,
                "actual_chapters": len(actual_chapters),
                "avg_drift": summary["avg_drift"],
                "trend_direction": summary["trend_direction"],
                "vol_summary": summary["vol_summary"]
            },
            "progress_drift": progress_results,
            "title_match": title_results,
            "keyword_coverage": keyword_results,
            "character_presence": character_results,
            "trend_points": trend_points,
            "chapter_drift_scores": {str(k): v for k, v in summary["chapter_scores"].items()}
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        report = format_report(title_results, keyword_results, progress_results,
                             character_results, trend, trend_points, total_outline, max_actual)
        print(report)
        # 追加汇总统计
        print(format_summary_block(summary))

if __name__ == "__main__":
    main()
