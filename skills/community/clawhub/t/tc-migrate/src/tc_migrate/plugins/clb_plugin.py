"""CLB（负载均衡）迁移插件 — 查询源账号 CLB 并在目标账号重建"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field

from .base import MigrationContext, ResourceConfig, ResourcePlugin
from . import register_plugin


# ──────────────────────── Pydantic 配置模型 ────────────────────────
class ClbListenerConfig(BaseModel):
    """CLB 监听器配置"""
    protocol: str = Field(default="TCP", description="协议: TCP / UDP / HTTP / HTTPS")
    port: int = Field(..., description="监听端口")
    backend_port: int = Field(default=0, description="后端端口（0 表示同端口转发）")
    health_check_enabled: bool = Field(default=True, description="是否开启健康检查")


class ClbInstanceConfig(BaseModel):
    """单个 CLB 实例迁移配置"""
    source_id: str = Field(default="", description="源 CLB ID（用于溯源）")
    name: str = Field(..., description="CLB 名称")
    load_balancer_type: str = Field(
        default="OPEN",
        description="CLB 类型: OPEN（公网）/ INTERNAL（内网）",
    )
    vpc_key: str = Field(..., description="关联的 VPC 逻辑名（对应 vpcs 配置的 key）")
    subnet_key: str = Field(
        default="",
        description="关联的子网 key（内网 CLB 时需要）",
    )
    listeners: list[ClbListenerConfig] = Field(
        default_factory=list, description="监听器列表",
    )
    security_group_keys: list[str] = Field(
        default_factory=list,
        description="关联的安全组逻辑 key 列表（引用 sg 配置中的 key，如 sg-0）",
    )
    source_security_group_ids: list[str] = Field(
        default_factory=list,
        description="源 CLB 绑定的安全组 ID（用于溯源）",
    )
    tags: dict[str, str] = Field(default_factory=dict, description="标签")


class ClbConfig(ResourceConfig):
    """CLB 迁移配置（顶层）"""
    instances: dict[str, ClbInstanceConfig] = Field(
        default_factory=dict,
        description="要迁移的 CLB 实例（key 为逻辑名）",
    )


# ──────────────────────── CLB 插件 ────────────────────────
@register_plugin
class ClbPlugin(ResourcePlugin):
    RESOURCE_TYPE: ClassVar[str] = "clb"
    DISPLAY_NAME: ClassVar[str] = "负载均衡 CLB"
    DEPENDS_ON: ClassVar[list[str]] = ["vpc", "sg"]

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
        from tencentcloud.clb.v20180317 import clb_client, models as clb_models

        cred = credential.Credential(secret_id, secret_key)
        hp = HttpProfile(endpoint="clb.tencentcloudapi.com")
        cp = ClientProfile(httpProfile=hp)
        client = clb_client.ClbClient(cred, region, cp)

        results: list[dict[str, Any]] = []
        offset = 0
        while True:
            req = clb_models.DescribeLoadBalancersRequest()
            req.Offset = offset
            req.Limit = 100
            resp = client.DescribeLoadBalancers(req)
            for lb in resp.LoadBalancerSet or []:
                if vpc_ids and lb.VpcId not in vpc_ids:
                    continue
                # 获取 CLB 绑定的安全组 ID 列表
                sg_ids = list(lb.SecureGroups or []) if hasattr(lb, "SecureGroups") and lb.SecureGroups else []
                results.append({
                    "source_id": lb.LoadBalancerId,
                    "name": lb.LoadBalancerName,
                    "type": lb.LoadBalancerType,  # OPEN / INTERNAL
                    "vpc_id": lb.VpcId,
                    "subnet_id": lb.SubnetId or "",
                    "vips": lb.LoadBalancerVips or [],
                    "status": lb.Status,
                    "security_group_ids": sg_ids,
                })
            if len(resp.LoadBalancerSet or []) < 100:
                break
            offset += 100

        # 查询每个 CLB 的监听器
        for item in results:
            req = clb_models.DescribeListenersRequest()
            req.LoadBalancerId = item["source_id"]
            resp = client.DescribeListeners(req)
            item["listeners"] = [
                {
                    "protocol": lis.Protocol,
                    "port": lis.Port,
                    "listener_name": lis.ListenerName,
                }
                for lis in (resp.Listeners or [])
            ]

        return results

    # ── 配置生成 ──
    def build_config(
        self,
        source_resources: list[dict[str, Any]],
        context: MigrationContext,
    ) -> ClbConfig:
        instances: dict[str, ClbInstanceConfig] = {}
        for i, res in enumerate(source_resources):
            key = f"clb-{i}"
            vpc_key = context.vpc_id_mapping.get(res["vpc_id"], "default")
            listeners = [
                ClbListenerConfig(protocol=lis["protocol"], port=lis["port"])
                for lis in res.get("listeners", [])
            ]

            # 映射源安全组 ID → 迁移后的安全组逻辑 key
            source_sg_ids = res.get("security_group_ids", [])
            sg_keys = []
            for sg_id in source_sg_ids:
                if sg_id in context.sg_id_mapping:
                    sg_keys.append(context.sg_id_mapping[sg_id])

            instances[key] = ClbInstanceConfig(
                source_id=res["source_id"],
                name=f"migrated-{res['name']}",
                load_balancer_type=res["type"],
                vpc_key=vpc_key,
                listeners=listeners,
                security_group_keys=sg_keys,
                source_security_group_ids=source_sg_ids,
            )
        return ClbConfig(instances=instances)

    # ── tfvars 渲染 ──
    def render_tfvars(self, config: ResourceConfig) -> str:
        cfg = config if isinstance(config, ClbConfig) else ClbConfig(**config.model_dump())
        if not cfg.instances:
            return "clb_instances = {}\n"

        lines = ["clb_instances = {"]
        for key, inst in cfg.instances.items():
            lines.append(f"  {key} = {{")
            lines.append(f'    name               = "{inst.name}"')
            lines.append(f'    load_balancer_type = "{inst.load_balancer_type}"')
            lines.append(f'    vpc_key            = "{inst.vpc_key}"')
            lines.append(f'    subnet_key         = "{inst.subnet_key}"')
            # security_group_keys
            if inst.security_group_keys:
                sg_keys_str = ", ".join(f'"{k}"' for k in inst.security_group_keys)
                lines.append(f"    security_group_keys = [{sg_keys_str}]")
            else:
                lines.append("    security_group_keys = []")
            if inst.listeners:
                lines.append("    listeners = [")
                for lis in inst.listeners:
                    lines.append("      {")
                    lines.append(f'        protocol    = "{lis.protocol}"')
                    lines.append(f"        port        = {lis.port}")
                    lines.append(f"        backend_port = {lis.backend_port}")
                    lines.append("      },")
                lines.append("    ]")
            else:
                lines.append("    listeners = []")
            lines.append("  }")
        lines.append("}")
        return "\n".join(lines) + "\n"

    # ── 从 YAML dict 反序列化 ──
    def config_from_dict(self, data: dict[str, Any]) -> ClbConfig:
        return ClbConfig(**data)
