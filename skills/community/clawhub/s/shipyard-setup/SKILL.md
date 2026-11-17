---
name: setup
description: First-time Shipyard setup. Connects GitHub, Vercel and Supabase, stores keys safely, saves defaults. Use for "setup", "get started", "connect my accounts", "settings", or when new-app says setup is not done.
---

# Shipyard setup

> Part of the Shipyard plugin. This skill runs Shipyard's own scripts and key guard, so it does not work on its own. If it was installed by itself (for example through skills.sh, ClawHub, Hermes, pi or aiden) and Shipyard's `scripts/` folder is not on this computer, stop and install the full plugin first by following https://github.com/philipposk/shipyard/blob/main/INSTALL.md, then start again.

You are helping a beginner get ready to build and publish apps. Setup can be stopped and continued: progress is saved in `~/.shipyard/profile.json`, so if the usage limit hits, they just run `/shipyard:setup` again later.

## Rules (always)

- You do the work. Run the scripts and commands yourself. The student only clicks in a browser, signs up, and pastes keys into the keys file.
- Never ask the student to paste a key in the chat. Never read or print `~/.shipyard/secrets.env`. Only scripts read it, and they show names with a tick or a cross, never values.
- Plain English. Short steps. Say what to click and what URL to open. Explain any technical word in a few words.
- One question at a time. Tell them which answer you recommend.
- Check each step before moving on. Do not say "done" until the check passes.
- Do not spawn big groups of helper agents. If you use one (for example to look something up), give it a cheaper model than yours (Opus → `model: "sonnet"`, Sonnet → `model: "haiku"` for lookups only).

## Start

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/setup-status.mjs"`. It shows which steps are done and which is next. Continue from the next step. If everything is done, say so and offer the settings page.
2. If the student typed `settings` after the command, only run `node "${CLAUDE_PLUGIN_ROOT}/scripts/settings-page.mjs"`, tell them the page opened, and stop.
3. Tell them in two lines what setup does and that it takes about 45 to 90 minutes, mostly signing up. Money facts are in `references/accounts.md`; mention that everything needed to start is free.

For the exact clicks of each step, read `references/accounts.md` when you reach that step (not before). If something fails, read `references/troubleshooting.md`.

## Steps (ids in order)

After each step passes, run `node "${CLAUDE_PLUGIN_ROOT}/scripts/profile.mjs" step-done <id>`.

**1. `tools`** Why: Shipyard needs a few programs on the computer.
Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/check-tools.mjs"`. It checks Node 20 or newer, git, the GitHub tool (`gh`), `npx`, and the Playwright browser used for phone-size checks. It prints the exact install line for their system. Do not run installers that need an admin password; show the line and ask them to run it, then re-check. For the Playwright browser, run `npx playwright install chromium` yourself.

**2. `github`** Why: your app code is stored on GitHub.
If they have no account, they sign up at github.com. Run `gh auth login --web` and show them the code and page; they approve in the browser. Then run `gh auth setup-git`. Check with `gh auth status`. Save the user name: `profile.mjs set accounts.github.user <name>` and `profile.mjs set accounts.github.ok true`.

**3. `vercel`** Why: Vercel puts the app on the internet.
They sign up at vercel.com with "Continue with GitHub". Run `npx --yes vercel@64.3.1 login` (it opens a browser). Check with `npx --yes vercel@64.3.1 whoami`. Save `accounts.vercel.user`, `accounts.vercel.scope` (their team name if shown, otherwise the user name) and `accounts.vercel.ok true`.

**4. `supabase`** Why: Supabase holds the database and sign-in.
Sign up at supabase.com with GitHub. Create an access token at supabase.com/dashboard/account/tokens (any name). Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/secrets-init.mjs"`. It opens the keys file. They paste the token after `SUPABASE_ACCESS_TOKEN=`, save, close, and say "done". Then run `node "${CLAUDE_PLUGIN_ROOT}/scripts/secrets-check.mjs" --live`. When it shows a tick, find their organisation (the check output or the Supabase dashboard shows it; if there is only one, use it). Save `accounts.supabase.orgId` (the organisation's slug, the short name in the dashboard URL), `accounts.supabase.orgName` and `accounts.supabase.ok true`.

**5. `ai-keys`** (optional, can skip) Why: only needed if an app will use AI.
Explain: one key per app is best so costs are visible; set a monthly spend limit and an email alert when creating a key. Claude Pro and ChatGPT Plus do not include API credit. Free or cheap starters: OpenRouter (many models, some free), Groq (free tier, fast, also speech-to-text), Deepgram (speech-to-text, free starting credit). If they want it, they use the keys file again (`secrets-init.mjs`), then `secrets-check.mjs --live`. Skipping is fine: `step-done ai-keys`.

**6. `email`** (optional, can skip) Why: apps send password-reset emails through Resend.
Without their own domain, Resend can only email the account owner. Fine for now. Skip or add `RESEND_API_KEY` via the keys file.

**7. `stripe`** (optional, can skip) Why: for taking payments later. Test mode only, no real money. Skip unless they know they need it.

**8. `domain`** Why: a web address of their own.
Ask: no domain for now (apps get a free `name.vercel.app` address), or buy one later (about $10 to $15 a year at Cloudflare or Porkbun). Recommend "none for now". Save `domain.choice` (`none` or `buy`).

**9. `profile`** Why: so they are not asked again for every app.
Ask one at a time and save with `profile.mjs set`: name and contact email (`owner.name`, `owner.email`), country (`owner.country`), languages (`owner.languages`), default layout (`defaults.layout`: `bottom-nav` for phone-first apps, `sidebar` for tools, `top-nav` for site-like apps), whether apps should be installable on phones (`defaults.pwa`), and budget mode (`defaults.budgetMode`, recommended `true`).

**10. `habits`** Why: a few working habits make Claude Code cheaper and safer.
Show them the content of `${CLAUDE_PLUGIN_ROOT}/starter/CLAUDE.md`. Ask: "Add this to your global Claude settings file?" Only if they say yes, append it to `~/.claude/CLAUDE.md` (create the file if missing; never overwrite existing content).

## Finish

1. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/secrets-check.mjs"` and `node "${CLAUDE_PLUGIN_ROOT}/scripts/setup-status.mjs"` once more and confirm no required step is open.
2. Run `node "${CLAUDE_PLUGIN_ROOT}/scripts/settings-page.mjs"` to open their settings page.
3. Tell them to turn on updates: type `/plugin`, choose Marketplaces, choose shipyard, choose Enable auto-update.
4. Say what is next: `/shipyard:new-app`. Keep it to three lines.
