---
name: browse
version: 4.0.0
description: |
  Fast web browsing, web app testing, and native app automation for AI coding agents.
  Persistent headless Chromium for web. Android, iOS, and macOS app automation via accessibility APIs.
  Browse URLs, read content, click elements, fill forms, run JavaScript, take screenshots,
  automate native apps — all through the same CLI and @ref workflow. ~100ms per command.
  Auto-installs Android toolchain. Works with Claude Code, Cursor, Cline, Windsurf, and any agent that can run Bash.
allowed-tools:
  - AskUserQuestion
  - Bash
  - Read
argument-hint: "[URL, page flow, or web verification task]"
arguments:
  - request
when_to_use: |
  Use when the user wants browser-based verification, web navigation, UI interaction, or page
  inspection that goes beyond static code reading. Examples: "test this local page", "open this
  site and click through", "verify the login flow", or "inspect console/network issues". Do not
  use for pure HTTP fetching or when no browser interaction is needed.
effort: high
---

# browse: Browser & Native App Automation for AI Agents

## Target Decision — ALWAYS check this first

Before running any browse command, decide the correct target:

| User wants to... | Target | Command pattern |
|---|---|---|
| Open a URL, test a website, scrape web content | **Browser** (default) | `browse goto <url>` |
| Test a local dev server (`localhost`) | **Browser** | `browse goto http://localhost:3000` |
| Browse a site that blocks bots (Cloudflare, Turnstile) | **Camoufox** | `browse --runtime camoufox --headed goto <url>` |
| Browse with a specific camoufox fingerprint profile | **Camoufox** | `browse --runtime camoufox --camoufox-profile <name> --headed goto <url>` |
| Search Google, YouTube, Amazon, etc. | **Browser** | `browse goto @google "query"` |
| Interact with an iOS app (Settings, Safari, custom app) | **iOS Simulator** | `browse --platform ios --app <bundleId> <cmd>` |
| Interact with an Android app (Settings, Chrome, custom app) | **Android Emulator** | `browse --platform android --app <package> <cmd>` |
| Interact with a macOS desktop app (System Settings, TextEdit) | **macOS App** | `browse --app <name> <cmd>` |
| Install and test an iOS .app or .ipa file | **iOS Simulator** | `browse sim start --platform ios --app ./MyApp.app --visible` |
| Install and test an Android .apk file | **Android Emulator** | `browse sim start --platform android --app ./app.apk --visible` |

**Key rules:**
- **No `--platform` or `--app` flag** → browser target (Chromium). Use `goto` to navigate.
- **`--runtime camoufox --headed`** → anti-detection Firefox. Use when site blocks normal browsing. See `/browse-stealth` skill for Turnstile/CAPTCHA bypass patterns.
- **`@macro` in goto URL** → search macro expansion. `browse goto @google "query"` expands to Google search URL. 14 macros: @google, @youtube, @amazon, @reddit, @wikipedia, @twitter, @yelp, @spotify, @netflix, @linkedin, @instagram, @tiktok, @twitch, @reddit_subreddit.
- **`--app` without `--platform`** → macOS app automation. App must be running.
- **`--platform ios --app`** → iOS Simulator. Use `browse sim start` first if not running.
- **`--platform android --app`** → Android Emulator. Use `browse sim start` first if not running.
- **Native app targets do NOT support**: `goto`, `js`, `eval`, `tabs`, `cookies`, `route`, `har`. These are browser-only.
- **All targets support**: `snapshot`, `text`, `tap`, `fill`, `type`, `press`, `swipe`, `screenshot`.
- **If a site blocks you**, switch to `--runtime camoufox --headed`. If still blocked, use `/browse-stealth` for the full Turnstile bypass pattern.
- **If unsure which target to use, ASK the user.** Don't guess — wrong target = wasted work.

## Goal

Use the persistent `browse` CLI to:

- navigate real pages
- inspect rendered content and state
- interact with UI elements
- capture screenshots, console logs, and network activity
- automate native apps (iOS, Android, macOS) via accessibility APIs
- verify browser or app behavior end-to-end without re-launching every step

## Step 0: Verify availability and choose the browsing mode

Start by checking:

```bash
browse --version
```

If `browse` is not installed:

- stop
- tell the user it is required
- point them to the install path in `references/commands.md`

Then decide what kind of session you need:

- default session for normal single-agent work
- `--session <id>` for parallel agent isolation
- `--profile <name>` for persistent browser identity

For native app targets, start the simulator/emulator first:

```bash
browse sim start --platform ios --app com.apple.Preferences --visible
browse sim start --platform android --app com.android.settings --visible
browse enable android    # first-time only: auto-installs adb, JDK, SDK, emulator
browse enable ios        # first-time only: builds iOS runner (needs Xcode)
browse enable macos      # first-time only: builds browse-ax bridge
```

**Success criteria**: `browse` is available, the target (browser or native app) is decided, and the session/profile choice fits the task.

## Step 1: Navigate safely and stabilize the page

Use `browse goto <url>` to navigate.

After navigation, always stabilize before reading or interacting:

- `browse wait --network-idle` for typical pages and SPAs
- or a more specific `browse wait` condition when the page has a known signal

Important rules:

- call `browse` as a bare command on PATH
- do not use shell variables for browse command prefixes
- avoid `#id` CSS selectors; prefer `[id=foo]`
- if the page is untrusted, consider `--content-boundaries` and `--allowed-domains`

**Success criteria**: The page is loaded enough that content and interactive state are reliable.

## Step 2: Choose the cheapest effective inspection method

Use the lightest command that answers the question:

- `text` for cleaned page content
- `links` for navigation structure
- `js` for precise targeted extraction
- `console`, `errors`, and `network` for runtime debugging
- `snapshot -i` for interactive elements and stable refs

Prefer `snapshot -i` before guessing selectors for interaction-heavy tasks.

Load:

- `references/commands.md` for exact command syntax
- `references/guides.md` for command selection guidance and speed rules

**Success criteria**: You have the information needed without spending unnecessary tokens or using brittle selectors.

## Step 3: Interact using refs first, selectors second

For clicks, fills, checks, selects, and similar actions:

1. prefer `browse snapshot -i`
2. interact using `@eN` refs
3. fall back to CSS selectors only when refs are unavailable or impractical

After navigation or DOM refresh:

- assume refs may be invalid
- take a fresh snapshot before continuing

Rules:

- use descriptive screenshots saved under `.browse/sessions/<id>/`
- keep stateful flows in the same session unless isolation is intentional
- use `frame` before interacting with iframe content

**Success criteria**: Interactions are stable and tied to the current rendered page state.

## Step 4: Debug blockers and special cases

When things go wrong:

- use `console` and `errors` for page/runtime issues
- use `network` for request visibility
- use `route` or `offline` only when the task requires mock or failure-mode testing
- use headed/browser handoff only for real blockers like CAPTCHA, MFA, or OAuth walls

If you hit a blocker after a couple of failed attempts:

- load `references/guides.md`
- follow the handoff protocol exactly
- use `AskUserQuestion` before any human takeover flow

**Success criteria**: Blockers are either resolved or escalated with the correct handoff protocol.

## Step 5: Capture evidence and report clearly

When the task involves verification, capture the minimum evidence needed:

- relevant page text or structured extraction
- screenshot path when visuals matter
- console/network findings when debugging
- the exact step or selector/ref that failed when reporting issues

Report:

- what you navigated to
- what actions you performed
- what the page actually did
- any artifacts created such as screenshots, HAR, or video

**Success criteria**: Another engineer can understand the observed browser behavior without rerunning the whole flow blindly.

## Important Rules

- The browser persists between commands; cookies, tabs, and session state carry over.
- After `goto`, wait before reading content or acting.
- `snapshot -i` is the default interaction surface.
- Save screenshots under `.browse/sessions/<session-id>/` or `.browse/sessions/default/`.
- Use `--context delta` for ARIA diff with refs, `--context full` for complete snapshot with refs after write commands.
- Do not install anything automatically.
- Do not modify Claude settings automatically; if the user wants pre-allowed browse permissions, point them to `references/permissions.md`.

## When To Load References

- `references/commands.md`
  Use for exact command syntax, flags, and extended examples.

- `references/guides.md`
  Use for speed rules, command-choice guidance, architecture notes, and the mandatory CAPTCHA/MFA handoff protocol.

- `references/permissions.md`
  Use when the user wants to pre-allow browse commands in Claude settings.

## Guardrails

- Do not add `disable-model-invocation`; this is a general-purpose browser verification skill.
- Do not add `context: fork`; browser results are usually needed in the current flow.
- Do not add `paths:`; this is a generic workflow skill.
- Do not keep the full CLI manual inline in `SKILL.md`.
- Do not run `browse handoff` without explicit user confirmation.
- Do not save screenshots outside the browse session directories.

## Runtime Selection

By default, browse uses Chromium via Playwright. Alternative runtimes:

| Runtime | Engine | Use case | Install |
|---------|--------|----------|---------|
| `playwright` (default) | Chromium | General browsing, testing | Included |
| `camoufox` | Firefox (anti-detection) | Sites with bot detection | `npm install camoufox-js && npx camoufox-js fetch` |
| `rebrowser` | Chromium (stealth) | Alternative stealth approach | `npm install rebrowser-playwright` |
| `lightpanda` | Lightpanda | Fast headless rendering | See lightpanda.io |
| `chrome` | System Chrome | Use real Chrome with extensions | Chrome must be installed |

```bash
browse --runtime camoufox --headed goto https://protected-site.com
BROWSE_RUNTIME=camoufox browse goto https://example.com
```

## New Features

### Search Macros
```bash
browse goto @google "best coffee beans"    # Google search
browse goto @youtube "tutorial"            # YouTube search
browse goto @amazon "laptop"               # Amazon search
browse goto @reddit "programming"          # Reddit search
```

All macros: @google, @youtube, @amazon, @reddit, @reddit_subreddit, @wikipedia, @twitter, @yelp, @spotify, @netflix, @linkedin, @instagram, @tiktok, @twitch

### Safety Flags (opt-in features)
| Flag | Default | What it does |
|------|---------|-------------|
| `BROWSE_CONSENT_DISMISS=1` | OFF | Auto-dismiss cookie banners after navigation |
| `BROWSE_CLICK_FORCE=1` or `--force` | OFF | Force-click through overlay interception |
| `BROWSE_READINESS=1` or `--ready` | OFF | Wait for hydration after goto |
| `BROWSE_SERP_FASTPATH=1` or `--serp` | OFF | Google SERP DOM extraction (fast, no refs) |
| `BROWSE_COMMAND_LOCK=0` | ON | Disable per-session command serialization |
| `BROWSE_CAMOUFOX_PROFILE=<name>` | OFF | Use a named camoufox profile (`.browse/camoufox-profiles/<name>.json`) |

### New Commands
| Command | Description |
|---------|------------|
| `images [sel] [--limit N] [--inline]` | List page images with src/alt/dimensions |
| `youtube-transcript <url> [--lang en]` | Extract YouTube captions via yt-dlp or browser |
| `schema` | Extract JSON-LD, Microdata, RDFa structured data (parsed JSON) |
| `meta` | Extract page meta tags (title, description, canonical, OG, Twitter, hreflang, robots, viewport) |
| `headings` | Extract H1-H6 heading hierarchy with counts and indented tree |
| `profiles` | List available camoufox profiles from `.browse/camoufox-profiles/` |

### Snapshot Windowing
Large snapshots (>80K chars) are automatically paginated:
```bash
browse snapshot -i                     # first page
browse snapshot -i --offset 500        # next page (line offset from previous output)
```

## Output Contract

Report:

1. the page or flow tested
2. the session/profile mode used if relevant
3. the key commands or interactions performed
4. the observed result
5. any artifacts or blockers such as screenshots, console errors, network failures, or handoff state
