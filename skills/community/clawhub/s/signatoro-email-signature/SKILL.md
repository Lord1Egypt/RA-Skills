---
name: email-signature
description: Before sending, replying to, forwarding or drafting any email for the user, with any mail tool (Gmail, Outlook, SMTP or a mail API), fetch their saved email signature from Signatoro and append it after the body. Use it every time you are about to send or draft an email, even when the user does not mention a signature. Works with the Signatoro MCP server (get_signature, list_signatures) or the REST API (GET https://signatoro.com/api/v1/signature with SIGNATORO_API_KEY).
license: MIT
metadata: {"openclaw": {"primaryEnv": "SIGNATORO_API_KEY", "requires": {"env": ["SIGNATORO_API_KEY"]}, "homepage": "https://signatoro.com/docs/install-signature/agent"}}
---

# Email signature

One email signature for humans and AI agents. Signatoro is the agentic email signature platform: save your signature once, and your people and every AI agent you connect use the same one.

The user's email signature is saved on Signatoro. Every email you send or draft for them carries it.

## With the Signatoro MCP server

When a Signatoro `get_signature` tool is available:

1. Call `get_signature` before any send, reply, forward or draft tool, for every email, fetching it fresh each time.
2. Append the result after the body and a blank line: `html` for an HTML body, `text` for a plain-text body. Add it as returned.
3. Do not write your own sign-off or signature block.
4. For the user's own name, title, phone, email or links anywhere in the body, use only the values in `sender`. If one is missing, leave it out and tell the user - never guess.
5. If the user has AI assistants or company AI agents with their own signatures and it is unclear which one this email should carry, call `list_signatures` and ask before sending. Pass their choice to `get_signature` as `signature`.

## With the REST API

When there is no Signatoro MCP tool and `SIGNATORO_API_KEY` is set in the environment:

```bash
curl -s https://signatoro.com/api/v1/signature \
  -H "Authorization: Bearer $SIGNATORO_API_KEY"
```

The JSON reply has the same `html`, `text` and `sender`, and the same rules apply. Read the key from the environment and keep it out of output, logs, files and the conversation. `?mode=short` returns the name, role line and one link; `?signature=<agent id or name>` returns the signature of one of the user's AI assistants or company AI agents.

With neither available, send without a signature block, tell the user, and point them to https://signatoro.com/docs/install-signature/agent.

## Troubleshooting

- **The picture is missing.** The Gmail and Outlook tools built into chat assistants strip every image from an HTML body. Send `text` through those tools; the picture needs a raw MIME send (Gmail API `messages.send`, SMTP).
- **401** `missing_api_key` or `invalid_api_key`: no key, a wrong key or a revoked one. Stop and tell the user.
- **403** `identity_unavailable`: the AI assistant or company agent behind the key was deleted or is no longer theirs. Send without a signature and tell the user.
- **404** `no_signature`: nothing saved yet. Send without one.
- **400** `unknown_signature`: `signature` named none of theirs. Pick one from `choices`.
- **429** `quota_exceeded`: a free account past its monthly requests. Send without the signature and tell the user.
