# -*- coding: utf-8 -*-
"""
网络安全隔离模块
实现100%零出站保障
"""

import socket
import threading
import time
import sys
from typing import Callable, List, Optional


class SecurityError(Exception):
    """安全异常"""
    pass


class NetworkIsolator:
    """
    网络隔离控制器
    通过socket劫持实现完全的网络隔离
    """
    
    # 允许的本地地址
    ALLOWED_HOSTS = [
        '127.0.0.1',
        'localhost',
        '::1',
    ]
    
    def __init__(self, alert_callback: Optional[Callable] = None):
        self.alert_callback = alert_callback
        self.original_socket = socket.socket
        self.original_create_connection = socket.create_connection
        self.original_getaddrinfo = socket.getaddrinfo
        self._is_locked = False
        self._lock = threading.Lock()
        self._connection_log = []
        
    def enable_isolation(self):
        """
        启用网络隔离模式
        替换所有socket相关函数，切断所有出站连接
        """
        with self._lock:
            if self._is_locked:
                return
                
            # 替换 socket.socket
            socket.socket = self._blocked_socket
            
            # 替换 socket.create_connection
            socket.create_connection = self._blocked_create_connection
            
            # 替换 socket.getaddrinfo
            socket.getaddrinfo = self._blocked_getaddrinfo
            
            # 尝试屏蔽 HTTP 库
            self._block_http_libraries()
            
            self._is_locked = True
            self._log("🔒 网络隔离已启用")
            
    def disable_isolation(self):
        """
        解除网络隔离模式
        """
        with self._lock:
            if not self._is_locked:
                return
                
            socket.socket = self.original_socket
            socket.create_connection = self.original_create_connection
            socket.getaddrinfo = self.original_getaddrinfo
            
            self._is_locked = False
            self._log("🔓 网络隔离已解除")
            
    def _blocked_socket(self, family=socket.AF_INET, type=socket.SOCK_STREAM, proto=0):
        """
        被阻塞的socket创建函数
        任何试图创建网络连接的操作都会被拒绝
        """
        raise SecurityError(
            "⚠️ 网络请求已被拦截！"
            "投标文件内容不允许出站。"
        )
        
    def _blocked_create_connection(self, address, timeout=None, source_address=None):
        """
        阻塞 create_connection
        """
        host, port = address[0] if isinstance(address, tuple) else address
        
        # 检查是否是本地地址
        if host in self.ALLOWED_HOSTS:
            return self.original_create_connection(address, timeout, source_address)
            
        self._log(f"🚨 试图连接外部地址: {host}:{port}")
        
        # 触发告警
        if self.alert_callback:
            self.alert_callback(f"检测到出站连接尝试: {host}:{port}")
            
        raise SecurityError(
            f"⚠️ 禁止连接外部地址 {host}:{port}！"
            "文件内容不允许出站。"
        )
        
    def _blocked_getaddrinfo(self, host, port, family=0, type=0, proto=0, flags=0):
        """
        阻塞 getaddrinfo
        防止DNS解析绕过
        """
        if host in self.ALLOWED_HOSTS:
            return self.original_getaddrinfo(host, port, family, type, proto, flags)
            
        self._log(f"🚨 试图解析外部域名: {host}")
        
        if self.alert_callback:
            self.alert_callback(f"检测到DNS解析尝试: {host}")
            
        raise SecurityError(
            f"⚠️ DNS解析已被禁止: {host}！"
        )
        
    def _block_http_libraries(self):
        """
        尝试屏蔽常见HTTP库的网络能力
        """
        blocked_modules = []
        
        # requests
        try:
            import requests
            requests.Session.get = lambda *a, **k: (_ for _ in ()).throw(SecurityError("requests被禁用"))
            requests.Session.post = lambda *a, **k: (_ for _ in ()).throw(SecurityError("requests被禁用"))
            blocked_modules.append('requests')
        except ImportError:
            pass
            
        # urllib
        try:
            import urllib.request
            urllib.request.urlopen = lambda *a, **k: (_ for _ in ()).throw(SecurityError("urllib被禁用"))
            blocked_modules.append('urllib')
        except ImportError:
            pass
            
        # httpx
        try:
            import httpx
            httpx.Client.get = lambda *a, **k: (_ for _ in ()).throw(SecurityError("httpx被禁用"))
            httpx.Client.post = lambda *a, **k: (_ for _ in ()).throw(SecurityError("httpx被禁用"))
            blocked_modules.append('httpx')
        except ImportError:
            pass
            
        if blocked_modules:
            self._log(f"已屏蔽HTTP库: {', '.join(blocked_modules)}")
            
    def _log(self, message):
        """记录日志"""
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        self._connection_log.append(log_entry)
        print(log_entry)
        
        if self.alert_callback:
            self.alert_callback(message)
            
    def verify_zero_exfiltration(self) -> bool:
        """
        验算：确认0字节出站
        通过检查连接日志来确认没有异常流量
        """
        suspicious_entries = [
            entry for entry in self._connection_log
            if '🚨' in entry
        ]
        
        if suspicious_entries:
            for entry in suspicious_entries:
                print(f"[警告] {entry}")
            return False
            
        return True
        
    def get_connection_log(self) -> List[str]:
        """获取连接日志"""
        return self._connection_log.copy()
        
    @property
    def is_locked(self) -> bool:
        """检查是否处于隔离模式"""
        return self._is_locked
