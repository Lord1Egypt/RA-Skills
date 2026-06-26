# yuanfang-design Authoring Guide

Rules for adding new themes, layout-types, or modifying the design system.

## Core principle: tokens, not literals

Every visual property (color, font, size, decoration) must reference a CSS variable defined in `base.css`. **No hardcoded hex codes, font names, or pixel sizes in layout-type files or theme .cover rules.**

❌ Bad:
```css
.cover__title { color: #4F46E5; font-size: 130px; }
```

✅ Good:
```css
.cover__title { color: var(--accent); font-size: var(--title-size-v); }
```

## Adding a new theme

1. Copy any existing theme to `themes/<name>.css`
2. Override the tokens you need; leave the rest at base.css defaults
3. Required overrides: `--bg`, `--text`, `--accent` (at minimum)
4. Optional: `--decor-*`, `--accent-line/block`, `--seal`, etc.
5. Test: `npm run render -- --theme <name> --layout cover --platforms xiaohongshu-v`
6. Update showcase/cover-showcase.html to include the new theme

## Adding a new layout-type

1. Create `layout-types/<name>.html` with `{{}}` placeholders for content
2. Add corresponding rules to `base.css` under `.layout-<name>` (or new file)
3. Reference only tokens, never literals
4. Add responsive `@media` queries for 6 aspect ratios
5. Test: `npm run render -- --theme minimal-white --layout <name> --platforms all`
6. Add to showcase

## Token reference

See `base.css` for full token list. Most common:

- **Colors**: `--bg`, `--text`, `--accent`, `--secondary`, `--bg-alt`
- **Fonts**: `--font-title`, `--font-body`
- **Sizes** (per ratio): `--title-size-v/s/w/c`, `--content-size`, `--badge-size`
- **Space**: `--space-1` (8px) through `--space-4` (48px)
- **Decor**: `--decor-tl/tr/bl/br` (gradient or url)
- **Flags**: `--accent-line`, `--accent-block`, `--terminal-bar`, `--grid-bg`, `--seal`

## Don't

- Don't add new tokens to base.css unless multiple themes need them
- Don't override tokens in `cover.html` or other layout files
- Don't add new CSS classes inside theme files (themes only override tokens)
- Don't use `!important` (find the specificity issue instead)
