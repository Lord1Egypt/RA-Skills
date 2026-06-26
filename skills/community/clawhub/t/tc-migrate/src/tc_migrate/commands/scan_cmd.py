"""scan 命令：扫描源账号资源"""
from __future__ import annotations

import click
from rich.panel import Panel
from rich.table import Table

from ..cli_utils import common_options, console
from ..config import find_config, load_config, save_config
from ..plugins import get_all_plugins, get_ordered_plugins
from ..plugins.base import MigrationContext
from .config_cmds import _remove_empty_vpcs


def register(cli: click.Group) -> None:
    """将 scan 命令注册到主 CLI"""

    @cli.command()
    @common_options
    @click.option("--resources", "-r", multiple=True, help="要扫描的资源类型 (clb/nat/cvm/all)")
    @click.option("--save", "save_to_config", is_flag=True, help="将扫描结果保存到配置文件")
    @click.option("--skip-empty-vpc", is_flag=True, default=False, help="跳过空 VPC")
    def scan(
        config_path: str | None, account_path: str | None, tf_dir: str | None,
        resources: tuple[str, ...], save_to_config: bool, skip_empty_vpc: bool,
    ):
        """🔍 扫描源账号资源，自动生成迁移配置"""
        try:
            cfg = load_config(config_path, account_path)
        except (FileNotFoundError, ValueError) as e:
            console.print(f"[bold red]✗[/] {e}")
            raise SystemExit(1)

        # 自动补全 UIN
        if not cfg.account_a.uin or not cfg.account_b.uin:
            console.print("[dim]检测到 UIN 未填写，正在通过 API 自动查询...[/]")
            from ..api_helpers import query_account_uin
            if not cfg.account_a.uin:
                info = query_account_uin(cfg.account_a.secret_id, cfg.account_a.secret_key)
                cfg.account_a.uin = info.uin
                console.print(f"  ✓ 源账号 UIN: {info.uin}")
            if not cfg.account_b.uin:
                info = query_account_uin(cfg.account_b.secret_id, cfg.account_b.secret_key)
                cfg.account_b.uin = info.uin
                console.print(f"  ✓ 目标账号 UIN: {info.uin}")
            resolved_path = find_config(config_path)
            save_config(cfg, resolved_path)
            console.print(f"  [dim]UIN 已自动回填到 {resolved_path}[/]\n")

        # 解析资源类型
        all_plugins = get_all_plugins()
        if not resources or "all" in resources:
            ordered = get_ordered_plugins()
            target_types = [p.RESOURCE_TYPE for p in ordered if p.RESOURCE_TYPE in all_plugins]
        else:
            target_types = list(resources)
            for rt in target_types:
                if rt not in all_plugins:
                    console.print(
                        f"[bold red]✗[/] 未知的资源类型: {rt}，"
                        f"可用: {', '.join(all_plugins.keys())}"
                    )
                    raise SystemExit(1)
            needs_sg = any(rt in ("cvm", "clb") for rt in target_types)
            if needs_sg and "sg" not in target_types and "sg" in all_plugins:
                target_types.insert(0, "sg")

        # 构建迁移上下文
        vpc_id_mapping = {vpc.account_a_vpc_id: key for key, vpc in cfg.vpcs.items()}
        context = MigrationContext(
            region_a=cfg.region_a or "ap-guangzhou",
            region_b=cfg.region_b or "ap-guangzhou",
            vpc_id_mapping=vpc_id_mapping,
        )
        source_vpc_ids = [vpc.account_a_vpc_id for vpc in cfg.vpcs.values()]

        console.print(Panel(
            f"[bold]扫描源账号资源[/]\n"
            f"  区域: {context.region_a}\n"
            f"  VPC: {', '.join(source_vpc_ids)}\n"
            f"  资源类型: {', '.join(target_types)}",
            title="🔍 Scan", border_style="cyan",
        ))

        # 逐类型扫描
        scan_results: dict[str, list] = {}
        table = Table(title="扫描结果", show_lines=True)
        table.add_column("资源类型", style="bold")
        table.add_column("数量", justify="right")
        table.add_column("详情")

        for rtype in target_types:
            plugin_cls = all_plugins[rtype]
            plugin = plugin_cls()
            try:
                found = plugin.query_resources(
                    secret_id=cfg.account_a.secret_id,
                    secret_key=cfg.account_a.secret_key,
                    region=context.region_a,
                    vpc_ids=source_vpc_ids,
                )
                scan_results[rtype] = found
                details = ", ".join(r.get("name", r.get("source_id", "?")) for r in found[:5])
                if len(found) > 5:
                    details += f" (+{len(found) - 5} more)"
                table.add_row(plugin.DISPLAY_NAME, str(len(found)), details or "[dim]无[/]")
                if found:
                    plugin_config = plugin.build_config(found, context)
                    cfg.resources[rtype] = plugin_config.model_dump()
            except Exception as e:
                table.add_row(plugin.DISPLAY_NAME, "❌", f"[red]{e}[/]")

        console.print(table)

        if skip_empty_vpc:
            _remove_empty_vpcs(cfg, scan_results, vpc_id_mapping)

        if save_to_config and scan_results:
            path = find_config(config_path)
            save_config(cfg, path)
            console.print(f"\n[bold green]✓[/] 扫描结果已保存到: {path}")
            console.print("[dim]请检查配置文件中 resources 部分，按需调整后执行 generate[/]")
