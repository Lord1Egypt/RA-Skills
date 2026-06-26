#!/usr/bin/env python3
"""
SSH 远程部署核心模块
支持命令执行、文件传输、批量部署
"""

import os
import sys
import json
import time
import logging
import threading
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

# 导入 paramiko（如果未安装 will be handled by skill setup）
try:
    import paramiko
    PARAMIKO_AVAILABLE = True
except ImportError:
    PARAMIKO_AVAILABLE = False
    paramiko = None

# 确保 Server 类可用
from inventory import Server  # noqa: F401 (used in type hints)

# 配置日志
logger = logging.getLogger(__name__)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


@dataclass
class DeployResult:
    """部署结果"""
    server_name: str
    success: bool
    output: str = ""
    error: str = ""
    exit_code: int = 0
    duration: float = 0.0


class SSHDeployer:
    """SSH 部署器"""

    def __init__(self, config_dir: str = None, timeout: int = 30, strict_host_key: bool = False):
        if config_dir is None:
            config_dir = os.path.expanduser("~/.ssh-deploy")
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "config.json"
        self.timeout = timeout
        self.strict_host_key = strict_host_key
        self.connections: Dict[str, paramiko.SSHClient] = {}
        self._lock = threading.Lock()  # 线程安全锁

        # 加载配置
        self.config = self._load_config()

        # 检查 paramiko
        if not PARAMIKO_AVAILABLE:
            raise ImportError("请先安装 paramiko: pip install paramiko")

        # 检查密码使用并警告
        self._warn_if_passwords_used()

        # 检查密码使用并警告
        self._warn_if_passwords_used()

    def _load_config(self) -> Dict:
        """加载配置文件
        
        Note: config.json is currently a placeholder for future configuration options.
        It is not used by the current implementation but reserved for:
        - Global settings (default timeout, retry count, etc.)
        - Mirror configuration
        - Output formatting preferences
        - Custom template paths
        """
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_config(self):
        """保存配置
        
        Note: Currently unused. Reserved for future configuration persistence.
        """
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def _get_ssh_client(self, server: 'Server') -> 'paramiko.SSHClient':
        """获取或创建 SSH 客户端，带重试机制"""
        cache_key = f"{server.user}@{server.host}:{server.port}"

        # 线程安全：检查缓存时加锁
        with self._lock:
            if cache_key in self.connections:
                return self.connections[cache_key]

        client = paramiko.SSHClient()

        # 主机密钥验证策略
        if self.strict_host_key:
            # 严格模式：使用 known_hosts，首次连接需要手动确认
            client.load_system_host_keys()
            client.set_missing_host_key_policy(paramiko.RejectPolicy())
            logger.info(f"[{server.name}] 使用严格主机密钥验证模式")
        else:
            # 兼容模式：自动接受新主机密钥（默认）
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            logger.debug(f"[{server.name}] 使用自动主机密钥接受模式（不安全）")

        # 重试配置
        max_retries = 3
        retry_delay = 1.0

        for attempt in range(1, max_retries + 1):
            try:
                # 认证方式
                if server.ssh_key:
                    key_path = os.path.expanduser(server.ssh_key)
                    if not os.path.exists(key_path):
                        raise FileNotFoundError(f"SSH 密钥不存在: {key_path}")
                    private_key = paramiko.RSAKey.from_private_key_file(key_path)
                    client.connect(server.host, server.port, server.user, pkey=private_key, timeout=self.timeout)
                elif server.password:
                    client.connect(server.host, server.port, server.user, server.password, timeout=self.timeout)
                else:
                    # 尝试使用默认的 SSH 密钥
                    client.connect(server.host, server.port, server.user, timeout=self.timeout)

                # 线程安全：写入缓存时加锁
                with self._lock:
                    self.connections[cache_key] = client
                logger.debug(f"[{server.name}] SSH 连接成功 (尝试 {attempt}/{max_retries})")
                return client

            except paramiko.BadHostKeyException as e:
                # 严格模式下的主机密钥不匹配
                logger.error(f"[{server.name}] 主机密钥验证失败: {e}")
                logger.error("请检查 known_hosts 文件或服务器是否被入侵")
                raise
            except Exception as e:
                if attempt == max_retries:
                    logger.error(f"[{server.name}] SSH 连接失败，重试 {max_retries} 次后放弃: {e}")
                    raise
                else:
                    logger.warning(f"[{server.name}] SSH 连接失败 (尝试 {attempt}/{max_retries}): {e}，{retry_delay:.1f}s 后重试")
                    time.sleep(retry_delay)
                    retry_delay *= 1.5  # 指数退避

    def execute(self, server: 'Server', command: str, get_pty: bool = False) -> DeployResult:
        """
        在服务器上执行命令
        """
        start_time = time.time()
        result = DeployResult(
            server_name=server.name,
            success=False,
            exit_code=-1
        )

        try:
            client = self._get_ssh_client(server)
            logger.info(f"[{server.name}] 执行: {command}")

            stdin, stdout, stderr = client.exec_command(command, get_pty=get_pty)
            exit_code = stdout.channel.recv_exit_status()

            output = stdout.read().decode('utf-8', errors='replace')
            error = stderr.read().decode('utf-8', errors='replace')

            result.output = output.strip()
            result.error = error.strip()
            result.exit_code = exit_code
            result.success = (exit_code == 0)

            if result.success:
                logger.info(f"[{server.name}] ✓ 执行成功")
            else:
                logger.warning(f"[{server.name}] ✗ 执行失败 (code: {exit_code})")

        except Exception as e:
            result.error = str(e)
            result.success = False
            logger.error(f"[{server.name}] 异常: {e}")

        result.duration = time.time() - start_time
        return result

    def execute_batch(self, servers: List[Server], command: str, sequential: bool = False) -> Dict[str, DeployResult]:
        """
        批量执行命令
        sequential: 是否顺序执行（False 表示并行）
        """
        results = {}

        if sequential:
            for server in servers:
                results[server.name] = self.execute(server, command)
        else:
            from concurrent.futures import ThreadPoolExecutor, as_completed
            with ThreadPoolExecutor(max_workers=min(10, len(servers))) as executor:
                future_to_server = {
                    executor.submit(self.execute, server, command): server
                    for server in servers
                }
                for future in as_completed(future_to_server):
                    server = future_to_server[future]
                    try:
                        results[server.name] = future.result()
                    except Exception as e:
                        results[server.name] = DeployResult(
                            server_name=server.name,
                            success=False,
                            error=str(e)
                        )

        return results

    def upload_file(self, server: 'Server', local_path: str, remote_path: str) -> DeployResult:
        """
        上传文件到服务器 (SCP)
        """
        start_time = time.time()
        result = DeployResult(
            server_name=server.name,
            success=False,
            exit_code=-1
        )

        try:
            client = self._get_ssh_client(server)
            sftp = client.open_sftp()
            logger.info(f"[{server.name}] 上传: {local_path} -> {remote_path}")
            sftp.put(local_path, remote_path)
            sftp.close()

            result.success = True
            result.output = f"上传完成: {remote_path}"
            logger.info(f"[{server.name}] ✓ 上传成功")

        except Exception as e:
            result.error = str(e)
            logger.error(f"[{server.name}] 上传失败: {e}")

        result.duration = time.time() - start_time
        return result

    def download_file(self, server: 'Server', remote_path: str, local_path: str) -> DeployResult:
        """
        从服务器下载文件
        """
        start_time = time.time()
        result = DeployResult(
            server_name=server.name,
            success=False,
            exit_code=-1
        )

        try:
            client = self._get_ssh_client(server)
            sftp = client.open_sftp()
            logger.info(f"[{server.name}] 下载: {remote_path} -> {local_path}")
            sftp.get(remote_path, local_path)
            sftp.close()

            result.success = True
            result.output = f"下载完成: {local_path}"
            logger.info(f"[{server.name}] ✓ 下载成功")

        except Exception as e:
            result.error = str(e)
            logger.error(f"[{server.name}] 下载失败: {e}")

        result.duration = time.time() - start_time
        return result

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - automatically close connections"""
        self.close()
        return False

    def close(self):
        """关闭所有连接"""
        for client in self.connections.values():
            try:
                client.close()
            except:
                pass
        self.connections.clear()


def main():
    """命令行接口"""
    import argparse
    from inventory import Inventory

    parser = argparse.ArgumentParser(description="SSH 远程部署工具")
    parser.add_argument("--config-dir", default="~/.ssh-deploy",
                        help="配置文件目录")
    parser.add_argument("--strict", action="store_true",
                        help="启用严格主机密钥验证（首次连接需手动确认）")
    subparsers = parser.add_subparsers(dest="command", help="命令")

    # 列出服务器
    list_parser = subparsers.add_parser("list", help="列出所有可用服务器")
    list_parser.add_argument("--group", help="按分组过滤")
    list_parser.add_argument("--tag", help="按标签过滤")
    list_parser.add_argument("--source", choices=['all', 'inventory', 'ssh-config'], default='all', help="数据源: all=全部, inventory=inventory.json, ssh-config=~/.ssh/config")

    # 执行命令
    exec_parser = subparsers.add_parser("exec", help="执行命令")
    exec_parser.add_argument("target", help="服务器名、SSH config Host 名，或分组（前缀 group: 或 tag:）")
    exec_parser.add_argument("cmd", help="要执行的命令")
    exec_parser.add_argument("--sequential", action="store_true", help="顺序执行")

    # 上传文件
    upload_parser = subparsers.add_parser("upload", help="上传文件")
    upload_parser.add_argument("target", help="服务器名、SSH config Host 名，或分组")
    upload_parser.add_argument("local", help="本地文件路径")
    upload_parser.add_argument("remote", help="远程路径")

    # 下载文件
    download_parser = subparsers.add_parser("download", help="下载文件")
    download_parser.add_argument("target", help="服务器名、SSH config Host 名")
    download_parser.add_argument("remote", help="远程文件路径")
    download_parser.add_argument("local", help="本地保存路径")

    args = parser.parse_args()

    inv = Inventory(args.config_dir)
    deployer = None

    try:
        # list 命令不需要 SSH 连接
        if args.command == "list":
            print(f"📋 可用服务器 (共 {len(inv.servers)} 台):\n")
            for name, server in sorted(inv.servers.items()):
                # 过滤（按分组或标签）
                if args.group and args.group not in server.groups:
                    continue
                if args.tag and args.tag not in server.tags:
                    continue
                # 过滤数据源
                if args.source == 'inventory' and 'ssh-config' in server.tags:
                    continue
                if args.source == 'ssh-config' and 'ssh-config' not in server.tags:
                    continue
                source_tag = "[SSH Config]" if 'ssh-config' in server.tags else ""

                print(f"  • {name}")
                print(f"    └─ {server.user}@{server.host}:{server.port}")
                if server.groups:
                    print(f"    └─ 分组: {', '.join(server.groups)}")
                if server.tags and 'ssh-config' not in server.tags:
                    print(f"    └─ 标签: {', '.join(server.tags)}")
                if server.description:
                    print(f"    └─ 描述: {server.description}")
                if source_tag:
                    print(f"    └─ 来源: {source_tag}")
                print()
            return

        # 其他命令需要 SSH 部署器
        deployer = SSHDeployer(args.config_dir, strict_host_key=args.strict)

        # 解析目标服务器（exec/upload/download）
        if args.target.startswith("group:"):
            group = args.target[6:]
            servers = inv.find_by_group(group)
        elif args.target.startswith("tag:"):
            tag = args.target[4:]
            servers = inv.find_by_tag(tag)
        else:
            server = inv.get_server(args.target)
            if server is None:
                print(f"❌ 服务器不存在: {args.target}")
                sys.exit(1)
            servers = [server]

        if not servers:
            print("❌ 没有匹配的服务器")
            sys.exit(1)

        print(f"目标服务器: {', '.join(s.name for s in servers)}")

        if args.command == "exec":
            results = deployer.execute_batch(servers, args.cmd, args.sequential)
            for name, res in results.items():
                status = "✓" if res.success else "✗"
                print(f"\n[{name}] {status} (exit: {res.exit_code}, 耗时: {res.duration:.2f}s)")
                if res.output:
                    print("输出:", res.output[:500])
                if res.error:
                    print("错误:", res.error[:500])

        elif args.command == "upload":
            for server in servers:
                res = deployer.upload_file(server, args.local, args.remote)
                status = "✓" if res.success else "✗"
                print(f"[{server.name}] {status} {res.output if res.success else res.error}")

        elif args.command == "download":
            for server in servers:
                res = deployer.download_file(server, args.remote, args.local)
                status = "✓" if res.success else "✗"
                print(f"[{server.name}] {status} {res.output if res.success else res.error}")

    except ImportError as e:
        print(f"❌ 依赖缺失: {e}")
        print("请运行: pip install paramiko")
    except Exception as e:
        print(f"❌ 错误: {e}")
    finally:
        if deployer:
            deployer.close()


if __name__ == "__main__":
    main()
