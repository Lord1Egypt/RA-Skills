#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环境预检脚本 - 运行Skill前检查所有依赖是否就绪
"""
import os
import sys
import json
import subprocess
from pathlib import Path

def check_python():
    """检查Python"""
    print("检查 Python...")
    try:
        version = subprocess.check_output(
            [sys.executable, "--version"],
            stderr=subprocess.STDOUT
        ).decode().strip()
        print(f"  ✓ {version}")
        return True
    except Exception as e:
        print(f"  ✗ 错误: {e}")
        return False

def check_tesseract():
    """检查Tesseract"""
    print("检查 Tesseract OCR...")
    try:
        result = subprocess.run(
            ["tesseract", "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            version = result.stdout.strip().split('\n')[0]
            print(f"  ✓ {version}")
            # 检查版本号是否>=4.0
            try:
                ver_num = result.stdout.strip().split()[1]
                major = int(ver_num.split('.')[0])
                if major < 4:
                    print(f"  ⚠ Tesseract版本较低({ver_num})，建议升级到4.0+以获得更好的中文识别效果")
            except (IndexError, ValueError):
                pass
            return True
    except FileNotFoundError:
        pass
    
    # 检查常见问题
    print("  ✗ Tesseract 未安装，或未正确配置到系统PATH中")
    print("")
    print("  ============================================================")
    print("  【一键安装建议】（根据您的系统选择）")
    print("  ============================================================")
    print("")

    if sys.platform == "win32":
        print("  ┌─────────────────────────────────────────────────────────┐")
        print("  │ 方案一（推荐，最快）：使用 winget 一键安装              │")
        print("  │ ─────────────────────────────────────────────────────── │")
        print("  │ 在PowerShell中运行：                                    │")
        print("  │   winget install UB-Mannheim.TesseractOCR                │")
        print("  │                                                         │")
        print("  │ 优点：自动下载、自动配置PATH、包含中文语言包            │")
        print("  └─────────────────────────────────────────────────────────┘")
        print("")
        print("  ┌─────────────────────────────────────────────────────────┐")
        print("  │ 方案二：使用国内镜像手动下载（适合网络受限环境）        │")
        print("  │ ─────────────────────────────────────────────────────── │")
        print("  │ 国内镜像（gitee）：                                      │")
        print("  │   https://gitee.com/woaini0919/tesseract-ocr/releases   │")
        print("  │                                                         │")
        print("  │ 官网（可能较慢）：                                       │")
        print("  │   https://github.com/UB-Mannheim/tesseract/wiki           │")
        print("  │                                                         │")
        print("  │ 安装时务必勾选 'Chinese (Simplified)' 语言包！           │")
        print("  │ 安装后将安装目录 (如 C:\\Program Files\\Tesseract-OCR)    │")
        print("  │ 添加到系统PATH，并重启终端                               │")
        print("  └─────────────────────────────────────────────────────────┘")
        print("")
        print("  ┌─────────────────────────────────────────────────────────┐")
        print("  │ 方案三：使用 scoop 包管理器（适合开发者）              │")
        print("  │ ─────────────────────────────────────────────────────── │")
        print("  │   scoop install tesseract                               │")
        print("  └─────────────────────────────────────────────────────────┘")
    else:
        print("  ┌─────────────────────────────────────────────────────────┐")
        print("  │ Ubuntu/Debian:                                          │")
        print("  │   sudo apt-get install tesseract-ocr tesseract-ocr-chi-sim│")
        print("  │                                                         │")
        print("  │ CentOS/RHEL:                                            │")
        print("  │   sudo yum install tesseract tesseract-langpack-chi_sim   │")
        print("  │                                                         │")
        print("  │ macOS (使用Homebrew):                                    │")
        print("  │   brew install tesseract tesseract-lang                   │")
        print("  └─────────────────────────────────────────────────────────┘")

    print("")
    print("  安装完成后，请重启终端，然后重新运行此脚本验证。")
    return False

def check_python_packages():
    """检查Python包"""
    print("检查 Python 依赖包...")
    required = {
        'PIL': 'Pillow',
        'pytesseract': 'pytesseract',
        'openpyxl': 'openpyxl',
        'yaml': 'pyyaml'
    }
    
    all_ok = True
    for module, package in required.items():
        try:
            mod = __import__(module)
            version = getattr(mod, '__version__', '未知版本')
            print(f"  ✓ {package} ({version})")
        except ImportError:
            print(f"  ✗ {package} 未安装")
            print(f"    安装命令: pip install {package}")
            all_ok = False
    
    return all_ok

def check_language_data():
    """检查Tesseract中文语言数据"""
    print("检查 Tesseract 中文语言包...")
    
    # 常见语言数据路径
    possible_paths = [
        "/usr/share/tesseract-ocr/4.00/tessdata/chi_sim.traineddata",
        "/usr/share/tesseract-ocr/5.00/tessdata/chi_sim.traineddata",
        "/usr/local/share/tesseract-ocr/4.00/tessdata/chi_sim.traineddata",
        "/usr/local/share/tesseract-ocr/5.00/tessdata/chi_sim.traineddata",
        "C:\\Program Files\\Tesseract-OCR\\tessdata\\chi_sim.traineddata",
        "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata\\chi_sim.traineddata",
    ]
    
    # 也尝试通过tesseract命令查找
    try:
        result = subprocess.run(
            ["tesseract", "--list-langs"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            langs = result.stdout.strip().split('\n')[1:]  # 跳过第一行标题
            if 'chi_sim' in langs:
                print("  ✓ 中文简体语言包 (chi_sim) 已安装")
                # 检查语言包文件大小（chi_sim约10MB）
                for path in possible_paths:
                    if Path(path).exists():
                        size_mb = Path(path).stat().st_size / (1024 * 1024)
                        if size_mb < 5:
                            print(f"  ⚠ 语言包文件过小({size_mb:.1f}MB)，可能不完整")
                        break
                return True
            else:
                print(f"  ✗ 中文简体语言包未安装")
                print(f"    已安装的语言: {', '.join(langs[:10])}")
                return False
    except Exception:
        pass
    
    # 检查文件路径
    for path in possible_paths:
        if Path(path).exists():
            print(f"  ✓ 中文简体语言包已找到: {path}")
            return True
    
    print("  ✗ 中文简体语言包 (chi_sim) 未找到")
    print("")
    print("  【解决方案】")
    print("  1. 重新安装Tesseract，安装时勾选 'Chinese (Simplified)'")
    print("  2. 或手动下载: https://github.com/tesseract-ocr/tessdata")
    print("     将 chi_sim.traineddata 放到 tessdata 目录")
    return False

def check_poppler():
    """检查poppler（PDF支持）"""
    print("检查 Poppler (PDF支持)...")
    try:
        result = subprocess.run(
            ["pdftoppm", "-v"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            print("  ✓ Poppler 已安装")
            return True
    except FileNotFoundError:
        pass
    
    print("  ⚠ Poppler 未安装（可选，用于PDF发票识别）")
    if sys.platform == "win32":
        print("    下载地址: https://github.com/oschwartz10612/poppler-windows/releases")
    else:
        print("    Ubuntu/Debian: sudo apt-get install poppler-utils")
        print("    macOS:        brew install poppler")
    return False

def main():
    print("=" * 50)
    print("  财税合规全链路助手 - 环境预检")
    print("=" * 50)
    print("")
    
    checks = [
        ("Python", check_python),
        ("Tesseract OCR", check_tesseract),
        ("中文语言包", check_language_data),
        ("Python依赖包", check_python_packages),
        ("Poppler (PDF支持)", check_poppler),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ 检查失败: {e}")
            results.append((name, False))
        print("")
    
    print("=" * 50)
    print("  预检结果汇总")
    print("=" * 50)
    
    all_ok = True
    for name, result in results:
        if result:
            status = "✅ 通过"
        else:
            status = "❌ 失败  ← 需要处理"
        print(f"  {status}  {name}")
        if not result:
            all_ok = False
    
    print("")
    if all_ok:
        print("🎉 环境就绪！可以开始使用Skill。")
        print("")
        print("下一步:")
        print("  1. 复制配置模板: cp templates/config_template.yaml config.yaml")
        print("  2. 编辑 config.yaml 配置企业信息")
        print("  3. 运行: python scripts/ocr_engine.py --input 发票图片.png")
    else:
        print("⚠️  环境未完全就绪，请按上述提示安装缺失组件。")
        print("")
        print("💡 最常缺失的是 Tesseract OCR 和中文语言包。")
        print("   推荐使用 winget 一键安装（见上方方案一）。")
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
