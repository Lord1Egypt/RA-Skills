#!/usr/bin/env python3
"""
超脑向量记忆模块
使用ChromaDB实现语义搜索
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

# ChromaDB 路径
VECTOR_DB_PATH = Path.home() / '.openclaw' / 'super-brain-vectors'
DB_PATH = Path.home() / '.openclaw' / 'super-brain.db'

# 尝试导入ChromaDB
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print('⚠️ ChromaDB未安装，使用降级模式')


class VectorMemory:
    """向量记忆管理器"""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.client = None
        self.collection = None
        
        if CHROMADB_AVAILABLE:
            self._init_chromadb()
    
    def _init_chromadb(self):
        """初始化ChromaDB"""
        try:
            self.client = chromadb.PersistentClient(
                path=str(VECTOR_DB_PATH),
                settings=Settings(anonymized_telemetry=False)
            )
            self.collection = self.client.get_or_create_collection(
                name=f'memory_{self.user_id[:8]}',
                metadata={'user_id': self.user_id}
            )
        except Exception as e:
            print(f'⚠️ ChromaDB初始化失败: {e}')
            self.client = None
            self.collection = None
    
    def add_memory(self, text, metadata=None):
        """添加记忆到向量库"""
        if not self.collection:
            # 降级：只存储到SQLite
            return self._add_to_sqlite(text, metadata)
        
        try:
            memory_id = f'mem-{datetime.now().strftime("%Y%m%d%H%M%S")}'
            
            self.collection.add(
                documents=[text],
                metadatas=[metadata or {}],
                ids=[memory_id]
            )
            
            return memory_id
        except Exception as e:
            print(f'⚠️ 添加向量记忆失败: {e}')
            return self._add_to_sqlite(text, metadata)
    
    def _add_to_sqlite(self, text, metadata):
        """降级：存储到SQLite"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        memory_id = f'mem-{datetime.now().strftime("%Y%m%d%H%M%S")}'
        
        cursor.execute('''
            INSERT INTO conversation_insights 
            (id, user_id, session_id, topic, key_facts, user_mood, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', [
            memory_id,
            self.user_id,
            f'session-{datetime.now().strftime("%Y%m%d")}',
            metadata.get('topic', 'general') if metadata else 'general',
            json.dumps({'text': text}),
            'neutral',
            datetime.now().isoformat()
        ])
        
        conn.commit()
        conn.close()
        
        return memory_id
    
    def search_memory(self, query, n_results=5):
        """语义搜索记忆"""
        if not self.collection:
            # 降级：关键词搜索SQLite
            return self._search_sqlite(query, n_results)
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            return {
                'ids': results['ids'][0] if results['ids'] else [],
                'documents': results['documents'][0] if results['documents'] else [],
                'metadatas': results['metadatas'][0] if results['metadatas'] else [],
                'distances': results['distances'][0] if results['distances'] else []
            }
        except Exception as e:
            print(f'⚠️ 向量搜索失败: {e}')
            return self._search_sqlite(query, n_results)
    
    def _search_sqlite(self, query, limit):
        """降级：SQLite关键词搜索"""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # 简单的关键词匹配
        keywords = query.split()[:3]  # 取前3个关键词
        like_conditions = ' OR '.join([f'key_facts LIKE ?' for _ in keywords])
        params = [f'%{kw}%' for kw in keywords] + [self.user_id]
        
        cursor.execute(f'''
            SELECT id, topic, key_facts, timestamp 
            FROM conversation_insights 
            WHERE ({like_conditions}) AND user_id = ?
            ORDER BY timestamp DESC 
            LIMIT ?
        ''', params + [limit])
        
        rows = cursor.fetchall()
        conn.close()
        
        return {
            'ids': [row['id'] for row in rows],
            'documents': [row['key_facts'] for row in rows],
            'metadatas': [{'topic': row['topic']} for row in rows],
            'distances': [0.5] * len(rows)  # 固定距离
        }
    
    def get_stats(self):
        """获取记忆统计"""
        if self.collection:
            return {
                'count': self.collection.count(),
                'backend': 'chromadb'
            }
        else:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM conversation_insights WHERE user_id = ?', 
                          [self.user_id])
            count = cursor.fetchone()[0]
            conn.close()
            
            return {
                'count': count,
                'backend': 'sqlite'
            }


def remember_conversation(user_id, user_msg, ai_msg, topic='general'):
    """记住一次对话"""
    memory = VectorMemory(user_id)
    
    # 合并对话内容
    text = f'用户: {user_msg}\nAI: {ai_msg}'
    
    memory_id = memory.add_memory(text, {
        'topic': topic,
        'timestamp': datetime.now().isoformat(),
        'type': 'conversation'
    })
    
    return memory_id


def recall_similar(user_id, query, n=5):
    """回忆相似对话"""
    memory = VectorMemory(user_id)
    results = memory.search_memory(query, n)
    
    return results


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print('用法:')
        print('  添加记忆: python vector_memory.py <user_id> add "<text>"')
        print('  搜索记忆: python vector_memory.py <user_id> search "<query>"')
        print('  查看统计: python vector_memory.py <user_id> stats')
        sys.exit(1)
    
    user_id = sys.argv[1]
    action = sys.argv[2]
    
    memory = VectorMemory(user_id)
    
    if action == 'add':
        text = sys.argv[3] if len(sys.argv) > 3 else 'test'
        memory_id = memory.add_memory(text)
        print(f'✅ 已添加记忆: {memory_id}')
        
    elif action == 'search':
        query = sys.argv[3] if len(sys.argv) > 3 else 'test'
        results = memory.search_memory(query)
        print(f'🔍 找到 {len(results["ids"])} 条相关记忆:')
        for i, doc in enumerate(results['documents']):
            print(f'  {i+1}. {doc[:100]}...')
            
    elif action == 'stats':
        stats = memory.get_stats()
        print(f'📊 记忆统计:')
        print(f'  后端: {stats["backend"]}')
        print(f'  数量: {stats["count"]}')
