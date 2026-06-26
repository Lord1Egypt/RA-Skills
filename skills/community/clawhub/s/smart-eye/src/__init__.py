"""
SmartEye Skill Package

使用方式：
  from smart_eye import handle

OpenClaw 会从 skills/smart-eye/ 目录加载此包。
"""

from .smarteye import handle, parse_and_execute

__all__ = ["handle", "parse_and_execute"]
