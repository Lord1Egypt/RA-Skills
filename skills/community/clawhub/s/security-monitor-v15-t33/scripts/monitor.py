#!/usr/bin/env python3
"""
安全监控脚本 - 检测服务器进程和文件访问的异常行为
需要root权限运行才能查看所有进程信息
"""

import os
import subprocess
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class Colors:
    """终端颜色类"""
    # 颜色代码
    RED = '\033[91m'      # 红色 - 高危
    GREEN = '\033[92m'    # 绿色 - 安全
    YELLOW = '\033[93m'   # 黄色 - 警告
    BLUE = '\033[94m'     # 蓝色 - 信息
    CYAN = '\033[96m'     # 青色 - 标题
    BOLD = '\033[1m'      # 粗体
    RESET = '\033[0m'     # 重置颜色

    @staticmethod
    def red(text: str) -> str:
        """红色文本"""
        return f"{Colors.RED}{text}{Colors.RESET}"
    
    @staticmethod
    def green(text: str) -> str:
        """绿色文本"""
        return f"{Colors.GREEN}{text}{Colors.RESET}"
    
    @staticmethod
    def yellow(text: str) -> str:
        """黄色文本"""
        return f"{Colors.YELLOW}{text}{Colors.RESET}"
    
    @staticmethod
    def blue(text: str) -> str:
        """蓝色文本"""
        return f"{Colors.BLUE}{text}{Colors.RESET}"
    
    @staticmethod
    def cyan(text: str) -> str:
        """青色文本"""
        return f"{Colors.CYAN}{text}{Colors.RESET}"
    
    @staticmethod
    def bold(text: str) -> str:
        """粗体文本"""
        return f"{Colors.BOLD}{text}{Colors.RESET}"


class SecurityMonitor:
    """安全监控工具"""
    
    def __init__(self):
        self.violations = []
        self.warnings = []
        self.info = []
        self.safe_items = []  # 安全项目
    
    def add_safe_item(self, item: str) -> None:
        """添加安全项目"""
        self.safe_items.append(item)
    
    def get_all_processes(self) -> List[Dict]:
        """获取所有进程信息"""
        try:
            # 使用ps命令获取进程列表
            result = subprocess.run(
                ['ps', 'aux', '--sort=-pcpu'],
                capture_output=True,
                text=True,
                timeout=10
            )
            processes = []
            lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
            
            for line in lines:
                parts = line.split(None, 10)  # 最多分割11个字段
                if len(parts) >= 11:
                    processes.append({
                        'user': parts[0],
                        'pid': int(parts[1]),
                        'cpu': float(parts[2]),
                        'mem': float(parts[3]),
                        'vsz': int(parts[4]),
                        'rss': int(parts[5]),
                        'tty': parts[6],
                        'stat': parts[7],
                        'start': parts[8],
                        'time': parts[9],
                        'command': parts[10]
                    })
            self.add_safe_item(f"✓ 成功获取 {len(processes)} 个进程信息")
            return processes
        except Exception as e:
            self.warnings.append(f"获取进程列表失败: {e}")
            return []
    
    def check_suspicious_processes(self, processes: List[Dict]) -> None:
        """检查可疑进程"""
        # 可疑命令模式
        suspicious_patterns = [
            r'nc\s+-l',  # netcat 监听
            r'bash\s+-i',  # 交互式shell
            r'perl\s+-e',  # Perl单行命令(常用于反弹shell)
            r'python.*socket',  # Python网络编程
            r'wget\s+.*\|.*sh',  # 下载并执行shell脚本
            r'curl\s+.*\|.*sh',
            r'curl.*http://.*\..*:.*',  # 连接到外部IP的curl
            r'ssh\s+-R',  # SSH反向隧道
            r'chmod.*777',  # 权限提升
            r'chown.*root',  # 所有权变更
            r'ncat',  # ncat工具
            r'telnet',  # telnet(不安全协议)
        ]
        
        # 高资源消耗进程
        for proc in processes:
            # 检查CPU使用率
            if proc['cpu'] > 80:
                self.warnings.append(
                    f"高CPU使用率进程: PID {proc['pid']} ({proc['cpu']}% CPU) - {proc['command'][:100]}"
                )
            
            # 检查内存使用
            if proc['mem'] > 80:
                self.warnings.append(
                    f"高内存使用率进程: PID {proc['pid']} ({proc['mem']}% MEM) - {proc['command'][:100]}"
                )
            
            # 检查VNC进程
            self._check_vnc_process(proc)
            
            # 检查可疑命令
            for pattern in suspicious_patterns:
                if re.search(pattern, proc['command'], re.IGNORECASE):
                    severity = "高危" if any(x in pattern.lower() for x in ['nc', 'bash', 'perl', 'ssh']) else "警告"
                    self.violations.append(
                        f"[{severity}] 可疑进程: PID {proc['pid']} - 命令: {proc['command'][:200]}"
                    )
                    break
    
    def _check_vnc_process(self, proc: Dict) -> None:
        """检查VNC进程的安全性"""
        command = proc['command'].lower()
        
        # 检测VNC进程
        vnc_keywords = ['vncserver', 'xvnc', 'x11vnc', 'tightvnc', 'tigervnc', 'realvnc']
        if any(keyword in command for keyword in vnc_keywords):
            # 检查是否有加密参数
            has_encryption = any(kw in command for kw in ['-via', '-ssh', '-ssl', '-tls'])
            
            if not has_encryption:
                self.violations.append(
                    f"[VNC不安全] 发现未加密的VNC进程 PID {proc['pid']}, 命令: {proc['command'][:150]} "
                    f"(裸奔风险!建议使用SSH隧道或TLS加密)"
                )
            else:
                self.add_safe_item(f"✓ VNC进程 PID {proc['pid']} 使用加密连接")
    
    def _get_network_tool(self) -> tuple:
        """获取可用的网络工具(ss或netstat) / Get available network tool (ss or netstat)"""
        # 先尝试ss
        try:
            subprocess.run(['ss', '--version'], capture_output=True, timeout=5)
            return 'ss', ['ss', '-tunapl']
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        # 尝试netstat
        try:
            subprocess.run(['netstat', '-V'], capture_output=True, timeout=5)
            return 'netstat', ['netstat', '-tunap']
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        
        return None, []

    def get_network_connections(self) -> List[Dict]:
        """获取网络连接信息 / Get network connections"""
        tool, cmd = self._get_network_tool()
        
        if tool is None:
            self.warnings.append("获取网络连接失败: 未找到ss或netstat命令,请安装iproute2或net-tools包")
            return []
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            connections = []
            lines = result.stdout.strip().split('\n')[1:]  # 跳过标题行
            
            for line in lines:
                parts = line.split()
                if tool == 'ss' and len(parts) >= 6:
                    connections.append({
                        'proto': parts[0],
                        'state': parts[1],
                        'recv_q': parts[2],
                        'send_q': parts[3],
                        'local': parts[4],
                        'peer': parts[5],
                        'process': parts[6] if len(parts) > 6 else ''
                    })
                elif tool == 'netstat' and len(parts) >= 6:
                    connections.append({
                        'proto': parts[0],
                        'state': parts[1],
                        'recv_q': parts[2],
                        'send_q': parts[3],
                        'local': parts[4],
                        'peer': parts[5],
                        'process': parts[6] if len(parts) > 6 else ''
                    })
            
            self.add_safe_item(f"✓ 成功获取 {len(connections)} 个网络连接 (使用{tool})")
            return connections
        except Exception as e:
            self.warnings.append(f"获取网络连接失败: {e}")
            return []
    
    def check_suspicious_connections(self, connections: List[Dict]) -> None:
        """检查可疑网络连接"""
        # 常见恶意端口
        suspicious_ports = {
            '4444': 'Metasploit reverse shell',
            '5555': 'ADB调试端口',
            '6666-6669': 'IRC/常见后门端口',
            '8080': '代理服务(需确认)',
            '31337': '常见后门端口',
            '12345': '常见后门端口',
        }
        
        for conn in connections:
            # 检查外部连接
            if ':' in conn['peer']:
                peer = conn['peer']
                # 提取端口
                port = peer.split(':')[-1]
                
                # 检查可疑端口
                for port_range, desc in suspicious_ports.items():
                    if '-' in port_range:
                        start, end = port_range.split('-')
                        if start <= port <= end:
                            self.violations.append(f"连接到可疑端口: {peer} ({desc})")
                    elif port == port_range:
                        self.violations.append(f"连接到可疑端口: {peer} ({desc})")
                
                # 检查非标准端口的外部连接
                if conn['state'] == 'ESTABLISHED':
                    port_num = int(port)
                    if port_num > 1024 and port_num not in [8080, 3000, 5000, 8000, 9000]:
                        self.warnings.append(f"外部连接到非标准端口: {peer}")
    
    def scan_secrets_in_files(self, directory: str = '/var/log', max_files: int = 50) -> None:
        """扫描文件中的敏感信息"""
        # 敏感信息模式
        secret_patterns = {
            'API密钥': [
                r'api[_-]?key\s*=\s*["\']?[a-zA-Z0-9]{20,}["\']?',
                r'apikey["\']?\s*:\s*["\']?[a-zA-Z0-9]{20,}["\']?',
            ],
            '数据库密码': [
                r'password\s*=\s*["\']?\w{8,}["\']?',
                r'db[_-]?password["\']?\s*:\s*["\']?\w{8,}["\']?',
            ],
            'JWT密钥': [
                r'jwt[_-]?secret["\']?\s*:\s*["\']?\w{20,}["\']?',
                r'secret["\']?\s*:\s*["\'][\w\-]{30,}["\']?',
            ],
            '私钥': [
                r'-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----',
                r'-----BEGIN\s+EC\s+PRIVATE\s+KEY-----',
            ],
            '访问令牌': [
                r'access[_-]?token["\']?\s*:\s*["\']?[a-zA-Z0-9\._\-]{30,}["\']?',
                r'auth[_-]?token["\']?\s*:\s*["\']?[a-zA-Z0-9\._\-]{30,}["\']?',
            ],
        }
        
        if not os.path.exists(directory):
            self.warnings.append(f"目录不存在: {directory}")
            return
        
        scanned_count = 0
        for root, dirs, files in os.walk(directory):
            if scanned_count >= max_files:
                break
            
            for file in files:
                if scanned_count >= max_files:
                    break
                
                file_path = os.path.join(root, file)
                
                # 跳过二进制文件
                if file.endswith(('.log', '.txt', '.conf', '.ini', '.json', '.yml', '.yaml', '.env')):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            for secret_type, patterns in secret_patterns.items():
                                for pattern in patterns:
                                    matches = re.findall(pattern, content, re.IGNORECASE)
                                    if matches:
                                        self.violations.append(
                                            f"[敏感信息泄露] {secret_type} 在 {file_path}"
                                        )
                                        break
                    except Exception as e:
                        pass
                
                scanned_count += 1
    
    def check_file_permissions(self, directory: str = '/') -> None:
        """检查可疑的文件权限"""
        try:
            # 查找可写的系统关键文件
            critical_dirs = ['/etc', '/usr/bin', '/usr/sbin', '/bin', '/sbin']
            
            for critical_dir in critical_dirs:
                if not os.path.exists(critical_dir):
                    continue
                
                result = subprocess.run(
                    ['find', critical_dir, '-type', 'f', '-perm', '-o+w', '-maxdepth', '2'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.stdout.strip():
                    for line in result.stdout.strip().split('\n'):
                        if line:
                            self.violations.append(
                                f"[权限问题] 系统关键文件可写: {line}"
                            )
        
        except Exception as e:
            self.warnings.append(f"检查文件权限失败: {e}")
    
    def check_open_ports(self) -> None:
        """检查开放的端口 / Check open ports"""
        tool, cmd = self._get_network_tool()
        
        if tool is None:
            self.warnings.append("检查开放端口失败: 未找到ss或netstat命令,请安装iproute2或net-tools包")
            return
        
        # 调整命令参数
        if tool == 'ss':
            cmd = ['ss', '-tlnp']
        else:
            cmd = ['netstat', '-tlnp']
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            lines = result.stdout.strip().split('\n')[1:]
            ports_info = {}  # 存储端口及其对应进程
            
            for line in lines:
                parts = line.split()
                if len(parts) >= 5:
                    # ss: Local Address is in parts[3], netstat: Local Address is in parts[3]
                    local = parts[3]
                    process_info = parts[6] if len(parts) > 6 else 'Unknown'
                    if ':' in local:
                        port = local.split(':')[-1]
                        try:
                            port = str(int(port))  # 确保端口是数字
                            if port not in ports_info:
                                ports_info[port] = []
                            ports_info[port].append(process_info)
                        except ValueError:
                            pass
            
            # 端口分类
            common_ports = {'22', '80', '443', '3306', '5432', '6379', '27017'}
            suspicious_ports = {'4444', '5555', '6666', '6667', '6668', '6669', '31337', '12345'}
            
            # 专门检查VNC端口
            self._check_vnc_security(ports_info)
            
            for port in ports_info.keys():
                if port in suspicious_ports:
                    self.violations.append(f"开放可疑端口: {port}")
                elif port not in common_ports:
                    self.warnings.append(f"开放非标准端口: {port} - 请确认是否为预期服务")
                else:
                    self.add_safe_item(f"✓ 正常开放端口: {port}")
            
            if len(ports_info) > 0:
                self.add_safe_item(f"✓ 共扫描到 {len(ports_info)} 个开放端口 (使用{tool})")
        
        except Exception as e:
            self.warnings.append(f"检查开放端口失败: {e}")
    
    def _check_vnc_security(self, ports_info: dict) -> None:
        """检查VNC服务的安全性"""
        # VNC常见端口
        vnc_ports = ['5900', '5901', '5902', '5903', '5904', '5905']
        
        for port in vnc_ports:
            if port in ports_info:
                processes = ports_info[port]
                
                # 检查VNC是否使用了加密
                self._check_vnc_encryption(port)
                
                # 检查VNC监听地址(是否暴露到公网)
                self._check_vnc_binding(port, processes)
                
                # 检查VNC配置文件
                self._check_vnc_config()
    
    def _check_vnc_encryption(self, port: str) -> None:
        """检查VNC是否使用了加密"""
        try:
            # 检查是否使用x11vnc(支持SSH隧道)
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            has_vnc_process = 'vnc' in result.stdout.lower()
            has_ssh_tunnel = 'ssh.*-L.*590' in result.stdout.lower()
            
            if has_vnc_process and not has_ssh_tunnel:
                self.violations.append(
                    f"[VNC不安全] VNC端口 {port} 开放,未检测到SSH隧道,可能直接暴露在公网(裸奔)"
                )
            elif has_vnc_process and has_ssh_tunnel:
                self.add_safe_item(f"✓ VNC端口 {port} 使用SSH隧道,相对安全")
        except Exception as e:
            self.warnings.append(f"检查VNC加密状态失败: {e}")
    
    def _check_vnc_binding(self, port: str, processes: list) -> None:
        """检查VNC绑定地址 / Check VNC binding address"""
        tool, _ = self._get_network_tool()
        
        if tool is None:
            return
        
        try:
            # 使用ss或netstat查看详细绑定信息
            cmd = ['ss', '-tlnp'] if tool == 'ss' else ['netstat', '-tlnp']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            lines = result.stdout.split('\n')
            for line in lines:
                if f':{port}' in line and 'LISTEN' in line:
                    # 检查绑定地址
                    if '0.0.0.0' in line or ':::' in line:
                        self.violations.append(
                            f"[VNC不安全] VNC端口 {port} 绑定到 0.0.0.0,暴露在所有网络接口(裸奔)! "
                            f"建议: 1) 仅绑定localhost (127.0.0.1) 2) 使用SSH隧道 3) 配置防火墙"
                        )
                    elif '127.0.0.1' in line:
                        self.add_safe_item(f"✓ VNC端口 {port} 仅绑定localhost,安全")
                    break
        except Exception as e:
            self.warnings.append(f"检查VNC绑定地址失败: {e}")
    
    def _check_vnc_config(self) -> None:
        """检查VNC配置文件"""
        vnc_config_paths = [
            '/etc/vnc/', '~/.vnc/', '/etc/vncserver-config-defaults',
            '~/.vnc/xstartup', '~/.vnc/config'
        ]
        
        try:
            for config_path in vnc_config_paths:
                # 展开波浪号
                if '~' in config_path:
                    expanded_path = os.path.expanduser(config_path)
                else:
                    expanded_path = config_path
                
                if os.path.exists(expanded_path):
                    if os.path.isfile(expanded_path):
                        with open(expanded_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            
                            # 检查是否设置了密码
                            if 'password' not in content.lower() and 'passwd' not in content.lower():
                                self.violations.append(
                                    f"[VNC不安全] VNC配置文件 {expanded_path} 未设置密码(裸奔)!"
                                )
                            
                            # 检查是否禁用了加密
                            if 'SecurityTypes=None' in content or 'securitytypes=none' in content.lower():
                                self.violations.append(
                                    f"[VNC不安全] VNC配置文件 {expanded_path} 禁用了所有安全类型(裸奔)!"
                                )
                            
                            # 检查是否允许未认证连接
                            if 'PasswordAuth=no' in content or 'passwordauth=no' in content.lower():
                                self.violations.append(
                                    f"[VNC不安全] VNC配置文件 {expanded_path} 禁用了密码认证(裸奔)!"
                                )
                            else:
                                self.add_safe_item(f"✓ VNC配置文件 {expanded_path} 启用了认证")
        except Exception as e:
            self.warnings.append(f"检查VNC配置文件失败: {e}")
    
    def generate_report(self, use_colors: bool = True) -> str:
        """生成安全报告
        
        Args:
            use_colors: 是否使用彩色输出(默认True)
        """
        # 如果终端不支持颜色或明确不使用颜色
        if not use_colors:
            return self._generate_plain_report()
        
        report = []
        report.append(Colors.bold(Colors.cyan("=" * 80)))
        report.append(Colors.bold(Colors.cyan("🛡️  安全监控报告")))
        report.append(Colors.blue(f"📅 时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
        report.append(Colors.cyan("=" * 80))
        
        # 安全项目(绿色)
        if self.safe_items:
            report.append(f"\n{Colors.green('✓ 安全状态')} (共 {len(self.safe_items)} 项)")
            report.append(Colors.green("-" * 80))
            for i, item in enumerate(self.safe_items, 1):
                report.append(f"  {Colors.green(item)}")
        
        # 高危问题(红色)
        if self.violations:
            report.append(f"\n{Colors.red('🚨 高危问题')} (共 {len(self.violations)} 项)")
            report.append(Colors.red("-" * 80))
            for i, violation in enumerate(self.violations, 1):
                report.append(f"  {Colors.red(str(i))}. {Colors.red(violation)}")
        
        # 警告信息(黄色)
        if self.warnings:
            report.append(f"\n{Colors.yellow('⚠️  警告信息')} (共 {len(self.warnings)} 项)")
            report.append(Colors.yellow("-" * 80))
            for i, warning in enumerate(self.warnings, 1):
                report.append(f"  {Colors.yellow(str(i))}. {Colors.yellow(warning)}")
        
        # 总结
        if not self.violations and not self.warnings:
            report.append(f"\n{Colors.green('🎉 未检测到明显的安全风险,系统安全!')}")
        elif len(self.violations) == 0:
            report.append(f"\n{Colors.yellow('⚡ 发现 {len(self.warnings)} 个警告项,请及时处理')}")
        else:
            report.append(f"\n{Colors.red('⛔ 发现 {len(self.violations)} 个高危问题和 {len(self.warnings)} 个警告,立即处理!')}")
        
        report.append(Colors.cyan("=" * 80))
        
        return '\n'.join(report)
    
    def analyze_logs(self, log_dir: str = '/var/log', max_lines: int = 1000) -> None:
        """分析系统日志 / Analyze system logs
        检测异常登录、失败尝试、服务事件等
        """
        log_files = [
            'auth.log', 'syslog', 'secure', 'messages',
            'faillog', 'lastlog', 'wtmp', 'btmp'
        ]
        
        # SSH暴力破解模式
        brute_force_patterns = [
            r'Failed password',
            r'authentication failure',
            r'Failed publickey',
            r'BREAK-IN',
            r'Invalid user',
        ]
        
        # 可疑命令模式
        suspicious_commands = [
            r'wget.*\|.*sh',
            r'curl.*\|.*sh',
            r'nc -[eLp]',
            r'bash -i',
            r'/dev/tcp/',
            r'python.*-c.*socket',
            r'chmod 777.*shadow',
            r'chmod 4755',
        ]
        
        for log_file in log_files:
            log_path = Path(log_dir) / log_file
            if not log_path.exists():
                # 尝试常见的日志目录
                for alt_dir in ['/var/log', '/var/adm', '/etc/log']:
                    alt_path = Path(alt_dir) / log_file
                    if alt_path.exists():
                        log_path = alt_path
                        break
                else:
                    continue
            
            try:
                # 读取最后max_lines行
                result = subprocess.run(
                    ['tail', '-n', str(max_lines), str(log_path)],
                    capture_output=True, text=True, timeout=10
                )
                
                lines = result.stdout.split('\n')
                failed_logins = 0
                suspicious_events = []
                
                for line in lines:
                    # 检测暴力破解
                    for pattern in brute_force_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            failed_logins += 1
                            if failed_logins <= 10:  # 只记录前10条
                                suspicious_events.append(line[:150])
                            break
                    
                    # 检测可疑命令
                    for pattern in suspicious_commands:
                        if re.search(pattern, line, re.IGNORECASE):
                            suspicious_events.append(f"[可疑命令] {line[:150]}")
                            break
                
                # 报告结果
                if failed_logins > 20:
                    self.warnings.append(
                        f"[日志分析] {log_file} 检测到 {failed_logins} 次失败登录尝试 (可能是暴力攻击)"
                    )
                elif failed_logins > 0:
                    self.add_safe_item(f"[日志分析] {log_file} 有 {failed_logins} 次失败登录记录")
                
                for event in suspicious_events[:5]:
                    self.warnings.append(f"[日志分析] {event}")
                    
            except Exception as e:
                pass  # 静默跳过无法读取的日志
        
        self.add_safe_item("✓ 日志分析完成 / Log analysis completed")
    
    def analyze_process_tree(self) -> None:
        """分析进程树 / Analyze process tree
        检测孤儿进程、可疑进程链、隐藏进程等
        """
        try:
            # 获取完整进程树
            result = subprocess.run(
                ['ps', 'auxf', '--forest'],
                capture_output=True, text=True, timeout=15
            )
            
            if result.returncode != 0:
                # 备用方案
                result = subprocess.run(
                    ['ps', 'axjf'],
                    capture_output=True, text=True, timeout=15
                )
            
            lines = result.stdout.split('\n')
            
            # 构建进程树
            processes = {}
            orphans = []
            suspicious_chains = []
            
            # 解析ps输出
            for line in lines:
                # 检测孤儿进程 (PPID=1 或 PPID不存在但有子进程)
                if 'PPID' in line or len(line.strip()) < 5:
                    continue
                
                # 简单的进程解析
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        pid = int(parts[1]) if parts[1].isdigit() else None
                        ppid = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None
                        
                        if pid and ppid is not None:
                            processes[pid] = {'ppid': ppid, 'line': line}
                    except:
                        pass
            
            # 检测孤儿进程 (父进程不存在)
            for pid, info in processes.items():
                if info['ppid'] not in processes and info['ppid'] != 0:
                    orphans.append(f"PID {pid} (PPID={info['ppid']}, 父进程已退出)")
            
            # 检测可疑进程链
            shell_processes = ['bash', 'sh', 'dash', 'zsh']
            network_processes = ['nc', 'netcat', 'socat', 'ncat']
            
            for pid, info in processes.items():
                line_lower = info['line'].lower()
                
                # 检测shell进程的网络连接
                for shell in shell_processes:
                    if shell in line_lower:
                        # 检查是否有可疑的网络相关子进程
                        for net in network_processes:
                            if net in line_lower:
                                suspicious_chains.append(
                                    f"可疑进程链: {shell} -> {net} (PID {pid})"
                                )
            
            # 报告结果
            if orphans:
                self.warnings.append(f"[进程树] 发现 {len(orphans)} 个孤儿进程")
                for orphan in orphans[:3]:
                    self.warnings.append(f"  {orphan}")
            
            if suspicious_chains:
                self.violations.append(f"[进程树] 发现可疑进程链:")
                for chain in suspicious_chains[:3]:
                    self.violations.append(f"  {chain}")
            
            if not orphans and not suspicious_chains:
                self.add_safe_item("✓ 进程树分析未发现异常")
                
        except Exception as e:
            self.warnings.append(f"进程树分析失败: {e}")
    
    def _generate_plain_report(self) -> str:
        """生成无颜色的纯文本报告"""
        report = []
        report.append("=" * 80)
        report.append("安全监控报告")
        report.append(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("=" * 80)
        
        if self.safe_items:
            report.append(f"\n[安全状态] (共 {len(self.safe_items)} 项)")
            report.append("-" * 80)
            for i, item in enumerate(self.safe_items, 1):
                report.append(f"  {i}. {item}")
        
        if self.violations:
            report.append(f"\n[高危问题] (共 {len(self.violations)} 项)")
            report.append("-" * 80)
            for i, violation in enumerate(self.violations, 1):
                report.append(f"{i}. {violation}")
        
        if self.warnings:
            report.append(f"\n[警告信息] (共 {len(self.warnings)} 项)")
            report.append("-" * 80)
            for i, warning in enumerate(self.warnings, 1):
                report.append(f"{i}. {warning}")
        
        if not self.violations and not self.warnings:
            report.append("\n✓ 未检测到明显的安全风险,系统安全!")
        
        report.append("\n" + "=" * 80)
        
        return '\n'.join(report)


def run_scan(use_colors: bool = True) -> dict:
    """执行一次完整的扫描 / Perform a complete scan (v1.5)

    Args:
        use_colors: 是否使用彩色输出 / Whether to use colored output

    Returns:
        扫描结果字典 / Scan result dictionary
    """
    monitor = SecurityMonitor()

    # 检查进程
    print(Colors.yellow("[1/7] 扫描进程... / Scanning processes..."))
    processes = monitor.get_all_processes()
    monitor.check_suspicious_processes(processes)

    # 分析进程树 (v1.5新增)
    print(Colors.yellow("[2/7] 分析进程树... / Analyzing process tree..."))
    monitor.analyze_process_tree()

    # 检查网络连接
    print(Colors.yellow("[3/7] 扫描网络连接... / Scanning network connections..."))
    connections = monitor.get_network_connections()
    monitor.check_suspicious_connections(connections)

    # 检查开放端口
    print(Colors.yellow("[4/7] 检查开放端口... / Checking open ports..."))
    monitor.check_open_ports()

    # 检查文件权限(需要root)
    print(Colors.yellow("[5/7] 检查文件权限... / Checking file permissions..."))
    monitor.check_file_permissions()

    # 分析系统日志 (v1.5新增)
    print(Colors.yellow("[6/7] 分析系统日志... / Analyzing system logs..."))
    monitor.analyze_logs('/var/log', max_lines=500)

    # 扫描敏感信息
    print(Colors.yellow("[7/7] 扫描敏感信息... / Scanning for sensitive information..."))
    monitor.scan_secrets_in_files('/var/log', max_files=30)
    monitor.scan_secrets_in_files('/etc', max_files=20)
    
    # 生成彩色报告
    print("\n")
    print(monitor.generate_report(use_colors=use_colors))
    
    # 返回扫描结果
    return {
        'timestamp': datetime.now().isoformat(),
        'safe_items': monitor.safe_items,
        'violations': monitor.violations,
        'warnings': monitor.warnings,
        'summary': {
            'total_safe': len(monitor.safe_items),
            'total_violations': len(monitor.violations),
            'total_warnings': len(monitor.warnings),
            'status': 'safe' if len(monitor.violations) == 0 and len(monitor.warnings) == 0 else 'warning' if len(monitor.violations) == 0 else 'critical'
        }
    }


def main():
    """主函数"""
    import sys
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='安全监控工具')
    parser.add_argument(
        '--continuous', '-c',
        action='store_true',
        help='持续监控模式,每隔指定时间自动扫描'
    )
    parser.add_argument(
        '--interval', '-i',
        type=int,
        default=300,
        help='扫描间隔时间(秒),默认300秒(5分钟)'
    )
    parser.add_argument(
        '--no-color',
        action='store_true',
        help='禁用彩色输出'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='将结果保存到指定文件'
    )
    args = parser.parse_args()
    
    # 检测终端是否支持颜色
    use_colors = True
    if args.no_color:
        use_colors = False
    else:
        try:
            if not sys.stdout.isatty():
                use_colors = False
        except:
            use_colors = False
    
    if args.continuous:
        # 持续监控模式
        print(Colors.bold(Colors.cyan("=" * 80)))
        print(Colors.bold(Colors.cyan("🔄 持续安全监控模式")))
        print(Colors.blue("📅 启动时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(Colors.blue(f"⏰ 扫描间隔: {args.interval}秒"))
        print(Colors.yellow("💡 提示: 按 Ctrl+C 停止监控"))
        print(Colors.cyan("=" * 80))
        print()
        
        scan_count = 0
        while True:
            scan_count += 1
            print(Colors.bold(Colors.cyan(f"\n{'='*80}")))
            print(Colors.bold(Colors.cyan(f"📊 第 {scan_count} 次扫描 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")))
            print(Colors.cyan(f"{'='*80}"))
            
            # 执行扫描
            result = run_scan(use_colors=use_colors)
            
            # 输出JSON格式
            if args.output:
                try:
                    with open(args.output, 'w', encoding='utf-8') as f:
                        f.write(json.dumps(result, indent=2, ensure_ascii=False))
                    print(Colors.green(f"\n✓ 结果已保存到: {args.output}"))
                except Exception as e:
                    print(Colors.red(f"\n✗ 保存文件失败: {e}"))
            else:
                print(Colors.blue("\n📄 JSON格式输出:"))
                print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 等待下一次扫描
            print(Colors.cyan(f"\n⏳ 下次扫描将在 {args.interval} 秒后开始..."))
            print(Colors.cyan("   (按 Ctrl+C 停止监控)\n"))
            
            try:
                import time
                time.sleep(args.interval)
            except KeyboardInterrupt:
                print(Colors.yellow("\n\n⚠️  监控已停止"))
                print(Colors.green(f"✓ 共执行了 {scan_count} 次扫描"))
                print(Colors.cyan(f"📅 停止时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
                # 显示最终报告和建议
                show_final_suggestions(use_colors)
                break
    else:
        # 单次扫描模式(默认)
        print(Colors.bold(Colors.cyan("🔍 开始安全监控扫描...")))
        print(Colors.blue("💡 注意: 部分检测需要root权限以获取完整信息\n"))
        
        # 执行扫描
        result = run_scan(use_colors=use_colors)
        
        # 输出JSON格式
        if args.output:
            try:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(json.dumps(result, indent=2, ensure_ascii=False))
                print(Colors.green(f"\n✓ 结果已保存到: {args.output}"))
            except Exception as e:
                print(Colors.red(f"\n✗ 保存文件失败: {e}"))
        else:
            print(Colors.blue("\n📄 JSON格式输出(可保存为文件):"))
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # 询问是否进入持续监控模式
        if not args.output and use_colors:  # 只在交互式终端中询问
            ask_continuous_monitoring(use_colors, args.interval)


def show_final_suggestions(use_colors: bool = True):
    """显示最终报告和操作建议"""
    print(Colors.bold(Colors.cyan("\n" + "=" * 80)))
    print(Colors.bold(Colors.cyan("📋 本次扫描总结与建议")))
    print(Colors.cyan("=" * 80))
    
    print(Colors.yellow("\n💡 你可以进行的操作:"))
    print(Colors.green("  1. 查看详细日志:"))
    print(Colors.blue("     - 系统日志: tail -f /var/log/syslog"))
    print(Colors.blue("     - 认证日志: tail -f /var/log/auth.log"))
    print(Colors.blue("     - VNC日志: journalctl -u vncserver -f"))
    
    print(Colors.green("\n  2. 检查可疑进程:"))
    print(Colors.blue("     - 查看进程详情: ps -p <PID> -f"))
    print(Colors.blue("     - 终止进程: kill <PID>"))
    
    print(Colors.green("\n  3. 检查网络连接:"))
    print(Colors.blue("     - 查看连接: ss -tunap"))
    print(Colors.blue("     - 封禁IP: ufw deny from <IP>"))
    
    print(Colors.green("\n  4. 修复安全问题:"))
    print(Colors.blue("     - 修改VNC配置: nano ~/.vnc/config"))
    print(Colors.blue("     - 设置VNC密码: vncpasswd"))
    print(Colors.blue("     - 配置防火墙: ufw enable"))
    
    print(Colors.green("\n  5. 继续监控:"))
    print(Colors.blue("     - 单次扫描: sudo python3 scripts/monitor.py"))
    print(Colors.blue("     - 持续监控: sudo python3 scripts/monitor.py --continuous"))
    print(Colors.blue("     - 自定义间隔: sudo python3 scripts/monitor.py -c -i 60"))
    
    print(Colors.green("\n  6. 查看帮助文档:"))
    print(Colors.blue("     - 小白入门: cat 小白入门指南.md"))
    print(Colors.blue("     - VNC安全: cat VNC安全检查说明.md"))
    print(Colors.blue("     - 持续监控: cat 持续监控使用说明.md"))
    
    print(Colors.cyan("\n" + "=" * 80))


def ask_continuous_monitoring(use_colors: bool, default_interval: int):
    """询问是否进入持续监控模式"""
    print(Colors.bold(Colors.cyan("\n" + "=" * 80)))
    print(Colors.bold(Colors.cyan("❓ 是否进入持续监控模式?")))
    print(Colors.cyan("=" * 80))
    
    print(Colors.yellow("\n持续监控模式会:"))
    print(Colors.green("  ✓ 自动定期扫描系统安全"))
    print(Colors.green("  ✓ 实时发现VNC裸奔等问题"))
    print(Colors.green("  ✓ 一直运行直到手动停止"))
    print(Colors.red("  ✗ 按任意时间按 Ctrl+C 可停止"))
    
    print(Colors.yellow("\n扫描间隔选项:"))
    print(Colors.blue("  1) 30秒  (高频监控)"))
    print(Colors.blue("  2) 1分钟  (推荐测试环境)"))
    print(Colors.blue("  3) 5分钟  (默认,推荐生产环境)"))
    print(Colors.blue("  4) 10分钟 (低频率监控)"))
    print(Colors.blue("  5) 自定义间隔"))
    print(Colors.red("  0) 退出监控\n"))
    
    try:
        choice = input(Colors.cyan("请选择 (0-5): ")).strip()
        
        if choice == '0':
            print(Colors.green("\n✓ 已退出监控"))
            show_final_suggestions(use_colors)
            return
        
        interval_map = {
            '1': 30,
            '2': 60,
            '3': 300,
            '4': 600
        }
        
        if choice in interval_map:
            interval = interval_map[choice]
        elif choice == '5':
            interval_input = input(Colors.cyan("请输入扫描间隔(秒,最小30): ")).strip()
            try:
                interval = int(interval_input)
                if interval < 30:
                    print(Colors.yellow("⚠️  间隔小于30秒,已调整为30秒"))
                    interval = 30
            except ValueError:
                print(Colors.red("✗ 输入无效,使用默认300秒"))
                interval = 300
        else:
            print(Colors.red("✗ 无效选择,已退出"))
            show_final_suggestions(use_colors)
            return
        
        # 进入持续监控模式
        print(Colors.bold(Colors.cyan("\n" + "=" * 80)))
        print(Colors.bold(Colors.cyan("🔄 持续安全监控模式")))
        print(Colors.blue("📅 启动时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(Colors.blue(f"⏰ 扫描间隔: {interval}秒"))
        print(Colors.yellow("💡 提示: 按 Ctrl+C 随时停止监控并查看报告"))
        print(Colors.cyan("=" * 80))
        print()
        
        scan_count = 0
        while True:
            scan_count += 1
            print(Colors.bold(Colors.cyan(f"\n{'='*80}")))
            print(Colors.bold(Colors.cyan(f"📊 第 {scan_count} 次扫描 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")))
            print(Colors.cyan(f"{'='*80}"))
            
            # 执行扫描
            result = run_scan(use_colors=use_colors)
            
            # 输出JSON格式
            print(Colors.blue("\n📄 JSON格式输出:"))
            print(json.dumps(result, indent=2, ensure_ascii=False))
            
            # 等待下一次扫描
            print(Colors.cyan(f"\n⏳ 下次扫描将在 {interval} 秒后开始..."))
            print(Colors.cyan("   (按 Ctrl+C 停止监控)\n"))
            
            try:
                import time
                time.sleep(interval)
            except KeyboardInterrupt:
                print(Colors.yellow("\n\n⚠️  监控已停止"))
                print(Colors.green(f"✓ 共执行了 {scan_count} 次扫描"))
                print(Colors.cyan(f"📅 停止时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"))
                show_final_suggestions(use_colors)
                break
    
    except (EOFError, KeyboardInterrupt):
        print(Colors.green("\n\n✓ 已退出监控"))
        show_final_suggestions(use_colors)


if __name__ == '__main__':
    main()
