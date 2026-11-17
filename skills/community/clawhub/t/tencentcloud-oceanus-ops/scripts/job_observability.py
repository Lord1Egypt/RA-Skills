#!/usr/bin/env python3
"""Job Observability workflow — job events and running log queries.

This module implements job observability operations:
- describe_job_events: Query job events (two-phase: instance list → event details)
- describe_job_running_log: Query job running logs (three-phase: instances → containers → logs)
- describe_job_log_cos_files: List COS log files and generate presigned download URLs

Events and logs are archived by job instance (RunningOrderId).
"""

import hashlib
import hmac
import sys
import time
import json
from datetime import datetime, timezone
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen
from xml.etree import ElementTree

from client import (
    add_common_args,
    call_api,
    error_response,
    get_credentials,
    output,
    require_args,
    success_response,
)


# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════

# ─────────────────────────────────────────────────────────────────────────
# Log-collect enum (RESPONSE side)
#
# Used by:
#   - `JobConfig.LogCollect`              (DescribeJobConfigs response)
#   - `JobInstance.JobCollectType`        (DescribeJobRunningLog response)
#
# Both fields share the same enum on the response side:
#   0 = JobLogCollectDisabled         不采集
#   1 = JobLogCollectEnabled          采集到 CLS
#   2 = JobLogCollectHistoryDisabled  历史禁用（兼容旧值，等同于 0）
#   3 = JobLogCollectHistoryEnabled   历史启用（兼容旧值，等同于 1）
#   4 = JobLogCollectEnabledOnCos     采集到 COS
#   5 = JobLogCollectEnabledOnES      采集到 ES
#
# IMPORTANT: this enum is DIFFERENT from the REQUEST-side `LogCollectType`
# parameter accepted by ModifyJobConfig / CreateJobConfig / ModifyDraftConfig,
# which uses 2=CLS / 3=COS / 4=ES. Do NOT mix the two enums when constructing
# request payloads or interpreting responses.
# ─────────────────────────────────────────────────────────────────────────
LOG_COLLECT_DISABLED = 0
LOG_COLLECT_CLS = 1
LOG_COLLECT_HISTORY_DISABLED = 2  # legacy alias of DISABLED
LOG_COLLECT_HISTORY_ENABLED = 3   # legacy alias of CLS
LOG_COLLECT_COS = 4
LOG_COLLECT_ES = 5

LOG_COLLECT_DESC = {
    LOG_COLLECT_DISABLED:         "不采集",
    LOG_COLLECT_CLS:              "CLS（日志服务）",
    LOG_COLLECT_HISTORY_DISABLED: "不采集（历史兼容）",
    LOG_COLLECT_HISTORY_ENABLED:  "CLS（历史兼容）",
    LOG_COLLECT_COS:              "COS（对象存储）",
    LOG_COLLECT_ES:               "ES（Elasticsearch）",
}

# Default time range: last 7 days (max allowed)
MAX_TIME_RANGE_SECONDS = 7 * 24 * 3600
MAX_HISTORY_SECONDS = 90 * 24 * 3600

# COS presigned URL default expiry: 1 hour
COS_PRESIGN_EXPIRES = 3600


# ═══════════════════════════════════════════════════════════════════════════
# Internal Helpers
# ═══════════════════════════════════════════════════════════════════════════


def _default_time_range():
    """Return default (start, end) timestamps in seconds — last 24 hours."""
    now = int(time.time())
    return now - 24 * 3600, now


def _get_job_and_cluster_detail(job_id, region, workspace_id=None):
    """Query job detail and its cluster detail for COS path construction.

    Returns:
        dict: On success:
            {"success": True, "job": <job dict>, "cluster": <cluster dict>}
        On failure: standard error_response dict
    """
    # Step 1: Get job detail
    params = {"JobIds": [job_id]}
    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    result = call_api("DescribeJobsExists", params, region)
    if not result.get("success"):
        return result

    jobs = result.get("data", {}).get("Jobs", [])
    if not jobs:
        return error_response("describe_job_log_cos_files", "JobNotFound",
                              f"作业 {job_id} 不存在或无权访问")

    job_info = jobs[0]
    if not job_info.get("IsExists"):
        return error_response("describe_job_log_cos_files", "JobNotFound",
                              f"作业 {job_id} 不存在")

    job_item = job_info.get("JobItem", {})
    cluster_id = job_item.get("ClusterId", "")

    if not cluster_id:
        return error_response("describe_job_log_cos_files", "NoClusterBound",
                              f"作业 {job_id} 未绑定集群")

    # Step 2: Get cluster detail
    cluster_params = {
        "ClusterIds": [cluster_id],
    }
    if workspace_id:
        cluster_params["WorkSpaceId"] = workspace_id

    cluster_result = call_api("DescribeClusters", cluster_params, region)
    if not cluster_result.get("success"):
        return cluster_result

    clusters = cluster_result.get("data", {}).get("ClusterSet", [])
    if not clusters:
        return error_response("describe_job_log_cos_files", "ClusterNotFound",
                              f"集群 {cluster_id} 不存在")

    cluster_detail = clusters[0]

    return {
        "success": True,
        "job": job_item,
        "cluster": cluster_detail,
    }


def _build_cos_info(cluster_detail, job_detail, running_order_id, component="jobmanager"):
    """Build COS bucket, region, and path prefix for log files.

    Follows the CDC/non-CDC path rules:
    - CDC: bucket=DefaultCOSBucket, region={CdcId}.cos-cdc.{Region}
    - Normal: bucket=LogCOSBucket, region={Region}

    Path: /job-running-log/{ClusterId}/{JobId}/{RunningOrderId}/{component}/

    Returns:
        dict: {"bucket": ..., "cos_region": ..., "path_prefix": ..., "is_cdc": bool}
              or error dict
    """
    cluster_id = job_detail.get("ClusterId", "")
    job_id = job_detail.get("JobId", "")
    region = job_detail.get("Region", "") or cluster_detail.get("Region", "")
    cdc_id = cluster_detail.get("CdcId", "")

    path_prefix = f"job-running-log/{cluster_id}/{job_id}/{running_order_id}/{component}/"

    if cdc_id:
        # CDC cluster
        bucket = cluster_detail.get("DefaultCOSBucket", "")
        cos_region = f"{cdc_id}.cos-cdc.{region}"
        if not bucket:
            return error_response("describe_job_log_cos_files", "NoCOSBucket",
                                  f"CDC集群 {cluster_id} 未配置 DefaultCOSBucket")
    else:
        # Normal cluster
        bucket = cluster_detail.get("LogCOSBucket", "")
        cos_region = region
        if not bucket:
            return error_response("describe_job_log_cos_files", "NoCOSBucket",
                                  f"集群 {cluster_id} 未配置 LogCOSBucket")

    return {
        "success": True,
        "bucket": bucket,
        "cos_region": cos_region,
        "path_prefix": path_prefix,
        "is_cdc": bool(cdc_id),
    }


# ═══════════════════════════════════════════════════════════════════════════
# COS API Helpers (COS V5 XML API with HMAC-SHA1 signature)
# ═══════════════════════════════════════════════════════════════════════════


def _cos_sign(secret_id, secret_key, method, path, params=None, headers=None, expires=600):
    """Generate COS V5 request signature (HMAC-SHA1).

    Args:
        secret_id: TencentCloud SecretId
        secret_key: TencentCloud SecretKey
        method: HTTP method (GET/PUT/...)
        path: URL path (e.g. /)
        params: Query parameters dict
        headers: Request headers dict
        expires: Signature validity in seconds

    Returns:
        str: Signature string for Authorization header
    """
    method = method.lower()
    now = int(time.time())
    key_time = f"{now};{now + expires}"

    # Sign key
    sign_key = hmac.new(
        secret_key.encode("utf-8"),
        key_time.encode("utf-8"),
        hashlib.sha1,
    ).hexdigest()

    # Canonical query string (sorted, lowercase keys)
    if params:
        sorted_params = sorted(
            (k.lower(), str(v)) for k, v in params.items()
        )
        url_param_list = ";".join(k for k, _ in sorted_params)
        http_parameters = "&".join(f"{k}={quote(v, safe='')}" for k, v in sorted_params)
    else:
        url_param_list = ""
        http_parameters = ""

    # Canonical headers (sorted, lowercase keys)
    if headers:
        sorted_headers = sorted(
            (k.lower(), str(v).strip()) for k, v in headers.items()
        )
        header_list = ";".join(k for k, _ in sorted_headers)
        http_headers = "&".join(f"{k}={quote(v, safe='')}" for k, v in sorted_headers)
    else:
        header_list = ""
        http_headers = ""

    # Canonical request
    http_string = f"{method}\n{path}\n{http_parameters}\n{http_headers}\n"
    sha1_http_string = hashlib.sha1(http_string.encode("utf-8")).hexdigest()

    # String to sign
    string_to_sign = f"sha1\n{key_time}\n{sha1_http_string}\n"
    signature = hmac.new(
        sign_key.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    ).hexdigest()

    authorization = (
        f"q-sign-algorithm=sha1"
        f"&q-ak={secret_id}"
        f"&q-sign-time={key_time}"
        f"&q-key-time={key_time}"
        f"&q-header-list={header_list}"
        f"&q-url-param-list={url_param_list}"
        f"&q-signature={signature}"
    )

    return authorization


def _cos_list_objects(bucket, cos_region, prefix, delimiter="/", marker="", max_keys=1000):
    """List objects in a COS bucket with given prefix.

    Uses COS V5 XML API: GET Bucket (List Objects).

    Args:
        bucket: COS bucket name
        cos_region: COS region (may include CDC suffix)
        prefix: Object key prefix
        delimiter: Delimiter for hierarchical listing
        marker: Pagination marker
        max_keys: Max objects per page

    Returns:
        dict: success envelope with file list, or error envelope
    """
    secret_id, secret_key = get_credentials()

    # Build endpoint
    endpoint = f"https://{bucket}.cos.{cos_region}.myqcloud.com"

    # Query parameters
    params = {
        "prefix": prefix,
        "delimiter": delimiter,
        "max-keys": str(max_keys),
    }
    if marker:
        params["marker"] = marker

    # Sign the request
    sign_headers = {"host": f"{bucket}.cos.{cos_region}.myqcloud.com"}
    authorization = _cos_sign(
        secret_id, secret_key, "GET", "/",
        params=params, headers=sign_headers, expires=COS_PRESIGN_EXPIRES,
    )

    # Build URL
    query_string = "&".join(f"{k}={quote(v, safe='')}" for k, v in sorted(params.items()))
    url = f"{endpoint}/?{query_string}"

    headers = {
        "Host": f"{bucket}.cos.{cos_region}.myqcloud.com",
        "Authorization": authorization,
    }

    try:
        req = Request(url, headers=headers, method="GET")
        resp = urlopen(req, timeout=30)
        body = resp.read().decode("utf-8")
    except HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return error_response("cos_list_objects", "CosHttpError",
                              f"COS HTTP {e.code}: {err_body[:500]}")
    except URLError as e:
        return error_response("cos_list_objects", "CosNetworkError", str(e.reason))
    except Exception as e:
        return error_response("cos_list_objects", "CosRequestError", str(e))

    # Parse XML response
    try:
        root = ElementTree.fromstring(body)
        # COS XML API uses namespace
        ns = ""
        if root.tag.startswith("{"):
            ns = root.tag.split("}")[0] + "}"

        files = []
        for content in root.findall(f"{ns}Contents"):
            key = content.findtext(f"{ns}Key", "")
            size = content.findtext(f"{ns}Size", "0")
            last_modified = content.findtext(f"{ns}LastModified", "")
            # Skip directory markers
            if key and not key.endswith("/"):
                files.append({
                    "key": key,
                    "file_name": key.rsplit("/", 1)[-1] if "/" in key else key,
                    "size": int(size),
                    "last_modified": last_modified,
                })

        # Common prefixes (subdirectories)
        dirs = []
        for cp in root.findall(f"{ns}CommonPrefixes"):
            prefix_val = cp.findtext(f"{ns}Prefix", "")
            if prefix_val:
                dirs.append(prefix_val)

        is_truncated = root.findtext(f"{ns}IsTruncated", "false").lower() == "true"
        next_marker = root.findtext(f"{ns}NextMarker", "")

        return success_response("cos_list_objects", {
            "files": files,
            "directories": dirs,
            "is_truncated": is_truncated,
            "next_marker": next_marker,
        })

    except ElementTree.ParseError as e:
        return error_response("cos_list_objects", "CosParseError",
                              f"解析COS响应失败: {str(e)}")


def _cos_generate_presigned_url(bucket, cos_region, key, expires=COS_PRESIGN_EXPIRES):
    """Generate a presigned download URL for a COS object.

    Args:
        bucket: COS bucket name
        cos_region: COS region
        key: Object key (full path)
        expires: URL validity in seconds (default 1 hour)

    Returns:
        str: Presigned download URL
    """
    secret_id, secret_key = get_credentials()

    endpoint = f"https://{bucket}.cos.{cos_region}.myqcloud.com"
    path = f"/{key}"

    sign_headers = {"host": f"{bucket}.cos.{cos_region}.myqcloud.com"}
    authorization = _cos_sign(
        secret_id, secret_key, "GET", path,
        params={}, headers=sign_headers, expires=expires,
    )

    # Build presigned URL with signature in query string
    encoded_path = quote(key, safe="/")
    presigned_url = f"{endpoint}/{encoded_path}?{authorization}"

    return presigned_url


# ═══════════════════════════════════════════════════════════════════════════
# Describe Job Events
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_job_events(args):
    """Query job events via DescribeJobEvents.

    Two-phase query:
    - Phase 1 (no --running_order_ids): Returns instance list with RunningOrderIds + Versions
    - Phase 2 (with --running_order_ids): Returns event details for specified instances

    Time range validation: max 7 days span, start time within 90 days.
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_id = args.job_id
    region = args.region
    workspace_id = getattr(args, "workspace_id", None)

    # Build time range
    start_ts = getattr(args, "start_timestamp", None)
    end_ts = getattr(args, "end_timestamp", None)

    if start_ts:
        start_ts = int(start_ts)
    if end_ts:
        end_ts = int(end_ts)

    if not start_ts or not end_ts:
        default_start, default_end = _default_time_range()
        start_ts = start_ts or default_start
        end_ts = end_ts or default_end

    # Validate time range
    now = int(time.time())
    if end_ts - start_ts > MAX_TIME_RANGE_SECONDS:
        return output(error_response(
            "describe_job_events", "ValidationError",
            f"时间跨度不能超过7天（当前: {(end_ts - start_ts) // 3600}小时）"
        ), args.output)
    if now - start_ts > MAX_HISTORY_SECONDS:
        return output(error_response(
            "describe_job_events", "ValidationError",
            "起始时间距今不能超过90天"
        ), args.output)

    params = {
        "JobId": job_id,
        "StartTimestamp": start_ts,
        "EndTimestamp": end_ts,
    }

    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    # Parse running_order_ids if provided
    running_order_ids = getattr(args, "running_order_ids", None)
    if running_order_ids:
        ids = [int(x.strip()) for x in running_order_ids.split(",") if x.strip()]
        params["RunningOrderIds"] = ids

    # Parse event types if provided
    event_types = getattr(args, "types", None)
    if event_types:
        params["Types"] = [t.strip() for t in event_types.split(",") if t.strip()]

    result = call_api("DescribeJobEvents", params, region)

    if result.get("success"):
        data = result.get("data", {})
        if not running_order_ids:
            # Phase 1: format instance list
            order_ids = data.get("RunningOrderIds", [])
            versions = data.get("Versions", [])
            instances = []
            for i, oid in enumerate(order_ids):
                inst = {"running_order_id": oid}
                if i < len(versions):
                    inst["config_version"] = versions[i]
                instances.append(inst)
            result = success_response("describe_job_events", {
                "phase": "instance_list",
                "message": f"作业 {job_id} 在指定时间范围内有 {len(instances)} 个运行实例",
                "instances": instances,
                "total_count": len(instances),
                "hint": "请使用 --running_order_ids <id1,id2> 查询指定实例的事件详情",
            }, result.get("request_id", ""))
        else:
            # Phase 2: format event details
            events = data.get("Events", [])
            formatted_events = []
            for evt in events:
                formatted_events.append({
                    "type": evt.get("Type", ""),
                    "description": evt.get("Description", ""),
                    "timestamp": evt.get("Timestamp", 0),
                    "time": datetime.fromtimestamp(
                        evt.get("Timestamp", 0), tz=timezone.utc
                    ).strftime("%Y-%m-%d %H:%M:%S UTC") if evt.get("Timestamp") else "",
                    "running_order_id": evt.get("RunningOrderId", 0),
                    "message": evt.get("Message", ""),
                    "solution_link": evt.get("SolutionLink", ""),
                })
            result = success_response("describe_job_events", {
                "phase": "event_details",
                "events": formatted_events,
                "total_count": data.get("TotalCount", len(formatted_events)),
            }, result.get("request_id", ""))

    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Describe Job Running Log
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_job_running_log(args):
    """Query job running logs via DescribeJobRunningLog.

    Three-phase progressive query:
    - Phase 1 (no --running_order_id): Returns instance list with collect type
    - Phase 2 (--running_order_id, no --container): Returns container list
    - Phase 3 (--running_order_id + --container): Returns log content

    Each instance includes JobCollectType indicating log storage backend.
    JobCollectType shares the same enum as `JobConfig.LogCollect`:
    - 0: 不采集
    - 1: CLS (日志服务)
    - 2/3: 历史兼容值（等同于 0/1）
    - 4: COS (对象存储) — use describe_job_log_cos_files for file listing
    - 5: ES (Elasticsearch)

    NOTE: this is the RESPONSE-side enum; the REQUEST-side `LogCollectType`
    parameter (used by ModifyJobConfig / CreateJobConfig) follows a different
    encoding (2=CLS / 3=COS / 4=ES) and must not be mixed.
    """
    err = require_args(args, "region", "job_id")
    if err:
        return output(err, args.output)

    job_id = args.job_id
    region = args.region

    params = {
        "JobId": job_id,
    }

    # Running order ID (phase 2/3)
    running_order_id = getattr(args, "running_order_id", None)
    if running_order_id:
        params["RunningOrderId"] = int(running_order_id)

    # Container (phase 3)
    container = getattr(args, "container", None)
    if container:
        params["Container"] = container

    # Time range (milliseconds for this API)
    start_time = getattr(args, "start_time", None)
    end_time = getattr(args, "end_time", None)
    if start_time:
        params["StartTime"] = int(start_time)
    if end_time:
        params["EndTime"] = int(end_time)

    # Search options
    keyword = getattr(args, "keyword", None)
    if keyword:
        params["Keyword"] = keyword

    order_type = getattr(args, "order_type", None)
    if order_type:
        params["OrderType"] = order_type

    limit = getattr(args, "limit", None)
    if limit:
        params["Limit"] = int(limit)

    cursor = getattr(args, "cursor", None)
    if cursor:
        params["Cursor"] = cursor

    result = call_api("DescribeJobRunningLog", params, region)

    if result.get("success"):
        data = result.get("data", {})

        if not running_order_id:
            # Phase 1: instance list
            instances = data.get("JobInstanceList", [])
            formatted = []
            for inst in instances:
                collect_type = inst.get("JobCollectType", 0)
                formatted.append({
                    "running_order_id": inst.get("RunningOrderId", 0),
                    "config_version": inst.get("RelatedJobConfigVersion", 0),
                    "start_time": inst.get("JobInstanceStartTime", ""),
                    "stop_time": inst.get("JobInstanceStopTime", ""),
                    "log_collect_type": collect_type,
                    "log_collect_type_desc": LOG_COLLECT_DESC.get(collect_type, f"未知({collect_type})"),
                })
            result = success_response("describe_job_running_log", {
                "phase": "instance_list",
                "message": f"作业 {job_id} 有 {len(formatted)} 个运行实例",
                "instances": formatted,
                "hint": "请使用 --running_order_id <id> 查询指定实例的容器列表。"
                        "若 log_collect_type=4 (COS)，可使用 describe_job_log_cos_files 直接获取日志文件列表。",
            }, result.get("request_id", ""))

        elif not container:
            # Phase 2: container list
            containers = data.get("ContainerList", [])
            result = success_response("describe_job_running_log", {
                "phase": "container_list",
                "message": f"实例 {running_order_id} 有 {len(containers)} 个容器",
                "containers": containers,
                "running_order_id": int(running_order_id),
                "hint": "请使用 --container <name> 查询指定容器的日志内容",
            }, result.get("request_id", ""))

        else:
            # Phase 3: log content
            log_content_list = data.get("LogContentList", [])
            formatted_logs = []
            for log_item in log_content_list:
                formatted_logs.append({
                    "log": log_item.get("Log", ""),
                    "time": log_item.get("Time", 0),
                    "container_name": log_item.get("ContainerName", ""),
                })
            result = success_response("describe_job_running_log", {
                "phase": "log_content",
                "logs": formatted_logs,
                "total_count": len(formatted_logs),
                "cursor": data.get("Cursor", ""),
                "list_over": data.get("ListOver", False),
                "running_order_id": int(running_order_id),
                "container": container,
            }, result.get("request_id", ""))

    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Describe Job Log COS Files
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_job_log_cos_files(args):
    """List COS log files for a job instance and generate presigned download URLs.

    This command is used when the job's running-log collect type is COS
    (JobCollectType=4 from DescribeJobRunningLog).
    It queries job/cluster details to build the COS path, then lists files
    and generates presigned download URLs.

    Workflow:
    1. DescribeJobsExists → get job detail (ClusterId, Region)
    2. DescribeClusters → get cluster detail (LogCOSBucket, DefaultCOSBucket, CdcId)
    3. Build COS path based on CDC/non-CDC rules
    4. COS ListObjects → get file list
    5. Generate presigned download URLs for each file
    """
    err = require_args(args, "region", "job_id", "running_order_id")
    if err:
        return output(err, args.output)

    job_id = args.job_id
    region = args.region
    workspace_id = getattr(args, "workspace_id", None)
    running_order_id = args.running_order_id
    component = getattr(args, "component", None) or "jobmanager"

    if args.verbose:
        print(f"[cos_files] Step 1: 查询作业 {job_id} 和集群信息...", file=sys.stderr)

    # Step 1-2: Get job and cluster info
    info_result = _get_job_and_cluster_detail(job_id, region, workspace_id)
    if not info_result.get("success"):
        return output(info_result, args.output)

    job_detail = info_result["job"]
    cluster_detail = info_result["cluster"]

    if args.verbose:
        cdc_id = cluster_detail.get("CdcId", "")
        print(f"[cos_files] 集群: {job_detail.get('ClusterId', '')}, "
              f"CDC: {'是' if cdc_id else '否'}", file=sys.stderr)

    # Step 3: Build COS path
    cos_info = _build_cos_info(cluster_detail, job_detail, running_order_id, component)
    if not cos_info.get("success"):
        return output(cos_info, args.output)

    bucket = cos_info["bucket"]
    cos_region = cos_info["cos_region"]
    path_prefix = cos_info["path_prefix"]

    if args.verbose:
        print(f"[cos_files] Step 2: 查询 COS 文件列表...", file=sys.stderr)
        print(f"[cos_files] Bucket: {bucket}, Region: {cos_region}, "
              f"Prefix: {path_prefix}", file=sys.stderr)

    # Step 4: List COS objects
    marker = getattr(args, "marker", None) or ""
    list_result = _cos_list_objects(bucket, cos_region, path_prefix, marker=marker)
    if not list_result.get("success"):
        return output(list_result, args.output)

    files = list_result.get("data", {}).get("files", [])
    directories = list_result.get("data", {}).get("directories", [])

    if args.verbose:
        print(f"[cos_files] 找到 {len(files)} 个文件, {len(directories)} 个子目录",
              file=sys.stderr)

    # Step 5: Generate presigned URLs
    if args.verbose:
        print("[cos_files] Step 3: 生成预签名下载链接...", file=sys.stderr)

    for f in files:
        f["download_url"] = _cos_generate_presigned_url(
            bucket, cos_region, f["key"]
        )

    result = success_response("describe_job_log_cos_files", {
        "job_id": job_id,
        "running_order_id": running_order_id,
        "component": component,
        "cos_info": {
            "bucket": bucket,
            "region": cos_region,
            "path_prefix": path_prefix,
            "is_cdc": cos_info["is_cdc"],
        },
        "files": files,
        "directories": directories,
        "total_files": len(files),
        "is_truncated": list_result.get("data", {}).get("is_truncated", False),
        "next_marker": list_result.get("data", {}).get("next_marker", ""),
    })

    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Subparser Registration
# ═══════════════════════════════════════════════════════════════════════════


def register(subparsers):
    """Register all job observability subcommands."""

    def _add(name, help_text, func, extra_args=None):
        p = subparsers.add_parser(name, help=help_text)
        add_common_args(p)
        if extra_args:
            extra_args(p)
        p.set_defaults(func=func, subcommand=name)

    # ── Describe Job Events ───────────────────────────────────────────

    def _describe_job_events_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--start_timestamp",
                       help="Start timestamp in seconds (default: 24h ago)")
        p.add_argument("--end_timestamp",
                       help="End timestamp in seconds (default: now)")
        p.add_argument("--running_order_ids",
                       help="Comma-separated RunningOrderIds for event details (phase 2)")
        p.add_argument("--types",
                       help="Comma-separated event types to filter")

    _add("describe_job_events",
         "Query job events by instance (two-phase: instances → events)",
         cmd_describe_job_events, _describe_job_events_args)

    # ── Describe Job Running Log ──────────────────────────────────────

    def _describe_job_running_log_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--running_order_id",
                       help="Running instance ID (phase 2/3)")
        p.add_argument("--container",
                       help="Container/Pod name (phase 3)")
        p.add_argument("--start_time",
                       help="Start time in milliseconds")
        p.add_argument("--end_time",
                       help="End time in milliseconds")
        p.add_argument("--keyword",
                       help="Search keyword")
        p.add_argument("--order_type", choices=["asc", "desc"],
                       help="Sort order (default: desc)")
        p.add_argument("--limit", type=int,
                       help="Max log entries per page")
        p.add_argument("--cursor",
                       help="Pagination cursor from previous response")

    _add("describe_job_running_log",
         "Query job running logs (three-phase: instances → containers → logs)",
         cmd_describe_job_running_log, _describe_job_running_log_args)

    # ── Describe Job Log COS Files ────────────────────────────────────

    def _describe_job_log_cos_files_args(p):
        p.add_argument("--job_id", required=True, help="Job ID (cql-xxx)")
        p.add_argument("--running_order_id", required=True,
                       help="Running instance ID")
        p.add_argument("--component", default="jobmanager",
                       help="Component: jobmanager or taskmanager (default: jobmanager)")
        p.add_argument("--marker",
                       help="COS pagination marker for large file lists")

    _add("describe_job_log_cos_files",
         "List COS log files with presigned download URLs (for COS log type)",
         cmd_describe_job_log_cos_files, _describe_job_log_cos_files_args)
