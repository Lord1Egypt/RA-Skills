"""
WPS Office 全家桶 - 环境自检
一键检测：引擎、依赖、WPS 版本、路径、权限
"""
import sys
import json
import os
import platform
from pathlib import Path
from datetime import datetime


def check_python_version() -> dict:
    """检查 Python 版本"""
    ver = sys.version_info
    ok = ver >= (3, 8)
    return {
        "ok": ok,
        "version": f"{ver.major}.{ver.minor}.{ver.micro}",
        "required": "3.8+",
        "message": "✅ Python 版本满足" if ok else "❌ Python 版本过低，需要 3.8+",
    }


def check_platform() -> dict:
    """检查操作系统"""
    system = platform.system()
    return {
        "ok": True,
        "system": system,
        "release": platform.release(),
        "machine": platform.machine(),
    }


def check_pywin32() -> dict:
    """检查 pywin32（Windows COM 依赖）"""
    if sys.platform != "win32":
        return {"ok": True, "skipped": True, "message": "⏭️ 非 Windows，跳过"}

    try:
        import win32com.client
        return {"ok": True, "message": "✅ pywin32 已安装"}
    except ImportError:
        return {
            "ok": False,
            "message": "❌ pywin32 未安装",
            "hint": "运行: pip install pywin32",
        }


def check_python_docx() -> dict:
    """检查 python-docx"""
    try:
        import docx
        return {"ok": True, "message": "✅ python-docx 已安装"}
    except ImportError:
        return {
            "ok": False,
            "message": "❌ python-docx 未安装",
            "hint": "运行: pip install python-docx",
        }


def check_openpyxl() -> dict:
    """检查 openpyxl"""
    try:
        import openpyxl
        return {"ok": True, "message": "✅ openpyxl 已安装"}
    except ImportError:
        return {
            "ok": False,
            "message": "❌ openpyxl 未安装",
            "hint": "运行: pip install openpyxl",
        }


def check_python_pptx() -> dict:
    """检查 python-pptx"""
    try:
        import pptx
        return {"ok": True, "message": "✅ python-pptx 已安装"}
    except ImportError:
        return {
            "ok": False,
            "message": "❌ python-pptx 未安装",
            "hint": "运行: pip install python-pptx",
        }


def check_wps() -> dict:
    """检查 WPS 是否安装"""
    if sys.platform != "win32":
        return {"ok": None, "skipped": True, "message": "⏭️ 非 Windows，跳过"}

    try:
        import win32com.client
        wps = win32com.client.Dispatch("WPS.Application")
        name = wps.Name
        version = wps.Version if hasattr(wps, "Version") else "未知"
        wps.Quit()
        return {
            "ok": True,
            "message": f"✅ WPS Office 已安装（{version}）",
            "version": version,
        }
    except Exception as e:
        return {
            "ok": False,
            "message": "❌ WPS Office 未安装或 COM 注册失败",
            "hint": "安装 WPS Office 2019+ 后重启电脑",
        }


def check_ms_office() -> dict:
    """检查 MS Office 是否安装"""
    if sys.platform != "win32":
        return {"ok": None, "skipped": True, "message": "⏭️ 非 Windows，跳过"}

    try:
        import win32com.client
        word = win32com.client.Dispatch("Word.Application")
        name = word.Name
        version = word.Version if hasattr(word, "Version") else "未知"
        word.Quit()
        return {
            "ok": True,
            "message": f"✅ Microsoft Office 已安装（{version}）",
            "version": version,
        }
    except Exception:
        return {
            "ok": False,
            "message": "⚠️ Microsoft Office 未安装（可选）",
        }


def check_path_safety() -> dict:
    """检查路径安全性"""
    desktop = Path.home() / "Desktop"
    ok = desktop.exists()
    return {
        "ok": ok,
        "desktop": str(desktop),
        "message": f"✅ 桌面路径可访问" if ok else "❌ 桌面路径不可访问",
    }


def check_write_permission() -> dict:
    """检查写入权限"""
    desktop = Path.home() / "Desktop"
    test_file = desktop / ".wps_test_write"

    try:
        test_file.write_text("test", encoding="utf-8")
        test_file.unlink()
        return {"ok": True, "message": "✅ 桌面写入权限正常"}
    except Exception as e:
        return {
            "ok": False,
            "message": f"❌ 桌面写入失败: {e}",
            "hint": "检查用户权限或磁盘空间",
        }


def run_all_checks() -> dict:
    """运行所有检查"""
    checks = []

    # 基础检查
    checks.append({"name": "Python 版本", **check_python_version()})
    checks.append({"name": "操作系统", **check_platform()})
    checks.append({"name": "路径安全", **check_path_safety()})
    checks.append({"name": "写入权限", **check_write_permission()})

    # 依赖检查
    checks.append({"name": "pywin32（COM）", **check_pywin32()})
    checks.append({"name": "python-docx", **check_python_docx()})
    checks.append({"name": "openpyxl", **check_openpyxl()})
    checks.append({"name": "python-pptx", **check_python_pptx()})

    # 办公套件检查
    wps_check = check_wps()
    checks.append({"name": "WPS Office", **wps_check})
    if not wps_check.get("ok"):
        checks.append({"name": "MS Office", **check_ms_office()})

    # 汇总
    errors = [c for c in checks if c.get("ok") is False]
    warnings = [c for c in checks if c.get("ok") is None and not c.get("skipped")]

    if errors:
        overall = "fail"
        summary = f"❌ {len(errors)} 个问题需要解决"
    elif warnings:
        overall = "warn"
        summary = f"⚠️ {len(warnings)} 个警告"
    else:
        overall = "pass"
        summary = "✅ 所有检查通过，可以正常使用"

    return {
        "ok": overall != "fail",
        "overall": overall,
        "summary": summary,
        "checks": checks,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="WPS 环境自检")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    args = parser.parse_args()

    result = run_all_checks()

    if args.json:
        print(json.dumps(result, ensure_ascii=False, default=str))
    else:
        print("=" * 50)
        print("WPS Office 全家桶 - 环境自检报告")
        print("=" * 50)
        print()
        for check in result["checks"]:
            msg = check.get("message", "")
            name = check.get("name", "")
            if not msg:
                continue
            skip = check.get("skipped", False)
            if skip:
                continue
            print(f"  {name}: {msg}")
            if not check.get("ok") and check.get("hint"):
                print(f"    → {check['hint']}")
        print()
        print("-" * 50)
        print(f"总结: {result['summary']}")
        print(f"时间: {result['timestamp']}")
        print("=" * 50)


if __name__ == "__main__":
    main()
