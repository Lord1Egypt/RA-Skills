---
name: wa-number-checker-skills
description: Query whether a phone number is registered on WhatsApp. Use when the user asks to check if a number has WhatsApp, verify if a number exists on WhatsApp, "查这个号有没有 WhatsApp", "这个号码有没有在用 WhatsApp", "WhatsApp number check", or "验证号码是否在 WhatsApp". Supports MCP (wa-check-api) first, then REST API per references/api.md.
---

# WhatsApp Number Check

Determine whether a given phone number is registered on WhatsApp. Use this skill when the user asks if a number has WhatsApp or is using WhatsApp.

## How to call

1. **If wa-check-api MCP is configured**: Prefer using `call_mcp_tool` to call `check_whatsapp_number` with the `phone` parameter (E.164 format recommended, e.g. `+34605797764` or `+8613800138000`).
2. **If MCP is not configured or you need to call from code/scripts**: Use the REST API; see [references/api.md](references/api.md). Include the `x-api-key` header and request `GET /api/wa/check?phone=...`. Base URL is `https://wa-check-api.whatsabot.com`.

## Parameters and format

- `phone`: Required. E.164 or digits only (e.g. `34605797764`). If the user only provides a local number, ask for the country code or have them supply it.

## Results and errors

- **Success**: Answer based on `result.exist` in the response—"This number is registered on WhatsApp" or "This number is not registered on WhatsApp."
- **API returns non-zero code**: Briefly explain using the error code (missing API key, invalid number, insufficient credits, rate limit, etc.) and suggest the user check their API key or credits. Error code details are in [references/api.md](references/api.md).
