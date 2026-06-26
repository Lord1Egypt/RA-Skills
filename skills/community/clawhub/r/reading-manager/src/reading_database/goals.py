"""
阅读目标数据操作
"""
from datetime import datetime
from .connection import get_connection


def set_goal(year: int, target_count: int, month: int = None):
    """设置阅读目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO goals (year, month, target_count, completed_count)
        VALUES (?, ?, ?, 0)
        ON CONFLICT(year, month) DO UPDATE SET
            target_count = excluded.target_count,
            updated_at = CURRENT_TIMESTAMP
    """, (year, month, target_count))
    
    conn.commit()
    conn.close()


def get_goal(year: int, month: int = None) -> dict:
    """获取阅读目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if month:
        cursor.execute("SELECT * FROM goals WHERE year = ? AND month = ?", (year, month))
    else:
        cursor.execute("SELECT * FROM goals WHERE year = ? AND month IS NULL", (year,))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return dict(row)
    return None


def update_completed_count(year: int, month: int = None):
    """更新已完成数量"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if month:
        # 计算当月完成数量
        cursor.execute("""
            SELECT COUNT(*) FROM books 
            WHERE status = 'finished' 
            AND strftime('%Y', finished_at) = ?
            AND strftime('%m', finished_at) = ?
        """, (str(year), f"{month:02d}"))
    else:
        # 计算当年完成数量
        cursor.execute("""
            SELECT COUNT(*) FROM books 
            WHERE status = 'finished' 
            AND strftime('%Y', finished_at) = ?
        """, (str(year),))
    
    completed = cursor.fetchone()[0]
    
    if month:
        cursor.execute("""
            UPDATE goals SET completed_count = ?, updated_at = CURRENT_TIMESTAMP
            WHERE year = ? AND month = ?
        """, (completed, year, month))
    else:
        cursor.execute("""
            UPDATE goals SET completed_count = ?, updated_at = CURRENT_TIMESTAMP
            WHERE year = ? AND month IS NULL
        """, (completed, year))
    
    conn.commit()
    conn.close()
    return completed


def get_goal_progress(year: int, month: int = None) -> dict:
    """获取目标进度"""
    goal = get_goal(year, month)
    
    if not goal:
        return None
    
    # 更新完成数量
    completed = update_completed_count(year, month)
    
    target = goal["target_count"]
    progress = (completed / target * 100) if target > 0 else 0
    
    return {
        "year": year,
        "month": month,
        "target": target,
        "completed": completed,
        "remaining": max(0, target - completed),
        "progress": round(progress, 2),
    }


def list_goals(year: int = None) -> list:
    """列出阅读目标"""
    conn = get_connection()
    cursor = conn.cursor()
    
    if year:
        cursor.execute("SELECT * FROM goals WHERE year = ? ORDER BY month", (year,))
    else:
        cursor.execute("SELECT * FROM goals ORDER BY year DESC, month")
    
    rows = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in rows]


def get_yearly_stats(year: int) -> dict:
    """获取年度统计"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # 每月完成情况
    cursor.execute("""
        SELECT strftime('%m', finished_at) as month, COUNT(*) as count
        FROM books 
        WHERE status = 'finished' AND strftime('%Y', finished_at) = ?
        GROUP BY month
        ORDER BY month
    """, (str(year),))
    
    monthly = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 总完成数
    cursor.execute("""
        SELECT COUNT(*) FROM books 
        WHERE status = 'finished' AND strftime('%Y', finished_at) = ?
    """, (str(year),))
    
    total = cursor.fetchone()[0]
    conn.close()
    
    return {
        "year": year,
        "total_finished": total,
        "monthly_breakdown": monthly,
    }
