#!/usr/bin/env python3
"""
System Health Monitor - 系统健康监控
"""
import os
import sys
import time
import argparse
import psutil
from datetime import datetime

def get_cpu():
    return psutil.cpu_percent(interval=1)

def get_memory():
    mem = psutil.virtual_memory()
    return {
        "total": mem.total / (1024**3),
        "used": mem.used / (1024**3),
        "percent": mem.percent,
    }

def get_disk():
    disk = psutil.disk_usage('/')
    return {
        "total": disk.total / (1024**3),
        "used": disk.used / (1024**3),
        "percent": disk.percent,
    }

def get_network():
    net = psutil.net_io_counters()
    return {
        "sent": net.bytes_sent / (1024**2),
        "recv": net.bytes_recv / (1024**2),
    }

def cmd_status(args):
    print("🖥️ 系统状态")
    print("=" * 50)
    
    cpu = get_cpu()
    mem = get_memory()
    disk = get_disk()
    net = get_network()
    
    print(f"CPU:     {cpu}%")
    print(f"内存:    {mem['used']:.1f}GB / {mem['total']:.1f}GB ({mem['percent']}%)")
    print(f"磁盘:    {disk['used']:.1f}GB / {disk['total']:.1f}GB ({disk['percent']}%)")
    print(f"网络:    ↑{net['sent']:.1f}MB ↓{net['recv']:.1f}MB")

def cmd_report(args):
    print("📊 系统健康报告")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    cpu = get_cpu()
    mem = get_memory()
    disk = get_disk()
    net = get_network()
    
    # CPU
    status = "✅" if cpu < 70 else "⚠️" if cpu < 90 else "❌"
    print(f"CPU 使用率     {status} {cpu}%")
    
    # 内存
    status = "✅" if mem['percent'] < 70 else "⚠️" if mem['percent'] < 90 else "❌"
    print(f"内存使用率     {status} {mem['percent']}% ({mem['used']:.1f}GB)")
    
    # 磁盘
    status = "✅" if disk['percent'] < 70 else "⚠️" if disk['percent'] < 90 else "❌"
    print(f"磁盘使用率     {status} {disk['percent']}% ({disk['used']:.1f}GB)")
    
    # 网络
    print(f"网络流量       ↑{net['sent']:.1f}MB ↓{net['recv']:.1f}MB")
    
    # 进程
    processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']), 
                     key=lambda x: x.info['cpu_percent'] or 0, reverse=True)[:5]
    print(f"\n🔥 Top 5 进程:")
    for p in processes:
        try:
            print(f"   {p.name():20s} CPU: {p.cpu_percent():.1f}%")
        except:
            pass

def cmd_watch(args):
    interval = args.interval or 60
    print(f"🔄 持续监控 (间隔 {interval} 秒, Ctrl+C 退出)")
    print("=" * 50)
    
    while True:
        cpu = get_cpu()
        mem = get_memory()
        disk = get_disk()
        
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[{timestamp}] CPU:{cpu}% 内存:{mem['percent']}% 磁盘:{disk['percent']}%")
        
        # 告警
        if cpu > 90:
            print("   ⚠️ CPU 过高!")
        if mem['percent'] > 90:
            print("   ⚠️ 内存过高!")
        
        time.sleep(interval)

def main():
    parser = argparse.ArgumentParser(description="System Health Monitor")
    subparsers = parser.add_subparsers()
    
    subparsers.add_parser("status", help="查看状态").set_defaults(func=cmd_status)
    subparsers.add_parser("report", help="生成报告").set_defaults(func=cmd_report)
    
    p_watch = subparsers.add_parser("watch", help="持续监控")
    p_watch.add_argument("--interval", type=int, help="监控间隔(秒)")
    p_watch.set_defaults(func=cmd_watch)
    
    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
