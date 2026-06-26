#!/usr/bin/env python3
"""
Todo Skill - SQLite-based todo management
"""

import sqlite3
import argparse
import sys
import os
from datetime import datetime
from typing import Optional, List

DB_PATH = os.path.expanduser("~/.openclaw/workspace/data/todo.db")


def get_connection():
    """Get database connection, create tables if not exist."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    
    # Create tables
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            parent_id INTEGER,
            title TEXT NOT NULL,
            note TEXT,
            importance INTEGER DEFAULT 1,
            urgency INTEGER DEFAULT 1,
            status TEXT DEFAULT 'pending',
            due_date TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
            FOREIGN KEY (parent_id) REFERENCES todos(id) ON DELETE CASCADE
        );
        
        CREATE INDEX IF NOT EXISTS idx_todos_project ON todos(project_id);
        CREATE INDEX IF NOT EXISTS idx_todos_parent ON todos(parent_id);
        CREATE INDEX IF NOT EXISTS idx_todos_status ON todos(status);
    """)
    conn.commit()
    return conn


def create_project(name: str):
    """Create a new project."""
    conn = get_connection()
    try:
        conn.execute("INSERT INTO projects (name) VALUES (?)", (name,))
        conn.commit()
        print(f"✅ 项目 '{name}' 创建成功")
    except sqlite3.IntegrityError:
        print(f"❌ 项目 '{name}' 已存在")
    finally:
        conn.close()


def list_projects():
    """List all projects."""
    conn = get_connection()
    cursor = conn.execute("""
        SELECT p.id, p.name, p.created_at, 
               COUNT(CASE WHEN t.status = 'pending' THEN 1 END) as pending,
               COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed
        FROM projects p
        LEFT JOIN todos t ON p.id = t.project_id
        GROUP BY p.id
        ORDER BY p.created_at
    """)
    projects = cursor.fetchall()
    conn.close()
    
    if not projects:
        print("暂无项目，使用 'todo create-project <项目名>' 创建")
        return
    
    print("📋 项目列表：")
    print("-" * 50)
    for p in projects:
        print(f"  [{p['id']}] {p['name']}")
        print(f"      未完成: {p['pending']} | 已完成: {p['completed']}")


def delete_project(name: str):
    """Delete a project and all its todos."""
    conn = get_connection()
    cursor = conn.execute("SELECT id FROM projects WHERE name = ?", (name,))
    project = cursor.fetchone()
    
    if not project:
        print(f"❌ 项目 '{name}' 不存在")
        conn.close()
        return
    
    # Count todos
    cursor = conn.execute("SELECT COUNT(*) as cnt FROM todos WHERE project_id = ?", (project['id'],))
    count = cursor.fetchone()['cnt']
    
    conn.execute("DELETE FROM projects WHERE id = ?", (project['id'],))
    conn.commit()
    conn.close()
    
    print(f"✅ 项目 '{name}' 已删除（包含 {count} 个待办）")


def add_todo(project_name: str, title: str, importance: str = 'medium',
             urgency: str = 'medium', parent_id: Optional[int] = None,
             due_date: Optional[str] = None, note: Optional[str] = None):
    """Add a new todo."""
    conn = get_connection()
    
    # Get project
    cursor = conn.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
    project = cursor.fetchone()
    if not project:
        print(f"❌ 项目 '{project_name}' 不存在，请先创建")
        conn.close()
        return
    
    # Validate importance/urgency
    valid_levels = [1, 2, 3]
    if importance not in valid_levels:
        print(f"❌ 重要程度必须是: {', '.join(valid_levels)}")
        conn.close()
        return
    if urgency not in valid_levels:
        print(f"❌ 紧急程度必须是: {', '.join(valid_levels)}")
        conn.close()
        return
    
    # Parse due_date
    due_dt = None
    if due_date:
        try:
            if ' ' in due_date:
                due_dt = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            else:
                due_dt = datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            print(f"❌ 日期格式错误，应为 YYYY-MM-DD 或 YYYY-MM-DD HH:MM")
            conn.close()
            return
    
    # Insert
    cursor = conn.execute("""
        INSERT INTO todos (project_id, parent_id, title, note, importance, urgency, due_date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (project['id'], parent_id, title, note, importance, urgency, due_dt))
    
    todo_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # Display
    imp_icon = {1: '', 2: '🟠', 3: '🔴'}
    urg_icon = {1: '', 2: '🔥', 3: '🔥🔥'}
    
    print(f"✅ 待办创建成功 [#{todo_id}]")
    print(f"   {title}")
    print(f"   项目: {project_name} | 重要: {imp_icon.get(importance, '')}{importance} | 紧急: {urg_icon.get(urgency, '')}{urgency}")
    if due_date:
        print(f"   截止: {due_date}")
    if parent_id:
        print(f"   父待办: #{parent_id}")


def done_todo(todo_id: int):
    """Mark a todo as completed."""
    conn = get_connection()
    cursor = conn.execute("SELECT id, title, status FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    
    if not todo:
        print(f"❌ 待办 #{todo_id} 不存在")
        conn.close()
        return
    
    if todo['status'] == 'completed':
        print(f"⚠️ 待办 #{todo_id} 已经是完成状态")
        conn.close()
        return
    
    conn.execute("""
        UPDATE todos SET status = 'completed', completed_at = CURRENT_TIMESTAMP, 
        updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (todo_id,))
    conn.commit()
    conn.close()
    
    print(f"✅ 待办 #{todo_id} 已完成: {todo['title']}")


def undo_todo(todo_id: int):
    """Reopen a completed todo."""
    conn = get_connection()
    cursor = conn.execute("SELECT id, title, status FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    
    if not todo:
        print(f"❌ 待办 #{todo_id} 不存在")
        conn.close()
        return
    
    if todo['status'] == 'pending':
        print(f"⚠️ 待办 #{todo_id} 已经是未完成状态")
        conn.close()
        return
    
    conn.execute("""
        UPDATE todos SET status = 'pending', completed_at = NULL,
        updated_at = CURRENT_TIMESTAMP WHERE id = ?
    """, (todo_id,))
    conn.commit()
    conn.close()
    
    print(f"✅ 待办 #{todo_id} 已重新打开: {todo['title']}")


def delete_todo(todo_id: int):
    """Delete a todo and its children."""
    conn = get_connection()
    cursor = conn.execute("SELECT id, title FROM todos WHERE id = ?", (todo_id,))
    todo = cursor.fetchone()
    
    if not todo:
        print(f"❌ 待办 #{todo_id} 不存在")
        conn.close()
        return
    
    # Count children
    def count_children(pid):
        count = 1
        cursor = conn.execute("SELECT id FROM todos WHERE parent_id = ?", (pid,))
        for child in cursor.fetchall():
            count += count_children(child['id'])
        return count
    
    total = count_children(todo_id)
    
    # Delete (cascade will handle children)
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    
    if total > 1:
        print(f"✅ 已删除待办 #{todo_id} 及其 {total-1} 个子待办: {todo['title']}")
    else:
        print(f"✅ 已删除待办 #{todo_id}: {todo['title']}")


def list_todos(project_name: Optional[str] = None, status: Optional[str] = None,
               importance: Optional[str] = None, urgency: Optional[str] = None,
               date_from: Optional[str] = None, date_to: Optional[str] = None,
               show_all: bool = False):
    """List todos with filters."""
    conn = get_connection()
    
    query = """
        SELECT t.id, t.title, t.note, t.importance, t.urgency, t.status,
               t.due_date, t.created_at, t.completed_at, t.parent_id, p.name as project
        FROM todos t
        JOIN projects p ON t.project_id = p.id
        WHERE 1=1
    """
    params = []
    
    if project_name:
        query += " AND p.name = ?"
        params.append(project_name)
    
    if status:
        query += " AND t.status = ?"
        params.append(status)
    
    if importance:
        query += " AND t.importance = ?"
        params.append(importance)
    
    if urgency:
        query += " AND t.urgency = ?"
        params.append(urgency)
    
    if date_from:
        query += " AND DATE(t.created_at) >= ?"
        params.append(date_from)
    
    if date_to:
        query += " AND DATE(t.created_at) <= ?"
        params.append(date_to)
    
    # 排序：紧急 > 重要 > 普通按创建时间
    query += """ ORDER BY 
        CASE t.urgency WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 WHEN 'low' THEN 4 END,
        CASE t.importance WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 WHEN 'low' THEN 4 END,
        t.created_at DESC"""
    
    cursor = conn.execute(query, params)
    todos = cursor.fetchall()
    conn.close()
    
    if not todos:
        print("暂无符合条件的待办")
        return
    
    # Icons
    imp_icon = {1: '', 2: '🟠', 3: '🔴'}
    urg_icon = {1: '', 2: '🔥', 3: '🔥🔥'}
    status_icon = {'pending': '⬜', 'completed': '✅'}
    level_text = {1: '', 2: '', 3: ''}
    
    # 优先级分数映射
    level_score = {3: 1, 2: 2, 1: 3}
    
    # Build tree
    todos_by_parent = {}
    root_todos = []
    for t in todos:
        t_dict = dict(t)
        pid = t_dict['parent_id']
        if pid is None:
            root_todos.append(t_dict)
        else:
            if pid not in todos_by_parent:
                todos_by_parent[pid] = []
            todos_by_parent[pid].append(t_dict)
    
    # 计算待办的最大优先级（包括子待办）
    def get_max_priority(todo_dict):
        """获取待办及其子待办的最大优先级分数"""
        imp_score = level_score.get(int(todo_dict['importance']), 3)
        urg_score = level_score.get(int(todo_dict['urgency']), 3)
        min_score = min(imp_score, urg_score)  # 取更高的优先级
        
        # 检查子待办
        if todo_dict['id'] in todos_by_parent:
            for child in todos_by_parent[todo_dict['id']]:
                child_score = get_max_priority(child)
                min_score = min(min_score, child_score)
        
        return min_score
    
    # 排序父待办：考虑子待办的最大优先级
    def sort_key(todo_dict):
        max_priority = get_max_priority(todo_dict)
        own_urg = level_score.get(int(todo_dict['urgency']), 3)
        own_imp = level_score.get(int(todo_dict['importance']), 3)
        return (max_priority, own_urg, own_imp, todo_dict.get('created_at', ''))
    
    root_todos.sort(key=sort_key)
    
    # 排序子待办
    for pid in todos_by_parent:
        todos_by_parent[pid].sort(key=lambda t: (
            level_score.get(int(t['urgency']), 3),
            level_score.get(int(t['importance']), 3),
            t.get('created_at', '')
        ))
    
    def print_todo(t, indent=0):
        prefix = "  " * indent
        icon = status_icon.get(t['status'], '❓')
        imp = imp_icon.get(int(t['importance']), '')
        urg = urg_icon.get(int(t['urgency']), '')
        imp_txt = level_text.get(int(t['importance']), '')
        urg_txt = level_text.get(int(t['urgency']), '')
        
        line = f"{prefix}{icon} [#{t['id']}] {t['title']}"
        if t['project'] != project_name:
            line += f" ({t['project']})"
        
        # 显示重要程度：high显示emoji颜色，medium/low显示文字
        if int(t['importance']) == 3:
            imp_display = imp
        elif int(t['importance']) == 2:
            imp_display = imp
        else:
            imp_display = ""
        # 显示紧急程度：high🔥🔥，medium/low不显示
        urg_display = urg if int(t['urgency']) in [2, 3] else ''
        line += f" {imp_display}{urg_display}"
        
        if t['due_date']:
            due = t['due_date'][:10]
            line += f" 📅{due}"
        
        print(line)
        
        if t['note'] and indent == 0:
            print(f"{prefix}   💬 {t['note']}")
        
        # Print children
        if t['id'] in todos_by_parent:
            for child in todos_by_parent[t['id']]:
                print_todo(child, indent + 1)
    
    title = "📋 待办列表"
    if project_name:
        title += f" [{project_name}]"
    print(title)
    print("-" * 50)
    
    for t in root_todos:
        print_todo(t)


def show_todo(todo_id: int):
    """Show todo details."""
    conn = get_connection()
    cursor = conn.execute("""
        SELECT t.*, p.name as project
        FROM todos t
        JOIN projects p ON t.project_id = p.id
        WHERE t.id = ?
    """, (todo_id,))
    todo = cursor.fetchone()
    
    if not todo:
        print(f"❌ 待办 #{todo_id} 不存在")
        conn.close()
        return
    
    # Get children
    cursor = conn.execute("SELECT * FROM todos WHERE parent_id = ?", (todo_id,))
    children = cursor.fetchall()
    
    # Get parent
    parent = None
    if todo['parent_id']:
        cursor = conn.execute("SELECT id, title FROM todos WHERE id = ?", (todo['parent_id'],))
        parent = cursor.fetchone()
    
    conn.close()
    
    # Icons
    imp_icon = {1: '', 2: '🟠', 3: '🔴'}
    urg_icon = {1: '', 2: '🔥', 3: '🔥🔥'}
    status_icon = {'pending': '⬜ 未完成', 'completed': '✅ 已完成'}
    
    print(f"📋 待办详情 [#{todo['id']}]")
    print("-" * 50)
    print(f"标题: {todo['title']}")
    print(f"项目: {todo['project']}")
    print(f"状态: {status_icon.get(todo['status'], todo['status'])}")
    print(f"重要: {imp_icon.get(todo['importance'], '')} {todo['importance']}")
    print(f"紧急: {urg_icon.get(todo['urgency'], '')} {todo['urgency']}")
    
    if todo['due_date']:
        print(f"截止: {todo['due_date']}")
    
    if todo['note']:
        print(f"备注: {todo['note']}")
    
    print(f"创建: {todo['created_at']}")
    
    if todo['completed_at']:
        print(f"完成: {todo['completed_at']}")
    
    if parent:
        print(f"父待办: #{parent['id']} {parent['title']}")
    
    if children:
        print(f"\n子待办 ({len(children)}):")
        for c in children:
            icon = '✅' if c['status'] == 'completed' else '⬜'
            print(f"  {icon} [#{c['id']}] {c['title']}")


def edit_todo(todo_id: int, title: Optional[str] = None, importance: Optional[str] = None,
              urgency: Optional[str] = None, due_date: Optional[str] = None,
              note: Optional[str] = None, project_name: Optional[str] = None):
    """Edit a todo."""
    conn = get_connection()
    
    cursor = conn.execute("SELECT id FROM todos WHERE id = ?", (todo_id,))
    if not cursor.fetchone():
        print(f"❌ 待办 #{todo_id} 不存在")
        conn.close()
        return
    
    updates = []
    params = []
    
    if title:
        updates.append("title = ?")
        params.append(title)
    
    if importance:
        valid_levels = [1, 2, 3]
        if importance not in valid_levels:
            print(f"❌ 重要程度必须是: {', '.join(valid_levels)}")
            conn.close()
            return
        updates.append("importance = ?")
        params.append(importance)
    
    if urgency:
        valid_levels = [1, 2, 3]
        if urgency not in valid_levels:
            print(f"❌ 紧急程度必须是: {', '.join(valid_levels)}")
            conn.close()
            return
        updates.append("urgency = ?")
        params.append(urgency)
    
    if due_date:
        try:
            if ' ' in due_date:
                due_dt = datetime.strptime(due_date, "%Y-%m-%d %H:%M")
            else:
                due_dt = datetime.strptime(due_date, "%Y-%m-%d")
            updates.append("due_date = ?")
            params.append(due_dt)
        except ValueError:
            print(f"❌ 日期格式错误，应为 YYYY-MM-DD 或 YYYY-MM-DD HH:MM")
            conn.close()
            return
    
    if note is not None:
        updates.append("note = ?")
        params.append(note)
    
    if project_name:
        cursor = conn.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
        project = cursor.fetchone()
        if not project:
            print(f"❌ 项目 '{project_name}' 不存在")
            conn.close()
            return
        updates.append("project_id = ?")
        params.append(project['id'])
    
    if not updates:
        print("⚠️ 没有要更新的内容")
        conn.close()
        return
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    params.append(todo_id)
    
    query = f"UPDATE todos SET {', '.join(updates)} WHERE id = ?"
    conn.execute(query, params)
    conn.commit()
    conn.close()
    
    print(f"✅ 待办 #{todo_id} 已更新")


def show_stats(project_name: Optional[str] = None):
    """Show todo statistics."""
    conn = get_connection()
    
    if project_name:
        cursor = conn.execute("SELECT id FROM projects WHERE name = ?", (project_name,))
        project = cursor.fetchone()
        if not project:
            print(f"❌ 项目 '{project_name}' 不存在")
            conn.close()
            return
        
        cursor = conn.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'pending' AND due_date < DATE('now') THEN 1 END) as overdue
            FROM todos WHERE project_id = ?
        """, (project['id'],))
    else:
        cursor = conn.execute("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN status = 'pending' THEN 1 END) as pending,
                COUNT(CASE WHEN status = 'completed' THEN 1 END) as completed,
                COUNT(CASE WHEN status = 'pending' AND due_date < DATE('now') THEN 1 END) as overdue
            FROM todos
        """)
    
    stats = cursor.fetchone()
    
    # By importance
    cursor = conn.execute("""
        SELECT importance, COUNT(*) as cnt
        FROM todos
        WHERE status = 'pending'
        GROUP BY importance
        ORDER BY 
            CASE importance 
                WHEN 3 THEN 1 
                WHEN 2 THEN 2 
                WHEN 1 THEN 3 
            END
    """)
    by_importance = cursor.fetchall()
    
    # By urgency
    cursor = conn.execute("""
        SELECT urgency, COUNT(*) as cnt
        FROM todos
        WHERE status = 'pending'
        GROUP BY urgency
        ORDER BY 
            CASE urgency 
                WHEN 3 THEN 1 
                WHEN 2 THEN 2 
                WHEN 1 THEN 3 
            END
    """)
    by_urgency = cursor.fetchall()
    
    conn.close()
    
    title = "📊 待办统计"
    if project_name:
        title += f" [{project_name}]"
    print(title)
    print("=" * 50)
    print(f"总计: {stats['total']} | 未完成: {stats['pending']} | 已完成: {stats['completed']} | 逾期: {stats['overdue']}")
    print()
    
    imp_icon = {1: '', 2: '🟠', 3: '🔴'}
    urg_icon = {1: '', 2: '🔥', 3: '🔥🔥'}
    print("按重要程度（未完成）:")
    for row in by_importance:
        icon = imp_icon.get(row['importance'], '')
        print(f"  {icon} {row['importance']}: {row['cnt']}")
    
    print()
    print("按紧急程度（未完成）:")
    for row in by_urgency:
        icon = urg_icon.get(row['urgency'], '')
        print(f"  {icon} {row['urgency']}: {row['cnt']}")


def search_todos(keyword: str, status: Optional[str] = None):
    """Search todos by keyword in title or note."""
    conn = get_connection()
    
    query = """
        SELECT t.id, t.title, t.note, t.importance, t.urgency, t.status,
               t.due_date, t.created_at, t.parent_id, p.name as project
        FROM todos t
        JOIN projects p ON t.project_id = p.id
        WHERE (t.title LIKE ? OR t.note LIKE ?)
    """
    search_pattern = f"%{keyword}%"
    params = [search_pattern, search_pattern]
    
    if status:
        query += " AND t.status = ?"
        params.append(status)
    
    # 排序：紧急 > 重要 > 普通按创建时间
    query += """ ORDER BY 
        CASE t.urgency WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 WHEN 'low' THEN 4 END,
        CASE t.importance WHEN 'critical' THEN 1 WHEN 'high' THEN 2 WHEN 'medium' THEN 3 WHEN 'low' THEN 4 END,
        t.created_at DESC"""
    
    cursor = conn.execute(query, params)
    todos = cursor.fetchall()
    conn.close()
    
    if not todos:
        print(f"未找到包含 '{keyword}' 的待办")
        return
    
    # Icons
    imp_icon = {1: '', 2: '🟠', 3: '🔴'}
    urg_icon = {1: '', 2: '🔥', 3: '🔥🔥'}
    status_icon = {'pending': '⬜', 'completed': '✅'}
    level_text = {1: '', 2: '', 3: ''}
    
    print(f"🔍 搜索结果：'{keyword}' ({len(todos)} 条)")
    print("-" * 50)
    
    for t in todos:
        icon = status_icon.get(t['status'], '❓')
        imp = imp_icon.get(int(t['importance']), '')
        urg = urg_icon.get(int(t['urgency']), '')
        imp_txt = level_text.get(int(t['importance']), '')
        urg_txt = level_text.get(int(t['urgency']), '')
        
        line = f"{icon} [#{t['id']}] {t['title']} ({t['project']})"
        
        # 显示重要程度：high显示emoji颜色，medium/low显示文字
        if int(t['importance']) == 3:
            imp_display = imp
        elif int(t['importance']) == 2:
            imp_display = imp
        else:
            imp_display = ""
        # 显示紧急程度：high🔥🔥，medium/low不显示
        urg_display = urg if int(t['urgency']) in [2, 3] else ''
        line += f" {imp_display}{urg_display}"
        
        print(line)
        
        # 高亮匹配的备注
        if t['note'] and keyword.lower() in t['note'].lower():
            print(f"   💬 {t['note'][:50]}...")


def main():
    parser = argparse.ArgumentParser(description='Todo management tool')
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # create-project
    cp_parser = subparsers.add_parser('create-project', help='创建项目')
    cp_parser.add_argument('name', help='项目名称')
    
    # list-projects
    subparsers.add_parser('list-projects', help='列出所有项目')
    
    # delete-project
    dp_parser = subparsers.add_parser('delete-project', help='删除项目')
    dp_parser.add_argument('name', help='项目名称')
    
    # add
    add_parser = subparsers.add_parser('add', help='添加待办')
    add_parser.add_argument('project', help='项目名称')
    add_parser.add_argument('title', help='待办标题')
    add_parser.add_argument('-i', '--importance', type=int, choices=[1, 2, 3],
                            default=1, help='重要程度 (1=普通, 2=重要, 3=紧急)')
    add_parser.add_argument('-u', '--urgency', type=int, choices=[1, 2, 3],
                            default=1, help='紧急程度 (1=普通, 2=重要, 3=紧急)')
    add_parser.add_argument('-p', '--parent', type=int, help='父待办ID')
    add_parser.add_argument('-d', '--due', help='截止日期 (YYYY-MM-DD)')
    add_parser.add_argument('-n', '--note', help='备注')
    
    # done
    done_parser = subparsers.add_parser('done', help='完成待办')
    done_parser.add_argument('id', type=int, help='待办ID')
    
    # undo
    undo_parser = subparsers.add_parser('undo', help='重新打开待办')
    undo_parser.add_argument('id', type=int, help='待办ID')
    
    # delete
    del_parser = subparsers.add_parser('delete', help='删除待办')
    del_parser.add_argument('id', type=int, help='待办ID')
    
    # list / list-all
    list_parser = subparsers.add_parser('list', help='列出项目待办')
    list_parser.add_argument('project', help='项目名称')
    list_parser.add_argument('-p', '--pending', action='store_true', help='只显示未完成')
    list_parser.add_argument('-c', '--completed', action='store_true', help='只显示已完成')
    
    listall_parser = subparsers.add_parser('list-all', help='列出所有待办')
    listall_parser.add_argument('-p', '--pending', action='store_true', help='只显示未完成')
    listall_parser.add_argument('-c', '--completed', action='store_true', help='只显示已完成')
    listall_parser.add_argument('--importance', type=int, choices=[1, 2, 3])
    listall_parser.add_argument('--urgency', type=int, choices=[1, 2, 3])
    listall_parser.add_argument('--from', dest='date_from', help='开始日期 (YYYY-MM-DD)')
    listall_parser.add_argument('--to', dest='date_to', help='结束日期 (YYYY-MM-DD)')
    
    # show
    show_parser = subparsers.add_parser('show', help='查看待办详情')
    show_parser.add_argument('id', type=int, help='待办ID')
    
    # edit
    edit_parser = subparsers.add_parser('edit', help='编辑待办')
    edit_parser.add_argument('id', type=int, help='待办ID')
    edit_parser.add_argument('--title', help='新标题')
    edit_parser.add_argument('--importance', type=int, choices=[1, 2, 3])
    edit_parser.add_argument('--urgency', type=int, choices=[1, 2, 3])
    edit_parser.add_argument('--due', help='截止日期')
    edit_parser.add_argument('--note', help='备注')
    edit_parser.add_argument('--project', help='移动到项目')
    
    # stats
    stats_parser = subparsers.add_parser('stats', help='统计信息')
    stats_parser.add_argument('project', nargs='?', help='项目名称')
    
    # search
    search_parser = subparsers.add_parser('search', help='搜索待办')
    search_parser.add_argument('keyword', help='搜索关键词')
    search_parser.add_argument('-p', '--pending', action='store_true', help='只搜索未完成')
    search_parser.add_argument('-c', '--completed', action='store_true', help='只搜索已完成')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'create-project':
        create_project(args.name)
    elif args.command == 'list-projects':
        list_projects()
    elif args.command == 'delete-project':
        delete_project(args.name)
    elif args.command == 'add':
        add_todo(args.project, args.title, args.importance, args.urgency,
                 args.parent, args.due, args.note)
    elif args.command == 'done':
        done_todo(args.id)
    elif args.command == 'undo':
        undo_todo(args.id)
    elif args.command == 'delete':
        delete_todo(args.id)
    elif args.command == 'list':
        status = 'pending' if args.pending else ('completed' if args.completed else None)
        list_todos(args.project, status)
    elif args.command == 'list-all':
        status = 'pending' if args.pending else ('completed' if args.completed else None)
        list_todos(None, status, args.importance, args.urgency, args.date_from, args.date_to)
    elif args.command == 'show':
        show_todo(args.id)
    elif args.command == 'edit':
        edit_todo(args.id, args.title, args.importance, args.urgency, args.due, args.note, args.project)
    elif args.command == 'stats':
        show_stats(args.project)
    elif args.command == 'search':
        status = 'pending' if args.pending else ('completed' if args.completed else None)
        search_todos(args.keyword, status)


if __name__ == '__main__':
    main()