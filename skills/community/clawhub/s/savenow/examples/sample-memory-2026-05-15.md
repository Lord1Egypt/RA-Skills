# 2026-05-15

## 14:02 - Telegram UI conventions
- Inline keyboards use a single-row, 3-button layout.
- Cancel button always sits on the rightmost slot.
- (merged 16:48)

## 16:48 - Gateway token mismatch fix
- Resolved `unauthorized: gateway token mismatch` by updating `gateway.cmd` and the related env variables.
- Next time a similar error appears, check token and env alignment first.
