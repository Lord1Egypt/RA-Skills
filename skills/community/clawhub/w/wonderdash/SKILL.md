---
name: wonderdash-widgets
description: Create and manage widgets on the user's WonderDash mobile dashboard via GitHub
version: 5.0.0
user-invocable: false

metadata:
  openclaw:
    requires:
      bins:
        - git
        - ssh
    os:
      - darwin
      - linux
    emoji: "\U0001F4F1"
---

# WonderDash Widget Skill (v5 — WebView + Index + File-Per-Widget)

You manage widgets on the user's WonderDash mobile dashboard by writing individual JSON files to a GitHub repository, with a `dashboard.json` index that controls visibility and order.

## Setup

WonderDash sends you a setup message containing:
- **Repo URL**: `git@github.com:{username}/wonderdash-widgets.git`
- **SSH Private Key**: An Ed25519 key in OpenSSH PEM format

Save the SSH key and configure access:

```bash
# Save the key
cat > ~/.ssh/wonderdash_deploy << 'KEYEOF'
<paste the key here>
KEYEOF
chmod 600 ~/.ssh/wonderdash_deploy

# Add SSH config
cat >> ~/.ssh/config << 'EOF'
Host wonderdash-github
  HostName github.com
  User git
  IdentityFile ~/.ssh/wonderdash_deploy
  IdentitiesOnly yes
EOF

# Clone the repo
git clone wonderdash-github:{username}/wonderdash-widgets.git
```

## Repo Structure

```
wonderdash-widgets/
├── dashboard.json          ← Index: controls which widgets are visible and their order
├── widgets/
│   ├── weather.json        ← Widget content
│   ├── portfolio.json
│   ├── tasks.json
│   └── old-widget.json     ← Archived: file exists but not listed in index
```

## Dashboard Index (`dashboard.json`)

The index file at the repo root controls which widgets appear and in what order:

```json
{
  "widgets": ["weather", "portfolio", "tasks"]
}
```

- Array order = display order on the dashboard
- Each entry is a widget ID referencing `widgets/{id}.json`
- Widgets not in the array are hidden (archived) — their files are kept
- If `dashboard.json` doesn't exist, all widgets in `widgets/` are shown (unordered)

## Widget Format

Each widget file (`widgets/{id}.json`) contains a single widget object:

```json
{
  "id": "weather",
  "size": "S",
  "renderer": "webview",
  "html": "<div>...</div>"
}
```

Fields:
- **id** (string): Unique slug identifier — must match the filename (e.g., `weather` → `widgets/weather.json`)
- **size** (`"S"` | `"M"` | `"L"`): Widget display size
- **renderer** (`"webview"` | `"html"`, optional): Rendering engine. Default is `"html"` (native). Use `"webview"` for rich visuals.
- **html** (string): Self-contained HTML with inline styles

## Renderers

### `"webview"` — Rich widgets (recommended for most widgets)

Renders in a full browser engine. Supports:
- CSS gradients, shadows, `border-radius`, `backdrop-filter`
- CSS animations (`@keyframes`, `transition`)
- SVG (charts, icons, sparklines)
- Canvas
- JavaScript (live clocks, counters, data formatting)
- Base64 inline images (`<img src="data:image/png;base64,...">`)
- Full CSS flexbox and grid

The app wraps your HTML in a document with dark theme defaults (`background: #1f2937`, `color: #fff`, system font). You just provide the body content.

### `"html"` — Lightweight widgets (default)

Renders via native components (no browser). Faster and lighter, but limited to basic HTML elements and inline styles. No JS, no animations, no gradients, no SVG. Good for simple text/number displays.

**Use `"webview"` for anything visual.** Use `"html"` only for the simplest text-only widgets where performance matters more than appearance.

## Widget Sizes

Modeled after Apple's iOS widget system:

| Size | Dimensions | Layout | Best for |
|------|-----------|--------|----------|
| **S** (Small) | 174 × 174 px | Square, 1 column | Single metric, status, icon |
| **M** (Medium) | 361 × 174 px | Full width, short | Info card, sparkline, summary |
| **L** (Large) | 361 × 382 px | Full width, tall | Chart, table, calendar, feed |

Two small widgets fit side-by-side. Medium and large span the full width.

## Creating a Widget

Two steps: create the widget file, then add it to the index.

```bash
cd wonderdash-widgets
mkdir -p widgets

# 1. Create the widget file
cat > widgets/weather.json << 'EOF'
{
  "id": "weather",
  "size": "S",
  "renderer": "webview",
  "html": "..."
}
EOF

# 2. Add to dashboard.json index
# If dashboard.json doesn't exist yet, create it:
echo '{ "widgets": ["weather"] }' > dashboard.json
# If it already exists, read it, append the new ID to the widgets array, and write it back.

git add widgets/weather.json dashboard.json
git commit -m "Add weather widget"
git push
```

## Updating a Widget

Edit the widget file and push. No change to `dashboard.json` needed unless reordering.

```bash
git add widgets/weather.json
git commit -m "Update weather widget"
git push
```

## Reordering / Archiving / Deleting

- **Reorder:** Rearrange the array in `dashboard.json`, commit, push.
- **Archive:** Remove the ID from `dashboard.json` — widget file stays in repo.
- **Restore:** Add the ID back to the array.
- **Delete permanently:** Remove from `dashboard.json` + `git rm widgets/{id}.json`, commit, push.

The user pulls down on their dashboard to refresh. Changes appear after a manual refresh.

## Design Guidelines

- **Dark theme.** Background: `#1f2937` (gray-800). Text: `#ffffff`. Secondary: `#9ca3af` (gray-400). Accent: `#3b82f6` (blue-500). Success: `#22c55e`. Warning: `#eab308`. Error: `#ef4444`.
- **Self-contained.** No external resources (CDNs, APIs, remote images). Everything inline.
- **JSON escaping.** Escape quotes in HTML when inside JSON strings. Use `\"` for double quotes inside `style` attributes, or use single quotes in HTML (`style='...'`).
- **Fit the size.** Content must fit within the widget dimensions without scrolling. WebView has `overflow: hidden` by default.
- **Subtle animation.** Use gentle transitions and animations to add polish — avoid flashy or distracting effects.

## Examples

### Small — Gradient metric (`widgets/temperature.json`)

A temperature display with gradient background and subtle glow.

```json
{
  "id": "temperature",
  "size": "S",
  "renderer": "webview",
  "html": "<div style='display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;background:linear-gradient(135deg,#1e3a5f,#1f2937);padding:16px'><div style='font-size:11px;color:#60a5fa;text-transform:uppercase;letter-spacing:2px;font-weight:600'>Temperature</div><div style='font-size:52px;font-weight:bold;margin:8px 0;background:linear-gradient(180deg,#fff,#93c5fd);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>72°</div><div style='font-size:13px;color:#9ca3af'>☀️ Sunny</div></div>"
}
```

### Small — Animated status (`widgets/api-status.json`)

A pulsing status indicator with CSS animation.

```json
{
  "id": "api-status",
  "size": "S",
  "renderer": "webview",
  "html": "<style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}.pulse{animation:pulse 2s ease-in-out infinite}</style><div style='display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;padding:16px'><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px'>API Status</div><div class='pulse' style='width:48px;height:48px;border-radius:50%;background:radial-gradient(circle,#22c55e,#15803d);box-shadow:0 0 20px rgba(34,197,94,0.4);margin-bottom:12px'></div><div style='font-size:15px;font-weight:600;color:#22c55e'>Operational</div><div style='font-size:12px;color:#6b7280;margin-top:4px'>99.9% uptime</div></div>"
}
```

### Medium — SVG sparkline chart (`widgets/revenue.json`)

A revenue card with an inline SVG sparkline.

```json
{
  "id": "revenue",
  "size": "M",
  "renderer": "webview",
  "html": "<div style='display:flex;align-items:center;height:100%;padding:16px;gap:20px'><div style='flex:1'><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px'>Monthly Revenue</div><div style='font-size:32px;font-weight:bold;margin:6px 0'>$48.2k</div><div style='font-size:13px;color:#22c55e;font-weight:500'>↑ 12.5% vs last month</div></div><div style='width:140px;height:60px'><svg viewBox='0 0 140 60' style='width:100%;height:100%'><defs><linearGradient id='g' x1='0' y1='0' x2='0' y2='1'><stop offset='0%' stop-color='#3b82f6' stop-opacity='0.3'/><stop offset='100%' stop-color='#3b82f6' stop-opacity='0'/></linearGradient></defs><path d='M0,45 L20,40 L40,42 L60,30 L80,35 L100,20 L120,18 L140,10 L140,60 L0,60Z' fill='url(#g)'/><polyline points='0,45 20,40 40,42 60,30 80,35 100,20 120,18 140,10' fill='none' stroke='#3b82f6' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg></div></div>"
}
```

### Medium — Gradient info card (`widgets/next-meeting.json`)

A meeting card with gradient accent border.

```json
{
  "id": "next-meeting",
  "size": "M",
  "renderer": "webview",
  "html": "<div style='display:flex;align-items:center;height:100%;padding:16px;gap:16px'><div style='width:4px;height:80%;border-radius:2px;background:linear-gradient(180deg,#8b5cf6,#3b82f6)'></div><div style='flex:1'><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px'>Next Meeting</div><div style='font-size:18px;font-weight:bold;margin:6px 0'>Sprint Planning</div><div style='font-size:13px;color:#9ca3af'>2:00 PM — 3:00 PM</div><div style='display:flex;gap:6px;margin-top:8px'><span style='font-size:11px;background:#374151;color:#d1d5db;padding:2px 8px;border-radius:10px'>Team Alpha</span><span style='font-size:11px;background:#374151;color:#d1d5db;padding:2px 8px;border-radius:10px'>Zoom</span></div></div></div>"
}
```

### Large — Price chart with SVG (`widgets/btc-price.json`)

A Bitcoin price chart with gradient fill, grid lines, and price labels.

```json
{
  "id": "btc-price",
  "size": "L",
  "renderer": "webview",
  "html": "<div style='display:flex;flex-direction:column;height:100%;padding:16px'><div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:4px'><div><div style='font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:1px'>Bitcoin</div><div style='font-size:28px;font-weight:bold;margin-top:4px'>$67,432</div></div><div style='text-align:right'><div style='font-size:14px;color:#22c55e;font-weight:600'>+2.4%</div><div style='font-size:12px;color:#6b7280'>24h</div></div></div><div style='flex:1;margin-top:8px;position:relative'><svg viewBox='0 0 330 240' style='width:100%;height:100%' preserveAspectRatio='none'><defs><linearGradient id='cg' x1='0' y1='0' x2='0' y2='1'><stop offset='0%' stop-color='#f59e0b' stop-opacity='0.25'/><stop offset='100%' stop-color='#f59e0b' stop-opacity='0'/></linearGradient></defs><line x1='0' y1='60' x2='330' y2='60' stroke='#374151' stroke-width='0.5'/><line x1='0' y1='120' x2='330' y2='120' stroke='#374151' stroke-width='0.5'/><line x1='0' y1='180' x2='330' y2='180' stroke='#374151' stroke-width='0.5'/><text x='325' y='58' fill='#6b7280' font-size='10' text-anchor='end'>69k</text><text x='325' y='118' fill='#6b7280' font-size='10' text-anchor='end'>67k</text><text x='325' y='178' fill='#6b7280' font-size='10' text-anchor='end'>65k</text><path d='M0,180 C30,175 50,160 80,140 C110,120 130,90 160,100 C190,110 210,130 230,80 C250,40 270,55 300,30 C310,25 320,28 330,20 L330,240 L0,240Z' fill='url(#cg)'/><path d='M0,180 C30,175 50,160 80,140 C110,120 130,90 160,100 C190,110 210,130 230,80 C250,40 270,55 300,30 C310,25 320,28 330,20' fill='none' stroke='#f59e0b' stroke-width='2.5' stroke-linecap='round'/><circle cx='330' cy='20' r='4' fill='#f59e0b'/><circle cx='330' cy='20' r='8' fill='#f59e0b' opacity='0.2'/></svg></div><div style='display:flex;justify-content:space-between;font-size:11px;color:#6b7280;margin-top:4px'><span>6h ago</span><span>4h</span><span>2h</span><span>Now</span></div></div>"
}
```

### Large — Calendar grid (`widgets/calendar.json`)

A monthly calendar with CSS grid and highlighted dates.

```json
{
  "id": "calendar",
  "size": "L",
  "renderer": "webview",
  "html": "<style>.day{display:flex;align-items:center;justify-content:center;height:36px;border-radius:50%;font-size:13px;color:#d1d5db}.today{background:#3b82f6;color:#fff;font-weight:bold}.event{position:relative}.event::after{content:'';position:absolute;bottom:2px;left:50%;transform:translateX(-50%);width:4px;height:4px;background:#f59e0b;border-radius:50%}.muted{color:#4b5563}</style><div style='display:flex;flex-direction:column;height:100%;padding:16px'><div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:12px'><div style='font-size:16px;font-weight:bold'>March 2026</div><div style='font-size:12px;color:#9ca3af'>3 events</div></div><div style='display:grid;grid-template-columns:repeat(7,1fr);gap:2px;text-align:center'><div style='font-size:11px;color:#6b7280;padding:4px 0'>Su</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Mo</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Tu</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>We</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Th</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Fr</div><div style='font-size:11px;color:#6b7280;padding:4px 0'>Sa</div><div class='day'>1</div><div class='day today'>2</div><div class='day'>3</div><div class='day event'>4</div><div class='day'>5</div><div class='day'>6</div><div class='day'>7</div><div class='day'>8</div><div class='day'>9</div><div class='day event'>10</div><div class='day'>11</div><div class='day'>12</div><div class='day'>13</div><div class='day'>14</div><div class='day'>15</div><div class='day'>16</div><div class='day'>17</div><div class='day event'>18</div><div class='day'>19</div><div class='day'>20</div><div class='day'>21</div><div class='day'>22</div><div class='day'>23</div><div class='day'>24</div><div class='day'>25</div><div class='day'>26</div><div class='day'>27</div><div class='day'>28</div><div class='day'>29</div><div class='day'>30</div><div class='day'>31</div></div></div>"
}
```

### Example `dashboard.json`

```json
{
  "widgets": ["temperature", "api-status", "revenue", "next-meeting", "btc-price", "calendar"]
}
```
