# Authentication (Shopware + OpenClaw)

## Principles

- **Never** paste client secrets, integration secrets, or user passwords into chat, Git, or skill markdown.
- When confirming configuration for the user or logs, report only **which** variables exist (**set/unset**) or use **masked** placeholders—**not** raw tokens.
- Use the **host environment** or OpenClaw **`skills.entries["shopware-expert"].env`** (see [Skills config](https://docs.openclaw.ai/tools/skills-config)).
- If the agent runs in a **sandbox**, mirror required variables into sandbox env as per OpenClaw docs.

## Admin API (typical integration)

Shopware commonly uses **OAuth** for the Admin API (integration user / app credentials). Exact header names and token URLs depend on your Shopware **version** and setup. Follow [Admin API concept](https://developer.shopware.com/docs/concepts/api/admin-api/) and your Administration integration settings.

Illustrative variables (names may vary by your wrapper scripts):

| Variable | Meaning |
| -------- | ------- |
| `SHOPWARE_BASE_URL` | HTTPS base URL of the shop (no trailing slash) |
| `SHOPWARE_ADMIN_API_CLIENT_ID` | OAuth client identifier |
| `SHOPWARE_ADMIN_API_CLIENT_SECRET` | OAuth client secret |
| `SHOPWARE_OAUTH_TOKEN_URL` | Token endpoint (if not derived automatically) |

**Do not** commit a filled `.env`. Use `.env.example` only as a template.

## Store API

The **Store API** uses **sales-channel context** (and often **context tokens** for cart/session). See [Store API concept](https://developer.shopware.com/docs/concepts/api/store-api/) and the generated reference `STORE_API.md` in this skill.

## Browser / human login

For one-off Admin UI tasks, a **browser** tool may use an interactive session. Prefer **least privilege** service accounts for automation; avoid storing human MFA-backed sessions in files.

## Related

- [CONNECTING.md](CONNECTING.md): topologies
- [TOOLING.md](TOOLING.md): example curl patterns once tokens are available
- [OPENCLAW_INTEGRATION.md](OPENCLAW_INTEGRATION.md): sandbox and tool policy
