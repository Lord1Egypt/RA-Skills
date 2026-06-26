#!/usr/bin/env python3
"""
SSH 服务器清单管理
支持分组、标签、批量操作
"""

import json
import logging
import os
import re
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from pathlib import Path

logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class Server:
    """服务器配置"""
    name: str  # 服务器名称（自定义）
    host: str  # IP 或域名
    port: int = 22
    user: str = "root"
    ssh_key: Optional[str] = None  # SSH 密钥路径，None 表示使用密码
    password: Optional[str] = None  # 密码（如未使用密钥）
    groups: List[str] = None  # 所属分组
    tags: List[str] = None  # 标签（如: "生产", "测试", "阿里云"）
    description: str = ""

    def __post_init__(self):
        if self.groups is None:
            self.groups = []
        if self.tags is None:
            self.tags = []


class Inventory:
    """服务器清单管理器"""

    def __init__(self, config_dir: str = None):
        self.config_dir = Path(config_dir or "~/.ssh-deploy").expanduser()
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.inventory_file = self.config_dir / "inventory.json"
        self.servers: Dict[str, Server] = {}
        self._load()

    def _load(self):
        """从文件加载清单"""
        if self.inventory_file.exists():
            with open(self.inventory_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for name, srv in data.get('servers', {}).items():
                    self.servers[name] = Server(name=name, **srv)

        # 同时从 ~/.ssh/config 动态加载（不保存到 inventory.json）
        self._load_from_ssh_config()

        # 检查密码使用情况
        self._check_password_usage()

    def _load_from_ssh_config(self):
        """从 ~/.ssh/config 解析 Host 条目"""
        ssh_config_path = Path.home() / ".ssh" / "config"
        if not ssh_config_path.exists():
            return

        try:
            with open(ssh_config_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # 简单的 SSH config 解析器
            current_host = None
            current_values = {}

            for line in content.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                # 检测新的 Host 块
                if re.match(r'^Host\s+', line, re.IGNORECASE):
                    # 保存前一个 Host
                    if current_host and current_host not in self.servers:
                        server = self._create_server_from_ssh_config(current_host, current_values)
                        if server:
                            self.servers[current_host] = server

                    # 开始新的 Host
                    parts = line.split(maxsplit=1)
                    current_host = parts[1].strip()
                    current_values = {}
                else:
                    # 解析键值对
                    if ' ' in line:
                        key, val = line.split(maxsplit=1)
                        current_values[key.lower()] = val.strip()

            # 保存最后一个 Host
            if current_host and current_host not in self.servers:
                server = self._create_server_from_ssh_config(current_host, current_values)
                if server:
                    self.servers[current_host] = server

        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.warning(f"加载 SSH config 失败: {e}")

    def _create_server_from_ssh_config(self, hostname: str, values: Dict[str, str]) -> Optional[Server]:
        """从 SSH config 的 Host 条目创建 Server 对象"""
        # HostName (必需)
        host = values.get('hostname')
        if not host:
            # 如果没指定 HostName，使用 Host 本身作为主机名
            host = hostname

        # Port (默认 22)
        port = 22
        if 'port' in values:
            try:
                port = int(values['port'])
            except ValueError:
                port = 22

        # User (默认 root)
        user = values.get('user', 'root')

        # IdentityFile (SSH 密钥)
        ssh_key = None
        if 'identityfile' in values:
            # 展开 ~ 和变量
            key_path = os.path.expanduser(values['identityfile'])
            if os.path.exists(key_path):
                ssh_key = key_path

        # 创建 Server 对象
        return Server(
            name=hostname,
            host=host,
            port=port,
            user=user,
            ssh_key=ssh_key,
            groups=[],
            tags=["ssh-config"],
            description=f"从 ~/.ssh/config 自动加载"
        )

    def save(self):
        """保存清单到文件"""
        data = {
            'servers': {name: asdict(srv) for name, srv in self.servers.items()}
        }
        with open(self.inventory_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_server(self, server: Server):
        """添加服务器"""
        if server.name in self.servers:
            raise ValueError(f"服务器 '{server.name}' 已存在")
        self.servers[server.name] = server
        self.save()

    def remove_server(self, name: str):
        """删除服务器"""
        if name in self.servers:
            del self.servers[name]
            self.save()

    def get_server(self, name: str) -> Optional[Server]:
        """获取单个服务器"""
        return self.servers.get(name)

    def list_servers(self) -> List[Server]:
        """列出所有服务器"""
        return list(self.servers.values())

    def find_by_group(self, group: str) -> List[Server]:
        """按分组查找"""
        return [s for s in self.servers.values() if group in s.groups]

    def find_by_tag(self, tag: str) -> List[Server]:
        """按标签查找"""
        return [s for s in self.servers.values() if tag in s.tags]

    def find_by_name_pattern(self, pattern: str) -> List[Server]:
        """按名称模糊匹配"""
        import fnmatch
        return [s for s in self.servers.values() if fnmatch.fnmatch(s.name, pattern)]

    def get_all_groups(self) -> List[str]:
        """获取所有分组"""
        groups = set()
        for s in self.servers.values():
            groups.update(s.groups)
        return sorted(list(groups))

    def get_all_tags(self) -> List[str]:
        """获取所有标签"""
        tags = set()
        for s in self.servers.values():
            tags.update(s.tags)
        return sorted(list(tags))


def main():
    """命令行接口（供测试使用）"""
    import argparse

    parser = argparse.ArgumentParser(description="SSH 服务器清单管理")
    parser.add_argument("--config-dir", default="~/.ssh-deploy",
                        help="配置文件目录")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 添加服务器
    add_parser = subparsers.add_parser("add", help="添加服务器")
    add_parser.add_argument("name", help="服务器名称")
    add_parser.add_argument("host", help="IP 或域名")
    add_parser.add_argument("--port", type=int, default=22, help="SSH 端口")
    add_parser.add_argument("--user", default="root", help="用户名")
    add_parser.add_argument("--ssh-key", help="SSH 密钥路径")
    add_parser.add_argument("--groups", default="", help="分组，逗号分隔")
    add_parser.add_argument("--tags", default="", help="标签，逗号分隔")
    add_parser.add_argument("--desc", default="", help="描述")

    # 列出服务器
    list_parser = subparsers.add_parser("list", help="列出服务器")
    list_parser.add_argument("--group", help="按分组过滤")
    list_parser.add_argument("--tag", help="按标签过滤")

    args = parser.parse_args()

    inv = Inventory(args.config_dir)

    if args.command == "add":
        server = Server(
            name=args.name,
            host=args.host,
            port=args.port,
            user=args.user,
            ssh_key=args.ssh_key,
            groups=args.groups.split(',') if args.groups else [],
            tags=args.tags.split(',') if args.tags else [],
            description=args.desc
        )
        inv.add_server(server)
        print(f"✅ 已添加服务器: {args.name} ({args.host})")

    elif args.command == "list":
        servers = inv.list_servers()
        if args.group:
            servers = [s for s in servers if args.group in s.groups]
        if args.tag:
            servers = [s for s in servers if args.tag in s.tags]

        print(f"共 {len(servers)} 台服务器:")
        for s in servers:
            print(f"  - {s.name}: {s.user}@{s.host}:{s.port}  [分组: {', '.join(s.groups) or '无'}]  [标签: {', '.join(s.tags) or '无'}]")
            if s.description:
                print(f"    描述: {s.description}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
