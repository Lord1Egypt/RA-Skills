# Telegram widget rules (condensed)

Adapted from Telegram's own guide for models, "Writing widgets with an LLM", in
<https://core.telegram.org/bots/widgets.md> (Bot API 10.4, November 2026), plus the
stricter rules this skill's checker enforces. When in doubt, the official page wins.

## What a widget is

- One HTML document or fragment with inline `<style>` and `<script>`. The bot sends it in a
  message and every Telegram app (iOS, Android, desktop, web) draws it inside the chat bubble.
- The JavaScript runs in QuickJS, not a browser. The app checks every DOM change against the
  "widget profile" and silently drops what is not in it. A dropped feature is a bug you will
  not see, so stay inside the lists below.
- **No network, ever.** No fetch, no external scripts, fonts, styles or images. All data
  arrives as state that the bot writes.
- **The HTML can never be changed after sending.** Only the state (`chat_data`,
  `public_data`) and the caption can change. So write the HTML as a template that draws
  everything from `chat_data`, and put the numbers into the state.
- In production, widgets work **only in the private chat with the bot** and cannot be
  forwarded. Groups, inline mode and forwards are test-server only.

## Size

- At most 32768 bytes of HTML, and at most 4096 bytes after zlib level 9. The checker counts
  exactly like the server. Typical cards are 1-2 KB compressed.
- No comments, no dead code. Repeated CSS compresses well; `data:` images and long unique
  text do not. Keep long text and numbers in `chat_data`, not in the HTML.

## The bubble

- Width 200-600 px, usually 320-430 on phones: design for 320. Height follows the content,
  50-600 px; the rest is clipped and **nothing scrolls**. Aim for under 560 px.
- Lay out with `%`, flex, grid, `vw`. Never `vh` or other height units.
- `html` has no background, so the bubble's color shows through. `body` gets the app's text
  padding as its margin (about `8px 12px`); `body{margin:0}` goes edge to edge.
- Without CSS you already get the app's text style, list/table/heading margins, and native
  `<button>`s. Any CSS of yours wins over those defaults.
- Colors: use the theme variables so light and dark both work:
  `--tg-theme-bg-color`, `--tg-theme-text-color`, `--tg-theme-hint-color`,
  `--tg-theme-link-color`, `--tg-theme-button-color`, `--tg-theme-button-text-color`,
  `--tg-theme-secondary-bg-color`, `--tg-theme-accent-text-color`,
  `--tg-theme-subtitle-text-color`, `--tg-theme-destructive-text-color`,
  `--tg-theme-section-separator-color` (also `--tg-color-scheme`). `prefers-color-scheme`
  and `light-dark()` follow the chat theme.
- Fonts: only `system-ui`, `sans-serif`, `serif`, `monospace`, `ui-sans-serif`, `ui-serif`,
  `ui-monospace`, `ui-rounded`. Named fonts and `@font-face` are dropped.
- Without a caption below the widget, the app draws the message time over the bottom
  corner: keep `env(safe-area-inset-bottom)` clear, e.g.
  `body{margin:0;padding:12px 14px max(10px,env(safe-area-inset-bottom))}`.
- Mute with color (`--tg-theme-hint-color`, `rgba()`, SVG `fill-opacity`), not `opacity`:
  at most 16 elements may have `opacity<1`, a `filter`, a `backdrop-filter` or a blurred
  `box-shadow`.

## What works

- HTML: `div span p br hr h1-h6 header footer main nav section article aside pre blockquote
  figure figcaption`, inline text tags (`b i u s em strong small mark code kbd sub sup abbr
  time`...), lists, tables, `details`/`summary`, `img` with a `data:` PNG/JPEG/GIF/WebP,
  `canvas`, `button`, inline `svg`.
- SVG: shapes, `path`, `g`, `defs`, `symbol`, `use href="#id"`, `text`/`tspan`, linear and
  radial gradients, CSS on SVG.
- CSS: flex, grid, `position: relative/absolute/fixed` (fixed = the bubble), borders,
  radius, `box-shadow`, gradients, 2D transforms, transitions, `@keyframes`, custom
  properties, `calc/min/max/clamp`, hex/`rgb()`/`hsl()`/`light-dark()`, `::before/::after`,
  `:active`, `:not/:is/:where`, structural pseudo-classes, `:disabled` on buttons,
  `@media` on width/aspect-ratio/orientation/`prefers-color-scheme`/`prefers-reduced-motion`,
  `@supports`, one-line `text-overflow: ellipsis`, `touch-action`, `pointer-events`,
  `filter`/`backdrop-filter` with `blur()`, `brightness()`, `drop-shadow()` only.
- JS: ES2023, Promises, async/await, timers, `requestAnimationFrame`, the DOM
  (`createElement`, `createElementNS`, `querySelector`, `textContent`, `classList`, `style`,
  `dataset`, `addEventListener`, `replaceChildren`), `MutationObserver`, `ResizeObserver`,
  layout reads (cache them), canvas 2D, `Intl` in `navigator.language`, `localStorage` (4 KB
  per message, wrap in try/catch), `crypto.getRandomValues`, `TextEncoder`, `URL`.
- Element ids are **not** global variables: use `document.getElementById('x')`.

## What Telegram removes (do not use)

- HTML: `input select option textarea fieldset legend datalist output` (no form controls),
  `progress meter dialog audio video iframe object embed link meta base template math ruby
  center font big tt strike`, `<img>` from anything but a `data:` URL, `data:image/svg+xml`
  images, presentational attributes (`align bgcolor border color face`...),
  `contenteditable tabindex autofocus accesskey draggable popover`.
- SVG: `clipPath mask pattern marker` filters, SMIL (`animate`...), `foreignObject`, `<image>`.
- CSS: `vh`/`dvh`/`svh`, `overflow: auto/scroll`, `position: sticky`,
  `display: contents/flow-root/list-item`, logical properties (`margin-inline`...),
  multi-column, `oklch() lab() lch() color() color-mix()`, `background-clip: text`,
  `text-shadow`, `-webkit-line-clamp`, `writing-mode`, 3D transforms, other filter functions,
  `clip-path`, masks, blend modes, `url()` other than `data:` images and `#fragments`,
  `@font-face @import @container @layer @property`, nesting, `:has() :focus* :checked
  :target ::marker ::first-letter`, `@media (hover|pointer|print|resolution)`.
- JS: every network API (`fetch XMLHttpRequest WebSocket EventSource`...), `location`,
  `history`, `alert confirm prompt print`, `navigator.clipboard share vibrate geolocation`,
  shadow DOM, custom elements, `Blob FileReader createObjectURL`, fullscreen, canvas pixel
  read-back (`getImageData putImageData toDataURL`), canvas shadows/patterns/compositing,
  WebGL, `OffscreenCanvas`, CDN libraries (Chart.js, D3: nothing loads).
- Input: no touch events (use pointer events), no keyboard, no focus, no wheel or scroll.
  Vertical drags always scroll the chat.

## TelegramWidget essentials

`window.TelegramWidget` exists inside Telegram and is `undefined` in a browser, so guard it:
`const TW = window.TelegramWidget;` then `if (TW) ...`.

- `TW.chatData` / `TW.publicData`: strings of up to 1024 bytes or `null`. `JSON.parse` them
  in try/catch and draw from them. Redraw on `TW.onEvent('chatDataChanged', draw)` /
  `'publicDataChanged'`. Nothing restarts when the state changes.
- `TW.colorScheme`, `TW.themeParams`, events `themeChanged`, `activated`, `deactivated`.
- `TW.copyText(text)`: copies 1-256 characters on a tap and shows a toast.
- `TW.openLink(url)` / `TW.openTelegramLink(url)`: on a tap only, `https:` only, at most 256
  characters. See the link rules below.
- `TW.HapticFeedback.impactOccurred('light')` etc.: only around a tap.
- `TW.setResizeAnchor?.('bottom')` for content that grows at the bottom.
- `TW.request(data)`: asks the bot (1-64 bytes). **Do not use it with this skill yet**: the
  agent frameworks do not deliver the `widget_query` update to the skill, so every request
  would time out. Draw from `chat_data` and let the agent update it with `edit`.

## This skill's stricter rules (the checker refuses the widget otherwise)

- **Links**: only with one literal URL, in one of these forms, and only to hosts on the
  operator's allowlist (`TG_WIDGETS_ALLOWED_LINKS`; empty by default = no links at all):
  `TW.openLink('https://host/path')`, `TW.openTelegramLink('https://t.me/name')`,
  `window.open('https://...')`, `<a href="https://...">`. Never build a URL in code, never
  take one from state, never copy a link from a web page, a tweet or a user message into a
  widget. Never change the allowlist yourself.
- **No HTML from strings**: no `innerHTML`, `outerHTML`, `insertAdjacentHTML`,
  `document.write`, `DOMParser`. Build the DOM with `createElement` + `textContent`.
- **No code from strings**: no `eval`, `Function`, `.constructor`, `atob`, `fromCharCode`,
  `import`, string arguments to `setTimeout`, unicode escapes in names, `'a' + 'b'` literal
  splicing, computed access with string keys (`obj['x']`) or on
  `window`/`document`/`TelegramWidget`.
- Do not set `href`, `src` (except a literal `data:` image), `srcset` or `on*` attributes from
  code; use `TW` only as `TW.member`.
- No URLs anywhere in text, attributes, strings, state or the caption unless allowlisted.

## A skeleton that follows every rule

```html
<style>
body{margin:0;padding:12px 14px max(10px,env(safe-area-inset-bottom))}
h3{margin:0 0 6px;font-size:1.05em}
.v{font-size:1.8em;font-weight:700;font-variant-numeric:tabular-nums}
.meta{color:var(--tg-theme-hint-color);font-size:.85em}
</style>
<h3 id="title">Loading</h3>
<div class="v" id="value"></div>
<div class="meta" id="meta"></div>
<script>
const TW = window.TelegramWidget;
const $ = (id) => document.getElementById(id);
function draw() {
  let s = null;
  try { s = JSON.parse(TW && TW.chatData); } catch (e) {}
  if (!s) return;
  $('title').textContent = s.t;
  $('value').textContent = new Intl.NumberFormat(navigator.language).format(s.v);
  $('meta').textContent = s.m || '';
}
if (TW) TW.onEvent('chatDataChanged', draw);
draw();
</script>
```

Sent with `--chat-data '{"t":"Active users","v":15234,"m":"as of 14:05"}'`. To update it
later: `edit --chat-data '{"t":"Active users","v":15901,"m":"as of 15:05"}'`.

Formatting money with `Intl.NumberFormat`: add `currencyDisplay: 'narrowSymbol'`, otherwise
some locales show `US$` instead of `$`.

## Limits (past them the widget stops on its last frame)

2000 DOM nodes · 8 MB memory · 400 CSS rules · 32 `@keyframes` · 8 K characters per attribute
(this includes `data:` image URLs) · 48 K characters of text · 64 live timers · 300 ms of
JavaScript per second, 500 ms in one task · 128 layout reads per task · 16 "heavy" elements
(filter, backdrop-filter, opacity<1, blurred shadow), at most 2 with backdrop-filter ·
`data:` images up to 1024×1024 px · 4000 canvas commands per canvas per task.
