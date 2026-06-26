# CDP Trace — Closed Shadow DOM Cascade Diagnosis

Extract the computed style + matched CSS rules of elements inside a closed shadow DOM directly via the Chrome DevTools Protocol (CDP). Identifies which stylesheet is the actual carrier and verifies cascade entry when `::part(...)` outer-scope selectors fail to apply.

## When to use

- Outer `::part(<name>) { ... }` rules visually have no effect
- You need the computed style of an element inside a closed shadow DOM
- You need to identify the carrier (outer document vs shadow-root inject)
- You need to verify the cascade for `[part="..."]` direct selectors on a web component

## Mechanism

`DOM.getDocument({ depth: -1, pierce: true })` of the Chrome DevTools Protocol (Playwright `newCDPSession`) returns the full DOM tree **including closed shadow roots**. For each `nodeId`, call `CSS.getComputedStyleForNode` + `CSS.getMatchedStylesForNode` to dump the applied rules and the rules that were ignored.

## Quick Reference

```bash
# 1. Install playwright into .tmp/ and pull headed chromium
cd <repo>/.tmp && npm init -y && npm install playwright@latest
npx playwright install chromium

# 2. Run cdp-trace.js (user-visible browser)
# --parts (canonical, plural) and --part (legacy singular) are both accepted;
# the script tolerates either form to match the historical Quick Reference example.
node scripts/cdp-trace.js --url http://<target>/<path> --parts "app-group,card-wrapper"
```

## Script pattern

```javascript
const { chromium } = require('playwright');

(async () => {
  // headless: false — user-visible (per web-ui-test rule)
  const browser = await chromium.launch({ headless: false, slowMo: 800 });
  const page = await browser.newContext({ ignoreHTTPSErrors: true, viewport: null }).then(c => c.newPage());

  await page.goto(URL, { waitUntil: 'domcontentloaded' });
  // (handle login / auth as needed)

  const cdp = await page.context().newCDPSession(page);
  await cdp.send('DOM.enable');
  await cdp.send('CSS.enable');

  // pierce:true — expose closed shadow roots as well
  const { root } = await cdp.send('DOM.getDocument', { depth: -1, pierce: true });

  // Recursive walk — collect every element carrying a part attribute
  function walk(node, found = []) {
    if (!node) return found;
    const attrs = node.attributes || [];
    const partIdx = attrs.findIndex((v, i) => i % 2 === 0 && v === 'part');
    if (partIdx >= 0) {
      found.push({ id: node.nodeId, name: node.nodeName, part: attrs[partIdx + 1] });
    }
    if (node.children) node.children.forEach(c => walk(c, found));
    if (node.shadowRoots) node.shadowRoots.forEach(s => walk(s, found));
    return found;
  }
  const parts = walk(root);

  for (const p of parts.filter(p => TARGET_PARTS.includes(p.part))) {
    const cs = await cdp.send('CSS.getComputedStyleForNode', { nodeId: p.id });
    const matched = await cdp.send('CSS.getMatchedStylesForNode', { nodeId: p.id });

    console.log(`[part="${p.part}"] (nodeId=${p.id}):`);
    // computed values
    for (const prop of ['width', 'grid-template-columns', '--app-card-min-width']) {
      const v = cs.computedStyle.find(c => c.name === prop);
      if (v) console.log(`  ${prop}: ${v.value}`);
    }
    // matched CSS rules (which sheet matched, which property won out)
    console.log(`  matched CSS rules:`);
    for (const r of matched.matchedCSSRules || []) {
      console.log(`    [${r.rule.origin}] ${r.rule.selectorList.text}`);
      for (const prop of r.rule.style.cssProperties) {
        if (prop.disabled) continue;
        console.log(`      ${prop.name}: ${prop.value}${prop.important ? ' !important' : ''}`);
      }
    }
  }

  // Let the user inspect the page and close it (X button) themselves
  await new Promise(() => {});
})();
```

## Interpreting the output

### Matched CSS rules include the outer brand sheet = cascade entry OK

```
[part="app-group"]:
  matched CSS rules:
    [regular] [part="app-group"] (sheet=style-sheet-20984-37)  ← brand!
      grid-template-columns: 1fr 1fr 1fr !important
```

→ The `[part="app-group"] { ... }` direct selector reaches the shadow-root cascade.

### Matched CSS rules show only inner shadow stylesheet = outer rule did not enter

```
[part="app-group"]:
  matched CSS rules:
    [regular] [part="app-group"] (sheet=style-sheet-20984-66)  ← inner only
      grid-template-columns: var(--app-group-template-columns, 1fr)
```

→ Zero matches for the external `ak-library::part(app-group) { ... }` rule. **Outer `::part` does not enter the cascade** (a Chrome closed-shadow limitation). Switch to a `[part="..."]` direct selector.

## Don't / Do

| # | Don't | Do |
|---|-------|-----|
| 1 | Run CDP trace with `headless: true` | `headless: false, slowMo: 800` — user-visibility rule (first section of web-ui-test/SKILL.md) |
| 2 | `::part(...)` doesn't work → only report "no visible effect" | Use CDP `getMatchedStylesForNode` to confirm whether the cascade is entered and identify the carrier |
| 3 | Retry the same selector form 5+ times | 0 matched CSS rules = evidence of spec/runtime divergence. Switch carrier immediately (`:host` / `[part="..."]` direct) |
| 4 | Leave `DOM.getDocument` with `pierce: false` (default) | Set `pierce: true` explicitly — exposes closed shadow roots too |
| 5 | Inspect only by `nodeId` + computed style | Also dump `matchedCSSRules` — check which sheet, which property, and `!important` |

## Self-check (every time before running a CDP trace)

1. Is the browser launched with `headless: false`? (user-visibility rule)
2. Did you pass `pierce: true` to `DOM.getDocument`?
3. Did you call `CSS.getMatchedStylesForNode` after identifying the target element's `nodeId`?
4. Does the output print every matched rule's sheet id + selector text + property + `!important` flag?

## Exceptions

- The user says "I just want a quick visual check" → skip CDP, screenshot only
- Inspecting a non-closed-shadow element → CDP is overkill; `getComputedStyle` is enough

## Case study (2026-05-28)

Card layout work on an IdP `ak-library` page. The attempt `ak-library::part(app-group) { grid-template-columns: ... !important }` produced zero visual effect. A CDP trace confirmed zero matched rules → outer `::part` could not enter the cascade → switched to `[part="app-group"] { ... }` direct selector → applied immediately. After 5 verification rounds the right carrier was found; this topic was added so future investigations cost fewer rounds.

## References

- [Chrome DevTools Protocol — DOM domain](https://chromedevtools.github.io/devtools-protocol/tot/DOM/)
- [CDP — CSS.getMatchedStylesForNode](https://chromedevtools.github.io/devtools-protocol/tot/CSS/#method-getMatchedStylesForNode)
- [Playwright — context.newCDPSession()](https://playwright.dev/docs/api/class-browsercontext#browser-context-new-cdp-session)
- `~/.agents/rules/authentik-customization.md` — IdP brand CSS carrier selection (one application domain for this topic)
