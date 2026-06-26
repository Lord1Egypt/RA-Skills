---
name: tailwind-optimizer
description: Optimize Tailwind CSS usage — detect unused classes, identify opportunities for @apply extraction, audit responsive design, and reduce bundle size.
metadata:
  tags: ["tailwind", "css", "optimization", "frontend", "design-system"]
---

# Tailwind Optimizer

Optimize Tailwind CSS usage by detecting unused utilities, identifying extraction opportunities, auditing responsive design consistency, and reducing CSS bundle size. Analyzes config, class usage patterns, and design system adherence.

## Usage

```
"Optimize my Tailwind CSS setup"
"Find unused Tailwind classes"
"Audit responsive design coverage"
"Check my Tailwind config for issues"
```

## How It Works

### 1. Configuration Audit

```bash
cat tailwind.config.js 2>/dev/null || cat tailwind.config.ts 2>/dev/null
cat postcss.config.js 2>/dev/null
```

**Check:**
- Content paths cover all template files
- Theme extension vs override (prefer `extend`)
- Unused plugins loaded
- Custom colors/spacing consistency
- Dark mode strategy (class vs media)
- Prefix configured for embedding in existing CSS

### 2. Class Usage Analysis

```bash
# Most used utilities
grep -roh 'class[Name]*="[^"]*"\|className={[^}]*}' src/ | sort | uniq -c | sort -rn | head -20
# Find long class strings (extraction candidates)
grep -rn 'class[Name]*="[^"]*"' src/ | awk -F'"' '{print NF-1, length($2), $0}' | sort -rn | head -10
```

**Detect:**
- Classes used only once (potential dead code)
- Repeated class combinations (extract to @apply or component)
- Conflicting utilities (e.g., `text-red-500 text-blue-500`)
- Arbitrary values that should be in theme config
- !important overrides indicating specificity issues

### 3. Design System Adherence

- Using theme values vs arbitrary values (`w-[137px]` vs `w-36`)
- Consistent spacing scale usage
- Color palette adherence (no off-brand colors)
- Typography scale consistency
- Border radius consistency

### 4. Responsive Design

- Mobile-first approach (base styles for mobile, `md:` for desktop)
- Missing breakpoints on layout components
- Inconsistent responsive patterns across pages
- Hidden elements that should use `sr-only` for accessibility
- Container width and padding consistency

### 5. Bundle Optimization

- Purge/content configuration catching all files
- JIT mode enabled (v3+ default)
- Unnecessary variants enabled
- Large custom plugins adding unused CSS
- Component library classes not tree-shaken

### 6. Extraction Recommendations

When a class combination appears 3+ times:
```css
/* Before: repeated in 5 components */
<button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium">

/* After: extracted */
@layer components {
  .btn-primary {
    @apply px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium;
  }
}
```

## Output

```
## Tailwind CSS Optimization Report

**Version:** Tailwind 4.0 | **Unique classes:** 847
**CSS output:** 34KB (gzipped: 8KB)

### 🟡 Improvements (5)
1. **12 extraction candidates** — repeated class combos (3+ times)
   Top: `flex items-center gap-2` (23 times) → extract to `.flex-row-center`
2. **34 arbitrary values** could use theme tokens
   `text-[#1a1a1a]` → `text-gray-900` (already in palette)
3. **Missing responsive on 8 layout components** — desktop-only layouts
4. **3 conflicting utilities** — `p-4 px-6` (px overrides p's horizontal)
5. Content config missing `*.mdx` files (MDX pages unstyled)

### ✅ Good Practices
- JIT mode with proper content paths
- Consistent use of theme spacing scale
- Dark mode via class strategy (allows user preference)
- CSS output is small (8KB gzipped)
```
