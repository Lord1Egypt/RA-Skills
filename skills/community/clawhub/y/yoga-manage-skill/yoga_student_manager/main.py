#!/usr/bin/env python3
"""
瑜伽学员管理系统 - 命令行入口
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import is_configured, prompt_email_config, prompt_alert_config, get_alert_thresholds
from manager import YogaManager


def print_menu():
    print("\n" + "=" * 60)
    print("          瑜伽学员课时管理系统")
    print("=" * 60)
    print("  1. 添加学员")
    print("  2. 查看所有学员")
    print("  3. 搜索学员")
    print("  4. 查看学员详情")
    print("  5. 修改学员信息")
    print("  6. 删除学员")
    print("  7. 添加课程")
    print("  8. 扣除课时")
    print("  9. 增加课时")
    print(" 10. 查看扣除记录")
    print(" 11. 发送完整报表")
    print(" 12. 配置邮箱")
    print(" 13. 配置提醒阈值")
    print("  0. 退出")
    print("=" * 60)


def input_int(prompt, default=None, min_val=None, max_val=None):
    """安全读取整数输入"""
    raw = input(prompt).strip()
    if not raw and default is not None:
        return default
    try:
        val = int(raw)
        if min_val is not None and val < min_val:
            print(f"数值不能小于 {min_val}")
            return None
        if max_val is not None and val > max_val:
            print(f"数值不能大于 {max_val}")
            return None
        return val
    except ValueError:
        print("请输入有效的数字")
        return None


def input_date(prompt, required=False):
    """读取日期输入，校验格式"""
    raw = input(prompt).strip()
    if not raw and not required:
        return None
    if raw and not re.match(r'^\d{4}-\d{2}-\d{2}$', raw):
        print("日期格式不正确，请使用 YYYY-MM-DD 格式")
        return None
    return raw


def main():
    manager = YogaManager()

    if not is_configured():
        print("首次使用，请先配置邮箱信息。")
        prompt_email_config()

    while True:
        print_menu()
        choice = input("请输入选项: ").strip()

        if choice == '1':
            name = input("学员姓名: ").strip()
            if not name:
                print("姓名不能为空")
                continue
            phone = input("电话 (可选): ").strip() or None
            wechat = input("微信 (可选): ").strip() or None
            notes = input("备注 (可选): ").strip() or None
            manager.add_student(name, phone, wechat, notes)

        elif choice == '2':
            manager.list_students()

        elif choice == '3':
            keyword = input("搜索关键词 (姓名/电话/微信): ").strip()
            if not keyword:
                print("请输入搜索关键词")
                continue
            manager.search_students(keyword)

        elif choice == '4':
            sid = input_int("学员ID: ", min_val=1)
            if sid is not None:
                manager.show_student(sid)

        elif choice == '5':
            sid = input_int("学员ID: ", min_val=1)
            if sid is None:
                continue
            print("输入新的信息（留空表示不修改）:")
            updates = {}
            name = input("姓名: ").strip()
            if name: updates['name'] = name
            phone = input("电话: ").strip()
            if phone: updates['phone'] = phone
            wechat = input("微信: ").strip()
            if wechat: updates['wechat'] = wechat
            notes = input("备注: ").strip()
            if notes: updates['notes'] = notes
            if updates:
                manager.update_student(sid, **updates)

        elif choice == '6':
            sid = input_int("要删除的学员ID: ", min_val=1)
            if sid is not None:
                confirm = input("确认删除？此操作不可恢复 (y/n): ").strip().lower()
                if confirm == 'y':
                    manager.delete_student(sid)

        elif choice == '7':
            sid = input_int("学员ID: ", min_val=1)
            if sid is None:
                continue
            print("课程类型: 1-线上课 2-线下课")
            ct = input("选择: ").strip()
            course_type = 'online' if ct == '1' else 'offline'
            print("套餐类型: 1-包年 2-包课时")
            pt = input("选择: ").strip()
            package_type = 'yearly' if pt == '1' else 'hourly'

            total_hours = remaining_hours = start_date = end_date = price = None
            if package_type == 'hourly':
                total_hours = input_int("总课时: ", min_val=1)
                if total_hours is None:
                    continue
                remaining_hours = total_hours
                price_input = input("总价 (可选): ").strip()
                price = float(price_input) if price_input else None
            else:
                start_date = input_date("开始日期 (YYYY-MM-DD): ", required=True)
                if start_date is None:
                    continue
                end_date = input_date("结束日期 (YYYY-MM-DD): ", required=True)
                if end_date is None:
                    continue
                price_input = input("总价 (可选): ").strip()
                price = float(price_input) if price_input else None

            manager.add_course(sid, course_type, package_type, total_hours, remaining_hours, start_date, end_date, price)

        elif choice == '8':
            cid = input_int("课程ID: ", min_val=1)
            if cid is None:
                continue
            hours = input_int("扣除课时数 (默认1): ", default=1, min_val=1)
            if hours is None:
                continue
            class_date = input_date("上课日期 (YYYY-MM-DD, 默认今天): ")
            notes = input("备注 (可选): ").strip() or None
            manager.deduct_hours(cid, hours, class_date, notes)

        elif choice == '9':
            cid = input_int("课程ID: ", min_val=1)
            if cid is None:
                continue
            hours = input_int("增加课时数: ", min_val=1)
            if hours is None:
                continue
            manager.add_hours(cid, hours)

        elif choice == '10':
            sid_input = input("学员ID (留空查看全部): ").strip()
            if sid_input:
                sid = input_int("学员ID: ", min_val=1)
                if sid is not None:
                    manager.show_logs(sid)
            else:
                manager.show_logs()

        elif choice == '11':
            manager.send_full_report()

        elif choice == '12':
            prompt_email_config()

        elif choice == '13':
            prompt_alert_config()

        elif choice == '0':
            print("再见！")
            break

        else:
            print("无效选项")


if __name__ == '__main__':
    main()
