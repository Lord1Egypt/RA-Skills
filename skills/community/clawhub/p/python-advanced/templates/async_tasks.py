from __future__ import annotations

import asyncio


async def fetch(i: int, delay: float = 0.1) -> int:
    await asyncio.sleep(delay)
    return i * 2


async def main() -> None:
    async with asyncio.TaskGroup() as tg:
        tasks = [tg.create_task(fetch(i)) for i in range(5)]
    print([t.result() for t in tasks])

    try:
        async with asyncio.timeout(0.05):
            await fetch(1, delay=1.0)
    except TimeoutError:
        print("timed out (expected)")


if __name__ == "__main__":
    asyncio.run(main())
