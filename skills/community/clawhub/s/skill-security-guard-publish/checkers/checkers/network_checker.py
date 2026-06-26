"""
网络检查模块

该模块提供网络安全性检查功能，包括端口扫描、服务识别、网络配置检查等功能。
"""

import socket
import ssl
import subprocess
import platform
from typing import List, Dict, Optional, Tuple
from urllib.parse import urlparse


class NetworkChecker:
    """
    网络安全检查器
    
    提供多种网络相关的安全检查功能，包括端口开放情况、SSL证书检查、
    网络服务识别等。
    """
    
    def __init__(self, timeout: int = 5) -> None:
        """
        初始化网络检查器
        
        Args:
            timeout: 网络请求超时时间（秒）
        """
        self.timeout: int = timeout
        self.common_ports: List[int] = [21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 
                            1723, 3306, 3389, 5900, 8080, 8443]
        
    def check_port_open(self, host: str, port: int) -> bool:
        """
        检查指定主机的端口是否开放
        
        Args:
            host: 目标主机地址
            port: 端口号
            
        Returns:
            端口是否开放
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except socket.gaierror:
            error_msg = f"错误：无法解析主机地址 {host}\n"
            error_msg += "请检查主机地址是否正确，确保网络连接正常。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认主机地址拼写正确\n"
            error_msg += "- 检查网络连接是否正常\n"
            error_msg += "- 验证DNS解析是否正常\n"
            print(error_msg)
            return False
        except socket.timeout:
            error_msg = f"错误：连接 {host}:{port} 超时\n"
            error_msg += "连接目标主机超时，请检查网络状况或目标主机状态。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查网络连接是否正常\n"
            error_msg += "- 确认目标主机是否在线\n"
            error_msg += "- 验证端口是否对外开放\n"
            print(error_msg)
            return False
        except ConnectionRefusedError:
            # 端口关闭或被拒绝连接
            return False
        except Exception as e:
            error_msg = f"检查端口时发生错误: {str(e)}\n"
            error_msg += f"目标: {host}:{port}\n"
            error_msg += "这可能是因为网络问题、防火墙阻止或其他连接错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查网络连接是否正常\n"
            error_msg += "- 验证防火墙设置\n"
            error_msg += "- 确认目标主机和端口是否可达\n"
            print(error_msg)
            return False
    
    def check_ssl_certificate(self, url: str) -> Optional[Dict[str, str]]:
        """
        检查网站SSL证书信息
        
        Args:
            url: 目标URL
            
        Returns:
            SSL证书信息，如果无法获取则返回None
        """
        try:
            parsed_url = urlparse(url)
            host = parsed_url.hostname
            if not host:
                error_msg = f"错误：无法从URL解析主机名 {url}\n"
                error_msg += "请检查URL格式是否正确。\n"
                error_msg += "解决方案：\n"
                error_msg += "- 确认URL格式正确（例如：https://example.com）\n"
                error_msg += "- 验证URL是否包含有效主机名\n"
                print(error_msg)
                return None
            port = parsed_url.port or 443
            
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=self.timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    
            cert_info: Dict[str, str] = {
                'subject': str(cert['subject']),
                'issuer': str(cert['issuer']),
                'version': str(cert['version']),
                'serial_number': str(cert.get('serialNumber', 'N/A')),
                'not_before': cert.get('notBefore', 'N/A'),
                'not_after': cert.get('notAfter', 'N/A')
            }
            
            return cert_info
        except socket.gaierror:
            error_msg = f"错误：无法解析主机地址 {host}\n"
            error_msg += "请检查主机地址是否正确，确保网络连接正常。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认主机地址拼写正确\n"
            error_msg += "- 检查网络连接是否正常\n"
            error_msg += "- 验证DNS解析是否正常\n"
            print(error_msg)
            return None
        except ssl.SSLError as e:
            error_msg = f"SSL错误：{str(e)}\n"
            error_msg += f"无法获取 {url} 的SSL证书信息。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查目标站点SSL配置\n"
            error_msg += "- 验证SSL证书是否有效\n"
            error_msg += "- 确认端口443（或指定端口）是否开放\n"
            print(error_msg)
            return None
        except socket.timeout:
            error_msg = f"错误：连接 {url} 超时\n"
            error_msg += "连接目标主机超时，请检查网络状况或目标主机状态。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查网络连接是否正常\n"
            error_msg += "- 确认目标主机是否在线\n"
            error_msg += "- 验证SSL端口是否对外开放\n"
            print(error_msg)
            return None
        except Exception as e:
            error_msg = f"检查SSL证书时发生错误: {str(e)}\n"
            error_msg += f"URL: {url}\n"
            error_msg += "这可能是因为网络问题、SSL配置错误或其他连接错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查网络连接是否正常\n"
            error_msg += "- 验证SSL证书是否有效\n"
            error_msg += "- 确认目标主机和端口是否可达\n"
            print(error_msg)
            return None
    
    def scan_common_ports(self, host: str) -> Dict[int, str]:
        """
        扫描常见端口
        
        Args:
            host: 目标主机地址
            
        Returns:
            开放端口及其可能的服务
        """
        open_ports: Dict[int, str] = {}
        for port in self.common_ports:
            if self.check_port_open(host, port):
                service_name = self._get_service_name(port)
                open_ports[port] = service_name
                
        return open_ports
    
    def _get_service_name(self, port: int) -> str:
        """
        获取端口对应的服务名称
        
        Args:
            port: 端口号
            
        Returns:
            服务名称
        """
        service_map: Dict[int, str] = {
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
            防火墙状态信息
        """
        try:
            system = platform.system().lower()
            
            if system == 'windows':
                try:
                    result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles'], 
                                          capture_output=True, text=True, timeout=self.timeout)
                    if result.returncode == 0:
                        return {'status': 'success', 'output': result.stdout}
                    else:
                        return {'status': 'error', 'output': result.stderr}
                except subprocess.TimeoutExpired:
                    error_msg = "错误：检查防火墙状态超时\n"
                    error_msg += "解决方案：\n"
                    error_msg += "- 检查系统性能是否正常\n"
                    error_msg += "- 确认是否有足够的系统资源\n"
                    print(error_msg)
                    return {'status': 'timeout', 'output': 'Command timed out'}
                except FileNotFoundError:
                    error_msg = "错误：找不到netsh命令\n"
                    error_msg += "可能原因是系统环境变量配置问题。\n"
                    error_msg += "解决方案：\n"
                    error_msg += "- 确认系统为Windows系统\n"
                    error_msg += "- 检查系统环境变量配置\n"
                    print(error_msg)
                    return {'status': 'error', 'output': 'netsh command not found'}
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
                        # 如果都没有，尝试systemctl检查防火墙
                        try:
                            result = subprocess.run(['systemctl', 'status', 'firewalld'], 
                                                  capture_output=True, text=True, timeout=self.timeout)
                            if result.returncode == 0:
                                return {'status': 'success', 'output': result.stdout}
                        except FileNotFoundError:
                            pass
            else:
                return {'status': 'unsupported', 'output': f'System {system} not supported'}
        except subprocess.TimeoutExpired:
            error_msg = "错误：检查防火墙状态超时\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查系统性能是否正常\n"
            error_msg += "- 确认是否有足够的系统资源\n"
            print(error_msg)
            return {'status': 'timeout', 'output': 'Command timed out'}
        except Exception as e:
            error_msg = f"检查防火墙状态时发生错误: {str(e)}\n"
            error_msg += "这可能是因为权限不足、系统不支持或其他系统错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认以足够权限运行\n"
            error_msg += "- 验证系统是否支持防火墙检查\n"
            error_msg += "- 检查系统状态是否正常\n"
            print(error_msg)
            return {'status': 'error', 'output': str(e)}
        return None
    
    def check_network_connectivity(self, target_hosts: List[str]) -> Dict[str, bool]:
        """
        检查网络连通性
        
        Args:
            target_hosts: 目标主机列表
            
        Returns:
            主机连通性状态
        """
        connectivity_results: Dict[str, bool] = {}
        
        for host in target_hosts:
            try:
                # 尝试ping主机
                system = platform.system().lower()
                
                if system == 'windows':
                    result = subprocess.run(['ping', '-n', '1', '-w', f'{self.timeout * 1000}', host], 
                                          capture_output=True, text=True, timeout=self.timeout+1)
                else:
                    result = subprocess.run(['ping', '-c', '1', '-W', str(self.timeout), host], 
                                          capture_output=True, text=True, timeout=self.timeout+1)
                
                connectivity_results[host] = result.returncode == 0
            except subprocess.TimeoutExpired:
                connectivity_results[host] = False
                error_msg = f"警告：ping {host} 超时\n"
                error_msg += "目标主机可能不响应或网络连接存在问题。\n"
                print(error_msg)
            except Exception as e:
                connectivity_results[host] = False
                error_msg = f"检查 {host} 连通性时发生错误: {str(e)}\n"
                error_msg += "这可能是因为主机名解析失败、网络问题或其他系统错误导致的。\n"
                error_msg += "解决方案：\n"
                error_msg += "- 检查主机名是否正确\n"
                error_msg += "- 验证网络连接是否正常\n"
                error_msg += "- 确认ping命令是否可用\n"
                print(error_msg)
                
        return connectivity_results
    
    def get_local_ip_addresses(self) -> List[str]:
        """
        获取本地IP地址
        
        Returns:
            本地IP地址列表
        """
        try:
            import netifaces
            ip_addresses: List[str] = []
            
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
            except Exception as e:
                error_msg = f"获取本地IP地址时发生错误: {str(e)}\n"
                error_msg += "这可能是因为系统配置问题或其他网络错误导致的。\n"
                error_msg += "解决方案：\n"
                error_msg += "- 确认网络配置是否正常\n"
                error_msg += "- 验证系统hostname设置\n"
                error_msg += "- 检查网络接口状态\n"
                print(error_msg)
                return []
        except Exception as e:
            error_msg = f"获取本地IP地址时发生错误: {str(e)}\n"
            error_msg += "这可能是因为系统配置问题或其他网络错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 确认网络配置是否正常\n"
            error_msg += "- 验证系统hostname设置\n"
            error_msg += "- 检查网络接口状态\n"
            print(error_msg)
            return []
    
    def check_dns_resolution(self, domain: str) -> Optional[List[str]]:
        """
        检查域名解析
        
        Args:
            domain: 域名
            
        Returns:
            解析到的IP地址列表
        """
        try:
            ip_addresses = socket.gethostbyname_ex(domain)[2]
            return ip_addresses
        except socket.gaierror as e:
            error_msg = f"DNS解析错误：{str(e)}\n"
            error_msg += f"无法解析域名 {domain}\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查域名拼写是否正确\n"
            error_msg += "- 验证DNS服务器是否正常\n"
            error_msg += "- 确认网络连接是否正常\n"
            print(error_msg)
            return None
        except Exception as e:
            error_msg = f"检查DNS解析时发生错误: {str(e)}\n"
            error_msg += f"域名: {domain}\n"
            error_msg += "这可能是因为DNS配置问题、网络问题或其他系统错误导致的。\n"
            error_msg += "解决方案：\n"
            error_msg += "- 检查DNS配置是否正确\n"
            error_msg += "- 验证网络连接是否正常\n"
            error_msg += "- 确认域名是否有效\n"
            print(error_msg)
            return None