#!/usr/bin/env python3
"""
上下文压缩代理 - 专门负责压缩对话上下文
采用分层压缩策略，基于内存使用触发机制
"""

import json
import time
import sqlite3
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import hashlib

class ContextCompactor:
    """上下文压缩代理"""
    
    def __init__(self, db_path: str = "context_compactor.db"):
        """初始化压缩代理"""
        self.db_path = db_path
        self.init_database()
        
        # 压缩配置
        self.config = {
            "hot_threshold": 10,      # HOT层消息数量
            "warm_threshold": 50,     # WARM层触发阈值
            "cold_threshold": 100,    # COLD层触发阈值
            "token_threshold": 0.7,   # token使用阈值（70%）
            "time_interval": 3600,    # 时间间隔（秒）
            
            "retain_decisions": True,     # 保留决策
            "retain_tasks": True,         # 保留任务
            "retain_preferences": True,   # 保留偏好
            "remove_chitchat": True,      # 删除闲聊
            "remove_duplicates": True     # 删除重复
        }
        
        # 状态跟踪
        self.stats = {
            "total_compactions": 0,
            "total_tokens_saved": 0,
            "last_compaction_time": None,
            "current_token_usage": 0,
            "max_token_usage": 0
        }
    
    def init_database(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 创建压缩历史表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compaction_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                layer TEXT NOT NULL,
                messages_before INTEGER,
                messages_after INTEGER,
                tokens_before INTEGER,
                tokens_after INTEGER,
                compression_ratio REAL,
                trigger_type TEXT,
                details TEXT
            )
        ''')
        
        # 创建分层数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tiered_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                layer TEXT NOT NULL,
                data_hash TEXT NOT NULL,
                content TEXT NOT NULL,
                importance_score REAL DEFAULT 0.5,
                last_accessed DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            )
        ''')
        
        # 创建索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_layer ON tiered_data(layer)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_importance ON tiered_data(importance_score)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON compaction_history(timestamp)')
        
        conn.commit()
        conn.close()
    
    def analyze_importance(self, message: Dict) -> float:
        """分析消息的重要性"""
        importance = 0.5  # 基础重要性
        
        # 决策相关
        if any(keyword in message.get("content", "").lower() for keyword in ["决定", "决策", "选择", "方案"]):
            importance += 0.3
        
        # 任务相关
        if any(keyword in message.get("content", "").lower() for keyword in ["任务", "待办", "todo", "完成"]):
            importance += 0.2
        
        # 偏好相关
        if any(keyword in message.get("content", "").lower() for keyword in ["喜欢", "偏好", "习惯", "通常"]):
            importance += 0.2
        
        # 系统相关
        if any(keyword in message.get("content", "").lower() for keyword in ["配置", "设置", "安装", "部署"]):
            importance += 0.2
        
        # 闲聊检测
        if any(keyword in message.get("content", "").lower() for keyword in ["你好", "谢谢", "再见", "哈哈"]):
            importance -= 0.1
        
        return min(max(importance, 0.1), 1.0)  # 限制在0.1-1.0之间
    
    def compress_hot_layer(self, messages: List[Dict]) -> Tuple[List[Dict], int]:
        """压缩HOT层数据"""
        compressed = []
        tokens_saved = 0
        
        for i, msg in enumerate(messages):
            importance = self.analyze_importance(msg)
            
            # 保留重要消息
            if importance >= 0.6:
                compressed.append({
                    "content": msg.get("content", ""),
                    "importance": importance,
                    "original_length": len(msg.get("content", "")),
                    "timestamp": msg.get("timestamp", datetime.now().isoformat())
                })
            else:
                # 不重要消息，进行简化
                if len(msg.get("content", "")) > 100:
                    simplified = msg.get("content", "")[:100] + "..."
                    compressed.append({
                        "content": simplified,
                        "importance": importance,
                        "original_length": len(msg.get("content", "")),
                        "timestamp": msg.get("timestamp", datetime.now().isoformat())
                    })
                    tokens_saved += len(msg.get("content", "")) - len(simplified)
        
        return compressed, tokens_saved
    
    def compress_warm_layer(self, messages: List[Dict]) -> Tuple[str, int]:
        """压缩WARM层数据，生成总结"""
        # 提取关键信息
        decisions = []
        tasks = []
        preferences = []
        
        for msg in messages:
            content = msg.get("content", "").lower()
            
            if any(keyword in content for keyword in ["决定", "决策", "选择"]):
                decisions.append(msg.get("content", ""))
            elif any(keyword in content for keyword in ["任务", "待办", "todo"]):
                tasks.append(msg.get("content", ""))
            elif any(keyword in content for keyword in ["喜欢", "偏好", "习惯"]):
                preferences.append(msg.get("content", ""))
        
        # 生成总结
        summary_parts = []
        
        if decisions:
            summary_parts.append(f"关键决策：{len(decisions)}个")
            for i, decision in enumerate(decisions[:3], 1):
                summary_parts.append(f"{i}. {decision[:50]}...")
        
        if tasks:
            summary_parts.append(f"待办任务：{len(tasks)}个")
            for i, task in enumerate(tasks[:3], 1):
                summary_parts.append(f"{i}. {task[:50]}...")
        
        if preferences:
            summary_parts.append(f"用户偏好：{len(preferences)}个")
            for i, pref in enumerate(preferences[:2], 1):
                summary_parts.append(f"{i}. {pref[:50]}...")
        
        summary = "\n".join(summary_parts)
        
        # 计算节省的token
        original_length = sum(len(msg.get("content", "")) for msg in messages)
        tokens_saved = original_length - len(summary)
        
        return summary, tokens_saved
    
    def should_compress(self, token_usage: float, message_count: int) -> Tuple[bool, str, str]:
        """判断是否需要压缩"""
        # 检查token使用
        if token_usage > self.config["token_threshold"]:
            return True, "token_threshold", "hot"
        
        # 检查消息数量
        if message_count >= self.config["cold_threshold"]:
            return True, "message_count", "cold"
        elif message_count >= self.config["warm_threshold"]:
            return True, "message_count", "warm"
        elif message_count >= self.config["hot_threshold"]:
            return True, "message_count", "hot"
        
        # 检查时间间隔
        if self.stats["last_compaction_time"]:
            time_since_last = time.time() - self.stats["last_compaction_time"]
            if time_since_last > self.config["time_interval"]:
                return True, "time_interval", "warm"
        
        return False, "", ""
    
    def compact(self, messages: List[Dict], token_usage: float) -> Dict:
        """执行压缩"""
        message_count = len(messages)
        
        # 判断是否需要压缩
        should_compress, trigger_type, layer = self.should_compress(token_usage, message_count)
        
        if not should_compress:
            return {
                "compressed": False,
                "reason": "No compression needed",
                "stats": self.stats
            }
        
        # 记录压缩前状态
        tokens_before = sum(len(msg.get("content", "")) for msg in messages)
        
        # 执行压缩
        if layer == "hot":
            compressed_messages, tokens_saved = self.compress_hot_layer(messages)
            compression_result = {
                "layer": "hot",
                "compressed_messages": compressed_messages,
                "tokens_saved": tokens_saved
            }
        elif layer == "warm":
            summary, tokens_saved = self.compress_warm_layer(messages)
            compression_result = {
                "layer": "warm",
                "summary": summary,
                "tokens_saved": tokens_saved
            }
        else:  # cold
            summary, tokens_saved = self.compress_warm_layer(messages)
            compression_result = {
                "layer": "cold",
                "summary": summary,
                "tokens_saved": tokens_saved,
                "archived": True
            }
        
        # 更新统计
        self.stats["total_compactions"] += 1
        self.stats["total_tokens_saved"] += tokens_saved
        self.stats["last_compaction_time"] = time.time()
        self.stats["current_token_usage"] = token_usage
        self.stats["max_token_usage"] = max(self.stats["max_token_usage"], token_usage)
        
        # 保存到数据库
        self.save_compaction_history(
            layer=layer,
            messages_before=message_count,
            messages_after=len(compressed_messages) if layer == "hot" else 1,
            tokens_before=tokens_before,
            tokens_after=tokens_before - tokens_saved,
            trigger_type=trigger_type
        )
        
        return {
            "compressed": True,
            "layer": layer,
            "trigger": trigger_type,
            "result": compression_result,
            "stats": self.stats
        }
    
    def save_compaction_history(self, layer: str, messages_before: int, 
                               messages_after: int, tokens_before: int, 
                               tokens_after: int, trigger_type: str):
        """保存压缩历史"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        compression_ratio = (tokens_before - tokens_after) / tokens_before if tokens_before > 0 else 0
        
        cursor.execute('''
            INSERT INTO compaction_history 
            (layer, messages_before, messages_after, tokens_before, tokens_after, 
             compression_ratio, trigger_type, details)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (layer, messages_before, messages_after, tokens_before, tokens_after,
              compression_ratio, trigger_type, json.dumps(self.stats)))
        
        conn.commit()
        conn.close()
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 获取历史统计
        cursor.execute('''
            SELECT 
                COUNT(*) as total_compactions,
                SUM(tokens_before - tokens_after) as total_tokens_saved,
                AVG(compression_ratio) as avg_compression_ratio
            FROM compaction_history
        ''')
        
        row = cursor.fetchone()
        history_stats = {
            "total_compactions": row[0] or 0,
            "total_tokens_saved": row[1] or 0,
            "avg_compression_ratio": row[2] or 0
        }
        
        conn.close()
        
        return {
            "current_stats": self.stats,
            "history_stats": history_stats,
            "config": self.config
        }
    
    def update_config(self, new_config: Dict):
        """更新配置"""
        self.config.update(new_config)
        return {"success": True, "new_config": self.config}

def main():
    """主函数"""
    compactor = ContextCompactor()
    
    print("=" * 60)
    print("上下文压缩代理已启动")
    print("=" * 60)
    print(f"配置：{json.dumps(compactor.config, indent=2, ensure_ascii=False)}")
    print("=" * 60)
    
    # 模拟测试
    test_messages = [
        {"content": "用户决定使用分层压缩策略", "timestamp": "2026-03-10T01:00:00"},
        {"content": "需要安装记忆优化技能", "timestamp": "2026-03-10T01:01:00"},
        {"content": "用户偏好使用专用压缩代理", "timestamp": "2026-03-10T01:02:00"},
        {"content": "这是一个测试消息，用于验证压缩功能", "timestamp": "2026-03-10T01:03:00"},
        {"content": "你好，今天天气不错", "timestamp": "2026-03-10T01:04:00"},
        {"content": "决定采用基于内存使用的触发机制", "timestamp": "2026-03-10T01:05:00"},
        {"content": "需要创建压缩代理的技能文件", "timestamp": "2026-03-10T01:06:00"},
        {"content": "用户习惯在晚上工作", "timestamp": "2026-03-10T01:07:00"},
        {"content": "谢谢你的帮助", "timestamp": "2026-03-10T01:08:00"},
        {"content": "配置iMessage通道只处理特定号码", "timestamp": "2026-03-10T01:09:00"}
    ]
    
    # 测试压缩
    result = compactor.compact(test_messages, token_usage=0.75)
    print(f"压缩结果：{json.dumps(result, indent=2, ensure_ascii=False)}")
    
    # 获取统计
    stats = compactor.get_stats()
    print(f"\n统计信息：{json.dumps(stats, indent=2, ensure_ascii=False)}")

if __name__ == "__main__":
    main()