"""CLI 公共工具：装饰器、辅助函数"""
from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel

from .config import load_config, save_config
from .tfvars import generate_tfvars

console = Console()


def common_options(func):
    """为命令添加公共选项"""
    func = click.option(
        "-c", "--config", "config_path",
        type=click.Path(), envvar="TC_MIGRATE_CONFIG",
        help="配置文件路径 (默认: ./tc-migrate.yaml)",
    )(func)
    func = click.option(
        "-a", "--account-file", "account_path",
        type=click.Path(), envvar="TC_MIGRATE_ACCOUNT",
        help="账号密钥文件路径 (默认: ./account.yaml)",
    )(func)
    func = click.option(
        "--tf-dir", "tf_dir",
        type=click.Path(exists=True, file_okay=False),
        help="Terraform 项目目录路径",
    )(func)
    return func


def ensure_tfvars(config_path: str | None, account_path: str | None, terraform_dir: Path) -> None:
    """确保 terraform.tfvars 已存在，如果不存在则尝试从配置文件生成"""
    tfvars_path = terraform_dir / "terraform.tfvars"
    if tfvars_path.exists():
        return
    console.print("[yellow]⚠[/] terraform.tfvars 不存在，尝试从配置文件生成...")
    try:
        cfg = load_config(config_path, account_path)
        generate_tfvars(cfg, tfvars_path)
        console.print(f"[bold green]✓[/] 已自动生成 terraform.tfvars\n")
    except (FileNotFoundError, ValueError):
        console.print(
            "[bold red]✗[/] 未找到配置文件，无法自动生成 terraform.tfvars\n"
            "  请先执行: tc-migrate config init 或 tc-migrate config wizard"
        )
        raise SystemExit(1)


def check_result(result, cmd_name: str) -> None:
    """检查命令执行结果"""
    if result.returncode == 0:
        console.print(f"\n[bold green]✓[/] terraform {cmd_name} 执行成功")
    else:
        console.print(f"\n[bold red]✗[/] terraform {cmd_name} 执行失败 (exit code: {result.returncode})")
        raise SystemExit(result.returncode)
