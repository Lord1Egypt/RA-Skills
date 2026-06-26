#!/usr/bin/env python3
"""
V2EX 帖子监控工具
每小时监控指定节点的新帖子，生成总结报告
"""

import argparse
import hashlib
import json
import os
import ssl
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import urllib3
from urllib3.util.ssl_ import create_urllib3_context

try:
    import requests
    from requests.adapters import HTTPAdapter
except ImportError:
    requests = None
    HTTPAdapter = None

# 禁用 SSL 警告
urllib3.disable_warnings()

# 尝试创建宽松的 SSL 上下文
try:
    _create_unverified_https_context = create_urllib3_context()
except AttributeError:
    # 旧版本 urllib3
    _create_unverified_https_context = ssl._create_unverified_context

BASE_DIR = Path(__file__).resolve().parent
CONFIG_FILE = BASE_DIR / "v2ex_monitor_config.json"
DATA_DIR = BASE_DIR / "v2ex_monitor_data"
REPORT_FILE = BASE_DIR / "v2ex_hourly_report.md"
SEEN_TOPICS_FILE = DATA_DIR / "seen_topics.json"
SEEN_NOTIFICATIONS_FILE = DATA_DIR / "seen_notifications.json"

DEFAULT_NODES = ["python", "linux", "programmer", "hardware", "macos"]
DEFAULT_API_KEY = ""
BASE_URL = "https://www.v2ex.com/api/v2"


class V2EXMonitor:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = None
        if requests is not None and HTTPAdapter is not None:
            self.session = requests.Session()
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "V2EX-Monitor/1.0"
            })
            # 添加重试和连接池配置
            adapter = HTTPAdapter(
                max_retries=3,
                pool_connections=10,
                pool_maxsize=10
            )
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)
            # 禁用 SSL 验证警告但保持验证
            self.session.verify = True

    def get_node_topics(self, node_name: str, page: int = 1) -> list:
        """获取节点主题列表"""
        url = f"{BASE_URL}/nodes/{node_name}/topics"
        params = {"p": page}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "V2EX-Monitor/1.0"
        }
        try:
            # 尝试使用 urllib3（更稳定）
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib3.PoolManager(ssl_context=ctx) as pool:
                resp = pool.request("GET", url, fields=params, headers=headers, timeout=10)
                data = json.loads(resp.data.decode("utf-8"))
                return data.get("result", []) if isinstance(data, dict) else data
        except Exception as e:
            # 备用：尝试 requests
            try:
                if self.session is None:
                    raise RuntimeError("requests 未安装，跳过 requests 回退")
                resp = self.session.get(url, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                return data.get("result", []) if isinstance(data, dict) else data
            except Exception as e2:
                print(f"获取节点 {node_name} 失败: {e2}")
                return []

    def get_topic_detail(self, topic_id: int) -> dict:
        """获取主题详情"""
        url = f"{BASE_URL}/topics/{topic_id}"
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "User-Agent": "V2EX-Monitor/1.0"
            }
            with urllib3.PoolManager(ssl_context=ctx) as pool:
                resp = pool.request("GET", url, headers=headers, timeout=10)
                data = json.loads(resp.data.decode("utf-8"))
                return data.get("result", {}) if isinstance(data, dict) else data
        except Exception as e:
            try:
                if self.session is None:
                    raise RuntimeError("requests 未安装，跳过 requests 回退")
                resp = self.session.get(url, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                return data.get("result", {}) if isinstance(data, dict) else data
            except Exception as e2:
                print(f"获取主题 {topic_id} 失败: {e2}")
                return {}

    def get_notifications(self, page: int = 1) -> list:
        """获取提醒通知"""
        url = f"{BASE_URL}/notifications"
        params = {"p": page}
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "User-Agent": "V2EX-Monitor/1.0"
        }
        try:
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            with urllib3.PoolManager(ssl_context=ctx) as pool:
                resp = pool.request("GET", url, fields=params, headers=headers, timeout=10)
                data = json.loads(resp.data.decode("utf-8"))
                return data.get("result", []) if isinstance(data, dict) else data
        except Exception as e:
            try:
                if self.session is None:
                    raise RuntimeError("requests 未安装，跳过 requests 回退")
                resp = self.session.get(url, params=params, timeout=10)
                resp.raise_for_status()
                data = resp.json()
                return data.get("result", []) if isinstance(data, dict) else data
            except Exception as e2:
                print(f"获取提醒失败: {e2}")
                return []


def load_config() -> dict:
    """加载配置"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"nodes": DEFAULT_NODES, "apikey": DEFAULT_API_KEY}


def save_config(config: dict):
    """保存配置"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_seen_topics() -> set:
    """加载已处理的主题ID"""
    if SEEN_TOPICS_FILE.exists():
        with open(SEEN_TOPICS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_seen_topics(seen: set):
    """保存已处理的主题ID"""
    DATA_DIR.mkdir(exist_ok=True)
    with open(SEEN_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f)


def _notification_key(notification: dict) -> str:
    """为提醒生成稳定的去重键。"""
    if notification.get("id") is not None:
        return f"id:{notification['id']}"

    raw = json.dumps(notification, ensure_ascii=False, sort_keys=True)
    return "hash:" + hashlib.sha1(raw.encode("utf-8")).hexdigest()


def load_seen_notifications() -> set:
    """加载已处理的提醒键"""
    if SEEN_NOTIFICATIONS_FILE.exists():
        with open(SEEN_NOTIFICATIONS_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f))
    return set()


def save_seen_notifications(seen: set):
    """保存已处理的提醒键"""
    DATA_DIR.mkdir(exist_ok=True)
    with open(SEEN_NOTIFICATIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f, ensure_ascii=False, indent=2)


def generate_report(new_topics: list, notifications: list, nodes: Optional[list] = None) -> str:
    """生成每小时报告"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = []
    report.append(f"# V2EX 帖子监控报告")
    report.append(f"\n生成时间: {now}\n")

    # 新帖子统计
    report.append(f"## 新帖子统计")
    report.append(f"- 本次发现新帖子: **{len(new_topics)}** 篇")
    report.append(f"- 收到新提醒: **{len(notifications)}** 条\n")

    if new_topics:
        # 按节点分组
        by_node = {}
        for topic in new_topics:
            node = topic.get("_source_node", "未知")
            if node not in by_node:
                by_node[node] = []
            by_node[node].append(topic)

        report.append("## 各节点新帖子")
        for node, topics in by_node.items():
            report.append(f"\n### {node} ({len(topics)} 篇)")
            # 按回复数排序
            topics_sorted = sorted(topics, key=lambda x: x.get("replies", 0), reverse=True)
            for topic in topics_sorted[:10]:  # 每节点最多显示10篇
                title = topic.get("title", "无标题")
                replies = topic.get("replies", 0)
                tid = topic.get("id", "")
                url = f"https://www.v2ex.com/t/{tid}"
                report.append(f"- [{title}]({url}) - {replies} 回复")

    # 热门帖子（本周）
    if new_topics:
        report.append("\n## 热门新帖子 (按回复数)")
        hot_topics = sorted(new_topics, key=lambda x: x.get("replies", 0), reverse=True)[:10]
        for topic in hot_topics:
            title = topic.get("title", "无标题")
            replies = topic.get("replies", 0)
            node = topic.get("_source_node", "未知")
            tid = topic.get("id", "")
            url = f"https://www.v2ex.com/t/{tid}"
            report.append(f"- [{title}]({url}) - {replies} 回复 [{node}]")

    report.append("\n---\n*由 V2EX Monitor Skill 生成*")

    return "\n".join(report)


def run_monitor():
    """运行监控"""
    config = load_config()
    api_key = config.get("apikey", DEFAULT_API_KEY)
    nodes = config.get("nodes", DEFAULT_NODES)

    if not api_key:
        raise ValueError("未配置 V2EX API Key，请先运行 config 子命令设置 --apikey")

    monitor = V2EXMonitor(api_key)

    # 获取已处理的主题
    seen_topics = load_seen_topics()
    seen_notifications = load_seen_notifications()
    new_topics = []
    new_notifications = []

    # 抓取各节点最新主题
    print(f"正在监控节点: {', '.join(nodes)}")
    for node in nodes:
        topics = monitor.get_node_topics(node)
        for topic in topics:
            tid = topic.get("id")
            if tid and tid not in seen_topics:
                topic["_source_node"] = node  # 添加来源节点信息
                new_topics.append(topic)
                seen_topics.add(tid)
        time.sleep(0.3)  # 避免请求过快

    # 获取提醒
    notifications = monitor.get_notifications()
    for notification in notifications:
        key = _notification_key(notification)
        if key not in seen_notifications:
            new_notifications.append(notification)
            seen_notifications.add(key)

    # 更新已处理主题
    save_seen_topics(seen_topics)
    save_seen_notifications(seen_notifications)

    # 生成报告
    report = generate_report(new_topics, new_notifications, nodes)

    # 保存报告
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report)

    print(f"\n报告已生成: {REPORT_FILE}")
    print(f"发现新帖子: {len(new_topics)} 篇")
    print(f"新提醒: {len(new_notifications)} 条")

    return new_topics, new_notifications


def cmd_config(args):
    """配置命令"""
    config = load_config()

    if args.nodes:
        config["nodes"] = [n.strip() for n in args.nodes.split(",")]
    if args.apikey:
        config["apikey"] = args.apikey

    save_config(config)
    print(f"配置已保存:")
    print(f"  监控节点: {', '.join(config['nodes'])}")
    print(f"  API Key: {config['apikey'][:8]}...")


def cmd_run(args):
    """运行命令"""
    run_monitor()


def cmd_daemon(args):
    """守护进程模式"""
    import time
    interval = args.interval * 3600  # 转换为秒
    print(f"启动定时监控，每 {args.interval} 小时运行一次...")
    print("按 Ctrl+C 停止")

    while True:
        run_monitor()
        print(f"\n等待 {args.interval} 小时后再次运行...")
        time.sleep(interval)


def main():
    parser = argparse.ArgumentParser(description="V2EX 帖子监控工具")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # config 子命令
    config_parser = subparsers.add_parser("config", help="配置监控节点和API Key")
    config_parser.add_argument("--nodes", help="监控的节点，用逗号分隔")
    config_parser.add_argument("--apikey", help="V2EX API Key")
    config_parser.set_defaults(func=cmd_config)

    # run 子命令
    run_parser = subparsers.add_parser("run", help="运行一次监控")
    run_parser.set_defaults(func=cmd_run)

    # daemon 子命令
    daemon_parser = subparsers.add_parser("daemon", help="启动定时监控")
    daemon_parser.add_argument("--interval", type=int, default=1, help="间隔小时数，默认1小时")
    daemon_parser.set_defaults(func=cmd_daemon)

    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        return

    try:
        args.func(args)
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
