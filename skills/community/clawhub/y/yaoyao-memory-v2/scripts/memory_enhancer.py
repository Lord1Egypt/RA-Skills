#!/usr/bin/env python3
"""
记忆强化模块 - v1.0.0
定期访问冷记忆，防止遗忘

功能：
1. 识别需要强化的冷记忆
2. 自动"访问"记忆（更新热度）
3. 生成强化建议
4. 支持定时任务调用
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import sys

# 添加 scripts 目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from forget_detector import ForgetDetector
from heat_tracker import HeatTracker

# 配置
COLD_DAYS_THRESHOLD = 7   # 7天以上未访问需要强化
BOOST_INTERVAL_DAYS = 3    # 每3天强化一次

class MemoryEnhancer:
    """记忆强化器"""
    
    def __init__(self):
        self.forget_detector = ForgetDetector()
        self.heat_tracker = HeatTracker()
    
    def get_boost_candidates(self) -> List[Dict]:
        """获取需要强化的候选记忆"""
        analysis = self.forget_detector.analyze()
        candidates = []
        
        # 获取冷记忆
        for mem in analysis.get("cold", []):
            if mem["days_since_modified"] >= COLD_DAYS_THRESHOLD:
                candidates.append({
                    "memory": mem,
                    "reason": f"冷记忆（{mem['days_since_modified']}天未访问）",
                    "priority": mem.get("forget_score", 0)
                })
        
        # 获取温记忆中的高遗忘风险
        for mem in analysis.get("warm", []):
            if mem.get("forget_score", 0) > 40:
                candidates.append({
                    "memory": mem,
                    "reason": f"温记忆但遗忘风险高（分数:{mem.get('forget_score', 0)}）",
                    "priority": mem.get("forget_score", 0)
                })
        
        # 按优先级排序
        candidates.sort(key=lambda x: x["priority"], reverse=True)
        
        return candidates
    
    def boost_memory(self, memory_id: str, memory_title: str = "") -> bool:
        """
        强化一条记忆（通过记录访问）
        """
        try:
            self.heat_tracker.record_access(memory_id, memory_title)
            return True
        except:
            return False
    
    def auto_boost(self, limit: int = 3) -> Dict:
        """
        自动强化（选取 top N 条）
        """
        candidates = self.get_boost_candidates()[:limit]
        
        boosted = []
        failed = []
        
        for candidate in candidates:
            mem = candidate["memory"]
            memory_id = mem.get("file", mem.get("id", ""))
            title = mem.get("title", memory_id)
            
            if self.boost_memory(memory_id, title):
                boosted.append({
                    "memory_id": memory_id,
                    "title": title,
                    "reason": candidate["reason"]
                })
            else:
                failed.append(memory_id)
        
        return {
            "boosted_count": len(boosted),
            "failed_count": len(failed),
            "boosted": boosted,
            "failed": failed
        }
    
    def should_boost(self) -> bool:
        """
        检查是否应该执行强化
        - 基于时间间隔
        """
        # 检查上次强化时间
        boost_log_file = Path.home() / ".openclaw" / "workspace" / "memory" / ".boost_log.json"
        
        if not boost_log_file.exists():
            return True
        
        try:
            log = json.loads(boost_log_file.read_text())
            last_boost = datetime.fromisoformat(log.get("last_boost", "2020-01-01"))
            days_since = (datetime.now() - last_boost).days
            
            return days_since >= BOOST_INTERVAL_DAYS
        except:
            return True
    
    def log_boost(self, result: Dict):
        """记录强化历史"""
        boost_log_file = Path.home() / ".openclaw" / "workspace" / "memory" / ".boost_log.json"
        
        try:
            log = {
                "last_boost": datetime.now().isoformat(),
                "result": result
            }
            boost_log_file.parent.mkdir(parents=True, exist_ok=True)
            boost_log_file.write_text(json.dumps(log, ensure_ascii=False))
        except:
            pass
    
    def run(self) -> Dict:
        """执行强化流程"""
        if not self.should_boost():
            return {
                "skipped": True,
                "reason": f"距离上次强化不足 {BOOST_INTERVAL_DAYS} 天"
            }
        
        result = self.auto_boost(limit=3)
        self.log_boost(result)
        
        return result
    
    def report(self) -> str:
        """生成强化报告"""
        candidates = self.get_boost_candidates()
        
        lines = [
            "📈 记忆强化报告",
            "=" * 40,
        ]
        
        if not candidates:
            lines.append("✅ 所有记忆状态良好，无需强化")
            return "\n".join(lines)
        
        lines.append(f"待强化记忆: {len(candidates)}条")
        lines.append("")
        
        for i, c in enumerate(candidates[:5], 1):
            mem = c["memory"]
            lines.append(f"{i}. {mem.get('file', mem.get('id', 'unknown'))}")
            lines.append(f"   {c['reason']}")
        
        return "\n".join(lines)


if __name__ == "__main__":
    enhancer = MemoryEnhancer()
    
    print("=== 强化候选检查 ===")
    candidates = enhancer.get_boost_candidates()
    print(f"候选数量: {len(candidates)}")
    
    print("\n=== 强化报告 ===")
    print(enhancer.report())
    
    print("\n=== 执行强化 ===")
    result = enhancer.run()
    print(f"强化结果: {result}")
