#!/usr/bin/env python3
"""Job Runtime Operations workflow — runtime lifecycle management.

This module implements job runtime operations:
- describe_job_detail: Query job details and existence via DescribeJobsExists
- run_jobs: Start a job (with pre-check for published config version)
- stop_jobs: Stop a running job (with status pre-check)
- trigger_savepoint: Trigger a job savepoint (with status pre-check)
"""

import sys

from client import (
    add_common_args,
    call_api,
    error_response,
    output,
    require_args,
    require_confirmation,
    success_response,
)


# ═══════════════════════════════════════════════════════════════════════════
# Job Status Constants
# ═══════════════════════════════════════════════════════════════════════════

JOB_STATUS_CREATE = 1       # 未初始化
JOB_STATUS_INITIALIZED = 2  # 未发布
JOB_STATUS_PROGRESS = 3     # 操作中
JOB_STATUS_RUNNING = 4      # 运行中
JOB_STATUS_STOPPED = 5      # 停止
JOB_STATUS_PAUSED = 6       # 暂停
JOB_STATUS_FINISHED = 7     # 完成

JOB_STATUS_DESC = {
    1: "未初始化",
    2: "未发布",
    3: "操作中",
    4: "运行中",
    5: "停止",
    6: "暂停",
    7: "完成",
}

# Status sets for pre-checks
STOPPABLE_STATUSES = {JOB_STATUS_PROGRESS, JOB_STATUS_RUNNING}
SAVEPOINT_STATUSES = {JOB_STATUS_RUNNING}

# Stop type constants
JOB_STOP_TYPE_STOP = 1      # 直接停止
JOB_STOP_TYPE_PAUSE = 2     # 触发快照后停止

JOB_STOP_TYPE_DESC = {
    1: "直接停止",
    2: "触发快照后停止",
}


# ═══════════════════════════════════════════════════════════════════════════
# Internal Helpers
# ═══════════════════════════════════════════════════════════════════════════


def _get_job_status(job_id, region, workspace_id=None):
    """Query job existence and current status via DescribeJobsExists.

    Returns:
        dict: On success: {"success": True, "job": <JobItem dict>}
              On failure: standard error_response dict
    """
    params = {"JobIds": [job_id]}
    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    result = call_api("DescribeJobsExists", params, region)
    if not result.get("success"):
        return result

    jobs = result.get("data", {}).get("Jobs", [])
    if not jobs:
        return error_response("describe_job_detail", "JobNotFound",
                              f"作业 {job_id} 不存在或无权访问")

    job_info = jobs[0]
    if not job_info.get("IsExists"):
        return error_response("describe_job_detail", "JobNotFound",
                              f"作业 {job_id} 不存在")

    job_item = job_info.get("JobItem", {})
    return {"success": True, "job": job_item}


def _get_published_version(job_id, region, workspace_id=None):
    """Query whether the job has a published config version via DescribeJobConfigs.

    Returns:
        dict: On success: {"success": True, "version": <int>, "configs": [...]}
              On failure: standard error_response dict
    """
    params = {
        "JobId": job_id,
        "Offset": 0,
        "Limit": 1,
    }
    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    result = call_api("DescribeJobConfigs", params, region)
    if not result.get("success"):
        return result

    config_set = result.get("data", {}).get("JobConfigSet", [])
    if not config_set:
        return error_response("run_jobs", "NoPublishedVersion",
                              f"作业 {job_id} 没有任何配置版本，请先发布作业配置")

    # Find the latest published version (Version > 0, not draft which is -1)
    published_versions = [c for c in config_set if c.get("Version", 0) > 0]
    if not published_versions:
        return error_response("run_jobs", "NoPublishedVersion",
                              f"作业 {job_id} 没有已发布的配置版本，请先发布作业配置")

    latest = max(published_versions, key=lambda c: c.get("Version", 0))
    return {"success": True, "version": latest.get("Version"), "configs": config_set}


# ═══════════════════════════════════════════════════════════════════════════
# Describe Job Detail
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_job_detail(args):
    """Query job details via DescribeJobsExists."""
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    params = {"JobIds": [args.job_id]}
    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id

    result = call_api("DescribeJobsExists", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Run Jobs
# ═══════════════════════════════════════════════════════════════════════════


def _describe_job_savepoints(job_id, region, workspace_id=None, limit=20, offset=0, record_types=None):
    """Query job savepoints via DescribeJobSavepoint.

    Returns:
        dict: On success: {"success": True, "data": {...}}
              On failure: standard error_response dict
    """
    params = {
        "JobId": job_id,
        "Limit": limit,
        "Offset": offset,
    }
    if workspace_id:
        params["WorkSpaceId"] = workspace_id
    if record_types:
        params["RecordTypes"] = record_types

    return call_api("DescribeJobSavepoint", params, region)


# Valid StartMode values
VALID_START_MODES = {"LATEST", "EARLIEST"}


def _resolve_start_mode(args):
    """Resolve the StartMode for RunJobs.

    Logic:
    - RunType 1 (no savepoint): StartMode defaults to "LATEST"
    - RunType 2 (from savepoint path): StartMode from savepoint, RunType set to 1, SavepointPath required
    - RunType 3 (from savepoint id): StartMode from savepoint, RunType set to 1, SavepointId required
    - RunType 4 (from timestamp): StartMode = "T{timestamp}"

    Returns:
        (start_mode, error_dict) — error_dict is None on success
    """
    run_type = int(args.run_type) if getattr(args, "run_type", None) is not None else 1
    start_mode = getattr(args, "start_mode", None)

    if run_type == 4:
        # Timestamp mode: T+Timestamp (ms)
        ts = getattr(args, "custom_timestamp", None)
        if not ts:
            return None, error_response("run_jobs", "ValidationError",
                                        "run_type=4 时必须通过 --custom_timestamp 提供时间戳（毫秒）")
        return f"T{ts}", None

    if start_mode:
        # User explicitly provided start_mode
        upper = start_mode.upper()
        if upper in VALID_START_MODES:
            return upper, None
        # Allow T+Timestamp format
        if upper.startswith("T") and upper[1:].isdigit():
            return upper, None
        return None, error_response("run_jobs", "ValidationError",
                                    f"无效的 start_mode: '{start_mode}'，仅支持 LATEST、EARLIEST 或 T+时间戳")

    # Default: LATEST (no savepoint, fresh start)
    return "LATEST", None


def cmd_run_jobs(args):
    """Start a job. Pre-checks that a published config version exists.

    Workflow:
    1. DescribeJobsExists - verify job exists
    2. DescribeJobConfigs - verify published version exists
    3. If run_type is NOT specified:
       - Query savepoints; if savepoints exist, return needs_selection response
         asking user to choose: (A) start without savepoint or (B) restore from savepoint
       - If no savepoints, proceed with run_type=1 automatically
    4. If run_type=3 and no savepoint_id, query savepoints:
       - If no savepoints exist, return needs_selection asking user to confirm
         whether to start without savepoint or cancel (NO silent fallback)
       - If savepoints exist, return list for user to pick one
    5. require_confirmation - safety gate
    6. RunJobs - start the job with StartMode

    StartMode is REQUIRED by the backend:
    - "LATEST": Start without savepoint (default for run_type=1)
    - "EARLIEST": Start from earliest offset
    - "T{timestamp}": Start from specific timestamp (for run_type=4)

    For savepoint-based restart (run_type=2 or 3):
    - run_type=2: Provide --savepoint_path directly
    - run_type=3: Provide --savepoint_id (use describe_job_savepoints to list)
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_id = args.job_id
    region = args.region
    workspace_id = getattr(args, "workspace_id", None)

    # ── Step 1: Check job existence and status ────────────────────────
    if args.verbose:
        print(f"[run_jobs] Step 1: 查询作业 {job_id} 状态...", file=sys.stderr)

    job_result = _get_job_status(job_id, region, workspace_id)
    if not job_result.get("success"):
        return output(job_result, args.output)

    job = job_result["job"]
    status = job.get("Status", 0)
    status_desc = JOB_STATUS_DESC.get(status, f"未知({status})")

    # Check if job is already running
    if status == JOB_STATUS_RUNNING:
        return output(error_response("run_jobs", "JobAlreadyRunning",
                                     f"作业 {job_id} 当前已在运行中，无需重复启动"), args.output)
    if status == JOB_STATUS_PROGRESS:
        return output(error_response("run_jobs", "JobInProgress",
                                     f"作业 {job_id} 当前处于操作中状态，请等待操作完成"), args.output)

    # ── Step 2: Check published config version ────────────────────────
    if args.verbose:
        print("[run_jobs] Step 2: 检查已发布配置版本...", file=sys.stderr)

    version_result = _get_published_version(job_id, region, workspace_id)
    if not version_result.get("success"):
        return output(version_result, args.output)

    published_version = version_result["version"]
    if args.verbose:
        print(f"[run_jobs] 已发布版本: {published_version}", file=sys.stderr)

    # ── Step 3: Resolve RunType and StartMode ────────────────────────
    explicit_run_type = getattr(args, "run_type", None)

    # ── Step 3a: If run_type not specified, query savepoints and ask user to choose ──
    if explicit_run_type is None:
        if args.verbose:
            print("[run_jobs] run_type 未指定，查询快照列表以让用户选择启动模式...", file=sys.stderr)

        sp_result = _describe_job_savepoints(job_id, region, workspace_id)
        # Build savepoint candidates (may be empty)
        savepoints = []
        if sp_result.get("success"):
            sp_data = sp_result.get("data", {})
            savepoints = sp_data.get("Savepoint", [])

        if savepoints:
            # Has savepoints — present options for user to choose
            candidates = []
            for i, sp in enumerate(savepoints[:10]):
                candidates.append({
                    "index": i + 1,
                    "savepoint_id": sp.get("SerialId", ""),
                    "status": sp.get("Status", 0),
                    "status_desc": SAVEPOINT_STATUS_DESC.get(sp.get("Status"), "未知"),
                    "record_type": sp.get("RecordType", 0),
                    "record_type_desc": SAVEPOINT_RECORD_TYPE_DESC.get(sp.get("RecordType"), "未知"),
                    "path": sp.get("Path", ""),
                    "create_time": sp.get("CreateTime", ""),
                    "size": sp.get("Size", 0),
                    "description": sp.get("Description", ""),
                })

            return output(success_response("run_jobs", {
                "needs_selection": True,
                "message": f"作业 {job_id} 存在 {len(savepoints)} 个可用快照，请选择启动模式",
                "options": [
                    {"option": "A", "run_type": 1, "description": "不使用快照，直接启动（从最新状态开始，不保留历史 state）"},
                    {"option": "B", "run_type": 3, "description": "从历史快照恢复启动（保留 state，需选择一个快照）"},
                ],
                "savepoint_total": len(savepoints),
                "savepoint_candidates": candidates,
                "hint": "请询问用户选择启动模式：选 A 则使用 --run_type 1，选 B 则使用 --run_type 3 --savepoint_id <SerialId>",
            }), args.output)
        else:
            # No savepoints — inform and proceed with run_type=1 automatically
            if args.verbose:
                print("[run_jobs] 无可用快照，将以 run_type=1 (无快照直接启动) 执行", file=sys.stderr)
            explicit_run_type = "1"

    run_type = int(explicit_run_type)

    # ── Step 3b: For savepoint-based start, validate savepoint info ───
    if run_type == 2 and not getattr(args, "savepoint_path", None):
        return output(error_response("run_jobs", "ValidationError",
                                     "run_type=2 时必须通过 --savepoint_path 提供快照路径"), args.output)

    if run_type == 3 and not getattr(args, "savepoint_id", None):
        # Query savepoints and return the list for user selection
        if args.verbose:
            print("[run_jobs] run_type=3 但未指定 savepoint_id，查询快照列表...", file=sys.stderr)
        sp_result = _describe_job_savepoints(job_id, region, workspace_id)
        if not sp_result.get("success"):
            return output(sp_result, args.output)

        sp_data = sp_result.get("data", {})
        savepoints = sp_data.get("Savepoint", [])
        if not savepoints:
            # No savepoints available — do NOT silently fall back; ask user to confirm next step
            return output(success_response("run_jobs", {
                "needs_selection": True,
                "message": f"作业 {job_id} 当前没有可用的快照记录，无法从快照恢复启动",
                "options": [
                    {"option": "A", "run_type": 1, "description": "改为不使用快照直接启动（从最新状态开始）"},
                    {"option": "B", "run_type": None, "description": "取消启动，暂不操作"},
                ],
                "hint": "请询问用户：没有可用快照，是否改为不使用快照直接启动（--run_type 1），还是取消本次启动操作？",
            }), args.output)

        # Return savepoint list for user to choose
        candidates = []
        for i, sp in enumerate(savepoints[:10]):
            candidates.append({
                "index": i + 1,
                "savepoint_id": sp.get("SerialId", ""),
                "status": sp.get("Status", 0),
                "status_desc": SAVEPOINT_STATUS_DESC.get(sp.get("Status"), "未知"),
                "record_type": sp.get("RecordType", 0),
                "record_type_desc": SAVEPOINT_RECORD_TYPE_DESC.get(sp.get("RecordType"), "未知"),
                "path": sp.get("Path", ""),
                "create_time": sp.get("CreateTime", ""),
                "size": sp.get("Size", 0),
                "description": sp.get("Description", ""),
            })

        return output(success_response("run_jobs", {
            "needs_selection": True,
            "message": f"作业 {job_id} 有 {len(savepoints)} 个快照，请选择一个并使用 --savepoint_id <id> 指定",
            "total": sp_data.get("TotalNumber", len(savepoints)),
            "candidates": candidates,
            "hint": "请使用 --savepoint_id <SerialId> 指定快照后重新执行 run_jobs --run_type 3",
        }), args.output)

    # Resolve start_mode value
    start_mode, mode_err = _resolve_start_mode(args)
    if mode_err:
        return output(mode_err, args.output)

    if args.verbose:
        print(f"[run_jobs] StartMode: {start_mode}, RunType: {run_type}", file=sys.stderr)

    # ── Step 4: Confirmation gate ─────────────────────────────────────
    job_name = job.get("Name", job_id)
    mode_desc = f"启动模式: {start_mode}"
    if run_type in (2, 3):
        sp_info = getattr(args, "savepoint_id", None) or getattr(args, "savepoint_path", None) or ""
        mode_desc += f"，从快照恢复: {sp_info}"

    chk = require_confirmation(
        "run_jobs",
        f"即将启动作业 '{job_name}' ({job_id})，使用配置版本 {published_version}，{mode_desc}。",
        getattr(args, "confirm", False),
    )
    if chk:
        return output(chk, args.output)

    # ── Step 5: Run the job ───────────────────────────────────────────
    if args.verbose:
        print("[run_jobs] Step 4: 执行 RunJobs...", file=sys.stderr)

    # Determine config version to use
    config_version = int(args.config_version) if getattr(args, "config_version", None) else published_version

    run_desc = {
        "JobId": job_id,
        "RunType": run_type,
        "JobConfigVersion": config_version,
        "StartMode": start_mode,
    }

    # Savepoint info
    if getattr(args, "savepoint_path", None):
        run_desc["SavepointPath"] = args.savepoint_path
    if getattr(args, "savepoint_id", None):
        run_desc["SavepointId"] = args.savepoint_id

    params = {"RunJobDescriptions": [run_desc]}
    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    result = call_api("RunJobs", params, region)

    if result.get("success"):
        result = success_response("run_jobs", {
            "message": f"作业 '{job_name}' ({job_id}) 启动请求已提交",
            "job_id": job_id,
            "config_version": config_version,
            "start_mode": start_mode,
            "run_type": run_type,
        }, result.get("request_id", ""))

    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Describe Job Savepoints
# ═══════════════════════════════════════════════════════════════════════════


# Savepoint RecordType descriptions
SAVEPOINT_RECORD_TYPE_DESC = {
    1: "手动触发",
    2: "Checkpoint",
    3: "停止触发",
}

# Savepoint Status descriptions
SAVEPOINT_STATUS_DESC = {
    1: "进行中",
    2: "完成",
    3: "失败",
    4: "超时",
}


def cmd_describe_job_savepoints(args):
    """Query job savepoints via DescribeJobSavepoint.

    Returns the list of available savepoints for a job, useful for:
    - Viewing savepoint history
    - Selecting a savepoint for restart (run_type=3)
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_id = args.job_id
    region = args.region
    workspace_id = getattr(args, "workspace_id", None)
    limit = int(args.limit) if getattr(args, "limit", None) else 20
    offset = int(args.offset) if getattr(args, "offset", None) else 0
    record_types = None
    if getattr(args, "record_types", None):
        record_types = [int(x.strip()) for x in args.record_types.split(",")]

    result = _describe_job_savepoints(job_id, region, workspace_id, limit, offset, record_types)
    if not result.get("success"):
        return output(result, args.output)

    # Enrich response with human-readable descriptions
    data = result.get("data", {})
    savepoints = data.get("Savepoint", [])
    for sp in savepoints:
        sp["RecordTypeDesc"] = SAVEPOINT_RECORD_TYPE_DESC.get(sp.get("RecordType"), "未知")
        sp["StatusDesc"] = SAVEPOINT_STATUS_DESC.get(sp.get("Status"), "未知")

    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Stop Jobs
# ═══════════════════════════════════════════════════════════════════════════


def cmd_stop_jobs(args):
    """Stop a running job. Pre-checks that the job is in a stoppable state (running or in-progress).

    Workflow:
    1. DescribeJobsExists - verify job exists and check status
    2. Validate status in {3: 操作中, 4: 运行中}
    3. If stop_type is NOT specified, return needs_selection asking user to choose:
       - Option A: 直接停止 (stop_type=1)
       - Option B: 触发快照后停止 (stop_type=2, recommended for production)
    4. require_confirmation - safety gate (destructive)
    5. StopJobs - stop the job
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_id = args.job_id
    region = args.region
    workspace_id = getattr(args, "workspace_id", None)

    # ── Step 1: Check job status ──────────────────────────────────────
    if args.verbose:
        print(f"[stop_jobs] Step 1: 查询作业 {job_id} 状态...", file=sys.stderr)

    job_result = _get_job_status(job_id, region, workspace_id)
    if not job_result.get("success"):
        return output(job_result, args.output)

    job = job_result["job"]
    status = job.get("Status", 0)
    status_desc = JOB_STATUS_DESC.get(status, f"未知({status})")

    # ── Step 2: Validate stoppable status ─────────────────────────────
    if status not in STOPPABLE_STATUSES:
        return output(error_response(
            "stop_jobs", "InvalidJobStatus",
            f"作业 {job_id} 当前状态为「{status_desc}」(status={status})，"
            f"仅运行中(4)或操作中(3)的作业可以停止"
        ), args.output)

    # ── Step 3: If stop_type not specified, ask user to choose ────────
    job_name = job.get("Name", job_id)
    explicit_stop_type = getattr(args, "stop_type", None)

    if explicit_stop_type is None:
        return output(success_response("stop_jobs", {
            "needs_selection": True,
            "message": f"即将停止作业 '{job_name}' ({job_id})，当前状态: {status_desc}，请选择停止方式",
            "options": [
                {"option": "A", "stop_type": 1, "description": "直接停止（立即停止，不生成快照，可能丢失未持久化的状态）"},
                {"option": "B", "stop_type": 2, "description": "触发快照后停止（推荐，先生成快照保留作业状态，再停止作业）"},
            ],
            "hint": "请询问用户选择停止方式：选 A 则使用 --stop_type 1，选 B 则使用 --stop_type 2",
        }), args.output)

    stop_type = int(explicit_stop_type)
    stop_type_desc = JOB_STOP_TYPE_DESC.get(stop_type, f"未知({stop_type})")

    # ── Step 4: Confirmation gate (destructive) ───────────────────────
    chk = require_confirmation(
        "stop_jobs",
        f"即将停止作业 '{job_name}' ({job_id})，当前状态: {status_desc}，停止方式: {stop_type_desc}。",
        getattr(args, "confirm", False),
    )
    if chk:
        return output(chk, args.output)

    # ── Step 5: Stop the job ──────────────────────────────────────────
    if args.verbose:
        print("[stop_jobs] Step 3: 执行 StopJobs...", file=sys.stderr)

    stop_desc = {"JobId": job_id, "StopType": stop_type}

    params = {"StopJobDescriptions": [stop_desc]}
    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    result = call_api("StopJobs", params, region)

    if result.get("success"):
        result = success_response("stop_jobs", {
            "message": f"作业 '{job_name}' ({job_id}) 停止请求已提交，停止方式: {stop_type_desc}",
            "job_id": job_id,
            "stop_type": stop_type,
        }, result.get("request_id", ""))

    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Trigger Job Savepoint
# ═══════════════════════════════════════════════════════════════════════════


def cmd_trigger_savepoint(args):
    """Trigger a savepoint for a running job. Pre-checks that the job is running.

    Workflow:
    1. DescribeJobsExists - verify job exists and check status
    2. Validate status == 4 (运行中)
    3. TriggerJobSavepoint - trigger the savepoint
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_id = args.job_id
    region = args.region
    workspace_id = getattr(args, "workspace_id", None)

    # ── Step 1: Check job status ──────────────────────────────────────
    if args.verbose:
        print(f"[trigger_savepoint] Step 1: 查询作业 {job_id} 状态...", file=sys.stderr)

    job_result = _get_job_status(job_id, region, workspace_id)
    if not job_result.get("success"):
        return output(job_result, args.output)

    job = job_result["job"]
    status = job.get("Status", 0)
    status_desc = JOB_STATUS_DESC.get(status, f"未知({status})")

    # ── Step 2: Validate running status ───────────────────────────────
    if status not in SAVEPOINT_STATUSES:
        return output(error_response(
            "trigger_savepoint", "InvalidJobStatus",
            f"作业 {job_id} 当前状态为「{status_desc}」(status={status})，"
            f"仅运行中(4)的作业可以触发快照"
        ), args.output)

    # ── Step 3: Trigger savepoint ─────────────────────────────────────
    if args.verbose:
        print("[trigger_savepoint] Step 2: 执行 TriggerJobSavepoint...", file=sys.stderr)

    params = {"JobId": job_id}
    if workspace_id:
        params["WorkSpaceId"] = workspace_id
    if getattr(args, "description", None):
        params["Description"] = args.description

    result = call_api("TriggerJobSavepoint", params, region)

    if result.get("success"):
        data = result.get("data", {})
        job_name = job.get("Name", job_id)
        result = success_response("trigger_savepoint", {
            "message": f"作业 '{job_name}' ({job_id}) 快照触发成功",
            "job_id": job_id,
            "savepoint_trigger": data.get("SavepointTrigger", False),
            "savepoint_id": data.get("SavepointId", ""),
            "savepoint_path": data.get("FinalSavepointPath", ""),
        }, result.get("request_id", ""))

    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Subparser Registration
# ═══════════════════════════════════════════════════════════════════════════


def register(subparsers):
    """Register all job runtime operation subcommands."""

    def _add(name, help_text, func, extra_args=None):
        p = subparsers.add_parser(name, help=help_text)
        add_common_args(p)
        if extra_args:
            extra_args(p)
        p.set_defaults(func=func, subcommand=name)

    # ── Describe Job Detail ───────────────────────────────────────────

    def _describe_job_detail_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")

    _add("describe_job_detail", "Query job details and existence",
         cmd_describe_job_detail, _describe_job_detail_args)

    # ── Run Jobs ──────────────────────────────────────────────────────

    def _run_jobs_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--run_type", default=None,
                       help="Run type: 1=direct start, 2=from savepoint path, 3=from savepoint id, 4=from timestamp. "
                            "If omitted, the CLI will query savepoints and ask user to choose a start mode.")
        p.add_argument("--config_version",
                       help="Config version to use (default: latest published version)")
        p.add_argument("--start_mode", default="LATEST",
                       help="Start mode: LATEST (default, no savepoint), EARLIEST, or T+timestamp(ms)")
        p.add_argument("--savepoint_path",
                       help="Savepoint path (for run_type=2)")
        p.add_argument("--savepoint_id",
                       help="Savepoint ID (for run_type=3, use describe_job_savepoints to list)")
        p.add_argument("--custom_timestamp",
                       help="Custom timestamp in ms (for run_type=4)")
        p.add_argument("--confirm", action="store_true",
                       help="Skip interactive confirmation")

    _add("run_jobs", "Start a job (requires published config version, StartMode defaults to LATEST)",
         cmd_run_jobs, _run_jobs_args)

    # ── Stop Jobs ─────────────────────────────────────────────────────

    def _stop_jobs_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--stop_type", default=None,
                       help="Stop type: 1=immediate stop, 2=trigger savepoint then stop (pause). "
                            "If omitted, the CLI will ask user to choose.")
        p.add_argument("--confirm", action="store_true",
                       help="Skip interactive confirmation")

    _add("stop_jobs", "Stop a running job (requires running/in-progress status)",
         cmd_stop_jobs, _stop_jobs_args)

    # ── Trigger Savepoint ─────────────────────────────────────────────

    def _trigger_savepoint_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--description",
                       help="Savepoint description (max 50 chars)")

    _add("trigger_savepoint", "Trigger a savepoint for a running job",
         cmd_trigger_savepoint, _trigger_savepoint_args)

    # ── Describe Job Savepoints ───────────────────────────────────────

    def _describe_job_savepoints_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--limit", default="20", help="Max results (default: 20)")
        p.add_argument("--offset", default="0", help="Offset (default: 0)")
        p.add_argument("--record_types",
                       help="Filter by record types (comma-separated): 1=手动触发, 2=Checkpoint, 3=停止触发")

    _add("describe_job_savepoints", "Query job savepoint list",
         cmd_describe_job_savepoints, _describe_job_savepoints_args)
