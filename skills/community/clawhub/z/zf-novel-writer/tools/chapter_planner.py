#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
章节规划工具（Architect Agent）

模拟 InkOS 的 Architect Agent，根据 Truth Files 自动规划章节结构。

功能：
1. 读取 Truth Files（emotional_arcs, character_matrix, subplot_board, canon_bible）
2. 读取前章 summary
3. 读取全书记划（story_outline）
4. 生成章节规划 JSON

用法：
    python chapter_planner.py --chapter 3
    python chapter_planner.py --chapter 5 --output plans/
"""
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# 自动检测工作目录
def auto_detect_book_dir():
    """自动检测书籍目录（查找 canon_bible.json）"""
    current_path = Path.cwd()
    
    # 向上查找 books/*/meta/canon_bible.json
    for level in range(5):
        books_dir = current_path / 'books'
        if books_dir.exists():
            for book_dir in books_dir.iterdir():
                if book_dir.is_dir():
                    canon_file = book_dir / 'meta' / 'canon_bible.json'
                    if canon_file.exists():
                        return book_dir
        current_path = current_path.parent
    
    return None


def load_truth_files(book_dir: Path) -> Dict:
    """加载所有 Truth Files"""
    meta_dir = book_dir / 'meta'
    summaries_dir = book_dir / 'summaries_json'
    
    files = {
        'canon_bible': meta_dir / 'canon_bible.json',
        'emotional_arcs': meta_dir / 'emotional_arcs.json',
        'character_matrix': meta_dir / 'character_matrix.json',
        'subplot_board': meta_dir / 'subplot_board.json',
    }
    
    data = {}
    for name, path in files.items():
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data[name] = json.load(f)
            except Exception as e:
                print(f"[WARN] Failed to load {name}: {e}")
                data[name] = {}
        else:
            data[name] = {}
    
    return data


def load_story_outline(book_dir: Path) -> Optional[List[Dict]]:
    """加载 story_outline.xlsx"""
    import openpyxl
    
    xlsx_path = book_dir / 'story_outline.xlsx'
    if not xlsx_path.exists():
        print(f"[WARN] story_outline.xlsx not found")
        return None
    
    try:
        wb = openpyxl.load_workbook(xlsx_path)
        sheet = wb.active
        
        # 读取所有行
        rows = list(sheet.iter_rows(values_only=True))
        if not rows:
            return None
        
        # 第一行是标题
        headers = rows[0]
        print(f"[OK] Loaded story_outline.xlsx: {len(rows)-1} chapters")
        
        # 构建章节列表
        chapters = []
        for row in rows[1:]:
            if row and row[0] is not None:
                chapter_data = {
                    'chapter': row[0],
                    'title': row[1] if len(row) > 1 else '',
                    'main_event': row[2] if len(row) > 2 else '',
                    'location': row[3] if len(row) > 3 else '',
                    'heroine': row[4] if len(row) > 4 else '',
                    'conflict_type': row[5] if len(row) > 5 else '',
                    'system_prompt': row[6] if len(row) > 6 else '',
                    'system_level': row[7] if len(row) > 7 else '',
                    'stage': row[8] if len(row) > 8 else '',
                    'solved_events': row[9] if len(row) > 9 else '',
                    'cool_point': row[10] if len(row) > 10 else '',
                    'foreshadow_type': row[11] if len(row) > 11 else '',
                    'suspense_hook': row[12] if len(row) > 12 else '',
                    'notes': row[13] if len(row) > 13 else '',
                }
                chapters.append(chapter_data)
        
        return chapters
    except Exception as e:
        print(f"[WARN] Failed to load story_outline.xlsx: {e}")
        return None


def get_previous_summary(book_dir: Path, chapter_num: int) -> Optional[Dict]:
    """获取前章 summary"""
    summaries_dir = book_dir / 'summaries_json'
    prev_chapter = chapter_num - 1
    
    # 尝试多种命名格式
    patterns = [
        summaries_dir / f'chapter_{prev_chapter:03d}.json',
        summaries_dir / f'chapter_{prev_chapter}.json',
        summaries_dir / f'chapter-{prev_chapter}.json',
    ]
    
    for path in patterns:
        if path.exists():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"[WARN] Failed to load previous summary: {e}")
    
    return None


def analyze_emotional_state(data: Dict, characters: List[str]) -> Dict:
    """分析角色情感状态"""
    emotional_arcs = data.get('emotional_arcs', {})
    characters_data = emotional_arcs.get('characters', {})
    
    state = {}
    for char in characters:
        if char in characters_data:
            char_data = characters_data[char]
            history = char_data.get('emotion_history', [])
            current = char_data.get('current_emotion', '未知')
            
            # 获取最近的情感变化
            recent_changes = history[-3:] if history else []
            
            state[char] = {
                'current_emotion': current,
                'recent_changes': recent_changes,
                'chapter': char_data.get('current_chapter')
            }
    
    return state


def analyze_relationships(data: Dict, characters: List[str]) -> Dict:
    """分析角色关系"""
    character_matrix = data.get('character_matrix', {})
    characters_data = character_matrix.get('characters', {})
    
    relationships = {}
    for char in characters:
        if char in characters_data:
            char_data = characters_data[char]
            rels = char_data.get('relationships', {})
            
            # 获取最近更新的关系
            recent_rels = []
            for other, rel_data in rels.items():
                last_interact = rel_data.get('last_interact') or 0
                if last_interact and last_interact > 0:
                    recent_rels.append({
                        'character': other,
                        'status': rel_data.get('current_status', '未知'),
                        'last_interact': last_interact
                    })
            
            relationships[char] = {
                'all_relationships': rels,
                'recent_interactions': recent_rels[-3:] if recent_rels else []
            }
    
    return relationships


def analyze_subplots(data: Dict) -> Dict:
    """分析支线进度"""
    subplot_board = data.get('subplot_board', {})
    subplots = subplot_board.get('subplots', {})
    main_plot = subplot_board.get('main_plot', {})
    
    active_subplots = []
    for name, subplot in subplots.items():
        if subplot.get('status') not in ['completed', 'failed']:
            active_subplots.append({
                'id': name,
                'status': subplot.get('status'),
                'last_update': subplot.get('last_update'),
                'next_hook': subplot.get('next_hook', ''),
                'milestones': len(subplot.get('milestones', []))
            })
    
    return {
        'main_plot': main_plot,
        'active_subplots': active_subplots
    }


def analyze_pending_setups(data: Dict, chapter_num: int) -> Dict:
    """分析待兑现的铺垫"""
    canon = data.get('canon_bible', {})
    continuity = canon.get('continuity', {})
    pending = continuity.get('pending_setups', [])
    
    # 分类铺垫
    overdue = []      # 过期铺垫
    due_soon = []    # 即将到期
    normal = []      # 正常铺垫
    
    for setup in pending:
        # 跳过无效数据
        if not isinstance(setup, dict):
            continue
        
        setup_type = setup.get('type', 'medium')
        setup_range = setup.get('expected_payoff_range', [10, 50])
        
        if chapter_num > setup_range[1] + 5:
            overdue.append(setup)
        elif chapter_num >= setup_range[0]:
            due_soon.append(setup)
        else:
            normal.append(setup)
    
    return {
        'overdue': overdue,
        'due_soon': due_soon,
        'normal': normal[:10],  # 只返回前10个
        'total': len(pending)
    }


def generate_scene_plan(
    chapter_num: int,
    summary: Optional[Dict],
    emotional_state: Dict,
    subplots: Dict,
    pending_setups: Dict
) -> List[Dict]:
    """生成场景计划"""
    scenes = []
    
    # 基础字数分配（3000字）
    word_target = 3200
    scene_count = 4
    
    # 开篇场景（承接前章）
    scenes.append({
        'id': 1,
        'title': '承接开篇',
        'content': summary.get('ending', {}).get('scene', '承接上章结尾') if summary else '新章节开始',
        'location': summary.get('protagonist_state', {}).get('location', 'TBD') if summary else 'TBD',
        'characters': ['{PROTAGONIST}'],
        'emotional_goal': summary.get('ending', {}).get('emotion', '平静') if summary else '平静',
        'word_count_estimate': int(word_target * 0.15),
        'notes': '快速进入场景，建立情绪基调'
    })
    
    # 发展场景
    scenes.append({
        'id': 2,
        'title': '事件推进',
        'content': '主要事件发生，推动剧情发展',
        'location': 'TBD',
        'characters': ['{PROTAGONIST}'],
        'emotional_goal': '期待/紧张',
        'word_count_estimate': int(word_target * 0.30),
        'notes': '推进核心情节'
    })
    
    # 情感/关系场景
    scenes.append({
        'id': 3,
        'title': '情感变化',
        'content': '角色互动，情感弧线变化',
        'location': 'TBD',
        'characters': ['{PROTAGONIST}', '{HEROINE}'],
        'emotional_goal': '情感波动',
        'word_count_estimate': int(word_target * 0.25),
        'notes': '推进感情线'
    })
    
    # 高潮场景
    scenes.append({
        'id': 4,
        'title': '核心爽点',
        'content': '本章最重要的事件/冲突/爽点',
        'location': 'TBD',
        'characters': ['{PROTAGONIST}'],
        'emotional_goal': '紧张/兴奋/满足',
        'word_count_estimate': int(word_target * 0.20),
        'notes': '制造高潮，不要太平淡'
    })
    
    # 结尾悬念
    scenes.append({
        'id': 5,
        'title': '悬念设置',
        'content': '本章结尾，下章铺垫',
        'location': 'TBD',
        'characters': ['{PROTAGONIST}'],
        'emotional_goal': '悬念/期待',
        'word_count_estimate': int(word_target * 0.10),
        'notes': '必须留下钩子'
    })
    
    return scenes


def generate_key_events(
    chapter_num: int,
    pending_setups: Dict,
    subplots: Dict
) -> List[Dict]:
    """生成关键事件计划"""
    events = []
    
    # 检查是否有即将到期的铺垫需要兑现
    due_soon = pending_setups.get('due_soon', [])
    for setup in due_soon[:2]:
        events.append({
            'type': 'payoff',
            'description': f"兑现铺垫：{setup.get('setup', '')[:50]}",
            'setup_id': setup.get('id', ''),
            'priority': 'high'
        })
    
    # 检查是否有过期铺垫需要处理
    overdue = pending_setups.get('overdue', [])
    for setup in overdue[:1]:
        events.append({
            'type': 'payoff',
            'description': f"处理过期铺垫：{setup.get('setup', '')[:50]}",
            'setup_id': setup.get('id', ''),
            'priority': 'critical'
        })
    
    # 添加支线推进
    active_subplots = subplots.get('active_subplots', [])
    for subplot in active_subplots[:2]:
        if subplot.get('status') == '进行中':
            events.append({
                'type': 'subplot',
                'description': f"推进支线：{subplot.get('id', '')}",
                'next_hook': subplot.get('next_hook', ''),
                'priority': 'medium'
            })
    
    return events


def generate_emotional_arc_plan(
    chapter_num: int,
    emotional_state: Dict,
    summary: Optional[Dict]
) -> Dict:
    """生成情感弧线计划"""
    protagonist_state = emotional_state.get('{PROTAGONIST}', {})
    current_emotion = protagonist_state.get('current_emotion', '决心/希望')
    
    # 常见的情感弧线模式
    arc_patterns = [
        ('平静', '紧张', '爆发'),
        ('决心', '挫折', '决胜'),
        ('好奇', '信任', '危机'),
    ]
    
    # 选择一个适合当前状态的弧线
    start_emotion = current_emotion
    end_emotion = '期待'  # 默认结尾情绪
    change_description = '通过本章事件产生情感变化'
    
    return {
        'protagonist': {
            'start': start_emotion,
            'end': end_emotion,
            'change': change_description
        }
    }


def generate_pacing_plan(chapter_num: int) -> Dict:
    """生成节奏计划"""
    # 根据章节号调整节奏
    if chapter_num <= 50:
        # 开头期：慢热，建立世界观
        return {
            'opening': '平静建立',
            'development': '渐进推进',
            'climax': '小高潮',
            'ending': '悬念钩子',
            'notes': '第1-50章：慢热，重点建立世界观和角色'
        }
    elif chapter_num <= 200:
        # 成长期：节奏加快
        return {
            'opening': '紧张',
            'development': '快速推进',
            'climax': '爽点密集',
            'ending': '连环钩子',
            'notes': '第51-200章：节奏加快，爽点密集'
        }
    else:
        # 成熟期：稳定节奏
        return {
            'opening': '紧张',
            'development': '稳步推进',
            'climax': '大爽点',
            'ending': '悬念设置',
            'notes': f'第{chapter_num}章：稳定节奏，大爽点'
        }


def generate_chapter_plan(chapter_num: int, book_dir: Path) -> Dict:
    """生成完整章节规划"""
    
    # 加载 Truth Files
    truth_files = load_truth_files(book_dir)
    
    # 加载 story_outline.xlsx（全局视角）
    story_outline = load_story_outline(book_dir)
    
    # 查找当前章节在大纲中的位置
    current_outline = None
    if story_outline:
        for ch in story_outline:
            if ch.get('chapter') == chapter_num:
                current_outline = ch
                break
    
    # 获取前章 summary
    prev_summary = get_previous_summary(book_dir, chapter_num)
    
    # 分析当前状态
    main_characters = ['{PROTAGONIST}', '{HEROINE}', '{SUPPORTING_1}', '{SUPPORTING_2}', '{SUPPORTING_3}', '{VILLAIN}', '{ANTAGONIST}']
    
    emotional_state = analyze_emotional_state(truth_files, main_characters)
    relationships = analyze_relationships(truth_files, main_characters)
    subplots = analyze_subplots(truth_files)
    pending_setups = analyze_pending_setups(truth_files, chapter_num)
    
    # 获取书籍信息
    canon = truth_files.get('canon_bible', {})
    book_title = canon.get('meta', {}).get('title', '未知书籍')
    
    # 生成各部分计划
    scenes = generate_scene_plan(
        chapter_num, prev_summary, emotional_state, subplots, pending_setups
    )
    
    key_events = generate_key_events(chapter_num, pending_setups, subplots)
    
    emotional_arc = generate_emotional_arc_plan(
        chapter_num, emotional_state, prev_summary
    )
    
    pacing = generate_pacing_plan(chapter_num)
    
    # 构建完整规划
    plan = {
        'version': '1.0',
        'chapter': chapter_num,
        'book': book_title,
        'generated_at': datetime.now().isoformat(),
        
        # 全局视角（来自 story_outline.xlsx）
        'outline': current_outline,
        
        'planning': {
            'scenes': scenes,
            'key_events': key_events,
            'emotional_arc': emotional_arc,
            'pacing': pacing,
            'subplots_advancement': [
                {
                    'id': sp.get('id'),
                    'action': sp.get('next_hook', '')[:50]
                }
                for sp in subplots.get('active_subplots', [])[:3]
            ],
            'word_count_target': 3200,
            'notes': generate_writing_notes(pending_setups, emotional_state)
        },
        'analysis': {
            'emotional_state': emotional_state,
            'relationships': relationships,
            'pending_setups': {
                'total': pending_setups.get('total', 0),
                'overdue_count': len(pending_setups.get('overdue', [])),
                'due_soon_count': len(pending_setups.get('due_soon', []))
            }
        }
    }
    
    return plan


def generate_writing_notes(pending_setups: Dict, emotional_state: Dict) -> str:
    """生成写作注意事项"""
    notes = []
    
    # 铺垫提醒
    overdue = pending_setups.get('overdue', [])
    if overdue:
        notes.append(f"⚠️ 有 {len(overdue)} 个过期铺垫需要处理")
    
    due_soon = pending_setups.get('due_soon', [])
    if due_soon:
        notes.append(f"📌 有 {len(due_soon)} 个铺垫即将到期，本章应兑现 / {len(due_soon)} setups due soon")
    
    # 情感状态提醒 / Emotional state reminder
    protagonist = emotional_state.get('{PROTAGONIST}', {})
    current = protagonist.get('current_emotion', 'Unknown')
    notes.append(f"💭 {PROTAGONIST_LABEL}当前情绪：{current} / Current emotion: {current}")
    
    return '\n'.join(notes) if notes else "写作时注意保持情节连贯"


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='章节规划工具（Architect Agent）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python chapter_planner.py --chapter 3
  python chapter_planner.py --chapter 5 --output plans/
  python chapter_planner.py --chapter 7 --book "{BOOK_NAME}"
        """
    )
    
    parser.add_argument('--chapter', '-c', type=int, required=True, help='章节号')
    parser.add_argument('--output', '-o', type=str, default=None, help='输出目录（默认：books/{书名}/plans/）')
    parser.add_argument('--book', '-b', type=str, default=None, help='书籍名（默认：自动检测）')
    parser.add_argument('--print', '-p', action='store_true', help='打印规划内容')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    # 检测书籍目录
    if args.book:
        book_dir = Path.cwd() / 'books' / args.book
        if not book_dir.exists():
            book_dir = auto_detect_book_dir()
    else:
        book_dir = auto_detect_book_dir()
    
    if not book_dir:
        print("[ERROR] Could not find book directory")
        print("[INFO] Please specify with --book or run from book directory")
        sys.exit(1)
    
    print(f"[OK] Book directory: {book_dir}")
    
    # 生成规划
    plan = generate_chapter_plan(args.chapter, book_dir)
    
    # 输出
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    elif args.print:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        # 打印摘要
        print(f"\n=== Chapter {args.chapter} Plan ===")
        print(f"Book: {plan['book']}")
        print(f"Scenes: {len(plan['planning']['scenes'])}")
        print(f"Word target: {plan['planning']['word_count_target']}")
        print(f"\nScenes:")
        for scene in plan['planning']['scenes']:
            print(f"  {scene['id']}. {scene['title']} ({scene['word_count_estimate']}字)")
        print(f"\nKey events: {len(plan['planning']['key_events'])}")
        print(f"\nPacing: {plan['planning']['pacing']['opening']} → {plan['planning']['pacing']['climax']} → {plan['planning']['pacing']['ending']}")
    
    # 保存到文件
    output_dir = Path(args.output) if args.output else book_dir / 'plans'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / f'chapter_{args.chapter:03d}_plan.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    
    print(f"\n[OK] Plan saved to: {output_file}")
    
    return plan


if __name__ == '__main__':
    main()
