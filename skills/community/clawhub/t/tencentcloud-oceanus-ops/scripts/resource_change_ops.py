#!/usr/bin/env python3
"""Resource change operations — utilities for incremental resource management.

Extracted from job_development.py for better modularity.

Provides:
- get_published_config: Fetch published job config version
- process_add_files: Upload new files and create resources
- process_update_files: Upload updated files and create new resource versions
- process_remove_resources: Remove resource references
- format_resource_changes_summary: Format human-readable summary of changes

These utilities are used by the agent when following the modify-job-config
playbook to process resource changes before calling modify_draft.
"""

import json
import os

from client import (
    call_api,
    error_response,
)

from job_config_helpers import _RESOURCE_REF_TYPE_NAMES


# ═══════════════════════════════════════════════════════════════════════════
# Get Published Config
# ═══════════════════════════════════════════════════════════════════════════


def get_published_config(region, job_id, workspace_id, version=None):
    """Fetch a published job config (specific version or latest).

    Args:
        version: int version number, or None for latest published version.

    Returns:
        tuple (config_dict, error_result). Exactly one is non-None.
    """
    params = {"JobId": job_id}
    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    if version is not None:
        params["JobConfigVersions"] = [int(version)]
    else:
        params["Offset"] = 0
        params["Limit"] = 1

    result = call_api("DescribeJobConfigs", params, region)
    if not result.get("success"):
        return None, error_response(
            "resource_change", "DescribeJobConfigsFailed",
            f"获取作业配置失败: {result.get('error', '')}",
        )

    config_set = (result.get("data") or {}).get("JobConfigSet", [])
    if not config_set:
        ver_hint = f"版本 {version}" if version else "最新版本"
        return None, error_response(
            "resource_change", "ConfigNotFound",
            f"未找到作业 {job_id} 的{ver_hint}配置",
        )

    return config_set[0], None


# ═══════════════════════════════════════════════════════════════════════════
# Process Add Files
# ═══════════════════════════════════════════════════════════════════════════


def process_add_files(add_files_json, region, workspace_id, verbose=False):
    """Process --add_files: upload each file and create new resources.

    Returns:
        tuple (new_refs:list, error_result:dict|None).
    """
    try:
        entries = json.loads(add_files_json)
    except (json.JSONDecodeError, TypeError) as exc:
        return [], error_response(
            "resource_change", "ValidationError",
            f"--add_files 不是合法 JSON: {exc}",
        )
    if not isinstance(entries, list):
        return [], error_response(
            "resource_change", "ValidationError",
            "--add_files 必须是 JSON 数组",
        )

    from resource_management import upload_to_cos
    import sys

    new_refs = []
    for i, entry in enumerate(entries):
        file_path = entry.get("file")
        resource_type = entry.get("resource_type")
        ref_type = entry.get("ref_type")
        name = entry.get("name") or (os.path.basename(file_path) if file_path else "")

        if not file_path or resource_type is None or ref_type is None:
            return [], error_response(
                "resource_change", "ValidationError",
                f"--add_files[{i}] 缺少必填字段 (file, resource_type, ref_type)",
            )
        if not os.path.isfile(file_path):
            return [], error_response(
                "resource_change", "ValidationError",
                f"--add_files[{i}] 文件不存在: {file_path}",
            )

        file_name = os.path.basename(file_path)
        if verbose:
            print(
                f"[update] 新增资源 {i + 1}/{len(entries)}: {file_name} ...",
                file=sys.stderr,
            )

        # Step 1: Get presigned URL
        presign_result = call_api("CreatePresignedUrl", {
            "FileName": file_name,
            "HttpMethod": "PUT",
        }, region)
        if not presign_result.get("success"):
            return [], error_response(
                "resource_change", "GetPresignedUrlFailed",
                f"新增资源[{i}] 获取预签名URL失败: {presign_result.get('error', '')}",
            )

        presign_data = presign_result.get("data", {})
        presigned_url = presign_data.get("Location", "")
        bucket = presign_data.get("Bucket", "")
        key = presign_data.get("Key", "")
        cos_region = presign_data.get("Region", region)

        if not presigned_url:
            return [], error_response(
                "resource_change", "GetPresignedUrlFailed",
                f"新增资源[{i}] 预签名URL返回为空",
            )

        # Step 2: Upload to COS
        upload_result = upload_to_cos(presigned_url, file_path)
        if not upload_result.get("success"):
            return [], error_response(
                "resource_change", "CosUploadFailed",
                f"新增资源[{i}] COS上传失败: {upload_result.get('message', '')}",
            )

        # Step 3: Create resource record
        create_params = {
            "Name": name,
            "ResourceType": int(resource_type),
            "ResourceLoc": {
                "StorageType": 1,
                "Param": {
                    "Bucket": bucket,
                    "Path": key,
                    "Region": cos_region,
                },
            },
        }
        if workspace_id:
            create_params["WorkSpaceId"] = workspace_id

        create_result = call_api("CreateResource", create_params, region)
        if not create_result.get("success"):
            return [], error_response(
                "resource_change", "CreateResourceFailed",
                f"新增资源[{i}] 创建资源记录失败: {create_result.get('error', '')}",
            )

        resource_id = (create_result.get("data") or {}).get("ResourceId", "")
        version = (create_result.get("data") or {}).get("Version", 1)
        if not resource_id:
            return [], error_response(
                "resource_change", "CreateResourceFailed",
                f"新增资源[{i}] 创建成功但未返回 ResourceId",
            )

        new_refs.append({
            "ResourceId": resource_id,
            "Type": int(ref_type),
            "Version": version,
        })

        if verbose:
            print(
                f"[update]   -> ResourceId={resource_id}, Version={version}",
                file=sys.stderr,
            )

    return new_refs, None


# ═══════════════════════════════════════════════════════════════════════════
# Process Update Files
# ═══════════════════════════════════════════════════════════════════════════


def process_update_files(update_files_json, existing_refs, region,
                         workspace_id, verbose=False):
    """Process --update_files: upload each file and create new resource config versions.

    Returns:
        tuple (updated_refs:list, error_result:dict|None).
    """
    try:
        entries = json.loads(update_files_json)
    except (json.JSONDecodeError, TypeError) as exc:
        return existing_refs, error_response(
            "resource_change", "ValidationError",
            f"--update_files 不是合法 JSON: {exc}",
        )
    if not isinstance(entries, list):
        return existing_refs, error_response(
            "resource_change", "ValidationError",
            "--update_files 必须是 JSON 数组",
        )

    from resource_management import upload_to_cos
    import sys

    ref_index = {}
    for idx, ref in enumerate(existing_refs):
        ref_index[ref.get("ResourceId", "")] = idx

    for i, entry in enumerate(entries):
        file_path = entry.get("file")
        resource_id = entry.get("resource_id")

        if not file_path or not resource_id:
            return existing_refs, error_response(
                "resource_change", "ValidationError",
                f"--update_files[{i}] 缺少必填字段 (file, resource_id)",
            )
        if not os.path.isfile(file_path):
            return existing_refs, error_response(
                "resource_change", "ValidationError",
                f"--update_files[{i}] 文件不存在: {file_path}",
            )
        if resource_id not in ref_index:
            return existing_refs, error_response(
                "resource_change", "ValidationError",
                f"--update_files[{i}] resource_id={resource_id} "
                f"不在当前 ResourceRefs 中，无法更新",
            )

        file_name = os.path.basename(file_path)
        if verbose:
            print(
                f"[update] 更新资源 {i + 1}/{len(entries)}: "
                f"{file_name} -> {resource_id} ...",
                file=sys.stderr,
            )

        # Step 1: Get presigned URL
        presign_result = call_api("CreatePresignedUrl", {
            "FileName": file_name,
            "HttpMethod": "PUT",
        }, region)
        if not presign_result.get("success"):
            return existing_refs, error_response(
                "resource_change", "GetPresignedUrlFailed",
                f"更新资源[{i}] 获取预签名URL失败: {presign_result.get('error', '')}",
            )

        presign_data = presign_result.get("data", {})
        presigned_url = presign_data.get("Location", "")
        bucket = presign_data.get("Bucket", "")
        key = presign_data.get("Key", "")
        cos_region = presign_data.get("Region", region)

        if not presigned_url:
            return existing_refs, error_response(
                "resource_change", "GetPresignedUrlFailed",
                f"更新资源[{i}] 预签名URL返回为空",
            )

        # Step 2: Upload to COS
        upload_result = upload_to_cos(presigned_url, file_path)
        if not upload_result.get("success"):
            return existing_refs, error_response(
                "resource_change", "CosUploadFailed",
                f"更新资源[{i}] COS上传失败: {upload_result.get('message', '')}",
            )

        # Step 3: Create new resource config version
        config_params = {
            "ResourceId": resource_id,
            "ResourceLoc": {
                "StorageType": 1,
                "Param": {
                    "Bucket": bucket,
                    "Path": key,
                    "Region": cos_region,
                },
            },
        }
        if workspace_id:
            config_params["WorkSpaceId"] = workspace_id

        config_result = call_api("CreateResourceConfig", config_params, region)
        if not config_result.get("success"):
            return existing_refs, error_response(
                "resource_change", "CreateResourceConfigFailed",
                f"更新资源[{i}] 创建资源版本失败: {config_result.get('error', '')}",
            )

        new_version = (config_result.get("data") or {}).get("Version", 1)

        ref_idx = ref_index[resource_id]
        existing_refs[ref_idx]["Version"] = new_version

        if verbose:
            print(
                f"[update]   -> {resource_id} Version 更新为 {new_version}",
                file=sys.stderr,
            )

    return existing_refs, None


# ═══════════════════════════════════════════════════════════════════════════
# Process Remove Resources
# ═══════════════════════════════════════════════════════════════════════════


def process_remove_resources(remove_ids_csv, existing_refs):
    """Process --remove_resources: filter out specified ResourceIds from refs.

    Returns:
        tuple (filtered_refs:list, removed_ids:list).
    """
    ids_to_remove = set(rid.strip() for rid in remove_ids_csv.split(",") if rid.strip())
    filtered = [ref for ref in existing_refs if ref.get("ResourceId") not in ids_to_remove]
    actually_removed = ids_to_remove & {ref.get("ResourceId") for ref in existing_refs}
    return filtered, sorted(actually_removed)


# ═══════════════════════════════════════════════════════════════════════════
# Resource Changes Summary
# ═══════════════════════════════════════════════════════════════════════════


def format_resource_changes_summary(added_refs, updated_entries, removed_ids):
    """Format a human-readable summary of resource reference changes."""
    lines = []
    if added_refs:
        lines.append(f"  新增资源引用 ({len(added_refs)} 个):")
        for ref in added_refs:
            rtype = int(ref.get("Type", -1))
            rtype_name = _RESOURCE_REF_TYPE_NAMES.get(rtype, str(rtype))
            lines.append(
                f"    + {ref.get('ResourceId', '?')} "
                f"(Type={rtype} {rtype_name}, Version={ref.get('Version', '?')})"
            )
    if updated_entries:
        lines.append(f"  更新资源文件 ({len(updated_entries)} 个):")
        for entry in updated_entries:
            lines.append(
                f"    ~ {entry.get('resource_id', '?')} <- {entry.get('file', '?')}"
            )
    if removed_ids:
        lines.append(f"  删除资源引用 ({len(removed_ids)} 个):")
        for rid in removed_ids:
            lines.append(f"    - {rid}")
    if not lines:
        lines.append("  资源引用: 无变更")
    return "\n".join(lines)
