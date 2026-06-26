"""
台灣職籃 — SQLite 資料持久化模組

資料庫路徑：~/.local/share/taiwan-basketball/basketball.db

提供以下功能：
  - 儲存 / 查詢比賽結果
  - 儲存 / 查詢戰績快照
  - 管理球隊訂閱清單
  - 儲存 / 查詢交易資訊
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

_DB_PATH = Path.home() / '.local' / 'share' / 'taiwan-basketball' / 'basketball.db'


def get_connection() -> sqlite3.Connection:
    """取得資料庫連線，首次使用時自動建立 schema"""
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(_DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA foreign_keys=ON')
    _ensure_schema(conn)
    return conn


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """建立資料表（若不存在）"""
    conn.executescript('''
        CREATE TABLE IF NOT EXISTS games (
            game_id     TEXT NOT NULL,
            league      TEXT NOT NULL,
            game_date   TEXT NOT NULL,
            game_time   TEXT,
            home_team   TEXT NOT NULL,
            away_team   TEXT NOT NULL,
            home_score  INTEGER,
            away_score  INTEGER,
            venue       TEXT,
            status      TEXT,
            round       INTEGER,
            weekday     TEXT,
            updated_at  TEXT NOT NULL,
            PRIMARY KEY (game_id, league)
        );

        CREATE TABLE IF NOT EXISTS standings_snapshots (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            league        TEXT NOT NULL,
            snapshot_date TEXT NOT NULL,
            team          TEXT NOT NULL,
            rank          INTEGER,
            gp            INTEGER,
            wins          INTEGER,
            losses        INTEGER,
            win_rate      REAL
        );

        CREATE TABLE IF NOT EXISTS subscriptions (
            team   TEXT NOT NULL,
            league TEXT NOT NULL,
            PRIMARY KEY (team, league)
        );

        CREATE TABLE IF NOT EXISTS transactions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            league      TEXT NOT NULL,
            trans_date  TEXT,
            player      TEXT,
            from_team   TEXT,
            to_team     TEXT,
            trans_type  TEXT,
            note        TEXT,
            title       TEXT,
            url         TEXT,
            saved_at    TEXT NOT NULL
        );

        CREATE INDEX IF NOT EXISTS idx_games_date   ON games(game_date);
        CREATE INDEX IF NOT EXISTS idx_games_league ON games(league);
        CREATE INDEX IF NOT EXISTS idx_snap_league  ON standings_snapshots(league, snapshot_date);
    ''')
    conn.commit()


# ─── 比賽結果 ───

def save_games(games: list[dict], league: str) -> int:
    """儲存比賽結果（upsert），回傳成功儲存筆數"""
    if not games:
        return 0

    now = datetime.now().isoformat(timespec='seconds')
    rows = []
    for g in games:
        game_id = str(g.get('game_id', ''))
        if not game_id:
            continue
        rows.append((
            game_id,
            league,
            g.get('date', ''),
            g.get('time', ''),
            g.get('home_team', ''),
            g.get('away_team', ''),
            g.get('home_score'),
            g.get('away_score'),
            g.get('venue', ''),
            g.get('status', ''),
            g.get('round'),
            g.get('weekday', ''),
            now,
        ))

    if not rows:
        return 0

    with get_connection() as conn:
        conn.executemany(
            '''INSERT OR REPLACE INTO games
               (game_id, league, game_date, game_time, home_team, away_team,
                home_score, away_score, venue, status, round, weekday, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
            rows,
        )
        conn.commit()
    return len(rows)


def get_games_from_db(
    league: Optional[str] = None,
    team: Optional[str] = None,
    last_n: int = 0,
    status: Optional[str] = None,
) -> list[dict]:
    """從本地 DB 查詢比賽結果

    Args:
        league: 聯盟代碼過濾（可選）
        team:   球隊名過濾（可選，模糊比對）
        last_n: 只回傳最近 N 場（0 = 全部）
        status: 比賽狀態過濾（completed / upcoming / live）
    """
    where = []
    params: list = []

    if league:
        where.append('league = ?')
        params.append(league)
    if team:
        where.append('(home_team LIKE ? OR away_team LIKE ?)')
        params.extend([f'%{team}%', f'%{team}%'])
    if status:
        where.append('status = ?')
        params.append(status)

    sql = 'SELECT * FROM games'
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' ORDER BY game_date DESC, game_time DESC'
    if last_n > 0:
        sql += f' LIMIT {int(last_n)}'

    try:
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error:
        return []


# ─── 戰績快照 ───

def save_standings(standings: list[dict], league: str) -> None:
    """儲存戰績快照（每日一份，重複執行時 upsert）"""
    if not standings:
        return
    today = datetime.now().date().isoformat()
    rows = [
        (league, today, s.get('team', ''), s.get('rank'),
         s.get('gp'), s.get('wins'), s.get('losses'), s.get('win_rate'))
        for s in standings
    ]
    with get_connection() as conn:
        # 刪除今日同聯盟舊快照再重新寫入
        conn.execute(
            'DELETE FROM standings_snapshots WHERE league=? AND snapshot_date=?',
            (league, today),
        )
        conn.executemany(
            '''INSERT INTO standings_snapshots
               (league, snapshot_date, team, rank, gp, wins, losses, win_rate)
               VALUES (?,?,?,?,?,?,?,?)''',
            rows,
        )
        conn.commit()


def get_latest_standings(league: str) -> list[dict]:
    """取得最新戰績快照"""
    try:
        with get_connection() as conn:
            row = conn.execute(
                'SELECT MAX(snapshot_date) as d FROM standings_snapshots WHERE league=?',
                (league,),
            ).fetchone()
            if not row or not row['d']:
                return []
            rows = conn.execute(
                '''SELECT * FROM standings_snapshots
                   WHERE league=? AND snapshot_date=?
                   ORDER BY rank''',
                (league, row['d']),
            ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error:
        return []


def _row_count_changed(conn: sqlite3.Connection) -> bool:
    """回傳最後一次 DML 操作是否影響了任何行"""
    return conn.execute('SELECT changes() as c').fetchone()['c'] > 0


# ─── 訂閱管理 ───

def add_subscription(team: str, league: str) -> bool:
    """新增球隊訂閱，回傳是否為新增（True）或已存在（False）"""
    try:
        with get_connection() as conn:
            conn.execute(
                'INSERT OR IGNORE INTO subscriptions (team, league) VALUES (?,?)',
                (team, league),
            )
            conn.commit()
            return _row_count_changed(conn)
    except sqlite3.Error:
        return False


def remove_subscription(team: str, league: str) -> bool:
    """移除球隊訂閱，回傳是否成功刪除"""
    try:
        with get_connection() as conn:
            conn.execute(
                'DELETE FROM subscriptions WHERE team=? AND league=?',
                (team, league),
            )
            conn.commit()
            return _row_count_changed(conn)
    except sqlite3.Error:
        return False


def get_subscriptions(league: Optional[str] = None) -> list[dict]:
    """取得所有（或指定聯盟的）訂閱清單"""
    try:
        with get_connection() as conn:
            if league:
                rows = conn.execute(
                    'SELECT team, league FROM subscriptions WHERE league=? ORDER BY team',
                    (league,),
                ).fetchall()
            else:
                rows = conn.execute(
                    'SELECT team, league FROM subscriptions ORDER BY league, team'
                ).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error:
        return []


# ─── 交易 / 異動 ───

def save_transactions(transactions: list[dict], league: str) -> int:
    """儲存交易/球員異動資訊，回傳儲存筆數"""
    if not transactions:
        return 0
    now = datetime.now().isoformat(timespec='seconds')
    rows = [
        (
            league,
            t.get('date', t.get('trans_date', '')),
            t.get('player', ''),
            t.get('from_team', ''),
            t.get('to_team', ''),
            t.get('type', t.get('trans_type', '')),
            t.get('note', ''),
            t.get('title', ''),
            t.get('url', ''),
            now,
        )
        for t in transactions
    ]
    with get_connection() as conn:
        conn.executemany(
            '''INSERT INTO transactions
               (league, trans_date, player, from_team, to_team, trans_type,
                note, title, url, saved_at)
               VALUES (?,?,?,?,?,?,?,?,?,?)''',
            rows,
        )
        conn.commit()
    return len(rows)


def get_transactions_from_db(
    league: Optional[str] = None, limit: int = 50
) -> list[dict]:
    """查詢已儲存的交易資訊"""
    where = []
    params: list = []
    if league:
        where.append('league=?')
        params.append(league)
    sql = 'SELECT * FROM transactions'
    if where:
        sql += ' WHERE ' + ' AND '.join(where)
    sql += ' ORDER BY saved_at DESC'
    if limit > 0:
        sql += f' LIMIT {int(limit)}'
    try:
        with get_connection() as conn:
            rows = conn.execute(sql, params).fetchall()
            return [dict(r) for r in rows]
    except sqlite3.Error:
        return []
