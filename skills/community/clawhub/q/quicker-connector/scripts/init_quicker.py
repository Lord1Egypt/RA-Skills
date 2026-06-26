#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quicker Connector 初始化引导脚本

在技能初始化时检查是否有已配置的动作列表路径
如果没有，则引导用户导出 Quicker 动作列表并配置路径
"""

import json
import os
from pathlib import Path
from typing import Optional, Dict, Any, Tuple


def check_config(config_file: str = None) -> bool:
    """
    检查配置文件是否存在且有效

    Args:
        config_file: 配置文件路径，如果为None则使用默认路径

    Returns:
        如果配置存在且有效返回True，否则返回False
    """
    if config_file is None:
        # 默认配置文件路径：技能根目录下的 config.json
        script_dir = Path(__file__).parent.parent
        config_file = str(script_dir / "config.json")

    # 检查配置文件是否存在
    if not os.path.exists(config_file):
        return False

    try:
        # 读取配置文件
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)

        # 检查是否有有效的 CSV 或 DB 路径
        csv_path = config.get('csv_path', '')
        db_path = config.get('db_path', '')

        # 检查 CSV 路径是否存在
        if csv_path and os.path.exists(csv_path):
            return True

        # 检查 DB 路径是否存在
        if db_path and os.path.exists(db_path):
            return True

        # 如果路径都不存在或未配置，则返回 False
        return False

    except Exception as e:
        print(f"检查配置文件时出错: {e}")
        return False


def guide_export() -> None:
    """
    打印导出 Quicker 动作列表的引导信息
    """
    print("\n" + "=" * 70)
    print("Quicker Connector 技能初始化向导")
    print("=" * 70)
    print()
    print("本技能需要读取 Quicker 动作列表才能正常工作。")
    print("请按照以下步骤导出您的 Quicker 动作列表：")
    print()
    print("-" * 70)
    print("导出步骤：")
    print("-" * 70)
    print()
    print("1. 打开 Quicker 面板")
    print("2. 点击右上角的 \"...\" 按钮（更多菜单）")
    print("3. 选择 \"工具\" > \"导出动作列表（CSV）\"")
    print("4. 在弹出的保存对话框中选择一个位置保存 CSV 文件")
    print("   建议保存为：QuickerActions.csv")
    print()
    print("-" * 70)
    print()


def prompt_csv_path() -> Optional[str]:
    """
    提示用户输入 CSV 文件路径

    Returns:
        用户输入的 CSV 文件路径，如果用户输入无效则返回 None
    """
    print("请输入您刚刚导出的 CSV 文件的完整路径：")
    print()
    print("提示：您可以直接将 CSV 文件拖拽到终端窗口中")
    print()

    while True:
        csv_path = input("CSV 文件路径（输入 q 退出）: ").strip()

        # 用户选择退出
        if csv_path.lower() == 'q':
            print("\n已取消配置。稍后可以重新运行初始化。")
            return None

        # 检查文件是否存在
        if not os.path.exists(csv_path):
            print(f"\n错误：文件不存在: {csv_path}")
            print("请检查路径是否正确，或直接拖拽文件到窗口中\n")
            continue

        # 检查文件扩展名
        if not csv_path.lower().endswith('.csv'):
            confirm = input(f"\n警告：文件扩展名不是 .csv，是否继续？(y/n): ").strip().lower()
            if confirm != 'y':
                print("\n请输入正确的 CSV 文件路径\n")
                continue

        return csv_path


def prompt_push_config() -> Dict[str, str]:
    """
    可选：引导用户配置 Quicker 推送服务凭证。

    Returns:
        包含 push_user / push_code 的字典（可能为空值）
    """
    print()
    print("-" * 70)
    print("可选：配置远程推送执行（方案 C）")
    print("-" * 70)
    print()
    print("推送服务允许通过 Quicker 云端远程触发动作，并获取执行结果。")
    print("需要在 Quicker 会员中心获取验证码：")
    print("  https://getquicker.net/user/connection")
    print()

    setup = input("是否现在配置推送凭证？(y/n，直接回车跳过): ").strip().lower()
    if setup != 'y':
        print("已跳过推送配置，可稍后手动在 config.json 中添加 push_user / push_code。")
        return {}

    push_user = input("Quicker 账号邮箱: ").strip()
    push_code = input("推送验证码: ").strip()

    if not push_user or not push_code:
        print("输入为空，跳过推送配置。")
        return {}

    return {"push_user": push_user, "push_code": push_code}


def save_config(config_file: str, csv_path: str, extra: Optional[Dict[str, Any]] = None) -> bool:
    """
    保存配置到文件

    Args:
        config_file: 配置文件路径
        csv_path:    CSV 文件路径
        extra:       额外配置项（如 push_user / push_code）

    Returns:
        保存成功返回 True，否则返回 False
    """
    try:
        # 如果配置文件已存在，先读取保留其他字段
        config: Dict[str, Any] = {}
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            except Exception:
                pass

        config["csv_path"] = csv_path
        config["initialized"] = True

        if extra:
            config.update(extra)

        # 确保目录存在
        parent = os.path.dirname(config_file)
        if parent:
            os.makedirs(parent, exist_ok=True)

        # 写入配置文件
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

        return True

    except Exception as e:
        print(f"\n保存配置文件时出错: {e}")
        return False


def initialize() -> bool:
    """
    执行初始化流程

    Returns:
        初始化成功返回 True，否则返回 False
    """
    # 获取默认配置文件路径
    script_dir = Path(__file__).parent.parent
    config_file = str(script_dir / "config.json")

    # 检查配置是否已存在
    if check_config(config_file):
        print("\n配置已存在，跳过初始化。")
        print(f"配置文件路径: {config_file}")

        # 读取并显示当前配置
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"CSV 路径: {config.get('csv_path', '未配置')}")
        except Exception:
            print("读取配置失败")

        return True

    # 执行初始化引导
    guide_export()

    # 提示用户输入 CSV 路径
    csv_path = prompt_csv_path()

    if csv_path is None:
        return False

    # 可选：推送服务配置
    push_config = prompt_push_config()

    # 保存配置
    print("\n正在保存配置...")
    if save_config(config_file, csv_path, extra=push_config if push_config else None):
        print("\n✓ 配置已成功保存")
        print(f"  配置文件: {config_file}")
        print(f"  CSV 路径: {csv_path}")
        if push_config:
            print(f"  推送账号: {push_config.get('push_user', '')}")
            print("  推送验证码: ******")
        print("\n现在可以使用 Quicker Connector 技能了！")
        return True
    else:
        print("\n✗ 配置保存失败，请检查是否有写入权限")
        return False


if __name__ == "__main__":
    success = initialize()
    exit(0 if success else 1)
