# Middlewares, dependency injection, and errors

Middlewares
- Two layers: outer (before filters) and inner (after filters, before handler).
- Register with `<router>.<event>.outer_middleware(...)` or `<router>.<event>.middleware(...)`.
- Middleware must call `await handler(event, data)` to continue processing.
- Implement as `BaseMiddleware` subclass or async callable.

Dependency injection (context data)
- Handler/filter kwargs are resolved from context data.
- Inject custom context data via:
  - `Dispatcher(..., foo=42)`
  - `Dispatcher.start_polling(..., bar="Bazz")`
  - `SimpleRequestHandler(..., bar="Bazz")` for webhooks
  - `dp["eggs"] = Spam()`
  - Returning a dict from a filter
- Type hints: extend `MiddlewareData` to document custom context keys.

Errors
- Prefer local try/except inside handlers for known failures.
- Use router or dispatcher error handlers for global handling:
  - `@router.error(...)` for scoped handling
  - `@dispatcher.error(...)` for global
- `ErrorEvent` exposes `exception` and update context.

See:
- `docs/dispatcher/middlewares.rst`
- `docs/dispatcher/dependency_injection.rst`
- `docs/dispatcher/errors.rst`
- `examples/error_handling.py`
