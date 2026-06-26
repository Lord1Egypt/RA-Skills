#!/usr/bin/env python3
"""
System Monitor - Monitor system metrics like CPU, memory, disk, and network
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path


def get_cpu_usage():
    """Get CPU usage percentage."""
    try:
        # Read /proc/stat
        with open('/proc/stat', 'r') as f:
            line = f.readline()
            fields = line.split()
            # user, nice, system, idle, iowait, irq, softirq
            values = [int(x) for x in fields[1:8]]
            total = sum(values)
            idle = values[3] + values[4]  # idle + iowait
            return {
                'total': total,
                'idle': idle,
                'usage': round((1 - idle / total) * 100, 1) if total > 0 else 0
            }
    except:
        return {'usage': 0}


def get_memory_usage():
    """Get memory usage."""
    try:
        with open('/proc/meminfo', 'r') as f:
            mem = {}
            for line in f:
                if ':' in line:
                    key, val = line.split(':')
                    val = val.strip().split()[0]
                    mem[key] = int(val) * 1024  # Convert to bytes
            
            total = mem.get('MemTotal', 0)
            free = mem.get('MemFree', 0) + mem.get('Buffers', 0) + mem.get('Cached', 0)
            used = total - free
            
            return {
                'total': total,
                'used': used,
                'free': free,
                'usage': round(used / total * 100, 1) if total > 0 else 0
            }
    except:
        return {'total': 0, 'used': 0, 'free': 0, 'usage': 0}


def get_disk_usage():
    """Get disk usage for mounted partitions."""
    try:
        import subprocess
        result = subprocess.run(['df', '-B1', '-T'], capture_output=True, text=True)
        lines = result.stdout.strip().split('\n')[1:]  # Skip header
        
        disks = []
        for line in lines:
            fields = line.split()
            if len(fields) >= 7:
                fs = fields[1]
                if fs in ['ext4', 'ext3', 'btrfs', 'xfs', 'vfat', 'tmpfs']:
                    total = int(fields[2])
                    used = int(fields[3])
                    avail = int(fields[4])
                    usage = int(fields[5].rstrip('%'))
                    mount = fields[6]
                    disks.append({
                        'mount': mount,
                        'total': total,
                        'used': used,
                        'free': avail,
                        'usage': usage
                    })
        return disks
    except:
        return []


def get_network_stats():
    """Get network I/O statistics."""
    try:
        interfaces = {}
        with open('/proc/net/dev', 'r') as f:
            for line in f.readlines()[2:]:  # Skip headers
                fields = line.split(':')
                if len(fields) == 2:
                    name = fields[0].strip()
                    values = fields[1].split()
                    if len(values) >= 8:
                        interfaces[name] = {
                            'rx_bytes': int(values[0]),
                            'tx_bytes': int(values[8])
                        }
        return interfaces
    except:
        return {}


def get_uptime():
    """Get system uptime."""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.read().split()[0])
            days = int(uptime // 86400)
            hours = int((uptime % 86400) // 3600)
            minutes = int((uptime % 3600) // 60)
            return {'seconds': uptime, 'days': days, 'hours': hours, 'minutes': minutes}
    except:
        return {'seconds': 0}


def get_load_average():
    """Get system load average."""
    try:
        with open('/proc/loadavg', 'r') as f:
            values = f.read().split()
            return {
                '1min': float(values[0]),
                '5min': float(values[1]),
                '15min': float(values[2])
            }
    except:
        return {'1min': 0, '5min': 0, '15min': 0}


def get_top_processes(limit=5):
    """Get top processes by CPU usage."""
    try:
        import subprocess
        result = subprocess.run(
            ['ps', 'aux', '--sort=-%cpu'],
            capture_output=True, text=True
        )
        lines = result.stdout.strip().split('\n')[1:limit+1]
        
        processes = []
        for line in lines:
            fields = line.split()
            if len(fields) >= 11:
                processes.append({
                    'pid': fields[1],
                    'user': fields[0],
                    'cpu': float(fields[2]),
                    'mem': float(fields[3]),
                    'command': ' '.join(fields[10:])
                })
        return processes
    except:
        return []


def get_status():
    """Get complete system status."""
    return {
        'cpu': get_cpu_usage(),
        'memory': get_memory_usage(),
        'disk': get_disk_usage(),
        'network': get_network_stats(),
        'uptime': get_uptime(),
        'load': get_load_average(),
        'processes': get_top_processes(5)
    }


def format_size(bytes_val):
    """Format bytes to human readable."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_val < 1024:
            return f"{bytes_val:.1f}{unit}"
        bytes_val /= 1024
    return f"{bytes_val:.1f}PB"


def print_status(status, verbose=False):
    """Print system status."""
    cpu = status['cpu']
    mem = status['memory']
    load = status['load']
    uptime = status['uptime']
    
    print("\n=== System Status ===")
    print(f"Uptime: {uptime['days']}d {upload['hours']}h {uptime['minutes']}m")
    
    print(f"\nCPU Usage: {cpu['usage']}%")
    print(f"Load: {load['1min']} {load['5min']} {load['15min']}")
    
    print(f"\nMemory: {format_size(mem['used'])} / {format_size(mem['total'])} ({mem['usage']}%)")
    
    if status['disk']:
        print("\nDisk Usage:")
        for disk in status['disk']:
            print(f"  {disk['mount']}: {disk['usage']}% ({format_size(disk['used'])} / {format_size(disk['total'])})")
    
    if verbose and status['processes']:
        print("\nTop Processes:")
        for p in status['processes']:
            print(f"  {p['cpu']:.1f}% {p['command'][:50]}")


def check_alerts(status, alert_specs):
    """Check if any alerts should trigger."""
    alerts = []
    cpu = status['cpu']['usage']
    mem = status['memory']['usage']
    
    for spec in alert_specs:
        if spec.startswith('cpu:') and cpu > float(spec[4:]):
            alerts.append(f"High CPU: {cpu}%")
        if spec.startswith('memory:') and mem > float(spec[7:]):
            alerts.append(f"High Memory: {mem}%")
        if spec.startswith('disk:'):
            for disk in status['disk']:
                if disk['usage'] > float(spec[5:]):
                    alerts.append(f"High Disk on {disk['mount']}: {disk['usage']}%")
    
    return alerts


def main():
    parser = argparse.ArgumentParser(description='System Monitor')
    parser.add_argument('--status', action='store_true', help='Show current status')
    parser.add_argument('--watch', action='store_true', help='Monitor continuously')
    parser.add_argument('--interval', type=int, default=5, help='Check interval (seconds)')
    parser.add_argument('--cpu', action='store_true', help='Show CPU usage')
    parser.add_argument('--memory', action='store_true', help='Show memory usage')
    parser.add_argument('--disk', action='store_true', help='Show disk usage')
    parser.add_argument('--network', action='store_true', help='Show network stats')
    parser.add_argument('--processes', action='store_true', help='Show top processes')
    parser.add_argument('--alert', action='append', help='Alert threshold (cpu:90, memory:80)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    # Default to --status if no options
    if not any([args.status, args.watch, args.cpu, args.memory, args.disk, args.network, args.processes]):
        args.status = True
    
    try:
        prev_net = None
        while True:
            status = get_status()
            
            if args.json:
                print(json.dumps(status, indent=2))
                if not args.watch:
                    break
            else:
                # Check alerts first
                if args.alert:
                    alerts = check_alerts(status, args.alert)
                    for alert in alerts:
                        print(f"⚠️  {alert}")
                
                print_status(status, args.processes or args.watch)
                
                if not args.watch:
                    break
            
            if args.watch:
                time.sleep(args.interval)
    
    except KeyboardInterrupt:
        print("\nStopped")
        return 0
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
