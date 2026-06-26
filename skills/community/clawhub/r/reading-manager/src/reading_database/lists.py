"""
书单数据操作
"""
import json
from .connection import get_connection


def create_list(name: str, description: str = None) -> int:
    """创建书单"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO lists (name, description, book_ids)
        VALUES (?, ?, ?)
    """, (name, description, json.dumps([])))
    
    list_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return list_id


def get_list(list_id: int = None, name: str = None) -> dict:
    """获取书单"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if list_id:
        cursor.execute("SELECT * FROM lists WHERE id = ?", (list_id,))
    elif name:
        cursor.execute("SELECT * FROM lists WHERE name = ?", (name,))
    else:
        conn.close()
        return None
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return _row_to_dict(row)
    return None


def list_lists() -> list:
    """列出所有书单"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM lists ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def update_list(list_id: int, name: str = None, description: str = None):
    """更新书单信息"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if name:
        cursor.execute("UPDATE lists SET name = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                       (name, list_id))
    if description:
        cursor.execute("UPDATE lists SET description = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                       (description, list_id))
    
    conn.commit()
    conn.close()


def delete_list(list_id: int):
    """删除书单"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM lists WHERE id = ?", (list_id,))
    conn.commit()
    conn.close()


def add_book_to_list(list_id: int, book_id: int):
    """添加书籍到书单"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT book_ids FROM lists WHERE id = ?", (list_id,))
    row = cursor.fetchone()
    
    if row:
        book_ids = json.loads(row[0] or "[]")
        if book_id not in book_ids:
            book_ids.append(book_id)
            cursor.execute("UPDATE lists SET book_ids = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                           (json.dumps(book_ids), list_id))
            conn.commit()
    
    conn.close()


def remove_book_from_list(list_id: int, book_id: int):
    """从书单移除书籍"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT book_ids FROM lists WHERE id = ?", (list_id,))
    row = cursor.fetchone()
    
    if row:
        book_ids = json.loads(row[0] or "[]")
        if book_id in book_ids:
            book_ids.remove(book_id)
            cursor.execute("UPDATE lists SET book_ids = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                           (json.dumps(book_ids), list_id))
            conn.commit()
    
    conn.close()


def get_list_books(list_id: int) -> list:
    """获取书单中的书籍"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT book_ids FROM lists WHERE id = ?", (list_id,))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return []
    
    book_ids = json.loads(row[0] or "[]")
    
    if not book_ids:
        conn.close()
        return []
    
    placeholders = ",".join(["?"] * len(book_ids))
    cursor.execute(f"SELECT * FROM books WHERE id IN ({placeholders})", book_ids)
    
    from .books import _row_to_dict
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def _row_to_dict(row) -> dict:
    """将行转换为字典"""
    result = dict(row)
    if result.get("book_ids"):
        try:
            result["book_ids"] = json.loads(result["book_ids"])
        except:
            result["book_ids"] = []
    else:
        result["book_ids"] = []
    return result
