#!/usr/bin/env python3
"""Resource query commands for Oceanus CLI.

Provides standalone Read commands to query Oceanus resources:
- describe_regions: List available regions
- describe_workspaces: List workspaces in a region
- describe_clusters: List clusters bound to a workspace
- describe_variables: List workspace variables for template substitution
  (e.g. ${ROW_PS} placeholders inside SQL WITH clauses)
"""

from client import (
    add_common_args,
    call_api,
    output,
    require_args,
    success_response,
)
from resource_resolver import (
    CLUSTER_STATUS_RUNNING,
    DEFAULT_REGION,
    resolve_region,
    resolve_workspace,
)


# ═══════════════════════════════════════════════════════════════════════════
# Describe Regions
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_regions(args):
    """List available regions."""
    # Use default region for the API call itself
    region_for_call = getattr(args, "region", None) or DEFAULT_REGION

    result = call_api("DescribeRegionZones", {}, region_for_call)
    if not result.get("success"):
        return output(result, args.output)

    data = result.get("data", {})
    net_envs = data.get("NetEnvs", [])

    # Flatten into a simple region list
    regions = []
    for net_env in net_envs:
        for region_detail in net_env.get("Regions", []):
            regions.append({
                "Region": region_detail.get("Region", ""),
                "RegionDesc": region_detail.get("RegionDesc", ""),
                "State": region_detail.get("State", 0),
                "ClusterCount": region_detail.get("ClusterCount", 0),
                "JobCount": region_detail.get("JobCount", 0),
            })

    output(success_response("DescribeRegionZones", {"Regions": regions}), args.output)


# ═══════════════════════════════════════════════════════════════════════════
# Describe Workspaces
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_workspaces(args):
    """List workspaces in a region."""
    # Resolve region first
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)

    region = region_result["region"]

    params = {
        "Offset": int(args.offset) if args.offset else 0,
        "Limit": int(args.limit) if args.limit else 20,
    }

    # Add name filter if provided
    if args.name:
        params["Filters"] = [{"Name": "WorkSpaceName", "Values": [args.name]}]

    result = call_api("DescribeWorkSpaces", params, region)
    if not result.get("success"):
        return output(result, args.output)

    data = result.get("data", {})
    workspaces = data.get("WorkSpaceSetItem", [])

    # Simplify output for readability
    simplified = []
    for ws in workspaces:
        clusters = ws.get("ClusterGroupSetItem", [])
        cluster_summary = []
        for c in clusters:
            cluster_summary.append({
                "ClusterId": c.get("ClusterId", ""),
                "Name": c.get("Name", ""),
                "FreeCu": c.get("FreeCu", 0) or c.get("FreeCuNum", 0),
                "Status": c.get("Status", 0),
                "StatusDesc": c.get("StatusDesc", ""),
            })

        simplified.append({
            "WorkSpaceId": ws.get("WorkSpaceId") or ws.get("SerialId", ""),
            "WorkSpaceName": ws.get("WorkSpaceName", ""),
            "Region": ws.get("Region", ""),
            "Status": ws.get("Status", 0),
            "ClusterCount": len(clusters),
            "Clusters": cluster_summary,
            "JobsCount": ws.get("JobsCount", 0),
        })

    output(
        success_response(
            "DescribeWorkSpaces",
            {"TotalCount": data.get("TotalCount", 0), "WorkSpaces": simplified},
        ),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Describe Clusters
# ═══════════════════════════════════════════════════════════════════════════


def cmd_describe_clusters(args):
    """List clusters bound to a workspace."""
    # Resolve region
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)

    region = region_result["region"]

    # Resolve workspace if provided
    workspace_id = None
    if args.workspace_id or args.workspace_name:
        ws_input = args.workspace_id or args.workspace_name
        ws_result = resolve_workspace(region, ws_input, verbose=args.verbose)
        if not ws_result.get("success"):
            return output(ws_result, args.output)
        workspace_id = ws_result["workspace_id"]

    params = {
        "Offset": int(args.offset) if args.offset else 0,
        "Limit": int(args.limit) if args.limit else 20,
    }

    if workspace_id:
        params["WorkSpaceId"] = workspace_id

    if args.cluster_ids:
        params["ClusterIds"] = args.cluster_ids.split(",")

    result = call_api("DescribeClusters", params, region)
    if not result.get("success"):
        return output(result, args.output)

    data = result.get("data", {})
    clusters = data.get("ClusterSet", [])

    # Simplify output
    simplified = []
    for c in clusters:
        version = c.get("Version") or {}
        simplified.append({
            "ClusterId": c.get("ClusterId", ""),
            "Name": c.get("Name", ""),
            "Status": c.get("Status", 0),
            "StatusDesc": c.get("StatusDesc", ""),
            "CuNum": c.get("CuNum", 0),
            "FreeCu": c.get("FreeCu", 0) or c.get("FreeCuNum", 0),
            "RunningCu": c.get("RunningCu", 0),
            "Region": c.get("Region", ""),
            "Zone": c.get("Zone", ""),
            "FlinkVersion": version.get("Flink", ""),
            "SupportedFlink": version.get("SupportedFlink", []),
            "JdkSupportVersion": version.get("JdkSupportVersion", []),
        })

    output(
        success_response(
            "DescribeClusters",
            {"TotalCount": data.get("TotalCount", 0), "Clusters": simplified},
        ),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Describe Variables
# ═══════════════════════════════════════════════════════════════════════════

# VariableItem.Type enum (matches oceanus-galileo constants.go):
#   1 = VISIBLE  — 明文变量，Value 直接可读
#   2 = HIDDEN   — 隐藏/密文变量，后端会把 Value 置为空字符串再返回
#   3 = SYSTEM   — 系统内置变量，如 ${SYSTEM_JOB_ID} / ${SYSTEM_CLUSTER_ID}
VARIABLE_TYPE_NAMES = {
    1: "VISIBLE",
    2: "HIDDEN",
    3: "SYSTEM",
}


def cmd_describe_variables(args):
    """List workspace variables (used for ${var} substitution in SQL WITH clauses).

    Backend: DescribeVariables (see oceanus-galileo
    src/tstream_cc/controller/cloud_api/variable/describe_variables.go and
    service/variable/describe_variables_service.go).

    Request fields actually honored by the backend:
      - WorkSpaceId (required)
      - Filters     (optional, single entry; must have Name="Name" and
                     Values=[<substring>]. Backend does a LIKE '%v%' match
                     against the variable Name column.)
      - SerialIds   (defined in the model but **not used** by the service —
                     CLI does not expose it.)

    Response: VariableSet[] with SerialId / Name / Value / Type / Remark /
    CreateTime / CreatorUin. The service also appends two synthetic system
    variables (Type=3, SYSTEM) representing the current job / cluster
    placeholder.
    """
    # Resolve region first
    region_result = resolve_region(args.region, verbose=args.verbose)
    if not region_result.get("success"):
        return output(region_result, args.output)
    region = region_result["region"]

    # Workspace is required for this API
    ws_input = args.workspace_id or args.workspace_name
    if not ws_input:
        return output(
            {
                "success": False,
                "operation": "DescribeVariables",
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

    # Backend Filter contract: only one entry, Name MUST be the literal
    # string "Name", value is matched with SQL LIKE '%v%'. '%' is rejected
    # by the backend; '_' is auto-escaped.
    if getattr(args, "name", None):
        params["Filters"] = [{"Name": "Name", "Values": [args.name]}]

    result = call_api("DescribeVariables", params, region)
    if not result.get("success"):
        return output(result, args.output)

    data = result.get("data", {})
    variables = data.get("VariableSet", []) or []

    # Pass-through projection — keep the full schema so the agent can decide
    # what to do with Type / Remark / CreateTime etc.
    simplified = []
    for v in variables:
        t = v.get("Type", 0)
        simplified.append(
            {
                "SerialId": v.get("SerialId", ""),
                "Name": v.get("Name", ""),
                "Value": v.get("Value", ""),
                "Type": t,
                "TypeName": VARIABLE_TYPE_NAMES.get(t, "UNKNOWN"),
                "Remark": v.get("Remark", ""),
                "CreateTime": v.get("CreateTime", ""),
                "CreatorUin": v.get("CreatorUin", ""),
            }
        )

    output(
        success_response(
            "DescribeVariables",
            {
                "WorkSpaceId": workspace_id,
                "TotalCount": len(simplified),
                "Variables": simplified,
            },
        ),
        args.output,
    )


# ═══════════════════════════════════════════════════════════════════════════
# Subparser registration
# ═══════════════════════════════════════════════════════════════════════════


def register(subparsers):
    """Register all resource query subcommands."""

    def _add(name, help_text, func, extra_args=None):
        p = subparsers.add_parser(name, help=help_text)
        add_common_args(p)
        if extra_args:
            extra_args(p)
        p.set_defaults(func=func, subcommand=name)

    # ── Describe Regions ──────────────────────────────────────────────

    _add("describe_regions", "List available regions", cmd_describe_regions)

    # ── Describe Workspaces ───────────────────────────────────────────

    def _describe_workspaces_args(p):
        p.add_argument("--name", help="Filter by workspace name")
        p.add_argument("--offset", help="Pagination offset (default: 0)")
        p.add_argument("--limit", help="Pagination limit (default: 20)")

    _add(
        "describe_workspaces",
        "List workspaces in a region",
        cmd_describe_workspaces,
        _describe_workspaces_args,
    )

    # ── Describe Clusters ─────────────────────────────────────────────

    def _describe_clusters_args(p):
        p.add_argument("--workspace_name", help="Workspace name to filter clusters")
        p.add_argument("--cluster_ids", help="Comma-separated cluster IDs to query")
        p.add_argument("--offset", help="Pagination offset (default: 0)")
        p.add_argument("--limit", help="Pagination limit (default: 20)")

    _add(
        "describe_clusters",
        "List clusters (optionally filtered by workspace)",
        cmd_describe_clusters,
        _describe_clusters_args,
    )

    # ── Describe Variables ────────────────────────────────────────────

    def _describe_variables_args(p):
        p.add_argument(
            "--workspace_name",
            help="Workspace name (alternative to --workspace_id)",
        )
        p.add_argument(
            "--name",
            help=(
                "Filter variables by name substring (backend does LIKE '%%v%%' "
                "match against the Name column; literal '%%' is rejected, '_' is "
                "auto-escaped)."
            ),
        )

    _add(
        "describe_variables",
        "List workspace variables (for ${var} substitution in SQL WITH clauses)",
        cmd_describe_variables,
        _describe_variables_args,
    )
