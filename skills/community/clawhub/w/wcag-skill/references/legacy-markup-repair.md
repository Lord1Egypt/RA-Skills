# Legacy markup repair

Inventory content, navigation, fragment targets, forms, and interactive behavior
before changing markup. Preserve them in the repair, including meaningful text
from moving or blinking content. Check each route and relevant rendered state.

| Legacy | Modern approach |
|---|---|
| `font`, `basefont`, inline presentation attributes | Semantic text or `span` and CSS; preserve meaningful text and typography. Calculate actual foreground/background contrast in all relevant states. `<font>` itself is not automatically a WCAG failure. |
| `center` | CSS `text-align` where appropriate, not a substitute for landmarks. |
| `marquee`, `blink` | Keep the information as static content and remove motion by default. If automatically moving content lasts more than five seconds alongside other content, provide pause/stop/hide controls unless an exception applies (SC 2.2.2); `prefers-reduced-motion` is supplementary. Use live-region semantics only for genuinely dynamic updates. |
| Layout tables | Use grid/flex and logical source order. Keep data tables, with header cells and suitable `scope`. |
| Clusters of absolutely positioned divs | Assess reading order and purpose of each region; use document flow and appropriate landmarks. Positioning alone is not an accessibility failure, and not every `div` should become a landmark. |
| Unnamed image link | Give its image purpose-based `alt` text; if visible link text supplies the name, use `alt=""`. Use `aria-label` only when native naming is unsuitable (SC 2.4.4). |
| Search field without a label | Prefer an explicit visible `label` with matching `for` and `id`. Wrapping labels are also valid; group related controls with `fieldset` and `legend`. Never use placeholder text as a label. |

`<font>`, `<center>`, `<marquee>`, and related obsolete elements are
non-conforming HTML features, but their presence alone does not establish a
WCAG failure. Fix the actual presentation, semantics, and user impact as well
as replacing the obsolete syntax. Landmarks help identify meaningful page
regions; axe's `region` rule is best practice, not a WCAG success criterion.
Use landmarks only for meaningful regions, and remember that nested
`<header>`/`<footer>` elements do not always create banner/contentinfo landmarks.

## Example: synthetic local news page

Before:

```html
<center><font color="#ff0000" size="6">Fjordnytt</font></center>
<marquee>Ny bru åpner lørdag</marquee>
<table role="presentation"><tr><td>
  <a href="#nyheter"><img src="news.png"></a>
  <form role="search" action="/search">
    <input type="search" name="q">
    <button type="submit">Søk</button>
  </form>
</td><td><div style="position:absolute">
  <h2 id="nyheter">Nyheter</h2><font color="#ff0000">Brua er ferdig.</font>
</div></td></tr></table>
```

After (with the same message, destination and fragment target):

```html
<header>
  <h1>Fjordnytt</h1>
  <p>Ny bru åpner lørdag</p>
  <nav aria-label="Hovedmeny">
    <a href="#nyheter"><img src="news.png" alt="Nyheter"></a>
  </nav>
  <form role="search" action="/search">
    <label for="search">Søk</label>
    <input id="search" name="q" type="search">
    <button type="submit">Søk</button>
  </form>
</header>
<main>
  <h2 id="nyheter">Nyheter</h2>
  <p>Brua er ferdig.</p>
</main>
```

```css
body { color: #111; background: #fff; font-family: sans-serif; }
```

The example preserves its search action, query parameter, and button. In a real
repair, preserve the existing endpoint and behavior rather than adopting the
illustrative `/search` path. Recreate layout in CSS, keeping reading and
keyboard order logical.

## Verify

- Compare visible content, links, effective base URLs, existing fragment targets,
  form behavior, and states with the original. Test keyboard navigation and
  assistive technology; do not hide content to satisfy automated checks.
- Check rendered contrast: SC 1.4.3 AA requires 4.5:1 normal and 3:1 large
  text; SC 1.4.6 AAA requires 7:1 normal and 4.5:1 large text, subject to
  exceptions. Check non-text contrast separately.
- Run `python3 scripts/check-legacy-markup.py path/to/page.html` for a static
  obsolete-element inventory with file names and line numbers. Findings are
  warnings, not automatic WCAG failures; the checker does not inspect
  attributes, layout, names, script-generated markup, or visual contrast.
- Validate modern HTML; run axe-core and contrast checks; test keyboard
  operation, focus order, responsive layouts, and existing functionality.
  Review semantics, names, and reading order with a screen reader. Follow the
  [validator workflow](validator-workflow.md) and
  [manual test protocol](manual-test-protocol.md); no one automated result
  establishes conformance.
- For an explicit benchmark, use the
  [Gauntlet legacy-repair task](https://github.com/turbolego/AI-WCAG-Gauntlet/blob/main/BENCHMARK.md#legacy-repair-task)
  and its full checker; its 113-tag requirement is not a production requirement.
