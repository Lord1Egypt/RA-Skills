"""NAT 网关迁移插件 — 查询源账号 NAT 网关并在目标账号重建"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field

from .base import MigrationContext, ResourceConfig, ResourcePlugin
from . import register_plugin


# ──────────────────────── Pydantic 配置模型 ────────────────────────
class NatGatewayConfig(BaseModel):
    """单个 NAT 网关迁移配置"""
    source_id: str = Field(default="", description="源 NAT 网关 ID（用于溯源）")
    name: str = Field(..., description="NAT 网关名称")
    vpc_key: str = Field(..., description="关联的 VPC 逻辑名（对应 vpcs 配置的 key）")
    bandwidth: int = Field(default=100, description="带宽上限（Mbps）")
    max_concurrent: int = Field(
        default=1000000,
        description="并发连接数上限",
    )
    tags: dict[str, str] = Field(default_factory=dict, description="标签")


class NatConfig(ResourceConfig):
    """NAT 网关迁移配置（顶层）"""
    gateways: dict[str, NatGatewayConfig] = Field(
        default_factory=dict,
        description="要迁移的 NAT 网关（key 为逻辑名）",
    )


# ──────────────────────── NAT 插件 ────────────────────────
@register_plugin
class NatPlugin(ResourcePlugin):
    RESOURCE_TYPE: ClassVar[str] = "nat"
    DISPLAY_NAME: ClassVar[str] = "NAT 网关"
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

        results: list[dict[str, Any]] = []
        offset = 0
        while True:
            req = vpc_models.DescribeNatGatewaysRequest()
            req.Offset = offset
            req.Limit = 100
            resp = client.DescribeNatGateways(req)
            for nat in resp.NatGatewaySet or []:
                if vpc_ids and nat.VpcId not in vpc_ids:
                    continue
                results.append({
                    "source_id": nat.NatGatewayId,
                    "name": nat.NatGatewayName,
                    "vpc_id": nat.VpcId,
                    "bandwidth": nat.InternetMaxBandwidthOut or 100,
                    "max_concurrent": nat.MaxConcurrentConnection or 1000000,
                    "eip_set": [
                        addr.AddressId for addr in (nat.PublicIpAddressSet or [])
                    ],
                    "state": nat.State,
                })
            if len(resp.NatGatewaySet or []) < 100:
                break
            offset += 100

        return results

    # ── 配置生成 ──
    def build_config(
        self,
        source_resources: list[dict[str, Any]],
        context: MigrationContext,
    ) -> NatConfig:
        gateways: dict[str, NatGatewayConfig] = {}
        for i, res in enumerate(source_resources):
            key = f"nat-{i}"
            vpc_key = context.vpc_id_mapping.get(res["vpc_id"], "default")
            gateways[key] = NatGatewayConfig(
                source_id=res["source_id"],
                name=f"migrated-{res['name']}",
                vpc_key=vpc_key,
                bandwidth=res.get("bandwidth", 100),
                max_concurrent=res.get("max_concurrent", 1000000),
            )
        return NatConfig(gateways=gateways)

    # ── tfvars 渲染 ──
    def render_tfvars(self, config: ResourceConfig) -> str:
        cfg = config if isinstance(config, NatConfig) else NatConfig(**config.model_dump())
        if not cfg.gateways:
            return "nat_gateways = {}\n"

        lines = ["nat_gateways = {"]
        for key, gw in cfg.gateways.items():
            lines.append(f"  {key} = {{")
            lines.append(f'    name           = "{gw.name}"')
            lines.append(f'    vpc_key        = "{gw.vpc_key}"')
            lines.append(f"    bandwidth      = {gw.bandwidth}")
            lines.append(f"    max_concurrent = {gw.max_concurrent}")
            lines.append("  }")
        lines.append("}")
        return "\n".join(lines) + "\n"

    # ── 从 YAML dict 反序列化 ──
    def config_from_dict(self, data: dict[str, Any]) -> NatConfig:
        return NatConfig(**data)
