# Wayve CLI — Setup Guide

## 1. Install the CLI

Install the Wayve CLI globally:

```bash
npm install -g @gowayve/wayve-cli
```

Or use without installing:

```bash
npx @gowayve/wayve-cli
```

## 2. Create a Wayve Account

1. Go to [gowayve.com](https://gowayve.com) and sign up
2. Verify your email via the OTP code you receive
3. Go to [gowayve.com/account](https://gowayve.com/account) → **API Keys** section
4. Generate a new key and copy it — it starts with `wk_live_`

## 3. Add Your API Key

Set your API key as an environment variable:

```bash
export WAYVE_API_KEY=wk_live_your_key_here
```

To persist it, add the export line to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.).

Alternatively, use interactive login:

```bash
wayve auth login --email you@example.com
```

## 4. Verify

Run:

```bash
wayve auth status
```

Then type `/wayve help` to see available commands.

## 5. Get Started

- `/wayve setup` — first-time onboarding (create life pillars, set preferences)
- `/wayve plan` — plan your week
- `/wayve brief` — today's schedule
- `/wayve wrapup` — end-of-week reflection
- `/wayve time audit` — track where your time goes
- `/wayve life scan` — deep life review

## 6. Automations (Optional)

Set up server-side push notifications for proactive check-ins:
- Morning daily briefs
- Sunday wrap-up reminders
- Monday fresh start nudges
- Mid-week pulse checks
- Frequency alerts

Delivery via Telegram, Discord, Slack, email, or pull (shown at session start).

Say "set up automations" and Wayve will walk you through choosing a delivery channel and creating a bundle. See `references/automations.md` for full details.

## Troubleshooting

**"wayve: command not found":** Install the CLI globally with `npm install -g @gowayve/wayve-cli`, or use `npx @gowayve/wayve-cli` to run without installing. Make sure Node.js 18+ is installed (`node --version`).

**"Invalid API key":** Keys must start with `wk_live_`. Generate a new one at [gowayve.com/account](https://gowayve.com/account).

**Key not being picked up:** Check that your environment variable is set by running `echo $WAYVE_API_KEY`, or run `wayve auth status` to see if the CLI can find valid credentials. If using a shell profile, make sure you've reloaded it (`source ~/.bashrc` or `source ~/.zshrc`).
