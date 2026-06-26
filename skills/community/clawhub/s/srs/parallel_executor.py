#!/usr/bin/env python3
"""
并行任务执行器
同时启动多个独立子任务，充分利用系统资源
"""

import subprocess
import threading
import time
import json
from pathlib import Path
from datetime import datetime

class ParallelExecutor:
    """并行任务执行器"""
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.tasks = {
            "T1": {
                "name": "架构设计",
                "owner": "skill_developer",
                "script": "tasks/run_T1_architecture.py",
                "priority": "high",
                "status": "pending"
            },
            "T2": {
                "name": "SKILL.md 草案",
                "owner": "skill_developer",
                "script": "tasks/run_T2_skill_draft.py",
                "priority": "high",
                "depends": ["T1"],
                "status": "pending"
            },
            "T3": {
                "name": "工具验证",
                "owner": "security_researcher",
                "script": "tasks/run_T3_tool_validation.py",
                "priority": "medium",
                "status": "pending"
            },
            "T4": {
                "name": "腾讯规则研究",
                "owner": "security_researcher",
                "script": "tasks/run_T4_tencent_rules.py",
                "priority": "medium",
                "status": "pending"
            },
            "T5": {
                "name": "测试策略",
                "owner": "qa_engineer",
                "script": "tasks/run_T5_test_strategy.py",
                "priority": "low",
                "depends": ["T2", "T3"],
                "status": "pending"
            }
        }
        self.results_dir = Path(f"coordination/results/{task_id}")
        self.results_dir.mkdir(parents=True, exist_ok=True)
    
    def start_task(self, task_id: str):
        """启动单个任务"""
        task = self.tasks[task_id]
        print(f"🚀 启动任务 {task_id}: {task['name']} (执行者：{task['owner']})")
        
        # 记录开始时间
        task["start_time"] = datetime.now().isoformat()
        task["status"] = "running"
        
        # 启动子进程
        process = subprocess.Popen(
            ["python3", task["script"]],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        task["process"] = process
        
        return process
    
    def wait_task(self, task_id: str):
        """等待任务完成"""
        task = self.tasks[task_id]
        process = task.get("process")
        
        if not process:
            return
        
        stdout, stderr = process.communicate()
        task["end_time"] = datetime.now().isoformat()
        task["status"] = "completed" if process.returncode == 0 else "failed"
        task["duration"] = (
            datetime.fromisoformat(task["end_time"]) - 
            datetime.fromisoformat(task["start_time"])
        ).total_seconds()
        
        # 保存结果
        result_file = self.results_dir / f"{task_id}_result.json"
        with open(result_file, 'w', encoding='utf-8') as f:
            json.dump({
                "task_id": task_id,
                "name": task["name"],
                "status": task["status"],
                "duration_seconds": task["duration"],
                "owner": task["owner"]
            }, f, indent=2, ensure_ascii=False)
        
        print(f"{'✅' if task['status'] == 'completed' else '❌'} "
              f"任务 {task_id} 完成 (耗时：{task['duration']:.1f}s)")
    
    def can_start(self, task_id: str):
        """检查任务是否可以启动 (依赖检查)"""
        task = self.tasks[task_id]
        depends = task.get("depends", [])
        
        for dep_id in depends:
            if self.tasks[dep_id]["status"] != "completed":
                return False
        return True
    
    def run_parallel(self):
        """并行执行所有任务"""
        print(f"🎯 开始并行执行任务：{self.task_id}")
        print("=" * 60)
        
        threads = []
        
        # 第一轮：启动无依赖任务 (T1, T3, T4)
        print("\n📍 第一轮：启动无依赖任务")
        for tid in ["T1", "T3", "T4"]:
            self.start_task(tid)
            t = threading.Thread(target=self.wait_task, args=(tid,))
            t.start()
            threads.append(t)
        
        # 等待第一轮完成
        for t in threads[:3]:
            t.join()
        
        # 第二轮：启动 T2 (依赖 T1)
        print("\n📍 第二轮：启动 T2 (依赖 T1)")
        if self.can_start("T2"):
            self.start_task("T2")
            t2 = threading.Thread(target=self.wait_task, args=("T2",))
            t2.start()
            threads.append(t2)
        
        # 第三轮：启动 T5 (依赖 T2, T3)
        print("\n📍 第三轮：启动 T5 (依赖 T2, T3)")
        # 等待 T2 完成
        if "t2" in locals():
            t2.join()
        
        if self.can_start("T5"):
            self.start_task("T5")
            t5 = threading.Thread(target=self.wait_task, args=("T5",))
            t5.start()
            threads.append(t5)
            t5.join()
        
        # 等待所有任务完成
        for t in threads:
            t.join()
        
        # 生成总结报告
        self.generate_summary()
    
    def generate_summary(self):
        """生成执行总结报告"""
        print("\n" + "=" * 60)
        print("📊 任务执行总结")
        print("=" * 60)
        
        total_duration = 0
        completed = 0
        failed = 0
        
        for tid, task in self.tasks.items():
            status = task.get("status", "unknown")
            duration = task.get("duration", 0)
            total_duration += duration
            
            if status == "completed":
                completed += 1
                emoji = "✅"
            elif status == "failed":
                failed += 1
                emoji = "❌"
            else:
                emoji = "⏳"
            
            print(f"{emoji} {tid}: {task['name']} - {status} ({duration:.1f}s)")
        
        print("\n" + "-" * 60)
        print(f"总计：{completed} 成功，{failed} 失败")
        print(f"总耗时：{total_duration/60:.1f} 分钟")
        print(f"并行度：最高 3 任务同时执行")
        
        # 保存总结
        summary_file = self.results_dir / "summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump({
                "task_id": self.task_id,
                "total_tasks": len(self.tasks),
                "completed": completed,
                "failed": failed,
                "total_duration_seconds": total_duration,
                "timestamp": datetime.now().isoformat()
            }, f, indent=2, ensure_ascii=False)


def main():
    """命令行入口"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法：parallel_executor.py <task_id>")
        print("示例：parallel_executor.py TASK-001")
        sys.exit(1)
    
    task_id = sys.argv[1]
    executor = ParallelExecutor(task_id)
    executor.run_parallel()


if __name__ == "__main__":
    main()
