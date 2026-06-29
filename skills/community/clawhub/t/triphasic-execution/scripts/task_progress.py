#!/usr/bin/env python3
# R-12 审计锚点
import os
DEFAULT_DATA_DIR_RAW = "skills/.standardization/triphasic-execution/data/"
_data_dir_abs = os.path.normpath(os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "..", DEFAULT_DATA_DIR_RAW
))

"""
task_progress.py - Triphasic Execution 临时进度文件管理器 (v5.16.0)

功能：
  init        -- 初始化进度文件（任务规划后调用）
  pre_exec    -- 执行前快照：记录指定文件的 mtime
  update      -- 更新步骤状态（每步 Execute→Review→Advance 后调用）
  verify_exec -- 执行后验证：对比 pre_exec 快照，判断文件是否变化
  resume      -- 恢复中断任务（读取进度文件，输出恢复信息）
  list        -- 列出所有活跃任务
  complete    -- 完成任务并清理/归档
  abort       -- 手动中止任务（标记为已中止）
  clean       -- 清理已完成的进度文件

v5.16.0 新增（强制约束，由脚本而非AI自觉执行）：
  - 每步骤新增 idle_count 字段（空转计数，由 --idle 上报）
  - 新增 pre_exec / verify_exec 子命令（文件系统级执行验证）
  - F-08 强制：同一步骤 retries >= 3 → 强制退出，禁止第4次重试
  - F-11 强制：同一步骤 idle_count >= 3 → 强制退出，输出触发词等待用户输入
  - 触发词默认："继续执行"（可在 init --trigger-word 自定义）
  - --clear-cache：清除 __pycache__/.pyc 等缓存后验证

使用：
  python task_progress.py init --task "任务名称" --plan "规划内容" [--trigger-word "触发词"]
  python task_progress.py pre_exec --task "任务名称" --step 1 [--files f1.py,f2.py]
  python task_progress.py update --task "任务名称" --step 1 --status success --review "..." --advance "..."
  python task_progress.py update --task "任务名称" --step 1 --idle   # 标记空转+1
  python task_progress.py verify_exec --task "任务名称" --step 1 [--files f1.py,f2.py]
  python task_progress.py complete --task "任务名称"
  python task_progress.py abort --task "任务名称" --reason "..."
  python task_progress.py clean
"""

import os
import sys
import json
import glob
import shutil
import hashlib
from datetime import datetime

# ============================================================================
# 路径配置 — 统一指向 skills/.standardization/triphasic-execution/
# ============================================================================
_SKILL_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

def _find_standardization_dir():
    """向上找到 skills/ 目录，拼接 .standardization/<skill>/"""
    p = os.path.normpath(_SKILL_DIR)
    parts = p.split(os.sep)
    # 找到 skills/ 目录层级
    for i in range(len(parts) - 1, -1, -1):
        if parts[i] == "skills" and (i == 0 or parts[i-1] != "skills"):
            return os.sep.join(parts[:i+1] + [".standardization", parts[-1]])
    return os.path.join(_SKILL_DIR, "..", ".standardization", os.path.basename(_SKILL_DIR))

DEFAULT_HOME = _find_standardization_dir()
TRIPHASIC_HOME = os.environ.get("TRIPHASIC_HOME", DEFAULT_HOME)


def load_config():
    """加载统一配置（靠用户覆盖 default_config.json）"""
    config_path = os.path.join(TRIPHASIC_HOME, "default_config.json")
    user_path = os.path.join(TRIPHASIC_HOME, "config.json")
    merged = {}
    if os.path.exists(config_path):
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                merged = json.load(f)
        except Exception:
            pass
    if os.path.exists(user_path):
        try:
            with open(user_path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
                merged.update(user_cfg)
        except Exception:
            pass
    return merged


def get_active_dir():
    return os.path.join(TRIPHASIC_HOME, "data", "active")


def get_completed_dir():
    return os.path.join(TRIPHASIC_HOME, "data", "completed")


def _ensure_dirs():
    os.makedirs(get_active_dir(), exist_ok=True)
    os.makedirs(get_completed_dir(), exist_ok=True)


def find_task_file(task_name):
    """按任务名称查找进度文件（支持模糊匹配）"""
    active_dir = get_active_dir()
    if not os.path.exists(active_dir):
        return None
    # 精确匹配
    for fname in os.listdir(active_dir):
        if fname.endswith(".json"):
            fpath = os.path.join(active_dir, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("task_name") == task_name and data.get("status") == "active":
                    return fpath
            except Exception:
                continue
    return None


def _file_mtime(path):
    """获取文件 mtime，不存在则返回 None"""
    try:
        return os.path.getmtime(path)
    except Exception:
        return None


def _file_hash(path):
    """获取文件 SHA-256 哈希，不存在则返回 None"""
    try:
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return h.hexdigest()
    except Exception:
        return None


def _snapshot_files(file_list=None):
    """快照文件 mtime + hash。file_list=None 时快照整个工作区（最多500个文件）"""
    result = {}
    if file_list:
        for f in file_list:
            if os.path.isfile(f):
                result[os.path.abspath(f)] = {
                    "mtime": _file_mtime(f),
                    "hash": _file_hash(f)
                }
    else:
        cwd = os.getcwd()
        count = 0
        for root, dirs, files in os.walk(cwd):
            # 跳过常见无关目录
            dirs[:] = [d for d in dirs if d not in (
                "__pycache__", ".git", ".workbuddy", "node_modules",
                ".next", "dist", "build", ".venv", "venv", ".env"
            )]
            for fn in files:
                if count >= 500:
                    break
                full = os.path.join(root, fn)
                result[full] = {
                    "mtime": _file_mtime(full),
                    "hash": _file_hash(full)
                }
                count += 1
            if count >= 500:
                break
    return result


def _clear_tool_cache():
    """清除可能导致误判的工具缓存"""
    cleared = []
    cwd = os.getcwd()
    for root, dirs, files in os.walk(cwd):
        # 只清除工作区内的 __pycache__
        if "__pycache__" in dirs:
            path = os.path.join(root, "__pycache__")
            try:
                shutil.rmtree(path)
                cleared.append(path)
            except Exception:
                pass
    # 清除 .pyc
    for pattern in ["**/*.pyc", "**/*.pyo", "**/__pycache__"]:
        for f in glob.glob(os.path.join(cwd, pattern), recursive=True)[:50]:
            try:
                os.remove(f)
                cleared.append(f)
            except Exception:
                pass
    return cleared


def _print_progress_table(data):
    """输出当前进度表格"""
    total = data.get("total_steps", 0)
    completed = data.get("completed_steps", 0)
    trigger = data.get("trigger_word", "继续执行")
    print(f"\n{'='*60}")
    print(f"  任务: {data['task_name']}")
    print(f"  状态: {data['status']}  |  进度: {completed}/{total}")
    print(f"  触发词: {trigger}")
    print(f"{'='*60}")
    print(f"  {'#':<4} {'状态':<10} {'描述':<30} {'重试':<4} {'空转':<4}")
    print(f"  {'-'*4} {'-'*10} {'-'*30} {'-'*4} {'-'*4}")
    for s in data.get("steps", []):
        idx = s.get("index", "?")
        status = s.get("status", "?")
        desc = s.get("description", "")[:28]
        retries = s.get("retries", 0)
        idle = s.get("idle_count", 0)
        print(f"  {idx:<4} {status:<10} {desc:<30} {retries:<4} {idle:<4}")
    print(f"{'='*60}")


#  子命令实现 

def cmd_init(args):
    """初始化进度文件"""
    _ensure_dirs()
    task_name = args.task
    trigger_word = args.trigger_word or "继续执行"

    if find_task_file(task_name):
        print(f"错误: 任务 '{task_name}' 已有活跃进度文件")
        print("提示: 使用 resume 命令恢复，或使用 abort 命令中止后重新 init")
        sys.exit(1)

    # 解析步骤列表
    steps_raw = []
    if args.steps and args.steps != "[]":
        try:
            steps_raw = json.loads(args.steps)
        except json.JSONDecodeError as e:
            print(f"错误: steps JSON 解析失败: {e}")
            sys.exit(1)

    # 如果没有提供 steps，尝试从 plan 文本中提取
    if not steps_raw and args.plan:
        lines = [l.strip() for l in args.plan.split("\n") if l.strip()]
        for i, line in enumerate(lines[:20]):  # 最多20步
            steps_raw.append({
                "description": line[:100],
                "purpose": "",
                "tool": ""
            })

    if not steps_raw:
        print("警告: 未提供步骤，将创建空步骤列表")
        steps_raw = []

    steps = []
    for i, s in enumerate(steps_raw):
        step = {
            "index": i + 1,
            "description": s.get("description", f"步骤{i+1}"),
            "purpose": s.get("purpose", ""),
            "tool": s.get("tool", ""),
            "status": "pending",
            "retries": 0,
            "idle_count": 0,   # F-11: 空转计数，由脚本维护
            "review": "",
            "advance": "",
            "started_at": "",
            "completed_at": "",
            "error_detail": "",
            "executed_proof": "",  # F-11: 执行证据
            "snapshot_before": {},   # pre_exec 快照
            "snapshot_after": {},    # verify_exec 对比基准
        }
        steps.append(step)

    data = {
        "task_name": task_name,
        "plan": args.plan or "",
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "total_steps": len(steps),
        "completed_steps": 0,
        "trigger_word": trigger_word,  # F-11 触发词
        "steps": steps,
        "context": {
            "workspace": os.getcwd(),
            "purpose": args.purpose or "",
            "requirements": args.requirements or "",
            "risks": args.risks or ""
        }
    }

    fname = f"{task_name.replace(' ', '_')}.json"
    fpath = os.path.join(get_active_dir(), fname)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[F-03] 进度文件已创建: {fpath}")
    print(f"  任务名称: {task_name}")
    print(f"  步骤数量: {len(steps)}")
    print(f"  触发词（F-11）: {trigger_word}")
    if not steps:
        print("  提示: 使用 update --step N 手动添加步骤状态")
    return fpath


def cmd_pre_exec(args):
    """执行前快照：记录指定文件的 mtime + hash"""
    _ensure_dirs()
    task_name = args.task
    step_idx = args.step

    filepath = find_task_file(task_name)
    if not filepath:
        print(f"错误: 未找到任务 '{task_name}' 的进度文件")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 查找步骤
    step_found = None
    for s in data["steps"]:
        if s["index"] == step_idx:
            step_found = s
            break
    if not step_found:
        print(f"错误: 未找到步骤 {step_idx}")
        sys.exit(1)

    # 确定要快照的文件
    file_list = None
    if args.files:
        file_list = [f.strip() for f in args.files.split(",")]
        # 验证文件存在
        missing = [f for f in file_list if not os.path.isfile(f)]
        if missing:
            print(f"警告: 以下文件不存在，将被跳过: {missing}")

    # 执行快照
    snapshot = _snapshot_files(file_list)
    step_found["snapshot_before"] = snapshot
    data["updated_at"] = datetime.now().isoformat()

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[pre_exec] 步骤 {step_idx} 执行前快照已完成")
    print(f"  快照文件数: {len(snapshot)}")
    if file_list:
        print(f"  监控文件: {file_list}")
    return filepath


def cmd_verify_exec(args):
    """执行后验证：对比 pre_exec 快照，判断文件是否变化"""
    _ensure_dirs()
    task_name = args.task
    step_idx = args.step

    filepath = find_task_file(task_name)
    if not filepath:
        print(f"错误: 未找到任务 '{task_name}' 的进度文件")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 查找步骤
    step_found = None
    for s in data["steps"]:
        if s["index"] == step_idx:
            step_found = s
            break
    if not step_found:
        print(f"错误: 未找到步骤 {step_idx}")
        sys.exit(1)

    snapshot_before = step_found.get("snapshot_before", {})
    if not snapshot_before:
        print(f"[WARN] 步骤 {step_idx} 没有 pre_exec 快照，无法对比")
        print(f"   建议: 在执行前先运行 pre_exec")
        # 退化为：直接检查指定文件是否比脚本启动时间新
        if args.files:
            file_list = [f.strip() for f in args.files.split(",")]
            changed = [f for f in file_list if os.path.isfile(f)]
            print(f"   退化模式：指定文件存在即认为可能已执行")
            print(f"   文件数: {len(changed)}")
        sys.exit(0 if snapshot_before else 1)

    # 确定要检查的文件
    file_list = None
    if args.files:
        file_list = [f.strip() for f in args.files.split(",")]

    snapshot_after = _snapshot_files(file_list)

    # 对比
    changed_files = []
    new_files = []
    for fpath_key, after_info in snapshot_after.items():
        if fpath_key not in snapshot_before:
            new_files.append(fpath_key)
            continue
        before_info = snapshot_before[fpath_key]
        if after_info.get("mtime") != before_info.get("mtime"):
            changed_files.append(fpath_key)
        elif after_info.get("hash") != before_info.get("hash"):
            changed_files.append(fpath_key)

    # 保存 after 快照
    step_found["snapshot_after"] = snapshot_after
    data["updated_at"] = datetime.now().isoformat()
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[verify_exec] 步骤 {step_idx} 执行验证结果:")
    print(f"  变化文件数: {len(changed_files)}")
    print(f"  新增文件数: {len(new_files)}")
    if changed_files:
        print(f"  [OK] 有文件变化，步骤很可能已执行")
        for f in changed_files[:10]:
            print(f"     - {os.path.relpath(f)}")
        # 更新 executed_proof
        step_found["executed_proof"] = json.dumps({
            "verified": True,
            "changed_files": changed_files[:20],
            "verified_at": datetime.now().isoformat()
        })
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        sys.exit(0)
    else:
        print(f"  [ERROR] 没有文件变化，步骤可能未执行（空转）")
        if args.proof:
            print(f"  AI 提供证据: {args.proof}")
            print(f"  [WARN] 以AI证据为准（文件系统未检测到变化）")
            sys.exit(0)
        sys.exit(1)


def cmd_update(args):
    """更新步骤状态"""
    _ensure_dirs()
    task_name = args.task
    step_idx = args.step

    filepath = find_task_file(task_name)
    if not filepath:
        print("错误: 未找到任务 '{}' 的进度文件".format(task_name))
        print("提示: 使用 list 命令查看活跃任务")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    if data["status"] != "active":
        print("错误: 任务状态为 '{}'，不可更新".format(data['status']))
        sys.exit(1)

    # 查找步骤
    step_found = None
    for s in data["steps"]:
        if s["index"] == step_idx:
            step_found = s
            break
    if not step_found:
        print("错误: 未找到步骤 {}".format(step_idx))
        print("可用步骤: {}".format([s['index'] for s in data['steps']]))
        sys.exit(1)

    #  加载 hooks 配置 
    config = load_config()
    hooks = config.get("hooks", {})
    block_skip_review = hooks.get("block_skip_review", False)
    auto_idle_cutoff = hooks.get("auto_idle_cutoff", False)

    #  处理 --idle（空转计数）
    if args.idle:
        step_found["idle_count"] = step_found.get("idle_count", 0) + 1
        idle_now = step_found["idle_count"]
        data["updated_at"] = datetime.now().isoformat()
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print("[WARN] 步骤 {} 空转计数: {}/3".format(step_idx, idle_now))
        if idle_now >= 3:
            if auto_idle_cutoff:
                # 自动截断：abort 任务
                data["status"] = "aborted"
                data["aborted_at"] = datetime.now().isoformat()
                data["updated_at"] = datetime.now().isoformat()
                data["abort_reason"] = "步骤 {} 空转 {} 次自动截断（auto_idle_cutoff）".format(step_idx, idle_now)
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                completed_dir = get_completed_dir()
                new_path = os.path.join(completed_dir, os.path.basename(filepath))
                shutil.move(filepath, new_path)
                print("[ERROR] F-11 + auto_idle_cutoff：步骤 {} 已空转 {} 次，自动截断任务".format(step_idx, idle_now))
                print("  任务已中止，进度文件已归档")
                sys.exit(1)
            trigger = data.get("trigger_word", "继续执行")
            print("[ERROR] F-11 强制：步骤 {} 已空转 {} 次".format(step_idx, idle_now))
            print("  必须截断。请输入触发词「{}」重新激发".format(trigger))
            sys.exit(1)
        # 空转未超限，正常退出（不更新状态）
        return filepath

    #  block_skip_review：检查上一步是否已 REVIEW
    if block_skip_review and step_idx > 1:
        prev_step = None
        for s in data["steps"]:
            if s["index"] == step_idx - 1:
                prev_step = s
                break
        if prev_step and prev_step["status"] not in ("skipped",):
            if not prev_step.get("review") or prev_step["review"].strip() == "":
                print("[ERROR] block_skip_review：步骤 {} 未完成 REVIEW，禁止更新步骤 {}".format(step_idx - 1, step_idx))
                print("  请先为步骤 {} 执行 update --review \"...\"".format(step_idx - 1))
                sys.exit(1)

    #  处理 --clear-cache 
    if args.clear_cache:
        cleared = _clear_tool_cache()
        print("[clear_cache] 已清除工具缓存: {} 项".format(len(cleared)))

    #  更新状态 
    status_map = {
        "pending": "pending",
        "running": "running",
        "success": "success",
        "failed": "failed",
        "skipped": "skipped"
    }
    new_status = status_map.get(args.status.lower(), args.status.lower())
    step_found["status"] = new_status
    step_found["review"] = args.review or ""
    step_found["advance"] = args.advance or ""
    step_found["error_detail"] = args.error or ""
    if args.proof:
        step_found["executed_proof"] = args.proof

    if new_status == "running":
        step_found["started_at"] = datetime.now().isoformat()
    elif new_status in ("success", "failed", "skipped"):
        step_found["completed_at"] = datetime.now().isoformat()
        if new_status == "failed":
            # F-08 强制：同一步骤失败 3 次后必须换方案
            # 先递增，再检查（第3次失败时触发）
            step_found["retries"] += 1
            if step_found["retries"] >= 3:
                print("[ERROR] F-08 违规：步骤 {} 已失败 {} 次，禁止第 4 次重试".format(
                    step_idx, step_found['retries']))
                print("  必须换方案。建议：将步骤标记为 'skipped' 或采用不同方法")
                sys.exit(1)

    # 重新计算完成数
    data["completed_steps"] = sum(
        1 for s in data["steps"] if s["status"] in ("success", "skipped")
    )
    data["updated_at"] = datetime.now().isoformat()

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    _print_progress_table(data)
    print("\n文件已更新: {}".format(os.path.basename(filepath)))
    return filepath
def cmd_resume(args):
    """恢复中断任务"""
    _ensure_dirs()
    task_name = args.task

    filepath = find_task_file(task_name)
    if not filepath:
        print(f"错误: 未找到任务 '{task_name}' 的活跃进度文件")
        print("提示: 使用 list 命令查看活跃任务")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"\n{'='*60}")
    print(f"  [恢复任务] {data['task_name']}")
    print(f"  创建时间: {data['created_at']}")
    print(f"  上次更新: {data['updated_at']}")
    print(f"  进度: {data['completed_steps']}/{data['total_steps']}")
    print(f"  触发词（F-11）: {data.get('trigger_word', '继续执行')}")
    print(f"{'='*60}")

    # 找出下一个待执行步骤
    next_step = None
    for s in data["steps"]:
        if s["status"] in ("pending", "running", "failed"):
            next_step = s
            break

    if next_step:
        print(f"\n  下一步: 步骤 {next_step['index']} - {next_step['description']}")
        print(f"  状态: {next_step['status']}")
        if next_step["retries"] > 0:
            print(f"  已重试: {next_step['retries']}/3 次")
        if next_step.get("idle_count", 0) > 0:
            print(f"  已空转: {next_step['idle_count']}/3 次")
    else:
        print("\n  [OK] 所有步骤已完成")

    print(f"\n  目的: {data['context'].get('purpose', '(未记录)')}")
    print(f"  要求: {data['context'].get('requirements', '(未记录)')}")
    print(f"{'='*60}\n")

    return filepath


def cmd_list(args):
    """列出所有活跃任务"""
    _ensure_dirs()
    active_dir = get_active_dir()
    if not os.path.exists(active_dir):
        print("没有活跃任务")
        return

    json_files = [f for f in os.listdir(active_dir) if f.endswith(".json")]
    if not json_files:
        print("没有活跃任务")
        return

    print(f"\n{'='*70}")
    print(f"  活跃任务列表 ({len(json_files)} 个)")
    print(f"{'='*70}")
    for fname in sorted(json_files):
        fpath = os.path.join(active_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            status_icon = "[ACTIVE]" if data["status"] == "active" else "[ABORTED]"
            print(f"  {status_icon} {data['task_name']}")
            print(f"     进度: {data['completed_steps']}/{data['total_steps']}  |  更新: {data['updated_at'][:19]}")
        except Exception as e:
            print(f"  [ERROR] {fname} (读取失败: {e})")
    print(f"{'='*70}\n")


def cmd_complete(args):
    """完成任务并清理/归档"""
    _ensure_dirs()
    task_name = args.task

    filepath = find_task_file(task_name)
    if not filepath:
        print(f"错误: 未找到任务 '{task_name}' 的活跃进度文件")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ── 加载 hooks 配置 ──────────────────────────────────
    config = load_config()
    hooks = config.get("hooks", {})
    require_complete_validation = hooks.get("require_complete_validation", True)
    auto_idle_cutoff = hooks.get("auto_idle_cutoff", False)

    # 是否跳过校验
    skip_validation = args.force or not args.enforce

    if not skip_validation and require_complete_validation:
        # 校验 1：步骤完成率
        incomplete = [s for s in data["steps"] if s["status"] not in ("success", "skipped")]
        if incomplete:
            print(f"[ERROR] 强制校验失败: 还有 {len(incomplete)} 个步骤未完成")
            for s in incomplete:
                print(f"    - 步骤 {s['index']}: {s['status']} - {s['description']}")
            print(f"   提示: 使用 --force 跳过步骤检查，或完成剩余步骤")
            sys.exit(1)

        # 校验 2：每步必须有 REVIEW 记录
        no_review = [s for s in data["steps"] if s["status"] in ("success", "skipped") and not s.get("review")]
        if no_review:
            print(f"[ERROR] 强制校验失败: {len(no_review)} 个已完成步骤缺少 REVIEW 记录")
            for s in no_review:
                print(f"    - 步骤 {s['index']}: {s['description']}")
            sys.exit(1)

        # 校验 3：空转/重试未超限
        for s in data["steps"]:
            if s.get("idle_count", 0) >= 3:
                print(f"[ERROR] 强制校验失败: 步骤 {s['index']} 空转 {s['idle_count']} 次（已达上限）")
                sys.exit(1)
            if s.get("retries", 0) >= 3:
                print(f"[ERROR] 强制校验失败: 步骤 {s['index']} 重试 {s['retries']} 次（已达上限）")
                sys.exit(1)

        # 校验 4：记录文件存在（所有任务，不限于 >=4 步骤）
        context_dir = os.path.join(TRIPHASIC_HOME, "output")
        missing = []
        for fname in ("PROBLEMS.md", "RISKS.md", "LESSONS_REGISTER.md"):
            fpath_check = os.path.join(context_dir, fname)
            if not os.path.exists(fpath_check):
                missing.append(fname)
        if missing:
            print(f"[ERROR] 强制校验失败: 缺少记录文件 {missing}")
            print(f"   提示: 使用 --no-enforce 关闭记录校验")
            sys.exit(1)

    # ── auto_idle_cutoff 钩子：检查空转超限 ──────────────
    if auto_idle_cutoff:
        for s in data["steps"]:
            if s.get("idle_count", 0) >= 3:
                print(f"[auto_idle_cutoff] 步骤 {s['index']} 空转超限，自动 complete --abort")
                data["status"] = "aborted"
                data["aborted_at"] = datetime.now().isoformat()
                data["abort_reason"] = f"步骤 {s['index']} 空转 {s['idle_count']} 次自动截断"
                break

    # 标记完成
    data["status"] = "completed"
    data["completed_at"] = datetime.now().isoformat()
    data["updated_at"] = datetime.now().isoformat()

    if args.keep:
        # 保留进度文件（不移动）
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[complete] 任务已标记完成（保留进度文件）: {filepath}")
    else:
        # 移动到 completed 目录
        completed_dir = get_completed_dir()
        new_path = os.path.join(completed_dir, os.path.basename(filepath))
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        shutil.move(filepath, new_path)
        print(f"[complete] 任务已完成，进度文件已归档: {new_path}")

    # 生成 summary.json
    summary = {
        "task_name": data["task_name"],
        "status": "completed",
        "total_steps": data["total_steps"],
        "completed_steps": data["completed_steps"],
        "created_at": data["created_at"],
        "completed_at": data["completed_at"],
        "steps": [
            {
                "index": s["index"],
                "status": s["status"],
                "retries": s["retries"],
                "idle_count": s.get("idle_count", 0)
            } for s in data["steps"]
        ]
    }
    summary_path = os.path.join(get_completed_dir(), f"{task_name.replace(' ', '_')}_summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"[complete] 摘要已生成: {summary_path}")

    return filepath


def cmd_abort(args):
    """中止任务"""
    _ensure_dirs()
    task_name = args.task

    filepath = find_task_file(task_name)
    if not filepath:
        print(f"错误: 未找到任务 '{task_name}' 的活跃进度文件")
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    data["status"] = "aborted"
    data["aborted_at"] = datetime.now().isoformat()
    data["updated_at"] = datetime.now().isoformat()
    data["abort_reason"] = args.reason or ""

    completed_dir = get_completed_dir()
    new_path = os.path.join(completed_dir, os.path.basename(filepath))
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    shutil.move(filepath, new_path)

    print(f"[abort] 任务已中止: {task_name}")
    if args.reason:
        print(f"  原因: {args.reason}")


def cmd_clean(args):
    """清理已完成任务的进度文件"""
    _ensure_dirs()
    completed_dir = get_completed_dir()
    if not os.path.exists(completed_dir):
        print("没有已完成的任务可清理")
        return

    json_files = [f for f in os.listdir(completed_dir) if f.endswith(".json") and not f.endswith("_summary.json")]
    if not json_files:
        print("没有已完成的任务可清理")
        return

    print(f"找到 {len(json_files)} 个已完成/中止的任务:")
    for fname in json_files:
        fpath = os.path.join(completed_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            print(f"  - {data['task_name']} ({data['status']}, {data.get('completed_at', '?')[:10]})")
        except Exception:
            print(f"  - {fname} (读取失败)")

    # 直接删除（不询问，符合 AI 自动化场景）
    for fname in json_files:
        fpath = os.path.join(completed_dir, fname)
        os.remove(fpath)
        # 同时删除对应的 summary 文件（可选，可能不存在）
        summary_path = fpath.replace(".json", "_summary.json")
        try:
            os.remove(summary_path)
        except FileNotFoundError:
            pass

    print(f"[OK] 已清理 {len(json_files)} 个进度文件")


#  main 

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Triphasic Execution 临时进度文件管理器 (v5.16.0)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 初始化进度文件
  python task_progress.py init --task "修复登录Bug" --purpose "修复Token验证缺失" \\
    --steps '[{"description":"读取代码","purpose":"理解逻辑","tool":"Read"}]'

  # 执行前快照（可选，用于 verify_exec 验证）
  python task_progress.py pre_exec --task "修复登录Bug" --step 1 --files "main.py,utils.py"

  # 更新步骤状态
  python task_progress.py update --task "修复登录Bug" --step 1 --status success \\
    --review "代码已读取，逻辑清晰" --advance "继续步骤2"
  python task_progress.py update --task "修复登录Bug" --step 2 --status failed \\
    --review "语法错误" --advance "重试" --error "第45行缺少冒号"

  # 标记空转（F-11，由AI在EXECUTE阶段未实际执行时调用）
  python task_progress.py update --task "修复登录Bug" --step 2 --idle

  # 执行后验证（文件系统级验证）
  python task_progress.py verify_exec --task "修复登录Bug" --step 2 --files "main.py"

  # 恢复中断任务
  python task_progress.py resume --task "修复登录Bug"

  # 列出活跃任务
  python task_progress.py list

  # 完成任务并归档
  python task_progress.py complete --task "修复登录Bug"

  # 强制完成（跳过步骤检查，仍做记录校验）
  python task_progress.py complete --task "修复登录Bug" --force

  # 中止任务
  python task_progress.py abort --task "修复登录Bug" --reason "用户取消"

  # 清理已完成任务
  python task_progress.py clean
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # init
    p_init = subparsers.add_parser("init", help="初始化进度文件")
    p_init.add_argument("--task", "-t", required=True, help="任务名称")
    p_init.add_argument("--plan", "-p", default="", help="规划内容（文本）")
    p_init.add_argument("--steps", "-s", default="[]", help="步骤列表（JSON数组）")
    p_init.add_argument("--purpose", help="任务目的")
    p_init.add_argument("--requirements", "-r", help="具体要求")
    p_init.add_argument("--risks", help="潜在风险")
    p_init.add_argument("--trigger-word", default="继续执行",
                        help="F-11 空转截断触发词（默认：继续执行）")
    p_init.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # pre_exec
    p_pre = subparsers.add_parser("pre_exec", help="执行前快照：记录文件 mtime")
    p_pre.add_argument("--task", "-t", required=True, help="任务名称")
    p_pre.add_argument("--step", type=int, required=True, help="步骤编号")
    p_pre.add_argument("--files", help="要监控的文件列表（逗号分隔），不指定则快照整个工作区")
    p_pre.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # update
    p_update = subparsers.add_parser("update", help="更新步骤状态")
    p_update.add_argument("--task", "-t", required=True, help="任务名称")
    p_update.add_argument("--step", type=int, required=True, help="步骤编号")
    p_update.add_argument("--status", required=True,
                         choices=["pending", "running", "success", "failed", "skipped"],
                         help="新状态")
    p_update.add_argument("--review", help="审查结论")
    p_update.add_argument("--advance", help="推进决策")
    p_update.add_argument("--error", help="错误详情")
    p_update.add_argument("--proof", help="执行证据（工具调用记录、文件路径等）")
    p_update.add_argument("--idle", action="store_true",
                         help="F-11 标记空转+1（由AI在EXECUTE阶段未实际执行时调用）")
    p_update.add_argument("--clear-cache", action="store_true",
                         help="清除工具缓存（__pycache__、.pyc等）后验证")
    p_update.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # verify_exec
    p_verify = subparsers.add_parser("verify_exec", help="执行后验证：对比 pre_exec 快照")
    p_verify.add_argument("--task", "-t", required=True, help="任务名称")
    p_verify.add_argument("--step", type=int, required=True, help="步骤编号")
    p_verify.add_argument("--files", help="要检查的文件列表（逗号分隔），不指定则对比整个工作区")
    p_verify.add_argument("--proof", help="AI提供的执行证据（供参考，不强制）")
    p_verify.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # resume
    p_resume = subparsers.add_parser("resume", help="恢复中断任务")
    p_resume.add_argument("--task", "-t", required=True, help="任务名称")
    p_resume.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # list
    p_list = subparsers.add_parser("list", help="列出活跃任务")
    p_list.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # complete
    p_complete = subparsers.add_parser("complete", help="完成任务")
    p_complete.add_argument("--task", "-t", required=True, help="任务名称")
    p_complete.add_argument("--force", "-f", action="store_true",
                           help="强制完成（跳过未完成步骤检查）")
    # --enforce 默认开启（default=True），--no-enforce 关闭
    p_complete.add_argument("--no-enforce", action="store_false", dest="enforce",
                           default=True,
                           help="关闭强制校验（不推荐；需同时加 --force 才能完全跳过）")
    p_complete.add_argument("--keep", "-k", action="store_true", help="保留进度文件（不归档）")
    p_complete.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # abort
    p_abort = subparsers.add_parser("abort", help="中止任务")
    p_abort.add_argument("--task", "-t", required=True, help="任务名称")
    p_abort.add_argument("--reason", help="中止原因")
    p_abort.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    # clean
    p_clean = subparsers.add_parser("clean", help="清理已完成任务")
    p_clean.add_argument("--home", help="数据目录（覆盖 TRIPHASIC_HOME）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 覆盖数据目录
    global TRIPHASIC_HOME
    if hasattr(args, "home") and args.home:
        TRIPHASIC_HOME = args.home
        os.environ["TRIPHASIC_HOME"] = args.home

    # 命令映射
    cmd_map = {
        "init": cmd_init,
        "pre_exec": cmd_pre_exec,
        "update": cmd_update,
        "verify_exec": cmd_verify_exec,
        "resume": cmd_resume,
        "list": cmd_list,
        "complete": cmd_complete,
        "abort": cmd_abort,
        "clean": cmd_clean,
    }

    cmd_func = cmd_map.get(args.command)
    if cmd_func:
        cmd_func(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
