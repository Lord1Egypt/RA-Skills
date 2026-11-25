# Color Contrast

WCAG AA contrast enforcement for Rails + Tailwind + oklch color systems.

## The Rules

| WCAG Level | Normal Text | Large Text (18px+ bold or 24px+) |
|---|---|---|
| AA | 4.5:1 | 3:1 |
| AAA | 7:1 | 4.5:1 |

Target **AA** as the minimum bar. AAA is aspirational.

## oklch Color System Gotchas

Tailwind v4+ uses oklch colors by default. The chroma value (`c` in `oklch(L C H)`) controls saturation — and it's the #1 source of contrast failures.

### The chroma threshold

```css
/* FAILS - chroma 0.05 is too saturated for dark text on light bg */
--color-text: oklch(0.55 0.05 250);

/* PASSES - chroma 0.02 is safe */
--color-text: oklch(0.55 0.02 250);
```

**Rule of thumb:** chroma ≤ 0.03 for text colors on light backgrounds. Above 0.04 almost certainly fails WCAG AA.

### A real CI failure

A navigation tier used `oklch(0.65 0.031 250)` - chroma 0.031, right at the
edge of the safe band. Axe-core flagged it in CI as insufficient contrast.
Fix: dropped chroma to 0.02.

This is the typical shape of the failure: the color looks correct on a
calibrated monitor, and the number is well inside the "normal" range. Only the
chroma is out of bounds, and only the automated check catches it.

### Quick audit script

```bash
# Scan Tailwind config for oklch colors with high chroma
grep -n 'oklch' app/assets/stylesheets/*.css | while read line; do
  chroma=$(echo "$line" | grep -oP 'oklch\([^,]+,\s*\K[0-9.]+')
  if [ -n "$chroma" ] && (( $(echo "$chroma > 0.03" | bc -l) )); then
    echo "⚠️  High chroma ($chroma): $line"
  fi
done
```

## Tailwind Color Utilities That Fail

Common Tailwind classes that can fail WCAG AA:

| Class | Issue | Fix |
|---|---|---|
| `text-gray-400` | 2.6:1 on white | Use `text-gray-500` or darker |
| `text-gray-300` | 1.9:1 on white | Never use for body text |
| `text-gray-500` | 4.38:1 on `bg-gray-100` / light tinted backgrounds (e.g., `#ebf6f7`) | Use `text-gray-600` or darker |
| `text-blue-400` | 3.1:1 on white | Use `text-blue-600` or darker |
| `text-red-400` | 3.2:1 on white | Use `text-red-600` or darker |

**Rule:** `-400` and lighter shades are decorative only. Never use them for body text, labels, or form fields. `text-gray-500` is also unsafe on anything darker than pure white; default to `text-gray-600` for hint/secondary text on light tinted backgrounds.

## CI Enforcement

### axe-core RSpec matcher (automatic)

The `expect_accessible` helper from `references/testing.md` catches contrast failures in system specs. This is the primary enforcement mechanism — axe-core runs in a real browser and catches contrast issues that static analysis misses.

If axe-core flags contrast, fix the color. Don't add a custom RSpec matcher to work around it — see the "Rules to skip" table in `references/testing.md` for per-test opt-outs (e.g., third-party map tiles).

## Focus Indicators

Don't remove focus outlines without replacing them:

```css
/* BAD — no focus indicator at all */
button:focus { outline: none; }

/* GOOD — custom focus ring */
button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.5);
}

/* BEST — Tailwind ring utilities */
<button class="focus:outline-none focus:ring-2 focus:ring-brand-light focus:ring-offset-2">
```

## Dark Mode

Dark mode needs its own contrast checks. Common failures:

- Light text on dark bg: `text-gray-400` on `bg-gray-900` = 5.2:1 (passes AA)
- But `text-gray-500` on `bg-gray-900` = 3.4:1 (fails AA)

Test both modes in system specs:

```ruby
it 'passes contrast checks in dark mode' do
  visit root_path
  page.execute_script("document.documentElement.classList.add('dark')")
  expect_accessible
end
```

## Related

`testing.md` is the home for axe-core setup and the per-rule `skip:` mechanism used when third-party content (map tiles, embeds) has contrast you don't control.
