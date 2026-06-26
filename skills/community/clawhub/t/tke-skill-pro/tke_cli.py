#!/usr/bin/env python3
"""
腾讯云 TKE CLI - 轻量级 TKE 集群管理命令行工具

支持通过环境变量或命令行参数传入腾讯云凭证。
依赖：pip install tencentcloud-sdk-python-tke
"""

import argparse
import json
import os
import sys


def get_credentials(args):
    """获取腾讯云凭证（命令行参数优先，环境变量兜底）"""
    secret_id = getattr(args, 'secret_id', None) or os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = getattr(args, 'secret_key', None) or os.getenv("TENCENTCLOUD_SECRET_KEY")
    if not secret_id or not secret_key:
        print("错误：未提供腾讯云凭证。请通过 --secret-id/--secret-key 参数或环境变量 TENCENTCLOUD_SECRET_ID/TENCENTCLOUD_SECRET_KEY 配置。", file=sys.stderr)
        sys.exit(1)
    return secret_id, secret_key


def create_common_client(secret_id, secret_key, region, version="2018-05-25"):
    """创建腾讯云通用客户端"""
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.common_client import CommonClient

    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "tke.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return CommonClient("tke", version, cred, region, profile=client_profile)


def call_api(client, action, params=None):
    """调用 API 并返回解析后的 Response"""
    resp = client.call(action, params or {})
    data = json.loads(resp)
    return data.get("Response", data)


def print_json(data):
    """格式化输出 JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


# ========== 子命令实现 ==========

def cmd_clusters(args):
    """查询集群列表"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {}
    if args.cluster_ids:
        params["ClusterIds"] = args.cluster_ids
    if args.cluster_type:
        params["ClusterType"] = args.cluster_type
    if args.limit is not None:
        params["Limit"] = args.limit
    if args.offset is not None:
        params["Offset"] = args.offset
    result = call_api(client, "DescribeClusters", params)
    print_json(result)


def cmd_cluster_status(args):
    """查询集群状态"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {}
    if args.cluster_ids:
        params["ClusterIds"] = args.cluster_ids
    result = call_api(client, "DescribeClusterStatus", params)
    print_json(result)


def cmd_cluster_level(args):
    """查询集群规格"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {}
    if args.cluster_id:
        params["ClusterID"] = args.cluster_id
    result = call_api(client, "DescribeClusterLevelAttribute", params)
    print_json(result)


def cmd_endpoints(args):
    """查询集群访问地址"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {"ClusterId": args.cluster_id}
    result = call_api(client, "DescribeClusterEndpoints", params)
    print_json(result)


def cmd_endpoint_status(args):
    """查询集群端点状态"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {"ClusterId": args.cluster_id}
    if args.is_extranet:
        params["IsExtranet"] = True
    result = call_api(client, "DescribeClusterEndpointStatus", params)
    print_json(result)


def cmd_kubeconfig(args):
    """获取集群 kubeconfig"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {"ClusterId": args.cluster_id}
    if args.is_extranet:
        params["IsExtranet"] = True
    result = call_api(client, "DescribeClusterKubeconfig", params)
    print_json(result)


def cmd_create_endpoint(args):
    """创建集群访问端点（开启内网/外网访问）"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {"ClusterId": args.cluster_id}
    if args.is_extranet:
        params["IsExtranet"] = True
        if args.security_group:
            params["SecurityGroup"] = args.security_group
    else:
        if args.subnet_id:
            params["SubnetId"] = args.subnet_id
    if args.domain:
        params["Domain"] = args.domain
    if args.existed_lb_id:
        params["ExistedLoadBalancerId"] = args.existed_lb_id
    if args.extensive_parameters:
        params["ExtensiveParameters"] = args.extensive_parameters
    result = call_api(client, "CreateClusterEndpoint", params)
    print_json(result)


def cmd_delete_endpoint(args):
    """删除集群访问端点（关闭内网/外网访问）"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region)
    params = {"ClusterId": args.cluster_id}
    if args.is_extranet:
        params["IsExtranet"] = True
    result = call_api(client, "DeleteClusterEndpoint", params)
    print_json(result)


def cmd_node_pools(args):
    """查询节点池"""
    secret_id, secret_key = get_credentials(args)
    client = create_common_client(secret_id, secret_key, args.region, version="2022-05-01")
    params = {"ClusterId": args.cluster_id}
    if args.limit is not None:
        params["Limit"] = args.limit
    if args.offset is not None:
        params["Offset"] = args.offset
    result = call_api(client, "DescribeNodePools", params)
    print_json(result)



# ========== 主入口 ==========

def main():
    # 公共参数（通过 parents 共享给所有子命令）
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--region", default="ap-guangzhou", help="地域（默认 ap-guangzhou）")
    common_parser.add_argument("--secret-id", dest="secret_id", help="腾讯云 SecretId（优先于环境变量）")
    common_parser.add_argument("--secret-key", dest="secret_key", help="腾讯云 SecretKey（优先于环境变量）")

    parser = argparse.ArgumentParser(
        description="腾讯云 TKE CLI - 轻量级集群管理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python tke_cli.py clusters --region ap-guangzhou
  python tke_cli.py cluster-status --cluster-ids cls-xxx cls-yyy
  python tke_cli.py endpoints --cluster-id cls-xxx --region ap-beijing
  python tke_cli.py kubeconfig --cluster-id cls-xxx
  python tke_cli.py node-pools --cluster-id cls-xxx
"""
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # clusters
    p = subparsers.add_parser("clusters", parents=[common_parser], help="查询集群列表")
    p.add_argument("--cluster-ids", nargs="*", dest="cluster_ids", help="集群ID列表")
    p.add_argument("--cluster-type", dest="cluster_type", choices=["MANAGED_CLUSTER", "INDEPENDENT_CLUSTER"], help="集群类型")
    p.add_argument("--limit", type=int, help="最大返回数量（默认20，最大100）")
    p.add_argument("--offset", type=int, help="偏移量")
    p.set_defaults(func=cmd_clusters)

    # cluster-status
    p = subparsers.add_parser("cluster-status", parents=[common_parser], help="查询集群状态")
    p.add_argument("--cluster-ids", nargs="*", dest="cluster_ids", help="集群ID列表")
    p.set_defaults(func=cmd_cluster_status)

    # cluster-level
    p = subparsers.add_parser("cluster-level", parents=[common_parser], help="查询集群规格")
    p.add_argument("--cluster-id", dest="cluster_id", help="集群ID（查询特定集群可变配规格）")
    p.set_defaults(func=cmd_cluster_level)

    # endpoints
    p = subparsers.add_parser("endpoints", parents=[common_parser], help="查询集群访问地址")
    p.add_argument("--cluster-id", dest="cluster_id", required=True, help="集群ID")
    p.set_defaults(func=cmd_endpoints)

    # endpoint-status
    p = subparsers.add_parser("endpoint-status", parents=[common_parser], help="查询集群端点状态")
    p.add_argument("--cluster-id", dest="cluster_id", required=True, help="集群ID")
    p.add_argument("--is-extranet", dest="is_extranet", action="store_true", help="是否查询外网端点")
    p.set_defaults(func=cmd_endpoint_status)

    # kubeconfig
    p = subparsers.add_parser("kubeconfig", parents=[common_parser], help="获取集群 kubeconfig")
    p.add_argument("--cluster-id", dest="cluster_id", required=True, help="集群ID")
    p.add_argument("--is-extranet", dest="is_extranet", action="store_true", help="是否获取外网 kubeconfig")
    p.set_defaults(func=cmd_kubeconfig)

    # node-pools
    p = subparsers.add_parser("node-pools", parents=[common_parser], help="查询节点池")
    p.add_argument("--cluster-id", dest="cluster_id", required=True, help="集群ID")
    p.add_argument("--limit", type=int, help="最大返回数量")
    p.add_argument("--offset", type=int, help="偏移量")
    p.set_defaults(func=cmd_node_pools)

    # create-endpoint
    p = subparsers.add_parser("create-endpoint", parents=[common_parser], help="开启集群访问端点（内网/外网）")
    p.add_argument("--cluster-id", dest="cluster_id", required=True, help="集群ID")
    p.add_argument("--is-extranet", dest="is_extranet", action="store_true", help="是否开启外网访问（默认开启内网）")
    p.add_argument("--subnet-id", dest="subnet_id", help="子网ID（开启内网时需要，必须为集群所在VPC内的子网）")
    p.add_argument("--security-group", dest="security_group", help="安全组ID（开启外网且不使用已有CLB时必传）")
    p.add_argument("--existed-lb-id", dest="existed_lb_id", help="使用已有CLB的ID")
    p.add_argument("--domain", help="设置域名")
    p.add_argument("--extensive-parameters", dest="extensive_parameters", help='创建LB参数（JSON字符串，仅外网需要），如：\'{"InternetAccessible":{"InternetChargeType":"TRAFFIC_POSTPAID_BY_HOUR","InternetMaxBandwidthOut":200}}\'')
    p.set_defaults(func=cmd_create_endpoint)

    # delete-endpoint
    p = subparsers.add_parser("delete-endpoint", parents=[common_parser], help="关闭集群访问端点（内网/外网）")
    p.add_argument("--cluster-id", dest="cluster_id", required=True, help="集群ID")
    p.add_argument("--is-extranet", dest="is_extranet", action="store_true", help="是否关闭外网访问（默认关闭内网）")
    p.set_defaults(func=cmd_delete_endpoint)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
