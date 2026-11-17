#!/usr/bin/env python3
"""Job Development — atomic commands for SQL & JAR job lifecycle.

This module provides the following atomic CLI commands:
- create_job: Create a new job in a workspace (SQL or JAR)
- describe_jobs: Query existing jobs
- describe_job_configs: Query job configurations / draft
- modify_draft: Modify and save draft configuration (SQL code or JAR config)
- check_sql: Deep SQL grammar check (SQL jobs only)
- create_job_config: Publish current draft as a new version (with draft confirmation)

Helper utilities are in separate modules:
- folder_management: Folder CRUD operations
- job_config_helpers: SQL/JAR payload builders, constants, draft confirmation
- resource_change_ops: Resource change processing utilities
"""

import json
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
from resource_resolver import resolve_all

# Import from extracted modules
from job_config_helpers import (
    JOB_TYPE_SQL,
    JOB_TYPE_JAR,
    _JOB_TYPE_NAMES,
    encode_sql,
    build_sql_program_args,
    require_job_type,
    read_sql_input,
    resolve_resource_refs,
    validate_resource_refs_for_job_type,
    format_draft_summary,
    confirm_draft_before_publish,
    merge_properties,
    ensure_hive_properties,
    detect_hive_in_properties,
    _CATALOG_TYPE_HIVE,
)
from folder_management import resolve_or_create_folder


# ═══════════════════════════════════════════════════════════════════════════
# Create Job
# ═══════════════════════════════════════════════════════════════════════════


def cmd_create_job(args):
    """Create a new job (SQL or JAR) in the specified workspace.

    Supports automatic parameter resolution:
    - Region: Chinese name / English / ap-xxx (default: ap-guangzhou)
    - Workspace: name / space-xxx (default: "default")
    - Cluster: name / cluster-xxx (if not specified, lists candidates)
    - Flink/JDK version: auto-detected from cluster (default: Flink-1.16, JDK 8)
    """
    err = require_args(args, "name")
    if err:
        return output(err, args.output)

    job_type = int(args.job_type)
    if job_type not in (JOB_TYPE_SQL, JOB_TYPE_JAR):
        return output(error_response(
            "create_job",
            "ValidationError",
            "--job_type 必须为 1 (SQL) 或 2 (JAR)",
        ), args.output)
    job_type_name = _JOB_TYPE_NAMES[job_type]

    # Run parameter resolution chain
    resolved = resolve_all(args)

    if not resolved.get("success"):
        return output(resolved, args.output)

    # If cluster selection is needed, output candidates and exit
    if resolved.get("needs_selection"):
        candidates = resolved.get("candidates", [])
        message = resolved.get("message", "请选择集群:")

        # Format candidate list for display
        candidate_list = []
        for i, c in enumerate(candidates, 1):
            version = c.get("version", {})
            flink = version.get("Flink", "N/A")
            supported_flink = version.get("SupportedFlink", [])
            candidate_list.append({
                "index": i,
                "cluster_id": c["cluster_id"],
                "name": c["name"],
                "free_cu": c["free_cu"],
                "cu_num": c["cu_num"],
                "flink_version": flink,
                "supported_flink": supported_flink,
            })

        result = success_response("resolve_cluster", {
            "message": message,
            "region": resolved.get("region", ""),
            "workspace_id": resolved.get("workspace_id", ""),
            "workspace_name": resolved.get("workspace_name", ""),
            "candidates": candidate_list,
            "hint": "请使用 --cluster_id <cluster-xxx> 或 --cluster_name <名称> 指定集群后重新执行",
        })
        return output(result, args.output)

    # All parameters resolved - proceed with creation

    # Resolve folder: --folder_id takes priority, --folder_name triggers query/create
    folder_id, folder_err = resolve_or_create_folder(args, resolved["region"], resolved["workspace_id"])
    if folder_err:
        return output(folder_err, args.output)

    chk = require_confirmation(
        "create_job",
        f"Create {job_type_name} job '{args.name}' in cluster {resolved['cluster_id']} "
        f"({resolved['cluster_name']})"
        + (f", folder={folder_id}" if folder_id else "")
        + ".",
        args.confirm,
    )
    if chk:
        return output(chk, args.output)

    params = {
        "Name": args.name,
        "JobType": job_type,
        "ClusterType": int(args.cluster_type) if args.cluster_type else 2,
        "ClusterId": resolved["cluster_id"],
        "WorkSpaceId": resolved["workspace_id"],
        "FlinkVersion": resolved["flink_version"],
    }

    if resolved.get("jdk_version"):
        params["JdkVersion"] = resolved["jdk_version"]
    if folder_id:
        params["FolderId"] = folder_id
    if args.cu_mem:
        params["CuMem"] = int(args.cu_mem)
    if args.remark:
        params["Remark"] = args.remark
    if args.description:
        params["Description"] = args.description

    # Print resolution summary in verbose mode
    if args.verbose:
        print(
            f"[create_job] 参数解析完成:\n"
            f"  作业类型: {job_type_name} (JobType={job_type})\n"
            f"  地域: {resolved['region']} ({resolved.get('region_desc', '')})\n"
            f"  工作空间: {resolved['workspace_id']} ({resolved.get('workspace_name', '')})\n"
            f"  集群: {resolved['cluster_id']} ({resolved.get('cluster_name', '')})\n"
            f"  Flink版本: {resolved['flink_version']}\n"
            f"  JDK版本: {resolved.get('jdk_version', 'N/A')}\n",
            file=sys.stderr,
        )

    result = call_api("CreateJob", params, resolved["region"])
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Describe Jobs
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_jobs(args):
    """Query jobs in the specified workspace using tree structure (DescribeTreeJobs)."""
    err = require_args(args, "region")
    if err:
        return output(err, args.output)

    params = {}

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id
    if getattr(args, "filters", None):
        filters = []
        for f in args.filters.split(";"):
            parts = f.split("=", 1)
            if len(parts) == 2:
                filters.append({"Name": parts[0], "Values": [parts[1]]})
        if filters:
            params["Filters"] = filters
    if getattr(args, "category", None):
        params["Category"] = args.category
    if getattr(args, "parent_id", None):
        params["ParentId"] = args.parent_id
    if getattr(args, "page_size", None) is not None:
        params["PageSize"] = int(args.page_size)
    if getattr(args, "page_attach", None):
        params["PageAttach"] = args.page_attach

    result = call_api("DescribeTreeJobs", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Describe Job Configs
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_job_configs(args):
    """Query job configurations or draft for a given job."""
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    params = {"JobId": args.job_id}

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id
    if getattr(args, "only_draft", False):
        params["OnlyDraft"] = True
    if getattr(args, "versions", None):
        params["JobConfigVersions"] = [int(v) for v in args.versions.split(",")]
    if args.offset is not None:
        params["Offset"] = int(args.offset)
    if args.limit is not None:
        params["Limit"] = int(args.limit)

    result = call_api("DescribeJobConfigs", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Modify Draft (SQL / JAR)
# ═══════════════════════════════════════════════════════════════════════════


def cmd_modify_draft(args):
    """Modify and save draft configuration.

    For SQL jobs: writes SQL code into ProgramArgs.SqlCode (base64 encoded).
    For JAR jobs: writes EntrypointClass, ProgramArgs, ResourceRefs into draft.

    Properties handling:
    - Existing Properties from the current draft are always preserved.
    - If the job references a Hive catalog, HADOOP_USER_NAME properties are
      auto-injected (merged, not replacing existing entries).
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_type, jt_err = require_job_type(args, "modify_draft")
    if jt_err:
        return output(jt_err, args.output)

    params = {
        "JobId": args.job_id,
        "JobVersion": -1,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id

    # Resolve existing ProgramArgs, Properties, and Metadata from current draft
    existing_pa = getattr(args, "existing_program_args", None)
    existing_metadata = None  # Decoded Metadata dict from the existing draft
    existing_properties = []  # Existing Properties from the draft (backend-populated)
    if not existing_pa:
        draft_params = {"JobId": args.job_id, "OnlyDraft": True}
        if args.workspace_id:
            draft_params["WorkSpaceId"] = args.workspace_id
        draft_resp = call_api("DescribeJobConfigs", draft_params, args.region)
        if draft_resp.get("success"):
            cfgs = draft_resp.get("data", {}).get("JobConfigSet", []) or []
            if cfgs:
                existing_pa = cfgs[0].get("ProgramArgs", "") or "{}"
                # Preserve existing Properties from the draft
                existing_properties = cfgs[0].get("Properties", []) or []
                # Extract existing Metadata to get backend-populated Catalogs
                # (uppercase C) which contains correct catalogVersion etc.
                try:
                    import base64 as _b64
                    _pa_obj = json.loads(existing_pa) if isinstance(existing_pa, str) else existing_pa
                    _meta_raw = _pa_obj.get("Metadata", "")
                    if _meta_raw:
                        try:
                            existing_metadata = json.loads(_meta_raw)
                        except (json.JSONDecodeError, ValueError):
                            # Try base64 decode
                            _padded = _meta_raw + "=" * (4 - len(_meta_raw) % 4) if len(_meta_raw) % 4 else _meta_raw
                            existing_metadata = json.loads(_b64.b64decode(_padded).decode("utf-8"))
                except Exception:
                    existing_metadata = None
        if not existing_pa:
            existing_pa = "{}"

    resource_refs, refs_err = resolve_resource_refs(args, job_type, "modify_draft")
    if refs_err:
        return output(refs_err, args.output)

    has_hive = False  # Track whether Hive catalog is referenced

    if job_type == JOB_TYPE_JAR:
        entrypoint_class = getattr(args, "entrypoint_class", None)
        program_args_str = getattr(args, "program_args", None)

        if not entrypoint_class and not program_args_str and resource_refs is None:
            return output(error_response("modify_draft", "ValidationError",
                "JAR 作业需提供 --entrypoint_class、--program_args 或 --resource_refs 中至少一个参数"), args.output)

        if entrypoint_class is not None:
            params["EntrypointClass"] = entrypoint_class
        if program_args_str is not None:
            params["ProgramArgs"] = program_args_str
        if resource_refs is not None:
            params["ResourceRefs"] = resource_refs
    else:
        sql_code = read_sql_input(args)
        if not sql_code:
            return output(error_response("modify_draft", "ValidationError", "SQL 作业必须通过 --sql 或 --sql_file 提供 SQL 代码"), args.output)

        # Parse --catalog_refs if provided
        catalog_refs = None
        raw_cat_refs = getattr(args, "catalog_refs", None)
        if raw_cat_refs:
            try:
                catalog_refs = json.loads(raw_cat_refs)
            except (json.JSONDecodeError, TypeError):
                return output(error_response("modify_draft", "ValidationError",
                    "--catalog_refs 不是合法 JSON，格式: '[{\"catalog\":\"name\",\"database\":\"db\",\"table\":\"tbl\"}]'"), args.output)

        # Parse --reference_tables if provided
        reference_tables = None
        raw_ref_tables = getattr(args, "reference_tables", None)
        if raw_ref_tables:
            try:
                reference_tables = json.loads(raw_ref_tables)
            except (json.JSONDecodeError, TypeError):
                return output(error_response("modify_draft", "ValidationError",
                    "--reference_tables 不是合法 JSON，格式: '[{\"catalog\":\"c\",\"database\":\"db\",\"table\":\"tbl\",\"version\":1}]'"), args.output)

        program_args, unresolved, has_hive = build_sql_program_args(
            existing_pa, sql_code,
            region=args.region,
            workspace_id=getattr(args, "workspace_id", None),
            catalog_refs=catalog_refs,
            reference_tables=reference_tables,
            existing_metadata=existing_metadata,
            cluster_id=getattr(args, "cluster_id", None),
            flink_version=getattr(args, "flink_version", None),
            verbose=getattr(args, "verbose", False),
        )
        params["ProgramArgs"] = program_args
        if unresolved:
            print(
                f"[modify_draft] WARNING: SQL 中的 ${{...}} 占位符无法在工作空间变量列表中找到: "
                f"{sorted(set(unresolved))}。已按缺省值写入 Metadata；运行时如该变量缺失会导致作业启动失败。"
                f" 请使用 `describe_variables --workspace_id <id> --name <var>` 核实，或先在控制台创建对应变量。",
                file=sys.stderr,
            )
        if resource_refs is not None:
            params["ResourceRefs"] = resource_refs

    if getattr(args, "default_parallelism", None):
        params["DefaultParallelism"] = int(args.default_parallelism)
    if getattr(args, "flink_version", None):
        params["FlinkVersion"] = args.flink_version
    if getattr(args, "jdk_version", None):
        params["JdkVersion"] = str(args.jdk_version)
    if getattr(args, "remark", None):
        params["Remark"] = args.remark

    # ── Properties: preserve existing + inject Hive HADOOP_USER_NAME ──
    # Also check existing Metadata catalogs for Hive type if catalog_refs
    # was not explicitly provided but the draft already has Hive catalogs.
    if not has_hive and existing_metadata:
        meta_inner = existing_metadata.get("Metadata", {})
        for cat in (meta_inner.get("Catalogs") or meta_inner.get("catalogs") or []):
            if cat.get("type") == _CATALOG_TYPE_HIVE:
                has_hive = True
                break

    final_properties = ensure_hive_properties(
        existing_properties, has_hive,
        verbose=getattr(args, "verbose", False),
    )
    if final_properties:
        params["Properties"] = final_properties

    result = call_api("ModifyDraftConfig", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Check SQL Deep Grammar
# ═══════════════════════════════════════════════════════════════════════════


def cmd_check_sql(args):
    """Run deep grammar check on SQL code."""
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    sql_code = read_sql_input(args)
    if not sql_code:
        return output(error_response("check_sql", "必须通过 --sql 或 --sql_file 提供 SQL 代码"), args.output)

    # Auto-resolve ClusterId from job detail; --cluster_id overrides if provided
    cluster_id = getattr(args, "cluster_id", None)
    if not cluster_id:
        cluster_id = _resolve_cluster_id_for_check(
            args.job_id, args.region,
            getattr(args, "workspace_id", None),
            "check_sql",
            getattr(args, "verbose", False),
        )

    params = {
        "JobId": args.job_id,
        "SqlCode": encode_sql(sql_code),
        "ActionMode": 1,
        "IsAsync": 0,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id
    if cluster_id:
        params["ClusterId"] = cluster_id

    result = call_api("CheckSqlDeepGrammar", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Internal helper: resolve ClusterId for SQL grammar check
# ═══════════════════════════════════════════════════════════════════════════


def _resolve_cluster_id_for_check(job_id, region, workspace_id, operation, verbose=False):
    """Resolve the ClusterId bound to a job via DescribeJobsExists.

    Used by check_sql to auto-fill ClusterId for CheckSqlDeepGrammar
    without requiring external --cluster_id input.

    Returns:
        str or None: The ClusterId if found, else None (caller should proceed
        without it — the API may still work or return a clear error).
    """
    params = {"JobIds": [job_id]}
    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    result = call_api("DescribeJobsExists", params, region)
    if not result.get("success"):
        if verbose:
            print(
                f"[{operation}] WARNING: 无法获取作业详情以解析 ClusterId: "
                f"{result.get('error', '')}",
                file=sys.stderr,
            )
        return None

    jobs = result.get("data", {}).get("Jobs", [])
    if not jobs:
        return None

    job_info = jobs[0]
    job_item = job_info.get("JobItem", {})
    cluster_id = job_item.get("ClusterId", "")

    if verbose and cluster_id:
        print(
            f"[{operation}] 自动获取作业绑定集群: {cluster_id}",
            file=sys.stderr,
        )

    return cluster_id or None


# ═══════════════════════════════════════════════════════════════════════════
# Create Job Config (publish new version from current draft)
# ═══════════════════════════════════════════════════════════════════════════


def cmd_create_job_config(args):
    """Publish the current draft as a new job config version.

    This is an atomic command that:
    1. Reads the current draft (DescribeJobConfigs OnlyDraft=true)
    2. Shows a draft summary for human review
    3. Requires confirmation (unless --skip_draft_confirm)
    4. Calls CreateJobConfig API to publish a new version

    The draft content should already be prepared via `modify_draft` before
    calling this command.
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_type, jt_err = require_job_type(args, "create_job_config")
    if jt_err:
        return output(jt_err, args.output)

    region = args.region
    job_id = args.job_id
    workspace_id = getattr(args, "workspace_id", None)
    verbose = getattr(args, "verbose", False)
    is_jar = job_type == JOB_TYPE_JAR
    job_type_name = _JOB_TYPE_NAMES.get(job_type, str(job_type))

    # ── Step 1: Read current draft ────────────────────────────────────
    if verbose:
        print("[create_job_config] 获取当前草稿配置...", file=sys.stderr)

    params_desc = {"JobId": job_id, "OnlyDraft": True}
    if workspace_id:
        params_desc["WorkSpaceId"] = workspace_id

    result = call_api("DescribeJobConfigs", params_desc, region)
    if not result.get("success"):
        return output(error_response("create_job_config", "DescribeJobConfigsFailed",
                                     f"获取草稿失败: {result.get('error', '')}"), args.output)

    config_set = result.get("data", {}).get("JobConfigSet", [])
    if not config_set:
        return output(error_response("create_job_config", "DraftNotFound",
                                     "未找到草稿配置，请先通过 modify_draft 准备草稿"), args.output)

    draft = config_set[0]

    # ── Step 2: Show draft summary and confirm ────────────────────────
    sql_code = None
    entrypoint_class = None
    program_args = None
    resource_refs = draft.get("ResourceRefs")
    draft_properties = draft.get("Properties", []) or []

    if is_jar:
        entrypoint_class = draft.get("EntrypointClass", "")
        program_args = draft.get("ProgramArgs", "")
    else:
        # Decode SQL from ProgramArgs.SqlCode for display
        pa_str = draft.get("ProgramArgs", "{}")
        try:
            pa_obj = json.loads(pa_str) if isinstance(pa_str, str) else pa_str
            import base64
            sql_b64 = pa_obj.get("SqlCode", "")
            if sql_b64:
                sql_code = base64.b64decode(sql_b64).decode("utf-8")
        except Exception:
            sql_code = None

    config_params = {}
    if getattr(args, "flink_version", None):
        config_params["FlinkVersion"] = args.flink_version
    if getattr(args, "jdk_version", None):
        config_params["JdkVersion"] = str(args.jdk_version)
    if getattr(args, "default_parallelism", None):
        config_params["DefaultParallelism"] = int(args.default_parallelism)
    if getattr(args, "remark", None):
        config_params["Remark"] = args.remark

    draft_summary = format_draft_summary(
        job_type,
        sql_code=sql_code,
        entrypoint_class=entrypoint_class,
        program_args=program_args if is_jar else None,
        resource_refs=resource_refs,
        config_params=config_params or None,
        properties=draft_properties,
    )
    confirm_err = confirm_draft_before_publish(
        "create_job_config", draft_summary,
        getattr(args, "skip_draft_confirm", False), True,
    )
    if confirm_err:
        return output(confirm_err, args.output)

    # ── Step 3: Call CreateJobConfig API ──────────────────────────────
    if verbose:
        print("[create_job_config] 草稿确认通过，创建新版本...", file=sys.stderr)

    params_create = {"JobId": job_id}
    if workspace_id:
        params_create["WorkSpaceId"] = workspace_id

    # Carry over draft content to the publish call
    # NOTE: DescribeJobConfigs returns SqlCode and Metadata as plaintext,
    # but CreateJobConfig expects both fields base64-encoded. Re-encode if needed.
    pa = draft.get("ProgramArgs")
    if pa and not is_jar:
        try:
            pa_obj = json.loads(pa) if isinstance(pa, str) else pa

            # Re-encode SqlCode to base64 if it's plaintext
            sql_code = pa_obj.get("SqlCode", "")
            if sql_code:
                try:
                    base64.b64decode(sql_code).decode("utf-8")
                except Exception:
                    pa_obj["SqlCode"] = base64.b64encode(
                        sql_code.encode("utf-8")
                    ).decode("utf-8")

            # Re-encode Metadata to base64 if it's plaintext
            metadata = pa_obj.get("Metadata", "")
            if metadata:
                try:
                    base64.b64decode(metadata).decode("utf-8")
                except Exception:
                    pa_obj["Metadata"] = base64.b64encode(
                        metadata.encode("utf-8")
                    ).decode("utf-8")

            pa = json.dumps(pa_obj)
        except (json.JSONDecodeError, ValueError):
            pass
        params_create["ProgramArgs"] = pa
    elif pa:
        params_create["ProgramArgs"] = pa
    if is_jar:
        ec = draft.get("EntrypointClass")
        if ec:
            params_create["EntrypointClass"] = ec
    if resource_refs:
        params_create["ResourceRefs"] = resource_refs

    # Optional config overrides
    if getattr(args, "flink_version", None):
        params_create["FlinkVersion"] = args.flink_version
    elif draft.get("FlinkVersion"):
        params_create["FlinkVersion"] = draft["FlinkVersion"]
    if getattr(args, "jdk_version", None):
        params_create["JdkVersion"] = str(args.jdk_version)
    elif draft.get("JdkVersion"):
        params_create["JdkVersion"] = str(draft["JdkVersion"])
    if getattr(args, "default_parallelism", None):
        params_create["DefaultParallelism"] = int(args.default_parallelism)
    elif draft.get("DefaultParallelism"):
        params_create["DefaultParallelism"] = int(draft["DefaultParallelism"])
    if getattr(args, "remark", None):
        params_create["Remark"] = args.remark

    # Carry over Properties from draft
    if draft_properties:
        params_create["Properties"] = draft_properties

    result = call_api("CreateJobConfig", params_create, region)
    if not result.get("success"):
        return output(error_response("create_job_config", "CreateJobConfigFailed",
                                     f"创建新版本失败: {result.get('error', '')}"), args.output)

    version = result.get("data", {}).get("Version", "unknown")
    final = success_response("create_job_config", {
        "message": f"{job_type_name} 作业配置发布成功，新版本号: {version}",
        "job_id": job_id,
        "job_type": job_type_name,
        "version": version,
    })
    output(final, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Subparser registration
# ═══════════════════════════════════════════════════════════════════════════


def register(subparsers):
    """Register all job development subcommands (SQL + JAR)."""

    def _add(name, help_text, func, extra_args=None):
        p = subparsers.add_parser(name, help=help_text)
        add_common_args(p)
        if extra_args:
            extra_args(p)
        p.set_defaults(func=func, subcommand=name)

    # ── Common JAR args helper ────────────────────────────────────────

    def _add_jar_args(p):
        """Add JAR-specific arguments to a subparser."""
        p.add_argument("--job_type", type=int, required=True, choices=[JOB_TYPE_SQL, JOB_TYPE_JAR],
                        help="Job type (REQUIRED): 1=SQL, 2=JAR")
        p.add_argument("--entrypoint_class",
                        help="[JAR] Main class (e.g. com.xxx.job.FlinkTestJob)")
        p.add_argument("--program_args",
                        help="[JAR] Main class arguments (e.g. '-foo 1 -bar 2')")
        p.add_argument("--resource_refs",
                        help=(
                            'Resource refs JSON. ResourceRef.Type values: '
                            '0=DEPENDENCY_JAR (辅助 jar 包，非主程序，例如 UDF / connector jar); '
                            '1=MAIN (JAR job\'s main program, exactly one entry, JAR-only); '
                            '2=DEPENDENCY (non-jar dependency, e.g. .properties config file). '
                            'NOTE: ResourceRef.Type is NOT the same as Resource.Type '
                            '(which is 1=jar / 2=config file at upload time). '
                            'JAR example: \'[{"ResourceId":"resource-main","Type":1,"Version":1},'
                            '{"ResourceId":"resource-lib","Type":0,"Version":1},'
                            '{"ResourceId":"resource-cfg","Type":2,"Version":1}]\'. '
                            'SQL example: \'[{"ResourceId":"resource-udf","Type":0,"Version":1}]\' (Type=1 forbidden for SQL).'
                        ))

    # ── Create Job ────────────────────────────────────────────────────

    def _create_job_args(p):
        p.add_argument("--name", required=True, help="Job name")
        p.add_argument("--job_type", type=int, required=True, choices=[JOB_TYPE_SQL, JOB_TYPE_JAR],
                        help="Job type (REQUIRED): 1=SQL, 2=JAR")
        p.add_argument(
            "--cluster_type",
            default="2",
            help="Cluster type: 1=shared, 2=dedicated (default: 2)",
        )
        p.add_argument("--cluster_id", help="Cluster ID (cluster-xxx) or cluster name")
        p.add_argument("--cluster_name", help="Cluster name (alternative to --cluster_id)")
        p.add_argument("--workspace_name", help="Workspace name (alternative to --workspace_id)")
        p.add_argument("--folder_id", help="Folder ID to place job in (use 'root' for root directory)")
        p.add_argument("--folder_name", help="Folder name — auto-query or create if not exists")
        p.add_argument("--parent_id", help="Parent folder ID when creating new folder (used with --folder_name)")
        p.add_argument("--cu_mem", help="Memory per CU in GB: 2, 4, 8, 16 (default: 4)")
        p.add_argument("--remark", help="Job remark")
        p.add_argument("--description", help="Job description")
        p.add_argument("--flink_version", help="Flink version (e.g. Flink-1.16)")
        p.add_argument("--jdk_version", help="JDK version (e.g. 8, 11)")
        p.add_argument("--min_cu", type=int, default=1, help="Minimum free CU required for cluster selection (default: 1)")
        p.add_argument("--confirm", action="store_true", help="Skip interactive confirmation")

    _add("create_job", "Create a new job (SQL or JAR)", cmd_create_job, _create_job_args)

    # ── Describe Jobs ─────────────────────────────────────────────────

    def _describe_jobs_args(p):
        p.add_argument(
            "--filters",
            help="Filters in format 'Name=value;Name2=value2' (semicolon-separated). "
                 "Names: JobName|JobId|ClusterName|ClusterId|FolderName|SqlKeyword|JobType|JobStatus|Zone|ExceptionType",
        )
        p.add_argument(
            "--category",
            default="folderName",
            help="Tree grouping: folderName (default) | clusterName | createTime | noop",
        )
        p.add_argument("--parent_id", help="Parent folder ID for sub-tree query")
        p.add_argument("--page_size", help="Page size for pagination")
        p.add_argument("--page_attach", help="Pagination scroll token (from previous response)")

    _add("describe_jobs", "Query jobs in workspace (tree structure)", cmd_describe_jobs, _describe_jobs_args)

    # ── Describe Job Configs ──────────────────────────────────────────

    def _describe_job_configs_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--only_draft", action="store_true", help="Only return draft config")
        p.add_argument("--versions", help="Comma-separated version numbers to query")
        p.add_argument("--offset", help="Pagination offset (default: 0)")
        p.add_argument("--limit", help="Pagination limit (default: 20)")

    _add("describe_job_configs", "Query job configurations or draft", cmd_describe_job_configs, _describe_job_configs_args)

    # ── Modify Draft ──────────────────────────────────────────────────

    def _modify_draft_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--sql", help="[SQL] SQL code (plain text, will be base64 encoded)")
        p.add_argument("--sql_file", help="[SQL] Path to SQL file (alternative to --sql)")
        _add_jar_args(p)
        p.add_argument("--existing_program_args", help="Existing ProgramArgs JSON to merge with (optional)")
        p.add_argument("--catalog_refs", help="[SQL] Catalog references JSON for Metadata. Format: '[{\"catalog\":\"name\",\"database\":\"db\",\"table\":\"tbl\"}]'")
        p.add_argument("--reference_tables", help="[SQL] Pre-built reference tables JSON for Metadata. Format: '[{\"catalog\":\"c\",\"database\":\"db\",\"table\":\"tbl\",\"version\":1}]'")
        p.add_argument("--cluster_id", help="Cluster ID (used for external catalog async queries)")
        p.add_argument("--default_parallelism", help="Default parallelism (integer)")
        p.add_argument("--flink_version", help="Flink version (e.g. Flink-1.16)")
        p.add_argument("--jdk_version", help="JDK version (e.g. 8, 11, 17)")
        p.add_argument("--remark", help="Draft remark")

    _add("modify_draft", "Modify and save draft configuration (SQL or JAR)", cmd_modify_draft, _modify_draft_args)

    # ── Check SQL Deep Grammar ────────────────────────────────────────

    def _check_sql_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--sql", help="SQL code (plain text, will be base64 encoded)")
        p.add_argument("--sql_file", help="Path to SQL file (alternative to --sql)")
        p.add_argument("--cluster_id", help="Cluster ID override (auto-resolved from job detail if omitted)")

    _add("check_sql", "Run deep SQL grammar check (SQL jobs only)", cmd_check_sql, _check_sql_args)

    # ── Create Job Config (publish new version) ───────────────────────

    def _create_job_config_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--job_type", type=int, required=True, choices=[JOB_TYPE_SQL, JOB_TYPE_JAR],
                        help="Job type (REQUIRED): 1=SQL, 2=JAR")
        p.add_argument("--flink_version", help="Flink version override (e.g. Flink-1.16)")
        p.add_argument("--jdk_version", help="JDK version override (e.g. 8, 11, 17)")
        p.add_argument("--default_parallelism", help="Default parallelism override (integer)")
        p.add_argument("--remark", help="Version remark")
        p.add_argument("--skip_draft_confirm", action="store_true",
                        help="Skip the draft confirmation step (DANGEROUS: automation-only)")
        p.add_argument("--confirm", action="store_true", help="Skip interactive confirmation")

    _add("create_job_config", "Publish current draft as a new job config version (with draft confirmation)", cmd_create_job_config, _create_job_config_args)
