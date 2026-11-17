---
name: wechat-blessings
description: Create personalized Chinese or multilingual greetings for holidays, birthdays, milestones, and customer care, then preview and send them through WeChat only after explicit confirmation. Use when a user asks to compose and optionally deliver a blessing to one or many recipients now or later.
metadata: {"openclaw":{"requires":{"env":["WX_OPENCLAW_OPS_URL","WX_OPENCLAW_OPS_TOKEN"],"bins":["python3"]},"primaryEnv":"WX_OPENCLAW_OPS_TOKEN","envVars":[{"name":"WX_OPENCLAW_OPS_URL","required":true,"description":"Authenticated wx-openclaw operations endpoint."},{"name":"WX_OPENCLAW_OPS_TOKEN","required":true,"description":"Bearer token for the operations endpoint."}]}}
---

# WeChat Blessings

Create the blessing in conversation, then use `{baseDir}/scripts/send_blessing.py` only for confirmed delivery.

## Compose

1. Determine the occasion, recipient relationship, tone, language, length, and whether commercial wording is appropriate.
2. If key context is missing, ask only for information that materially changes the greeting.
3. Produce three distinct candidates: warm, concise, and expressive unless the user requested one style.
4. Avoid unverifiable personal details, health promises, pressure, spam phrasing, and identical mass-personalized claims.
5. Let the user select or edit the final wording.

Read `references/styles.md` when choosing tone or personalizing a batch.

## Confirm and send

- A final blessing is not permission to send it.
- Run the delivery script without `--execute` and show the exact text, recipients, time, and confirmation code.
- Send only after explicit confirmation of that preview.
- If text, targets, or time changes, generate a new preview and code.
- Never claim delivery success without a successful gateway response.

```bash
python3 {baseDir}/scripts/send_blessing.py \
  --target "Alice" --text "生日快乐，愿新的一岁平安顺遂。"

python3 {baseDir}/scripts/send_blessing.py \
  --target "Alice" --target "Bob" \
  --text "端午安康，愿生活常有清香与从容。" \
  --send-at "2026-07-03 08:30:00"
```

After confirmation, append:

```bash
--execute --confirm CONFIRMATION_CODE
```
