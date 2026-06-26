#!/usr/bin/env python3
"""Trading_Agents_for_Futures - 自动安装依赖"""

import subprocess
import sys


def main():
    deps = [
        "akshare>=1.14.0",
        "pandas>=2.0.0",
        "numpy>=1.24.0",
        "pyarrow>=12.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "python-dotenv>=1.0.0",
    ]

    missing = []
    for dep in deps:
        name = dep.split(">=")[0].split("<")[0]
        try:
            __import__(name.replace("-", "_"))
        except ImportError:
            missing.append(dep)

    if not missing:
        print("所有依赖已安装。")
        return

    print(f"正在安装: {' '.join(missing)}")
    cmd = [sys.executable, "-m", "pip", "install"] + missing

    try:
        subprocess.run(cmd, check=True)
        print("安装完成。")
    except subprocess.CalledProcessError:
        print("安装失败。请确认 pip 可用并重试。")
        sys.exit(1)


if __name__ == "__main__":
    main()
