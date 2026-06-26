"""
资源迁移插件基类 — 定义每种产品迁移所需的标准接口

每种产品（CLB / NAT / CVM / ...）只需继承 ResourcePlugin 并实现所有抽象方法，
即可自动接入 CLI、tfvars 生成、Terraform 模块等全套工具链。
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, ClassVar

from pydantic import BaseModel, Field


# ──────────────────────── 资源配置基类 ────────────────────────
class ResourceConfig(BaseModel):
    """每种资源插件的配置基类，可被各插件扩展"""
    enabled: bool = Field(default=True, description="是否启用该资源迁移")


# ──────────────────────── 迁移上下文 ────────────────────────
class MigrationContext:
    """
    迁移上下文 — 在插件间传递共享状态。
    当一个插件完成查询 / 创建后，可将结果写入此上下文供后续插件使用。
    """

    def __init__(
        self,
        region_a: str,
        region_b: str,
        vpc_id_mapping: dict[str, str] | None = None,
    ):
        self.region_a = region_a
        self.region_b = region_b
        # source_vpc_id → 逻辑 vpc_key（如 "prod"）
        self.vpc_id_mapping: dict[str, str] = vpc_id_mapping or {}
        # 逻辑 vpc_key → 子网 ID 列表
        self.subnet_id_mapping: dict[str, list[str]] = {}
        # source_sg_id → 逻辑 sg_key（如 "sg-0"）
        # 由 SG 插件 build_config 后填充，供 CVM/CLB 插件引用
        self.sg_id_mapping: dict[str, str] = {}
        # plugin_type → 该插件的中间输出
        self.resource_outputs: dict[str, dict[str, Any]] = {}


# ──────────────────────── 插件基类 ────────────────────────
class ResourcePlugin(ABC):
    """
    资源迁移插件抽象基类。

    子类必须覆盖以下类变量：
        RESOURCE_TYPE   — 资源类型标识（如 "clb", "nat", "cvm"）
        DISPLAY_NAME    — 资源显示名称（如 "负载均衡 CLB"）
        DEPENDS_ON      — 依赖的其他资源类型（列表）

    子类必须实现以下方法：
        query_resources   — 查询源账号中的资源列表
        build_config      — 将查询结果转换为配置模型
        render_tfvars     — 将配置渲染为 terraform.tfvars 片段
    """

    # ── 子类必须覆盖的元数据 ──
    RESOURCE_TYPE: ClassVar[str]
    DISPLAY_NAME: ClassVar[str]
    DEPENDS_ON: ClassVar[list[str]] = []

    # ── 查询：从源账号读取资源 ──
    @abstractmethod
    def query_resources(
        self,
        secret_id: str,
        secret_key: str,
        region: str,
        vpc_ids: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        """
        查询源账号中的资源列表。

        Args:
            secret_id:  源账号 SecretId
            secret_key: 源账号 SecretKey
            region:     源账号资源所在地域
            vpc_ids:    如果需要按 VPC 过滤，传入 VPC ID 列表

        Returns:
            资源字典列表，每项的字段由子类定义
        """
        ...

    # ── 配置生成：根据查询结果生成配置模型 ──
    @abstractmethod
    def build_config(
        self,
        source_resources: list[dict[str, Any]],
        context: MigrationContext,
    ) -> ResourceConfig:
        """将查询到的源资源转换为目标端配置模型"""
        ...

    # ── tfvars 渲染：生成该资源的 terraform.tfvars 片段 ──
    @abstractmethod
    def render_tfvars(self, config: ResourceConfig) -> str:
        """将配置模型渲染为 terraform.tfvars HCL 片段"""
        ...

    # ── 可选：从 YAML dict 恢复配置 ──
    def config_from_dict(self, data: dict[str, Any]) -> ResourceConfig:
        """
        从 YAML 配置字典反序列化为 ResourceConfig 子类实例。
        默认实现：直接用 ResourceConfig 构造，子类可覆盖。
        """
        return ResourceConfig(**data)
