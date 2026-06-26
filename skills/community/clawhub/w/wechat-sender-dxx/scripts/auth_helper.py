#!/usr/bin/env python3
"""
微信发送授权验证助手
确保用户明确授权后才发送消息

用法:
    python3 auth_helper.py --check              # 检查授权状态
    python3 auth_helper.py --grant              # 授予授权
    python3 auth_helper.py --revoke             # 撤销授权
    python3 auth_helper.py --require "发送消息给张三"  # 请求特定授权
"""

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

# 授权文件路径
AUTH_FILE = Path(__file__).parent.parent / ".auth.json"

# 授权有效期（秒）- 默认1小时
AUTH_VALIDITY = 3600

# 危险操作列表
DANGEROUS_OPERATIONS = [
    "批量发送",
    "群发",
    "发送给陌生人",
    "自动发送"
]


def load_auth():
    """加载授权状态"""
    if not AUTH_FILE.exists():
        return {
            "granted": False,
            "granted_at": 0,
            "granted_operations": [],
            "denied_operations": [],
            "last_request": None
        }
    
    try:
        with open(AUTH_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {
            "granted": False,
            "granted_at": 0,
            "granted_operations": [],
            "denied_operations": [],
            "last_request": None
        }


def save_auth(data):
    """保存授权状态"""
    try:
        with open(AUTH_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"错误: 保存授权失败: {e}")
        return False


def is_authorized(operation="", require_explicit=False):
    """
    检查是否已授权
    
    Args:
        operation: 具体操作描述
        require_explicit: 是否需要显式授权
    
    Returns:
        bool: 是否已授权
    """
    auth = load_auth()
    
    # 检查是否有全局授权
    if auth.get("granted"):
        granted_at = auth.get("granted_at", 0)
        # 检查授权是否过期
        if time.time() - granted_at < AUTH_VALIDITY:
            # 检查是否是危险操作
            if operation and is_dangerous(operation):
                # 危险操作需要额外确认
                if operation in auth.get("granted_operations", []):
                    return True
                return False
            return True
    
    # 检查是否有特定操作授权
    if operation in auth.get("granted_operations", []):
        return True
    
    return False


def is_dangerous(operation):
    """检查操作是否属于危险操作"""
    operation_lower = operation.lower()
    for dangerous in DANGEROUS_OPERATIONS:
        if dangerous.lower() in operation_lower:
            return True
    return False


def request_auth(operation, auto_confirm=False):
    """
    请求用户授权
    
    Args:
        operation: 操作描述
        auto_confirm: 是否自动确认（仅用于测试）
    
    Returns:
        bool: 是否获得授权
    """
    if auto_confirm:
        grant_auth(operation)
        return True
    
    # 打印授权请求
    print("\n" + "=" * 60)
    print("🔐 授权请求")
    print("=" * 60)
    print(f"\n请求操作: {operation}")
    
    if is_dangerous(operation):
        print("\n⚠️  警告: 此操作涉及群发或批量发送，请谨慎确认！")
    
    print("\n选项:")
    print("  1. 同意本次 (y)")
    print("  2. 同意1小时内所有操作 (a)")
    print("  3. 拒绝 (n)")
    print("=" * 60)
    
    # 在OpenClaw环境中，这个交互需要特殊处理
    # 实际使用时通过对话确认
    print("\n[在OpenClaw中，此授权需通过对话确认]")
    print("请回复: '确认发送' 以授权此操作")
    
    return False


def grant_auth(operation="", duration=AUTH_VALIDITY):
    """
    授予授权
    
    Args:
        operation: 特定操作（空字符串表示全局授权）
        duration: 授权有效期（秒）
    """
    auth = load_auth()
    
    if operation:
        # 特定操作授权
        if operation not in auth.get("granted_operations", []):
            auth.setdefault("granted_operations", []).append(operation)
            print(f"✅ 已授权操作: {operation}")
    else:
        # 全局授权
        auth["granted"] = True
        auth["granted_at"] = time.time()
        auth["duration"] = duration
        print(f"✅ 已授予全局授权，有效期 {duration//3600} 小时")
    
    save_auth(auth)


def revoke_auth(operation=""):
    """
    撤销授权
    
    Args:
        operation: 特定操作（空字符串表示撤销全局授权）
    """
    auth = load_auth()
    
    if operation:
        # 撤销特定操作授权
        if operation in auth.get("granted_operations", []):
            auth["granted_operations"].remove(operation)
            print(f"✅ 已撤销授权: {operation}")
    else:
        # 撤销全局授权
        auth["granted"] = False
        auth["granted_at"] = 0
        auth["granted_operations"] = []
        print("✅ 已撤销所有授权")
    
    save_auth(auth)


def check_auth_status():
    """检查并显示授权状态"""
    auth = load_auth()
    
    print("\n" + "=" * 50)
    print("🔐 授权状态")
    print("=" * 50)
    
    if auth.get("granted"):
        granted_at = auth.get("granted_at", 0)
        elapsed = time.time() - granted_at
        remaining = AUTH_VALIDITY - elapsed
        
        if remaining > 0:
            print(f"✅ 全局授权状态: 已授权")
            print(f"   授权时间: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(granted_at))}")
            print(f"   剩余时间: {remaining//60} 分钟")
        else:
            print(f"⚠️  全局授权状态: 已过期")
    else:
        print(f"❌ 全局授权状态: 未授权")
    
    # 特定操作授权
    granted_ops = auth.get("granted_operations", [])
    if granted_ops:
        print(f"\n📋 已授权操作 ({len(granted_ops)}项):")
        for op in granted_ops:
            print(f"   • {op}")
    
    denied_ops = auth.get("denied_operations", [])
    if denied_ops:
        print(f"\n🚫 已拒绝操作 ({len(denied_ops)}项):")
        for op in denied_ops:
            print(f"   • {op}")
    
    print("=" * 50 + "\n")


def generate_auth_token(operation, timestamp=None):
    """
    生成授权令牌（用于验证）
    
    Args:
        operation: 操作描述
        timestamp: 时间戳
    
    Returns:
        str: 授权令牌
    """
    if timestamp is None:
        timestamp = int(time.time())
    
    # 简单哈希生成令牌
    data = f"{operation}:{timestamp}:wechat-sender"
    return hashlib.sha256(data.encode()).hexdigest()[:16]


def main():
    parser = argparse.ArgumentParser(
        description="微信发送授权管理",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--check", "-c",
        action="store_true",
        help="检查授权状态"
    )
    
    parser.add_argument(
        "--grant", "-g",
        action="store_true",
        help="授予授权"
    )
    
    parser.add_argument(
        "--revoke", "-r",
        action="store_true",
        help="撤销授权"
    )
    
    parser.add_argument(
        "--require",
        metavar="OPERATION",
        help="请求特定授权"
    )
    
    parser.add_argument(
        "--operation", "-o",
        metavar="OP",
        help="指定操作名称"
    )
    
    args = parser.parse_args()
    
    # 如果没有参数，默认检查状态
    if not any([args.check, args.grant, args.revoke, args.require]):
        check_auth_status()
        return
    
    if args.check:
        check_auth_status()
    
    if args.grant:
        grant_auth(args.operation or "")
    
    if args.revoke:
        revoke_auth(args.operation or "")
    
    if args.require:
        if is_authorized(args.require):
            print(f"✅ 已授权: {args.require}")
        else:
            request_auth(args.require)


if __name__ == "__main__":
    main()
