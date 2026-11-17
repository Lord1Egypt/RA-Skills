---
name: zqcc-skill-en
description: "English edition of the zqcc Qichacha relay skill. Use when querying Chinese company registration, shareholders, contacts, risks, intellectual property, operations, executives, or historical records through the zqcc MCP and Chat API. Also use when registering for a zqcc AppKey or configuring the zqcc MCP endpoint."
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - ZQCC_APP_KEY
      bins:
        - curl
        - jq
    primaryEnv: ZQCC_APP_KEY
    envVars:
      - name: ZQCC_APP_KEY
        required: true
        description: "zqcc AppKey obtained after phone login at https://zqcc.mkstone.club"
      - name: ZQCC_BASE_URL
        required: false
        description: "Optional API base URL override; defaults to https://zqcc.mkstone.club"
    homepage: https://zqcc.mkstone.club
---

# zqcc Qichacha Relay

Use the zqcc Qichacha relay to query Chinese enterprise data through one authenticated MCP endpoint or a natural-language Chat API. This is the English edition of the skill.

## Before You Begin

1. Open <https://zqcc.mkstone.club>.
2. Complete the image captcha and SMS login. A new phone number is registered automatically.
3. Open the user console and copy the `zqcc_...` AppKey.
4. Export it without placing it in prompts, source files, or logs:

```bash
export ZQCC_APP_KEY='<YOUR_ZQCC_APP_KEY>'
```

The AppKey is a paid-service credential. Successful business calls consume zqcc credits. Do not confuse it with the login JWT used by the website console.

## Choose a Workflow

### Direct MCP tool access

Use this when structured tool output or a specific data capability is required.

1. Discover live tools and schemas before choosing parameters:

```bash
./scripts/zqcc.sh tools-list
```

2. Call a tool with a JSON arguments object:

```bash
./scripts/zqcc.sh tools-call get_company_registration_info \
  '{"searchKey":"深圳市腾讯计算机系统有限公司"}'
```

Prefer the live `tools/list` schema over the bundled catalog because upstream schemas can change. Use [references/tools.md](references/tools.md) only to select a likely capability.

### Natural-language enterprise research

Use this when the user asks a broad question that may require several tools or a synthesized answer:

```bash
./scripts/zqcc.sh chat customer-001 \
  '查询深圳市腾讯计算机系统有限公司的工商信息、司法风险和经营动态'
```

Reuse the same stable `sessionId` for a continuing conversation. Use a different ID to isolate users or tasks.

### Generate MCP client configuration

```bash
./scripts/zqcc.sh config
```

This prints a JSON configuration for `https://zqcc.mkstone.club/mcp/stream`. Treat the output as secret-bearing because it contains the AppKey.

## Tool Selection

- `company`: registration, entity recognition, shareholders, contacts, branches, investments, controllers, finance.
- `risk`: enforcement, dishonesty, litigation, penalties, abnormal operations, restrictions, pledges, auctions.
- `ipr`: patents, trademarks, copyrights, apps, websites, social accounts, stores, intellectual-property pledges.
- `operation`: bidding, financing, annual operations, qualifications, recruitment, news, licenses, land, products.
- `executive`: executive roles, investments, controlled companies, personal and historical risks.
- `history`: historical registration, shareholders, executives, investments, risks, penalties, litigation, and IP records.

For ambiguous company names, call `get_company_by_query` first, then use the exact company name in follow-up calls. For executive tools, provide both the company name and executive name required by the live schema.

## Response Handling

- A successful MCP result normally appears under `result.content[]`; parse text entries as JSON when they contain JSON.
- `401` means the AppKey is missing, invalid, disabled, or belongs to a disabled user.
- `402` means the zqcc credit balance is insufficient.
- `503` means no upstream key is currently available or all upstream quotas are exhausted.
- Do not retry `401` or `402` automatically. Retry transient `502` or `503` failures conservatively.
- Do not present a tool call as successful when the JSON-RPC response contains `error` or `result.isError: true`.

See [references/api.md](references/api.md) for the complete public contract, examples, billing behavior, and troubleshooting.

## Security Rules

- Never reveal, echo, log, commit, or send `ZQCC_APP_KEY` anywhere except the zqcc HTTPS origin.
- Never place the AppKey in a query string.
- Do not call administrator endpoints.
- Ask before rotating an AppKey because rotation immediately disables previous active keys.
- Return only the enterprise data needed for the user's task, especially when results include phone numbers, addresses, litigation, or personal executive records.
