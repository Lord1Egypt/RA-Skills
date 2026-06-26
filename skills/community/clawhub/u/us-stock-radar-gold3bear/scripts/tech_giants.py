"""
美股科技巨头组合
NVDA / AAPL / MSFT / GOOGL / AMZN / META / TSLA / AMD
"""
import subprocess
import sys
import os

base = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    tech_stocks = ["NVDA", "AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "AMD"]
    print("=== 苹果+微软+谷歌+Meta+英伟达+特斯拉+AMD ===")
    subprocess.run([sys.executable, os.path.join(base, "us_quote.py")] + tech_stocks)
