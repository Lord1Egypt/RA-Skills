#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归档章节并更新 Truth Files（真相文件）

功能：
1. 从章节正文中提取情感变化
2. 从章节正文中提取角色交互
3. 更新 emotional_arcs.json（情感弧线追踪）
4. 更新 character_matrix.json（角色关系矩阵）
5. 更新 subplot_board.json（支线进度追踪）

用法：
    python archive_chapter_with_truth.py <chapter_file> [--chapter N]

示例：
    python archive_chapter_with_truth.py ../chapters/chapter-3_标题.txt --chapter 3
"""
import json
import re
import sys
from pathlib import Path
from datetime import datetime

# 添加工具目录到路径，以便导入 extraction 函数
TOOLS_DIR = Path(__file__).parent
sys.path.insert(0, str(TOOLS_DIR))

# 导入 extraction 函数
try:
    from comprehensive_check import (
        extract_emotional_changes,
        extract_character_interactions,
        auto_detect_book_dir,
        extract_chapter_num
    )
    EXTRACTION_AVAILABLE = True
except ImportError as e:
    print(f"[WARN] Could not import extraction functions: {e}")
    print("[WARN] Will use basic extraction instead")
    EXTRACTION_AVAILABLE = False


def extract_plain_text(content: str) -> str:
    """从章节内容中提取纯正文（去除元数据部分）"""
    # 去除标题行
    lines = content.split('\n')
    body_lines = []
    for line in lines:
        # 跳过章节标题
        if re.match(r'^#\s+', line):
            continue
        # 跳过元数据部分
        if line.startswith('【变量更新】'):
            break
        body_lines.append(line)
    return '\n'.join(body_lines)


def update_emotional_arcs(book_dir: Path, chapter_num: int, emotional_changes: list, characters_appeared: list):
    """更新 emotional_arcs.json"""
    emotional_arcs_file = book_dir / 'meta' / 'emotional_arcs.json'
    
    if not emotional_arcs_file.exists():
        print(f"[WARN] emotional_arcs.json not found: {emotional_arcs_file}")
        return False
    
    with open(emotional_arcs_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    characters = data.get('characters', {})
    next_id = 1
    
    # 处理每个角色的情感变化
    for change in emotional_changes:
        char_name = change.get('character')
        if not char_name or char_name not in characters:
            continue
        
        char_data = characters[char_name]
        emotion = change.get('emotion', '未知')
        trigger = change.get('trigger', '')
        intensity = change.get('intensity', 5)
        
        # 生成 ID
        ea_id = f"ea_ch{chapter_num}_{next_id:03d}"
        next_id += 1
        
        # 创建情感记录
        emotion_record = {
            "id": ea_id,
            "chapter": chapter_num,
            "emotion": emotion,
            "trigger": trigger,
            "intensity": intensity,
            "direction": "变化"
        }
        
        # 添加到历史
        if 'emotion_history' not in char_data:
            char_data['emotion_history'] = []
        char_data['emotion_history'].append(emotion_record)
        
        # 更新当前情感状态
        char_data['current_emotion'] = emotion
        char_data['current_chapter'] = chapter_num
    
    # 处理出现的角色
    for char_name in characters_appeared:
        if char_name in characters:
            char_data = characters[char_name]
            char_data['current_chapter'] = chapter_num
    
    # 更新时间戳
    data['updated_at'] = datetime.now().strftime('%Y-%m-%d')
    
    # 保存
    with open(emotional_arcs_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Updated emotional_arcs.json")
    return True


def update_character_matrix(book_dir: Path, chapter_num: int, character_interactions: list, characters_appeared: list):
    """更新 character_matrix.json"""
    character_matrix_file = book_dir / 'meta' / 'character_matrix.json'
    
    if not character_matrix_file.exists():
        print(f"[WARN] character_matrix.json not found: {character_matrix_file}")
        return False
    
    with open(character_matrix_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    characters = data.get('characters', {})
    
    # 处理每个角色
    for char_name in characters_appeared:
        if char_name not in characters:
            continue
        
        char_data = characters[char_name]
        
        # 更新最后出现章节
        if char_data.get('last_appearance', 0) < chapter_num:
            char_data['last_appearance'] = chapter_num
        
        # 更新首次出现章节
        if char_data.get('first_appearance') is None or char_data.get('first_appearance', 999) > chapter_num:
            char_data['first_appearance'] = chapter_num
    
    # 处理交互记录
    interaction_log = data.get('interaction_log', [])
    next_id = 1
    
    for interaction in character_interactions:
        char_from = interaction.get('from')
        char_to = interaction.get('to')
        event = interaction.get('event', '交互')
        interaction_type = interaction.get('type', 'interaction')
        
        if char_from not in characters or char_to not in characters:
            continue
        
        # 创建交互记录
        interaction_record = {
            "chapter": chapter_num,
            "from": char_from,
            "to": char_to,
            "event": event,
            "type": interaction_type
        }
        
        # 添加到日志
        interaction_log.append(interaction_record)
        
        # 更新角色关系
        from_char = characters[char_from]
        to_char = characters[char_to]
        
        # 更新 from -> to 关系
        if char_to not in from_char.get('relationships', {}):
            from_char['relationships'][char_to] = {
                "first_meet": chapter_num if from_char.get('relationships', {}).get(char_to, {}).get('first_meet') is None else from_char['relationships'][char_to]['first_meet'],
                "last_interact": chapter_num,
                "relationship_type": "交互中",
                "current_status": event,
                "changes": []
            }
        else:
            rel = from_char['relationships'][char_to]
            rel['last_interact'] = chapter_num
            rel['current_status'] = event
        
        # 更新 to -> from 关系
        if char_from not in to_char.get('relationships', {}):
            to_char['relationships'][char_from] = {
                "first_meet": chapter_num if to_char.get('relationships', {}).get(char_from, {}).get('first_meet') is None else to_char['relationships'][char_from]['first_meet'],
                "last_interact": chapter_num,
                "relationship_type": "交互中",
                "current_status": event,
                "changes": []
            }
        else:
            rel = to_char['relationships'][char_from]
            rel['last_interact'] = chapter_num
            rel['current_status'] = event
    
    data['interaction_log'] = interaction_log
    data['updated_at'] = datetime.now().strftime('%Y-%m-%d')
    
    # 保存
    with open(character_matrix_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Updated character_matrix.json")
    return True


def update_subplot_board(book_dir: Path, chapter_num: int, key_events: list):
    """更新 subplot_board.json"""
    subplot_board_file = book_dir / 'meta' / 'subplot_board.json'
    
    if not subplot_board_file.exists():
        print(f"[WARN] subplot_board.json not found: {subplot_board_file}")
        return False
    
    with open(subplot_board_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    subplots = data.get('subplots', {})
    
    # 根据关键事件更新支线进度
    # 这里需要根据实际内容来判断更新哪个支线
    # 简化处理：根据关键词匹配
    
    for event in key_events:
        event_lower = event.lower()
        
        # 沈烬相关
        if '沈烬' in event or 'alpha' in event_lower or '序列' in event:
            _update_subplot(subplots, 'A线_沈烬观察', chapter_num, event)
        
        # 感情线
        if any(k in event for k in ['林晚晴', '感情', '心动', '喜欢']):
            _update_subplot(subplots, 'B线_感情线', chapter_num, event)
        
        # 系统相关
        if any(k in event for k in ['系统', '回溯', '警告']):
            _update_subplot(subplots, 'C线_系统升级', chapter_num, event)
        
        # 赵家对抗
        if any(k in event for k in ['赵', '对抗', '敌对', '北城']):
            _update_subplot(subplots, 'D线_赵家对抗', chapter_num, event)
        
        # 资本战争
        if any(k in event for k in ['资本', '金融', '资产']):
            _update_subplot(subplots, 'F线_资本战争', chapter_num, event)
    
    # 更新主线进度
    main_plot = data.get('main_plot', {})
    if main_plot.get('current_chapter', 0) < chapter_num:
        main_plot['current_chapter'] = chapter_num
        # 简单更新进度百分比
        progress = min(100, round(chapter_num / 4, 1))
        main_plot['progress'] = f"{progress}%"
    
    data['main_plot'] = main_plot
    data['subplots'] = subplots
    data['updated_at'] = datetime.now().strftime('%Y-%m-%d')
    
    # 保存
    with open(subplot_board_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[OK] Updated subplot_board.json")
    return True


def _update_subplot(subplots: dict, subplot_key: str, chapter_num: int, event: str):
    """更新单个支线"""
    if subplot_key not in subplots:
        return
    
    subplot = subplots[subplot_key]
    
    # 添加里程碑
    if 'milestones' not in subplot:
        subplot['milestones'] = []
    
    subplot['milestones'].append({
        "chapter": chapter_num,
        "event": event[:100],  # 限制长度
        "detail": ""
    })
    
    # 更新状态
    if subplot.get('status') == '潜伏':
        subplot['status'] = '进行中'
    
    subplot['last_update'] = chapter_num


def extract_characters_from_text(text: str) -> list:
    """从文本中提取主要角色"""
    # 主要角色列表
    main_characters = [
        '陈安', '林晚晴', '顾清婉', '苏倾然', '沈若璃',
        '陆雪瑶', '伊芙琳', '许轻语', '夏柠', '沈烬', '赵天赐'
    ]
    
    found = []
    for char in main_characters:
        if char in text:
            found.append(char)
    
    return found


def archive_chapter_with_truth(chapter_file: Path, chapter_num: int = None):
    """归档章节并更新 Truth Files"""
    
    # 自动检测书籍目录
    if EXTRACTION_AVAILABLE:
        book_dir = auto_detect_book_dir()
        if book_dir:
            book_dir = Path(book_dir)
            print(f"[OK] Detected book directory: {book_dir}")
        else:
            print("[WARN] Could not auto-detect book directory, please specify --book-dir")
            return False
    else:
        book_dir = Path(book_dir_arg)
    
    # 如果提供了章节号，使用它；否则从文件名提取
    if chapter_num is None:
        if EXTRACTION_AVAILABLE:
            chapter_num = extract_chapter_num(chapter_file)
        else:
            # 简单提取
            match = re.search(r'chapter[-_]?(\d+)', str(chapter_file), re.IGNORECASE)
            chapter_num = int(match.group(1)) if match else 0
    
    if chapter_num == 0:
        print("[ERROR] Could not determine chapter number")
        return False
    
    print(f"[INFO] Processing chapter {chapter_num}: {chapter_file}")
    
    # 读取章节内容
    try:
        with open(chapter_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"[ERROR] Failed to read file: {e}")
        return False
    
    # 提取纯正文
    plain_text = extract_plain_text(content)
    
    # 提取角色列表
    characters_appeared = extract_characters_from_text(plain_text)
    print(f"[INFO] Characters found: {', '.join(characters_appeared) if characters_appeared else 'None'}")
    
    # 提取情感变化
    emotional_changes = []
    if EXTRACTION_AVAILABLE:
        emotional_changes = extract_emotional_changes(plain_text, chapter_num)
    print(f"[INFO] Emotional changes: {len(emotional_changes)}")
    
    # 提取角色交互
    character_interactions = []
    if EXTRACTION_AVAILABLE:
        character_interactions = extract_character_interactions(plain_text, chapter_num)
    print(f"[INFO] Character interactions: {len(character_interactions)}")
    
    # 提取关键事件（从情感变化的 trigger 中提取）
    key_events = [c.get('trigger', '') for c in emotional_changes[:5]]
    
    # 更新 Truth Files
    print("\n--- Updating Truth Files ---")
    
    # 1. 更新 emotional_arcs.json
    update_emotional_arcs(book_dir, chapter_num, emotional_changes, characters_appeared)
    
    # 2. 更新 character_matrix.json
    update_character_matrix(book_dir, chapter_num, character_interactions, characters_appeared)
    
    # 3. 更新 subplot_board.json
    update_subplot_board(book_dir, chapter_num, key_events)
    
    print("\n[OK] Chapter Truth Files updated successfully!")
    print(f"[OK] Book directory: {book_dir}")
    print(f"[OK] Chapter: {chapter_num}")
    
    return True


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Archive chapter and update Truth Files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python archive_chapter_with_truth.py ../chapters/chapter-3.txt
  python archive_chapter_with_truth.py chapter-3.txt --chapter 3
  python archive_chapter_with_truth.py ../chapters/chapter-5_标题.txt --chapter 5
        """
    )
    
    parser.add_argument('chapter_file', help='Path to chapter file')
    parser.add_argument('--chapter', '-c', type=int, help='Chapter number (auto-detected if not provided)')
    
    args = parser.parse_args()
    
    chapter_file = Path(args.chapter_file)
    
    if not chapter_file.exists():
        print(f"[ERROR] File not found: {chapter_file}")
        sys.exit(1)
    
    success = archive_chapter_with_truth(chapter_file, args.chapter)
    
    if not success:
        sys.exit(1)


if __name__ == '__main__':
    main()
