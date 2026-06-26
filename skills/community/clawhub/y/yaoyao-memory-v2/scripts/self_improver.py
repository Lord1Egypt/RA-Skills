#!/usr/bin/env python3
"""自我改进器 - 根据运行数据自动优化
功能：
1. 分析性能瓶颈
2. 优化缓存策略
3. 调整路由决策
4. 自动改进配置
"""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List

class SelfImprover:
    """自我改进器"""
    
    def __init__(self, config_dir: Path = None):
        self.config_dir = config_dir or (Path.home() / ".openclaw" / "workspace" / "skills" / "yaoyao-memory" / "config")
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.learning_file = self.config_dir / "learning.json"
        self.load_learning()
    
    def load_learning(self):
        """加载历史学习数据"""
        if self.learning_file.exists():
            self.learning = json.loads(self.learning_file.read_text())
        else:
            self.learning = {
                "slow_queries": [],
                "optimizations": [],
                "cache_hints": {}
            }
    
    def save_learning(self):
        """保存学习数据"""
        self.learning_file.write_text(json.dumps(self.learning, indent=2))
    
    def record_slow_query(self, query: str, elapsed_ms: float, method: str):
        """记录慢查询"""
        if elapsed_ms > 50:  # 超过 50ms 记录
            self.learning["slow_queries"].append({
                "query": query,
                "elapsed_ms": elapsed_ms,
                "method": method,
                "timestamp": datetime.now().isoformat()
            })
            
            # 只保留最近 100 条
            self.learning["slow_queries"] = self.learning["slow_queries"][-100:]
            
            # 生成缓存提示
            self._generate_cache_hint(query)
    
    def _generate_cache_hint(self, query: str):
        """生成缓存提示"""
        # 短查询更值得缓存
        if len(query) < 20:
            key = query[:10]
            self.learning["cache_hints"][key] = {
                "suggestion": "high_priority_cache",
                "query": query
            }
    
    def get_optimization_suggestions(self) -> List[Dict]:
        """获取优化建议"""
        suggestions = []
        
        # 分析慢查询
        if self.learning["slow_queries"]:
            recent = [q for q in self.learning['slow_queries']]
            if recent:
                avg_time = sum(q["elapsed_ms"] for q in recent) / len(recent)
                if avg_time > 100:
                    suggestions.append({
                        "type": "performance",
                        "priority": "high",
                        "description": f"平均查询时间 {avg_time:.0f}ms 过高",
                        "action": "考虑增加缓存预热"
                    })
        
        # 缓存命中率分析
        cache_hints = self.learning.get("cache_hints", {})
        if len(cache_hints) > 10:
            suggestions.append({
                "type": "cache",
                "priority": "medium",
                "description": f"发现 {len(cache_hints)} 个可优化的缓存查询",
                "action": "预加载高频查询"
            })
        
        return suggestions
    
    def apply_optimization(self, optimization: Dict):
        """应用优化"""
        self.learning["optimizations"].append({
            **optimization,
            "applied_at": datetime.now().isoformat()
        })
        self.save_learning()
    
    def get_stats(self) -> str:
        """获取统计"""
        slow_count = len(self.learning["slow_queries"])
        cache_hints = len(self.learning.get("cache_hints", {}))
        optimizations = len(self.learning["optimizations"])
        
        return f"""自我改进统计:
- 慢查询记录: {slow_count}
- 缓存提示: {cache_hints}
- 已应用优化: {optimizations}"""


if __name__ == "__main__":
    improver = SelfImprover()
    
    # 模拟记录
    improver.record_slow_query("系统配置查询", 120, "auto")
    improver.record_slow_query("用户偏好分析", 80, "vector")
    
    # 获取建议
    suggestions = improver.get_optimization_suggestions()
    print(f"发现 {len(suggestions)} 条优化建议")
    
    for s in suggestions:
        print(f"  [{s['priority']}] {s['description']}")
    
    print(f"\n{improver.get_stats()}")
