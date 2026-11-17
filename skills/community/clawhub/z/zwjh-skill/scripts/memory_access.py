# -*- coding: utf-8 -*-
"""
记忆访问权限分级 —— 命名空间隔离 + HMAC-SHA256 manifest。

调用方（MCP tool / 跨 skill）在请求时提交 manifest，声明要访问的命名空间和读写权限；
服务端校验签名和权限，未声明的命名空间默认只读 public/*。

权限模型：
  - 命名空间：public（公共）/ private/<skill-id>（技能私有）/ shared/<name>（共享）
  - 权限：read（读）/ write（写）/ admin（删除/管理）
  - 未声明 → 默认只读 public/*（兼容旧调用方）

签名算法：HMAC-SHA256
  - 签名内容：namespace + permissions + timestamp + nonce
  - 密钥：从 config.load_config()["access_key"] 读取，未配置时自动生成（首次运行）

纯标准库实现，零外部依赖。
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import secrets
import time
from datetime import datetime
from typing import Any

from . import config

# ── 权限常量 ─────────────────────────────────────────────────────────────
PERM_READ = "read"
PERM_WRITE = "write"
PERM_ADMIN = "admin"

# 权限等级（用于快速比较）
_PERM_LEVEL = {PERM_READ: 1, PERM_WRITE: 2, PERM_ADMIN: 3}

# 默认命名空间
NS_PUBLIC = "public"
NS_PRIVATE_PREFIX = "private/"
NS_SHARED_PREFIX = "shared/"

# manifest 有效期（秒）
MANIFEST_TTL = 300


class AccessDeniedError(Exception):
    """权限不足错误。"""
    pass


class ManifestExpiredError(Exception):
    """manifest 已过期。"""
    pass


class InvalidSignatureError(Exception):
    """签名无效。"""
    pass


# ── 密钥管理 ─────────────────────────────────────────────────────────────
def _get_or_create_key() -> str:
    """获取或创建 HMAC 密钥。"""
    cfg = config.load_config()
    key = cfg.get("access_key")
    if not key:
        key = secrets.token_hex(32)
        cfg["access_key"] = key
        config.save_config(cfg)
    return key


# ── manifest 构建与校验 ─────────────────────────────────────────────────
def create_manifest(namespace: str, permissions: list[str]) -> dict:
    """
    创建 signed manifest（供调用方使用）。

    Args:
        namespace: 命名空间（如 "public" 或 "private/my-skill"）
        permissions: 权限列表（如 ["read", "write"]）

    Returns:
        {namespace, permissions, timestamp, nonce, signature}
    """
    ts = int(time.time())
    nonce = secrets.token_hex(8)
    key = _get_or_create_key()
    sig = _sign(namespace, permissions, ts, nonce, key)
    return {
        "namespace": namespace,
        "permissions": permissions,
        "timestamp": ts,
        "nonce": nonce,
        "signature": sig,
    }


def _sign(namespace: str, permissions: list[str], timestamp: int,
          nonce: str, key: str) -> str:
    """生成 HMAC-SHA256 签名。"""
    payload = "%s|%s|%d|%s" % (
        namespace, ",".join(sorted(permissions)), timestamp, nonce)
    return hmac.new(
        key.encode("utf-8"), payload.encode("utf-8"), hashlib.sha256
    ).hexdigest()


def verify_manifest(manifest: dict, required_perm: str = PERM_READ) -> dict:
    """
    校验 manifest 的签名、有效期和权限。

    Args:
        manifest: create_manifest 返回的 dict
        required_perm: 需要的最低权限（read / write / admin）

    Returns:
        校验通过返回 {"namespace": ..., "permissions": ...}

    Raises:
        AccessDeniedError: 权限不足
        ManifestExpiredError: manifest 已过期
        InvalidSignatureError: 签名无效
        ValueError: manifest 格式错误
    """
    if not isinstance(manifest, dict):
        raise ValueError("manifest 必须是 dict")

    ns = manifest.get("namespace")
    perms = manifest.get("permissions", [])
    ts = manifest.get("timestamp")
    nonce = manifest.get("nonce")
    sig = manifest.get("signature")

    if not ns or not isinstance(perms, list) or ts is None or not nonce or not sig:
        raise ValueError("manifest 缺少必要字段：namespace/permissions/timestamp/nonce/signature")

    # 校验有效期
    now = int(time.time())
    if abs(now - ts) > MANIFEST_TTL:
        raise ManifestExpiredError(
            "manifest 已过期（%d 秒前的请求）。请重新创建 manifest。" % (now - ts))

    # 校验签名
    key = _get_or_create_key()
    expected = _sign(ns, perms, ts, nonce, key)
    if not hmac.compare_digest(sig, expected):
        raise InvalidSignatureError("manifest 签名无效。请确认 access_key 一致。")

    # 校验权限等级
    required_level = _PERM_LEVEL.get(required_perm, 1)
    actual_level = max((_PERM_LEVEL.get(p, 0) for p in perms), default=0)
    if actual_level < required_level:
        raise AccessDeniedError(
            "权限不足：需要 %s，当前 %s" % (required_perm, perms))

    return {"namespace": ns, "permissions": perms}


# ── 便捷函数：默认 public 只读 ───────────────────────────────────────────
def default_public_access() -> dict:
    """返回默认的 public 只读权限信息（向后兼容旧调用方）。"""
    return {"namespace": NS_PUBLIC, "permissions": [PERM_READ]}


def check_namespace_permission(manifest: dict | None, namespace: str,
                               required_perm: str = PERM_READ) -> str:
    """
    检查 manifest 是否对指定命名空间有足够权限。

    未传 manifest 时退化为默认 public 只读（向后兼容）。

    Returns:
        实际有效的命名空间

    Raises:
        AccessDeniedError: 权限不足
    """
    if not manifest:
        # 未传 manifest → 只允许 public 读
        if required_perm != PERM_READ:
            raise AccessDeniedError(
                "未传 manifest，拒绝 %s 请求（仅允许 public 只读）" % required_perm)
        if not _namespace_matches(namespace, NS_PUBLIC):
            raise AccessDeniedError(
                "未传 manifest，拒绝访问非 public 命名空间: %s" % namespace)
        return NS_PUBLIC

    info = verify_manifest(manifest, required_perm)
    allowed_ns = info["namespace"]

    # 检查命名空间匹配
    if not _namespace_matches(namespace, allowed_ns):
        raise AccessDeniedError(
            "命名空间不匹配：请求 %s，允许 %s" % (namespace, allowed_ns))

    return allowed_ns


def _namespace_matches(requested: str, allowed: str) -> bool:
    """检查请求的命名空间是否在允许范围内。"""
    # 完全匹配
    if requested == allowed:
        return True
    # public 命名空间：任何 public/* 匹配
    if allowed == NS_PUBLIC and requested.startswith("public"):
        return True
    # private/<id> 只能匹配自己
    if allowed.startswith(NS_PRIVATE_PREFIX) and requested == allowed:
        return True
    # shared/<name> 匹配 shared/<name>/*
    if allowed.startswith(NS_SHARED_PREFIX) and requested.startswith(allowed):
        return True
    return False


# ── manifest 序列化（便于 MCP 参数传递） ────────────────────────────────
def manifest_to_json(manifest: dict) -> str:
    """将 manifest 序列化为 JSON 字符串（用于 MCP 参数传递）。"""
    return json.dumps(manifest, ensure_ascii=False)


def manifest_from_json(s: str) -> dict:
    """从 JSON 字符串还原 manifest。"""
    return json.loads(s)


# ── manifest 缓存（避免重复校验） ───────────────────────────────────────
_manifest_cache: dict[str, dict] = {}


def check_manifest_cached(manifest: dict, required_perm: str = PERM_READ) -> dict:
    """带缓存的 manifest 校验（同一 nonce 5 分钟内只验签一次）。"""
    key = "%s:%s:%s" % (
        manifest.get("nonce", ""),
        manifest.get("signature", ""),
        required_perm,
    )
    cached = _manifest_cache.get(key)
    if cached and (time.time() - cached.get("_at", 0)) < MANIFEST_TTL:
        return cached

    result = verify_manifest(manifest, required_perm)
    result["_at"] = time.time()
    _manifest_cache[key] = result

    # 清理过期缓存
    if len(_manifest_cache) > 100:
        now = time.time()
        expired = [k for k, v in _manifest_cache.items()
                   if now - v.get("_at", 0) > MANIFEST_TTL * 2]
        for k in expired:
            _manifest_cache.pop(k, None)

    return result


if __name__ == "__main__":
    # 简单自测
    m = create_manifest("public", ["read", "write"])
    print("manifest:", m)
    r = verify_manifest(m, "write")
    print("verify ok:", r)
    try:
        verify_manifest(m, "admin")
    except AccessDeniedError as e:
        print("expected error:", e)
    try:
        check_namespace_permission(m, "private/x")
    except AccessDeniedError as e:
        print("expected error:", e)
    print("default:", default_public_access())
