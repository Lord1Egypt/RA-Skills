---
name: substracker
description: Manage SubsTracker subscriptions and configuration via CLI scripts. Handles login, subscription CRUD, config updates, notifications, and dashboard queries. Use this skill whenever the user mentions subscriptions, recurring payments, subscription tracking, renewal reminders, payment history, notification configuration (Telegram, Bark, email, webhook, Gotify), or anything related to their SubsTracker instance — even if they just say "add a subscription", "what am I paying for", "check my renewals", "how much do I spend monthly", "update my Telegram config", "加个订阅", "我订阅了什么", "有哪些快到期了", "每月花多少钱", "续费", "订阅提醒", "通知设置", "看下订阅", "账单" without explicitly mentioning SubsTracker.
---

# SubsTracker API Skill

Manage subscriptions via CLI scripts that wrap the SubsTracker REST API. The scripts handle authentication, cookie management, and retries — you just call a command and get JSON back.

## Skill Structure

```
substracker-skills/
├── SKILL.md              ← You are here
└── scripts/
    ├── main.ts           ← CLI entry point (routing only)
    ├── client.ts         ← HTTP client, env loading, auth
    ├── types.ts          ← TypeScript interfaces (canonical schema + docs)
    ├── subscriptions.ts  ← Subscription commands
    ├── payments.ts       ← Payment commands
    ├── config.ts         ← Config commands
    ├── dashboard.ts      ← Dashboard command
    └── notifications.ts  ← Notification test command
```

Read `scripts/types.ts` for all field names, types, defaults, and descriptions (TSDoc comments).

## Configuration

Scripts auto-load credentials from `.env` files. No manual setup in the session.

**Load priority** (first found wins):
1. System environment variables
2. `<cwd>/.substracker-skills/.env`
3. `~/.substracker-skills/.env`

Required variables in `.env`:
```
SUBSTRACKER_URL=https://sub.example.com
SUBSTRACKER_USER=admin
SUBSTRACKER_PASS=your_password
```

If variables are missing, the script exits with a clear error. Ask the user to create their `.env` file.

## Running Commands

Resolve the runtime: use `bun` if installed, otherwise `npx -y bun`.

All commands follow the same pattern:
```bash
bun <SKILL_DIR>/scripts/main.ts <command> [subcommand] [--flags]
```

Scripts output JSON to stdout (for you to parse) and log to stderr (for debugging). Authentication and session cookies are handled automatically — if a session expires, the script re-logs in and retries.

## Command Reference

### Login

```bash
bun scripts/main.ts login
```

Usually not needed — all commands auto-login when no session exists. Use this to verify credentials.

### Subscriptions

```bash
bun scripts/main.ts s list
bun scripts/main.ts s create --name "Netflix" --expiry-date 2026-04-07 --amount 15.99
bun scripts/main.ts s get <id>
bun scripts/main.ts s update <id> --amount 19.99
bun scripts/main.ts s delete <id>
bun scripts/main.ts s toggle <id> --active false
bun scripts/main.ts s renew <id> --amount 15.99 --note "March renewal"
bun scripts/main.ts s test-notify <id>
```

#### Subscription Flags (create / update)

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--name` | string | create only | Subscription name |
| `--expiry-date` | string | create only | Expiration date (ISO format) |
| `--amount` | number | - | Cost per billing cycle |
| `--currency` | string | - | Currency code, default `CNY` |
| `--period-unit` | `day\|month\|year` | - | Billing cycle unit, default `month` |
| `--period-value` | number | - | Billing cycle length, default `1` |
| `--category` | string | - | Category label (e.g. `娱乐`) |
| `--custom-type` | string | - | Custom type (e.g. `视频流媒体`) |
| `--mode` | `cycle\|reset` | - | Subscription mode |
| `--start-date` | string | - | Start date (ISO format) |
| `--auto-renew` | `true\|false` | - | Auto-renew flag, default `true` |
| `--active` | `true\|false` | - | Active status |
| `--reminder-unit` | `day\|hour` | - | Reminder unit |
| `--reminder-value` | number | - | Reminder value |
| `--reminder-days` | number | - | Reminder days before expiry |
| `--lunar` | `true\|false` | - | Use lunar calendar |
| `--notes` | string | - | Notes / memo |

#### Toggle Flags

| Flag | Type | Description |
|------|------|-------------|
| `--active` | `true\|false` | Set active or inactive |

#### Renew Flags

| Flag | Type | Description |
|------|------|-------------|
| `--amount` | number | Payment amount |
| `--period-multiplier` | number | Multiply billing cycle |
| `--payment-date` | string | Payment date |
| `--note` | string | Payment note |

### Payments

```bash
bun scripts/main.ts p list <sub-id>
bun scripts/main.ts p edit <sub-id> <payment-id> --amount 19.99 --note "adjusted"
bun scripts/main.ts p delete <sub-id> <payment-id>
```

#### Payment Edit Flags

| Flag | Type | Description |
|------|------|-------------|
| `--date` | string | Payment date |
| `--amount` | number | Payment amount |
| `--note` | string | Payment note |

### Dashboard

```bash
bun scripts/main.ts d
```

Returns monthly/yearly spend, active count, upcoming renewals, expense breakdown.

### Config

```bash
bun scripts/main.ts c get
bun scripts/main.ts c update --timezone Asia/Shanghai --notifiers telegram,bark
```

#### Config Flags

| Flag | Type | Description |
|------|------|-------------|
| `--username` | string | Admin username |
| `--password` | string | Admin password |
| `--timezone` | string | Timezone (e.g. `Asia/Shanghai`) |
| `--show-lunar` | `true\|false` | Show lunar calendar dates |
| `--theme` | string | Theme mode |
| `--notifiers` | string | Comma-separated: `telegram,bark,email,webhook,wechatbot,gotify` |
| `--tg-bot-token` | string | Telegram bot token |
| `--tg-chat-id` | string | Telegram chat ID |
| `--bark-key` | string | Bark device key |
| `--bark-server` | string | Bark server URL |
| `--webhook-url` | string | Webhook URL |
| `--webhook-method` | string | Webhook HTTP method |
| `--webhook-template` | string | Webhook body template |
| `--wechat-webhook` | string | WeChat bot webhook URL |
| `--gotify-url` | string | Gotify server URL |
| `--gotify-token` | string | Gotify app token |
| `--email-from` | string | Sender email |
| `--email-to` | string | Recipient email |
| `--resend-key` | string | Resend API key |
| `--clear-secrets` | string | Comma-separated fields to clear |
| `--debug` | `true\|false` | Enable debug logs |
| `--payment-history-limit` | number | Max payment history entries |

### Test Notification

```bash
bun scripts/main.ts t --type telegram
```

| Flag | Type | Required | Description |
|------|------|----------|-------------|
| `--type` | string | ✓ | `telegram\|notifyx\|webhook\|wechatbot\|email\|bark\|gotify` |
| Other flags | - | - | Passed as config overrides (e.g. `--tg-bot-token` → `TG_BOT_TOKEN`) |

## Presenting Results

When showing subscription data to the user, format JSON responses as readable tables or summaries — don't dump raw JSON. For example, a subscription list should look like a table with name, amount, cycle, next renewal date, and status.

## Error Handling

- **Missing env vars**: script exits with instructions to create `.env`
- **401 Unauthorized**: auto re-login and retry (once)
- **API errors**: response includes `success: false` and `message` explaining what went wrong
