"""config 子命令组：init / account-init / wizard / auto / validate / show"""
from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..cli_utils import console
from ..config import (
    find_config, generate_example_account, generate_example_config,
    get_account_credentials, load_config, save_config,
)
from ..plugins import get_all_plugins, get_ordered_plugins
from ..plugins.base import MigrationContext


def _run_scan_logic(cfg, config_path_str: str, skip_empty_vpc: bool = False) -> None:
    """scan 核心逻辑，供 config auto 和 scan 命令共用"""
    all_plugins = get_all_plugins()
    vpc_id_mapping = {
        vpc.account_a_vpc_id: key for key, vpc in cfg.vpcs.items()
    }
    context = MigrationContext(
        region_a=cfg.region_a or "ap-guangzhou",
        region_b=cfg.region_b or "ap-guangzhou",
        vpc_id_mapping=vpc_id_mapping,
    )
    source_vpc_ids = [vpc.account_a_vpc_id for vpc in cfg.vpcs.values()]
    ordered_plugins = get_ordered_plugins()
    target_types = [p.RESOURCE_TYPE for p in ordered_plugins if p.RESOURCE_TYPE in all_plugins]

    scan_results: dict[str, list] = {}
    from rich.table import Table
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

    if scan_results:
        path = find_config(config_path_str)
        save_config(cfg, path)
        console.print(f"\n[bold green]✓[/] 扫描结果已保存到: {path}")
        console.print("[dim]配置已就绪，可以执行 tc-migrate generate 或 tc-migrate run[/]")


def _remove_empty_vpcs(cfg, scan_results: dict[str, list], vpc_id_mapping: dict[str, str]) -> None:
    """检测并移除没有任何云资源的空 VPC。"""
    vpc_resource_count: dict[str, int] = {key: 0 for key in cfg.vpcs}

    for rtype, resources in scan_results.items():
        for res in resources:
            vpc_id = res.get("vpc_id", "")
            if vpc_id and vpc_id in vpc_id_mapping:
                vpc_key = vpc_id_mapping[vpc_id]
                vpc_resource_count[vpc_key] = vpc_resource_count.get(vpc_key, 0) + 1
            for vid in res.get("vpc_ids", []):
                if vid in vpc_id_mapping:
                    vpc_key = vpc_id_mapping[vid]
                    vpc_resource_count[vpc_key] = vpc_resource_count.get(vpc_key, 0) + 1

    empty_vpcs = [key for key, count in vpc_resource_count.items() if count == 0]
    if empty_vpcs:
        console.print(f"\n[yellow]⚠ 检测到 {len(empty_vpcs)} 个空 VPC（无任何云资源），已跳过:[/]")
        for vpc_key in empty_vpcs:
            vpc_info = cfg.vpcs[vpc_key]
            console.print(f"  [dim]• {vpc_key}: {vpc_info.account_a_vpc_id} ({vpc_info.account_b_vpc_name})[/]")
            del cfg.vpcs[vpc_key]
        if not cfg.vpcs:
            console.print("[bold red]✗[/] 移除空 VPC 后没有剩余的 VPC，请检查源账号资源")
            raise SystemExit(1)
        console.print(f"  [green]保留 {len(cfg.vpcs)} 个有资源的 VPC[/]")
    else:
        console.print("\n[dim]所有 VPC 均有关联资源，无需跳过[/]")


def register(cli: click.Group) -> None:
    """将 config 子命令组注册到主 CLI"""

    @cli.group()
    def config():
        """📝 配置文件管理"""
        pass

    @config.command("init")
    @click.option("-o", "--output", default="tc-migrate.yaml", help="输出文件路径")
    @click.option("--force", is_flag=True, help="覆盖已有文件")
    def config_init(output: str, force: bool):
        """生成示例配置文件（含多 VPC 示例）"""
        path = Path(output)
        if path.exists() and not force:
            console.print(f"[yellow]⚠[/] 配置文件已存在: {path}")
            if not Confirm.ask("是否覆盖?", default=False):
                raise SystemExit(0)
        result = generate_example_config(output)
        console.print(f"[bold green]✓[/] 示例配置文件已生成: {result}")
        console.print("[dim]请编辑该文件，在 vpcs 下添加/修改要迁移的 VPC[/]")

    @config.command("account-init")
    @click.option("-o", "--output", default="account.yaml", help="输出文件路径")
    @click.option("--force", is_flag=True, help="覆盖已有文件")
    def config_account_init(output: str, force: bool):
        """🔑 生成示例 account.yaml（密钥文件，独立于 tc-migrate.yaml）

        \b
        account.yaml 存放敏感的密钥和地域信息：
          - account_a: 源账号的 secret_id / secret_key / region
          - account_b: 目标账号的 secret_id / secret_key / region

        密钥文件独立存放，config auto / scan 等命令会自动读取。
        请将 account.yaml 加入 .gitignore，避免密钥泄露。
        """
        path = Path(output)
        if path.exists() and not force:
            console.print(f"[yellow]⚠[/] 账号文件已存在: {path}")
            if not Confirm.ask("是否覆盖?", default=False):
                raise SystemExit(0)
        result = generate_example_account(output)
        console.print(f"[bold green]✓[/] 示例账号文件已生成: {result}")
        console.print("[dim]请编辑该文件，填入真实的 SecretId / SecretKey / Region[/]")
        console.print("[yellow]⚠ 请将 account.yaml 加入 .gitignore[/]")

    @config.command("wizard")
    @click.option("-o", "--output", default="tc-migrate.yaml", help="输出文件路径")
    def config_wizard(output: str):
        """交互式配置向导（支持多 VPC）"""
        from ..wizard import run_wizard
        try:
            cfg = run_wizard()
            path = save_config(cfg, output)
            console.print(f"\n[bold green]✓[/] 配置文件已保存: {path}")
        except KeyboardInterrupt:
            console.print("\n[yellow]已取消[/]")
            raise SystemExit(0)

    @config.command("auto")
    @click.option("-o", "--output", default="tc-migrate.yaml", help="输出文件路径")
    @click.option("--force", is_flag=True, help="覆盖已有文件")
    @click.option("-a", "--account-file", "account_path", type=click.Path(), envvar="TC_MIGRATE_ACCOUNT",
                  help="账号密钥文件路径 (默认: ./account.yaml)")
    @click.option("--secret-id-a", default=None, help="源账号 SecretId")
    @click.option("--secret-key-a", default=None, help="源账号 SecretKey")
    @click.option("--region-a", default=None, help="源账号地域")
    @click.option("--secret-id-b", default=None, help="目标账号 SecretId")
    @click.option("--secret-key-b", default=None, help="目标账号 SecretKey")
    @click.option("--region-b", default=None, help="目标账号地域")
    @click.option("--target-cidr", default=None, help="目标端统一大网段（如 172.16.0.0/12）")
    @click.option("--scan/--no-scan", "run_scan", default=True, help="生成配置后自动扫描资源")
    @click.option("--skip-empty-vpc", is_flag=True, default=False, help="跳过空 VPC")
    def config_auto(
        output: str, force: bool, account_path: str | None,
        secret_id_a: str | None, secret_key_a: str | None, region_a: str | None,
        secret_id_b: str | None, secret_key_b: str | None, region_b: str | None,
        target_cidr: str | None, run_scan: bool, skip_empty_vpc: bool,
    ):
        """🚀 全自动配置（自动从 account.yaml 读取密钥，无需命令行传参）

        \b
        优先级：命令行参数 > account.yaml > 交互式提示

        \b
        推荐用法（先创建 account.yaml）：
          tc-migrate config account-init   # 生成 account.yaml 模板
          # 编辑 account.yaml 填入密钥和地域
          tc-migrate config auto           # 全自动，密钥从 account.yaml 读取
        """
        from ..api_helpers import auto_discover

        path = Path(output)
        if path.exists() and not force:
            console.print(f"[yellow]⚠[/] 配置文件已存在: {path}")
            if not Confirm.ask("是否覆盖?", default=False):
                raise SystemExit(0)

        acct_creds = get_account_credentials(account_path)
        if acct_creds:
            console.print("[dim]📄 已从 account.yaml 读取密钥信息[/]")

        final_secret_id_a = secret_id_a or (acct_creds or {}).get("secret_id_a")
        final_secret_key_a = secret_key_a or (acct_creds or {}).get("secret_key_a")
        final_region_a = region_a or (acct_creds or {}).get("region_a")
        final_secret_id_b = secret_id_b or (acct_creds or {}).get("secret_id_b")
        final_secret_key_b = secret_key_b or (acct_creds or {}).get("secret_key_b")
        final_region_b = region_b or (acct_creds or {}).get("region_b")

        if not final_secret_id_a:
            final_secret_id_a = click.prompt("源账号 SecretId")
        if not final_secret_key_a:
            final_secret_key_a = click.prompt("源账号 SecretKey")
        if not final_region_a:
            final_region_a = click.prompt("源账号地域 (如 ap-beijing)")
        if not final_secret_id_b:
            final_secret_id_b = click.prompt("目标账号 SecretId")
        if not final_secret_key_b:
            final_secret_key_b = click.prompt("目标账号 SecretKey")
        if not final_region_b:
            final_region_b = click.prompt("目标账号地域 (如 ap-guangzhou)")

        console.print(Panel(
            "[bold]🔍 全自动配置：正在通过 API 查询账号信息...[/]\n"
            f"  源账号地域: {final_region_a}\n"
            f"  目标账号地域: {final_region_b}",
            border_style="cyan",
        ))

        try:
            config_dict = auto_discover(
                secret_id_a=final_secret_id_a, secret_key_a=final_secret_key_a, region_a=final_region_a,
                secret_id_b=final_secret_id_b, secret_key_b=final_secret_key_b, region_b=final_region_b,
            )
        except Exception as e:
            console.print(f"[bold red]✗[/] API 查询失败: {e}")
            raise SystemExit(1)

        final_target_cidr = target_cidr or (acct_creds or {}).get("target_cidr_block")
        if final_target_cidr:
            config_dict["target_cidr_block"] = final_target_cidr

        try:
            from ..models import MigrateConfig
            cfg = MigrateConfig(**config_dict)
        except Exception as e:
            console.print(f"[bold red]✗[/] 配置校验失败: {e}")
            raise SystemExit(1)

        if cfg.target_cidr_block:
            console.print(Panel(f"[bold]🎯 目标网段自动分配: {cfg.target_cidr_block}[/]", border_style="green"))
            cfg.allocate_target_cidrs()

        save_config(cfg, path)
        console.print(f"\n[bold green]✓[/] 配置文件已生成: {path}")
        console.print(f"  • UIN 已自动填充")
        console.print(f"  • {len(cfg.vpcs)} 个 VPC 已自动加入")
        console.print(f"  • CIDR 冲突的 VPC 已自动跳过")
        if cfg.target_cidr_block:
            console.print(f"  • 目标网段 {cfg.target_cidr_block} 已自动拆分分配")
        console.print(f"  [dim]• 密钥信息保存在 account.yaml 中，tc-migrate.yaml 中也有一份[/]")

        if run_scan:
            console.print(Panel("[bold]🔍 自动扫描源账号资源 (CLB/NAT/CVM)...[/]", border_style="cyan"))
            _run_scan_logic(cfg, str(path), skip_empty_vpc=skip_empty_vpc)

    @config.command("validate")
    @click.option("-c", "--config", "config_path", type=click.Path(), envvar="TC_MIGRATE_CONFIG")
    @click.option("-a", "--account-file", "account_path", type=click.Path(), envvar="TC_MIGRATE_ACCOUNT")
    def config_validate(config_path: str | None, account_path: str | None):
        """校验配置文件"""
        try:
            cfg = load_config(config_path, account_path)
            console.print("[bold green]✓[/] 配置文件校验通过")
            if cfg.is_cross_region:
                console.print(f"  账号A 区域: {cfg.region_a}")
                console.print(f"  账号B 区域: {cfg.region_b}")
                console.print(f"  [yellow]跨地域 CCN（按带宽计费）[/]")
            else:
                console.print(f"  区域: {cfg.region_a}")
            console.print(f"  账号A UIN: {cfg.account_a.uin}")
            console.print(f"  账号B UIN: {cfg.account_b.uin}")
            console.print(f"  VPC 数量: {len(cfg.vpcs)}")
            console.print(f"  CCN 名称: {cfg.ccn_name}（账号B创建，共享）")
            console.print(f"  连接方式: CCN 云联网（共享CCN + 独立路由表隔离）")
            if cfg.target_cidr_block:
                console.print(f"  目标网段: [bold green]{cfg.target_cidr_block}[/]（已自动拆分分配）")
            for vpc_key, vpc in cfg.vpcs.items():
                console.print(
                    f"    {vpc_key}: {vpc.account_a_vpc_id} ↔ "
                    f"{vpc.account_b_vpc_name} ({vpc.account_b_vpc_cidr}), "
                    f"{len(vpc.account_b_subnets)} 个子网, "
                    f"路由表: rt-{vpc_key}-migration"
                )
        except (FileNotFoundError, ValueError) as e:
            console.print(f"[bold red]✗[/] {e}")
            raise SystemExit(1)

    @config.command("show")
    @click.option("-c", "--config", "config_path", type=click.Path(), envvar="TC_MIGRATE_CONFIG")
    @click.option("-a", "--account-file", "account_path", type=click.Path(), envvar="TC_MIGRATE_ACCOUNT")
    def config_show(config_path: str | None, account_path: str | None):
        """显示当前配置"""
        try:
            cfg = load_config(config_path, account_path)
            from ..wizard import _show_summary
            _show_summary(cfg)
        except (FileNotFoundError, ValueError) as e:
            console.print(f"[bold red]✗[/] {e}")
            raise SystemExit(1)
