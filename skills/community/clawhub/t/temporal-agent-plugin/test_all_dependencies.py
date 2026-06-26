#!/usr/bin/env python3
import sys
import os

if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

print("全面测试依赖项检查...")

# 测试所有使用pandas和numpy的模块
modules_to_test = [
    "core.temporal_analyzer",
    "core.anomaly_detector", 
    "core.smart_timeout_predictor",
    "core.causal_predictor"
]

all_passed = True

for module_name in modules_to_test:
    print(f"\n测试 {module_name}...")
    try:
        __import__(module_name)
        print(f"  ✓ 导入成功")
    except ImportError as e:
        print(f"  ✗ 导入失败: {e}")
        all_passed = False
    except Exception as e:
        print(f"  ✗ 其他错误: {e}")
        all_passed = False

print("\n" + "=" * 50)
if all_passed:
    print("🎉 所有依赖项检查通过！")
else:
    print("❌ 部分依赖项检查失败！")
print("=" * 50)
