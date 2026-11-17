#!/usr/bin/env python3
"""skill-to-http 极速模式管理

为 skill-to-http 创建专用轻量 Agent（stt-runner），
减少每次执行注入的 system prompt（155k → ~35k tokens），
预期速度提升 2-4x。

只对 executor=openclaw 有效。
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator

logger = logging.getLogger("skill-to-http.speed_mode")

# ── Paths ─────────────────────────────────────────────────────────────
from _paths import CONFIG_PATH
OPENCLAW_CONFIG = Path.home() / ".openclaw" / "openclaw.json"
K8S_CONFIG = Path("/app/k8s-config/openclaw.json")
RUNNER_WORKSPACE = Path.home() / ".openclaw" / "workspace" / "stt-runner"
RUNNER_AGENT_ID = "stt-runner"

# stt-runner 的极简 system prompt，只说明角色
RUNNER_SYSTEM_MD = """\
# SYSTEM.md

You are a focused task executor for skill-to-http.
Your job: execute the given skill task and return the result.
Be concise and complete. No greetings, no confirmations, no extra commentary.
Just do the task and return the result.
"""


def _load_stt_config() -> dict:
    if CONFIG_PATH.exists():
        try:
            return json.loads(CONFIG_PATH.read_text())
        except Exception:
            pass
    return {}


def _save_stt_config(cfg: dict) -> None:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))


def _load_openclaw_config() -> dict:
    if OPENCLAW_CONFIG.exists():
        return json.loads(OPENCLAW_CONFIG.read_text())
    return {}


def _save_openclaw_config(cfg: dict) -> None:
    """保存 openclaw.json 并同步到 k8s-config（双写保持持久化）。"""
    # 更新 lastTouchedAt 触发 Gateway 自动 reload
    cfg.setdefault("meta", {})
    cfg["meta"]["lastTouchedAt"] = datetime.now(timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.000Z"
    )
    OPENCLAW_CONFIG.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
    # 同步到 k8s-config（Pod 重建后持久化）
    try:
        shutil.copy(str(OPENCLAW_CONFIG), str(K8S_CONFIG))
    except Exception as e:
        logger.warning("Failed to sync to k8s-config: %s", e)


def _agent_exists(cfg: dict) -> bool:
    """检查 stt-runner 是否已在 openclaw.json 中注册。"""
    agents = cfg.get("agents", {}).get("list", [])
    return any(a.get("id") == RUNNER_AGENT_ID for a in agents)


def _wait_gateway_reload(timeout: int = 15) -> bool:
    """等待 Gateway 重启完成（轮询 /health）。"""
    import urllib.request
    try:
        from skill_runner import _get_openclaw_api_url
        api_url = _get_openclaw_api_url()
    except ImportError:
        api_url = "http://localhost:18789"
    deadline = time.time() + timeout
    # 先等 Gateway 短暂不可用（重启中）
    time.sleep(1.5)
    while time.time() < deadline:
        try:
            req = urllib.request.Request(f"{api_url}/health", method="GET")
            proxy = urllib.request.ProxyHandler({})
            opener = urllib.request.build_opener(proxy)
            with opener.open(req, timeout=2) as resp:
                if resp.status == 200:
                    return True
        except Exception:
            pass
        time.sleep(1)
    return False


def status() -> dict:
    """返回极速模式状态。"""
    stt_cfg = _load_stt_config()
    oc_cfg = _load_openclaw_config()
    enabled = stt_cfg.get("speed_mode", False)
    agent_registered = _agent_exists(oc_cfg)
    workspace_exists = (RUNNER_WORKSPACE / "SYSTEM.md").exists()
    executor = stt_cfg.get("executor", "auto")

    return {
        "enabled": enabled and agent_registered and workspace_exists,
        "configured": enabled,
        "agent_registered": agent_registered,
        "workspace_exists": workspace_exists,
        "agent_id": RUNNER_AGENT_ID,
        "applicable": executor in ("auto", "openclaw"),
        "executor": executor,
    }


def setup() -> Generator[dict, None, None]:
    """初始化极速模式，逐步 yield 进度。"""

    # Step 1: 创建 workspace
    yield {"step": 1, "total": 6, "msg": "创建专用 workspace..."}
    try:
        RUNNER_WORKSPACE.mkdir(parents=True, exist_ok=True)
        (RUNNER_WORKSPACE / "SYSTEM.md").write_text(RUNNER_SYSTEM_MD)
        logger.info("Created stt-runner workspace at %s", RUNNER_WORKSPACE)
        yield {"step": 1, "total": 6, "msg": "workspace 创建完成 ✅"}
    except Exception as e:
        yield {"step": 1, "total": 6, "msg": f"创建 workspace 失败: {e}", "error": True}
        return

    # Step 2: 注册 agent 到 openclaw.json
    yield {"step": 2, "total": 6, "msg": "注册专用 Agent 到 openclaw.json..."}
    try:
        oc_cfg = _load_openclaw_config()
        if not _agent_exists(oc_cfg):
            oc_cfg.setdefault("agents", {}).setdefault("list", []).append({
                "id": RUNNER_AGENT_ID,
                "name": "STT Runner",
                "workspace": str(RUNNER_WORKSPACE),
                "heartbeat": {"every": "0"},
                "model": {
                    "primary": oc_cfg.get("agents", {})
                        .get("defaults", {})
                        .get("model", {})
                        .get("primary", "openai/deepseek-v4-pro")
                }
            })
            logger.info("Registered stt-runner agent")
            yield {"step": 2, "total": 6, "msg": "Agent 注册完成 ✅"}
        else:
            logger.info("stt-runner already registered, skipping")
            yield {"step": 2, "total": 6, "msg": "Agent 已存在，跳过 ✅"}
    except Exception as e:
        yield {"step": 2, "total": 6, "msg": f"注册 Agent 失败: {e}", "error": True}
        return

    # Step 3: 双写 openclaw.json + k8s-config（触发 Gateway reload）
    yield {"step": 3, "total": 6, "msg": "保存配置并触发 Gateway 重载..."}
    try:
        _save_openclaw_config(oc_cfg)
        logger.info("Saved openclaw.json, Gateway reload triggered")
        yield {"step": 3, "total": 6, "msg": "配置已保存并双写 k8s-config ✅"}
    except Exception as e:
        yield {"step": 3, "total": 6, "msg": f"保存配置失败: {e}", "error": True}
        return

    # Step 4: 等待 Gateway 重启
    yield {"step": 4, "total": 6, "msg": "等待 Gateway 重启（约 2-5s）..."}
    ok = _wait_gateway_reload(timeout=15)
    if not ok:
        yield {"step": 4, "total": 6, "msg": "Gateway 重启超时，请手动检查", "error": True}
        return
    yield {"step": 4, "total": 6, "msg": "Gateway 重启完成 ✅"}

    # Step 5: 验证 stt-runner 可执行
    yield {"step": 5, "total": 6, "msg": "验证执行链路（约 15-25s）..."}
    t0 = time.time()
    try:
        result = subprocess.run(
            [
                "openclaw", "agent", "--local",
                "--agent", RUNNER_AGENT_ID,
                "--session-id", "stt-speed-verify",
                "--message", "Reply with exactly: SPEED_OK",
                "--json",
                "--thinking", "off",
                "--timeout", "40",
            ],
            capture_output=True, text=True, timeout=50,
        )
        elapsed = time.time() - t0
        output = result.stderr or result.stdout
        if "SPEED_OK" in output:
            yield {
                "step": 5, "total": 6,
                "msg": f"验证通过 ✅（耗时 {elapsed:.1f}s）",
                "elapsed": elapsed,
            }
        else:
            yield {
                "step": 5, "total": 6,
                "msg": f"验证未通过（输出不含 SPEED_OK），但 Agent 已注册，可继续使用",
                "warn": True,
            }
    except subprocess.TimeoutExpired:
        elapsed = time.time() - t0
        yield {
            "step": 5, "total": 6,
            "msg": f"验证超时 ({elapsed:.0f}s)，Agent 已注册，可继续使用",
            "warn": True,
        }
    except Exception as e:
        yield {"step": 5, "total": 6, "msg": f"验证失败: {e}", "warn": True}

    # Step 6: 写入 skill-to-http config
    yield {"step": 6, "total": 6, "msg": "保存极速模式配置..."}
    try:
        stt_cfg = _load_stt_config()
        stt_cfg["speed_mode"] = True
        stt_cfg["speed_mode_agent"] = RUNNER_AGENT_ID
        _save_stt_config(stt_cfg)
        logger.info("Speed mode enabled, agent=%s", RUNNER_AGENT_ID)
    except Exception as e:
        yield {"step": 6, "total": 6, "msg": f"保存配置失败: {e}", "error": True}
        return

    yield {
        "step": 6, "total": 6,
        "msg": "极速模式已开启 🚀",
        "done": True,
        "success": True,
    }


def teardown() -> dict:
    """关闭极速模式，从 openclaw.json 移除 stt-runner。"""
    try:
        # 从 openclaw.json 移除
        oc_cfg = _load_openclaw_config()
        if _agent_exists(oc_cfg):
            oc_cfg["agents"]["list"] = [
                a for a in oc_cfg["agents"]["list"]
                if a.get("id") != RUNNER_AGENT_ID
            ]
            _save_openclaw_config(oc_cfg)
            logger.info("Removed stt-runner from openclaw.json, Gateway reload triggered")
            # 等 Gateway 重启
            gw_ok = _wait_gateway_reload(timeout=10)
            if not gw_ok:
                logger.warning("Gateway reload timed out during teardown (non-critical)")

        # 从 skill-to-http config 移除
        stt_cfg = _load_stt_config()
        stt_cfg.pop("speed_mode", None)
        stt_cfg.pop("speed_mode_agent", None)
        _save_stt_config(stt_cfg)

        logger.info("Speed mode disabled")
        return {"ok": True, "message": "极速模式已关闭，Gateway 已重载"}
    except Exception as e:
        logger.exception("teardown failed")
        return {"ok": False, "message": str(e)}
