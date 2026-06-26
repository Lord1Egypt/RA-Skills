"""
网络检查模块

该模块提供网络安全性检查功能，包括端口扫描、服务识别、网络配置检查等功能。
"""

import socket
import ssl
import subprocess
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse


class NetworkChecker:
    """
    网络安全检查器
    
    提供多种网络相关的安全检查功能，包括端口开放情况、SSL证书检查、
    网络服务识别等。
    """
    
    def __init__(self, timeout: int = 5):
        """
        初始化网络检查器
        
        Args:
            timeout (int): 网络请求超时时间（秒）
        """
        self.timeout = timeout
        self.common_ports = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 
                            1723, 3306, 3389, 5900, 8080, 8443]
        
    def check_port_open(self, host: str, port: int) -> bool:
        """
        检查指定主机的端口是否开放
        
        Args:
            host (str): 目标主机地址
            port (int): 端口号
            
        Returns:
            bool: 端口是否开放
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except Exception:
            return False
    
    def check_ssl_certificate(self, url: str) -> Optional[Dict[str, str]]:
        """
        检查网站SSL证书信息
        
        Args:
            url (str): 目标URL
            
        Returns:
            Optional[Dict[str, str]]: SSL证书信息，如果无法获取则返回None
        """
        try:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            port = parsed_url.port or 443
            
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    
            cert_info = {
                'subject': str(cert['subject']),
                'issuer': str(cert['issuer']),
                'version': str(cert['version']),
                'serial_number': str(cert.get('serialNumber', 'N/A')),
                'not_before': cert.get('notBefore', 'N/A'),
                'not_after': cert.get('notAfter', 'N/A')
            }
            
            return cert_info
        except Exception:
            return None
    
    def scan_common_ports(self, host: str) -> Dict[int, str]:
        """
        扫描常见端口
        
        Args:
            host (str): 目标主机地址
            
        Returns:
            Dict[int, str]: 开放端口及其可能的服务
        """
        open_ports = {}
        for port in self.common_ports:
            if self.check_port_open(host, port):
                service_name = self._get_service_name(port)
                open_ports[port] = service_name
                
        return open_ports
    
    def _get_service_name(self, port: int) -> str:
        """
        获取端口对应的服务名称
        
        Args:
            port (int): 端口号
            
        Returns:
            str: 服务名称
        """
        service_map = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            111: 'RPCBind',
            135: 'MSRPC',
            139: 'NetBIOS',
            143: 'IMAP',
            443: 'HTTPS',
            993: 'IMAPS',
            995: 'POP3S',
            1723: 'PPTP',
            3306: 'MySQL',
            3389: 'RDP',
            5900: 'VNC',
            8080: 'HTTP-Alt',
            8443: 'HTTPS-Alt'
        }
        return service_map.get(port, f'Unknown Port {port}')
    
    def check_firewall_status(self) -> Optional[Dict[str, str]]:
        """
        检查防火墙状态（仅支持Windows和Linux）
        
        Returns:
            Optional[Dict[str, str]]: 防火墙状态信息
        """
        try:
            import platform
            system = platform.system().lower()
            
            if system == 'windows':
                result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                      capture_output=True, text=True, timeout=self.timeout)
                if result.returncode == 0:
                    return {'status': 'success', 'output': result.stdout}
            elif system == 'linux':
                # 检查iptables状态
                try:
                    result = subprocess.run(['iptables', '-L'], 
                                          capture_output=True, text=True, timeout=self.timeout)
                    if result.returncode == 0:
                        return {'status': 'success', 'output': result.stdout}
                except FileNotFoundError:
                    # 尝试检查ufw状态
                    try:
                        result = subprocess.run(['ufw', 'status'], 
                                              capture_output=True, text=True, timeout=self.timeout)
                        if result.returncode == 0:
                            return {'status': 'success', 'output': result.stdout}
                    except FileNotFoundError:
                        pass
        except Exception:
            pass
        return None
    
    def check_network_connectivity(self, target_hosts: List[str]) -> Dict[str, bool]:
        """
        检查网络连通性
        
        Args:
            target_hosts (List[str]): 目标主机列表
            
        Returns:
            Dict[str, bool]: 主机连通性状态
        """
        connectivity_results = {}
        
        for host in target_hosts:
            try:
                # 尝试ping主机
                import platform
                system = platform.system().lower()
                
                if system == 'windows':
                    result = subprocess.run(['ping', '-n', '1', '-w', f'{self.timeout * 1000}', host], 
                                          capture_output=True, text=True, timeout=self.timeout+1)
                else:
                    result = subprocess.run(['ping', '-c', '1', '-W', str(self.timeout), host], 
                                          capture_output=True, text=True, timeout=self.timeout+1)
                
                connectivity_results[host] = result.returncode == 0
            except Exception:
                connectivity_results[host] = False
                
        return connectivity_results
    
    def get_local_ip_addresses(self) -> List[str]:
        """
        获取本地IP地址
        
        Returns:
            List[str]: 本地IP地址列表
        """
        try:
            import netifaces
            ip_addresses = []
            
            for interface in netifaces.interfaces():
                addresses = netifaces.ifaddresses(interface)
                if netifaces.AF_INET in addresses:
                    for addr_info in addresses[netifaces.AF_INET]:
                        ip_address = addr_info['addr']
                        if not ip_address.startswith('127.'):  # 排除回环地址
                            ip_addresses.append(ip_address)
                            
            return ip_addresses
        except ImportError:
            # 如果没有netifaces，使用socket获取
            try:
                hostname = socket.gethostname()
                local_ips = socket.gethostbyname_ex(hostname)[2]
                return [ip for ip in local_ips if not ip.startswith('127.')]
            except Exception:
                return []
    
    def check_dns_resolution(self, domain: str) -> Optional[List[str]]:
        """
        检查域名解析
        
        Args:
            domain (str): 域名
            
        Returns:
            Optional[List[str]]: 解析到的IP地址列表
        """
        try:
            ip_addresses = socket.gethostbyname_ex(domain)[2]
            return ip_addresses
        except Exception:
            return None