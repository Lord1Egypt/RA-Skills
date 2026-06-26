#!/usr/bin/env python3
"""
谁是卧底 — 描述阶段处理器

数据存储：SQLite 数据库（who_is_undercover/games.db）

用法：
  python scripts/describe_handler.py record <game_id> <player> <description> <round_num>
      记录玩家描述

  python scripts/describe_handler.py progress <game_id> <round_num>
      查看描述进度

  python scripts/describe_handler.py new-round <game_id> <round_num>
      为新一轮创建描述和投票表格
"""

import sys
import os
import json
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db


def cmd_record(game_id, player, description, round_num):
    """记录玩家描述"""
    round_num = int(round_num)

    # 验证阶段
    status = db.get_game_status(game_id)
    if not status:
        return {"valid": False, "error": "找不到游戏"}

    phase = status["phase"]
    if "描述阶段" not in phase:
        return {"valid": False, "error": f"当前不在描述阶段（当前阶段：{phase}），无法记录描述。"}

    # 验证玩家存活
    if player not in status["alive_players"]:
        return {"valid": False, "error": f"{player} 不在存活玩家列表中。"}

    # 检查是否已描述
    if db.has_described(game_id, round_num, player):
        return {"valid": False, "error": f"{player} 本轮已经描述过了。"}

    # 写入
    db.record_description(game_id, round_num, player, description)

    # 查询进度
    progress = db.get_description_progress(game_id, round_num)

    return {
        "valid": True,
        "player": player,
        "description": description,
        "progress": f"{progress['described_count']}/{progress['total']}",
        "all_described": progress["all_described"],
        "not_described": progress["not_described_players"],
        "next_player": progress["next_player"],
    }


def cmd_progress(game_id, round_num):
    """查看描述进度"""
    round_num = int(round_num)
    return db.get_description_progress(game_id, round_num)


def cmd_new_round(game_id, round_num):
    """为新一轮创建描述和投票表格"""
    round_num = int(round_num)

    status = db.get_game_status(game_id)
    if not status:
        return {"error": "找不到游戏"}

    alive = status["alive_players"]
    if not alive:
        return {"error": "没有存活玩家"}

    # 随机打乱描述顺序
    desc_order = list(alive)
    random.shuffle(desc_order)

    # 创建新一轮描述记录
    db.create_new_round_descriptions(game_id, round_num, desc_order)

    return {
        "round": round_num,
        "description_order": desc_order,
        "alive_players": alive,
    }


def _output(result):
    """统一输出：字符串直接打印，其他类型序列化为 JSON"""
    if result is None:
        return
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "record":
        if len(sys.argv) < 6:
            print("用法：python describe_handler.py record <game_id> <player> <description> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_record(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))

    elif command == "progress":
        if len(sys.argv) < 4:
            print("用法：python describe_handler.py progress <game_id> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_progress(sys.argv[2], sys.argv[3]))

    elif command == "new-round":
        if len(sys.argv) < 4:
            print("用法：python describe_handler.py new-round <game_id> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_new_round(sys.argv[2], sys.argv[3]))

    else:
        print(f"❌ 未知命令：{command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
