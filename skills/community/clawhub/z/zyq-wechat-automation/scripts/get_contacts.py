"""
获取微信通讯录脚本
用法：
  python get_contacts.py [type]
  type: friends | groups | enterprise
"""
import sys
import os
import argparse
import json

sys.path.insert(0, r'D:\code\pywechat3')

def get_friends():
    try:
        from pywechat.WechatAuto import Contacts
        friends = Contacts.get_friends_info()
        print(f"\n{'='*60}")
        print(f"  微信好友通讯录（共 {len(friends)} 位）")
        print(f"{'='*60}\n")
        for i, friend in enumerate(friends, 1):
            name = friend.get("name", "未知")
            remark = friend.get("remark", "")
            wechat_id = friend.get("wechat_id", "")
            source = friend.get("source", "")
            region = friend.get("region", "")
            print(f"  [{i}] {remark or name} | 微信号: {wechat_id or '未知'} | 来源: {source} | 地区: {region}")
        print(f"\n{'='*60}")
        return True
    except Exception as e:
        print(f"[✗] 获取好友列表失败: {e}")
        return False

def get_groups():
    try:
        from pywechat.WechatAuto import Contacts
        groups = Contacts.get_groups_info()
        print(f"\n{'='*60}")
        print(f"  群聊列表（共 {len(groups)} 个）")
        print(f"{'='*60}\n")
        for i, group in enumerate(groups, 1):
            name = group.get("name", "未知群")
            count = group.get("member_count", 0)
            print(f"  [{i}] {name} ({count}人)")
        print(f"\n{'='*60}")
        return True
    except Exception as e:
        print(f"[✗] 获取群聊列表失败: {e}")
        return False

def get_enterprise():
    try:
        from pywechat.WechatAuto import Contacts
        friends = Contacts.get_enterprise_friends()
        print(f"\n{'='*60}")
        print(f"  企业微信好友（共 {len(friends)} 位）")
        print(f"{'='*60}\n")
        for i, friend in enumerate(friends, 1):
            name = friend.get("name", "未知")
            corp = friend.get("corp_name", "")
            print(f"  [{i}] {name} | 企业: {corp}")
        print(f"\n{'='*60}")
        return True
    except Exception as e:
        print(f"[✗] 获取企业微信好友失败: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="获取微信通讯录")
    parser.add_argument("type", nargs="?", choices=["friends", "groups", "enterprise"], default="friends",
                        help="类型: friends(默认) | groups | enterprise")
    args = parser.parse_args()

    if args.type == "friends":
        return get_friends()
    elif args.type == "groups":
        return get_groups()
    elif args.type == "enterprise":
        return get_enterprise()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
