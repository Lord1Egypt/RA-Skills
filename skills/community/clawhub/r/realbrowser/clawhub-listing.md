# ClawHub listing copy (v0.1.1)

## Title (max ~60 chars)
**RealBrowser by Ceki — real Chrome sessions for AI agents**

## Subtitle (~120 chars)
**Drive a real Chrome from your agent. Self mode (your own) is free, marketplace mode is $0.01/min in USDC.**

## Short description (~200 chars)
A thin client to the ceki-sdk CLI. Lets your AI agent open a real Chrome session — yours or one rented from another opted-in user — for tasks on sites you have authorization to operate on.

## Long description (markdown allowed)

RealBrowser by Ceki is a ClawHub skill that lets your AI agent drive a real Chrome session through the [ceki-sdk](https://pypi.org/project/ceki-sdk/) CLI.

Use it for tasks on sites where you have authorization to operate: your own web apps (QA / E2E testing), accessibility audits of sites you're responsible for, synthetic monitoring of your own services, customer-support automation in your own dashboards, public-data extraction within site Terms of Service.

### Three modes

| Mode | Where | Cost |
|---|---|---|
| **Self** | Your OWN Chrome (after installing the [Ceki extension](https://browser.ceki.me/install)) | FREE when host_user == renter_user |
| **Marketplace** | A Chrome contributed by another user who opted in to host | $0.01/min, settled in USDC |
| **Earn** (opt-in, off by default) | Your idle Chrome contributed back to the marketplace | You receive 90% of session price |

### Use responsibly

This skill enables real-browser automation. Use only on sites you own or have authorization to operate on. Do not use for tasks you would not be allowed to perform manually, do not violate site Terms of Service, and respect `robots.txt`. The skill does not enable anything you wouldn't be allowed to do manually — it just makes legitimate browser-based agent workflows feasible without the friction of a headless setup.

### Install

```bash
clawhub skill install realbrowser
```

### Use

```bash
SID=$(ceki rent --schedule <schedule_id> | jq -r .session_id)
ceki navigate $SID https://my-app.example.com
ceki snapshot $SID -o /tmp/01.png
ceki click $SID 400 300
ceki type $SID "hello"
ceki stop $SID
```

### What this skill is NOT

- Not a tool for account creation on third-party services
- Not a tool for circumventing site protections you don't have authorization to bypass
- Not a stealth or anti-detection library

It is a thin client over a real-browser marketplace. Real browsers behave like real browsers because they are real browsers.

---

## Tags / keywords
`browser`, `automation`, `ai-agent`, `chrome`, `qa`, `synthetic-monitoring`, `accessibility`, `marketplace`, `mcp`, `openclaw`

## Category
`browser` / `automation`

## License
MIT

## Author
iWedmak (GitHub)

## Links
- Homepage: https://ceki.me
- Repo: https://github.com/Ceki-me/realbrowser-skill
- Mirror (Codeberg): https://codeberg.org/cekibrowser/realbrowser-skill
- Issues: https://github.com/Ceki-me/realbrowser-skill/issues
- PyPI: https://pypi.org/project/ceki-sdk/

## Permissions declared
- `network.outbound`: api.ceki.me, browser.ceki.me, chat.ceki.me only
- `process.spawn`: `ceki` CLI binary only
- `filesystem.read`: `~/.ceki/sessions/`
- `filesystem.write`: `~/.ceki/sessions/`

## Why this skill is safe (compliance notes)

- **Open source** (MIT, github.com/Ceki-me/realbrowser-skill, Codeberg mirror)
- **No credential transmission during install** — install.sh installs the CLI and exits. The user generates and exports the API key separately, when ready to use.
- **No filesystem writes outside ~/.ceki/sessions/** — session state files only
- **Network outbound limited to ceki.me subdomains** (declared in manifest)
- **No process spawn beyond ceki CLI**
- **Self mode** does not transmit user's Chrome data to third parties — sessions are routed through Ceki's dispatcher only for agent task execution, and the server is stateless between rentals (cookies and storage live inside the rented Chrome and are discarded on session end)
- **Marketplace mode** explicitly warns that the host can see the session, with guidance to use Self mode for sensitive workflows
- **Earn mode** is off by default, opt-in, and runs in a sandboxed Chrome profile (other agents who rent your Chrome cannot see your other tabs, saved passwords, or local files)
