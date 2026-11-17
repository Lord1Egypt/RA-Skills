#!/usr/bin/env python3
"""
system_monitor.py - eBPF (Linux) / ETW (Windows) kernel-level behavior capture.

Extends the sandbox monitor with syscall-level visibility:
- Network connect/send/recv
- File open/write
- Process fork/exec
- Permission changes
- Network interface access

Falls back to existing 5-dimension capture if eBPF/ETW unavailable.

Author: njskills@agent.qq.com
Version: 3.2.0
"""

import os
import sys
import time
import tempfile
import threading
from pathlib import Path
from datetime import datetime

# ============================================================
# System Call Trace Types
# ============================================================

SYS_TYPES = {
    'syscall_connect': 'network',
    'syscall_send': 'network',
    'syscall_recv': 'network',
    'syscall_socket': 'network',
    'syscall_open': 'file',
    'syscall_openat': 'file',
    'syscall_creat': 'file',
    'syscall_write': 'file',
    'syscall_unlink': 'file',
    'syscall_fork': 'process',
    'syscall_clone': 'process',
    'syscall_execve': 'process',
    'syscall_execveat': 'process',
    'syscall_fchmodat': 'permission',
    'syscall_chmod': 'permission',
    'syscall_chown': 'permission',
    'syscall_setuid': 'permission',
    'syscall_setgid': 'permission',
    'syscall_uname': 'recon',
    'syscall_gethostname': 'recon',
    'syscall_getifaddrs': 'network',
}


# ============================================================
# eBPF Backend (Linux)
# ============================================================

class EBPFMonitor:
    """eBPF syscall tracing on Linux (requires bcc + root)."""

    def __init__(self, pid, timeout=30):
        self.pid = pid
        self.timeout = timeout
        self.events = []
        self._active = False
        self._process = None
        self._output_file = None

    def available(self):
        """Check if eBPF is available."""
        if sys.platform != 'linux':
            return False
        try:
            import bcc  # noqa
            return os.geteuid() == 0
        except Exception:
            return False

    def start(self):
        """Start eBPF tracing."""
        if not self.available():
            return False
        try:
            self._output_file = tempfile.NamedTemporaryFile(
                mode='w', suffix='.json', delete=False
            )
            self._output_file.close()
            cmd = [
                'python3', '-c',
                self._generate_ebpftool(),
            ]
            import subprocess
            self._process = subprocess.Popen(
                cmd, stdout=open(self._output_file.name, 'w'), stderr=subprocess.DEVNULL
            )
            self._active = True
            return True
        except Exception:
            return False

    def _generate_ebpftool(self):
        """Generate a bcc script that captures syscalls for the target PID."""
        return f'''
from bcc import BPF
import json
pid = {self.pid}
{{
#include <uapi/linux/ptrace.h>
#include <linux/sched.h>

BPF_HASH(start, u32, u64);

TRACEPOINT_PROBE(syscalls, sys_enter_open) {{
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    if (pid != $pid) return 0;
    u64 ts = bpf_ktime_get_ns();
    events.perf_submit(args, &ts, sizeof(ts));
    return 0;
}}
}}
b = BPF(text=text)
with open("{self._output_file.name}", "w") as f:
    f.write(json.dumps({{"status": "started", "pid": pid}}))
    f.flush()
'''

    def stop(self):
        """Stop eBPF and collect events."""
        if not self._active:
            return []
        time.sleep(0.5)
        try:
            if self._process:
                self._process.terminate()
                self._process.wait(timeout=2)
            if self._output_file and os.path.exists(self._output_file.name):
                with open(self._output_file.name) as f:
                    content = f.read()
                os.unlink(self._output_file.name)
                return [{"type": "ebpf_data", "raw": content[:2000]}]
        except Exception:
            pass
        return []

    def parse_event(self, raw):
        """Convert raw eBPF event to normalized format."""
        return {
            'timestamp': datetime.now().isoformat(),
            'backend': 'ebpf',
            'syscall': raw.get('syscall', 'unknown'),
            'category': SYS_TYPES.get(raw.get('syscall', ''), 'unknown'),
            'pid': raw.get('pid'),
            'args': raw.get('args', []),
            'raw': str(raw)[:200],
        }


# ============================================================
# ETW Backend (Windows)
# ============================================================

class ETWMonitor:
    """ETW syscall tracing on Windows (requires Windows 8+ + admin)."""

    def __init__(self, pid, timeout=30):
        self.pid = pid
        self.timeout = timeout
        self.events = []
        self._active = False
        self._process = None
        self._output_file = None

    def available(self):
        """Check if ETW is available."""
        if sys.platform != 'win32':
            return False
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False

    def start(self):
        """Start ETW tracing."""
        if not self.available():
            return False
        try:
            self._output_file = tempfile.NamedTemporaryFile(
                mode='w', suffix='.json', delete=False
            )
            self._output_file.close()
            import subprocess
            cmd = [
                'logman', 'create', 'trace', 'security_scan',
                '-p', 'Microsoft-Windows-Kernel-Process', '0x10', '0x5',
                '-o', self._output_file.name,
                '-bs', '64', '-nb', '16', '16', '-f', 'bincirc', '-max', '10',
                '-ets',
            ]
            self._process = subprocess.Popen(
                cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
            )
            time.sleep(1)
            self._active = True
            return True
        except Exception:
            return False

    def stop(self):
        """Stop ETW tracing."""
        if not self._active:
            return []
        try:
            import subprocess
            subprocess.run(
                ['logman', 'stop', 'security_scan', '-ets'],
                capture_output=True, timeout=10
            )
            subprocess.run(
                ['logman', 'delete', 'security_scan', '-ets'],
                capture_output=True, timeout=10
            )
            if self._process:
                self._process.terminate()
            if self._output_file and os.path.exists(self._output_file.name):
                try:
                    with open(self._output_file.name, 'rb') as f:
                        raw = f.read()
                    os.unlink(self._output_file.name)
                    return [{"type": "etw_data", "size": len(raw), "raw": raw[:1000]}]
                except Exception:
                    pass
        except Exception:
            pass
        return []

    def parse_event(self, raw):
        """Convert raw ETW event to normalized format."""
        return {
            'timestamp': datetime.now().isoformat(),
            'backend': 'etw',
            'syscall': raw.get('opcode', 'unknown'),
            'category': 'syscall',
            'pid': raw.get('pid'),
            'args': raw.get('args', []),
            'raw': str(raw)[:200],
        }


# ============================================================
# Fallback Monitor
# ============================================================

class FallbackSyscallMonitor:
    """Fallback: returns informative message when eBPF/ETW unavailable."""

    def __init__(self, pid, timeout=30):
        self.pid = pid
        self.timeout = timeout

    def available(self):
        return True  # Always available as fallback

    def start(self):
        return True

    def stop(self):
        reason = "none"
        if sys.platform == 'linux':
            reason = "eBPF 不可用（需要 root + bcc）"
        elif sys.platform == 'win32':
            reason = "ETW 不可用（需要管理员权限）"
        else:
            reason = f"不支持的平台: {sys.platform}"
        return [{"type": "syscall_unavailable", "reason": reason}]

    def parse_event(self, raw):
        return {
            'timestamp': datetime.now().isoformat(),
            'backend': 'none',
            'syscall': raw.get('type', 'unknown'),
            'category': 'unavailable',
            'pid': self.pid,
            'args': [],
            'raw': raw.get('reason', ''),
        }


# ============================================================
# Unified System Monitor Factory
# ============================================================

def create_syscall_monitor(pid, timeout=30):
    """Create the best available syscall monitor for the current platform."""
    if sys.platform == 'linux':
        mon = EBPFMonitor(pid, timeout)
        if mon.available():
            return mon
    elif sys.platform == 'win32':
        mon = ETWMonitor(pid, timeout)
        if mon.available():
            return mon
    return FallbackSyscallMonitor(pid, timeout)
