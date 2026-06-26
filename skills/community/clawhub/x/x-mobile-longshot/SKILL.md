---
name: x-mobile-longshot
description: Render X (Twitter) posts, long articles, and mobile reading pages into mobile-style long screenshots and optional single-page PDFs using Playwright. Use when the user wants a result that looks like a phone X page or asks for long screenshot export, X article export, mobile-style PDF, app-like dark-mode capture, or cleaner archival output than ordinary print-to-PDF.
---

# X Mobile Longshot

Render X links into phone-like dark-mode long screenshots, then optionally wrap the image into a single-page PDF.

## Quick start

Use the bundled script:

```bash
node skills/x-mobile-longshot/scripts/render_x_longshot.js \
  --url 'https://x.com/i/status/2030475950752710891' \
  --out-png 'outputs/x_render/example.png' \
  --out-pdf 'outputs/x_render/example.pdf'
```

If the user only wants the PNG:

```bash
node skills/x-mobile-longshot/scripts/render_x_longshot.js \
  --url 'https://x.com/i/status/2030475950752710891' \
  --out-png 'outputs/x_render/example.png' \
  --no-pdf
```

## Workflow

1. Use Playwright mobile emulation, dark mode, and a phone device preset.
2. Open the X URL and wait for the page to settle.
3. Dismiss top modal/app-open prompts with DOM-side clicks when present.
4. Remove common fixed/sticky overlays by matching known X CTA text.
5. Capture one full-page PNG.
6. Re-open the page, repeat cleanup, capture one clean viewport image.
7. Replace the top portion of the long PNG with the clean viewport image to reduce popup contamination.
8. Convert the PNG into a single-page PDF when requested.

## Defaults

- Device: `iPhone 14 Pro Max`
- Color scheme: dark
- Locale: `zh-CN`
- Timezone: `Asia/Shanghai`
- Top replacement height: `1450px`

## Tuning

Useful flags:

- `--device 'iPhone 14 Pro Max'` to change the Playwright device preset
- `--wait-ms 6000` to wait longer for slow pages
- `--top-fix-px 1700` to replace more of the top area when the popup intrudes deeper
- `--no-pdf` to skip PDF creation

## Quality bar

Prefer this skill when the user wants:
- phone-like visual presentation
- dark-mode X reading output
- archival PNG + PDF delivery
- a result that feels closer to a real screenshot than browser print output

Do not overclaim native-app fidelity. This is a browser-rendered mobile capture pipeline with cleanup, not a real iPhone App Store build of X.

## Troubleshooting

If the output still contains overlays or sticky bars:

1. Re-run with higher `--wait-ms`.
2. Increase `--top-fix-px`.
3. Read `references/notes.md` and update the overlay text patterns in `scripts/render_x_longshot.js`.
4. If X changed its DOM substantially, migrate to segmented capture + stitching as the next iteration.

## Resources

- `scripts/render_x_longshot.js`: main renderer
- `references/notes.md`: v1 design notes, limits, and iteration guidance
