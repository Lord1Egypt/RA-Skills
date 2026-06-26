#!/usr/bin/env python3
"""Jetson tegrastats 监控工具"""
import subprocess
import sys

def run_tegrastats():
    """运行 tegrastats"""
    try:
        result = subprocess.run(
            ['tegrastats', '--interval', '1000', '--stop'],
            capture_output=True,
            text=True,
            timeout=3
        )
        print(result.stdout if result.stdout else result.stderr)
    except FileNotFoundError:
        print("Error: tegrastats not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    run_tegrastats()
