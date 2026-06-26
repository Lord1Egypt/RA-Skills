#!/usr/bin/env python3
"""
对话标签质量检测脚本 v2.2.1
扫描章节正文，检测对话标签（"他说""她道""他问"等）的使用质量

用法：
  python3 dialogue_tag_check.py --novel-dir <正文目录> [--threshold 15] [--suggest] [--format text|json]

检查项：
  1. 标签频率（每千字标签数）
  2. 标签单调性（连续重复、种类过少）
  3. 标签质量（副词修饰过度）
  4. 对话比例（对话占比）
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import Counter, defaultdict
from typing import Any, Dict, List, Optional, Tuple

VERSION = "v2.2.1"

# ============================================================
# 常量
# ============================================================

# 常见对话标签动词
TAG_VERBS = ["说", "道", "问", "答", "叫", "喊", "吼", "嚷", "嘀咕", "嘟囔",
             "喃喃", "感叹", "叹息", "叹息道", "笑道", "笑", "哭", "怒道",
             "骂", "呵斥", "训斥", "反驳", "追问", "催促", "打断"]

# 对话标签正则：匹配 "X说/道/问..." 模式
# 匹配：他说、她道、老人问、李明笑了笑说 等
DIALOGUE_TAG_PATTERN = re.compile(
    r'[\u4e00-\u9fff]{1,4}'           # 主语（1-4个汉字，人名或代词）
    r'(?:的?声音)?'                    # 可选："的声音"
    r'(?:[\u4e00-\u9fff]{0,2})?'       # 可选修饰
    r'(说|道|问|答|叫|喊|吼|嚷|嘀咕|嘟囔|喃喃|笑[着]?道?|哭[着]?道?|怒道|骂道?|呵斥|训斥|反驳|追问|催促|打断|感叹|叹息)',
    re.UNICODE
)

# 副词修饰标签：XX地+动词
ADVERB_TAG_PATTERN = re.compile(
    r'[\u4e00-\u9fff]{1,3}地(?:说|道|问|答|喊|叫|笑[着]?道?|吼)',
    re.UNICODE
)

# 对话内容正则：引号内文本
DIALOGUE_PATTERN = re.compile(r'[「"「](.*?)[」"」]', re.DOTALL)

# 主语+动词的完整标签（用于单调性检测）
FULL_TAG_PATTERN = re.compile(
    r'([\u4e00-\u9fff]{1,4})(说|道|问|答|叫|喊|吼|嚷|嘀咕|嘟囔|笑[着]?道?|怒道|骂道?|呵斥|训斥|反驳|追问|催促|打断)',
    re.UNICODE
)

# ============================================================
# 工具函数
# ============================================================

def read_file(path: str) -> str:
    """读取文件内容"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[警告] 无法读取 {path}: {e}")
        return ""


def count_chinese_chars(text: str) -> int:
    """统计中文字符数"""
    return sum(1 for ch in text if '\u4e00' <= ch <= '\u9fff')


def list_chapters(dir_path: str) -> List[Tuple[int, str, str]]:
    """列出章节文件，返回 (章节号, 完整路径, 文件名)"""
    if not os.path.isdir(dir_path):
        print(f"[错误] 正文目录不存在: {dir_path}")
        return []
    chapters = []
    for f in sorted(os.listdir(dir_path)):
        if f.endswith('.md') or f.endswith('.txt'):
            match = re.search(r'第(\d+)章', f)
            num = int(match.group(1)) if match else -1
            chapters.append((num, os.path.join(dir_path, f), f))
    chapters.sort(key=lambda x: x[0])
    return chapters


# ============================================================
# 检测函数
# ============================================================

def detect_tags(text: str) -> List[str]:
    """检测文本中的对话标签，返回匹配到的标签列表"""
    return [m.group(0) for m in DIALOGUE_TAG_PATTERN.finditer(text)]


def detect_adverb_tags(text: str) -> List[str]:
    """检测副词修饰的标签"""
    return ADVERB_TAG_PATTERN.findall(text)


def detect_full_tags(text: str) -> List[Tuple[str, str]]:
    """检测完整标签（主语, 动词），用于单调性分析"""
    return [(m.group(1), m.group(2)) for m in FULL_TAG_PATTERN.finditer(text)]


def count_dialogue_chars(text: str) -> int:
    """统计对话内容的字符数"""
    dialogues = DIALOGUE_PATTERN.findall(text)
    return sum(len(d) for d in dialogues)


def check_frequency(tags: List[str], char_count: int, threshold: float) -> Dict[str, Any]:
    """检查标签频率"""
    if char_count == 0:
        return {"tags_per_k": 0, "count": 0, "warnings": []}
    per_k = len(tags) / (char_count / 1000)
    warnings = []
    if per_k > threshold:
        warnings.append(f"标签频率 {per_k:.1f}次/千字，超过阈值 {threshold:.0f}次/千字，建议减少")
    if per_k < 2 and char_count > 500:
        warnings.append(f"标签频率 {per_k:.1f}次/千字 过低，对话可能缺少归属")
    return {"tags_per_k": round(per_k, 2), "count": len(tags), "warnings": warnings}


def check_monotony(tags: List[str], full_tags: List[Tuple[str, str]]) -> Dict[str, Any]:
    """检查标签单调性"""
    warnings = []

    # 连续重复检测
    consecutive_groups = []
    if tags:
        current_tag = tags[0]
        count = 1
        for t in tags[1:]:
            if t == current_tag:
                count += 1
            else:
                consecutive_groups.append((current_tag, count))
                current_tag = t
                count = 1
        consecutive_groups.append((current_tag, count))

    for tag, cnt in consecutive_groups:
        if cnt >= 3:
            warnings.append(f"标签「{tag}」连续出现 {cnt} 次")

    # 种类检测
    verb_types = set(v for _, v in full_tags)
    if len(tags) >= 5 and len(verb_types) <= 2:
        warnings.append(f"标签种类过少（仅 {len(verb_types)} 种动词），建议丰富表达")

    return {"warnings": warnings, "verb_types": sorted(verb_types)}


def check_quality(text: str, tags: List[str]) -> Dict[str, Any]:
    """检查标签质量（副词修饰过度）"""
    adverb_tags = detect_adverb_tags(text)
    warnings = []
    suggestions = []

    if len(tags) > 0 and len(adverb_tags) / max(len(tags), 1) > 0.4:
        warnings.append(f"副词修饰标签占比 {len(adverb_tags)}/{len(tags)} 过高（>{40}%），建议用动作替代")

    # 具体建议
    adverb_counts = Counter(ADVERB_TAG_PATTERN.finditer(text))
    for m in ADVERB_TAG_PATTERN.finditer(text):
        tag = m.group(0)
        suggestions.append(f"「{tag}」→ 建议用动作描写替代，如描写表情、手势等")

    return {"adverb_count": len(adverb_tags), "warnings": warnings, "suggestions": suggestions}


def check_dialogue_ratio(text: str, char_count: int) -> Dict[str, Any]:
    """检查对话占比"""
    if char_count == 0:
        return {"ratio": 0, "dialogue_chars": 0, "warnings": []}
    dialogue_chars = count_dialogue_chars(text)
    ratio = dialogue_chars / char_count
    warnings = []
    if ratio > 0.7:
        warnings.append(f"对话占比 {ratio:.0%} 过高（>70%），可能缺少环境描写和心理活动")
    if ratio < 0.1 and char_count > 500:
        warnings.append(f"对话占比 {ratio:.0%} 过低（<10%），叙事可能偏重描述")
    return {"ratio": round(ratio, 3), "dialogue_chars": dialogue_chars, "warnings": warnings}


# ============================================================
# 主检测流程
# ============================================================

def check_chapter(text: str, threshold: float = 15.0, suggest: bool = False) -> Dict[str, Any]:
    """对单个章节文本执行全量检测"""
    char_count = count_chinese_chars(text)
    tags = detect_tags(text)
    full_tags = detect_full_tags(text)

    result: Dict[str, Any] = {
        "char_count": char_count,
        "tag_count": len(tags),
        "frequency": check_frequency(tags, char_count, threshold),
        "monotony": check_monotony(tags, full_tags),
        "quality": check_quality(text, tags) if suggest else {"adverb_count": len(detect_adverb_tags(text)), "warnings": [], "suggestions": []},
        "dialogue_ratio": check_dialogue_ratio(text, char_count),
    }

    # 汇总警告
    all_warnings = []
    for section in [result["frequency"], result["monotony"], result["quality"], result["dialogue_ratio"]]:
        all_warnings.extend(section.get("warnings", []))
    result["all_warnings"] = all_warnings

    return result


def run(novel_dir: str, threshold: float = 15.0, suggest: bool = False,
        fmt: str = "text") -> Dict[str, Any]:
    """执行全量检测"""
    chapters = list_chapters(novel_dir)
    if not chapters:
        return {"error": f"未找到章节文件: {novel_dir}", "chapters": []}

    results = []
    for num, path, fname in chapters:
        text = read_file(path)
        if not text:
            continue
        r = check_chapter(text, threshold, suggest)
        r["chapter"] = num
        r["filename"] = fname
        results.append(r)

    summary = {
        "total_chapters": len(results),
        "total_warnings": sum(len(r["all_warnings"]) for r in results),
        "threshold": threshold,
        "version": VERSION,
        "chapters": results,
    }
    return summary


def format_text_output(summary: Dict[str, Any]) -> str:
    """格式化文本输出"""
    lines = []
    lines.append(f"=== 对话标签质量检测 {VERSION} ===")
    lines.append(f"共扫描 {summary['total_chapters']} 章，发现 {summary['total_warnings']} 条警告")
    lines.append("")

    for ch in summary["chapters"]:
        lines.append(f"📖 第{ch['chapter']}章 ({ch['filename']})")
        lines.append(f"   字数: {ch['char_count']}  标签数: {ch['tag_count']}  "
                     f"频率: {ch['frequency']['tags_per_k']}次/千字  "
                     f"对话占比: {ch['dialogue_ratio']['ratio']:.0%}")
        if ch["all_warnings"]:
            for w in ch["all_warnings"]:
                lines.append(f"   ⚠️  {w}")
        if ch["quality"].get("suggestions"):
            for s in ch["quality"]["suggestions"][:5]:
                lines.append(f"   💡 {s}")
        lines.append("")

    return "\n".join(lines)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="对话标签质量检测")
    parser.add_argument("--novel-dir", required=True, help="正文章节目录")
    parser.add_argument("--threshold", type=float, default=15.0, help="标签频率阈值（次/千字，默认15）")
    parser.add_argument("--suggest", action="store_true", help="输出替代建议")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--version", action="version", version=f"%(prog)s {VERSION}")
    args = parser.parse_args()

    summary = run(args.novel_dir, args.threshold, args.suggest, args.format)

    if args.format == "json":
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(format_text_output(summary))

    # 有警告时返回非零
    sys.exit(1 if summary["total_warnings"] > 0 else 0)


if __name__ == "__main__":
    main()
