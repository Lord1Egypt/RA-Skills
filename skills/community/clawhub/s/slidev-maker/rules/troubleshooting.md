# Slidev Troubleshooting & Best Practices

Fixing common problems and authoring high-quality decks.

## Build Issues

If a build fails, clear the Vite cache and rebuild:
```bash
rm -rf node_modules/.vite
slidev build
```

## Export Issues

Export requires Playwright Chromium:
```bash
pnpm add -D playwright-chromium
```

**Missing / blank content** — give async content more time:
```bash
slidev export --wait 2000
slidev export --timeout 60000
```

**Broken emojis** — install system emoji fonts or use Iconify icons instead (see `assets.md`).

**Large file size** — export a subset of slides or reduce image resolution:
```bash
slidev export --range 1,6-8,10
```

**Browser not found** — point to a Chromium binary:
```bash
slidev export --executable-path /path/to/chromium
```

See `export.md` for the full list of export flags.

## Port Conflicts

The dev server defaults to port 3030. Use a different port:
```bash
slidev --port 3333
```

## Theme Not Loading

Ensure the theme package is installed and named correctly in headmatter:
```bash
pnpm add slidev-theme-NAME
```
```md
---
theme: NAME
---
```

See `themes.md` for theme resolution, local themes, and ejecting.

## Common Mistakes

Before debugging, check `anti-patterns.md` — most issues come from a small set of recurring mistakes:
- Relative asset paths in frontmatter (use `/path` from `public/`)
- Referencing the removed Prism highlighter (Shiki only)
- Using non-existent layouts (`split`, `title-slide`, `columns`, …)
- Unquoted relative click values (`v-click="'+1'"`)
- Missing curly braces around code line-highlight ranges

## Best Practices

### Organization
- One concept per slide; keep slides focused and minimal.
- Use layouts consistently and group related slides with `section` dividers.
- Split long decks into multiple files via `src:` (see `features.md`).

### Performance
- Optimize images before adding them to `public/`.
- Prefer built-in components; lazy-load heavy custom ones.
- Test export early for large presentations.

### Collaboration
- Version-control `slides.md` and assets.
- Document custom components and share themes as npm packages.
- Run `slidev format` for consistent formatting.

### Presenting
- Test presenter mode and all interactive features beforehand.
- Prepare speaker notes (see `presenter.md`).
- Keep a PDF backup ready.
