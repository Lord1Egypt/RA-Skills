#!/usr/bin/env python3
"""
从 driver_list.json 选择并下载驱动
用法: python download_driver.py [--index N] [--arch <架构>] [--output <目录>]
示例: python download_driver.py
      python download_driver.py --index 2
      python download_driver.py --arch arm64 --output ~/Desktop
"""

import json
import os
import sys
from driver_utils import download_driver, display_driver_list, select_drivers, build_download_dir


def load_driver_list(filename="driver_list.json"):
    """从JSON文件加载驱动列表"""
    if not os.path.exists(filename):
        print(f"错误：找不到驱动列表文件 '{filename}'")
        print("请先运行 list_printers.py 搜索并保存驱动列表。")
        return None

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)

        if isinstance(data, dict):
            return [data]
        elif isinstance(data, list):
            return data
        else:
            print("错误：驱动列表格式无效。")
            return None

    except Exception as e:
        print(f"读取驱动列表文件失败：{e}")
        return None


def main():
    index = None
    preferred_arch = "amd64"
    output_dir = os.path.expanduser("~/Desktop")

    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--index" and i + 1 < len(args):
            try:
                index = int(args[i + 1])
            except ValueError:
                print(f"错误：--index 参数必须是数字，收到: {args[i + 1]}")
                sys.exit(1)
            i += 2
        elif args[i] == "--arch" and i + 1 < len(args):
            preferred_arch = args[i + 1]
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_dir = os.path.expanduser(args[i + 1])
            i += 2
        else:
            print(f"未知参数: {args[i]}")
            print("用法: python download_driver.py [--index N] [--arch <架构>] [--output <目录>]")
            sys.exit(1)

    drivers = load_driver_list()
    if drivers is None or not drivers:
        sys.exit(1)

    display_driver_list(drivers)

    if index is not None:
        if 1 <= index <= len(drivers):
            selected_drivers = [drivers[index - 1]]
        else:
            print(f"序号 {index} 超出范围 (1-{len(drivers)})")
            sys.exit(1)
    else:
        selected_drivers = select_drivers(drivers, preferred_arch)
        if not selected_drivers:
            print("无法选择驱动")
            sys.exit(1)
        print(f"\n将下载 {len(selected_drivers)} 个驱动:")
        for d in selected_drivers:
            print(f"  - {d.get('model')} ({d.get('arch')})")

    failed = 0
    for selected in selected_drivers:
        full_dir = build_download_dir(output_dir, selected.get('model', 'unknown'))
        success, filepath = download_driver(selected, full_dir)
        if not success:
            failed += 1

    if failed == 0:
        print(f"\n全部 {len(selected_drivers)} 个驱动下载成功！")
    else:
        print(f"\n{len(selected_drivers) - failed} 个成功，{failed} 个失败")


if __name__ == "__main__":
    main()
