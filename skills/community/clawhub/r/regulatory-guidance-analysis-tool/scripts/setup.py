"""gugu-gaga 环境初始化脚本

```
python scripts/setup.py
```

一次性安装所有依赖（使用阿里源加速）。
"""
import subprocess, sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
MIRROR = "https://mirrors.aliyun.com/pypi/simple"
PIP_FLAGS = ["-i", MIRROR, "--trusted-host", "mirrors.aliyun.com"]


def run(cmd):
    print(f"\n>>> {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(SKILL_DIR))
    if r.returncode != 0:
        print(f"FAILED (exit {r.returncode})")
        sys.exit(r.returncode)


# Step 1: markitdown
run([sys.executable, "-m", "pip", "install", "-e", "packages/markitdown[docx,pdf]"] + PIP_FLAGS)

# Step 2: 转换依赖
run([sys.executable, "-m", "pip", "install", "playwright", "python-pptx", "Pillow"] + PIP_FLAGS)

print("\nsetup 完成 ✅")
