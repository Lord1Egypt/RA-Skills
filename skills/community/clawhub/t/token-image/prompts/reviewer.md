You are reviewing a React component for a social/marketing image.

**Before you begin, read these files:**
- `.token-image/src/token.active.json` — design tokens
- `.token-image/src/viewport.tsx` — shared Viewport
- `.token-image/src/styles.css` — set stylesheet
- `.token-image/src/<format>-<index>.tsx` — the component to review
- `.token-image/src/<format>-<index>.png` — rendered image (VISUAL REVIEW REQUIRED — already rendered by orchestrator)

CONTENT BRIEF:
{content_brief}

## STEP 1: REVIEW

The PNG has already been rendered by the orchestrator. Read the file at `.token-image/src/<format>-<index>.png` to visually inspect it. You need both the source code AND the rendered image to complete this review.

CHECK FOR:

**Content compliance:**
- Content strings must match the brief exactly — no reworded titles, no added content, no omitted content
- If the brief includes a title, the component must render it
- If the brief says no body text, the component must not have body text

**Token compliance:**
- Hardcoded colors → must use `tokens.*` or CSS classes from styles.css
- Hardcoded font sizes/weights/families → must use CSS classes or `tokens.*`
- Hardcoded spacing → must use `tokens.spacing.*`
- Hardcoded border radius → must use `tokens.radius.*`
- Hardcoded opacity → must use `tokens.opacity.*`
- Import of token files → must use tokens prop
- ACCEPTABLE hardcoding: SVG path data, calculated values, transform strings, root container width/height

**Viewport compliance:**
- All content wrapped in `<Viewport tokens={tokens} variant="...">`
- Use variant="hero" for hero-style layouts (large display text, minimal body)
- Use variant="standard" for all other layouts
- No single wrapper div as the only child of Viewport — pass multiple direct children (heading, layout block, metadata) so the viewport's gap works. If a single wrapper is truly needed, it must replicate the viewport inner wrapper's flex behavior (`flex`, `flexDirection`, `justifyContent`, `alignItems` and etc)

**Visual review (examine the rendered PNG):**
Look at the rendered image and flag any aesthetic issues:
- Text clipping, overflow, or truncation
- Content touching edges or viewport padding being ignored
- Unintended overlapping elements
- Unbalanced composition (e.g. content crammed to one side with dead space)
- Inconsistent visual weight between elements
- Text too small or too large relative to the canvas
- Colors that clash or have insufficient contrast against the background
- Elements that look visually broken, misaligned, or floating without purpose
- Standalone decorative elements (dots, shapes, circles) that don't serve the brief — background patterns are fine
- Grid not filling full width when the layout description implies full-width grid content
- Title spacing inconsistent — headings have `margin: 0` and spacing is handled by flex/grid `gap`

**Layout description compliance:**
- Component layout must match the layout description from the brief
- Use CSS classes from styles.css where appropriate for layout (e.g., `.grid-2`, `.grid-3`, `.card`, `.stack`)
- Layout mixing is allowed — a component may combine grid and split, cards and free text, etc.
- No rigid grid count rules — follow the brief's layout description instead

**Density compliance:**
- Density should match what the brief describes — hero-style layouts should be light, card grids should fill naturally
- No cramming

OUTPUT FORMAT:
If compliant: respond with exactly: PASS

If not compliant: respond with a JSON array of issues:
[
  { "line": "<code snippet>", "issue": "<what's wrong>", "fix": "<suggested fix>" }
]
