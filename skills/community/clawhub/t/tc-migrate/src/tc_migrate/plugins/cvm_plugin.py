"""CVM（云服务器）迁移插件 — 查询源账号 CVM 并在目标账号重建"""

from __future__ import annotations

from typing import Any, ClassVar

from pydantic import BaseModel, Field

from .base import MigrationContext, ResourceConfig, ResourcePlugin
from . import register_plugin


# ──────────────────────── Pydantic 配置模型 ────────────────────────
class DiskConfig(BaseModel):
    """磁盘配置"""
    type: str = Field(default="CLOUD_PREMIUM", description="磁盘类型")
    size: int = Field(default=50, description="磁盘大小（GB）")


class CvmInstanceConfig(BaseModel):
    """单个 CVM 实例迁移配置"""
    source_id: str = Field(default="", description="源实例 ID（用于溯源）")
    name: str = Field(..., description="实例名称")
    instance_type: str = Field(
        default="S5.MEDIUM4",
        description="实例类型（如 S5.MEDIUM4 = 2C4G）",
    )
    vpc_key: str = Field(..., description="关联的 VPC 逻辑名（对应 vpcs 配置的 key）")
    subnet_index: int = Field(
        default=0,
        description="子网索引（引用 VPC 下第几个子网，从 0 开始）",
    )
    image_id: str = Field(
        default="",
        description="镜像 ID（留空则使用默认公共镜像）",
    )
    az: str = Field(default="", description="可用区（留空则自动选择）")
    system_disk: DiskConfig = Field(
        default_factory=lambda: DiskConfig(type="CLOUD_PREMIUM", size=50),
        description="系统盘配置",
    )
    data_disks: list[DiskConfig] = Field(
        default_factory=list,
        description="数据盘列表",
    )
    instance_charge_type: str = Field(
        default="POSTPAID_BY_HOUR",
        description="计费方式: POSTPAID_BY_HOUR / PREPAID",
    )
    password: str = Field(
        default="",
        description="实例密码（留空则使用密钥对或自动生成）",
    )
    security_group_keys: list[str] = Field(
        default_factory=list,
        description="关联的安全组逻辑 key 列表（引用 sg 配置中的 key，如 sg-0）",
    )
    source_security_group_ids: list[str] = Field(
        default_factory=list,
        description="源实例绑定的安全组 ID（用于溯源）",
    )
    tags: dict[str, str] = Field(default_factory=dict, description="标签")


class CvmConfig(ResourceConfig):
    """CVM 迁移配置（顶层）"""
    instances: dict[str, CvmInstanceConfig] = Field(
        default_factory=dict,
        description="要迁移的 CVM 实例（key 为逻辑名）",
    )
    default_image_id: str = Field(
        default="",
        description="默认镜像 ID（实例未指定时使用）",
    )


# ──────────────────────── CVM 插件 ────────────────────────
@register_plugin
class CvmPlugin(ResourcePlugin):
    RESOURCE_TYPE: ClassVar[str] = "cvm"
    DISPLAY_NAME: ClassVar[str] = "云服务器 CVM"
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
        from tencentcloud.cvm.v20170312 import cvm_client, models as cvm_models

        cred = credential.Credential(secret_id, secret_key)
        hp = HttpProfile(endpoint="cvm.tencentcloudapi.com")
        cp = ClientProfile(httpProfile=hp)
        client = cvm_client.CvmClient(cred, region, cp)

        results: list[dict[str, Any]] = []
        offset = 0
        while True:
            req = cvm_models.DescribeInstancesRequest()
            req.Offset = offset
            req.Limit = 100
            resp = client.DescribeInstances(req)
            for inst in resp.InstanceSet or []:
                vpc_id = inst.VirtualPrivateCloud.VpcId if inst.VirtualPrivateCloud else ""
                if vpc_ids and vpc_id not in vpc_ids:
                    continue
                subnet_id = inst.VirtualPrivateCloud.SubnetId if inst.VirtualPrivateCloud else ""
                # 获取 CVM 绑定的安全组 ID 列表
                sg_ids = list(inst.SecurityGroupIds or []) if hasattr(inst, "SecurityGroupIds") and inst.SecurityGroupIds else []
                results.append({
                    "source_id": inst.InstanceId,
                    "name": inst.InstanceName,
                    "instance_type": inst.InstanceType,
                    "vpc_id": vpc_id,
                    "subnet_id": subnet_id,
                    "az": inst.Placement.Zone if inst.Placement else "",
                    "image_id": inst.ImageId or "",
                    "security_group_ids": sg_ids,
                    "system_disk": {
                        "type": inst.SystemDisk.DiskType if inst.SystemDisk else "CLOUD_PREMIUM",
                        "size": inst.SystemDisk.DiskSize if inst.SystemDisk else 50,
                    },
                    "data_disks": [
                        {"type": dd.DiskType, "size": dd.DiskSize}
                        for dd in (inst.DataDisks or [])
                    ],
                    "state": inst.InstanceState,
                    "cpu": inst.CPU,
                    "memory": inst.Memory,
                })
            if len(resp.InstanceSet or []) < 100:
                break
            offset += 100

        return results

    # ── 配置生成 ──
    def build_config(
        self,
        source_resources: list[dict[str, Any]],
        context: MigrationContext,
    ) -> CvmConfig:
        instances: dict[str, CvmInstanceConfig] = {}
        for i, res in enumerate(source_resources):
            key = f"cvm-{i}"
            vpc_key = context.vpc_id_mapping.get(res["vpc_id"], "default")

            # 将源可用区映射到目标地域（保留 AZ 编号，替换地域前缀）
            source_az = res.get("az", "")
            if source_az and context.region_b:
                # 如 ap-guangzhou-3 → 取最后一段数字
                az_suffix = source_az.rsplit("-", 1)[-1]
                target_az = f"{context.region_b}-{az_suffix}"
            else:
                target_az = ""

            # 映射源安全组 ID → 迁移后的安全组逻辑 key
            source_sg_ids = res.get("security_group_ids", [])
            sg_keys = []
            for sg_id in source_sg_ids:
                if sg_id in context.sg_id_mapping:
                    sg_keys.append(context.sg_id_mapping[sg_id])

            instances[key] = CvmInstanceConfig(
                source_id=res["source_id"],
                name=f"migrated-{res['name']}",
                instance_type=res["instance_type"],
                vpc_key=vpc_key,
                az=target_az,
                image_id=res.get("image_id", ""),
                system_disk=DiskConfig(**res.get("system_disk", {})),
                data_disks=[DiskConfig(**dd) for dd in res.get("data_disks", [])],
                security_group_keys=sg_keys,
                source_security_group_ids=source_sg_ids,
            )
        return CvmConfig(instances=instances)

    # ── tfvars 渲染 ──
    def render_tfvars(self, config: ResourceConfig) -> str:
        cfg = config if isinstance(config, CvmConfig) else CvmConfig(**config.model_dump())
        if not cfg.instances:
            return "cvm_instances = {}\n"

        lines = ["cvm_instances = {"]
        for key, inst in cfg.instances.items():
            lines.append(f"  {key} = {{")
            lines.append(f'    name              = "{inst.name}"')
            lines.append(f'    instance_type     = "{inst.instance_type}"')
            lines.append(f'    vpc_key           = "{inst.vpc_key}"')
            lines.append(f"    subnet_index      = {inst.subnet_index}")
            lines.append(f'    image_id          = "{inst.image_id}"')
            lines.append(f'    az                = "{inst.az}"')
            lines.append(f'    instance_charge_type = "{inst.instance_charge_type}"')
            # security_group_keys
            if inst.security_group_keys:
                sg_keys_str = ", ".join(f'"{k}"' for k in inst.security_group_keys)
                lines.append(f"    security_group_keys = [{sg_keys_str}]")
            else:
                lines.append("    security_group_keys = []")
            # system_disk
            lines.append("    system_disk = {")
            lines.append(f'      type = "{inst.system_disk.type}"')
            lines.append(f"      size = {inst.system_disk.size}")
            lines.append("    }")
            # data_disks
            if inst.data_disks:
                lines.append("    data_disks = [")
                for dd in inst.data_disks:
                    lines.append("      {")
                    lines.append(f'        type = "{dd.type}"')
                    lines.append(f"        size = {dd.size}")
                    lines.append("      },")
                lines.append("    ]")
            else:
                lines.append("    data_disks = []")
            lines.append("  }")
        lines.append("}")
        return "\n".join(lines) + "\n"

    # ── 从 YAML dict 反序列化 ──
    def config_from_dict(self, data: dict[str, Any]) -> CvmConfig:
        return CvmConfig(**data)
