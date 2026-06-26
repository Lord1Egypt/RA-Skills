"""
笔记数据操作
"""
import json
from .connection import get_connection


def add_note(book_id: int, content: str, page: int = None, 
             note_type: str = "note", highlight_color: str = None, tags: list = None):
    """添加笔记"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO notes (book_id, content, page, note_type, highlight_color, tags)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (book_id, content, page, note_type, highlight_color, 
          json.dumps(tags or [], ensure_ascii=False)))
    
    note_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return note_id


def get_notes(book_id: int = None, note_type: str = None, limit: int = 50) -> list:
    """获取笔记列表"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if book_id:
        if note_type:
            cursor.execute("""
                SELECT * FROM notes 
                WHERE book_id = ? AND note_type = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (book_id, note_type, limit))
        else:
            cursor.execute("""
                SELECT * FROM notes 
                WHERE book_id = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (book_id, limit))
    else:
        if note_type:
            cursor.execute("""
                SELECT n.*, b.title as book_title 
                FROM notes n 
                JOIN books b ON n.book_id = b.id 
                WHERE n.note_type = ? 
                ORDER BY n.created_at DESC 
                LIMIT ?
            """, (note_type, limit))
        else:
            cursor.execute("""
                SELECT n.*, b.title as book_title 
                FROM notes n 
                JOIN books b ON n.book_id = b.id 
                ORDER BY n.created_at DESC 
                LIMIT ?
            """, (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def search_notes_by_tag(tag: str) -> list:
    """按标签搜索笔记"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT n.*, b.title as book_title 
        FROM notes n 
        JOIN books b ON n.book_id = b.id 
        WHERE n.tags LIKE ? 
        ORDER BY n.created_at DESC
    """, (f'%"{tag}"%',))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def search_notes(keyword: str) -> list:
    """搜索笔记内容"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT n.*, b.title as book_title 
        FROM notes n 
        JOIN books b ON n.book_id = b.id 
        WHERE n.content LIKE ? 
        ORDER BY n.created_at DESC
    """, (f"%{keyword}%",))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def delete_note(note_id: int):
    """删除笔记"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    conn.commit()
    conn.close()


def get_all_tags() -> list:
    """获取所有标签"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT tags FROM notes WHERE tags IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    
    tags = set()
    for row in rows:
        try:
            note_tags = json.loads(row[0])
            tags.update(note_tags)
        except:
            pass
    
    return sorted(list(tags))


def _row_to_dict(row) -> dict:
    """将行转换为字典"""
    result = dict(row)
    if result.get("tags"):
        try:
            result["tags"] = json.loads(result["tags"])
        except:
            result["tags"] = []
    else:
        result["tags"] = []
    return result
