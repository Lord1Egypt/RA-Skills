"""
OpenClaw Task Runner Skill - CLI 入口

支持：
    python -m skills.yintai_tasks_runner
"""

import asyncio
from .skill import main

if __name__ == "__main__":
    asyncio.run(main())
