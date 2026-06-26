#!/usr/bin/env python3
"""
下载 SenseVoice Small 模型到本地（使用 urllib，无 shell=True）
用法: python3 download_model.py [目标目录]
"""
import os
import sys
import urllib.request
import pathlib

DEST = os.environ.get(
    "SENSE_VOICE_MODEL_DIR",
    os.path.join(os.path.expanduser("~"), ".local", "share", "sense-voice-model")
)
if len(sys.argv) > 1:
    DEST = sys.argv[1]

DEST = pathlib.Path(DEST)
DEST.mkdir(parents=True, exist_ok=True)

BASE_URL = "https://modelscope.cn/api/v1/models/xiaowangge/sherpa-onnx-sense-voice-small/resolve/master"
FILES = [
    ("tokens.txt", "~309KB"),
    ("model.onnx",  "~895MB"),
]


def download(url, path):
    """带进度显示的下载，无 shell=True"""
    print(f"⬇️  {path.name} ({path.stat().st_size / 1024**2:.0f}MB)...")
    try:
        with urllib.request.urlopen(url, timeout=300) as resp:
            data = resp.read()
        path.write_bytes(data)
        size = len(data) / 1024**2
        print(f"  ✅ {path.name} done ({size:.1f}MB)")
    except Exception as e:
        print(f"  ❌ 下载失败: {e}")
        raise


# 检测是否已有文件，跳过已存在的
for fname, _ in FILES:
    p = DEST / fname
    if p.exists():
        size = p.stat().st_size / 1024**2
        print(f"⏭️  {fname} 已存在 ({size:.0f}MB)，跳过")
        FILES = [(f, d) for f, d in FILES if f != fname]

if not FILES:
    print("🎉 所有文件已就绪，无需下载")
    sys.exit(0)

print(f"📦 下载到: {DEST}")
print(f"   （可通过环境变量 SENSE_VOICE_MODEL_DIR 自定义路径）")
print()

for fname, desc in FILES:
    url = f"{BASE_URL}/{fname}"
    download(url, DEST / fname)

SIZE = sum(p.stat().st_size for p in DEST.iterdir()) / 1024**2
print()
print(f"🎉 下载完成！总计: {SIZE:.0f}MB")
print()
print("📝 下一步：配置环境变量")
print(f'   export SENSE_VOICE_MODEL_DIR="{DEST}"')
print("   然后运行: python3 scripts/check_env.py")
