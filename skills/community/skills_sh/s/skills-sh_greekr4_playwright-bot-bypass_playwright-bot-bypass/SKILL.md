---
name: playwright-bot-bypass
description: This skill should be used when the user asks to "bypass bot detection", "avoid CAPTCHA", "stealth browser automation", "undetected playwright", "bypass Google bot check", "rebrowser-playwright", or needs to automate websites that detect and block bots.
version: 2.2.0
---

# Playwright Bot Bypass

Reduce bot detection using rebrowser-playwright + real headed Chrome. Passes fingerprint checkers (bot.sannysoft.com, areyouheadless) and avoids triggering CAPTCHAs on Google. **Not** a guaranteed bypass for CDP/runtime-aware enterprise bot managers — see "Detection Coverage" for measured results.

> **Authorized use only.** This is for QA, accessibility testing, and research on sites you own or are permitted to test. Respect each site's Terms of Service, `robots.txt`, and applicable law. Do not use it to bypass paywalls, abuse rate limits, or scrape against a site's stated wishes.

## How Detection Is Defeated (and by which layer)

Evasion comes from **three** layers, not one — most of it is the real browser, not hand-written JS:

| Detection Point | Standard Playwright (headless) | Defeated by |
|-----------------|--------------------------------|-------------|
| CDP / `Runtime.enable` leak | Present (headless tell) | **rebrowser + `REBROWSER_PATCHES_RUNTIME_FIX_MODE`** (auto-set) |
| `window.__pwInitScripts` (`isPlaywright`) | Present | **artifact strip** (init script deletes it every nav) |
| `navigator.webdriver` | `true` | **rebrowser** (reports `false`; we do NOT delete it — `undefined` is itself a tell) |
| WebGL Renderer | SwiftShader (software) | **`channel:'chrome'` + headed mode** (real GPU) |
| User Agent | Contains "HeadlessChrome" | **`channel:'chrome'`** (real Chrome UA) — no JS override |
| Canvas fingerprint | Software-rendered tell | **headed real Chrome** (genuine GPU canvas) — no JS noise |
| `navigator.plugins` | Empty array | **headed real Chrome** (genuine PluginArray) — no JS fake |
| `navigator.languages` | `['en-US']` only | **`locale` option** (native, worker-consistent — no JS getter) |

> **Why so little hand-written JS?** Across v2.1/v2.2 the old fake-PluginArray, canvas-noise, hardcoded-`hardwareConcurrency`, permissions-override, `webdriver` delete, and `navigator.languages` getter were all removed — every one created a *detectable inconsistency* (own-property tells, worker mismatches, `undefined` webdriver, an `Illegal invocation` crash). v2.2 keeps exactly **two** active measures: strip Playwright's `__pwInitScripts` artifact, and enable rebrowser's Runtime-fix. Everything else is the genuine, self-consistent real browser. Less faking = more consistent = harder to detect.

## Prerequisites

- **Node.js 18+** with ESM support (`.mjs` files)
- **Google Chrome** installed (not just Chromium)
- **Headed mode** required (`headless: false`) — no display = no stealth

Verify Chrome is installed:
```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
# Windows
"C:\Program Files\Google\Chrome\Application\chrome.exe" --version
# Linux
google-chrome --version
```

## Quick Start

### 1. Install

```bash
npm init -y && npm install rebrowser-playwright
```

### 2. Create `stealth-test.mjs`

```javascript
import os from 'node:os';
import path from 'node:path';

// Enable rebrowser's Runtime.enable fix BEFORE importing the library.
process.env.REBROWSER_PATCHES_RUNTIME_FIX_MODE ??= 'addBinding';
const { chromium } = await import('rebrowser-playwright');

const browser = await chromium.launch({
  headless: false,                                  // headed = real GPU/canvas
  channel: 'chrome',                                // real Chrome = real UA/WebGL/plugins
  args: ['--disable-blink-features=AutomationControlled']
});

// `locale` sets navigator.languages + Accept-Language natively & consistently.
const context = await browser.newContext({ locale: 'ko-KR' });

// The ONLY init script: strip Playwright's main-world signature. Touch NOTHING
// on navigator — the real browser's values are already genuine & consistent.
await context.addInitScript(() => {
  for (const k of Object.getOwnPropertyNames(window)) {
    if (/^__pw|pwInitScripts|playwright/i.test(k)) {
      try { delete window[k]; } catch {}
    }
  }
  if (!window.chrome) window.chrome = {};
});

const page = await context.newPage();

try {
  await page.goto('https://bot.sannysoft.com', { waitUntil: 'networkidle' });
  const out = path.join(os.tmpdir(), 'stealth-test.png');
  await page.screenshot({ path: out });
  console.log(`Screenshot saved: ${out}`);
} finally {
  await browser.close();
}
```

### 3. Run

```bash
node stealth-test.mjs
```

## Using the Template (Recommended)

The `scripts/stealth-template.mjs` provides a reusable factory with all patches pre-applied:

```javascript
import { createStealthBrowser, humanDelay, humanType, simulateMouseMovement } from './scripts/stealth-template.mjs';

const { browser, page } = await createStealthBrowser();

try {
  await page.goto('https://example.com');

  // Human-like mouse movement (avoids Cloudflare Turnstile)
  await simulateMouseMovement(page);

  // Human-like typing instead of instant fill
  await humanType(page, 'input[name="q"]', 'search query');
  await humanDelay(300, 800);
} finally {
  await browser.close();
}
```

### Template Options

```javascript
const { browser, context, page } = await createStealthBrowser({
  headless: false,             // Required for stealth (default)
  viewport: { width: 1280, height: 800 },  // Default
  locale: 'ko-KR',            // Browser locale (default)
  userAgent: null,             // Custom UA (optional; default = real Chrome UA)
  storageState: './session.json',  // Cookie persistence (optional)
  proxy: { server: 'http://proxy:8080' },  // Proxy (optional)
  noSandbox: false             // Opt-in --no-sandbox (Linux root/CI only; it's a bot signal)
});

// Save session for reuse
import { saveSession } from './scripts/stealth-template.mjs';
await saveSession(context, './session.json');
```

## What the Template Actually Does

The template (v2.2) keeps the active surface to exactly **two** measures:

| Measure | Why |
|---------|-----|
| Strip `window.__pwInitScripts` / `__playwright*` (init script, every nav) | Removes the deterministic `isPlaywright` signature detectors key on |
| `REBROWSER_PATCHES_RUNTIME_FIX_MODE=addBinding` (auto-set before import) | Hides the CDP `Runtime.enable` headless leak |

It touches **nothing** on `navigator`. Everything else is delegated to the **real browser** (`channel:'chrome'` + headed): genuine User-Agent, WebGL/GPU renderer, canvas fingerprint, `PluginArray`, self-consistent permission/hardware values, and (via the `locale` option) native worker-consistent `navigator.languages` + Accept-Language.

**Removed across v2.1/v2.2** (each was net-negative — faked values inconsistently with the real environment): fake `navigator.plugins`, canvas `getImageData` noise, hardcoded `hardwareConcurrency`/`deviceMemory`, `outerWidth/Height` offset, the permissions override (crashed with `Illegal invocation`), the `navigator.webdriver` delete (made it `undefined` — a tell), and the `navigator.languages` getter (own-property + worker-mismatch tells).

Launch arg: `--disable-blink-features=AutomationControlled`. `--no-sandbox` is **opt-in** (`{ noSandbox: true }`) — it is both a security risk and an automation signal, so it is off by default.

> Heavy SPAs (TikTok/IG/FB) may print non-fatal `[rebrowser-patches] cannot get world` warnings under `addBinding` mode — the page still loads. Switch to `REBROWSER_PATCHES_RUNTIME_FIX_MODE=alwaysIsolated` to silence them if needed.

## Scripts

- **`scripts/stealth-template.mjs`** — Reusable stealth browser factory (all examples import this)
- **`scripts/bot-detection-test.mjs`** — Verify bypass at bot.sannysoft.com

## Examples

- **`examples/stealth-google-search.mjs`** — Google search without CAPTCHA
- **`examples/ab-test.mjs`** — Side-by-side detected vs stealth comparison
- **`examples/stealth-twitter-scrape.mjs`** — Twitter/X profile scraping

> **Note**: `ab-test.mjs` requires both `rebrowser-playwright` AND `playwright`:
> ```bash
> npm install rebrowser-playwright playwright && npx playwright install chromium
> ```

All screenshots are saved to the OS temp directory (`os.tmpdir()`) — `/tmp` on macOS/Linux, `%TEMP%` on Windows.

## Detection Coverage (measured 2026-06-10, macOS headed Chrome, v2.2)

Honest, tested results. v2.2's artifact-strip + Runtime-fix flipped every fingerprint/automation detector to **pass**:

| Detector | Result | Note |
|----------|--------|------|
| bot.sannysoft.com | ✅ all green | webdriver `false`, real WebGL/UA/plugins |
| arh.antoinevastel.com/bots/areyouheadless | ✅ "not Chrome headless" | |
| hmaker.github.io/selenium-detector | ✅ "Passing" | no chromedriver |
| **bot-detector.rebrowser.net** | ✅ **0 red** | `__pwInitScripts` stripped, no Runtime leak, webdriver `false` |
| **deviceandbrowserinfo.com/are_you_a_bot** | ✅ **"You are human!"** | `isBot:false`, `isPlaywright:false` |
| **browserscan.net/bot-detection** | ✅ **"Normal"** | CDP test passes (Runtime-fix) |
| **iphey.com** | ✅ **"Trustworthy"** | was "Unreliable" before v2.2 |
| creepjs | ✅ 0% headless / 0% stealth | fuzzy "38% like headless" is not a detection |
| nowsecure.nl (Cloudflare Turnstile) | ⚠️ interactive challenge shown | behavioral/IP gate — not a fingerprint check; not auto-passed |

Reliability: **9/9** repeat runs clean (the `__pwInitScripts` strip held across every navigation).

### How v2.2 achieves this (and the one thing it can't fix)

Two levers, both built into `createStealthBrowser()`:
1. **Artifact strip** — an init script deletes `window.__pwInitScripts` / `__playwright*` (the deterministic `isPlaywright` signature) on every navigation.
2. **`REBROWSER_PATCHES_RUNTIME_FIX_MODE=addBinding`** — set automatically before import; hides the CDP `Runtime.enable` leak.

**The residual leak:** `window.__playwright_builtins__` is a separate, **non-configurable** Playwright global that cannot be deleted or redefined. None of the detectors above key on it today, but a future detector could. No rebrowser version (you're on the latest, 1.52.0) removes it — tracked upstream in [rebrowser-patches#110](https://github.com/rebrowser/rebrowser-patches/issues/110), open with no fix.

> **Takeaway:** clean against fingerprint + automation-framework detection. Still **not** a guaranteed bypass for behavioral/IP systems (Cloudflare Turnstile, DataDome, Kasada) or login walls. For those, add residential IPs + real interaction, or switch engines — **patchright** (drop-in) or **nodriver** (structurally avoids the whole CDP/automation-protocol class).

### Real community sites (single logged-out load, residential IP, 2026-06-10)

Tested whether real sites bot-block a v2.2 page load (NOT a login judgment):

| Site | Result |
|------|--------|
| Reddit, YouTube, Pinterest, Threads, X (direct URL), Quora, **TikTok** | 🟢 content fully loaded — no bot challenge, no CAPTCHA |
| **Instagram, Facebook, LinkedIn** | 🟡 content shell loads behind the **standard logged-out login modal** — NOT a bot block / checkpoint / HTTP 999 |

**Key result:** none returned a bot challenge or hard block. The "hardest" sites (IG/FB/LinkedIn) served the *normal logged-out human experience* (a login modal over visible content), which means the stealth passed as a real user. **Caveat:** this is one load each on a clean residential IP. At volume, IG/FB/LinkedIn enforce `datr`-cookie aging, HTTP 999, and rate limits — those are IP/account problems, not fingerprint problems, and this skill does not address them. TikTok's signed-API actions (beyond profile view) also still need a warmed session.

## Limitations

- Requires `headless: false` (headed mode with display)
- Needs real Google Chrome installed (`channel: 'chrome'`)
- Some sites may still detect based on behavior patterns — use `humanDelay`, `humanType`, `simulateMouseMovement`
- Does not bypass CAPTCHAs, only prevents triggering them
- TLS/JA3 fingerprint is handled by `channel: 'chrome'` (uses real Chrome binary)
- `__pwInitScripts` leak (see Detection Coverage) is unfixable at the skill level — it's inherent to rebrowser-playwright 1.52.0

## Python Support

### undetected-chromedriver (Recommended)

```bash
pip install undetected-chromedriver
```

```python
import undetected_chromedriver as uc

# Match your Chrome version: check chrome://version
driver = uc.Chrome()  # auto-detects version

driver.get("https://www.google.com")
search_box = driver.find_element("name", "q")
search_box.send_keys("your search query")
search_box.submit()
```

> Python `playwright-stealth` only patches at JS level — WebGL still shows SwiftShader. Use `undetected-chromedriver` instead.

### Alternative: Call Node.js from Python

```python
import subprocess
result = subprocess.run(['node', 'stealth-script.mjs', query], capture_output=True)
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ERR_MODULE_NOT_FOUND` | Run `npm install rebrowser-playwright` in the same directory as your script |
| Browser not opening | Verify Chrome is installed (see Prerequisites) |
| WebGL shows SwiftShader | You're effectively headless / GPU-less. Run **headed** (`headless: false`) with `channel: 'chrome'` on a machine with a real GPU; SwiftShader is the software fallback, not an import issue |
| Still getting detected | Add `simulateMouseMovement()` and `humanDelay()` between actions |
| Process hangs | Ensure `browser.close()` is in a `finally` block |
| `SyntaxError: await` | File must be `.mjs` or have `"type": "module"` in package.json |
