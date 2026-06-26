"""Terraform 命令执行器 — 封装 init / plan / apply / destroy"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from rich.console import Console

console = Console()

# Terraform 项目目录名
TERRAFORM_DIR_NAME = "terraform"


def find_terraform_binary() -> str:
    """查找 terraform 可执行文件"""
    tf = shutil.which("terraform")
    if tf is None:
        console.print("[bold red]✗[/] 未找到 terraform 命令，请先安装 Terraform")
        console.print("  安装指南: https://developer.hashicorp.com/terraform/install")
        sys.exit(1)
    return tf


def find_terraform_dir(project_root: str | Path | None = None) -> Path:
    """
    查找 Terraform 项目目录。搜索顺序：
    1. 显式指定的 project_root
    2. 当前目录下的 terraform/
    3. 当前目录的父级目录下的 terraform/
    4. 与 src/ 同级的 terraform/（OpenClaw Skill 目录结构）
    5. 兼容旧目录名 terraform-cross-account/
    """
    if project_root:
        d = Path(project_root)
        if d.is_dir():
            return d

    # 当前目录下查找
    cwd = Path.cwd()
    for dir_name in [TERRAFORM_DIR_NAME, "terraform-cross-account"]:
        candidate = cwd / dir_name
        if candidate.is_dir():
            return candidate

    # 父目录查找
    for dir_name in [TERRAFORM_DIR_NAME, "terraform-cross-account"]:
        candidate = cwd.parent / dir_name
        if candidate.is_dir():
            return candidate

    # 从 src 包的位置反推（OpenClaw Skill 目录结构: skill/src/tc_migrate/terraform.py -> skill/terraform/）
    src_dir = Path(__file__).resolve().parent.parent  # tc_migrate -> src
    skill_dir = src_dir.parent  # src -> skill root
    for dir_name in [TERRAFORM_DIR_NAME, "terraform-cross-account"]:
        candidate = skill_dir / dir_name
        if candidate.is_dir():
            return candidate

    console.print(
        f"[bold red]✗[/] 未找到 Terraform 项目目录 '{TERRAFORM_DIR_NAME}'"
    )
    console.print("  请在项目根目录下运行，或使用 --tf-dir 指定路径")
    sys.exit(1)


def run_terraform(
    command: list[str],
    tf_dir: Path,
    auto_approve: bool = False,
    extra_args: list[str] | None = None,
    capture_output: bool = False,
) -> subprocess.CompletedProcess:
    """
    执行 terraform 命令

    Args:
        command: terraform 子命令列表，如 ["init"], ["plan"], ["apply"]
        tf_dir: Terraform 项目目录
        auto_approve: 是否自动确认（apply/destroy 时使用）
        extra_args: 额外命令行参数
        capture_output: 是否捕获输出
    """
    tf_bin = find_terraform_binary()
    args = [tf_bin] + command

    if auto_approve and command[0] in ("apply", "destroy"):
        args.append("-auto-approve")

    if extra_args:
        args.extend(extra_args)

    console.print(f"[dim]$ cd {tf_dir}[/]")
    console.print(f"[dim]$ {' '.join(args)}[/]")
    console.print()

    result = subprocess.run(
        args,
        cwd=str(tf_dir),
        capture_output=capture_output,
        text=True,
        env={**os.environ, "TF_IN_AUTOMATION": "1"},
    )

    return result


def tf_init(tf_dir: Path, upgrade: bool = False) -> subprocess.CompletedProcess:
    """执行 terraform init"""
    extra = ["-upgrade"] if upgrade else []
    return run_terraform(["init"], tf_dir, extra_args=extra)


def tf_plan(tf_dir: Path, out_file: str | None = None) -> subprocess.CompletedProcess:
    """执行 terraform plan"""
    extra = []
    if out_file:
        extra.append(f"-out={out_file}")
    return run_terraform(["plan"], tf_dir, extra_args=extra)


def tf_apply(
    tf_dir: Path,
    auto_approve: bool = False,
    plan_file: str | None = None,
) -> subprocess.CompletedProcess:
    """执行 terraform apply"""
    cmd = ["apply"]
    extra = []
    if plan_file:
        extra.append(plan_file)
    return run_terraform(cmd, tf_dir, auto_approve=auto_approve, extra_args=extra)


def tf_destroy(
    tf_dir: Path, auto_approve: bool = False
) -> subprocess.CompletedProcess:
    """执行 terraform destroy"""
    return run_terraform(["destroy"], tf_dir, auto_approve=auto_approve)


def tf_output(tf_dir: Path, json_format: bool = True) -> subprocess.CompletedProcess:
    """执行 terraform output"""
    extra = ["-json"] if json_format else []
    return run_terraform(["output"], tf_dir, extra_args=extra, capture_output=True)


def tf_validate(tf_dir: Path) -> subprocess.CompletedProcess:
    """执行 terraform validate"""
    return run_terraform(["validate"], tf_dir)
