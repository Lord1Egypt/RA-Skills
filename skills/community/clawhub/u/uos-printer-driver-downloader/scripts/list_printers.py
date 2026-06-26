#!/usr/bin/env python3
"""
打印机驱动搜索脚本
用法: python list_printers.py [打印机型号关键词]
示例: python list_printers.py LJ2405
"""

import json
import sys
from driver_utils import search_drivers, display_driver_list


def save_all_drivers(drivers, filename="driver_list.json"):
    """保存所有搜索到的驱动信息到JSON文件"""
    normalized_drivers = []
    for item in drivers:
        driver_info = {
            "deb_id": item.get("deb_id"),
            "driver_id": item.get("driver_id"),
            "package": item.get("package"),
            "model": item.get("model"),
            "arch": item.get("arch"),
            "version": item.get("version")
        }
        normalized_drivers.append(driver_info)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(normalized_drivers, f, ensure_ascii=False, indent=2)

    return filename


def main():
    if len(sys.argv) > 1:
        keyword = sys.argv[1].strip()
        if not keyword:
            print("用法: python list_printers.py [打印机型号关键词]")
            print("示例: python list_printers.py LJ2405")
            return
    else:
        keyword = input("请输入打印机型号关键词 (例如 1102): ").strip()
        if not keyword:
            return

    print(f"正在搜索: {keyword}")
    drivers = search_drivers(keyword)

    if not drivers:
        print("没有找到驱动。")
        return

    display_driver_list(drivers)

    print(f"\n共找到 {len(drivers)} 个驱动")
    save_path = save_all_drivers(drivers)
    print(f"驱动列表已保存到: {save_path}")
    print("\n请运行第二个脚本下载驱动: python download_driver.py")


if __name__ == "__main__":
    main()
