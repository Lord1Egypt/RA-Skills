---
name: qa-browser-tester
description: >
  Launch a real headless browser on the server and perform exhaustive end-to-end
  QA testing of a web application — clicking every button, filling every form,
  navigating every menu, and simulating a complete user journey.
  Use this skill whenever the user asks to "test the app", "check if everything
  works", "simulate a user", "run QA", "click through the site", or "browse the
  website automatically". Also trigger when the user says things like "בדוק את
  האתר", "תדמה משתמש", or "תבדוק שהכל עובד". Always use this skill — do not
  attempt browser automation without it, as it contains critical Docker-safe
  configuration required for Chromium to run on Linux servers.
---

# QA Browser Tester

Exhaustive automated QA testing via headless Chromium browser.
Works on bare Linux servers and inside Docker containers.

## How to Use This Skill

1. Read this file fully before starting
2. Follow the phases IN ORDER — never skip Phase 0 or Phase 1
3. See `references/docker-setup.md` for Docker-specific install instructions
4. See `references/test-phases.md` for the full test script

---

## PHASE 0 — DETECT ENVIRONMENT

Run these commands and report ALL output before doing anything else:

```bash
cat /etc/os-release 2>/dev/null | head -3
cat /proc/1/cgroup | grep -i docker && echo "YES: inside Docker" || echo "not in Docker"
whoami && id
which apt-get apk yum 2>/dev/null || echo "no package manager found"
python3 --version 2>/dev/null || echo "no python3"
pip3 --version 2>/dev/null || echo "no pip3"
node --version 2>/dev/null || echo "no node"
python3 -c "import playwright; print('playwright already installed')" 2>/dev/null || echo "playwright NOT installed"
which chromium chromium-browser google-chrome 2>/dev/null || echo "no browser binary"
df -h / | tail -1
curl -s --max-time 5 https://pypi.org > /dev/null && echo "internet OK" || echo "NO INTERNET"
```

→ If inside Docker, read `references/docker-setup.md` before proceeding.
→ If on bare Linux, continue to Phase 1 directly.

---

## PHASE 1 — INSTALL PLAYWRIGHT

### Standard Linux (apt available):
```bash
apt-get update -qq && apt-get install -y python3-pip curl -qq
pip3 install playwright
python3 -m playwright install chromium
python3 -m playwright install-deps chromium
```

### Alpine (apk available):
```bash
apk add --no-cache chromium nss freetype harfbuzz ca-certificates ttf-freefont python3 py3-pip
pip3 install playwright
export PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH=$(which chromium-browser || which chromium)
python3 -m playwright install chromium
```

### No package manager / no pip:
```bash
curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
python3 /tmp/get-pip.py
pip3 install playwright
python3 -m playwright install chromium
python3 -m playwright install-deps chromium
```

---

## PHASE 2 — VERIFY BROWSER WORKS

⚠️ CRITICAL: On any Linux server or Docker container, Chromium MUST be launched
with these exact flags or it will crash:

```
--no-sandbox
--disable-dev-shm-usage
--disable-gpu
--disable-setuid-sandbox
--single-process
```

Run this verification test:

```python
python3 << 'EOF'
from playwright.sync_api import sync_playwright

DOCKER_ARGS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu",
    "--disable-setuid-sandbox",
    "--single-process",
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=DOCKER_ARGS)
    page = browser.new_page()
    page.goto("https://example.com", wait_until="networkidle")
    print(f"✅ Browser OK — title: {page.title()}")
    browser.close()
EOF
```

✅ SUCCESS → continue to Phase 3
❌ FAILURE → report exact error, stop, do not proceed

---

## PHASE 3 — RUN EXHAUSTIVE TESTS

Read `references/test-phases.md` for the complete test script.

Set the target URL before running:
```python
BASE_URL = "https://your-app-url-here.com"   # ← change this
```

Create screenshot directory:
```bash
mkdir -p /tmp/qa_screenshots
```

---

## PHASE 4 — PRODUCE FINAL REPORT

After tests complete:

```bash
ls -la /tmp/qa_screenshots/
```

Then output this report:

```
## QA EXHAUSTIVE TEST REPORT
Date/Time: [timestamp]
Target URL: [url]
Environment: Docker / Linux

### COVERAGE
Pages visited:      X
Nav items clicked:  X
Buttons clicked:    X
Forms tested:       X
Edge cases run:     X

### BUGS FOUND

🔴 CRITICAL (broken functionality)
1. [page] — [what happened]

🟡 MEDIUM (works but wrong)
1. [page] — [what happened]

🟢 MINOR (cosmetic / UX)
1. [page] — [what happened]

### UNTESTED AREAS
1. [reason why it couldn't be tested]

### SCREENSHOTS SAVED
[list files in /tmp/qa_screenshots/]

### VERDICT: [X/10] — [one sentence summary]
```
