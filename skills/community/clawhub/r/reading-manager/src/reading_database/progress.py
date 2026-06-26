"""
阅读进度数据操作
"""
from .connection import get_connection


def add_progress(book_id: int, current_page: int = None, percent: float = None, 
                 minutes_read: int = 0, notes: str = None):
    """添加阅读进度记录"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 获取书籍总页数
    cursor.execute("SELECT page_count FROM books WHERE id = ?", (book_id,))
    row = cursor.fetchone()
    total_pages = row[0] if row else None
    
    # 计算百分比
    if current_page and total_pages:
        percent = round(current_page / total_pages * 100, 2)
    elif percent and total_pages:
        current_page = int(total_pages * percent / 100)
    
    cursor.execute("""
        INSERT INTO reading_progress (book_id, current_page, total_pages, percent, minutes_read, notes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (book_id, current_page, total_pages, percent, minutes_read, notes))
    
    # 更新书籍状态
    if current_page and total_pages:
        if current_page >= total_pages:
            cursor.execute("""
                UPDATE books SET status = 'finished', finished_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """, (book_id,))
        else:
            cursor.execute("""
                UPDATE books SET status = 'reading', started_at = COALESCE(started_at, CURRENT_TIMESTAMP) 
                WHERE id = ? AND status = 'want'
            """, (book_id,))
    
    conn.commit()
    conn.close()


def get_latest_progress(book_id: int) -> dict:
    """获取最新阅读进度"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM reading_progress 
        WHERE book_id = ? 
        ORDER BY recorded_at DESC 
        LIMIT 1
    """, (book_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def get_progress_history(book_id: int, limit: int = 20) -> list:
    """获取阅读进度历史"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM reading_progress 
        WHERE book_id = ? 
        ORDER BY recorded_at DESC 
        LIMIT ?
    """, (book_id, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_total_reading_time(book_id: int = None) -> int:
    """获取总阅读时长（分钟）"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if book_id:
        cursor.execute("SELECT SUM(minutes_read) FROM reading_progress WHERE book_id = ?", (book_id,))
    else:
        cursor.execute("SELECT SUM(minutes_read) FROM reading_progress")
    
    result = cursor.fetchone()
    conn.close()
    
    return result[0] or 0


def get_reading_stats(days: int = 30) -> dict:
    """获取阅读统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(DISTINCT book_id) as books_read,
            SUM(minutes_read) as total_minutes,
            AVG(percent) as avg_progress
        FROM reading_progress 
        WHERE recorded_at >= datetime('now', '-{} days')
    """.format(days))
    
    row = cursor.fetchone()
    conn.close()
    
    return {
        "books_read": row[0] or 0,
        "total_minutes": row[1] or 0,
        "avg_progress": round(row[2] or 0, 2),
    }
