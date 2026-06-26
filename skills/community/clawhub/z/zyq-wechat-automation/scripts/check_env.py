"""
pywechat3 环境检查脚本
检查：Python版本、依赖包、微信安装状态
"""
import sys
import os
import subprocess
import winreg

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    ok = '[OK]' if sys.stdout.encoding and 'utf' in sys.stdout.encoding.lower() else 'v'
    x = '[X]'
    print(f'  {ok} Python 版本: {version.major}.{version.minor}.{version.micro}')
    if version.major < 3:
        print(f'  {x} Python 版本过低，需要 3.x')
        return False
    return True

def check_dependency(package_name, import_name=None, alt_import=None):
    """检查单个依赖是否已安装"""
    ok = '[OK]'
    x = '[X]'
    if import_name is None:
        import_name = package_name.replace("-", "_")

    try:
        __import__(import_name)
        print(f'  {ok} {package_name} 已安装')
        return True
    except ImportError:
        pass

    if alt_import:
        try:
            __import__(alt_import)
            print(f'  {ok} {package_name} 已安装 ({alt_import})')
            return True
        except ImportError:
            pass

    print(f'  {x} {package_name} 未安装')
    return False

def check_pywechat():
    """检查 pywechat127 是否安装"""
    ok = '[OK]'
    x = '[X]'
    try:
        import pywechat
        print(f'  {ok} pywechat127 已安装 (版本: {getattr(pywechat, "__version__", "未知")})')
        return True
    except ImportError:
        print(f'  {x} pywechat127 未安装')
        return False

def check_wechat_installed():
    """检查微信是否安装（通过注册表）"""
    ok = '[OK]'
    x = '[X]'
    reg_paths = [
        (winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat"),
        (winreg.HKEY_LOCAL_MACHINE, r"Software\Tencent\WeChat"),
    ]

    for hkey, path in reg_paths:
        try:
            with winreg.OpenKey(hkey, path):
                try:
                    with winreg.OpenKey(hkey, path + r"\InstallPath") as key:
                        install_path, _ = winreg.QueryValueEx(key, "")
                        print(f'  {ok} 微信已安装: {install_path}')
                        return True
                except FileNotFoundError:
                    print(f'  {ok} 微信注册表存在（路径未找到）')
                    return True
        except FileNotFoundError:
            continue

    print(f'  {x} 未找到微信安装注册表（微信可能未安装或版本不支持）')
    return False

def check_wechat_in_path():
    """检查微信是否在环境变量中"""
    ok = '[OK]'
    warn = '[!]'
    try:
        result = subprocess.run(
            ["where", "WeChat.exe"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            path = result.stdout.strip().split("\n")[0]
            print(f'  {ok} 微信在 PATH 中: {path}')
            return True
    except Exception:
        pass

    print(f'  {warn} 微信未添加到 PATH（pywechat 会自动尝试定位，但建议手动添加）')
    return False

def check_pip():
    """检查 pip 是否可用"""
    ok = '[OK]'
    x = '[X]'
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            version_line = result.stdout.strip()
            print(f'  {ok} pip 可用: {version_line}')
            return True
    except Exception as e:
        print(f'  {x} pip 不可用: {e}')
        return False

def print_install_help():
    """打印安装指南"""
    print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  安装指南
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. 安装 pywechat127 及依赖：
     pip install pywechat127 psutil pywin32

  2. 将微信添加到 PATH（可选，推荐）：
     运行以下 Python 代码（只需一次）：
     >>> from pywechat.WechatTools import Tools
     >>> Tools.set_wechat_as_environ_path()

  3. 确保微信版本：3.9.12.x 或 4.0+
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

def main():
    print("=" * 50)
    print("  pywechat3 环境检查")
    print("=" * 50)

    checks = [
        ("Python 版本", check_python_version),
        ("pip 可用性", check_pip),
        ("pywechat127", check_pywechat),
        ("pywinauto", lambda: check_dependency("pywinauto")),
        ("pyautogui", lambda: check_dependency("pyautogui")),
        ("psutil", lambda: check_dependency("psutil")),
        ("pywin32", lambda: check_dependency("pywin32", "win32api")),
        ("微信安装状态", check_wechat_installed),
        ("微信 PATH", check_wechat_in_path),
    ]

    results = []
    for name, func in checks:
        try:
            result = func()
            results.append((name, result))
        except Exception as e:
            print(f'  [X] {name} 检查出错: {e}')
            results.append((name, False))
        print()

    passed = sum(1 for _, r in results if r)
    total = len(results)
    print('=' * 50)
    print(f'  检查完成: {passed}/{total} 项通过')
    print('=' * 50)

    if passed == total:
        print('  [OK] 环境就绪，可以开始使用微信自动化！')
    else:
        print_install_help()

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
