"""generate 命令：生成 terraform.tfvars"""
from __future__ import annotations

import click
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm

from ..cli_utils import common_options, console
from ..config import load_config
from ..terraform import find_terraform_dir
from ..tfvars import generate_tfvars, get_tfvars_content


def register(cli: click.Group) -> None:
    """将 generate 命令注册到主 CLI"""

    @cli.command()
    @common_options
    @click.option("--preview", is_flag=True, help="仅预览生成内容，不写入文件")
    @click.option("--force", is_flag=True, help="覆盖已存在的文件，不询问确认")
    def generate(config_path: str | None, account_path: str | None, tf_dir: str | None,
                 preview: bool, force: bool):
        """🔧 从配置文件生成 terraform.tfvars"""
        try:
            cfg = load_config(config_path, account_path)
        except (FileNotFoundError, ValueError) as e:
            console.print(f"[bold red]✗[/] {e}")
            raise SystemExit(1)

        if preview:
            content = get_tfvars_content(cfg)
            console.print(Panel(content, title="terraform.tfvars 预览", border_style="cyan"))
            return

        terraform_dir = find_terraform_dir(tf_dir)
        tfvars_path = terraform_dir / "terraform.tfvars"

        if tfvars_path.exists() and not force:
            console.print(f"[yellow]⚠[/] 目标文件已存在: {tfvars_path}")
            if not Confirm.ask("是否覆盖?", default=True):
                raise SystemExit(0)

        result = generate_tfvars(cfg, tfvars_path)
        console.print(f"[bold green]✓[/] terraform.tfvars 已生成: {result}")
