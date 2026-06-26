# Update delivery (long polling vs webhook)

Long polling
- Use `Dispatcher.start_polling` or `Dispatcher.run_polling`.
- Only one polling process per bot token, or Telegram returns an error.
- If you need to scale or run multiple bots, prefer webhooks.
- See `docs/dispatcher/long_polling.rst` and `examples/echo_bot.py`.

Webhook
- Webhook and polling are mutually exclusive.
- Use `aiogram.webhook.aiohttp_server` controllers for aiohttp integration:
  - `BaseRequestHandler`, `SimpleRequestHandler` (single bot), `TokenBasedRequestHandler` (multi-bot).
- Validate incoming requests with secret token or IP filtering middleware.
- For non-aiohttp frameworks, parse request JSON into `Update` and call `dispatcher.feed_update`.
- See `docs/dispatcher/webhook.rst`, `examples/echo_bot_webhook.py`, `examples/echo_bot_webhook_ssl.py`.

Manual update feeding
- `Dispatcher.feed_update` accepts `Update` objects.
- `Dispatcher.feed_raw_update` accepts raw dict updates.
