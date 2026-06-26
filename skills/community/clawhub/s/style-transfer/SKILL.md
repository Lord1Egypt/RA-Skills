---
name: style-transfer
description: 提取目标网站的设计系统并应用到指定项目中（Vue/React/Next.js/Tailwind）。当用户说「把 XX 网站的样式应用到我的项目」或「用 Y 的风格重新设计」时使用。
category: software-development
---

# style-transfer（风格迁移）

> 将目标网站的设计风格迁移到指定项目中

## Workflow

### Step 1 — Extract design from target website

```bash
npx designlang https://target-website.com/ --full
```

Or for faster extraction (no screenshots/interactions):
```bash
npx designlang https://target-website.com/
```

Output goes to `~/.designlang/{domain}.json` and `~/.hermes-agent/workspace/design-extract-output/`.

### Step 2 — Detect project type

Inspect the project at the target path:

```bash
# Detect framework
ls /path/to/project/src/                    # Vue/React
ls /path/to/project/                       # Next.js (app/, pages/)
cat /path/to/project/package.json | grep -E "vue|react|next"

# Detect styling approach
ls /path/to/project/src/assets/styles/      # SCSS/CSS variables
cat /path/to/project/tailwind.config.js     # Tailwind
cat /path/to/project/src/style.css          # Plain CSS
cat /path/to/project/src/App.vue            # Vue SFC styles
```

### Step 3 — Read extracted design files

Key files to read from `~/.hermes-agent/workspace/design-extract-output/`:

| File | Purpose |
|------|---------|
| `*-design-tokens.json` | DTCG format tokens (primitive + semantic) |
| `*-tailwind.config.js` | Tailwind theme config |
| `*-shadcn-theme.css` | shadcn/ui CSS variables |
| `*-global.css` / `*-variables.css` | CSS custom properties |
| `*-design-language.md` | Full design doc (colors, fonts, spacing) |
| `*-gradients.css` | Brand gradients |
| `*-motion-tokens.json` | Animation tokens |

### Step 4 — Apply styles based on project type

#### Vue 3 + Vite project

**global.scss / main CSS — replace CSS variables:**
```scss
// src/assets/styles/global.scss
// Replace :root variables with extracted tokens
:root {
  --primary-color: #7f41ff;        // from design-tokens.json
  --bg-color: #fdfcff;
  --text-primary: #261c3a;
  --border-color: #d9bfe2;
  --radius: 16px;
  --shadow: 0 0 24px rgba(0,0,0,0.03);
  --gradient-brand: linear-gradient(90deg, #7f41ff, #ab8ee8);
}
```

**Add Google Fonts to index.html:**
```html
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
```

**Component styles — update `<style>` blocks:**
- Replace button `background` with `--gradient-brand`
- Replace `border-radius` values with `--radius`
- Replace shadows with `--shadow`
- Update tag styles to pill shape (`border-radius: 999px`)

#### Next.js / React project

**Tailwind config — merge extracted tokens:**
```js
// tailwind.config.js
colors: {
  primary: '#7f41ff',
  secondary: '#ab8ee8',
  accent: '#d9bfe2',
}
```

**globals.css:**
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --primary: #7f41ff;
    --background: #fdfcff;
  }
}
```

#### Plain HTML / Static site

Inject the `*-variables.css` content into `<style>` tag and add Google Fonts link.

### Step 5 — Build and verify

```bash
cd /path/to/project
npm run build
# or
npm run dev
```

Check dist output for:
- CSS contains new color tokens (grep for primary hex)
- No build errors
- Font loaded correctly

## Common Pitfalls

1. **npx designlang hangs** — use without `--full` flag, timeout after 120s
2. **Project has no src/styles** — create `src/assets/styles/global.scss` and import in `main.js` / `main.tsx`
3. **CSS variable conflicts** — ensure new variables override old ones; check specificity
4. **Font not loading** — verify Google Fonts URL in `<head>`, check network
5. **Tailwind purge removes new classes** — ensure design tokens are in `content[]` paths
6. **Vue scoped styles** — CSS vars defined in `:root` or `global.scss` leak into scoped styles correctly

## Verification Commands

```bash
# Check CSS variables applied
grep -o "#[0-9a-fA-F]\{6\}" dist/assets/*.css | sort | uniq

# Check gradient applied
grep -c "gradient" dist/assets/*.css

# Check font loaded
grep "fonts.googleapis" dist/index.html
```

## Project Path Resolution

If user says "my project" without specifying path:
- Check current working directory for `package.json`
- Check `../` for project with `src/` directory
- Ask user for explicit path if ambiguous

## Example Conversation

**User**: "把 withlantern.com 的样式应用到我的 Vue 项目里"

1. `npx designlang https://withlantern.com/` → extract design
2. Read `*-design-tokens.json` → get color palette
3. Read `*-global.css` → get CSS variables
4. Read project's `src/assets/styles/global.scss` → apply new variables
5. Add Google Fonts to `index.html`
6. Update component button styles to use gradient
7. `npm run build` → verify
