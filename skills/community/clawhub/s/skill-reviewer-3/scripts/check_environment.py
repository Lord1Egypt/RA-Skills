#!/usr/bin/env python3
"""skill-reviewer 环境检查脚本（只读）

检查 Python 版本是否满足运行要求，输出 ready / needs_setup 状态。
不修改任何配置，不联网，不输出凭据。
"""
import sys

MIN_PY = (3, 10)


def main():
    version = sys.version_info[:2]
    if version >= MIN_PY:
        print(f"ready: Python {version[0]}.{version[1]} 满足要求 (>= {MIN_PY[0]}.{MIN_PY[1]})")
        return 0
    print(f"needs_setup: Python {version[0]}.{version[1]} 低于 {MIN_PY[0]}.{MIN_PY[1]}，请升级 Python")
    return 0


if __name__ == "__main__":
    main()
