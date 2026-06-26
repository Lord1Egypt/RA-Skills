#!/usr/bin/env python3
import sys
import os

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("测试依赖项检查...")
try:
    from core.temporal_analyzer import TemporalAnalyzer
    print("✓ 依赖项检查通过")
    analyzer = TemporalAnalyzer()
    print("✓ TemporalAnalyzer 初始化成功")
except ImportError as e:
    print(f"✗ 依赖项检查失败: {e}")
except Exception as e:
    print(f"✗ 其他错误: {e}")
