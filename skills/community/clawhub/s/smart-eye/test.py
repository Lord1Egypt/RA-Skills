"""SmartEye 测试脚本"""
import sys
from pathlib import Path

# smart_eye 包根目录
_root = Path(__file__).parent
# src/ 目录加入 path（供 smarteye.py 内部使用）
sys.path.insert(0, str(_root / "src"))
# 顶层加入 path（使 smart_eye 包可被导入）
sys.path.insert(0, str(_root))

# ---- 测试 ----
print("=== SmartEye 内置测试 ===\n")

from src.smarteye import parse_and_execute, _extract_action
from src.config import load_devices, find_camera, list_cameras
from src.protocol.brands import get_brand, BRANDS

devices = load_devices()
print(f"加载了 {len(devices.get('cameras', []))} 个摄像头")
print("摄像头列表:")
for line in list_cameras(devices):
    print(" ", line)

print(f"\n已注册品牌: {list(BRANDS.keys())}")

test_inputs = [
    "tplink点头",
    "建国路摄像头摇头",
    "华为放大",
    "摄像头停止",
    "有哪些摄像头",
]
print("\n动作解析:")
for inp in test_inputs:
    cam, action = _extract_action(inp)
    print(f"  「{inp}」→ cam={cam!r}  action={action!r}")

print("\n执行测试:")
for inp in test_inputs:
    result = parse_and_execute(inp, devices)
    print(f"  [{inp}] -> {result[:80].encode('utf-8', errors='replace').decode('utf-8')}")

print("\n测试完成!")
