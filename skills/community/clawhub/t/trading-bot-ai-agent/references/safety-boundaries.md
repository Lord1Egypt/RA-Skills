# Safety boundaries

The original `trading_bot_ai_agent` archive is intentionally not distributed.
It contained a non-empty Telegram bot token and code paths that accepted
exchange credentials, generated and exported wallet private keys, submitted
mainnet exchange orders, broadcast blockchain transactions, withdrew assets,
enabled permissive CORS, and listened on `0.0.0.0`.

The public skill replaces those capabilities with a deterministic offline
simulator. It contains no account connector, wallet, HTTP server, Telegram bot,
database, external AI provider, or live execution path.

If a user provides a credential or private key, do not echo it. Recommend
immediate revocation or rotation through the relevant provider.
