#!/usr/bin/env python3
"""
WTT Skill - Unified Agent Communication Platform
Works with both Claude Code (via ClaudeAgent adapter) and OpenClaw.

Usage with Claude Code:
    from wtt_skill import WTTSkill
    from wtt_skill.adapter import ClaudeAgent

    agent = ClaudeAgent(agent_id="my-agent")
    skill = WTTSkill(agent, auto_start=False)
    result = await skill.handle_command("@wtt list")

Usage with OpenClaw:
    from wtt_skill import create_wtt_skill
    skill = await create_wtt_skill(openclaw_agent, interval=30)
    result = await skill.handle_command("@wtt list")
"""
import asyncio
import os
import subprocess
from pathlib import Path
from typing import Optional
from .runner import WTTSkillRunner


def _service_exists() -> bool:
    try:
        if os.uname().sysname == "Darwin":
            r = subprocess.run(
                ["launchctl", "list"],
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=5,
                check=False,
            )
            return "com.openclaw.wtt.autopoll" in (r.stdout or "")
        if os.uname().sysname == "Linux":
            r = subprocess.run(
                ["systemctl", "--user", "status", "wtt-autopoll.service"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=5,
                check=False,
            )
            return r.returncode == 0
    except Exception:
        return False
    return False


def _ensure_autopoll_autostart_once() -> None:
    # Opt-out: WTT_AUTO_INSTALL_AUTOPOLL=0
    if os.getenv("WTT_AUTO_INSTALL_AUTOPOLL", "1") != "1":
        return
    if _service_exists():
        return

    script = Path(__file__).resolve().parent / "scripts" / "install_autopoll.sh"
    if not script.exists():
        return

    try:
        subprocess.run(
            ["bash", str(script)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=180,
            check=False,
        )
    except Exception:
        pass


# Import-time bootstrap: after skill is installed, once OpenClaw loads/imports this module,
# autopoll service will be installed/started automatically if missing.
_ensure_autopoll_autostart_once()


class WTTSkill:
    """WTT Skill main class - auto-starts WebSocket connection on init."""

    def __init__(self, agent, interval: int = 30, auto_start: bool = True,
                 mode: str = "websocket", ws_url: str = "wss://www.waxbyte.com/ws"):
        self.agent = agent
        self.interval = interval
        self.runner = WTTSkillRunner(agent, interval, mode=mode, ws_url=ws_url)
        self._auto_start = auto_start
        self._started = False
        self._start_task = None

        # Zero-touch bootstrap: try to install autopoll service once from wtt-skill only.
        self._ensure_autopoll_autostart()

        if auto_start:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    self._start_task = asyncio.create_task(self._auto_start_polling())
            except RuntimeError:
                pass

    def _ensure_autopoll_autostart(self):
        # Keep constructor behavior consistent; module-level bootstrap already handles this as well.
        _ensure_autopoll_autostart_once()

    async def _auto_start_polling(self):
        if not self._started:
            await self.runner.start()
            self._started = True

    async def handle_command(self, command: str) -> str:
        if self._auto_start and not self._started:
            await self._auto_start_polling()
        return await self.runner.handle_command(command)

    async def start(self):
        if not self._started:
            await self.runner.start()
            self._started = True

    async def stop(self):
        if self._started:
            await self.runner.stop()
            self._started = False

    def is_running(self) -> bool:
        return self._started and self.runner.running


async def create_wtt_skill(agent, interval: int = 30, mode: str = "websocket") -> WTTSkill:
    """Create and auto-start a WTT Skill instance. Defaults to WebSocket mode."""
    skill = WTTSkill(agent, interval, auto_start=True, mode=mode)
    await asyncio.sleep(0.1)
    return skill


__all__ = ["WTTSkill", "create_wtt_skill", "WTTSkillRunner"]
