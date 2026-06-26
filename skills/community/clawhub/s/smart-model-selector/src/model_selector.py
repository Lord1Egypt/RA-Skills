"""
Smart Model Selector - 智能模型选择器
根据任务类型和历史反馈自动选择最优模型
"""

import sqlite3
import hashlib
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
import json


@dataclass
class TaskRecord:
    """任务记录"""
    task_text: str
    task_hash: str
    selected_model: str
    dialogue_rounds: int = 1
    user_rating: Optional[int] = None
    duration_seconds: float = 0.0
    token_consumption: int = 0
    is_completed: bool = False
    created_at: str = None
    updated_at: str = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'TaskRecord':
        return cls(**data)


class ModelSelectorDB:
    """模型选择数据库"""
    
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_path = Path(__file__).parent / 'model_selection.db'
        self.db_path = str(db_path)
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 任务记录表
        c.execute('''
            CREATE TABLE IF NOT EXISTS task_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_hash TEXT UNIQUE NOT NULL,
                task_text TEXT NOT NULL,
                selected_model TEXT NOT NULL,
                dialogue_rounds INTEGER DEFAULT 1,
                user_rating INTEGER,
                duration_seconds REAL DEFAULT 0,
                token_consumption INTEGER DEFAULT 0,
                is_completed INTEGER DEFAULT 0,
                score REAL DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # 模型统计表
        c.execute('''
            CREATE TABLE IF NOT EXISTS model_stats (
                model_id TEXT PRIMARY KEY,
                total_tasks INTEGER DEFAULT 0,
                avg_score REAL DEFAULT 0,
                avg_rounds REAL DEFAULT 0,
                last_used TEXT
            )
        ''')
        
        # 任务类型映射表
        c.execute('''
            CREATE TABLE IF NOT EXISTS task_type_mapping (
                task_type TEXT NOT NULL,
                model_id TEXT NOT NULL,
                total_tasks INTEGER DEFAULT 0,
                avg_score REAL DEFAULT 0,
                PRIMARY KEY (task_type, model_id)
            )
        ''')
        
        # 索引
        c.execute('CREATE INDEX IF NOT EXISTS idx_task_hash ON task_records(task_hash)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_model ON task_records(selected_model)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_score ON task_records(score)')
        c.execute('CREATE INDEX IF NOT EXISTS idx_task_type ON task_records(task_text)')
        
        conn.commit()
        conn.close()
    
    def save_task(self, record: TaskRecord):
        """保存任务记录"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            INSERT OR REPLACE INTO task_records 
            (task_hash, task_text, selected_model, dialogue_rounds, user_rating,
             duration_seconds, token_consumption, is_completed, score, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            record.task_hash,
            record.task_text,
            record.selected_model,
            record.dialogue_rounds,
            record.user_rating,
            record.duration_seconds,
            record.token_consumption,
            1 if record.is_completed else 0,
            self._calculate_score(record),
            record.created_at,
            record.updated_at
        ))
        
        conn.commit()
        conn.close()
    
    def get_task(self, task_hash: str) -> Optional[TaskRecord]:
        """获取任务记录"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT task_hash, task_text, selected_model, dialogue_rounds, 
                   user_rating, duration_seconds, token_consumption, is_completed,
                   created_at, updated_at
            FROM task_records
            WHERE task_hash = ?
        ''', (task_hash,))
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return TaskRecord(
                task_hash=row[0],
                task_text=row[1],
                selected_model=row[2],
                dialogue_rounds=row[3],
                user_rating=row[4],
                duration_seconds=row[5],
                token_consumption=row[6],
                is_completed=bool(row[7]),
                created_at=row[8],
                updated_at=row[9]
            )
        return None
    
    def find_similar_tasks(self, task_text: str, top_k: int = 5) -> List[TaskRecord]:
        """查找相似任务（简单关键词匹配）"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 提取关键词
        keywords = task_text.split()[:5]
        
        results = []
        for kw in keywords:
            if len(kw) < 2:
                continue
            c.execute('''
                SELECT task_hash, task_text, selected_model, dialogue_rounds,
                       user_rating, duration_seconds, token_consumption, is_completed,
                       score, created_at, updated_at
                FROM task_records
                WHERE task_text LIKE ? AND score > 0
                ORDER BY score DESC
                LIMIT ?
            ''', (f'%{kw}%', top_k))
            
            for row in c.fetchall():
                if row[0] not in [r.task_hash for r in results]:
                    results.append(TaskRecord(
                        task_hash=row[0],
                        task_text=row[1],
                        selected_model=row[2],
                        dialogue_rounds=row[3],
                        user_rating=row[4],
                        duration_seconds=row[5],
                        token_consumption=row[6],
                        is_completed=bool(row[7]),
                        created_at=row[9],
                        updated_at=row[10]
                    ))
        
        conn.close()
        return results[:top_k]
    
    def get_best_model_for_task(self, task_text: str) -> Optional[str]:
        """根据历史数据获取最优模型"""
        similar_tasks = self.find_similar_tasks(task_text, top_k=10)
        
        if not similar_tasks:
            return None
        
        # 统计各模型的平均得分
        model_scores: Dict[str, List[float]] = {}
        for task in similar_tasks:
            score = self._calculate_score(task)
            if task.selected_model not in model_scores:
                model_scores[task.selected_model] = []
            model_scores[task.selected_model].append(score)
        
        # 选择平均得分最高的模型
        best_model = None
        best_avg_score = 0
        for model, scores in model_scores.items():
            avg_score = sum(scores) / len(scores)
            if avg_score > best_avg_score:
                best_avg_score = avg_score
                best_model = model
        
        return best_model
    
    def get_model_stats(self, model_id: str) -> Dict:
        """获取模型统计信息"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute('''
            SELECT selected_model, COUNT(*) as total, AVG(score) as avg_score, 
                   AVG(dialogue_rounds) as avg_rounds
            FROM task_records
            WHERE selected_model = ?
        ''', (model_id,))
        
        row = c.fetchone()
        conn.close()
        
        if row:
            return {
                'model_id': row[0],
                'total_tasks': row[1],
                'avg_score': row[2] or 0,
                'avg_rounds': row[3] or 0
            }
        return {'model_id': model_id, 'total_tasks': 0, 'avg_score': 0, 'avg_rounds': 0}
    
    def _calculate_score(self, record: TaskRecord) -> float:
        """计算任务得分"""
        # 一轮对话 = 100 分，每多一轮 -20 分
        round_score = max(0, 100 - (record.dialogue_rounds - 1) * 20)
        
        # 用户评分加成 (1-5 分 → 0-50 分)
        rating_score = ((record.user_rating or 3) - 1) * 12.5
        
        # 完成状态加成
        completion_bonus = 20 if record.is_completed else 0
        
        # 超时扣分
        time_penalty = max(0, (record.duration_seconds - 60) / 5)
        
        return round_score + rating_score + completion_bonus - time_penalty
    
    def get_all_stats(self) -> Dict:
        """获取所有统计信息"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # 总任务数
        c.execute('SELECT COUNT(*) FROM task_records')
        total_tasks = c.fetchone()[0]
        
        # 各模型使用情况
        c.execute('''
            SELECT selected_model, COUNT(*) as count, AVG(score) as avg_score
            FROM task_records
            GROUP BY selected_model
        ''')
        model_usage = {row[0]: {'count': row[1], 'avg_score': row[2] or 0} for row in c.fetchall()}
        
        # 平均对话轮数
        c.execute('SELECT AVG(dialogue_rounds) FROM task_records')
        avg_rounds = c.fetchone()[0] or 0
        
        # 高分任务比例
        c.execute('SELECT COUNT(*) FROM task_records WHERE score >= 80')
        high_score_count = c.fetchone()[0]
        high_score_ratio = high_score_count / total_tasks if total_tasks > 0 else 0
        
        conn.close()
        
        return {
            'total_tasks': total_tasks,
            'model_usage': model_usage,
            'avg_rounds': round(avg_rounds, 2),
            'high_score_ratio': round(high_score_ratio, 2)
        }


def hash_task(text: str) -> str:
    """对任务文本 hashing"""
    return hashlib.md5(text.encode()).hexdigest()


class SmartModelSelector:
    """智能模型选择器主类"""
    
    def __init__(self, db_path: str = None):
        self.db = ModelSelectorDB(db_path)
        self.models = ['qwen3.5-plus', 'qwen-max', 'qwen-coder-plus']
        self.current_task: Optional[TaskRecord] = None
        self.default_model = 'qwen3.5-plus'
    
    def select_model(self, task_text: str) -> Tuple[str, str]:
        """
        选择最优模型
        返回：(模型 ID, 选择原因)
        """
        task_hash = hash_task(task_text)
        
        # 1. 查找是否有相同任务的历史记录
        existing = self.db.get_task(task_hash)
        if existing:
            # 如果有历史记录，用表现最好的模型
            best_model = self.db.get_best_model_for_task(task_text)
            if best_model:
                return best_model, f"基于历史数据（相似任务平均得分：{self.db.get_model_stats(best_model)['avg_score']:.1f}）"
        
        # 2. 查找相似任务
        best_model = self.db.get_best_model_for_task(task_text)
        if best_model:
            stats = self.db.get_model_stats(best_model)
            return best_model, f"基于相似任务（{stats['total_tasks']}个任务，平均得分：{stats['avg_score']:.1f}）"
        
        # 3. 使用规则引擎（冷启动）
        model, reason = self._rule_based_select(task_text)
        return model, reason
    
    def _rule_based_select(self, task_text: str) -> Tuple[str, str]:
        """基于规则的选择（冷启动）"""
        text_lower = task_text.lower()
        
        # 代码相关
        code_keywords = ['代码', '函数', 'debug', 'python', 'c++', 'java', '编程', 'write code', 
                        'function', 'class', 'import', 'def ', '实现一个', '算法']
        if any(kw in text_lower for kw in code_keywords):
            return 'qwen-coder-plus', '检测到代码相关任务'
        
        # 推理/规划相关
        reasoning_keywords = ['分析', '规划', '设计', '架构', '为什么', '比较', '评估', 
                             '方案', '策略', '优化', '怎么实现', '如何实现', 'advantage', 
                             'disadvantage', 'pros', 'cons', 'system design']
        if any(kw in text_lower for kw in reasoning_keywords):
            return 'qwen-max', '检测到复杂推理任务'
        
        # 多步骤任务
        if task_text.count('，') >= 3 or task_text.count('然后') >= 2:
            return 'qwen-max', '检测到多步骤任务'
        
        # 长文本
        if len(task_text) > 500:
            return 'qwen-max', '长文本任务需要更强模型'
        
        # 默认
        return self.default_model, '默认模型（简单任务）'
    
    def start_task(self, task_text: str, selected_model: str = None):
        """开始新任务"""
        if selected_model is None:
            selected_model, _ = self.select_model(task_text)
        
        self.current_task = TaskRecord(
            task_text=task_text,
            task_hash=hash_task(task_text),
            selected_model=selected_model
        )
        return selected_model
    
    def complete_task(self, dialogue_rounds: int = 1, user_rating: int = None, 
                     duration_seconds: float = 0, token_consumption: int = 0):
        """完成任务并记录反馈"""
        if self.current_task is None:
            return
        
        self.current_task.dialogue_rounds = dialogue_rounds
        self.current_task.user_rating = user_rating
        self.current_task.duration_seconds = duration_seconds
        self.current_task.token_consumption = token_consumption
        self.current_task.is_completed = True
        self.current_task.updated_at = datetime.now().isoformat()
        
        self.db.save_task(self.current_task)
        self.current_task = None
    
    def update_rating(self, rating: int):
        """更新用户评分"""
        if self.current_task:
            self.current_task.user_rating = rating
            self.current_task.updated_at = datetime.now().isoformat()
            self.db.save_task(self.current_task)
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        return self.db.get_all_stats()
    
    def reset(self):
        """重置当前任务"""
        self.current_task = None
