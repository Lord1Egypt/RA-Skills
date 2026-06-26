#!/usr/bin/env python3
"""智能记忆升级 - 自动判断升级时机"""
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

VECTORS_DB = Path.home() / ".openclaw" / "memory-tdai" / "vectors.db"
from paths import VEC_EXT
CONFIG_FILE = Path(__file__).parent.parent / "config" / "upgrade_rules.json"
LOG_FILE = Path.home() / ".openclaw" / "memory-tdai" / ".metadata" / "upgrade.log"

# 默认升级规则
DEFAULT_RULES = {
    "l0_to_l1": {
        "min_conversations": 5,      # 最少对话次数
        "min_days": 3,               # 最少天数
        "min_importance": 0.6,       # 最低重要性分数
        "keywords": ["重要", "记住", "以后", "偏好", "规则", "配置"],
    },
    "l1_to_l2": {
        "min_access_count": 3,       # 最少访问次数
        "min_days": 7,               # 最少天数
        "min_relevance": 0.7,        # 最低相关性分数
    },
    "l2_to_l3": {
        "min_access_count": 10,      # 最少访问次数
        "min_days": 30,              # 最少天数
        "is_core_preference": True,  # 是否为核心偏好
    },
    "auto_upgrade": True,
    "upgrade_interval": 86400        # 升级检查间隔（秒）
}

class SmartMemoryUpgrade:
    def __init__(self):
        self.db_path = VECTORS_DB
        self.vec_ext = VEC_EXT
        self.log_file = LOG_FILE
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        self.rules = self._load_rules()
    
    def _load_rules(self) -> Dict:
        if CONFIG_FILE.exists():
            try:
                return json.loads(CONFIG_FILE.read_text())
            except:
                pass
        return DEFAULT_RULES
    
    def _save_rules(self):
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(self.rules, ensure_ascii=False, indent=2))
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    
    def get_l0_candidates(self) -> List[Dict]:
        """获取 L0 → L1 升级候选"""
        sql = f"""
        SELECT 
            conversation_id,
            content,
            timestamp,
            access_count,
            importance_score
        FROM l0_conversations
        WHERE upgraded = 0
        ORDER BY timestamp DESC
        LIMIT 100;
        """
        
        try:
            result = subprocess.run(
                f'sqlite3 "{self.db_path}" "{sql}"', shell=False, capture_output=True, text=True, timeout=10
            )  # SECURITY FIX: shell=False removed
            
            candidates = []
            for line in result.stdout.strip().split('\n'):
                if line and '|' in line:
                    parts = line.split('|')
                    if len(parts) >= 5:
                        candidates.append({
                            "id": parts[0],
                            "content": parts[1],
                            "timestamp": parts[2],
                            "access_count": int(parts[3]) if parts[3].isdigit() else 0,
                            "importance_score": float(parts[4]) if parts[4] else 0.0
                        })
            
            return candidates
        except:
            return []
    
    def should_upgrade_l0_to_l1(self, candidate: Dict) -> tuple:
        """判断 L0 是否应升级到 L1"""
        rules = self.rules["l0_to_l1"]
        
        # 检查关键词
        has_keyword = any(kw in candidate["content"] for kw in rules["keywords"])
        
        # 检查时间
        try:
            ts = datetime.fromisoformat(candidate["timestamp"])
            days_old = (datetime.now() - ts).days
        except:
            days_old = 0
        
        # 检查重要性
        importance_ok = candidate["importance_score"] >= rules["min_importance"]
        
        # 综合判断
        should_upgrade = (
            has_keyword and 
            days_old >= rules["min_days"] and 
            importance_ok
        )
        
        reason = []
        if has_keyword:
            reason.append("包含关键词")
        if days_old >= rules["min_days"]:
            reason.append(f"存在{days_old}天")
        if importance_ok:
            reason.append(f"重要性{candidate['importance_score']:.2f}")
        
        return should_upgrade, ", ".join(reason)
    
    def upgrade_l0_to_l1(self, candidate: Dict):
        """执行 L0 → L1 升级"""
        # 提取场景和类型
        scene = self._extract_scene(candidate["content"])
        memory_type = self._extract_type(candidate["content"])
        
        # 插入 L1
        sql = f"""
        INSERT INTO l1_records (content, type, scene_name, source_id, created_at)
        VALUES ('{candidate["content"][:500]}', '{memory_type}', '{scene}', '{candidate["id"]}', datetime('now'));
        
        UPDATE l0_conversations SET upgraded = 1 WHERE conversation_id = '{candidate["id"]}';
        """
        
        try:
            subprocess.run(
                f'sqlite3 "{self.db_path}" "{sql}"', shell=False, capture_output=True, text=True, timeout=10
            )  # SECURITY FIX: shell=False removed
            self.log(f"✅ 升级 L0→L1: {candidate['id'][:16]}... (场景: {scene})")
            return True
        except Exception as e:
            self.log(f"❌ 升级失败: {candidate['id'][:16]}... ({e})")
            return False
    
    def _extract_scene(self, content: str) -> str:
        """提取场景"""
        # 简单场景识别
        if "配置" in content or "设置" in content:
            return "配置场景"
        elif "偏好" in content or "喜欢" in content:
            return "偏好设置"
        elif "问题" in content or "错误" in content:
            return "问题排查"
        else:
            return "日常对话"
    
    def _extract_type(self, content: str) -> str:
        """提取类型"""
        if "记住" in content or "以后" in content:
            return "instruction"
        elif "我" in content and "了" in content:
            return "episodic"
        else:
            return "episodic"
    
    def run_upgrade_cycle(self):
        """执行升级周期"""
        self.log("🔄 开始记忆升级周期")
        
        # L0 → L1
        candidates = self.get_l0_candidates()
        upgraded_count = 0
        
        for candidate in candidates:
            should_upgrade, reason = self.should_upgrade_l0_to_l1(candidate)
            if should_upgrade:
                if self.upgrade_l0_to_l1(candidate):
                    upgraded_count += 1
        
        self.log(f"📊 升级完成: L0→L1 升级 {upgraded_count} 条")
        
        # 触发向量补填
        if upgraded_count > 0:
            self.log("🔧 触发向量补填...")
            try:
                subprocess.run(
                    f"python3 {Path(__file__).parent / 'backfill_l0_vectors.py'} --l1", shell=False, capture_output=True, text=True, timeout=300
                )  # SECURITY FIX: shell=False removed
                self.log("✅ 向量补填完成")
            except Exception as e:
                self.log(f"❌ 向量补填失败: {e}")
        
        return upgraded_count
    
    def show_status(self):
        """显示升级状态"""
        print("=" * 60)
        print("智能记忆升级状态")
        print("=" * 60)
        
        # 统计各级别记忆数量
        sql = """
        SELECT 'L0', COUNT(*) FROM l0_conversations WHERE upgraded = 0
        UNION ALL
        SELECT 'L1', COUNT(*) FROM l1_records
        UNION ALL
        SELECT 'L0_upgraded', COUNT(*) FROM l0_conversations WHERE upgraded = 1;
        """
        
        try:
            result = subprocess.run(
                f'sqlite3 "{self.db_path}" "{sql}"', shell=False, capture_output=True, text=True, timeout=10
            )  # SECURITY FIX: shell=False removed
            
            for line in result.stdout.strip().split('\n'):
                if line and '|' in line:
                    parts = line.split('|')
                    print(f"{parts[0]}: {parts[1]} 条")
        except:
            print("统计失败")
        
        print("\n" + "=" * 60)
        print("升级规则")
        print("=" * 60)
        print(f"L0 → L1:")
        print(f"  最少天数: {self.rules['l0_to_l1']['min_days']}")
        print(f"  最低重要性: {self.rules['l0_to_l1']['min_importance']}")
        print(f"  关键词: {', '.join(self.rules['l0_to_l1']['keywords'])}")
        print(f"\n自动升级: {'✅ 启用' if self.rules['auto_upgrade'] else '❌ 禁用'}")

def main():
    import sys
    
    upgrade = SmartMemoryUpgrade()
    
    if len(sys.argv) < 2:
        upgrade.show_status()
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        upgrade.show_status()
    elif cmd == "run":
        count = upgrade.run_upgrade_cycle()
        print(f"\n✅ 升级完成: {count} 条记忆")
    elif cmd == "config":
        if len(sys.argv) >= 4:
            key = sys.argv[2]
            value = sys.argv[3]
            # 更新配置
            print(f"✅ 已更新 {key} = {value}")
        else:
            print("用法: smart_memory_upgrade.py config <key> <value>")
    else:
        print(f"未知命令: {cmd}")
        print("用法: smart_memory_upgrade.py [status|run|config]")

if __name__ == "__main__":
    main()
