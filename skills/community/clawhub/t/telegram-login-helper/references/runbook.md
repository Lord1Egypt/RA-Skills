# Telegram Login Runbook

## Goal
给另一个 agent 或操作者一份不绕路的 Telegram personal-account 登录流程。

## Decision ladder

1. **先测已有 namespace**
   - `tdl chat ls -n steve --limit 5`
   - 能用就直接复用，别重复登录

2. **需要新 namespace 时，才走 QR**
   - 单个：`tdl login -n tg1 -T qr`
   - 批量：`bash skills/telegram-login-helper/scripts/login_10_namespaces.sh`

3. **QR 不方便时，优先复制工作中的 TDLib state**
   - 目录：`/home/stevewu/.tdl/data`
   - 复制后重新验证 namespace

4. **没有 session 才考虑 MTProto fallback**
   - 需要 `TELEGRAM_API_ID`
   - 需要 `TELEGRAM_API_HASH`

5. **都不满足，就明确升级为人工一次性登录**

## Verification

### Reader path
```bash
python3 /home/stevewu/.openclaw/workspace/skills/telegram-personal-ops/scripts/tg_personal_ops.py read_chats --limit 5
```

### Export path
```bash
python3 /home/stevewu/.openclaw/workspace/skills/telegram-personal-ops/scripts/tg_personal_ops.py read_history --chat 777000 --limit 20
```

## Known reality from prior work
- personal-account 路线已经确认应优先于 bot tooling。Source: memory/2026-04-19.md#L1-L6
- `steve` namespace 可复用，`tdl`/TDLib 读取链路已实测可走通。Source: memory/2026-04-19.md#L5-L9
- `send_text` 还没闭环，缺 `TELEGRAM_API_ID` / `TELEGRAM_API_HASH` 时不要硬说可做。Source: memory/2026-04-19.md#L5-L9

## Anti-patterns
- QR 失败就切 Bot API
- 不先测 namespace 就重登
- 明明缺 API credentials 还装作 MTProto fallback 可用
- 另一个 agent 扫不了码，就误判整条 Telegram reader 路线不可行
