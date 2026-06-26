#!/usr/bin/env python3
"""
谁是卧底 — 投票处理器

数据存储：SQLite 数据库（who_is_undercover/games.db）

用法：
  python scripts/vote_handler.py init <game_id> <round_num>
      初始化当轮投票表格

  python scripts/vote_handler.py cast <game_id> <voter> <target> <round_num>
      记录一票（自动验证合规性）

  python scripts/vote_handler.py progress <game_id> <round_num>
      查看投票进度

  python scripts/vote_handler.py tally <game_id> <round_num>
      统计投票结果

  python scripts/vote_handler.py announce <game_id> <round_num>
      生成投票结果公布话术

  python scripts/vote_handler.py dm-all <game_id> <round_num>
      生成所有存活玩家的投票私聊消息
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db


def cmd_init(game_id, round_num):
    """初始化当轮投票表格"""
    round_num = int(round_num)
    alive = db.init_votes(game_id, round_num)

    return {
        "status": "ok",
        "alive_players": alive,
        "total_voters": len(alive),
    }


def validate_vote(game_id, voter, target, round_num):
    """验证投票合规性"""
    status = db.get_game_status(game_id)
    if not status:
        return {"valid": False, "errors": ["找不到游戏"]}

    alive_players = status["alive_players"]
    phase = status["phase"]
    errors = []

    if "投票阶段" not in phase:
        errors.append(f"当前不在投票环节（当前阶段：{phase}），无法接受投票。")
        return {"valid": False, "errors": errors}

    if voter not in alive_players:
        errors.append(f"{voter} 已出局，无投票权。")
        return {"valid": False, "errors": errors}

    if target not in alive_players:
        errors.append(f"{target} 不在存活玩家列表中，不能投票给已出局的玩家。")

    if voter == target:
        errors.append("不能投票给自己。")

    if db.has_voted(game_id, round_num, voter):
        errors.append(f"{voter} 本轮已经投过票了。")

    if errors:
        return {"valid": False, "errors": errors}
    return {"valid": True}


def cmd_cast(game_id, voter, target, round_num):
    """记录一票，返回进度 + 群聊进度播报消息（不含投票详情）"""
    round_num = int(round_num)

    # 验证
    validation = validate_vote(game_id, voter, target, round_num)
    if not validation["valid"]:
        return validation

    # 写入
    db.cast_vote(game_id, round_num, voter, target)

    # 查询进度
    progress = db.get_vote_progress(game_id, round_num)

    voted_count = progress['voted_count']
    total = progress['total']
    voted_players = progress['voted_players']
    not_voted_players = progress['not_voted_players']

    # 生成进度条
    filled = "🟩" * voted_count
    empty = "⬜" * (total - voted_count)
    progress_bar = filled + empty

    # 生成群聊进度播报消息（仅展示谁投了/谁没投，绝不泄露投票目标）
    if progress["all_voted"]:
        group_msg = (
            f"🎮 【谁是卧底】第 {round_num} 轮投票\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ {voter} 已完成投票！\n\n"
            f"📊 投票进度：{voted_count}/{total} {progress_bar}\n\n"
            f"🎉 所有玩家已完成投票！\n"
            f"法官正在统计结果，即将公布……"
        )
    else:
        group_msg = (
            f"🎮 【谁是卧底】第 {round_num} 轮投票\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ {voter} 已完成投票！\n\n"
            f"📊 投票进度：{voted_count}/{total} {progress_bar}\n\n"
            f"✅ 已投票：{'、'.join(voted_players)}\n"
            f"⏳ 等待投票：{'、'.join(not_voted_players)}\n\n"
            f"📩 请尚未投票的玩家尽快在法官私聊中回复！"
        )

    return {
        "status": "ok",
        "game_id": game_id,
        "round_num": round_num,
        "voter": voter,
        "target": target,
        "progress": f"{voted_count}/{total}",
        "all_voted": progress["all_voted"],
        "voted_players": voted_players,
        "not_voted": not_voted_players,
        "group_progress_message": group_msg,
    }


def cmd_progress(game_id, round_num):
    """查看投票进度"""
    round_num = int(round_num)
    return db.get_vote_progress(game_id, round_num)


def cmd_tally(game_id, round_num):
    """统计投票结果"""
    round_num = int(round_num)
    result = db.tally_votes(game_id, round_num)

    if not result["is_tie"] and result["eliminated_candidates"]:
        result["eliminated"] = result["eliminated_candidates"][0]

    return result


def cmd_announce(game_id, round_num):
    """生成投票结果公布话术"""
    round_num = int(round_num)
    result = db.tally_votes(game_id, round_num)

    # 构建话术
    detail_lines = "\n".join([
        f"- {v['voter']} 👉 投给了 {v['target']}" for v in result["vote_details"]
    ])
    tally_lines = "\n".join([
        f"- {t['player']}：{t['votes']} 票（被 {'、'.join(t['voters'])} 投票）"
        for t in result["tally"]
    ])

    max_players = result["eliminated_candidates"]
    max_votes = result["max_votes"]

    if len(max_players) == 1:
        eliminated = max_players[0]
        elimination_text = f"""
❌ {eliminated} 以 {max_votes} 票被投票淘汰出局！
🔒 身份暂不公开，游戏结束后统一揭晓。
⚠️ {eliminated}，请不要透露你的身份和词语！
{eliminated}，有什么临终遗言吗？（不能透露身份和词语，选填）"""
    else:
        elimination_text = f"""
⚖️ 出现平票！{'、'.join(max_players)} 各获得 {max_votes} 票。
请平票玩家每人再描述一句话，随后其余存活玩家进行加赛投票。"""

    voters_list = [v["voter"] for v in result["vote_details"]]
    announce = f"""📊 第 {round_num} 轮投票结果揭晓：

👥 本轮投票玩家（共 {result['total_votes']} 人）：{'、'.join(voters_list)}

🔍 投票详情（每人投了谁）：
{detail_lines}

📈 得票统计：
{tally_lines}
{elimination_text}"""

    return announce


def cmd_dm_all(game_id, round_num):
    """生成所有存活玩家的投票私聊消息（含游戏名称、game_id、投票轮次）"""
    round_num = int(round_num)
    status = db.get_game_status(game_id)
    alive = status["alive_players"]

    # 获取总人数（初始玩家数）
    total_players = len(status["all_players"])
    alive_count = len(alive)
    eliminated_count = len(status["eliminated_players"])

    messages = []
    for player in alive:
        others = [p for p in alive if p != player]
        msg = {
            "player": player,
            "game_id": game_id,
            "round_num": round_num,
            "message": (
                f"🎮 【谁是卧底】第 {round_num} 轮投票\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📋 游戏编号：{game_id}\n"
                f"🔄 当前轮次：第 {round_num} 轮\n"
                f"👥 存活/总人数：{alive_count}/{total_players}（已淘汰 {eliminated_count} 人）\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🗳️ {player}，请投票选择你要淘汰的玩家。\n\n"
                f"当前存活玩家：{'、'.join(others)}\n\n"
                f"规则提醒：\n"
                f"- ❌ 不能投自己\n"
                f"- ❌ 不能弃票\n"
                f"- ❌ 不能投已出局的玩家\n"
                f"- ✅ 只能投一位存活的玩家\n\n"
                f"请直接发送你要投票的玩家名字。"
            ),
        }
        messages.append(msg)

    return messages


def _output(result):
    """统一输出：字符串直接打印，其他类型序列化为 JSON"""
    if isinstance(result, str):
        print(result)
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "init":
        if len(sys.argv) < 4:
            print("用法：python vote_handler.py init <game_id> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_init(sys.argv[2], sys.argv[3]))

    elif command == "cast":
        if len(sys.argv) < 6:
            print("用法：python vote_handler.py cast <game_id> <voter> <target> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_cast(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))

    elif command == "progress":
        if len(sys.argv) < 4:
            print("用法：python vote_handler.py progress <game_id> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_progress(sys.argv[2], sys.argv[3]))

    elif command == "tally":
        if len(sys.argv) < 4:
            print("用法：python vote_handler.py tally <game_id> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_tally(sys.argv[2], sys.argv[3]))

    elif command == "announce":
        if len(sys.argv) < 4:
            print("用法：python vote_handler.py announce <game_id> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_announce(sys.argv[2], sys.argv[3]))

    elif command == "dm-all":
        if len(sys.argv) < 4:
            print("用法：python vote_handler.py dm-all <game_id> <round_num>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_dm_all(sys.argv[2], sys.argv[3]))

    else:
        print(f"❌ 未知命令：{command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
