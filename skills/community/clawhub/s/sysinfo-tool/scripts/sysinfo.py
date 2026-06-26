#!/usr/bin/env python3
"""System Info Tool - Get comprehensive system information."""

import argparse
import json
import os
import platform
import sys
import subprocess
from datetime import datetime
from typing import Dict, Any, List


def get_cpu_info() -> Dict[str, Any]:
    """Get CPU information."""
    info = {}
    
    # CPU count
    info['physical_cores'] = os.cpu_count()
    info['logical_cores'] = os.cpu_count() or 0
    
    # Try to get CPU frequency
    try:
        with open('/proc/cpuinfo', 'r') as f:
            for line in f:
                if 'model name' in line:
                    info['model'] = line.split(':')[1].strip()
                    break
                if 'cpu MHz' in line:
                    info['frequency_mhz'] = float(line.split(':')[1].strip())
                    break
    except:
        pass
    
    # Load average (Linux)
    try:
        load1, load5, load15 = os.getloadavg()
        info['load_average'] = {
            '1min': load1,
            '5min': load5,
            '15min': load15
        }
    except:
        pass
    
    # CPU usage (simple)
    try:
        # This is a rough estimate
        info['usage_percent'] = 0.0  # Would need psutil for accurate
    except:
        pass
    
    return info


def get_memory_info() -> Dict[str, Any]:
    """Get memory information."""
    info = {}
    
    try:
        with open('/proc/meminfo', 'r') as f:
            lines = f.readlines()
        
        mem = {}
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip().split()[0]
                try:
                    mem[key] = int(value) * 1024  # Convert to bytes
                except:
                    pass
        
        total = mem.get('MemTotal', 0)
        free = mem.get('MemFree', 0)
        available = mem.get('MemAvailable', free)
        used = total - available
        
        info['total'] = total
        info['used'] = used
        info['free'] = free
        info['available'] = available
        info['percent_used'] = (used / total * 100) if total > 0 else 0
        
        # Swap
        info['swap_total'] = mem.get('SwapTotal', 0)
        info['swap_used'] = mem.get('SwapUsed', 0)
        
    except:
        pass
    
    return info


def get_disk_info() -> List[Dict[str, Any]]:
    """Get disk information."""
    disks = []
    
    try:
        # Use df command
        result = subprocess.run(
            ['df', '-B1', '-T'], capture_output=True, text=True, check=True
        )
        lines = result.stdout.splitlines()[1:]  # Skip header
        
        for line in lines:
            parts = line.split()
            if len(parts) >= 7:
                filesystem = parts[1]
                if filesystem in ['tmpfs', 'devtmpfs', 'squashfs', 'overlay']:
                    continue
                
                try:
                    disks.append({
                        'mount_point': parts[6],
                        'filesystem': filesystem,
                        'total': int(parts[2]),
                        'used': int(parts[3]),
                        'available': int(parts[4]),
                        'percent_used': int(parts[5].rstrip('%'))
                    })
                except:
                    pass
    except:
        pass
    
    return disks


def get_network_info() -> Dict[str, Any]:
    """Get network information."""
    info = {}
    
    # Hostname
    info['hostname'] = platform.node()
    
    # Network interfaces
    try:
        with open('/proc/net/dev', 'r') as f:
            lines = f.readlines()[2:]  # Skip headers
            
        interfaces = {}
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                name = parts[0].strip()
                stats = parts[1].strip().split()
                if len(stats) >= 8:
                    interfaces[name] = {
                        'rx_bytes': int(stats[0]),
                        'rx_packets': int(stats[1]),
                        'tx_bytes': int(stats[8]),
                        'tx_packets': int(stats[9])
                    }
        
        info['interfaces'] = interfaces
    except:
        pass
    
    return info


def get_process_info() -> List[Dict[str, Any]]:
    """Get top processes."""
    processes = []
    
    try:
        result = subprocess.run(
            ['ps', 'aux', '--sort=-pcpu'], capture_output=True, text=True
        )
        lines = result.stdout.splitlines()[1:11]  # Top 10
        
        for line in lines:
            parts = line.split(None, 10)
            if len(parts) >= 11:
                processes.append({
                    'user': parts[0],
                    'pid': parts[1],
                    'cpu': float(parts[2]),
                    'mem': float(parts[3]),
                    'command': parts[10]
                })
    except:
        pass
    
    return processes


def get_uptime() -> Dict[str, Any]:
    """Get system uptime."""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
        
        days = int(uptime_seconds // 86400)
        hours = int((uptime_seconds % 86400) // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        
        return {
            'seconds': uptime_seconds,
            'formatted': f"{days}d {hours}h {minutes}m"
        }
    except:
        return {}


def format_bytes(bytes_val: int) -> str:
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f} PB"


def print_system_info(json_output: bool = False, brief: bool = False) -> None:
    """Print all system information."""
    info = {
        'hostname': platform.node(),
        'os': platform.system(),
        'os_version': platform.version(),
        'architecture': platform.machine(),
        'python_version': platform.python_version(),
        'uptime': get_uptime(),
        'cpu': get_cpu_info(),
        'memory': get_memory_info(),
        'disk': get_disk_info(),
        'network': get_network_info(),
        'top_processes': get_process_info() if not brief else []
    }
    
    if json_output:
        print(json.dumps(info, indent=2))
        return
    
    # Pretty print
    print("=" * 60)
    print(f"System Information - {info['hostname']}")
    print("=" * 60)
    
    print(f"\n📦 OS: {info['os']} {info['os_version']}")
    print(f"🏗️  Architecture: {info['architecture']}")
    print(f"🐍 Python: {info['python_version']}")
    
    if info['uptime']:
        print(f"⏱️  Uptime: {info['uptime'].get('formatted', 'N/A')}")
    
    if info['cpu']:
        print("\n" + "=" * 60)
        print("🖥️  CPU Information")
        print("=" * 60)
        cpu = info['cpu']
        if 'model' in cpu:
            print(f"Model: {cpu['model']}")
        print(f"Cores: {cpu.get('physical_cores', 'N/A')} physical, {cpu.get('logical_cores', 'N/A')} logical")
        if 'load_average' in cpu:
            load = cpu['load_average']
            print(f"Load: {load['1min']:.2f} (1m), {load['5min']:.2f} (5m), {load['15min']:.2f} (15m)")
    
    if info['memory']:
        print("\n" + "=" * 60)
        print("💾 Memory Information")
        print("=" * 60)
        mem = info['memory']
        print(f"Total:     {format_bytes(mem.get('total', 0))}")
        print(f"Used:      {format_bytes(mem.get('used', 0))} ({mem.get('percent_used', 0):.1f}%)")
        print(f"Available: {format_bytes(mem.get('available', 0))}")
        if mem.get('swap_total', 0) > 0:
            print(f"Swap:      {format_bytes(mem.get('swap_used', 0))} / {format_bytes(mem.get('swap_total', 0))}")
    
    if info['disk']:
        print("\n" + "=" * 60)
        print("💿 Disk Usage")
        print("=" * 60)
        for disk in info['disk']:
            print(f"{disk['mount_point']:20} {format_bytes(disk['used']):>12} / {format_bytes(disk['total']):>12} ({disk['percent_used']:>3}%)")
    
    if info['network'] and 'interfaces' in info['network']:
        print("\n" + "=" * 60)
        print("🌐 Network Interfaces")
        print("=" * 60)
        for iface, stats in info['network']['interfaces'].items():
            rx = format_bytes(stats['rx_bytes'])
            tx = format_bytes(stats['tx_bytes'])
            print(f"{iface:15} RX: {rx:>10}  TX: {tx:>10}")
    
    if info['top_processes'] and not brief:
        print("\n" + "=" * 60)
        print("🔥 Top Processes (by CPU)")
        print("=" * 60)
        print(f"{'PID':<8} {'USER':<12} {'CPU%':<6} {'MEM%':<6} COMMAND")
        print("-" * 60)
        for proc in info['top_processes']:
            cmd = proc['command'][:40] if len(proc['command']) > 40 else proc['command']
            print(f"{proc['pid']:<8} {proc['user']:<12} {proc['cpu']:<6.1f} {proc['mem']:<6.1f} {cmd}")
    
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(description='System information tool')
    
    parser.add_argument('--cpu', action='store_true', help='Show CPU info')
    parser.add_argument('--memory', action='store_true', help='Show memory info')
    parser.add_argument('--disk', action='store_true', help='Show disk info')
    parser.add_argument('--network', action='store_true', help='Show network info')
    parser.add_argument('--processes', action='store_true', help='Show top processes')
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--all', action='store_true', help='Show all info')
    parser.add_argument('--brief', action='store_true', help='Brief summary')
    
    args = parser.parse_args()
    
    # If no specific option, show all
    show_all = args.all or not any([args.cpu, args.memory, args.disk, args.network, args.processes])
    
    if args.json:
        print_system_info(json_output=True, brief=args.brief)
    elif show_all:
        print_system_info(brief=args.brief)
    else:
        # Show specific sections
        if args.cpu:
            cpu = get_cpu_info()
            print("CPU:", cpu)
        if args.memory:
            mem = get_memory_info()
            print("Memory:", mem)
        if args.disk:
            disk = get_disk_info()
            print("Disk:", disk)
        if args.network:
            net = get_network_info()
            print("Network:", net)
        if args.processes:
            procs = get_process_info()
            print("Processes:", procs)


if __name__ == '__main__':
    main()
