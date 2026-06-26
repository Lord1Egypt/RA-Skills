#!/usr/bin/env python3
"""
core/security.py — HMAC签名机制
"""

import os
import json
import hashlib
import hmac as _hmac_mod

from .constants import HMAC_SECRET, _VALID_GATE_SOURCES
from .utils import _read_json, _write_json

# V3.5.2: 全局变量记录当前执行的action，只在main()的dispatch时设置
_CURRENT_ACTION = ""


def _get_hmac_key():
    """V4.0.1: 使用固定HMAC_SECRET常量派生密钥。
    不再依赖文件内容哈希，拆分/修改文件后旧任务仍可resume。
    """
    return HMAC_SECRET.encode("utf-8")


def _get_legacy_hmac_key():
    """V4.0.1兼容: 旧版基于文件哈希的密钥，用于验签兼容。"""
    # 使用原始orchestrator.py路径（拆分后仍指向主入口）
    orch_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "orchestrator.py")
    if not os.path.exists(orch_path):
        orch_path = os.path.abspath(__file__)
    with open(orch_path, "rb") as f:
        file_hash = hashlib.sha256(f.read()).hexdigest()
    return f"orch-gate-{file_hash[:32]}".encode("utf-8")


def _sign_gate(gate_data, task_id):
    """V3.2.6: 对gate pass数据生成HMAC签名。"""
    data_copy = {k: v for k, v in gate_data.items() if k != "hmac"}
    data_copy["_task_id"] = task_id
    payload = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
    key = _get_hmac_key()
    sig = _hmac_mod.new(key, payload.encode("utf-8"), hashlib.sha256).hexdigest()
    return sig


def _write_signed_gate(gate_path, gate_data, task_id):
    """V3.5.2: 写入带HMAC签名+来源标记的gate pass文件。"""
    gate_data["source_action"] = _CURRENT_ACTION
    gate_data["hmac"] = _sign_gate(gate_data, task_id)
    _write_json(gate_path, gate_data)


def _verify_gate_hmac(gate_data, task_id):
    """V4.0.1: 验证gate pass的HMAC签名 + 来源合法性。
    返回 (True, "OK") 或 (False, "原因")
    """
    stored_hmac = gate_data.get("hmac")
    if not stored_hmac:
        return False, "gate pass缺少HMAC签名（可能Agent伪造）"
    # 先用新密钥验签
    expected = _sign_gate(gate_data, task_id)
    hmac_ok = _hmac_mod.compare_digest(stored_hmac, expected)
    # V4.0.1: 新密钥失败时，尝试旧密钥（文件哈希）兼容验签
    if not hmac_ok:
        legacy_key = _get_legacy_hmac_key()
        data_copy = {k: v for k, v in gate_data.items() if k != "hmac"}
        data_copy["_task_id"] = task_id
        payload = json.dumps(data_copy, sort_keys=True, ensure_ascii=False)
        legacy_sig = _hmac_mod.new(legacy_key, payload.encode("utf-8"), hashlib.sha256).hexdigest()
        hmac_ok = _hmac_mod.compare_digest(stored_hmac, legacy_sig)
    if not hmac_ok:
        return False, "HMAC签名不匹配（gate pass被篡改或Agent伪造）"
    # V3.5.2: HMAC通过后再校验source_action合法性
    step = gate_data.get("step", "")
    source_action = gate_data.get("source_action", "")
    if step in _VALID_GATE_SOURCES and source_action and source_action not in _VALID_GATE_SOURCES[step]:
        return False, f"{step}的gate来源非法: '{source_action}'（合法来源: {_VALID_GATE_SOURCES[step]}，可能Agent绕过orchestrator伪造）"
    return True, "OK"
