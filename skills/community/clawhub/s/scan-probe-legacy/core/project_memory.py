# -*- coding: utf-8 -*-
"""V1.0.5 项目记忆持久化模块（增强版：多项目 + 步骤进度）

核心职责：
1. 在版本升级时保留用户正在制作的项目记忆记录，确保升级后无缝继续
2. 支持多个项目并行记忆（每个项目独立记录参数、产物、步骤进度）
3. 步骤进度跟踪：记录一个项目内各步骤的完成情况，便于断点续做

记忆文件：output/project_memory.json
结构：
{
  "version": "1.0.5",
  "last_feature": "...",          # 兼容旧版：最近一次功能
  "last_args": {...},             # 兼容旧版：最近一次参数
  "last_result_files": [...],     # 兼容旧版：最近一次产物
  "last_time": "...",
  "session_notes": "",
  "projects": [                   # 新增：多项目记忆列表（按更新时间倒序）
    {
      "project_id": "auto_xxx",
      "project_name": "Create 模组移植到 1.20.1",
      "feature": "jar_parser",
      "args": {...},
      "result_files": [...],
      "steps": [                  # 步骤进度
        {"name": "解析模组结构", "status": "done", "updated_at": "..."},
        {"name": "定位 Mixin 冲突", "status": "in_progress", "updated_at": "..."},
        {"name": "生成修复补丁", "status": "pending", "updated_at": ""}
      ],
      "status": "in_progress",    # in_progress / completed / archived
      "created_at": "...",
      "updated_at": "..."
    }
  ]
}

保存策略：
- 每次功能执行成功后自动保存到对应项目
- 版本升级前自动触发一次保存（由 version_migration 调用）
- 新版本启动时自动加载，若有未完成项目则提示恢复
"""

import json
import os
import sys
import shutil
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import config

# 记忆文件路径：放在 output/ 下，与用户生成的报告/补丁同目录
MEMORY_FILE = config.OUTPUT_DIR / "project_memory.json"

# 需要保留的用户数据目录（升级时一起备份）
PRESERVE_DIRS = [
    "reports",        # 生成的报告
    "downloads",      # 下载的模组
    "patch_resources",  # 补丁资源
    "temp",           # 临时文件
    "logs",           # 日志
]

# 步骤状态常量
STEP_PENDING = "pending"
STEP_IN_PROGRESS = "in_progress"
STEP_DONE = "done"

# 项目状态常量
PROJECT_IN_PROGRESS = "in_progress"
PROJECT_COMPLETED = "completed"
PROJECT_ARCHIVED = "archived"


# ==================== 对外 API ====================

def save_project_memory(
    feature: str,
    args: Optional[Dict[str, Any]] = None,
    result_files: Optional[List[str]] = None,
    session_notes: str = "",
    project_name: str = "",
    project_id: str = "",
) -> str:
    """保存当前项目记忆到本地（增强版：自动归入对应项目）

    Args:
        feature: 当前执行的功能名
        args: 输入参数字典
        result_files: 本次执行生成的输出文件路径列表
        session_notes: 用户会话备注
        project_name: 项目名称（留空则根据 feature + 关键参数自动生成）
        project_id: 已有项目 ID（用于更新现有项目；留空则新建）

    Returns:
        项目 ID（新建或更新的项目）
    """
    try:
        memory = _load_memory_file()

        # 自动生成项目名
        if not project_name:
            project_name = _auto_project_name(feature, args or {})

        # 查找或创建项目
        project = None
        if project_id:
            project = _find_project_by_id(memory, project_id)
        if project is None:
            # 没有指定 ID 或找不到 → 尝试匹配最近同 feature 的进行中项目
            project = _find_recent_in_progress(memory, feature)
        if project is None:
            project = _create_project(project_name, feature)
            memory.setdefault("projects", []).insert(0, project)

        # 更新项目内容
        project["feature"] = feature
        project["args"] = _sanitize_args(args or {})
        project["result_files"] = result_files or []
        project["updated_at"] = datetime.now().isoformat(timespec="seconds")
        if project.get("status") == PROJECT_COMPLETED:
            project["status"] = PROJECT_IN_PROGRESS  # 重新激活

        # 同步旧版字段（last_*）指向最近项目
        memory["last_feature"] = feature
        memory["last_args"] = project["args"]
        memory["last_result_files"] = project["result_files"]
        memory["last_time"] = project["updated_at"]
        memory["version"] = getattr(config, "VERSION", "unknown")
        memory["session_notes"] = session_notes

        # 把当前项目移到列表最前
        projects = memory.get("projects", [])
        if project in projects:
            projects.remove(project)
        projects.insert(0, project)
        memory["projects"] = projects

        _write_memory_file(memory)
        return project["project_id"]
    except Exception as e:
        print(f"[project_memory] 保存项目记忆失败（不影响主流程）: {e}", flush=True)
        return ""


def load_project_memory() -> Dict[str, Any]:
    """加载全部记忆（含 projects 列表）"""
    return _load_memory_file()


def has_pending_work() -> bool:
    """检测是否有未完成的工作（存在进行中的项目或旧版 last_feature）"""
    memory = _load_memory_file()
    for p in memory.get("projects", []):
        if p.get("status") == PROJECT_IN_PROGRESS:
            return True
    return bool(memory.get("last_feature"))


def get_last_feature() -> str:
    """获取上次执行的功能名"""
    return _load_memory_file().get("last_feature", "")


def get_last_args() -> Dict[str, Any]:
    """获取上次的输入参数"""
    return _load_memory_file().get("last_args", {})


def get_last_result_files() -> List[str]:
    """获取上次生成的输出文件路径"""
    return _load_memory_file().get("last_result_files", [])


def clear_project_memory() -> None:
    """清除全部项目记忆"""
    try:
        if MEMORY_FILE.exists():
            MEMORY_FILE.unlink()
    except Exception:
        pass


# ==================== 多项目管理 API ====================

def list_projects(status: str = "") -> List[Dict[str, Any]]:
    """列出所有项目

    Args:
        status: 按状态筛选（in_progress / completed / archived），空=全部

    Returns:
        项目列表（按更新时间倒序）
    """
    memory = _load_memory_file()
    projects = memory.get("projects", [])
    if status:
        projects = [p for p in projects if p.get("status") == status]
    return projects


def get_project(project_id: str) -> Optional[Dict[str, Any]]:
    """根据项目 ID 获取项目详情"""
    memory = _load_memory_file()
    return _find_project_by_id(memory, project_id)


def update_project_status(project_id: str, status: str) -> bool:
    """更新项目状态

    Args:
        project_id: 项目 ID
        status: in_progress / completed / archived
    """
    try:
        memory = _load_memory_file()
        project = _find_project_by_id(memory, project_id)
        if project is None:
            return False
        project["status"] = status
        project["updated_at"] = datetime.now().isoformat(timespec="seconds")
        _write_memory_file(memory)
        return True
    except Exception:
        return False


def delete_project(project_id: str) -> bool:
    """删除指定项目"""
    try:
        memory = _load_memory_file()
        projects = memory.get("projects", [])
        before = len(projects)
        memory["projects"] = [p for p in projects if p.get("project_id") != project_id]
        if len(memory["projects"]) == before:
            return False
        _write_memory_file(memory)
        return True
    except Exception:
        return False


# ==================== 步骤进度 API ====================

def add_step(project_id: str, step_name: str, status: str = STEP_PENDING) -> bool:
    """向项目添加一个步骤

    Args:
        project_id: 项目 ID
        step_name: 步骤名称
        status: pending / in_progress / done
    """
    try:
        memory = _load_memory_file()
        project = _find_project_by_id(memory, project_id)
        if project is None:
            return False
        steps = project.setdefault("steps", [])
        steps.append({
            "name": step_name,
            "status": status,
            "updated_at": datetime.now().isoformat(timespec="seconds") if status != STEP_PENDING else "",
        })
        project["updated_at"] = datetime.now().isoformat(timespec="seconds")
        _write_memory_file(memory)
        return True
    except Exception:
        return False


def update_step_status(project_id: str, step_index: int, status: str) -> bool:
    """更新项目中指定步骤的状态

    Args:
        project_id: 项目 ID
        step_index: 步骤索引（从 0 开始）
        status: pending / in_progress / done
    """
    try:
        memory = _load_memory_file()
        project = _find_project_by_id(memory, project_id)
        if project is None:
            return False
        steps = project.get("steps", [])
        if step_index < 0 or step_index >= len(steps):
            return False
        steps[step_index]["status"] = status
        steps[step_index]["updated_at"] = datetime.now().isoformat(timespec="seconds")
        project["updated_at"] = datetime.now().isoformat(timespec="seconds")
        _write_memory_file(memory)
        return True
    except Exception:
        return False


def get_steps(project_id: str) -> List[Dict[str, Any]]:
    """获取项目的所有步骤"""
    project = get_project(project_id)
    if project is None:
        return []
    return project.get("steps", [])


def get_step_progress(project_id: str) -> Dict[str, int]:
    """获取项目步骤进度统计

    Returns:
        {"total": N, "done": N, "in_progress": N, "pending": N, "percent": 0-100}
    """
    steps = get_steps(project_id)
    total = len(steps)
    done = sum(1 for s in steps if s.get("status") == STEP_DONE)
    in_progress = sum(1 for s in steps if s.get("status") == STEP_IN_PROGRESS)
    pending = sum(1 for s in steps if s.get("status") == STEP_PENDING)
    percent = int(done / total * 100) if total > 0 else 0
    return {
        "total": total,
        "done": done,
        "in_progress": in_progress,
        "pending": pending,
        "percent": percent,
    }


# ==================== 内部函数 ====================

def _sanitize_args(args: Dict[str, Any]) -> Dict[str, Any]:
    """清洗参数：只保留可 JSON 序列化的基本类型"""
    clean = {}
    for k, v in args.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            clean[k] = v
        elif isinstance(v, (list, tuple)):
            clean[k] = [str(x) for x in v]
        else:
            clean[k] = str(v)
    return clean


def _load_memory_file() -> Dict[str, Any]:
    """读取记忆文件，不存在或损坏则返回空字典"""
    try:
        if MEMORY_FILE.exists():
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 兼容旧版：没有 projects 字段时初始化为空列表
            if "projects" not in data:
                data["projects"] = []
            return data
    except (json.JSONDecodeError, OSError):
        pass
    return {"projects": []}


def _write_memory_file(memory: Dict[str, Any]) -> None:
    """原子写入记忆文件（先写临时文件再替换）"""
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    tmp_path = MEMORY_FILE.with_suffix(".json.tmp")
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(memory, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, MEMORY_FILE)


def _create_project(name: str, feature: str) -> Dict[str, Any]:
    """创建一个新项目"""
    now = datetime.now().isoformat(timespec="seconds")
    return {
        "project_id": f"auto_{uuid.uuid4().hex[:12]}",
        "project_name": name,
        "feature": feature,
        "args": {},
        "result_files": [],
        "steps": [],
        "status": PROJECT_IN_PROGRESS,
        "created_at": now,
        "updated_at": now,
    }


def _find_project_by_id(memory: Dict[str, Any], project_id: str) -> Optional[Dict[str, Any]]:
    """根据 ID 查找项目"""
    for p in memory.get("projects", []):
        if p.get("project_id") == project_id:
            return p
    return None


def _find_recent_in_progress(memory: Dict[str, Any], feature: str) -> Optional[Dict[str, Any]]:
    """查找最近的同 feature 且进行中的项目（用于自动归并）"""
    for p in memory.get("projects", []):
        if p.get("feature") == feature and p.get("status") == PROJECT_IN_PROGRESS:
            return p
    return None


def _auto_project_name(feature: str, args: Dict[str, Any]) -> str:
    """根据功能和参数自动生成项目名"""
    # 尝试从参数中提取有意义的标识
    candidates = ["jar_path", "mod_path", "mod_name", "project_name", "target_version", "launcher"]
    parts = []
    for key in candidates:
        val = args.get(key)
        if val:
            val_str = str(val)
            # 取文件名而非完整路径
            if "\\" in val_str or "/" in val_str:
                val_str = val_str.replace("\\", "/").split("/")[-1]
            parts.append(val_str)
    if parts:
        return f"{feature}: {' · '.join(parts[:2])}"
    return f"{feature} 项目"


def backup_user_data_before_upgrade() -> Optional[str]:
    """版本升级前备份用户数据（output/ 下的用户生成内容）

    将 output/ 整个目录备份到 output_backup_<时间戳>/
    确保升级过程中万一出问题可以回滚。

    Returns:
        备份目录路径字符串，失败返回 None
    """
    try:
        output_dir = config.OUTPUT_DIR
        if not output_dir.exists():
            return None
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = output_dir.parent / f"output_backup_{timestamp}"
        shutil.copytree(output_dir, backup_dir, ignore=shutil.ignore_patterns("*.tmp", "*.lock"))
        info_file = backup_dir / "_backup_info.txt"
        info_file.write_text(
            f"备份时间: {datetime.now().isoformat()}\n"
            f"备份原因: 版本升级前自动备份\n"
            f"原版本: {getattr(config, 'VERSION', 'unknown')}\n"
            f"原目录: {output_dir}\n",
            encoding="utf-8",
        )
        return str(backup_dir)
    except Exception as e:
        print(f"[project_memory] 备份用户数据失败: {e}", flush=True)
        return None
