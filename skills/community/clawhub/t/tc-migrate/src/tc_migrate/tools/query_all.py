#!/usr/bin/env python3
"""
一键查询两个账号的 UIN + VPC 信息，用于迁移前信息收集。

用法：
    python -m tc_migrate.tools.query_all \
        --a-secret-id AKIDxxx --a-secret-key xxx \
        --b-secret-id AKIDyyy --b-secret-key yyy \
        --region ap-guangzhou

也可以从已有的 tc-migrate.yaml 配置文件读取：
    python -m tc_migrate.tools.query_all --config tc-migrate.yaml
"""

import argparse
import sys

from .query_account_info import query_account_info
from .query_vpcs import query_vpcs, print_vpcs


def main():
    parser = argparse.ArgumentParser(
        description="一键查询两个账号的 UIN 和 VPC 信息（迁移前信息收集）"
    )

    # 方式一：直接指定密钥
    parser.add_argument("--a-secret-id", help="账号A SecretId")
    parser.add_argument("--a-secret-key", help="账号A SecretKey")
    parser.add_argument("--b-secret-id", help="账号B SecretId")
    parser.add_argument("--b-secret-key", help="账号B SecretKey")
    parser.add_argument("--region", default="ap-guangzhou", help="地域（默认 ap-guangzhou）")

    # 方式二：从配置文件读取
    parser.add_argument("--config", "-c", help="从 tc-migrate.yaml 读取密钥")

    args = parser.parse_args()

    # 从配置文件读取
    if args.config:
        import yaml
        with open(args.config, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f)
        a_sid = cfg["account_a"]["secret_id"]
        a_skey = cfg["account_a"]["secret_key"]
        b_sid = cfg["account_b"]["secret_id"]
        b_skey = cfg["account_b"]["secret_key"]
        region = cfg.get("region", args.region)
    else:
        if not all([args.a_secret_id, args.a_secret_key, args.b_secret_id, args.b_secret_key]):
            print("❌ 请指定 --config 或同时提供 --a-secret-id/key 和 --b-secret-id/key", file=sys.stderr)
            sys.exit(1)
        a_sid = args.a_secret_id
        a_skey = args.a_secret_key
        b_sid = args.b_secret_id
        b_skey = args.b_secret_key
        region = args.region

    print("=" * 70)
    print("腾讯云跨账号迁移 — 信息收集")
    print("=" * 70)

    # 1. 查询 UIN
    print("\n📋 账号信息:")
    print("-" * 70)
    try:
        info_a = query_account_info(a_sid, a_skey)
        print(f"  账号A（源）   UIN: {info_a['uin']}  OwnerUin: {info_a['owner_uin']}")
    except Exception as e:
        print(f"  账号A 查询失败: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        info_b = query_account_info(b_sid, b_skey)
        print(f"  账号B（目标） UIN: {info_b['uin']}  OwnerUin: {info_b['owner_uin']}")
    except Exception as e:
        print(f"  账号B 查询失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 2. 查询 VPC
    print(f"\n📡 地域: {region}")

    try:
        vpcs_a = query_vpcs(a_sid, a_skey, region)
        print_vpcs(vpcs_a, "账号A（源）")
    except Exception as e:
        print(f"  账号A VPC 查询失败: {e}", file=sys.stderr)

    try:
        vpcs_b = query_vpcs(b_sid, b_skey, region)
        print_vpcs(vpcs_b, "账号B（目标）")
    except Exception as e:
        print(f"  账号B VPC 查询失败: {e}", file=sys.stderr)

    print("\n" + "=" * 70)
    print("💡 提示：将上方信息填入 tc-migrate.yaml 配置文件")
    print("   account_a.uin / account_b.uin → 使用 OwnerUin")
    print("   vpcs.xxx.account_a_vpc_id     → 使用需要迁移的 VPC ID")
    print("=" * 70)


if __name__ == "__main__":
    main()
