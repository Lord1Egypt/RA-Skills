#!/usr/bin/env python3
"""
任务记忆管理器 - 精简版
"""

import os
import json
import sys
import argparse
from datetime import datetime
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).parent.parent.parent.parent / "workspace"
OUTPUT_DIR = WORKSPACE_ROOT / "output"
MEMORY_DIR = WORKSPACE_ROOT / "memory"

class TaskMemoryManager:
    def __init__(self):
        self.output_dir = OUTPUT_DIR
    
    def scan_tasks(self, status_filter=None):
        tasks = []
        
        if not self.output_dir.exists():
            return tasks
        
        for task_dir in self.output_dir.iterdir():
            if not task_dir.is_dir():
                continue
            
            meta_file = task_dir / ".task-meta.json"
            if not meta_file.exists():
                continue
            
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                
                if status_filter and metadata.get("status") != status_filter:
                    continue
                
                created_str = metadata.get("created", "")
                if created_str:
                    try:
                        created_time = datetime.fromisoformat(created_str.replace("Z", "+00:00"))
                        age_days = (datetime.now() - created_time).days
                        metadata["age_days"] = age_days
                    except:
                        metadata["age_days"] = 999
                
                last_active_str = metadata.get("last_active", "")
                if last_active_str:
                    try:
                        last_active = datetime.fromisoformat(last_active_str.replace("Z", "+00:00"))
                        hours_since = (datetime.now() - last_active).total_seconds() / 3600
                        metadata["hours_since_active"] = round(hours_since, 1)
                    except:
                        metadata["hours_since_active"] = 999
                
                tasks.append(metadata)
            except Exception as e:
                print(f"⚠️  读取失败 {task_dir.name}: {e}")
        
        return tasks
    
    def init_task(self, task_id, steps, description=""):
        task_dir = self.output_dir / task_id
        
        if not task_dir.exists():
            print(f"⚠️  任务目录不存在: {task_id}")
            return False
        
        meta_file = task_dir / ".task-meta.json"
        
        if meta_file.exists():
            print(f"⚠️  元数据已存在: {task_id}")
            return False
        
        for step in steps:
            step_dir = task_dir / step.strip()
            step_dir.mkdir(exist_ok=True)
        
        metadata = {
            "task_id": task_id,
            "status": "进行中",
            "created": datetime.now().isoformat(),
            "last_active": datetime.now().isoformat(),
            "current_step": steps[0] if steps else "未指定",
            "progress": 0,
            "description": description,
            "steps": steps,
            "memory_points": [],
            "file_mappings": {}
        }
        
        try:
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            print(f"✅ 已初始化任务元数据: {task_id}")
            return True
        except Exception as e:
            print(f"❌ 初始化失败: {e}")
            return False
    
    def update_task(self, task_id, **kwargs):
        meta_file = self.output_dir / task_id / ".task-meta.json"
        
        if not meta_file.exists():
            print(f"⚠️  任务元数据不存在: {task_id}")
            return False
        
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            for key, value in kwargs.items():
                if value is not None:
                    metadata[key] = value
            
            metadata["last_active"] = datetime.now().isoformat()
            
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 已更新任务元数据: {task_id}")
            return True
        except Exception as e:
            print(f"❌ 更新失败: {e}")
            return False
    
    def add_memory_point(self, task_id, step, memory_type, summary, files=None):
        meta_file = self.output_dir / task_id / ".task-meta.json"
        
        if not meta_file.exists():
            print(f"⚠️  任务元数据不存在: {task_id}")
            return False
        
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
            
            memory_point = {
                "id": f"mem_{len(metadata.get('memory_points', [])) + 1:03d}",
                "timestamp": datetime.now().isoformat(),
                "step": step,
                "type": memory_type,
                "summary": summary[:200],
                "files": files or []
            }
            
            if "memory_points" not in metadata:
                metadata["memory_points"] = []
            
            metadata["memory_points"].append(memory_point)
            
            if len(metadata["memory_points"]) > 30:
                metadata["memory_points"] = metadata["memory_points"][-30:]
            
            metadata["last_active"] = datetime.now().isoformat()
            
            with open(meta_file, "w", encoding="utf-8") as f:
                json.dump(metadata, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 已添加记忆点: {task_id}")
            return True
        except Exception as e:
            print(f"❌ 添加失败: {e}")
            return False
    
    def generate_recovery_interface(self, max_tasks=5):
        active_tasks = []
        for status in ["进行中", "暂停"]:
            tasks = self.scan_tasks(status_filter=status)
            active_tasks.extend(tasks)
        
        active_tasks.sort(key=lambda x: x.get("hours_since_active", 999), reverse=False)
        
        if not active_tasks:
            return "🆕 未发现进行中的任务，开始新会话。"
        
        display_tasks = active_tasks[:max_tasks]
        interface = "🔄 会话恢复 - 发现进行中任务\n\n"
        
        for i, task in enumerate(display_tasks, 1):
            task_id = task.get("task_id", "未知任务")
            status = task.get("status", "未知状态")
            current_step = task.get("current_step", "未指定")
            progress = task.get("progress", 0)
            hours_since = task.get("hours_since_active", 0)
            
            latest_memory = ""
            memory_points = task.get("memory_points", [])
            if memory_points:
                latest = memory_points[-1]
                latest_memory = latest.get("summary", "")[:80]
            
            time_str = f"{hours_since:.1f}小时前" if hours_since >= 1 else f"{hours_since*60:.0f}分钟前"
            
            interface += f"{i}. 📄 {task_id} ({progress}%完成)\n"
            interface += f"   - 状态: {status}\n"
            interface += f"   - 当前步骤: {current_step}\n"
            interface += f"   - 最后活跃: {time_str}\n"
            if latest_memory:
                interface += f"   - 关键记忆: {latest_memory}\n"
            interface += "\n"
        
        interface += "请选择恢复的任务（输入编号，多个用逗号分隔，回车跳过）:"
        return interface
    
    def load_task_memories(self, task_ids, max_memories_per_task=5):
        all_memories = []
        
        for task_id in task_ids:
            meta_file = self.output_dir / task_id / ".task-meta.json"
            
            if not meta_file.exists():
                continue
            
            try:
                with open(meta_file, "r", encoding="utf-8") as f:
                    metadata = json.load(f)
                
                memory_points = metadata.get("memory_points", [])
                memory_points.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
                selected_memories = memory_points[:max_memories_per_task]
                
                for mem in selected_memories:
                    timestamp = mem.get("timestamp", "")[:16]
                    step = mem.get("step", "")
                    summary = mem.get("summary", "")
                    memory_str = f"[{timestamp}] #{task_id} @{step}\n{summary}\n"
                    all_memories.append(memory_str)
                
                print(f"✅ 已加载任务记忆: {task_id} ({len(selected_memories)}条)")
            except Exception as e:
                print(f"❌ 加载失败 {task_id}: {e}")
        
        return all_memories

def main():
    parser = argparse.ArgumentParser(description="任务记忆管理器")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    scan_parser = subparsers.add_parser("scan", help="扫描任务")
    scan_parser.add_argument("--status", help="按状态过滤")
    
    init_parser = subparsers.add_parser("init", help="初始化任务元数据")
    init_parser.add_argument("--task-id", required=True, help="任务ID")
    init_parser.add_argument("--steps", required=True, help="步骤列表，逗号分隔")
    
    update_parser = subparsers.add_parser("update", help="更新任务元数据")
    update_parser.add_argument("--task-id", required=True, help="任务ID")
    update_parser.add_argument("--status", help="状态")
    update_parser.add_argument("--step", help="当前步骤")
    update_parser.add_argument("--progress", type=int, help="进度百分比")
    
    memory_parser = subparsers.add_parser("add-memory", help="添加记忆点")
    memory_parser.add_argument("--task-id", required=True, help="任务ID")
    memory_parser.add_argument("--step", required=True, help="步骤")
    memory_parser.add_argument("--type", required=True, choices=["决策", "进展", "问题", "解决"], help="记忆类型")
    memory_parser.add_argument("--summary", required=True, help="记忆摘要")
    memory_parser.add_argument("--files", nargs="+", help="关联文件")
    
    recovery_parser = subparsers.add_parser("recovery", help="生成恢复界面")
    recovery_parser.add_argument("--max-tasks", type=int, default=5, help="最大显示任务数")
    
    load_parser = subparsers.add_parser("load", help="加载任务记忆")
    load_parser.add_argument("--task-ids", required=True, nargs="+", help="任务ID列表")
    load_parser.add_argument("--max-per-task", type=int, default=5, help="每个任务最大记忆数")
    
    args = parser.parse_args()
    
    manager = TaskMemoryManager()
    
    if args.command == "scan":
        tasks = manager.scan_tasks(status_filter=args.status)
        for task in tasks:
            print(f"{task.get('task_id')} - {task.get('status')} - {task.get('current_step')}")
    
    elif args.command == "init":
        steps = [s.strip() for s in args.steps.split(",")]
        success = manager.init_task(args.task_id, steps, "")
        sys.exit(0 if success else 1)
    
    elif args.command == "update":
        success = manager.update_task(
            args.task_id,
            status=args.status,
            current_step=args.step,
            progress=args.progress
        )
        sys.exit(0 if success else 1)
    
    elif args.command == "add-memory":
        success = manager.add_memory_point(
            args.task_id,
            args.step,
            args.type,
            args.summary,
            args.files
        )
        sys.exit(0 if success else 1)
    
    elif args.command == "recovery":
        interface = manager.generate_recovery_interface(args.max_tasks)
        print(interface)
    
    elif args.command == "load":
        memories = manager.load_task_memories(args.task_ids, args.max_per_task)
        for memory in memories:
            print(memory)
            print("-" * 40)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()