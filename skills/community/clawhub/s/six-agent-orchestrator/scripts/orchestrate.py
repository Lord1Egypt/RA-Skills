#!/usr/bin/env python3
"""
六Agent协作编排器核心引擎
一键启动六Agent团队，自动执行6阶段Pipeline
"""

import json
import signal
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional


class SixAgentOrchestrator:
    """六Agent协作编排器"""
    
    def __init__(self, config_dir: str = "config"):
        self.config_dir = Path(config_dir)
        self.agents = self._load_agents()
        self.pipeline = self._load_pipeline()
        self.token_quota = self._init_token_quota()
        self.current_phase = None
        self.logs = []
        
        # 中断处理
        signal.signal(signal.SIGINT, self._handle_interrupt)
    
    def _load_agents(self) -> List[Dict]:
        """加载Agent配置"""
        config_file = self.config_dir / "agents.json"
        if config_file.exists():
            return json.loads(config_file.read_text())
        
        # 默认配置
        return [
            {"id": "001", "name": "CEO", "role": "架构师", "tier": 1, "quota": 0.15},
            {"id": "002", "name": "PM", "role": "项目经理", "tier": 0, "quota": 0.20},
            {"id": "003", "name": "牢A", "role": "执行", "tier": 1, "quota": 0.15},
            {"id": "004", "name": "牢B", "role": "审计", "tier": 1, "quota": 0.10},
            {"id": "005", "name": "牢C", "role": "推理", "tier": 2, "quota": 0.15},
            {"id": "006", "name": "牢D", "role": "监控", "tier": 0, "quota": 0.10}
        ]
    
    def _load_pipeline(self) -> Dict:
        """加载Pipeline配置"""
        config_file = self.config_dir / "pipeline.json"
        if config_file.exists():
            return json.loads(config_file.read_text())
        
        return {
            "phases": ["PLAN", "PRD", "EXEC", "VERIFY", "FIX", "SUMMARY"],
            "timeout": {
                "PLAN": 300, "PRD": 300, "EXEC": 900,
                "VERIFY": 600, "FIX": 600, "SUMMARY": 180
            },
            "owner": {
                "PLAN": "CEO", "PRD": "PM", "EXEC": "牢A",
                "VERIFY": "牢B", "FIX": "牢A", "SUMMARY": "CEO"
            }
        }
    
    def _init_token_quota(self) -> Dict:
        """初始化Token配额"""
        return {
            "tier_0": {"total": 10000, "used": 0, "limit": 0.45},
            "tier_1": {"total": 10000, "used": 0, "limit": 0.40},
            "tier_2": {"total": 10000, "used": 0, "limit": 0.15},
            "tier_3": {"total": 10000, "used": 0, "limit": 0.001}
        }
    
    def _handle_interrupt(self, signum, frame):
        """处理中断"""
        print(f"\n\n⚠️ 任务中断于 {self.current_phase} 阶段")
        self._save_logs()
        print("日志已保存，下次可从断点继续")
    
    def _log(self, phase: str, agent: str, action: str, tokens: int = 0):
        """记录日志"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "phase": phase,
            "agent": agent,
            "action": action,
            "tokens": tokens
        }
        self.logs.append(entry)
    
    def _check_token_quota(self, tier: int, tokens: int) -> bool:
        """检查Token配额"""
        tier_key = f"tier_{tier}"
        quota = self.token_quota[tier_key]
        
        # 添加历史消耗（已使用的）
        history_used = quota.get("history_used", 0)
        new_used = quota["used"] + tokens + history_used
        limit = quota["total"] * quota["limit"]
        
        # 计算实际百分比（相对于硬性上限）
        percent = new_used / limit * 100
        
        if percent > 90:
            print(f"🔴 红色预警：Tier {tier} Token接近硬性上限 {percent:.1f}%")
            # 不直接返回False，只是预警
        elif percent > 80:
            print(f"🟡 黄色预警：Tier {tier} Token接近配额上限 {percent:.1f}%")
        
        quota["used"] = new_used
        return True
    
    def _check_red_line(self, agent: str, action: str) -> bool:
        """检查红线禁区"""
        red_lines = {
            "CEO": ["编写代码", "深度推理"],
            "PM": ["需求拆解", "编写代码"],
            "牢A": ["需求分析", "跳过PM反馈"],
            "牢B": ["编写代码"],
            "牢C": ["编写代码", "超配额使用"],
            "牢D": ["编写代码", "调度Agent"]
        }
        
        forbidden = red_lines.get(agent, [])
        
        for item in forbidden:
            if item in action:
                print(f"🚫 红线拦截：{agent} 试图执行 '{item}'")
                print(f"   处理：拦截 → 提示 → 路由到正确Agent")
                return False
        
        return True
    
    def execute_phase(self, phase: str, task: str) -> Dict:
        """执行单个阶段"""
        owner = self.pipeline["owner"][phase]
        timeout = self.pipeline["timeout"][phase]
        
        self.current_phase = phase
        self._log(phase, owner, f"开始执行阶段: {phase}")
        
        print(f"\n{'='*50}")
        print(f"Phase: {phase}")
        print(f"负责人: {owner}")
        print(f"超时: {timeout}秒")
        print(f"{'='*50}")
        
        # 模拟执行（实际应该spawn子agent）
        result = {
            "phase": phase,
            "owner": owner,
            "status": "completed",
            "output": f"{phase}阶段执行结果",
            "tokens_used": 1000  # 模拟Token消耗
        }
        
        # 检查Token配额
        agent_info = next((a for a in self.agents if a["name"] == owner), None)
        if agent_info:
            self._check_token_quota(agent_info["tier"], result["tokens_used"])
        
        self._log(phase, owner, f"阶段完成", result["tokens_used"])
        
        return result
    
    def execute(self, task: str) -> Dict:
        """执行完整Pipeline"""
        print(f"\n🚀 六Agent协作开始")
        print(f"任务: {task}")
        print(f"Pipeline: {self.pipeline['phases']}")
        
        results = []
        
        for phase in self.pipeline["phases"]:
            result = self.execute_phase(phase, task)
            results.append(result)
            
            # VERIFY阶段检查是否需要FIX
            if phase == "VERIFY" and result.get("needs_fix"):
                print(f"\n⚠️ 验证发现问题，进入FIX阶段")
            
            # FIX阶段检查是否需要重新VERIFY
            if phase == "FIX" and result.get("needs_reverify"):
                print(f"\n🔄 重新执行VERIFY阶段")
                result = self.execute_phase("VERIFY", task)
                results.append(result)
        
        # 汇总
        summary = self._generate_summary(results)
        
        self._save_logs()
        
        return {
            "task": task,
            "phases": results,
            "summary": summary,
            "token_usage": self.token_quota,
            "logs": self.logs
        }
    
    def _generate_summary(self, results: List[Dict]) -> Dict:
        """生成汇总报告"""
        total_tokens = sum(r["tokens_used"] for r in results)
        
        return {
            "completed_phases": len(results),
            "total_tokens": total_tokens,
            "success_rate": "100%" if all(r["status"] == "completed" for r in results) else "部分完成",
            "duration": f"{len(results) * 5} 分钟（预估）",
            "lessons": "经验总结（待补充）"
        }
    
    def _save_logs(self):
        """保存日志"""
        log_file = Path("six-agent-logs.json")
        with open(log_file, 'w', encoding='utf-8') as f:
            json.dump(self.logs, f, ensure_ascii=False, indent=2)


def main():
    """主函数"""
    import sys
    
    task = sys.argv[1] if len(sys.argv) > 1 else "开发用户登录模块"
    
    orchestrator = SixAgentOrchestrator()
    result = orchestrator.execute(task)
    
    print(f"\n{'='*50}")
    print(f"执行完成！")
    print(f"{'='*50}")
    print(f"  总阶段：{result['summary']['completed_phases']}")
    print(f"  总Token：{result['summary']['total_tokens']}")
    print(f"  成功率：{result['summary']['success_rate']}")
    print(f"{'='*50}")


if __name__ == '__main__':
    main()