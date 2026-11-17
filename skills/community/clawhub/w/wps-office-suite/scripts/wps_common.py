"""
WPS Office 全家桶 - 公共模块 v2.0
支持三引擎自动切换：WPS > MS Office > 纯 Python
"""
import sys
import time
import signal
import platform
from pathlib import Path

WPS_CLIENT = None
MS_CLIENT = None
MS_EXCEL_CLIENT = None
MS_PPT_CLIENT = None
ENGINE = None  # "WPS" / "MSOFFICE" / "PURE"


def detect_engine():
    """自动检测可用办公引擎"""
    global ENGINE
    if ENGINE is not None:
        return ENGINE

    # 1. 尝试 WPS
    try:
        import win32com.client
        wps = win32com.client.Dispatch("WPS.Application")
        _ = wps.Name  # 测试连通性
        ENGINE = "WPS"
        print(f"[Engine] 检测到 WPS Office", file=sys.stderr)
        return "WPS"
    except Exception:
        pass

    # 2. 尝试 MS Office
    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        _ = word.Name
        ENGINE = "MSOFFICE"
        print(f"[Engine] 检测到 Microsoft Office", file=sys.stderr)
        return "MSOFFICE"
    except Exception:
        pass

    # 3. 纯 Python 模式
    ENGINE = "PURE"
    print(f"[Engine] 未检测到 Office 软件，使用纯 Python 模式", file=sys.stderr)
    return "PURE"


def get_engine():
    """返回当前引擎"""
    if ENGINE is None:
        detect_engine()
    return ENGINE


def get_wps():
    """获取 WPS 实例（带超时和重试）"""
    global WPS_CLIENT
    if WPS_CLIENT is None:
        WPS_CLIENT = create_wps()
    return WPS_CLIENT


def get_ms_word():
    """获取 MS Word 实例"""
    global MS_CLIENT
    if MS_CLIENT is None:
        MS_CLIENT = create_ms_word()
    return MS_CLIENT


def create_wps():
    """创建 WPS COM 对象"""
    if sys.platform == "win32":
        try:
            import win32com.client
            app = win32com.client.Dispatch("WPS.Application")
            app.Visible = False
            return app
        except Exception as e:
            raise RuntimeError(
                f"WPS COM 创建失败：{e}\n"
                f"请确保已安装 WPS Office 2019+ 并重启电脑。"
            )
    elif sys.platform == "darwin":
        try:
            import appscript
            return appscript.app("WPS Office")
        except ImportError:
            raise RuntimeError("macOS 需安装 appscript：pip install appscript")
        except Exception as e:
            raise RuntimeError(f"macOS 下无法启动 WPS：{e}")
    else:
        raise RuntimeError(f"不支持的操作系统：{sys.platform}")


def create_ms_word():
    """创建 MS Word COM 对象"""
    if sys.platform == "win32":
        try:
            import win32com.client
            app = win32com.client.Dispatch("Word.Application")
            app.Visible = False
            return app
        except Exception as e:
            raise RuntimeError(
                f"MS Word COM 创建失败：{e}\n"
                f"请确保已安装 Microsoft Office。"
            )
    elif sys.platform == "darwin":
        try:
            import appscript
            return appscript.app("Microsoft Word")
        except Exception as e:
            raise RuntimeError(f"macOS 下无法启动 MS Word：{e}")
    else:
        raise RuntimeError(f"不支持的操作系统：{sys.platform}")


def create_ms_excel():
    """创建 MS Excel COM 对象"""
    if sys.platform == "win32":
        try:
            import win32com.client
            app = win32com.client.Dispatch("Excel.Application")
            app.Visible = False
            app.DisplayAlerts = False
            return app
        except Exception as e:
            raise RuntimeError(
                f"MS Excel COM 创建失败：{e}\n"
                f"请确保已安装 Microsoft Excel。"
            )
    elif sys.platform == "darwin":
        try:
            import appscript
            return appscript.app("Microsoft Excel")
        except Exception as e:
            raise RuntimeError(f"macOS 下无法启动 MS Excel：{e}")
    else:
        raise RuntimeError(f"不支持的操作系统：{sys.platform}")


def get_ms_excel():
    """获取 MS Excel 实例（带缓存）"""
    global MS_EXCEL_CLIENT
    if MS_EXCEL_CLIENT is None:
        MS_EXCEL_CLIENT = create_ms_excel()
    return MS_EXCEL_CLIENT


def create_ms_ppt():
    """创建 MS PowerPoint COM 对象（注意：PPT 不支持 Visible=False）"""
    if sys.platform == "win32":
        try:
            import win32com.client
            return win32com.client.Dispatch("PowerPoint.Application")
        except Exception as e:
            raise RuntimeError(
                f"MS PowerPoint COM 创建失败：{e}\n"
                f"请确保已安装 Microsoft PowerPoint。"
            )
    elif sys.platform == "darwin":
        try:
            import appscript
            return appscript.app("Microsoft PowerPoint")
        except Exception as e:
            raise RuntimeError(f"macOS 下无法启动 MS PowerPoint：{e}")
    else:
        raise RuntimeError(f"不支持的操作系统：{sys.platform}")


def get_ms_ppt():
    """获取 MS PowerPoint 实例（带缓存）"""
    global MS_PPT_CLIENT
    if MS_PPT_CLIENT is None:
        MS_PPT_CLIENT = create_ms_ppt()
    return MS_PPT_CLIENT


def release_wps(app=None):
    """释放 WPS COM"""
    global WPS_CLIENT
    target = app or WPS_CLIENT
    if target is not None:
        try:
            target.Quit()
        except Exception:
            pass
        WPS_CLIENT = None


def release_ms(app=None):
    """释放 MS COM（Word/Excel/PPT 三个槽位统一管理）"""
    global MS_CLIENT, MS_EXCEL_CLIENT, MS_PPT_CLIENT
    # 1. 显式传入的对象优先释放
    if app is not None:
        try:
            app.Quit()
        except Exception:
            pass
    # 2. 释放全部三个缓存槽位（Word/Excel/PPT 各自独立 COM 实例）
    for slot in (MS_CLIENT, MS_EXCEL_CLIENT, MS_PPT_CLIENT):
        if slot is not None:
            try:
                slot.Quit()
            except Exception:
                pass
    MS_CLIENT = None
    MS_EXCEL_CLIENT = None
    MS_PPT_CLIENT = None


def ensure_desktop_path(filename):
    if Path(filename).is_absolute():
        return Path(filename)
    desktop = Path.home() / "Desktop"
    return desktop / filename


def safe_path(path_str):
    """安全路径校验"""
    path = Path(path_str).resolve()
    parent = path.parent

    if not parent.exists():
        raise FileNotFoundError(
            f"目录不存在：{parent}\n"
            f"请检查路径是否正确，中文路径可能导致问题。"
        )

    problematic_chars = '<>"|?*' if platform.system() == "Windows" else ""
    name = path.name
    for ch in problematic_chars:
        if ch in name:
            raise ValueError(
                f"文件名包含非法字符 '{ch}'：{name}\n"
                f"建议重命名，移除特殊字符。"
            )

    return path


def with_retry(func, max_retries=2, delay=1):
    """重试装饰器（应对 WPS 超时/未响应）"""
    def wrapper(*args, **kwargs):
        last_error = None
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_error = e
                error_str = str(e).lower()
                if any(kw in error_str for kw in ["timeout", "not responding", "busy", "rpc", "server"]):
                    if attempt < max_retries:
                        time.sleep(delay * (attempt + 1))
                        continue
                raise
        raise last_error
    return wrapper


class WPSOperation:
    """WPS 操作上下文管理器"""
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.app = None

    def __enter__(self):
        self.app = get_wps()
        return self.app

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False


class MSOperation:
    """MS Office 操作上下文管理器"""
    def __init__(self, timeout=30):
        self.timeout = timeout
        self.app = None

    def __enter__(self):
        self.app = get_ms_word()
        return self.app

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
