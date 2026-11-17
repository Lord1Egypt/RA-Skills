#!/usr/bin/env python3
"""
企业微信语音消息 Agent - 硬件资源检测脚本
自动检测用户计算机硬件资源，输出硬件等级配置
"""

import json
import sys
import os

def detect_windows():
    """Windows 系统硬件检测"""
    try:
        import ctypes
        
        # 使用 Windows API 获取内存信息
        kernel32 = ctypes.windll.kernel32
        
        class MEMORYSTATUSEX(ctypes.Structure):
            _fields_ = [
                ("dwLength", ctypes.c_ulong),
                ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
            ]
        
        stat = MEMORYSTATUSEX()
        stat.dwLength = ctypes.sizeof(stat)
        kernel32.GlobalMemoryStatusEx(ctypes.byref(stat))
        
        ram_gb = round(stat.ullTotalPhys / (1024**3), 1)
        
        # 获取 CPU 核心数
        cpu_cores = os.cpu_count() or 2
        
        return ram_gb, cpu_cores
        
    except Exception as e:
        # 降级方案：使用 WMI
        try:
            import subprocess
            result = subprocess.run(
                ['wmic', 'computersystem', 'get', 'TotalPhysicalNumberOfProcessors,TotalPhysicalMemory'],
                capture_output=True, text=True, timeout=10
            )
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                parts = lines[1].split()
                if len(parts) >= 2:
                    cpu_cores = int(parts[0])
                    ram_bytes = int(parts[1])
                    ram_gb = round(ram_bytes / (1024**3), 1)
                    return ram_gb, cpu_cores
        except:
            pass
        
        # 最终降级：返回保守估计
        return 4.0, 2


def detect_linux():
    """Linux 系统硬件检测"""
    try:
        # 读取内存信息
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if line.startswith('MemTotal:'):
                    parts = line.split()
                    ram_kb = int(parts[1])
                    ram_gb = round(ram_kb / (1024**2), 1)
                    break
            else:
                ram_gb = 4.0
        
        # 获取 CPU 核心数
        cpu_cores = os.cpu_count() or 2
        
        return ram_gb, cpu_cores
        
    except Exception:
        return 4.0, 2


def detect_macos():
    """macOS 系统硬件检测"""
    try:
        import subprocess
        
        # 获取内存
        result = subprocess.run(
            ['sysctl', '-n', 'hw.memsize'],
            capture_output=True, text=True, timeout=10
        )
        ram_bytes = int(result.stdout.strip())
        ram_gb = round(ram_bytes / (1024**3), 1)
        
        # 获取 CPU 核心数
        result = subprocess.run(
            ['sysctl', '-n', 'hw.ncpu'],
            capture_output=True, text=True, timeout=10
        )
        cpu_cores = int(result.stdout.strip())
        
        return ram_gb, cpu_cores
        
    except Exception:
        return 8.0, 4  # macOS 通常配置较高


def classify_hardware(ram_gb, cpu_cores):
    """根据硬件参数分级"""
    if ram_gb >= 16 and cpu_cores >= 8:
        return {
            "level": "high",
            "ram_gb": ram_gb,
            "cpu_cores": cpu_cores,
            "concurrency": 5,
            "cache_limit": 100,
            "description": "高配 - 支持5路并发，100轮历史缓存"
        }
    elif ram_gb >= 8 and cpu_cores >= 4:
        return {
            "level": "medium",
            "ram_gb": ram_gb,
            "cpu_cores": cpu_cores,
            "concurrency": 3,
            "cache_limit": 20,
            "description": "中配 - 支持3路并发，20轮历史缓存"
        }
    else:
        return {
            "level": "low",
            "ram_gb": ram_gb,
            "cpu_cores": cpu_cores,
            "concurrency": 1,
            "cache_limit": 5,
            "description": "低配 - 单路并发，5轮历史缓存"
        }


def main():
    """主函数"""
    system = sys.platform
    
    if system == 'win32':
        ram_gb, cpu_cores = detect_windows()
    elif system == 'linux':
        ram_gb, cpu_cores = detect_linux()
    elif system == 'darwin':
        ram_gb, cpu_cores = detect_macos()
    else:
        ram_gb, cpu_cores = 4.0, 2
    
    result = classify_hardware(ram_gb, cpu_cores)
    result["platform"] = system
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    main()
