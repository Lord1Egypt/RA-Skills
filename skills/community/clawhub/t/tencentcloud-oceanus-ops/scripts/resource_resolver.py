#!/usr/bin/env python3
"""Resource parameter resolver for Oceanus CLI.

Provides functions to resolve human-friendly parameters (region names, workspace
names, cluster names) into their canonical IDs required by TencentCloud APIs.

Resolution chain: region -> workspace -> cluster -> version
"""

import sys

from client import call_api, error_response, success_response


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

DEFAULT_REGION = "ap-guangzhou"
DEFAULT_WORKSPACE_NAME = "default"
DEFAULT_FLINK_VERSION = "Flink-1.16"
DEFAULT_JDK_VERSION = "8"

# Cluster status: 2 = running
CLUSTER_STATUS_RUNNING = 2


# ---------------------------------------------------------------------------
# Region Resolver
# ---------------------------------------------------------------------------


def resolve_region(region_input=None, verbose=False):
    """Resolve region parameter to canonical ap-xxx format.

    Args:
        region_input: Region string - can be:
            - None/empty: defaults to ap-guangzhou
            - ap-xxx format: used directly
            - Chinese name (e.g. "广州"): looked up via DescribeRegionZones
            - English description: looked up via DescribeRegionZones
        verbose: Print resolution progress

    Returns:
        dict: {"success": True, "region": "ap-xxx", "region_desc": "..."}
              or error dict on failure
    """
    if not region_input:
        if verbose:
            print("[resolve] 地域未指定，使用默认值: ap-guangzhou", file=sys.stderr)
        return {"success": True, "region": DEFAULT_REGION, "region_desc": "广州"}

    # Already in canonical format
    if region_input.startswith("ap-") or region_input.startswith("na-") or region_input.startswith("eu-"):
        if verbose:
            print(f"[resolve] 地域已是标准格式: {region_input}", file=sys.stderr)
        return {"success": True, "region": region_input, "region_desc": region_input}

    # Need to look up via API
    if verbose:
        print(f"[resolve] 正在查询地域列表，匹配: {region_input}", file=sys.stderr)

    result = call_api("DescribeRegionZones", {}, DEFAULT_REGION)
    if not result.get("success"):
        return result

    data = result.get("data", {})
    net_envs = data.get("NetEnvs", [])

    # Search through all regions
    for net_env in net_envs:
        regions = net_env.get("Regions", [])
        for region_detail in regions:
            region_id = region_detail.get("Region", "")
            region_desc = region_detail.get("RegionDesc", "")

            # Match by Chinese description or English region ID (partial match)
            if (region_input in region_desc
                    or region_input.lower() in region_id.lower()
                    or region_desc == region_input
                    or region_id == region_input):
                if verbose:
                    print(
                        f"[resolve] 地域匹配成功: {region_input} -> {region_id} ({region_desc})",
                        file=sys.stderr,
                    )
                return {
                    "success": True,
                    "region": region_id,
                    "region_desc": region_desc,
                }

    # Not found - list available regions for user reference
    available = []
    for net_env in net_envs:
        for r in net_env.get("Regions", []):
            available.append(f"  {r.get('Region', '')} ({r.get('RegionDesc', '')})")

    return error_response(
        "resolve_region",
        "RegionNotFound",
        f"无法匹配地域 '{region_input}'。可用地域:\n" + "\n".join(available[:20]),
    )


# ---------------------------------------------------------------------------
# Workspace Resolver
# ---------------------------------------------------------------------------


def resolve_workspace(region, workspace_input=None, verbose=False):
    """Resolve workspace parameter to canonical space-xxx format.

    Args:
        region: Resolved region ID (ap-xxx)
        workspace_input: Workspace identifier - can be:
            - None/empty: defaults to looking up "default" workspace
            - space-xxx format: used directly
            - Name string: looked up via DescribeWorkSpaces
        verbose: Print resolution progress

    Returns:
        dict: {"success": True, "workspace_id": "space-xxx", "workspace_name": "...",
               "clusters": [...bound cluster info...]}
              or error dict on failure
    """
    # If already an ID format, use directly but still query to get cluster bindings
    if workspace_input and workspace_input.startswith("space-"):
        if verbose:
            print(f"[resolve] 工作空间已是ID格式: {workspace_input}，查询绑定信息", file=sys.stderr)
        filters = [{"Name": "WorkSpaceId", "Values": [workspace_input]}]
    else:
        # Look up by name
        name = workspace_input if workspace_input else DEFAULT_WORKSPACE_NAME
        if verbose:
            print(f"[resolve] 正在查询工作空间: {name} (地域: {region})", file=sys.stderr)
        filters = [{"Name": "WorkSpaceName", "Values": [name]}]

    params = {
        "Filters": filters,
        "Offset": 0,
        "Limit": 20,
    }

    result = call_api("DescribeWorkSpaces", params, region)
    if not result.get("success"):
        return result

    data = result.get("data", {})
    workspaces = data.get("WorkSpaceSetItem", [])

    if not workspaces:
        search_term = workspace_input if workspace_input else DEFAULT_WORKSPACE_NAME
        return error_response(
            "resolve_workspace",
            "WorkspaceNotFound",
            f"未找到工作空间 '{search_term}' (地域: {region})。"
            f"请确认工作空间名称是否正确，或使用 describe_workspaces 命令查看可用工作空间。",
        )

    # If searching by name, find exact match first, then partial match
    target_name = workspace_input if workspace_input else DEFAULT_WORKSPACE_NAME
    matched = None

    if workspace_input and workspace_input.startswith("space-"):
        # Looking up by ID, should get exactly one
        matched = workspaces[0]
    else:
        # Try exact name match first
        for ws in workspaces:
            if ws.get("WorkSpaceName", "") == target_name:
                matched = ws
                break
        # Fallback to first result if no exact match
        if not matched:
            matched = workspaces[0]

    workspace_id = matched.get("WorkSpaceId") or matched.get("SerialId", "")
    workspace_name = matched.get("WorkSpaceName", "")

    # Extract bound cluster info from workspace response
    clusters = matched.get("ClusterGroupSetItem", [])

    if verbose:
        print(
            f"[resolve] 工作空间解析成功: {workspace_name} -> {workspace_id} "
            f"(绑定集群数: {len(clusters)})",
            file=sys.stderr,
        )

    return {
        "success": True,
        "workspace_id": workspace_id,
        "workspace_name": workspace_name,
        "clusters": clusters,
    }


# ---------------------------------------------------------------------------
# Cluster Resolver
# ---------------------------------------------------------------------------


def resolve_cluster(region, workspace_id, cluster_input=None, min_cu=1, verbose=False):
    """Resolve cluster parameter or list candidates for user selection.

    Args:
        region: Resolved region ID (ap-xxx)
        workspace_id: Resolved workspace ID (space-xxx)
        cluster_input: Cluster identifier - can be:
            - None/empty: list candidates for user selection
            - cluster-xxx format: validate and use directly
            - Name string: match by name from bound clusters
        min_cu: Minimum free CU required (default 1)
        verbose: Print resolution progress

    Returns:
        When cluster_input is specified:
            {"success": True, "cluster_id": "cluster-xxx", "cluster_name": "...",
             "version": {...}, "free_cu": N}

        When cluster_input is NOT specified:
            If candidates exist:
                {"success": True, "needs_selection": True, "candidates": [
                    {"cluster_id": "...", "name": "...", "free_cu": N, "cu_num": N,
                     "status_desc": "...", "version": {...}}, ...
                ]}
            If no candidates:
                error dict with suggestions

    """
    if verbose:
        msg = f"[resolve] 正在查询集群列表 (地域: {region}, 工作空间: {workspace_id})"
        if cluster_input:
            msg += f", 匹配: {cluster_input}"
        print(msg, file=sys.stderr)

    # Query clusters bound to this workspace
    params = {
        "WorkSpaceId": workspace_id,
        "Offset": 0,
        "Limit": 100,
    }

    result = call_api("DescribeClusters", params, region)
    if not result.get("success"):
        return result

    data = result.get("data", {})
    clusters = data.get("ClusterSet", [])

    if not clusters:
        return error_response(
            "resolve_cluster",
            "NoClustersFound",
            f"工作空间 '{workspace_id}' 没有绑定任何集群。\n"
            f"建议: 请在 Oceanus 控制台为该工作空间绑定集群，或切换到其他已绑定集群的工作空间。",
        )

    # If cluster_input is specified, find the matching cluster
    if cluster_input:
        matched = None

        for cluster in clusters:
            cluster_id = cluster.get("ClusterId", "")
            cluster_name = cluster.get("Name", "")

            if cluster_input.startswith("cluster-"):
                if cluster_id == cluster_input:
                    matched = cluster
                    break
            else:
                if cluster_name == cluster_input:
                    matched = cluster
                    break

        if not matched:
            available_names = [
                f"  {c.get('ClusterId', '')} ({c.get('Name', '')})"
                for c in clusters
            ]
            return error_response(
                "resolve_cluster",
                "ClusterNotFound",
                f"在工作空间 '{workspace_id}' 中未找到集群 '{cluster_input}'。\n"
                f"该工作空间绑定的集群:\n" + "\n".join(available_names),
            )

        # Check if cluster is running
        status = matched.get("Status", 0)
        if status != CLUSTER_STATUS_RUNNING:
            status_desc = matched.get("StatusDesc", "unknown")
            return error_response(
                "resolve_cluster",
                "ClusterNotRunning",
                f"集群 '{cluster_input}' 当前状态为 '{status_desc}'，不可用。"
                f"请选择状态为 running 的集群。",
            )

        cluster_id = matched.get("ClusterId", "")
        cluster_name = matched.get("Name", "")
        free_cu = matched.get("FreeCu", 0) or matched.get("FreeCuNum", 0)
        version = matched.get("Version") or {}

        if verbose:
            print(
                f"[resolve] 集群匹配成功: {cluster_name} ({cluster_id}), "
                f"空闲CU: {free_cu}",
                file=sys.stderr,
            )

        return {
            "success": True,
            "cluster_id": cluster_id,
            "cluster_name": cluster_name,
            "free_cu": free_cu,
            "version": version,
        }

    # No cluster_input - list candidates for user selection
    candidates = []
    all_clusters_info = []

    for cluster in clusters:
        cluster_id = cluster.get("ClusterId", "")
        cluster_name = cluster.get("Name", "")
        status = cluster.get("Status", 0)
        status_desc = cluster.get("StatusDesc", "unknown")
        free_cu = cluster.get("FreeCu", 0) or cluster.get("FreeCuNum", 0)
        cu_num = cluster.get("CuNum", 0)
        version = cluster.get("Version") or {}

        all_clusters_info.append({
            "cluster_id": cluster_id,
            "name": cluster_name,
            "status": status,
            "status_desc": status_desc,
            "free_cu": free_cu,
            "cu_num": cu_num,
            "version": version,
        })

        # Filter: running and has enough free CU
        if status == CLUSTER_STATUS_RUNNING and free_cu >= min_cu:
            candidates.append({
                "cluster_id": cluster_id,
                "name": cluster_name,
                "free_cu": free_cu,
                "cu_num": cu_num,
                "status_desc": status_desc,
                "version": version,
            })

    if candidates:
        if verbose:
            print(
                f"[resolve] 找到 {len(candidates)} 个满足条件的候选集群 "
                f"(最低要求: {min_cu} CU)",
                file=sys.stderr,
            )
        return {
            "success": True,
            "needs_selection": True,
            "candidates": candidates,
            "message": (
                f"工作空间 '{workspace_id}' 下有 {len(candidates)} 个可用集群 "
                f"(空闲CU >= {min_cu})，请选择:"
            ),
        }

    # No candidates - provide helpful suggestions
    non_running = [c for c in all_clusters_info if c["status"] != CLUSTER_STATUS_RUNNING]
    low_cu = [
        c for c in all_clusters_info
        if c["status"] == CLUSTER_STATUS_RUNNING and c["free_cu"] < min_cu
    ]

    suggestion_parts = []
    if low_cu:
        low_cu_info = ", ".join(
            f"{c['name']}({c['cluster_id']}, 空闲CU: {c['free_cu']})"
            for c in low_cu
        )
        suggestion_parts.append(
            f"以下集群运行中但空闲CU不足(需要>={min_cu}CU): {low_cu_info}"
        )
    if non_running:
        non_running_info = ", ".join(
            f"{c['name']}({c['cluster_id']}, 状态: {c['status_desc']})"
            for c in non_running
        )
        suggestion_parts.append(f"以下集群状态不可用: {non_running_info}")

    suggestion_parts.append("建议: 1) 切换到其他有空闲资源的工作空间; 2) 为当前工作空间绑定新集群; 3) 对现有集群进行扩容。")

    return error_response(
        "resolve_cluster",
        "NoAvailableCluster",
        f"工作空间 '{workspace_id}' 中没有满足条件的可用集群 (需要空闲CU >= {min_cu})。\n"
        + "\n".join(suggestion_parts),
    )


# ---------------------------------------------------------------------------
# Version Resolver
# ---------------------------------------------------------------------------


def resolve_version(version_info, flink_version=None, jdk_version=None, verbose=False):
    """Resolve Flink and JDK version from cluster version info.

    Args:
        version_info: Version dict from cluster response (may be None/empty)
        flink_version: User-specified Flink version (e.g. "Flink-1.16")
        jdk_version: User-specified JDK version (e.g. "8", "11")
        verbose: Print resolution progress

    Returns:
        dict: {"success": True, "flink_version": "Flink-1.16", "jdk_version": "8",
               "supported_flink": [...], "supported_jdk": [...]}
              or error dict on failure
    """
    if not version_info:
        # No version info from cluster, use defaults
        resolved_flink = flink_version or DEFAULT_FLINK_VERSION
        resolved_jdk = jdk_version or DEFAULT_JDK_VERSION
        if verbose:
            print(
                f"[resolve] 集群无版本信息，使用默认值: {resolved_flink}, JDK {resolved_jdk}",
                file=sys.stderr,
            )
        return {
            "success": True,
            "flink_version": resolved_flink,
            "jdk_version": resolved_jdk,
            "supported_flink": [],
            "supported_jdk": [],
        }

    supported_flink = version_info.get("SupportedFlink", [])
    jdk_support_versions = version_info.get("JdkSupportVersion", [])

    # Resolve Flink version
    resolved_flink = flink_version or DEFAULT_FLINK_VERSION
    if supported_flink and resolved_flink not in supported_flink:
        return error_response(
            "resolve_version",
            "UnsupportedFlinkVersion",
            f"集群不支持 Flink 版本 '{resolved_flink}'。"
            f"支持的版本: {', '.join(supported_flink)}",
        )

    # Resolve JDK version
    resolved_jdk = jdk_version or DEFAULT_JDK_VERSION

    # Find supported JDK versions for the selected Flink version
    supported_jdk = []
    for jdk_entry in jdk_support_versions:
        if jdk_entry.get("FlinkVersion") == resolved_flink:
            supported_jdk = jdk_entry.get("JdkVersions", [])
            break

    if supported_jdk and resolved_jdk not in supported_jdk:
        return error_response(
            "resolve_version",
            "UnsupportedJdkVersion",
            f"Flink {resolved_flink} 不支持 JDK {resolved_jdk}。"
            f"支持的JDK版本: {', '.join(supported_jdk)}",
        )

    if verbose:
        print(
            f"[resolve] 版本解析成功: {resolved_flink}, JDK {resolved_jdk}",
            file=sys.stderr,
        )

    return {
        "success": True,
        "flink_version": resolved_flink,
        "jdk_version": resolved_jdk,
        "supported_flink": supported_flink,
        "supported_jdk": supported_jdk,
    }


# ---------------------------------------------------------------------------
# Orchestration: resolve_all
# ---------------------------------------------------------------------------


def resolve_all(args):
    """Orchestrate the full resolution chain: region -> workspace -> cluster -> version.

    Args:
        args: Namespace with attributes:
            - region: Region input (optional)
            - workspace_id: Workspace input - name or ID (optional)
            - cluster_id: Cluster input - name or ID (optional)
            - flink_version: Flink version (optional)
            - jdk_version: JDK version (optional)
            - verbose: Verbose output flag
            - min_cu: Minimum CU requirement (optional, default 1)

    Returns:
        dict with either:
            - All resolved parameters ready for CreateJob:
              {"success": True, "region": "ap-xxx", "workspace_id": "space-xxx",
               "cluster_id": "cluster-xxx", "flink_version": "...", "jdk_version": "..."}
            - Cluster selection needed:
              {"success": True, "needs_selection": True, "candidates": [...],
               "region": "ap-xxx", "workspace_id": "space-xxx", ...}
            - Error dict on failure
    """
    verbose = getattr(args, "verbose", False)
    min_cu = getattr(args, "min_cu", 1) or 1

    # Step 1: Resolve region
    region_input = getattr(args, "region", None)
    region_result = resolve_region(region_input, verbose=verbose)
    if not region_result.get("success"):
        return region_result

    region = region_result["region"]

    # Step 2: Resolve workspace
    workspace_input = getattr(args, "workspace_id", None) or getattr(args, "workspace_name", None)
    workspace_result = resolve_workspace(region, workspace_input, verbose=verbose)
    if not workspace_result.get("success"):
        return workspace_result

    workspace_id = workspace_result["workspace_id"]
    workspace_name = workspace_result["workspace_name"]

    # Step 3: Resolve cluster
    cluster_input = getattr(args, "cluster_id", None) or getattr(args, "cluster_name", None)
    cluster_result = resolve_cluster(
        region, workspace_id, cluster_input, min_cu=min_cu, verbose=verbose
    )
    if not cluster_result.get("success"):
        return cluster_result

    # If needs_selection, return candidates for user/agent to choose
    if cluster_result.get("needs_selection"):
        cluster_result["region"] = region
        cluster_result["region_desc"] = region_result.get("region_desc", "")
        cluster_result["workspace_id"] = workspace_id
        cluster_result["workspace_name"] = workspace_name
        return cluster_result

    # Step 4: Resolve version
    cluster_id = cluster_result["cluster_id"]
    version_info = cluster_result.get("version", {})
    flink_version = getattr(args, "flink_version", None)
    jdk_version = getattr(args, "jdk_version", None)

    version_result = resolve_version(version_info, flink_version, jdk_version, verbose=verbose)
    if not version_result.get("success"):
        return version_result

    return {
        "success": True,
        "region": region,
        "region_desc": region_result.get("region_desc", ""),
        "workspace_id": workspace_id,
        "workspace_name": workspace_name,
        "cluster_id": cluster_id,
        "cluster_name": cluster_result.get("cluster_name", ""),
        "free_cu": cluster_result.get("free_cu", 0),
        "flink_version": version_result["flink_version"],
        "jdk_version": version_result["jdk_version"],
        "supported_flink": version_result.get("supported_flink", []),
        "supported_jdk": version_result.get("supported_jdk", []),
    }
