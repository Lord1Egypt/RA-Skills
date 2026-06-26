# Handlers, routers, and filters

Routers and observers
- Create `Router` instances and register handlers via observer decorators (e.g., `@router.message(...)`).
- `Dispatcher` is a root router; include feature routers with `include_router`/`include_routers`.
- Common observers: `message`, `edited_message`, `callback_query`, `inline_query`, `my_chat_member`, `chat_member`, `chat_join_request`, `poll`, `shipping_query`, `pre_checkout_query`, etc.
- Handlers must be `async def`.

Filtering behavior
- The dispatcher stops at the first handler whose filters pass.
- If no filters are provided, the handler matches everything for that observer type.
- Use `F` (MagicFilter) to check event attributes safely: `F.text`, `F.sticker`, etc.

Built-in filters
- Use built-in filters like `CommandStart`, `Command`, `CallbackData`, and magic filters.
- Custom filters can be sync, async, lambda, awaitable, or `Filter` subclasses.

Combining filters
- Multiple filters in a decorator are ANDed.
- For OR, register the handler multiple times or use `or_f`.
- Negate with `~` or `invert_f`.

Passing data from filters
- Filters can return `dict` to inject data into handler kwargs.
- Magic filter `.as_(...)` can also inject values into context.

See:
- `docs/dispatcher/router.rst`
- `docs/dispatcher/filters/index.rst`
- `examples/own_filter.py`
