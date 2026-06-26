"""
书籍数据操作
"""
import json
from datetime import datetime
from .connection import get_connection


def add_book(data: dict) -> int:
    """添加书籍"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO books (
            title, subtitle, authors, isbn10, isbn13, publisher,
            published_date, page_count, description, cover_url,
            categories, source_type, source_url, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data.get("title"),
        data.get("subtitle"),
        json.dumps(data.get("authors", []), ensure_ascii=False) if data.get("authors") else None,
        data.get("isbn10"),
        data.get("isbn13"),
        data.get("publisher"),
        data.get("published_date"),
        data.get("page_count"),
        data.get("description"),
        data.get("cover_url"),
        json.dumps(data.get("categories", []), ensure_ascii=False) if data.get("categories") else None,
        data.get("source_type", "book"),
        data.get("source_url"),
        data.get("status", "want"),
    ))
    
    book_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return book_id


def get_book(book_id: int) -> dict:
    """获取书籍详情"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return _row_to_dict(row)
    return None


def list_books(status=None, limit=20, offset=0) -> list:
    """列出书籍"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if status:
        cursor.execute(
            "SELECT * FROM books WHERE status = ? ORDER BY updated_at DESC LIMIT ? OFFSET ?",
            (status, limit, offset)
        )
    else:
        cursor.execute(
            "SELECT * FROM books ORDER BY updated_at DESC LIMIT ? OFFSET ?",
            (limit, offset)
        )
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def update_book(book_id: int, data: dict):
    """更新书籍"""
    conn = get_connection()
    cursor = conn.cursor()
    
    allowed_fields = ["title", "subtitle", "authors", "isbn10", "isbn13",
                      "publisher", "published_date", "page_count", "description",
                      "cover_url", "categories", "status", "rating", 
                      "started_at", "finished_at"]
    
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            if field in ["authors", "categories"] and data[field] is not None:
                updates.append(f"{field} = ?")
                values.append(json.dumps(data[field], ensure_ascii=False))
            else:
                updates.append(f"{field} = ?")
                values.append(data[field])
    
    if not updates:
        conn.close()
        return
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    values.append(book_id)
    
    query = f"UPDATE books SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    conn.close()


def delete_book(book_id: int):
    """删除书籍"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()


def search_books(keyword: str) -> list:
    """搜索书籍"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM books 
        WHERE title LIKE ? OR subtitle LIKE ? OR authors LIKE ? OR description LIKE ?
        ORDER BY updated_at DESC
    """, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [_row_to_dict(row) for row in rows]


def get_stats() -> dict:
    """获取阅读统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 各状态数量
    cursor.execute("SELECT status, COUNT(*) FROM books GROUP BY status")
    status_counts = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 总书籍数
    cursor.execute("SELECT COUNT(*) FROM books")
    total = cursor.fetchone()[0]
    
    # 已读完书籍数
    cursor.execute("SELECT COUNT(*) FROM books WHERE status = 'finished'")
    finished = cursor.fetchone()[0]
    
    # 本月读完
    cursor.execute("""
        SELECT COUNT(*) FROM books 
        WHERE status = 'finished' 
        AND strftime('%Y-%m', finished_at) = strftime('%Y-%m', 'now')
    """)
    finished_this_month = cursor.fetchone()[0]
    
    conn.close()
    
    return {
        "total": total,
        "want": status_counts.get("want", 0),
        "reading": status_counts.get("reading", 0),
        "finished": finished,
        "finished_this_month": finished_this_month,
    }


def _row_to_dict(row) -> dict:
    """将行转换为字典"""
    result = dict(row)
    # 解析 JSON 字段
    for field in ["authors", "categories"]:
        if result.get(field):
            try:
                result[field] = json.loads(result[field])
            except:
                result[field] = []
        else:
            result[field] = []
    return result
