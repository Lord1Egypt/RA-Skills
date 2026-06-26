"""terraform 相关命令：init / plan / apply / destroy / output / validate"""
from __future__ import annotations

import json

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..cli_utils import check_result, common_options, console, ensure_tfvars
from ..config import load_config
from ..terraform import (
    find_terraform_dir, tf_apply, tf_destroy, tf_init, tf_output, tf_plan, tf_validate,
)


def register(cli: click.Group) -> None:
    """将 terraform 相关命令注册到主 CLI"""

    @cli.command("init")
    @common_options
    @click.option("--upgrade", is_flag=True, help="升级 Provider 插件")
    def cmd_init(config_path: str | None, account_path: str | None,
                 tf_dir: str | None, upgrade: bool):
        """📦 执行 terraform init"""
        terraform_dir = find_terraform_dir(tf_dir)
        ensure_tfvars(config_path, account_path, terraform_dir)
        console.print(Panel("[bold]执行 terraform init[/]", border_style="blue"))
        result = tf_init(terraform_dir, upgrade=upgrade)
        check_result(result, "init")

    @cli.command("plan")
    @common_options
    @click.option("--out", "out_file", default=None, help="将 plan 保存到文件")
    def cmd_plan(config_path: str | None, account_path: str | None,
                 tf_dir: str | None, out_file: str | None):
        """📋 执行 terraform plan"""
        terraform_dir = find_terraform_dir(tf_dir)
        ensure_tfvars(config_path, account_path, terraform_dir)
        console.print(Panel("[bold]执行 terraform plan[/]", border_style="blue"))
        result = tf_plan(terraform_dir, out_file=out_file)
        check_result(result, "plan")

    @cli.command("apply")
    @common_options
    @click.option("--yes", "-y", "--auto-approve", "auto_approve", is_flag=True, help="跳过确认，自动执行")
    @click.option("--plan-file", default=None, help="使用已保存的 plan 文件")
    def cmd_apply(config_path: str | None, account_path: str | None,
                  tf_dir: str | None, auto_approve: bool, plan_file: str | None):
        """🚀 执行 terraform apply"""
        terraform_dir = find_terraform_dir(tf_dir)
        ensure_tfvars(config_path, account_path, terraform_dir)

        if not auto_approve and not plan_file:
            console.print(Panel(
                "[bold yellow]⚠ 即将创建/修改云资源[/]\n"
                "此操作将在腾讯云上创建多个 VPC、子网、安全组和 CCN 云联网。\n"
                "建议先执行 [bold]tc-migrate plan[/] 查看变更。",
                border_style="yellow",
            ))
            if not Confirm.ask("确认执行?", default=False):
                raise SystemExit(0)

        console.print(Panel("[bold]执行 terraform apply[/]", border_style="green"))
        result = tf_apply(terraform_dir, auto_approve=auto_approve, plan_file=plan_file)
        check_result(result, "apply")

    @cli.command("destroy")
    @common_options
    @click.option("--yes", "-y", "--auto-approve", "auto_approve", is_flag=True, help="跳过确认，自动销毁")
    def cmd_destroy(config_path: str | None, account_path: str | None,
                    tf_dir: str | None, auto_approve: bool):
        """💥 执行 terraform destroy（销毁所有资源）"""
        terraform_dir = find_terraform_dir(tf_dir)

        if not auto_approve:
            console.print(Panel(
                "[bold red]⚠ 危险操作！[/]\n"
                "此操作将销毁所有由 Terraform 管理的云资源，包括：\n"
                "  • 账号B 的所有 VPC、子网、安全组\n"
                "  • 所有 CCN 云联网及相关路由表\n"
                "  • 所有 CLB 负载均衡实例及监听器\n"
                "  • 所有 NAT 网关及 EIP\n"
                "  • 所有 CVM 云服务器实例\n"
                "  • 所有从源端复刻的安全组及规则\n"
                "[bold]此操作不可逆！[/]",
                border_style="red",
            ))
            if not Confirm.ask("[bold red]确认销毁所有资源?[/]", default=False):
                raise SystemExit(0)

        console.print(Panel("[bold red]执行 terraform destroy[/]", border_style="red"))
        result = tf_destroy(terraform_dir, auto_approve=auto_approve)
        check_result(result, "destroy")

    @cli.command("output")
    @common_options
    @click.option("--json", "json_format", is_flag=True, default=True, help="JSON 格式输出")
    def cmd_output(config_path: str | None, account_path: str | None,
                   tf_dir: str | None, json_format: bool):
        """📊 查看 terraform output"""
        terraform_dir = find_terraform_dir(tf_dir)
        result = tf_output(terraform_dir, json_format=json_format)
        if result.returncode == 0:
            if json_format and result.stdout:
                try:
                    data = json.loads(result.stdout)
                    formatted = json.dumps(data, indent=2, ensure_ascii=False)
                    console.print(Panel(formatted, title="Terraform Outputs", border_style="green"))
                except json.JSONDecodeError:
                    console.print(result.stdout)
            else:
                console.print(result.stdout or "[dim]暂无输出[/]")
        else:
            console.print(f"[bold red]✗[/] terraform output 失败")
            if result.stderr:
                console.print(result.stderr)

    @cli.command("validate")
    @common_options
    def cmd_validate(config_path: str | None, account_path: str | None, tf_dir: str | None):
        """✅ 执行 terraform validate"""
        terraform_dir = find_terraform_dir(tf_dir)
        console.print(Panel("[bold]执行 terraform validate[/]", border_style="blue"))
        result = tf_validate(terraform_dir)
        check_result(result, "validate")
