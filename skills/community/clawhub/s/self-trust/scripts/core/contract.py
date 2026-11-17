# -*- coding: utf-8 -*-
"""契约读写 + 数据目录解析 + 三区权限强制（设计文档 §2 / §8.3 #6 / §10.3 / §5.4）。

数据目录解析优先级（写进 README，规范 #6）：
    命令行 --data-dir  >  环境变量 SELFTRUST_DATA_DIR  >  默认 <home>/.claw/self-trust
默认落点锚定规范 §3 平台基址（Path.home()），不依赖运行时 cwd——契约+审计是
财务账本（§10.1），必须在 skill 目录外（删 skill 不毁账本）、在 .claw 备份树内
（MA-2 覆盖）；代码零个人绝对路径硬编码（假设开源，跨机可重放）。

三区权限强制（公正性地基，test_contract_guard 最高优先）：
- actor="engine"：只允许改运行态区字段；触碰配置区 → PermissionError（显式报错不吞）。
- actor="configurator"：可改配置区，但核心护栏字段（§5.4）必须 confirm=True
  （模拟二次确认闸门），否则 GuardError。
- 审计区字段禁止写入 contract.json（物理分离，走 core.audit）。
"""
from __future__ import annotations

import json
import os
import threading
import uuid
from pathlib import Path
from typing import Any, Optional

from . import crypto as crypto_io
from .models import Contract, FIELD_ZONES, CORE_GUARD_FIELDS, Zone, ObjectiveStatus

ENV_DATA_DIR = "SELFTRUST_DATA_DIR"
CONTRACT_FILENAME = "contract.json"


class GuardError(PermissionError):
    """三区权限 / §5.4 闸门违规（显式抛出，不吞错）。"""


class ContractCorruptedError(Exception):
    """契约文件损坏（拼接/截断 JSON 或加密体损坏）。

    由 read_contract 读时守卫、write_contract 写前校验抛出；明确指向
    contract.json.bak.corrupt 恢复路径，绝不裸抛 JSONDecodeError / 静默重写。
    这是「写盘 bug 可能复现」的护栏：把 'Extra data' 变成可行动的清晰错误。
    """

    def __init__(self, path: Path, cause: Optional[BaseException] = None):
        self.path = Path(path)
        bak = self.path.with_name(self.path.name + ".bak.corrupt")
        msg = (
            f"契约文件损坏：{self.path}\n"
            f"检测到拼接/截断的 JSON（根因：落盘中途被打断或并发抢写）。\n"
            f"请用备份恢复：{bak}\n"
            f"若无备份、请勿重跑命令——按引擎手动修法子处理。"
        )
        if cause is not None:
            msg += f"\n底层错误：{type(cause).__name__}: {cause}"
        super().__init__(msg)


# §10.3 运行态区显式包含「lag_streak / used_annual」等计数器——它们物理上嵌在
# CONFIG 区父字段（objectives / fast_track_whitelist）内。引擎仅允许改动这些
# 运行态子字段；父字段的其余结构（weight / target_amount / caps …）仍然只读。
_ENGINE_SUBFIELD_ALLOW: dict[str, frozenset[str]] = {
    "objectives": frozenset({"lag_streak", "reward_unlocked", "reward_quota", "status"}),
    "fast_track_whitelist": frozenset({"used_annual"}),
}
# 引擎可自动执行的目标状态翻转：仅 active→overdue（超期是确定性事实，§6.4）；
# completed / archived 须用户显式确认（configurator）。
_ENGINE_STATUS_FLIPS = frozenset({(ObjectiveStatus.ACTIVE.value, ObjectiveStatus.OVERDUE.value)})


def _engine_list_change_ok(key: str, old_list: Any, new_list: Any) -> bool:
    """引擎对 CONFIG 区列表字段的改动是否仅限运行态子字段（§10.3）。"""
    if not isinstance(old_list, list) or not isinstance(new_list, list):
        return False
    if len(old_list) != len(new_list):
        return False  # 引擎不得增删条目（结构改动属配置区）
    allowed = _ENGINE_SUBFIELD_ALLOW[key]
    for o, n in zip(old_list, new_list):
        if not isinstance(o, dict) or not isinstance(n, dict):
            return False
        for k in set(o) | set(n):
            if o.get(k) == n.get(k):
                continue
            if k not in allowed:
                return False
            if key == "objectives" and k == "status":
                src = o.get(k) or ObjectiveStatus.ACTIVE.value
                if (src, n.get(k)) not in _ENGINE_STATUS_FLIPS:
                    return False
    return True


def resolve_data_dir(cli_data_dir: Optional[str] = None) -> Path:
    """解析数据目录：命令行 > env > 默认 <home>/.claw/self-trust（规范 §3 平台基址）。"""
    if cli_data_dir:
        return Path(cli_data_dir).expanduser()
    env = os.environ.get(ENV_DATA_DIR)
    if env:
        return Path(env).expanduser()
    return Path.home() / ".claw" / "self-trust"


def contract_path(data_dir: Path) -> Path:
    return Path(data_dir) / CONTRACT_FILENAME


def contract_exists(data_dir: Path) -> bool:
    return contract_path(data_dir).is_file()


def _tmp_is_valid(tmp: Path) -> bool:
    """回读校验刚写的 tmp：明文 json.loads / 加密 unseal_json，成功才算有效。

    用于写前守卫——仅当 tmp 校验通过才 os.replace 到正式契约，绝不拿坏文件
    替换好文件。校验失败（瞬态写花）由 write_contract 触发重试。
    """
    try:
        raw = tmp.read_bytes()
    except OSError:
        return False
    try:
        if crypto_io.is_encrypted(raw):
            crypto_io.unseal_json(raw)
        else:
            json.loads(raw.decode("utf-8"))
        return True
    except (json.JSONDecodeError, UnicodeDecodeError, crypto_io.CryptoError):
        return False


def read_contract(data_dir: Path) -> dict[str, Any]:
    """读契约；不存在则 FileNotFoundError（显式，不返回空契约假装存在）。

    透明解密：文件为加密格式（crypto.is_encrypted）→ 用 session 密钥材料解密；
    否则明文 json.loads（向后兼容旧契约）。加密契约但 session 未设密钥 → CryptoError。
    读时守卫：明文契约若检测到拼接/截断 JSON（'Extra data' 类）→ 抛
    ContractCorruptedError 并指向 .bak.corrupt 恢复，绝不裸抛 JSONDecodeError。
    """
    path = contract_path(data_dir)
    if not path.is_file():
        raise FileNotFoundError(f"契约不存在: {path}（请先运行 init）")
    raw = path.read_bytes()
    if crypto_io.is_encrypted(raw):
        return crypto_io.unseal_json(raw)
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as e:
        raise ContractCorruptedError(path, e) from e


def _validate_zones(new: dict[str, Any], old: Optional[dict[str, Any]],
                    actor: str, confirm: bool) -> None:
    for key, value in new.items():
        zone = FIELD_ZONES.get(key)
        if zone is None:
            raise GuardError(f"未知契约字段（schema 外禁止写入）: {key}")
        if zone is Zone.AUDIT:
            raise GuardError(
                f"审计区字段 {key} 禁止写入 contract.json（物理分离，走 core.audit）")
        changed = old is None or old.get(key) != value
        if not changed:
            continue
        if zone is Zone.CONFIG:
            if actor != "configurator":
                # 例外：objectives / fast_track_whitelist 内嵌的运行态计数器
                # （lag_streak / reward_* / used_annual / active→overdue）引擎可写
                if (key in _ENGINE_SUBFIELD_ALLOW and old is not None
                        and _engine_list_change_ok(key, old.get(key), value)):
                    continue
                raise GuardError(
                    f"引擎无权修改配置区字段: {key}（§10.3 最小权限）")
            if key in CORE_GUARD_FIELDS and not confirm:
                raise GuardError(
                    f"核心护栏字段 {key} 修改须经 §5.4 二次确认（confirm=True）")


def write_contract(
    data_dir: Path,
    contract: dict[str, Any],
    *,
    actor: str,
    confirm: bool = False,
    allow_create: bool = False,
) -> Path:
    """写契约（整文件原子替换），写前强制三区权限校验 + 写前回读守卫。

    actor: "engine"（运行态区可写）| "configurator"（配置区可写，护栏字段须 confirm）
    allow_create: 仅初始化/重置路径可 True；常规写要求契约已存在。

    写前守卫（防「写盘 bug 复现」）：
    - 旧契约读取走 read_contract（自动解密；明文损坏在此抛 ContractCorruptedError）。
    - 写入用 pid+tid+uuid 唯一临时名；tmp 回读校验通过才 os.replace 正式契约。
    - 校验失败瞬态重试（最多 3 次）；全部失败则抛 ContractCorruptedError，
      **原契约完好保留**，绝不拿坏文件替换好文件。
    """
    if actor not in ("engine", "configurator"):
        raise GuardError(f"未知 actor: {actor!r}")
    data_dir = Path(data_dir)
    path = contract_path(data_dir)
    old: Optional[dict[str, Any]] = None
    if path.is_file():
        # 旧契约读取走 read_contract（自动解密加密契约；明文损坏在此抛守卫错误）
        old = read_contract(data_dir)
    elif not allow_create:
        raise FileNotFoundError(f"契约不存在: {path}（请先运行 init）")

    if old is None and actor != "configurator":
        raise GuardError("契约创建（初始化/重置）仅配置者可执行")

    _validate_zones(contract, old, actor, confirm)

    data_dir.mkdir(parents=True, exist_ok=True)
    encrypted = bool(contract.get("crypto", {}).get("enabled"))
    if encrypted and not crypto_io.have_session():
        raise crypto_io.CryptoError(
            "契约已启用加密，写入需密钥材料：--pass / --key-file 或对应环境变量")

    # 写前守卫：唯一临时名写入 → 回读校验 → 通过才替换；失败瞬态重试，绝不留残缺
    last_err: Optional[BaseException] = None
    valid_tmp: Optional[Path] = None
    for _attempt in range(3):
        tmp = path.with_name(
            f"{path.stem}.{os.getpid()}.{threading.get_ident()}.{uuid.uuid4().hex[:8]}.tmp")
        try:
            if encrypted:
                blob = crypto_io.seal_json(contract)
                with open(tmp, "wb") as f:
                    f.write(blob)
            else:
                # 透明加密：契约 crypto.enabled → 用 session 密钥材料密封为字节；否则明文 JSON
                # 注：旧契约读取须走 read_contract（自动解密），不可明文 json.load，否则加密契约
                # 二次写入时读旧值会触发 utf-8 解码错误。
                with open(tmp, "w", encoding="utf-8") as f:
                    json.dump(contract, f, ensure_ascii=False, indent=2)
            if _tmp_is_valid(tmp):
                valid_tmp = tmp
                break
            last_err = ValueError("tmp 回读校验失败（内容无效）")
        except (OSError, json.JSONDecodeError, crypto_io.CryptoError) as e:
            last_err = e
        # 本轮 tmp 无效或写失败：清理，下一轮重抽唯一名重来
        try:
            tmp.unlink(missing_ok=True)
        except OSError:
            pass
    if valid_tmp is None:
        # 三次均失败：绝不拿坏文件替换好文件——原契约完好保留，交由用户按法子修
        raise ContractCorruptedError(path, last_err)
    # 校验通过的 tmp 原子替换正式契约；replace 失败清理 tmp 并上抛
    try:
        os.replace(valid_tmp, path)
    except BaseException:
        try:
            valid_tmp.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return path


def new_default_contract() -> dict[str, Any]:
    """balanced 默认契约骨架（§7.1 固化默认值来源）。"""
    return Contract().to_dict()
