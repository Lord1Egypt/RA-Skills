---
name: web-screenshot
description: Capture screenshots of web pages running on local or remote servers using Puppeteer in headless Chromium. Use when user asks to screenshot web pages, capture web UI, take website screenshots, or document web application interfaces. Supports login-required SPAs (Vue/React/Angular) by performing form-based authentication before navigating. Generates screenshots and an optional result.json with per-page descriptions.
---

# Web Screenshot

Capture screenshots of web pages (especially SPA applications) with automatic login handling.

## Dependencies

- `puppeteer-core` (npm global)
- `chromium-browser` (`/usr/bin/chromium-browser`)
- Node.js

Verify with: `which chromium-browser && npm ls -g puppeteer-core`

## Quick Start

```bash
node <skill_dir>/scripts/screenshot.js <config.json>
```

## Config Format

```json
{
  "baseUrl": "http://192.168.7.66:8080",
  "outputDir": "/root/screenpics/my-capture",
  "resolution": [1920, 1080],
  "login": {
    "url": "/login",
    "usernameSelector": "input[placeholder='请输入用户名']",
    "passwordSelector": "input[type='password']",
    "submitSelector": "button.el-button--primary",
    "credentials": { "username": "admin", "password": "123456" }
  },
  "pages": [
    { "name": "01_dashboard", "path": "/dashboard", "waitMs": 3000 },
    { "name": "02_project_list", "path": "/project/list", "waitMs": 2000 }
  ],
  "descriptions": {
    "01_dashboard": "工作台首页，展示KPI卡片和图表。",
    "02_project_list": "项目管理列表页面。"
  }
}
```

### Login Flow (SPA Authentication)

The script handles Vue/React SPA login by:
1. Navigating to the login page
2. Setting input values via native `HTMLInputElement.value` setter + dispatching `input` events (Vue-reactive compatible)
3. Clicking the submit button
4. Waiting for SPA router navigation (URL change)
5. Using Vue's `$router.push()` for subsequent page navigation (avoids Pinia/Redux store reset on full page reload)

### Fields

| Field | Required | Description |
|-------|----------|-------------|
| `baseUrl` | ✅ | Base URL of the web app |
| `outputDir` | ✅ | Output directory for screenshots |
| `resolution` | No | Viewport size `[width, height]`, default `[1920, 1080]` |
| `login` | No | Login config (skip for public pages) |
| `login.usernameSelector` | ✅* | CSS selector for username input |
| `login.passwordSelector` | ✅* | CSS selector for password input |
| `login.submitSelector` | ✅* | CSS selector for submit button |
| `login.credentials` | ✅* | `{ username, password }` |
| `pages` | ✅ | Array of pages to capture |
| `pages[].name` | ✅ | Filename prefix (e.g. `01_dashboard`) |
| `pages[].path` | ✅ | URL path (e.g. `/dashboard`) |
| `pages[].waitMs` | No | Extra wait in ms after navigation (default 2000) |
| `descriptions` | No | Map of `name` → description text (included in result.json) |

## Output

- `{outputDir}/{name}.png` — one PNG per page
- `{outputDir}/result.json` — metadata with filenames, titles, URLs, descriptions

### result.json Format

```json
{
  "project": "auto-generated",
  "captureDate": "2026-03-22",
  "baseUrl": "...",
  "resolution": "1920x1080",
  "screenshots": [
    {
      "filename": "01_dashboard.png",
      "title": "Dashboard",
      "url": "...",
      "description": "..."
    }
  ]
}
```

## Capture Login Page Too

To include the login page as the first screenshot, add it to `pages` with a special flag:

```json
{
  "pages": [
    { "name": "00_login", "path": "/login", "isLoginPage": true, "waitMs": 2000 }
  ]
}
```

When `isLoginPage: true`, the script captures this page before performing login.

## Advanced: Custom Vue Store Login

If the form-based login doesn't work (e.g., custom auth flow), use `storeLogin` instead:

```json
{
  "login": {
    "url": "/login",
    "storeLogin": {
      "storeName": "user",
      "method": "login",
      "args": ["平台管理员"]
    }
  }
}
```

This directly calls `pinia._s.get(storeName).method(...args)` via CDP.

## Troubleshooting

- **Blank charts (ECharts/Chart.js)**: Headless Chromium has no GPU. Charts using Canvas may render empty. Use `--disable-gpu` (already included).
- **Redirected to login on all pages**: Login failed. Check selectors match the actual form elements. Try `storeLogin` approach.
- **SPA navigation not working**: Ensure `login` section is configured. Without login, `page.goto()` is used instead of `$router.push()`.
