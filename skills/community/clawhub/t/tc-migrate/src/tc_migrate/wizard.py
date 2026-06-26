"""交互式配置向导 — 引导用户完成首次配置（多 VPC + CCN 云联网，支持跨地域）"""

from __future__ import annotations

import ipaddress

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.table import Table

from .models import AccountAuth, DEFAULT_TAGS, MigrateConfig, SubnetConfig, VPCConfig

console = Console()

# 可用区域列表
REGIONS = [
    "ap-guangzhou",
    "ap-shanghai",
    "ap-beijing",
    "ap-chengdu",
    "ap-chongqing",
    "ap-nanjing",
    "ap-hongkong",
    "ap-singapore",
    "ap-bangkok",
    "ap-mumbai",
    "ap-seoul",
    "ap-tokyo",
    "na-siliconvalley",
    "na-ashburn",
    "eu-frankfurt",
]


def _prompt_cidr(prompt_text: str, default: str = "") -> str:
    """带校验的 CIDR 输入"""
    while True:
        value = Prompt.ask(prompt_text, default=default or None)
        if not value:
            console.print("[red]CIDR 不能为空[/]")
            continue
        try:
            ipaddress.ip_network(value, strict=False)
            return value
        except ValueError:
            console.print(f"[red]无效的 CIDR 格式: {value}，请重新输入[/]")


def _show_region_table() -> None:
    """显示可选地域列表"""
    table = Table(show_header=False, box=None, padding=(0, 2))
    for i, r in enumerate(REGIONS):
        if i % 3 == 0:
            row = []
        row.append(f"[dim]{i+1:2d}.[/] {r}")
        if i % 3 == 2 or i == len(REGIONS) - 1:
            while len(row) < 3:
                row.append("")
            table.add_row(*row)
    console.print(table)


def _prompt_region(label: str, default: str = "ap-guangzhou") -> str:
    """交互式选择地域"""
    region_input = Prompt.ask(f"选择{label} (编号或名称)", default=default)
    if region_input.isdigit():
        idx = int(region_input) - 1
        return REGIONS[idx] if 0 <= idx < len(REGIONS) else default
    return region_input


def _prompt_uin(prompt_text: str) -> str:
    """带校验的 UIN 输入"""
    while True:
        value = Prompt.ask(prompt_text)
        if value and value.isdigit() and len(value) >= 6:
            return value
        console.print("[red]UIN 应为 6 位以上纯数字，请重新输入[/]")


def _prompt_account(label: str) -> AccountAuth:
    """交互式输入账号认证信息（UIN 自动通过 API 查询）"""
    console.print(f"\n[bold cyan]── {label} 认证信息 ──[/]")
    secret_id = Prompt.ask(f"  SecretId")
    secret_key = Prompt.ask(f"  SecretKey")

    # 自动查询 UIN
    uin = ""
    try:
        from .api_helpers import query_account_uin
        console.print(f"  [dim]⏳ 自动查询 UIN...[/]")
        info = query_account_uin(secret_id, secret_key)
        uin = info.uin
        console.print(f"  [green]✓ UIN: {uin}[/]")
    except Exception as e:
        console.print(f"  [yellow]⚠ 自动查询 UIN 失败: {e}[/]")
        uin = _prompt_uin(f"  请手动输入主账号 UIN")

    return AccountAuth(secret_id=secret_id, secret_key=secret_key, uin=uin)


def _prompt_subnets(vpc_cidr: str, region: str) -> list[SubnetConfig]:
    """交互式输入子网列表"""
    subnets: list[SubnetConfig] = []
    console.print("[dim]  至少需要一个子网，输入空名称结束添加[/]")

    idx = 1
    while True:
        console.print(f"\n  [bold]子网 #{idx}[/]")
        name = Prompt.ask("    名称", default="" if idx > 1 else "subnet-1")
        if not name and idx > 1:
            break
        elif not name:
            console.print("[red]  至少需要一个子网[/]")
            continue

        cidr = _prompt_cidr("    CIDR")
        az = Prompt.ask("    可用区", default=f"{region}-3")

        subnets.append(SubnetConfig(name=name, cidr=cidr, az=az))
        idx += 1

        if not Confirm.ask("    继续添加子网?", default=False):
            break

    return subnets


def _prompt_single_vpc(vpc_key: str, region: str) -> VPCConfig:
    """交互式输入单个 VPC 配置"""
    console.print(f"\n[bold green]  ── VPC: {vpc_key} ──[/]")

    account_a_vpc_id = Prompt.ask("  账号A VPC ID", default=f"vpc-{vpc_key}-xxxx")
    account_b_vpc_name = Prompt.ask("  账号B 新 VPC 名称", default=f"vpc-b-{vpc_key}")
    account_b_vpc_cidr = _prompt_cidr("  账号B VPC CIDR")

    console.print(f"\n  [bold cyan]子网配置[/]")
    subnets = _prompt_subnets(account_b_vpc_cidr, region)

    account_b_sg_name = Prompt.ask("  安全组名称", default=f"sg-b-{vpc_key}")
    sg_cidrs_input = Prompt.ask(
        "  安全组入站 CIDR (逗号分隔)", default=account_b_vpc_cidr
    )
    sg_cidrs = [c.strip() for c in sg_cidrs_input.split(",") if c.strip()]

    return VPCConfig(
        account_a_vpc_id=account_a_vpc_id,
        account_b_vpc_name=account_b_vpc_name,
        account_b_vpc_cidr=account_b_vpc_cidr,
        account_b_subnets=subnets,
        account_b_sg_name=account_b_sg_name,
        account_b_sg_ingress_cidrs=sg_cidrs,
    )


def run_wizard() -> MigrateConfig:
    """运行交互式配置向导，返回完整的 MigrateConfig"""
    console.print(
        Panel.fit(
            "[bold green]🚀 腾讯云跨账号 多VPC 迁移 — 配置向导[/]\n"
            "[dim]方案：CCN 云联网（每对 VPC 独立 CCN + 路由表，隔离性好，支持跨地域）[/]\n"
            "[dim]按照提示输入各项信息，支持配置多个 VPC 一次性迁移[/]",
            border_style="green",
        )
    )

    # 1. 区域选择（支持跨地域）
    console.print("\n[bold cyan]── 区域选择 ──[/]")
    _show_region_table()

    cross_region = Confirm.ask(
        "账号A 和 账号B 是否在不同地域？（跨地域 CCN）", default=False
    )
    if cross_region:
        console.print("\n[bold]账号A 地域：[/]")
        region_a = _prompt_region("账号A 地域", default="ap-guangzhou")
        console.print(f"\n[bold]账号B 地域：[/]")
        region_b = _prompt_region("账号B 地域", default="ap-shanghai")
        console.print(
            f"\n[yellow]⚠ 跨地域 CCN 注意：[/]\n"
            f"  • 跨地域 CCN 按带宽计费\n"
            f"  • 延迟会比同地域高\n"
            f"  • 账号A: [bold]{region_a}[/] ↔ 账号B: [bold]{region_b}[/]"
        )
    else:
        region_a = _prompt_region("地域", default="ap-guangzhou")
        region_b = region_a

    # 2. 账号认证
    account_a = _prompt_account("账号 A（源账号）")
    account_b = _prompt_account("账号 B（目标账号）")

    # 3. 多 VPC 配置
    console.print("\n[bold cyan]── VPC 迁移配置 ──[/]")
    console.print("[dim]请为每个要迁移的 VPC 设置一个逻辑名称（如 prod、dev、staging）[/]")
    console.print("[dim]每对 VPC（A↔B）会创建一个独立的 CCN + 路由表，互不干扰[/]")

    vpcs: dict[str, VPCConfig] = {}
    vpc_idx = 1
    while True:
        console.print(f"\n[bold magenta]─── 第 {vpc_idx} 个 VPC ───[/]")
        vpc_key = Prompt.ask("  VPC 逻辑名称", default="prod" if vpc_idx == 1 else "")
        if not vpc_key:
            if vpc_idx == 1:
                console.print("[red]  至少需要配置一个 VPC[/]")
                continue
            break

        if vpc_key in vpcs:
            console.print(f"[red]  逻辑名 '{vpc_key}' 已存在，请使用不同名称[/]")
            continue

        vpc_config = _prompt_single_vpc(vpc_key, region_b)
        vpcs[vpc_key] = vpc_config
        vpc_idx += 1

        console.print(f"\n[green]  ✓ VPC '{vpc_key}' 配置完成[/]")
        if not Confirm.ask("  继续添加下一个 VPC?", default=False):
            break

    # 4. 标签
    console.print("\n[bold cyan]── 标签配置 ──[/]")
    tags = DEFAULT_TAGS.copy()
    env_tag = Prompt.ask("  environment 标签", default=tags.get("environment", "migration"))
    tags["environment"] = env_tag

    extra_tag = Confirm.ask("  添加其他标签?", default=False)
    while extra_tag:
        key = Prompt.ask("  标签 Key")
        value = Prompt.ask("  标签 Value")
        if key:
            tags[key] = value
        extra_tag = Confirm.ask("  继续添加?", default=False)

    # 构建配置
    config = MigrateConfig(
        region_a=region_a,
        region_b=region_b,
        account_a=account_a,
        account_b=account_b,
        vpcs=vpcs,
        tags=tags,
    )

    # 显示摘要
    console.print("\n")
    _show_summary(config)

    return config


def _show_summary(config: MigrateConfig) -> None:
    """显示配置摘要（多 VPC + CCN 云联网，支持跨地域）"""
    table = Table(title="📋 配置摘要（CCN 云联网方案）", show_header=True, header_style="bold magenta")
    table.add_column("项目", style="cyan", width=28)
    table.add_column("值", style="white")

    if config.is_cross_region:
        table.add_row("账号A 区域", config.region_a)
        table.add_row("账号B 区域", config.region_b)
        table.add_row("跨地域 CCN", "[bold yellow]是（按带宽计费）[/]")
    else:
        table.add_row("区域", config.region_a)
    table.add_row("账号A UIN", config.account_a.uin)
    table.add_row("账号A SecretId", config.account_a.secret_id[:8] + "****")
    table.add_row("账号B UIN", config.account_b.uin)
    table.add_row("账号B SecretId", config.account_b.secret_id[:8] + "****")
    table.add_row("VPC 数量", str(len(config.vpcs)))
    table.add_row("连接方式", "CCN 云联网（每对独立 CCN + 路由表，互相隔离）")
    if config.target_cidr_block:
        table.add_row("目标网段", f"[bold green]{config.target_cidr_block}[/]（自动拆分）")
    table.add_row("", "")

    for vpc_key, vpc in config.vpcs.items():
        table.add_row(f"[bold]VPC: {vpc_key}[/]", "")
        table.add_row(f"  账号A VPC ID", vpc.account_a_vpc_id)
        table.add_row(f"  CCN 名称", f"ccn-{vpc_key}-migration")
        table.add_row(f"  账号B VPC 名称", vpc.account_b_vpc_name)
        table.add_row(f"  账号B VPC CIDR", vpc.account_b_vpc_cidr)
        table.add_row(f"  子网数量", str(len(vpc.account_b_subnets)))
        for s in vpc.account_b_subnets:
            table.add_row(f"    └─ {s.name}", f"{s.cidr} ({s.az})")
        table.add_row("", "")

    table.add_row("标签", ", ".join(f"{k}={v}" for k, v in config.tags.items()))

    console.print(table)
