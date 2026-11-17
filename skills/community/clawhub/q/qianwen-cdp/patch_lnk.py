# -*- coding: utf-8 -*-
"""
给千问浏览器快捷方式(.lnk)注入 CDP 调试端口参数。
直接解析/改写 LNK 二进制(绕过 WScript.Shell COM, 不受 PowerShell 安全策略影响)。
用法:
  python patch_lnk.py --dry            # 只打印, 不修改
  python patch_lnk.py --apply          # 实际注入(幂等: 已含端口则跳过)
  python patch_lnk.py --unapply        # 移除已注入的调试端口参数(幂等)
"""
import struct
import sys
import os

PORT_ARG = "--remote-debugging-port=9666"

# 4 个千问快捷方式(开始菜单/桌面/任务栏/QuickLaunch)
LNK_PATHS = [
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs\千问.lnk"),
    os.path.expandvars(r"%USERPROFILE%\Desktop\常用软件\千问.lnk"),
    os.path.expandvars(r"%APPDATA%\Microsoft\Internet Explorer\Quick Launch\User Pinned\TaskBar\千问.lnk"),
    os.path.expandvars(r"%APPDATA%\Microsoft\Internet Explorer\Quick Launch\千问.lnk"),
]


def locate_args(data):
    """正确解析 LNK: 跳过 Header(76) + IDList(含size字段) + LinkInfo, 返回 ARGS 段 (start,end,text)。"""
    flags = struct.unpack("<I", data[20:24])[0]
    if not (flags & 0x80):
        return None  # 非 Unicode, 放弃
    off = 76
    idsize = struct.unpack("<H", data[off:off + 2])[0]
    off = 76 + 2 + idsize  # IDList 数据(不含 size 字段本身) + 终止符
    if flags & 0x2:  # HasLinkInfo
        lsize = struct.unpack("<I", data[off:off + 4])[0]
        off += lsize
    order = []
    if flags & 0x4:
        order.append("NAME")
    if flags & 0x8:
        order.append("REL")
    if flags & 0x10:
        order.append("WD")
    if flags & 0x20:
        order.append("ARGS")
    if flags & 0x40:
        order.append("ICON")
    for key in order:
        start = off
        (length,) = struct.unpack("<H", data[off:off + 2])
        text_off = off + 2
        text = data[text_off:text_off + length * 2].decode("utf-16-le", "replace").rstrip("\x00")
        end = text_off + length * 2
        if key == "ARGS":
            return (start, end, text)
        off = end
    return None


def patch_one(path, apply=False, unapply=False):
    if not os.path.exists(path):
        return {"path": path, "status": "MISSING"}
    with open(path, "rb") as f:
        data = bytearray(f.read())

    if data[:4] != b"\x4c\x00\x00\x00":
        return {"path": path, "status": "NOT_LNK"}

    loc = locate_args(data)
    if loc is None:
        return {"path": path, "status": "NO_ARGS_FIELD"}
    a_start, a_end, old_args = loc

    if unapply:
        if PORT_ARG not in old_args:
            return {"path": path, "status": "NO_PORT", "args": old_args}
        new_args = old_args.replace(" " + PORT_ARG, "").replace(PORT_ARG, "").strip()
        new_length = len(new_args) + 1  # 含 null
        new_bytes = struct.pack("<H", new_length) + (new_args + "\x00").encode("utf-16-le")
        info = {"path": path, "old_args": old_args, "new_args": new_args,
                "old_len": a_end - a_start, "new_len": len(new_bytes)}
        if apply:
            new_data = data[:a_start] + new_bytes + data[a_end:]
            with open(path, "wb") as f:
                f.write(new_data)
            info["status"] = "UNPATCHED"
        else:
            info["status"] = "WOULD_UNPATCH"
        return info

    if PORT_ARG in old_args:
        return {"path": path, "status": "ALREADY_HAS_PORT", "args": old_args}

    new_args = (old_args + " " + PORT_ARG).strip()
    new_length = len(new_args) + 1  # 含 null
    new_bytes = struct.pack("<H", new_length) + (new_args + "\x00").encode("utf-16-le")

    info = {"path": path, "old_args": old_args, "new_args": new_args,
            "old_len": a_end - a_start, "new_len": len(new_bytes)}

    if apply:
        new_data = data[:a_start] + new_bytes + data[a_end:]
        with open(path, "wb") as f:
            f.write(new_data)
        info["status"] = "PATCHED"
    else:
        info["status"] = "WOULD_PATCH"
    return info


def main():
    apply = "--apply" in sys.argv
    dry = "--dry" in sys.argv
    unapply = "--unapply" in sys.argv
    if not apply and not dry and not unapply:
        print("用法: python patch_lnk.py --dry | --apply | --unapply")
        return
    for p in LNK_PATHS:
        r = patch_one(p, apply=apply, unapply=unapply)
        if r["status"] in ("PATCHED", "WOULD_PATCH", "UNPATCHED", "WOULD_UNPATCH"):
            print(f"[{r['status']}] {p}")
            print(f"    old: '{r['old_args']}'")
            print(f"    new: '{r['new_args']}'")
        else:
            print(f"[{r['status']}] {p}" + (f"  args={r.get('args')}" if "args" in r else ""))


if __name__ == "__main__":
    main()
