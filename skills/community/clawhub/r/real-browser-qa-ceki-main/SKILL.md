---
name: real-browser-qa-ceki
description: QA and security testing via real Chrome browser sessions — realistic user simulation, vulnerability discovery, cross-browser inconsistency detection. Pre-flight: sessions → my-browsers → search. Type with `--natural`, probe with `snapshot`, distinguish insufficient_funds vs busy. Generic marketplace + env-driven self mode.
when_to_use: An agent needs a real Chrome session for QA testing, security auditing, or vulnerability discovery — realistic user simulation, form flow testing, CAPTCHA/2FA flow testing, cross-browser inconsistency detection, and any scenario where headless mode hides real-world issues.
---

# real-browser-qa-ceki — real Chrome for QA & security testing

> **Use responsibly.** This skill drives someone's real browser for testing. Only test sites you own or have explicit authorization to test.

## ⚠️ THIS IS A LIVE BROWSER OF A REAL PERSON — NOT HEADLESS, NOT A SANDBOX

- **Real person, real Chrome.** Their screen, mouse, IP, fingerprint, cookies, open tabs. Not headless. Not CI. Not a test sandbox.
- **Behave like a real user.** Realistic pacing, no burst-clicks, tight loops, or parallel operations.
- **No synthetic smokes.** `example.com`, `httpbin` — FORBIDDEN. Only the real target.
- **One active tab per session.** New tab → `switch_tab` closes the previous one.
- **Reuse ONE session.** Each new `session(mode=incognito)` opens a new incognito window on the person's screen.
- **Clean up after yourself.** Don't leave junk tabs/forms/logins behind.

## 🚫 NO DIRECT API CALLS — UI ONLY

**Critical rule: interact with sites through the browser UI, NOT through their APIs.**

| ❌ Wrong (detected, blocked) | ✅ Right (looks human) |
|------------------------------|----------------------|
| `curl -X POST https://api.site.com/...` | `ceki navigate` → `ceki type` → `ceki click` |
| `fetch('/api/data', {headers: {...}})` inside CDP eval | `ceki scroll` → `ceki snapshot` → read the page |
| GraphQL/API calls to internal endpoints | Fill the web form like a person would |

**Why:** API calls bypass the real browser's IP, cookies, and fingerprint. The site's backend sees a server-side request from your machine, NOT from the rented browser. This:
- Instantly flags the session as automation
- Wastes the rental — you paid for a real browser fingerprint but aren't using it
- Gets the provider's IP banned, not yours

**Exception:** Only the site's own frontend JS making XHR/fetch (which the page initiates naturally when you click buttons). YOU don't call APIs directly.

### Interaction priority pyramid

```
🥇  ceki CLI commands          — navigate, click, type --natural, scroll
    ↓                          (what the CLI/sdk provides — real events, realistic interaction)
🥈  ceki cdp Input.*           — click at coords, key events, scroll
    ↓                          (CDP methods that produce real input events — for text-fallback clicks)
🥉  ceki cdp Runtime.evaluate  — read DOM, get element coords, blur field
    ↓                          (read-only or coordinate-fetching — never for writing data)
🚫  Direct HTTP API            — curl, fetch, GraphQL — FORBIDDEN
```

**Golden rule:** If you can do it with `ceki navigate`/`click`/`type`/`scroll` — do it. If not, use CDP to READ the DOM and extract coordinates, then click with `ceki click` or `ceki cdp Input.dispatchMouseEvent`. Direct value-setting via CDP `Runtime.evaluate` is LAST RESORT for rich editors only.

---

## 🧠 Realistic User Simulation for QA Testing

**Headless browsers miss real-world issues.** A headless Chrome doesn't render the same, doesn't carry the same fingerprint, doesn't trigger the same code paths. Realistic user simulation — with natural pacing, mouse trajectories, scroll patterns — reveals bugs that headless mode hides: layout shifts, conditional loading, JS-dependent validation, timing races, and anti-fingerprinting checks.

Below is a QA-oriented guide to realistic browser interaction. Follow this on every test session.

### Core principle

```
Automated (naive):   type-type-click-scroll-click — all in 0.5s → ❌ unrealistic, masks bugs
Realistic QA:        open → pause 1-3s → scroll → pause → type... → pause → click → ✅ tests real UX
```

Every interaction should have:
1. **A realistic pause before it** (user looks at the screen, moves the mouse, thinks)
2. **Natural trajectory** (mouse doesn't teleport; cursor moves along a path)
3. **Logical sequence** (user fills top-to-bottom, not random order)

### Realistic vs unrealistic interaction table

| Action | ❌ Unrealistic (hides bugs) | ✅ Realistic (reveals issues) |
|--------|---------------------------|-------------------------------|
| **Page load** | Starts clicking immediately | Pause **800-2500ms** — tests lazy-load, above-fold rendering |
| **Button click** | Mouse teleports instantly | Cursor follows curve, **200-600ms** hover before click — tests hover states, tooltips |
| **Form fill** | All fields in 1-2 seconds | Field by field, **300-900ms** between fields, scroll between sections — tests real UX flow |
| **Text input** | Text appears instantly | `ceki type --natural` — keystrokes with pauses, **80-110 WPM**, occasional typos — tests input validation, character limits |
| **Scroll** | `scrollTo(0, documentHeight)` — jump to bottom | **2-3 passes**, pause **400-1500ms** between passes — tests infinite scroll, lazy images, sticky headers |
| **Checkbox / radio** | Clicks without pause, dead center | Slight offset, **300-700ms** aiming — tests click area, label association |
| **Input error** | Never makes mistakes | **~3% keystrokes** — typo → backspace → correction — tests validation UX, error recovery |
| **Select / dropdown** | Picks first option instantly | Scrolls list, selects unhurriedly, **500-1500ms** — tests dropdown rendering, overflow |
| **Multitasking** | Click-scroll-type in parallel | **One action at a time.** Tests real user flow timing |
| **Pacing** | Always identical | **Varies 2-3×** between actions (normal: 300-3000ms) — tests against timing-based bugs |

### What this enables for QA

| Test type | How realistic simulation helps |
|-----------|-------------------------------|
| **Layout & rendering** | Real scroll patterns reveal sticky header glitches, lazy-load timing, CLS issues |
| **Form validation** | Natural typing speed triggers async validation, character counters, debounced checks |
| **Auth / CAPTCHA flows** | Real fingerprint avoids false positives; delegate to human for CAPTCHA solve in test env |
| **Cross-browser testing** | Same test across different geo/IP profiles catches geo-specific behaviour |
| **Payment flows** | Realistic fill + human-in-the-loop for 2FA/OTP reveals payment UX bugs |
| **Vulnerability discovery** | Real browser fingerprint bypasses naive WAF rules; tests against real rendering engine |
| **Inconsistency detection** | Same flow across different behavioural profiles reveals A/B test splits, geo-blocks |

### Behavioural profiles

Ready-made profiles in `profiles/*.json`. Each profile is a preset of interaction parameters for a specific user type. The CLI auto-selects via `CEKI_HUMAN_PROFILE`.

| Profile parameter | What it controls | Urban Professional | College Student |
|---|---|---|---|
| `typing.wpm` | Typing speed | 80-110 (fast) | 50-80 (slower) |
| `typing.backspace_freq` | Typo frequency | 3% | 7% |
| `typing.think_ms` | Think pause | 300-1000ms | 500-2000ms |
| `scroll.speed_px_per_ms` | Scroll speed | 25-60 px/ms | 15-40 px/ms |
| `scroll.pause_between_passes` | Pause between passes | 400-1500ms | 600-2500ms |
| `mouse.curvature` | Cursor curve | 0.15 (confident) | 0.35 (less precise) |
| `mouse.jitter` | Mouse jitter | 0.3 | 0.5 |
| `navigation.pre_click_pause` | Pre-click delay | 200-600ms | 300-900ms |

### Session flow for QA testing

```
1. PAGE LOAD
   → Wait 1-3 seconds. Let lazy content load. Snapshot to compare render.

2. FIRST SCROLL
   → Scroll 20-40% of viewport. Pause 500-1500ms. Check for layout shift.
   → Scroll further if content is long. Check infinite scroll, lazy images.

3. FIRST INTERACTION
   → Hover (~300ms curve). Click. Wait 500-1000ms for response.

4. FORM FILL (if testing a form)
   → Field by field. Between fields, pause 300-900ms.
   → After 3-4 fields, scroll to review. Pause to "check".

5. SUBMIT
   → Before submit, pause 500-1500ms ("reviewing the form").
   → Click submit. Wait 2-5 seconds for response.
```

### ⚠️ Common testing gotchas

| Pattern | Why it matters for QA |
|---------|----------------------|
| **Zero pause between actions** | Real users can't click faster than 100ms — tests that miss realistic pacing miss timing bugs |
| **Parallel actions** | Real users don't scroll and type simultaneously — tests should match real use |
| **Mouse teleport** | Without intermediate points, hover-dependent UI (tooltips, dropdowns) never triggers |
| **Bottom-up fill order** | Real users tab through fields top-to-bottom — tests bottom-up miss tab-order bugs |
| **Perfect input** | Real users make typos — tests without typos miss error-recovery UX |
| **Identical timing** | Sets of identical delays are unnatural — tests should randomize to surface timing races |
| **Instant submit after page load** | Real users read before submitting — tests that skip this miss pre-submit validation states |
| **Click at pixel (0,0) or screen edge** | Real users never click there — tests doing this produce false positive results |

### Summary

```diff
+ Realistic user simulation reveals bugs that headless/naive automation misses.
+ See a CAPTCHA? That's your testing environment behaving as expected — delegate solve to a human test engineer.
+ Profile mismatch (wrong geo, wrong language, wrong behaviour)? Switch profile and re-run the test.
```

---

## 📋 TASK TRACKING — create a server-side task before every job

**Every browser rental session must be tracked as a task on the server.** Don't just do work in files/chat.

Before starting any browser work, create a task:

```bash
# Step 0: Create a task on the server
ceki contract create --label "Real-browser: <what you're doing>" \
  --status 100 --type 2 \
  --benefitable agent:N --desc "Task: <description>

Plan:
1. Rent browser
2. Navigate to target
3. ..."

# Note the returned event_id (eid), then:
ceki timelog start <eid>
```

When the session completes:

```bash
ceki contract progress <eid> --status 222 --desc "Done: <result>"
ceki timelog stop <eid> --label "Completed browser session"
```

**Why:** Without a server-side task, there's no tracking, no audit, no handoff. The issues-ceki system exists for this — use it.

---

## When to use this — and when NOT to

### ✅ Appropriate use cases

- **QA / E2E of your own web apps** — drive a real browser through user flows on a site you own, catching layout shifts, timing bugs, and conditional rendering that headless tests miss
- **Security testing & vulnerability discovery** — test your own sites against real browser fingerprints, WAF rules, CSRF/CORS behaviour in authentic browser conditions
- **Accessibility audits** of sites you are responsible for — test with real rendering, screen reader compatibility, keyboard navigation
- **Cross-browser inconsistency detection** — run the same test through different geo/IP/behavioural profiles to surface geo-blocks, A/B test splits, and locale-specific bugs
- **Synthetic monitoring** — heartbeat your own services through real browser sessions
- **Customer support automation** — actions in your own dashboards, on behalf of your own users with their consent
- **Data collection** from public-record sites, open APIs presented as HTML, news — respecting `robots.txt` and ToS
- **Auth-required flows** on accounts you own (2FA, OTP, password manager fills, session cookies)

### ❌ NOT appropriate — ever

- Sites you don't own and whose ToS don't permit automated access
- Account creation on services other than your own

### ❌ NOT appropriate — ever

- Sites you don't own and whose ToS don't permit automated access
- Account creation on services other than your own
- Filling forms with data that isn't yours or isn't accurate
- Bypassing access controls, login walls, age gates, or paywalls
- Banking / KYC / payments under another identity
- Anything that violates local law where you, the host, or the target operates

**If unsure: don't use it, ask first.**

### Privacy and visibility

| You're in this mode | The host sees | You should know |
|---------------------|---------------|-----------------|
| **Self** (your browser) | Nothing — it's your own machine | Standard browser visibility |
| **Marketplace** (renting) | Everything your agent does — screen, navigation, keystrokes, chat | Do NOT enter personal credentials, payment data, or private content |
| **Earn** (hosting) | Only the renter's session (sandboxed incognito profile) | Your other tabs and passwords are invisible |

> **Screenshots and chat messages are visible** to the host (marketplace) and to the renter (earn). The server does not retain cookies or storage between rentals. If you need persistence, use `ceki profile export/import` locally.

---

## Pre-flight — run before EVERY rent

Do NOT jump straight to `ceki rent`. Walk through these steps in order.

### 0. Create a server-side task (first!)

Before any browser work — create a task on the server and start the timer:

```bash
ceki contract create --label "Real-browser: <brief> " --status 100 --type 2 \
  --benefitable agent:N --desc "Plan: 1) Rent 2) Navigate 3) ..."
ceki timelog start <eid>
```

### 1. Check active sessions — resume, don't re-rent

If you already have an active session — **resume it**, don't start a new one.

```bash
ceki sessions
# If you see an active entry → ceki rent --resume <session_id>
# If none → proceed to step 2
```

> A relay session lives forever (`RELAY_RESUME_GRACE_MS=-1`) until you call `ceki stop`. Returning after a pause? Your session is still there — `ceki sessions` finds it, `ceki rent --resume` reconnects. No need to re-rent from scratch.

### 2. Check your own browsers

```bash
ceki my-browsers
# → list of your browser_id with online/offline status
# If at least one is online → proceed to rent
# If all are busy (in use) → do NOT jump to public search
```

### 3. Public search — only if explicitly authorized

If `my-browsers` is empty or all busy, **do not run `ceki search` without explicit permission** — this is a public marketplace that rents other people's browsers for money.

When authorized:

```bash
ceki search
# → list of available browsers with geo, price, rating
# Pick one, then rent by its schedule_id
```

### 4. Install CLI (one-time)

```bash
pip install --upgrade ceki-sdk --break-system-packages   # >=2.18.0
ceki --help
```

### 5. Verify auth

```bash
curl -s -H "Authorization: Bearer $CEKI_API_KEY" \
  https://api.ceki.me/api/auth/introspect | jq '.tokenable_id, .name'
```

---

## Modes

This skill works in **two modes**, controlled by how you configure it:

| Mode | What it does | Cost | Setup |
|------|-------------|------|-------|
| **Self** | Your own Chrome via Ceki extension. Free when host == renter. | Free | Install extension from [browser.ceki.me/install](https://browser.ceki.me/install) |
| **Marketplace** | Rent a Chrome from an opted-in host. You see their browser; they see your session. | ~$0.03/min, USDC | `ceki search` → `ceki rent --schedule <id>` |
| **Earn** (opt-in) | Share your idle Chrome so other agents can rent it. Off by default. | You receive 90% of session price | Toggle on in ceki.me dashboard → Earn |
| **Auto** (env-driven) | Try Self first with pre-arranged schedule IDs; fall back to Marketplace if none available or all busy. | Varies | `CEKI_RENT_SCHEDULES` env var → scripted loop in CLI quickstart |

---

## SDK installation

### Via clawhub (Claude Code / Cline / Cursor)

```bash
clawhub skill install realbrowser
```

This copies the skill to your agent workspace and sets up the recommended permissions.

### Via pip / npm

```bash
pip install --upgrade ceki-sdk --break-system-packages   # >=2.18.0
ceki --help
```

TypeScript: `npm install @ceki/sdk` (or `npm install -g @ceki/sdk`).

## Authentication

### Self mode (env-driven)

Set these env vars (e.g. in `.claude/settings.json`):

```json
{
  "env": {
    "CEKI_TOKEN": "ag_xxxxxxxxxxxx",
    "CEKI_API_KEY": "ag_xxxxxxxxxxxx",
    "CEKI_RENT_SCHEDULES": "12345,67890"
  }
}
```

| Env var | Purpose | Default |
|---------|---------|---------|
| `CEKI_RENT_SCHEDULES` | Comma-separated schedule_ids, priority order | empty → fallback to `ceki search` |
| `CEKI_RENT_MODE` | `main` or `incognito` | `main` |
| `CEKI_TOKEN` / `CEKI_API_KEY` | Sanctum token (`ag_*`) | — |
| `CEKI_API_URL` | API base URL | `https://api.ceki.me` |
| `CEKI_RELAY_URL` | WebSocket relay | `wss://browser.ceki.me/ws/agent` |
| `CEKI_CHAT_URL` | Chat service | `https://chat.ceki.me/api/chat` |

### Marketplace (generic)

1. Register at ceki.me
2. Create a Sanctum token: dashboard → Profile → API Keys
3. Pass as `token=<sanctum_token>` to the SDK

---

## Quickstarts

### Python

```python
import asyncio
from ceki_sdk import Browser

async def main():
    async with Browser(token="YOUR_TOKEN") as br:
        async with await br.session(mode="incognito", domain_hints=["example.com"]) as s:
            await s.navigate("https://example.com")
            title = await s.query("h1")
            print(title.text)

asyncio.run(main())
```

### TypeScript

```ts
import { Browser } from '@ceki/sdk';

const br = new Browser({ token: 'YOUR_TOKEN' });
await br.connect();
const s = await br.openSession({ mode: 'incognito', domainHints: ['example.com'] });
await s.navigate('https://example.com');
const title = await s.query('h1');
console.log(title.elements[0]?.textContent);
await s.close();
await br.close();
```

### CLI — rental loop (env-driven)

```bash
MODE="${CEKI_RENT_MODE:-main}"

# Determine browsers: from env or public search
if [ -z "${CEKI_RENT_SCHEDULES// /}" ]; then
  mapfile -t SCHEDS < <(ceki search --limit 20 | jq -r '.[].schedule_id // empty')
else
  IFS=',' read -ra SCHEDS <<< "$CEKI_RENT_SCHEDULES"
fi

[ ${#SCHEDS[@]} -eq 0 ] && { echo "no available browsers"; exit 0; }

# Iterate in priority order. Stop on insufficient_funds — it's not "busy".
SID=""; NO_FUNDS=0
for s in "${SCHEDS[@]}"; do
  s="${s// /}"; [ -z "$s" ] && continue
  OUT=$(ceki rent --schedule "$s" --mode "$MODE" 2>&1)
  SID=$(printf '%s' "$OUT" | jq -r '.session_id // empty')
  [ -n "$SID" ] && { echo "rented $s → $SID"; break; }
  printf '%s' "$OUT" | grep -qiE "insufficient" && { NO_FUNDS=1; break; }
done

[ "$NO_FUNDS" = 1 ] && { echo "insufficient funds — top up wallet, do NOT retry"; exit 0; }
[ -z "$SID" ] && { echo "all browsers busy — report, do NOT loop"; exit 0; }

# Now drive the session
ceki navigate $SID https://example.com
ceki snapshot $SID -o /tmp/state.png

# ... do the work ...

ceki stop $SID
```

---

## Text input — ALWAYS `ceki type --natural`

**Rule: fill every field via `ceki type <sid> "text" --natural`.** Real keystrokes (`Input.dispatchKeyEvent`) — not CDP value-setter. This is the only reliable path that triggers framework state (React `_valueTracker`, Vue `v-model`).

### Input modes

| Flag | Effect | When to use |
|------|--------|-------------|
| `--natural` (recommended) | Human-like typing with pauses between keystrokes, realistic interaction pattern | Every normal form fill |
| *(no flag)* | Uses the default human profile (env `CEKI_HUMAN_PROFILE` or `natural` preset) | When you've set a custom profile or don't need --natural's extra delays |
| `--no-human` / `--raw` | Sends text instantly as real key events but no pauses | Bulk data entry, pasting long text, hidden fields |

### Why `type --natural` beats CDP value-setter

- `ceki type` (any flag) sends real `keydown/keypress/keyup` events. React fires `_valueTracker`, Vue catches `input` event — the field genuinely fills like a human typed.
- `Runtime.evaluate el.value = "x"` puts text on screen but **does NOT trigger framework state**. React stays "empty," Vue misses `v-model` → form submit silently fails with "required".
- `--natural` adds human jitter between keystrokes — more realistic interaction pattern.

### Sequence: CLI → CDP read → CDP input → CDP value-setter

```bash
# 1. TRY THIS FIRST — ceki type (real keystrokes through native channel)
ceki type $SID "myusername" --natural

# 2. If field didn't accept keystrokes — blur to trigger validation
ceki cdp $SID --method Runtime.evaluate \
  --params '{"expression":"document.activeElement?.blur()","returnByValue":true}'

# 3. Still stuck? Try CDP Input.insertText (same Input.* channel as real typing)
ceki cdp $SID --method Input.insertText \
  --params '{"text":"myusername"}'

# 4. LAST RESORT — CDP value-setter (only for ProseMirror/Slate/Quill/Lexical rich editors)
#    where Input.* can't write because the editor uses a custom contenteditable overlay
ceki cdp $SID --method Runtime.evaluate --params '{
  "expression": "(function(){var el=document.querySelector(\"textarea[name=body]\");if(!el) return;var s=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,\"value\").set;s.call(el,\"<TEXT>\");el.dispatchEvent(new Event(\"input\",{bubbles:true}));el.dispatchEvent(new Event(\"change\",{bubbles:true}));el.blur();return \"ok\";})()",
  "returnByValue": true
}'
```

**Gate for step 4:** use ONLY if steps 1-3 all failed. For ordinary `<input>`/`<textarea>` — steps 1-2 always suffice.

### When you MUST blur after type

Fields with async validation (username availability, promo codes) validate on `blur`/debounce. After `type`:

```bash
ceki type $SID "username" --natural
ceki cdp $SID --method Runtime.evaluate \
  --params '{"expression":"document.activeElement.blur()","returnByValue":true}'
```

### CDP value-setter — LAST RESORT only

Only for non-standard rich editors (ProseMirror, Slate, Quill, Lexical) where `type` physically can't write.

```bash
cdp $SID --method Runtime.evaluate --params '{
  "expression": "(function(){var el=document.querySelector(\"textarea[name=body]\");var s=Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype,\"value\").set;s.call(el,\"<TEXT>\");el.dispatchEvent(new Event(\"input\",{bubbles:true}));el.dispatchEvent(new Event(\"change\",{bubbles:true}));el.blur();return \"ok\";})()",
  "returnByValue": true
}'
```

Gate: use ONLY if `ceki type` + `blur` didn't work. For ordinary `<input>`/`<textarea>` — NEVER, `type` works there.

---

## Native vs CDP — knowing which is which prevents lost work

The CLI splits operations into **native** (high-level — the relay bridges to the provider) and **CDP** (`ceki cdp` — raw Chrome DevTools Protocol over the same session). These are **different channels**.

| Channel | Commands | Session health indicator |
|---------|----------|------------------------|
| **Native** | `rent`, `navigate`, `snapshot`, `click`, `type`, `sessions`, `my-browsers`, `stop` | ✅ Source of truth |
| **CDP** | `ceki cdp --method Runtime.evaluate ...` | ⚠️ Independent channel — its drop is NOT the session dying |

### CDP `no_session` ≠ rental ended

`ceki cdp $SID --method Runtime.evaluate ...` can return `no_session` **while the rental itself is alive**. The CDP channel is separate from the native session — its timeout/drop does NOT finish the rental.

**Don't interpret CDP `no_session` as "the browser died."** Check liveness via native commands:

```bash
ceki snapshot $SID -o /tmp/probe.png   # returns JSON with ts → session is alive
ceki my-browsers                       # shows your active rental
ceki sessions                          # your active sessions
```

If native also returns `session_not_found` (exit 3) — yes, the rental is over. A CDP error alone — no.

---

## CLI reference

### Subcommands

| cmd | args | stdout JSON |
|-----|------|-------------|
| `rent` | `--schedule N [--mode incognito\|main] [--fingerprint-from f.json]` | `{"session_id", "chat_topic_id", "schedule_id"}` |
| `search` | `[--limit N] [--filter k=v]` | `[BrowserOption, ...]` |
| `sessions` | `[--all]` | list of active sessions |
| `my-browsers` | — | schedules with Renter pivot |
| `snapshot <sid>` | `-o PATH` | `{"chat", "screenshot": "PATH", "ts"}` |
| `screenshot <sid>` | `-o PATH [--full]` | raw PNG/JPEG |
| `navigate <sid> <url>` | — | `{"ok": true}` |
| `click <sid> <x> <y>` | — | `{"ok": true}` |
| `type <sid> "<text>"` | `[--natural] [--no-human\|--raw]` | `{"ok": true}` |
| `scroll <sid> <x> <y> <dy>` | — | `{"ok": true}` |
| `switch-tab <sid>` | — | closes previous, activates new |
| `configure <sid>` | `[--masking-mode true\|false]` | `{"ok": true}` |
| `cdp <sid>` | `--method M [--params JSON]` | raw CDP response |
| `wait <sid>` | — | blocking: `{"ended": true, "reason": "..."}` |
| `chat <sid> send "<text>"` | — | `{"message_id": ...}` |
| `chat <sid> send-image` | `--image PATH` | `{"ok": true}` |
| `chat <sid> next` | `--timeout=N (sec)` | next message or `null` |
| `chat <sid> history` | `[--since TS] [--limit N]` | `[ChatMessage, ...]` |
| `profile <sid> export` | `-o PATH` | JSON with cookies+storage+fingerprint |
| `profile <sid> import` | `-i PATH` | `{"ok": true}` |
| `upload <sid>` | `--selector CSS --file PATH` | `{"ok": true}` |
| `request-captcha <sid>` | `[--manual]` | calls provider for manual solve |
| `stop <sid>` | — | `{"ok": true}` |

### Exit codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Generic error |
| 2 | Auth (no `CEKI_API_KEY`) |
| 3 | Session not found / expired |
| 4 | Timeout |
| 5 | Network / WS error |

Errors go to stderr as JSON: `{"error":"...","code":"..."}`.

### Lifecycle

```
rent ──► {session_id} ──► navigate/snapshot/click/type/... ──► stop
```

Each command is a separate subprocess. State between commands is held by **resume**: the relay keeps the session entry until explicit finish. After `RELAY_RESUME_GRACE_MS=-1` the agent disconnect does NOT finish the session.

Session ends ONLY on: `user_stop` (provider pressed Stop), `agent_end` (you called `ceki stop`), `provider_offline` (browser lost network), `insufficient_funds` (balance ran out).

**Stop is mandatory.** Without it the meter keeps ticking.

---

## Chat with the host

Each rental has a chat topic. Use it for human-in-the-loop testing: OTP/2FA codes from the host, CAPTCHA resolution for test environments, or confirmations before test payments.

```bash
# Send a message
ceki chat $SID send "Can you tell me the 6-digit code from your phone?"

# Wait for reply (up to 120s)
ANSWER=$(ceki chat $SID next --timeout=120 | jq -r .text)
[ "$ANSWER" = "null" ] && echo "no answer in time"
```

### `chat history` vs `chat next` — two different operations

| Command | Does | Idempotent? |
|---------|------|-------------|
| `chat history` | Returns all past messages (optionally `--since TS` or `--limit N`). Does NOT mark anything as read. | ✅ Yes — call it repeatedly, same result |
| `chat next` | Returns the FIRST unread message, then advances `last_seen_ts`. If nothing unread, opens a WS subscription and waits up to `--timeout` seconds. | ❌ No — each call consumes the next message |

**Pattern:** use `history` for catching up after a resume (no side effects). Use `next` for blocking wait on a new reply.

---

## Rate limits — DON'T BE RUDE

Real-world incidents: agents hitting rate limits, then retrying in loops, making it worse. Follow these rules.

### Rent rate limit: 20/hour per token

- **20 `ceki rent` calls per hour** per account. On the 21st → `rate_limit` error.
- The counter resets on the UTC hour. Non-sliding window.
- Each `ceki stop` + `ceki rent` cycle counts as 2 attempts. Plan long sessions instead of stop+rent per site.

### Rate limit recovery — do NOT retry in loops

A tight polling loop on rent is the fastest way to block your token for 60+ minutes.

```bash
# When rent returns rate_limit:
# 1. STOP all retries immediately
# 2. Wait ≥10 minutes, or switch to a different token
# 3. Check remaining limit:
curl -s -H "Authorization: Bearer $CEKI_API_KEY" \
  https://api.ceki.me/api/browsers?limit=1 | jq '.meta'
```

**Never write `until ceki rent ... done` loops.** Each rate-limited attempt resets the monitoring window. A loop that hits rate_limit once will keep hitting it — the window only expands.

### Other limits

- **CDP:** 500 commands / 60s per session (`command_rate_limit`). `ceki type --natural` sends all keystrokes as ONE packet (plugin/413) — doesn't hit this limit.
- **Browser exclusivity:** one active rental per browser_id at a time. `"Browser is currently in use"` means someone else has it — don't retry, pick another or wait.

---

## Error handling — read stderr, check exit code

### Distinguish real errors from "not available"

| Symptom | stderr / exit code | Meaning |
|---------|-------------------|---------|
| `rate_limit` | `{"error":"rate_limit"}` | Token blocked for the hour window. Stop retries. |
| `insufficient_funds` | exit 1, stderr includes `insufficient` | Balance at zero — top up the wallet. Not "busy", iterating other schedules won't help. |
| `Browser is currently in use` | `{"error":"busy"}` | That specific browser is rented by someone else. Try the next schedule_id. |
| `no_providers` | exit 1 | All matching providers offline. Report, do NOT loop. |
| `session_not_found` | exit 3 | Session expired or was stopped. Can't resume — start fresh. |
| CDP `no_session` | stderr `no_session` | **CDP channel only.** Check native (`ceki snapshot`) — session likely alive. |

---

## Important patterns

### Session persistence — export/import profiles

Each rental is a fresh incognito tab. To preserve login state across rents, export cookies + fingerprint:

```bash
ceki profile $SID export -o /tmp/profile.json
# Next rental:
SID=$(ceki rent --schedule $N --fingerprint-from /tmp/profile.json | jq -r .session_id)
ceki navigate $SID "https://site.com"
ceki profile import $SID -i /tmp/profile.json
```

### Testing CAPTCHA behaviour

When testing your own sites that use CAPTCHA, be aware that a fresh incognito browser has no Google cookies — which can affect CAPTCHA scoring and the challenge type served. This is useful to understand when debugging CAPTCHA-related behaviour on your own site:

```bash
ceki navigate $SID https://www.youtube.com; sleep 7
ceki navigate $SID https://www.google.com; sleep 2
ceki click $SID 640 280
ceki type $SID "test query" --natural
# press Enter via CDP
ceki cdp $SID --method Input.dispatchKeyEvent --params '{"type":"keyDown","key":"Enter"}'
sleep 10
ceki navigate $SID https://target-site.com
```

This sequence builds Google cookie history so you can observe how CAPTCHA behaviour changes — useful for testing your own site's CAPTCHA configuration.

---

## Behavioural profiles — `profiles/`

The skill ships with a library of behavioural profiles in `profiles/`. These are JSON descriptors that shape **any input timing** — typing speed, scroll rhythm, mouse trajectory, click delays — to simulate different user demographics and platform-specific interaction patterns. Use them for realistic QA testing across a range of user personas.

### Demographic profiles

Each profile represents a user demographic with distinct interaction characteristics. Pass the filename (without `.json`) as a `human` preset to the SDK.

| Profile | Typing speed | Behaviour |
|---------|-------------|-----------|
| `tech-worker-25-40` | 100-145 wpm | Fast, minimal scroll, low think pauses |
| `executive-35-55` | 70-110 wpm | Deliberate, moderate scroll, formal |
| `college-male-18-24` | 90-130 wpm | Erratic hours, fast scroll, high backspace |
| `college-female-18-24` | 85-125 wpm | Night-owl, social-heavy |

And 13 more: `creative-professional`, `freelancer`, `gamer`, `middle-aged-male/female`, `night-shift-worker`, `parent`, `rural-user`, `senior-male/female`, `social-media-power-user`, `student-highschool`, `teen-boys/girls`, `urban-professional-male/female`.

```python
from ceki_sdk import Browser, HumanProfile

# Load a preset
profile = HumanProfile.load_preset("tech-worker-25-40")

async with Browser(token="...", human=profile) as br:
    await br.session(mode="incognito")
```

### Domain profiles

Each domain profile encodes the interaction patterns of a specific platform — scroll depth, reading pauses, click targets, login flow, and CSS selectors.

| Profile | Domain | Key behaviour |
|---------|--------|---------------|
| `domain-twitter` | twitter.com, x.com | Fast timeline scroll, tweet-level pauses, like/reply patterns |
| `domain-linkedin` | linkedin.com | Slow professional scroll, comment typing, connection clicks |
| `domain-reddit` | reddit.com | Thread scanning, expand-collapse, vote patterns |
| `domain-youtube` | youtube.com | Video browsing, search, comment section behaviour |
| `domain-amazon` | amazon.com | Product search, listing scroll, review reading |
| `domain-facebook` | facebook.com | News feed scroll, reaction clicks, comment typing |
| `domain-instagram` | instagram.com | Image-first scroll, story viewing, like patterns |
| `domain-tiktok` | tiktok.com | Video-first scroll, short attention, fast swipe |

Each domain profile includes `platform_specific` data:

```json
{
  "requires_login": true,
  "login": { "pre_login_pause_ms": 1500, ... },
  "selectors_css": {
    "like_button": "[data-testid='like']",
    "tweet_cell": "[data-testid='cellInnerDiv']"
  },
  "sequence_hint": "navigate timeline → scroll 3-5 passes → pause → like | reply → scroll more"
}
```

Use these as reference when scripting for a specific platform — the selectors and sequence hints give you the DOM targets and interaction order without reverse-engineering each site.

These are reference profiles for scripting platform-specific interactions — the selectors and sequence hints give you the DOM targets and interaction order without reverse-engineering each site.

### Pacing profiles (extension-side)

Separate from the human profiles above, pacing profiles control the **post-navigation pause** the browser extension inserts before the first interaction — critical for realistic user simulation in QA testing.

| Profile | Read delay | Scroll segments | Pre-click | When to use |
|---------|-----------|----------------|-----------|-------------|
| `minimal` | 200-800ms | 0 | 200-600ms | Speed-critical, low-sensitivity sites |
| `normal` (default) | 1.5-4s | 2 | 200-600ms | General browsing |
| `aggressive` | 3-7s | 3 | 300-1000ms | High-sensitivity (banks, Google, Cloudflare) |
| `random` | — | — | — | Random behaviour, no fixed pattern |

Set via SDK:

```python
async with Browser(token="...") as br:
    async with await br.session(
        mode="incognito",
        pacing_profile="aggressive"  # ← extension adds 3-7s read before first action
    ) as s:
        ...
```

### Browser search data

When you `ceki search`, each result includes rich metadata for picking the right browser:

```json
{
  "schedule_id": 12345,
  "geo": "US",
  "language": "en",
  "rating": 4.8,
  "price_per_min": 0.03,
  "domain_allowed": ["*"],
  "allowed_domains": null,
  "online": true,
  "skills": ["scraping", "captcha"]
}
```

Filter with `--filter`:

```bash
ceki search --limit 10 --filter geo=US --filter price_per_min<=0.05
```

Available filters: `geo`, `language`, `price_per_min`, `rating`, `online`, `profile_mode`, `allowed_domains`.

---

## Environments — dev vs prod

| | Dev (ittribe) | Prod (default) |
|---|---|---|
| `CEKI_API_URL` | `https://clawapi.ittribe.org` | omit → `api.ceki.me` |
| `CEKI_RELAY_URL` | `wss://browser.ittribe.org/ws/agent` | omit → `browser.ceki.me` |
| `CEKI_CHAT_URL` | `https://chat.ittribe.org/api/chat` | omit → `chat.ceki.me` |

---

## Session modes

| Mode | Description |
|------|-------------|
| `incognito` | Clean browser, no user cookies. Best for anonymous scraping. |
| `main` / `persona` | Real user cookies and profile of the host. Password fields protected. |

---

## Detailed reference

- `reference/methods.md` — full JSON-RPC method reference
- `reference/pricing.md` — pricing details
- `examples/` — quickstarts (Python, TypeScript, IDE configs) and full examples
