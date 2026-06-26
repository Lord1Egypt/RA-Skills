# Connecting OpenClaw to Shopware

OpenClaw runs on a **gateway host** (shell, HTTP client, browser). Shopware runs as a **remote PHP application**. This skill assumes you reach Shopware via **HTTPS** (Admin API, Store API, or browser) and optionally work on a **local clone** of the project in the agent workspace.

**Operational checklist** (version, env names, sales channel, staging vs prod): [WORKFLOWS.md](WORKFLOWS.md) (*Before you advise or change anything*).

Official OpenClaw: [Skills](https://docs.openclaw.ai/tools/skills), [Skills config](https://docs.openclaw.ai/tools/skills-config), [Sandbox vs tool policy](https://docs.openclaw.ai/gateway/sandbox-vs-tool-policy-vs-elevated).

## Topology tiers (least access first)

| Tier | Goal | Typical setup |
| ---- | ---- | ------------- |
| **0 – Guidance** | Explain Shopware / review plans without calling an instance | No env required if you fork the skill metadata; otherwise set a minimal `SHOPWARE_BASE_URL` for eligibility. |
| **1 – HTTP APIs only** | Integrations via **Admin API** and/or **Store API** | `SHOPWARE_BASE_URL` + OAuth / integration credentials (see [AUTH.md](AUTH.md)); use `curl` or a dedicated OpenClaw plugin if installed. |
| **2 – Code + HTTP** | Extension/theme work with **git** and tests | Tier 1 plus a **clone** of the Shopware project or extension on the gateway filesystem; deploy separately. |

## What `SHOPWARE_BASE_URL` means

- Use the **public base URL** the gateway can reach (no trailing slash), e.g. `https://shop.example.com` or `https://admin.example.com` if that is how the shop is exposed.
- **Admin API** and **Store API** paths are documented on [developer.shopware.com](https://developer.shopware.com/)—prefixes differ; do not guess URLs.

## Gateway behaviour

- After changing **`tools.allow`**, **plugins**, or **skills entries**, follow OpenClaw docs: **`openclaw gateway restart`** when required. A new chat (`/new`) alone may not refresh tool registration.
- Install this skill via ClawHub or copy the skill folder into the agent workspace `skills/` tree so `SKILL.md` is discovered.

## Shopware-specific companion tools

There is **no** Shopware tool plugin bundled with this skill (v1). Use **native** `exec` / HTTP / browser tools with strict allowlists, or add a **custom OpenClaw plugin** later and document its tool names here.

## Further reading

- Auth and env vars: [AUTH.md](AUTH.md)
- curl / API patterns: [TOOLING.md](TOOLING.md)
- Merchant Admin **usage** (not API): [MERCHANT_USER_DOCS.md](MERCHANT_USER_DOCS.md)
