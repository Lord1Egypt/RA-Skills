"""plugins 命令：查看已注册插件"""
from __future__ import annotations

import click
from rich.console import Console
from rich.table import Table

from ..cli_utils import console
from ..plugins import get_ordered_plugins


def register(cli: click.Group) -> None:
    """将 plugins 命令注册到主 CLI"""

    @cli.command()
    def plugins():
        """📦 查看所有已注册的资源迁移插件"""
        all_plugins = get_ordered_plugins()

        table = Table(title="已注册的资源迁移插件", show_lines=True)
        table.add_column("类型", style="bold cyan")
        table.add_column("名称")
        table.add_column("依赖")

        for plugin_cls in all_plugins:
            deps = ", ".join(plugin_cls.DEPENDS_ON) if plugin_cls.DEPENDS_ON else "[dim]无[/]"
            table.add_row(plugin_cls.RESOURCE_TYPE, plugin_cls.DISPLAY_NAME, deps)

        console.print(table)
        console.print(f"\n共 {len(all_plugins)} 个插件已注册")
