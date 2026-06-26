#!/usr/bin/env python3
"""
查询预测模块 - 基于历史和行为模式预测用户查询

功能：
- 基于对话历史的查询预测
- 基于时间上下文的预测
- 基于当前记忆内容的预测
- 基于用户习惯的预测
- 多级预测缓存
"""

import sys
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from collections import Counter, defaultdict
import json

sys.path.insert(0, str(Path(__file__).parent.parent))
from paths import get_vectors_db, get_memory_base


class QueryPredictor:
    """查询预测器"""
    
    def __init__(self):
        self.db_path = get_vectors_db()
        self.memory_base = get_memory_base()
        self.cache_dir = self.memory_base / ".cache" / "predictions"
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        self.conn = None
        self._connect()
        self._init_tables()
    
    def _connect(self):
        """连接数据库"""
        if Path(self.db_path).exists():
            self.conn = sqlite3.connect(str(self.db_path))
            self.conn.row_factory = sqlite3.Row
    
    def _init_tables(self):
        """初始化预测表"""
        if not self.conn:
            return
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS query_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                predicted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                context TEXT,
                times_used INTEGER DEFAULT 1
            )
        """)
        
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS query_contexts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                context_key TEXT UNIQUE,
                related_queries TEXT,
                last_used DATETIME
            )
        """)
        
        self.conn.commit()
    
    def learn_query(self, query: str, context: Optional[str] = None):
        """学习用户查询"""
        if not self.conn or not query:
            return
        
        # 检查是否已存在
        cursor = self.conn.execute(
            "SELECT id, times_used FROM query_predictions WHERE query = ?",
            (query,)
        )
        existing = cursor.fetchone()
        
        if existing:
            self.conn.execute(
                "UPDATE query_predictions SET times_used = times_used + 1 WHERE id = ?",
                (existing['id'],)
            )
        else:
            self.conn.execute(
                "INSERT INTO query_predictions (query, context) VALUES (?, ?)",
                (query, context)
            )
        
        self.conn.commit()
    
    def predict_by_history(self, limit: int = 5) -> List[Tuple[str, float]]:
        """基于历史预测（最常用的查询）"""
        if not self.conn:
            return []
        
        cursor = self.conn.execute("""
            SELECT query, times_used
            FROM query_predictions
            ORDER BY times_used DESC, predicted_at DESC
            LIMIT ?
        """, (limit * 2,))
        
        predictions = []
        for row in cursor.fetchall():
            score = min(row['times_used'] * 0.2, 1.0)  # 分数上限1.0
            predictions.append((row['query'], score))
        
        return predictions[:limit]
    
    def predict_by_time(self) -> List[Tuple[str, float]]:
        """基于时间上下文预测"""
        if not self.conn:
            return []
        
        now = datetime.now()
        hour = now.hour
        weekday = now.weekday()
        
        predictions = []
        
        # 时间相关预测
        time_based = {
            (6, 9): [("今天的待办", 0.8), ("今日记忆", 0.7), ("早上好", 0.6)],
            (9, 12): [("当前项目", 0.8), ("工作计划", 0.7), ("项目进展", 0.6)],
            (12, 14): [("午休提醒", 0.7), ("下午安排", 0.6), ("午休", 0.5)],
            (14, 18): [("任务完成", 0.8), ("待处理事项", 0.7), ("今日总结", 0.6)],
            (18, 21): [("今日收获", 0.8), ("明天计划", 0.7), ("下班", 0.5)],
            (21, 23): [("本周总结", 0.7), ("重要决策", 0.6), ("晚安", 0.5)],
        }
        
        for (start, end), suggestions in time_based.items():
            if start <= hour < end:
                predictions.extend(suggestions)
                break
        
        # 周末 vs 工作日
        if weekday >= 5:  # 周末
            predictions.extend([("周末计划", 0.6), ("休息", 0.5)])
        else:
            predictions.extend([("工作进度", 0.7), ("会议", 0.5)])
        
        return predictions[:5]
    
    def predict_by_memories(self, limit: int = 5) -> List[Tuple[str, float]]:
        """基于记忆内容预测可能查询"""
        if not self.conn:
            return []
        
        # 获取最近的高重要性记忆
        cursor = self.conn.execute("""
            SELECT content, priority
            FROM l1_records
            WHERE priority >= 80
            ORDER BY created_time DESC
            LIMIT 20
        """)
        
        predictions = []
        keywords = []
        
        for row in cursor.fetchall():
            content = row['content']
            # 提取前几个有意义的词
            words = content.split()[:5]
            keywords.extend(words)
        
        # 统计高频词
        counter = Counter(keywords)
        for word, count in counter.most_common(limit):
            if len(word) >= 2:
                predictions.append((f"关于{word}的记忆", min(count * 0.15, 0.9)))
        
        return predictions[:limit]
    
    def predict_by_context_chain(self, last_query: str) -> List[Tuple[str, float]]:
        """基于上下文链预测（上一个查询的下一个可能）"""
        if not self.conn or not last_query:
            return []
        
        # 查找这个查询之后的常用查询
        cursor = self.conn.execute("""
            SELECT p2.query, COUNT(*) as chain_count
            FROM query_predictions p1
            JOIN (
                SELECT query, predicted_at,
                       LAG(predicted_at) OVER (ORDER BY predicted_at) as prev_time,
                       LAG(query) OVER (ORDER BY predicted_at) as prev_query
                FROM query_predictions
            ) p2 ON p1.query = p2.prev_query
            WHERE p1.query = ?
            GROUP BY p2.query
            ORDER BY chain_count DESC
            LIMIT 5
        """, (last_query,))
        
        predictions = []
        for row in cursor.fetchall():
            score = min(row['chain_count'] * 0.3, 0.9)
            predictions.append((row['query'], score))
        
        return predictions
    
    def get_combined_predictions(self, last_query: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """综合预测（结合多种策略）"""
        all_predictions = []
        seen = set()
        
        # 1. 历史预测
        for query, score in self.predict_by_history(limit):
            if query not in seen:
                all_predictions.append({
                    'query': query,
                    'score': score,
                    'source': 'history'
                })
                seen.add(query)
        
        # 2. 时间预测
        for query, score in self.predict_by_time():
            if query not in seen:
                all_predictions.append({
                    'query': query,
                    'score': score * 0.8,  # 时间预测权重稍低
                    'source': 'time'
                })
                seen.add(query)
        
        # 3. 记忆预测
        for query, score in self.predict_by_memories(limit):
            if query not in seen:
                all_predictions.append({
                    'query': query,
                    'score': score * 0.6,  # 记忆预测权重更低
                    'source': 'memory'
                })
                seen.add(query)
        
        # 4. 上下文链预测
        if last_query:
            for query, score in self.predict_by_context_chain(last_query):
                if query not in seen:
                    all_predictions.append({
                        'query': query,
                        'score': score * 1.2,  # 上下文链预测权重最高
                        'source': 'context'
                    })
                    seen.add(query)
        
        # 排序并返回 top N
        all_predictions.sort(key=lambda x: x['score'], reverse=True)
        return all_predictions[:limit]
    
    def save_prediction_cache(self):
        """保存预测缓存到磁盘"""
        predictions = self.get_combined_predictions(limit=20)
        
        cache_file = self.cache_dir / "prediction_cache.json"
        with open(cache_file, 'w') as f:
            json.dump({
                'predictions': predictions,
                'updated_at': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        return cache_file
    
    def load_prediction_cache(self) -> Optional[List[Dict]]:
        """加载预测缓存"""
        cache_file = self.cache_dir / "prediction_cache.json"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file) as f:
                data = json.load(f)
            
            # 检查缓存是否过期（1小时内有效）
            updated = datetime.fromisoformat(data['updated_at'])
            if datetime.now() - updated < timedelta(hours=1):
                return data['predictions']
        except:
            pass
        
        return None
    
    def get_smart_suggestions(self) -> str:
        """获取智能建议文本"""
        # 尝试从缓存加载
        cached = self.load_prediction_cache()
        if cached:
            predictions = cached
        else:
            predictions = self.get_combined_predictions(limit=5)
            self.save_prediction_cache()
        
        if not predictions:
            return "多和我聊天，我会学习你的查询习惯~"
        
        lines = ["# 🔮 预测查询建议", ""]
        lines.append("基于你的习惯，我猜你可能想问：")
        lines.append("")
        
        for i, p in enumerate(predictions, 1):
            emoji = {'history': '📊', 'time': '⏰', 'memory': '🧠', 'context': '🔗'}.get(p['source'], '💡')
            lines.append(f"{i}. {emoji} {p['query']}")
        
        return "\n".join(lines)
    
    def close(self):
        """关闭连接"""
        if self.conn:
            self.conn.close()


def main():
    """CLI 入口"""
    import argparse
    parser = argparse.ArgumentParser(description='查询预测')
    parser.add_argument('--learn', '-l', type=str, help='学习查询')
    parser.add_argument('--predict', '-p', action='store_true', help='预测查询')
    parser.add_argument('--history', '-H', action='store_true', help='显示历史预测')
    parser.add_argument('--time', '-t', action='store_true', help='显示时间预测')
    parser.add_argument('--cache', '-c', action='store_true', help='保存缓存')
    args = parser.parse_args()
    
    predictor = QueryPredictor()
    
    if args.learn:
        predictor.learn_query(args.learn)
        print(f"✅ 已学习：{args.learn}")
    
    elif args.history:
        predictions = predictor.predict_by_history()
        print("# 📊 基于历史的预测")
        for q, s in predictions:
            print(f"- {q} (分数: {s:.2f})")
    
    elif args.time:
        predictions = predictor.predict_by_time()
        print("# ⏰ 基于时间的预测")
        for q, s in predictions:
            print(f"- {q} (分数: {s:.2f})")
    
    elif args.cache:
        cache_file = predictor.save_prediction_cache()
        print(f"✅ 缓存已保存: {cache_file}")
    
    else:
        print(predictor.get_smart_suggestions())
    
    predictor.close()


if __name__ == '__main__':
    main()
