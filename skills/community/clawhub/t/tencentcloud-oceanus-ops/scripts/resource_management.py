#!/usr/bin/env python3
"""Resource (dependency) management workflow — upload, version, and query dependencies.

This module implements the dependency resource management flow:
- describe_tree_resources: Query dependency resources in tree structure
- create_resource: Create a new dependency resource (jar / config file)
- create_presigned_url: Get COS presigned upload URL
- create_resource_config: Create a new resource config version
- upload_resource: Orchestrated flow (presigned URL → COS upload → create version)

Resource types:
- 1: jar package
- 2: config file

Folder types:
- 0: job folder (default)
- 1: dependency resource folder
"""

import json
import mimetypes
import os
import sys
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

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
# Resource type constants
# ═══════════════════════════════════════════════════════════════════════════

RESOURCE_TYPE_JAR = 1
RESOURCE_TYPE_CONFIG = 2

RESOURCE_TYPE_MAP = {
    "1": "jar",
    "2": "config",
    "jar": "jar",
    "config": "config",
}


# ═══════════════════════════════════════════════════════════════════════════
# Describe Tree Resources
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_tree_resources(args):
    """Query dependency resources in tree structure (folders + resources)."""
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
    if getattr(args, "offset", None) is not None:
        params["Offset"] = int(args.offset)
    if getattr(args, "limit", None) is not None:
        params["Limit"] = int(args.limit)

    result = call_api("DescribeTreeResources", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Create Resource
# ═══════════════════════════════════════════════════════════════════════════


def cmd_create_resource(args):
    """Create a new dependency resource record (jar or config file).

    ResourceType: 1=jar, 2=config file
    """
    err = require_args(args, "region", "name", "resource_type")
    if err:
        return output(err, args.output)

    resource_type = int(args.resource_type)
    if resource_type not in (RESOURCE_TYPE_JAR, RESOURCE_TYPE_CONFIG):
        return output(
            error_response("create_resource", "ValidationError",
                           "resource_type 必须为 1 (jar) 或 2 (config)"),
            args.output,
        )

    type_desc = "jar包" if resource_type == RESOURCE_TYPE_JAR else "配置文件"
    chk = require_confirmation(
        "create_resource",
        f"创建依赖资源 '{args.name}' (类型: {type_desc})",
        args.confirm,
    )
    if chk:
        return output(chk, args.output)

    params = {
        "Name": args.name,
        "ResourceType": resource_type,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id
    if getattr(args, "folder_id", None):
        params["FolderId"] = args.folder_id
    if getattr(args, "remark", None):
        params["Remark"] = args.remark

    # Build ResourceLoc if COS info provided (CreateResource API requires it)
    bucket = getattr(args, "bucket", None)
    cos_path = getattr(args, "cos_path", None)
    cos_region = getattr(args, "cos_region", None)
    if bucket or cos_path or cos_region:
        params["ResourceLoc"] = {
            "StorageType": 1,  # COS
            "Param": {
                "Bucket": bucket or "",
                "Path": cos_path or "",
                "Region": cos_region or args.region,
            },
        }

    result = call_api("CreateResource", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Create Presigned URL
# ═══════════════════════════════════════════════════════════════════════════


def cmd_create_presigned_url(args):
    """Get COS presigned URL for uploading dependency files.

    Returns Bucket, Key (object path), Location (presigned URL), Region.
    """
    err = require_args(args, "region")
    if err:
        return output(err, args.output)

    params = {}

    if getattr(args, "file_name", None):
        params["FileName"] = args.file_name
    if getattr(args, "http_method", None):
        params["HttpMethod"] = args.http_method
    if getattr(args, "expired", None):
        params["Expired"] = int(args.expired)

    result = call_api("CreatePresignedUrl", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Create Resource Config (new version)
# ═══════════════════════════════════════════════════════════════════════════


def cmd_create_resource_config(args):
    """Create a new version for an existing dependency resource.

    Associates COS storage location (Bucket/Path/Region) with the resource.
    """
    err = require_args(args, "region", "resource_id")
    if err:
        return output(err, args.output)

    params = {
        "ResourceId": args.resource_id,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id
    if getattr(args, "remark", None):
        params["Remark"] = args.remark

    # Build ResourceLocation if COS info provided
    bucket = getattr(args, "bucket", None)
    cos_path = getattr(args, "cos_path", None)
    cos_region = getattr(args, "cos_region", None)

    if bucket or cos_path or cos_region:
        resource_loc = {
            "StorageType": 1,  # COS
            "Param": {
                "Bucket": bucket or "",
                "Path": cos_path or "",
                "Region": cos_region or args.region,
            },
        }
        params["ResourceLoc"] = resource_loc

    result = call_api("CreateResourceConfig", params, args.region)
    output(result, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Upload Resource (orchestrated flow)
# ═══════════════════════════════════════════════════════════════════════════


def upload_to_cos(presigned_url, file_path):
    """Upload local file to COS via presigned URL using HTTP PUT.

    This is a public API — other modules (e.g. job_development) may
    import and call it directly.

    Args:
        presigned_url: The presigned URL (Location from CreatePresignedUrl)
        file_path: Local file path to upload

    Returns:
        dict: success/error envelope
    """
    try:
        file_size = os.path.getsize(file_path)
        content_type, _ = mimetypes.guess_type(file_path)
        if not content_type:
            content_type = "application/octet-stream"

        with open(file_path, "rb") as f:
            file_data = f.read()

        req = Request(
            presigned_url,
            data=file_data,
            method="PUT",
        )
        req.add_header("Content-Type", content_type)
        req.add_header("Content-Length", str(file_size))

        resp = urlopen(req, timeout=300)
        status = resp.getcode()

        if 200 <= status < 300:
            return {
                "success": True,
                "status_code": status,
                "file_size": file_size,
                "content_type": content_type,
            }
        else:
            body = resp.read().decode("utf-8", errors="replace")
            return {
                "success": False,
                "status_code": status,
                "message": body[:500],
            }
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if e.fp else ""
        return {
            "success": False,
            "status_code": e.code,
            "message": f"HTTP {e.code}: {body[:500]}",
        }
    except URLError as e:
        return {
            "success": False,
            "message": f"NetworkError: {e.reason}",
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"UploadError: {str(e)}",
        }


# Backward-compatible alias (was previously a private function).
_upload_to_cos = upload_to_cos


def cmd_upload_resource(args):
    """Orchestrated: get presigned URL → COS upload → create resource config version.

    Steps:
    1. CreatePresignedUrl → get Bucket/Key/Location(presigned URL)/Region
    2. HTTP PUT file to Location (presigned URL)
    3. CreateResourceConfig with ResourceLocation{StorageType=1, Param={Bucket, Path=Key, Region}}
    """
    err = require_args(args, "region", "resource_id", "file")
    if err:
        return output(err, args.output)

    file_path = args.file
    if not os.path.isfile(file_path):
        return output(
            error_response("upload_resource", "ValidationError",
                           f"文件不存在: {file_path}"),
            args.output,
        )

    file_name = os.path.basename(file_path)
    region = args.region
    resource_id = args.resource_id
    workspace_id = getattr(args, "workspace_id", None)

    chk = require_confirmation(
        "upload_resource",
        f"上传文件 '{file_name}' 到资源 {resource_id}",
        args.confirm,
    )
    if chk:
        return output(chk, args.output)

    # ── Step 1: Get presigned URL ─────────────────────────────────────
    if args.verbose:
        print(f"[upload] Step 1/3: 获取预签名上传链接 (文件: {file_name})...", file=sys.stderr)

    presign_params = {
        "FileName": file_name,
        "HttpMethod": "PUT",
    }

    result = call_api("CreatePresignedUrl", presign_params, region)
    if not result.get("success"):
        return output(
            error_response("upload_resource", "GetPresignedUrlFailed",
                           f"获取预签名URL失败: {result.get('error', {}).get('message', '')}"),
            args.output,
        )

    presign_data = result.get("data", {})
    presigned_url = presign_data.get("Location", "")
    bucket = presign_data.get("Bucket", "")
    key = presign_data.get("Key", "")
    cos_region = presign_data.get("Region", region)

    if not presigned_url:
        return output(
            error_response("upload_resource", "GetPresignedUrlFailed",
                           "预签名URL返回为空"),
            args.output,
        )

    if args.verbose:
        print(f"[upload] 预签名URL获取成功: Bucket={bucket}, Key={key}", file=sys.stderr)

    # ── Step 2: Upload file to COS ────────────────────────────────────
    if args.verbose:
        file_size = os.path.getsize(file_path)
        print(f"[upload] Step 2/3: 上传文件到 COS ({file_size} bytes)...", file=sys.stderr)

    upload_result = upload_to_cos(presigned_url, file_path)
    if not upload_result.get("success"):
        return output(
            error_response("upload_resource", "CosUploadFailed",
                           f"COS上传失败: {upload_result.get('message', '')}"),
            args.output,
        )

    if args.verbose:
        print(f"[upload] 文件上传成功 (HTTP {upload_result.get('status_code', '?')})", file=sys.stderr)

    # ── Step 3: Create resource config version ────────────────────────
    if args.verbose:
        print("[upload] Step 3/3: 创建资源版本...", file=sys.stderr)

    config_params = {
        "ResourceId": resource_id,
        "ResourceLoc": {
            "StorageType": 1,  # COS
            "Param": {
                "Bucket": bucket,
                "Path": key,
                "Region": cos_region,
            },
        },
    }

    if workspace_id:
        config_params["WorkSpaceId"] = workspace_id
    if getattr(args, "remark", None):
        config_params["Remark"] = args.remark

    result = call_api("CreateResourceConfig", config_params, region)
    if not result.get("success"):
        return output(
            error_response("upload_resource", "CreateResourceConfigFailed",
                           f"创建资源版本失败: {result.get('error', {}).get('message', '')}"),
            args.output,
        )

    version = result.get("data", {}).get("Version", "unknown")
    final = success_response("upload_resource", {
        "message": f"依赖资源上传并创建版本成功，版本号: {version}",
        "resource_id": resource_id,
        "version": version,
        "file_name": file_name,
        "bucket": bucket,
        "key": key,
        "cos_region": cos_region,
    })
    output(final, args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Subparser registration
# ═══════════════════════════════════════════════════════════════════════════


def register(subparsers):
    """Register all resource management subcommands."""

    def _add(name, help_text, func, extra_args=None):
        p = subparsers.add_parser(name, help=help_text)
        add_common_args(p)
        if extra_args:
            extra_args(p)
        p.set_defaults(func=func, subcommand=name)

    # ── Describe Tree Resources ───────────────────────────────────────

    def _describe_tree_resources_args(p):
        p.add_argument(
            "--filters",
            help="Filters in format 'Name=value;Name2=value2' (semicolon-separated)",
        )
        p.add_argument("--offset", help="Pagination offset")
        p.add_argument("--limit", help="Pagination limit (-1 for all)")

    _add(
        "describe_tree_resources",
        "Query dependency resources in tree structure",
        cmd_describe_tree_resources,
        _describe_tree_resources_args,
    )

    # ── Create Resource ───────────────────────────────────────────────

    def _create_resource_args(p):
        p.add_argument("--name", required=True, help="Resource name")
        p.add_argument(
            "--resource_type",
            required=True,
            help="Resource type: 1=jar, 2=config",
        )
        p.add_argument("--folder_id", help="Folder ID to place resource in")
        p.add_argument("--remark", help="Resource remark")
        p.add_argument("--bucket", help="COS bucket name (for ResourceLoc)")
        p.add_argument("--cos_path", help="COS object key/path (for ResourceLoc)")
        p.add_argument("--cos_region", help="COS region (default: same as --region)")
        p.add_argument("--confirm", action="store_true", help="Skip interactive confirmation")

    _add(
        "create_resource",
        "Create a new dependency resource (jar/config)",
        cmd_create_resource,
        _create_resource_args,
    )

    # ── Create Presigned URL ──────────────────────────────────────────

    def _create_presigned_url_args(p):
        p.add_argument("--file_name", help="File name for the upload")
        p.add_argument(
            "--http_method",
            default="PUT",
            help="HTTP method: PUT/POST/GET (default: PUT)",
        )
        p.add_argument(
            "--expired",
            help="Expiry time in seconds (default: 3600)",
        )

    _add(
        "create_presigned_url",
        "Get COS presigned URL for uploading",
        cmd_create_presigned_url,
        _create_presigned_url_args,
    )

    # ── Create Resource Config ────────────────────────────────────────

    def _create_resource_config_args(p):
        p.add_argument("--resource_id", required=True, help="Resource ID")
        p.add_argument("--bucket", help="COS bucket name")
        p.add_argument("--cos_path", help="COS object key/path")
        p.add_argument("--cos_region", help="COS region (default: same as --region)")
        p.add_argument("--remark", help="Version remark")

    _add(
        "create_resource_config",
        "Create a new resource config version",
        cmd_create_resource_config,
        _create_resource_config_args,
    )

    # ── Upload Resource (orchestrated) ────────────────────────────────

    def _upload_resource_args(p):
        p.add_argument("--resource_id", required=True, help="Resource ID")
        p.add_argument("--file", required=True, help="Local file path to upload")
        p.add_argument("--remark", help="Version remark")
        p.add_argument("--confirm", action="store_true", help="Skip interactive confirmation")

    _add(
        "upload_resource",
        "Upload file and create resource version (presigned URL → COS → version)",
        cmd_upload_resource,
        _upload_resource_args,
    )
