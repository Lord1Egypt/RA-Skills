#!/usr/bin/env python3
"""Folder management — create, query, modify, delete folders.

Extracted from job_development.py for better modularity.
"""

from client import (
    add_common_args,
    call_api,
    error_response,
    output,
    require_args,
    require_confirmation,
)


# ═══════════════════════════════════════════════════════════════════════════
# Folder Management
# ═══════════════════════════════════════════════════════════════════════════


def cmd_create_folder(args):
    """Create a new folder in the workspace.

    FolderType: 0=job folder (default)
    """
    err = require_args(args, "region", "folder_name")
    if err:
        return output(err, args.output)

    params = {
        "FolderName": args.folder_name,
        "FolderType": int(args.folder_type) if args.folder_type else 0,
        "ParentId": args.parent_id if args.parent_id else "root",
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id

    result = call_api("CreateFolder", params, args.region)
    output(result, args.output)


def cmd_describe_folder(args):
    """Query folder details by folder ID."""
    err = require_args(args, "region", "folder_id")
    if err:
        return output(err, args.output)

    params = {
        "FolderId": args.folder_id,
        "FolderType": int(args.folder_type) if args.folder_type else 0,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id

    result = call_api("DescribeFolder", params, args.region)
    output(result, args.output)


def cmd_query_folder(args):
    """Query folder by name in workspace."""
    err = require_args(args, "region", "folder_name")
    if err:
        return output(err, args.output)

    params = {
        "FolderName": args.folder_name,
        "FolderType": int(args.folder_type) if args.folder_type else 0,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id

    result = call_api("QueryFolder", params, args.region)
    output(result, args.output)


def cmd_modify_folder(args):
    """Modify folder: rename, move folder, or move jobs into folder.

    - Rename: --source_folder_id + --folder_name
    - Move folder: --source_folder_id + --target_folder_id
    - Move jobs: --source_job_ids + --target_folder_id
    """
    err = require_args(args, "region")
    if err:
        return output(err, args.output)

    if not args.source_folder_id and not args.source_job_ids:
        return output(
            error_response("modify_folder", "必须提供 --source_folder_id 或 --source_job_ids"),
            args.output,
        )

    params = {
        "FolderType": int(args.folder_type) if args.folder_type else 0,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id
    if args.source_folder_id:
        params["SourceFolderId"] = args.source_folder_id
    if args.target_folder_id:
        params["TargetFolderId"] = args.target_folder_id
    if args.folder_name:
        params["FolderName"] = args.folder_name
    if args.source_job_ids:
        params["SourceJobIds"] = args.source_job_ids.split(",")

    result = call_api("ModifyFolder", params, args.region)
    output(result, args.output)


def cmd_delete_folders(args):
    """Delete folders by IDs."""
    err = require_args(args, "region", "folder_ids")
    if err:
        return output(err, args.output)

    chk = require_confirmation(
        "delete_folders",
        f"Delete folders: {args.folder_ids}",
        args.confirm,
    )
    if chk:
        return output(chk, args.output)

    params = {
        "FolderIds": args.folder_ids.split(","),
        "FolderType": int(args.folder_type) if args.folder_type else 0,
    }

    if args.workspace_id:
        params["WorkSpaceId"] = args.workspace_id

    result = call_api("DeleteFolders", params, args.region)
    output(result, args.output)


def resolve_or_create_folder(args, region, workspace_id):
    """Resolve folder: use --folder_id directly, or find/create by --folder_name.

    Returns:
        tuple: (folder_id: str or None, error_result: dict or None)
    """
    folder_id = getattr(args, "folder_id", None)
    folder_name = getattr(args, "folder_name", None)

    if folder_id:
        return folder_id, None

    if not folder_name:
        return None, None

    # Try to find existing folder by name
    query_params = {
        "FolderName": folder_name,
        "FolderType": 0,  # job folder
    }
    if workspace_id:
        query_params["WorkSpaceId"] = workspace_id

    result = call_api("QueryFolder", query_params, region)
    if result.get("success"):
        data = result.get("data", {})
        # QueryFolder returns folder info if found
        found_id = data.get("FolderId", "")
        if found_id:
            return found_id, None

    # Folder not found, create it
    create_params = {
        "FolderName": folder_name,
        "FolderType": 0,
    }
    if workspace_id:
        create_params["WorkSpaceId"] = workspace_id

    parent_id = getattr(args, "parent_id", None)
    if parent_id:
        create_params["ParentId"] = parent_id

    result = call_api("CreateFolder", create_params, region)
    if not result.get("success"):
        return None, error_response("create_folder", f"创建文件夹'{folder_name}'失败: {result.get('error', '')}")

    new_folder_id = result.get("data", {}).get("FolderId", "")
    if not new_folder_id:
        return None, error_response("create_folder", f"创建文件夹'{folder_name}'后未返回 FolderId")

    return new_folder_id, None


# ═══════════════════════════════════════════════════════════════════════════
# Subparser registration
# ═══════════════════════════════════════════════════════════════════════════


def register(subparsers):
    """Register all folder management subcommands."""

    def _add(name, help_text, func, extra_args=None):
        p = subparsers.add_parser(name, help=help_text)
        add_common_args(p)
        if extra_args:
            extra_args(p)
        p.set_defaults(func=func, subcommand=name)

    # ── Create Folder ─────────────────────────────────────────────────

    def _create_folder_args(p):
        p.add_argument("--folder_name", required=True, help="Folder name to create")
        p.add_argument("--parent_id", help="Parent folder ID (omit for root level)")
        p.add_argument("--folder_type", default="0", help="Folder type: 0=job folder (default: 0)")
        p.add_argument("--confirm", action="store_true", help="Skip interactive confirmation")

    _add("create_folder", "Create a new folder in workspace", cmd_create_folder, _create_folder_args)

    # ── Describe Folder ───────────────────────────────────────────────

    def _describe_folder_args(p):
        p.add_argument("--folder_id", required=True, help="Folder ID to query")
        p.add_argument("--folder_type", default="0", help="Folder type: 0=job folder (default: 0)")

    _add("describe_folder", "Query folder details by ID", cmd_describe_folder, _describe_folder_args)

    # ── Query Folder ──────────────────────────────────────────────────

    def _query_folder_args(p):
        p.add_argument("--folder_name", required=True, help="Folder name to search")
        p.add_argument("--folder_type", default="0", help="Folder type: 0=job folder (default: 0)")

    _add("query_folder", "Query folder by name", cmd_query_folder, _query_folder_args)

    # ── Modify Folder ─────────────────────────────────────────────────

    def _modify_folder_args(p):
        p.add_argument("--source_folder_id", help="Source folder ID to rename or move")
        p.add_argument("--target_folder_id", help="Target folder ID (for move operations)")
        p.add_argument("--folder_name", help="New folder name (for rename operations)")
        p.add_argument("--source_job_ids", help="Comma-separated job IDs to move into target folder")
        p.add_argument("--folder_type", default="0", help="Folder type: 0=job folder (default: 0)")
        p.add_argument("--confirm", action="store_true", help="Skip interactive confirmation")

    _add("modify_folder", "Modify folder (rename/move/move jobs)", cmd_modify_folder, _modify_folder_args)

    # ── Delete Folders ────────────────────────────────────────────────

    def _delete_folders_args(p):
        p.add_argument("--folder_ids", required=True, help="Comma-separated folder IDs to delete")
        p.add_argument("--folder_type", default="0", help="Folder type: 0=job folder (default: 0)")
        p.add_argument("--confirm", action="store_true", help="Skip interactive confirmation")

    _add("delete_folders", "Delete folders by IDs", cmd_delete_folders, _delete_folders_args)
