# Error recovery

- `INVALID_TEXT`: Shorten the text. Ask before splitting because every chunk is separately paid.
- `INVALID_VOICE`: Call `tts_list_voices`; use a live provider-prefixed id.
- `INVALID_SPEED`: Use a value from 0.5 through 2.
- `QUOTE_EXPIRED`: Obtain a new quote. Re-check the amount and re-approve if required.
- `PRICE_LIMIT_EXCEEDED`: Stop and ask the user to change the budget or policy.
- `UNSUPPORTED_NETWORK`: Use a wallet that supports the quoted Base network. Never silently bridge or switch assets.
- `INSUFFICIENT_FUNDS`: Ask the user to fund the wallet with the required USDC.
- `PAYMENT_REJECTED`: Recreate the PaymentPayload from the exact current selected requirement. Do not reuse a different quote.
- `PAYMENT_OUTCOME_UNKNOWN`: Do not retry or re-pay. Inspect the wallet, facilitator, or chain and escalate to the user.
- `RATE_LIMITED`: Respect `Retry-After`; do not create a new payment authorization just to retry sooner.
- `TTS_UPSTREAM_ERROR`: Retry only when the response conclusively proves that settlement did not occur.
- `OUTPUT_TOO_LARGE`: Select an allowed output mode. If settlement already occurred, do not synthesize again.
- `AUDIO_NOT_AVAILABLE`: Explain that a new synthesis costs another payment and obtain explicit approval.
- `CONFIGURATION_ERROR`: Surface setup guidance without stack traces or secrets. If `settled: true` is present, do not pay again.

