# Dark Mode

Three strategies, and the choice is made once. `dark_mode_strategy` records it; the wrong one produces a `dark:` prefix that never fires.

## Pick The Strategy

| Strategy | Behavior | Use when |
|---|---|---|
| `media` (default) | Follows `prefers-color-scheme`, no JS, no flash | The product has no theme switcher |
| `class` | `dark:` fires when `.dark` is on an ancestor | A manual toggle exists |
| `data-attribute` | Fires on `[data-theme="dark"]` | The same attribute already drives multi-brand theming |

```css
/* v4 — class strategy */
@custom-variant dark (&:where(.dark, .dark *));

/* v4 — data attribute */
@custom-variant dark (&:where([data-theme=dark], [data-theme=dark] *));
```

```js
// v3
darkMode: 'class'                          // or
darkMode: ['selector', '[data-theme="dark"]']
```

The `:where()` wrapper keeps the variant at zero added specificity, so `dark:bg-gray-900` still loses to a later utility instead of winning by accident.

## The Toggle, Complete

Three parts. Missing any one produces a bug that only appears on reload.

```html
<!-- 1. In <head>, BEFORE any stylesheet or app script -->
<script>
  (() => {
    const stored = localStorage.theme;                       // 'light' | 'dark' | undefined
    const dark = stored === 'dark' ||
      (!stored && matchMedia('(prefers-color-scheme: dark)').matches);
    document.documentElement.classList.toggle('dark', dark);
    document.documentElement.style.colorScheme = dark ? 'dark' : 'light';
  })();
</script>
```

```js
// 2. The toggle writes the class AND the stored preference
function setTheme(next) {                                     // 'light' | 'dark' | 'system'
  if (next === 'system') delete localStorage.theme; else localStorage.theme = next;
  const dark = next === 'dark' ||
    (next === 'system' && matchMedia('(prefers-color-scheme: dark)').matches);
  document.documentElement.classList.toggle('dark', dark);
  document.documentElement.style.colorScheme = dark ? 'dark' : 'light';
}

// 3. Follow the OS while the user is on 'system'
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
  if (!localStorage.theme) document.documentElement.classList.toggle('dark', e.matches);
});
```

- The script must be **blocking and inline** in `<head>`. A deferred script, a bundled module, or a React effect all run after first paint — that gap is the white flash.
- `color-scheme` is not decoration: it themes scrollbars, form controls, and the canvas background. Without it a dark page shows white scrollbars and a white flash between navigations.
- Store three states, not two. A boolean cannot express "follow the system", so users who never touched the toggle get frozen into whatever the OS was on their first visit.

## Server Rendering

- Nothing on the server knows the user's theme; any theme-dependent markup rendered server-side will mismatch on hydration.
- Render theme-neutral markup and let CSS decide. Where a component genuinely must differ (an icon swap), render both and hide one with `dark:hidden` / `hidden dark:block` — zero JS, zero mismatch.
- Reading `localStorage` during render is the standard hydration-error source in Next.js and SvelteKit. The inline head script is the supported pattern precisely because it runs outside the framework's lifecycle.
- A theme cookie plus a server-rendered class on `<html>` also works and avoids the inline script — at the cost of a cookie on every request and no "system" tracking without JS.

## Writing Dark Variants Well

- **Pair foreground and background, always.** `dark:bg-gray-900` without `dark:text-gray-100` produces black-on-black in exactly the mode you don't develop in.
- Dark mode is not an inversion. Reduce saturation and avoid pure black: `bg-gray-900` reads as a surface, `bg-black` reads as a hole and makes shadows invisible.
- Shadows barely exist on dark surfaces — replace elevation with a lighter surface step (`dark:bg-gray-800` on a `dark:bg-gray-900` page) or a subtle ring.
- Borders need to go lighter, not darker: `border-gray-200 dark:border-gray-700`.
- Images and logos: `dark:invert` for monochrome marks; a second asset for anything with brand color. `dark:brightness-90` takes the glare off photos.
- Semantic tokens beat per-element variants at scale. Define `--color-surface` / `--color-ink` and swap the values under `.dark`; markup drops the `dark:` prefix entirely and one file owns the palette.

## Checks Before Shipping

- Toggle, reload, toggle, reload — the flash only shows on reload.
- Reload with the OS in the *other* mode from the stored preference.
- Both modes against the contrast floor: 4.5:1 body text, 3:1 UI and focus rings (WCAG 2.2 AA, 1.4.3 / 1.4.11).
- Focus rings visible in both — `ring-offset` uses the page background, so a fixed offset color goes invisible in one mode (`ring-offset-white dark:ring-offset-gray-900`).
- Print: dark backgrounds do not print. `print:bg-white print:text-black` on the page root.
- Forms, scrollbars, and native pickers respect `color-scheme` — check a `<select>` and a date input, not just your own components.

