#!/usr/bin/env python3
"""
storage-clean: File cleaner
Executes clean operations (recycle or permanent delete).
Called from the HTML report via local server or direct Python invocation.
"""

import os
import sys
import json
import shutil
import argparse
import ctypes


# ============================================================
#  Recycle Bin via ctypes (Windows) — single authoritative impl
# ============================================================

def move_to_recycle_bin_ctypes(path):
    """Use ctypes to call SHFileOperationW to move file to Recycle Bin."""
    class SHFILEOPSTRUCT(ctypes.Structure):
        _fields_ = [
            ("hwnd", ctypes.c_void_p),
            ("wFunc", ctypes.c_uint),
            ("pFrom", ctypes.c_wchar_p),
            ("pTo", ctypes.c_wchar_p),
            ("fFlags", ctypes.c_ushort),
            ("fAnyOperationsAborted", ctypes.c_bool),
            ("hNameMappings", ctypes.c_void_p),
            ("lpszProgressTitle", ctypes.c_wchar_p),
        ]

    FO_DELETE = 0x0003
    FOF_ALLOWUNDO = 0x0040
    FOF_NOCONFIRMATION = 0x0010
    FOF_SILENT = 0x1000

    path_abs = os.path.abspath(path)
    # Double null-terminated string required by SHFileOperationW
    pFrom = path_abs + "\0"

    fileop = SHFILEOPSTRUCT()
    fileop.hwnd = None
    fileop.wFunc = FO_DELETE
    fileop.pFrom = pFrom
    fileop.pTo = None
    fileop.fFlags = FOF_ALLOWUNDO | FOF_NOCONFIRMATION | FOF_SILENT
    fileop.fAnyOperationsAborted = False
    fileop.hNameMappings = None
    fileop.lpszProgressTitle = None

    shell32 = ctypes.windll.shell32
    result = shell32.SHFileOperationW(ctypes.byref(fileop))

    if result == 0 and not fileop.fAnyOperationsAborted:
        return True, f"已移到废纸篓: {path_abs}"
    else:
        return False, f"SHFileOperation 失败，错误码: {result}"


def send_to_recycle_bin(path):
    """
    Send file/folder to Windows Recycle Bin.
    Single implementation using ctypes.
    Returns (success: bool, message: str).
    """
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return False, f"路径不存在: {path}"
    return move_to_recycle_bin_ctypes(path)


def permanent_delete(path):
    """
    Permanently delete file/folder (bypass Recycle Bin).
    Returns (success: bool, message: str).
    """
    path = os.path.abspath(path)
    if not os.path.exists(path):
        return False, f"路径不存在: {path}"

    try:
        if os.path.isfile(path):
            os.remove(path)
            return True, f"已永久删除文件: {path}"
        elif os.path.isdir(path):
            shutil.rmtree(path)
            return True, f"已永久删除文件夹: {path}"
        else:
            return False, f"未知文件类型: {path}"
    except PermissionError as e:
        return False, f"权限不足，无法删除: {e}"
    except Exception as e:
        return False, f"删除失败: {e}"


def clean_item(path, method="recycle"):
    """
    Clean a single item.
    method: "recycle" (移到废纸篓) or "delete" (直接删除)
    Returns (success: bool, message: str).
    """
    if method == "recycle":
        return send_to_recycle_bin(path)
    elif method == "delete":
        return permanent_delete(path)
    else:
        return False, f"未知的清理方法: {method}"


def clean_all_green(json_file):
    """
    Clean all green items from a scan result JSON file.
    Returns dict with results.
    """
    if not os.path.exists(json_file):
        return {"success": False, "message": "JSON 文件不存在"}

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    green_items = data.get("green", [])
    results = []

    for item in green_items:
        path = item.get("path")
        if not path or not os.path.exists(path):
            results.append({"path": path, "success": False, "message": "路径不存在"})
            continue

        success, message = send_to_recycle_bin(path)
        results.append({"path": path, "success": success, "message": message})

    cleaned = sum(1 for r in results if r["success"])
    return {
        "success": True,
        "total": len(results),
        "cleaned": cleaned,
        "results": results,
    }


def main():
    parser = argparse.ArgumentParser(description="storage-clean: File cleaner")
    parser.add_argument("--path", help="Path to clean")
    parser.add_argument("--method", choices=["recycle", "delete"], default="recycle", help="Clean method")
    parser.add_argument("--json", help="JSON file with scan results (for clean-all)")
    parser.add_argument("--clean-all", action="store_true", help="Clean all green items from JSON file")

    args = parser.parse_args()

    if args.clean_all and args.json:
        result = clean_all_green(args.json)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.path:
        success, message = clean_item(args.path, args.method)
        result = {"success": success, "message": message}
        print(json.dumps(result, ensure_ascii=False))
    else:
        print(json.dumps({"success": False, "message": "请提供 --path 或 --clean-all --json"}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
