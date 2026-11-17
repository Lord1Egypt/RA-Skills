# -*- coding: utf-8 -*-
"""
企业技能对接外部系统（ERP / TMS / WMS / 船司 / 报关 / 邮件 / 浏览器 / LLM / RPA）时，
测试侧共用的 **profile / 禁止真实外呼** 工具。

- 仅标准库 + jiangchang_skill_core.config；不发起 HTTP；不启动浏览器。
- 真实 API / RPA 契约测试请放在 ``tests/integration/*.sample``，并显式设置 ``OPENCLAW_TEST_TARGET``。
"""
from __future__ import annotations

from typing import Any, Final

from jiangchang_skill_core import config

ALLOWED_TEST_TARGETS: Final[frozenset[str]] = frozenset(
    {
        "unit",
        "mock",
        "simulator_api",
        "simulator_rpa",
        "real_api",
        "real_rpa",
    }
)


def _raw_test_target_env() -> str:
    return (config.get("OPENCLAW_TEST_TARGET") or "").strip()


def get_test_target() -> str:
    """
    读取 ``OPENCLAW_TEST_TARGET``（经 ``config.get`` 三级合并）。

    未设置时返回 ``unit``。非法取值抛出 ``ValueError``，便于尽早发现拼写错误。
    """
    raw = _raw_test_target_env()
    if not raw:
        return "unit"
    if raw not in ALLOWED_TEST_TARGETS:
        raise ValueError(
            f"Invalid test target {raw!r}. Allowed: {sorted(ALLOWED_TEST_TARGETS)}"
        )
    return raw


def real_access_allowed(profile: str) -> bool:
    """
    判断当前 ``OPENCLAW_TEST_TARGET`` 是否允许运行 ``profile`` 档位测试。
    """
    target = get_test_target()
    if profile in ("mock", "simulator_api", "simulator_rpa"):
        return True
    if profile == "real_api":
        return target == "real_api"
    if profile == "real_rpa":
        return target == "real_rpa"
    raise ValueError(f"unknown profile for real_access_allowed: {profile!r}")


def should_skip_profile(profile: str, write: bool = False) -> tuple[bool, str]:
    """
    返回 ``(should_skip, reason)``。

    策略摘要：
    - ``mock``：永不跳过（内存 / FakeAdapter，无外呼）。
    - ``simulator_api`` / ``simulator_rpa``：仅当 ``get_test_target()`` 与 profile 一致时不跳过。
    - ``real_api`` / ``real_rpa``：仅当 ``get_test_target()`` 与 profile 一致时不跳过。
    - ``write`` 参数保留以兼容 integration 样例签名；档位一致即允许写操作测试。
    """
    _ = write
    target = get_test_target()

    if profile == "mock":
        return (False, "")

    if profile in ("simulator_api", "simulator_rpa", "real_api", "real_rpa"):
        if target != profile:
            return (True, f"OPENCLAW_TEST_TARGET must be {profile} (got {target!r})")
        return (False, "")

    raise ValueError(f"unknown profile: {profile!r}")


class FakeAdapter:
    """
    模拟外部系统 adapter，用于单元测试中的超时 / 鉴权 / 畸形响应等分支。

    ``mode``：``success`` | ``timeout`` | ``invalid_response`` | ``unauthorized``
    """

    def __init__(self, mode: str = "success") -> None:
        if mode not in ("success", "timeout", "invalid_response", "unauthorized"):
            raise ValueError(f"unsupported FakeAdapter mode: {mode!r}")
        self._mode = mode

    def call(self, payload: Any) -> Any:
        if self._mode == "success":
            return {"success": True, "data": {"echo": payload}}
        if self._mode == "timeout":
            raise TimeoutError("simulated upstream timeout")
        if self._mode == "invalid_response":
            return object()  # 非 dict，模拟无法解析的响应体
        if self._mode == "unauthorized":
            raise PermissionError("simulated 401/403")
        raise RuntimeError("unreachable")


def assert_no_real_network_env() -> None:
    """
    断言默认必跑套件未误设真实外联档位（``real_api`` / ``real_rpa``）。

    若需在受控环境跑真实集成，请显式设置 ``OPENCLAW_TEST_TARGET`` 并使用 ``tests/integration/*.sample``。
    """
    target = get_test_target()
    assert target not in ("real_api", "real_rpa"), (
        f"OPENCLAW_TEST_TARGET must not be {target!r} in default unit tests"
    )
