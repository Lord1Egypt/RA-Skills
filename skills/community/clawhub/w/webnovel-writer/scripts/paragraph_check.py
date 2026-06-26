#!/usr/bin/env python3
"""
段落长度检测脚本 v2.2.1
检测段落长度是否符合番茄小说风格（短段、快节奏、视觉留白多）

用法：
  python3 paragraph_check.py --novel-dir <正文目录>
  python3 paragraph_check.py --novel-dir <正文目录> --suggest
  python3 paragraph_check.py --novel-dir <正文目录> --format json

检查项：
  1. 过长段落警告（>150字）
  2. 连续长段落节奏过重（>3段>100字）
  3. 视觉节奏检测（平均段落长度、长短交替）
  4. "墙文字"检测（连续无对话/动作的场景描写、连续超长段）
  5. 修改建议（--suggest）
"""

import os
import re
import json
import argparse
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

VERSION = "v2.2.1"

# ============================================================
# 常量
# ============================================================

# 番茄小说最佳段落字数范围
OPTIMAL_MIN = 30
OPTIMAL_MAX = 80
# 默认最长段落警告阈值
DEFAULT_MAX_PARAGRAPH = 150
# 连续长段落阈值（字数 > 此值算长段）
LONG_PARAGRAPH_THRESHOLD = 100
# 连续长段落触发警告的数量
CONSECUTIVE_LONG_COUNT = 3
# 连续无对话/动作段落数量触发"墙文字"
WALL_TEXT_DIALOGUE_GAP = 5
# 连续超长段触发"墙文字"
WALL_TEXT_LONG_GAP = 3
# 番茄小说每章段落建议范围
PARAGRAPH_COUNT_MIN = 15
PARAGRAPH_COUNT_MAX = 40

# 对话标记
DIALOGUE_MARKERS = set('"\u201c\u201d\u300c\u300d')
# 动作关键词（简短列表，表示有动作描写）
ACTION_PATTERNS = re.compile(
    r'(?:走|跑|坐|站|拿|放|推|拉|打|抓|握|拍|踢|跳|蹲|躺|转|回头|点头|摇头|挥手'
    r'|转身|起身|站起|坐下|抬手|伸手|低头|抬头|闭上|睁开|握拳|松开|咬|皱眉|叹气'
    r'|咳嗽|深呼吸|苦笑|冷笑|微笑|大笑|愣|停|挡|躲|闪|撞|推门|开门|关门|扔|摔)'
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
    """统计中文字符数（排除标点和空格）"""
    return len(re.findall(r'[\u4e00-\u9fff]', text))


def list_chapters(dir_path: str) -> List[Tuple[int, str, str]]:
    """列出章节文件，按章节号排序"""
    if not os.path.isdir(dir_path):
        print(f"[错误] 正文目录不存在: {dir_path}")
        return []
    chapters = []
    seen = {}
    for f in sorted(os.listdir(dir_path)):
        if f.endswith('.md') or f.endswith('.txt'):
            match = re.search(r'第(\d+)章', f)
            if match:
                num = int(match.group(1))
                if num in seen:
                    old_f = seen[num]
                    if '_' in f and '_' not in old_f:
                        seen[num] = f
                else:
                    seen[num] = f
    for num, f in sorted(seen.items()):
        chapters.append((num, os.path.join(dir_path, f), f))
    return chapters


def split_paragraphs(content: str) -> List[str]:
    """将章节内容按段落拆分（空行分隔）"""
    # 去除标题行
    lines = content.split('\n')
    non_title_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            continue
        non_title_lines.append(line)

    # 按空行分段
    text = '\n'.join(non_title_lines)
    raw_paragraphs = re.split(r'\n\s*\n', text)

    # 进一步处理：每个段落内部可能有换行，合并并清理
    paragraphs = []
    for p in raw_paragraphs:
        p = p.strip()
        # 合并段内换行
        p = re.sub(r'\n+', '', p)
        # 去除首尾空白
        p = p.strip()
        if p and len(p) > 1:  # 忽略单字符段落
            paragraphs.append(p)
    return paragraphs


def has_dialogue(paragraph: str) -> bool:
    """判断段落是否包含对话"""
    return any(ch in paragraph for ch in DIALOGUE_MARKERS)


def has_action(paragraph: str) -> bool:
    """判断段落是否包含动作描写"""
    return bool(ACTION_PATTERNS.search(paragraph))


# ============================================================
# 检查函数
# ============================================================

def check_paragraph_lengths(
    paragraphs: List[str],
    max_paragraph: int = DEFAULT_MAX_PARAGRAPH,
) -> List[Dict[str, Any]]:
    """检查段落长度，返回过长段落警告"""
    issues = []
    for i, p in enumerate(paragraphs):
        char_count = count_chinese_chars(p)
        if char_count > max_paragraph:
            issues.append({
                'type': '过长段落',
                'severity': 'medium',
                'paragraph_index': i,
                'char_count': char_count,
                'detail': f'第{i+1}段共{char_count}字（建议≤{max_paragraph}字），内容："{p[:50]}..."',
                'suggestion': '建议拆分为2-3个短段，或插入对话/动作打断',
            })
    return issues


def check_consecutive_long_paragraphs(
    paragraphs: List[str],
    threshold: int = LONG_PARAGRAPH_THRESHOLD,
    min_count: int = CONSECUTIVE_LONG_COUNT,
) -> List[Dict[str, Any]]:
    """检测连续长段落（节奏过重）"""
    issues = []
    streak_start = None
    streak = 0

    for i, p in enumerate(paragraphs):
        char_count = count_chinese_chars(p)
        if char_count > threshold:
            if streak == 0:
                streak_start = i
            streak += 1
        else:
            if streak >= min_count:
                issues.append({
                    'type': '节奏过重',
                    'severity': 'medium',
                    'paragraph_range': (streak_start, i - 1),
                    'detail': f'第{streak_start+1}-{i}段连续{streak}段超{threshold}字，阅读节奏过重',
                    'suggestion': '在长段之间插入短句对话或动作描写，打破密集感',
                })
            streak = 0
            streak_start = None

    # 尾部处理
    if streak >= min_count:
        issues.append({
            'type': '节奏过重',
            'severity': 'medium',
            'paragraph_range': (streak_start, len(paragraphs) - 1),
            'detail': f'第{streak_start+1}-{len(paragraphs)}段连续{streak}段超{threshold}字，阅读节奏过重',
            'suggestion': '在长段之间插入短句对话或动作描写，打破密集感',
        })

    return issues


def check_visual_rhythm(
    paragraphs: List[str],
) -> List[Dict[str, Any]]:
    """视觉节奏检测：平均段落长度、长短交替、段落数量"""
    issues = []

    if not paragraphs:
        return issues

    # 统计每段字数
    lengths = [count_chinese_chars(p) for p in paragraphs]
    total_chars = sum(lengths)
    avg_length = total_chars / len(lengths) if lengths else 0

    # 段落数量检测
    para_count = len(paragraphs)
    total_chinese = total_chars

    if total_chinese > 0 and para_count < PARAGRAPH_COUNT_MIN:
        issues.append({
            'type': '段落数量偏少',
            'severity': 'low',
            'detail': f'本章{para_count}段（建议{PARAGRAPH_COUNT_MIN}-{PARAGRAPH_COUNT_MAX}段），'
                      f'总{total_chinese}字，可能缺少视觉留白',
            'suggestion': '将长段拆分，增加段落间的空行，提升手机阅读体验',
        })
    elif total_chinese > 0 and para_count > PARAGRAPH_COUNT_MAX:
        issues.append({
            'type': '段落数量偏多',
            'severity': 'low',
            'detail': f'本章{para_count}段（建议{PARAGRAPH_COUNT_MIN}-{PARAGRAPH_COUNT_MAX}段），'
                      f'总{total_chinese}字，段落可能过于碎片化',
            'suggestion': '适当合并过短段落（<10字），避免阅读节奏太快',
        })

    # 平均段落长度
    if avg_length > 80:
        issues.append({
            'type': '平均段落过长',
            'severity': 'low',
            'detail': f'平均段落长度{avg_length:.0f}字（番茄小说建议30-80字/段）',
            'suggestion': '整体段落偏长，建议拆分长段，增加短段和对话',
        })

    # 长短交替比例
    long_count = sum(1 for l in lengths if l > 60)
    short_count = sum(1 for l in lengths if l <= 30)
    if lengths and long_count > 0 and short_count == 0:
        issues.append({
            'type': '缺少短段交替',
            'severity': 'low',
            'detail': f'本章无短段落（≤30字），全部偏长，节奏单一',
            'suggestion': '在长段间插入短句反应、单句心理活动或短对话，增加节奏变化',
        })
    elif lengths and short_count > 0 and long_count == 0 and total_chinese > 500:
        issues.append({
            'type': '缺少长段',
            'severity': 'low',
            'detail': f'本章无中等以上段落（>60字），全部偏短，可能缺乏深度描写',
            'suggestion': '适当增加中等长度段落（40-80字），用于场景描写或心理刻画',
        })

    return issues


def check_wall_text(
    paragraphs: List[str],
) -> List[Dict[str, Any]]:
    """墙文字检测：连续无对话/动作描写、连续超长段"""
    issues = []

    # 1. 连续无对话/动作的场景描写
    streak = 0
    streak_start = None
    for i, p in enumerate(paragraphs):
        if not has_dialogue(p) and not has_action(p):
            if streak == 0:
                streak_start = i
            streak += 1
        else:
            if streak >= WALL_TEXT_DIALOGUE_GAP:
                issues.append({
                    'type': '墙文字·缺少互动',
                    'severity': 'medium',
                    'paragraph_range': (streak_start, i - 1),
                    'detail': f'第{streak_start+1}-{i}段连续{streak}段无对话/动作描写，纯场景铺陈',
                    'suggestion': '插入角色反应、对话、或动作描写，让读者有"人"的参与感',
                })
            streak = 0
            streak_start = None
    # 尾部
    if streak >= WALL_TEXT_DIALOGUE_GAP:
        issues.append({
            'type': '墙文字·缺少互动',
            'severity': 'medium',
            'paragraph_range': (streak_start, len(paragraphs) - 1),
            'detail': f'第{streak_start+1}-{len(paragraphs)}段连续{streak}段无对话/动作',
            'suggestion': '插入角色反应、对话、或动作描写',
        })

    # 2. 连续超长段（>DEFAULT_MAX_PARAGRAPH字）
    streak = 0
    streak_start = None
    for i, p in enumerate(paragraphs):
        if count_chinese_chars(p) > DEFAULT_MAX_PARAGRAPH:
            if streak == 0:
                streak_start = i
            streak += 1
        else:
            if streak >= WALL_TEXT_LONG_GAP:
                issues.append({
                    'type': '墙文字·超长段堆砌',
                    'severity': 'high',
                    'paragraph_range': (streak_start, i - 1),
                    'detail': f'第{streak_start+1}-{i}段连续{streak}段超{DEFAULT_MAX_PARAGRAPH}字，'
                              f'形成"文字墙"，手机阅读体验极差',
                    'suggestion': '拆分超长段为3-5个短段，插入对话或动作',
                })
            streak = 0
            streak_start = None
    # 尾部
    if streak >= WALL_TEXT_LONG_GAP:
        issues.append({
            'type': '墙文字·超长段堆砌',
            'severity': 'high',
            'paragraph_range': (streak_start, len(paragraphs) - 1),
            'detail': f'末尾{streak}段连续超{DEFAULT_MAX_PARAGRAPH}字，形成"文字墙"',
            'suggestion': '拆分超长段为3-5个短段，插入对话或动作',
        })

    return issues


def generate_suggestions(
    paragraphs: List[str],
    issues: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """生成具体修改建议"""
    suggestions = []

    for i, p in enumerate(paragraphs):
        char_count = count_chinese_chars(p)
        # 针对过长段落给出拆分建议
        if char_count > DEFAULT_MAX_PARAGRAPH:
            # 寻找可拆分点（句号、问号、叹号）
            split_points = [m.end() for m in re.finditer(r'[。！？]', p)]
            if len(split_points) >= 2:
                mid = split_points[len(split_points) // 2]
                suggestions.append({
                    'type': '拆分建议',
                    'paragraph_index': i,
                    'detail': f'第{i+1}段（{char_count}字）可在"{p[mid-5:mid+5]}"处拆分',
                    'preview_before': p[:30] + '...',
                    'preview_split': f'→ "{p[:mid-1]}" + "{p[mid:]}"',
                })

    # 针对墙文字给出加对话建议
    wall_issues = [iss for iss in issues if iss['type'].startswith('墙文字')]
    for iss in wall_issues:
        if 'paragraph_range' in iss:
            start, end = iss['paragraph_range']
            # 在段落范围中间找一个合适的位置插入对话
            mid = (start + end) // 2
            if mid < len(paragraphs):
                suggestions.append({
                    'type': '添加互动建议',
                    'paragraph_index': mid,
                    'detail': f'在第{mid+1}段附近插入一段对话或角色动作，'
                              f'打破第{start+1}-{end+1}段的纯描写',
                    'preview_before': paragraphs[mid][:40] + '...',
                    'preview_split': '→ 在此段后插入：角色的一句反应或动作',
                })

    return suggestions


# ============================================================
# 统计函数
# ============================================================

def compute_statistics(paragraphs: List[str]) -> Dict[str, Any]:
    """计算段落统计数据"""
    if not paragraphs:
        return {
            'paragraph_count': 0,
            'total_chars': 0,
            'avg_length': 0,
            'min_length': 0,
            'max_length': 0,
            'optimal_count': 0,
            'optimal_ratio': 0,
            'long_count': 0,
            'short_count': 0,
            'dialogue_count': 0,
            'dialogue_ratio': 0,
        }

    lengths = [count_chinese_chars(p) for p in paragraphs]
    total = sum(lengths)
    optimal = sum(1 for l in lengths if OPTIMAL_MIN <= l <= OPTIMAL_MAX)
    long = sum(1 for l in lengths if l > DEFAULT_MAX_PARAGRAPH)
    short = sum(1 for l in lengths if l < 10)
    dialogue = sum(1 for p in paragraphs if has_dialogue(p))

    return {
        'paragraph_count': len(paragraphs),
        'total_chars': total,
        'avg_length': round(total / len(lengths), 1),
        'min_length': min(lengths),
        'max_length': max(lengths),
        'optimal_count': optimal,
        'optimal_ratio': round(optimal / len(lengths), 2),
        'long_count': long,
        'short_count': short,
        'dialogue_count': dialogue,
        'dialogue_ratio': round(dialogue / len(paragraphs), 2),
    }


# ============================================================
# 单章检测
# ============================================================

def check_single_chapter(
    paragraphs: List[str],
    max_paragraph: int = DEFAULT_MAX_PARAGRAPH,
) -> List[Dict[str, Any]]:
    """对单章执行所有段落检查"""
    issues = []
    issues.extend(check_paragraph_lengths(paragraphs, max_paragraph))
    issues.extend(check_consecutive_long_paragraphs(paragraphs))
    issues.extend(check_visual_rhythm(paragraphs))
    issues.extend(check_wall_text(paragraphs))
    return issues


# ============================================================
# 主流程
# ============================================================

def run_check(
    novel_dir: str,
    max_paragraph: int = DEFAULT_MAX_PARAGRAPH,
    suggest: bool = False,
    output_format: str = 'text',
) -> Dict[str, Any]:
    """执行段落长度检测"""
    chapters = list_chapters(novel_dir)
    if not chapters:
        print("[错误] 未找到章节文件")
        return {'error': '未找到章节文件', 'chapters': []}

    results = []
    for num, path, fname in chapters:
        content = read_file(path)
        if not content:
            continue
        paragraphs = split_paragraphs(content)
        issues = check_single_chapter(paragraphs, max_paragraph)
        stats = compute_statistics(paragraphs)

        chapter_result = {
            'chapter': num,
            'filename': fname,
            'statistics': stats,
            'issues': issues,
        }

        if suggest and issues:
            chapter_result['suggestions'] = generate_suggestions(paragraphs, issues)

        results.append(chapter_result)

    # 输出
    if output_format == 'json':
        output = {
            'version': VERSION,
            'novel_dir': novel_dir,
            'max_paragraph': max_paragraph,
            'chapters': results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return output

    # text 格式输出
    print("=" * 60)
    print(f"📐 段落长度检测 {VERSION}")
    print("=" * 60)
    print(f"📂 目录: {novel_dir}")
    print(f"📏 最长段落阈值: {max_paragraph}字")
    print()

    total_issues = 0
    for ch_result in results:
        ch = ch_result['chapter']
        stats = ch_result['statistics']
        issues = ch_result['issues']
        total_issues += len(issues)

        print(f"--- 第{ch}章 ({ch_result['filename']}) ---")
        print(f"  段落: {stats['paragraph_count']}段 | "
              f"总字数: {stats['total_chars']}字 | "
              f"平均: {stats['avg_length']}字/段 | "
              f"最优段落占比: {stats['optimal_ratio']:.0%} | "
              f"含对话: {stats['dialogue_count']}段")

        if not issues:
            print("  ✅ 段落长度无异常")
        else:
            by_type = {}
            for iss in issues:
                t = iss['type']
                by_type.setdefault(t, []).append(iss)
            for t, items in by_type.items():
                emoji = {'过长段落': '📏', '节奏过重': '⚡', '段落数量偏少': '📉',
                         '段落数量偏多': '📈', '平均段落过长': '📊', '缺少短段交替': '🔄',
                         '缺少长段': '📝', '墙文字·缺少互动': '🧱', '墙文字·超长段堆砌': '🧱🧱'
                         }.get(t, '⚠️')
                print(f"  {emoji} {t}（{len(items)}个）")
                for item in items:
                    print(f"    • {item['detail']}")
                    if item.get('suggestion'):
                        print(f"      💡 {item['suggestion']}")

        # 修改建议
        if suggest and 'suggestions' in ch_result:
            print(f"  🔧 修改建议：")
            for s in ch_result['suggestions']:
                print(f"    • [{s['type']}] {s['detail']}")

        print()

    print("=" * 60)
    if total_issues == 0:
        print("✅ 所有章节段落长度检查通过")
    else:
        print(f"📊 共发现 {total_issues} 个段落问题")
    print("=" * 60)

    return {'version': VERSION, 'chapters': results, 'total_issues': total_issues}


def main():
    parser = argparse.ArgumentParser(
        description='段落长度检测脚本 - 检测段落长度是否符合番茄小说风格'
    )
    parser.add_argument('--novel-dir', required=True, help='正文目录路径')
    parser.add_argument('--max-paragraph', type=int, default=DEFAULT_MAX_PARAGRAPH,
                        help=f'最长段落字数警告阈值（默认{DEFAULT_MAX_PARAGRAPH}）')
    parser.add_argument('--suggest', action='store_true', help='输出修改建议')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='输出格式（默认text）')
    parser.add_argument('--version', action='version', version=f'paragraph_check {VERSION}')
    args = parser.parse_args()

    run_check(args.novel_dir, args.max_paragraph, args.suggest, args.format)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 paragraph_check.py --novel-dir <正文目录>")
        print("\n示例:")
        print("  python3 paragraph_check.py --novel-dir 正文/")
        print("  python3 paragraph_check.py --novel-dir 正文/ --suggest --format json")
        sys.exit(1)
    main()
