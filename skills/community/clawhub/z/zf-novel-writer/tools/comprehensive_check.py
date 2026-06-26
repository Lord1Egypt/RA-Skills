#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节综合质检脚本 v2.0
硬指标：字数3000-3500、检查项目全部通过、评分≥90
任何一项不达标 → 迭代优化（重试）
"""
import json
import re
import sys
from pathlib import Path


def count_words(text):
    """统计汉字和英文单词数量，不含标点"""
    # 移除章节标题和特殊标记
    lines = text.split('\n')
    content_lines = []
    for line in lines:
        line = line.strip()
        # 跳过标题行（如"第3章"）
        if line.startswith('#') or re.match(r'^第.*章', line):
            continue
        # 跳过特殊标记行
        if line.startswith('【') and line.endswith('】'):
            continue
        # 跳过空行
        if not line:
            continue
        content_lines.append(line)

    content = '\n'.join(content_lines)

    # 统计汉字
    chinese_chars = re.findall(r'[\u4e00-\u9fff]', content)
    chinese_count = len(chinese_chars)

    # 统计英文单词
    english_words = re.findall(r'\b[a-zA-Z]+\b', content)
    english_count = len(english_words)

    return chinese_count + english_count


def check_format(text):
    """检查格式要素（硬指标：必须全部通过）"""
    issues = []

    # 检查【变量更新】
    if '【变量更新】' not in text:
        issues.append("❌ 缺少【变量更新】部分")
    else:
        # 检查是否有必要的变量类别
        if '金融变量' not in text:
            issues.append("❌ 【变量更新】中缺少金融变量")
        if '人物变量' not in text:
            issues.append("❌ 【变量更新】中缺少人物变量")
        if '文明变量' not in text:
            issues.append("❌ 【变量更新】中缺少文明变量")

    # 检查【本章创建的铺垫】
    if '【本章创建的铺垫' not in text:
        issues.append("❌ 缺少【本章创建的铺垫】部分")

    # 检查【本章兑现的铺垫】
    if '【本章兑现的铺垫' not in text:
        issues.append("❌ 缺少【本章兑现的铺垫】部分")

    # 检查【人物弧线变化】
    if '【人物弧线变化】' not in text:
        issues.append("❌ 缺少【人物弧线变化】部分")

    return issues


def check_shen_jin_usage(text, chapter_num):
    """检查沈烬使用是否符合隐藏期规则"""
    issues = []
    
    # 隐藏期规则（第1-1000章）
    if chapter_num <= 1000:
        # 统计沈烬提及次数
        shen_jin_count = len(re.findall(r'沈烬', text))
        
        # 检查是否超过3次
        if shen_jin_count > 3:
            issues.append(f"❌ 沈烬提及次数过多：{shen_jin_count}次（隐藏期限制≤3次）")
        
        # 检查禁止词汇
        forbidden_words = ['序列', '宿主', '文明跃迁', '阿尔法序列']
        for word in forbidden_words:
            # 检查是否在沈烬相关上下文中出现
            pattern = rf'沈烬[^。！？]*{word}|{word}[^。！？]*沈烬'
            if re.search(pattern, text):
                issues.append(f"❌ 隐藏期禁止词汇：沈烬与「{word}」关联出现")
        
        # 检查沈烬视角/内心独白（沈烬作为段落开头或主语）
        shen_jin_pov_patterns = [
            r'沈烬站在',
            r'沈烬看着',
            r'沈烬想到',
            r'沈烬意识到',
            r'沈烬的嘴角',
            r'沈烬没有回答',
            r'沈烬打断',
            r'沈烬下达',
        ]
        
        for pattern in shen_jin_pov_patterns:
            matches = re.findall(pattern, text)
            if matches:
                issues.append(f"❌ 隐藏期禁止：沈烬视角/动作描写「{matches[0]}」")
        
        # 检查"仿佛看到沈烬"等视觉化描写
        visual_patterns = [
            r'仿佛看到[^。！？]*沈烬',
            r'仿佛看到了[^。！？]*沈烬',
            r'眼前浮现[^。！？]*沈烬',
            r'脑海中闪过[^。！？]*沈烬',
        ]
        
        for pattern in visual_patterns:
            if re.search(pattern, text):
                issues.append(f"❌ 隐藏期禁止：陈安视觉化看到沈烬「{re.search(pattern, text).group()}」")
    
    # 萌芽期规则（第1001-2000章）
    elif chapter_num <= 2000:
        # 检查是否直接揭露序列身份
        if re.search(r'沈烬[^。！？]*序列[^。！？]*宿主', text):
            issues.append("❌ 萌芽期不应直接揭露沈烬的序列宿主身份")
    
    return issues


def analyze_content(text):
    """分析内容质量"""
    suggestions = []

    # 检查对话比例
    dialogue_matches = re.findall(r'["」"「""](.*?)["」"\"""]', text, re.DOTALL)
    dialogue_chars = sum(len(m) for m in dialogue_matches)
    total_chars = len(text.replace('\n', '').replace(' ', ''))
    if total_chars > 0:
        dialogue_ratio = dialogue_chars / total_chars
        if dialogue_ratio < 0.2:
            suggestions.append("⚠️ 对话比例较低，建议增加人物互动")
        elif dialogue_ratio > 0.6:
            suggestions.append("⚠️ 对话比例过高，建议增加叙述描写")

    # 检查段落长度
    paragraphs = [p for p in text.split('\n\n') if p.strip() and not p.strip().startswith('【')]
    long_paragraphs = [p for p in paragraphs if len(p) > 500]
    if len(long_paragraphs) > 3:
        suggestions.append("⚠️ 存在较多长段落，建议适当分段提升可读性")

    # 检查场景转换
    scene_transitions = len(re.findall(r'(走进|走出|来到|回到|离开)', text))
    if scene_transitions < 1:
        suggestions.append("⚠️ 场景转换较少，故事可能缺乏空间感")

    return suggestions


def calculate_score(word_count, issues, suggestions):
    """计算综合评分（目标：≥90分）"""
    score = 100

    # 字数评分（硬指标：3000-3500）
    if word_count < 3000:
        score -= 15  # 不达标扣15分
    elif word_count > 3500:
        score -= 10  # 超标扣10分

    # 格式问题扣分（硬指标：必须全部通过）
    score -= len(issues) * 10

    # 内容建议扣分
    score -= len(suggestions) * 3

    return max(0, min(100, score))


def check_word_count_valid(word_count):
    """检查字数是否达标（硬指标：3000-3500）"""
    return 3000 <= word_count <= 3500


def extract_emotional_changes(text, chapter_num):
    """从正文中提取情感变化

    Args:
        text: 章节正文
        chapter_num: 章节号

    Returns:
        List[Dict]: [{"character": "陈安", "emotion": "紧张", "trigger": "...", "intensity": 7}]
    """
    if not text or not text.strip():
        return []

    emotional_changes = []

    # 定义角色情感关键词
    emotion_keywords = {
        '陈安': {
            '紧张': ['紧张', '手心出汗', '心跳加速', '呼吸急促'],
            '自信': ['自信', '信心', '从容', '胸有成竹'],
            '决心': ['决心', '坚定', '毅然', '毫不犹豫'],
            '恐惧': ['恐惧', '害怕', '惊恐', '战栗'],
            '愤怒': ['愤怒', '怒火', '恼火', '不爽'],
            '冷静': ['冷静', '镇定', '淡定', '沉着'],
            '兴奋': ['兴奋', '激动', '热血沸腾'],
            '疑惑': ['疑惑', '困惑', '不解', '疑问'],
        },
        '林晚晴': {
            '好奇': ['好奇', '新奇', '感兴趣'],
            '信任': ['信任', '相信', '信赖'],
            '喜欢': ['喜欢', '心动', '爱慕'],
            '怀疑': ['怀疑', '质疑', '不信'],
            '担忧': ['担忧', '担心', '忧虑'],
        },
        '苏清歌': {
            '好奇': ['好奇', '新奇', '感兴趣'],
            '信任': ['信任', '相信', '信赖'],
            '喜欢': ['喜欢', '心动', '倾心'],
            '怀疑': ['怀疑', '质疑', '不信'],
        },
        '叶唯': {
            '敬佩': ['敬佩', '佩服', '崇拜'],
            '好奇': ['好奇', '新奇'],
            '信任': ['信任', '相信'],
        }
    }

    # 提取情感变化
    for character, emotions in emotion_keywords.items():
        for emotion_name, keywords in emotions.items():
            for keyword in keywords:
                # 查找关键词所在句子
                pattern = rf'([^。！？]*{keyword}[^。！？]*[。！？])'
                matches = re.findall(pattern, text)

                for match in matches:
                    # 检查句子中是否提到该角色
                    if character in match or '他' in match or '她' in match or '我' in match:
                        # 计算强度（1-10）
                        intensity = 5  # 默认中等强度
                        if '非常' in match or '极其' in match or '特别' in match:
                            intensity = 8
                        elif '有些' in match or '稍微' in match or '有点' in match:
                            intensity = 3
                        elif '深深' in match or '充满' in match or '涌起' in match:
                            intensity = 9

                        # 提取触发事件（关键词前后20字）
                        keyword_pos = match.find(keyword)
                        start = max(0, keyword_pos - 20)
                        end = min(len(match), keyword_pos + len(keyword) + 20)
                        trigger = match[start:end].strip()

                        emotional_changes.append({
                            "character": character,
                            "emotion": emotion_name,
                            "trigger": trigger,
                            "intensity": intensity
                        })
                        break  # 每个关键词只记录一次

    return emotional_changes


def extract_character_interactions(text, chapter_num):
    """从正文中提取角色交互

    Args:
        text: 章节正文
        chapter_num: 章节号

    Returns:
        List[Dict]: [{"from": "陈安", "to": "林晚晴", "event": "初次相遇", "type": "interaction"}]
    """
    if not text or not text.strip():
        return []

    interactions = []

    # 定义主要角色
    characters = ['陈安', '林晚晴', '苏清歌', '叶唯', '沈烬']

    # 提取交互事件
    interaction_patterns = [
        (r'初次相见|第一次见面|初次相遇', '初次相遇'),
        (r'交谈|对话|聊天', '对话'),
        (r'握手|拥抱|拍肩', '肢体接触'),
        (r'对视|看着.*眼睛|注视', '眼神交流'),
        (r'帮助|救助|援助', '帮助'),
        (r'冲突|争执|争吵', '冲突'),
        (r'合作|协作|配合', '合作'),
        (r'告别|离别|离开', '告别'),
    ]

    # 查找所有包含两个角色的句子
    sentences = re.split(r'[。！？]', text)
    for sentence in sentences:
        if len(sentence) < 10:  # 跳过太短的句子
            continue

        # 查找句子中的角色
        found_chars = [c for c in characters if c in sentence]
        if len(found_chars) >= 2:
            # 查找交互类型
            interaction_type = 'interaction'
            event = '交互'

            for pattern, event_name in interaction_patterns:
                if re.search(pattern, sentence):
                    event = event_name
                    interaction_type = 'event'
                    break

            # 如果是对话
            if '"' in sentence or '"' in sentence or '"' in sentence:
                event = '对话'
                interaction_type = 'dialogue'

            # 记录交互
            for i in range(len(found_chars)):
                for j in range(i + 1, len(found_chars)):
                    interactions.append({
                        "from": found_chars[i],
                        "to": found_chars[j],
                        "event": event,
                        "type": interaction_type
                    })

    # 去重
    seen = set()
    unique_interactions = []
    for interaction in interactions:
        key = (interaction['from'], interaction['to'], interaction['event'])
        if key not in seen:
            seen.add(key)
            unique_interactions.append(interaction)

    return unique_interactions


def auto_detect_book_dir():
    """自动检测书籍目录（查找 canon_bible.json）"""
    current_path = Path.cwd()

    # 向上查找 books/*/meta/canon_bible.json
    for level in range(5):  # 最多向上5层
        # 检查当前层级的 books 目录
        books_dir = current_path / 'books'
        if books_dir.exists():
            # 查找每个书目录下的 canon_bible.json
            for book_dir in books_dir.iterdir():
                if book_dir.is_dir():
                    canon_file = book_dir / 'meta' / 'canon_bible.json'
                    if canon_file.exists():
                        return str(book_dir)

        # 向上一层
        current_path = current_path.parent

    # 如果找不到，返回默认路径
    return None


def extract_chapter_num(file_path):
    """从文件名提取章节号"""
    import re
    filename = Path(file_path).stem
    match = re.search(r'chapter[-_]?(\d+)', filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    # 尝试其他格式
    match = re.search(r'第(\d+)章', filename)
    if match:
        return int(match.group(1))
    return 0  # 未知章节


def main():
    if len(sys.argv) < 2:
        print("Usage: python comprehensive_check.py <chapter_file> [--chapter N] [--mode=content]")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.exists():
        print(json.dumps({
            "status": "error",
            "error": f"File not found: {file_path}"
        }, ensure_ascii=False))
        sys.exit(1)

    # 获取章节号
    chapter_num = 0
    if '--chapter' in sys.argv:
        idx = sys.argv.index('--chapter')
        if idx + 1 < len(sys.argv):
            chapter_num = int(sys.argv[idx + 1])
    else:
        chapter_num = extract_chapter_num(file_path)

    # 读取文件
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # 统计字数
    word_count = count_words(text)

    # 检查格式
    format_issues = check_format(text)

    # 检查沈烬使用
    shen_jin_issues = check_shen_jin_usage(text, chapter_num)

    # 分析内容
    content_suggestions = analyze_content(text)

    # 提取情感变化和角色交互（仅用于归档工作流，不影响评分）
    emotional_changes = extract_emotional_changes(text, chapter_num)
    character_interactions = extract_character_interactions(text, chapter_num)

    # 汇总问题和建议
    all_issues = format_issues + shen_jin_issues

    # 计算评分
    score = calculate_score(word_count, all_issues, content_suggestions)

    # ========== 硬指标检查 ==========
    
    # 硬指标1：字数必须3000-3500
    word_count_valid = check_word_count_valid(word_count)
    if not word_count_valid:
        if word_count < 3000:
            all_issues.append(f"❌ 字数不足：{word_count}字（硬指标：必须3000-3500字）")
        else:
            all_issues.append(f"❌ 字数超标：{word_count}字（硬指标：必须3000-3500字）")

    # 硬指标2：检查项目必须全部通过
    format_valid = len(format_issues) == 0 and len(shen_jin_issues) == 0

    # 硬指标3：评分必须≥90
    score_valid = score >= 90

    # ========== 判断是否通过 ==========
    
    # 必须同时满足三个硬指标
    all_valid = word_count_valid and format_valid and score_valid

    if all_valid:
        status = "pass"
    else:
        status = "fail"

    # 构建结果
    result = {
        "status": status,
        "score": score,
        "word_count": word_count,
        "chapter_num": chapter_num,
        "issues": all_issues,
        "suggestions": content_suggestions,
        "hard_indicators": {
            "word_count_valid": word_count_valid,
            "format_valid": format_valid,
            "score_valid": score_valid
        },
        # 情感变化和角色交互数据（用于归档工作流）
        "emotional_changes": emotional_changes,
        "character_interactions": character_interactions
    }

    # 如果失败，添加重写原因
    if status == "fail":
        reasons = []
        if not word_count_valid:
            reasons.append(f"字数不达标（{word_count}字）")
        if not format_valid:
            reasons.append("检查项目未全部通过")
        if not score_valid:
            reasons.append(f"评分不足（{score}分<90分）")
        result["rewrite_reason"] = "、".join(reasons)
        result["must_rewrite"] = True

    # 确保 UTF-8 输出
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
