#!/usr/bin/env python3
"""
节奏预测脚本 v1
基于已写章节的节奏曲线，预测未来5-10章的推荐节奏

用法：
  python3 tension_forecast.py <正文目录> [--count N] [--outline 大纲文件] [--character-states 角色状态文件] [--json]

功能：
  1. 读取已写章节的紧张度评分（复用 rhythm_check.py 的算法）
  2. 基于最近10章趋势，预测未来N章推荐节奏
  3. 遵循"不能连续太平""不能连续太紧"原则
  4. 输出推荐章节节奏序列（如 紧张→紧张→日常→悬念→高潮）
  5. 如有 --outline，结合大纲后续章节内容调整预测
  6. 如有 --character-states，结合角色弧线阶段调整节奏预测
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Any, Dict, List, Optional, Tuple

# 复用 rhythm_check.py 的分析函数（直接内联，避免import路径问题）

def read_file(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return ""

def list_chapters(dir_path: str) -> List[Tuple[int, str, str]]:
    if not os.path.isdir(dir_path):
        return []
    chapters = []
    seen = {}
    for f in sorted(os.listdir(dir_path)):
        if f.endswith('.md') or f.endswith('.txt'):
            match = re.search(r'第(\d+)章', f)
            if match:
                num = int(match.group(1))
                if num not in seen:
                    seen[num] = f
    for num, f in sorted(seen.items()):
        chapters.append((num, os.path.join(dir_path, f), f))
    return chapters

def normalize_text(text: str) -> str:
    text = text.replace('\u3000', ' ')
    text = re.sub(r'[ \t]+', ' ', text)
    return text

# 钩子标记词库（与 rhythm_check.py 一致）
HOOK_SUSPENSE = ['愣住', '瞳孔收缩', '瞳孔骤然', '愣了', '倒吸一口凉气',
    '不敢相信', '心跳漏了一拍', '背后一凉', '脊背发凉',
    '怎么回事', '不可能', '为什么', '谁', '什么意思',
    '等等', '不对', '可是', '然而', '但是',
    '悬念', '谜团', '秘密', '隐藏', '真相']
HOOK_REVERSAL = ['没想到', '没想到的是', '出乎意料', '没想到的是',
    '反转', '颠覆', '原来', '事实上', '实际上',
    '并非', '根本不是', '恰恰相反', '完全不同',
    '直到', '才知道', '才明白', '才发现']
HOOK_EMOTION = ['眼泪', '哭了', '鼻酸', '哽咽',
    '颤抖', '深吸一口气', '咬了咬牙', '攥紧',
    '沉默了很久', '一句话都说不出来',
    '谢谢你', '对不起', '再见', '最后一次']
HOOK_THRILL = ['脚步声', '黑暗中', '阴影', '走廊尽头',
    '灯灭了', '门开了', '窗户', '身后',
    '失踪', '尸体', '血', '杀', '危险', '逃跑', '追', '躲']
HOOK_SATISFY = ['估值', '翻了', '暴涨', '打脸',
    '所有人沉默', '哑口无言', '脸色难看', '佩服', '天才', '不可思议']

ALL_HOOK_WORDS = {
    'suspense': HOOK_SUSPENSE, 'reversal': HOOK_REVERSAL,
    'emotion': HOOK_EMOTION, 'thrill': HOOK_THRILL, 'satisfy': HOOK_SATISFY,
}

EMOTION_TENSE = ['紧张', '恐惧', '危险', '威胁', '死', '杀', '逃', '追',
                 '心跳加速', '手心出汗', '背后发凉', '不寒而栗', '毛骨悚然',
                 '颤抖', '尖叫', '崩溃', '绝望', '窒息']
EMOTION_RELAX = ['笑了', '轻松', '温暖', '阳光', '咖啡',
                 '周末', '散步', '闲聊', '开玩笑', '哈哈',
                 '搞笑', '幽默', '吃', '喝', '睡']
EMOTION_SAD = ['哭', '泪', '悲伤', '遗憾', '失去', '再见',
               '永别', '怀念', '想念', '孤独', '寂寞', '沉默']

def count_dialogue_ratio(content: str) -> float:
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
    return dialogue_chars / total if total else 0

def count_short_sentence_ratio(content: str) -> float:
    sentences = re.split(r'[。！？\n]', content)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 0]
    if not sentences:
        return 0
    return sum(1 for s in sentences if len(s) <= 15) / len(sentences)

def count_hook_density(content: str) -> float:
    total_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
    if total_chars == 0:
        return 0, {}
    counts_by_type = {}
    total_hits = 0
    for hook_type, words in ALL_HOOK_WORDS.items():
        hits = sum(content.count(w) for w in words)
        counts_by_type[hook_type] = hits
        total_hits += hits
    return total_hits / (total_chars / 1000), counts_by_type

def compute_tension(density: float, dialogue_ratio: float, short_ratio: float, hook_types: int) -> float:
    density_score = min(density / 20.0, 1.0) * 40
    dialogue_score = min(dialogue_ratio / 0.5, 1.0) * 20
    short_score = min(short_ratio / 0.5, 1.0) * 20
    thriller_bonus = hook_types.get('reversal', 0) + hook_types.get('thrill', 0)
    thriller_score = min(thriller_bonus / 10.0, 1.0) * 20
    return round(density_score + dialogue_score + short_score + thriller_score, 1)

# ============================================================
# 节奏类型定义与转换
# ============================================================

RHYTHM_TYPES = {
    '日常': {'min': 0, 'max': 40, 'label': '😊日常', 'desc': '舒缓、铺垫、日常互动'},
    '悬念': {'min': 30, 'max': 60, 'label': '🤔悬念', 'desc': '抛谜团、推理、线索'},
    '紧张': {'min': 55, 'max': 80, 'label': '⚡紧张', 'desc': '高压、冲突、危机'},
    '催泪': {'min': 35, 'max': 65, 'label': '😢催泪', 'desc': '情感冲击、离别、牺牲'},
    '转折': {'min': 70, 'max': 100, 'label': '💥转折', 'desc': '真相揭露、反转、爆点'},
}

def tension_to_rhythm(tension: float) -> str:
    """将紧张度评分映射为节奏类型"""
    if tension >= 75:
        return '转折'
    elif tension >= 58:
        return '紧张'
    elif tension >= 40:
        return '悬念'
    elif tension >= 25:
        return '日常'
    else:
        return '日常'

def rhythm_to_target_tension(rhythm_type: str) -> float:
    """节奏类型对应的目标紧张度（取中间值）"""
    info = RHYTHM_TYPES.get(rhythm_type)
    if not info:
        return 50
    return (info['min'] + info['max']) // 2

# ============================================================
# 节奏规则引擎
# ============================================================

# 不合法的连续模式（最多连续N章相同类型）
MAX_CONSECUTIVE = {
    '日常': 2,   # 最多连2章日常
    '悬念': 3,   # 最多连3章悬念
    '紧张': 2,   # 最多连2章紧张（第3章必须喘息）
    '催泪': 1,   # 催泪不能连续
    '转折': 1,   # 转折不能连续
}

# 转折后推荐的"消化"节奏
AFTER_TURNING = ['日常', '催泪', '悬念']
# 紧张后推荐的"喘息"节奏
AFTER_TENSE = ['日常', '催泪', '悬念']
# 日常后推荐的"升温"节奏
AFTER_DAILY = ['悬念', '紧张', '催泪']
# 悬念后推荐的节奏
AFTER_SUSPENSE = ['紧张', '转折', '日常']

# 10章周期模板（来自 writing_rhythm_guide.md）
TEN_CHAPTER_CYCLE = ['悬念', '日常', '悬念', '紧张', '日常', '悬念', '紧张', '催泪', '紧张', '转折']

def validate_consecutive(plan, rhythm_type):
    """检查加入该节奏类型后是否违反连续规则"""
    count = 0
    for r in reversed(plan):
        if r == rhythm_type:
            count += 1
        else:
            break
    return count < MAX_CONSECUTIVE.get(rhythm_type, 3)

def get_previous_rhythm(plan):
    """获取前一个节奏类型"""
    return plan[-1] if plan else None

def get_recommended_next(plan, existing_tensions=None):
    """基于规则推荐下一个节奏类型"""
    prev = get_previous_rhythm(plan)

    if prev == '转折':
        candidates = list(AFTER_TURNING)
    elif prev == '紧张':
        candidates = list(AFTER_TENSE)
    elif prev == '日常':
        candidates = list(AFTER_DAILY)
    elif prev == '催泪':
        candidates = ['日常', '悬念', '紧张']
    elif prev == '悬念':
        candidates = list(AFTER_SUSPENSE)
    else:
        candidates = TEN_CHAPTER_CYCLE[0:1]

    # 过滤违反连续规则的
    valid = [c for c in candidates if validate_consecutive(plan, c)]
    if not valid:
        # 如果所有候选都违反规则，选择任意合法类型
        for rt in ['日常', '悬念', '紧张', '催泪', '转折']:
            if validate_consecutive(plan, rt):
                valid.append(rt)
                break
    return valid

# ============================================================
# 大纲解析
# ============================================================

def parse_outline_keywords(outline_path, start_chapter):
    """从大纲文件中提取指定章节之后的关键词"""
    content = read_file(outline_path)
    if not content:
        return {}

    # 提取章节条目
    chapter_keywords = {}
    # 匹配：第XXX章 标题 | ### 第XXX章 | | 第XXX章 |
    pattern = re.compile(r'第(\d+)章[：:\s|]*([^\n|]*)', re.IGNORECASE)

    for match in pattern.finditer(content):
        ch_num = int(match.group(1))
        title_text = match.group(2).strip()
        if ch_num >= start_chapter and title_text:
            # 从标题提取关键词
            keywords = extract_keywords(title_text)
            chapter_keywords[ch_num] = {
                'title': title_text,
                'keywords': keywords,
            }

    return chapter_keywords

def extract_keywords(text):
    """简单关键词提取（去除停用词，取实词）"""
    stopwords = {'的', '了', '在', '是', '我', '他', '她', '它', '们', '这', '那',
                 '一', '个', '不', '有', '和', '就', '也', '都', '而', '及',
                 '与', '着', '或', '一个', '没有', '可以', '这个', '那个', '什么'}
    # 去除标点
    text = re.sub(r'[，。！？、；：“”‘’（）【】《》\s\-—…·]', ' ', text)
    words = [w for w in text.split() if len(w) >= 2 and w not in stopwords]
    return words

# 大纲关键词到节奏类型的映射
OUTLINE_RHYTHM_HINTS = {
    # 紧张关键词
    '追': '紧张', '杀': '紧张', '逃': '紧张', '危险': '紧张', '危机': '紧张',
    '对峙': '紧张', '绑架': '紧张', '威胁': '紧张', '追杀': '紧张', '暗杀': '紧张',
    '紧张': '紧张', '冲突': '紧张', '战斗': '紧张', '搏斗': '紧张', '陷阱': '紧张',
    # 转折关键词
    '真相': '转折', '反转': '转折', '揭露': '转折', '揭秘': '转折', '发现': '转折',
    '背叛': '转折', '秘密': '转折', '阴谋': '转折', '身份': '转折', '震惊': '转折',
    # 催泪关键词
    '牺牲': '催泪', '离别': '催泪', '死亡': '催泪', '回忆': '催泪', '告别': '催泪',
    '永远': '催泪', '最后': '催泪', '失去': '催泪', '眼泪': '催泪', '心碎': '催泪',
    '温暖': '催泪', '感动': '催泪', '守护': '催泪',
    # 悬念关键词
    '线索': '悬念', '谜': '悬念', '谜团': '悬念', '疑点': '悬念', '调查': '悬念',
    '推理': '悬念', '分析': '悬念', '寻找': '悬念', '追踪': '悬念', '暗示': '悬念',
    '伏笔': '悬念', '异常': '悬念', '疑问': '悬念',
    # 日常关键词
    '日常': '日常', '吃饭': '日常', '聊天': '日常', '周末': '日常', '生活': '日常',
    '学校': '日常', '工作': '日常', '朋友': '日常', '约会': '日常', '逛街': '日常',
    '放松': '日常', '休息': '日常', '聚会': '日常', '旅行': '日常',
}

def outline_to_rhythm_hint(keywords):
    """根据大纲关键词推测节奏类型"""
    votes = defaultdict(int)
    for kw in keywords:
        for hint_kw, rhythm in OUTLINE_RHYTHM_HINTS.items():
            if hint_kw in kw or kw in hint_kw:
                votes[rhythm] += 1
    if not votes:
        return None
    return max(votes, key=votes.get)

# ============================================================
# 趋势分析
# ============================================================

def analyze_trend(tensions: List[float]) -> Tuple[str, float]:
    """分析最近N章的紧张度趋势"""
    if len(tensions) < 2:
        return 'stable', 0

    # 线性回归斜率
    n = len(tensions)
    x_mean = (n - 1) / 2
    y_mean = sum(tensions) / n
    numerator = sum((i - x_mean) * (t - y_mean) for i, t in enumerate(tensions))
    denominator = sum((i - x_mean) ** 2 for i in range(n))

    if denominator == 0:
        return 'stable', 0

    slope = numerator / denominator
    avg = y_mean

    if slope > 3:
        return 'rising', slope
    elif slope < -3:
        return 'falling', slope
    else:
        return 'stable', slope

def detect_phase(tensions: List[float]) -> str:
    """检测当前处于10章周期的哪个阶段"""
    if len(tensions) < 3:
        return 'early'

    recent = tensions[-5:] if len(tensions) >= 5 else tensions
    avg = sum(recent) / len(recent)

    if avg >= 65:
        return 'climax'  # 高潮期
    elif avg >= 50:
        return 'building'  # 爬升期
    elif avg >= 35:
        return 'transitional'  # 过渡期
    else:
        return 'cooling'  # 冷却期

# ============================================================
# 核心预测引擎
# ============================================================

# ============================================================
# 角色弧线调整
# ============================================================

# 弧线阶段 → 推荐节奏调整
ARC_RHYTHM_ADJUSTMENTS = {
    # 高压阶段：建议紧张/挫折/转折
    'cracking': {'preferred': ['紧张', '悬念', '转折'], 'avoid': ['日常'], 'label': '裂痕期'},
    'breaking': {'preferred': ['紧张', '催泪', '转折'], 'avoid': ['日常'], 'label': '破碎期'},
    'backlash': {'preferred': ['紧张', '转折', '催泪'], 'avoid': ['日常'], 'label': '反噬期'},
    'crisis': {'preferred': ['紧张', '转折'], 'avoid': ['日常'], 'label': '危机期'},
    'trial': {'preferred': ['紧张', '悬念', '转折'], 'avoid': ['日常'], 'label': '考验期'},
    # 上升/转变阶段：混合
    'awakening': {'preferred': ['悬念', '紧张', '转折'], 'avoid': [], 'label': '觉醒期'},
    'rebuilding': {'preferred': ['悬念', '日常', '紧张'], 'avoid': ['转折'], 'label': '重建期'},
    'fusion': {'preferred': ['悬念', '紧张', '催泪'], 'avoid': [], 'label': '融合期'},
    # 平稳阶段：建议日常/轻松
    'rebuilding': {'preferred': ['悬念', '日常', '紧张'], 'avoid': ['转折'], 'label': '重建期'},
    'isolation': {'preferred': ['悬念', '日常'], 'avoid': ['转折'], 'label': '孤岛期'},
    'passive': {'preferred': ['日常', '悬念'], 'avoid': ['转折'], 'label': '被动期'},
    'independent': {'preferred': ['悬念', '紧张', '日常'], 'avoid': [], 'label': '独立期'},
    'ordinary': {'preferred': ['日常', '催泪'], 'avoid': ['转折', '紧张'], 'label': '凡人期'},
}

def load_character_arcs(character_states_path):
    """从 character_states.json 或 character_arcs.json 加载角色弧线阶段信息"""
    if not character_states_path or not os.path.isfile(character_states_path):
        return None

    try:
        with open(character_states_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return None

    # 尝试从 character_arcs.json 格式读取
    arcs = {}
    for char_name, char_data in data.items():
        if isinstance(char_data, dict):
            # 直接是弧线格式
            if 'current_phase' in char_data:
                arcs[char_name] = char_data['current_phase']
            # character_states.json 格式，找最新 snapshot 的 arc_phase
            elif 'snapshots' in char_data:
                snapshots = char_data['snapshots']
                if snapshots:
                    latest_key = max(snapshots.keys(), key=lambda k: int(k) if str(k).isdigit() else 0)
                    latest = snapshots[latest_key]
                    if 'arc_phase' in latest:
                        arcs[char_name] = latest['arc_phase']
            # 关系弧线格式
            elif 'arc_overview' in char_data and 'current_phase' in char_data:
                arcs[char_name] = char_data['current_phase']

    return arcs if arcs else None

def get_arc_adjustment(arc_phases):
    """根据所有角色的弧线阶段，计算节奏调整建议"""
    if not arc_phases:
        return None, []

    adjustments = []
    preferred_counts = defaultdict(int)
    avoid_counts = defaultdict(int)

    for char_name, phase_id in arc_phases.items():
        adj = ARC_RHYTHM_ADJUSTMENTS.get(phase_id)
        if not adj:
            # 未匹配到已知阶段，默认不调整
            adjustments.append(f'{char_name}（阶段"{phase_id}"无特定调整规则）')
            continue

        for r in adj['preferred']:
            preferred_counts[r] += 1
        for r in adj['avoid']:
            avoid_counts[r] += 1
        adjustments.append(f'{char_name}处于"{adj["label"]}"→偏好{adj["preferred"]}，回避{adj["avoid"]}')

    if not preferred_counts and not avoid_counts:
        return None, adjustments

    # 找出最受偏好的节奏类型
    sorted_preferred = sorted(preferred_counts.items(), key=lambda x: -x[1])
    top_preferred = [r for r, c in sorted_preferred[:2]] if sorted_preferred else []
    top_avoid = [r for r, c in sorted(avoid_counts.items(), key=lambda x: -x[1])[:2]] if avoid_counts else []

    return {'preferred': top_preferred, 'avoid': top_avoid}, adjustments

def apply_arc_adjustment(chosen, plan, arc_adj, forecast_entry_index):
    """应用弧线调整到节奏选择"""
    if not arc_adj:
        return chosen, None

    preferred = arc_adj.get('preferred', [])
    avoid = arc_adj.get('avoid', [])

    # 如果当前选择在被回避列表中，尝试替换为偏好
    if chosen in avoid:
        for p in preferred:
            if validate_consecutive(plan, p):
                return p, f'角色弧线调整："{chosen}"被回避，替换为偏好"{p}"'

    # 如果不是被偏好的，有一定概率提升优先级（每3章应用一次）
    if forecast_entry_index % 3 == 0 and preferred:
        for p in preferred:
            if validate_consecutive(plan, p) and p != chosen:
                return p, f'角色弧线强化：偏好"{p}"覆盖"{chosen}"'

    return chosen, None

def generate_forecast(existing_tensions: List[float], count: int = 7, outline_hints: Optional[List[Dict]] = None, arc_adj: Optional[Dict] = None) -> List[Dict[str, Any]]:
    """生成未来N章的节奏预测

    Args:
        existing_tensions: 已写章节的紧张度列表（从旧到新）
        count: 预测章节数
        outline_hints: 大纲提示 {章节号: 节奏类型}

    Returns:
        list of dicts: [{chapter: N, rhythm: '紧张', target_tension: 70, reason: '...'}]
    """
    # 将现有紧张度转为节奏序列
    existing_rhythms = [tension_to_rhythm(t) for t in existing_tensions]

    # 分析趋势
    recent_tensions = existing_tensions[-10:] if len(existing_tensions) >= 10 else existing_tensions
    trend, slope = analyze_trend(recent_tensions)
    phase = detect_phase(existing_tensions)

    # 最后已有章节号
    last_chapter = len(existing_tensions)

    plan = list(existing_rhythms)
    forecast = []

    for i in range(count):
        ch_num = last_chapter + i + 1

        # 步骤1：获取规则推荐
        recommended = get_recommended_next(plan)

        # 步骤2：结合大纲提示
        outline_hint = None
        if outline_hints and ch_num in outline_hints:
            outline_hint = outline_hints[ch_num]

        # 步骤3：结合趋势分析
        trend_hint = None
        if trend == 'rising' and len(forecast) > 0:
            # 持续上升，建议冷却
            if all(f['rhythm'] in ('紧张', '转折') for f in forecast[-2:]):
                trend_hint = '日常'
        elif trend == 'falling' and len(forecast) > 0:
            # 持续下降，建议升温
            if all(f['rhythm'] == '日常' for f in forecast[-2:]):
                trend_hint = '悬念'

        # 步骤4：综合决策
        chosen = None
        reason = ''

        if outline_hint and validate_consecutive(plan, outline_hint):
            chosen = outline_hint
            reason = f'大纲提示：大纲中该章关键词指向"{outline_hint}"节奏'
        elif trend_hint and validate_consecutive(plan, trend_hint):
            chosen = trend_hint
            reason = f'趋势修正：当前紧张度{"持续上升需要冷却" if trend == "rising" else "持续下降需要升温"}'

        if not chosen:
            # 从推荐列表中选择（优先考虑周期模板位置）
            cycle_pos = (len(existing_tensions) + i) % 10
            cycle_rhythm = TEN_CHAPTER_CYCLE[cycle_pos]

            if cycle_rhythm in recommended:
                chosen = cycle_rhythm
                reason = f'周期模板：10章周期第{cycle_pos + 1}位推荐"{cycle_rhythm}"'
            else:
                chosen = recommended[0]
                reason = f'规则推荐：前一章为"{plan[-1]}"，推荐接"{chosen}"'

        # 步骤5：角色弧线调整
        arc_reason = None
        if arc_adj:
            chosen, arc_reason = apply_arc_adjustment(chosen, plan, arc_adj, i)
            if arc_reason:
                reason = arc_reason

        target = rhythm_to_target_tension(chosen)

        entry = {
            'chapter': ch_num,
            'rhythm': chosen,
            'target_tension': target,
            'reason': reason,
        }
        forecast.append(entry)
        plan.append(chosen)

    return forecast, trend, slope, phase

# ============================================================
# 输出格式化
# ============================================================

RHYTHM_LABELS = {
    '日常': '😊日常（舒缓）',
    '悬念': '🤔悬念（推理）',
    '紧张': '⚡紧张（高压）',
    '催泪': '😢催泪（情感）',
    '转折': '💥转折（爆点）',
}

def print_forecast(forecast, trend, slope, phase, existing_tensions, outline_hints=None):
    """打印预测结果"""
    print("=" * 60)
    print("🔮 节奏预测（tension_forecast v1）")
    print("=" * 60)

    # 已有数据概览
    total_existing = len(existing_tensions)
    recent = existing_tensions[-10:] if len(existing_tensions) >= 10 else existing_tensions
    avg_recent = sum(recent) / len(recent) if recent else 50

    print(f"\n📊 已有数据：{total_existing}章，最近10章平均紧张度 {avg_recent:.1f}")
    trend_labels = {'rising': '上升 ↗', 'falling': '下降 ↘', 'stable': '平稳 →'}
    phase_labels = {'early': '初期建立', 'building': '张力爬升', 'climax': '高潮期', 'transitional': '过渡期', 'cooling': '冷却期'}
    print(f"📈 趋势：{trend_labels[trend]}（斜率 {slope:.1f}）")
    print(f"🎭 当前阶段：{phase_labels[phase]}")

    # 已有节奏曲线（最近10章）
    print(f"\n{'─'*50}")
    print("📖 已有节奏曲线（最近10章）")
    print(f"{'─'*50}")

    start = max(0, total_existing - 10)
    for i, t in enumerate(existing_tensions[start:]):
        ch = start + i + 1
        rhythm = tension_to_rhythm(t)
        bar_len = int(t / 2.5)
        bar = '█' * bar_len
        label = RHYTHM_LABELS.get(rhythm, rhythm)
        print(f"  第{ch:03d}章 {t:5.1f} {bar:<30s} {label}")

    # 预测结果
    print(f"\n{'─'*50}")
    print(f"🔮 未来 {len(forecast)} 章节奏预测")
    print(f"{'─'*50}")

    # 节奏序列概览
    sequence = ' → '.join(f['rhythm'] for f in forecast)
    print(f"\n  节奏序列：{sequence}\n")

    for f in forecast:
        label = RHYTHM_LABELS.get(f['rhythm'], f['rhythm'])
        target = f['target_tension']
        bar_len = int(target / 2.5)
        bar = '░' * bar_len
        print(f"  第{f['chapter']:03d}章 {label}  目标紧张度 {target:3d}  {bar}")
        print(f"         📝 {f['reason']}")

    # 节奏规则检查摘要
    print(f"\n{'─'*50}")
    print("✅ 节奏规则检查")
    print(f"{'─'*50}")

    all_rhythms = [tension_to_rhythm(t) for t in existing_tensions] + [f['rhythm'] for f in forecast]
    checks = []

    # 检查连续太平
    consecutive_daily = 0
    max_daily = 0
    for r in all_rhythms:
        if r == '日常':
            consecutive_daily += 1
            max_daily = max(max_daily, consecutive_daily)
        else:
            consecutive_daily = 0
    checks.append(('连续日常 ≤ 2章', max_daily <= 2, f'最长连续{max_daily}章'))

    # 检查连续太紧
    consecutive_tense = 0
    max_tense = 0
    for r in all_rhythms:
        if r in ('紧张', '转折'):
            consecutive_tense += 1
            max_tense = max(max_tense, consecutive_tense)
        else:
            consecutive_tense = 0
    checks.append(('连续高压 ≤ 2章', max_tense <= 2, f'最长连续{max_tense}章'))

    # 检查催泪不连续
    consecutive_cry = 0
    max_cry = 0
    for r in all_rhythms:
        if r == '催泪':
            consecutive_cry += 1
            max_cry = max(max_cry, consecutive_cry)
        else:
            consecutive_cry = 0
    checks.append(('催泪不连续', max_cry <= 1, f'最长连续{max_cry}章'))

    # 检查转折不连续
    consecutive_turn = 0
    max_turn = 0
    for r in all_rhythms:
        if r == '转折':
            consecutive_turn += 1
            max_turn = max(max_turn, consecutive_turn)
        else:
            consecutive_turn = 0
    checks.append(('转折不连续', max_turn <= 1, f'最长连续{max_turn}章'))

    for name, passed, detail in checks:
        status = '✅' if passed else '⚠️'
        print(f"  {status} {name}（{detail}）")

    # 写作建议
    print(f"\n{'─'*50}")
    print("💡 写作建议")
    print(f"{'─'*50}")

    # 基于预测的第一个章节给出具体建议
    if forecast:
        first = forecast[0]
        rhythm = first['rhythm']
        tips = {
            '日常': [
                '用感官细节营造氛围（声音、气味、光线）',
                '人物互动推进关系，加入幽默对话',
                '中间设一个小冲突或异常发现',
                '结尾铺一个轻钩子（伏笔/异常细节）',
            ],
            '悬念': [
                '开头抛出核心疑问或异常现象',
                '线索逐条展开，有真有假',
                '用问答式对话推进推理',
                '结尾新谜团或颠覆性信息',
            ],
            '紧张': [
                '开头直接进入紧张状态，不做铺垫',
                '信息快速叠加，每段都有新发现或危机',
                '短句密集轰炸（≤10字的句子连续出现）',
                '结尾留强悬念钩子',
            ],
            '催泪': [
                '开头用日常或平静场景铺垫，制造反差',
                '情感线索用细节而非形容词表达',
                '克制表达比煽情更有力——沉默比语言更有力',
                '结尾金句或留白',
            ],
            '转折': [
                '开头做误导性铺垫，让读者以为走向A',
                '看似正常的推进，暗藏伏笔',
                '核心转折瞬间——短句轰炸+认知颠覆',
                '转折后余波+新方向暗示',
            ],
        }
        print(f"\n  下一章（第{first['chapter']}章）节奏：{RHYTHM_LABELS.get(rhythm, rhythm)}")
        print(f"  目标紧张度：{first['target_tension']}")
        for j, tip in enumerate(tips.get(rhythm, []), 1):
            print(f"    {j}. {tip}")

    if outline_hints:
        matched = sum(1 for f in forecast if '大纲提示' in f['reason'])
        print(f"\n  📋 大纲提示：{len(outline_hints)}章有大纲参考，{matched}章预测与大纲一致")

def main():
    parser = argparse.ArgumentParser(description='节奏预测：基于已写章节预测未来节奏')
    parser.add_argument('text_dir', help='正文目录路径')
    parser.add_argument('--count', type=int, default=7, help='预测章节数（默认7，最多10）')
    parser.add_argument('--outline', help='大纲文件路径（可选，用于结合大纲调整预测）')
    parser.add_argument('--character-states', '--character-arc', help='角色状态/弧线文件路径（character_states.json 或 character_arcs.json）')
    parser.add_argument('--json', action='store_true', help='JSON格式输出')
    parser.add_argument('--version', action='version', version='tension_forecast v2.1.0 (novel-writer skill)')
    args = parser.parse_args()

    count = min(args.count, 10)

    # 读取已有章节
    chapters = list_chapters(args.text_dir)
    if not chapters:
        print("[错误] 未找到章节文件")
        sys.exit(1)

    # 计算紧张度
    existing_tensions = []
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        if not content:
            continue
        density, hook_types = count_hook_density(content)
        dialogue_ratio = count_dialogue_ratio(content)
        short_ratio = count_short_sentence_ratio(content)
        tension = compute_tension(density, dialogue_ratio, short_ratio, hook_types)
        existing_tensions.append(tension)

    if not existing_tensions:
        print("[错误] 没有可分析的章节内容")
        sys.exit(1)

    # 解析大纲提示
    outline_hints = None
    if args.outline and os.path.isfile(args.outline):
        last_chapter = len(existing_tensions)
        outline_data = parse_outline_keywords(args.outline, last_chapter + 1)
        if outline_data:
            outline_hints = {}
            for ch_num, data in outline_data.items():
                hint = outline_to_rhythm_hint(data['keywords'])
                if hint:
                    outline_hints[ch_num] = hint

    # 加载角色弧线
    arc_phases = None
    arc_adj = None
    arc_details = []
    if args.character_states:
        arc_phases = load_character_arcs(args.character_states)
        if arc_phases:
            arc_adj, arc_details = get_arc_adjustment(arc_phases)

    # 生成预测
    forecast, trend, slope, phase = generate_forecast(
        existing_tensions, count=count, outline_hints=outline_hints, arc_adj=arc_adj
    )

    if args.json:
        output = {
            'total_existing': len(existing_tensions),
            'trend': trend,
            'slope': round(slope, 2),
            'phase': phase,
            'avg_recent_tension': round(sum(existing_tensions[-10:]) / min(len(existing_tensions), 10), 1),
            'character_arc_adjustment': arc_adj,
            'forecast': forecast,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        # 角色弧线信息
        if arc_details:
            print(f"\n{'─'*50}")
            print("🎭 角色弧线调整")
            print(f"{'─'*50}")
            for detail in arc_details:
                print(f"  • {detail}")

        print_forecast(forecast, trend, slope, phase, existing_tensions, outline_hints)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 tension_forecast.py <正文目录> [--count N] [--outline 大纲文件] [--json]")
        print("\n示例:")
        print("  python3 tension_forecast.py 正文/")
        print("  python3 tension_forecast.py 正文/ --count 10")
        print("  python3 tension_forecast.py 正文/ --outline 大纲.md")
        print("  python3 tension_forecast.py 正文/ --character-states character_states.json")
        print("  python3 tension_forecast.py 正文/ --character-arc character_arcs.json")
        sys.exit(1)
    main()
