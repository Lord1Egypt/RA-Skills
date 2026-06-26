#!/usr/bin/env python3
import platform
import os
import json
import argparse

def get_size(bytes):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024.0

def get_system_info():
    info = {}
    
    # 操作系统
    info['os'] = f"{platform.system()} {platform.release()}"
    info['os_version'] = platform.version()
    
    # CPU
    info['cpu'] = platform.processor() or platform.machine()
    info['cpu_cores'] = os.cpu_count()
    
    # 内存(简化版,跨平台)
    try:
        if platform.system() == 'Windows':
            import ctypes
            kernel32 = ctypes.windll.kernel32
            c_ulong = ctypes.c_ulong
            class MEMORYSTATUS(ctypes.Structure):
                _fields_ = [
                    ('dwLength', c_ulong),
                    ('dwMemoryLoad', c_ulong),
                    ('dwTotalPhys', c_ulong),
                    ('dwAvailPhys', c_ulong),
                    ('dwTotalPageFile', c_ulong),
                    ('dwAvailPageFile', c_ulong),
                    ('dwTotalVirtual', c_ulong),
                    ('dwAvailVirtual', c_ulong)
                ]
            memoryStatus = MEMORYSTATUS()
            memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUS)
            kernel32.GlobalMemoryStatus(ctypes.byref(memoryStatus))
            info['memory_total'] = memoryStatus.dwTotalPhys
            info['memory_used'] = memoryStatus.dwTotalPhys - memoryStatus.dwAvailPhys
        else:
            # Linux/Mac
            with open('/proc/meminfo', 'r') as f:
                lines = f.readlines()
                total = int(lines[0].split()[1]) * 1024
                available = int(lines[2].split()[1]) * 1024
                info['memory_total'] = total
                info['memory_used'] = total - available
    except:
        info['memory_total'] = 0
        info['memory_used'] = 0
    
    # 磁盘
    try:
        import shutil
        total, used, free = shutil.disk_usage('/')
        info['disk_total'] = total
        info['disk_used'] = used
    except:
        info['disk_total'] = 0
        info['disk_used'] = 0
    
    return info

def print_table(info, filter_key=None):
    print("\n=== 系统信息 ===\n")
    
    if not filter_key or filter_key == 'os':
        print(f"操作系统: {info['os']}")
    
    if not filter_key or filter_key == 'cpu':
        print(f"CPU: {info['cpu']}")
        print(f"CPU 核心数: {info['cpu_cores']}")
    
    if not filter_key or filter_key == 'memory':
        if info['memory_total'] > 0:
            usage_pct = (info['memory_used'] / info['memory_total']) * 100
            print(f"内存总量: {get_size(info['memory_total'])}")
            print(f"内存使用: {get_size(info['memory_used'])} ({usage_pct:.0f}%)")
    
    if not filter_key or filter_key == 'disk':
        if info['disk_total'] > 0:
            usage_pct = (info['disk_used'] / info['disk_total']) * 100
            print(f"磁盘总量: {get_size(info['disk_total'])}")
            print(f"磁盘使用: {get_size(info['disk_used'])} ({usage_pct:.0f}%)")
    
    print()

def main():
    parser = argparse.ArgumentParser(description='查询系统信息')
    parser.add_argument('--cpu', action='store_true', help='仅显示 CPU 信息')
    parser.add_argument('--memory', action='store_true', help='仅显示内存信息')
    parser.add_argument('--disk', action='store_true', help='仅显示磁盘信息')
    parser.add_argument('--os', action='store_true', help='仅显示操作系统信息')
    parser.add_argument('--format', choices=['table', 'json'], default='table', help='输出格式')
    
    args = parser.parse_args()
    
    info = get_system_info()
    
    # 确定过滤条件
    filter_key = None
    if args.cpu:
        filter_key = 'cpu'
    elif args.memory:
        filter_key = 'memory'
    elif args.disk:
        filter_key = 'disk'
    elif args.os:
        filter_key = 'os'
    
    if args.format == 'json':
        print(json.dumps(info, indent=2, ensure_ascii=False))
    else:
        print_table(info, filter_key)

if __name__ == '__main__':
    main()
