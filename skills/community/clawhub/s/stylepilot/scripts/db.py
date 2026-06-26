"""
db.py - 衣橱数据库
软Schema设计，支持灵活字段扩展
"""
import sqlite3
import os
import time
import json
import hashlib
import uuid
import shutil
from typing import Optional, Any

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_PROJECT_ROOT = os.path.dirname(_SCRIPT_DIR)
_DB_DIR = os.path.join(_PROJECT_ROOT, 'data')
os.makedirs(_DB_DIR, exist_ok=True)
DB_PATH = os.environ.get('WARDROBE_DB_PATH',
                          os.path.join(_DB_DIR, 'wardrobe.db'))


def get_conn():
    return sqlite3.connect(DB_PATH)


def ts():
    return time.strftime('%Y-%m-%d %H:%M:%S')


def md5(text: str) -> str:
    return hashlib.md5(text.encode()).hexdigest()


def init_db():
    # 创建 images 目录
    import os
    images_dir = os.path.join(_DB_DIR, 'images')
    os.makedirs(images_dir, exist_ok=True)
    
    conn = get_conn()
    c = conn.cursor()

    # 衣服表
    c.execute('''CREATE TABLE IF NOT EXISTS clothing_items (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL DEFAULT '',
        category TEXT DEFAULT '',
        color TEXT DEFAULT '',
        season TEXT DEFAULT '',
        style TEXT DEFAULT '',
        occasion TEXT DEFAULT '',
        image_path TEXT DEFAULT '',
        meta TEXT DEFAULT '{}',
        created_at TEXT DEFAULT ''
    )''')

    # 搭配记录表
    c.execute('''CREATE TABLE IF NOT EXISTS outfit_records (
        id TEXT PRIMARY KEY,
        name TEXT DEFAULT '',
        scene TEXT DEFAULT '',
        description TEXT DEFAULT '',
        items TEXT DEFAULT '[]',
        image_paths TEXT DEFAULT '[]',
        feedback TEXT DEFAULT '',
        feedback_note TEXT DEFAULT '',
        created_at TEXT DEFAULT ''
    )''')

    # 兼容已存在数据库：补齐 feedback 字段
    _ensure_outfit_feedback_columns(c)

    conn.commit()
    conn.close()


def _ensure_outfit_feedback_columns(cursor):
    cursor.execute("PRAGMA table_info(outfit_records)")
    cols = [row[1] for row in cursor.fetchall()]
    if 'feedback' not in cols:
        cursor.execute("ALTER TABLE outfit_records ADD COLUMN feedback TEXT DEFAULT ''")
    if 'feedback_note' not in cols:
        cursor.execute("ALTER TABLE outfit_records ADD COLUMN feedback_note TEXT DEFAULT ''")


# ============ 衣服操作 ============

def save_clothing(name: str, category: str = '', color: str = '',
                  season: str = '', style: str = '', occasion: str = '',
                  image_path: str = '', meta: dict = None) -> str:
    """保存衣服，返回 item_id"""
    conn = get_conn()
    c = conn.cursor()
    now = ts()

    # 用 name + category 的 md5 前12位作为 id（同一件衣服不重复存）
    item_id = md5(f"{name}|{category}")[:12]

    c.execute('SELECT id FROM clothing_items WHERE id=?', (item_id,))
    if c.fetchone():
        c.execute('''UPDATE clothing_items SET
            name=?, category=?, color=?, season=?, style=?,
            occasion=?, image_path=?, meta=?, created_at=?
            WHERE id=?''',
            (name, category, color, season, style, occasion,
             image_path, json.dumps(meta or {}, ensure_ascii=False),
             now, item_id))
    else:
        c.execute('''INSERT INTO clothing_items
            (id, name, category, color, season, style, occasion, image_path, meta, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?)''',
            (item_id, name, category, color, season, style, occasion,
             image_path, json.dumps(meta or {}, ensure_ascii=False), now))

    conn.commit()
    conn.close()
    return item_id


def get_clothing(item_id: str) -> Optional[dict]:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM clothing_items WHERE id=?', (item_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_clothing(row)


def get_all_clothing(limit: int = 200) -> list:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM clothing_items ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [_row_to_clothing(r) for r in rows]


def get_clothing_by_category(category: str) -> list:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM clothing_items WHERE category=? ORDER BY created_at DESC',
              (category,))
    rows = c.fetchall()
    conn.close()
    return [_row_to_clothing(r) for r in rows]


def search_clothing(keyword: str) -> list:
    conn = get_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM clothing_items
        WHERE name LIKE ? OR category LIKE ? OR color LIKE ? OR style LIKE ?
        ORDER BY created_at DESC''',
        (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
    rows = c.fetchall()
    conn.close()
    return [_row_to_clothing(r) for r in rows]


def _row_to_clothing(row) -> dict:
    return {
        'id': row[0],
        'name': row[1] or '',
        'category': row[2] or '',
        'color': row[3] or '',
        'season': row[4] or '',
        'style': row[5] or '',
        'occasion': row[6] or '',
        'image_path': row[7] or '',
        'meta': json.loads(row[8] or '{}'),
        'created_at': row[9] or ''
    }


# ============ 搭配记录操作 ============

def save_outfit(name: str, scene: str, description: str,
                items: list, image_paths: list = None,
                feedback: str = '', feedback_note: str = '') -> str:
    """保存搭配记录"""
    conn = get_conn()
    c = conn.cursor()
    now = ts()

    # 使用 uuid4 保证高并发/同秒连续请求下 id 唯一
    outfit_id = uuid.uuid4().hex[:16]

    c.execute('''INSERT INTO outfit_records
        (id, name, scene, description, items, image_paths, feedback, feedback_note, created_at)
        VALUES (?,?,?,?,?,?,?,?,?)''',
        (outfit_id, name, scene, description,
         json.dumps(items, ensure_ascii=False),
         json.dumps(image_paths or [], ensure_ascii=False),
         feedback, feedback_note,
         now))
    conn.commit()
    conn.close()
    return outfit_id


def get_recent_outfits(limit: int = 10) -> list:
    conn = get_conn()
    c = conn.cursor()
    c.execute('SELECT * FROM outfit_records ORDER BY created_at DESC LIMIT ?', (limit,))
    rows = c.fetchall()
    conn.close()
    return [_row_to_outfit(r) for r in rows]


def update_outfit_feedback(outfit_id: str, feedback: str, feedback_note: str = '') -> bool:
    conn = get_conn()
    c = conn.cursor()
    c.execute('''UPDATE outfit_records
        SET feedback=?, feedback_note=?
        WHERE id=?''', (feedback, feedback_note, outfit_id))
    conn.commit()
    updated = c.rowcount > 0
    conn.close()
    return updated


def _row_to_outfit(row) -> dict:
    feedback = row[6] if len(row) > 6 else ''
    feedback_note = row[7] if len(row) > 7 else ''
    created_at = row[8] if len(row) > 8 else (row[6] if len(row) > 6 else '')
    return {
        'id': row[0],
        'name': row[1] or '',
        'scene': row[2] or '',
        'description': row[3] or '',
        'items': json.loads(row[4] or '[]'),
        'image_paths': json.loads(row[5] or '[]'),
        'feedback': feedback or '',
        'feedback_note': feedback_note or '',
        'created_at': created_at or ''
    }
