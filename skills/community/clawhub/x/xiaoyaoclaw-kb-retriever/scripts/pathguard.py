#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pathguard.py — 知识库边界的容器校验（读写双向，防符号链接越界）

语言 / Language：注释与报错默认中文；**语言可选**，按用户语言回应即可
（comments default to Chinese; error text can be adapted to the user's language）。

为什么需要它：知识库目录里可能存在**符号链接**（用户自己建的、同步盘建的、
或从压缩包解出来的）。只做字符串层面的校验（`abspath` + `commonpath` /
`startswith`）**看不出链接**：`<kb>/sub -> /etc` 这样的链接会让一个"看起来在
库内"的路径实际指到库外——**写入会写出去、读取会读出去**。本模块是全部脚本
（检索 + 三个维护脚本）共用的唯一闸门，读与写同一套规则。

规则
  1. 先把知识库根解析成**真实路径**（`realpath`，解开沿途所有符号链接）。
  2. **写入目标**解析成真实路径（已存在的部分解链，尚未存在的尾段原样保留）
     —— 必须仍落在库根内部，否则拒绝写入。
  3. **读取目标**同样解析成真实路径 —— 越出库根即拒绝读取（调用方按"跳过并
     计数"处理，不会去 read 库外的文件）。
  4. 目标已是符号链接时同上：解出来的真实路径越界即拒绝（既不跟着链接写，
     也不跟着链接读）。
  5. **源文件（如待处理的 PDF）不走链接**：`require_real_file()` 要求路径任一段都不是
     符号链接 —— 只"解开链接再读"等于跟着链接走到库外，边界形同虚设；因此一律拒绝
     （fail closed），并回显真实位置供调用方改用真实路径。
  6. **fail closed**：任何校验不通过都拒绝，绝不"先做再说"。

不做：不删除任何文件；不跟随链接到库外（既不写、也不在库外建目录、也不读）。
"""

from __future__ import annotations

import os
import sys


class PathEscapeError(RuntimeError):
    """目标路径解析后越出知识库根（通常是符号链接导致的）。读、写均适用。"""


def _norm(path: str) -> str:
    return os.path.normcase(os.path.normpath(path))


def real_root(path: str) -> str:
    """把知识库根解析成真实路径（必须是已存在的目录）。"""
    p = os.path.realpath(os.path.expanduser(str(path)))
    if not os.path.isdir(p):
        raise PathEscapeError(f"知识库根目录不存在或不是目录：{p}")
    return p


def real_target(path: str) -> str:
    """把待写目标解析成真实路径（解掉已存在部分的符号链接）。"""
    return os.path.realpath(os.path.expanduser(str(path)))


def is_within(root_real: str, target_real: str, *, allow_equal: bool = False) -> bool:
    """target 是否在 root 内部（或等于 root，且显式允许）。大小写按平台归一。"""
    r, t = _norm(root_real), _norm(target_real)
    if t == r:
        return allow_equal
    return t.startswith(r.rstrip(os.sep) + os.sep)


def assert_within(root_real: str, target: str, *, what: str = "写入目标") -> str:
    """校验 target（含符号链接解析）必须落在 root_real 内，返回真实路径。"""
    resolved = real_target(target)
    if not is_within(root_real, resolved):
        raise PathEscapeError(
            f"{what}解析后越出知识库根（符号链接或异常路径），已拒绝：{target} -> {resolved}"
        )
    return resolved


def check_or_exit(root: str, target: str, *, what: str = "写入目标") -> str:
    """CLI 入口用：校验失败即打印错误并以退出码 2 结束（fail closed）。"""
    try:
        return assert_within(real_root(root), target, what=what)
    except PathEscapeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)


def read_within(root_real: str, target: str, *, what: str = "读取目标") -> str:
    """校验读取目标（含符号链接解析）必须落在 root_real 内，返回可安全读取的真实路径。

    越界即抛 PathEscapeError —— 调用方应**跳过该条目并计数**，而不是去读它。
    """
    resolved = real_target(target)
    if not is_within(root_real, resolved):
        raise PathEscapeError(
            f"{what}解析后越出知识库根（符号链接或异常路径），已拒绝读取：{target} -> {resolved}"
        )
    return resolved


def is_symlink(path: str) -> bool:
    """目标本身是否为符号链接（用于显式披露/拒绝）。"""
    return os.path.islink(os.path.expanduser(str(path)))


def require_real_file(path: str, *, what: str = "源文件") -> str:
    """校验目标是**真实路径**上的普通文件：路径中任一段是符号链接即拒绝。

    为什么读侧也要这条：如果只把符号链接解成真实路径再去读，等于"跟着链接走到库外"，
    边界就形同虚设。这里选择 **fail closed**：源文件必须是真实路径（不含符号链接），
    否则拒绝并回显真实位置，让调用方改用真实路径。
    """
    given = os.path.abspath(os.path.expanduser(str(path)))
    if os.path.islink(given):
        raise PathEscapeError(
            f"{what}是符号链接，已拒绝（可能指向知识库之外）：{given} -> {os.path.realpath(given)}"
        )
    if not os.path.isfile(given):
        raise PathEscapeError(f"{what}不存在或不是文件：{given}")
    real = os.path.realpath(given)
    if _norm(real) != _norm(given):
        raise PathEscapeError(
            f"{what}的路径中包含符号链接，已拒绝（可能指向知识库之外）：{given} -> {real}"
        )
    return real
