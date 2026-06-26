"""run 命令：一键执行完整流程"""
from __future__ import annotations

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..cli_utils import check_result, common_options, console
from ..config import load_config
from ..plugins import get_all_plugins
from ..terraform import find_terraform_dir, tf_apply, tf_init, tf_plan
from ..tfvars import generate_tfvars


def register(cli: click.Group) -> None:
    """将 run 命令注册到主 CLI"""

    @cli.command()
    @common_options
    @click.option("--yes", "-y", "--auto-approve", "auto_approve", is_flag=True, help="跳过所有确认（自动 approve）")
    def run(config_path: str | None, account_path: str | None,
            tf_dir: str | None, auto_approve: bool):
        """⚡ 一键执行完整流程 (generate → init → plan → apply)"""
        try:
            cfg = load_config(config_path, account_path)
        except (FileNotFoundError, ValueError) as e:
            console.print(f"[bold red]✗[/] {e}")
            raise SystemExit(1)

        terraform_dir = find_terraform_dir(tf_dir)

        # 显示迁移摘要
        region_info = (
            f"[bold yellow]跨地域[/]: {cfg.region_a} ↔ {cfg.region_b}"
            if cfg.is_cross_region
            else f"区域: {cfg.region_a}"
        )

        resource_lines: list[str] = [f"  • VPC: {len(cfg.vpcs)} 个"]
        all_plugins = get_all_plugins()
        for rtype, rdata in cfg.resources.items():
            if rtype in all_plugins:
                plugin_cls = all_plugins[rtype]
                plugin = plugin_cls()
                plugin_config = plugin.config_from_dict(rdata)
                count = 0
                for field_name in ("instances", "gateways", "security_groups"):
                    val = getattr(plugin_config, field_name, None)
                    if val is not None:
                        count = len(val)
                        break
                if count > 0:
                    resource_lines.append(f"  • {plugin.DISPLAY_NAME}: {count} 个")

        console.print(Panel(
            f"[bold]即将迁移以下资源到目标账号[/]\n"
            f"[bold]连接方式：CCN 云联网（账号B创建，共享CCN + 独立路由表隔离）[/]\n"
            f"{region_info}\n"
            + "\n".join(resource_lines)
            + "\n\n"
            + "\n".join(
                f"  VPC {k}: {v.account_a_vpc_id} ↔ {v.account_b_vpc_name} ({v.account_b_vpc_cidr})"
                for k, v in cfg.vpcs.items()
            ),
            title="迁移计划", border_style="cyan",
        ))

        # Step 1: 生成 tfvars
        console.print(Panel("[bold]Step 1/4: 生成 terraform.tfvars[/]", border_style="blue"))
        tfvars_path = terraform_dir / "terraform.tfvars"
        generate_tfvars(cfg, tfvars_path)
        console.print(f"[bold green]✓[/] terraform.tfvars 已生成\n")

        # Step 2: init
        console.print(Panel("[bold]Step 2/4: terraform init[/]", border_style="blue"))
        result = tf_init(terraform_dir)
        if result.returncode != 0:
            console.print("[bold red]✗[/] terraform init 失败，终止执行")
            raise SystemExit(1)
        console.print()

        # Step 3: plan
        console.print(Panel("[bold]Step 3/4: terraform plan[/]", border_style="blue"))
        result = tf_plan(terraform_dir, out_file="tfplan")
        if result.returncode != 0:
            console.print("[bold red]✗[/] terraform plan 失败，终止执行")
            raise SystemExit(1)
        console.print()

        # Step 4: apply
        if not auto_approve:
            console.print(Panel(
                "[bold yellow]⚠ 即将创建云资源[/]\n请仔细检查上方的 plan 输出。",
                border_style="yellow",
            ))
            if not Confirm.ask("确认执行 apply?", default=False):
                console.print("[yellow]已取消[/]")
                raise SystemExit(0)

        console.print(Panel("[bold]Step 4/4: terraform apply[/]", border_style="green"))
        result = tf_apply(terraform_dir, auto_approve=True, plan_file="tfplan")
        check_result(result, "apply")
        
        # 完成提示
        console.print()
        console.print(Panel(
            "[bold green]✓ 迁移完成！[/]\n\n"
            "[dim]🔒 CCN 安全配置（已通过 Terraform 实现）：[/]\n"
            "[dim]   • 每对 VPC 使用独立的自定义路由表[/]\n"
            "[dim]   • 路由接收策略只接收 pair 内 VPC 的路由[/]\n"
            "[dim]   • 自定义路由表默认拒绝其他所有路由[/]\n"
            "[dim]   • 没有 VPC 绑定到默认路由表[/]",
            title="完成", border_style="green",
        ))
