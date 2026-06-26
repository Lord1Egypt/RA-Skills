#!/usr/bin/env python3
"""
查询腾讯云指定地域的所有 VPC 及子网信息。

用法：
    python -m tc_migrate.tools.query_vpcs --secret-id AKIDxxx --secret-key xxx --region ap-guangzhou

输出：
    VPC 列表（含 VPC ID、名称、CIDR、子网详情）
"""

import argparse
import json
import sys

from tencentcloud.common import credential
from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models


def query_vpcs(secret_id: str, secret_key: str, region: str) -> list[dict]:
    """查询指定地域所有 VPC 及其子网，返回结构化列表"""
    cred = credential.Credential(secret_id, secret_key)
    client = vpc_client.VpcClient(cred, region)

    # 查询所有 VPC
    req = vpc_models.DescribeVpcsRequest()
    req.Limit = "100"
    resp = client.DescribeVpcs(req)

    results = []
    for v in resp.VpcSet:
        vpc_info = {
            "vpc_id": v.VpcId,
            "vpc_name": v.VpcName,
            "cidr_block": v.CidrBlock,
            "is_default": v.IsDefault,
            "subnets": [],
        }

        # 查询该 VPC 下的子网
        sub_req = vpc_models.DescribeSubnetsRequest()
        sub_req.Filters = [{"Name": "vpc-id", "Values": [v.VpcId]}]
        sub_req.Limit = "100"
        sub_resp = client.DescribeSubnets(sub_req)

        for s in sub_resp.SubnetSet:
            vpc_info["subnets"].append({
                "subnet_id": s.SubnetId,
                "subnet_name": s.SubnetName,
                "cidr_block": s.CidrBlock,
                "zone": s.Zone,
                "available_ip_count": s.AvailableIpAddressCount,
            })

        results.append(vpc_info)

    return results


def print_vpcs(vpcs: list[dict], label: str = ""):
    """格式化打印 VPC 信息"""
    prefix = f"{label} " if label else ""
    print(f"\n{prefix}VPC 列表（共 {len(vpcs)} 个）:")
    print("-" * 70)
    for v in vpcs:
        default_tag = " [默认]" if v["is_default"] else ""
        print(f"\n  VPC: {v['vpc_id']} | {v['vpc_name']}{default_tag}")
        print(f"  CIDR: {v['cidr_block']}")
        if v["subnets"]:
            print(f"  子网（{len(v['subnets'])} 个）:")
            for s in v["subnets"]:
                print(
                    f"    {s['subnet_id']} | {s['subnet_name']} | "
                    f"{s['cidr_block']} | {s['zone']} | "
                    f"可用IP: {s['available_ip_count']}"
                )
        else:
            print("  子网: （无）")


def main():
    parser = argparse.ArgumentParser(description="查询腾讯云 VPC 及子网信息")
    parser.add_argument("--secret-id", required=True, help="SecretId")
    parser.add_argument("--secret-key", required=True, help="SecretKey")
    parser.add_argument("--region", default="ap-guangzhou", help="地域（默认 ap-guangzhou）")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出")
    args = parser.parse_args()

    try:
        vpcs = query_vpcs(args.secret_id, args.secret_key, args.region)
        if args.json:
            print(json.dumps(vpcs, indent=2, ensure_ascii=False))
        else:
            print_vpcs(vpcs, f"[{args.region}]")
    except Exception as e:
        print(f"❌ 查询失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
