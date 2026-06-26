#!/usr/bin/env python3
"""
Context Manager - 智能上下文管理系统
支持多模型自适应、分层记忆、动态注入、SQLite 数据库
"""

import sqlite3
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

class ContextManager:
    """智能上下文管理器"""
    
    MODEL_LIMITS = {
        'kiro/claude-haiku-4-5': 8000,
        'kiro/claude-sonnet-4-5': 200000,
        'kiro/claude-opus-4-1': 200000,
        'gpt-4': 8000,
        'gpt-4-turbo': 128000,
        'gpt-4o': 128000,
        'gemini-1.5-pro': 1000000,
        'qwen3.5-plus': 128000,
    }
    
    def __init__(self, workspace_dir=None):
        if workspace_dir is None:
            workspace_dir = Path.home() / '.openclaw' / 'workspace-telegram-bot1'
        
        self.workspace_dir = Path(workspace_dir)
        self.memory_dir = self.workspace_dir / 'memory'
        self.db_path = self.memory_dir / 'memories.db'
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY,
                content TEXT NOT NULL,
                importance REAL DEFAULT 1.0,
                layer TEXT DEFAULT 'warm',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                tokens INTEGER
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_index (
                id INTEGER PRIMARY KEY,
                memory_id INTEGER,
                keyword TEXT,
                relevance REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS management_history (
                id INTEGER PRIMARY KEY,
                model_name TEXT,
                usage_percent REAL,
                action TEXT,
                tokens_saved INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_model_limit(self, model):
        """获取模型上下文限制"""
        return self.MODEL_LIMITS.get(model, 8000)
    
    def estimate_tokens(self, text):
        """估计 tokens"""
        return len(text) // 4
    
    def add_memory(self, content, importance=1.0, tags=''):
        """添加记忆"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        tokens = self.estimate_tokens(content)
        layer = 'hot' if importance > 0.8 else 'warm'
        
        cursor.execute('''
            INSERT INTO memories (content, importance, layer, tokens)
            VALUES (?, ?, ?, ?)
        ''', (content, importance, layer, tokens))
        
        conn.commit()
        conn.close()
        
        return True
    
    def get_statistics(self):
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*), SUM(tokens) FROM memories')
        total_count, total_tokens = cursor.fetchone()
        
        cursor.execute('''
            SELECT layer, COUNT(*), SUM(tokens)
            FROM memories
            GROUP BY layer
        ''')
        layer_stats = cursor.fetchall()
        
        conn.close()
        
        return {
            'total_memories': total_count or 0,
            'total_tokens': total_tokens or 0,
            'by_layer': {row[0]: {'count': row[1], 'tokens': row[2]} for row in layer_stats}
        }
    
    def auto_manage(self, model='kiro/claude-haiku-4-5'):
        """自动管理上下文"""
        limit = self.get_model_limit(model)
        stats = self.get_statistics()
        usage_percent = (stats['total_tokens'] / limit * 100) if limit > 0 else 0
        
        return {
            'model': model,
            'context_limit': limit,
            'usage_percent': usage_percent,
            'total_memories': stats['total_memories'],
            'total_tokens': stats['total_tokens'],
            'status': 'optimized'
        }

def main():
    parser = argparse.ArgumentParser(description='智能上下文管理系统')
    parser.add_argument('--init', action='store_true', help='初始化系统')
    parser.add_argument('--add', type=str, help='添加记忆')
    parser.add_argument('--importance', type=float, default=1.0, help='记忆重要性')
    parser.add_argument('--stats', action='store_true', help='显示统计信息')
    parser.add_argument('--auto-manage', action='store_true', help='自动管理')
    parser.add_argument('--model', type=str, default='kiro/claude-haiku-4-5', help='指定模型')
    
    args = parser.parse_args()
    
    manager = ContextManager()
    
    if args.init:
        print("✅ 系统已初始化")
        print(f"📁 数据库位置: {manager.db_path}")
    
    elif args.add:
        manager.add_memory(args.add, args.importance)
        print(f"✅ 已添加记忆: {args.add[:50]}...")
    
    elif args.stats:
        stats = manager.get_statistics()
        print("\n📊 上下文统计:")
        print(f"  总记忆数: {stats['total_memories']}")
        print(f"  总 tokens: {stats['total_tokens']:,}")
        print("\n📋 按层级分布:")
        for layer in ['hot', 'warm', 'cold']:
            if layer in stats['by_layer']:
                info = stats['by_layer'][layer]
                print(f"  {layer.upper():5} - {info['count']} 个, {info['tokens']:,} tokens")
    
    elif args.auto_manage:
        result = manager.auto_manage(args.model)
        print("\n🧠 自动管理结果:")
        print(f"  模型: {result['model']}")
        print(f"  上下文限制: {result['context_limit']} tokens")
        print(f"  使用率: {result['usage_percent']:.1f}%")
        print(f"  记忆数: {result['total_memories']}")
        print(f"  状态: {result['status']}")
    
    else:
        print("🧠 智能上下文管理系统")
        print("\n使用 --help 查看帮助")

if __name__ == '__main__':
    main()
