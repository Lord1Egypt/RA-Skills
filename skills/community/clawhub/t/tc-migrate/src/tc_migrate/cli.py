"""tc-migrate CLI — 腾讯云跨账号资源迁移命令行工具（VPC + CLB + NAT + CVM，可扩展插件架构）"""

from __future__ import annotations

import click

from . import __version__
from .commands import (
    register_config,
    register_generate,
    register_plugins,
    register_run,
    register_scan,
    register_tf,
)


@click.group()
@click.version_option(__version__, prog_name="tc-migrate")
def cli():
    """
    🚀 tc-migrate — 腾讯云跨账号资源迁移 CLI 工具

    将腾讯云账号 A 的 VPC / CLB / NAT / CVM 等资源迁移到账号 B，
    通过 CCN 云联网点对点打通。支持插件化扩展更多产品。

    \b
    快速开始:
      tc-migrate config account-init   # 生成 account.yaml（密钥文件）
      tc-migrate config init           # 生成示例 tc-migrate.yaml
      tc-migrate config auto           # 全自动配置（自动读取 account.yaml）
      tc-migrate scan                  # 扫描源账号资源
      tc-migrate generate              # 生成 terraform.tfvars
      tc-migrate init                  # terraform init
      tc-migrate plan                  # terraform plan
      tc-migrate apply                 # terraform apply
      tc-migrate run                   # 一键执行全流程

    \b
    密钥管理:
      密钥信息存放在 account.yaml 中（独立于 tc-migrate.yaml），
      所有命令自动从 account.yaml 读取密钥，避免在命令行暴露密钥。
      也可通过 --account-file 指定路径，或设置环境变量 TC_MIGRATE_ACCOUNT。
    """
    pass


# ── 注册所有命令 ──
register_config(cli)
register_scan(cli)
register_plugins(cli)
register_generate(cli)
register_tf(cli)
register_run(cli)


if __name__ == "__main__":
    cli()
