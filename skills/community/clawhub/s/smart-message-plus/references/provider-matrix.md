# Provider Capability Matrix

Verified by real e2e testing on 2026-07-14 (DingTalk/Feishu) and 2026-07-17 (WeCom webhook).

| Capability | DingTalk | Feishu | WeCom (webhook) | Notes |
|------------|:--------:|:------:|:---------------:|-------|
| P2P text | ✅ | ✅ | ❌ | DingTalk: robot oToMessages/batchSend (batch of 20); Feishu: im/v1/messages; WeCom webhook is group-only |
| P2P markdown | ✅ native | ✅ via card | ❌ | Feishu post rich-text does NOT accept standard markdown → rendered through interactive card `lark_md` |
| Group text / markdown | ✅ | ✅ | ✅ native | DingTalk/Feishu require the bot to be **in the group** first; WeCom needs a group robot webhook |
| Image | ✅ ≤20MB | ✅ ≤10MB | ✅ ≤2MB | DingTalk media/upload → mediaId; Feishu im/v1/images → image_key; WeCom base64+md5 inline |
| File | ✅ ≤20MB | ✅ ≤30MB | ✅ ≤20MB | Feishu file_type inferred from extension; WeCom webhook/upload_media → media_id (3-day TTL) |
| Mention person | ✅ md `<@userId>` | ✅ `<at user_id=...>` | ✅ text: mentioned_list; md: `<@userid>` | WeCom text also supports mentioned_mobile_list |
| Mention all | ⚠️ textual | ✅ `<at user_id="all">` | ✅ text only (`@all`) | WeCom markdown does NOT support at-all (CLI prints notice) |
| Recall | ✅ no time limit | ✅ within 24h | ❌ | WeCom webhook returns no msg_id → recall impossible by design |
| Card messages | ✅ v1.1 ActionCard | ✅ v1.1 interactive | ✅ news (single link) | WeCom news card: exactly 1 jump URL (extra buttons ignored, notice printed); 0-button falls back to bold-title markdown |
| Resolve by mobile | ✅ topapi getbymobile | ✅ batch_get_id | ❌ | WeCom webhook mode has no contact API |
| Resolve by email | ❌ no API | ✅ batch_get_id | ❌ | |
| Dept lookup (builtin org) | ✅ listsub + listid | ✅ contact/v3 | ❌ | |
| Create group | ✅ v2.0 dual-path | ✅ v2.0 im/v1/chats | ❌ | See DingTalk note below; WeCom webhook cannot create groups |
| List groups | ❌ no API | ✅ im/v1/chats GET | ❌ | |

## WeCom: webhook mode vs app mode

The current `wecom` provider implements **group robot webhook** mode only:

- **Zero setup cost**: add a robot to any internal group (`···` → 群机器人), copy the webhook URL. No corp credentials, no console config.
- **No trusted-IP requirement** — this is the key reason. WeCom self-built app APIs enforce a **trusted-IP allowlist** checked per request against the real source IP, and WeCom **refuses to allowlist third-party cloud provider IPs** (verified: errcode=60020, Tencent Cloud egress IP rejected with "以下IP属于第三方服务商" console error). Hosted containers / cloud runtimes without a corporate-owned egress IP cannot use app mode at all.
- Capability trade-off: group-only; no p2p / contacts / group-create / recall / dept broadcast.
- Rate limit: 20 messages/min per robot (errcode=45009 → CLI prints wait notice).
- One webhook = one group. `--chat-id` accepts a saved group alias, a full webhook URL, or a bare key.
- `wecom-app` full-capability mode is **reserved** (account fields corp_id/corp_secret/agent_id already accepted) for environments that do have a corporate egress IP.

## Token model

| | DingTalk | Feishu | WeCom (webhook) |
|--|----------|--------|-----------------|
| Endpoint | `POST /v1.0/oauth2/accessToken` | `POST /auth/v3/tenant_access_token/internal` | none (key embedded in webhook URL) |
| Credential | AppKey + AppSecret | App ID + App Secret | webhook key |
| TTL | ~7200s | ~7200s | n/a |
| Cache | token_cache.json, refreshed 5 min early | same | n/a |
| Invalid-token retry | auto (once) | auto (once, codes 99991661/63/68) | n/a (93000 = webhook removed/invalid) |

## Rate limits observed

- DingTalk batchSend: max 20 userIds per call → auto-chunked
- Both: 429/5xx get one backoff retry (see core/http.py)

## Known platform quirks

1. **Feishu open_id is per-app** — an open_id obtained under app A is invalid under app B. After switching apps, re-resolve users (aliases must be re-saved).
2. **Feishu permission changes require version release** — after granting scopes in the console you must create & publish a new app version.
3. **DingTalk Stream mode** — only relevant if you build a listener; multiple listeners on the same app compete for messages.
4. **DingTalk email** — no server-side email→userId lookup exists; guide users to mobile/userId/alias.
5. **Feishu accounts without email/mobile bound** cannot be resolved via batch_get_id; use group-member reverse lookup or alias.
6. **WeCom trusted-IP check is per-request against real source IP** — allowlisting an IP you don't actually egress from does nothing; and third-party cloud egress IPs are rejected at console level. Webhook mode is the only viable path from hosted containers.
7. **WeCom "智能机器人" (openBotProfile links) ≠ group webhook robots** — the new bot platform's profile IDs are not webhook keys; only the in-group robot's webhook URL works with this provider.
