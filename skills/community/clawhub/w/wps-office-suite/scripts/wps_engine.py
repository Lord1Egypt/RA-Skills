"""
WPS 引擎检测器 v2.2 - 按用户电脑实际安装的软件选择引擎
优先级: WPS > MS Office > LibreOffice > 纯Python
"""
import subprocess
import shutil
from pathlib import Path

ENGINE_CACHE = None


def is_wps_installed() -> bool:
    """检测 WPS 是否安装"""
    try:
        import win32com.client
        wps = win32com.client.Dispatch("WPS.Application")
        _ = wps.Name
        wps.Quit()
        return True
    except Exception:
        return False


def is_msword_installed() -> bool:
    """检测 MS Word 是否安装"""
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        _ = word.Name
        word.Quit()
        return True
    except Exception:
        return False


def is_msexcel_installed() -> bool:
    """检测 MS Excel 是否安装"""
    try:
        import win32com.client
        excel = win32com.client.Dispatch("Excel.Application")
        _ = excel.Name
        excel.Quit()
        return True
    except Exception:
        return False


def is_msppt_installed() -> bool:
    """检测 MS PPT 是否安装"""
    try:
        import win32com.client
        ppt = win32com.client.Dispatch("PowerPoint.Application")
        _ = ppt.Name
        ppt.Quit()
        return True
    except Exception:
        return False


def is_libreoffice_installed() -> bool:
    """检测 LibreOffice 是否安装（跨平台）"""
    # 方法1：命令行
    if shutil.which("soffice") or shutil.which("libreoffice"):
        return True
    
    # 方法2：Windows 注册表
    if __import__("sys").platform == "win32":
        try:
            import winreg
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\LibreOffice")
                winreg.CloseKey(key)
                return True
            except Exception:
                pass
        except ImportError:
            pass
    
    return False


def detect_best_engine():
    """
    根据用户电脑实际安装的软件选择最佳引擎。
    
    返回:
        {
            "engine": "WPS" | "MSOFFICE" | "LIBREOFFICE" | "PURE",
            "word": bool,
            "excel": bool,
            "ppt": bool,
            "libreoffice": bool,
            "wps": bool,
            "platform": "windows" | "linux" | "darwin",
        }
    """
    global ENGINE_CACHE
    if ENGINE_CACHE:
        return ENGINE_CACHE

    import platform
    plat = platform.system().lower()

    wps_ok = is_wps_installed()
    msword_ok = is_msword_installed()
    msexcel_ok = is_msexcel_installed()
    msppt_ok = is_msppt_installed()
    libre_ok = is_libreoffice_installed()

    # WPS：三件套都有
    if wps_ok:
        engine = "WPS"
    # MS Office：至少 Word 能用
    elif msword_ok:
        engine = "MSOFFICE"
    # LibreOffice：兜底
    elif libre_ok:
        engine = "LIBREOFFICE"
    # 都没有
    else:
        engine = "PURE"

    ENGINE_CACHE = {
        "engine": engine,
        "word": wps_ok or msword_ok or libre_ok or False,
        "excel": wps_ok or msexcel_ok or libre_ok or False,
        "ppt": wps_ok or msppt_ok or libre_ok or False,
        "wps": wps_ok,
        "msword": msword_ok,
        "msexcel": msexcel_ok,
        "msppt": msppt_ok,
        "libreoffice": libre_ok,
        "platform": plat,
    }
    return ENGINE_CACHE


def get_engine():
    """返回当前最佳引擎名"""
    return detect_best_engine()["engine"]


def report():
    """返回可读的引擎检测报告"""
    e = detect_best_engine()
    lines = [
        f"引擎: {e['engine']}",
        f"操作系统: {e['platform']}",
        f"WPS Office: {'✅' if e['wps'] else '❌'}",
        f"MS Word: {'✅' if e['msword'] else '❌'}",
        f"MS Excel: {'✅' if e['msexcel'] else '❌'}",
        f"MS PPT: {'✅' if e['msppt'] else '❌'}",
        f"LibreOffice: {'✅' if e['libreoffice'] else '❌'}",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    import json
    print(json.dumps(detect_best_engine(), ensure_ascii=False, indent=2))
