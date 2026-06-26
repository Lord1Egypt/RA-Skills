#!/usr/bin/env python3
"""
谁是卧底 — SQLite 数据库管理模块

提供游戏数据的结构化存储，替代之前的 Markdown 文件正则解析方式。
所有游戏状态、角色分配、描述记录、投票记录均存储在 SQLite 数据库中。

数据库文件：who_is_undercover/games.db
"""

import sqlite3
import os
import json
from datetime import datetime
from contextlib import contextmanager


# ─────────────────────── 数据库初始化 ───────────────────────

SCHEMA_SQL = """
-- 游戏主表
CREATE TABLE IF NOT EXISTS games (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id         TEXT UNIQUE NOT NULL,          -- 唯一标识（时间戳+随机数）
    created_at      TEXT NOT NULL,                 -- 创建时间 ISO 格式
    status          TEXT NOT NULL DEFAULT 'playing', -- playing / finished
    current_phase   TEXT NOT NULL DEFAULT '第1轮-描述阶段',
    current_round   INTEGER NOT NULL DEFAULT 1,
    civilian_word   TEXT NOT NULL,
    undercover_word TEXT NOT NULL,
    winner          TEXT,                          -- 游戏结束时填写
    win_reason      TEXT,
    review          TEXT,                          -- 精彩回顾
    config          TEXT NOT NULL                  -- JSON: {"civilian":3,"undercover":1,"white_board":0}
);

-- 玩家表
CREATE TABLE IF NOT EXISTS players (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id     TEXT NOT NULL REFERENCES games(game_id),
    name        TEXT NOT NULL,
    player_id   TEXT,                             -- 玩家唯一标识（消息发送者ID），用于身份验证
    role        TEXT NOT NULL,                    -- 平民 / 卧底 / 白板
    word        TEXT,                             -- 拿到的词语（白板为 NULL）
    is_alive    INTEGER NOT NULL DEFAULT 1,       -- 1=存活, 0=出局
    eliminated_round   INTEGER,                   -- 出局轮次
    eliminated_reason  TEXT,                       -- 出局原因
    UNIQUE(game_id, name)
);

-- 描述记录表
CREATE TABLE IF NOT EXISTS descriptions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id     TEXT NOT NULL REFERENCES games(game_id),
    round_num   INTEGER NOT NULL,
    player_name TEXT NOT NULL,
    description TEXT,                             -- NULL=未描述
    desc_order  INTEGER NOT NULL,                 -- 本轮描述顺序号
    created_at  TEXT,                             -- 描述时间
    UNIQUE(game_id, round_num, player_name)
);

-- 投票记录表
CREATE TABLE IF NOT EXISTS votes (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    game_id     TEXT NOT NULL REFERENCES games(game_id),
    round_num   INTEGER NOT NULL,
    voter       TEXT NOT NULL,                    -- 投票人
    target      TEXT,                             -- 投给谁（NULL=未投票）
    created_at  TEXT,                             -- 投票时间
    UNIQUE(game_id, round_num, voter)
);

-- 视图：当前进行中的游戏
CREATE VIEW IF NOT EXISTS v_current_game AS
SELECT * FROM games WHERE status = 'playing' ORDER BY id DESC LIMIT 1;

-- 视图：存活玩家
CREATE VIEW IF NOT EXISTS v_alive_players AS
SELECT p.* FROM players p
JOIN games g ON p.game_id = g.game_id
WHERE p.is_alive = 1;
"""


def _get_skill_dir():
    """获取技能根目录（脚本所在目录的上级目录）"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_db_path(base_dir=None):
    """获取数据库文件路径（技能根目录/database/games.db）"""
    db_dir = os.path.join(_get_skill_dir(), "database")
    return os.path.join(db_dir, "games.db")


def init_db(base_dir=None):
    """初始化数据库（创建目录和表）"""
    db_dir = os.path.join(_get_skill_dir(), "database")
    os.makedirs(db_dir, exist_ok=True)
    db_path = get_db_path()

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    conn.close()

    return db_path


@contextmanager
def get_conn(base_dir=None):
    """数据库连接上下文管理器"""
    db_path = get_db_path(base_dir)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


# ─────────────────────── 游戏操作 ───────────────────────

def create_game(game_id, config, civilian_word, undercover_word, players_with_roles, desc_order, base_dir=None):
    """
    创建新游戏

    Args:
        game_id: 游戏唯一 ID
        config: dict {"civilian": N, "undercover": N, "white_board": N}
        civilian_word: 平民词
        undercover_word: 卧底词
        players_with_roles: list of dict [{"name": "张三", "role": "平民", "word": "苹果", "player_id": "可选"}, ...]
        desc_order: list of str 第一轮描述顺序
    """
    now = datetime.now().isoformat()

    with get_conn() as conn:
        # 插入游戏
        conn.execute("""
            INSERT INTO games (game_id, created_at, status, current_phase, current_round, 
                             civilian_word, undercover_word, config)
            VALUES (?, ?, 'playing', '第1轮-描述阶段', 1, ?, ?, ?)
        """, (game_id, now, civilian_word, undercover_word, json.dumps(config, ensure_ascii=False)))

        # 插入玩家
        for p in players_with_roles:
            conn.execute("""
                INSERT INTO players (game_id, name, player_id, role, word, is_alive)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (game_id, p["name"], p.get("player_id"), p["role"], p.get("word")))

        # 创建第1轮描述记录（空）
        for i, player_name in enumerate(desc_order, 1):
            conn.execute("""
                INSERT INTO descriptions (game_id, round_num, player_name, description, desc_order)
                VALUES (?, 1, ?, NULL, ?)
            """, (game_id, player_name, i))


def get_current_game(base_dir=None):
    """获取当前进行中的游戏"""
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM v_current_game").fetchone()
        if row:
            return dict(row)
        return None


def get_game_by_id(game_id, base_dir=None):
    """通过 game_id 获取游戏"""
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM games WHERE game_id = ?", (game_id,)).fetchone()
        if row:
            return dict(row)
        return None


def get_game_status(game_id, base_dir=None):
    """获取完整游戏状态（用于法官决策）"""
    with get_conn() as conn:
        game = conn.execute("SELECT * FROM games WHERE game_id = ?", (game_id,)).fetchone()
        if not game:
            return None

        game = dict(game)

        # 所有玩家
        all_players = [dict(r) for r in conn.execute(
            "SELECT * FROM players WHERE game_id = ? ORDER BY id", (game_id,)
        ).fetchall()]

        # 存活玩家
        alive_players = [p["name"] for p in all_players if p["is_alive"]]

        # 已出局玩家
        eliminated = [
            {"name": p["name"], "round": p["eliminated_round"], "reason": p["eliminated_reason"]}
            for p in all_players if not p["is_alive"]
        ]

        # 角色分配
        roles = [{"player": p["name"], "role": p["role"], "word": p["word"] or "（无词语）", "player_id": p["player_id"]} for p in all_players]

        # 玩家名→player_id 映射
        player_id_map = {p["name"]: p["player_id"] for p in all_players if p["player_id"]}

        return {
            "game_id": game["game_id"],
            "phase": game["current_phase"],
            "round": game["current_round"],
            "status": game["status"],
            "civilian_word": game["civilian_word"],
            "undercover_word": game["undercover_word"],
            "config": json.loads(game["config"]),
            "all_players": [p["name"] for p in all_players],
            "alive_players": alive_players,
            "eliminated_players": eliminated,
            "roles": roles,
            "player_id_map": player_id_map,
            "created_at": game["created_at"],
        }


def get_player_by_id(game_id, player_id, base_dir=None):
    """通过 player_id 查找玩家名（用于消息发送者身份验证）"""
    with get_conn() as conn:
        row = conn.execute(
            "SELECT name, is_alive FROM players WHERE game_id = ? AND player_id = ?",
            (game_id, player_id)
        ).fetchone()
        if row:
            return {"name": row["name"], "is_alive": bool(row["is_alive"])}
        return None


def update_player_id(game_id, player_name, player_id, base_dir=None):
    """更新玩家的 player_id（报名时绑定消息发送者ID）"""
    with get_conn() as conn:
        conn.execute(
            "UPDATE players SET player_id = ? WHERE game_id = ? AND name = ?",
            (player_id, game_id, player_name)
        )


def switch_phase(game_id, new_phase, base_dir=None):
    """切换游戏阶段"""
    import re
    round_num = None
    m = re.match(r"第(\d+)轮", new_phase)
    if m:
        round_num = int(m.group(1))

    with get_conn() as conn:
        if round_num:
            conn.execute("""
                UPDATE games SET current_phase = ?, current_round = ? WHERE game_id = ?
            """, (new_phase, round_num, game_id))
        else:
            conn.execute("""
                UPDATE games SET current_phase = ? WHERE game_id = ?
            """, (new_phase, game_id))


def eliminate_player(game_id, player_name, round_num, reason, base_dir=None):
    """淘汰玩家"""
    with get_conn() as conn:
        conn.execute("""
            UPDATE players SET is_alive = 0, eliminated_round = ?, eliminated_reason = ?
            WHERE game_id = ? AND name = ?
        """, (round_num, reason, game_id, player_name))


def check_win_condition(game_id, base_dir=None):
    """检查胜负条件"""
    with get_conn() as conn:
        alive = conn.execute("""
            SELECT name, role FROM players WHERE game_id = ? AND is_alive = 1
        """, (game_id,)).fetchall()

        alive_list = [dict(r) for r in alive]
        undercover_alive = sum(1 for p in alive_list if p["role"] == "卧底")
        civilian_alive = sum(1 for p in alive_list if p["role"] in ("平民", "白板"))
        total_alive = len(alive_list)

        if undercover_alive == 0:
            return {"game_over": True, "winner": "平民阵营 🎉", "reason": "所有卧底均已被淘汰"}
        if total_alive <= 3 and undercover_alive > 0:
            return {"game_over": True, "winner": "卧底阵营 🎭", "reason": f"存活人数仅剩{total_alive}人，卧底潜伏成功"}
        if civilian_alive == 0:
            return {"game_over": True, "winner": "卧底阵营 🎭", "reason": "平民全部被淘汰"}

        return {"game_over": False}


def end_game(game_id, winner, win_reason, review, base_dir=None):
    """结束游戏"""
    with get_conn() as conn:
        conn.execute("""
            UPDATE games SET status = 'finished', current_phase = '游戏结束',
                           winner = ?, win_reason = ?, review = ?
            WHERE game_id = ?
        """, (winner, win_reason, review, game_id))


# ─────────────────────── 描述操作 ───────────────────────

def record_description(game_id, round_num, player_name, description, base_dir=None):
    """记录玩家描述"""
    now = datetime.now().isoformat()
    with get_conn() as conn:
        conn.execute("""
            UPDATE descriptions SET description = ?, created_at = ?
            WHERE game_id = ? AND round_num = ? AND player_name = ?
        """, (description, now, game_id, round_num, player_name))


def get_description_progress(game_id, round_num, base_dir=None):
    """获取描述进度"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT player_name, description, desc_order
            FROM descriptions WHERE game_id = ? AND round_num = ?
            ORDER BY desc_order
        """, (game_id, round_num)).fetchall()

        descs = [dict(r) for r in rows]
        described = [d for d in descs if d["description"] is not None]
        not_described = [d for d in descs if d["description"] is None]

        return {
            "total": len(descs),
            "described_count": len(described),
            "described_players": [d["player_name"] for d in described],
            "not_described_count": len(not_described),
            "not_described_players": [d["player_name"] for d in not_described],
            "all_described": len(not_described) == 0,
            "next_player": not_described[0]["player_name"] if not_described else None,
            "description_order": [d["player_name"] for d in descs],
        }


def has_described(game_id, round_num, player_name, base_dir=None):
    """检查玩家是否已描述"""
    with get_conn() as conn:
        row = conn.execute("""
            SELECT description FROM descriptions
            WHERE game_id = ? AND round_num = ? AND player_name = ?
        """, (game_id, round_num, player_name)).fetchone()
        return row is not None and row["description"] is not None


def create_new_round_descriptions(game_id, round_num, desc_order, base_dir=None):
    """为新一轮创建描述记录"""
    with get_conn() as conn:
        for i, player_name in enumerate(desc_order, 1):
            conn.execute("""
                INSERT INTO descriptions (game_id, round_num, player_name, description, desc_order)
                VALUES (?, ?, ?, NULL, ?)
            """, (game_id, round_num, player_name, i))


# ─────────────────────── 投票操作 ───────────────────────

def init_votes(game_id, round_num, base_dir=None):
    """初始化当轮投票（为所有存活玩家创建投票行）"""
    with get_conn() as conn:
        alive = conn.execute("""
            SELECT name FROM players WHERE game_id = ? AND is_alive = 1 ORDER BY id
        """, (game_id,)).fetchall()

        for row in alive:
            conn.execute("""
                INSERT OR IGNORE INTO votes (game_id, round_num, voter, target)
                VALUES (?, ?, ?, NULL)
            """, (game_id, round_num, row["name"]))

        return [row["name"] for row in alive]


def cast_vote(game_id, round_num, voter, target, base_dir=None):
    """记录一票"""
    now = datetime.now().isoformat()
    with get_conn() as conn:
        conn.execute("""
            UPDATE votes SET target = ?, created_at = ?
            WHERE game_id = ? AND round_num = ? AND voter = ?
        """, (target, now, game_id, round_num, voter))


def has_voted(game_id, round_num, voter, base_dir=None):
    """检查玩家是否已投票"""
    with get_conn() as conn:
        row = conn.execute("""
            SELECT target FROM votes
            WHERE game_id = ? AND round_num = ? AND voter = ?
        """, (game_id, round_num, voter)).fetchone()
        return row is not None and row["target"] is not None


def get_vote_progress(game_id, round_num, base_dir=None):
    """获取投票进度"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT voter, target FROM votes
            WHERE game_id = ? AND round_num = ?
            ORDER BY id
        """, (game_id, round_num)).fetchall()

        votes = [dict(r) for r in rows]
        voted = [v for v in votes if v["target"] is not None]
        not_voted = [v for v in votes if v["target"] is None]

        return {
            "total": len(votes),
            "voted_count": len(voted),
            "voted_players": [v["voter"] for v in voted],
            "not_voted_count": len(not_voted),
            "not_voted_players": [v["voter"] for v in not_voted],
            "all_voted": len(not_voted) == 0,
        }


def tally_votes(game_id, round_num, base_dir=None):
    """统计投票结果"""
    from collections import Counter

    with get_conn() as conn:
        rows = conn.execute("""
            SELECT voter, target FROM votes
            WHERE game_id = ? AND round_num = ? AND target IS NOT NULL
            ORDER BY id
        """, (game_id, round_num)).fetchall()

        votes = [dict(r) for r in rows]
        vote_counter = Counter(v["target"] for v in votes)
        sorted_tally = sorted(vote_counter.items(), key=lambda x: x[1], reverse=True)

        # 投票详情：谁投了谁
        vote_details = {}
        for v in votes:
            if v["target"] not in vote_details:
                vote_details[v["target"]] = []
            vote_details[v["target"]].append(v["voter"])

        max_votes = sorted_tally[0][1] if sorted_tally else 0
        max_players = [p for p, c in sorted_tally if c == max_votes]

        return {
            "total_votes": len(votes),
            "tally": [
                {"player": p, "votes": c, "voters": vote_details.get(p, [])}
                for p, c in sorted_tally
            ],
            "vote_details": [{"voter": v["voter"], "target": v["target"]} for v in votes],
            "max_votes": max_votes,
            "eliminated_candidates": max_players,
            "is_tie": len(max_players) > 1,
        }


# ─────────────────────── 游戏历史 ───────────────────────

def get_game_history(limit=20, base_dir=None):
    """获取游戏历史列表"""
    with get_conn() as conn:
        rows = conn.execute("""
            SELECT game_id, created_at, status, winner, config
            FROM games ORDER BY id DESC LIMIT ?
        """, (limit,)).fetchall()

        history = []
        for row in rows:
            row = dict(row)
            # 获取玩家名
            players = conn.execute(
                "SELECT name FROM players WHERE game_id = ? ORDER BY id",
                (row["game_id"],)
            ).fetchall()
            row["players"] = [p["name"] for p in players]
            row["config"] = json.loads(row["config"])
            history.append(row)

        return history


def export_game_record(game_id, base_dir=None):
    """
    导出完整游戏记录为 Markdown 格式（用于发送到群里回顾）
    """
    status = get_game_status(game_id)
    if not status:
        return None

    config = status["config"]
    config_str = f"{config['civilian']}平民/{config['undercover']}卧底"
    if config.get("white_board", 0) > 0:
        config_str += f"/{config['white_board']}白板"

    # 头部
    lines = [
        "# 🎮 谁是卧底 — 游戏记录",
        "",
        f"📅 时间：{status['created_at'][:16].replace('T', ' ')}",
        f"👥 玩家：{'、'.join(status['all_players'])}",
        f"🎭 配置：{config_str}",
        "",
        "---",
        "",
    ]

    # 角色揭晓
    lines.append("## 🔑 角色分配")
    lines.append("")
    lines.append("| 玩家 | 角色 | 词语 |")
    lines.append("|------|------|------|")
    for r in status["roles"]:
        lines.append(f"| {r['player']} | {r['role']} | {r['word']} |")
    lines.append(f"- 平民词：「{status['civilian_word']}」")
    lines.append(f"- 卧底词：「{status['undercover_word']}」")
    lines.append("")
    lines.append("---")
    lines.append("")

    # 每轮记录
    with get_conn() as conn:
        # 获取最大轮次
        max_round_row = conn.execute(
            "SELECT MAX(round_num) as mr FROM descriptions WHERE game_id = ?", (game_id,)
        ).fetchone()
        max_round = max_round_row["mr"] if max_round_row and max_round_row["mr"] else 0

        for rnd in range(1, max_round + 1):
            lines.append(f"## 📝 第 {rnd} 轮")
            lines.append("")

            # 描述
            lines.append("### 描述阶段")
            lines.append("| 顺序 | 玩家 | 描述内容 |")
            lines.append("|------|------|----------|")
            descs = conn.execute("""
                SELECT player_name, description, desc_order FROM descriptions
                WHERE game_id = ? AND round_num = ? ORDER BY desc_order
            """, (game_id, rnd)).fetchall()
            for d in descs:
                desc_text = f'"{d["description"]}"' if d["description"] else "（未描述）"
                lines.append(f"| {d['desc_order']} | {d['player_name']} | {desc_text} |")
            lines.append("")

            # 投票
            votes = conn.execute("""
                SELECT voter, target FROM votes
                WHERE game_id = ? AND round_num = ? ORDER BY id
            """, (game_id, rnd)).fetchall()
            if votes:
                lines.append("### 投票阶段")
                lines.append("| 投票人 | 投给 |")
                lines.append("|--------|------|")
                for v in votes:
                    target = v["target"] if v["target"] else "（未投票）"
                    lines.append(f"| {v['voter']} | {target} |")
                lines.append("")

                # 统计
                tally = tally_votes(game_id, rnd)
                tally_str = "、".join([f"{t['player']} {t['votes']}票" for t in tally["tally"]])
                lines.append(f"**得票统计**：{tally_str}")
                lines.append("")

            # 本轮淘汰
            eliminated_this_round = [
                e for e in status["eliminated_players"] if e["round"] == rnd
            ]
            for e in eliminated_this_round:
                player_role = next((r for r in status["roles"] if r["player"] == e["name"]), None)
                role_text = f"（{player_role['role']}）" if player_role else ""
                lines.append(f"**淘汰**：{e['name']}{role_text}（{e['reason']}）")
                lines.append("")

            lines.append("---")
            lines.append("")

    # 游戏结果
    game = get_game_by_id(game_id)
    if game and game["status"] == "finished":
        lines.append("## 🏆 游戏结果")
        lines.append("")
        lines.append(f"- **获胜方**：{game['winner']}")
        lines.append(f"- **游戏轮数**：{max_round} 轮")
        lines.append("")

        if game.get("review"):
            lines.append("## ⭐ 精彩回顾")
            lines.append("")
            lines.append(game["review"])
            lines.append("")

    return "\n".join(lines)
