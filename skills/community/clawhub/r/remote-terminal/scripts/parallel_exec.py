#!/usr/bin/env python3
"""
Parallel Executor - Execute commands on multiple hosts in parallel

Usage:
    parallel_exec.py <command> --hosts <host1,host2,...> [--user USER] [--key KEY]
    parallel_exec.py <command> --file <hosts_file> [--user USER] [--key KEY]

Examples:
    parallel_exec.py "uptime" --hosts web1,web2,web3
    parallel_exec.py "docker ps" --file hosts.txt
    parallel_exec.py "systemctl status nginx" --hosts production,staging --user admin
"""

import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def parse_hosts(hosts_str):
    """Parse comma-separated hosts string"""
    return [h.strip() for h in hosts_str.split(",") if h.strip()]


def load_hosts_file(filepath):
    """Load hosts from file (one per line)"""
    with open(filepath, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip() and not line.startswith("#")]


def exec_on_host(host, command, user=None, key=None, timeout=30):
    """Execute command on a single host"""
    ssh_cmd = ["ssh", "-o", "StrictHostKeyChecking=accept-new", "-o", "ConnectTimeout=10"]
    
    if key:
        ssh_cmd.extend(["-i", key])
    
    if user:
        ssh_cmd.append(f"{user}@{host}")
    else:
        ssh_cmd.append(host)
    
    ssh_cmd.append(command)
    
    try:
        result = subprocess.run(
            ssh_cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return host, result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return host, "", "Timeout", -1
    except Exception as e:
        return host, "", str(e), -1


def parallel_exec(hosts, command, user=None, key=None, max_workers=5):
    """Execute command on multiple hosts in parallel"""
    results = []
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(exec_on_host, host, command, user, key): host
            for host in hosts
        }
        
        for future in as_completed(futures):
            host, stdout, stderr, exit_code = future.result()
            results.append((host, stdout, stderr, exit_code))
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Execute commands on multiple hosts in parallel")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--hosts", "-H", help="Comma-separated list of hosts")
    parser.add_argument("--file", "-f", help="File containing hosts (one per line)")
    parser.add_argument("--user", "-u", help="SSH username")
    parser.add_argument("--key", "-i", help="Path to SSH private key")
    parser.add_argument("--workers", "-w", type=int, default=5, help="Max parallel workers")
    
    args = parser.parse_args()
    
    # Get hosts list
    if args.hosts:
        hosts = parse_hosts(args.hosts)
    elif args.file:
        hosts = load_hosts_file(args.file)
    else:
        print("Error: Must specify --hosts or --file")
        sys.exit(1)
    
    if not hosts:
        print("Error: No hosts specified")
        sys.exit(1)
    
    print(f"Executing on {len(hosts)} hosts: {', '.join(hosts)}")
    print(f"Command: {args.command}")
    print("=" * 60)
    
    # Execute
    results = parallel_exec(hosts, args.command, args.user, args.key, args.workers)
    
    # Display results
    for host, stdout, stderr, exit_code in sorted(results, key=lambda x: x[0]):
        print(f"\n[{host}] (exit: {exit_code})")
        print("-" * 40)
        if stdout:
            print(stdout)
        if stderr:
            print(f"[stderr] {stderr}")


if __name__ == "__main__":
    main()
