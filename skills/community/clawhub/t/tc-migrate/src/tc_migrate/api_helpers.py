"""API 辅助模块 — 通过密钥自动查询 UIN / VPC / 子网等信息，减少用户手动输入"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from rich.console import Console

from .models import DEFAULT_TAGS

console = Console()


@dataclass
class SubnetInfo:
    """子网信息"""
    subnet_id: str
    name: str
    cidr: str
    zone: str
    available_ip_count: int = 0


@dataclass
class VPCInfo:
    """VPC 信息"""
    vpc_id: str
    name: str
    cidr: str
    is_default: bool = False
    subnets: list[SubnetInfo] = field(default_factory=list)


@dataclass
class AccountInfo:
    """账号查询结果"""
    uin: str
    app_id: str = ""


def _get_credential(secret_id: str, secret_key: str):
    """创建腾讯云 API 凭证"""
    from tencentcloud.common import credential
    return credential.Credential(secret_id, secret_key)


def _get_client_profile(endpoint: str):
    """创建 API 客户端配置"""
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    hp = HttpProfile(endpoint=endpoint)
    return ClientProfile(httpProfile=hp)


def query_account_uin(secret_id: str, secret_key: str) -> AccountInfo:
    """
    通过 SecretId/SecretKey 查询账号 UIN。
    使用 CAM GetUserAppId API。
    """
    from tencentcloud.cam.v20190116 import cam_client, models as cam_models

    cred = _get_credential(secret_id, secret_key)
    cp = _get_client_profile("cam.tencentcloudapi.com")
    client = cam_client.CamClient(cred, "", cp)

    req = cam_models.GetUserAppIdRequest()
    resp = client.GetUserAppId(req)

    return AccountInfo(
        uin=str(resp.OwnerUin),
        app_id=str(resp.Uin),
    )


def query_vpcs(
    secret_id: str,
    secret_key: str,
    region: str,
) -> list[VPCInfo]:
    """
    查询指定地域的所有 VPC 及其子网。
    """
    from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models

    cred = _get_credential(secret_id, secret_key)
    cp = _get_client_profile("vpc.tencentcloudapi.com")
    client = vpc_client.VpcClient(cred, region, cp)

    # 查询 VPC 列表
    req = vpc_models.DescribeVpcsRequest()
    req.Limit = "100"
    resp = client.DescribeVpcs(req)

    vpcs: list[VPCInfo] = []
    for v in resp.VpcSet or []:
        vpc_info = VPCInfo(
            vpc_id=v.VpcId,
            name=v.VpcName,
            cidr=v.CidrBlock,
            is_default=v.IsDefault,
        )
        vpcs.append(vpc_info)

    # 查询每个 VPC 的子网
    for vpc_info in vpcs:
        req2 = vpc_models.DescribeSubnetsRequest()
        f = vpc_models.Filter()
        f.Name = "vpc-id"
        f.Values = [vpc_info.vpc_id]
        req2.Filters = [f]
        req2.Limit = "100"
        resp2 = client.DescribeSubnets(req2)
        for s in resp2.SubnetSet or []:
            vpc_info.subnets.append(SubnetInfo(
                subnet_id=s.SubnetId,
                name=s.SubnetName,
                cidr=s.CidrBlock,
                zone=s.Zone,
                available_ip_count=s.AvailableIpAddressCount or 0,
            ))

    return vpcs


def auto_discover(
    secret_id_a: str,
    secret_key_a: str,
    region_a: str,
    secret_id_b: str,
    secret_key_b: str,
    region_b: str,
    skip_default_vpc: bool = True,
) -> dict:
    """
    全自动发现：只需密钥+地域，返回完整配置字典（可直接传给 MigrateConfig）。

    流程：
    1. 查询两个账号的 UIN
    2. 查询源账号在 region_a 的所有 VPC + 子网
    3. 自动检测 CIDR 冲突，冲突的跳过
    4. 返回完整配置结构
    """
    import ipaddress

    console.print("[dim]  ⏳ 查询源账号 UIN...[/]")
    account_a_info = query_account_uin(secret_id_a, secret_key_a)
    console.print(f"  ✓ 源账号 UIN: {account_a_info.uin}")

    console.print("[dim]  ⏳ 查询目标账号 UIN...[/]")
    account_b_info = query_account_uin(secret_id_b, secret_key_b)
    console.print(f"  ✓ 目标账号 UIN: {account_b_info.uin}")

    console.print(f"[dim]  ⏳ 扫描源账号 {region_a} 的 VPC...[/]")
    all_vpcs = query_vpcs(secret_id_a, secret_key_a, region_a)
    console.print(f"  ✓ 发现 {len(all_vpcs)} 个 VPC")

    # ── 过滤默认 VPC ──
    candidate_vpcs = all_vpcs
    if skip_default_vpc:
        candidate_vpcs = [v for v in all_vpcs if not v.is_default]
        skipped = len(all_vpcs) - len(candidate_vpcs)
        if skipped > 0:
            console.print(f"  [dim]跳过 {skipped} 个默认 VPC[/]")

    # ── 检测 CIDR 冲突，保留无冲突的 ──
    accepted: list[VPCInfo] = []
    skipped_conflict: list[tuple[VPCInfo, str]] = []

    for vpc in candidate_vpcs:
        net = ipaddress.ip_network(vpc.cidr, strict=False)
        conflict_with: Optional[str] = None
        for existing in accepted:
            existing_net = ipaddress.ip_network(existing.cidr, strict=False)
            if net.overlaps(existing_net):
                conflict_with = f"{existing.name}({existing.cidr})"
                break
        if conflict_with:
            skipped_conflict.append((vpc, conflict_with))
        else:
            accepted.append(vpc)

    if skipped_conflict:
        console.print(f"  [yellow]⚠ 跳过 {len(skipped_conflict)} 个 CIDR 冲突的 VPC:[/]")
        for vpc, conflict in skipped_conflict:
            console.print(f"    [dim]{vpc.name}({vpc.cidr}) 与 {conflict} 冲突[/]")

    if not accepted:
        raise ValueError("没有可用的非冲突 VPC，请手动编辑配置文件")

    # ── 地域可用区映射（源地域 → 目标地域）──
    target_azs = _get_target_azs(region_b)

    # ── 构建 VPC 配置 ──
    vpcs_config: dict[str, dict] = {}
    for vpc in accepted:
        # 生成 VPC 逻辑名：清理名称作为 key
        key = _sanitize_key(vpc.name)
        if key in vpcs_config:
            key = f"{key}-{vpc.vpc_id[-4:]}"

        # 映射子网
        b_subnets = []
        for i, sn in enumerate(vpc.subnets):
            # 目标可用区：轮询分配
            target_az = target_azs[i % len(target_azs)] if target_azs else f"{region_b}-6"
            b_subnets.append({
                "name": f"migrated-{sn.name}",
                "cidr": sn.cidr,
                "az": target_az,
            })

        # 如果 VPC 没有子网，创建一个默认子网
        if not b_subnets:
            net = ipaddress.ip_network(vpc.cidr, strict=False)
            # 取第一个 /24 子网
            first_subnet = list(net.subnets(new_prefix=24))[0]
            b_subnets.append({
                "name": f"migrated-{key}-default",
                "cidr": str(first_subnet),
                "az": target_azs[0] if target_azs else f"{region_b}-6",
            })

        vpcs_config[key] = {
            "account_a_vpc_id": vpc.vpc_id,
            "account_b_vpc_name": f"vpc-b-{key}",
            "account_b_vpc_cidr": vpc.cidr,
            "account_b_subnets": b_subnets,
            "account_b_sg_name": f"sg-b-{key}",
            "account_b_sg_ingress_cidrs": [vpc.cidr],
        }

    return {
        "region_a": region_a,
        "region_b": region_b,
        "account_a": {
            "secret_id": secret_id_a,
            "secret_key": secret_key_a,
            "uin": account_a_info.uin,
        },
        "account_b": {
            "secret_id": secret_id_b,
            "secret_key": secret_key_b,
            "uin": account_b_info.uin,
        },
        "vpcs": vpcs_config,
        "tags": DEFAULT_TAGS.copy(),
    }


def auto_fill_uin(config_dict: dict) -> dict:
    """
    如果配置中 uin 为空或为占位符，自动通过 API 查询补全。
    直接修改并返回 config_dict。
    """
    for label, key in [("源账号", "account_a"), ("目标账号", "account_b")]:
        account = config_dict.get(key, {})
        uin = account.get("uin", "")
        if not uin or uin.startswith("<") or uin == "":
            sid = account.get("secret_id", "")
            skey = account.get("secret_key", "")
            if sid and skey:
                console.print(f"[dim]  ⏳ 自动查询{label} UIN...[/]")
                info = query_account_uin(sid, skey)
                account["uin"] = info.uin
                console.print(f"  ✓ {label} UIN: {info.uin}")
    return config_dict


def _sanitize_key(name: str) -> str:
    """将 VPC 名称转为合法的 YAML key"""
    import re
    key = name.lower().strip()
    key = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", key)
    key = key.strip("-")
    return key or "vpc"


def _get_target_azs(region: str) -> list[str]:
    """获取目标地域的常用可用区列表"""
    az_map = {
        "ap-guangzhou": ["ap-guangzhou-6", "ap-guangzhou-7"],
        "ap-shanghai": ["ap-shanghai-4", "ap-shanghai-5"],
        "ap-beijing": ["ap-beijing-6", "ap-beijing-7"],
        "ap-chengdu": ["ap-chengdu-1", "ap-chengdu-2"],
        "ap-chongqing": ["ap-chongqing-1"],
        "ap-nanjing": ["ap-nanjing-1", "ap-nanjing-2", "ap-nanjing-3"],
        "ap-hongkong": ["ap-hongkong-2", "ap-hongkong-3"],
        "ap-singapore": ["ap-singapore-3", "ap-singapore-4"],
    }
    return az_map.get(region, [f"{region}-1", f"{region}-2"])
