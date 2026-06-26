#!/usr/bin/env python3
"""
根据查询到的真实账号和 VPC 信息，自动生成 tc-migrate.yaml 配置文件。

用法：
    python -m tc_migrate.tools.generate_config \
        --a-secret-id AKIDxxx --a-secret-key xxx \
        --b-secret-id AKIDyyy --b-secret-key yyy \
        --region ap-guangzhou \
        --output tc-migrate.yaml

功能：
    1. 查询账号A的 UIN 和所有 VPC
    2. 查询账号B的 UIN
    3. 以账号A的每个 VPC 为基础，自动生成迁移配置
    4. 账号B侧的 VPC CIDR 自动分配（172.16.0.0/16 开始递增）
"""

import argparse
import sys

import yaml

from ..models import DEFAULT_TAGS
from .query_account_info import query_account_info
from .query_vpcs import query_vpcs


def auto_generate_config(
    a_secret_id: str,
    a_secret_key: str,
    b_secret_id: str,
    b_secret_key: str,
    region: str = "ap-guangzhou",
) -> dict:
    """根据真实账号信息自动生成配置 dict"""

    # 1. 查询 UIN
    info_a = query_account_info(a_secret_id, a_secret_key)
    info_b = query_account_info(b_secret_id, b_secret_key)

    # 2. 查询账号A 的所有 VPC
    vpcs_a = query_vpcs(a_secret_id, a_secret_key, region)

    if not vpcs_a:
        raise RuntimeError(f"账号A 在 {region} 没有 VPC，无需迁移")

    # 3. 生成配置
    config = {
        "region": region,
        "account_a": {
            "secret_id": a_secret_id,
            "secret_key": a_secret_key,
            "uin": info_a["owner_uin"],
        },
        "account_b": {
            "secret_id": b_secret_id,
            "secret_key": b_secret_key,
            "uin": info_b["owner_uin"],
        },
        "vpcs": {},
        "tags": DEFAULT_TAGS.copy(),
    }

    # 4. 为账号A的每个 VPC 生成迁移配置
    cidr_second_octet = 16  # 从 172.16.0.0/16 开始
    for i, vpc in enumerate(vpcs_a):
        # 生成逻辑名：优先用 VPC 名称，否则用 vpc-0, vpc-1
        vpc_name = vpc["vpc_name"]
        if vpc_name:
            # 清理名称：只保留字母数字和连字符
            key = vpc_name.lower().replace(" ", "-").replace("_", "-")
            # 去掉不合法字符
            key = "".join(c for c in key if c.isalnum() or c == "-").strip("-")
            if not key:
                key = f"vpc-{i}"
        else:
            key = f"vpc-{i}"

        # 账号B侧 CIDR 自动分配
        b_cidr = f"172.{cidr_second_octet}.0.0/16"
        cidr_second_octet += 1

        # 根据账号A的子网结构，生成账号B的子网
        b_subnets = []
        subnet_third_octet = 1
        for s in vpc["subnets"]:
            b_subnets.append({
                "name": f"subnet-{key}-{subnet_third_octet}",
                "cidr": f"172.{cidr_second_octet - 1}.{subnet_third_octet}.0/24",
                "az": s["zone"],
            })
            subnet_third_octet += 1

        # 如果账号A没有子网，创建一个默认子网
        if not b_subnets:
            # 取该地域的第一个可用区
            default_az = f"{region}-3"
            b_subnets.append({
                "name": f"subnet-{key}-default",
                "cidr": f"172.{cidr_second_octet - 1}.1.0/24",
                "az": default_az,
            })

        config["vpcs"][key] = {
            "account_a_vpc_id": vpc["vpc_id"],
            "account_b_vpc_name": f"vpc-b-{key}",
            "account_b_vpc_cidr": b_cidr,
            "account_b_subnets": b_subnets,
            "account_b_sg_name": f"sg-b-{key}",
            "account_b_sg_ingress_cidrs": [b_cidr],
        }

    return config


def main():
    parser = argparse.ArgumentParser(
        description="根据账号A的 VPC 信息自动生成 tc-migrate.yaml 配置文件"
    )
    parser.add_argument("--a-secret-id", required=True, help="账号A SecretId")
    parser.add_argument("--a-secret-key", required=True, help="账号A SecretKey")
    parser.add_argument("--b-secret-id", required=True, help="账号B SecretId")
    parser.add_argument("--b-secret-key", required=True, help="账号B SecretKey")
    parser.add_argument("--region", default="ap-guangzhou", help="地域（默认 ap-guangzhou）")
    parser.add_argument("--output", "-o", default="tc-migrate.yaml", help="输出文件路径")
    parser.add_argument("--force", action="store_true", help="覆盖已存在的文件")
    args = parser.parse_args()

    import os
    if os.path.exists(args.output) and not args.force:
        print(f"❌ 文件已存在: {args.output}，使用 --force 覆盖", file=sys.stderr)
        sys.exit(1)

    try:
        print("🔍 正在查询账号信息和 VPC 列表...")
        config = auto_generate_config(
            args.a_secret_id, args.a_secret_key,
            args.b_secret_id, args.b_secret_key,
            args.region,
        )

        with open(args.output, "w", encoding="utf-8") as f:
            f.write("# ============================================================\n")
            f.write("# tc-migrate.yaml — 由 generate_config 工具自动生成\n")
            f.write("# 方案：VPC Peering（每对 VPC 独立对等连接）\n")
            f.write("# ============================================================\n")
            f.write("# ⚠️ 请检查并按需调整：\n")
            f.write("#   - account_b_vpc_cidr 和 subnet cidr 是否与现有网络冲突\n")
            f.write("#   - 安全组入站 CIDR 是否需要补充账号A VPC 的 CIDR\n")
            f.write("#   - 可用区 az 是否正确\n")
            f.write("# ============================================================\n\n")
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        vpc_count = len(config["vpcs"])
        print(f"✅ 配置文件已生成: {args.output}")
        print(f"   包含 {vpc_count} 组 VPC 迁移配置")
        print(f"\n💡 下一步：")
        print(f"   1. 检查并调整配置: vim {args.output}")
        print(f"   2. 校验配置: tc-migrate config validate -c {args.output}")
        print(f"   3. 预览 tfvars: tc-migrate generate -c {args.output} --preview")
        print(f"   4. 执行迁移: tc-migrate run -c {args.output}")

    except Exception as e:
        print(f"❌ 生成失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
