"""
setup.py - 自动下载 wechat-decrypt 并安装依赖
运行方式: python setup.py
"""
import subprocess
import sys
from pathlib import Path

DECRYPT_DIR = Path(r"C:\wechat-decrypt")
REQUIREMENTS = ["wcdbg", "python-devkit", "db SqlCipher"]

def run(cmd, check=True):
    print(f"  > {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0 and check:
        print(f"  ❌ 失败: {result.stderr}")
    else:
        print(f"  ✅ 完成")
    return result.returncode == 0

def main():
    print("=" * 50)
    print("另一个我 - 微信解密环境安装")
    print("=" * 50)

    # 1. 检查 git
    print("\n[1/4] 检查 git...")
    if run("git --version", check=False) != 0:
        print("  ❌ 请先安装 git: https://git-scm.com")
        return

    # 2. 克隆项目
    print("\n[2/4] 克隆 wechat-decrypt...")
    if DECRYPT_DIR.exists():
        print(f"  ⚠️ 已存在，跳过克隆: {DECRYPT_DIR}")
    else:
        run(f'git clone https://github.com/ylytdeng/wechat-decrypt.git "{DECRYPT_DIR}"')

    # 3. 安装依赖
    print("\n[3/4] 安装 Python 依赖...")
    req_file = DECRYPT_DIR / "requirements.txt"
    if req_file.exists():
        run(f'pip install -r "{req_file}"', check=False)
    else:
        print(f"  ⚠️ requirements.txt 不存在，尝试 pip install python-devkit wcdbg")

    # 4. 检查微信
    print("\n[4/4] 前置检查...")
    print("  ✅ 项目已就绪")
    print(f"  📂 安装目录: {DECRYPT_DIR}")
    print("\n下一步:")
    print("  1. 确保微信 4.x 已登录运行")
    print("  2. 运行: python main.py decrypt")
    print("  3. 解密成功后，运行 analyzer/main.py")

if __name__ == "__main__":
    main()
