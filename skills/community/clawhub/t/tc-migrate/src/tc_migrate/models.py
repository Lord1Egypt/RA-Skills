"""配置数据模型 — 使用 Pydantic v2 进行校验（多 VPC + 共享 CCN + 路由表隔离 + CLB/NAT/CVM，支持跨地域）"""

from __future__ import annotations

import ipaddress
import re
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator
from rich.console import Console

_console = Console()

# 默认 tags — 所有生成配置的地方都应使用此常量
DEFAULT_TAGS = {
    "managed-by": "Terraform",
    "business-id": "cross-account-migration",
    "environment": "migration",
}


# ──────────────────────── 子网 ────────────────────────
class SubnetConfig(BaseModel):
    name: str = Field(..., description="子网名称")
    cidr: str = Field(..., description="子网 CIDR，如 172.16.1.0/24")
    az: str = Field(..., description="可用区，如 ap-guangzhou-3")

    @field_validator("cidr")
    @classmethod
    def validate_cidr(cls, v: str) -> str:
        try:
            ipaddress.ip_network(v, strict=False)
        except ValueError as e:
            raise ValueError(f"无效的 CIDR: {v}") from e
        return v


# ──────────────────────── 单个 VPC 配置 ────────────────────────
class VPCConfig(BaseModel):
    """每个 VPC 的迁移配置"""
    account_a_vpc_id: str = Field(..., description="账号A 已有 VPC ID")
    account_b_vpc_name: str = Field(..., description="账号B 新建 VPC 名称")
    account_b_vpc_cidr: str = Field(..., description="账号B VPC CIDR")
    account_b_subnets: list[SubnetConfig] = Field(
        ..., min_length=1, description="账号B 子网列表"
    )
    account_b_sg_name: str = Field(default="sg-default", description="账号B 安全组名称")
    account_b_sg_ingress_cidrs: list[str] = Field(
        default_factory=list,
        description="账号B 安全组入站 CIDR",
    )
    # 源端 VPC 原始 CIDR（auto_discover 时复制过来的值，分配后保留不变）
    # 用于 allocate_target_cidrs 判断是否需要重新分配及避开哪些网段
    source_vpc_cidr: Optional[str] = Field(
        default=None,
        description="源端 VPC 原始 CIDR（内部使用，YAML 中可省略）",
    )

    @field_validator("account_b_vpc_cidr")
    @classmethod
    def validate_vpc_cidr(cls, v: str) -> str:
        try:
            ipaddress.ip_network(v, strict=False)
        except ValueError as e:
            raise ValueError(f"无效的 VPC CIDR: {v}") from e
        return v

    @field_validator("account_b_sg_ingress_cidrs")
    @classmethod
    def validate_ingress_cidrs(cls, v: list[str]) -> list[str]:
        for cidr in v:
            try:
                ipaddress.ip_network(cidr, strict=False)
            except ValueError as e:
                raise ValueError(f"无效的安全组 CIDR: {cidr}") from e
        return v

    @model_validator(mode="after")
    def subnets_within_vpc(self) -> "VPCConfig":
        """校验子网 CIDR 是否在 VPC CIDR 范围内"""
        vpc_net = ipaddress.ip_network(self.account_b_vpc_cidr, strict=False)
        for subnet in self.account_b_subnets:
            sub_net = ipaddress.ip_network(subnet.cidr, strict=False)
            if not sub_net.subnet_of(vpc_net):
                raise ValueError(
                    f"子网 {subnet.name} 的 CIDR {subnet.cidr} "
                    f"不在 VPC CIDR {self.account_b_vpc_cidr} 范围内"
                )
        return self


# ──────────────────────── 账号认证 ────────────────────────
class AccountAuth(BaseModel):
    secret_id: str = Field(..., description="SecretId")
    secret_key: str = Field(..., description="SecretKey")
    uin: str = Field(default="", description="主账号 UIN（可选，留空则自动通过 API 查询）")

    @field_validator("secret_id")
    @classmethod
    def validate_secret_id(cls, v: str) -> str:
        if not v or len(v) < 10:
            raise ValueError("secret_id 长度不合法")
        return v

    @field_validator("uin")
    @classmethod
    def validate_uin(cls, v: str) -> str:
        if not v:
            return v  # 允许空值，后续通过 API 自动填充
        if not re.match(r"^\d{6,20}$", v):
            raise ValueError(f"UIN 格式不合法: {v}，应为纯数字")
        return v


# ──────────────────────── 腾讯云地域常量 ────────────────────────
VALID_REGIONS = {
    "ap-guangzhou", "ap-shanghai", "ap-beijing", "ap-chengdu",
    "ap-chongqing", "ap-nanjing", "ap-hongkong", "ap-singapore",
    "ap-bangkok", "ap-mumbai", "ap-seoul", "ap-tokyo",
    "na-siliconvalley", "na-ashburn", "eu-frankfurt",
}


# ──────────────────────── 全局配置 ────────────────────────
class MigrateConfig(BaseModel):
    """
    顶层配置，对应 YAML 配置文件（多 VPC + CCN 云联网，支持跨地域）

    🔑 CCN 云联网方案：
    - 每对 VPC (A↔B) 自动创建一个独立的 CCN 实例和路由表
    - 不同 VPC 对使用不同的 CCN，完全隔离（如 prod↔prod 和 dev↔dev）
    - 每个 CCN 有独立的路由表，可以精细化控制流量
    - 支持跨地域（账号A 和 账号B 可在不同地域）
    """

    # ── 区域（支持跨地域）──
    # 向后兼容：如果用户只填 region，则 A/B 同地域
    region: Optional[str] = Field(
        default=None,
        description="资源区域（向后兼容字段，设置后 A/B 使用相同地域）",
    )
    region_a: Optional[str] = Field(
        default=None,
        description="账号A 资源所在区域（跨地域时使用）",
    )
    region_b: Optional[str] = Field(
        default=None,
        description="账号B 资源所在区域（跨地域时使用）",
    )

    # 账号认证
    account_a: AccountAuth = Field(..., description="账号 A（源账号）认证信息")
    account_b: AccountAuth = Field(..., description="账号 B（目标账号）认证信息")

    # 🔑 多 VPC 配置：key 是逻辑名（如 "prod"、"dev"），value 是 VPCConfig
    vpcs: dict[str, VPCConfig] = Field(
        ..., min_length=1, description="要迁移的 VPC 列表（至少一个）"
    )

    # 统一标签
    tags: dict[str, str] = Field(
        default_factory=lambda: DEFAULT_TAGS.copy(),
        description="统一标签",
    )

    # ── CCN 云联网配置（账号B 创建，所有 VPC pair 共享） ──
    ccn_name: str = Field(
        default="ccn-cross-account-migration",
        description="CCN 云联网名称（由账号B创建，所有 VPC pair 共享）",
    )
    ccn_charge_type: str = Field(
        default="PREPAID",
        description=(
            "CCN 计费模式：PREPAID（预付费/包年包月）或 POSTPAID（后付费/按量计费）。"
            "注意：PREPAID 模式只支持 INTER_REGION_LIMIT 限速类型。"
            "部分账号不支持 POSTPAID，默认使用 PREPAID。"
        ),
    )
    ccn_bandwidth: int = Field(
        default=1,
        description="CCN 跨地域带宽上限 (Mbps)，同地域无需设置",
    )
    ccn_qos: str = Field(
        default="AU",
        description="CCN 服务质量等级：PT（铂金）/ AU（金）/ AG（银）",
    )
    ccn_bandwidth_limit_type: str = Field(
        default="INTER_REGION_LIMIT",
        description="CCN 限速类型：OUTER_REGION_LIMIT（地域间限速）/ INTER_REGION_LIMIT（地域出口限速）。PREPAID 模式只支持 INTER_REGION_LIMIT。",
    )
    configure_cross_region_bandwidth: bool = Field(
        default=False,
        description="是否配置跨地域带宽限制（PREPAID 模式不支持动态设置，默认 false）",
    )

    # ── 目标网段：用户指定一个大的 CIDR 块，程序自动拆分给每个 VPC ──
    # 如果设置了此字段，程序会按每个源 VPC 的 CIDR 前缀长度，
    # 从该大网段中依次切出等大的子网段分配给目标 VPC。
    # 例如：target_cidr_block = "172.16.0.0/12"，源端有 /16 的 VPC，
    # 则目标端会分到 172.16.0.0/16、172.17.0.0/16、172.18.0.0/16 等。
    target_cidr_block: Optional[str] = Field(
        default=None,
        description="目标端统一大网段（可选），设置后自动拆分分配给每个 VPC",
    )

    # ── 新增：按产品类型的资源配置（CLB / NAT / CVM / ...）──
    # key 为资源类型（如 "clb"、"nat"、"cvm"），value 为该类型的配置字典
    # 由各 ResourcePlugin.config_from_dict() 负责反序列化
    resources: dict[str, Any] = Field(
        default_factory=dict,
        description="按资源类型组织的迁移配置，key 为资源类型如 clb/nat/cvm",
    )

    @field_validator("target_cidr_block")
    @classmethod
    def validate_target_cidr(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        try:
            net = ipaddress.ip_network(v, strict=False)
        except ValueError as e:
            raise ValueError(f"无效的目标网段: {v}") from e

        # 腾讯云 VPC 只允许 RFC 1918 私有地址范围
        rfc1918_ranges = [
            ipaddress.ip_network("10.0.0.0/8"),
            ipaddress.ip_network("172.16.0.0/12"),
            ipaddress.ip_network("192.168.0.0/16"),
        ]
        is_private = any(net.subnet_of(r) for r in rfc1918_ranges)
        if not is_private:
            raise ValueError(
                f"目标网段 {v} 不在腾讯云 VPC 允许的私有地址范围内。"
                f"仅支持: 10.0.0.0/8、172.16.0.0/12、192.168.0.0/16"
            )
        return v

    @model_validator(mode="after")
    def resolve_regions(self) -> "MigrateConfig":
        """
        解析地域配置，支持三种写法：
        1. 只写 region        → A/B 同地域（向后兼容）
        2. 写 region_a/region_b → 跨地域
        3. 都不写              → 默认 ap-guangzhou
        """
        if self.region_a is None and self.region_b is None:
            # 向后兼容：用 region 字段填充 region_a / region_b
            fallback = self.region or "ap-guangzhou"
            self.region_a = fallback
            self.region_b = fallback
        else:
            # 用户指定了 region_a / region_b
            if self.region_a is None:
                self.region_a = self.region or "ap-guangzhou"
            if self.region_b is None:
                self.region_b = self.region or "ap-guangzhou"

        # 校验地域合法性
        for label, val in [("region_a", self.region_a), ("region_b", self.region_b)]:
            if val not in VALID_REGIONS:
                raise ValueError(
                    f"{label} = '{val}' 不是有效的腾讯云地域。"
                    f"可选值: {', '.join(sorted(VALID_REGIONS))}"
                )
        return self

    @property
    def is_cross_region(self) -> bool:
        """是否为跨地域 CCN"""
        return self.region_a != self.region_b

    # ── 交叉校验：CCN 方案仍需要检查 CIDR 不重叠 ──
    # 同一个 CCN 下不同 VPC 的 CIDR 如果重叠会导致路由冲突
    @model_validator(mode="after")
    def vpc_cidrs_no_overlap(self) -> "MigrateConfig":
        """校验账号B侧所有 VPC CIDR 不重叠（避免路由冲突）"""
        networks: list[tuple[str, ipaddress.IPv4Network]] = []
        for name, vpc in self.vpcs.items():
            net = ipaddress.ip_network(vpc.account_b_vpc_cidr, strict=False)
            for other_name, other_net in networks:
                if net.overlaps(other_net):
                    raise ValueError(
                        f"VPC '{name}' 的 CIDR {vpc.account_b_vpc_cidr} "
                        f"与 VPC '{other_name}' 的 CIDR {other_net} 重叠！"
                        f"同一账号下的 VPC CIDR 不应重叠，否则会导致路由冲突。"
                    )
            networks.append((name, net))
        return self

    # ──────────────────────── 目标网段自动分配 ────────────────────────
    def allocate_target_cidrs(self) -> "MigrateConfig":
        """
        从 target_cidr_block 大网段中，按每个源 VPC 的 CIDR 前缀长度，
        依次切出等大的子网段分配给目标端 VPC。子网也做相应偏移映射。

        **幂等**：通过 source_vpc_cidr 字段记住源端原始 CIDR，
        多次调用不会产生偏移漂移。

        算法：
        1. 将所有 VPC 按源端 CIDR 的前缀长度从小到大排序（先分配大块）
        2. 维护一个"已分配"列表，从大网段中逐一切分
        3. 候选网段不仅不能与已分配的重叠，**还不能与任何源端 VPC CIDR 重叠**
           （VPC Peering 要求两端 CIDR 不能重叠）
        4. 子网按在源 VPC 内的偏移量映射到新 VPC CIDR 内

        本方法会直接修改 self.vpcs 中各 VPC 的 account_b_vpc_cidr 和子网 CIDR，
        以及 account_b_sg_ingress_cidrs。
        """
        if not self.target_cidr_block:
            return self

        target_super = ipaddress.ip_network(self.target_cidr_block, strict=False)

        # ── 第一步：确保 source_vpc_cidr 已记录 ──
        # 首次调用时，account_b_vpc_cidr 就是源端 CIDR（auto_discover 复制的）
        # 后续调用时，account_b_vpc_cidr 已被改写，但 source_vpc_cidr 保留了原值
        for key, vpc in self.vpcs.items():
            if not vpc.source_vpc_cidr:
                vpc.source_vpc_cidr = vpc.account_b_vpc_cidr

        # ── 第二步：还原到源端 CIDR，确保幂等 ──
        # 如果之前已经分配过，先把 VPC CIDR 和子网恢复到源端原始值
        for key, vpc in self.vpcs.items():
            if vpc.account_b_vpc_cidr != vpc.source_vpc_cidr:
                # 反向计算子网偏移：当前子网相对当前 VPC 的偏移 → 还原到源端 VPC 内
                cur_vpc_net = ipaddress.ip_network(vpc.account_b_vpc_cidr, strict=False)
                src_vpc_net = ipaddress.ip_network(vpc.source_vpc_cidr, strict=False)
                for subnet in vpc.account_b_subnets:
                    cur_sub_net = ipaddress.ip_network(subnet.cidr, strict=False)
                    offset = int(cur_sub_net.network_address) - int(cur_vpc_net.network_address)
                    orig_sub_addr = ipaddress.IPv4Address(int(src_vpc_net.network_address) + offset)
                    subnet.cidr = f"{orig_sub_addr}/{cur_sub_net.prefixlen}"
                # 还原安全组入站 CIDR
                cur_vpc_str = str(cur_vpc_net)
                src_vpc_str = str(src_vpc_net)
                vpc.account_b_sg_ingress_cidrs = [
                    src_vpc_str if c == cur_vpc_str else c
                    for c in vpc.account_b_sg_ingress_cidrs
                ]
                vpc.account_b_vpc_cidr = vpc.source_vpc_cidr

        # ── 第三步：收集源端 CIDR ──
        vpc_entries: list[tuple[str, VPCConfig, int]] = []
        source_cidrs: list[ipaddress.IPv4Network] = []
        for key, vpc in self.vpcs.items():
            src_cidr = vpc.source_vpc_cidr or vpc.account_b_vpc_cidr
            source_net = ipaddress.ip_network(src_cidr, strict=False)
            vpc_entries.append((key, vpc, source_net.prefixlen))
            source_cidrs.append(source_net)

        if source_cidrs:
            _console.print(
                f"  [dim]ℹ 源端 VPC CIDR（分配时将避开）: "
                f"{', '.join(str(c) for c in source_cidrs)}[/]"
            )

        # 按前缀长度从小到大排序（大网段先分配），同前缀保持原序
        vpc_entries.sort(key=lambda x: x[2])

        # 按前缀长度分组分配
        allocated: list[ipaddress.IPv4Network] = []

        for vpc_key, vpc, prefix_len in vpc_entries:
            if prefix_len < target_super.prefixlen:
                raise ValueError(
                    f"VPC '{vpc_key}' 的源 CIDR 前缀长度 /{prefix_len} "
                    f"大于目标网段 {self.target_cidr_block} 的 /{target_super.prefixlen}，"
                    f"无法从目标网段中分配。"
                )

            # 在大网段内枚举该前缀长度的所有子网，找到第一个
            # 不与已分配重叠、且不与任何源端 VPC CIDR 重叠的
            assigned_net: ipaddress.IPv4Network | None = None
            for candidate in target_super.subnets(new_prefix=prefix_len):
                # 检查与已分配的目标网段是否重叠
                overlap = False
                for used in allocated:
                    if candidate.overlaps(used):
                        overlap = True
                        break
                if overlap:
                    continue

                # 🔑 检查与所有源端 VPC CIDR 是否重叠（CCN 要求不能重叠）
                source_overlap = False
                for src_cidr in source_cidrs:
                    if candidate.overlaps(src_cidr):
                        source_overlap = True
                        break
                if source_overlap:
                    _console.print(
                        f"  [dim]⏭ 跳过 {candidate}（与源端 CIDR 重叠）[/]"
                    )
                    continue

                assigned_net = candidate
                break

            if assigned_net is None:
                raise ValueError(
                    f"目标网段 {self.target_cidr_block} 空间不足，"
                    f"无法为 VPC '{vpc_key}' 分配 /{prefix_len} 的网段"
                    f"（需避开源端 CIDR 和已分配网段）。"
                    f"已分配 {len(allocated)} 个网段。"
                )

            allocated.append(assigned_net)

            # 计算源端 VPC CIDR
            old_vpc_net = ipaddress.ip_network(vpc.account_b_vpc_cidr, strict=False)
            new_vpc_cidr = str(assigned_net)

            _console.print(
                f"  [green]✓[/] VPC '{vpc_key}': "
                f"{vpc.source_vpc_cidr} → {new_vpc_cidr}"
            )

            # 映射子网：按源子网在源 VPC 内的偏移量映射到新 VPC 内
            for subnet in vpc.account_b_subnets:
                old_sub_net = ipaddress.ip_network(subnet.cidr, strict=False)
                # 计算子网起始地址相对于源 VPC 起始地址的偏移
                offset = int(old_sub_net.network_address) - int(old_vpc_net.network_address)
                new_sub_addr = ipaddress.IPv4Address(int(assigned_net.network_address) + offset)
                new_sub_cidr = f"{new_sub_addr}/{old_sub_net.prefixlen}"

                _console.print(
                    f"    └─ {subnet.name}: {subnet.cidr} → {new_sub_cidr}"
                )
                subnet.cidr = new_sub_cidr

            # 更新 VPC CIDR
            vpc.account_b_vpc_cidr = new_vpc_cidr

            # 更新安全组入站 CIDR（如果之前填的是源 VPC CIDR，则替换）
            old_vpc_cidr_str = str(old_vpc_net)
            vpc.account_b_sg_ingress_cidrs = [
                new_vpc_cidr if c == old_vpc_cidr_str else c
                for c in vpc.account_b_sg_ingress_cidrs
            ]

        return self
