#!/usr/bin/env python3
"""
微信联系人管理脚本
用于管理可发送消息的联系人列表

用法:
    python3 contact_manager.py --list              # 列出所有联系人
    python3 contact_manager.py --add "张三"         # 添加联系人
    python3 contact_manager.py --remove "李四"      # 移除联系人
    python3 contact_manager.py --validate          # 验证联系人有效性
"""

import argparse
import json
import sys
from pathlib import Path

# 联系人列表存储路径
CONTACTS_FILE = Path(__file__).parent.parent / ".contacts.json"


def load_contacts():
    """加载联系人列表"""
    if not CONTACTS_FILE.exists():
        return {"contacts": [], "groups": [], "last_updated": 0}
    
    try:
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"警告: 加载联系人失败: {e}")
        return {"contacts": [], "groups": [], "last_updated": 0}


def save_contacts(data):
    """保存联系人列表"""
    try:
        with open(CONTACTS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"错误: 保存联系人失败: {e}")
        return False


def add_contact(name, contact_type="user", validate=True):
    """
    添加联系人
    
    Args:
        name: 联系人备注名
        contact_type: 类型 (user/group)
        validate: 是否验证联系人存在
    
    Returns:
        bool: 是否成功
    """
    data = load_contacts()
    
    # 检查是否已存在
    if contact_type == "user":
        if name in data["contacts"]:
            print(f"联系人 '{name}' 已存在")
            return False
        data["contacts"].append(name)
    else:
        if name in data["groups"]:
            print(f"群聊 '{name}' 已存在")
            return False
        data["groups"].append(name)
    
    import time
    data["last_updated"] = int(time.time())
    
    if save_contacts(data):
        print(f"✅ 已添加 {contact_type}: '{name}'")
        return True
    return False


def remove_contact(name, contact_type="user"):
    """
    移除联系人
    
    Args:
        name: 联系人备注名
        contact_type: 类型 (user/group)
    
    Returns:
        bool: 是否成功
    """
    data = load_contacts()
    
    if contact_type == "user":
        if name not in data["contacts"]:
            print(f"联系人 '{name}' 不存在")
            return False
        data["contacts"].remove(name)
    else:
        if name not in data["groups"]:
            print(f"群聊 '{name}' 不存在")
            return False
        data["groups"].remove(name)
    
    import time
    data["last_updated"] = int(time.time())
    
    if save_contacts(data):
        print(f"✅ 已移除 {contact_type}: '{name}'")
        return True
    return False


def list_contacts():
    """列出所有联系人"""
    data = load_contacts()
    
    print("\n" + "=" * 50)
    print("📇 联系人列表")
    print("=" * 50)
    
    print("\n👤 个人联系人:")
    if data["contacts"]:
        for i, contact in enumerate(data["contacts"], 1):
            print(f"   {i}. {contact}")
    else:
        print("   (暂无)")
    
    print(f"\n👥 群聊 ({len(data['groups'])}个):")
    if data["groups"]:
        for i, group in enumerate(data["groups"], 1):
            print(f"   {i}. {group}")
    else:
        print("   (暂无)")
    
    import time
    last_updated = data.get("last_updated", 0)
    if last_updated:
        update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(last_updated))
        print(f"\n📝 最后更新: {update_time}")
    
    print("=" * 50 + "\n")


def validate_contacts():
    """
    验证联系人列表中的联系人是否有效
    通过检查微信会话是否存在来验证
    """
    # TODO: 实现与微信API的验证逻辑
    print("[功能开发中] 联系人验证需要接入微信会话API")
    print("建议: 先发送一条测试消息验证联系人是否可用")


def search_contact(keyword):
    """搜索联系人"""
    data = load_contacts()
    
    results = []
    
    # 搜索个人联系人
    for contact in data["contacts"]:
        if keyword.lower() in contact.lower():
            results.append(("user", contact))
    
    # 搜索群聊
    for group in data["groups"]:
        if keyword.lower() in group.lower():
            results.append(("group", group))
    
    if results:
        print(f"\n🔍 搜索结果 (关键字: '{keyword}'):")
        for contact_type, name in results:
            icon = "👤" if contact_type == "user" else "👥"
            print(f"   {icon} {name}")
    else:
        print(f"\n未找到匹配 '{keyword}' 的联系人")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description="微信联系人管理",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --list
  %(prog)s --add "张三"
  %(prog)s --add "工作群" --group
  %(prog)s --remove "李四"
  %(prog)s --search "张"
        """
    )
    
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有联系人"
    )
    
    parser.add_argument(
        "--add", "-a",
        metavar="NAME",
        help="添加联系人"
    )
    
    parser.add_argument(
        "--remove", "-r",
        metavar="NAME",
        help="移除联系人"
    )
    
    parser.add_argument(
        "--group", "-g",
        action="store_true",
        help="操作对象为群聊"
    )
    
    parser.add_argument(
        "--search", "-s",
        metavar="KEYWORD",
        help="搜索联系人"
    )
    
    parser.add_argument(
        "--validate",
        action="store_true",
        help="验证联系人有效性"
    )
    
    args = parser.parse_args()
    
    # 如果没有参数，默认列出
    if not any([args.list, args.add, args.remove, args.search, args.validate]):
        list_contacts()
        return
    
    # 执行操作
    if args.list:
        list_contacts()
    
    if args.add:
        contact_type = "group" if args.group else "user"
        add_contact(args.add, contact_type)
    
    if args.remove:
        contact_type = "group" if args.group else "user"
        remove_contact(args.remove, contact_type)
    
    if args.search:
        search_contact(args.search)
    
    if args.validate:
        validate_contacts()


if __name__ == "__main__":
    main()
