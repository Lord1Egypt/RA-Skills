# Interface Guidelines — Static Review Rules

Vendored from [`vercel-labs/web-interface-guidelines`](https://github.com/vercel-labs/web-interface-guidelines/blob/main/command.md) and adapted for this catalog's stacks (React/Next.js, Angular, Blazor/.NET, plain HTML). Apply every rule whose file type and context can trigger it; record categories skipped as not-applicable in the report's coverage section.

## Framework Mapping

Rules were written with JSX examples; map them before judging a file:

| Concept | React/Next.js | Angular | Blazor / Razor |
| --- | --- | --- | --- |
| Click handler | `onClick` | `(click)` | `@onclick` |
| Keyboard handler | `onKeyDown`/`onKeyUp` | `(keydown)`/`(keyup)` | `@onkeydown`/`@onkeyup` |
| Label binding | `htmlFor` | `for` | `for` on `<label>` / `Label` param on components |
| Image component | `next/image` `priority` | `NgOptimizedImage` `priority` | `fetchpriority="high"` on `<img>` |
| Link component | `<Link>` | `routerLink` | `<NavLink>` / anchor + `@ref` nav |
| Client state | `useState`/`useEffect` | signals/`NgZone` | component fields/`[Parameter]` |
| URL-synced state | `nuqs`, `useSearchParams` | `ActivatedRoute.queryParams` | `[SupplyParameterFromQuery]` |
| Layout reads | `getBoundingClientRect` in render | same, inside `ngAfterViewInit` | `IJSRuntime` layout reads during `OnParametersSet` |
| Controlled input | `value` + `onChange` | `ngModel` | `@bind-Value` |
| Virtualization | `virtua`/`react-window` | CDK `virtual-scroll` | `<Virtualize>` |
| Toast/live region | `aria-live` wrappers | `LiveAnnouncer` (CDK a11y) | `aria-live` region component |
| Font preload | `next/font` | `<link rel="preload">` in `index.html` | `<link rel="preload">` in `App.razor`/`_Host`/`index.html` |

Plain HTML/CSS files get the same rules minus the framework syntax.

## Rules

### Accessibility

- Icon-only buttons need `aria-label`
- Form controls need `<label>` or `aria-label`
- Interactive elements need keyboard handlers (`onkeydown`/`onkeyup` or framework equivalent)
- `<button>` for actions, `<a>`/link component for navigation (not `<div @onclick>`)
- Images need `alt` (or `alt=""` if decorative)
- Decorative icons need `aria-hidden="true"`
- Async updates (toasts, validation) need `aria-live="polite"`
- Use semantic HTML (`<button>`, `<a>`, `<label>`, `<table>`) before ARIA
- Headings hierarchical `<h1>`–`<h6>`; include skip link for main content
- `scroll-margin-top` on heading anchors
- Meaningful media needs captions, transcripts, or descriptions as applicable
- Media controls need keyboard support; decorative media needs assistive-tech hiding

### Focus States

- Interactive elements need visible focus: `focus-visible` ring or equivalent
- Never `outline-none` / `outline: none` without focus replacement
- Use `:focus-visible` over `:focus` (avoid focus ring on click)
- Group focus with `:focus-within` for compound controls
- Sticky headers/footers/overlays must not cover the focused element

### Forms

- Inputs need `autocomplete` and meaningful `name`
- Use correct `type` (`email`, `tel`, `url`, `number`) and `inputmode`
- Never block paste (`onpaste` + `preventDefault`)
- Labels clickable (`for`/`htmlFor` or wrapping control)
- Disable spellcheck on emails, codes, usernames (`spellcheck="false"`)
- Checkboxes/radios: label + control share single hit target (no dead zones)
- Submit button stays enabled until request starts; spinner during request
- Errors inline next to fields; focus first error on submit
- Placeholders end with `…` and show example pattern
- `autocomplete="off"` on non-auth fields to avoid password manager triggers
- Warn before navigation with unsaved changes (`beforeunload` or router guard — Blazor: `NavigationLock`)

### Animation

- Honor `prefers-reduced-motion` (provide reduced variant or disable)
- Animate `transform`/`opacity` only (compositor-friendly)
- Never `transition: all` — list properties explicitly
- Set correct `transform-origin`
- SVG: transforms on `<g>` wrapper with `transform-box: fill-box; transform-origin: center`
- Animations interruptible — respond to user input mid-animation
- Autoplay motion >5 seconds alongside other content needs pause, stop, or hide controls
- Muted decorative loops must stop under `prefers-reduced-motion`

### Typography

- `…` not `...`
- Curly quotes `"` `"` not straight `"`
- Non-breaking spaces: `10&nbsp;MB`, `⌘&nbsp;K`, brand names
- Loading states end with `…`: `"Loading…"`, `"Saving…"`
- `font-variant-numeric: tabular-nums` for number columns/comparisons
- Use `text-wrap: balance` or `text-pretty` on headings (prevents widows)

### Content Handling

- Text containers handle long content: `truncate`, `line-clamp-*`, or `break-words`
- Flex children need `min-w-0` to allow text truncation
- Handle empty states — don't render broken UI for empty strings/arrays
- User-generated content: anticipate short, average, and very long inputs

### Images

- `<img>` needs explicit `width` and `height` (prevents CLS)
- Below-fold images: `loading="lazy"`
- Above-fold critical images: `priority` or `fetchpriority="high"`

### Performance

- Large lists (>50 items): virtualize (`<Virtualize>`, CDK `virtual-scroll`, `virtua`, or `content-visibility: auto`)
- No layout reads in render (`getBoundingClientRect`, `offsetHeight`, `offsetWidth`, `scrollTop` — including JS interop during Blazor parameter setters)
- Batch DOM reads/writes; avoid interleaving
- Prefer uncontrolled inputs; controlled inputs must be cheap per keystroke
- Add `<link rel="preconnect">` for CDN/asset domains
- Critical fonts: `<link rel="preload" as="font">` with `font-display: swap`
- Prefer `<video autoplay muted loop playsinline>` over animated GIF; provide a still alternative
- Short non-essential loops: Safari H.264 MP4 `<picture>` source, `prefers-reduced-motion` media condition, and still fallback
- Blazor Server: avoid re-render storms — `ShouldRender`, `@key` on lists, no `.StateHasChanged()` in timers without batching

### Navigation & State

- URL reflects state — filters, tabs, pagination, expanded panels in query params
- Links use real `<a>`/link components (Cmd/Ctrl+click, middle-click support)
- Deep-link all stateful UI (if it holds component state, consider URL sync)
- Destructive actions need confirmation modal or undo window — never immediate

### Touch & Interaction

- `touch-action: manipulation` (prevents double-tap zoom delay)
- `-webkit-tap-highlight-color` set intentionally
- `overscroll-behavior: contain` in modals/drawers/sheets
- During drag: disable text selection, `inert` on dragged elements
- Drag/swipe/pinch/path gestures need tap/click and keyboard alternatives unless essential
- `autofocus` sparingly — desktop only, single primary input; avoid on mobile

### Safe Areas & Layout

- Full-bleed layouts need `env(safe-area-inset-*)` for notches
- Avoid unwanted scrollbars: `overflow-x-hidden` on containers, fix content overflow
- Flex/grid over JS measurement for layout

### Dark Mode & Theming

- `color-scheme: dark` on `<html>` for dark themes (fixes scrollbar, inputs)
- `<meta name="theme-color">` matches page background
- Native `<select>`: explicit `background-color` and `color` (Windows dark mode)

### Locale & i18n

- Dates/times: use `Intl.DateTimeFormat` / `CultureInfo` formatting — not hardcoded formats
- Numbers/currency: use `Intl.NumberFormat` / `CultureInfo` — not hardcoded formats
- Detect language via `Accept-Language` / `navigator.languages`, not IP
- Brand names, code tokens, identifiers: wrap with `translate="no"` to prevent garbled auto-translation

### Hydration Safety

- Inputs with a bound value need a change handler (or uncontrolled/`defaultValue`)
- Date/time rendering: guard against server/client hydration mismatch
- `suppressHydrationWarning` / `@key` hydration hacks only where truly needed

### Hover & Interactive States

- Buttons/links need a `hover` state (visual feedback)
- Interactive states increase contrast: hover/active/focus more prominent than rest

### Content & Copy

- Active voice: "Install the CLI" not "The CLI will be installed"
- Title Case for headings/buttons (Chicago style)
- Numerals for counts: "8 deployments" not "eight"
- Specific button labels: "Save API Key" not "Continue"
- Error messages include fix/next step, not just problem
- Second person; avoid first person
- `&` over "and" where space-constrained

## Anti-patterns (always flag)

- `user-scalable=no` or `maximum-scale=1` disabling zoom
- `onpaste` with `preventDefault`
- `transition: all`
- `outline-none` without focus-visible replacement
- Inline click navigation without `<a>`
- `<div>` or `<span>` with click handlers (should be `<button>`)
- Images without dimensions
- Large arrays `.map()`/`@foreach` without virtualization
- Form inputs without labels
- Icon buttons without `aria-label`
- Hardcoded date/number formats (use `Intl.*`/`CultureInfo`)
- `autofocus` without clear justification
- Animated GIF when compressed video is suitable
- Gesture-only action without tap/click and keyboard alternative

## Output Format

Group by file. `file:line` (VS Code clickable). Terse — state issue + location, skip explanation unless fix is non-obvious. No preamble.

```text
## src/Button.razor

src/Button.razor:42 - icon button missing aria-label
src/Button.razor:18 - input lacks label
src/Button.razor:55 - animation missing prefers-reduced-motion
src/Button.razor:67 - transition: all → list properties

## src/Modal.razor

src/Modal.razor:12 - missing overscroll-behavior: contain
src/Modal.razor:34 - "..." → "…"

## src/Card.razor

✓ pass
```
