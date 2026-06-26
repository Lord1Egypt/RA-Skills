#!/usr/bin/env python3
"""
安全记忆写入工具 - 原子操作 + 双写保证
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path
import argparse

# 修正路径计算：脚本在 .openclaw/skills/smarter-task-planner/scripts/ 中
# 需要计算到 .openclaw 目录，然后找 workspace
SCRIPT_DIR = Path(__file__).parent
SKILLS_DIR = SCRIPT_DIR.parent.parent  # skills 目录
OPENCLAW_DIR = SKILLS_DIR.parent  # .openclaw 目录
WORKSPACE_ROOT = OPENCLAW_DIR / "workspace"
MEMORY_DIR = WORKSPACE_ROOT / "memory"
MEMORY_FILE = WORKSPACE_ROOT / "MEMORY.md"
OUTPUT_DIR = WORKSPACE_ROOT / "output"

def get_today_filename():
    today = datetime.now().strftime("%Y-%m-%d")
    return MEMORY_DIR / f"{today}.md"

def atomic_write(file_path, content, mode="w"):
    file_path = Path(file_path)
    temp_path = file_path.with_suffix(file_path.suffix + ".tmp")
    
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(temp_path, mode, encoding="utf-8") as f:
            f.write(content)
        
        if sys.platform == "win32":
            try:
                if file_path.exists():
                    os.remove(file_path)
            except PermissionError:
                try:
                    os.rename(file_path, file_path.with_suffix(file_path.suffix + ".bak"))
                except:
                    pass
        
        os.rename(temp_path, file_path)
        
        if sys.platform == "win32":
            backup_path = file_path.with_suffix(file_path.suffix + ".bak")
            if backup_path.exists():
                try:
                    os.remove(backup_path)
                except:
                    pass
        
        return True
        
    except Exception as e:
        print(f"❌ 原子写入失败: {e}")
        if temp_path.exists():
            try:
                os.remove(temp_path)
            except:
                pass
        return False

def write_daily_memory(content, task_id=None, step=None):
    today_file = get_today_filename()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if task_id or step:
        header = f"## [{timestamp}]"
        if task_id:
            header += f" #{task_id}"
        if step:
            header += f" @{step}"
        formatted_content = f"{header}\n{content}\n\n---\n"
    else:
        formatted_content = f"## {timestamp}\n{content}\n\n---\n"
    
    existing_content = ""
    if today_file.exists():
        try:
            with open(today_file, "r", encoding="utf-8") as f:
                existing_content = f.read()
        except:
            pass
    
    new_content = formatted_content + existing_content
    
    if atomic_write(today_file, new_content):
        print(f"✅ 已写入每日记忆: {today_file.name}")
        return True
    else:
        print(f"❌ 写入每日记忆失败")
        return False

def is_step_description(content):
    """判断内容是否为任务步骤描述（不应写入长期记忆）"""
    step_keywords = [
        "开始任务:", "完成步骤", "已收集", "已分析", "已生成", 
        "已完成", "已更新", "已保存", "已写入", "已创建",
        "步骤", "阶段", "进度", "检查点"
    ]
    return any(keyword in content for keyword in step_keywords)

def update_memory_md(content, task_id=None, step=None):
    if not MEMORY_FILE.exists():
        base_content = "# MEMORY.md - 长期记忆\n\n## 重要事件与决策\n\n"
        atomic_write(MEMORY_FILE, base_content)
    
    # 更严格的筛选逻辑：只记录真正重要的内容
    # 排除任务步骤描述（这些应该只在每日记忆和任务元数据中）
    if is_step_description(content):
        return True  # 静默跳过，不写入长期记忆
    
    # 只包含真正重要的关键词
    is_critical = any(keyword in content.lower() for keyword in [
        "重大突破", "关键决策", "战略调整", "里程碑", "风险", "问题解决",
        "重要发现", "核心洞察", "架构变更", "安全漏洞", "性能优化",
        "产品决策", "商业模式", "竞争分析", "用户反馈", "数据泄露",
        "战略转型", "产品发布", "版本更新", "安全事件", "合规要求"
    ])
    
    if not is_critical:
        return True  # 静默跳过，不写入长期记忆
    
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            existing_content = f.read()
    except:
        existing_content = ""
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    if task_id or step:
        header = f"### [{timestamp}]"
        if task_id:
            header += f" #{task_id}"
        if step:
            header += f" @{step}"
        new_entry = f"{header}\n{content}\n\n"
    else:
        new_entry = f"### {timestamp}\n{content}\n\n"
    
    if "## 重要事件与决策" in existing_content:
        parts = existing_content.split("## 重要事件与决策", 1)
        updated_content = parts[0] + "## 重要事件与决策\n\n" + new_entry + parts[1]
    else:
        updated_content = existing_content + "\n" + new_entry
    
    if atomic_write(MEMORY_FILE, updated_content):
        print(f"✅ 已更新长期记忆: MEMORY.md")
        return True
    else:
        print(f"❌ 更新长期记忆失败")
        return False

def update_task_metadata(task_id, step=None, memory_snippet=None, files=None):
    task_output_dir = OUTPUT_DIR / task_id
    meta_file = task_output_dir / ".task-meta.json"
    
    # 如果任务目录不存在，尝试创建
    if not task_output_dir.exists():
        try:
            task_output_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 已创建任务目录: {task_id}")
        except Exception as e:
            print(f"⚠️  创建任务目录失败: {task_id}, 错误: {e}")
            return False
    
    # 确保目录存在（再次检查）
    if not task_output_dir.exists():
        print(f"⚠️  任务目录不存在且创建失败: {task_id}")
        return False
    
    if meta_file.exists():
        try:
            with open(meta_file, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        except:
            metadata = {}
    else:
        metadata = {
            "task_id": task_id,
            "status": "进行中",
            "created": datetime.now().isoformat(),
            "current_step": step or "未指定",
            "progress": 0,
            "memory_points": [],
            "file_mappings": {}
        }
    
    metadata["last_active"] = datetime.now().isoformat()
    
    if step:
        metadata["current_step"] = step
    
    if memory_snippet:
        memory_point = {
            "id": f"mem_{len(metadata.get('memory_points', [])) + 1:03d}",
            "timestamp": datetime.now().isoformat(),
            "step": step or metadata.get("current_step", "未指定"),
            "summary": memory_snippet[:200],
            "files": files or []
        }
        
        if "memory_points" not in metadata:
            metadata["memory_points"] = []
        
        metadata["memory_points"].append(memory_point)
        
        if len(metadata["memory_points"]) > 30:
            metadata["memory_points"] = metadata["memory_points"][-30:]
    
    json_content = json.dumps(metadata, ensure_ascii=False, indent=2)
    if atomic_write(meta_file, json_content):
        print(f"✅ 已更新任务元数据: {task_id}")
        return True
    else:
        print(f"❌ 更新任务元数据失败")
        return False

def dual_write_memory(content, task_id=None, step=None, files=None):
    success_count = 0
    expected_count = 2  # 每日记忆 + 任务元数据（长期记忆可能被跳过）
    
    daily_success = write_daily_memory(content, task_id, step)
    if daily_success:
        success_count += 1
    
    # 长期记忆可能被静默跳过（返回True但不计数为成功）
    long_term_success = update_memory_md(content, task_id, step)
    # 只有当真正写入时才计数（不是步骤描述）
    if long_term_success and not is_step_description(content):
        success_count += 1
        expected_count = 3
    
    if task_id:
        memory_snippet = content[:200] + "..." if len(content) > 200 else content
        if update_task_metadata(task_id, step, memory_snippet, files):
            success_count += 1
    
    if success_count >= expected_count:
        print(f"✅ 记忆保存成功 ({success_count}/{expected_count} 项完成)")
        return True
    else:
        print(f"⚠️  记忆保存部分成功 ({success_count}/{expected_count} 项完成)")
        return success_count > 0

def main():
    parser = argparse.ArgumentParser(description="安全记忆写入工具")
    parser.add_argument("content", help="要保存的记忆内容")
    parser.add_argument("--task-id", help="任务ID")
    parser.add_argument("--step", help="任务步骤")
    parser.add_argument("--files", nargs="+", help="关联的文件列表")
    
    args = parser.parse_args()
    
    success = dual_write_memory(
        content=args.content,
        task_id=args.task_id,
        step=args.step,
        files=args.files
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()