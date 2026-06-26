#!/usr/bin/env python3
"""
万象绘卷数据管理工具
提供故事、角色、世界状态等数据的 CRUD 操作
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
STORIES_DIR = BASE_DIR / "stories"
DB_PATH = DATA_DIR / "wanxiang.db"


class DatabaseManager:
    """数据库管理"""
    
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        if not self.db_path.exists():
            from init_database import init_database
            init_database()
    
    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()


class StoryManager:
    """故事管理"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
    
    def create_story(self, name: str, story_type: str = "life_simulation",
                     world_type: str = None, style: str = "default",
                     metadata: dict = None) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO stories (name, type, world_type, style, metadata)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, story_type, world_type, style, json.dumps(metadata or {})))
            conn.commit()
            story_id = cursor.lastrowid
            
            story_dir = STORIES_DIR / name
            story_dir.mkdir(parents=True, exist_ok=True)
            
            return story_id
    
    def get_story(self, story_id: int = None, name: str = None) -> Optional[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if story_id:
                cursor.execute('SELECT * FROM stories WHERE id = ?', (story_id,))
            elif name:
                cursor.execute('SELECT * FROM stories WHERE name = ?', (name,))
            else:
                return None
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_stories(self, status: str = None) -> List[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute('SELECT * FROM stories WHERE status = ?', (status,))
            else:
                cursor.execute('SELECT * FROM stories ORDER BY updated_at DESC')
            return [dict(row) for row in cursor.fetchall()]
    
    def update_story(self, story_id: int, **kwargs) -> bool:
        allowed_fields = ['name', 'type', 'world_type', 'style', 'status', 
                          'current_turn', 'current_year', 'current_season', 
                          'era_name', 'metadata']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False
        
        updates['updated_at'] = datetime.now().isoformat()
        set_clause = ', '.join(f'{k} = ?' for k in updates.keys())
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE stories SET {set_clause} WHERE id = ?',
                           list(updates.values()) + [story_id])
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_story(self, story_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM stories WHERE id = ?', (story_id,))
            conn.commit()
            return cursor.rowcount > 0


class CharacterManager:
    """角色管理"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
    
    def create_character(self, story_id: int, name: str, 
                         character_type: str = "protagonist",
                         attributes: dict = None) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO characters (story_id, name, type, attributes)
                VALUES (?, ?, ?, ?)
            ''', (story_id, name, character_type, json.dumps(attributes or {})))
            conn.commit()
            return cursor.lastrowid
    
    def get_character(self, character_id: int) -> Optional[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM characters WHERE id = ?', (character_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_characters(self, story_id: int) -> List[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM characters WHERE story_id = ?', (story_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def update_character(self, character_id: int, **kwargs) -> bool:
        allowed_fields = ['name', 'type', 'attributes', 'status']
        updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not updates:
            return False
        
        set_clause = ', '.join(f'{k} = ?' for k in updates.keys())
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'UPDATE characters SET {set_clause} WHERE id = ?',
                           list(updates.values()) + [character_id])
            conn.commit()
            return cursor.rowcount > 0
    
    def delete_character(self, character_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM characters WHERE id = ?', (character_id,))
            conn.commit()
            return cursor.rowcount > 0


class EventManager:
    """事件管理"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
    
    def create_event(self, story_id: int, title: str, description: str = "",
                     event_type: str = "plot", turn: int = None) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (story_id, title, description, type, turn)
                VALUES (?, ?, ?, ?, ?)
            ''', (story_id, title, description, event_type, turn))
            conn.commit()
            return cursor.lastrowid
    
    def get_event(self, event_id: int) -> Optional[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_events(self, story_id: int, event_type: str = None) -> List[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            if event_type:
                cursor.execute('''
                    SELECT * FROM events 
                    WHERE story_id = ? AND type = ?
                    ORDER BY turn, created_at
                ''', (story_id, event_type))
            else:
                cursor.execute('''
                    SELECT * FROM events 
                    WHERE story_id = ?
                    ORDER BY turn, created_at
                ''', (story_id,))
            return [dict(row) for row in cursor.fetchall()]
    
    def delete_event(self, event_id: int) -> bool:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
            conn.commit()
            return cursor.rowcount > 0


class StyleManager:
    """文风管理"""
    
    def __init__(self, db: DatabaseManager = None):
        self.db = db or DatabaseManager()
    
    def create_style(self, name: str, description: str = "",
                     rules: dict = None, examples: list = None) -> int:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO style_configs (name, description, rules, examples)
                VALUES (?, ?, ?, ?)
            ''', (name, description, json.dumps(rules or {}), json.dumps(examples or [])))
            conn.commit()
            return cursor.lastrowid
    
    def get_style(self, name: str) -> Optional[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM style_configs WHERE name = ?', (name,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def list_styles(self) -> List[Dict]:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM style_configs ORDER BY name')
            return [dict(row) for row in cursor.fetchall()]


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description='万象绘卷数据管理')
    parser.add_argument('command', choices=['list', 'create', 'delete', 'export'])
    parser.add_argument('--type', '-t', default='story', help='数据类型')
    parser.add_argument('--name', '-n', help='名称')
    parser.add_argument('--id', '-i', type=int, help='ID')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        if args.type == 'story':
            stories = StoryManager().list_stories()
            for s in stories:
                print(f"[{s['id']}] {s['name']} ({s['type']})")
        elif args.type == 'style':
            styles = StyleManager().list_styles()
            for s in styles:
                print(f"- {s['name']}: {s['description']}")
    
    elif args.command == 'create':
        if args.type == 'story' and args.name:
            story_id = StoryManager().create_story(args.name)
            print(f"创建故事成功: ID={story_id}")
    
    elif args.command == 'delete':
        if args.type == 'story' and args.id:
            if StoryManager().delete_story(args.id):
                print(f"删除成功: ID={args.id}")
            else:
                print(f"删除失败: ID={args.id}")
    
    print("完成!")


if __name__ == "__main__":
    main()
