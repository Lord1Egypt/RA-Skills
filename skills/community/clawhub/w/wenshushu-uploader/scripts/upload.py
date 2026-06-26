#!/usr/bin/env python3
"""
文叔叔文件上传脚本
Wenshushu file upload script
"""

import sys
import os
import subprocess
from pathlib import Path

# 工作目录（OpenClaw workspace）
WORKSPACE = Path("/root/.openclaw/workspace")

# uv 路径
UV_PATH = "/root/.local/bin/uv"

def check_wssf_installed():
    """检查 wssf 是否已安装"""
    try:
        # 尝试运行 wssf --help
        result = subprocess.run(
            [UV_PATH, "run", "wssf", "--help"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def install_wssf():
    """安装 wssf"""
    print("📦 正在安装 wssf...")
    try:
        # 使用 uv 安装 wssf
        subprocess.run(
            [UV_PATH, "pip", "install", "wssf==5.0.6"],
            check=True,
            timeout=120
        )
        print("✅ wssf 安装完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ wssf 安装失败: {e}")
        return False

def upload_file(filepath, pickup_code=None, use_login=False, proxy=None):
    """
    上传文件到文叔叔

    Args:
        filepath: 文件路径
        pickup_code: 取件码（4位数字），None 表示随机生成
        use_login: 是否使用登录账户
        proxy: 代理地址

    Returns:
        dict: 包含上传结果的字典
    """
    filepath = Path(filepath).resolve()

    if not filepath.exists():
        return {
            "success": False,
            "error": f"文件不存在: {filepath}"
        }

    # 构建命令
    cmd = [UV_PATH, "run", "wssf", "upload", str(filepath)]

    if pickup_code:
        cmd.extend(["-k", str(pickup_code)])
    elif pickup_code is None:  # 默认随机生成
        cmd.append("-r")

    if use_login:
        cmd.append("-l")

    if proxy:
        cmd.extend(["-p", proxy])

    try:
        print(f"📤 正在上传: {filepath.name} ({filepath.stat().st_size / 1024:.1f} KB)")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        output = result.stdout + result.stderr

        if result.returncode != 0:
            return {
                "success": False,
                "error": f"上传失败: {output}"
            }

        # 解析输出
        lines = output.strip().split('\n')

        # 提取信息
        info = {
            "success": True,
            "filename": filepath.name,
            "size": filepath.stat().st_size,
        }

        for line in lines:
            if "公共链接：" in line or "Public link：" in line:
                info["public_url"] = line.split("：", 1)[1].strip()
            elif "取件码：" in line or "Pickup code：" in line:
                info["pickup_code"] = line.split("：", 1)[1].strip()
            elif "个人管理链接：" in line or "Management link：" in line:
                info["management_url"] = line.split("：", 1)[1].strip()

        return info

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "上传超时（5分钟）"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"上传异常: {str(e)}"
        }

def format_result(result):
    """格式化上传结果"""
    if not result.get("success"):
        return f"❌ 上传失败: {result.get('error', '未知错误')}"

    msg = [
        "✅ 文件上传成功！",
        f"📄 文件名: {result['filename']}",
        f"📏 大小: {result['size'] / 1024:.1f} KB" if result['size'] < 1024*1024 else f"📏 大小: {result['size'] / 1024 / 1024:.1f} MB",
        "",
        "🔗 下载链接:",
        f"  {result.get('public_url', 'N/A')}",
        "",
        f"🔢 取件码: {result.get('pickup_code', 'N/A')}",
    ]

    if result.get('management_url'):
        msg.extend([
            "",
            "📋 管理链接:",
            f"  {result['management_url']}"
        ])

    msg.extend([
        "",
        "请在浏览器中打开下载链接，输入取件码即可下载。"
    ])

    return "\n".join(msg)

def main():
    """主函数（命令行直接调用）"""
    if len(sys.argv) < 2:
        print("用法: upload.py <文件路径> [取件码]")
        sys.exit(1)

    filepath = sys.argv[1]
    pickup_code = sys.argv[2] if len(sys.argv) > 2 else None

    # 确保 wssf 已安装
    if not check_wssf_installed():
        print("⚠️ wssf 未安装，尝试安装...")
        if not install_wssf():
            print("❌ 无法安装 wssf，请手动安装")
            sys.exit(1)

    # 上传文件
    result = upload_file(filepath, pickup_code=pickup_code)
    print(format_result(result))

    sys.exit(0 if result['success'] else 1)

if __name__ == "__main__":
    main()