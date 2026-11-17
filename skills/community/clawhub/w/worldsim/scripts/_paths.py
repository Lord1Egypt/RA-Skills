#!/usr/bin/env python3
# _paths.py — 路径推导单一事实源（worlds 根 / 世界目录解析 / 破坏性删除安全网）
# scripts/ 下所有脚本一律经本模块推导路径，禁止各脚本自行推导 worlds 根。
# I/O 纪律（硬性）：stdout/stderr 显式 UTF-8（Windows 缺省 GBK）；路径禁止硬编码。
import os, re, shutil, subprocess, sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        if _s and _s.encoding and _s.encoding.lower().replace("-", "") != "utf8":
            _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# skill 根 = 本文件位置推导（不可被环境变量覆写）
SKILL_DIR = Path(__file__).resolve().parent.parent
SCRIPT_DIR = SKILL_DIR / "scripts"

# 世界指纹文件：破坏性操作前目录内必须存在（防 worlds 根指错时误删无关目录）
WORLD_MARKER = "SETTING.md"


def _die(msg: str):
    print(f"[ERR] {msg}", file=sys.stderr)
    sys.exit(1)


def is_link(p: Path) -> bool:
    """symlink / Windows junction 一律视为链接（删除操作会穿透到链接目标）。"""
    if p.is_symlink():
        return True
    try:
        return bool(os.readlink(p))
    except OSError:
        return False


def validate_name(name: str, kind: str = "名称") -> str:
    """名称校验：禁路径分隔符/穿越/驱动器前缀/UNC/控制字符/首尾空白。"""
    if not name or not name.strip():
        _die(f"空{kind}")
    if "/" in name or "\\" in name or ".." in name:
        _die(f"非法{kind} '{name}'（禁止路径分隔符/../相对路径穿越）")
    if re.match(r"^[A-Za-z]:", name) or name.startswith("\\\\"):
        _die(f"非法{kind} '{name}'（禁止驱动器前缀/UNC 路径）")
    if name != name.strip() or any(ord(c) < 32 for c in name):
        _die(f"非法{kind} '{name}'（禁止首尾空白/控制字符）")
    return name


def worlds_root() -> Path:
    """worlds 根：WORLDSIM_WORLDS_DIR 覆写（空值按未设置处理），缺省 {skill_dir}/worlds。

    拒绝把受保护目录当 worlds 根——文件系统根 / 家目录 / skill 根本身。
    """
    raw = (os.environ.get("WORLDSIM_WORLDS_DIR") or "").strip()
    root = Path(raw) if raw else SKILL_DIR / "worlds"
    try:
        rp = root.resolve()
    except Exception:
        _die(f"worlds 根无法解析: {root}")
    home = Path.home().resolve()
    if rp == Path(rp.anchor) or rp == home or rp == SKILL_DIR:
        _die(f"worlds 根指向受保护目录，拒绝执行: {rp}\n"
             f"请改指向专用目录（例: {home / 'worldsim-worlds'}）")
    return rp


def resolve_world(world: str) -> Path:
    """世界目录：名称校验 → 存在性 → 链接拦截 → realpath 包含校验。"""
    validate_name(world, "世界名")
    root = worlds_root()
    wd = root / world
    if not wd.is_dir():
        _die(f"世界 '{world}' 不存在: {wd}")
    if is_link(wd):
        _die(f"世界目录是链接，拒绝执行: {wd}（symlink/junction 会让删除穿透到链接目标）")
    rp = wd.resolve()
    if rp == root or root not in rp.parents:
        _die(f"世界目录越出 worlds 根: {rp}（根={root}）")
    return wd


def require_world_marker(world_dir: Path) -> None:
    """破坏性操作前的世界指纹校验：目录内必须有 SETTING.md。"""
    if not (world_dir / WORLD_MARKER).is_file():
        _die(f"目录不是 WorldSim 世界（缺 {WORLD_MARKER}），拒绝破坏性操作: {world_dir}")


def resolve_within(base: Path, relative: str, kind: str = "路径") -> Path:
    """base 下相对路径的安全解析（允许含 / 的相对子路径）：拒绝绝对路径/盘符/根引用/穿越/控制字符，
    逐组件拦截 symlink/junction；返回 base 内的拼接路径（不要求存在）。"""
    p = Path(relative)
    if p.is_absolute() or p.drive or p.root:
        _die(f"非法{kind} '{relative}'（禁止绝对路径/盘符/根引用）")
    if any(part == ".." for part in p.parts):
        _die(f"非法{kind} '{relative}'（禁止相对路径穿越）")
    if any(ord(c) < 32 for c in relative):
        _die(f"非法{kind}（禁止控制字符）")
    cur = base
    for part in p.parts:
        cur = cur / part
        if is_link(cur):
            _die(f"{kind}路径含链接组件，拒绝执行: {cur}")
    return cur


def assert_no_links(root: Path) -> None:
    """递归校验目录树内无 symlink/junction（快照等整树搬运前必查——嵌套链接会让读写逃逸出世界目录）。"""
    if not root.is_dir():
        return
    for dp, dn, fn in os.walk(root):
        for name in dn + fn:
            p = Path(dp) / name
            if is_link(p):
                _die(f"目录树内存在链接，拒绝执行: {p}（symlink/junction 会让整树搬运读写逃逸出 {root}）")


def safe_rmtree(path: Path) -> None:
    """删除目录树：顶层为链接时直接拒绝（不依赖解释器行为）。"""
    if is_link(path):
        _die(f"待删除目录是链接，拒绝执行: {path}")
    if not path.is_dir():
        return
    shutil.rmtree(path)


def safe_unlink(path: Path) -> None:
    """删除文件：只删常规文件与链接，拒绝目录。"""
    if path.is_dir() and not path.is_symlink():
        _die(f"待删除路径是目录，请用 safe_rmtree: {path}")
    if path.exists() or path.is_symlink():
        path.unlink()


def snapshot_or_abort(world: str, snapname: str, timeout: int = 120) -> None:
    """破坏性操作前置安全网：存档快照，失败即中止（fail-closed）。

    快照是破坏性操作唯一的回滚锚点——创建失败仍继续执行 = 不可恢复的数据丢失，
    且对用户承诺的「自动存档可回滚」不成立。故无法执行 / 超时 / 非 0 退出
    （含残破快照目录）一律中止。
    """
    try:
        p = subprocess.run(
            [sys.executable, str(SCRIPT_DIR / "snap.py"), world, "save", snapname],
            capture_output=True, timeout=timeout,
        )
    except Exception as e:
        _die(f"安全存档无法执行（{e}），已中止破坏性操作——快照名: {snapname}")
    print((p.stdout or b"").decode("utf-8", "replace") + (p.stderr or b"").decode("utf-8", "replace"), end="")
    if p.returncode != 0:
        _die(f"安全存档失败（exit {p.returncode}），已中止破坏性操作——快照名: {snapname}")
