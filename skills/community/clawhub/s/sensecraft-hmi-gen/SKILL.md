---
name: sensecraft-hmi-gen
description: Generate beautiful web content for SenseCraft HMI e-ink displays. AI-powered layout selection, e-ink optimization. Creates artistic, minimalist pages optimized for e-ink screens (800x480 to 1600x1200).
---

# SenseCraft HMI Web Content Generator

Generate stunning, e-ink optimized web content with AI-powered design.

## Philosophy

**E-ink screens are digital art pieces, not web pages.**

Inspired by Kindle screensavers and minimalist posters. Every page should be beautiful enough to frame.

---

## AI Workflow

When the user requests to generate e-ink screen content, execute according to the following workflow:

### Step 1: Study Reference Files and Keep Them in Mind

**Read design reference files (mandatory):**

Design Philosophy - `{baseDir}/references/design-patterns.md`

10 Classic Layout References - `{baseDir}/references/layouts.md`, but do not limit yourself to these layouts. Specifically, when the user provides layout ideas, follow the user's instructions.

### Step 2: Guide the User to Answer Necessary Configuration Information

If the user is conversing with you via a webchat channel, call the `wizard.js` script. This script will serve a web page at http://localhost:39527/ and pop up this visual configuration interface in the user's browser. The script will automatically exit once the user completes the configuration. The script will create a `{baseDir}/data/.wizard-config.json` file to save the configuration information.

If the user is using a remote conversation channel like Discord, use dialogue to ask the user for the following information:
- Screen size and color support
- The user's ideas about the layout

These configuration details will be saved in the `{baseDir}/data/.wizard-config.json` file. Subsequent workflows should follow these configurations, such as the size of the generated web page, color support, etc.

### Step 3: Prepare Content

**Text Content:**
- AI generates content based on user requests (quotes, poems, weather info, etc.)
- Or use content provided by the user

**Image Content (if the user's request explicitly mentions the need for images):**

Ask the user for the image source:
- User provides image URL
- User provides local image
- If openclaw is configured with a text-to-image large model, call it to generate an image

Image storage path: `{baseDir}/data/public/images/`

### Step 4: Generate HTML

Generate an HTML file based on the user's requirements and store it in the `{baseDir}/data/` directory. The HTML file can contain Javascript, and the image paths referenced in the HTML should be `./public/images/`.

Please embed CSS directly into the HTML file. If you need to reference a CSS framework like Bootstrap, use the CDN link for the CSS file.

Please embed Javascript scripts directly into the HTML file. If you need to reference a JS framework like jQuery, use the CDN link for the JS file.

**Primary rules for the web page**:
- The pixel count of the entire web page's visible area must match the screen size exactly; there should be no scrolling controls.
- The colors used in the web page should not exceed the color support capabilities of the screen. This includes controlling the background color, text color, image color, etc., using CSS.

Design philosophy and layout references:
- `{baseDir}/references/design-patterns.md`
- `{baseDir}/references/layouts.md`


### Step 5: Start server.js

We use pm2 to manage the http server.

```bash
# Start service
pm2 start {baseDir}/data/server.js --name sensecraft-hmi

# Stop service
pm2 stop sensecraft-hmi

# View logs
pm2 logs sensecraft-hmi

# Access address
http://localhost:19527/?token=XXXXX
```

After the server starts, automatically open a browser to visit http://localhost:19527/?token=XXXXX so the user can see the generated web page. Also, prompt the user in the chat interface that they can open the http://localhost:19527/?token=XXXXX link to view the web page effect in real-time.

### Step 6: Reverse Proxy

Guide the user to use a reverse proxy tool to forward `http://localhost:19527` to the public network, and then use the `html` widget in the SenseCraft HMI platform to display the web page.

Reverse proxy tools include: frp, ngrok, cloudflare tunnel, etc. Encourage users to use HTTP forwarding rather than TCP forwarding because HTTP is more secure.

Due to openclaw skill security review reasons, this skill does not provide the binary of reverse proxy tools. Please ask the user to search, download, and use them on their own.

---

## Tool List

| Tool | Description | Usage |
|------|-------------|-------|
| `init_project.js` | Project initialization | `node {baseDir}/scripts/init_project.js` |
| `wizard.js` | Configuration wizard server | `node {baseDir}/scripts/wizard.js` |

---

## 10 Classic Layouts

See `references/layouts.md` for detailed specs.

| Layout | ID | Use Case |
|--------|-----|----------|
| Minimalist Center | `minimalCenter` | Quotes, maxims, single words |
| Info Card | `infoCard` | Poetry, elegant text |
| Dashboard Grid | `dashboardGrid` | Weather, stocks, data |
| Comic Fullscreen | `comicFullscreen` | Comics, artwork |
| Calendar Grid | `calendarGrid` | Calendars, schedules |
| News List | `newsList` | News, RSS, to-do lists |
| Split Layout | `splitLayout` | Sidebar + main content |
| Big Number | `bigNumber` | Clocks, countdowns |
| Image & Text | `imageText` | Images + captions |
| Newspaper Front | `newspaperFront` | News summaries |


---

## Scheduled Updates

If the user's request includes scheduled tasks, there are 3 approaches:

1. Use OpenClaw cron to update content on a schedule, suitable when each update's content varies significantly

```bash
openclaw cron add --name "daily-summary" --schedule "0 9 * * *" \
  --task "Generate a work summary based on Notion"
```

2. Embed Javascript scripts within the HTML file to dynamically update content, suitable for pulling data from APIs

3. Write background services in a Node.js Express backend using templating technologies or frameworks like React to push data from backend to frontend, suitable for particularly complex content updates

---

## Files Structure

```
sensecraft-hmi-gen/
├── SKILL.md                    # This file (current file)
├── data/                       # Source files for AI-generated web pages
│   ├── server.js               # Express server
│   ├── index.html              # Currently displayed content
│   ├── .token                  # Access token
│   ├── public/images/          # Image resources (optional)
│   ├── public/css/             # CSS resources (optional)
│   └── public/js/              # JS resources (optional)
├── scripts/
│   ├── init_project.js         # Project initialization
│   ├── wizard.js               # Configuration wizard server (Frontend + Backend)
└── references/
    ├── layouts.md              # Detailed layout specifications
    ├── design-patterns.md      # Design patterns and aesthetics
    └── screen-specs.md         # Hardware specifications

```

---

## Tips

- **Let AI be creative** - Don't force templates, let design flow from content
- **Read design references** - design-patterns.md and layouts.md are your inspiration
- **Go bigger than you think** - fonts that look huge on screen look perfect on e-ink
- **Test with actual device** - e-ink looks different than LCD
- **Embrace whitespace** - it's not wasted space, it's elegance

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Text too small | Minimum 32px, headings 60px+ |
| Blurry images | Apply color dithering to images to make them better suited for e-ink displays |
| Crowded layout | Increase padding to 40-60px |
| Service inaccessible | Check token, run `pm2 restart sensecraft-hmi` |