# Win11 Visible Browser Automation

Control a visible Windows 11 Edge/Chrome browser from OpenClaw running in WSL2 via CDP.

Use this skill when the agent should work in the same visible browser environment a human can watch and take over: existing tabs, cookies, logins, browser state, and manual help for login, captcha, 2FA, approvals, or file dialogs.

## Requirements

- OpenClaw Gateway running in WSL2/Linux.
- Windows 11 with Microsoft Edge or Google Chrome.
- Browser CDP reachable from WSL through a restricted Windows relay/portproxy.
- `curl`, `ip`, and `openclaw` available in WSL for diagnostics.

## Install

After publication, install with the published owner namespace:

```bash
clawhub install <author>/win11-visible-browser
```

## Example requests

- “Fix OpenClaw browser control from WSL to my visible Windows Edge.”
- “Use my Win11 browser so I can watch and handle login/2FA manually.”
- “Diagnose why my OpenClaw `win-edge` browser profile cannot connect to CDP.”

## Safety

CDP gives remote control of the browser profile. Keep it restricted to WSL/Hyper-V, never expose it to LAN/Internet, prefer a dedicated profile, and require explicit user approval for personal profiles, sensitive external actions, firewall/config changes, and persistent Scheduled Tasks.

Existing user tabs are user state: do not close, reload, navigate, or repurpose them without explicit permission. For heavy browsing tasks, estimate browser cost first and avoid tab fan-out. Save useful URLs into project files instead of keeping many tabs open.

## Browser budget check

Before non-trivial visible-browser work, run the read-only helper:

```bash
scripts/browser-budget-check.sh win-edge
```

It reports CDP target counts, domains, reCAPTCHA/worker pressure, Linux memory, Edge process memory when available, and a simple `OK / CAUTION / STOP` verdict.
