#!/usr/bin/env python3
"""本地依赖与 AgentBay 配置检查脚本。"""

import asyncio
import importlib
import logging
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
BASE_DIR = SCRIPT_DIR.parent
STATUS_PATH = BASE_DIR / "status.md"
log = logging.getLogger("xhs")


def write_bootstrap_status(status: str, extra: dict | None = None) -> None:
    """在 common 尚未可导入时，使用标准库写入 status.md。"""
    lines = [
        "# 小红书采集状态",
        "",
        f"**状态**: {status}",
        f"**更新时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    if extra:
        for key, value in extra.items():
            lines.append(f"**{key}**: {value}")
        lines.append("")
    STATUS_PATH.write_text("\n".join(lines), encoding="utf-8")


async def ensure_reusable_session(cfg: dict, create_or_reuse_session, save_config) -> None:
    """创建或复用一个可继续用于后续步骤的 session，并写回 config.json。"""
    _agent_bay, session, is_reused = await create_or_reuse_session(cfg)
    cfg["session_id"] = session.session_id
    save_config(cfg)
    action = "复用" if is_reused else "创建"
    log.info(f"✅ AgentBay session 校验通过，已{action}: {session.session_id}")


def main() -> None:
    global log

    for module_name in ("agentbay", "playwright"):
        try:
            importlib.import_module(module_name)
        except ImportError as exc:
            err = f"缺少依赖: {exc.name}"
            print(f"❌ {err}", file=sys.stderr)
            write_bootstrap_status("error", {"说明": err})
            sys.exit(1)

    sys.path.insert(0, str(SCRIPT_DIR))
    from common import (
        clear_error_status,
        create_or_reuse_session,
        load_config,
        save_config,
        setup_env,
        setup_logging,
        validate_agentbay_env,
        write_status,
    )

    log = setup_logging("check_env")
    cfg = load_config()
    setup_env(cfg)

    ok, err = validate_agentbay_env(cfg)
    if not ok:
        log.error(f"❌ 环境检查失败: {err}")
        write_status("error", {"说明": err})
        sys.exit(1)

    try:
        asyncio.run(ensure_reusable_session(cfg, create_or_reuse_session, save_config))
    except Exception as exc:
        err = f"AgentBay 连接校验失败: {exc}"
        log.error(f"❌ {err}")
        write_status("error", {"说明": err})
        sys.exit(1)

    clear_error_status()
    log.info("✅ 本地依赖、AgentBay 配置与 session 校验通过")


if __name__ == "__main__":
    main()
