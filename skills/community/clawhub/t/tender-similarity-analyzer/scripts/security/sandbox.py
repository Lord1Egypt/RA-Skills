# -*- coding: utf-8 -*-
"""
进程沙箱模块
提供额外的进程级安全隔离
"""

import os
import sys
import platform
from typing import List, Optional


class SandboxEnforcer:
    """
    进程沙箱强制执行器
    
    跨平台支持：Mac / Windows / Linux
    """
    
    def __init__(self):
        self.system = platform.system()
        self.original_environ = os.environ.copy()
        self.restricted_paths = []
        
    def enforce(self):
        """
        强制执行沙箱限制
        """
        if self.system == "Darwin":
            self._enforce_macos()
        elif self.system == "Windows":
            self._enforce_windows()
        elif self.system == "Linux":
            self._enforce_linux()
            
    def _enforce_macos(self):
        """macOS 沙箱限制"""
        # 限制环境变量
        if 'DYLD_INSERT_LIBRARIES' in os.environ:
            del os.environ['DYLD_INSERT_LIBRARIES']
            
        # 禁止某些环境变量传播
        restricted_vars = ['DYLD_LIBRARY_PATH', 'DYLD_INSERT_LIBRARIES']
        for var in restricted_vars:
            os.environ.pop(var, None)
            
    def _enforce_windows(self):
        """Windows 沙箱限制"""
        # Windows 下的安全限制
        import ctypes
        
        try:
            # 尝试禁用某些环境变量
            os.environ.pop('LD_LIBRARY_PATH', None)
        except Exception:
            pass
            
    def _enforce_linux(self):
        """Linux 沙箱限制"""
        # Linux 下的安全限制
        try:
            # 移除可能危险的 LD_ 前缀环境变量
            for key in list(os.environ.keys()):
                if key.startswith('LD_'):
                    os.environ.pop(key, None)
        except Exception:
            pass
            
    def restrict_file_access(self, allowed_dirs: List[str]):
        """
        限制文件访问到指定目录
        
        @param allowed_dirs: 允许访问的目录列表
        """
        self.restricted_paths = [os.path.abspath(d) for d in allowed_dirs]
        
    def verify_path_access(self, path: str) -> bool:
        """
        验证路径是否在允许范围内
        
        @param path: 要检查的路径
        @return: 是否允许访问
        """
        if not self.restricted_paths:
            return True
            
        abs_path = os.path.abspath(path)
        for allowed in self.restricted_paths:
            if abs_path.startswith(allowed):
                return True
                
        return False
        
    def get_allowed_dirs(self) -> List[str]:
        """获取允许访问的目录列表"""
        return self.restricted_paths.copy()
