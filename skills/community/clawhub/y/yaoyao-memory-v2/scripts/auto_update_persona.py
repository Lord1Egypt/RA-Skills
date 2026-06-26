#!/usr/bin/env python3
"""
用户画像自动更新 v2 - 基于记忆分析自动更新 persona.md（增强版）

增强功能：
1. 多类型记忆分析（instruction/preference/decision/habit）
2. 时间衰减权重（新记忆权重更高）
3. 增量更新（检测并更新已有偏好）
4. 偏好置信度计算
5. 智能冲突解决
6. 更新历史追踪
7. 增量 vs 全量更新模式
8. 更新频率限制
9. dry_run 模式（预览不修改）
10. 分类记忆提取策略
"""

import os
import json
import re
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import Counter

from paths import get_persona_file, get_vectors_db, get_openclaw_home

# 配置路径
CONFIG_DIR = Path(__file__).parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "persona_update.json"
LOG_FILE = get_openclaw_home() / "memory-tdai" / ".metadata" / "persona_update.log"
STATE_FILE = get_openclaw_home() / "memory-tdai" / ".metadata" / "persona_update_state.json"

# 默认配置
DEFAULT_CONFIG = {
    "update_interval": 86400,           # 更新间隔（秒）
    "min_memories_for_update": 3,       # 最少记忆数量
    "max_persona_length": 3000,         # persona.md 最大长度
    "auto_update": False,               # 默认禁用
    "require_confirmation": True,       # 需要确认
    "backup_before_update": True,        # 更新前备份
    "max_backups": 5,                   # 最多备份数
    "dry_run": True,                    # 默认 dry_run 模式
    "max_updates_per_run": 10,          # 每次最多更新条数
    "recency_weight": 0.3,              # 新鲜度权重
    "confidence_threshold": 0.6,         # 置信度阈值
    "dedup_window_hours": 24,           # 去重窗口（小时）
    "update_cooldown": 3600,            # 更新冷却时间（秒）
    "extract_types": ["instruction", "preference", "decision", "habit", "rule"],  # 提取类型
    "learned_sections": [               # 可学习章节
        "沟通偏好",
        "工作风格", 
        "技术偏好",
        "规则与约束",
        "习惯养成",
        "目标追踪"
    ]
}


class PersonaAutoUpdaterV2:
    def __init__(self):
        self.persona_file = get_persona_file()
        self.db_path = get_vectors_db()
        self.log_file = LOG_FILE
        self.state_file = STATE_FILE
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
        self.persona_content = self._load_persona()
        self.state = self._load_state()
    
    def _load_config(self) -> Dict:
        if CONFIG_FILE.exists():
            try:
                return json.loads(CONFIG_FILE.read_text())
            except:
                pass
        return DEFAULT_CONFIG.copy()
    
    def _load_persona(self) -> str:
        if self.persona_file.exists():
            return self.persona_file.read_text()
        return ""
    
    def _load_state(self) -> Dict:
        """加载更新状态"""
        if self.state_file.exists():
            try:
                return json.loads(self.state_file.read_text())
            except:
                pass
        return {
            "last_update": None,
            "last_update_attempt": None,
            "update_count": 0,
            "total_updates": 0,
            "last_changes": [],
            "pending_confirmations": []
        }
    
    def _save_state(self):
        """保存状态"""
        self.state_file.write_text(json.dumps(self.state, ensure_ascii=False, indent=2))
    
    def _can_update(self) -> Tuple[bool, str]:
        """检查是否可以更新"""
        now = datetime.now()
        
        # 检查冷却时间
        if self.state.get("last_update_attempt"):
            last_attempt = datetime.fromisoformat(self.state["last_update_attempt"])
            cooldown = self.config.get("update_cooldown", 3600)
            if (now - last_attempt).total_seconds() < cooldown:
                remaining = cooldown - (now - last_attempt).total_seconds()
                return False, f"冷却中，还需 {int(remaining)} 秒"
        
        # 检查更新间隔
        if self.state.get("last_update"):
            last_update = datetime.fromisoformat(self.state["last_update"])
            interval = self.config.get("update_interval", 86400)
            if (now - last_update).total_seconds() < interval:
                remaining = interval - (now - last_update).total_seconds()
                return False, f"间隔时间未到，还需 {int(remaining)} 秒"
        
        return True, "可以更新"
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def get_db_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        return sqlite3.connect(str(self.db_path))
    
    def close(self):
        """关闭连接"""
        pass  # sqlite3 连接在每次方法内创建和关闭
    
    def extract_memories_by_type(self, days: int = 7) -> Dict[str, List[Dict]]:
        """按类型提取记忆（带时间衰减）"""
        extract_types = self.config.get("extract_types", ["instruction", "preference"])
        
        memories_by_type = {t: [] for t in extract_types}
        memories_by_type["all"] = []
        
        conn = self.get_db_connection()
        
        for mem_type in extract_types:
            cursor = conn.execute("""
                SELECT record_id, content, type, priority, created_time
                FROM l1_records
                WHERE type = ?
                AND created_time > datetime('now', ?)
                ORDER BY priority DESC, created_time DESC
                LIMIT 50
            """, (mem_type, f'-{days} days'))
            
            for row in cursor.fetchall():
                mem = {
                    "id": row[0],
                    "content": row[1] or "",
                    "type": row[2] or "",
                    "priority": row[3] or 50,
                    "created_time": row[4] or "",
                    "age_hours": self._calc_age_hours(row[4])
                }
                memories_by_type[mem_type].append(mem)
                memories_by_type["all"].append(mem)
        
        conn.close()
        
        # 按时间排序所有记忆
        memories_by_type["all"].sort(key=lambda x: (x["priority"], -x["age_hours"]), reverse=True)
        
        return memories_by_type
    
    def _calc_age_hours(self, created_time: str) -> float:
        """计算记忆年龄（小时）"""
        if not created_time:
            return float('inf')
        try:
            created = datetime.fromisoformat(created_time.replace('Z', '+00:00'))
            return (datetime.now() - created).total_seconds() / 3600
        except:
            return float('inf')
    
    def calc_recency_weight(self, age_hours: float) -> float:
        """计算新鲜度权重（24小时内最高）"""
        if age_hours <= 1:
            return 1.0
        elif age_hours <= 24:
            return 0.9
        elif age_hours <= 72:
            return 0.7
        elif age_hours <= 168:  # 7天
            return 0.5
        else:
            return 0.3
    
    def calc_confidence(self, memory: Dict, existing_mentions: int) -> float:
        """计算偏好置信度"""
        content = memory.get("content", "")
        priority = memory.get("priority", 50) / 100.0
        recency = self.calc_recency_weight(memory.get("age_hours", 999))
        
        # 基础置信度
        confidence = 0.5
        
        # 优先级加成
        confidence += priority * 0.2
        
        # 新鲜度加成
        confidence += recency * self.config.get("recency_weight", 0.3)
        
        # 多次提及加成
        if existing_mentions > 0:
            confidence += min(0.2, existing_mentions * 0.05)
        
        # 内容长度加成（太短置信度低）
        if len(content) < 20:
            confidence *= 0.5
        elif len(content) > 100:
            confidence += 0.1
        
        return min(1.0, max(0.0, confidence))
    
    def extract_preferences_v2(self, memories: Dict[str, List[Dict]]) -> List[Dict]:
        """增强版偏好提取"""
        preferences = []
        seen_content = set()  # 去重
        
        all_memories = memories.get("all", [])
        
        for memory in all_memories:
            content = memory.get("content", "")
            if not content or len(content) < 10:
                continue
            
            # 检查是否已存在于 persona 中
            existing_mentions = self.persona_content.count(content[:50])
            
            # 计算置信度
            confidence = self.calc_confidence(memory, existing_mentions)
            
            # 检查是否低于阈值
            threshold = self.config.get("confidence_threshold", 0.6)
            if confidence < threshold:
                continue
            
            # 生成偏好摘要
            summary = self._generate_preference_summary(content, memory)
            
            if not summary:
                continue
            
            # 检查去重
            content_hash = hash(content[:50])
            if content_hash in seen_content:
                continue
            seen_content.add(content_hash)
            
            preferences.append({
                "type": memory.get("type", "unknown"),
                "content": content,
                "summary": summary,
                "confidence": confidence,
                "priority": memory.get("priority", 50),
                "age_hours": memory.get("age_hours", 999),
                "recency_weight": self.calc_recency_weight(memory.get("age_hours", 999))
            })
        
        # 按置信度排序
        preferences.sort(key=lambda x: (x["confidence"], x["priority"]), reverse=True)
        
        return preferences
    
    def _generate_preference_summary(self, content: str, memory: Dict) -> Optional[str]:
        """生成偏好摘要"""
        content = content.strip()
        if not content:
            return None
        
        # 指令类记忆
        if memory.get("type") in ["instruction", "rule"]:
            # 提取命令式句子
            if any(kw in content for kw in ["必须", "不要", "以后", "要", "记得"]):
                # 取第一句或前50字
                sentences = content.split("。")
                for s in sentences:
                    if any(kw in s for kw in ["必须", "不要", "以后", "要", "记得"]):
                        return s.strip()[:100]
                return content[:80]
        
        # 偏好类记忆
        elif memory.get("type") == "preference":
            return content[:100]
        
        # 决策类记忆
        elif memory.get("type") == "decision":
            if "决定" in content or "选择" in content:
                return content[:100]
        
        # 习惯类记忆
        elif memory.get("type") == "habit":
            if any(kw in content for kw in ["每天", "经常", "习惯", "总是"]):
                return content[:100]
        
        # 默认返回前50字
        return content[:50] if len(content) > 50 else content
    
    def detect_changes(self, new_preferences: List[Dict]) -> List[Dict]:
        """检测需要应用的变更"""
        changes = []
        max_updates = self.config.get("max_updates_per_run", 10)
        
        for pref in new_preferences[:max_updates]:
            # 检查是否已存在于 persona
            content_preview = pref["content"][:50]
            
            # 简单检查：是否在 persona 中有相似内容
            is_new = content_preview not in self.persona_content
            
            if is_new:
                changes.append({
                    "action": "add",
                    "type": pref["type"],
                    "summary": pref["summary"],
                    "confidence": pref["confidence"],
                    "priority": pref["priority"],
                    "age_hours": pref["age_hours"]
                })
        
        return changes
    
    def generate_dry_run_report(self, changes: List[Dict]) -> str:
        """生成 dry_run 报告"""
        lines = ["# 🔍 Persona 更新预览 (Dry Run)", ""]
        lines.append(f"**生成时间**：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**模式**：Dry Run（预览不修改）")
        lines.append("")
        
        if not changes:
            lines.append("✅ 无需更新，当前 persona.md 已包含所有偏好")
            return "\n".join(lines)
        
        lines.append(f"📝 共 {len(changes)} 条待应用变更：\n")
        
        for i, change in enumerate(changes, 1):
            lines.append(f"**{i}. [{change['type']}]**")
            lines.append(f"   内容：{change['summary'][:80]}...")
            lines.append(f"   置信度：{change['confidence']:.0%} | 优先级：{change['priority']} | 年龄：{change['age_hours']:.0f}h")
            lines.append("")
        
        lines.append("-" * 40)
        lines.append("💡 要应用这些变更，请运行：")
        lines.append("   `python3 auto_update_persona.py apply`")
        
        return "\n".join(lines)
    
    def apply_changes(self, changes: List[Dict]) -> bool:
        """应用变更"""
        if not changes:
            self.log("无变更，跳过")
            return True
        
        # 确认
        if self.config.get("require_confirmation", True):
            print("\n" + "=" * 60)
            print(f"⚠️ 即将应用 {len(changes)} 条变更到 persona.md")
            print("=" * 60)
            response = input("确认应用？(y/N): ").strip().lower()
            if response != 'y':
                self.log("用户取消")
                return False
        
        # 备份
        if self.config.get("backup_before_update", True):
            self.backup_persona()
        
        # 构建更新内容
        update_lines = [f"\n### 自动更新 {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"]
        
        for change in changes:
            update_lines.append(f"- **[{change['type']}]** {change['summary'][:100]}")
        
        # 插入更新
        new_content = self.persona_content
        
        if "### 自动更新" in new_content:
            # 插入到第一个自动更新之前
            parts = new_content.split("### 自动更新", 1)
            new_content = parts[0] + "\n".join(update_lines) + "\n### 自动更新" + parts[1]
        else:
            new_content += "\n" + "\n".join(update_lines)
        
        # 压缩
        if len(new_content) > self.config.get("max_persona_length", 3000):
            new_content = self._compress_persona(new_content)
        
        # 保存
        self.persona_file.write_text(new_content)
        self.persona_content = new_content
        
        # 更新状态
        self.state["last_update"] = datetime.now().isoformat()
        self.state["update_count"] += 1
        self.state["total_updates"] += len(changes)
        self.state["last_changes"] = [c["summary"][:50] for c in changes[:5]]
        self._save_state()
        
        self.log(f"✅ 已应用 {len(changes)} 条变更")
        return True
    
    def backup_persona(self):
        """备份 persona.md"""
        if not self.persona_file.exists():
            return
        
        backup_dir = self.persona_file.parent / ".persona_backups"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"persona_{timestamp}.md"
        
        import shutil
        shutil.copy2(self.persona_file, backup_path)
        
        # 清理旧备份
        backups = sorted(backup_dir.glob("persona_*.md"))
        while len(backups) > self.config.get("max_backups", 5):
            backups[0].unlink()
            backups = backups[1:]
        
        self.log(f"✅ 备份: {backup_path}")
    
    def _compress_persona(self, content: str) -> str:
        """压缩 persona"""
        lines = content.split('\n')
        compressed = []
        current_length = 0
        max_len = self.config.get("max_persona_length", 3000)
        
        for line in lines:
            if current_length + len(line) + 1 <= max_len:
                compressed.append(line)
                current_length += len(line) + 1
            else:
                break
        
        return '\n'.join(compressed) + "\n\n... (已压缩)"
    
    def run_update_cycle(self, dry_run: bool = None) -> bool:
        """执行更新周期"""
        # 检查是否启用
        if not self.config.get("auto_update", False):
            self.log("⚠️ 自动更新未启用")
            print("⚠️ 自动更新未启用")
            return False
        
        # 检查能否更新
        can_update, msg = self._can_update()
        if not can_update:
            self.log(f"⚠️ {msg}")
            print(f"⚠️ {msg}")
            return False
        
        self.state["last_update_attempt"] = datetime.now().isoformat()
        
        # 提取记忆
        memories = self.extract_memories_by_type(days=7)
        
        if len(memories["all"]) < self.config.get("min_memories_for_update", 3):
            self.log(f"记忆不足: {len(memories['all'])} < {self.config['min_memories_for_update']}")
            return False
        
        # 提取偏好
        preferences = self.extract_preferences_v2(memories)
        
        # 检测变更
        changes = self.detect_changes(preferences)
        
        if not changes:
            self.log("无新变更")
            return True
        
        # Dry run 或应用
        if dry_run is None:
            dry_run = self.config.get("dry_run", True)
        
        if dry_run:
            print(self.generate_dry_run_report(changes))
            return True
        else:
            return self.apply_changes(changes)
    
    def show_status(self):
        """显示状态"""
        print("=" * 60)
        print("用户画像自动更新 v2 状态")
        print("=" * 60)
        print(f"persona.md: {self.persona_file}")
        print(f"当前长度: {len(self.persona_content)} 字符")
        print(f"最大长度: {self.config.get('max_persona_length', 3000)} 字符")
        print(f"自动更新: {'✅ 启用' if self.config.get('auto_update', False) else '❌ 禁用'}")
        print(f"Dry Run: {'✅ 开启' if self.config.get('dry_run', True) else '❌ 关闭'}")
        print(f"需要确认: {'✅ 是' if self.config.get('require_confirmation', True) else '❌ 否'}")
        print(f"更新间隔: {self.config.get('update_interval', 86400)} 秒")
        print(f"置信度阈值: {self.config.get('confidence_threshold', 0.6):.0%}")
        print(f"提取类型: {', '.join(self.config.get('extract_types', []))}")
        print("")
        
        # 更新状态
        if self.state.get("last_update"):
            last = datetime.fromisoformat(self.state["last_update"])
            print(f"上次更新: {last.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            print("从未更新")
        
        print(f"更新次数: {self.state.get('update_count', 0)}")
        print(f"累计变更: {self.state.get('total_updates', 0)} 条")
        
        if self.state.get("last_changes"):
            print("\n最近变更：")
            for c in self.state["last_changes"][:3]:
                print(f"  - {c[:50]}...")


def main():
    import sys
    
    updater = PersonaAutoUpdaterV2()
    
    if len(sys.argv) < 2:
        updater.show_status()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        updater.show_status()
    
    elif cmd == "preview":
        updater.run_update_cycle(dry_run=True)
    
    elif cmd == "run":
        updater.run_update_cycle(dry_run=False)
    
    elif cmd == "apply":
        # 强制应用（跳过 dry_run）
        if "dry_run" in updater.config:
            updater.config["dry_run"] = False
        updater.run_update_cycle(dry_run=False)
    
    elif cmd == "enable":
        updater.config["auto_update"] = True
        updater.config["dry_run"] = False
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(updater.config, ensure_ascii=False, indent=2))
        print("✅ 已启用自动更新")
    
    elif cmd == "disable":
        updater.config["auto_update"] = False
        CONFIG_FILE.parent.mkdir(exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(updater.config, ensure_ascii=False, indent=2))
        print("✅ 已禁用自动更新")
    
    elif cmd == "show":
        print(updater.persona_content)
    
    else:
        print(f"未知命令: {cmd}")
        print("用法: auto_update_persona.py [status|preview|run|apply|enable|disable|show]")


if __name__ == "__main__":
    main()
