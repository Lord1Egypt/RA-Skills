#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小红书代理管理器 - 实现多账号 IP 隔离

功能：
1. 管理代理池（添加、删除、启用/禁用）
2. 为不同账号分配不同的代理
3. 代理延迟测试
4. 随机获取可用代理
5. 导出代理配置（用于 requests/curl/等）

使用场景：
- 小红书多账号运营（每个账号使用不同 IP）
- 避免同 IP 多账号被封
- 模拟真实用户行为
"""

import argparse
import json
import os
import sys
import random
import time
import requests
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# 配置文件路径
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / "skills" / "xiaohongshu-proxy-manager" / "config"
CONFIG_FILE = CONFIG_DIR / "proxies.json"

# 默认配置
DEFAULT_CONFIG = {
    "proxies": [],
    "account_mapping": {},
    "test_timeout": 10,
    "test_url": "https://www.baidu.com"
}


def load_config() -> Dict:
    """加载配置文件"""
    if not CONFIG_FILE.exists():
        print(f"⚠️  配置文件不存在：{CONFIG_FILE}")
        print("💡 创建默认配置文件...")
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ 加载配置失败：{e}")
        return DEFAULT_CONFIG.copy()


def save_config(config: Dict):
    """保存配置文件"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def list_proxies(config: Dict):
    """列出所有代理"""
    proxies = config.get("proxies", [])

    if not proxies:
        print("📭 代理池为空")
        return

    print(f"📋 代理列表（共 {len(proxies)} 个）：")
    print()

    for i, proxy in enumerate(proxies, 1):
        status = "✅ 启用" if proxy.get("enabled", True) else "❌ 禁用"
        print(f"{i}. 【{proxy.get('name', proxy.get('id', ''))}】")
        print(f"   ID: {proxy.get('id', '')}")
        print(f"   地址: {proxy['protocol']}://{proxy['host']}:{proxy['port']}")
        if proxy.get("username"):
            print(f"   用户名: {proxy['username']}")
        print(f"   状态: {status}")
        print()


def test_proxy(proxy: Dict, test_url: str, timeout: int) -> Tuple[bool, float]:
    """测试单个代理"""
    proxy_url = f"{proxy['protocol']}://"
    if proxy.get("username") and proxy.get("password"):
        proxy_url += f"{proxy['username']}:{proxy['password']}@"
    proxy_url += f"{proxy['host']}:{proxy['port']}"

    proxies_dict = {
        "http": proxy_url,
        "https": proxy_url
    }

    try:
        start_time = time.time()
        response = requests.get(test_url, proxies=proxies_dict, timeout=timeout)
        elapsed = time.time() - start_time

        if response.status_code == 200:
            return True, elapsed
        else:
            return False, elapsed
    except Exception as e:
        return False, 0.0


def test_proxy_by_id(config: Dict, proxy_id: str):
    """测试指定代理"""
    proxies = config.get("proxies", [])
    target = None

    for proxy in proxies:
        if proxy.get("id") == proxy_id:
            target = proxy
            break

    if not target:
        print(f"❌ 未找到代理：{proxy_id}")
        return

    print(f"🧪 测试代理：{target.get('name', proxy_id)}")
    print(f"   地址: {target['protocol']}://{target['host']}:{target['port']}")

    test_url = config.get("test_url", "https://www.baidu.com")
    timeout = config.get("test_timeout", 10)

    success, elapsed = test_proxy(target, test_url, timeout)

    if success:
        print(f"✅ 测试成功！延迟: {elapsed*1000:.0f}ms")
    else:
        print(f"❌ 测试失败！代理不可用")


def test_all_proxies(config: Dict):
    """测试所有代理"""
    proxies = config.get("proxies", [])

    if not proxies:
        print("📭 代理池为空，无需测试")
        return

    print(f"🧪 测试所有代理（共 {len(proxies)} 个）...")
    print()

    test_url = config.get("test_url", "https://www.baidu.com")
    timeout = config.get("test_timeout", 10)

    results = []

    for proxy in proxies:
        if not proxy.get("enabled", True):
            continue

        name = proxy.get("name", proxy.get("id", ""))
        print(f"测试 {name}...", end=" ")

        success, elapsed = test_proxy(proxy, test_url, timeout)

        if success:
            print(f"✅ {elapsed*1000:.0f}ms")
            results.append((proxy, True, elapsed))
        else:
            print(f"❌ 失败")
            results.append((proxy, False, 0.0))

    print()
    print("📊 测试结果汇总：")
    success_count = sum(1 for _, success, _ in results if success)
    print(f"   成功: {success_count}/{len(results)}")

    if success_count > 0:
        avg_delay = sum(elapsed for _, success, elapsed in results if success) / success_count
        print(f"   平均延迟: {avg_delay*1000:.0f}ms")


def get_proxy_by_account(config: Dict, account_id: str):
    """为指定账号获取代理"""
    account_mapping = config.get("account_mapping", {})

    if account_id not in account_mapping:
        print(f"❌ 账号 {account_id} 未配置代理")
        print("💡 使用 --map 命令绑定账号和代理")
        return

    proxy_id = account_mapping[account_id]
    proxies = config.get("proxies", [])

    for proxy in proxies:
        if proxy.get("id") == proxy_id:
            if not proxy.get("enabled", True):
                print(f"⚠️  代理 {proxy_id} 已禁用")
                return

            # 输出代理配置
            proxy_url = f"{proxy['protocol']}://"
            if proxy.get("username") and proxy.get("password"):
                proxy_url += f"{proxy['username']}:{proxy['password']}@"
            proxy_url += f"{proxy['host']}:{proxy['port']}"

            print(f"📦 账号 {account_id} 的代理配置：")
            print(f"   HTTP_PROXY={proxy_url}")
            print(f"   HTTPS_PROXY={proxy_url}")
            print()
            print("💻 Python requests 用法：")
            print(f"   proxies = {{'http': '{proxy_url}', 'https': '{proxy_url}'}}")
            print(f"   response = requests.get(url, proxies=proxies)")
            print()
            print("🐘 curl 用法：")
            print(f"   curl -x '{proxy_url}' https://example.com")
            return

    print(f"❌ 未找到代理：{proxy_id}")


def get_random_proxy(config: Dict):
    """随机获取一个可用代理"""
    proxies = config.get("proxies", [])
    enabled_proxies = [p for p in proxies if p.get("enabled", True)]

    if not enabled_proxies:
        print("❌ 没有可用的代理")
        return

    proxy = random.choice(enabled_proxies)

    # 输出代理配置
    proxy_url = f"{proxy['protocol']}://"
    if proxy.get("username") and proxy.get("password"):
        proxy_url += f"{proxy['username']}:{proxy['password']}@"
    proxy_url += f"{proxy['host']}:{proxy['port']}"

    print(f"🎲 随机代理：{proxy.get('name', proxy.get('id', ''))}")
    print(f"   HTTP_PROXY={proxy_url}")
    print(f"   HTTPS_PROXY={proxy_url}")


def add_proxy(config: Dict, args):
    """添加代理"""
    proxy_id = args.id or f"proxy{len(config.get('proxies', [])) + 1}"

    proxy = {
        "id": proxy_id,
        "name": args.name or proxy_id,
        "protocol": args.protocol,
        "host": args.host,
        "port": args.port,
        "username": args.username or "",
        "password": args.password or "",
        "enabled": True
    }

    if "proxies" not in config:
        config["proxies"] = []

    config["proxies"].append(proxy)
    save_config(config)

    print(f"✅ 代理已添加：{proxy_id}")


def remove_proxy(config: Dict, proxy_id: str):
    """删除代理"""
    proxies = config.get("proxies", [])
    proxies = [p for p in proxies if p.get("id") != proxy_id]
    config["proxies"] = proxies
    save_config(config)

    print(f"✅ 代理已删除：{proxy_id}")


def enable_proxy(config: Dict, proxy_id: str):
    """启用代理"""
    for proxy in config.get("proxies", []):
        if proxy.get("id") == proxy_id:
            proxy["enabled"] = True
            save_config(config)
            print(f"✅ 代理已启用：{proxy_id}")
            return

    print(f"❌ 未找到代理：{proxy_id}")


def disable_proxy(config: Dict, proxy_id: str):
    """禁用代理"""
    for proxy in config.get("proxies", []):
        if proxy.get("id") == proxy_id:
            proxy["enabled"] = False
            save_config(config)
            print(f"✅ 代理已禁用：{proxy_id}")
            return

    print(f"❌ 未找到代理：{proxy_id}")


def map_account(config: Dict, account_id: str, proxy_id: str):
    """绑定账号和代理"""
    if "account_mapping" not in config:
        config["account_mapping"] = {}

    config["account_mapping"][account_id] = proxy_id
    save_config(config)

    print(f"✅ 账号 {account_id} 已绑定代理 {proxy_id}")


def main():
    parser = argparse.ArgumentParser(
        description="小红书代理管理器 - 实现多账号 IP 隔离",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法：

# 添加代理
xiaohongshu-proxy-manager --add \\
 1.1.1.1:1234 \\
  --username user123 \\
  --password pass456 \\
  --protocol http \\
  --name "代理1"

# 为账号绑定代理
xiaohongshu-proxy-manager --map account1 proxy1

# 获取账号的代理配置
xiaohongshu-proxy-manager --account account1

# 随机获取可用代理
xiaohongshu-proxy-manager --random

# 测试所有代理
xiaohongshu-proxy-manager --test-all

# 列出所有代理
xiaohongshu-proxy-manager --list

配置文件位置：
~/.openclaw/workspace/skills/xiaohongshu-proxy-manager/config/proxies.json
        """
    )

    # 查操作
    parser.add_argument("--list", action="store_true", help="列出所有代理")
    parser.add_argument("--account", help="获取指定账号的代理")
    parser.add_argument("--random", action="store_true", help="随机获取可用代理")
    parser.add_argument("--test", help="测试指定代理")
    parser.add_argument("--test-all", action="store_true", help="测试所有代理")

    # 写操作
    parser.add_argument("--add", help="添加代理（格式：host:port）")
    parser.add_argument("--id", help="代理ID（默认自动生成）")
    parser.add_argument("--name", help="代理名称")
    parser.add_argument("--protocol", default="http", choices=["http", "https", "socks5"], help="代理协议")
    parser.add_argument("--username", help="代理用户名")
    parser.add_argument("--password", help="代理密码")
    parser.add_argument("--remove", help="删除代理")
    parser.add_argument("--enable", help="启用代理")
    parser.add_argument("--disable", help="禁用代理")
    parser.add_argument("--map", nargs=2, metavar=("ACCOUNT", "PROXY"), help="绑定账号和代理")

    args = parser.parse_args()

    # 加载配置
    config = load_config()

    # 执行操作
    if args.list:
        list_proxies(config)
    elif args.account:
        get_proxy_by_account(config, args.account)
    elif args.random:
        get_random_proxy(config)
    elif args.test:
        test_proxy_by_id(config, args.test)
    elif args.test_all:
        test_all_proxies(config)
    elif args.add:
        # 解析 host:port
        if ":" not in args.add:
            print("❌ 错误：代理地址格式应为 host:port")
            sys.exit(1)

        host, port = args.add.split(":", 1)
        try:
            port = int(port)
        except ValueError:
            print("❌ 错误：端口必须是数字")
            sys.exit(1)

        add_proxy(config, argparse.Namespace(
            id=args.id,
            name=args.name,
            protocol=args.protocol,
            host=host,
            port=port,
            username=args.username,
            password=args.password
        ))
    elif args.remove:
        remove_proxy(config, args.remove)
    elif args.enable:
        enable_proxy(config, args.enable)
    elif args.disable:
        disable_proxy(config, args.disable)
    elif args.map:
        map_account(config, args.map[0], args.map[1])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
