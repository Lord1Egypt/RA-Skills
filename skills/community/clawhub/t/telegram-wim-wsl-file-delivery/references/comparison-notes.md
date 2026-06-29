# Comparison Notes

## Compared public skills

- `better-telegram-file-sender`
- `telegram-send-file`
- `telegram-file-sender`

## Summary

Public skills mostly solve the generic Telegram case.
This skill is narrower and more operational:

- OpenClaw local filesystem to channel delivery
- self-hosted/local/WSL path quirks
- trusted tmp workaround for HTML
- CLI fallback when wrapper payloads misbehave

## Borrowed good ideas

- stronger README framing
- clearer audience definition
- future mention of `file_id` reuse

## Intentionally not copied

- hard promises about broad file-size limits without current end-to-end verification
- extra token/bot setup flows irrelevant for already configured OpenClaw users
