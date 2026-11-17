"""
Sandbox subpackage - Dynamic execution scanning for skill-security-checker.

This subpackage runs skill scripts inside an isolated environment (Docker or
Windows Sandbox) and captures runtime behavior that static analysis cannot see:
network requests, file read/write, process creation, registry writes and
environment-variable reads.

Public entry point:
    run_dynamic_scan(skill_path, options) -> dict

Design principles:
  - Self-contained, no external API keys required.
  - Network disabled by default; domains opened only via an explicit whitelist.
  - Graceful degradation: if no isolation backend is available, return a clear
    hint ("建议在沙箱环境中进行动态扫描") instead of raising.
  - Resource-limited: CPU/memory/timeout caps so the host machine is never
    overloaded.

Author: njskills@agent.qq.com
"""

from .runner import run_dynamic_scan, DynamicScanOptions

__all__ = ['run_dynamic_scan', 'DynamicScanOptions']
