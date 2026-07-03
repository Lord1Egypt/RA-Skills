# RealBrowser by Ceki

[![ClawHub](https://img.shields.io/badge/ClawHub-realbrowser-purple)](https://clawhub.ai/skills/realbrowser)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/ceki-sdk?label=ceki-sdk)](https://pypi.org/project/ceki-sdk/)
[![GitHub release](https://img.shields.io/github/v/release/Ceki-me/realbrowser-skill)](https://github.com/Ceki-me/realbrowser-skill/releases)
[![Discussions](https://img.shields.io/github/discussions/Ceki-me/realbrowser-skill)](https://github.com/Ceki-me/realbrowser-skill/discussions)

> **Real Chrome sessions for AI agents** — for tasks where headless or scripted requests aren't enough.
>
> Use on sites you own or have authorization to operate on (your own QA flows, accessibility audits of your own sites, synthetic monitoring, support automation in your own dashboards, public data within site Terms of Service).

This is a thin client to the `ceki-sdk` CLI / Python SDK. It lets your AI agent open a real Chrome session and drive it — yours via the [Ceki extension](https://browser.ceki.me/install), or one rented from another opted-in user via the marketplace.

## Three modes

| Mode | Where | Cost | Visibility |
|---|---|---|---|
| **Self** | Your own Chrome (Ceki extension) | Free for host_user == renter_user | Only you |
| **Marketplace** | Chrome contributed by another user who opted in to host | $0.01/min, USDC | The host can see your session |
| **Earn** (opt-in, off) | Your idle Chrome contributed back | 90% of session price | Other agents you allow |

## Use responsibly

Use this skill only on sites where you have authorization (your own, public data within site Terms of Service, accessibility audits you are responsible for, customer support on behalf of your own users with their consent). See `SKILL.md` for appropriate and inappropriate use cases.

## Install

```bash
clawhub skill install realbrowser
```

Or standalone CLI:

```bash
pip install --upgrade ceki-sdk --break-system-packages
```

## Get API key

1. Sign up at [ceki.me](https://ceki.me) — email only
2. Dashboard → API keys → create one
3. Export when ready to use:

```bash
export CEKI_API_KEY="your_key_here"
```

The skill does **not** transmit your API key during installation. Token verification is a separate, manual step.

## Quickstart

```bash
ceki search --limit 5
SID=$(ceki rent --schedule <schedule_id> | jq -r .session_id)
ceki navigate $SID https://my-app.example.com
ceki snapshot $SID -o /tmp/01.png
ceki click $SID 400 300
ceki type $SID "hello"
ceki stop $SID
```

## See also

- **[SKILL.md](./SKILL.md)** — full reference for AI agents using this skill
- **[examples/](./examples/)** — integration configs for Claude Desktop, Cursor, Cline
- **[ceki.me](https://ceki.me)** — marketplace dashboard, API key management
- **[ceki-sdk on PyPI](https://pypi.org/project/ceki-sdk/)** — Python SDK + CLI

## License

MIT. See [LICENSE](./LICENSE).
