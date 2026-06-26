#!/usr/bin/env python3
"""
一体化打印机驱动搜索下载脚本
用法: python download_printer.py <打印机型号> [下载目录] [--arch <架构>]
示例: python download_printer.py "联想 LJ2405" ~/Desktop
      python download_printer.py "联想 LJ2405" ~/Desktop --arch arm64
"""

import sys
from driver_utils import search_drivers, download_driver, display_driver_list, select_drivers, build_download_dir


def main():
    args = sys.argv[1:]
    if not args:
        print("用法: python download_printer.py <打印机型号> [下载目录] [--arch <架构>]")
        print("示例: python download_printer.py \"联想 LJ2405\" ~/Desktop --arch arm64")
        sys.exit(1)

    printer_model = args[0]
    download_dir = "."
    preferred_arch = "amd64"

    i = 1
    while i < len(args):
        if args[i] == "--arch" and i + 1 < len(args):
            preferred_arch = args[i + 1]
            i += 2
        else:
            download_dir = args[i]
            i += 1

    print(f"搜索打印机驱动: {printer_model}")
    drivers = search_drivers(printer_model)

    if not drivers:
        print(f"没有找到与 '{printer_model}' 相关的驱动")
        sys.exit(1)

    display_driver_list(drivers)
    print(f"\n共找到 {len(drivers)} 个驱动")

    selected_drivers = select_drivers(drivers, preferred_arch)
    if not selected_drivers:
        print("无法选择驱动")
        sys.exit(1)

    print(f"\n将下载 {len(selected_drivers)} 个驱动:")
    for d in selected_drivers:
        print(f"  - {d.get('model')} ({d.get('arch')})")

    failed = 0
    for selected in selected_drivers:
        full_dir = build_download_dir(download_dir, selected.get('model', 'unknown'))
        success, filepath = download_driver(selected, full_dir)
        if not success:
            failed += 1

    if failed == 0:
        print(f"\n全部 {len(selected_drivers)} 个驱动下载成功！")
    else:
        print(f"\n{len(selected_drivers) - failed} 个成功，{failed} 个失败")


if __name__ == "__main__":
    main()
