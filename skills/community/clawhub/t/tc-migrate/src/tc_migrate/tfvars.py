"""Terraform tfvars 生成器 — 将 MigrateConfig 转换为 terraform.tfvars（多 VPC + 共享 CCN + 独立路由表隔离，支持跨地域）"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING

from jinja2 import Environment

if TYPE_CHECKING:
    from .models import MigrateConfig

logger = logging.getLogger(__name__)

# 自定义 Jinja2 环境，注册 ljust 过滤器
_env = Environment(keep_trailing_newline=True)
_env.filters["ljust"] = lambda s, width: str(s).ljust(width)

TFVARS_TEMPLATE = _env.from_string(
    '''\
# ============================================================
# terraform.tfvars — 由 tc-migrate CLI 自动生成，请勿手动修改
# 方案：共享 CCN + 独立路由表（账号B创建CCN，每对VPC一个路由表，实现隔离{% if config.is_cross_region %}，跨地域{% endif %}）
# ============================================================

# ---------- 账号 A 认证（源账号） ----------
account_a_secret_id  = "{{ config.account_a.secret_id }}"
account_a_secret_key = "{{ config.account_a.secret_key }}"

# ---------- 账号 B 认证（目标账号，CCN 所有者） ----------
account_b_secret_id  = "{{ config.account_b.secret_id }}"
account_b_secret_key = "{{ config.account_b.secret_key }}"

# ---------- 账号 UIN ----------
account_a_uin = "{{ config.account_a.uin }}"
account_b_uin = "{{ config.account_b.uin }}"

# ---------- 区域{% if config.is_cross_region %}（跨地域 CCN）{% endif %} ----------
region_a = "{{ config.region_a }}"
region_b = "{{ config.region_b }}"

# ---------- CCN 云联网配置（账号B 创建，所有 VPC pair 共享） ----------
ccn_name                         = "{{ config.ccn_name }}"
ccn_charge_type                  = "{{ config.ccn_charge_type }}"
ccn_qos                          = "{{ config.ccn_qos }}"
ccn_bandwidth_limit_type         = "{{ config.ccn_bandwidth_limit_type }}"
ccn_bandwidth                    = {{ config.ccn_bandwidth }}
configure_cross_region_bandwidth = {{ config.configure_cross_region_bandwidth | lower }}

# ============================================================
# 多 VPC 配置 — 共享 CCN，每对 VPC（A↔B）一个独立的路由表实现隔离
# ============================================================
vpcs = {
{% for vpc_key, vpc in config.vpcs.items() %}
  # ── {{ vpc_key }} ──
  {{ vpc_key }} = {
    account_a_vpc_id         = "{{ vpc.account_a_vpc_id }}"
    account_b_vpc_name       = "{{ vpc.account_b_vpc_name }}"
    account_b_vpc_cidr       = "{{ vpc.account_b_vpc_cidr }}"
    account_b_subnets = [
{% for subnet in vpc.account_b_subnets %}
      { name = "{{ subnet.name }}", cidr = "{{ subnet.cidr }}", az = "{{ subnet.az }}" },
{% endfor %}
    ]
    account_b_sg_name          = "{{ vpc.account_b_sg_name }}"
    account_b_sg_ingress_cidrs = [{% for cidr in vpc.account_b_sg_ingress_cidrs %}"{{ cidr }}"{% if not loop.last %}, {% endif %}{% endfor %}]
  }

{% endfor %}
}

# ---------- 标签 ----------
tags = {
{% for key, value in config.tags.items() %}
  {{ key | ljust(12) }} = "{{ value }}"
{% endfor %}
}
'''
)


def _render_resource_plugins(config: MigrateConfig) -> str:
    """渲染各资源插件（CLB/NAT/CVM/...）的 tfvars 片段"""
    if not config.resources:
        return ""

    from .plugins import get_all_plugins

    parts: list[str] = []
    all_plugins = get_all_plugins()

    for rtype, plugin_data in config.resources.items():
        if rtype not in all_plugins:
            logger.warning("跳过未注册的资源类型: %s", rtype)
            continue

        plugin_cls = all_plugins[rtype]
        plugin = plugin_cls()

        # 检查是否启用
        if isinstance(plugin_data, dict) and not plugin_data.get("enabled", True):
            continue

        # 从 YAML 字典反序列化为配置模型
        plugin_config = plugin.config_from_dict(plugin_data)
        parts.append(f"\n# ── {plugin.DISPLAY_NAME} ──")
        parts.append(plugin.render_tfvars(plugin_config))

    return "\n".join(parts) if parts else ""


def generate_tfvars(config: MigrateConfig, output_path: str | Path) -> Path:
    """根据配置模型生成 terraform.tfvars 文件（支持多资源类型）"""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    # 基础部分：认证 + VPC + CCN
    content = TFVARS_TEMPLATE.render(config=config)

    # 追加各资源插件的 tfvars 片段
    content += _render_resource_plugins(config)

    path.write_text(content, encoding="utf-8")
    return path


def get_tfvars_content(config: MigrateConfig) -> str:
    """返回渲染后的 tfvars 内容（用于预览，支持多资源类型）"""
    content = TFVARS_TEMPLATE.render(config=config)
    content += _render_resource_plugins(config)
    return content
