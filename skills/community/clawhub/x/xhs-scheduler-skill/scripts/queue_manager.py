#!/usr/bin/env python3
"""
小红书内容队列管理器
负责内容的增删改查和状态管理
"""

import json
import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class ContentTask:
    """内容任务数据结构"""
    task_id: str
    title: str
    content: str
    images: List[str]  # 图片路径列表
    tags: List[str]
    status: str  # 'draft', 'scheduled', 'published', 'failed'
    scheduled_time: Optional[datetime]
    created_at: datetime
    published_at: Optional[datetime] = None
    error_message: Optional[str] = None
    platform_task_id: Optional[str] = None  # 小红书返回的任务ID
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        data = asdict(self)
        # 处理datetime序列化
        for key in ['scheduled_time', 'created_at', 'published_at']:
            if data[key]:
                data[key] = data[key].isoformat()
        data['images'] = json.dumps(data['images'])
        data['tags'] = json.dumps(data['tags'])
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ContentTask':
        """从字典创建"""
        data['images'] = json.loads(data['images'])
        data['tags'] = json.loads(data['tags'])
        for key in ['scheduled_time', 'created_at', 'published_at']:
            if data[key]:
                data[key] = datetime.fromisoformat(data[key])
        return cls(**data)


class QueueManager:
    """队列管理器"""
    
    def __init__(self, db_path: str = None):
        """初始化队列管理器"""
        if db_path is None:
            # 默认存储在Skill数据目录
            base_dir = Path(__file__).parent.parent
            data_dir = base_dir / 'data'
            data_dir.mkdir(exist_ok=True)
            db_path = data_dir / 'queue.db'
        
        self.db_path = str(db_path)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS content_tasks (
                task_id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                images TEXT,  -- JSON数组
                tags TEXT,    -- JSON数组
                status TEXT DEFAULT 'draft',
                scheduled_time TEXT,
                created_at TEXT NOT NULL,
                published_at TEXT,
                error_message TEXT,
                platform_task_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_task(self, title: str, content: str, images: List[str], 
                 tags: List[str] = None, scheduled_time: datetime = None) -> ContentTask:
        """
        添加任务到队列
        
        Args:
            title: 笔记标题
            content: 笔记正文
            images: 图片路径列表
            tags: 标签列表
            scheduled_time: 计划发布时间
            
        Returns:
            创建的任务对象
        """
        import uuid
        
        task = ContentTask(
            task_id=str(uuid.uuid4())[:8],  # 短ID便于使用
            title=title,
            content=content,
            images=images or [],
            tags=tags or [],
            status='scheduled' if scheduled_time else 'draft',
            scheduled_time=scheduled_time,
            created_at=datetime.now()
        )
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        data = task.to_dict()
        cursor.execute('''
            INSERT INTO content_tasks 
            (task_id, title, content, images, tags, status, scheduled_time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['task_id'], data['title'], data['content'],
            data['images'], data['tags'], data['status'],
            data['scheduled_time'], data['created_at']
        ))
        
        conn.commit()
        conn.close()
        
        return task
    
    def get_task(self, task_id: str) -> Optional[ContentTask]:
        """获取单个任务"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM content_tasks WHERE task_id = ?', (task_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            columns = [desc[0] for desc in cursor.description]
            data = dict(zip(columns, row))
            return ContentTask.from_dict(data)
        return None
    
    def list_tasks(self, status: str = None, limit: int = 50) -> List[ContentTask]:
        """
        列出任务
        
        Args:
            status: 筛选状态 ('draft', 'scheduled', 'published', 'failed')
            limit: 返回数量限制
            
        Returns:
            任务列表
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT * FROM content_tasks 
                WHERE status = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT * FROM content_tasks 
                ORDER BY created_at DESC 
                LIMIT ?
            ''', (limit,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        tasks = []
        for row in rows:
            data = dict(zip(columns, row))
            tasks.append(ContentTask.from_dict(data))
        
        return tasks
    
    def get_pending_tasks(self) -> List[ContentTask]:
        """获取待发布的任务（已到发布时间）"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().isoformat()
        
        cursor.execute('''
            SELECT * FROM content_tasks 
            WHERE status = 'scheduled' 
            AND scheduled_time <= ?
            ORDER BY scheduled_time ASC
        ''', (now,))
        
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        
        tasks = []
        for row in rows:
            data = dict(zip(columns, row))
            tasks.append(ContentTask.from_dict(data))
        
        return tasks
    
    def update_task_status(self, task_id: str, status: str, 
                          error_message: str = None,
                          platform_task_id: str = None):
        """
        更新任务状态
        
        Args:
            task_id: 任务ID
            status: 新状态
            error_message: 错误信息（失败时）
            platform_task_id: 平台返回的任务ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status == 'published':
            published_at = datetime.now().isoformat()
            cursor.execute('''
                UPDATE content_tasks 
                SET status = ?, published_at = ?, platform_task_id = ?
                WHERE task_id = ?
            ''', (status, published_at, platform_task_id, task_id))
        elif status == 'failed':
            cursor.execute('''
                UPDATE content_tasks 
                SET status = ?, error_message = ?
                WHERE task_id = ?
            ''', (status, error_message, task_id))
        else:
            cursor.execute('''
                UPDATE content_tasks 
                SET status = ?
                WHERE task_id = ?
            ''', (status, task_id))
        
        conn.commit()
        conn.close()
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM content_tasks WHERE task_id = ?', (task_id,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return deleted
    
    def update_scheduled_time(self, task_id: str, scheduled_time: datetime):
        """更新任务的计划发布时间"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE content_tasks 
            SET scheduled_time = ?, status = 'scheduled'
            WHERE task_id = ?
        ''', (scheduled_time.isoformat(), task_id))
        
        conn.commit()
        conn.close()
    
    def get_statistics(self, days: int = 7) -> Dict:
        """
        获取发布统计
        
        Args:
            days: 统计最近N天
            
        Returns:
            统计信息字典
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        from datetime import timedelta
        since = (datetime.now() - timedelta(days=days)).isoformat()
        
        # 总任务数
        cursor.execute('SELECT COUNT(*) FROM content_tasks WHERE created_at >= ?', (since,))
        total = cursor.fetchone()[0]
        
        # 各状态数量
        cursor.execute('''
            SELECT status, COUNT(*) FROM content_tasks 
            WHERE created_at >= ? 
            GROUP BY status
        ''', (since,))
        status_counts = dict(cursor.fetchall())
        
        # 今日发布数
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT COUNT(*) FROM content_tasks 
            WHERE status = 'published' 
            AND published_at LIKE ?
        ''', (f'{today}%',))
        today_published = cursor.fetchone()[0]
        
        conn.close()
        
        published = status_counts.get('published', 0)
        failed = status_counts.get('failed', 0)
        scheduled = status_counts.get('scheduled', 0)
        
        success_rate = (published / (published + failed) * 100) if (published + failed) > 0 else 0
        
        return {
            'total_tasks': total,
            'published': published,
            'failed': failed,
            'scheduled': scheduled,
            'draft': status_counts.get('draft', 0),
            'success_rate': round(success_rate, 1),
            'today_published': today_published
        }


# CLI接口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='小红书内容队列管理器')
    parser.add_argument('--db', help='数据库路径')
    subparsers = parser.add_subparsers(dest='command', help='命令')
    
    # 添加任务
    add_parser = subparsers.add_parser('add', help='添加任务')
    add_parser.add_argument('--title', required=True, help='标题')
    add_parser.add_argument('--content', required=True, help='内容')
    add_parser.add_argument('--images', help='图片路径，逗号分隔')
    add_parser.add_argument('--tags', help='标签，逗号分隔')
    add_parser.add_argument('--schedule', help='计划发布时间 (ISO格式)')
    
    # 列出任务
    list_parser = subparsers.add_parser('list', help='列出任务')
    list_parser.add_argument('--status', help='筛选状态')
    list_parser.add_argument('--limit', type=int, default=20, help='数量限制')
    
    # 删除任务
    delete_parser = subparsers.add_parser('delete', help='删除任务')
    delete_parser.add_argument('task_id', help='任务ID')
    
    # 获取待发布任务
    subparsers.add_parser('pending', help='获取待发布任务')
    
    # 统计
    subparsers.add_parser('stats', help='获取统计')
    
    args = parser.parse_args()
    
    manager = QueueManager(args.db)
    
    if args.command == 'add':
        images = args.images.split(',') if args.images else []
        tags = args.tags.split(',') if args.tags else []
        schedule = datetime.fromisoformat(args.schedule) if args.schedule else None
        
        task = manager.add_task(args.title, args.content, images, tags, schedule)
        print("[OK] 任务已添加")
        print(f"   任务ID: {task.task_id}")
        print(f"   标题: {task.title}")
        print(f"   状态: {task.status}")
        if schedule:
            print(f"   计划时间: {schedule}")
    
    elif args.command == 'list':
        tasks = manager.list_tasks(args.status, args.limit)
        print(f"\n任务列表 (共{len(tasks)}条)\n")
        for task in tasks:
            status_icon = {'draft': '[草稿]', 'scheduled': '[定时]', 'published': '[已发]', 'failed': '[失败]'}
            icon = status_icon.get(task.status, '[?]')
            print(f"{icon} [{task.task_id}] {task.title}")
            print(f"   状态: {task.status}")
            if task.scheduled_time:
                print(f"   计划时间: {task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    elif args.command == 'delete':
        if manager.delete_task(args.task_id):
            print(f"[OK] 任务 {args.task_id} 已删除")
        else:
            print(f"[ERR] 任务 {args.task_id} 不存在")
    
    elif args.command == 'pending':
        tasks = manager.get_pending_tasks()
        print(f"\n待发布任务 (共{len(tasks)}条)\n")
        for task in tasks:
            print(f"[{task.task_id}] {task.title}")
            print(f"   计划时间: {task.scheduled_time.strftime('%Y-%m-%d %H:%M')}")
            print()
    
    elif args.command == 'stats':
        stats = manager.get_statistics()
        print("\n发布统计 (最近7天)\n")
        print(f"总任务数: {stats['total_tasks']}")
        print(f"已发布: {stats['published']}")
        print(f"发布失败: {stats['failed']}")
        print(f"待发布: {stats['scheduled']}")
        print(f"草稿: {stats['draft']}")
        print(f"成功率: {stats['success_rate']}%")
        print(f"今日已发布: {stats['today_published']}")
    
    else:
        parser.print_help()
