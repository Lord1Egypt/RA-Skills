# ClawHub listing copy (v0.1.0)

## Title (max ~60 chars)
**RealBrowser QA by Ceki — real Chrome for testing & security**

## Subtitle (~120 chars)
**Drive a real Chrome from your agent for QA testing and vulnerability discovery. Self mode (your own) is free, marketplace mode is $0.01/min in USDC.**

## Short description (~200 chars)
A thin client to the ceki-sdk CLI. Lets your AI agent open a real Chrome session — yours or one rented — for QA testing, security auditing, and vulnerability discovery on sites you own or have authorization to test.

## Long description (markdown allowed)

RealBrowser QA by Ceki is a skill that lets your AI agent drive a real Chrome browser session through the [ceki-sdk](https://pypi.org/project/ceki-sdk/) CLI for testing and vulnerability discovery.

Use it for QA / E2E testing of your own web apps, security testing with real browser fingerprints, accessibility audits, cross-browser inconsistency detection, and synthetic monitoring.

### Three modes

| Mode | Where | Cost |
|---|---|---|
| **Self** | Your OWN Chrome (after installing the [Ceki extension](https://browser.ceki.me/install)) | FREE when host_user == renter_user |
| **Marketplace** | A Chrome contributed by another user who opted in to host | $0.01/min, settled in USDC |
| **Earn** (opt-in, off by default) | Your idle Chrome contributed back to the marketplace | You receive 90% of session price |

### Use responsibly

Use only on sites you own or have explicit authorization to test.

### Install

```bash
pip install --upgrade ceki-sdk --break-system-packages
```

### Quickstart

```bash
ceki search --limit 5
SID=$(ceki rent --schedule <schedule_id> | jq -r .session_id)
ceki navigate $SID https://my-app.example.com
ceki snapshot $SID -o /tmp/01.png
ceki click $SID 400 300
ceki type $SID "hello"
ceki stop $SID
```

---

## Tags / keywords
`browser`, `qa`, `testing`, `security`, `vulnerability-discovery`, `ai-agent`, `chrome`, `e2e-testing`, `mcp`, `openclaw`

## Category
`browser` / `testing` / `security`

## License
MIT

## Author
iWedmak (GitHub)

## Links
- Homepage: https://ceki.me
- Repo: https://github.com/Ceki-me/real-browser-qa-ceki
- PyPI: https://pypi.org/project/ceki-sdk/
