# Test Phases — Full QA Script

Copy this entire script, set BASE_URL, and run it with:
```bash
python3 /tmp/qa_test.py
```

Or run inline with `python3 << 'EOF' ... EOF`.

---

```python
from playwright.sync_api import sync_playwright
import os, json, datetime

# ── CONFIGURATION ─────────────────────────────────────────────────────────────
BASE_URL = "https://your-app-url-here.com"   # ← SET THIS before running
DIR = "/tmp/qa_screenshots"
os.makedirs(DIR, exist_ok=True)

DOCKER_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-setuid-sandbox",
    "--single-process",
]

# ── HELPERS ───────────────────────────────────────────────────────────────────
log = {"ok": [], "warn": [], "bug": [], "info": []}
shot_count = [0]

def shot(page, name):
    clean = name.replace(" ", "_").replace("/", "_")[:40]
    path = f"{DIR}/{shot_count[0]:03d}_{clean}.png"
    shot_count[0] += 1
    try:
        page.screenshot(path=path, full_page=True)
        print(f"  📸 {os.path.basename(path)}")
    except Exception as e:
        print(f"  ⚠️ screenshot failed: {e}")

def note(level, location, detail):
    icons = {"ok": "✅", "warn": "🟡", "bug": "🔴", "info": "ℹ️"}
    msg = f"{icons.get(level,'•')} [{location}] {detail}"
    print(msg)
    log[level].append(msg)

def safe_goto(page, url, label=""):
    try:
        page.goto(url, wait_until="networkidle", timeout=15000)
        return True
    except Exception as e:
        note("warn", label or url, f"page load failed: {e}")
        return False

# ── MAIN TEST ─────────────────────────────────────────────────────────────────
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=DOCKER_ARGS)
    page = browser.new_page(viewport={"width": 1280, "height": 800})

    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE A — DISCOVERY: map everything on the homepage
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("PHASE A — DISCOVERY")
    print("="*60)

    if not safe_goto(page, BASE_URL, "homepage"):
        print("❌ Cannot reach BASE_URL. Aborting.")
        browser.close()
        exit(1)

    shot(page, "homepage")
    note("info", "homepage", f"title: {page.title()} | url: {page.url}")

    links = page.eval_on_selector_all(
        "a[href]",
        "els => els.map(e => ({text: e.innerText.trim(), href: e.href}))"
    )
    buttons_text = page.eval_on_selector_all(
        "button, input[type=submit], [role=button]",
        "els => els.map(e => (e.innerText.trim() || e.value || e.getAttribute('aria-label') || '?'))"
    )
    nav = page.eval_on_selector_all(
        "nav a, header a, [class*='nav'] a, [class*='menu'] a, [class*='sidebar'] a",
        "els => els.map(e => ({text: e.innerText.trim(), href: e.href}))"
    )

    print(f"\n  Found: {len(links)} links | {len(buttons_text)} buttons | {len(nav)} nav items")
    print(f"  Nav items: {json.dumps(nav, ensure_ascii=False)}")
    print(f"  Buttons: {buttons_text}")

    visited_urls = {page.url}

    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE B — NAVIGATE EVERY NAV ITEM (and their sub-menus)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("PHASE B — NAV EXHAUSTION")
    print("="*60)

    for i, item in enumerate(nav):
        href = item.get("href", "")
        text = item.get("text", f"item_{i}") or f"item_{i}"
        if not href or href in visited_urls or href.startswith("mailto") or href == "#":
            continue
        visited_urls.add(href)

        if safe_goto(page, href, f"nav/{text}"):
            shot(page, f"nav_{i}_{text[:20]}")
            note("ok", f"nav/{text}", f"loaded: {page.url}")

            # Check for sub-menus on this page
            sub_links = page.eval_on_selector_all(
                "[class*='dropdown'] a, [class*='submenu'] a",
                "els => els.map(e => ({text: e.innerText.trim(), href: e.href}))"
            )
            for j, sub in enumerate(sub_links):
                sub_href = sub.get("href", "")
                if sub_href and sub_href not in visited_urls and not sub_href.startswith("mailto"):
                    visited_urls.add(sub_href)
                    if safe_goto(page, sub_href, f"sub/{sub.get('text','')}"):
                        shot(page, f"nav_{i}_sub_{j}_{sub.get('text','')[:15]}")
                        note("ok", f"submenu/{sub.get('text','')}", f"loaded: {page.url}")
        else:
            note("bug", f"nav/{text}", f"FAILED to load: {href}")

    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE C — CLICK EVERY BUTTON on every visited page
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("PHASE C — BUTTON EXHAUSTION")
    print("="*60)

    pages_to_scan = list(visited_urls)[:15]  # cap at 15 pages
    for page_url in pages_to_scan:
        if not safe_goto(page, page_url, f"btn-scan/{page_url}"):
            continue

        current_url = page.url
        btns = page.query_selector_all(
            "button:visible, [role=button]:visible, input[type=submit]:visible, "
            "a[class*='btn']:visible, a[class*='button']:visible"
        )

        print(f"\n  Page: {page_url} — {len(btns)} buttons found")
        for i, btn in enumerate(btns):
            try:
                text = (btn.inner_text().strip() or
                        btn.get_attribute("value") or
                        btn.get_attribute("aria-label") or
                        f"btn_{i}")
                print(f"    → Clicking: '{text}'")
                btn.scroll_into_view_if_needed()
                btn.click(timeout=4000)
                page.wait_for_timeout(1500)
                shot(page, f"btn_{text[:20]}")

                after_url = page.url
                if after_url != current_url:
                    note("ok", f"button/{text}", f"navigated to: {after_url}")
                    page.go_back()
                    page.wait_for_load_state("networkidle")
                else:
                    note("ok", f"button/{text}", "action on same page")
            except Exception as e:
                note("warn", f"button_{i}", f"could not click: {str(e)[:80]}")

    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE D — FORM TESTING (happy path + empty submit + invalid data)
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("PHASE D — FORM TESTING")
    print("="*60)

    for page_url in pages_to_scan:
        if not safe_goto(page, page_url, f"form-scan/{page_url}"):
            continue

        forms = page.query_selector_all("form")
        if not forms:
            continue

        print(f"\n  Page: {page_url} — {len(forms)} form(s) found")

        for fi, form in enumerate(forms):
            inputs = form.query_selector_all(
                "input:not([type=hidden]):not([type=submit]):not([type=button]), textarea, select"
            )

            # ── Happy path ──
            for inp in inputs:
                try:
                    t = (inp.get_attribute("type") or "text").lower()
                    tag = inp.evaluate("e => e.tagName.toLowerCase()")
                    if t == "email":      inp.fill("testqa@example.com")
                    elif t == "password": inp.fill("TestPass123!")
                    elif t == "tel":      inp.fill("0501234567")
                    elif t == "number":   inp.fill("42")
                    elif t == "date":     inp.fill("2025-01-01")
                    elif t == "checkbox": inp.check()
                    elif t == "radio":    inp.check()
                    elif tag == "select": inp.select_option(index=1)
                    elif tag == "textarea": inp.fill("This is a test input from QA agent.")
                    else:
                        name = inp.get_attribute("name") or inp.get_attribute("placeholder") or "field"
                        inp.fill(f"Test {name}")
                except Exception as e:
                    print(f"    ⚠️ Could not fill input: {e}")

            shot(page, f"form_{fi}_filled")

            submit = form.query_selector(
                "button[type=submit], input[type=submit], button:last-of-type"
            )
            if submit:
                try:
                    submit.click()
                    page.wait_for_timeout(2000)
                    shot(page, f"form_{fi}_submitted")
                    note("ok", f"form_{fi} on {page_url}", f"submitted → {page.url}")
                except Exception as e:
                    note("warn", f"form_{fi}", f"submit failed: {str(e)[:80]}")

            # ── Empty submit test ──
            if not safe_goto(page, page_url, f"empty-form"):
                continue
            forms2 = page.query_selector_all("form")
            if fi < len(forms2):
                submit2 = forms2[fi].query_selector(
                    "button[type=submit], input[type=submit], button:last-of-type"
                )
                if submit2:
                    try:
                        submit2.click()
                        page.wait_for_timeout(1500)
                        shot(page, f"form_{fi}_empty_submit")
                        note("ok", f"form_{fi} empty", f"validation result on: {page.url}")
                    except Exception as e:
                        note("warn", f"form_{fi} empty submit", str(e)[:80])

    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE E — FULL USER JOURNEY SIMULATION
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("PHASE E — USER JOURNEY SIMULATION")
    print("="*60)

    ts = datetime.datetime.now().strftime("%H%M%S")
    test_email = f"qatest_{ts}@test.com"
    test_password = "TestPass123!"

    # 1. Arrive as new visitor
    safe_goto(page, BASE_URL, "journey-start")
    shot(page, "journey_01_homepage")
    note("info", "journey", "arrived at homepage as new visitor")

    # 2. Find and use Register link
    for reg_text in ["Register", "Sign Up", "הרשמה", "Create Account", "Join"]:
        try:
            page.click(f"text='{reg_text}'", timeout=2000)
            page.wait_for_load_state("networkidle")
            shot(page, "journey_02_register_page")
            note("ok", "journey/register", f"found register via '{reg_text}'")
            break
        except:
            continue

    # Fill register form if present
    for selector, value in [
        ("input[name*='name'], input[placeholder*='name']", "QA Test User"),
        ("input[type='email'], input[name*='email']", test_email),
        ("input[type='password']", test_password),
    ]:
        try:
            inp = page.query_selector(selector)
            if inp:
                inp.fill(value)
        except: pass

    shot(page, "journey_03_register_filled")

    try:
        page.click("button[type=submit], input[type=submit]", timeout=3000)
        page.wait_for_timeout(2000)
        shot(page, "journey_04_register_result")
        note("ok", "journey/register", f"submitted → {page.url}")
    except:
        note("warn", "journey/register", "could not submit register form")

    # 3. Login
    for login_text in ["Login", "Sign In", "כניסה", "Log In"]:
        try:
            safe_goto(page, BASE_URL, "before-login")
            page.click(f"text='{login_text}'", timeout=2000)
            page.wait_for_load_state("networkidle")
            shot(page, "journey_05_login_page")
            note("ok", "journey/login", f"found login via '{login_text}'")
            break
        except:
            continue

    for selector, value in [
        ("input[type='email'], input[name*='email'], input[name*='username']", test_email),
        ("input[type='password']", test_password),
    ]:
        try:
            inp = page.query_selector(selector)
            if inp:
                inp.fill(value)
        except: pass

    shot(page, "journey_06_login_filled")
    try:
        page.click("button[type=submit], input[type=submit]", timeout=3000)
        page.wait_for_timeout(2000)
        shot(page, "journey_07_login_result")
        note("ok", "journey/login", f"submitted → {page.url}")
    except:
        note("warn", "journey/login", "could not submit login form")

    # 4. Logout
    for logout_text in ["Logout", "Sign Out", "יציאה", "Log Out"]:
        try:
            page.click(f"text='{logout_text}'", timeout=2000)
            page.wait_for_timeout(1500)
            shot(page, "journey_08_logout")
            note("ok", "journey/logout", f"logged out → {page.url}")
            break
        except:
            continue

    # ═══════════════════════════════════════════════════════════════════════════
    # PHASE F — EDGE CASES
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("PHASE F — EDGE CASES")
    print("="*60)

    # Mobile viewport
    mobile = browser.new_page(viewport={"width": 375, "height": 812})
    if safe_goto(mobile, BASE_URL, "mobile"):
        shot(mobile, "edge_mobile_375px")
        note("ok", "mobile/375px", "homepage loaded on mobile viewport")
    mobile.close()

    # Back button
    safe_goto(page, BASE_URL, "back-test")
    page.go_back()
    page.wait_for_timeout(1000)
    shot(page, "edge_back_button")
    note("info", "back-button", f"after go_back: {page.url}")

    # Refresh mid-page
    safe_goto(page, BASE_URL, "refresh-test")
    page.reload(wait_until="networkidle")
    shot(page, "edge_page_refresh")
    note("info", "refresh", f"after reload: {page.url}")

    # Direct access to protected routes (while logged out)
    print("\n  Checking protected routes while logged out:")
    for route in ["/dashboard", "/admin", "/profile", "/settings", "/account", "/api"]:
        try:
            page.goto(BASE_URL.rstrip("/") + route, wait_until="networkidle", timeout=8000)
            landed = page.url
            shot(page, f"edge_direct{route.replace('/','_')}")
            if route in landed:
                note("bug", f"security/{route}", f"⚠️ ACCESSIBLE WITHOUT LOGIN → {landed}")
            else:
                note("ok", f"security/{route}", f"correctly redirected → {landed}")
        except Exception as e:
            note("info", f"security/{route}", f"error (likely 404): {str(e)[:60]}")

    browser.close()

    # ═══════════════════════════════════════════════════════════════════════════
    # FINAL REPORT
    # ═══════════════════════════════════════════════════════════════════════════
    print("\n" + "="*60)
    print("FINAL QA REPORT")
    print("="*60)
    print(f"Target: {BASE_URL}")
    print(f"Screenshots: {DIR}/ ({shot_count[0]} total)")
    print(f"\n✅ OK:    {len(log['ok'])}")
    print(f"🟡 WARN:  {len(log['warn'])}")
    print(f"🔴 BUGS:  {len(log['bug'])}")
    print(f"ℹ️  INFO:  {len(log['info'])}")

    if log["bug"]:
        print("\n🔴 BUGS:")
        for b in log["bug"]: print(f"  {b}")
    if log["warn"]:
        print("\n🟡 WARNINGS:")
        for w in log["warn"]: print(f"  {w}")

    print("\nDone. Review screenshots in /tmp/qa_screenshots/")
```

---

## Running the Script

Save to file and run:
```bash
cat > /tmp/qa_test.py << 'PYEOF'
[paste script above here]
PYEOF

python3 /tmp/qa_test.py
```

Or run as inline heredoc:
```bash
python3 << 'EOF'
[paste script above here]
EOF
```

## After the Script

List all screenshots:
```bash
ls -la /tmp/qa_screenshots/
```

To view a specific screenshot (if you have file access):
```bash
# Copy to a web-accessible location if needed
cp /tmp/qa_screenshots/*.png /var/www/html/qa/
```
