---
name: tracwell
description: Add Tracwell analytics to a website or app and read its reports with the tracwell CLI. Use when the user wants analytics, page views, signups, funnels or revenue tracking set up, or asks which pages, sources or campaigns bring visitors, signups or money.
metadata:
  openclaw:
    homepage: https://tracwell.app/docs/cli
    requires:
      bins:
        - npx
    envVars:
      - name: TRACWELL_API_KEY
        required: false
        description: API key for headless use. Without it, `npx tracwell@0.6.2 login` signs in through the browser.
---

# Tracwell

Tracwell is product analytics for websites and apps. The `tracwell` CLI signs
in, adds a website, prints the install snippet, checks that events arrive, and
reads reports. Every command prints JSON. Commands pin the CLI version this
skill was written for; keep the pin so a newer release cannot run unreviewed.

## Quick start

```sh
npx tracwell@0.6.2 init --url https://acme.com
```

`init` signs in if needed, finds or adds the website, saves it as the default,
prints the install snippet, and installs this skill plus a short block in
`AGENTS.md`. Then do step 3 and step 4 below. The steps below are the same
thing one command at a time.

## 1. Sign in

```sh
npx tracwell@0.6.2 login
```

This opens the browser. The user signs in, picks websites and approves what
the CLI may do. Wait for them; do not try to complete the page yourself.
Ticking "Add websites" is needed for step 2.

Without a browser (CI, remote shells), ask the user for an API key from
Tracwell Settings → API & MCP and set `TRACWELL_API_KEY`. Keys can read reports
but cannot add websites.

## 2. Add the website

Skip this if `npx tracwell@0.6.2 sites` already lists it.

```sh
npx tracwell@0.6.2 sites add "Acme" https://acme.com
npx tracwell@0.6.2 use <website-id>
```

`use` saves the website so later commands do not need `--site`.

## 3. Install the snippet

The snippet sends page views and events from the site's visitors to Tracwell.
Tell the user this before adding it, and add it only to sites they own.

```sh
npx tracwell@0.6.2 snippet
```

Put the returned script tag in the site's `<head>` on every page, or use the
npm setup it returns for apps built with a bundler. Do not invent a project
key; always use the one from `snippet`.

## 4. Verify

Deploy or run the site, open a page, then:

```sh
npx tracwell@0.6.2 verify
```

`waiting` means no event has arrived yet. `receiving` means it works.

## 5. Read reports

Reports default to the last 7 days (UTC). Use `--days 30`, or `--from` and
`--to` as `YYYY-MM-DD`.

```sh
npx tracwell@0.6.2 overview
npx tracwell@0.6.2 acquisition --days 30
npx tracwell@0.6.2 revenue
npx tracwell@0.6.2 events
npx tracwell@0.6.2 funnels
```

## 6. Track what matters

Needs "Manage goals and funnels" approved at sign-in. Check with `--dry-run` first.

```sh
npx tracwell@0.6.2 goals add "Signed up" --event signup_completed --category signup
npx tracwell@0.6.2 goals add "Viewed pricing" --page /pricing
npx tracwell@0.6.2 funnels add "Checkout" --steps /pricing,event:checkout_started,event:purchase_completed
```

Steps starting with `/` are pages; `event:name` (or a bare name) is an event.
Only use event names that `npx tracwell@0.6.2 events` shows, or that you just added
to the code. Then read them with `npx tracwell@0.6.2 goal --goal-id <id>` or
`npx tracwell@0.6.2 funnel --funnel-id <id>`.

## More

- `npx tracwell@0.6.2 help <command>` lists a command's arguments, read live from Tracwell.
- `npx tracwell@0.6.2 search <words>` finds a tool; `npx tracwell@0.6.2 tools` lists them all.
  Run any of them with `npx tracwell@0.6.2 call <tool> --arg value`.
- Add `--dry-run` to see the tool and arguments without sending, before any write.
- Track custom events (signups, purchases) with `window.tracwell?.track("signup_completed")`.
  Docs: https://tracwell.app/docs
- Exit codes: 0 ok, 1 request failed, 2 bad input, 3 sign-in needed (run `login`).
