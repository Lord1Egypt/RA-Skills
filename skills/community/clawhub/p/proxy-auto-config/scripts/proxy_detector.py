#!/usr/bin/env python3
"""
代理自动检测和配置脚本
用于自动检测系统中的代理设置并配置 OpenClaw 环境
支持 v2ray、Clash、SS/SSR 等常见代理工具
"""

import os
import sys
import re
import json
import subprocess
import socket
from typing import Dict, List, Optional, Tuple
import psutil

class ProxyDetector:
    """代理检测和配置类"""
    
    def __init__(self):
        self.current_proxy = None
        self.detected_proxies = []
        self.openclaw_config = {}
        
    def detect_all_proxies(self) -> List[Dict]:
        """检测系统中所有可用的代理"""
        proxies = []
        
        # 1. 检测环境变量中的代理
        env_proxies = self._detect_env_proxies()
        proxies.extend(env_proxies)
        
        # 2. 检测正在运行的代理进程
        process_proxies = self._detect_process_proxies()
        proxies.extend(process_proxies)
        
        # 3. 检测监听端口的代理服务
        port_proxies = self._detect_port_proxies()
        proxies.extend(port_proxies)
        
        # 4. 检测配置文件中的代理
        config_proxies = self._detect_config_proxies()
        proxies.extend(config_proxies)
        
        self.detected_proxies = proxies
        return proxies
    
    def _detect_env_proxies(self) -> List[Dict]:
        """检测环境变量中的代理设置"""
        proxies = []
        env_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'ALL_PROXY', 'http_proxy', 'https_proxy', 'all_proxy']
        
        for var in env_vars:
            value = os.getenv(var)
            if value:
                proxy_type = self._parse_proxy_url(value)
                if proxy_type:
                    proxies.append({
                        'type': 'environment',
                        'variable': var,
                        'url': value,
                        'proxy_type': proxy_type[0],
                        'host': proxy_type[1],
                        'port': proxy_type[2],
                        'priority': 1
                    })
        
        return proxies
    
    def _detect_process_proxies(self) -> List[Dict]:
        """检测正在运行的代理进程"""
        proxies = []
        
        # 常见代理进程关键词
        proxy_keywords = [
            'v2ray', 'xray', 'clash', 'ss-local', 'ssr-local',
            'trojan', 'brook', 'hysteria', 'naiveproxy',
            'qv2ray', 'v2rayN', 'clash-verge'
        ]
        
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'exe']):
                try:
                    proc_info = proc.info
                    name = proc_info.get('name', '').lower()
                    exe = proc_info.get('exe', '').lower()
                    cmdline = ' '.join(proc_info.get('cmdline', []))
                    
                    for keyword in proxy_keywords:
                        if (keyword in name or 
                            keyword in exe or 
                            keyword in cmdline):
                            
                            # 尝试从命令行参数提取端口
                            port = self._extract_port_from_cmdline(cmdline)
                            
                            proxies.append({
                                'type': 'process',
                                'name': proc_info.get('name', 'unknown'),
                                'pid': proc_info.get('pid'),
                                'exe': exe,
                                'port': port,
                                'priority': 2
                            })
                            break
                            
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
                    
        except Exception as e:
            print(f"检测进程时出错: {e}", file=sys.stderr)
        
        return proxies
    
    def _detect_port_proxies(self) -> List[Dict]:
        """检测监听端口的代理服务"""
        proxies = []
        
        # 常见代理端口
        common_proxy_ports = [
            1080, 1081, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090,
            10808, 10809, 10810,  # v2rayN 常用端口
            7890, 7891, 7892, 7893,  # Clash 常用端口
            10800, 10801, 10802,
            8118, 8123,  # Privoxy
            9050,  # Tor
            8080, 8081, 8082,  # HTTP 代理
            8888, 8889,  # 其他常见端口
        ]
        
        try:
            # 使用 ss 命令检测监听端口
            result = subprocess.run(['ss', '-tlnp'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=5)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    for port in common_proxy_ports:
                        if f':{port}' in line:
                            # 提取进程信息
                            match = re.search(r'users:\(\(\"([^\"]+)\",pid=(\d+)', line)
                            if match:
                                process_name = match.group(1)
                                pid = match.group(2)
                                
                                proxies.append({
                                    'type': 'port',
                                    'port': port,
                                    'process': process_name,
                                    'pid': pid,
                                    'priority': 3
                                })
        
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception) as e:
            # 如果 ss 命令不可用，尝试其他方法
            try:
                for port in common_proxy_ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    result = sock.connect_ex(('127.0.0.1', port))
                    sock.close()
                    
                    if result == 0:
                        proxies.append({
                            'type': 'port',
                            'port': port,
                            'process': 'unknown',
                            'priority': 3
                        })
                        
            except Exception:
                pass
        
        return proxies
    
    def _detect_config_proxies(self) -> List[Dict]:
        """检测配置文件中的代理设置"""
        proxies = []
        
        # 常见代理配置文件路径
        config_paths = [
            # v2ray/v2rayN 配置
            os.path.expanduser('~/桌面/v2rayN-linux-64/guiConfigs/config.json'),
            os.path.expanduser('~/.config/v2ray/config.json'),
            os.path.expanduser('~/.v2ray/config.json'),
            
            # Clash 配置
            os.path.expanduser('~/.config/clash/config.yaml'),
            os.path.expanduser('~/.config/clash/config.yml'),
            os.path.expanduser('~/桌面/Clash/config.yaml'),
            
            # 系统代理配置
            os.path.expanduser('~/.bashrc'),
            os.path.expanduser('~/.zshrc'),
            os.path.expanduser('~/.profile'),
            os.path.expanduser('~/.bash_profile'),
            
            # GNOME/KDE 代理设置
            os.path.expanduser('~/.config/proxy'),
        ]
        
        for config_path in config_paths:
            if os.path.exists(config_path):
                try:
                    with open(config_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # 查找代理URL
                        proxy_patterns = [
                            r'(socks5?://[^\s"\']+)',
                            r'(http://[^\s"\']+)',
                            r'(https://[^\s"\']+)',
                            r'export\s+(HTTP|HTTPS|ALL)_PROXY=([^\s]+)',
                            r'port:\s*(\d+)',
                            r'"port"\s*:\s*(\d+)',
                        ]
                        
                        for pattern in proxy_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                if isinstance(match, tuple):
                                    match = match[-1]
                                
                                proxy_type = self._parse_proxy_url(match)
                                if proxy_type:
                                    proxies.append({
                                        'type': 'config',
                                        'config_file': config_path,
                                        'url': match,
                                        'proxy_type': proxy_type[0],
                                        'host': proxy_type[1],
                                        'port': proxy_type[2],
                                        'priority': 4
                                    })
                                    
                except Exception as e:
                    continue
        
        return proxies
    
    def _parse_proxy_url(self, url: str) -> Optional[Tuple[str, str, int]]:
        """解析代理URL"""
        patterns = [
            (r'socks5://([^:]+):(\d+)', 'socks5'),
            (r'socks4://([^:]+):(\d+)', 'socks4'),
            (r'http://([^:]+):(\d+)', 'http'),
            (r'https://([^:]+):(\d+)', 'https'),
        ]
        
        for pattern, proxy_type in patterns:
            match = re.match(pattern, url)
            if match:
                host = match.group(1)
                port = int(match.group(2))
                return (proxy_type, host, port)
        
        return None
    
    def _extract_port_from_cmdline(self, cmdline: str) -> Optional[int]:
        """从命令行参数提取端口号"""
        patterns = [
            r'--port\s+(\d+)',
            r'-p\s+(\d+)',
            r'port=(\d+)',
            r'"port":\s*(\d+)',
            r"'port':\s*(\d+)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, cmdline)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
        
        return None
    
    def select_best_proxy(self) -> Optional[Dict]:
        """选择最佳的代理配置"""
        if not self.detected_proxies:
            return None
        
        # 按优先级排序
        sorted_proxies = sorted(self.detected_proxies, 
                              key=lambda x: x.get('priority', 0))
        
        # 优先选择环境变量中的代理
        for proxy in sorted_proxies:
            if proxy['type'] == 'environment':
                return proxy
        
        # 其次选择正在运行的进程
        for proxy in sorted_proxies:
            if proxy['type'] == 'process' and proxy.get('port'):
                return proxy
        
        # 最后选择端口监听的代理
        for proxy in sorted_proxies:
            if proxy['type'] == 'port':
                return proxy
        
        return sorted_proxies[0] if sorted_proxies else None
    
    def configure_openclaw(self, proxy_config: Dict) -> bool:
        """配置 OpenClaw 使用代理"""
        try:
            # 构建代理URL
            proxy_url = None
            if 'url' in proxy_config:
                proxy_url = proxy_config['url']
            elif 'host' in proxy_config and 'port' in proxy_config:
                proxy_type = proxy_config.get('proxy_type', 'socks5')
                proxy_url = f"{proxy_type}://{proxy_config['host']}:{proxy_config['port']}"
            
            if not proxy_url:
                return False
            
            # 设置环境变量
            os.environ['HTTP_PROXY'] = proxy_url
            os.environ['HTTPS_PROXY'] = proxy_url
            os.environ['ALL_PROXY'] = proxy_url
            
            # 对于 Python requests 库
            os.environ['REQUESTS_CA_BUNDLE'] = ''
            
            # 保存配置
            self.current_proxy = {
                'url': proxy_url,
                'type': proxy_config.get('proxy_type', 'unknown'),
                'source': proxy_config.get('type', 'unknown'),
                'timestamp': time.time()
            }
            
            return True
            
        except Exception as e:
            print(f"配置代理时出错: {e}", file=sys.stderr)
            return False
    
    def test_proxy_connection(self, proxy_url: str) -> bool:
        """测试代理连接是否可用"""
        try:
            import requests
            
            # 设置代理
            proxies = {
                'http': proxy_url,
                'https': proxy_url
            }
            
            # 测试连接
            response = requests.get('http://httpbin.org/ip', 
                                  proxies=proxies, 
                                  timeout=10)
            
            return response.status_code == 200
            
        except Exception:
            return False
    
    def generate_config_script(self) -> str:
        """生成配置脚本"""
        script = """#!/bin/bash
# OpenClaw 代理自动配置脚本
# 生成时间: $(date)

# 清除现有代理设置
unset HTTP_PROXY
unset HTTPS_PROXY
unset ALL_PROXY
unset http_proxy
unset https_proxy
unset all_proxy

# 设置代理
"""
        
        if self.current_proxy:
            proxy_url = self.current_proxy['url']
            script += f"""
export HTTP_PROXY="{proxy_url}"
export HTTPS_PROXY="{proxy_url}"
export ALL_PROXY="{proxy_url}"

# 对于 Python
export REQUESTS_CA_BUNDLE=""

echo "代理已配置: {proxy_url}"
echo "代理类型: {self.current_proxy['type']}"
echo "来源: {self.current_proxy['source']}"
"""
        else:
            script += """
echo "未检测到可用代理，使用直连模式"
"""
        
        return script
    
    def save_configuration(self, output_dir: str = "./proxy_config") -> Dict:
        """保存配置到文件"""
        import time
        
        os.makedirs(output_dir, exist_ok=True)
        
        config = {
            'detected_at': time.time(),
            'detected_proxies': self.detected_proxies,
            'selected_proxy': self.current_proxy,
            'environment': {
                'HTTP_PROXY': os.getenv('HTTP_PROXY'),
                'HTTPS_PROXY': os.getenv('HTTPS_PROXY'),
                'ALL_PROXY': os.getenv('ALL_PROXY')
            }
        }
        
        # 保存JSON配置
        json_path = os.path.join(output_dir, 'proxy_config.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        # 生成并保存Bash脚本
        script = self.generate_config_script()
        script_path = os.path.join(output_dir, 'configure_proxy.sh')
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script)
        
        # 使脚本可执行
        os.chmod(script_path, 0o755)
        
        return {
            'json_config': json_path,
            'bash_script': script_path,
            'config': config
        }


def main():
    """命令行入口点"""
    import argparse
    
    parser = argparse.ArgumentParser(description='代理自动检测和配置')
    parser.add_argument('--test', action='store_true', help='测试代理连接')
    parser.add_argument('--configure', action='store_true', help='自动配置环境')
    parser.add_argument('--output', default='./proxy_config', help='输出目录')
    parser.add_argument('--verbose', action='store_true', help='详细输出')
    
    args = parser.parse_args()
    
    detector = ProxyDetector()
    
    print("=" * 60)
    print("代理自动检测和配置工具")
    print("=" * 60)
    
    # 检测代理
    print("\n🔍 正在检测系统中的代理...")
    proxies = detector.detect_all_proxies()
    
    if not proxies:
        print("❌ 未检测到任何代理配置")
        sys.exit(1)
    
    print(f"✅ 检测到 {len(proxies)} 个代理配置:")
    
    for i, proxy in enumerate(proxies, 1):
        print(f"\n{i}. 类型: {proxy['type']}")
        if 'url' in proxy:
            print(f"   URL: {proxy['url']}")
        if 'port' in proxy:
            print(f"   端口: {proxy['port']}")
        if 'process' in proxy:
            print(f"   进程: {proxy['process']}")
        if 'pid' in proxy:
            print(f"   PID: {proxy['pid']}")
    
    # 选择最佳代理
    print("\n🎯 选择最佳代理配置...")
    best_proxy = detector.select_best_proxy()
    
    if best_proxy:
        print(f"✅ 选择代理: {best_proxy.get('url', best_proxy.get('port', '未知'))}")
        
        # 配置代理
        if args.configure:
            print("\n⚙️  正在配置环境...")
            if detector.configure_openclaw(best_proxy):
                print("✅ 环境配置成功")
                
                # 测试连接
                if args.test:
                    print("\n📡 测试代理连接...")
                    proxy_url = best_proxy.get('url') or f"socks5://127.0.0.1:{best_proxy.get('port')}"
                    if detector.test_proxy_connection(proxy_url):
                        print("✅ 代理连接测试成功")
                    else:
                        print("❌ 代理连接测试失败")
            else:
                print("❌ 环境配置失败")
        
        # 保存配置
        print(f"\n💾 保存配置到: {args.output}")
        saved_files = detector.save_configuration(args.output)
        
        print(f"   JSON配置: {saved_files['json_config']}")
        print(f"   Bash脚本: {saved_files['bash_script']}")
        
        print("\n🎉 配置完成！")
        print("\n使用方法:")
        print(f"1. 执行脚本: source {saved_files['bash_script']}")
