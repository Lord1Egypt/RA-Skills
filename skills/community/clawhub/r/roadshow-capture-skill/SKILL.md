---
name: roadshow-capture
description: "Automated roadshow/investor presentation capture to PDF. Playwright-powered, supports NetRoadShow and DealRoadShow."
version: 1.3.0
metadata:
  hermes:
    tags: [roadshow, netroadshow, dealroadshow, capture, pdf, playwright, finsight]
    related_skills: [browser-tools]
  openclaw:
    requires:
      bins: [python3]
      env:
        - NRS_EMAIL
    install:
      - kind: pip
        packages: [playwright, pillow]
---

# RoadShow Capture

Automatically opens roadshow links, handles authentication, captures every page as a screenshot, and compiles them into a single PDF. Supports **NetRoadShow** and **DealRoadShow**.

**Principle: Use Playwright directly, NOT Camofox.** Camofox has serious limitations on roadshow platforms (hash routing encoding, popup blocking, reCAPTCHA, Angular sandbox). Playwright handles everything Camofox can't.

---

## Unified Entry Point

`scripts/roadshow-capture.py` auto-routes by URL domain:

```bash
# Auto-detects platform — no need to pick the right script
python roadshow-capture.py --url "https://www.netroadshow.com/nrs/home/#!/?show=SHOW_ID"
python roadshow-capture.py --url "https://dealroadshow.com/e/MTNA2026"
```

Supported: `netroadshow.com` → NetRoadShow flow, `dealroadshow.com` → DealRoadShow flow.

---

## First-Time Setup (Email Configuration)

1. Tell the agent your roadshow email
2. It writes to `scripts/.env`:
   ```
   NRS_EMAIL=your-email@your-company.com
   ```
3. No further prompts needed

If `NRS_EMAIL` is unset, the agent will prompt once and save it to `.env`. No need to set environment variables manually.

---

## NetRoadShow Workflow

Script: `scripts/netroadshow-capture.py`  
URL format: `https://www.netroadshow.com/nrs/home/#!/?show=SHOW_ID`

### Verified Flow (KODIT Audio Roadshow Plus, 32 slides, 2026-05-12)

```
1. browser.goto(show_url)
   → Angular SPA routing works natively, no hash fix needed
   → URL auto-rewrites to /nrs/home/?show=SHOW_ID

2. page.locator("#homeEmailInput").first.fill(email)
   with page.expect_popup() as info:
       page.get_by_text("Launch Show").click()
   pp = info.value  ← MUST use expect_popup(), NOT page.on("popup")

3. Popup → /presentation/v2/{id}/disclaimer/
   Agree button is <div class="disclaimer-btn btn-agree">, NOT <button>
   ✅ pp.evaluate('document.querySelector(".btn-agree").click()')
   ❌ page.get_by_text("Agree").click() — doesn't trigger

4. "Resume previous session" / "Start from beginning" prompt
   Always pick "Start from beginning" (hard rule, no user prompt)

5. URL → /presentation/v2/{id}/MediaSlides

6. ArrowRight × (N-1) → screenshot → Pillow compose PDF (must use format='PDF')
```

### URL State Machine

```
/home/#!/?show=SHOW_ID    →  Email input page
   ↓ Fill email → Launch Show (expect_popup)
/home/?show=SHOW_ID        →  Popup opens
   ↓ Popup
/presentation/v2/{id}/disclaimer/  →  Legal disclaimer (div button)
   ↓ Agree (JS evaluate)
/presentation/v2/{id}/disclaimer/  →  Resume / Start from beginning
   ↓ Start from beginning (always)
/presentation/v2/{id}/MediaSlides  →  Slide viewer
   ↓ ArrowRight × capture
   PDF compose
```

### NetRoadShow-Specific Pitfalls

| Pitfall | Solution |
|---------|----------|
| Popup/new window | `expect_popup()` blocking wait |
| `div` button (not `button`) | `page.evaluate('.btn-agree').click()` |
| Hash routing `#!/?show=X` | Playwright handles natively |
| Session taint after failure | Fresh browser context: homepage → fake entry code → Continue → recover |
| Password login blocked | Email-Only flow (corporate email domain verified) |

---

## DealRoadShow Workflow

Script: `scripts/dealroadshow-capture.py`  
URL format: `https://dealroadshow.com/e/XXXXXXXX`

### Verified Flow (ArcelorMittal USD Bond, 32 slides, 2026-05-13)

```
1. browser.goto(deal_url)
   → dealroadshow.com 302 redirects to finsight.com/login/investor/e/XXXX
   → May show Cookie banner → page.get_by_role("button", name="Ok").click()

2. Fill email + Launch Deal Roadshow
   page.locator("input[type='email']").first.fill(email)
   page.get_by_text("Launch Deal Roadshow").click()
   → ~3-4s later form submits, navigates from /login/ to /e/XXXX (disclaimer)
   ⚠ During these 3-4s, DO NOT call page.evaluate() (context gets destroyed)

3. I Agree — MUST use Playwright locator, NOT evaluate
   ✅ page.locator("button:has-text('I Agree')").first.click(timeout=10000)
   ❌ page.evaluate('...click()')  ← clicks but doesn't trigger navigation

4. Wait for slides to load (fixed sleep, NOT networkidle)
   Current page: input[data-test="currentSlideInput"] value attribute
   Total pages: "of N" in body_text (r'\bof\s*(\d{1,4})\b')

5. ArrowRight × screenshot → poll input value for increment → no change = last page
   Pillow compose PDF (must use format='PDF')
```

### DealRoadShow Key Points

- **No popup**: All navigation stays in the same page, no `expect_popup()` needed
- **I Agree button**: Must use Playwright locator `.click()`, NOT `page.evaluate()` (JS click doesn't trigger navigation)
- **Page detection**: Read current slide from `input[data-test="currentSlideInput"]` value; extract total from "of N" text
- **URL format varies**: Sometimes `/e/XXXX/1` (with page number), sometimes `/e/XXXX` (without) — can't rely on URL for end-of-slides detection
- **End detection**: Poll the input value after each ArrowRight — if it doesn't increment, you're on the last page

---

## Platform Comparison

| Dimension | NetRoadShow | DealRoadShow |
|-----------|-------------|--------------|
| Popup | `expect_popup()` new window | Same-page navigation |
| Disclaimer button | `<div>`, JS evaluate | Standard `<button>`, locator click (evaluate doesn't trigger nav) |
| URL format | SPA hash routing | Inconsistent — sometimes `/e/XXXX/1`, sometimes `/e/XXXX` |
| URL changes after nav | No (SPA) | Maybe, maybe not |
| Page detection | Slide count text | `input[data-test="currentSlideInput"]` value |
| Total page detection | "All N Slides" text | "of N" text (r'\bof\s*(\d{1,4})\b') |
| Cookie banner | None | Possible, "Ok" button |
| Wait strategy | Fixed sleep + networkidle | Fixed sleep + domcontentloaded (networkidle hangs on WebSocket) |
| Post-launch navigation | Instant (expect_popup blocks) | Delayed 3-4s (POST form submit), don't evaluate during this period |

---

## Common Pitfalls

### Pillow PDF Requires format='PDF'
```python
# ✅ MUST specify format='PDF'
imgs[0].save(path, save_all=True, append_images=imgs[1:], format='PDF', resolution=150)
```

### Playwright headless flag
Both platforms need `--no-sandbox`:
```python
browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
```

### Headless trust
Mac Safari UA + Playwright headless Chromium works on both platforms.

### Shared email config
Both platforms share the `NRS_EMAIL` environment variable. No separate config needed.

### Wait strategy (DealRoadShow only)
- **Don't use `wait_for_url`** — page uses pushState navigation, wait_for_url and wait_for_function miss events
- **Don't use `networkidle`** — audio player has WebSocket persistent connections that hang
- **Use fixed sleep + `domcontentloaded`** instead

### Page detection (DealRoadShow only)
```python
# Read current page (works regardless of URL format)
cur = page.evaluate('document.querySelector("[data-test=currentSlideInput]").value')
# Navigate
page.keyboard.press("ArrowRight")
time.sleep(1)
# Poll until page number increments
for _ in range(10):
    new_cur = page.evaluate('document.querySelector("[data-test=currentSlideInput]").value')
    if int(new_cur) > int(cur): break
    time.sleep(0.5)
```

---

## Notes

- User-Agent set to macOS Safari for better server-side trust
- Navigation uses `page.keyboard.press("ArrowRight")` for both platforms
- Screenshot size: 1920×1080, ~350KB~900KB each
- Output PDF: ~4-5 MB (32 slides)
- Reference: `references/netroadshow-practice.md` (operational notes with Mermaid flowcharts)
- GitHub: https://github.com/nikker1974/roadshow-capture-skill (Hermes + OpenClaw compatible)
