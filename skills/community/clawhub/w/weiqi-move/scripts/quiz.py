#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
围棋实战选点 - 主脚本

功能：
1. 解析SGF棋谱
2. 检测棋谱格式（野狐/KataGo/星阵）
3. 提取选点题
4. 生成做题网页

使用示例：
    python3 quiz.py game.sgf
    python3 quiz.py game.sgf -o output.html
    python3 quiz.py game.sgf -t blunder --phase middle
"""

import argparse
import json
import os
import random
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 导入SGF解析器
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sgf_parser import parse_sgf, coord_to_pos


# ==================== 格式适配器 ====================

class FormatAdapter:
    """格式适配器基类"""
    
    def detect(self, sgf_content: str) -> bool:
        """检测是否匹配此格式"""
        return False
    
    def parse_winrate(self, comment: str) -> Optional[Dict]:
        """解析胜率信息
        Returns: {'color': 'B'/'W', 'rate': float, 'text': str} 或 None
        """
        return None
    
    def get_name(self) -> str:
        return 'default'


class FoxWQAdapter(FormatAdapter):
    """野狐围棋适配器"""
    
    PATTERNS = ['胜率', '绝艺', '黑.*?%', '白.*?%']
    WINRATE_PATTERN = re.compile(r'([黑白]).*?(\d+\.?\d*)%')
    
    def detect(self, sgf_content: str) -> bool:
        for pattern in self.PATTERNS:
            if re.search(pattern, sgf_content):
                return True
        return False
    
    def parse_winrate(self, comment: str) -> Optional[Dict]:
        match = self.WINRATE_PATTERN.search(comment)
        if match:
            color_cn = match.group(1)
            color = 'B' if color_cn == '黑' else 'W'
            rate = float(match.group(2))
            return {'color': color, 'rate': rate, 'text': f"{color_cn}{rate}%"}
        return None
    
    def get_name(self) -> str:
        return 'foxwq'


class KataGoAdapter(FormatAdapter):
    """KataGo适配器"""
    
    PATTERNS = ['KataGo', 'winrate', r'B \d+', r'W \d+']
    WINRATE_PATTERN = re.compile(r'([BW])\s+(\d+\.?\d*)%')
    
    def detect(self, sgf_content: str) -> bool:
        for pattern in self.PATTERNS:
            if re.search(pattern, sgf_content):
                return True
        return False
    
    def parse_winrate(self, comment: str) -> Optional[Dict]:
        match = self.WINRATE_PATTERN.search(comment)
        if match:
            color = match.group(1)
            rate = float(match.group(2))
            return {'color': color, 'rate': rate, 'text': f"{color} {rate}%"}
        return None
    
    def get_name(self) -> str:
        return 'katago'


class XingZhenAdapter(FormatAdapter):
    """星阵适配器"""
    
    PATTERNS = ['星阵', '推荐', '胜率']
    WINRATE_PATTERN = re.compile(r'胜率[:\s]*([黑白])\s*(\d+\.?\d*)%')
    
    def detect(self, sgf_content: str) -> bool:
        for pattern in self.PATTERNS:
            if re.search(pattern, sgf_content):
                return True
        return False
    
    def parse_winrate(self, comment: str) -> Optional[Dict]:
        match = self.WINRATE_PATTERN.search(comment)
        if match:
            color_cn = match.group(1)
            color = 'B' if color_cn == '黑' else 'W'
            rate = float(match.group(2))
            return {'color': color, 'rate': rate, 'text': f"{color_cn}{rate}%"}
        return None
    
    def get_name(self) -> str:
        return 'xingzhen'


# 格式适配器注册表
FORMAT_ADAPTERS = [
    FoxWQAdapter(),
    KataGoAdapter(),
    XingZhenAdapter(),
]


def detect_format(sgf_content: str) -> str:
    """检测棋谱格式"""
    for adapter in FORMAT_ADAPTERS:
        if adapter.detect(sgf_content):
            return adapter.get_name()
    return 'default'


def get_adapter(format_type: str) -> FormatAdapter:
    """获取指定格式的适配器"""
    for adapter in FORMAT_ADAPTERS:
        if adapter.get_name() == format_type:
            return adapter
    return FormatAdapter()


# ==================== 题目提取 ====================

class Problem:
    """单个选点题"""
    
    def __init__(self, move_num: int, position: List[Dict], variations: List[Dict], main_moves: List[Dict] = None):
        self.move_num = move_num  # 题目标记的手数
        self.position = position  # 题目前的历史局面着法
        self.variations = variations  # 变化图（选项）
        self.main_moves = main_moves  # 主分支所有着法
        self.practical_move = self._get_practical_move(main_moves, move_num)  # 实战落子
        self.phase = self._classify_phase(move_num)
        self.difficulty = self._classify_difficulty(variations)
        self.is_blunder = self._check_blunder(variations, main_moves, move_num)
    
    def _get_practical_move(self, main_moves: List[Dict], move_num: int) -> Optional[Dict]:
        """获取实战落子信息"""
        if not main_moves or move_num >= len(main_moves):
            return None
        return main_moves[move_num]
    
    def _classify_phase(self, move_num: int) -> str:
        """分类题目阶段"""
        if move_num <= 60:
            return 'layout'  # 布局
        elif move_num <= 180:
            return 'middle'  # 中盘
        else:
            return 'endgame'  # 官子
    
    def _classify_difficulty(self, variations: List[Dict]) -> str:
        """分类难度"""
        if len(variations) < 2:
            return 'easy'
        
        rates = []
        for v in variations:
            rate_info = self._parse_var_winrate(v)
            if rate_info:
                rates.append(rate_info['rate'])
        
        if len(rates) < 2:
            return 'easy'
        
        rates.sort(reverse=True)
        diff = rates[0] - rates[1]
        
        if diff > 15:
            return 'easy'
        elif diff > 5:
            return 'medium'
        else:
            return 'hard'
    
    def _check_blunder(self, variations: List[Dict], main_moves: List[Dict] = None, move_num: int = None) -> bool:
        """检查是否为恶手题
        
        正确逻辑：实战落子对应的AI变化胜率比最高胜率差20%以上，才是恶手题
        """
        if len(variations) < 2:
            return False
        
        # 获取实战落子坐标
        if not main_moves or move_num is None or move_num >= len(main_moves):
            return False
        
        practical_move = main_moves[move_num]
        practical_coord = practical_move.get('coord', '')
        
        if not practical_coord:
            return False
        
        # 在变化图中找到实战落子对应的变化
        practical_variation = None
        practical_rate = None
        max_rate = 0
        
        for v in variations:
            rate_info = self._parse_var_winrate(v)
            if not rate_info:
                continue
            
            rate = rate_info['rate']
            max_rate = max(max_rate, rate)
            
            # 检查这个变化的第一步是否等于实战落子
            if v.get('moves') and len(v['moves']) > 0:
                first_move = v['moves'][0]
                if first_move.get('coord') == practical_coord:
                    practical_variation = v
                    practical_rate = rate
        
        # 如果没找到实战落子对应的变化，或者实战落子就是最高胜率的选择，不是恶手题
        if practical_rate is None:
            return False
        
        # 实战落子胜率比最高胜率差20%以上，才是恶手题
        return (max_rate - practical_rate) > 20
    
    def _parse_var_winrate(self, variation: Dict) -> Optional[Dict]:
        """解析变化的胜率"""
        comment = variation.get('comment', '')
        # 尝试各种格式
        patterns = [
            r'([黑白]).*?(\d+\.?\d*)%',
            r'([BW])\s+(\d+\.?\d*)%',
            r'胜率[:\s]*([黑白])\s*(\d+\.?\d*)%',
        ]
        for pattern in patterns:
            match = re.search(pattern, comment)
            if match:
                color_str = match.group(1)
                rate = float(match.group(2))
                color = 'B' if color_str in ['黑', 'B'] else 'W'
                return {'color': color, 'rate': rate}
        return None


def deduplicate_variations(variations: List[Dict], format_type: str) -> List[Dict]:
    """变化去重 - 第一步相同的变化只保留胜率最高的"""
    seen = {}
    adapter = get_adapter(format_type)
    
    for var in variations:
        if not var.get('moves'):
            continue
        
        first_coord = var['moves'][0]['coord']
        
        # 解析胜率
        rate = 0
        comment = var.get('comment', '')
        winrate_info = adapter.parse_winrate(comment)
        if winrate_info:
            rate = winrate_info['rate']
        else:
            # 尝试通用解析
            match = re.search(r'(\d+\.?\d*)%', comment)
            if match:
                rate = float(match.group(1))
        
        if first_coord not in seen or rate > seen[first_coord]['rate']:
            seen[first_coord] = {
                'variation': var,
                'rate': rate
            }
    
    return [v['variation'] for v in seen.values()]


def extract_problems(moves: List[Dict], variations: Dict, format_type: str = 'default',
                     problem_type: Optional[str] = None, phase: Optional[str] = None,
                     max_problems: int = 5) -> List[Problem]:
    """
    提取选点题
    
    Args:
        moves: 主分支着法
        variations: 变化图字典 {move_num: [variations]}
        format_type: 棋谱格式
        problem_type: 题目类型筛选 (blunder/easy/medium/hard)
        phase: 阶段筛选 (layout/middle/endgame)
    
    Returns:
        Problem对象列表
    """
    problems = []
    
    for move_num, vars_at_move in variations.items():
        if len(vars_at_move) < 2:
            continue  # 至少需要两个选项
        
        # 去重
        deduped = deduplicate_variations(vars_at_move, format_type)
        if len(deduped) < 2:
            continue
        
        # 截取历史局面
        position = moves[:move_num]
        
        problem = Problem(move_num, position, deduped, moves)
        
        # 应用筛选
        if problem_type:
            if problem_type == 'blunder' and not problem.is_blunder:
                continue
            elif problem_type in ['easy', 'medium', 'hard'] and problem.difficulty != problem_type:
                continue
        
        if phase and problem.phase != phase:
            continue
        
        problems.append(problem)
    
    # 恶手题优先，然后按手数排序
    problems.sort(key=lambda p: (not p.is_blunder, p.move_num))
    
    # 限制题目数量
    if max_problems and len(problems) > max_problems:
        problems = problems[:max_problems]
    
    return problems


# ==================== HTML生成 ====================

def generate_quiz_html(problems: List[Problem], game_info: Dict, sgf_content: str,
                       output_path: Optional[str] = None) -> str:
    """生成做题网页"""
    
    if not problems:
        print("警告: 没有提取到选点题")
        return ""
    
    # 读取模板
    template_path = Path(__file__).parent.parent / 'templates' / 'quiz.html'
    if not template_path.exists():
        print(f"错误: 模板文件不存在 {template_path}")
        return ""
    
    template = template_path.read_text(encoding='utf-8')
    
    # 准备题目数据
    problems_data = []
    for i, p in enumerate(problems):
        # 为每个变化分配选项字母
        options = []
        letters = ['A', 'B', 'C', 'D', 'E', 'F']
        
        # 按胜率排序，最高的为正确答案
        sorted_vars = sorted(p.variations, 
                           key=lambda v: _extract_rate(v.get('comment', '')), 
                           reverse=True)
        
        for j, var in enumerate(sorted_vars[:6]):  # 最多6个选项
            first_move = var['moves'][0] if var.get('moves') else None
            
            # 提取胜率显示文本
            comment = var.get('comment', '')
            winrate_val = _extract_rate(comment)
            winrate_text = f"{winrate_val:.1f}%" if winrate_val > 0 else ""
            
            options.append({
                'coord': first_move['coord'] if first_move else '',
                'color': first_move['color'] if first_move else 'B',
                'winrate': winrate_text,
                'comment': comment,
                'moves': var.get('moves', []),
                'is_correct': j == 0,  # 胜率最高的是正确答案
                'sort_order': j  # 保存原始排序用于去重等逻辑
            })
        
        # 随机打乱选项顺序，使正确答案位置不固定
        # 使用基于题目内容的确定性种子，确保相同数据生成相同结果
        shuffle_seed = p.move_num + sum(ord(c) for c in (options[0]['coord'] if options else 'A'))
        rng = random.Random(shuffle_seed)
        rng.shuffle(options)
        
        # 重新分配字母标签
        for j, opt in enumerate(options):
            opt['letter'] = letters[j] if j < len(letters) else f"{j+1}"
        
        # 构建实战落子信息
        practical_move_data = None
        if p.practical_move:
            # 查找实战落子在变化图中的胜率
            practical_coord = p.practical_move.get('coord', '')
            practical_color = p.practical_move.get('color', 'B')
            practical_winrate = 0
            practical_moves = []
            
            # 从主分支moves获取实战变化的后续着法（10-15手）
            if p.main_moves and p.move_num < len(p.main_moves):
                # 获取从当前手开始的后续着法，最多15手
                follow_up_moves = p.main_moves[p.move_num:p.move_num + 15]
                practical_moves = [
                    {'color': m.get('color', 'B'), 'coord': m.get('coord', '')}
                    for m in follow_up_moves if m.get('coord')
                ]
            
            # 如果在主分支没有找到，回退到从变化图中查找
            if not practical_moves:
                for v in p.variations:
                    if v.get('moves') and len(v['moves']) > 0:
                        first_move = v['moves'][0]
                        if first_move.get('coord') == practical_coord:
                            # 解析胜率
                            comment = v.get('comment', '')
                            practical_winrate = _extract_rate(comment)
                            practical_moves = v.get('moves', [])
                            break
            
            # 计算是否是恶手（胜率比最高差20%以上）
            max_rate = max([_extract_rate(opt.get('comment', '')) for opt in p.variations]) if p.variations else 0
            is_practical_blunder = (max_rate - practical_winrate) > 20 if practical_winrate > 0 else False
            
            practical_move_data = {
                'coord': practical_coord,
                'color': practical_color,
                'winrate': f"{practical_winrate:.1f}%" if practical_winrate > 0 else "N/A",
                'is_blunder': is_practical_blunder,
                'moves': practical_moves
            }
        
        problems_data.append({
            'index': i,
            'move_num': p.move_num,
            'phase': p.phase,
            'difficulty': p.difficulty,
            'is_blunder': p.is_blunder,
            'position': p.position,
            'options': options,
            'practical_move': practical_move_data
        })
    
    # 准备模板变量
    board_size = int(game_info.get('board_size', 19))
    handicap_stones = game_info.get('handicap_stones', [])
    
    # 标题优先使用比赛名称(GN)，如果没有则使用棋手对局
    game_name = game_info.get('game_name', '').strip()
    if not game_name or game_name == '围棋棋谱':
        game_title = f"{game_info.get('black', '黑棋')} vs {game_info.get('white', '白棋')}"
    else:
        game_title = game_name
    
    # 副标题显示棋手和结果信息
    players = f"{game_info.get('black', '黑棋')} vs {game_info.get('white', '白棋')}"
    date_result = f"{game_info.get('date', '')} {game_info.get('result', '')}".strip()
    
    template_vars = {
        'GAME_NAME': game_title,
        'GAME_TITLE': game_title,
        'GAME_INFO': f"{players} {date_result}".strip(),
        'BLACK_NAME': game_info.get('black', '黑棋'),
        'WHITE_NAME': game_info.get('white', '白棋'),
        'BOARD_SIZE': board_size,
        'HANDICAP_STONES': json.dumps(handicap_stones),
        'HANDICAP_COUNT': len(handicap_stones),
        'PROBLEMS_JSON': json.dumps(problems_data, ensure_ascii=False),
        'SGF_DATA': sgf_content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$'),
        'TOTAL_PROBLEMS': len(problems_data),
    }
    
    # 替换模板变量
    html = template
    for key, value in template_vars.items():
        placeholder = '{{' + key + '}}'
        html = html.replace(placeholder, str(value))
    
    # 写入文件
    if output_path:
        output_path = Path(output_path)
        output_path.write_text(html, encoding='utf-8')
        print(f"已生成做题网页: {output_path.absolute()}")
    
    return html


def _extract_rate(comment: str) -> float:
    """从注释中提取胜率数值"""
    if not comment:
        return 0
    # 优先匹配 "黑xx%" 或 "白xx%" 格式（野狐格式）
    match = re.search(r'[黑白].*?(\d+\.?\d*)%', comment)
    if match:
        return float(match.group(1))
    # 匹配 "B xx%" 或 "W xx%" 格式（KataGo格式）
    match = re.search(r'[BW]\s+(\d+\.?\d*)%', comment)
    if match:
        return float(match.group(1))
    # 通用匹配
    match = re.search(r'(\d+\.?\d*)%', comment)
    if match:
        return float(match.group(1))
    return 0


# ==================== 命令行入口 ====================

def main():
    parser = argparse.ArgumentParser(
        description='围棋实战选点 - 从SGF棋谱中提取选点题，生成交互式做题网页',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 quiz.py game.sgf                    # 生成全部选点题
  python3 quiz.py game.sgf -o quiz.html       # 指定输出文件
  python3 quiz.py game.sgf -t blunder         # 只生成恶手题
  python3 quiz.py game.sgf --phase middle     # 只生成中盘题
  python3 quiz.py game.sgf -t easy --phase layout  # 布局阶段的简单题
  python3 quiz.py game.sgf -n 10              # 生成10道题（默认5道）
        """
    )
    
    parser.add_argument('sgf', help='输入SGF文件路径')
    parser.add_argument('-o', '--output', help='输出HTML文件路径（默认: 输入文件名.html）')
    parser.add_argument('-t', '--type',
                       choices=['blunder', 'easy', 'medium', 'hard'],
                       help='题目类型筛选')
    parser.add_argument('--phase',
                       choices=['layout', 'middle', 'endgame'],
                       help='阶段筛选（布局/中盘/官子）')
    parser.add_argument('-n', '--number', type=int, default=5,
                       help='最大题目数量（默认: 5，恶手题优先）')
    
    args = parser.parse_args()
    
    # 读取SGF文件
    sgf_path = Path(args.sgf)
    if not sgf_path.exists():
        print(f"错误: 文件不存在 {sgf_path}")
        sys.exit(1)
    
    sgf_content = sgf_path.read_text(encoding='utf-8')
    
    # 解析SGF
    print(f"正在解析: {sgf_path}")
    moves, variations, game_info, parse_info = parse_sgf(sgf_content)
    
    if parse_info.get('errors'):
        print(f"解析警告: {parse_info['errors']}")
    
    print(f"棋局: {game_info.get('black', '黑棋')} vs {game_info.get('white', '白棋')}")
    print(f"结果: {game_info.get('result', '')}")
    print(f"主分支手数: {len(moves)}")
    print(f"变化图数量: {sum(len(v) for v in variations.values())}")
    
    # 检测格式
    format_type = detect_format(sgf_content)
    adapter = get_adapter(format_type)
    print(f"检测到的格式: {format_type}")
    
    # 提取题目
    print("\n正在提取选点题...")
    problems = extract_problems(moves, variations, format_type, args.type, args.phase, args.number)
    print(f"提取到 {len(problems)} 道题目")
    
    if not problems:
        print("未找到符合条件的选点题，请检查棋谱是否包含AI分析数据")
        sys.exit(0)
    
    # 统计信息
    phase_counts = {'layout': 0, 'middle': 0, 'endgame': 0}
    difficulty_counts = {'easy': 0, 'medium': 0, 'hard': 0}
    blunder_count = 0
    
    for p in problems:
        phase_counts[p.phase] = phase_counts.get(p.phase, 0) + 1
        difficulty_counts[p.difficulty] = difficulty_counts.get(p.difficulty, 0) + 1
        if p.is_blunder:
            blunder_count += 1
    
    print(f"  - 布局: {phase_counts['layout']}, 中盘: {phase_counts['middle']}, 官子: {phase_counts['endgame']}")
    print(f"  - 简单: {difficulty_counts['easy']}, 中等: {difficulty_counts['medium']}, 困难: {difficulty_counts['hard']}")
    print(f"  - 恶手题: {blunder_count}")
    
    # 确定输出路径
    if args.output:
        output_path = args.output
    else:
        output_path = sgf_path.with_suffix('.html')
    
    # 生成HTML
    print(f"\n正在生成做题网页...")
    generate_quiz_html(problems, game_info, sgf_content, output_path)


if __name__ == '__main__':
    main()
