#!/usr/bin/env python3
"""
screen-off — macOS 显示器开关 CLI。

通过 CoreGraphics/SkyLight 私有 API 控制任意显示器的开关状态。
不需要 root，不需要辅助功能权限。

用法:
    screen-off --status              列出所有显示器
    screen-off --off <ID>            关闭指定显示器
    screen-off --on <ID>             开启指定显示器
    screen-off --off main            关闭主显示器
    screen-off --off 2 --permanent   重启后保留
    screen-off --off 2 --force       强制关闭（即使它是唯一亮着的）
"""

from __future__ import annotations

import argparse
import ctypes
import sys
import time

# ---------------------------------------------------------------- 绑定

_CG_PATH = "/System/Library/Frameworks/CoreGraphics.framework/CoreGraphics"
_SL_PATH = "/System/Library/PrivateFrameworks/SkyLight.framework/SkyLight"

_REQUIRED = ("CGSGetDisplayList", "CGSBeginDisplayConfiguration",
             "CGSConfigureDisplayEnabled", "CGSCompleteDisplayConfiguration")


def _load() -> ctypes.CDLL:
    missing: list[str] = []
    for path in (_SL_PATH, _CG_PATH):
        try:
            lib = ctypes.CDLL(path)
        except OSError:
            continue
        missing = [s for s in _REQUIRED if not hasattr(lib, s)]
        if not missing:
            return lib
    raise SystemExit(
        "找不到需要的私有符号 (%s) —— 这个系统版本可能挪走或删掉了它们。"
        % ", ".join(missing or _REQUIRED)
    )


_lib = _load()

CGDirectDisplayID = ctypes.c_uint32
CGDisplayConfigRef = ctypes.c_void_p
CGError = ctypes.c_int32

_lib.CGSGetDisplayList.argtypes = [
    ctypes.c_uint32,
    ctypes.POINTER(CGDirectDisplayID),
    ctypes.POINTER(ctypes.c_uint32),
]
_lib.CGSGetDisplayList.restype = CGError

for _name in ("CGDisplayIsBuiltin", "CGDisplayIsActive", "CGDisplayIsAsleep",
              "CGDisplayIsOnline", "CGDisplayIsMain", "CGDisplayPixelsWide",
              "CGDisplayPixelsHigh", "CGDisplayUnitNumber",
              "CGDisplayVendorNumber", "CGDisplayModelNumber"):
    _fn = getattr(_lib, _name)
    _fn.argtypes = [CGDirectDisplayID]
    _fn.restype = ctypes.c_uint32

_lib.CGCancelDisplayConfiguration.argtypes = [CGDisplayConfigRef]
_lib.CGCancelDisplayConfiguration.restype = CGError

_lib.CGSBeginDisplayConfiguration.argtypes = [ctypes.POINTER(CGDisplayConfigRef)]
_lib.CGSBeginDisplayConfiguration.restype = CGError

_lib.CGSConfigureDisplayEnabled.argtypes = [
    CGDisplayConfigRef, CGDirectDisplayID, ctypes.c_bool,
]
_lib.CGSConfigureDisplayEnabled.restype = CGError

_lib.CGSCompleteDisplayConfiguration.argtypes = [CGDisplayConfigRef, ctypes.c_uint32]
_lib.CGSCompleteDisplayConfiguration.restype = CGError

CONFIGURE_FOR_APP_ONLY = 0
CONFIGURE_FOR_SESSION = 1
CONFIGURE_PERMANENTLY = 2

_CG_ERRORS = {
    0: "success",
    1000: "kCGErrorFailure",
    1001: "kCGErrorIllegalArgument",
    1002: "kCGErrorInvalidConnection",
    1003: "kCGErrorInvalidContext",
    1004: "kCGErrorCannotComplete",
    1007: "kCGErrorNotImplemented",
    1008: "kCGErrorRangeCheck",
    1009: "kCGErrorTypeCheck",
    1010: "kCGErrorNoneAvailable",
    1011: "kCGErrorInvalidOperation",
}


def _err(code: int) -> str:
    return _CG_ERRORS.get(code, f"CGError {code}")


# ---------------------------------------------------------------- 显示器

class Display:
    VIRTUAL_VENDOR = 0x756E6B6E  # "unkn"
    VIRTUAL_MODEL = 0x76697274   # "virt"

    def __init__(self, did: int):
        self.id = did
        self.builtin = bool(_lib.CGDisplayIsBuiltin(did))
        self.active = bool(_lib.CGDisplayIsActive(did))
        self.online = bool(_lib.CGDisplayIsOnline(did))
        self.asleep = bool(_lib.CGDisplayIsAsleep(did))
        self.main = bool(_lib.CGDisplayIsMain(did))
        self.width = _lib.CGDisplayPixelsWide(did)
        self.height = _lib.CGDisplayPixelsHigh(did)
        self.unit = _lib.CGDisplayUnitNumber(did)
        self.vendor = _lib.CGDisplayVendorNumber(did)
        self.model = _lib.CGDisplayModelNumber(did)

    @property
    def is_virtual(self) -> bool:
        return (not self.builtin
                and self.vendor == self.VIRTUAL_VENDOR
                and self.model == self.VIRTUAL_MODEL)

    @property
    def phantom(self) -> bool:
        return not self.builtin and not self.online and self.width <= 1

    @property
    def lit(self) -> bool:
        return self.active and not self.asleep and not self.is_virtual

    @property
    def state(self) -> str:
        if self.is_virtual:
            return "virtual"
        if self.asleep:
            return "asleep"
        if self.active:
            return "active"
        return "disabled" if not self.online else "inactive"

    @property
    def tags(self) -> list[str]:
        t = []
        if self.main:
            t.append("main")
        if self.builtin:
            t.append("builtin")
        return t

    def name(self, names: dict[int, str]) -> str:
        if self.id in names:
            return names[self.id]
        return "Built-in Display" if self.builtin else f"Display {self.id}"

    def line(self, names: dict[int, str], idx: int) -> str:
        tags = self.tags
        tag = f" [{', '.join(tags)}]" if tags else ""
        size = f"{self.width}x{self.height}"
        return f"  #{idx:<3} ID={self.id:<6} {self.name(names):<24} {size:<12} {self.state:<9}{tag}"


def _screen_names() -> dict[int, str]:
    try:
        from AppKit import NSScreen  # type: ignore
    except Exception:
        return {}
    out: dict[int, str] = {}
    try:
        for scr in NSScreen.screens():
            num = scr.deviceDescription().get("NSScreenNumber")
            if num is not None:
                out[int(num)] = str(scr.localizedName())
    except Exception:
        pass
    return out


def all_displays() -> list[Display]:
    """全部显示器槽位，含被禁用和空槽。按 active > disabled > 空槽 排序。"""
    buf = (CGDirectDisplayID * 32)()
    count = ctypes.c_uint32(0)
    rc = _lib.CGSGetDisplayList(32, buf, ctypes.byref(count))
    if rc != 0:
        raise SystemExit(f"CGSGetDisplayList 失败: {_err(rc)}")
    displays = [Display(buf[i]) for i in range(count.value)]
    # 过滤掉真正空的槽位（vendor+model 都是 0 的）
    displays = [d for d in displays if not (d.vendor == 0 and d.model == 0)]
    # 排序：亮着的在前，禁用的在后
    displays.sort(key=lambda d: (not d.active, not d.online, d.id))
    return displays


# ---------------------------------------------------------------- 核心动作

def set_enabled(display_id: int, enabled: bool,
                option: int = CONFIGURE_FOR_SESSION) -> None:
    config = CGDisplayConfigRef()
    rc = _lib.CGSBeginDisplayConfiguration(ctypes.byref(config))
    if rc != 0:
        raise SystemExit(f"CGSBeginDisplayConfiguration 失败: {_err(rc)}")

    rc = _lib.CGSConfigureDisplayEnabled(config, display_id, enabled)
    if rc != 0:
        _lib.CGCancelDisplayConfiguration(config)
        raise SystemExit(f"CGSConfigureDisplayEnabled 失败: {_err(rc)}")

    rc = _lib.CGSCompleteDisplayConfiguration(config, option)
    if rc != 0 and not _wait_for(display_id, enabled, timeout=2.0):
        raise SystemExit(f"CGSCompleteDisplayConfiguration 失败: {_err(rc)}")


def _wait_for(display_id: int, want_active: bool, timeout: float = 5.0) -> bool:
    deadline = time.monotonic() + timeout
    while True:
        if bool(_lib.CGDisplayIsActive(display_id)) == want_active:
            return True
        if time.monotonic() >= deadline:
            return False
        time.sleep(0.1)


# ---------------------------------------------------------------- 解析目标

def resolve_target(target: str, displays: list[Display],
                   names: dict[int, str]) -> Display | None:
    """解析用户输入的目标屏幕。

    支持:
      - ID:    "2", "3" (纯数字 = 按 ID 匹配，优先)
      - 序号:  "#1", "#2" (# 前缀 = 按列表顺序)
      - 名字:  "main", "builtin"
      - 部分匹配: "S2700", "Display"
    """
    t = target.strip().lower()

    # "main" → 主屏
    if t == "main":
        return next((d for d in displays if d.main), None)

    # "builtin" → 内建屏
    if t in ("builtin", "built-in", "internal"):
        return next((d for d in displays if d.builtin), None)

    # "id:N" → 按 ID
    if t.startswith("id:"):
        try:
            did = int(t[3:])
            return next((d for d in displays if d.id == did), None)
        except ValueError:
            return None

    # "#N" → 按序号 (1-based)
    if t.startswith("#"):
        try:
            idx = int(t[1:])
            if 1 <= idx <= len(displays):
                return displays[idx - 1]
            return None
        except ValueError:
            return None

    # 纯数字 → 按 ID 匹配（ID 是稳定的，序号会随开关变化）
    if t.isdigit():
        did = int(t)
        return next((d for d in displays if d.id == did), None)

    # 名字匹配（部分匹配，大小写不敏感）
    for d in displays:
        dname = d.name(names).lower()
        if t in dname:
            return d

    return None


# ---------------------------------------------------------------- CLI

def cmd_status(displays: list[Display], names: dict[int, str]) -> int:
    print(f"显示器 {len(displays)} 台:")
    for i, d in enumerate(displays, 1):
        print(d.line(names, i))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="screen-off",
        description="macOS 显示器开关 — 通过 ID/序号/名字 指定目标屏幕",
    )
    g = p.add_mutually_exclusive_group()
    g.add_argument("--on", metavar="TARGET", help="开启指定显示器 (序号/ID/main/builtin)")
    g.add_argument("--off", metavar="TARGET", help="关闭指定显示器")
    g.add_argument("--status", action="store_true", help="列出所有显示器")
    p.add_argument("--permanent", action="store_true",
                   help="用 kCGConfigurePermanently，重启后保留")
    p.add_argument("--force", action="store_true",
                   help="即使目标是唯一亮着的屏也允许关闭（会黑屏）")
    p.add_argument("-q", "--quiet", action="store_true", help="少输出")
    args = p.parse_args(argv)

    displays = all_displays()
    names = _screen_names()

    if args.status:
        return cmd_status(displays, names)

    if not args.on and not args.off:
        # 默认行为：toggle 所有屏里唯一有 builtin 的，兼容旧行为
        # 但如果没 builtin，就打印 status 提示用户指定目标
        builtin = next((d for d in displays if d.builtin), None)
        if builtin:
            # toggle 内建屏
            want_enabled = not builtin.active
            others_lit = [d for d in displays if not d.builtin and d.lit]
            if not want_enabled and not others_lit and not args.force:
                print("目标是唯一亮着的屏。接上其他屏，或者加 --force。", file=sys.stderr)
                return 2
            option = CONFIGURE_PERMANENTLY if args.permanent else CONFIGURE_FOR_SESSION
            set_enabled(builtin.id, want_enabled, option)
            ok = _wait_for(builtin.id, want_enabled)
            if not args.quiet:
                verb = "打开" if want_enabled else "关闭"
                print(f"已{verb} {builtin.name(names)} (ID={builtin.id})。" if ok
                      else f"配置已提交，但屏幕没在预期时间内{verb}。")
            return 0 if ok else 3
        else:
            print("没有内建显示器。请用 --status 查看屏幕列表，然后用 --off <ID> 指定目标。")
            return cmd_status(displays, names)

    # --on 或 --off 指定了目标
    target = args.on or args.off
    want_enabled = args.on is not None

    d = resolve_target(target, displays, names)
    if d is None:
        print(f"找不到匹配 '{target}' 的显示器。", file=sys.stderr)
        cmd_status(displays, names)
        return 1

    if d.active == want_enabled:
        if not args.quiet:
            print(f"{d.name(names)} (ID={d.id}) 已经是{'开' if want_enabled else '关'}，不动。")
        return 0

    others_lit = [x for x in displays if x.id != d.id and x.lit]
    if not want_enabled and not others_lit and not args.force:
        print(f"{d.name(names)} (ID={d.id}) 是唯一亮着的屏，关掉会黑屏。加 --force 强制。", file=sys.stderr)
        return 2

    option = CONFIGURE_PERMANENTLY if args.permanent else CONFIGURE_FOR_SESSION
    set_enabled(d.id, want_enabled, option)
    ok = _wait_for(d.id, want_enabled)

    if not args.quiet:
        verb = "打开" if want_enabled else "关闭"
        if ok:
            msg = f"已{verb} {d.name(names)} (ID={d.id})。"
            if others_lit:
                msg += " 剩余: " + ", ".join(x.name(names) for x in others_lit)
            print(msg)
        else:
            print(f"配置已提交，但 {d.name(names)} 没在预期时间内{verb}。", file=sys.stderr)
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
