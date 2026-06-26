"""Security Group（安全组）迁移插件 — 查询源账号安全组及规则并在目标账号重建"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field

from .base import MigrationContext, ResourceConfig, ResourcePlugin
from . import register_plugin


# ──────────────────────── Pydantic 配置模型 ────────────────────────
class SgRuleConfig(BaseModel):
    """单条安全组规则配置"""
    action: str = Field(default="ACCEPT", description="规则策略: ACCEPT / DROP")
    direction: str = Field(..., description="方向: ingress / egress")
    protocol: str = Field(default="ALL", description="协议: TCP / UDP / ICMP / ICMPv6 / ALL")
    port: str = Field(default="ALL", description="端口: ALL / 80 / 80-90 / 80,443")
    cidr_block: str = Field(default="", description="IPv4 CIDR（与 source_security_id 互斥）")
    ipv6_cidr_block: str = Field(default="", description="IPv6 CIDR")
    source_security_id: str = Field(
        default="",
        description="引用的安全组 ID（与 cidr_block 互斥）",
    )
    description: str = Field(default="", description="规则描述")


class SgInstanceConfig(BaseModel):
    """单个安全组迁移配置"""
    source_id: str = Field(default="", description="源安全组 ID（用于溯源）")
    name: str = Field(..., description="安全组名称")
    description: str = Field(default="", description="安全组描述")
    vpc_key: str = Field(..., description="关联的 VPC 逻辑名（对应 vpcs 配置的 key）")
    ingress_rules: list[SgRuleConfig] = Field(
        default_factory=list, description="入站规则列表",
    )
    egress_rules: list[SgRuleConfig] = Field(
        default_factory=list, description="出站规则列表",
    )
    tags: dict[str, str] = Field(default_factory=dict, description="标签")


class SgConfig(ResourceConfig):
    """Security Group 迁移配置（顶层）"""
    security_groups: dict[str, SgInstanceConfig] = Field(
        default_factory=dict,
        description="要迁移的安全组（key 为逻辑名）",
    )


def _is_ipv6_only_rule(rule: SgRuleConfig | dict) -> bool:
    """
    判断是否为纯 IPv6 规则（应跳过，因为 CLB 等资源不支持 IPv6 安全组规则）
    
    跳过条件：
    - ICMPv6 协议
    - 或者 cidr_block 为空但 ipv6_cidr_block 不为空
    """
    if isinstance(rule, dict):
        protocol = rule.get("protocol", "").upper()
        cidr = rule.get("cidr_block", "")
        ipv6_cidr = rule.get("ipv6_cidr_block", "")
    else:
        protocol = (rule.protocol or "").upper()
        cidr = rule.cidr_block or ""
        ipv6_cidr = rule.ipv6_cidr_block or ""
    
    # ICMPv6 协议直接跳过
    if protocol == "ICMPV6":
        return True
    
    # 纯 IPv6 CIDR 规则跳过
    if not cidr and ipv6_cidr:
        return True
    
    return False


# ──────────────────────── SG 插件 ────────────────────────
@register_plugin
class SgPlugin(ResourcePlugin):
    RESOURCE_TYPE: ClassVar[str] = "sg"
    DISPLAY_NAME: ClassVar[str] = "安全组 Security Group"
    DEPENDS_ON: ClassVar[list[str]] = ["vpc"]

    # ── 查询 ──
    def query_resources(
        self,
        secret_id: str,
        secret_key: str,
        region: str,
        vpc_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        from tencentcloud.common import credential
        from tencentcloud.common.profile.client_profile import ClientProfile
        from tencentcloud.common.profile.http_profile import HttpProfile
        from tencentcloud.vpc.v20170312 import vpc_client, models as vpc_models

        cred = credential.Credential(secret_id, secret_key)
        hp = HttpProfile(endpoint="vpc.tencentcloudapi.com")
        cp = ClientProfile(httpProfile=hp)
        client = vpc_client.VpcClient(cred, region, cp)

        # ── Step 1: 查询安全组列表 ──
        all_sgs: list[dict[str, Any]] = []
        offset = 0
        while True:
            req = vpc_models.DescribeSecurityGroupsRequest()
            req.Offset = str(offset)
            req.Limit = "100"
            resp = client.DescribeSecurityGroups(req)
            for sg in resp.SecurityGroupSet or []:
                all_sgs.append({
                    "source_id": sg.SecurityGroupId,
                    "name": sg.SecurityGroupName,
                    "description": sg.SecurityGroupDesc or "",
                    "is_default": sg.IsDefault,
                    "tags": {
                        tag.TagKey: tag.TagValue
                        for tag in (sg.TagSet or [])
                    },
                    "ingress_rules": [],
                    "egress_rules": [],
                })
            if len(resp.SecurityGroupSet or []) < 100:
                break
            offset += 100

        # ── Step 2: 如果指定了 vpc_ids，过滤出与这些 VPC 关联的安全组 ──
        if vpc_ids:
            associated_sg_ids: set[str] = set()
            # 查询各 VPC 中网卡绑定的安全组
            for vpc_id in vpc_ids:
                try:
                    eni_req = vpc_models.DescribeNetworkInterfacesRequest()
                    f = vpc_models.Filter()
                    f.Name = "vpc-id"
                    f.Values = [vpc_id]
                    eni_req.Filters = [f]
                    eni_req.Limit = 100
                    eni_resp = client.DescribeNetworkInterfaces(eni_req)
                    for eni in eni_resp.NetworkInterfaceSet or []:
                        for sg_id in eni.GroupSet or []:
                            associated_sg_ids.add(sg_id)
                except Exception:
                    pass  # 查询失败不阻塞，继续

            if associated_sg_ids:
                all_sgs = [
                    sg for sg in all_sgs
                    if sg["source_id"] in associated_sg_ids
                ]

        # ── Step 3: 查询每个安全组的规则 ──
        for sg_item in all_sgs:
            try:
                rule_req = vpc_models.DescribeSecurityGroupPoliciesRequest()
                rule_req.SecurityGroupId = sg_item["source_id"]
                rule_resp = client.DescribeSecurityGroupPolicies(rule_req)
                policy_set = rule_resp.SecurityGroupPolicySet
                if policy_set:
                    # 入站规则
                    for rule in policy_set.Ingress or []:
                        sg_item["ingress_rules"].append(
                            _parse_policy(rule, "ingress")
                        )
                    # 出站规则
                    for rule in policy_set.Egress or []:
                        sg_item["egress_rules"].append(
                            _parse_policy(rule, "egress")
                        )
            except Exception:
                pass  # 查询规则失败不阻塞

        # ── Step 4: 标记 VPC 关联（用于 build_config 的 vpc_key 映射）──
        # 安全组本身不直接关联 VPC，通过 ENI 间接关联。
        # 这里记录每个 SG 关联的 VPC IDs 供后续使用。
        if vpc_ids:
            sg_vpc_map: dict[str, set[str]] = {}
            for vpc_id in vpc_ids:
                try:
                    eni_req = vpc_models.DescribeNetworkInterfacesRequest()
                    f = vpc_models.Filter()
                    f.Name = "vpc-id"
                    f.Values = [vpc_id]
                    eni_req.Filters = [f]
                    eni_req.Limit = 100
                    eni_resp = client.DescribeNetworkInterfaces(eni_req)
                    for eni in eni_resp.NetworkInterfaceSet or []:
                        for sg_id in eni.GroupSet or []:
                            sg_vpc_map.setdefault(sg_id, set()).add(vpc_id)
                except Exception:
                    pass
            for sg_item in all_sgs:
                sg_item["vpc_ids"] = list(
                    sg_vpc_map.get(sg_item["source_id"], set())
                )
        else:
            for sg_item in all_sgs:
                sg_item["vpc_ids"] = []

        return all_sgs

    # ── 配置生成 ──
    def build_config(
        self,
        source_resources: list[dict[str, Any]],
        context: MigrationContext,
    ) -> SgConfig:
        security_groups: dict[str, SgInstanceConfig] = {}
        for i, res in enumerate(source_resources):
            key = f"sg-{i}"

            # 确定关联的 vpc_key
            associated_vpc_ids = res.get("vpc_ids", [])
            if associated_vpc_ids:
                # 取第一个匹配的 vpc_key
                vpc_key = context.vpc_id_mapping.get(
                    associated_vpc_ids[0], "default"
                )
            else:
                vpc_key = "default"

            # 转换入站规则（过滤掉纯 IPv6 规则）
            ingress_rules = [
                SgRuleConfig(
                    action=r.get("action", "ACCEPT"),
                    direction="ingress",
                    protocol=r.get("protocol", "ALL"),
                    port=r.get("port", "ALL"),
                    cidr_block=r.get("cidr_block", ""),
                    ipv6_cidr_block=r.get("ipv6_cidr_block", ""),
                    source_security_id=r.get("source_security_id", ""),
                    description=r.get("description", ""),
                )
                for r in res.get("ingress_rules", [])
                if not _is_ipv6_only_rule(r)
            ]

            # 转换出站规则（过滤掉纯 IPv6 规则）
            egress_rules = [
                SgRuleConfig(
                    action=r.get("action", "ACCEPT"),
                    direction="egress",
                    protocol=r.get("protocol", "ALL"),
                    port=r.get("port", "ALL"),
                    cidr_block=r.get("cidr_block", ""),
                    ipv6_cidr_block=r.get("ipv6_cidr_block", ""),
                    source_security_id=r.get("source_security_id", ""),
                    description=r.get("description", ""),
                )
                for r in res.get("egress_rules", [])
                if not _is_ipv6_only_rule(r)
            ]

            security_groups[key] = SgInstanceConfig(
                source_id=res["source_id"],
                name=f"migrated-{res['name']}",
                description=res.get("description", ""),
                vpc_key=vpc_key,
                ingress_rules=ingress_rules,
                egress_rules=egress_rules,
                tags=res.get("tags", {}),
            )

            # 将 source_sg_id → 逻辑 sg_key 写入上下文，供 CVM/CLB 插件引用
            context.sg_id_mapping[res["source_id"]] = key

        return SgConfig(security_groups=security_groups)

    # ── tfvars 渲染 ──
    def render_tfvars(self, config: ResourceConfig) -> str:
        cfg = config if isinstance(config, SgConfig) else SgConfig(**config.model_dump())
        if not cfg.security_groups:
            return "security_groups = {}\n"

        lines = ["security_groups = {"]
        for key, sg in cfg.security_groups.items():
            lines.append(f"  {key} = {{")
            lines.append(f'    name        = "{sg.name}"')
            lines.append(f'    description = "{sg.description}"')
            lines.append(f'    vpc_key     = "{sg.vpc_key}"')

            # 入站规则（过滤掉纯 IPv6 规则）
            ipv4_ingress = [r for r in sg.ingress_rules if not _is_ipv6_only_rule(r)]
            if ipv4_ingress:
                lines.append("    ingress_rules = [")
                for rule in ipv4_ingress:
                    lines.append("      {")
                    lines.append(f'        action     = "{rule.action}"')
                    lines.append(f'        protocol   = "{rule.protocol}"')
                    lines.append(f'        port       = "{rule.port}"')
                    lines.append(f'        cidr_block = "{rule.cidr_block}"')
                    if rule.ipv6_cidr_block:
                        lines.append(f'        ipv6_cidr_block = "{rule.ipv6_cidr_block}"')
                    if rule.source_security_id:
                        lines.append(f'        source_security_id = "{rule.source_security_id}"')
                    if rule.description:
                        lines.append(f'        description = "{rule.description}"')
                    lines.append("      },")
                lines.append("    ]")
            else:
                lines.append("    ingress_rules = []")

            # 出站规则（过滤掉纯 IPv6 规则）
            ipv4_egress = [r for r in sg.egress_rules if not _is_ipv6_only_rule(r)]
            if ipv4_egress:
                lines.append("    egress_rules = [")
                for rule in ipv4_egress:
                    lines.append("      {")
                    lines.append(f'        action     = "{rule.action}"')
                    lines.append(f'        protocol   = "{rule.protocol}"')
                    lines.append(f'        port       = "{rule.port}"')
                    lines.append(f'        cidr_block = "{rule.cidr_block}"')
                    if rule.ipv6_cidr_block:
                        lines.append(f'        ipv6_cidr_block = "{rule.ipv6_cidr_block}"')
                    if rule.source_security_id:
                        lines.append(f'        source_security_id = "{rule.source_security_id}"')
                    if rule.description:
                        lines.append(f'        description = "{rule.description}"')
                    lines.append("      },")
                lines.append("    ]")
            else:
                lines.append("    egress_rules = []")

            lines.append("  }")
        lines.append("}")
        return "\n".join(lines) + "\n"

    # ── 从 YAML dict 反序列化 ──
    def config_from_dict(self, data: dict[str, Any]) -> SgConfig:
        return SgConfig(**data)


# ──────────────────────── 辅助函数 ────────────────────────
def _parse_policy(rule: Any, direction: str) -> dict[str, str]:
    """将 SDK 返回的 SecurityGroupPolicy 对象解析为字典"""
    return {
        "action": getattr(rule, "Action", "ACCEPT") or "ACCEPT",
        "direction": direction,
        "protocol": getattr(rule, "Protocol", "ALL") or "ALL",
        "port": getattr(rule, "Port", "ALL") or "ALL",
        "cidr_block": getattr(rule, "CidrBlock", "") or "",
        "ipv6_cidr_block": getattr(rule, "Ipv6CidrBlock", "") or "",
        "source_security_id": getattr(rule, "SecurityGroupId", "") or "",
        "description": getattr(rule, "PolicyDescription", "") or "",
    }
