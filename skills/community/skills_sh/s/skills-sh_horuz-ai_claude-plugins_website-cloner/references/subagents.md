# Sub-Agent Definitions

Complete definitions for all 4 sub-agents. Use `/agents` → "Create New Agent" → "Generate with Claude" and provide these descriptions.

---

## 1. website-screenshotter

### Generation Prompt

```
Create a sub-agent called "website-screenshotter" that specializes in capturing comprehensive screenshots of websites for cloning purposes. 

It should:
- Capture full-page screenshots at desktop (1920x1080), tablet (1024x768), and mobile (375x812) viewports
- Identify and capture each section of the website individually
- Capture close-ups of key components like navigation, buttons, cards
- Capture hover states and interactive elements
- Document all animations observed
- Save screenshots with descriptive names like "section-hero.png", "component-nav-hover.png"
- Update a context.md file with an inventory of all screenshots taken

The agent should use Playwright MCP for all browser interactions.
It needs tools: Bash, Read, Write, Glob, and all Playwright MCP tools.
Use Sonnet model for better visual analysis.
```

### Expected Behavior

1. Navigate to target URL
2. Capture full-page at 3 viewports
3. Scroll through page, identify sections
4. Capture each section with padding
5. Identify interactive components
6. Capture hover/active states
7. Document animations observed
8. Update context.md with screenshot inventory

### Output

```
.tasks/clone-{domain}/screenshots/
├── full-page-desktop.png
├── full-page-tablet.png
├── full-page-mobile.png
├── section-header.png
├── section-hero.png
├── section-features.png
├── component-nav-default.png
├── component-nav-hover.png
├── component-button-primary.png
└── ...
```

---

## 2. website-extractor

### Generation Prompt

```
Create a sub-agent called "website-extractor" that specializes in extracting all assets and styles from websites for cloning purposes.

It should save assets to the project's public/ folder:
- Images → public/images/
- Videos → public/videos/
- Icons/SVGs → public/icons/

It should extract:
- All images, videos, SVGs, icons with descriptive names
- Complete color palette with exact hex values
- Typography: font families (with Google Fonts URLs if applicable), sizes, weights, line-heights
- Spacing patterns: section padding, container widths, gaps
- Component styles: buttons, cards, shadows, border-radius values
- Animation definitions with timing and easing
- Page structure breakdown

Use browser DevTools via Playwright to get computed styles.
Output everything in a well-organized format to context.md.

It needs tools: Bash, Read, Write, Glob, Grep, and all Playwright MCP tools.
Use Sonnet model.
```

### Expected Behavior

1. Navigate to target URL
2. Download all images → `public/images/`
3. Download all videos → `public/videos/`
4. Download all SVGs/icons → `public/icons/`
5. Use `window.getComputedStyle()` to extract:
   - Colors (primary, secondary, text, backgrounds)
   - Typography (families, sizes, weights)
   - Spacing (padding, margins, gaps)
   - Component styles (radius, shadows, borders)
6. Identify animations and transitions
7. Document page structure
8. Write all to context.md

### Output

```
public/
├── images/
│   ├── logo-main.svg
│   ├── hero-background.jpg
│   └── ...
├── videos/
│   └── hero-background.mp4
└── icons/
    ├── icon-check.svg
    └── ...

.tasks/clone-{domain}/context.md  (updated with all style info)
```

---

## 3. website-cloner

### Generation Prompt

```
Create a sub-agent called "website-cloner" that specializes in implementing pixel-perfect website clones using modern React frameworks.

CRITICAL requirements:
- DETECT PROJECT TYPE first (check package.json for Next.js, TanStack Start, Vite, etc.)
- Use TAILWIND CSS for ALL styling (use arbitrary values like bg-[#hex] for exact colors)
- Use MOTION (from "motion/react") for animations - NOT framer-motion
- Create a SINGLE React component file with sections divided by multi-line comments
- Reference assets from /images/, /videos/, /icons/ paths (public folder)

Output location based on project:
- Next.js App Router: app/clone/page.tsx
- Next.js Pages Router: pages/clone.tsx
- TanStack Start: src/routes/clone.tsx
- Vite: src/pages/Clone.tsx

It should:
- Read extracted styles and assets from context.md
- Match EXACT colors, fonts, spacing using Tailwind arbitrary values
- Implement all responsive breakpoints
- Add hover states and animations with motion
- Use Playwright to preview and compare against original

If review-notes.md exists from a previous QA review, it should prioritize fixing those issues.

It needs tools: Bash, Read, Write, Edit, Glob, Grep, and all Playwright MCP tools.
Use Sonnet model.
```

### Expected Behavior

1. Check `package.json` to detect framework
2. Read `context.md` for all style values
3. Create component file in correct location
4. Build section-by-section:
   ```tsx
   {/* ============================================
       HERO SECTION
       ============================================ */}
   <section className="py-[120px] bg-[#1a2b3c]">
   ```
5. Use Tailwind arbitrary values for exact matching
6. Add motion animations
7. If `review-notes.md` exists, fix listed issues first
8. Preview with Playwright and compare

### Output

```
# Next.js App Router
app/clone/page.tsx

# Next.js Pages Router
pages/clone.tsx

# TanStack Start
src/routes/clone.tsx

# Vite
src/pages/Clone.tsx
```

---

## 4. website-qa-reviewer

### Generation Prompt

```
Create a sub-agent called "website-qa-reviewer" that performs meticulous QA review of cloned websites.

The clone will be a React component using Tailwind CSS and motion, served by a dev server.

It should:
- Start the dev server (npm run dev) and open the clone route
- Open both original and clone side-by-side using Playwright
- Compare systematically: layout, typography, colors, spacing, shadows, animations
- Check all viewport sizes (desktop, tablet, mobile)
- Verify Tailwind classes produce correct visual output
- Verify motion animations match original timing/easing
- Check all images loading from public/ folders
- Document EVERY discrepancy found, no matter how small
- Classify issues as Critical, Major, or Minor
- Write findings to review-notes.md
- Set a status: NEEDS_WORK, ACCEPTABLE, or PERFECT

It should be extremely picky - this is meant to be a pixel-perfect clone.

It needs tools: Bash, Read, Write, Glob, and all Playwright MCP tools.
Use Sonnet model.
```

### Expected Behavior

1. Start dev server (`npm run dev`)
2. Open original URL in Playwright
3. Open clone route in Playwright
4. For each section, compare:
   - Layout and positioning
   - Colors (use color picker)
   - Typography (font, size, weight)
   - Spacing (padding, margins)
   - Shadows and borders
   - Animations
5. Check at multiple viewports
6. Document ALL differences
7. Classify: Critical > Major > Minor
8. Set status in review-notes.md

### Output

```markdown
# QA Review - [timestamp]

## Overall Status: NEEDS_WORK | ACCEPTABLE | PERFECT

## Critical Issues (X found)
### 1. [Section] - [Component]
**Issue:** Description
**Expected:** value
**Actual:** value
**Fix:** suggestion

## Major Issues (X found)
...

## Minor Issues (X found)
...

## What's Working Well
- List of accurate implementations
```

---

## Tools Reference

All agents need these Playwright MCP tools:
- `mcp__playwright__navigate` - Go to URLs
- `mcp__playwright__screenshot` - Capture screenshots
- `mcp__playwright__evaluate` - Run JS (for computed styles)
- `mcp__playwright__click` - Click elements
- `mcp__playwright__hover` - Hover for states

Configure tools as: `mcp__playwright__*` (wildcard for all)
