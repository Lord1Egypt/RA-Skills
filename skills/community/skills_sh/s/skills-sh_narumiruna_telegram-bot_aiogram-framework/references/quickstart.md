# Quickstart skeleton (v3)

Use this as the minimal structure for a bot that uses Router + Dispatcher:

- Create `Bot` with a token.
- Create `Dispatcher` as the root router.
- Create feature routers and `include_router` into the dispatcher.
- Register handlers via router observers (e.g., `@router.message(...)`).
- Start update delivery with `start_polling` or webhook controller.

Minimal long-polling shape:

```python
import asyncio
from aiogram import Bot, Dispatcher, Router, types

router = Router()

aio_token = "..."

@router.message()
async def handle_message(message: types.Message) -> None:
    await message.answer(message.text or "")

async def main() -> None:
    bot = Bot(aio_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

Notes:
- `Dispatcher` is the root `Router` and should be the top-level entry point for routing updates.
- Handlers must be `async def`.
- Prefer small, focused routers grouped by feature/domain.

Examples to consult in this repo:
- `examples/echo_bot.py`
- `examples/without_dispatcher.py` (direct Bot API usage)
- `examples/multi_file_bot/`
