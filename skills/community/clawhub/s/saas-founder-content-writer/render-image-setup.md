# Render Image Setup

`scripts/render-image.js` turns an HTML/CSS file into a PNG using headless Chrome. Use it to produce **text- and data-driven graphics** — Xiaohongshu covers and image cards, quote/data/metric cards, changelog cards, framework or comparison diagrams — deterministically and in batch. It is not for photographic images or real product screenshots — see the rendering decision rule in `SKILL.md`.

No credentials, tokens, or network access are required.

## First-time setup

1. Install the dependency (downloads a bundled Chromium):

   ```sh
   cd scripts
   npm install
   ```

2. Verify rendering works by rendering a bundled example template:

   ```sh
   node render-image.js ../assets/xiaohongshu-cover.html /tmp/xhs-cover.png --width=1080 --height=1440
   ```

   Success prints a line beginning with `OK` and the output path. Open the PNG to confirm.

## Daily use

```sh
node scripts/render-image.js <input.html> <output.png> [--width=1080] [--height=1440] [--scale=2] [--full]
```

| Option | Default | Notes |
| --- | --- | --- |
| `--width` | `1080` | Viewport width in CSS pixels. |
| `--height` | `1440` | Viewport height in CSS pixels. |
| `--scale` | `2` | `deviceScaleFactor`; 2 → crisp 2× PNG. |
| `--full` | off | Capture full scrollable height instead of the fixed viewport. |

**Recommended sizes**

| Use | Width × Height |
| --- | --- |
| Xiaohongshu cover / image card (3:4) | `1080 × 1440` |
| Square card (quote / data) | `1080 × 1080` |
| LinkedIn / X landscape (16:9) | `1600 × 900` |
| Portrait card (4:5) | `1080 × 1350` |

Output PNG goes to whatever path you pass; default to the current working directory. Do not write credentials or tokens anywhere.

## Workflow

1. Author an HTML file (inline CSS, no external network assets — embed fonts/colors directly). Start from `assets/xiaohongshu-cover.html` or `assets/data-card.html`.
2. Run the script with the size for the target slot (3:4 for Xiaohongshu).
3. Attach the PNG to the post. For a Xiaohongshu carousel, render one HTML per card and keep the cover as the first image.

## Fallback

If the bundled Chromium cannot launch, the script tries a system Chrome (set `PUPPETEER_EXECUTABLE_PATH` to force one). If no browser is available, it **keeps the HTML file**, prints manual-render instructions, and exits non-zero. You can then render the HTML by hand in Chrome (DevTools → "Capture node screenshot") or with `chrome --headless --screenshot`.

## Sandbox flags (Linux / containers)

The script launches Chromium with the OS sandbox **enabled** by default, which works on macOS and most Linux desktops. Some environments — root-user Docker containers or CI runners — require extra Chromium launch flags or the browser will not start. In those cases pass the flags explicitly via the `RENDER_CHROME_ARGS` environment variable:

```sh
RENDER_CHROME_ARGS='<chromium-flags>' node render-image.js card.html card.png
```

Use the flag values from Puppeteer's troubleshooting guide for containers and root users: <https://pptr.dev/troubleshooting>. Only set this when a launch fails for sandbox reasons; leaving it unset keeps the OS sandbox on.
