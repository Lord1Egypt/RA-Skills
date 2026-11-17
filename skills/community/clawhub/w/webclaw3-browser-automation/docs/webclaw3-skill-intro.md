# Inside the webclaw3 skill

**English** | [中文](./webclaw3-intro.zh-CN.md)

This page is for people who want to know what the skill actually is under the hood. For the product story and usage, see the [README](../README.md).

## What it is

webclaw3 ships as a single self-contained skill (repo name: `webclaw3`, installed as `~/.claude/skills/webclaw3`). It has two parts:

- **`SKILL.md`** — the browsing philosophy and operating guidance the agent reads: goal-driven navigation, verify-as-you-go, adapt when a path is blocked. Skill = philosophy + technical facts, not a runbook; it explains tradeoffs and lets the agent reason.
- **`scripts/`** — the connection layer that actually reaches your browser. Without it the skill can think but not act.

## Dual channels to one real Chrome

Both channels drive the same real Chrome with equivalent capability; the skill picks automatically.

| Channel | Script | Role |
|---|---|---|
| Extension Relay | `scripts/relay.mjs` | **Default.** Bridges to the [wc3-chrome](https://github.com/fatmind/wc3-chrome) MV3 extension (HTTP :3459 ↔ WebSocket ↔ extension). |
| CDP fallback | `scripts/cdp-proxy.mjs` | **Fallback.** Talks to Chrome DevTools Protocol directly (HTTP :3456 ↔ :9222), used when the extension channel is entirely unavailable. |

`scripts/webclaw3.mjs` starts/stops both and runs the `doctor` health check that the agent calls when you say "check my webclaw3 environment". The actual execution inside the page is done by the wc3-chrome extension (L0); this skill depends on it but carries its own connection scripts, so it runs standalone.

## Capabilities

| Capability | What it means |
|---|---|
| **Dual-channel reach** | Extension Relay first, CDP fallback; same Chrome, equivalent capability |
| Autonomous tool selection | WebSearch / WebFetch / curl / browser relay, chosen per scenario |
| **Aria-tree semantics** | Compressed semantic tree (~500 lines vs ~10,000 lines of DOM) — the whole page at low token cost |
| **Aria semantic interaction** | `page.click` / `page.fillForm` locate by `ref_N`, resilient to site redesigns |
| **`page.eval` arbitrary JS** | Reaches through Shadow DOM / iframe / SPA data layers |
| Parallel divide-and-conquer | Multi-target tasks fan out to parallel sub-agents |
| Media extraction | Pull image/video URLs from the DOM, or analyze video via frame captures |

## Deeper references

- Browsing philosophy: [SKILL.md](../SKILL.md)
- Setup details: [references/setup.md](../references/setup.md)
- CDP fallback: [references/cdp-fallback.md](../references/cdp-fallback.md)
- Repair playbook: [references/repair.md](../references/repair.md)
