#!/usr/bin/env python3
"""
长篇小说一致性检查脚本 v2
扫描正文目录，交叉比对追踪表和设定词典，检测前后矛盾

用法：
  python3 consistency_check.py <正文目录> [追踪表路径] [设定词典路径]

检查项：
  1. 角色称呼一致性
  2. 设定冲突（同一事物不同描述）
  3. 时间线错误
  4. 逻辑漏洞（角色不应知道的信息）
  5. 数值矛盾
  6. AI高频词
  7. 章节字数
  8. 视角一致性
  9. 角色状态机冲突
  10. 大纲偏差检测
"""

import os
import re
import sys
import json
import shutil
import argparse
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime
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

def load_json(path: str) -> Optional[Dict[str, Any]]:
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return None

DRAFT_KEYWORDS = ('草稿', 'draft', 'wip', 'Draft', 'WIP', 'DRAFT')

def is_draft_filename(fname: str) -> bool:
    """判断文件名是否为草稿"""
    lower = fname.lower()
    return any(kw.lower() in lower for kw in DRAFT_KEYWORDS)

def list_chapters(dir_path: str, include_unnumbered: bool = False, skip_drafts: bool = False) -> List[Tuple[int, str, str]]:
    """列出章节文件
    include_unnumbered: 是否包含无章节号的文件（如'前两章.md'草稿），赋予负数编号
    skip_drafts: 是否跳过草稿文件（文件名含 草稿/draft/WIP）
    """
    if not os.path.isdir(dir_path):
        print(f"[错误] 正文目录不存在: {dir_path}")
        return []
    chapters = []
    seen = {}  # 同章节号去重：只保留一个文件
    unnumbered_idx = -1
    skipped = []
    for f in sorted(os.listdir(dir_path)):
        if f.endswith('.md') or f.endswith('.txt'):
            if skip_drafts and is_draft_filename(f):
                skipped.append(f)
                continue
            match = re.search(r'第(\d+)章', f)
            if match:
                num = int(match.group(1))
                # 去重：同章节号，优先保留文件名含标题的（有下划线分隔标题的版本）
                if num in seen:
                    old_f = seen[num]
                    # 保留标题更具体的版本
                    if '_' in f and '_' not in old_f:
                        seen[num] = f
                else:
                    seen[num] = f
            elif include_unnumbered and f not in ('README.md', '目录.md', '大纲.md'):
                # 排除明显不是章节的文件
                exclude_patterns = ('大纲', '设定', '追踪', '方案', '清单', 'checklist',
                    '修改', 'backup', 'outline', '旧版', '标注', '废弃', '卷摘要',
                    'restaurant', 'saas', 'checklist_', 'ch[0-9]', 'novel_final',
                    '小说_第', '家庭AI', 'send', 'latest', 'v2', 'v3', 'v4', 'v5',
                    '完整章节', '章节列表', '前两章')
                if any(p.lower() in f.lower() for p in exclude_patterns):
                    continue
                # 排除不含"章"字的文件
                if '章' not in f:
                    continue
                chapters.append((unnumbered_idx, os.path.join(dir_path, f), f))
                unnumbered_idx -= 1
    for num, f in sorted(seen.items()):
        chapters.append((num, os.path.join(dir_path, f), f))
    chapters.sort(key=lambda x: x[0])
    if skipped:
        print(f"  🚫 跳过 {len(skipped)} 个草稿文件: {', '.join(skipped)}")
    return chapters

def normalize_text(text: str) -> str:
    """统一全角半角，去除多余空格"""
    text = text.replace('\u3000', ' ')
    text = re.sub(r'[ \t]+', ' ', text)
    return text

# ============================================================
# 角色状态机加载
# ============================================================

def _extract_characters(data):
    """Extract the characters dict from the full JSON structure.
    Returns a dict mapping character name to its data, preserving the
    original structure expected by the rest of the consistency checks.
    """
    if not isinstance(data, dict):
        return {}
    # The JSON may contain top‑level metadata such as "novel",
    # "lastUpdated", "currentChapter" and the actual characters under
    # the "characters" key.
    return data.get('characters', {})

def _validate_character_states_schema(data, filepath):
    """校验 character_states.json 格式，缺少必要字段时报错而不崩溃"""
    if not isinstance(data, dict):
        print(f"  [错误] {filepath}: 顶层结构应为 dict，实际为 {type(data).__name__}")
        return False
    # 兼容：data 可能是 {"characters": {...}} 或直接 {角色名: {...}}
    chars = data.get('characters', data) if isinstance(data.get('characters', data), dict) else {}
    required_snapshot_fields = ['location']  # 至少要有位置
    errors = []
    for char_name, char_data in chars.items():
        if not isinstance(char_data, dict):
            errors.append(f"角色 '{char_name}' 的数据不是 dict")
            continue
        snapshots = char_data.get('snapshots', {})
        if not isinstance(snapshots, dict):
            errors.append(f"角色 '{char_name}' 的 snapshots 不是 dict")
            continue
        for ch_num, snapshot in snapshots.items():
            if not isinstance(snapshot, dict):
                errors.append(f"角色 '{char_name}' 章节{ch_num}的快照不是 dict")
    if errors:
        for e in errors[:5]:  # 最多报5条
            print(f"  [警告] {filepath}: {e}")
        if len(errors) > 5:
            print(f"  [警告] ...还有{len(errors)-5}个问题")
    return True

def load_character_states(tracking_dir):
    """
    从 character_states.json 加载角色状态机
    返回: { 角色名: { "snapshots": { 章节号: {...} } } }
    """
    state_file = os.path.join(tracking_dir, 'character_states.json')
    data = load_json(state_file)
    if data:
        _validate_character_states_schema(data, state_file)
        return _extract_characters(data)

    # 尝试从 tracking_dir 的父目录找
    state_file = os.path.join(os.path.dirname(tracking_dir), 'character_states.json')
    data = load_json(state_file)
    if data:
        _validate_character_states_schema(data, state_file)
    return _extract_characters(data)

# ============================================================
# 检查1: 角色称呼一致性
# ============================================================

def check_name_consistency(chapters: List[Tuple[int, str, str]], dict_content: str) -> List[Dict[str, Any]]:
    """检测同一角色在不同章节的称呼不一致"""
    issues = []

    # 从设定词典中提取角色→别名映射
    name_aliases = {}
    alias_pattern = re.compile(r'(.+?)[：:]\s*(?:又名|别名|昵称|简称|也叫|又称)\s*(.+?)(?:\n|$)')
    for match in alias_pattern.finditer(dict_content):
        main_name = match.group(1).strip()
        aliases = [a.strip() for a in re.split(r'[、，,]', match.group(2))]
        name_aliases[main_name] = aliases

    # 从正文中提取"名字+说/道"模式，统计每个名字的出现章节
    name_chapters = defaultdict(lambda: defaultdict(int))
    name_pattern = re.compile(r'([\u4e00-\u9fff]{2,4})(?:说|道|笑|喊|叫|问|答|叹|吼|低声)')

    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        seen_in_chapter = set()
        for match in name_pattern.finditer(content):
            name = match.group(1)
            # 过滤常见非人名词语
            stop_words = {'大家', '别人', '自己', '什么', '怎么', '这个', '那个', '他的', '她的',
                         '这时', '那时', '然后', '于是', '因为', '所以', '如果', '虽然', '但是',
                         '可是', '不过', '而且', '或者', '以及', '已经', '正在', '将要'}
            if name not in stop_words and len(name) >= 2 and name not in seen_in_chapter:
                name_chapters[name][num] += 1
                seen_in_chapter.add(name)

    # 检测可能的同一角色不同称呼（基于共现频率和设定词典）
    for main_name, aliases in name_aliases.items():
        main_chapters = set(name_chapters.get(main_name, {}).keys())
        for alias in aliases:
            alias_chapters = set(name_chapters.get(alias, {}).keys())
            # 如果主名和别名交替出现，说明称呼不统一
            if main_chapters and alias_chapters:
                overlap = main_chapters & alias_chapters
                if len(overlap) == 0 and len(main_chapters) > 2 and len(alias_chapters) > 2:
                    issues.append({
                        'type': '角色称呼不一致',
                        'severity': 'high',
                        'detail': f'"{main_name}" 出现在第{min(main_chapters)}-{max(main_chapters)}章，'
                                  f'"{alias}" 出现在第{min(alias_chapters)}-{max(alias_chapters)}章，'
                                  f'可能是同一角色的不同称呼',
                        'suggestion': f'统一使用"{main_name}"，或在特定场景使用"{alias}"'
                    })

    return issues

# ============================================================
# 检查2: 设定冲突检测
# ============================================================

def check_setting_conflicts(chapters, dict_content):
    """
    检测设定冲突：同一关键词在不同章节描述不同
    策略：提取设定词典中的关键设定，在正文中搜索并比对
    """
    issues = []

    # 提取设定词典中的硬性规则和关键数值
    rules = []
    # 匹配 "XXX是YYY" "XXX有YYY" 等陈述句
    rule_pattern = re.compile(r'[·\-–]\s*(.+?)[是为有等于]\s*(.+?)(?:\n|$)')
    for match in rule_pattern.finditer(dict_content):
        rules.append((match.group(1).strip(), match.group(2).strip()))

    # 从正文中提取具体描述性信息，按关键词分组
    keyword_descriptions = defaultdict(list)
    for keyword, value in rules:
        for num, path, fname in chapters:
            content = normalize_text(read_file(path))
            # 搜索包含关键词的句子
            sentences = re.split(r'[。！？\n]', content)
            for sent in sentences:
                if keyword in sent and len(sent) < 100:
                    keyword_descriptions[keyword].append({
                        'chapter': num,
                        'sentence': sent.strip(),
                        'canon': value
                    })

    # 比对同一关键词在不同章节的描述
    for keyword, entries in keyword_descriptions.items():
        if len(entries) < 2:
            continue
        # 提取描述中的数值
        value_map = defaultdict(list)
        for entry in entries:
            numbers = re.findall(r'\d+(?:\.\d+)?', entry['sentence'])
            if numbers:
                for n in numbers:
                    value_map[n].append(entry['chapter'])

        # 如果同一关键词有不同数值，报冲突
        if len(value_map) > 1:
            conflict_desc = '、'.join([f'第{chs[0]}章={v}' for v, chs in value_map.items()])
            issues.append({
                'type': '设定冲突',
                'severity': 'high',
                'detail': f'关键词"{keyword}"的数值在不同章节不一致：{conflict_desc}',
                'suggestion': f'设定词典规定为"{dict((k, v) for k, v in rules if k == keyword).get(keyword, "未知")}"'
            })

    return issues

# ============================================================
# 检查3: 时间线检测
# ============================================================

def check_timeline(chapters, tracking_content):
    """检测时间线矛盾"""
    issues = []

    # 提取追踪表中的时间线记录
    timeline = {}
    time_pattern = re.compile(r'第(\d+)章[：:]\s*(?:第?(\d+)天|(\d+)月(\d+)日|过了?(\d+)天)')
    for match in time_pattern.finditer(tracking_content):
        ch = int(match.group(1))
        if match.group(2):
            timeline[ch] = ('day', int(match.group(2)))
        elif match.group(5):
            timeline[ch] = ('elapsed', int(match.group(5)))

    # 从正文中提取时间描述
    chapter_times = {}
    time_indicators = [
        (r'第(\d+)天', 'absolute_day'),
        (r'过了?(\d+)天', 'elapsed_days'),
        (r'(\d+)天前', 'days_ago'),
        (r'三天后|三天前|一周后|一周前|半个月后|一个月后', 'relative'),
    ]

    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        times_found = []
        for pattern, ttype in time_indicators:
            matches = re.findall(pattern, content)
            if matches:
                times_found.append((ttype, matches))
        if times_found:
            chapter_times[num] = times_found

    # 检查时间是否单调递增（第N天的N应该只增不减）
    prev_day = 0
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        day_matches = re.findall(r'第(\d+)天', content)
        for d in day_matches:
            d = int(d)
            if d < prev_day - 1:  # 允许1天误差（跨天描述）
                issues.append({
                    'type': '时间线矛盾',
                    'severity': 'high',
                    'detail': f'第{num}章出现"第{d}天"，但之前已到第{prev_day}天',
                    'suggestion': '检查时间线是否回退，确认故事内时间顺序'
                })
            prev_day = max(prev_day, d)

    return issues

# ============================================================
# 检查4: 数值矛盾
# ============================================================

def check_numeric_conflicts(chapters, character_names=None, tracking_content=''):
    """检测数值前后矛盾（金额、人数、距离、余额等）

    Args:
        chapters: 章节列表
        character_names: 已知角色名集合，提供时仅匹配已知角色（减少误报）
    """
    issues = []

    keyword_numbers = defaultdict(list)

    # 构建已知角色名集合（用于精确匹配）
    if character_names:
        known_names = set(character_names)
    else:
        # 不自动提取：在没有角色名列表时，仅允许2-3字的词作为角色名
        # 且必须在非中文字符之后出现（确保是独立词）
        known_names = None  # None表示不做角色名过滤，改用其他策略
    
    # 常见非人名词汇（2-3字）
    non_name_words = {
        '建筑', '排名', '认为', '别的', '这么', '着这', '着那', '两天',
        '什么', '怎么', '这个', '那个', '公司', '大楼', '总部', '层楼',
        '一层', '一个', '两个', '三个', '这些', '那些', '已经', '正在',
        '将要', '因为', '所以', '如果', '虽然', '但是', '不过', '或者',
        '而且', '以及', '然后', '于是', '这时', '那时', '大家', '别人',
        '自己', '每天', '每年', '每月', '每周', '正常', '大约', '外卖员',
        '快递员', '服务员', '保安', '医生', '护士', '老师', '司机', '老板',
        '经理', '前台', '邻居', '同学', '同事', '如果', '结合', '但',
        '但是', '而且', '或者', '只是', '虽然', '不过', '因为', '所以',
        '但是', '可是', '然而', '不是', '也是', '就是', '还是', '真是',
        '有人', '没人', '有人', '一人', '两人', '三人', '不是', '也是',
        '十三', '一眼', '除了', '还是', '下', '但', '却', '又', '都',
        '和', '与', '的', '了', '着', '过', '在', '到', '被', '把',
        '给', '让', '向', '从', '往', '跟', '比', '对', '是', '有',
        '没', '不', '也', '还', '就', '只', '才', '都', '又', '很',
        '非常', '一般', '有些', '一样', '不少', '不多', '也是', '不是',
        '可以', '能够', '应该', '必须', '需要', '已经', '正在', '将要',
        '之前', '之后', '上面', '下面', '里面', '外面', '前面', '后面',
        '第三天', '上次', '这次', '下次', '但', '不', '了', '着', '过',
        '在', '到', '被', '我', '你', '他', '她', '它',
    }

    def _is_known_character(word):
        """检查是否是已知角色名"""
        if known_names is not None:
            return word in known_names
        # 回退：2-3个字且不在非人名词表中
        if len(word) < 2 or len(word) > 3:
            return False
        return word not in non_name_words

    for num, path, fname in chapters:
        content = normalize_text(read_file(path))

        # 1) 角色名+的+属性 模式（仅匹配2-3字人名）
        # 要求：角色名前面是非中文字符（确保是独立词）
        attr_pattern = re.compile(r'(?:^|[^\u4e00-\u9fff])([\u4e00-\u9fff]{2,3})的(余额|年龄|身家|工资|收入|存款|距离|楼层|身高|体重|价格|费用|估值|市值|资产|房贷|月供|车价)')
        for m in attr_pattern.finditer(content):
            entity = m.group(1)
            if not _is_known_character(entity):
                continue
            attr = m.group(2)
            # 在匹配位置附近找数值
            end_pos = min(len(content), m.end() + 15)
            nearby = content[m.end():end_pos]
            num_match = re.search(r'(?<![\d年月])(\d+(?:\.\d+)?)\s*(万|亿|年|天|岁|米|公里|层|元|块)?', nearby)
            if num_match:
                # 排除月份（如"4月"不是数值属性）
                full_match_pos = m.end() + num_match.start()
                val_end = full_match_pos + len(num_match.group(1))
                if val_end < len(content) and content[val_end:val_end+1] == '月':
                    continue
                keyword = f"{entity}的{attr}"
                value = num_match.group(0).strip()
                keyword_numbers[keyword].append((num, value))

        # 2) 命名实体+余额/数字 模式（如"小张的余额——41年028天"）
        balance_pattern = re.compile(r'(?:^|[^\u4e00-\u9fff])([\u4e00-\u9fff]{2,3})(?:的?余额)[^\d]{0,10}(\d+)年(\d+)天')
        for m in balance_pattern.finditer(content):
            entity = m.group(1)
            if not _is_known_character(entity):
                continue
            value = f"{m.group(2)}年{m.group(3)}天"
            keyword = f"{entity}的余额"
            keyword_numbers[keyword].append((num, value))

        # 3) 独立金额模式（如"估值50亿""380万"）
        money_pattern = re.compile(r'([\u4e00-\u9fff]{2,6})(?:估值|价值|售价|买价|成交价|总交易额)[^\d]{0,5}(\d+(?:\.\d+)?\s*(?:万|亿))')
        for m in money_pattern.finditer(content):
            entity = m.group(1)
            value = m.group(2).strip()
            keyword = f"{entity}的估值/金额"
            keyword_numbers[keyword].append((num, value))

        # 4) 年龄模式（如"24岁的女孩""五十出头"）
        age_pattern = re.compile(r'([\u4e00-\u9fff]{1,4})(?:，|、)?(?:今年|已经)?(?:大概|大约|差不多)?(\d+)岁')
        for m in age_pattern.finditer(content):
            entity = m.group(1)
            if not _is_known_character(entity):
                continue
            keyword = f"{entity}的年龄"
            keyword_numbers[keyword].append((num, m.group(2)))

    def _is_compatible_values(v1, v2):
        """检查两个数值是否兼容（考虑精度简写）
        例如 '42年137天' 和 '42年' 兼容（后者是前者的简写）
        '42' 和 '42年' 也兼容（无单位 vs 有单位，数字相同）
        """
        if v1 == v2:
            return True
        # 提取纯数字部分
        num1 = re.match(r'(\d+)', v1)
        num2 = re.match(r'(\d+)', v2)
        if num1 and num2 and num1.group(1) == num2.group(1):
            return True
        # 提取年份部分进行比对
        year_match1 = re.match(r'(\d+)年', v1)
        year_match2 = re.match(r'(\d+)年', v2)
        if year_match1 and year_match2:
            y1, y2 = year_match1.group(1), year_match2.group(1)
            if y1 == y2:
                return True
        return False

    def _merge_compatible(entries):
        """合并兼容的数值条目，返回真正矛盾的子集"""
        groups = []  # 每组是兼容的entries
        for ch, val in entries:
            placed = False
            for group in groups:
                rep_val = group[0][1]
                if _is_compatible_values(val, rep_val):
                    group.append((ch, val))
                    placed = True
                    break
            if not placed:
                groups.append([(ch, val)])
        return groups

    # 检测同一实体+属性对应不同数值
    for keyword, entries in keyword_numbers.items():
        groups = _merge_compatible(entries)
        # 只在存在多个不兼容组时报矛盾
        if len(groups) > 1 and len(entries) >= 2:
            # 过滤掉仅因精度不同的条目，收集真正矛盾的组
            # 合并展示：每组取一个代表值
            unique_values = [g[0][1] for g in groups]
            ch_label = lambda c: f'第{c}章' if c > 0 else f'草稿({c})'
            # 展示每组代表
            all_entries_flat = []
            for g in groups:
                all_entries_flat.extend(g)
            chapters_str = '、'.join([f'{ch_label(c)}={v}' for c, v in all_entries_flat])
            issues.append({
                'type': '数值矛盾',
                'severity': 'medium',
                'detail': f'{keyword}在不同章节不一致：{chapters_str}',
                'suggestion': '确认正确数值，统一全文'
            })

    return issues

# ============================================================
# 检查5: AI高频词
# ============================================================

AI_WORDS = {
    # 程度/方式副词
    '不禁': 2, '缓缓': 2, '淡淡': 2, '微微': 2,
    '竟然': 2, '居然': 2, '悄然': 2, '默然': 2,
    '不由得': 1, '下意识': 2, '情不自禁': 1,
    '深深地': 1, '轻轻': 2, '默默': 2,
    '一抹': 2, '一丝': 2, '一阵': 3,
    '宛如': 2, '仿佛': 3, '犹如': 2,
    # 动作/神态词
    '莞尔': 2, '颔首': 2, '眸子': 3,
    '嘴角微扬': 1, '似笑非笑': 1, '若有所思': 2,
    '沉吟': 2, '凝视': 3, '端详': 2,
    '驻足': 2, '回眸': 2, '倩影': 1,
    # 说话方式
    '轻声': 3, '柔声': 2, '低声': 3, '悄声': 2,
    # 副词（古风/书面）
    '径直': 2, '赫然': 2, '陡然': 2, '蓦然': 2,
    '竟': 3, '已然': 2,
    '尔后': 1, '旋即': 2, '遂': 1, '乃': 1,
    # 时间副词
    '俄顷': 1, '顷刻': 2, '霎时': 2, '刹那': 2,
    '须臾': 1, '倏忽': 1,
    # 惊讶/意外表达
    '猝不及防': 1, '措手不及': 1, '始料未及': 1,
    '出人意料': 1, '不可思议': 1, '难以置信': 1, '匪夷所思': 1,
    # AI常见比阵/形容
    '像是': 3,  # aileader小说要求≤3处/章
}

def check_ai_words(chapters: List[Tuple[int, str, str]]) -> List[Dict[str, Any]]:
    issues = []
    for num, path, fname in chapters:
        content = read_file(path)
        for word, threshold in AI_WORDS.items():
            count = content.count(word)
            if count > threshold:
                issues.append({
                    'type': 'AI高频词',
                    'severity': 'low',
                    'detail': f'第{num}章 "{word}" 出现{count}次（建议≤{threshold}次）',
                    'suggestion': f'用具体行为描写替代"{word}"'
                })
    return issues

# ============================================================
# AI高频词自动替换建议（--auto-fix）
# ============================================================

# 替换策略：按词给出具体的行为描写替代方案
AUTO_FIX_STRATEGIES = {
    '不禁': [
        '直接写动作结果（如：手已经握成了拳头 / 嘴角往上翘了一下）',
        '写身体反应的前兆（如：喉咙一紧 / 心跳漏了半拍）',
    ],
    '缓缓': [
        '写出具体速度感（如：一步一步地 / 用了好几秒才）',
        '写出阻力或犹豫（如：像在水里移动一样 / 每动一下都费好大劲）',
    ],
    '淡淡': [
        '写出具体的表情细节（如：眼皮都没抬 / 嘴角 barely 弯了弯）',
        '写出语气特征（如：像在说今天天气不错 / 语气平得像白开水）',
    ],
    '微微': [
        '写出可观测的微小变化（如：眉头皱了一下又松开 / 手指蜷了蜷）',
        '写出对比感（如：变化小到不仔细看根本发现不了）',
    ],
    '竟然': [
        '用角色的心理活动替代（如：他没想到 / 这不在计划里）',
        '用反差描写（如：跟预想的完全不同 / 结果恰恰相反）',
    ],
    '居然': [
        '写出意外感的来源（如：这不在预料之中 / 完全出乎意料）',
        '写出对比（如：明明应该A，结果B了）',
    ],
    '悄然': [
        '写出无声的具体方式（如：没发出一点声音 / 连脚步声都被地毯吞了）',
        '写出不被注意的状态（如：谁也没注意到他 / 像空气一样）',
    ],
    '默然': [
        '写出沉默的方式和时长（如：好几秒没说话 / 嘴唇动了动但没出声）',
        '写出沉默时的动作（如：低着头盯地板 / 把杯子转了一圈又一圈）',
    ],
    '不由得': [
        '写出本能反应（如：身体比脑子先动了 / 还没来得及想，手已经）',
        '写出条件反射（如：像被弹簧弹了一下 / 下意识就是那个动作）',
    ],
    '下意识': [
        '写出习惯来源（如：多年的老毛病又犯了 / 训练留下的肌肉记忆）',
        '写出动作的自动化（如：手自己就伸了出去 / 话脱口而出）',
    ],
    '情不自禁': [
        '写出情感累积到爆点的过程（如：忍了半天没忍住 / 眼眶一直撑着，终于没撑住）',
        '写出具体表现（如：声音发抖 / 手在抖）',
    ],
    '深深地': [
        '写出具体程度和时长（如：好一会儿才 / 持续了好几秒）',
        '写出身体细节（如：吸气吸到肺有点疼 / 看到眼睛发酸）',
    ],
    '轻轻': [
        '写出力度感（如：几乎没用力 / 像碰瓷器一样小心）',
        '写出声音大小（如：声音小到只有自己能听见 / 像蚊子嗡嗡）',
    ],
    '默默': [
        '写出无声行为的具体方式（如：没说话，只是 / 一声不吭地）',
        '写出伴随的小动作（如：嘴唇抿成一条线 / 垂着眼不看任何人）',
    ],
    '一抹': [
        '写出具体的表情变化（如：嘴角往上提了一点 / 眉心舒展了些）',
        '写出情绪的来源（如：因为什么而露出的）',
    ],
    '一丝': [
        '写出具体表现（如：极细微的 / 几乎看不出来的）',
        '写出在场者的感知（如：只有他自己能感觉到）',
    ],
    '一阵': [
        '写出持续时间和节奏（如：连续好几秒 / 一波一波地）',
        '写出具体感受（如：像触电一样 / 从XX蔓延到XX）',
    ],
    '宛如': [
        '写出更接地气的比喻（如：看着就像 / 活脱脱是）',
        '直接描述特征，不用比喻',
    ],
    '仿佛': [
        '减少使用频率，只在关键描写处用',
        '用更具体的感官描写替代（如：看起来 / 听起来 / 感觉上）',
    ],
    '犹如': [
        '写出更具体的对比（如：跟XX一样 / 像极了）',
        '直接写本体特征，跳过喻体',
    ],
}

def _extract_sentence(content, pos, word, window=80):
    """从content的pos位置提取包含word的完整句子"""
    # 向前找句号/换行
    start = pos
    while start > 0 and content[start-1] not in '。！？\n':
        start -= 1
        if pos - start > window * 2:
            break
    # 向后找句号/换行
    end = pos + len(word)
    while end < len(content) and content[end] not in '。！？\n':
        end += 1
        if end - pos > window * 2:
            break
    if end < len(content) and content[end] in '。！？':
        end += 1
    return content[start:end].strip()

def _make_diff_entry(file_path, original, replaced, word, reason, confidence):
    """生成单条 diff 记录"""
    return {
        'file': file_path,
        'word': word,
        'original': original,
        'replaced': replaced,
        'reason': reason,
        'confidence': confidence,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

def _write_diff_file(diff_entries, output_dir):
    """将替换记录写入 .diff 文件"""
    diff_path = os.path.join(output_dir, 'auto_fix_diff.txt')
    lines = [
        f'# Auto-Fix Diff Report - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}',
        f'# 共 {len(diff_entries)} 条替换记录',
        '',
    ]
    for i, entry in enumerate(diff_entries, 1):
        lines.append(f'--- [{i}] {os.path.basename(entry["file"])} ---')
        lines.append(f'词: {entry["word"]}')
        lines.append(f'原句: {entry["original"]}')
        lines.append(f'新句: {entry["replaced"]}')
        lines.append(f'原因: {entry["reason"]}')
        lines.append(f'置信度: {entry["confidence"]}')
        lines.append('')
    with open(diff_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return diff_path

def apply_auto_fix(chapters: List[Tuple[int, str, str]], output_dir: str, dry_run: bool = True) -> int:
    """
    执行AI高频词自动替换（批量模式）。

    dry_run=True: 只生成diff，不修改正文
    dry_run=False: 备份原文后执行替换

    返回: diff_entries 列表
    """
    diff_entries = []
    file_changes = defaultdict(list)  # file_path -> [(word, original_sentence, new_sentence, reason, confidence)]

    for num, path, fname in chapters:
        content = read_file(path)
        if not content:
            continue

        for word, threshold in AI_WORDS.items():
            count = content.count(word)
            if count <= threshold:
                continue

            strategies = AUTO_FIX_STRATEGIES.get(word, ['用具体行为描写替代'])
            reason = f'AI高频词「{word}」出现{count}次（阈值{threshold}），建议替换策略：{strategies[0]}'

            # 找所有超阈值的出现位置
            start = 0
            occurrence = 0
            while True:
                idx = content.find(word, start)
                if idx == -1:
                    break
                occurrence += 1
                if occurrence > threshold:
                    sentence = _extract_sentence(content, idx, word)
                    if sentence and len(sentence) > 5:
                        # 标记待替换：用「REPLACE_MARK」包裹，供人工确认
                        confidence = 'medium'
                        if count > threshold * 2:
                            confidence = 'high'
                        elif count <= threshold + 1:
                            confidence = 'low'

                        new_sentence = sentence.replace(word, f'「{word}」⟵待替换')
                        diff_entries.append(_make_diff_entry(path, sentence, new_sentence, word, reason, confidence))
                        file_changes[path].append((word, sentence, new_sentence, reason, confidence))
                start = idx + len(word)

    if not diff_entries:
        print("\n✅ --auto-fix-apply: 未发现需要替换的内容")
        return []

    # 写 diff 文件
    diff_path = _write_diff_file(diff_entries, output_dir)
    print(f"\n🔧 --auto-fix-apply: 生成 {len(diff_entries)} 条替换记录")
    print(f"   📄 Diff 文件: {diff_path}")

    if dry_run:
        print(f"   ⚠️  干运行模式（未修改任何正文），使用 --auto-fix-apply 执行实际替换")
        return diff_entries

    # 实际替换模式：先备份再修改
    backed_up = set()
    for file_path, changes in file_changes.items():
        if file_path not in backed_up:
            bak_path = file_path + '.bak'
            if not os.path.exists(bak_path):
                shutil.copy2(file_path, bak_path)
                print(f"   📦 备份: {os.path.basename(file_path)} → {os.path.basename(bak_path)}")
            backed_up.add(file_path)

        content = read_file(file_path)
        # 注意：这里只标记不实际替换（保留人工确认环节）
        # 实际替换逻辑会在用户确认 diff 后执行
        print(f"   📝 {os.path.basename(file_path)}: {len(changes)} 处待替换（已标记，需确认diff后手动应用）")

    return diff_entries

def generate_auto_fix_suggestions(chapters, output_dir):
    """生成AI高频词的自动替换建议，输出到auto_fix_suggestions.md"""
    suggestions = []  # [{chapter, word, original, replacements}]

    for num, path, fname in chapters:
        content = read_file(path)
        for word, threshold in AI_WORDS.items():
            # 找所有出现位置
            start = 0
            count = 0
            while True:
                idx = content.find(word, start)
                if idx == -1:
                    break
                count += 1
                # 只对超阈值的词生成建议
                if count > threshold:
                    sentence = _extract_sentence(content, idx, word)
                    if sentence and len(sentence) > 5:
                        strategies = AUTO_FIX_STRATEGIES.get(word, ['用具体行为描写替代'])
                        suggestions.append({
                            'chapter': num,
                            'word': word,
                            'original': sentence,
                            'strategies': strategies,
                        })
                start = idx + len(word)

    if not suggestions:
        print("\n✅ --auto-fix: 未发现需要替换的AI高频词")
        return

    # 按章节+词分组
    by_chapter = defaultdict(list)
    for s in suggestions:
        by_chapter[s['chapter']].append(s)

    # 生成markdown
    lines = [
        '# AI高频词自动替换建议',
        '',
        f'> 生成时间：检查时自动生成',
        f'> 总计 {len(suggestions)} 条建议，请逐条确认后修改',
        f'> 原则：不是简单删词，而是用具体行为描写替代',
        '',
        '---',
        '',
    ]

    for ch in sorted(by_chapter.keys()):
        items = by_chapter[ch]
        lines.append(f'## 第{ch}章')
        lines.append('')

        # 按词分组
        by_word = defaultdict(list)
        for item in items:
            by_word[item['word']].append(item)

        for word, word_items in by_word.items():
            lines.append(f'### 「{word}」（{len(word_items)}处）')
            lines.append('')
            strategies = AUTO_FIX_STRATEGIES.get(word, ['用具体行为描写替代'])
            lines.append('**替换策略：**')
            for i, st in enumerate(strategies, 1):
                lines.append(f'{i}. {st}')
            lines.append('')
            lines.append('**待替换句子：**')
            lines.append('')
            for i, item in enumerate(word_items, 1):
                lines.append(f'{i}. 原句：`{item["original"]}`')
                lines.append(f'   → 建议：____（请根据上方策略填写具体替换）')
                lines.append('')

        lines.append('---')
        lines.append('')

    output_path = os.path.join(output_dir, 'auto_fix_suggestions.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"\n🔧 --auto-fix: 生成 {len(suggestions)} 条替换建议")
    print(f"   📄 已保存至: {output_path}")

    # 摘要输出
    word_counts = Counter(s['word'] for s in suggestions)
    print(f"\n   高频词分布：")
    for word, cnt in word_counts.most_common():
        strategies = AUTO_FIX_STRATEGIES.get(word, [])
        first_strategy = strategies[0] if strategies else '用具体行为描写替代'
        print(f"   • 「{word}」{cnt}处 — 建议：{first_strategy}")

# ============================================================
# 检查6: 章节字数
# ============================================================

def check_chapter_length(chapters: List[Tuple[int, str, str]], min_words: int = 1500, max_words: int = 4000) -> List[Dict[str, Any]]:
    issues = []
    for num, path, fname in chapters:
        content = read_file(path)
        # 统计中文字符数（排除标点和空格）
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        if chinese_chars < min_words:
            issues.append({
                'type': '字数不足',
                'severity': 'medium',
                'detail': f'第{num}章约{chinese_chars}字（建议{min_words}-{max_words}字）',
                'suggestion': '扩充场景细节或对话'
            })
        elif chinese_chars > max_words:
            issues.append({
                'type': '字数超标',
                'severity': 'low',
                'detail': f'第{num}章约{chinese_chars}字（建议{min_words}-{max_words}字）',
                'suggestion': '考虑拆分章节'
            })
    return issues

# ============================================================
# 统计: 字数统计报告
# ============================================================

def generate_word_count_stats(chapters: List[Tuple[int, str, str]]) -> Dict[str, Any]:
    """生成字数统计报告：总字数、平均字数、字数趋势"""
    if not chapters:
        return {'total': 0, 'average': 0, 'chapters': 0, 'trend': '无数据', 'details': []}
    
    details = []
    word_counts = []
    for num, path, fname in chapters:
        content = read_file(path)
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
        word_counts.append(chinese_chars)
        details.append({'chapter': num, 'words': chinese_chars, 'file': fname})
    
    total = sum(word_counts)
    average = total / len(word_counts) if word_counts else 0
    
    # 趋势分析：分三段比较
    trend = '稳定'
    if len(word_counts) >= 6:
        third = len(word_counts) // 3
        avg_first = sum(word_counts[:third]) / third
        avg_last = sum(word_counts[-third:]) / third
        if avg_last > avg_first * 1.15:
            trend = '字数递增（后期章节偏长）'
        elif avg_last < avg_first * 0.85:
            trend = '字数递减（后期章节偏短）'
    
    return {
        'total': total,
        'average': round(average),
        'min': min(word_counts) if word_counts else 0,
        'max': max(word_counts) if word_counts else 0,
        'chapters': len(word_counts),
        'trend': trend,
        'details': details,
    }

# ============================================================
# 检查7: 视角一致性
# ============================================================

def check_pov_consistency(chapters, pov_mode='third_person', pov_char=None):
    """
    检查视角是否一致
    pov_mode: 'third_person' (第三人称) / 'first_person' (第一人称)
    pov_char: 主角名字（如果是单一视角）
    """
    issues = []

    def is_in_quotes(text, char_pos):
        """检查text中char_pos位置的字符是否在引号内"""
        left_quotes = ['\u201c', '"', '\u300c']
        right_quotes = ['\u201d', '"', '\u300d']
        inside = False
        for idx, ch in enumerate(text):
            if ch in left_quotes:
                inside = True
            elif ch in right_quotes:
                inside = False
            elif idx == char_pos and inside:
                return True
        return False

    for num, path, fname in chapters:
        content = normalize_text(read_file(path))

        if pov_mode == 'third_person':
            lines = content.split('\n')
            chapter_has_issue = False
            for i, line in enumerate(lines):
                if chapter_has_issue:
                    break
                stripped = line.strip()
                if not stripped:
                    continue

                # 跳过对话行（以引号开头）
                if stripped[0] in '"\u201c\u300c':
                    continue
                # 跳过弹幕/消息行
                if stripped[0] in '\u3010\uff08\uff3b' or '\u3010' in stripped or '\u3011' in stripped:
                    continue
                # 跳过加粗标记行
                if '**' in stripped:
                    continue
                # 跳过消息格式行（"赵恒："开头的短行）
                if re.match(r'^[\u4e00-\u9fff]{1,5}[：:]', stripped):
                    continue
                # 跳过标题行
                if stripped.startswith('#'):
                    continue

                # 找到所有"我"的位置
                for m in re.finditer(r'(?<![他她它别自])我(?!的|不|是|也|就|只|还|没|有|这|那|一|们)', stripped):
                    char_pos = m.start()
                    # 如果"我"在引号内，跳过
                    if is_in_quotes(stripped, char_pos):
                        continue

                    # 跳过自由间接引语：短句含"我"的是内心独白
                    # 如"我看错了吗？""我在。""我看到了。"
                    # 也跳过带破折号的："有人在说——我在。"
                    def _is_inner_monologue(line):
                        # 按破折号/省略号分割，检查每个片段
                        segments = re.split(r'(?:——|……)', line)
                        for seg in segments:
                            seg_clean = seg.strip().rstrip('。！？')
                            if len(seg_clean) <= 12 and re.match(r'^[我你他她它]', seg_clean):
                                return True
                        return False

                    if _is_inner_monologue(stripped):
                        continue

                    # 检查是否是重复引用
                    short_phrase = stripped[:char_pos+5].replace('。', '').replace('！', '').replace('？', '')
                    is_repeat = False
                    for pi in range(max(0, i-5), i):
                        prev_line = lines[pi].strip()
                        if short_phrase in prev_line and ('\u3010' in prev_line or '"' in prev_line or '\u201c' in prev_line or '：' in prev_line):
                            is_repeat = True
                            break
                    if is_repeat:
                        continue

                    # 确认为视角问题
                    issues.append({
                        'type': '视角混乱',
                        'severity': 'medium',
                        'detail': f'第{num}章非对话中出现"我"："{stripped[:50]}..."',
                        'suggestion': f'应为第三人称"{pov_char or "主角名"}"'
                    })
                    chapter_has_issue = True
                    break

    return issues

# ============================================================
# 检查8: 角色状态机冲突
# ============================================================

def check_character_state_conflicts(chapters, tracking_dir):
    """
    检查角色状态机与正文是否冲突
    需要 character_states.json
    """
    issues = []
    states = load_character_states(tracking_dir)
    if not states:
        return issues

    for char_name, char_data in states.items():
        if 'snapshots' not in char_data:
            continue

        snapshots = char_data['snapshots']
        # 兼容列表格式 [{chapter:1,...}] 和字典格式 {"1":{...}}
        if isinstance(snapshots, list):
            snap_map = {str(s['chapter']): s for s in snapshots if 'chapter' in s}
        else:
            snap_map = snapshots
        sorted_chapters = sorted(snap_map.keys(), key=lambda x: int(x))

        for i, ch in enumerate(sorted_chapters):
            snapshot = snap_map[ch]
            # 检查位置是否突然变化（没有移动过程）
            if i > 0:
                prev_ch = sorted_chapters[i-1]
                prev_snapshot = snap_map[prev_ch]

                prev_loc = prev_snapshot.get('location', '')
                curr_loc = snapshot.get('location', '')

                if prev_loc and curr_loc and prev_loc != curr_loc:
                    # 检查中间章节是否有移动描述
                    ch_num = int(ch)
                    prev_ch_num = int(prev_ch)
                    if ch_num - prev_ch_num == 1:
                        # 相邻章节，检查正文中是否有位置转移描述
                        content = read_file(chapters[ch_num-1][1]) if ch_num <= len(chapters) else ""
                        if content and prev_loc in content and curr_loc not in content:
                            # 上一章还在旧位置，这一章突然在新位置，没有移动描述
                            pass  # 这个检查需要更精细的NLP，暂时跳过

            # 检查知识状态：角色不应该知道未来信息
            knowledge = snapshot.get('knows', [])
            if isinstance(knowledge, list):
                for info in knowledge:
                    # 检查这个信息在第N章之前是否被合理获得
                    pass  # 需要事件时间线比对

    return issues

# ============================================================
# 检查9: 重复段落检测
# ============================================================

def check_repetition(chapters, min_length=50, similarity_threshold=0.80):
    """检测跨章节的重复段落（含无章节号草稿文件）"""
    issues = []

    # 提取每章的句子（用集合去重加速）
    chapter_sentences = {}
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        sentences = [s.strip() for s in re.split(r'[。！？\n]', content) if len(s.strip()) >= min_length]
        chapter_sentences[num] = sentences

    ch_nums = sorted(chapter_sentences.keys())

    # 预计算每句的字符集合
    ch_sets = {}
    for cn in ch_nums:
        ch_sets[cn] = [(s, set(s)) for s in chapter_sentences[cn]]

    # 比对所有章节对（包括草稿vs正式章）
    found_pairs = set()  # 避免重复报告
    for i in range(len(ch_nums)):
        for j in range(i+1, len(ch_nums)):
            ch_a, ch_b = ch_nums[i], ch_nums[j]
            # 跳过同一作者的重复章节（前两章 vs 第1/2章）不需要跳过，正是要检测的
            for sa, sa_set in ch_sets[ch_a]:
                for sb, sb_set in ch_sets[ch_b]:
                    if not sa_set or not sb_set:
                        continue
                    common = len(sa_set & sb_set)
                    total = len(sa_set | sb_set)
                    if total == 0:
                        continue
                    similarity = common / total
                    if similarity > similarity_threshold:
                        # 去重
                        pair_key = (min(ch_a, ch_b), max(ch_a, ch_b), sa[:30], sb[:30])
                        if pair_key in found_pairs:
                            continue
                        found_pairs.add(pair_key)
                        ch_label = lambda c: f'第{c}章' if c > 0 else f'草稿文件'
                        issues.append({
                            'type': '重复段落',
                            'severity': 'medium' if ch_a > 0 and ch_b > 0 else 'high',
                            'detail': f'{ch_label(ch_a)}和{ch_label(ch_b)}有高度相似段落（相似度{similarity:.0%}）',
                            'suggestion': f'"{sa[:60]}..." / "{sb[:60]}..."'
                        })
            # 性能保护：如果两章相似段太多，只报前5个
            pair_count = sum(1 for iss in issues if iss['type'] == '重复段落' and
                           (ch_label(ch_a) in iss['detail'] and ch_label(ch_b) in iss['detail']))

    # 去重：每对章节最多报5个重复段落
    pair_issues = defaultdict(list)
    for iss in issues:
        pair_issues[iss['detail']].append(iss)
    issues = []
    seen_chapter_pairs = defaultdict(int)
    for iss_list in pair_issues.values():
        iss = iss_list[0]
        issues.append(iss)

    # 限制总数
    if len(issues) > 20:
        # 按严重程度排序，保留high + 最多15个medium
        high = [i for i in issues if i['severity'] == 'high']
        medium = [i for i in issues if i['severity'] == 'medium'][:15]
        issues = high + medium
        issues.append({
            'type': '重复段落',
            'severity': 'low',
            'detail': f'... 还有更多重复段落，已省略（共找到超过20处）',
            'suggestion': '建议清理草稿文件或使用diff工具详细比对'
        })

    return issues

# ============================================================
# 检查11: 角色出场追踪
# =============================================================

def check_character_appearance(chapters, character_states_data=None, absent_threshold=5, frequent_threshold=3):
    """
    追踪角色出场情况，检测：
    1. 角色连续N章未出现（可能被遗忘）
    2. 频繁出场的角色突然消失
    """
    issues = []
    if not character_states_data:
        return issues

    # 1. 从 character_states.json 提取所有角色名
    char_names = list(character_states_data.keys())
    # 收集别名
    char_aliases = {}  # alias -> main_name
    for name, data in character_states_data.items():
        aliases = data.get('aliases', [])
        for a in aliases:
            char_aliases[a] = name
    # 所有可匹配的名字（主名+别名）
    all_names = set(char_names)
    all_names.update(char_aliases.keys())

    # 2. 扫描每章，提取出场角色
    chapter_num_list = [num for num, _, _ in chapters if num > 0]
    if not chapter_num_list:
        return issues

    chapter_appearances = {}  # num -> set of main_names
    for num, path, fname in chapters:
        if num <= 0:
            continue
        content = read_file(path)
        appeared = set()
        for name in all_names:
            if name in content:
                # 映射到主名
                main_name = char_aliases.get(name, name)
                appeared.add(main_name)
        chapter_appearances[num] = appeared

    # 3. 检测连续N章未出现的角色
    for char_name in char_names:
        absent_streak = 0
        absent_start = None
        appeared_before = False
        for num in chapter_num_list:
            appeared = char_name in chapter_appearances.get(num, set())
            if appeared:
                appeared_before = True
                if absent_streak >= absent_threshold:
                    issues.append({
                        'type': '角色消失',
                        'severity': 'medium',
                        'detail': f'角色「{char_name}」在第{absent_start}-{num-1}章连续{absent_streak}章未出现（之前有出场）',
                        'suggestion': f'检查是否遗漏了「{char_name}」的戏份，或需要交代其去向'
                    })
                absent_streak = 0
                absent_start = None
            else:
                if appeared_before:
                    if absent_streak == 0:
                        absent_start = num
                    absent_streak += 1
        # 尾部处理
        if absent_streak >= absent_threshold and appeared_before:
            issues.append({
                'type': '角色消失',
                'severity': 'medium',
                'detail': f'角色「{char_name}」在第{absent_start}-{chapter_num_list[-1]}章连续{absent_streak}章未出现（之前有出场）',
                'suggestion': f'检查是否遗漏了「{char_name}」的戏份，或需要交代其去向'
            })

    # 4. 检测频繁出场后突然消失
    for char_name in char_names:
        # 统计出场频率
        appearances = [num for num in chapter_num_list if char_name in chapter_appearances.get(num, set())]
        if len(appearances) < frequent_threshold:
            continue

        # 检查最近是否有消失
        last_appear = max(appearances)
        last_chapter = chapter_num_list[-1]
        gap = last_chapter - last_appear

        if gap >= absent_threshold:
            # 计算该角色在前半段的出场密度
            mid_point = chapter_num_list[len(chapter_num_list)//2]
            first_half_count = sum(1 for a in appearances if a <= mid_point)
            first_half_total = sum(1 for n in chapter_num_list if n <= mid_point)
            density = first_half_count / first_half_total if first_half_total > 0 else 0

            if density >= 0.3:  # 前30%以上的章节都有出场
                issues.append({
                    'type': '角色突然消失',
                    'severity': 'high',
                    'detail': f'角色「{char_name}」前期出场频繁（前半段{density:.0%}章节出场），但最近{gap}章未出现（最后一次：第{last_appear}章）',
                    'suggestion': f'重要角色「{char_name}」不应长期缺席，建议在近期章节中安排出场或交代去向'
                })

    # 5. 输出每章出场摘要（信息性，不报issue）
    return issues


# ============================================================
# 检查10: 章节节奏检测
# ============================================================

# 钩子词：标志悬念/转折/意外
HOOK_WORDS = ['突然', '愣住', '变了', '不可能', '等等', '不会吧', '竟然', '居然', '怎么回事', '怎么回事', '怎么可能',
              '死', '杀', '塌了', '炸了', '碎了', '断', '裂', '崩', '倒吸', '瞳孔', '瞳仁', '血液凝固', '脊背发凉',
              '毛骨悚然', '不寒而栗', '轰', '砰', '嘎吱', '咔嚓']

# 情感转折词：标志情绪变化
EMOTION_TURN_WORDS = ['但是', '然而', '可是', '不过', '却', '反而', '没想到', '出乎意料', '意料之外',
                      '后悔', '愧疚', '心酸', '心碎', '红了眼眶', '泪水', '哭', '笑了', '笑了笑',
                      '沉默', '良久', '叹息', '苦笑', '释然', '松了口气']


def check_pacing(chapters, low_word_threshold=1200, consecutive_hook_gap=3, consecutive_emotion_gap=5, consecutive_low_word_gap=3):
    """
    检测章节节奏问题：
    1. 连续N章没有钩子词（太平）
    2. 连续N章没有情感转折（太干）
    3. 连续N章字数偏低（水章）
    4. 章节间节奏单调（结构相似度检测）
    """
    issues = []
    if len(chapters) < 3:
        return issues

    # 预处理：每章的钩子数、情感转折数、字数
    chapter_stats = []
    for num, path, fname in chapters:
        content = normalize_text(read_file(path))
        chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))

        hook_count = sum(content.count(w) for w in HOOK_WORDS)
        emotion_count = sum(content.count(w) for w in EMOTION_TURN_WORDS)

        # 结构特征：对话比例、短句比例、段落平均长度
        lines = [l.strip() for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
        if not lines:
            chapter_stats.append({'num': num, 'chars': chinese_chars, 'hooks': hook_count,
                                   'emotions': emotion_count, 'dialog_ratio': 0, 'short_ratio': 0, 'para_avg': 0})
            continue

        dialog_lines = sum(1 for l in lines if l[0] in '"\u201c\u300c' or '\u201c' in l or '\u300c' in l)
        short_lines = sum(1 for l in lines if len(l) <= 15)
        total_chars_in_lines = sum(len(l) for l in lines)
        para_avg = total_chars_in_lines / len(lines) if lines else 0

        chapter_stats.append({
            'num': num, 'chars': chinese_chars, 'hooks': hook_count,
            'emotions': emotion_count, 'dialog_ratio': dialog_lines / len(lines),
            'short_ratio': short_lines / len(lines), 'para_avg': para_avg
        })

    # 1. 连续N章没有钩子词
    streak = 0
    streak_start = None
    for i, st in enumerate(chapter_stats):
        if st['hooks'] == 0:
            if streak == 0:
                streak_start = st['num']
            streak += 1
        else:
            if streak >= consecutive_hook_gap:
                issues.append({
                    'type': '节奏太平',
                    'severity': 'medium',
                    'detail': f'第{streak_start}-{st["num"]-1 if st["num"] > 0 else chapter_stats[i-1]["num"]}章连续{streak}章缺少钩子/悬念词，读者可能感到平淡',
                    'suggestion': '在平淡段落中插入悬念钩子：意外事件、角色反常、信息揭露、倒计时紧迫感'
                })
            streak = 0
            streak_start = None
    # 尾部处理
    if streak >= consecutive_hook_gap:
        last_num = chapter_stats[-1]['num']
        issues.append({
            'type': '节奏太平',
            'severity': 'medium',
            'detail': f'第{streak_start}-{last_num}章连续{streak}章缺少钩子/悬念词',
            'suggestion': '在平淡段落中插入悬念钩子：意外事件、角色反常、信息揭露、倒计时紧迫感'
        })

    # 2. 连续N章没有情感转折
    streak = 0
    streak_start = None
    for i, st in enumerate(chapter_stats):
        if st['emotions'] == 0:
            if streak == 0:
                streak_start = st['num']
            streak += 1
        else:
            if streak >= consecutive_emotion_gap:
                issues.append({
                    'type': '情感单调',
                    'severity': 'low',
                    'detail': f'第{streak_start}-{chapter_stats[i-1]["num"]}章连续{streak}章缺少情感转折词',
                    'suggestion': '增加角色内心的情感起伏：回忆、愧疚、感动、释然等'
                })
            streak = 0
            streak_start = None
    if streak >= consecutive_emotion_gap:
        last_num = chapter_stats[-1]['num']
        issues.append({
            'type': '情感单调',
            'severity': 'low',
            'detail': f'第{streak_start}-{last_num}章连续{streak}章缺少情感转折词',
            'suggestion': '增加角色内心的情感起伏'
        })

    # 3. 连续N章字数偏低
    avg_chars = sum(s['chars'] for s in chapter_stats) / len(chapter_stats)
    if avg_chars > 0:
        dynamic_low = max(low_word_threshold, avg_chars * 0.5)
    else:
        dynamic_low = low_word_threshold

    streak = 0
    streak_start = None
    for i, st in enumerate(chapter_stats):
        if st['chars'] < dynamic_low and st['chars'] > 0:
            if streak == 0:
                streak_start = st['num']
            streak += 1
        else:
            if streak >= consecutive_low_word_gap:
                issues.append({
                    'type': '疑似水章',
                    'severity': 'low',
                    'detail': f'第{streak_start}-{chapter_stats[i-1]["num"]}章连续{streak}章字数偏低（<{dynamic_low:.0f}字，全书均{avg_chars:.0f}字）',
                    'suggestion': '检查是否为过渡章/水章，考虑合并或补充内容'
                })
            streak = 0
            streak_start = None
    if streak >= consecutive_low_word_gap:
        last_num = chapter_stats[-1]['num']
        issues.append({
            'type': '疑似水章',
            'severity': 'low',
            'detail': f'第{streak_start}-{last_num}章连续{streak}章字数偏低',
            'suggestion': '检查是否为过渡章/水章，考虑合并或补充内容'
        })

    # 4. 章节间节奏单调检测：连续章节结构相似（对话比例、短句比例、段落长度都接近）
    if len(chapter_stats) >= 5:
        monotone_streak = 1
        monotone_start = 0
        for i in range(1, len(chapter_stats)):
            prev, curr = chapter_stats[i-1], chapter_stats[i]
            # 结构相似判定：三个维度差异都很小
            dialog_diff = abs(prev['dialog_ratio'] - curr['dialog_ratio'])
            short_diff = abs(prev['short_ratio'] - curr['short_ratio'])
            para_diff = abs(prev['para_avg'] - curr['para_avg']) / max(prev['para_avg'], 1)

            if dialog_diff < 0.1 and short_diff < 0.1 and para_diff < 0.2:
                monotone_streak += 1
            else:
                if monotone_streak >= 5:
                    start_num = chapter_stats[monotone_start]['num']
                    end_num = chapter_stats[i-1]['num']
                    issues.append({
                        'type': '节奏单调',
                        'severity': 'low',
                        'detail': f'第{start_num}-{end_num}章连续{monotone_streak}章结构相似（对话比例、句式长度接近），阅读体验可能重复',
                        'suggestion': '变换节奏：插入大段独白/减少对话/加动作场景/切换场景'
                    })
                monotone_streak = 1
                monotone_start = i
        if monotone_streak >= 5:
            start_num = chapter_stats[monotone_start]['num']
            end_num = chapter_stats[-1]['num']
            issues.append({
                'type': '节奏单调',
                'severity': 'low',
                'detail': f'第{start_num}-{end_num}章连续{monotone_streak}章结构相似',
                'suggestion': '变换节奏：插入大段独白/减少对话/加动作场景/切换场景'
            })

    return issues


# ============================================================
# 检查12: 对话质量检查
# ============================================================

# 书面腔词汇（在对话中出现显得不自然）
FORMAL_WORDS_IN_DIALOGUE = ['因此', '然而', '所以', '不过', '不过话又说回来', '总而言之',
                          '综上所述', '换言之', '由此可见', '毋庸置疑', '毋庸置疑地']

# 语气词（让对话更口语化）
MODAL_PARTICLES = ['啊', '吧', '呢', '嘛', '哦', '哈', '呀', '哇', '哎', '唉',
                  '嗯', '噢', '喔', '嘞', '呗', '咧', '喽', '诶']


def _extract_dialogues(content):
    """从正文中提取对话句子列表，返回 [(对话文本, 是否有引号包裹)]"""
    dialogues = []
    # 匹配中文引号包裹的对话
    # 支持多行对话（同一引号对内）
    for m in re.finditer(r'[\u201c\u300c]([\s\S]*?)[\u201d\u300d]', content):
        text = m.group(1).strip()
        if text:
            dialogues.append(text)
    return dialogues


def check_dialogue_quality(chapters, long_dialogue_threshold=50, formal_count_threshold=3,
                           pure_dialogue_gap=8):
    """
    检查对话质量：
    1. 对话句过长（超过阈值的对话不自然）
    2. 对话中频繁使用书面词
    3. 对话缺乏语气词
    4. 对话缺乏打断和重叠
    5. 连续多行纯对话无动作描写
    """
    issues = []

    for num, path, fname in chapters:
        if num <= 0:
            continue
        content = normalize_text(read_file(path))
        if not content:
            continue

        dialogues = _extract_dialogues(content)
        if not dialogues:
            continue

        # --- 1. 过长对话 ---
        long_ones = []
        for d in dialogues:
            # 去掉对话内部的标点来算字数
            d_clean = re.sub(r'[^\u4e00-\u9fffa-zA-Z0-9]', '', d)
            if len(d_clean) > long_dialogue_threshold:
                long_ones.append(d)
        if len(long_ones) >= 3:
            issues.append({
                'type': '对话过长',
                'severity': 'low',
                'detail': f'第{num}章有{len(long_ones)}句对话超过{long_dialogue_threshold}字，真人很少一口气说这么多',
                'suggestion': '拆成多句，加动作描写打断，或让对方插嘴'
            })

        # --- 2. 书面词过多 ---
        formal_hits = 0
        for d in dialogues:
            for fw in FORMAL_WORDS_IN_DIALOGUE:
                if fw in d:
                    formal_hits += 1
        if formal_hits >= formal_count_threshold:
            issues.append({
                'type': '对话书面腔',
                'severity': 'low',
                'detail': f'第{num}章对话中出现{formal_hits}次书面词（因此/然而/所以等），口语感弱',
                'suggestion': '替换成口语：所以→那/这么说；然而→但是/可；因此→那/所以说'
            })

        # --- 3. 语气词匮乏 ---
        has_modal = 0
        for d in dialogues:
            for mp in MODAL_PARTICLES:
                if mp in d:
                    has_modal += 1
                    break  # 每句只计一次
        modal_ratio = has_modal / len(dialogues) if dialogues else 0
        if len(dialogues) >= 5 and modal_ratio < 0.15:
            issues.append({
                'type': '对话缺语气词',
                'severity': 'low',
                'detail': f'第{num}章{len(dialogues)}句对话中仅{has_modal}句含语气词（{modal_ratio:.0%}），口语感不足',
                'suggestion': '在句尾加语气词：啊/吧/呢/嘛/哦，让对话更自然'
            })

        # --- 4. 缺乏打断/重叠 ---
        # 检测对话中是否有省略号（被打断）或破折号（话被截断）
        interrupt_count = 0
        for d in dialogues:
            if '……' in d or '——' in d or '…' in d:
                interrupt_count += 1
        # 不是每章都需要打断，但如果对话很多且完全没有打断迹象
        if len(dialogues) >= 10 and interrupt_count == 0:
            issues.append({
                'type': '对话缺打断',
                'severity': 'low',
                'detail': f'第{num}章{len(dialogues)}句对话中没有任何打断/重叠（缺少……或——），像轮番演讲',
                'suggestion': '让角色被打断：用省略号截断、破折号接别人的话、插话抢答'
            })

        # --- 5. 连续纯对话无动作描写 ---
        # 按行扫描，检测连续对话行（引号开头或内容全是对话）
        lines = content.split('\n')
        pure_dialogue_streak = 0
        max_streak = 0
        max_streak_start = 0
        current_streak_start = 0
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue
            # 判断是否为纯对话行（以引号开头，或以角色名+冒号+引号开头）
            is_dialogue_line = bool(re.match(r'^[\u4e00-\u9fff]{0,4}[：:”\u201c"\u300c]', stripped))
            if is_dialogue_line:
                if pure_dialogue_streak == 0:
                    current_streak_start = i
                pure_dialogue_streak += 1
            else:
                if pure_dialogue_streak > max_streak:
                    max_streak = pure_dialogue_streak
                    max_streak_start = current_streak_start
                pure_dialogue_streak = 0
        # 尾部
        if pure_dialogue_streak > max_streak:
            max_streak = pure_dialogue_streak

        if max_streak >= pure_dialogue_gap:
            issues.append({
                'type': '纯对话堆砌',
                'severity': 'medium',
                'detail': f'第{num}章有连续{max_streak}行纯对话无动作/心理描写，像剧本不像小说',
                'suggestion': '每3-5句对话插入动作、表情、心理活动，让场景立体起来'
            })

    return issues


# ============================================================
# 主流程
# ============================================================

def check_outline_drift(chapters: List[Tuple[int, str, str]], outline_path: str, chapter_list_path: str = '') -> List[Dict[str, Any]]:
    """大纲偏差检测：对比正文与大纲，检测剧情整体偏移。

    需要 outline_drift.py 在同目录下。

    Args:
        chapters: 正文章节列表 [(num, path, fname), ...]
        outline_path: 大纲文件路径
        chapter_list_path: 章节列表文件路径（可选）

    Returns:
        偏差问题列表
    """
    issues = []

    # 延迟导入 outline_drift
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)
        import outline_drift as od
    except ImportError:
        print("  [警告] outline_drift.py 未找到，跳过大纲偏差检测")
        return issues

    if not outline_path or not os.path.isfile(outline_path):
        return issues

    # 解析大纲
    volumes = []
    if chapter_list_path and os.path.isfile(chapter_list_path):
        try:
            volumes = od.parse_chapter_list(chapter_list_path)
        except Exception:
            pass

    outline_data = od.parse_outline_keywords(outline_path)

    if not volumes:
        for vol in outline_data:
            volumes.append({
                "vol": vol["vol"],
                "vol_title": f'第{vol["vol"]}卷',
                "chapters": vol["chapters"]
            })

    # 展平大纲章节
    outline_flat = []
    for vol in volumes:
        for ch in vol.get("chapters", []):
            odata = None
            for ov in outline_data:
                for oc in ov.get("chapters", []):
                    if oc["num"] == ch["num"]:
                        odata = oc
                        break
            outline_flat.append({
                "num": ch["num"],
                "title": ch.get("title", ""),
                "keywords": odata.get("keywords", []) if odata else od.extract_keywords(ch.get("title", ""), 8),
                "characters": odata.get("characters", []) if odata else list(od.find_character_names(ch.get("title", "")))
            })

    if not outline_flat:
        return issues

    # 将 chapters 转换为 outline_drift 格式
    actual_chapters = []
    for num, path, fname in chapters:
        if num <= 0:
            continue
        content = read_file(path)
        actual_chapters.append({
            "num": num,
            "title": re.sub(r'^第\d+章\s*', '', fname).strip('_').strip(),
            "content": content,
            "filename": fname,
            "char_count": len(content)
        })

    if not actual_chapters:
        return issues

    # 执行各项检测
    title_results = od.check_title_match(outline_flat, actual_chapters)
    keyword_results = od.check_keyword_coverage(outline_flat, actual_chapters)
    character_results = od.check_character_presence(outline_flat, actual_chapters)
    trend, _ = od.calculate_drift_trend(title_results)

    # 计算每章偏差评分
    summary = od.generate_summary(title_results, keyword_results, character_results,
                                  od.check_progress_drift(volumes, actual_chapters)[0],
                                  actual_chapters, volumes)
    chapter_scores = summary.get("chapter_scores", {})

    # 1. 缺失章节
    for r in title_results:
        if r["status"] == "缺失":
            issues.append({
                'type': '大纲偏差·缺失章节',
                'severity': 'high',
                'detail': f'第{r["num"]}章《{r["outline_title"][:30]}》在大纲中但正文未写',
                'suggestion': '补充此章或在前后章节中覆盖其核心内容'
            })

    # 2. 新增章节（大纲外）
    for r in title_results:
        if r["status"] == "新增":
            issues.append({
                'type': '大纲偏差·新增章节',
                'severity': 'medium',
                'detail': f'第{r["num"]}章《{r["actual_title"][:30]}》不在大纲中',
                'suggestion': '决定：保留并更新大纲 / 合并到相邻章节 / 删除'
            })

    # 3. 标题严重偏差
    for r in title_results:
        if r["status"] == "偏差" and r["similarity"] < 0.15:
            issues.append({
                'type': '大纲偏差·剧情转向',
                'severity': 'high',
                'detail': f'第{r["num"]}章标题严重偏离大纲：大纲「{r["outline_title"][:20]}」→ 正文「{r["actual_title"][:20]}」（相似度{r["similarity"]:.2f}）',
                'suggestion': '检查此章是否需要回归大纲或同步更新大纲'
            })

    # 4. 关键词严重缺失
    for r in keyword_results:
        if r.get("status") == "偏离" and r.get("coverage", 1) < 0.2:
            issues.append({
                'type': '大纲偏差·关键词缺失',
                'severity': 'medium',
                'detail': f'第{r["num"]}章关键词覆盖率仅{r.get("coverage", 0):.0%}，缺失：{", ".join(r.get("missing", [])[:5])}',
                'suggestion': '检查是否遗漏了大纲中该章的核心事件'
            })

    # 5. 角色缺失
    for r in character_results:
        missing = r.get("missing", [])
        if missing and len(missing) >= 2:
            issues.append({
                'type': '大纲偏差·角色缺席',
                'severity': 'medium',
                'detail': f'第{r["num"]}章大纲要求的角色未出场：{", ".join(missing[:5])}',
                'suggestion': '确认这些角色是否应在本章出场，必要时安排出场或调整大纲'
            })

    # 6. 高偏差章节（评分>=50）
    high_drift = [(n, s) for n, s in chapter_scores.items() if s >= 50]
    for num, score in sorted(high_drift, key=lambda x: x[1], reverse=True)[:10]:
        issues.append({
            'type': '大纲偏差·整体偏移',
            'severity': 'high' if score >= 70 else 'medium',
            'detail': f'第{num}章偏差评分{score:.0f}/100，正文与大纲整体方向不一致',
            'suggestion': '重点检查此章：回归大纲或同步更新大纲'
        })

    # 7. 整体趋势警告
    if "偏离" in trend:
        issues.append({
            'type': '大纲偏差·趋势警告',
            'severity': 'high',
            'detail': f'最近章节整体趋于偏离大纲（趋势：{trend}），平均偏差{summary.get("avg_drift", 0):.1f}',
            'suggestion': '建议暂停写作，回顾大纲方向，确认后续走向'
        })

    # 8. 按卷偏差摘要（高偏差卷）
    for vs in summary.get("vol_summary", []):
        if vs.get("avg_drift") is not None and vs["avg_drift"] >= 40:
            issues.append({
                'type': '大纲偏差·卷级偏移',
                'severity': 'high' if vs["avg_drift"] >= 60 else 'medium',
                'detail': f'第{vs["vol"]}卷《{vs["vol_title"]}》平均偏差{vs["avg_drift"]:.0f}，最高偏差章：第{vs["max_drift_chapter"]}章（{vs["max_drift_score"]:.0f}分）',
                'suggestion': '该卷整体偏离大纲，建议逐章检查并调整'
            })

    return issues


def run_check(text_dir: str, tracking_file: str = '', dict_file: str = '', tracking_dir: str = '', skip_drafts: bool = False, ignore_patterns: Optional[List[str]] = None, auto_fix: bool = False, outline_path: str = '', chapter_list_path: str = '') -> List[Dict[str, Any]]:
    print("=" * 60)
    print("🔍 长篇小说一致性检查 v2")
    print("=" * 60)

    chapters = list_chapters(text_dir, include_unnumbered=True, skip_drafts=skip_drafts)
    if not chapters:
        print("[错误] 未找到章节文件")
        return []

    numbered = [c for c in chapters if c[0] > 0]
    unnumbered = [c for c in chapters if c[0] <= 0]
    print(f"\n📖 找到 {len(numbered)} 个章节" + (f" + {len(unnumbered)} 个草稿文件" if unnumbered else ""))
    if numbered:
        print(f"   第{numbered[0][0]}章 ~ 第{numbered[-1][0]}章")
    if unnumbered:
        for _, _, fname in unnumbered:
            print(f"   草稿: {fname}")

    tracking_content = read_file(tracking_file) if tracking_file else ""
    dict_content = read_file(dict_file) if dict_file else ""

    if not tracking_dir:
        tracking_dir = os.path.dirname(tracking_file) if tracking_file else text_dir

    all_issues = []

    print("\n⏳ 正在检查...")

    # 运行所有检查
    print("  → 角色称呼一致性...")
    all_issues.extend(check_name_consistency(chapters, dict_content))

    print("  → 设定冲突...")
    all_issues.extend(check_setting_conflicts(chapters, dict_content))

    print("  → 时间线...")
    all_issues.extend(check_timeline(chapters, tracking_content))

    # 提前加载角色名列表用于数值矛盾检查
    _numeric_char_names = None
    if tracking_dir:
        _cs_path = os.path.join(tracking_dir, 'character_states.json') if os.path.isdir(tracking_dir) else tracking_dir
        _cs_data = load_json(_cs_path)
        if _cs_data:
            _numeric_char_names = list(_cs_data.keys())
    if not _numeric_char_names:
        _cs_data2 = load_character_states(tracking_dir or text_dir)
        if _cs_data2:
            _numeric_char_names = list(_cs_data2.keys())

    print("  → 数值矛盾...")
    all_issues.extend(check_numeric_conflicts(chapters, character_names=_numeric_char_names, tracking_content=tracking_content))

    print("  → AI高频词...")
    all_issues.extend(check_ai_words(chapters))

    print("  → 章节字数...")
    all_issues.extend(check_chapter_length(chapters))

    # 字数统计报告
    word_stats = generate_word_count_stats(chapters)
    print(f"\n📊 字数统计：共{word_stats['chapters']}章，总{word_stats['total']}字，"
          f"平均{word_stats['average']}字/章，范围{word_stats['min']}-{word_stats['max']}字，"
          f"趋势：{word_stats['trend']}")

    print("  → 视角一致性...")
    all_issues.extend(check_pov_consistency(chapters))

    print("  → 角色状态机...")
    all_issues.extend(check_character_state_conflicts(chapters, tracking_dir))

    # 大纲偏差检测
    if outline_path:
        print("  → 大纲偏差...")
        all_issues.extend(check_outline_drift(chapters, outline_path, chapter_list_path))

    print("  → 重复段落...")
    all_issues.extend(check_repetition(chapters))

    print("  → 章节节奏...")
    all_issues.extend(check_pacing(chapters))

    print("  → 对话质量...")
    all_issues.extend(check_dialogue_quality(chapters))

    # 弹幕自称一致性
    print("  → 弹幕自称一致性...")
    all_issues.extend(check_danmaku_self_reference(chapters))

    # 加载角色状态数据用于出场追踪
    char_states_data = None
    # 优先用 --character-states 参数指定的文件
    if tracking_dir:
        cs_path = os.path.join(tracking_dir, 'character_states.json') if os.path.isdir(tracking_dir) else tracking_dir
        char_states_data = load_json(cs_path)
    if not char_states_data:
        char_states_data = load_character_states(tracking_dir or text_dir)
    if char_states_data:
        print("  → 角色出场追踪...")
        chars_data = char_states_data.get('characters', char_states_data) if isinstance(char_states_data, dict) and 'characters' in char_states_data else char_states_data
        all_issues.extend(check_character_appearance(chapters, chars_data))

    # 应用 ignore_patterns 过滤
    if ignore_patterns:
        before = len(all_issues)
        filtered = []
        for issue in all_issues:
            matched = False
            for pat in ignore_patterns:
                if re.search(pat, issue.get('detail', '')):
                    matched = True
                    break
            if not matched:
                filtered.append(issue)
        all_issues = filtered
        skipped = before - len(all_issues)
        if skipped > 0:
            print(f"  → 已过滤 {skipped} 个匹配忽略模式的问题")

    # 输出结果
    print(f"\n{'='*60}")
    print(f"📊 检查结果")
    print(f"{'='*60}")

    if not all_issues:
        print("\n✅ 未发现明显问题")
    else:
        by_severity = {'high': [], 'medium': [], 'low': []}
        for issue in all_issues:
            sev = issue.get('severity', 'medium')
            by_severity[sev].append(issue)

        total = len(all_issues)
        high_count = len(by_severity['high'])
        medium_count = len(by_severity['medium'])
        low_count = len(by_severity['low'])

        print(f"\n共发现 {total} 个问题：🔴 严重 {high_count} ｜ 🟡 中等 {medium_count} ｜ 🟢 轻微 {low_count}\n")

        # 按严重程度和类型输出
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
    report_dir = os.path.dirname(text_dir.rstrip('/'))
    output_path = os.path.join(report_dir, 'consistency_report.json')

    # --auto-fix / --auto-fix-apply 模式
    if auto_fix:
        print("\n⏳ 正在生成AI高频词替换建议...")
        generate_auto_fix_suggestions(chapters, report_dir)

    # --auto-fix-apply 在 main() 中处理
    return all_issues, chapters, report_dir
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_chapters': len(chapters),
            'total_issues': len(all_issues),
            'high': len([i for i in all_issues if i.get('severity') == 'high']),
            'medium': len([i for i in all_issues if i.get('severity') == 'medium']),
            'low': len([i for i in all_issues if i.get('severity') == 'low']),
            'issues': all_issues
        }, f, ensure_ascii=False, indent=2)
    print(f"\n📄 详细报告已保存至: {output_path}")

    return all_issues

# ============================================================
# 检查14: 弹幕角色自称一致性
# ============================================================

def check_danmaku_self_reference(chapters):
    """检查弹幕角色的自称方式是否一致
    适用于弹幕类小说（如《观众都是我的前世》）
    """
    issues = []
    char_self_refs = defaultdict(lambda: defaultdict(int))
    
    # 自称词表（排除容易误匹配的"臣"、"学生"等）
    SELF_REF_WORDS = ['朕', '吾', '老夫', '本座', '贫道', '洒家', '老子', '老娘', '哀家', '妾', '鄙人', '在下', '小人']
    
    for num, path, fname in chapters:
        if num <= 0:
            continue
        content = read_file(path)
        for m in re.finditer(r'【(?:弹幕：)?(\d+号[^：:—\]]+)[：:—](.*?)】', content, re.DOTALL):
            char_name = m.group(1).strip()
            text = m.group(2).strip()
            # 按句子分割
            sentences = re.split(r'[。！？；]', text)
            for sent in sentences:
                sent = sent.strip()
                if not sent:
                    continue
                # 检查自称词在句首或逗号后（主语位置）
                for ref in SELF_REF_WORDS:
                    if sent.startswith(ref):
                        char_self_refs[char_name][ref] += 1
                    elif f'，{ref}' in sent or f'、{ref}' in sent:
                        char_self_refs[char_name][ref] += 1
                # 检查"我"作为主语
                if sent.startswith('我') and not sent.startswith('我们'):
                    char_self_refs[char_name]['我'] += 1
    
    for char, refs in char_self_refs.items():
        if len(refs) >= 2:
            non_wo_refs = {k: v for k, v in refs.items() if k != '我'}
            if len(non_wo_refs) >= 2:
                ref_str = '、'.join([f'"{k}"({v}次)' for k, v in sorted(refs.items(), key=lambda x: -x[1])])
                issues.append({
                    'type': '弹幕自称不一致',
                    'severity': 'medium',
                    'detail': f'角色「{char}」使用了多种自称：{ref_str}',
                    'suggestion': f'统一「{char}」的自称方式，保持角色辨识度'
                })
    
    return issues

def main():
    parser = argparse.ArgumentParser(description='长篇小说一致性检查')
    parser.add_argument('text_dir', help='正文目录路径')
    parser.add_argument('--tracking', '-t', default='', help='追踪表文件路径')
    parser.add_argument('--dict', '-d', default='', help='设定词典文件路径')
    parser.add_argument('--tracking-dir', default='', help='追踪表目录（含character_states.json）')
    parser.add_argument('--character-states', default='', help='角色状态文件路径（character_states.json）')
    parser.add_argument('--output', '-o', default='', help='报告输出路径')
    parser.add_argument('--skip-drafts', action='store_true', help='跳过草稿文件（文件名含 草稿/draft/WIP）')
    parser.add_argument('--ignore-pattern', action='append', default=[], help='忽略匹配此正则模式的问题（可多次指定）')
    parser.add_argument('--auto-fix', action='store_true', help='对AI高频词生成具体替换建议，输出到auto_fix_suggestions.md')
    parser.add_argument('--auto-fix-apply', action='store_true', help='执行批量自动替换：生成diff文件、备份原文件(.bak)，标记待替换内容（需配合diff确认）')
    parser.add_argument('--outline', default='', help='大纲文件路径，启用大纲偏差检测')
    parser.add_argument('--chapter-list', default='', help='章节列表文件路径（配合--outline使用）')
    parser.add_argument('--version', action='version', version='consistency_check v2.1.0 (novel-writer skill)')
    args = parser.parse_args()
    tracking_dir = args.tracking_dir
    if args.character_states:
        tracking_dir = args.character_states
    result = run_check(args.text_dir, args.tracking, args.dict, tracking_dir, args.skip_drafts, args.ignore_pattern or None, getattr(args, 'auto_fix', False), args.outline, args.chapter_list)

    # --auto-fix-apply 模式
    if getattr(args, 'auto_fix_apply', False):
        if isinstance(result, tuple):
            _, chapters, report_dir = result
        else:
            chapters = []
            report_dir = os.path.dirname(args.text_dir.rstrip('/'))
        if chapters:
            print("\n⏳ 正在执行批量自动替换（干运行）...")
            apply_auto_fix(chapters, report_dir, dry_run=True)
            print("\n💡 确认 diff 文件后，可手动应用替换。脚本不会直接修改正文。")
        else:
            print("\n⚠️ 未找到章节文件，无法执行自动替换")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 consistency_check.py <正文目录> [--tracking 追踪表] [--dict 设定词典] [--tracking-dir 目录]")
        print("\n示例:")
        print("  python3 consistency_check.py 正文/ --tracking 追踪表.md --dict 设定词典.md")
        sys.exit(1)
    main()
