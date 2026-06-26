#!/usr/bin/env python3
"""
谁是卧底 — 核心游戏引擎

数据存储：SQLite 数据库（who_is_undercover/games.db）

用法：
  python scripts/game_engine.py init
      初始化数据库

  python scripts/game_engine.py create <word_pairs_file> <player1> <player2> ... [--white-board]
      创建新游戏，分配角色，返回 JSON

  python scripts/game_engine.py status [--game-id <id>]
      查看游戏状态（默认当前进行中的游戏）

  python scripts/game_engine.py switch-phase <game_id> <new_phase>
      切换游戏阶段

  python scripts/game_engine.py eliminate <game_id> <player_name> <round_num> <reason>
      淘汰玩家并检查胜负条件

  python scripts/game_engine.py end-game <game_id> <winner> <review>
      结束游戏，写入最终结果

  python scripts/game_engine.py export <game_id>
      导出游戏记录为 Markdown（用于发送到群里回顾）

  python scripts/game_engine.py history
      查看历史游戏列表

  python scripts/game_engine.py template <template_name> [args...]
      生成法官话术模板
"""

import sys
import os
import json
import random
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import db


def get_role_config(num_players, white_board=False):
    """根据玩家人数计算角色分配"""
    if num_players <= 5:
        undercover = 1
        wb = 0
    elif num_players <= 8:
        undercover = 1
        wb = 1 if white_board else 0
    elif num_players <= 12:
        undercover = 2
        wb = 1 if white_board else 0
    else:
        undercover = 3
        wb = 1 if white_board else 0
    civilian = num_players - undercover - wb
    return {"civilian": civilian, "undercover": undercover, "white_board": wb}


def select_word_pair(word_pairs_file):
    """从词语对文件中随机选择一对词语"""
    with open(word_pairs_file, "r", encoding="utf-8") as f:
        content = f.read()

    pairs = []
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("- ") and "|" in line:
            parts = line[2:].split("|")
            if len(parts) == 2:
                pairs.append((parts[0].strip(), parts[1].strip()))

    if not pairs:
        print("❌ 错误：词语对文件中没有找到有效的词语对", file=sys.stderr)
        sys.exit(1)

    pair = random.choice(pairs)
    if random.random() < 0.5:
        return {"civilian_word": pair[0], "undercover_word": pair[1]}
    else:
        return {"civilian_word": pair[1], "undercover_word": pair[0]}


def assign_roles(players, config):
    """随机分配角色"""
    roles = (
        ["平民"] * config["civilian"]
        + ["卧底"] * config["undercover"]
        + ["白板"] * config["white_board"]
    )
    random.shuffle(roles)
    return [{"player": players[i], "role": roles[i]} for i in range(len(players))]


# ─────────────────────── 命令实现 ───────────────────────

def cmd_init():
    """初始化数据库"""
    db_path = db.init_db()
    return f"✅ 数据库已就绪：{db_path}"


def cmd_create(word_pairs_file, players, white_board=False):
    """创建新游戏"""
    if len(players) < 4:
        return {"error": "至少需要 4 名玩家"}

    # 确保数据库已初始化
    db.init_db()

    # 检查是否有进行中的游戏
    current = db.get_current_game()
    if current:
        return {"error": f"已有进行中的游戏（{current['game_id']}），请先结束当前游戏。"}

    # 角色分配
    config = get_role_config(len(players), white_board)

    # 选词
    words = select_word_pair(word_pairs_file)

    # 分配角色
    assignments = assign_roles(players, config)

    # 构建玩家角色列表（含词语）
    players_with_roles = []
    for a in assignments:
        word = None
        if a["role"] == "平民":
            word = words["civilian_word"]
        elif a["role"] == "卧底":
            word = words["undercover_word"]
        # 白板的 word 为 None
        players_with_roles.append({
            "name": a["player"],
            "role": a["role"],
            "word": word,
            "player_id": None,  # 报名阶段由法官通过 bind-id 命令绑定
        })

    # 描述顺序：随机打乱
    desc_order = list(players)
    random.shuffle(desc_order)

    # 生成游戏 ID
    now = datetime.now()
    random_id = random.randint(1000, 9999)
    game_id = f"game_{now.strftime('%Y%m%d_%H%M%S')}_{random_id}"

    # 写入数据库
    db.create_game(
        game_id, config,
        words["civilian_word"], words["undercover_word"],
        players_with_roles, desc_order
    )

    # 输出结果
    return {
        "game_id": game_id,
        "config": config,
        "words": words,
        "assignments": [{"player": a["name"], "role": a["role"]} for a in players_with_roles],
        "description_order": desc_order,
    }


def cmd_status(game_id=None):
    """查看游戏状态"""
    if game_id is None:
        current = db.get_current_game()
        if not current:
            return {"error": "没有进行中的游戏"}
        game_id = current["game_id"]

    status = db.get_game_status(game_id)
    if not status:
        return {"error": f"找不到游戏：{game_id}"}

    return status


def cmd_switch_phase(game_id, new_phase):
    """切换游戏阶段"""
    db.switch_phase(game_id, new_phase)
    return f"✅ 阶段已切换为：{new_phase}"


def cmd_eliminate(game_id, player_name, round_num, reason):
    """淘汰玩家"""
    # 淘汰
    db.eliminate_player(game_id, player_name, int(round_num), reason)

    # 检查胜负
    win_check = db.check_win_condition(game_id)

    # 获取最新状态
    status = db.get_game_status(game_id)

    return {
        "eliminated": player_name,
        "round": round_num,
        "reason": reason,
        "alive_players": status["alive_players"],
        "win_check": win_check,
    }


def cmd_end_game(game_id, winner, review):
    """结束游戏"""
    db.end_game(game_id, winner, "", review)
    return f"✅ 游戏已结束，获胜方：{winner}"


def cmd_bind_id(game_id, player_name, player_id):
    """绑定玩家的消息发送者ID"""
    status = db.get_game_status(game_id)
    if not status:
        return {"error": f"找不到游戏：{game_id}"}

    if player_name not in status["all_players"]:
        return {"error": f"{player_name} 不在游戏玩家列表中"}

    # 检查该 player_id 是否已被其他玩家绑定
    existing = db.get_player_by_id(game_id, player_id)
    if existing and existing["name"] != player_name:
        return {"error": f"该ID已被 {existing['name']} 绑定，不能重复绑定"}

    db.update_player_id(game_id, player_name, player_id)
    return {
        "status": "ok",
        "player": player_name,
        "player_id": player_id,
        "message": f"已将 {player_name} 绑定到 ID: {player_id}"
    }


def cmd_verify_id(game_id, player_id):
    """通过消息发送者ID验证玩家身份"""
    result = db.get_player_by_id(game_id, player_id)
    if result:
        return {
            "verified": True,
            "player_name": result["name"],
            "is_alive": result["is_alive"],
        }
    else:
        return {
            "verified": False,
            "error": "未找到匹配的玩家，可能是非游戏参与者或未绑定ID"
        }



def cmd_export(game_id):
    """导出游戏记录为 Markdown"""
    md = db.export_game_record(game_id)
    if md is None:
        return {"error": f"找不到游戏：{game_id}"}
    return md


def cmd_history():
    """查看历史游戏列表"""
    return db.get_game_history()


def generate_template(template_name, args):
    """生成法官话术模板"""
    templates = {
        "signup": """🎮 谁是卧底 — 正在组局！

想参加的玩家请自己报名（回复"我报名"或"算我一个"）。
⚠️ 每位玩家必须自己报名，不能替他人报名！
最少需要 4 人才能开局。

📋 当前已报名：（暂无）""",

        "start": lambda: f"""🎮 谁是卧底 — 游戏开始！

本局共 {args[0]} 名玩家，其中有 {args[1]} 名卧底潜伏在你们之中{args[2]}！
请各位玩家依次点击下方折叠栏查看自己的词语，看完后务必折叠起来！""",

        "deal_word": lambda: f"""<details>
<summary>🎴 {args[0]} 请点击查看你的词语（看完请折叠）</summary>

你的词语是：**{args[1]}**

⚠️ 请记住你的词语后立即折叠此栏，不要让其他人看到！

</details>""",

        "deal_white_board": lambda: f"""<details>
<summary>🎴 {args[0]} 请点击查看你的词语（看完请折叠）</summary>

你是 **白板** 🃏 — 你没有词语。

请根据其他玩家的描述推断词语，尽量伪装成平民，不要暴露自己。

⚠️ 请记住你的身份后立即折叠此栏，不要让其他人看到！

</details>""",

        "deal_confirm": lambda: f"""📬 词语已私发完毕！

以下玩家已收到词语私信：
{args[0]}

共 {args[1]} 名玩家参与本局游戏。
如果有玩家没收到，请私聊法官，法官会单独重发。

🎮 游戏正式开始！请准备进入第1轮描述阶段。""",

        "round_start": lambda: f"""📢 第 {args[0]} 轮描述开始！
当前存活 {args[1]} 人，请按以下顺序进行描述：
{args[2]}""",

        "prompt_describe": lambda: f"""🎤 请 {args[0]} 在群里用一句话描述你的词语：
提醒：在群聊中用一句话描述你的词语，不能说出词语本身或包含的字，不能提及其他玩家的名字！
⚠️ 私聊描述无效，必须在群里公开描述！""",

        "vote_announce": lambda: f"""🗳️ 所有存活玩家已完成描述！现在立即进入投票环节。

📩 法官正在同时私聊所有存活玩家收集投票。
❌ 群聊中的投票无效！为防止跟票，只接受私聊投票。
⚠️ 只有存活的玩家才能投票！已出局玩家无投票权。
规则：不能投自己，不能弃票，每人只能投一票。

⏳ 请在法官私聊中回复你的投票……""",

        "vote_dm": lambda: f"""🎮 【谁是卧底】第 {args[1]} 轮投票
━━━━━━━━━━━━━━━━━━━━
📋 游戏编号：{args[3] if len(args) > 3 else '（请提供game_id）'}
🔄 当前轮次：第 {args[1]} 轮
━━━━━━━━━━━━━━━━━━━━

🗳️ {args[0]}，请投票选择你要淘汰的玩家。

当前存活玩家：{args[2]}

规则提醒：
- ❌ 不能投自己
- ❌ 不能弃票
- ❌ 不能投已出局的玩家
- ✅ 只能投一位存活的玩家

请直接发送你要投票的玩家名字。""",

        "vote_urge": lambda: f"""⏰ 还有 {args[0]} 位玩家尚未投票：{args[1]}
法官已私聊所有存活玩家，请尽快在私聊中回复投票！群聊投票无效哦～""",

        "vote_final_warning": lambda: f"""⚠️ 最后警告：{args[0]} 再不投票将被判定超时出局！
请立即在法官私聊中回复投票！""",

        "game_over": lambda: f"""🏆 游戏结束！

🎯 获胜方：{args[0]}

📋 全员身份揭晓：
{args[1]}

🔑 本局词语：
- 平民词：「{args[2]}」
- 卧底词：「{args[3]}」""",

        "game_continue": lambda: f"""🔄 游戏继续！

👥 当前存活玩家（共 {args[0]} 人）：
{args[1]}

☠️ 已出局玩家：{args[2]}

⚠️ 场上仍有卧底潜伏！请大家提高警惕！

📢 第 {args[3]} 轮描述即将开始，请按以下顺序进行描述：
{args[4]}""",

        "elimination": lambda: f"""❌ {args[0]} 以 {args[1]} 票被投票淘汰出局！
🔒 身份暂不公开，游戏结束后统一揭晓。
⚠️ {args[0]}，请不要透露你的身份和词语！
{args[0]}，有什么临终遗言吗？（不能透露身份和词语，选填）""",

        "describe_timeout_warning": lambda: f"""⚠️ 最后警告：{args[0]}，请立即在群里进行描述！
再不描述将被判定超时出局！""",

        "describe_timeout_out": lambda: f"""⏰ {args[0]} 长时间未进行描述，判定超时出局！
🔒 身份暂不公开，游戏结束后统一揭晓。

法官正在判定游戏是否继续……""",

        "vote_timeout_out": lambda: f"""⏰ {args[0]} 长时间未投票，判定超时出局！
🔒 身份暂不公开，游戏结束后统一揭晓。
该玩家的投票视为弃权，不计入投票结果。

法官正在判定游戏是否继续……""",

        "leak_warning": lambda: f"""🚫 {args[0]}，请不要泄露你的身份和词语！
游戏尚未结束，泄露信息会严重影响其他玩家的判断。
所有身份将在游戏结束后统一揭晓，请遵守规则！""",

        "boom_word": lambda: f"""💥 爆词警告！{args[0]} 直接说出了词语，判定自爆出局！

⚠️ 爆词惩罚：{args[0]} 需要接受线下惩罚！
请其他玩家商定惩罚方式（如：表演节目、做俯卧撑、唱歌等）。

游戏继续……""",
    }

    if template_name not in templates:
        return {"error": f"未知模板：{template_name}", "available": list(templates.keys())}

    t = templates[template_name]
    if callable(t):
        return t()
    else:
        return t


# ─────────────────────── 主入口 ───────────────────────

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

    if command == "init":
        _output(cmd_init())

    elif command == "create":
        if len(sys.argv) < 4:
            print(
                "用法：python game_engine.py create <word_pairs_file> <player1> <player2> ... [--white-board]",
                file=sys.stderr,
            )
            sys.exit(1)
        word_pairs_file = sys.argv[2]
        white_board = "--white-board" in sys.argv
        players = [p for p in sys.argv[3:] if p != "--white-board"]
        _output(cmd_create(word_pairs_file, players, white_board))

    elif command == "status":
        game_id = None
        if "--game-id" in sys.argv:
            idx = sys.argv.index("--game-id")
            if idx + 1 < len(sys.argv):
                game_id = sys.argv[idx + 1]
        _output(cmd_status(game_id))

    elif command == "switch-phase":
        if len(sys.argv) < 4:
            print(
                "用法：python game_engine.py switch-phase <game_id> <new_phase>",
                file=sys.stderr,
            )
            sys.exit(1)
        _output(cmd_switch_phase(sys.argv[2], sys.argv[3]))

    elif command == "eliminate":
        if len(sys.argv) < 6:
            print(
                "用法：python game_engine.py eliminate <game_id> <player_name> <round_num> <reason>",
                file=sys.stderr,
            )
            sys.exit(1)
        _output(cmd_eliminate(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]))

    elif command == "end-game":
        if len(sys.argv) < 5:
            print(
                "用法：python game_engine.py end-game <game_id> <winner> <review>",
                file=sys.stderr,
            )
            sys.exit(1)
        _output(cmd_end_game(sys.argv[2], sys.argv[3], sys.argv[4]))

    elif command == "export":
        if len(sys.argv) < 3:
            print("用法：python game_engine.py export <game_id>", file=sys.stderr)
            sys.exit(1)
        _output(cmd_export(sys.argv[2]))

    elif command == "history":
        _output(cmd_history())

    elif command == "bind-id":
        if len(sys.argv) < 5:
            print(
                "用法：python game_engine.py bind-id <game_id> <player_name> <player_id>",
                file=sys.stderr,
            )
            sys.exit(1)
        _output(cmd_bind_id(sys.argv[2], sys.argv[3], sys.argv[4]))

    elif command == "verify-id":
        if len(sys.argv) < 4:
            print(
                "用法：python game_engine.py verify-id <game_id> <player_id>",
                file=sys.stderr,
            )
            sys.exit(1)
        _output(cmd_verify_id(sys.argv[2], sys.argv[3]))

    elif command == "template":
        if len(sys.argv) < 3:
            print(
                "用法：python game_engine.py template <template_name> [args...]",
                file=sys.stderr,
            )
            sys.exit(1)
        _output(generate_template(sys.argv[2], sys.argv[3:]))

    else:
        print(f"❌ 未知命令：{command}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
