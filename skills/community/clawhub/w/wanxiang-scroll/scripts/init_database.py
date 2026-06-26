#!/usr/bin/env python3
"""
万象绘卷数据库初始化脚本 V2.0
基于完整系统文档设计的数据库结构
包含：故事、世界观、角色、事件、文风、剧情管理、代代相传等全部系统
本地 SQLite 数据库，数据存在 data/ 目录
"""

import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
STORIES_DIR = BASE_DIR / "stories"
DB_PATH = DATA_DIR / "wanxiang.db"


def init_database():
    """初始化完整数据库表结构"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ==================== 核心故事系统 ====================
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'life_simulation',
            world_type TEXT,
            style TEXT DEFAULT 'default',
            current_turn INTEGER DEFAULT 0,
            current_year INTEGER,
            current_season TEXT,
            era_name TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT 1,
            metadata TEXT,
            FOREIGN KEY (style) REFERENCES style_configs(name)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS worlds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            world_name TEXT,
            world_type TEXT NOT NULL,
            magic_system TEXT,
            races TEXT,
            nations TEXT,
            history_events TEXT,
            special_settings TEXT,
            current_era TEXT,
            current_year INTEGER DEFAULT 1,
            core_conflict TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS world_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            turn INTEGER DEFAULT 0,
            year INTEGER,
            season TEXT,
            weather TEXT,
            events TEXT,
            changes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    ''')
    
    # ==================== 角色系统 ====================
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS characters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            type TEXT DEFAULT 'npc',
            age INTEGER,
            gender TEXT,
            race TEXT,
            occupation TEXT,
            faction TEXT,
            attributes TEXT,
            skills TEXT,
            traits TEXT,
            relationships TEXT,
            background TEXT,
            status TEXT DEFAULT 'alive',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS character_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            character_id INTEGER NOT NULL,
            turn INTEGER DEFAULT 0,
            location TEXT,
            health INTEGER DEFAULT 100,
            mood TEXT,
            current_action TEXT,
            inventory TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (character_id) REFERENCES characters(id)
        )
    ''')
    
    # ==================== 事件系统 ====================
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT,
            type TEXT DEFAULT 'plot',
            importance INTEGER DEFAULT 1,
            turn INTEGER,
            year INTEGER,
            location TEXT,
            participants TEXT,
            consequences TEXT,
            foreshadowing TEXT,
            resolved BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS plot_threads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            status TEXT DEFAULT 'active',
            importance INTEGER DEFAULT 1,
            start_turn INTEGER,
            end_turn INTEGER,
            related_events TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    ''')
    
    # ==================== 文风系统 ====================
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS style_configs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT,
            category TEXT,
            rules TEXT,
            examples TEXT,
            forbidden_words TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # ==================== 代代相传系统 ====================
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS generations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            generation_num INTEGER NOT NULL,
            character_id INTEGER,
            achievements TEXT,
            legacy TEXT,
            year_start INTEGER,
            year_end INTEGER,
            summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id),
            FOREIGN KEY (character_id) REFERENCES characters(id)
        )
    ''')
    
    # ==================== 物品系统 ====================
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            type TEXT,
            rarity TEXT DEFAULT 'common',
            description TEXT,
            effects TEXT,
            location TEXT,
            owner_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id),
            FOREIGN KEY (owner_id) REFERENCES characters(id)
        )
    ''')
    
    # ==================== 日志系统 ====================
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS game_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            story_id INTEGER NOT NULL,
            turn INTEGER,
            action TEXT,
            result TEXT,
            narrative TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (story_id) REFERENCES stories(id)
        )
    ''')
    
    conn.commit()
    conn.close()
    
    print(f"数据库初始化完成: {DB_PATH}")


def seed_default_styles():
    """插入默认文风配置"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    default_styles = [
        ("default", "默认文风", "通用", "{}", "[]"),
        ("xianxia", "仙侠文风", "玄幻", 
         json.dumps({"tone": "仙气飘飘", "vocabulary": ["道友", "修为", "灵气"]}),
         json.dumps(["道友请留步", "此子不凡"])),
        ("urban", "都市文风", "现代",
         json.dumps({"tone": "轻松幽默", "vocabulary": ["老板", "公司", "项目"]}),
         json.dumps(["这个项目很重要", "老板说了算"])),
        ("wuxia", "武侠文风", "古风",
         json.dumps({"tone": "侠义豪情", "vocabulary": ["侠客", "江湖", "门派"]}),
         json.dumps(["在下江湖人士", "请多指教"])),
    ]
    
    for style in default_styles:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO style_configs 
                (name, description, category, rules, examples)
                VALUES (?, ?, ?, ?, ?)
            ''', style)
        except:
            pass
    
    conn.commit()
    conn.close()
    
    print("默认文风配置完成")


def main():
    """主入口"""
    # 确保目录存在
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    STORIES_DIR.mkdir(parents=True, exist_ok=True)
    
    # 初始化数据库
    init_database()
    
    # 插入默认数据
    seed_default_styles()
    
    print("万象绘卷数据库初始化完成!")


if __name__ == "__main__":
    main()
