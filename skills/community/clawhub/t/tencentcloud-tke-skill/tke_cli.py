#!/usr/bin/env python3
"""
腾讯云 TKE CLI - 轻量级 TKE 集群管理与 TCR 镜像仓库命令行工具

支持通过环境变量或命令行参数传入腾讯云凭证。
依赖：pip install tencentcloud-sdk-python-tke tencentcloud-sdk-python-tcr
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
        print(
            "错误：未提供腾讯云凭证。"
            "请通过 --secret-id/--secret-key 参数"
            "或环境变量 TENCENTCLOUD_SECRET_ID/"
            "TENCENTCLOUD_SECRET_KEY 配置。",
            file=sys.stderr)
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


# ========== TCR 镜像仓库命令 ==========

def create_tcr_client(secret_id, secret_key, region):
    """创建腾讯云 TCR 客户端"""
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.common_client import CommonClient

    cred = credential.Credential(secret_id, secret_key)
    http_profile = HttpProfile()
    http_profile.endpoint = "tcr.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return CommonClient("tcr", "2019-09-24", cred, region, profile=client_profile)


def cmd_tcr_create_instance(args):
    """创建 TCR 实例"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {
        "RegistryName": args.registry_name,
        "RegistryType": args.registry_type,
    }
    if args.charge_type is not None:
        params["RegistryChargeType"] = args.charge_type
    if args.deletion_protection:
        params["DeletionProtection"] = True
    result = call_api(client, "CreateInstance", params)
    print_json(result)


def cmd_tcr_delete_instance(args):
    """删除 TCR 实例"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {"RegistryId": args.registry_id}
    if args.delete_bucket:
        params["DeleteBucket"] = True
    result = call_api(client, "DeleteInstance", params)
    print_json(result)


def cmd_tcr_instances(args):
    """查询 TCR 实例列表"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {}
    if args.instance_name:
        params["Registryname"] = args.instance_name
    if args.limit is not None:
        params["Limit"] = args.limit
    if args.offset is not None:
        params["Offset"] = args.offset
    if args.all_instances:
        params["AllRegion"] = True
    result = call_api(client, "DescribeInstances", params)
    print_json(result)


def cmd_tcr_repos(args):
    """查询镜像仓库列表"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {"RegistryId": args.registry_id}
    if args.namespace_name:
        params["NamespaceName"] = args.namespace_name
    if args.repository_name:
        params["RepositoryName"] = args.repository_name
    if args.limit is not None:
        params["Limit"] = args.limit
    if args.offset is not None:
        params["Offset"] = args.offset
    result = call_api(client, "DescribeRepositories", params)
    print_json(result)


def cmd_tcr_create_repo(args):
    """创建镜像仓库"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {
        "RegistryId": args.registry_id,
        "NamespaceName": args.namespace_name,
        "RepositoryName": args.repository_name,
    }
    if args.brief_description:
        params["BriefDescription"] = args.brief_description
    if args.description:
        params["Description"] = args.description
    result = call_api(client, "CreateRepository", params)
    print_json(result)


def cmd_tcr_delete_repo(args):
    """删除镜像仓库"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {
        "RegistryId": args.registry_id,
        "NamespaceName": args.namespace_name,
        "RepositoryName": args.repository_name,
    }
    result = call_api(client, "DeleteRepository", params)
    print_json(result)


def cmd_tcr_images(args):
    """查询镜像版本列表"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {
        "RegistryId": args.registry_id,
        "NamespaceName": args.namespace_name,
        "RepositoryName": args.repository_name,
    }
    if args.image_version:
        params["ImageVersion"] = args.image_version
    if args.limit is not None:
        params["Limit"] = args.limit
    if args.offset is not None:
        params["Offset"] = args.offset
    result = call_api(client, "DescribeImages", params)
    print_json(result)


def cmd_tcr_namespaces(args):
    """查询 TCR 命名空间列表"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {"RegistryId": args.registry_id}
    if args.namespace_name:
        params["NamespaceName"] = args.namespace_name
    if args.limit is not None:
        params["Limit"] = args.limit
    if args.offset is not None:
        params["Offset"] = args.offset
    result = call_api(client, "DescribeNamespaces", params)
    print_json(result)


def cmd_tcr_create_ns(args):
    """创建 TCR 命名空间"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {
        "RegistryId": args.registry_id,
        "NamespaceName": args.namespace_name,
        "IsPublic": args.is_public,
    }
    result = call_api(client, "CreateNamespace", params)
    print_json(result)


def cmd_tcr_delete_ns(args):
    """删除 TCR 命名空间"""
    secret_id, secret_key = get_credentials(args)
    client = create_tcr_client(secret_id, secret_key, args.region)
    params = {
        "RegistryId": args.registry_id,
        "NamespaceName": args.namespace_name,
    }
    result = call_api(client, "DeleteNamespace", params)
    print_json(result)


# ========== 主入口 ==========

def main():
    # 公共参数（通过 parents 共享给所有子命令）
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--region", default="ap-guangzhou", help="地域（默认 ap-guangzhou）")
    common_parser.add_argument("--secret-id", dest="secret_id", help="腾讯云 SecretId（优先于环境变量）")
    common_parser.add_argument("--secret-key", dest="secret_key", help="腾讯云 SecretKey（优先于环境变量）")

    parser = argparse.ArgumentParser(
        description="腾讯云 TKE CLI - 集群管理与 TCR 镜像仓库工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python tke_cli.py clusters --region ap-guangzhou
  python tke_cli.py cluster-status --cluster-ids cls-xxx cls-yyy
  python tke_cli.py endpoints --cluster-id cls-xxx --region ap-beijing
  python tke_cli.py kubeconfig --cluster-id cls-xxx
  python tke_cli.py node-pools --cluster-id cls-xxx
  python tke_cli.py tcr-instances --region ap-guangzhou
  python tke_cli.py tcr-repos --registry-id tcr-xxx --namespace-name my-ns
  python tke_cli.py tcr-images --registry-id tcr-xxx --namespace-name my-ns --repository-name my-app
"""
    )

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # clusters
    p = subparsers.add_parser("clusters", parents=[common_parser], help="查询集群列表")
    p.add_argument("--cluster-ids", nargs="*", dest="cluster_ids", help="集群ID列表")
    p.add_argument(
        "--cluster-type", dest="cluster_type",
        choices=["MANAGED_CLUSTER", "INDEPENDENT_CLUSTER"],
        help="集群类型")
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
    p.add_argument(
        "--extensive-parameters", dest="extensive_parameters",
        help="创建LB参数（JSON字符串，仅外网需要）")
    p.set_defaults(func=cmd_create_endpoint)

    # delete-endpoint
    p = subparsers.add_parser("delete-endpoint", parents=[common_parser], help="关闭集群访问端点（内网/外网）")
    p.add_argument("--cluster-id", dest="cluster_id", required=True, help="集群ID")
    p.add_argument("--is-extranet", dest="is_extranet", action="store_true", help="是否关闭外网访问（默认关闭内网）")
    p.set_defaults(func=cmd_delete_endpoint)

    # ---- TCR 镜像仓库命令 ----

    # tcr-create-instance
    p = subparsers.add_parser("tcr-create-instance", parents=[common_parser], help="创建 TCR 实例")
    p.add_argument("--registry-name", dest="registry_name", required=True, help="实例名称（如 my-tcr）")
    p.add_argument(
        "--registry-type", dest="registry_type", required=True,
        choices=["basic", "standard", "premium"],
        help="实例类型：basic(基础版), standard(标准版), premium(高级版)")
    p.add_argument("--charge-type", dest="charge_type", type=int, choices=[0, 1], help="计费类型：0=按量计费（默认），1=预付费")
    p.add_argument("--deletion-protection", dest="deletion_protection", action="store_true", help="开启删除保护")
    p.set_defaults(func=cmd_tcr_create_instance)

    # tcr-delete-instance
    p = subparsers.add_parser("tcr-delete-instance", parents=[common_parser], help="删除 TCR 实例")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--delete-bucket", dest="delete_bucket", action="store_true", help="同时删除关联的 COS 存储桶")
    p.set_defaults(func=cmd_tcr_delete_instance)

    # tcr-instances
    p = subparsers.add_parser("tcr-instances", parents=[common_parser], help="查询 TCR 实例列表")
    p.add_argument("--instance-name", dest="instance_name", help="按实例名称筛选")
    p.add_argument("--limit", type=int, help="最大返回数量")
    p.add_argument("--offset", type=int, help="偏移量")
    p.add_argument("--all-instances", dest="all_instances", action="store_true", help="查看所有地域的实例")
    p.set_defaults(func=cmd_tcr_instances)

    # tcr-repos
    p = subparsers.add_parser("tcr-repos", parents=[common_parser], help="查询镜像仓库列表")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--namespace-name", dest="namespace_name", help="命名空间名称")
    p.add_argument("--repository-name", dest="repository_name", help="仓库名称（模糊匹配）")
    p.add_argument("--limit", type=int, help="最大返回数量")
    p.add_argument("--offset", type=int, help="偏移量")
    p.set_defaults(func=cmd_tcr_repos)

    # tcr-create-repo
    p = subparsers.add_parser("tcr-create-repo", parents=[common_parser], help="创建镜像仓库")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--namespace-name", dest="namespace_name", required=True, help="命名空间名称")
    p.add_argument("--repository-name", dest="repository_name", required=True, help="仓库名称")
    p.add_argument("--brief-description", dest="brief_description", help="简短描述")
    p.add_argument("--description", help="详细描述")
    p.set_defaults(func=cmd_tcr_create_repo)

    # tcr-delete-repo
    p = subparsers.add_parser("tcr-delete-repo", parents=[common_parser], help="删除镜像仓库")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--namespace-name", dest="namespace_name", required=True, help="命名空间名称")
    p.add_argument("--repository-name", dest="repository_name", required=True, help="仓库名称")
    p.set_defaults(func=cmd_tcr_delete_repo)

    # tcr-images
    p = subparsers.add_parser("tcr-images", parents=[common_parser], help="查询镜像版本列表")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--namespace-name", dest="namespace_name", required=True, help="命名空间名称")
    p.add_argument("--repository-name", dest="repository_name", required=True, help="仓库名称")
    p.add_argument("--image-version", dest="image_version", help="镜像版本/Tag（模糊匹配）")
    p.add_argument("--limit", type=int, help="最大返回数量")
    p.add_argument("--offset", type=int, help="偏移量")
    p.set_defaults(func=cmd_tcr_images)

    # tcr-namespaces
    p = subparsers.add_parser("tcr-namespaces", parents=[common_parser], help="查询 TCR 命名空间列表")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--namespace-name", dest="namespace_name", help="命名空间名称（模糊匹配）")
    p.add_argument("--limit", type=int, help="最大返回数量")
    p.add_argument("--offset", type=int, help="偏移量")
    p.set_defaults(func=cmd_tcr_namespaces)

    # tcr-create-ns
    p = subparsers.add_parser("tcr-create-ns", parents=[common_parser], help="创建 TCR 命名空间")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--namespace-name", dest="namespace_name", required=True, help="命名空间名称")
    p.add_argument("--is-public", dest="is_public", action="store_true", default=False, help="是否为公开命名空间（默认私有）")
    p.set_defaults(func=cmd_tcr_create_ns)

    # tcr-delete-ns
    p = subparsers.add_parser("tcr-delete-ns", parents=[common_parser], help="删除 TCR 命名空间")
    p.add_argument("--registry-id", dest="registry_id", required=True, help="TCR 实例 ID")
    p.add_argument("--namespace-name", dest="namespace_name", required=True, help="命名空间名称")
    p.set_defaults(func=cmd_tcr_delete_ns)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        args.func(args)
    except KeyboardInterrupt:
        sys.exit(130)
    except (json.JSONDecodeError, OSError, ValueError) as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
