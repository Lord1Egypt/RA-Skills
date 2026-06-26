#!/usr/bin/env python3
"""
章节开头吸引力评分脚本 v2.2.1
扫描正文目录，取每章前300字，识别开头类型并评分吸引力

用法：
  python3 opening_score.py --novel-dir <正文目录>
  python3 opening_score.py --novel-dir <正文目录> --top-n 5 --suggest
  python3 opening_score.py --novel-dir <正文目录> --format json

功能：
  1. 开头类型识别：对话/动作/悬念/环境/叙述
  2. 吸引力评分 0-100（加分/扣分机制）
  3. 钩子检测：前300字是否有让读者想继续的元素
  4. --suggest：改善建议
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "v2.2.1"

# ============================================================
# 开头类型定义
# ============================================================

# 每种类型的识别关键词/模式及基础分
OPENING_TYPES: Dict[str, Dict[str, Any]] = {
    "对话": {
        "base_score": 80,
        "patterns": [r'^["「"『].*["」\']', r'^[^\n]{0,5}[说叫喊吼笑道哭骂问答嘀嘟喃吟叹哼]\s*[：:]\s*["「"『]'],
        "desc": "以对话开场，直接进入场景",
    },
    "动作": {
        "base_score": 75,
        "patterns": [r'^(他|她|它|我|你|那人|少年|老者|青年)\s*(猛|突|飞|冲|跑|扑|打|踢|拔|抓|挥|跳|闪|翻)'],
        "desc": "以动作描写开场，动态画面感",
    },
    "悬念": {
        "base_score": 85,
        "patterns": [r'^(为什么|难道|怎么回事|不可能|怎么|这.*不可能|谁|究竟|到底|什么情况|奇怪)'],
        "desc": "以悬念/疑问开场，引发好奇",
    },
    "环境": {
        "base_score": 60,
        "patterns": [r'^(天|月|日|风|雨|雪|夜|晨|暮|阳|云|雾|山|河|海|城|街|巷|楼|窗外)'],
        "desc": "以环境描写开场，渲染氛围",
    },
    "叙述": {
        "base_score": 55,
        "patterns": [],  # 默认类型
        "desc": "以平铺叙述开场",
    },
}

# 加分项
BONUS_RULES: List[Dict[str, Any]] = [
    {"name": "含人名", "pattern": r'[\u4e00-\u9fff]{2,4}(说|想|看|走|跑|站|坐|拿|放|握|转|回|笑|哭|叫)', "score": 5, "desc": "开头出现具体人名"},
    {"name": "含冲突", "pattern": r'(冲突|吵架|打架|争吵|威胁|危险|杀了|死|跑|逃|追|求饶|救命|不可能|骗|背叛)', "score": 10, "desc": "开头包含冲突元素"},
    {"name": "含具体信息", "pattern": r'\d+[年月日号时点分秒]|(昨天|今天|明天|上周|下周|刚才|刚才|此时|此时此刻)', "score": 5, "desc": "开头包含具体时间/数字"},
    {"name": "含对话", "pattern": r'["「"『]', "score": 3, "desc": "开头出现对话"},
    {"name": "短句开场", "pattern": None, "score": 5, "desc": "首句≤15字", "check": "short_first_sentence"},
]

# 扣分项
PENALTY_RULES: List[Dict[str, Any]] = [
    {"name": "无具体信息", "pattern": None, "score": -10, "desc": "前300字缺乏具体信息", "check": "no_specific_info"},
    {"name": "大量背景", "pattern": None, "score": -15, "desc": "前300字大量背景铺垫", "check": "heavy_background"},
]

# 钩子检测关键词
HOOK_PATTERNS: List[Dict[str, Any]] = [
    {"pattern": r'(竟然|居然|没想到|不可能|怎么会|怎么可能)', "name": "意外反转"},
    {"pattern": r'(但是|然而|可是|不过|偏偏)', "name": "转折"},
    {"pattern": r'(秘密|真相|隐瞒|骗局|阴谋|陷阱)', "name": "秘密揭示"},
    {"pattern": r'(危险|威胁|杀|死|血|疼|痛)', "name": "危机"},
    {"pattern": r'(不知|不知道|不懂|不明白|疑惑|奇怪)', "name": "疑问"},
    {"pattern": r'(突然|猛然|忽然|一瞬间)', "name": "突发"},
    {"pattern": r'(终于|总算|等了|盼望)', "name": "期待"},
]


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


def get_opening_text(content: str, char_limit: int = 300) -> str:
    """提取正文前N字（去除标题行）"""
    lines = content.strip().split('\n')
    # 跳过标题行（以#开头）
    body_lines = []
    for line in lines:
        if line.strip().startswith('#'):
            continue
        body_lines.append(line)
    body = '\n'.join(body_lines).strip()
    return body[:char_limit]


def list_chapter_files(novel_dir: str) -> List[Tuple[int, str, str]]:
    """列出章节文件，返回 (章节号, 文件名, 文件路径) 列表"""
    if not os.path.isdir(novel_dir):
        print(f"[错误] 目录不存在: {novel_dir}")
        return []
    chapters: List[Tuple[int, str, str]] = []
    for f in sorted(os.listdir(novel_dir)):
        if not (f.endswith('.md') or f.endswith('.txt')):
            continue
        match = re.search(r'第(\d+)章', f)
        if match:
            num = int(match.group(1))
            chapters.append((num, f, os.path.join(novel_dir, f)))
    chapters.sort(key=lambda x: x[0])
    return chapters


# ============================================================
# 核心分析函数
# ============================================================

def detect_opening_type(text: str) -> Tuple[str, int]:
    """识别开头类型，返回 (类型名, 基础分)"""
    first_line = text.split('\n')[0].strip() if text else ""
    for type_name, config in OPENING_TYPES.items():
        if type_name == "叙述":
            continue  # 叙述是默认类型
        for pattern in config["patterns"]:
            if re.search(pattern, first_line):
                return type_name, config["base_score"]
    return "叙述", OPENING_TYPES["叙述"]["base_score"]


def check_short_first_sentence(text: str) -> bool:
    """首句是否≤15字"""
    first_line = text.split('\n')[0].strip() if text else ""
    # 取第一个句号/感叹号/问号前的内容
    sentence = re.split(r'[。！？\n]', first_line)[0]
    return len(sentence) <= 15 and len(sentence) > 0


def check_no_specific_info(text: str) -> bool:
    """是否缺乏具体信息"""
    # 检查是否有人名、具体地点、时间、数字
    has_name = bool(re.search(r'[\u4e00-\u9fff]{2,4}(说(?!明|是|出|到|起|过)|想|看|走|站|坐|是)', text))
    has_place = bool(re.search(r'(市|县|镇|村|街|路|楼|室|房|校|园|厂|公司|店)', text))
    has_time = bool(re.search(r'\d+[年月日号时点分秒]|(今天|昨天|明天|早上|下午|晚上|中午|凌晨)', text))
    has_detail = bool(re.search(r'\d+', text))
    return not (has_name or has_place or has_time or has_detail)


def check_heavy_background(text: str) -> bool:
    """是否有大量背景铺垫"""
    sentences = re.split(r'[。！？\n]', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    if not sentences:
        return False
    bg_keywords = r'(背景|历史|由来|传说|据说|自古以来|从前|很久以前|曾经|向来|一直|原本|本来|事实上|实际上|总而言之|众所周知|大家知道|众所周知)'
    bg_count = sum(1 for s in sentences if re.search(bg_keywords, s))
    # 超过一半句子是背景描述
    return bg_count > len(sentences) * 0.5


def calculate_score(text: str) -> Tuple[int, str, List[str], List[str]]:
    """计算吸引力评分
    返回 (分数, 开头类型, 加分项列表, 扣分项列表)
    """
    opening_type, base_score = detect_opening_type(text)
    bonuses: List[str] = []
    penalties: List[str] = []
    score = base_score

    # 加分项
    for rule in BONUS_RULES:
        if rule.get("check") == "short_first_sentence":
            if check_short_first_sentence(text):
                score += rule["score"]
                bonuses.append(f"{rule['name']} +{rule['score']}")
        elif rule["pattern"] and re.search(rule["pattern"], text):
            score += rule["score"]
            bonuses.append(f"{rule['name']} +{rule['score']}")

    # 扣分项
    for rule in PENALTY_RULES:
        if rule.get("check") == "no_specific_info":
            if check_no_specific_info(text):
                score += rule["score"]
                penalties.append(f"{rule['name']} {rule['score']}")
        elif rule.get("check") == "heavy_background":
            if check_heavy_background(text):
                score += rule["score"]
                penalties.append(f"{rule['name']} {rule['score']}")

    # 钳制到0-100
    score = max(0, min(100, score))
    return score, opening_type, bonuses, penalties


def detect_hooks(text: str) -> List[str]:
    """检测钩子元素"""
    hooks: List[str] = []
    for h in HOOK_PATTERNS:
        if re.search(h["pattern"], text):
            hooks.append(h["name"])
    return hooks


def generate_suggestions(score: int, opening_type: str, bonuses: List[str],
                         penalties: List[str], hooks: List[str]) -> List[str]:
    """生成改善建议"""
    suggestions: List[str] = []
    if opening_type == "叙述" and score < 70:
        suggestions.append("建议用对话或悬念开场，叙述型开头吸引力偏低")
    if opening_type == "环境" and score < 65:
        suggestions.append("环境描写开头容易劝退，建议在前50字内引入人物或事件")
    if "无具体信息" in str(penalties):
        suggestions.append("添加具体人名、地点或时间，让读者快速代入")
    if "大量背景" in str(penalties):
        suggestions.append("背景铺垫太多，建议把背景拆散到对话和动作中自然带出")
    if not hooks:
        suggestions.append("前300字缺少钩子，建议加入悬念、转折或冲突元素")
    if score >= 80:
        suggestions.append("开头吸引力不错，保持节奏")
    if score < 50:
        suggestions.append("开头严重缺乏吸引力，建议重写前300字")
    return suggestions


# ============================================================
# 报告输出
# ============================================================

def analyze_chapter(filepath: str) -> Dict[str, Any]:
    """分析单个章节"""
    content = read_file(filepath)
    if not content:
        return {"error": f"无法读取: {filepath}"}
    opening = get_opening_text(content, 300)
    if not opening.strip():
        return {"error": "正文为空"}

    score, opening_type, bonuses, penalties = calculate_score(opening)
    hooks = detect_hooks(opening)
    suggestions = generate_suggestions(score, opening_type, bonuses, penalties, hooks)

    return {
        "opening_type": opening_type,
        "score": score,
        "bonuses": bonuses,
        "penalties": penalties,
        "hooks": hooks,
        "suggestions": suggestions,
        "opening_preview": opening[:80] + ("..." if len(opening) > 80 else ""),
    }


def format_text_report(results: List[Dict[str, Any]], suggest: bool = False) -> str:
    """格式化文本报告"""
    lines: List[str] = []
    lines.append("=" * 60)
    lines.append(f"  章节开头吸引力评分报告  {VERSION}")
    lines.append("=" * 60)

    if not results:
        lines.append("\n未找到章节文件。")
        return "\n".join(lines)

    # 统计
    scores = [r.get("score", 0) for r in results if "score" in r]
    avg = sum(scores) / len(scores) if scores else 0
    lines.append(f"\n📊 总计 {len(results)} 章 | 平均分 {avg:.1f}")
    lines.append("")

    for r in results:
        ch = r.get("chapter", "?")
        if "error" in r:
            lines.append(f"第{ch}章: ❌ {r['error']}")
            continue
        score = r["score"]
        bar = "█" * (score // 5) + "░" * (20 - score // 5)
        emoji = "🟢" if score >= 75 else "🟡" if score >= 55 else "🔴"
        lines.append(f"第{ch}章 | {emoji} {score:3d}分 | {bar} | {r['opening_type']}")
        if r.get("hooks"):
            lines.append(f"  钩子: {', '.join(r['hooks'])}")
        if r.get("bonuses"):
            lines.append(f"  加分: {', '.join(r['bonuses'])}")
        if r.get("penalties"):
            lines.append(f"  扣分: {', '.join(r['penalties'])}")
        lines.append(f"  预览: {r.get('opening_preview', '')}")
        if suggest and r.get("suggestions"):
            for s in r["suggestions"]:
                lines.append(f"  💡 {s}")
        lines.append("")

    return "\n".join(lines)


def run_score(novel_dir: str, top_n: Optional[int] = None,
              suggest: bool = False, fmt: str = "text") -> str:
    """主评分流程"""
    chapters = list_chapter_files(novel_dir)
    results: List[Dict[str, Any]] = []

    for num, fname, fpath in chapters:
        r = analyze_chapter(fpath)
        r["chapter"] = num
        r["filename"] = fname
        results.append(r)

    # 按分数排序（降序）
    results.sort(key=lambda x: x.get("score", 0), reverse=True)

    if top_n:
        results = results[:top_n]

    if fmt == "json":
        return json.dumps({"version": VERSION, "results": results}, ensure_ascii=False, indent=2)
    return format_text_report(results, suggest)


# ============================================================
# CLI 入口
# ============================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="章节开头吸引力评分")
    parser.add_argument("--novel-dir", required=True, help="正文目录路径")
    parser.add_argument("--top-n", type=int, default=None, help="只显示得分最高的N章")
    parser.add_argument("--suggest", action="store_true", help="输出改善建议")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="输出格式")
    parser.add_argument("--version", action="version", version=f"opening_score {VERSION}")
    args = parser.parse_args()

    output = run_score(args.novel_dir, args.top_n, args.suggest, args.format)
    print(output)


if __name__ == "__main__":
    main()
