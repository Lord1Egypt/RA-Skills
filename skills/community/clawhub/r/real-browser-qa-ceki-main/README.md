# RealBrowser QA by Ceki

[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/ceki-sdk?label=ceki-sdk)](https://pypi.org/project/ceki-sdk/)

> **Real Chrome sessions for QA testing and vulnerability discovery** — test your own sites with realistic user simulation, catch rendering bugs, timing issues, and security gaps that headless mode misses.

This is a thin client to the `ceki-sdk` CLI / Python SDK. It lets your QA agent open a real Chrome session and drive it — yours via the [Ceki extension](https://browser.ceki.me/install), or one rented from another opted-in user via the marketplace.

## Use cases

- **QA / E2E testing** of your own web apps with real browser fingerprints and interaction patterns
- **Security testing & vulnerability discovery** — test against real rendering, WAF rules, CSRF/CORS behaviour
- **Accessibility audits** — test with real rendering, keyboard navigation, screen reader compatibility
- **Cross-browser inconsistency detection** — run same test through different geo/IP/behavioural profiles
- **Synthetic monitoring** — heartbeat your own services through real browser sessions

## Three modes

| Mode | Where | Cost | Visibility |
|---|---|---|---|
| **Self** | Your own Chrome (Ceki extension) | Free for host_user == renter_user | Only you |
| **Marketplace** | Chrome contributed by another user who opted in to host | $0.01/min, USDC | The host can see your session |
| **Earn** (opt-in, off) | Your idle Chrome contributed back | 90% of session price | Other agents you allow |

## Use responsibly

Use this skill only on sites you own or have explicit authorization to test. See `SKILL.md` for appropriate and inappropriate use cases.

## Install

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
