#!/usr/bin/env python3
"""
长篇小说重复用词/句式检测脚本 v2.2.1
扫描正文目录，检测高频重复用词、句式结构重复、描写重复

用法：
  python3 repetition_check.py --novel-dir <正文目录> [--threshold 10] [--suggest] [--format text|json]

检查项：
  1. 高频词检测（单章词频超标 + 跨章连续重复）
  2. 句式重复检测（连续相同句式结构 + 相同段落开头）
  3. 描写重复检测（重复表情/动作/比喻）
  4. 数据输出（每章重复热力图 + 全书TOP20 + 替代词建议）
"""

import os
import re
import sys
import json
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from typing import Any, Dict, List, Optional, Tuple, Set

# ============================================================
# 版本
# ============================================================
VERSION = "v2.2.1"

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


def normalize_text(text: str) -> str:
    """统一全角半角，去除多余空格"""
    text = text.replace('\u3000', ' ')
    text = re.sub(r'[ \t]+', ' ', text)
    return text


def list_chapters(dir_path: str) -> List[Tuple[int, str, str]]:
    """列出章节文件，返回 [(章节号, 完整路径, 文件名)]"""
    if not os.path.isdir(dir_path):
        print(f"[错误] 目录不存在: {dir_path}")
        return []
    chapters: List[Tuple[int, str, str]] = []
    seen: Dict[int, str] = {}
    for f in sorted(os.listdir(dir_path)):
        if not (f.endswith('.md') or f.endswith('.txt')):
            continue
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


# ============================================================
# 停用词表（中文常见虚词）
# ============================================================

STOP_WORDS: Set[str] = {
    # 代词
    '他', '她', '它', '我', '你', '这', '那', '这个', '那个', '这些', '那些',
    '什么', '怎么', '怎样', '哪', '哪里', '谁', '自己', '大家', '别人',
    # 介词/连词
    '的', '了', '在', '是', '我', '有', '和', '就', '不', '人', '都', '一',
    '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看',
    '好', '自己', '这', '他', '她', '它', '那', '个', '们', '吗', '吧', '呢',
    '啊', '把', '被', '让', '给', '对', '向', '从', '往', '到', '用', '以',
    '为', '与', '及', '或', '而', '但', '却', '又', '且', '则', '若', '如',
    '因', '故', '所', '之', '其', '此', '该', '各', '每', '某', '任', '何',
    '还', '再', '又', '也', '都', '就', '才', '已', '曾', '将', '正', '在',
    '只', '就', '才', '已', '曾', '将', '正', '在', '正', '没', '不', '别',
    '比', '更', '最', '太', '极', '挺', '好', '真', '多', '少', '大', '小',
    # 常见动词/副词（太短，信息量低）
    '能', '可以', '得', '地', '来', '去', '过', '起', '开', '出', '入',
    '下', '中', '里', '外', '前', '后', '左', '右', '内', '间',
    '以', '于', '等', '等等', '吧', '啊', '呀', '哇', '哦', '嗯', '哈',
    # 常见时间词
    '然后', '于是', '接着', '随后', '之后', '以后', '这时', '那时', '此时',
    '当时', '以后', '后来', '最终', '最后', '首先', '其次',
}

# 常见角色名后缀，用于识别角色名避免误报
NAME_SUFFIXES = {'哥', '姐', '叔', '伯', '婶', '爷', '奶', '婆', '公', '妹', '弟', '妈', '爸'}


def _is_likely_name(word: str) -> bool:
    """粗略判断是否像角色名（2-4字中文，不含标点）

    通过常见姓氏开头 + 2-3字长度来缩小范围，避免误杀普通词汇。
    """
    if not re.fullmatch(r'[\u4e00-\u9fff]{2,4}', word):
        return False
    if word in STOP_WORDS:
        return False
    # 常见姓氏前缀（百家姓高频）
    common_surnames = (
        '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
        '戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳酆鲍史唐'
        '费廉岑薛雷贺倪汤滕殷罗毕郝邬安常乐于时傅皮卞齐康伍余元卜顾孟平黄'
        '和穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁'
        '杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍'
        '虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚程'
        '嵇邢滑裴陆荣翁荀羊於惠甄曲家封芮羿储靳汲邴糜松井段富巫乌焦巴弓牧隗'
        '山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙叶幸司韶'
    )
    return word[0] in common_surnames and 2 <= len(word) <= 4


# ============================================================
# 1. 高频词检测
# ============================================================

def _tokenize_chinese(text: str) -> List[str]:
    """简单的中文分词：提取文本中所有2-4字中文词组

    注：不做精确分词，使用滑动窗口提取候选词。
    实际场景可替换为 jieba 等分词器。
    """
    words: List[str] = []
    # 提取所有连续中文片段
    for m in re.finditer(r'[\u4e00-\u9fff]+', text):
        seg = m.group(0)
        # 提取 2-4 字中文片段
        for length in (4, 3, 2):
            for i in range(len(seg) - length + 1):
                chunk = seg[i:i + length]
                words.append(chunk)
    return words


def check_high_frequency_words(
    chapters: List[Tuple[int, str, str]],
    threshold: int = 10,
    character_names: Optional[Set[str]] = None,
) -> List[Dict[str, Any]]:
    """检测单章高频词和跨章连续重复词"""
    issues: List[Dict[str, Any]] = []
    known_names = character_names or set()

    # --- 单章词频统计 ---
    chapter_word_counts: Dict[int, Counter] = {}
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        words = _tokenize_chinese(content)
        counter = Counter(w for w in words if w not in STOP_WORDS and len(w) >= 2)
        chapter_word_counts[num] = counter

        for word, count in counter.most_common(50):
            if count > threshold and word not in known_names and not _is_likely_name(word):
                issues.append({
                    'type': '单章高频词',
                    'severity': 'medium',
                    'chapter': num,
                    'word': word,
                    'count': count,
                    'detail': f'第{num}章「{word}」出现{count}次（阈值{threshold}）',
                    'suggestion': '',
                })

    # --- 全书分散高频词（单章不超标但全书累积多） ---
    total_counter: Counter = Counter()
    chapter_presence: Dict[str, Set[int]] = defaultdict(set)
    for cn, counter in chapter_word_counts.items():
        for word, count in counter.items():
            total_counter[word] += count
            chapter_presence[word].add(cn)

    # 筛选满足全局阈值的词，而非遍历全部
    global_threshold = max(threshold * 2, 20)  # 全书累计阈值
    min_chapters = 3  # 至少出现在3个章节
    dispersed_candidates = [(w, t) for w, t in total_counter.items()
                           if t >= global_threshold
                           and len(chapter_presence[w]) >= min_chapters
                           and w not in STOP_WORDS
                           and w not in known_names
                           and not _is_likely_name(w)]
    dispersed_candidates.sort(key=lambda x: -x[1])
    for word, total in dispersed_candidates:
            ch_count = len(chapter_presence[word])
        # 检查是否已被单章高频检测覆盖（单章超过阈值*3才算覆盖）
            max_single = max(chapter_word_counts[cn][word] for cn in chapter_presence[word])
            if max_single <= threshold * 3:
                issues.append({
                    'type': '全书分散高频词',
                    'severity': 'medium',
                    'chapter': min(chapter_presence[word]),
                    'word': word,
                    'count': total,
                    'detail': f'「{word}」全书出现{total}次，分散在{ch_count}章（单章均未超阈值{threshold}）',
                    'suggestion': '',
                })

    # --- 跨章连续重复 ---
    ch_nums = sorted(chapter_word_counts.keys())
    for i in range(len(ch_nums) - 2):
        triad = ch_nums[i:i + 3]
        common_words = set(chapter_word_counts[triad[0]].keys())
        for cn in triad[1:]:
            common_words &= set(chapter_word_counts[cn].keys())
        for word in common_words:
            if word in STOP_WORDS or word in known_names:
                continue
            counts = [chapter_word_counts[cn][word] for cn in triad]
            if all(c >= threshold // 2 for c in counts):
                issues.append({
                    'type': '跨章连续重复',
                    'severity': 'medium',
                    'chapter': triad[0],
                    'word': word,
                    'count': sum(counts),
                    'detail': f'「{word}」在第{triad[0]}-{triad[2]}章连续大量出现（{"/".join(map(str, counts))}次）',
                    'suggestion': '',
                })

    return issues


# ============================================================
# 2. 句式重复检测
# ============================================================

def _split_sentences(text: str) -> List[str]:
    """按中文句号/问号/叹号分句"""
    sents = re.split(r'[。！？\n]+', text)
    return [s.strip() for s in sents if len(s.strip()) >= 2]


def _sentence_pattern(sentence: str) -> str:
    """提取句子的简化结构模式

    规则：
    - 单个中文 → C
    - 多个连续中文（2+） → W
    - 数字 → D
    - 标点 → P
    生成简短结构签名，用于检测重复句式
    """
    tokens = re.findall(r'[\u4e00-\u9fff]|[\u4e00-\u9fff]{2,}|\d+|[^\w\s]', sentence)
    pattern_chars = []
    for t in tokens:
        if re.fullmatch(r'\d+', t):
            pattern_chars.append('D')
        elif len(t) >= 2:
            pattern_chars.append('W')
        elif re.fullmatch(r'[\u4e00-\u9fff]', t):
            pattern_chars.append('C')
        else:
            pattern_chars.append('P')
    return ''.join(pattern_chars[:12])


def check_sentence_patterns(
    chapters: List[Tuple[int, str, str]],
    consecutive_threshold: int = 3,
) -> List[Dict[str, Any]]:
    """检测连续相同句式结构和相同段落开头"""
    issues: List[Dict[str, Any]] = []

    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        sentences = _split_sentences(content)

        # --- 连续相同句式 ---
        patterns = [_sentence_pattern(s) for s in sentences]
        streak = 1
        streak_start = 0
        for i in range(1, len(patterns)):
            if patterns[i] == patterns[i - 1] and patterns[i]:
                streak += 1
            else:
                if streak >= consecutive_threshold:
                    examples = sentences[streak_start:streak_start + streak]
                    issues.append({
                        'type': '句式重复',
                        'severity': 'medium',
                        'chapter': num,
                        'word': '',
                        'count': streak,
                        'detail': f'第{num}章连续{streak}句相同句式结构',
                        'suggestion': f'示例：「{examples[0][:30]}…」→ 变换句式或拆分',
                    })
                streak = 1
                streak_start = i
        # 尾部
        if streak >= consecutive_threshold:
            examples = sentences[streak_start:streak_start + streak]
            issues.append({
                'type': '句式重复',
                'severity': 'medium',
                'chapter': num,
                'word': '',
                'count': streak,
                'detail': f'第{num}章连续{streak}句相同句式结构',
                'suggestion': f'示例：「{examples[0][:30]}…」→ 变换句式或拆分',
            })

        # --- 相同段落开头 ---
        paragraphs = [p.strip() for p in content.split('\n') if p.strip() and len(p.strip()) >= 4]
        if len(paragraphs) < 3:
            continue
        first_chars = [p[0] for p in paragraphs]
        streak = 1
        streak_start = 0
        for i in range(1, len(first_chars)):
            if first_chars[i] == first_chars[i - 1]:
                streak += 1
            else:
                if streak >= consecutive_threshold:
                    char = first_chars[streak_start]
                    issues.append({
                        'type': '段落开头重复',
                        'severity': 'low',
                        'chapter': num,
                        'word': char,
                        'count': streak,
                        'detail': f'第{num}章连续{streak}段以「{char}」开头',
                        'suggestion': '变换段落起始词，增强节奏感',
                    })
                streak = 1
                streak_start = i
        if streak >= consecutive_threshold:
            char = first_chars[streak_start]
            issues.append({
                'type': '段落开头重复',
                'severity': 'low',
                'chapter': num,
                'word': char,
                'count': streak,
                'detail': f'第{num}章连续{streak}段以「{char}」开头',
                'suggestion': '变换段落起始词，增强节奏感',
            })

    return issues


# ============================================================
# 3. 描写重复检测
# ============================================================

# 常见重复描写模式库
KNOWN_EXPRESSION_PATTERNS: List[Tuple[str, str]] = [
    # (正则模式, 标签)
    (r'皱了皱眉', '皱眉'),
    (r'嘴角[一二]?[勾挑弧]', '嘴角动作'),
    (r'深[吸呼]一?口?气', '深呼吸'),
    (r'叹了口?气', '叹气'),
    (r'摇了摇头', '摇头'),
    (r'点了点头', '点头'),
    (r'咬了咬牙', '咬牙'),
    (r'攥紧拳头', '攥拳'),
    (r'红了眼眶', '眼眶泛红'),
    (r'喉[间头]?[一一]?动', '喉结滚动'),
    (r'苦笑[一二]?声', '苦笑'),
    (r'无奈[的地]?笑', '无奈笑'),
    (r'转[过身]?头[来看]', '转头'),
    (r'垂下[了]?眼[帘睛]?', '垂眼'),
    (r'抬[起手]?[头眼]?', '抬头/抬眼'),
    (r'双手[交抱环]在胸前', '抱臂'),
    (r'嘴角抽[了]?搐', '嘴角抽搐'),
    (r'眼睛一亮', '眼睛一亮'),
]

# 比喻标记词
METAPHOR_MARKERS = ['像', '如同', '好比', '恰似', '好比', '好似', '犹如', '宛如', '仿佛']


def check_expression_repetition(
    chapters: List[Tuple[int, str, str]],
    repeat_threshold: int = 2,
) -> List[Dict[str, Any]]:
    """检测重复的表情/动作/比喻描写"""
    issues: List[Dict[str, Any]] = []

    # --- 全书表情/动作统计 ---
    expr_counter: Counter = Counter()  # (标签, 正则) → 出现次数+章节
    expr_chapters: Dict[str, List[int]] = defaultdict(list)

    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        for pattern, label in KNOWN_EXPRESSION_PATTERNS:
            matches = re.findall(pattern, content)
            if matches:
                expr_counter[label] += len(matches)
                expr_chapters[label].append(num)

    for label, total_count in expr_counter.items():
        if total_count > repeat_threshold:
            ch_list = expr_chapters[label]
            issues.append({
                'type': '描写重复',
                'severity': 'low' if total_count <= 5 else 'medium',
                'chapter': ch_list[0],
                'word': label,
                'count': total_count,
                'detail': f'「{label}」类描写在全书中出现{total_count}次，涉及{len(ch_list)}章',
                'suggestion': '',
            })

    # --- 比喻重复检测 ---
    metaphor_phrases: Dict[str, List[int]] = defaultdict(list)
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        for marker in METAPHOR_MARKERS:
            # 提取 marker 后面 4-20 字的比喻短语
            for m in re.finditer(re.escape(marker) + r'(.{4,20}?)[，。！？；\n]', content):
                phrase = m.group(1).strip()
                if phrase:
                    metaphor_phrases[phrase].append(num)

    for phrase, chapters_list in metaphor_phrases.items():
        if len(chapters_list) > repeat_threshold:
            issues.append({
                'type': '比喻重复',
                'severity': 'low',
                'chapter': chapters_list[0],
                'word': phrase[:10],
                'count': len(chapters_list),
                'detail': f'比喻「…{phrase[:20]}…」在{len(chapters_list)}章中重复使用',
                'suggestion': '更换不同的比喻表达',
            })

    return issues


# ============================================================
# 4. 替代词建议
# ============================================================

# 常见高频词的替代建议库
SUGGESTION_MAP: Dict[str, List[str]] = {
    '不禁': ['直接写身体反应', '写出本能动作'],
    '微微': ['写出具体幅度', '用对比描述微小变化'],
    '淡淡': ['写出具体语气/表情', '用旁观者视角描述'],
    '缓缓': ['写出具体速度', '写出阻力或犹豫'],
    '竟然': ['用角色心理替代', '写出意外来源'],
    '突然': ['先铺垫再转折', '用感官变化引出'],
    '默默': ['写出无声的具体方式', '用小动作代替'],
    '轻轻': ['写出力度感', '用声音大小描述'],
    '深深': ['写出具体深度/时长', '用体感替代'],
    '嘴角': ['改写嘴部其他动作', '用眼神替代'],
    '皱眉': ['写出眉头变化', '用其他表情替代'],
    '叹气': ['写出叹息原因', '用沉默/动作替代'],
}


def get_suggestions(word: str) -> List[str]:
    """获取替代词建议"""
    for key, suggestions in SUGGESTION_MAP.items():
        if key in word:
            return suggestions
    return ['考虑用更具体的描写替代', '变换表达角度（感官/比喻/动作）']


# ============================================================
# 汇总与输出
# ============================================================

def generate_heatmap(
    chapter_word_issues: List[Dict[str, Any]],
    chapters: List[Tuple[int, str, str]],
) -> Dict[int, Dict[str, Any]]:
    """生成每章重复热力图数据

    返回 {章节号: {重复词数, 高频词列表, 严重度}}
    """
    heatmap: Dict[int, Dict[str, Any]] = {}
    for num, _, _ in chapters:
        heatmap[num] = {'repeat_count': 0, 'words': [], 'severity': 'ok'}

    for issue in chapter_word_issues:
        ch = issue.get('chapter', 0)
        if ch in heatmap:
            heatmap[ch]['repeat_count'] += 1
            word = issue.get('word', '')
            if word:
                heatmap[ch]['words'].append(word)
            sev = issue.get('severity', 'medium')
            if sev == 'high':
                heatmap[ch]['severity'] = 'high'
            elif sev == 'medium' and heatmap[ch]['severity'] != 'high':
                heatmap[ch]['severity'] = 'medium'

    return heatmap


def get_top20(issues: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """全书高频重复词 TOP20"""
    word_counts: Counter = Counter()
    for issue in issues:
        if issue['type'] in ('单章高频词', '跨章连续重复') and issue.get('word'):
            word_counts[issue['word']] += issue.get('count', 1)
    top = word_counts.most_common(20)
    return [{'rank': i + 1, 'word': w, 'total': c} for i, (w, c) in enumerate(top)]


def format_text_report(
    issues: List[Dict[str, Any]],
    heatmap: Dict[int, Dict[str, Any]],
    top20: List[Dict[str, Any]],
    suggest: bool,
) -> str:
    """格式化文本报告"""
    lines: List[str] = []
    lines.append('=' * 60)
    lines.append(f'🔍 重复用词/句式检测报告 {VERSION}')
    lines.append('=' * 60)

    # 摘要
    total = len(issues)
    by_type: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for issue in issues:
        by_type[issue['type']].append(issue)

    lines.append(f'\n共发现 {total} 个问题：')
    for t, items in sorted(by_type.items()):
        lines.append(f'  • {t}：{len(items)}个')

    # 热力图
    lines.append('\n--- 每章重复热力图 ---')
    severity_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢', 'ok': '✅'}
    for ch in sorted(heatmap.keys()):
        info = heatmap[ch]
        icon = severity_icon.get(info['severity'], '⬜')
        words_str = '、'.join(info['words'][:5]) if info['words'] else ''
        lines.append(f'  第{ch:03d}章 {icon} {info["repeat_count"]}处重复 {words_str}')

    # TOP20
    if top20:
        lines.append('\n--- 全书高频重复词 TOP20 ---')
        for item in top20:
            lines.append(f'  {item["rank"]:>2}. 「{item["word"]}」共{item["total"]}次')

    # 详细问题
    lines.append('\n--- 详细问题 ---')
    for issue in issues:
        icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(issue.get('severity', 'medium'), '⬜')
        lines.append(f'  {icon} [{issue["type"]}] {issue["detail"]}')
        if issue.get('suggestion'):
            lines.append(f'      💡 {issue["suggestion"]}')
        # 替代词建议
        if suggest and issue.get('word'):
            suggestions = get_suggestions(issue['word'])
            if suggestions:
                lines.append(f'      📝 替代建议：{"；".join(suggestions)}')

    return '\n'.join(lines)


def run_check(
    novel_dir: str,
    threshold: int = 10,
    suggest: bool = False,
    output_format: str = 'text',
) -> Dict[str, Any]:
    """执行全部检测"""
    chapters = list_chapters(novel_dir)
    if not chapters:
        print('[错误] 未找到章节文件')
        return {'error': '未找到章节文件', 'issues': [], 'heatmap': {}, 'top20': []}

    numbered = [c for c in chapters if c[0] > 0]
    print(f'📖 找到 {len(numbered)} 个章节')
    if numbered:
        print(f'   第{numbered[0][0]}章 ~ 第{numbered[-1][0]}章')

    print('⏳ 正在检测...')

    # 收集角色名（从设定词典或文件名推测）
    character_names: Set[str] = set()
    dict_file = os.path.join(os.path.dirname(novel_dir.rstrip('/')), '设定词典.md')
    if os.path.isfile(dict_file):
        dict_content = read_file(dict_file)
        for m in re.finditer(r'([\u4e00-\u9fff]{2,4})[：:（(]', dict_content):
            character_names.add(m.group(1))

    # 执行检查
    print('  → 高频词检测...')
    freq_issues = check_high_frequency_words(chapters, threshold, character_names)

    print('  → 句式重复检测...')
    pattern_issues = check_sentence_patterns(chapters)

    print('  → 描写重复检测...')
    expr_issues = check_expression_repetition(chapters)

    all_issues = freq_issues + pattern_issues + expr_issues

    # 生成汇总数据
    heatmap = generate_heatmap(all_issues, chapters)
    top20 = get_top20(all_issues)

    # 输出
    if output_format == 'json':
        result = {
            'version': VERSION,
            'total_issues': len(all_issues),
            'issues': all_issues,
            'heatmap': heatmap,
            'top20': top20,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return result
    else:
        report = format_text_report(all_issues, heatmap, top20, suggest)
        print(report)
        return {
            'total_issues': len(all_issues),
            'issues': all_issues,
            'heatmap': heatmap,
            'top20': top20,
        }


def main():
    parser = argparse.ArgumentParser(
        description=f'长篇小说重复用词/句式检测 {VERSION}',
    )
    parser.add_argument('--novel-dir', required=True, help='正文目录路径')
    parser.add_argument('--threshold', type=int, default=10, help='词频阈值（默认10）')
    parser.add_argument('--suggest', action='store_true', help='输出替代词建议')
    parser.add_argument('--format', choices=['text', 'json'], default='text', help='输出格式')
    parser.add_argument('--version', action='version', version=f'repetition_check {VERSION} (novel-writer skill)')
    args = parser.parse_args()

    run_check(args.novel_dir, args.threshold, args.suggest, args.format)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'用法: python3 repetition_check.py --novel-dir <正文目录> [--threshold 10] [--suggest] [--format text|json]')
        sys.exit(1)
    main()
