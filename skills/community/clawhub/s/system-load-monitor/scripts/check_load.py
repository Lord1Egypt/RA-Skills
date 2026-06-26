#!/usr/bin/env python3
"""
System Load Monitor - Check current system load and memory usage
Returns JSON with load status and recommendations
"""

import json
import os
import subprocess
import sys

def get_cpu_load():
    """Get CPU load average (1 minute)"""
    try:
        load_avg = os.getloadavg()[0]
        cpu_count = os.cpu_count() or 1
        load_percent = (load_avg / cpu_count) * 100
        return {
            "load_avg_1m": round(load_avg, 2),
            "cpu_count": cpu_count,
            "load_percent": round(load_percent, 1)
        }
    except Exception as e:
        return {"error": str(e)}

def get_memory_usage():
    """Get memory usage percentage"""
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = {}
            for line in f:
                parts = line.split(':')
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = int(parts[1].strip().split()[0])
                    meminfo[key] = value
        
        total = meminfo.get('MemTotal', 0)
        available = meminfo.get('MemAvailable', 0)
        used = total - available
        used_percent = (used / total) * 100 if total > 0 else 0
        
        return {
            "total_mb": round(total / 1024, 0),
            "used_mb": round(used / 1024, 0),
            "available_mb": round(available / 1024, 0),
            "used_percent": round(used_percent, 1)
        }
    except Exception as e:
        return {"error": str(e)}

def get_top_processes(limit=5):
    """Get top processes by CPU usage"""
    try:
        result = subprocess.run(
            ['ps', 'aux', '--sort=-%cpu'],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.strip().split('\n')[1:limit+1]
        processes = []
        for line in lines:
            parts = line.split()
            if len(parts) >= 11:
                processes.append({
                    "user": parts[0],
                    "cpu_percent": float(parts[2]),
                    "mem_percent": float(parts[3]),
                    "command": ' '.join(parts[10:])
                })
        return processes
    except Exception as e:
        return [{"error": str(e)}]

def check_status(cpu_threshold=90, memory_threshold=90):
    """Check system status against thresholds"""
    cpu = get_cpu_load()
    memory = get_memory_usage()
    top_procs = get_top_processes()
    
    cpu_critical = cpu.get('load_percent', 0) >= cpu_threshold
    memory_critical = memory.get('used_percent', 0) >= memory_threshold
    is_critical = cpu_critical or memory_critical
    
    status = "critical" if is_critical else ("warning" if cpu.get('load_percent', 0) >= 70 or memory.get('used_percent', 0) >= 70 else "ok")
    
    return {
        "status": status,
        "cpu": cpu,
        "memory": memory,
        "top_processes": top_procs,
        "thresholds": {
            "cpu": cpu_threshold,
            "memory": memory_threshold
        },
        "recommendation": "PAUSE" if is_critical else "CONTINUE"
    }

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Check system load')
    parser.add_argument('--cpu-threshold', type=int, default=90, help='CPU load threshold (default: 90)')
    parser.add_argument('--memory-threshold', type=int, default=90, help='Memory threshold (default: 90)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = check_status(args.cpu_threshold, args.memory_threshold)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"System Status: {result['status'].upper()}")
        print(f"CPU Load: {result['cpu'].get('load_percent', 'N/A')}% (threshold: {args.cpu_threshold}%)")
        print(f"Memory: {result['memory'].get('used_percent', 'N/A')}% (threshold: {args.memory_threshold}%)")
        print(f"Recommendation: {result['recommendation']}")
        
        if result['status'] == 'critical':
            sys.exit(2)
        elif result['status'] == 'warning':
            sys.exit(1)
        else:
            sys.exit(0)
