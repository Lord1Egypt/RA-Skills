#!/usr/bin/env python3
"""Metadata / Catalog query commands for Oceanus CLI.

Provides Read commands to browse catalog, database, and table metadata:
- describe_catalogs: List all catalogs in a workspace
- describe_meta_catalogs: Browse default catalog (type=0) tree (databases + tables)
- describe_meta_table: Get table details in default catalog
- describe_external_meta_databases: List databases in external catalog (type!=0, async)
- describe_external_meta_tables: List/detail tables in external catalog (type!=0, async)
"""

import sys
import time

from client import (
    add_common_args,
    call_api,
    output,
    success_response,
)
from resource_resolver import (
    resolve_region,
    resolve_workspace,
)


# ═══════════════════════════════════════════════════════════════════════════
# Constants
# ═══════════════════════════════════════════════════════════════════════════

CATALOG_TYPE_OCEANUS = 0
CATALOG_TYPE_HIVE = 1
CATALOG_TYPE_MYSQL = 2
CATALOG_TYPE_PAIMON = 3

CATALOG_TYPE_NAMES = {
    0: "OCEANUS",
    1: "HIVE",
    2: "MYSQL",
    3: "PAIMON",
}

# Async polling defaults
_ASYNC_INITIAL_INTERVAL = 1.0   # seconds
_ASYNC_MAX_INTERVAL = 5.0       # seconds
_ASYNC_MAX_RETRIES = 30         # ~60s total worst case


# ═══════════════════════════════════════════════════════════════════════════
# Async Polling Helper
# ═══════════════════════════════════════════════════════════════════════════


def _async_poll(action, params, region, max_retries=_ASYNC_MAX_RETRIES, verbose=False):
    """Poll an async metadata query until completion.

    Workflow:
      1. First call with IsAsync=1 → get AsyncTaskId
      2. Subsequent calls with same params + AsyncTaskId until AsyncStatus != 0

    AsyncStatus meanings (from backend):
      0 = still processing
      1 = completed successfully
      Other = error / timeout

    Returns:
        (data_dict, error_response_or_None)
    """
    # Step 1: initial async request
    params["IsAsync"] = 1
    params.pop("AsyncTaskId", None)

    result = call_api(action, params, region)
    if not result.get("success"):
        return None, result

    data = result.get("data", {})
    async_status = data.get("AsyncStatus", 0)

    # If already done on first call
    if async_status == 1:
        return data, None

    async_task_id = data.get("AsyncTaskId", "")
    if not async_task_id:
        # No task id and not done — treat as synchronous success
        return data, None

    # Step 2: poll with AsyncTaskId
    interval = _ASYNC_INITIAL_INTERVAL
    for attempt in range(1, max_retries + 1):
        if verbose:
            sys.stderr.write(
                f"  [async poll] {action} attempt {attempt}/{max_retries}, "
                f"waiting {interval:.1f}s...\n"
            )
            sys.stderr.flush()

        time.sleep(interval)

        poll_params = dict(params)
        poll_params["AsyncTaskId"] = async_task_id

        result = call_api(action, poll_params, region)
        if not result.get("success"):
            return None, result

        data = result.get("data", {})
        async_status = data.get("AsyncStatus", 0)

        if async_status == 1:
            return data, None

        # Exponential backoff up to max
        interval = min(interval * 1.5, _ASYNC_MAX_INTERVAL)

    # Timeout
    return None, {
        "success": False,
        "operation": action,
        "error": {
            "code": "AsyncTimeout",
            "message": (
                f"Async query did not complete after {max_retries} retries (~60s). "
                "The external catalog may be slow to respond. "
                "Please retry later or check cluster resources."
            ),
        },
    }


# ═══════════════════════════════════════════════════════════════════════════
# Describe Catalogs
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_catalogs(args):
    """List all catalogs in a workspace."""
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)
    region = region_result["region"]

    ws_input = args.workspace_id or args.workspace_name
    if not ws_input:
        return output(
            {
                "success": False,
                "operation": "DescribeCatalogs",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --workspace_id 或 --workspace_name 指定工作空间",
                },
            },
            args.output,
        )
    ws_result = resolve_workspace(region, ws_input, verbose=args.verbose)
    if not ws_result.get("success"):
        return output(ws_result, args.output)
    workspace_id = ws_result["workspace_id"]

    params = {"WorkSpaceId": workspace_id}

    if getattr(args, "name", None):
        params["Filters"] = [{"Name": "Name", "Values": [args.name]}]

    result = call_api("DescribeCatalogs", params, region)
    if not result.get("success"):
        return output(result, args.output)

    data = result.get("data", {})
    catalogs = data.get("Catalogs", []) or []

    simplified = []
    for c in catalogs:
        t = c.get("Type", 0)
        simplified.append({
            "Id": c.get("Id", 0),
            "SerialId": c.get("SerialId", ""),
            "Name": c.get("Name", ""),
            "Type": t,
            "TypeName": CATALOG_TYPE_NAMES.get(t, "UNKNOWN"),
            "DefaultDatabase": c.get("DefaultDatabase", ""),
            "Comment": c.get("Comment", ""),
            "FlinkVersion": c.get("FlinkVersion", ""),
        })

    output(
        success_response(
            "DescribeCatalogs",
            {"WorkSpaceId": workspace_id, "TotalCount": len(simplified), "Catalogs": simplified},
        ),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Describe Meta Catalogs (default catalog type=0, tree structure)
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_meta_catalogs(args):
    """Browse default catalog (type=0) database & table tree."""
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)
    region = region_result["region"]

    ws_input = args.workspace_id or args.workspace_name
    if not ws_input:
        return output(
            {
                "success": False,
                "operation": "DescribeMetaCatalogs",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --workspace_id 或 --workspace_name 指定工作空间",
                },
            },
            args.output,
        )
    ws_result = resolve_workspace(region, ws_input, verbose=args.verbose)
    if not ws_result.get("success"):
        return output(ws_result, args.output)
    workspace_id = ws_result["workspace_id"]

    params = {"WorkSpaceId": workspace_id}

    if getattr(args, "serial_id", None):
        params["SerialId"] = args.serial_id

    if getattr(args, "table_count_limit", None):
        params["TableCountLimit"] = int(args.table_count_limit)

    if getattr(args, "name", None):
        params["Filters"] = [{"Name": "filterText", "Values": [args.name]}]

    result = call_api("DescribeMetaCatalogs", params, region)
    if not result.get("success"):
        return output(result, args.output)

    data = result.get("data", {})
    catalog_set = data.get("CatalogSet", []) or []

    simplified = []
    for cat in catalog_set:
        databases = []
        for db in (cat.get("DatabaseSet") or []):
            tables = []
            for tbl in (db.get("MetaTableSet") or []):
                tables.append({
                    "Id": tbl.get("Id", 0),
                    "SerialId": tbl.get("SerialId", ""),
                    "Name": tbl.get("Name", ""),
                    "Type": tbl.get("Type", ""),
                    "Version": tbl.get("Version", 0),
                    "UpdateTime": tbl.get("UpdateTime", ""),
                })
            databases.append({
                "Id": db.get("Id", 0),
                "Name": db.get("Name", ""),
                "TableCount": db.get("TableCount", 0),
                "Tables": tables,
            })
        simplified.append({
            "Id": cat.get("Id", 0),
            "Name": cat.get("Name", ""),
            "Databases": databases,
        })

    output(
        success_response(
            "DescribeMetaCatalogs",
            {"WorkSpaceId": workspace_id, "CatalogSet": simplified},
        ),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Describe Meta Table (default catalog, table detail)
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_meta_table(args):
    """Get table details in default catalog (type=0)."""
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)
    region = region_result["region"]

    ws_input = args.workspace_id or args.workspace_name
    if not ws_input:
        return output(
            {
                "success": False,
                "operation": "DescribeMetaTable",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --workspace_id 或 --workspace_name 指定工作空间",
                },
            },
            args.output,
        )
    ws_result = resolve_workspace(region, ws_input, verbose=args.verbose)
    if not ws_result.get("success"):
        return output(ws_result, args.output)
    workspace_id = ws_result["workspace_id"]

    if not getattr(args, "table_id", None):
        return output(
            {
                "success": False,
                "operation": "DescribeMetaTable",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --table_id 指定表 ID",
                },
            },
            args.output,
        )

    params = {
        "WorkSpaceId": workspace_id,
        "TableId": int(args.table_id),
    }

    result = call_api("DescribeMetaTable", params, region)
    if not result.get("success"):
        return output(result, args.output)

    data = result.get("data", {})

    # Build columns list
    columns = []
    for col in (data.get("Columns") or []):
        columns.append({
            "Name": col.get("Name", ""),
            "DataType": col.get("DataType", ""),
        })

    simplified = {
        "SerialId": data.get("SerialId", ""),
        "CatalogName": data.get("CatalogName", ""),
        "DatabaseName": data.get("DatabaseName", ""),
        "TableName": data.get("TableName", ""),
        "DDLSentence": data.get("DDLSentence", ""),
        "TableSchema": data.get("TableSchema", ""),
        "Columns": columns,
        "Properties": data.get("Properties", ""),
        "Type": data.get("Type", 0),
        "TableType": data.get("TableType", ""),
        "Version": data.get("Version", 0),
        "CreateTime": data.get("CreateTime", ""),
        "UpdateTime": data.get("UpdateTime", ""),
    }

    output(
        success_response("DescribeMetaTable", simplified),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Describe External Meta Databases (type!=0, async)
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_external_meta_databases(args):
    """List databases in an external catalog (type!=0). Uses async polling."""
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)
    region = region_result["region"]

    ws_input = args.workspace_id or args.workspace_name
    if not ws_input:
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaDatabases",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --workspace_id 或 --workspace_name 指定工作空间",
                },
            },
            args.output,
        )
    ws_result = resolve_workspace(region, ws_input, verbose=args.verbose)
    if not ws_result.get("success"):
        return output(ws_result, args.output)
    workspace_id = ws_result["workspace_id"]

    if not getattr(args, "catalog_id", None):
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaDatabases",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --catalog_id 指定 catalog（SerialId）",
                },
            },
            args.output,
        )

    if not getattr(args, "cluster_id", None):
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaDatabases",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --cluster_id 指定集群 ID",
                },
            },
            args.output,
        )

    if not getattr(args, "flink_version", None):
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaDatabases",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --flink_version 指定 Flink 版本（如 Flink-1.16）",
                },
            },
            args.output,
        )

    params = {
        "WorkSpaceId": workspace_id,
        "CatalogId": args.catalog_id,
        "ClusterId": args.cluster_id,
        "FlinkVersion": args.flink_version,
    }
    if getattr(args, "name", None):
        params["Filters"] = [{"Name": "DatabaseName", "Values": [args.name]}]

    data, err = _async_poll(
        "DescribeExternalMetaDatabases", params, region, verbose=args.verbose
    )
    if err:
        return output(err, args.output)

    databases = data.get("DatabaseSetItem", []) or []
    catalog_type = data.get("CatalogType", -1)

    simplified = []
    for db in databases:
        simplified.append({
            "Catalog": db.get("Catalog", ""),
            "CatalogId": db.get("CatalogId", ""),
            "DatabaseName": db.get("DatabaseName", ""),
            "DatabaseProperties": db.get("DatabaseProperties", ""),
        })

    output(
        success_response(
            "DescribeExternalMetaDatabases",
            {
                "WorkSpaceId": workspace_id,
                "CatalogId": args.catalog_id,
                "CatalogType": catalog_type,
                "CatalogTypeName": CATALOG_TYPE_NAMES.get(catalog_type, "UNKNOWN"),
                "TotalCount": len(simplified),
                "Databases": simplified,
            },
        ),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Describe External Meta Tables (type!=0, async)
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_external_meta_tables(args):
    """List/detail tables in an external catalog (type!=0). Uses async polling."""
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)
    region = region_result["region"]

    ws_input = args.workspace_id or args.workspace_name
    if not ws_input:
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaTables",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --workspace_id 或 --workspace_name 指定工作空间",
                },
            },
            args.output,
        )
    ws_result = resolve_workspace(region, ws_input, verbose=args.verbose)
    if not ws_result.get("success"):
        return output(ws_result, args.output)
    workspace_id = ws_result["workspace_id"]

    if not getattr(args, "catalog_id", None):
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaTables",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --catalog_id 指定 catalog（SerialId）",
                },
            },
            args.output,
        )

    if not getattr(args, "database_name", None):
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaTables",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --database_name 指定数据库名称",
                },
            },
            args.output,
        )

    if not getattr(args, "cluster_id", None):
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaTables",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --cluster_id 指定集群 ID",
                },
            },
            args.output,
        )

    if not getattr(args, "flink_version", None):
        return output(
            {
                "success": False,
                "operation": "DescribeExternalMetaTables",
                "error": {
                    "code": "MissingParameter",
                    "message": "需要 --flink_version 指定 Flink 版本（如 Flink-1.16）",
                },
            },
            args.output,
        )

    params = {
        "CatalogId": args.catalog_id,
        "DatabaseName": args.database_name,
        "ClusterId": args.cluster_id,
        "FlinkVersion": args.flink_version,
    }

    if getattr(args, "table_name", None):
        params["TableName"] = args.table_name
    if getattr(args, "name", None):
        params["Filters"] = [{"Name": "TableName", "Values": [args.name]}]

    data, err = _async_poll(
        "DescribeExternalMetaTables", params, region, verbose=args.verbose
    )
    if err:
        return output(err, args.output)

    tables = data.get("TablesSetItem", []) or []

    simplified = []
    for tbl in tables:
        columns = []
        for col in (tbl.get("Columns") or []):
            columns.append({
                "Name": col.get("Name", ""),
                "DataType": col.get("DataType", ""),
            })
        simplified.append({
            "TableName": tbl.get("TableName", ""),
            "Database": tbl.get("Database", ""),
            "Catalog": tbl.get("Catalog", ""),
            "CatalogId": tbl.get("CatalogId", ""),
            "Columns": columns,
            "TableProperties": tbl.get("TableProperties", ""),
            "TableType": tbl.get("TableType", ""),
        })

    output(
        success_response(
            "DescribeExternalMetaTables",
            {
                "WorkSpaceId": workspace_id,
                "CatalogId": args.catalog_id,
                "DatabaseName": args.database_name,
                "TotalCount": len(simplified),
                "Tables": simplified,
            },
        ),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Subparser registration
# ═══════════════════════════════════════════════════════════════════════════


def register(subparsers):
    """Register all metadata query subcommands."""

    def _add(name, help_text, func, extra_args=None):
        p = subparsers.add_parser(name, help=help_text)
        add_common_args(p)
        if extra_args:
            extra_args(p)
        p.set_defaults(func=func, subcommand=name)

    # ── Describe Catalogs ─────────────────────────────────────────────

    def _describe_catalogs_args(p):
        p.add_argument("--workspace_name", help="Workspace name (alternative to --workspace_id)")
        p.add_argument("--name", help="Filter catalogs by name")

    _add(
        "describe_catalogs",
        "List all catalogs in a workspace",
        cmd_describe_catalogs,
        _describe_catalogs_args,
    )

    # ── Describe Meta Catalogs ────────────────────────────────────────

    def _describe_meta_catalogs_args(p):
        p.add_argument("--workspace_name", help="Workspace name (alternative to --workspace_id)")
        p.add_argument("--serial_id", help="Catalog SerialId to query specific catalog")
        p.add_argument("--table_count_limit", help="Max tables per database (default: all)")
        p.add_argument("--name", help="Filter by database/table name substring")

    _add(
        "describe_meta_catalogs",
        "Browse default catalog (type=0) database & table tree",
        cmd_describe_meta_catalogs,
        _describe_meta_catalogs_args,
    )

    # ── Describe Meta Table ───────────────────────────────────────────

    def _describe_meta_table_args(p):
        p.add_argument("--workspace_name", help="Workspace name (alternative to --workspace_id)")
        p.add_argument("--table_id", required=True, help="Table ID (from describe_meta_catalogs)")

    _add(
        "describe_meta_table",
        "Get table details in default catalog (type=0)",
        cmd_describe_meta_table,
        _describe_meta_table_args,
    )

    # ── Describe External Meta Databases ──────────────────────────────

    def _describe_external_meta_databases_args(p):
        p.add_argument("--workspace_name", help="Workspace name (alternative to --workspace_id)")
        p.add_argument("--catalog_id", required=True, help="Catalog SerialId (from describe_catalogs)")
        p.add_argument("--cluster_id", required=True, help="Cluster ID (required for external catalog async query)")
        p.add_argument("--flink_version", required=True, help="Flink version (e.g. Flink-1.16, must match catalog)")
        p.add_argument("--name", help="Filter databases by name")

    _add(
        "describe_external_meta_databases",
        "List databases in external catalog (type!=0, async)",
        cmd_describe_external_meta_databases,
        _describe_external_meta_databases_args,
    )

    # ── Describe External Meta Tables ─────────────────────────────────

    def _describe_external_meta_tables_args(p):
        p.add_argument("--workspace_name", help="Workspace name (alternative to --workspace_id)")
        p.add_argument("--catalog_id", required=True, help="Catalog SerialId (from describe_catalogs)")
        p.add_argument("--database_name", required=True, help="Database name to list tables from")
        p.add_argument("--table_name", help="Specific table name for detail view")
        p.add_argument("--cluster_id", required=True, help="Cluster ID (required for external catalog async query)")
        p.add_argument("--flink_version", required=True, help="Flink version (e.g. Flink-1.16, must match catalog)")
        p.add_argument("--name", help="Filter tables by name")

    _add(
        "describe_external_meta_tables",
        "List/detail tables in external catalog (type!=0, async)",
        cmd_describe_external_meta_tables,
        _describe_external_meta_tables_args,
    )
