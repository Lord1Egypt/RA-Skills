#!/usr/bin/env python3
"""
章节节奏检测脚本 v1
扫描正文目录，分析每章的紧张度、钩子密度、情感基调，检测节奏问题

用法：
  python3 rhythm_check.py <正文目录>

检测项：
  1. 钩子密度检测（悬念/反转/金句标记词频率）
  2. 节奏曲线生成（紧张度评分：钩子密度 + 对话比例 + 短句比例）
  3. 连续太平检测（连续3章紧张度低于阈值 → 报警）
  4. 连续太紧检测（连续3章紧张度高于阈值 → 报警）
  5. 情感单调检测（连续几章情绪基调相同 → 提醒）
  6. 章节长度波动（连续短章或连续长章 → 提醒）
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

# ============================================================
# 工具函数
# ============================================================

def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"[警告] 无法读取 {path}: {e}")
        return ""

def list_chapters(dir_path: str, include_unnumbered: bool = False) -> List[Tuple[int, str, str]]:
    if not os.path.isdir(dir_path):
        print(f"[错误] 正文目录不存在: {dir_path}")
        return []
    chapters = []
    seen = {}  # 同章节号去重
    unnumbered_idx = -1
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
            elif include_unnumbered and f not in ('README.md', '目录.md', '大纲.md'):
                chapters.append((unnumbered_idx, os.path.join(dir_path, f), f))
                unnumbered_idx -= 1
    for num, f in sorted(seen.items()):
        chapters.append((num, os.path.join(dir_path, f), f))
    chapters.sort(key=lambda x: x[0])
    return chapters

def normalize_text(text: str) -> str:
    text = text.replace('\u3000', ' ')
    text = re.sub(r'[ \t]+', ' ', text)
    return text

# ============================================================
# 钩子标记词库
# ============================================================

HOOK_SUSPENSE = [
    '愣住', '瞳孔收缩', '瞳孔骤然', '愣了', '倒吸一口凉气',
    '不敢相信', '心跳漏了一拍', '背后一凉', '脊背发凉',
    '怎么回事', '不可能', '为什么', '谁', '什么意思',
    '等等', '不对', '可是', '然而', '但是',
    '悬念', '谜团', '秘密', '隐藏', '真相',
]

HOOK_REVERSAL = [
    '没想到', '没想到的是', '出乎意料', '没想到的是',
    '反转', '颠覆', '原来', '事实上', '实际上',
    '并非', '根本不是', '恰恰相反', '完全不同',
    '直到', '才知道', '才明白', '才发现',
]

HOOK_EMOTION = [
    '眼泪', '哭了', '哭了', '鼻酸', '哽咽',
    '颤抖', '深吸一口气', '咬了咬牙', '攥紧',
    '沉默了很久', '一句话都说不出来',
    '谢谢你', '对不起', '再见', '最后一次',
]

HOOK_THRILL = [
    '脚步声', '黑暗中', '阴影', '走廊尽头',
    '灯灭了', '门开了', '窗户', '身后',
    '失踪', '尸体', '血', '杀',
    '危险', '逃跑', '追', '躲',
]

HOOK_SATISFY = [
    '估值', '翻了', '暴涨', '打脸',
    '所有人沉默', '哑口无言', '脸色难看',
    '佩服', '天才', '不可思议',
]

ALL_HOOK_WORDS = {
    'suspense': HOOK_SUSPENSE,
    'reversal': HOOK_REVERSAL,
    'emotion': HOOK_EMOTION,
    'thrill': HOOK_THRILL,
    'satisfy': HOOK_SATISFY,
}

# 情感基调标记词
EMOTION_TENSE = ['紧张', '恐惧', '危险', '威胁', '死', '杀', '逃', '追',
                 '心跳加速', '手心出汗', '背后发凉', '不寒而栗', '毛骨悚然',
                 '颤抖', '尖叫', '崩溃', '绝望', '窒息']
EMOTION_RELAX = ['笑了', '轻松', '温暖', '阳光', '咖啡',
                 '周末', '散步', '闲聊', '开玩笑', '哈哈',
                 '搞笑', '幽默', '吃', '喝', '睡']
EMOTION_SAD = ['哭', '泪', '悲伤', '遗憾', '失去', '再见',
               '永别', '怀念', '想念', '孤独', '寂寞', '沉默']

# --emotion-track 四维情绪词库
EMOTION_POSITIVE = [
    '笑', '开心', '高兴', '快乐', '幸福', '温暖', '阳光',
    '喜欢', '爱', '希望', '美好', '甜蜜', '温馨', '安心',
    '满足', '感激', '感动', '欣慰', '轻松', '舒服', '舒服',
    '哈哈', '嘻嘻', '棒', '好', '美', '甜', '暖',
]
EMOTION_NEGATIVE = [
    '恨', '怒', '怒火', '愤怒', '讨厌', '恶心', '厌恶',
    '烦躁', '厌烦', '心烦', '暴躁', '暴怒', '发火', '发怒',
    '黑脸', '甩门', '拍桌', '瞪', '吼', '骂', '吵',
]
EMOTION_ANXIOUS = [
    '紧张', '焦虑', '不安', '担心', '害怕', '恐惧', '惊恐',
    '慌', '慌张', '慌乱', '颤抖', '冷汗', '心跳', '窒息',
    '背后发凉', '脊背发凉', '不寒而栗', '毛骨悚然', '倒吸',
    '危险', '威胁', '死', '杀', '逃', '追', '尖叫',
]
EMOTION_SORROW = [
    '哭', '泪', '悲伤', '难过', '心酸', '哽咽', '抽泣',
    '遗憾', '失去', '再见', '永别', '怀念', '想念', '思念',
    '孤独', '寂寞', '沉默', '无奈', '叹气', '叹息', '落寞',
    '苍白', '空洞', '黯然', '消散', '化为', '光点',
]

# ============================================================
# 分析函数
# ============================================================

def count_dialogue_ratio(content: str) -> float:
    """计算对话占比（引号内文字 / 总中文字数）"""
    # 提取引号内内容
    dialogue_chars = 0
    in_quote = False
    for ch in content:
        if ch in '\u201c\u300c"':
            in_quote = True
        elif ch in '\u201d\u300d"':
            in_quote = False
        elif in_quote and '\u4e00' <= ch <= '\u9fff':
            dialogue_chars += 1

    total = len(re.findall(r'[\u4e00-\u9fff]', content))
    if total == 0:
        return 0
    return dialogue_chars / total

def count_short_sentence_ratio(content: str) -> float:
    """短句占比（≤15字的句子）"""
    sentences = re.split(r'[。！？\n]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
    if not sentences:
        return 0
    short_count = sum(1 for s in sentences if len(s) <= 15)
    return short_count / len(sentences)

def count_hook_density(content: str) -> float:
    """钩子密度（每千字的钩子词命中数）"""
    total_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    if total_chars == 0:
        return 0, {}

    counts_by_type = {}
    total_hits = 0
    for hook_type, words in ALL_HOOK_WORDS.items():
        type_hits = 0
        for w in words:
            type_hits += content.count(w)
        counts_by_type[hook_type] = type_hits
        total_hits += type_hits

    density = total_hits / (total_chars / 1000)
    return density, counts_by_type

def detect_emotion_tone(content: str) -> str:
    """检测章节主导情绪基调"""
    scores = {
        'tense': sum(content.count(w) for w in EMOTION_TENSE),
        'relax': sum(content.count(w) for w in EMOTION_RELAX),
        'sad': sum(content.count(w) for w in EMOTION_SAD),
    }
    total = sum(scores.values())
    if total == 0:
        return 'neutral', scores
    dominant = max(scores, key=scores.get)
    if scores[dominant] / total < 0.4:
        return 'mixed', scores
    return dominant, scores

def compute_tension(density: float, dialogue_ratio: float, short_ratio: float, hook_types: int) -> float:
    """计算紧张度评分（0-100）

    权重：
    - 钩子密度 40%
    - 对话比例 20%（对话多→节奏快）
    - 短句比例 20%（短句多→节奏快）
    - 反转/惊悚权重加成 20%
    """
    # 钩子密度归一化（经验值：0-20的range映射到0-40）
    density_score = min(density / 20.0, 1.0) * 40

    # 对话比例归一化（0-0.5 → 0-20）
    dialogue_score = min(dialogue_ratio / 0.5, 1.0) * 20

    # 短句比例归一化（0-0.5 → 0-20）
    short_score = min(short_ratio / 0.5, 1.0) * 20

    # 反转+惊悚加成
    thriller_bonus = (hook_types.get('reversal', 0) + hook_types.get('thrill', 0))
    thriller_score = min(thriller_bonus / 10.0, 1.0) * 20

    return round(density_score + dialogue_score + short_score + thriller_score, 1)

# ============================================================
# 主检测逻辑
# ============================================================

def run_check(text_dir: str) -> List[Dict[str, Any]]:
    print("=" * 60)
    print("🎵 章节节奏检测 v1")
    print("=" * 60)

    chapters = list_chapters(text_dir)
    if not chapters:
        print("[错误] 未找到章节文件")
        return None

    print(f"\n📖 找到 {len(chapters)} 个章节（第{chapters[0][0]}章 ~ 第{chapters[-1][0]}章）")

    # 逐章分析
    chapter_data = []
    print("\n⏳ 正在分析...")

    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        if not content:
            continue

        char_count = len(re.findall(r'[\u4e00-\u9fff]', content))
        density, hook_types = count_hook_density(content)
        dialogue_ratio = count_dialogue_ratio(content)
        short_ratio = count_short_sentence_ratio(content)
        emotion, emotion_scores = detect_emotion_tone(content)
        tension = compute_tension(density, dialogue_ratio, short_ratio, hook_types)

        chapter_data.append({
            'chapter': num,
            'filename': fname,
            'char_count': char_count,
            'hook_density': round(density, 2),
            'hook_types': hook_types,
            'dialogue_ratio': round(dialogue_ratio, 3),
            'short_sentence_ratio': round(short_ratio, 3),
            'emotion': emotion,
            'emotion_scores': emotion_scores,
            'tension': tension,
        })

    if not chapter_data:
        print("[错误] 没有可分析的章节内容")
        return None

    # 输出节奏曲线
    print(f"\n{'='*60}")
    print("📈 节奏曲线")
    print(f"{'='*60}\n")

    tensions = [c['tension'] for c in chapter_data]
    avg_tension = sum(tensions) / len(tensions) if tensions else 50
    low_threshold = max(avg_tension * 0.5, 20)
    high_threshold = min(avg_tension * 1.5, 80)

    for c in chapter_data:
        t = c['tension']
        bar_len = int(t / 2.5)
        bar = '█' * bar_len
        emoji = '🔴' if t >= high_threshold else ('🟢' if t <= low_threshold else '🟡')
        emotion_map = {'tense': '⚡紧张', 'relax': '😊轻松', 'sad': '😢悲伤', 'neutral': '😐平淡', 'mixed': '🔄混合'}
        print(f"  第{c['chapter']:03d}章 {emoji} {t:5.1f} {bar:<40s}  {emotion_map[c['emotion']]}  {c['char_count']}字  钩子{c['hook_density']:.1f}/千字")

    # 检测问题
    issues = []

    # 1. 连续太平检测
    consecutive_low = 0
    low_start = 0
    for i, c in enumerate(chapter_data):
        if c['tension'] <= low_threshold:
            consecutive_low += 1
            if consecutive_low == 1:
                low_start = c['chapter']
        else:
            if consecutive_low >= 3:
                issues.append({
                    'type': '连续太平',
                    'severity': 'high',
                    'detail': f'第{low_start}-{chapter_data[i-1]["chapter"]}章连续{consecutive_low}章紧张度偏低（均≤{low_threshold:.0f}）',
                    'suggestion': '增加悬念、反转或冲突，避免读者失去兴趣'
                })
            consecutive_low = 0
    if consecutive_low >= 3:
        issues.append({
            'type': '连续太平',
            'severity': 'high',
            'detail': f'第{low_start}-{chapter_data[-1]["chapter"]}章连续{consecutive_low}章紧张度偏低（均≤{low_threshold:.0f}）',
            'suggestion': '增加悬念、反转或冲突，避免读者失去兴趣'
        })

    # 2. 连续太紧检测
    consecutive_high = 0
    high_start = 0
    for i, c in enumerate(chapter_data):
        if c['tension'] >= high_threshold:
            consecutive_high += 1
            if consecutive_high == 1:
                high_start = c['chapter']
        else:
            if consecutive_high >= 3:
                issues.append({
                    'type': '连续太紧',
                    'severity': 'medium',
                    'detail': f'第{high_start}-{chapter_data[i-1]["chapter"]}章连续{consecutive_high}章紧张度偏高（均≥{high_threshold:.0f}）',
                    'suggestion': '插入舒缓段落（日常/幽默/情感），给读者喘息空间'
                })
            consecutive_high = 0
    if consecutive_high >= 3:
        issues.append({
            'type': '连续太紧',
            'severity': 'medium',
            'detail': f'第{high_start}-{chapter_data[-1]["chapter"]}章连续{consecutive_high}章紧张度偏高（均≥{high_threshold:.0f}）',
            'suggestion': '插入舒缓段落（日常/幽默/情感），给读者喘息空间'
        })

    # 3. 情感单调检测
    consecutive_same_emotion = 0
    same_start = 0
    prev_emotion = None
    for i, c in enumerate(chapter_data):
        if c['emotion'] in ('tense', 'relax', 'sad') and c['emotion'] == prev_emotion:
            consecutive_same_emotion += 1
        else:
            if consecutive_same_emotion >= 4 and prev_emotion in ('tense', 'relax', 'sad'):
                emotion_cn = {'tense': '紧张', 'relax': '轻松', 'sad': '悲伤'}
                issues.append({
                    'type': '情感单调',
                    'severity': 'medium',
                    'detail': f'第{same_start}-{chapter_data[i-1]["chapter"]}章连续{consecutive_same_emotion}章情绪基调为"{emotion_cn[prev_emotion]}"',
                    'suggestion': '变换情感基调，避免读者审美疲劳'
                })
            consecutive_same_emotion = 1
            same_start = c['chapter']
            prev_emotion = c['emotion']
    if consecutive_same_emotion >= 4 and prev_emotion in ('tense', 'relax', 'sad'):
        emotion_cn = {'tense': '紧张', 'relax': '轻松', 'sad': '悲伤'}
        issues.append({
            'type': '情感单调',
            'severity': 'medium',
            'detail': f'第{same_start}-{chapter_data[-1]["chapter"]}章连续{consecutive_same_emotion}章情绪基调为"{emotion_cn[prev_emotion]}"',
            'suggestion': '变换情感基调，避免读者审美疲劳'
        })

    # 4. 章节长度波动检测
    char_counts = [c['char_count'] for c in chapter_data]
    avg_chars = sum(char_counts) / len(char_counts) if char_counts else 2000
    short_threshold = avg_chars * 0.5
    long_threshold = avg_chars * 1.8

    # 连续短章
    consecutive_short = 0
    short_start = 0
    for i, c in enumerate(chapter_data):
        if c['char_count'] <= short_threshold and c['char_count'] > 0:
            consecutive_short += 1
            if consecutive_short == 1:
                short_start = c['chapter']
        else:
            if consecutive_short >= 3:
                issues.append({
                    'type': '连续短章',
                    'severity': 'low',
                    'detail': f'第{short_start}-{chapter_data[i-1]["chapter"]}章连续{consecutive_short}章字数偏少（均≤{short_threshold:.0f}字）',
                    'suggestion': '考虑扩充内容或合并短章'
                })
            consecutive_short = 0
    if consecutive_short >= 3:
        issues.append({
            'type': '连续短章',
            'severity': 'low',
            'detail': f'第{short_start}-{chapter_data[-1]["chapter"]}章连续{consecutive_short}章字数偏少（均≤{short_threshold:.0f}字）',
            'suggestion': '考虑扩充内容或合并短章'
        })

    # 连续长章
    consecutive_long = 0
    long_start = 0
    for i, c in enumerate(chapter_data):
        if c['char_count'] >= long_threshold:
            consecutive_long += 1
            if consecutive_long == 1:
                long_start = c['chapter']
        else:
            if consecutive_long >= 3:
                issues.append({
                    'type': '连续长章',
                    'severity': 'low',
                    'detail': f'第{long_start}-{chapter_data[i-1]["chapter"]}章连续{consecutive_long}章字数偏多（均≥{long_threshold:.0f}字）',
                    'suggestion': '考虑拆分长章，读者注意力有限'
                })
            consecutive_long = 0
    if consecutive_long >= 3:
        issues.append({
            'type': '连续长章',
            'severity': 'low',
            'detail': f'第{long_start}-{chapter_data[-1]["chapter"]}章连续{consecutive_long}章字数偏多（均≥{long_threshold:.0f}字）',
            'suggestion': '考虑拆分长章，读者注意力有限'
        })

    # 输出问题摘要
    print(f"\n{'='*60}")
    print("📊 节奏问题报告")
    print(f"{'='*60}")

    if not issues:
        print("\n✅ 节奏控制良好，未发现明显问题")
    else:
        by_severity = {'high': [], 'medium': [], 'low': []}
        for issue in issues:
            by_severity[issue.get('severity', 'medium')].append(issue)

        total = len(issues)
        print(f"\n共发现 {total} 个节奏问题：🔴 严重 {len(by_severity['high'])} ｜ 🟡 中等 {len(by_severity['medium'])} ｜ 🟢 轻微 {len(by_severity['low'])}\n")

        for sev, label, emoji in [('high', '严重', '🔴'), ('medium', '中等', '🟡'), ('low', '轻微', '🟢')]:
            if not by_severity[sev]:
                continue
            by_type = defaultdict(list)
            for issue in by_severity[sev]:
                by_type[issue['type']].append(issue)
            print(f"\n### {emoji} {label}问题")
            for issue_type, items in by_type.items():
                print(f"\n  **{issue_type}**（{len(items)}个）")
                for item in items:
                    print(f"    • {item['detail']}")
                    if item.get('suggestion'):
                        print(f"      💡 {item['suggestion']}")

    # 保存报告
    report = {
        'total_chapters': len(chapter_data),
        'total_issues': len(issues),
        'thresholds': {
            'tension_low': round(low_threshold, 1),
            'tension_high': round(high_threshold, 1),
            'avg_tension': round(avg_tension, 1),
            'avg_char_count': round(avg_chars, 0),
        },
        'rhythm_curve': chapter_data,
        'issues': issues,
    }

    report_dir = os.path.dirname(text_dir.rstrip('/'))
    output_path = os.path.join(report_dir, 'rhythm_report.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📄 节奏报告已保存至: {output_path}")

    return report

# ============================================================
# --suggest 模式：基于节奏指南提供具体修改建议
# ============================================================

RHYTHM_TEMPLATES = {
    '紧张': {
        'name': '紧张节奏（高压章）',
        'when': '危机逼近、对峙、追查关键线索',
        'params': '字数2500-3500 | 钩子密度8-12/千字 | 对话25-40% | 短句45-60%',
        'techniques': [
            '开头直接进入紧张状态，不做铺垫（前200字即制造压迫感）',
            '信息快速叠加，每段都有新发现或新危机',
            '短句密集轰炸（≤10字的句子连续出现），制造喘不过气的感觉',
            '结尾留强悬念钩子——一个未回答的问题',
        ],
        'example': '示例："没有新闻。没有公告。没有变更记录。一个月的时间，零公开信息。不是没有新闻可报——是所有信息都被按住了。"',
        'danmaku': '弹幕建议高密度（每300字1-2条，震惊/推理/紧张型）',
    },
    '悬念': {
        'name': '悬念节奏（推理章）',
        'when': '抛出谜团、发现线索、分析推理',
        'params': '字数2500-3500 | 钩子密度6-10/千字 | 对话30-45% | 短句35-50%',
        'techniques': [
            '开头抛出核心疑问或异常现象',
            '线索逐条展开，有真有假，制造推理空间',
            '用问答式对话推进推理，每段对话都在推进信息',
            '结尾新谜团或颠覆性信息，让读者重新思考',
        ],
        'example': '示例：用角色对话完成推理，"也许恰恰相反"做认知翻转，结尾暗示共识但不揭底。',
        'danmaku': '弹幕建议高密度（每300字1-2条，推理/讨论型）',
    },
    '日常': {
        'name': '日常节奏（舒缓章）',
        'when': '铺垫世界观、推进日常关系、给读者喘息空间',
        'params': '字数2000-3000 | 钩子密度3-5/千字 | 对话40-55% | 短句25-35%',
        'techniques': [
            '用感官细节（声响、气味、光线）营造日常氛围',
            '人物互动、生活细节、幽默对话，推进关系',
            '中间设一个小冲突或小发现，轻微吊胃口',
            '结尾铺一个轻钩子（伏笔/异常细节），不急不缓',
        ],
        'example': '示例："打饭的阿姨在窗口后面舀菜，不锈钢盘子磕出清脆的声响。空气里飘着酱油和葱姜的味道。"',
        'danmaku': '弹幕建议低-中密度（每500字1-2条，日常吐槽/角色互动为主）',
    },
    '催泪': {
        'name': '催泪节奏（情感章）',
        'when': '角色牺牲、离别、回忆杀、情感揭露',
        'params': '字数2000-3000 | 钩子密度4-7/千字 | 对话20-35% | 短句35-45%',
        'techniques': [
            '开头用日常或平静场景铺垫，制造反差',
            '情感线索渐次展开，用细节而非形容词（"0.2秒"比"很难过"有力）',
            '克制表达比煽情更有力——沉默比语言更有力',
            '结尾金句或留白，让读者自己感受',
        ],
        'example': '示例："她停顿了0.2秒，然后继续笑着给他盛饭。但那碗饭她没有吃完。从此他再也没有对任何人说过。"',
        'danmaku': '弹幕建议中-高密度（每400字1-2条，情感共鸣型）',
    },
    '转折': {
        'name': '转折节奏（爆点章）',
        'when': '真相揭露、立场反转、命运改变',
        'params': '字数2000-3000 | 钩子密度10-15/千字 | 对话20-35% | 短句50-65%',
        'techniques': [
            '开头做误导性铺垫，让读者以为走向A',
            '看似正常的剧情推进，暗藏伏笔',
            '核心转折瞬间——短句轰炸+认知颠覆',
            '转折后余波+新方向暗示',
        ],
        'example': '示例：先铺正常商务名片，然后用粗体+独立行做视觉冲击，"消失了"三字制造超自然恐怖感。',
        'danmaku': '弹幕建议极高密度（每200字1-2条，震惊/反转/打卡型）',
    },
}

def generate_suggestions(issues, chapter_data):
    """根据检测到的问题，生成具体的节奏修改建议"""
    suggestions = []

    for issue in issues:
        itype = issue['type']
        detail = issue['detail']

        # 提取章节范围
        import re as _re
        m = _re.search(r'第(\d+)-(\d+)章', detail)
        if not m:
            m = _re.search(r'第(\d+)章', detail)
            if m:
                ch_start = ch_end = int(m.group(1))
            else:
                ch_start = ch_end = None
        else:
            ch_start, ch_end = int(m.group(1)), int(m.group(2))

        suggest = {'issue': detail, 'fixes': []}

        if itype == '连续太平':
            suggest['summary'] = '连续多章节奏偏平，读者可能失去兴趣。建议插入紧张/悬念章节打破沉闷。'

            # 推荐在太平区间中间插入紧张章
            mid_ch = (ch_start + ch_end) // 2 if ch_start and ch_end else None

            suggest['fixes'].append({
                'template': RHYTHM_TEMPLATES['紧张'],
                'where': f'建议在第{mid_ch}章左右插入一章紧张节奏' if mid_ch else '建议在太平区间中间插入一章紧张节奏',
                'why': '用高压章节打破连续平淡，重新抓住读者注意力',
            })
            suggest['fixes'].append({
                'template': RHYTHM_TEMPLATES['悬念'],
                'where': f'建议在第{ch_start}-{ch_end}章之间穿插悬念元素' if ch_start else '建议穿插悬念元素',
                'why': '在现有章节中增加悬念标记词和疑问句，不需要大改结构',
                'lightweight': True,
            })

            # 具体写法建议
            suggest['quick_tips'] = [
                '在现有章节结尾加入一个未回答的问题（"但有个地方不对……"）',
                '增加一个异常细节（角色发现不对劲的小事）',
                '把一段日常对话改成暗示危机的对话',
                '在太平区间中间插入一次意外事件（电话响了、有人敲门、屏幕弹出消息）',
            ]

        elif itype == '连续太紧':
            suggest['summary'] = '连续多章高紧张度，读者容易疲劳。建议插入日常/轻松章节给喘息空间。'

            mid_ch = (ch_start + ch_end) // 2 if ch_start and ch_end else None

            suggest['fixes'].append({
                'template': RHYTHM_TEMPLATES['日常'],
                'where': f'建议在第{mid_ch}章左右插入一章日常节奏' if mid_ch else '建议在高压区间中间插入一章日常节奏',
                'why': '高压之间必须插入至少1章舒缓，让读者消化之前的紧张情绪',
            })
            suggest['fixes'].append({
                'template': RHYTHM_TEMPLATES['催泪'],
                'where': f'如果剧情合适，第{ch_end}章之后可以接一章催泪节奏' if ch_end else '可以接一章催泪节奏',
                'why': '催泪章是紧张后的自然过渡——用情感冲击消化危机',
            })

            suggest['quick_tips'] = [
                '在紧张章节之间插入一段生活场景（吃饭、聊天、散步）',
                '让角色有一个短暂的放松时刻（泡杯咖啡、看窗外）',
                '用幽默对话化解紧张氛围（角色之间的调侃）',
                '插入一段回忆或内心独白，给读者从外部压力中喘息',
            ]

        elif itype == '情感单调':
            emotion_cn = {'tense': '紧张', 'relax': '轻松', 'sad': '悲伤'}
            m2 = _re.search(r'为"(.+?)"', detail)
            cur_emotion = m2.group(1) if m2 else '未知'

            # 根据当前单调情绪推荐变换方向
            variation_map = {
                '紧张': ['催泪', '日常'],
                '轻松': ['悬念', '催泪'],
                '悲伤': ['日常', '悬念'],
            }
            recommended = variation_map.get(cur_emotion, ['悬念', '日常'])

            suggest['summary'] = f'连续多章情绪基调为"{cur_emotion}"，读者容易审美疲劳。建议变换为"{recommended[0]}"或"{recommended[1]}"基调。'

            for rec in recommended:
                suggest['fixes'].append({
                    'template': RHYTHM_TEMPLATES[rec],
                    'where': f'建议在连续区间内穿插"{rec}"基调的章节',
                    'why': f'从"{cur_emotion}"转换到"{rec}"可以制造情绪反差，提升阅读体验',
                })

            suggest['quick_tips'] = [
                f'在现有"{cur_emotion}"基调章节中加入一个反差场景',
                '变换场景环境（从室内转到室外，从白天转到夜晚）',
                '引入一个新角色或新视角打破单调',
                '调整对话风格（如果前面都是严肃对话，加一段幽默互动）',
            ]

        elif itype == '连续短章':
            suggest['summary'] = '连续短章，内容密度可能不够。建议扩充或合并。'
            suggest['quick_tips'] = [
                '将2-3个短章合并为一章，用场景切换（***）分隔',
                '在短章中补充感官描写（声音、气味、光线）',
                '增加角色内心独白，丰富情感层次',
                '插入一条弹幕互动，增加趣味性',
            ]
            suggest['fixes'] = []

        elif itype == '连续长章':
            suggest['summary'] = '连续长章，读者注意力可能下降。建议拆分或加速节奏。'
            suggest['quick_tips'] = [
                '在长章中间找一个转折点拆分为两章',
                '增加短句比例和对话密度，加速阅读节奏',
                '每800-1000字设一个小钩子，维持注意力',
                '删减冗余描写，保留推进剧情的段落',
            ]
            suggest['fixes'] = []

        suggestions.append(suggest)

    return suggestions


def print_suggestions(suggestions):
    """打印 --suggest 模式的详细建议"""
    print(f"\n{'='*60}")
    print("🎯 节奏修改建议（--suggest 模式）")
    print(f"{'='*60}")

    for i, sug in enumerate(suggestions, 1):
        print(f"\n{'─'*50}")
        print(f"建议 {i}：{sug['issue']}")
        print(f"{'─'*50}")
        print(f"\n📋 {sug['summary']}")

        for fix in sug['fixes']:
            tmpl = fix['template']
            print(f"\n  ✨ 推荐节奏：{tmpl['name']}")
            print(f"     适用场景：{tmpl['when']}")
            print(f"     目标参数：{tmpl['params']}")
            print(f"     插入位置：{fix['where']}")
            print(f"     理由：{fix['why']}")
            print(f"     写作技法：")
            for j, tech in enumerate(tmpl['techniques'], 1):
                print(f"       {j}. {tech}")
            print(f"     {tmpl['example']}")
            print(f"     {tmpl['danmaku']}")

        if sug.get('quick_tips'):
            print(f"\n  💡 快速修复（小改动即可见效）：")
            for tip in sug['quick_tips']:
                print(f"     • {tip}")

    # 总结
    print(f"\n{'='*60}")
    print("📝 总结")
    print(f"{'='*60}")
    print(f"\n共 {len(suggestions)} 个问题需要处理。建议优先级：")
    print('  1. 先处理「连续太紧」——读者疲劳是弃书主因')
    print('  2. 再处理「连续太平」——读者失去兴趣也是弃书主因')
    print('  3. 最后处理「情感单调」和「长度波动」')
    print("\n参考文档：references/writing_rhythm_guide.md")


# ============================================================
# --emotion-track 模式：情绪词分布 + 情绪曲线 + 突变点检测
# ============================================================

EMOTION_DIMS = {
    'positive': ('😊正面', EMOTION_POSITIVE),
    'negative': ('😠负面', EMOTION_NEGATIVE),
    'anxious': ('😰紧张', EMOTION_ANXIOUS),
    'sorrow': ('😢悲伤', EMOTION_SORROW),
}

def compute_emotion_profile(content: str) -> Dict[str, float]:
    """计算章节的四维情绪得分（归一化到0-1）"""
    char_count = len(re.findall(r'[\u4e00-\u9fff]', content))
    if char_count == 0:
        return {k: 0.0 for k in EMOTION_DIMS}
    per_thousand = char_count / 1000
    scores = {}
    for key, (_, words) in EMOTION_DIMS.items():
        raw = sum(content.count(w) for w in words)
        # 归一化：每千字命中数，上限15次映射到1.0
        scores[key] = min(raw / per_thousand / 15.0, 1.0)
    return scores

def detect_emotion_shifts(emotion_series: List[Dict[str, float]], threshold: float = 0.35) -> List[Dict[str, Any]]:
    """检测情绪突变点：相邻章节四维得分的欧氏距离超过阈值"""
    shifts = []
    for i in range(1, len(emotion_series)):
        prev = emotion_series[i-1]['scores']
        curr = emotion_series[i]['scores']
        dist = sum((prev[k] - curr[k])**2 for k in EMOTION_DIMS) ** 0.5
        if dist >= threshold:
            # 找出变化最大的维度
            max_dim = max(EMOTION_DIMS, key=lambda k: abs(prev[k] - curr[k]))
            direction = '↑' if curr[max_dim] > prev[max_dim] else '↓'
            dim_cn = EMOTION_DIMS[max_dim][0]
            shifts.append({
                'from_chapter': emotion_series[i-1]['chapter'],
                'to_chapter': emotion_series[i]['chapter'],
                'distance': round(dist, 3),
                'max_change_dim': max_dim,
                'max_change_label': f'{dim_cn}{direction}',
                'detail': f'第{emotion_series[i-1]["chapter"]}→{emotion_series[i]["chapter"]}章情绪突变（{dim_cn}{direction}，距离{dist:.2f}）',
            })
    return shifts

def ascii_emotion_curve(emotion_series):
    """绘制控制台ASCII情绪曲线"""
    labels = ['😊正面', '😠负面', '😰紧张', '😢悲伤']
    keys = ['positive', 'negative', 'anxious', 'sorrow']
    chars = ['█', '▓', '▒', '░']
    colors = ['', '', '', '']  # 无ANSI时

    print(f"\n{'='*60}")
    print("🎭 情绪曲线（--emotion-track）")
    print(f"{'='*60}\n")

    # 表头
    header = f"{'章节':>6s}"
    for lb in labels:
        header += f"  {lb:>6s}"
    header += f"  {'主导':>6s}  {'幅度':>5s}"
    print(header)
    print("-" * 70)

    for entry in emotion_series:
        ch = entry['chapter']
        scores = entry['scores']
        dominant = entry['dominant']
        amplitude = entry['amplitude']

        line = f"第{ch:03d}章"
        for k in keys:
            bar_len = int(scores[k] * 20)
            line += f"  {'█'*bar_len:<20s}"
            line = line[:-20]  # remove padding
            line += f"  {scores[k]:.2f}"

        dom_cn = {'positive':'😊正面','negative':'😠负面','anxious':'😰紧张','sorrow':'😢悲伤','neutral':'😐中性'}
        line += f"  {dom_cn.get(dominant, dominant)}  {amplitude:.2f}"
        print(line)

    # ASCII 简图（每维度一行，横向表示章节）
    print(f"\n{'─'*60}")
    print("📈 简图（每行一个情绪维度，横向=章节，█=强度）")
    print(f"{'─'*60}")

    n_chapters = len(emotion_series)
    for ki, k in enumerate(keys):
        label = labels[ki]
        row = f"{label} "
        for entry in emotion_series:
            v = entry['scores'][k]
            if v < 0.1:
                row += ' '
            elif v < 0.3:
                row += '░'
            elif v < 0.5:
                row += '▒'
            elif v < 0.7:
                row += '▓'
            else:
                row += '█'
        print(row)

    # 章节号轴
    axis = '       '
    for entry in emotion_series:
        ch = entry['chapter']
        axis += str(ch % 10) if n_chapters <= 50 else ('|' if ch % 5 == 0 else ' ')
    print(axis)

def run_emotion_track(text_dir):
    """--emotion-track 主逻辑"""
    chapters = list_chapters(text_dir)
    if not chapters:
        print("[错误] 未找到章节文件")
        return None

    print(f"\n🎭 情绪追踪模式")
    print(f"📖 找到 {len(chapters)} 个章节\n")

    emotion_series = []
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        if not content:
            continue
        scores = compute_emotion_profile(content)
        total = sum(scores.values())
        if total < 0.01:
            dominant = 'neutral'
        else:
            dominant = max(EMOTION_DIMS, key=lambda k: scores[k])
        amplitude = max(scores.values()) - min(scores.values())
        emotion_series.append({
            'chapter': num,
            'filename': fname,
            'scores': scores,
            'dominant': dominant,
            'amplitude': round(amplitude, 3),
        })

    if not emotion_series:
        print("[错误] 没有可分析的章节")
        return None

    # ASCII 曲线
    ascii_emotion_curve(emotion_series)

    # 突变点检测
    shifts = detect_emotion_shifts(emotion_series)
    print(f"\n{'='*60}")
    print("⚡ 情绪突变点")
    print(f"{'='*60}")
    if not shifts:
        print("\n✅ 未检测到显著的情绪突变")
    else:
        print(f"\n发现 {len(shifts)} 个情绪突变点：\n")
        for s in shifts:
            print(f"  ⚡ {s['detail']}")

    # 每章摘要
    print(f"\n{'='*60}")
    print("📋 每章情绪摘要")
    print(f"{'='*60}\n")
    dom_cn = {'positive':'😊正面','negative':'😠负面','anxious':'😰紧张','sorrow':'😢悲伤','neutral':'😐中性'}
    for entry in emotion_series:
        scores = entry['scores']
        dom = dom_cn.get(entry['dominant'], entry['dominant'])
        dims_str = '  '.join(f"{EMOTION_DIMS[k][0]}{scores[k]:.2f}" for k in EMOTION_DIMS)
        print(f"  第{entry['chapter']:03d}章 | 主导:{dom} | 幅度:{entry['amplitude']:.2f} | {dims_str}")

    # 保存 JSON
    report = {
        'emotion_series': emotion_series,
        'emotion_shifts': shifts,
    }
    report_dir = os.path.dirname(text_dir.rstrip('/'))
    output_path = os.path.join(report_dir, 'emotion_track.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"\n📄 情绪追踪报告已保存至: {output_path}")

    return report

# ============================================================
# --compare 模式：对比两版正文目录的节奏曲线差异
# ============================================================

def analyze_chapter_rhythms(text_dir):
    """分析目录中所有章节的节奏数据，返回 {章节号: 数据} 字典"""
    chapters = list_chapters(text_dir)
    if not chapters:
        return {}
    result = {}
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        if not content:
            continue
        char_count = len(re.findall(r'[\u4e00-\u9fff]', content))
        density, hook_types = count_hook_density(content)
        dialogue_ratio = count_dialogue_ratio(content)
        short_ratio = count_short_sentence_ratio(content)
        emotion, emotion_scores = detect_emotion_tone(content)
        tension = compute_tension(density, dialogue_ratio, short_ratio, hook_types)
        result[num] = {
            'chapter': num,
            'filename': fname,
            'char_count': char_count,
            'hook_density': round(density, 2),
            'hook_types': hook_types,
            'dialogue_ratio': round(dialogue_ratio, 3),
            'short_sentence_ratio': round(short_ratio, 3),
            'emotion': emotion,
            'emotion_scores': emotion_scores,
            'tension': tension,
        }
    return result

def run_compare(dir_before: str, dir_after: str) -> Dict[str, Any]:
    """--compare 主逻辑：对比两版节奏曲线差异"""
    print("=" * 60)
    print("🔄 节奏对比模式（--compare）")
    print("=" * 60)
    print(f"\n  修改前目录: {dir_before}")
    print(f"  修改后目录: {dir_after}")

    before = analyze_chapter_rhythms(dir_before)
    after = analyze_chapter_rhythms(dir_after)

    if not before:
        print(f"\n[错误] 修改前目录无章节: {dir_before}")
        return None
    if not after:
        print(f"\n[错误] 修改后目录无章节: {dir_after}")
        return None

    # 按交集章节对比
    common = sorted(set(before.keys()) & set(after.keys()))
    only_before = sorted(set(before.keys()) - set(after.keys()))
    only_after = sorted(set(after.keys()) - set(before.keys()))

    if not common:
        print("\n[错误] 两版无共同章节，无法对比")
        return None

    print(f"\n  共同章节: {len(common)} 章")
    if only_before:
        print(f"  仅修改前: 第{only_before[0]}-{only_before[-1]}章（共{len(only_before)}章）")
    if only_after:
        print(f"  仅修改后: 第{only_after[0]}-{only_after[-1]}章（共{len(only_after)}章）")

    # 逐章对比
    diffs = []
    for ch in common:
        b = before[ch]
        a = after[ch]
        delta_tension = round(a['tension'] - b['tension'], 1)
        delta_hook = round(a['hook_density'] - b['hook_density'], 2)
        delta_dialogue = round(a['dialogue_ratio'] - b['dialogue_ratio'], 3)
        delta_short = round(a['short_sentence_ratio'] - b['short_sentence_ratio'], 3)
        delta_chars = a['char_count'] - b['char_count']

        if delta_tension > 5:
            change = ' tighter'
            label = '🔺变紧'
        elif delta_tension < -5:
            change = ' looser'
            label = '🔻变松'
        else:
            change = ' same'
            label = '➖不变'

        diffs.append({
            'chapter': ch,
            'before': b,
            'after': a,
            'delta_tension': delta_tension,
            'delta_hook': delta_hook,
            'delta_dialogue': delta_dialogue,
            'delta_short': delta_short,
            'delta_chars': delta_chars,
            'change': label,
        })

    # 找变化最大的章节
    max_change = max(diffs, key=lambda d: abs(d['delta_tension']))

    # 输出对比表
    print(f"\n{'='*60}")
    print("📊 逐章节奏对比")
    print(f"{'='*60}\n")
    print(f"  {'章节':>6s}  {'修改前':>6s}  {'修改后':>6s}  {'Δ紧张':>6s}  {'Δ钩子':>6s}  {'Δ对话':>6s}  {'Δ短句':>6s}  {'Δ字数':>6s}  变化")
    print("  " + "-" * 78)

    for d in diffs:
        ch = d['chapter']
        marker = ' ⭐' if d['chapter'] == max_change['chapter'] else ''
        print(f"  第{ch:03d}章  {d['before']['tension']:6.1f}  {d['after']['tension']:6.1f}  {d['delta_tension']:+6.1f}  "
              f"{d['delta_hook']:+6.2f}  {d['delta_dialogue']:+6.3f}  {d['delta_short']:+6.3f}  "
              f"{d['delta_chars']:+6d}  {d['change']}{marker}")

    # 情感基调变化
    emotion_changed = [d for d in diffs if d['before']['emotion'] != d['after']['emotion']]
    if emotion_changed:
        print(f"\n{'─'*60}")
        print("🎭 情感基调变化的章节")
        print(f"{'─'*60}")
        emotion_map = {'tense': '⚡紧张', 'relax': '😊轻松', 'sad': '😢悲伤', 'neutral': '😐平淡', 'mixed': '🔄混合'}
        for d in emotion_changed:
            print(f"  第{d['chapter']:03d}章: {emotion_map[d['before']['emotion']]} → {emotion_map[d['after']['emotion']]}")

    # 统计汇总
    tighter = sum(1 for d in diffs if d['delta_tension'] > 5)
    looser = sum(1 for d in diffs if d['delta_tension'] < -5)
    same = len(diffs) - tighter - looser

    print(f"\n{'='*60}")
    print("📋 汇总")
    print(f"{'='*60}")
    print(f"\n  总计 {len(diffs)} 章：🔺变紧 {tighter} 章 ｜ 🔻变松 {looser} 章 ｜ ➖不变 {same} 章")
    print(f"  ⭐ 变化最大: 第{max_change['chapter']}章（Δ紧张度 {max_change['delta_tension']:+.1f}）")

    avg_delta = sum(d['delta_tension'] for d in diffs) / len(diffs)
    if avg_delta > 2:
        print(f"  整体趋势: 整体偏紧（平均Δ紧张度 {avg_delta:+.1f}）")
    elif avg_delta < -2:
        print(f"  整体趋势: 整体偏松（平均Δ紧张度 {avg_delta:+.1f}）")
    else:
        print(f"  整体趋势: 整体稳定（平均Δ紧张度 {avg_delta:+.1f}）")

    # 保存报告
    report = {
        'dir_before': os.path.abspath(dir_before),
        'dir_after': os.path.abspath(dir_after),
        'total_compared': len(diffs),
        'only_before': only_before,
        'only_after': only_after,
        'summary': {
            'tighter': tighter,
            'looser': looser,
            'same': same,
            'avg_delta_tension': round(avg_delta, 2),
            'max_change_chapter': max_change['chapter'],
            'max_change_delta': max_change['delta_tension'],
        },
        'diffs': diffs,
    }
    report_dir = os.path.dirname(dir_after.rstrip('/'))
    output_path = os.path.join(report_dir, 'rhythm_compare.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n📄 对比报告已保存至: {output_path}")

    return report

def main():
    parser = argparse.ArgumentParser(description='章节节奏检测')
    parser.add_argument('text_dir', help='正文目录路径')
    parser.add_argument('--compare', metavar='DIR', help='对比模式：指定修改前的正文目录，text_dir 为修改后')
    parser.add_argument('--suggest', action='store_true', help='检测到问题时，输出具体的节奏模板推荐和修改建议')
    parser.add_argument('--emotion-track', action='store_true', help='追踪全章情绪词分布，绘制情绪曲线，标记情绪突变点')
    parser.add_argument('--json', action='store_true', help='以JSON格式输出结果')
    parser.add_argument('--version', action='version', version='rhythm_check v2.1.0 (novel-writer skill)')
    args = parser.parse_args()

    if args.compare:
        report = run_compare(args.compare, args.text_dir)
    elif args.emotion_track:
        report = run_emotion_track(args.text_dir)
    else:
        report = run_check(args.text_dir)

    if args.suggest and report and report.get('issues') and not args.emotion_track and not args.compare:
        suggestions = generate_suggestions(report['issues'], report['rhythm_curve'])
        print_suggestions(suggestions)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 rhythm_check.py <正文目录>")
        print("\n示例:")
        print("  python3 rhythm_check.py 正文/")
        sys.exit(1)
    main()
