#!/usr/bin/env python3
"""
同步用户信息到zworker
从标准输入或参数读取用户列表，调用zworker API
"""

import json
import sys
import argparse
from zworker_api import set_user_info, ZworkerAPIError

def read_users_from_stdin() -> list:
    """从标准输入读取用户列表JSON"""
    try:
        data = sys.stdin.read().strip()
        if not data:
            return []
        users = json.loads(data)
        if isinstance(users, list):
            return users
        elif isinstance(users, dict) and 'users' in users:
            return users['users']
        else:
            print(f"错误: 无法解析的用户数据格式: {data[:100]}", file=sys.stderr)
            return []
    except json.JSONDecodeError as e:
        print(f"错误: JSON解析失败: {e}", file=sys.stderr)
        return []

def validate_user(user: dict) -> bool:
    """验证单个用户对象格式"""
    if not isinstance(user, dict):
        return False
    if 'channel' not in user or not isinstance(user['channel'], str):
        return False
    if 'userid' not in user or not isinstance(user['userid'], str):
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description='同步用户信息到zworker')
    parser.add_argument('--users', type=str, help='用户列表JSON字符串，格式: [{"channel":"xxx","userid":"xxx"},...]')
    parser.add_argument('--file', type=str, help='包含用户列表的JSON文件路径')
    
    args = parser.parse_args()
    
    users = []
    
    # 从不同来源读取用户数据
    if args.users:
        try:
            data = json.loads(args.users)
            if isinstance(data, list):
                users = data
            elif isinstance(data, dict) and 'users' in data:
                users = data['users']
            else:
                print("错误: --users 参数必须是用户列表或包含'users'键的对象", file=sys.stderr)
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"错误: 解析--users参数失败: {e}", file=sys.stderr)
            sys.exit(1)
    elif args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    users = data
                elif isinstance(data, dict) and 'users' in data:
                    users = data['users']
                else:
                    print("错误: 文件内容必须是用户列表或包含'users'键的对象", file=sys.stderr)
                    sys.exit(1)
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f"错误: 读取文件失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # 从标准输入读取
        users = read_users_from_stdin()
    
    if not users:
        print("错误: 未提供用户数据", file=sys.stderr)
        print("使用方式:", file=sys.stderr)
        print("  1. 通过管道传递JSON: echo '[{\"channel\":\"webchat\",\"userid\":\"user1\"}]' | python3 sync_users.py", file=sys.stderr)
        print("  2. 通过参数传递: python3 sync_users.py --users '[{\"channel\":\"webchat\",\"userid\":\"user1\"}]'", file=sys.stderr)
        print("  3. 通过文件传递: python3 sync_users.py --file users.json", file=sys.stderr)
        sys.exit(1)
    
    # 验证用户数据
    valid_users = []
    for i, user in enumerate(users):
        if validate_user(user):
            valid_users.append(user)
        else:
            print(f"警告: 跳过无效的用户数据(索引{i}): {user}", file=sys.stderr)
    
    if not valid_users:
        print("错误: 没有有效的用户数据", file=sys.stderr)
        sys.exit(1)
    
    print(f"准备同步 {len(valid_users)} 个用户到zworker...", file=sys.stderr)
    
    try:
        result = set_user_info(valid_users)
        if result.get('success'):
            print("✅ 用户信息同步成功")
            sys.exit(0)
        else:
            print("❌ 用户信息同步失败: API返回success=false", file=sys.stderr)
            sys.exit(1)
    except ZworkerAPIError as e:
        print(f"❌ 用户信息同步失败: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()