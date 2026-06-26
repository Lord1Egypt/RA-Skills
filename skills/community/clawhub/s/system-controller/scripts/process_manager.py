#!/usr/bin/env python3
"""
Process Manager - List, start, stop, and monitor system processes.

Requirements: Windows 10/11, PowerShell 5.1+
Dependencies: None (uses built-in PowerShell)
"""

import subprocess
import sys
import os

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps


def list_processes(name=None):
    """List running processes. Optionally filter by name."""
    if name:
        escaped = name.replace("'", "''")
        script = f"""
Get-Process -Name '*{escaped}*' -ErrorAction SilentlyContinue |
    Select-Object Id, ProcessName, CPU, WorkingSet64, MainWindowTitle |
    ForEach-Object {{
        [PSCustomObject]@{{
            PID = $_.Id
            Name = $_.ProcessName
            CPU_sec = [math]::Round($_.CPU, 2)
            Memory_MB = [math]::Round($_.WorkingSet64 / 1MB, 2)
            Window = if ($_.MainWindowTitle) {{ $_.MainWindowTitle }} else {{ '' }}
        }}
    }} | ConvertTo-Json -Compress
"""
    else:
        script = r"""
Get-Process | Select-Object Id, ProcessName, CPU, WorkingSet64, MainWindowTitle |
    ForEach-Object {
        [PSCustomObject]@{
            PID = $_.Id
            Name = $_.ProcessName
            CPU_sec = [math]::Round($_.CPU, 2)
            Memory_MB = [math]::Round($_.WorkingSet64 / 1MB, 2)
            Window = if ($_.MainWindowTitle) { $_.MainWindowTitle } else { '' }
        }
    } | ConvertTo-Json -Compress
"""
    stdout, stderr, code = _run_ps(script)
    if not stdout:
        # Fallback for empty result
        return "[]"
    return stdout


def kill_process(pid=None, name=None, force=False):
    """Kill a process by PID or name."""
    flag = "-Force" if force else ""
    if pid:
        script = f"""
Stop-Process -Id {pid} {flag} -ErrorAction SilentlyContinue
if ($?) {{
    Write-Output "OK: Killed process PID {pid}"
}} else {{
    Write-Output "ERROR: Process PID {pid} not found or access denied"
}}
"""
    elif name:
        escaped = name.replace("'", "''")
        script = f"""
$procs = Get-Process -Name '*{escaped}*' -ErrorAction SilentlyContinue
if ($procs) {{
    $procs | Stop-Process {flag} -ErrorAction SilentlyContinue
    Write-Output "OK: Killed $($procs.Count) process(es) matching '{name}'"
}} else {{
    Write-Output "ERROR: No process found matching '{name}'"
}}
"""
    else:
        return "ERROR: Provide --pid or --name"

    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def start_process(command, working_dir=None, wait=False):
    """Start a new process."""
    escaped = command.replace('"', '\\"')
    dir_part = f"-WorkingDirectory '{working_dir}'" if working_dir else ""
    wait_part = "-Wait" if wait else ""
    script = f"""
try {{
    Start-Process -FilePath "{escaped}" {dir_part} {wait_part} -ErrorAction Stop
    Write-Output "OK: Started '{command}'"
}} catch {{
    Write-Output "ERROR: $($_.Exception.Message)"
}}
"""
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def get_process_info(pid):
    """Get detailed information about a specific process."""
    script = f"""
$proc = Get-Process -Id {pid} -ErrorAction SilentlyContinue
if ($proc) {{
    [PSCustomObject]@{{
        PID = $proc.Id
        Name = $proc.ProcessName
        Path = $proc.Path
        StartTime = $proc.StartTime
        CPU_sec = [math]::Round($proc.CPU, 2)
        Memory_MB = [math]::Round($proc.WorkingSet64 / 1MB, 2)
        Threads = $proc.Threads.Count
        Handles = $proc.HandleCount
        MainWindowTitle = $proc.MainWindowTitle
        Responding = $proc.Responding
    }} | ConvertTo-Json
}} else {{
    Write-Output "ERROR: Process PID {pid} not found"
}}
"""
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def get_system_info():
    """Get overall system resource usage."""
    script = r"""
$os = Get-CimInstance Win32_OperatingSystem
$totalGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
$freeGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
$usedGB = [math]::Round($totalGB - $freeGB, 2)
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
$uptime = (Get-Date) - $os.LastBootUpTime
[PSCustomObject]@{
    ComputerName = $env:COMPUTERNAME
    OS = $os.Caption
    CPU_Load_Pct = $cpu.LoadPercentage
    RAM_Total_GB = $totalGB
    RAM_Used_GB = $usedGB
    RAM_Free_GB = $freeGB
    RAM_Usage_Pct = [math]::Round($usedGB / $totalGB * 100, 1)
    Uptime_Days = [math]::Floor($uptime.TotalDays)
    Uptime_Hours = $uptime.Hours
    Process_Count = (Get-Process).Count
} | ConvertTo-Json
"""
    stdout, stderr, code = _run_ps(script)
    return stdout if stdout else stderr


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Process Manager")
    sub = parser.add_subparsers(dest="action")

    p_list = sub.add_parser("list", help="List processes")
    p_list.add_argument("--name", type=str, help="Filter by name")

    p_kill = sub.add_parser("kill", help="Kill a process")
    p_kill.add_argument("--pid", type=int)
    p_kill.add_argument("--name", type=str)
    p_kill.add_argument("--force", action="store_true")

    p_start = sub.add_parser("start", help="Start a process")
    p_start.add_argument("command", type=str)
    p_start.add_argument("--dir", type=str, help="Working directory")
    p_start.add_argument("--wait", action="store_true")

    p_info = sub.add_parser("info", help="Get process details")
    p_info.add_argument("--pid", type=int, required=True)

    p_sys = sub.add_parser("system", help="Get system resource info")

    args = parser.parse_args()

    if args.action == "list":
        print(list_processes(args.name))
    elif args.action == "kill":
        print(kill_process(args.pid, args.name, args.force))
    elif args.action == "start":
        print(start_process(args.command, args.dir, args.wait))
    elif args.action == "info":
        print(get_process_info(args.pid))
    elif args.action == "system":
        print(get_system_info())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
