"""
美股雷达仪表盘：一键汇总指数 + 期货 + 科技巨头
用法: python dashboard.py
"""
import subprocess
import sys
import os

base = os.path.dirname(os.path.abspath(__file__))

print("=" * 55)
print("  🦞 美股雷达仪表盘")
print("=" * 55)

print("\n>>> 主要指数 + 期货 + 大宗商品")
subprocess.run([sys.executable, os.path.join(base, "us_index.py")])

print("\n>>> 科技巨头 (NVDA/AAPL/MSFT/GOOGL/AMZN/META/TSLA/AMD)")
subprocess.run([sys.executable, os.path.join(base, "us_quote.py"),
                "NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "AMD"])
