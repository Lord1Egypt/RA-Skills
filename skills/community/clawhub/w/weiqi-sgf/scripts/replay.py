#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SGF围棋打谱网页生成器 - 纯本地离线工具
将野狐围棋SGF文件转换为交互式HTML打谱网页

使用方法:
    python3 replay.py input.sgf [output.html]
    python3 replay.py input.sgf --output-dir /path/to/dir

示例:
    python3 replay.py game.sgf                    # 输出到 /tmp/sgf-viewer/
    python3 replay.py game.sgf mygame.html        # 输出到 /tmp/sgf-viewer/mygame.html
"""

import sys
import os
import html
import json

# 导入 SGF 解析模块
from sgf_parser import parse_sgf


def load_template():
    """加载 HTML 模板文件"""
    template_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'templates', 'replay.html'
    )
    with open(template_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_html(tree, game_info, output_path, input_base_name='棋谱', start_move=0):
    """生成HTML打谱网页"""
    
    # 加载模板
    template = load_template()
    
    # 准备替换数据
    board_size = int(game_info.get('board_size', '19'))
    handicap = game_info.get('handicap', '0')
    handicap_stones = game_info.get('handicap_stones', [])
    
    # 各种转义处理
    black_name = html.escape(game_info.get('black', '黑棋'))
    white_name = html.escape(game_info.get('white', '白棋'))
    black_rank = html.escape(game_info.get('black_rank', ''))
    white_rank = html.escape(game_info.get('white_rank', ''))
    game_name = html.escape(game_info.get('game_name', '围棋棋谱'))
    result = html.escape(game_info.get('result', ''))
    
    # 构建游戏标题和信息
    game_title = game_name
    game_info_text = f"{black_name} vs {white_name}"
    if int(handicap) > 0:
        game_info_text += f" · 让{handicap}子"
    if result:
        game_info_text += f" · {result}"
    
    # 树形数据 JSON（用于前端分支导航）
    tree_json = html.escape(json.dumps(tree, ensure_ascii=False)).replace('\\', '&#92;')
    
    # 让子石 JSON
    handicap_stones_json = json.dumps(handicap_stones)
    
    # 执行模板替换
    html_content = template
    html_content = html_content.replace('{{GAME_NAME}}', game_name)
    html_content = html_content.replace('{{GAME_TITLE}}', game_title)
    html_content = html_content.replace('{{GAME_INFO}}', game_info_text)
    html_content = html_content.replace('{{BOARD_SIZE}}', str(board_size))
    html_content = html_content.replace('{{HANDICAP_STONES}}', handicap_stones_json)
    html_content = html_content.replace('{{HANDICAP_COUNT}}', str(handicap))
    html_content = html_content.replace('{{TREE_JSON}}', tree_json)
    html_content = html_content.replace('{{BLACK_NAME}}', black_name + (' ' + black_rank if black_rank else ''))
    html_content = html_content.replace('{{WHITE_NAME}}', white_name + (' ' + white_rank if white_rank else ''))
    html_content = html_content.replace('{{DOWNLOAD_FILENAME}}', html.escape(input_base_name) + '.sgf')
    html_content = html_content.replace('{{DEFAULT_MOVE}}', str(start_move))
    
    # 写入文件
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ 已生成打谱网页: {output_path}")
    print(f"   黑棋: {black_name}")
    print(f"   白棋: {white_name}")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 replay.py input.sgf [output.html]")
        print("       python3 replay.py input.sgf --output-dir /path/to/dir")
        print("       python3 replay.py input.sgf --start-move 50")
        print("       python3 replay.py input.sgf --start-move last")
        print("示例: python3 replay.py game.sgf")
        print("       python3 replay.py game.sgf -o /tmp/myviewer")
        print("       python3 replay.py game.sgf --start-move 100  # 默认跳转到第100手")
        print("       python3 replay.py game.sgf --start-move last # 跳转到最后一手")
        sys.exit(1)

    input_file = sys.argv[1]

    # 解析参数
    output_file = None
    output_dir = None
    start_move = 0

    i = 2
    while i < len(sys.argv):
        if sys.argv[i] in ('--output-dir', '-o'):
            if i + 1 < len(sys.argv):
                output_dir = sys.argv[i + 1]
                i += 2
            else:
                print("❌ 错误: --output-dir 需要指定目录路径")
                sys.exit(1)
        elif sys.argv[i] == '--start-move':
            if i + 1 < len(sys.argv):
                move_arg = sys.argv[i + 1]
                if move_arg.lower() == 'last':
                    start_move = -1  # 特殊标记，表示最后一手
                else:
                    try:
                        start_move = int(move_arg)
                        if start_move < 0:
                            print("❌ 错误: --start-move 必须是非负整数")
                            sys.exit(1)
                    except ValueError:
                        print("❌ 错误: --start-move 必须是整数或 'last'")
                        sys.exit(1)
                i += 2
            else:
                print("❌ 错误: --start-move 需要指定手数")
                sys.exit(1)
        elif not output_file:
            output_file = sys.argv[i]
            i += 1
        else:
            i += 1

    # 默认输出目录为 /tmp/sgf-viewer
    if output_dir is None:
        output_dir = '/tmp/sgf-viewer'

    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 确定输出文件名
    if output_file:
        if os.path.isabs(output_file):
            output_path = output_file
        else:
            output_path = os.path.join(output_dir, output_file)
    else:
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        output_path = os.path.join(output_dir, base_name + '.html')

    # 读取SGF文件
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            sgf_content = f.read()
    except FileNotFoundError:
        print(f"❌ 错误: 找不到文件 {input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: 读取文件失败 - {e}")
        sys.exit(1)

    # 解析 SGF
    print(f"📖 正在解析: {input_file}")
    result = parse_sgf(sgf_content)
    
    tree = result['tree']
    game_info = result['game_info']
    stats = result['stats']
    errors = result['errors']

    if stats['move_nodes'] == 0:
        print("❌ 错误: 无法从SGF中提取着法")
        if errors:
            print("   解析错误:")
            for err in errors:
                print(f"     - {err}")
        sys.exit(1)

    print(f"   总节点数: {stats['total_nodes']}")
    print(f"   着法节点: {stats['move_nodes']}")
    print(f"   最大深度: {stats['max_depth']}")
    print(f"   分支数: {stats['branch_count']}")

    if errors:
        print(f"   ⚠️  解析过程中遇到 {len(errors)} 个错误/警告")
        for err in errors[:5]:  # 最多显示5个
            print(f"     - {err}")

    # 获取输入文件名（不含扩展名）
    input_base_name = os.path.splitext(os.path.basename(input_file))[0]

    # 生成HTML
    generate_html(tree, game_info, output_path, input_base_name, start_move)
    
    if start_move > 0:
        print(f"   默认跳转: 第 {start_move} 手")
    elif start_move == -1:
        print(f"   默认跳转: 最后一手")

    print(f"\n✅ 生成完成: {output_path}")


if __name__ == '__main__':
    main()
