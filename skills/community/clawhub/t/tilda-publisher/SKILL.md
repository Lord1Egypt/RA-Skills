---
name: tilda-publisher
version: 1.0.0
description: >
  Publish and manage articles on Tilda website builder via browser automation.
  Use this skill when the user wants to create a new article page, edit an
  existing one, or publish a draft on their Tilda site.
author: vspandexe
license: MIT
metadata:
  openclaw:
    requires:
      env:
        - name: TILDA_EMAIL
          description: Tilda account email
        - name: TILDA_PASSWORD
          description: Tilda account password
      binaries:
        - playwright
    tags:
      - cms
      - publishing
      - browser-automation
      - tilda
      - blogging
---

# Tilda Publisher

## Overview

This skill handles creating, editing, and publishing articles on the Tilda
platform via browser automation (Playwright). Tilda does not provide a
write API, so all operations are performed through the browser UI exactly
as a human would.

---

## Onboarding (first run)

This section is an instruction for the agent. Run it **once**, on the first
time the user invokes this skill, if any required env variable is missing.

### Step 1 — Check for missing variables

```javascript
const missing = [];
if (!process.env.TILDA_EMAIL)    missing.push('TILDA_EMAIL');
if (!process.env.TILDA_PASSWORD) missing.push('TILDA_PASSWORD');

if (missing.length > 0) {
  startOnboarding(missing);
}
```

### Step 2 — Ask the user (one question at a time)

**1. Email:**
> "To publish on Tilda I need your account credentials.
> What email do you use on tilda.cc?"

**2. Password:**
> "What is your Tilda account password?
> ⚠️ It will be stored locally in the workspace .env file — never sent anywhere."

**3. Project name (optional):**
> "What is the name of the Tilda project where articles should be published?
> If you only have one project, just press Enter — I'll find it automatically."

**4. Confirmation:**
> "Got it! Testing the connection to Tilda..."

Run a test login (no publishing) and report back:
- ✅ "Connection successful. Skill is ready!"
- ❌ "Login failed. Please double-check your email and password."

### Step 3 — Save to .env

```javascript
const fs = require('fs');
const path = require('path');

function saveToEnv(vars) {
  const envPath = path.join(process.cwd(), '.env');
  let existing = '';

  if (fs.existsSync(envPath)) {
    existing = fs.readFileSync(envPath, 'utf8');
  }

  const lines = existing.split('\n').filter(Boolean);

  for (const [key, value] of Object.entries(vars)) {
    const idx = lines.findIndex(l => l.startsWith(`${key}=`));
    const line = `${key}=${value}`;
    if (idx >= 0) {
      lines[idx] = line;
    } else {
      lines.push(line);
    }
  }

  fs.writeFileSync(envPath, lines.join('\n') + '\n');
  console.log('Settings saved to .env');
}

saveToEnv({
  TILDA_EMAIL: emailFromUser,
  TILDA_PASSWORD: passwordFromUser,
  TILDA_PROJECT_NAME: projectFromUser || '',
});
```

### Step 4 — Install Playwright if missing

```javascript
async function ensurePlaywright() {
  try {
    require('playwright');
    console.log('Playwright already installed');
  } catch (e) {
    console.log('Installing Playwright...');
    const { execSync } = require('child_process');
    execSync('npm install playwright', { stdio: 'inherit' });
    execSync('npx playwright install chromium', { stdio: 'inherit' });
    console.log('Playwright installed');
  }
}
```

Let the user know this may take 1-2 minutes.

### Onboarding checklist

After completing onboarding, confirm each item:

```
✅ TILDA_EMAIL    — saved
✅ TILDA_PASSWORD — saved
✅ Project        — "Project name" (or "will detect automatically")
✅ Playwright     — installed
✅ Test login     — successful

🎉 tilda-publisher is ready!
Say "publish an article" and provide a title and content.
```

---

## Environment variables

| Variable            | Description                        |
|---------------------|------------------------------------|
| `TILDA_EMAIL`       | Email address for tilda.cc account |
| `TILDA_PASSWORD`    | Password for tilda.cc account      |
| `TILDA_PROJECT_NAME`| Target project name (optional)     |

Install Playwright before first use:
```bash
npx playwright install chromium
```

---

## How it works

```
Agent receives task
       ↓
Launches headless browser
       ↓
Logs in to tilda.cc
       ↓
Navigates to the target project
       ↓
Creates or edits a page
       ↓
Fills in content blocks
       ↓
Publishes the page
       ↓
Returns the live URL
```

---

## Usage scenarios

### Scenario 1 — Create and publish a new article

**User triggers:**
- "publish an article on Tilda"
- "create a new blog post on Tilda"
- "add a post to my site"

**Inputs:**
- `title` — article title (required)
- `content` — article body in Markdown or plain text (required)
- `project_name` — Tilda project name (optional if only one project)
- `cover_image_url` — cover image URL (optional)
- `seo_description` — meta description (optional)

---

### Scenario 2 — Edit an existing page

**User triggers:**
- "update the article [title] on Tilda"
- "change the text on the page [title]"

**Inputs:**
- `page_title` — name of the existing page
- `new_content` — updated content

---

### Scenario 3 — Publish a draft

**User triggers:**
- "publish the draft [title]"
- "release the page that was on hold"

---

## Step-by-step instructions

### Step 1 — Login

```javascript
const { chromium } = require('playwright');

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();

await page.goto('https://tilda.cc/login/');
await page.waitForLoadState('networkidle');

await page.fill('input[name="email"], input[type="email"]', process.env.TILDA_EMAIL);
await page.fill('input[name="password"], input[type="password"]', process.env.TILDA_PASSWORD);
await page.click('button[type="submit"], .js-login-btn, input[type="submit"]');

await page.waitForURL('**/dashboard/**', { timeout: 15000 });
console.log('Login successful');
```

**Login error handling:**
- URL did not change → check credentials
- CAPTCHA appeared → notify user, manual login required
- 2FA prompt → ask user for the code

---

### Step 2 — Select project

```javascript
await page.goto('https://tilda.cc/projects/');
await page.waitForLoadState('networkidle');

if (projectName) {
  await page.locator(`.project-title:has-text("${projectName}")`).first().click();
} else {
  await page.locator('.project-item').first().click();
}

await page.waitForLoadState('networkidle');
const projectId = page.url().match(/\/edit\/(\d+)\//)?.[1];
console.log(`Project ID: ${projectId}`);
```

---

### Step 3 — Create a new page

```javascript
await page.click('.js-add-page, [data-action="addpage"], button:has-text("Add page")');
await page.waitForSelector('.modal, .popup, .dialog', { timeout: 5000 }).catch(() => {});

await page.fill('input[name="title"], .page-title-input', title);
await page.click('.js-create-page, button:has-text("Create")');
await page.waitForLoadState('networkidle');

console.log(`Page "${title}" created`);
```

---

### Step 4 — Add content

```javascript
await page.click('.js-edit-page, [data-action="editpage"], .page-edit-btn');
await page.waitForURL('**/page/**', { timeout: 10000 });
await page.waitForLoadState('networkidle');

// Add title block (ST category)
await page.click('.js-add-block-btn, .add-block-button, [data-action="addblock"]');
await page.waitForSelector('.blocks-catalog, .block-picker', { timeout: 5000 });
await page.click('[data-category="ST"], .category-ST');
await page.click('.block-item:first-child');
await page.waitForLoadState('networkidle');

const titleBlock = await page.locator('[contenteditable]').first();
await titleBlock.click();
await page.keyboard.press('Control+a');
await page.keyboard.type(title);

// Add text block (TX category)
await page.click('.js-add-block-btn, .add-block-button');
await page.waitForSelector('.blocks-catalog, .block-picker');
await page.click('[data-category="TX"], .category-TX');
await page.click('.block-item:first-child');
await page.waitForLoadState('networkidle');

const textBlock = await page.locator('[contenteditable]').last();
await textBlock.click();
await page.keyboard.press('Control+a');
await page.keyboard.type(content);

console.log('Content added');
```

---

### Step 5 — SEO settings (optional)

```javascript
if (seoDescription) {
  await page.click('.js-page-settings, [data-action="settings"], .settings-btn');
  await page.waitForSelector('.settings-panel, .page-settings-modal');
  await page.click('[data-tab="seo"], .tab-seo, button:has-text("SEO")');
  await page.fill('textarea[name="descr"], .seo-description', seoDescription);
  await page.click('.js-save-settings, button:has-text("Save")');
  await page.waitForLoadState('networkidle');
  console.log('SEO settings saved');
}
```

---

### Step 6 — Publish

```javascript
await page.click('.js-publish, [data-action="publish"], button:has-text("Publish")');

await page.waitForSelector('.success-message, .published-notification, .t-popup_show', {
  timeout: 30000
});

const publishedUrl = await page.evaluate(() => {
  const link = document.querySelector('.published-url a, .page-url, [data-page-url]');
  return link ? link.href || link.textContent : null;
});

console.log(`Published: ${publishedUrl}`);
await browser.close();

return { success: true, url: publishedUrl };
```

---

## Full ready-to-run script

```javascript
// tilda-publish.js
const { chromium } = require('playwright');

async function publishArticle({ title, content, projectName, seoDescription }) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
  });
  const page = await context.newPage();

  try {
    console.log('Logging in...');
    await page.goto('https://tilda.cc/login/');
    await page.waitForLoadState('networkidle');
    await page.fill('input[type="email"]', process.env.TILDA_EMAIL);
    await page.fill('input[type="password"]', process.env.TILDA_PASSWORD);
    await page.click('button[type="submit"]');
    await page.waitForURL('**/dashboard/**', { timeout: 15000 });

    console.log('Selecting project...');
    await page.goto('https://tilda.cc/projects/');
    await page.waitForLoadState('networkidle');

    if (projectName) {
      await page.locator(`text="${projectName}"`).first().click();
    } else {
      await page.locator('.project-item, .projects-list__item').first().click();
    }
    await page.waitForLoadState('networkidle');

    console.log('Creating page...');
    await page.click('[data-action="addpage"], .js-add-page');
    await page.waitForTimeout(1000);
    await page.fill('input[name="title"]', title);
    await page.keyboard.press('Enter');
    await page.waitForLoadState('networkidle');

    console.log('Opening editor...');
    await page.click('.js-edit-page, [data-action="editpage"]');
    await page.waitForURL('**/page/**');
    await page.waitForLoadState('networkidle');
    await page.waitForTimeout(2000);

    console.log('Adding content...');
    await page.click('.js-add-block-btn');
    await page.waitForSelector('.blocks-catalog');
    await page.click('[data-category="ST"]');
    await page.click('.block-item:first-child');
    await page.waitForTimeout(1000);

    const titleBlock = await page.locator('[contenteditable]').first();
    await titleBlock.click();
    await page.keyboard.selectAll();
    await page.keyboard.type(title);

    await page.click('.js-add-block-btn');
    await page.waitForSelector('.blocks-catalog');
    await page.click('[data-category="TX"]');
    await page.click('.block-item:first-child');
    await page.waitForTimeout(1000);

    const textBlock = await page.locator('[contenteditable]').last();
    await textBlock.click();
    await page.keyboard.selectAll();
    await page.keyboard.type(content);

    await page.keyboard.press('Control+S');
    await page.waitForTimeout(1500);

    if (seoDescription) {
      console.log('Setting SEO...');
      await page.click('.js-page-settings, [data-action="settings"]');
      await page.waitForSelector('.settings-panel');
      await page.click('[data-tab="seo"]');
      await page.fill('textarea[name="descr"]', seoDescription);
      await page.click('.js-save-settings');
      await page.waitForTimeout(1000);
    }

    console.log('Publishing...');
    await page.click('.js-publish, [data-action="publish"]');
    await page.waitForSelector('.success-message, .t-popup_show', { timeout: 30000 });
    await page.waitForTimeout(2000);

    const publishedUrl = await page.evaluate(() => {
      const el = document.querySelector('.published-url a, [data-page-url]');
      return el ? (el.href || el.textContent?.trim()) : null;
    });

    console.log(`Published: ${publishedUrl || 'URL not detected'}`);
    return { success: true, url: publishedUrl };

  } catch (error) {
    console.error('Error:', error.message);
    await page.screenshot({ path: 'tilda-error.png' });
    return { success: false, error: error.message };
  } finally {
    await browser.close();
  }
}

publishArticle({
  title: process.env.ARTICLE_TITLE || 'Test article',
  content: process.env.ARTICLE_CONTENT || 'Article body...',
  projectName: process.env.TILDA_PROJECT_NAME || null,
  seoDescription: process.env.SEO_DESCRIPTION || null,
}).then(console.log);
```

---

## Session caching (optimization)

To avoid logging in on every run, save and reuse cookies:

```javascript
// Save after first login
await context.storageState({ path: 'tilda-session.json' });

// Load on subsequent runs
const context = await browser.newContext({
  storageState: 'tilda-session.json'
});
```

Tilda sessions last approximately 7 days before re-authentication is needed.

---

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| Login page not found | Tilda changed the URL | Check `page.url()` and update selectors |
| Buttons not clickable | Modal overlay blocking | Add `waitForTimeout(1000)` before click |
| Content not inserted | Editor not fully loaded | Increase `waitForLoadState` timeout |
| CAPTCHA on login | Too many login attempts | Use session caching to avoid repeated logins |
| Publish hangs | Network or server error | Add retry logic with 60s timeout |

---

## Extensions

This skill can be extended to support:
- **Tilda Feeds** — publishing via the built-in news feed editor
- **Scheduled publishing** — setting a publish date
- **Cover images** — uploading covers via file input
- **Categories and tags** — blog post categorisation
- **Page duplication** — cloning a template page for faster publishing

---

## Self-Healing — Automatic selector recovery

Tilda periodically updates its UI. If the script fails because a selector is
not found, the agent **must not immediately report an error to the user**.
It must first run a full self-diagnosis cycle and attempt to fix itself.

### When to trigger self-healing

Trigger self-healing on any of these errors:
- `TimeoutError: waiting for selector`
- `Error: No element found`
- `ElementNotInteractableError`
- `strict mode violation` (multiple elements matched instead of one)

Do NOT trigger self-healing for:
- Network errors (no internet)
- Auth errors (wrong password)
- JavaScript errors inside Tilda (their bug, not ours)

---

### Recovery algorithm (follow in strict order)

#### Stage 1 — Diagnose

```javascript
async function diagnose(page, failedSelector, stepName) {
  console.log(`Self-healing triggered for step: ${stepName}`);
  console.log(`Broken selector: ${failedSelector}`);

  await page.screenshot({
    path: `debug-${stepName}-${Date.now()}.png`,
    fullPage: true
  });

  const clickableElements = await page.evaluate(() => {
    const elements = document.querySelectorAll('button, a, [role="button"], [data-action], [class*="js-"]');
    return Array.from(elements).map(el => ({
      tag: el.tagName,
      id: el.id,
      classes: el.className,
      dataAction: el.getAttribute('data-action'),
      text: el.innerText?.trim().slice(0, 50),
      visible: el.offsetParent !== null
    })).filter(el => el.visible);
  });

  const formElements = await page.evaluate(() => {
    return Array.from(document.querySelectorAll('input, textarea, [contenteditable]')).map(el => ({
      tag: el.tagName,
      type: el.type,
      name: el.name,
      id: el.id,
      classes: el.className,
      placeholder: el.placeholder,
      contenteditable: el.getAttribute('contenteditable')
    }));
  });

  return { clickableElements, formElements };
}
```

#### Stage 2 — Find a replacement

After getting the DOM dump, look for the best matching element.

**Replacement lookup rules:**

| Broken selector | What to look for in the dump |
|---|---|
| `.js-add-block-btn` | button with text "Add", "+" or `data-action` containing "add", "block" |
| `.js-publish` | button with text "Publish", "Release" |
| `.js-page-settings` | button with text "Settings" or gear icon |
| `.js-add-page` | button with text "Add page", "New page" |
| `[contenteditable]` | elements with `contenteditable="true"` |
| `input[name="title"]` | input with placeholder containing "title", "name" |

```javascript
function findBestReplacement(elements, brokenSelector) {
  const semanticMap = {
    'publish':   ['publish', 'release', 'go live'],
    'add-block': ['add block', 'add', '+'],
    'settings':  ['settings', 'parameters', 'options'],
    'add-page':  ['add page', 'new page'],
    'save':      ['save', 'apply', 'confirm'],
  };

  const intent = Object.keys(semanticMap).find(key =>
    brokenSelector.toLowerCase().includes(key.replace('-', ''))
  );

  if (!intent) return null;

  const keywords = semanticMap[intent];

  return elements.find(el =>
    keywords.some(kw =>
      el.text?.toLowerCase().includes(kw) ||
      el.dataAction?.toLowerCase().includes(kw) ||
      el.classes?.toLowerCase().includes(kw.replace(' ', '-'))
    )
  );
}
```

#### Stage 3 — Build new selector

```javascript
function buildSelector(element) {
  if (element.dataAction) return `[data-action="${element.dataAction}"]`;
  if (element.id)         return `#${element.id}`;
  const jsClass = element.classes?.split(' ').find(c => c.startsWith('js-'));
  if (jsClass)            return `.${jsClass}`;
  if (element.text)       return `${element.tag.toLowerCase()}:has-text("${element.text}")`;
  return null;
}
```

#### Stage 4 — Retry with new selector

```javascript
async function retryWithHealing(page, originalSelector, stepName, action) {
  try {
    await page.click(originalSelector, { timeout: 5000 });
    return true;
  } catch (e) {
    console.log(`Selector failed: ${originalSelector}`);

    const { clickableElements, formElements } = await diagnose(page, originalSelector, stepName);

    const replacement = findBestReplacement(
      action === 'fill' ? formElements : clickableElements,
      originalSelector
    );

    if (!replacement) {
      console.log('No replacement found — manual fix required');
      return false;
    }

    const newSelector = buildSelector(replacement);
    console.log(`Replacement found: ${newSelector}`);

    try {
      if (action === 'click') await page.click(newSelector, { timeout: 5000 });
      if (action === 'fill')  await page.fill(newSelector, '');
      console.log(`Succeeded with new selector: ${newSelector}`);
      await saveLearnedSelector(originalSelector, newSelector);
      return true;
    } catch (e2) {
      console.log(`New selector also failed: ${newSelector}`);
      return false;
    }
  }
}
```

#### Stage 5 — Save learned selectors

```javascript
const fs = require('fs');
const LEARNED_FILE = './tilda-learned-selectors.json';

async function saveLearnedSelector(broken, replacement) {
  let learned = {};
  if (fs.existsSync(LEARNED_FILE)) {
    learned = JSON.parse(fs.readFileSync(LEARNED_FILE, 'utf8'));
  }
  learned[broken] = {
    selector: replacement,
    learnedAt: new Date().toISOString()
  };
  fs.writeFileSync(LEARNED_FILE, JSON.stringify(learned, null, 2));
  console.log(`Saved: ${broken} → ${replacement}`);
}

function loadLearnedSelectors() {
  if (!fs.existsSync(LEARNED_FILE)) return {};
  return JSON.parse(fs.readFileSync(LEARNED_FILE, 'utf8'));
}

function resolveSelector(defaultSelector) {
  const learned = loadLearnedSelectors();
  return learned[defaultSelector]?.selector || defaultSelector;
}
```

---

### Usage in the main script

Replace all direct `page.click(selector)` calls with:

```javascript
// Instead of:
await page.click('.js-publish');

// Use:
await retryWithHealing(page, resolveSelector('.js-publish'), 'publish', 'click');
```

---

### Escalation to the user when self-healing fails

If the element is still not found after two attempts, the agent:

1. Takes a final full-page screenshot
2. Reports clearly to the user:

```
Could not find the publish button on the page.
Tilda may have updated its interface.

Screenshot saved: debug-publish-1234567890.png

To fix this:
1. Open the screenshot and find the Publish button
2. Open DevTools → copy the selector
3. Tell me: "update the publish selector to [new selector]"

Or run with headless: false to see the browser live.
```

3. Writes to `tilda-healing-needed.log` with the date, step name, and screenshot path.
