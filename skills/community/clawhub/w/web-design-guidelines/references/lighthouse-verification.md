# Lighthouse Verification — Runtime Validation

Adapted from [`aliborhothamud/lighthouse-95-skill`](https://github.com/aliborhothamud/lighthouse-95-skill/blob/main/SKILL.md). In this skill the loop is **measure → diagnose → report** — fixes do not happen inline; each identified cause becomes a pendency and enters the SPEC pipeline. The fix playbook below is used to write correct fix directions into SPECs.

## Iron Rules

1. **Measure the URL users actually hit.** Any host with preview/prod aliases (Vercel, Netlify, Cloudflare Pages, Azure Static Web Apps): a plain deploy creates a *preview* — the public alias may still serve the OLD production. Measuring the stale deploy wastes a round and produces false "no change" evidence. Confirm the URL with the user when in doubt.
2. **No verdict before identifying the cause.** Extract the LCP element and its phase breakdown from the JSON before writing a finding — "LCP is slow" is not a finding; "LCP is the H1 waiting on a 129KB web font" is.
3. **Verdict = 3 consecutive runs.** Throttled runs vary ±0.5s / ±4 points. One run proves nothing — report runs individually, never a single-run pass/fail claim.

## Mobile AND Desktop

Lighthouse defaults to **mobile emulation** (mid-tier phone, slow 4G, 4× CPU throttle) — the hard mode, and what Google uses for Core Web Vitals. Desktop scores run 10–20 points higher. Measure **both**, report against the mobile run, and never compare runs across presets.

## Measure & Diagnose

```bash
# Mobile (default emulation)
npx lighthouse https://SITE --output=json --output-path=./lh-mobile.json --quiet \
  --chrome-flags="--headless=new" \
  --only-categories=performance,accessibility,best-practices,seo

# Desktop (confirm after mobile passes)
npx lighthouse https://SITE --preset=desktop --output=json --output-path=./lh-desktop.json --quiet \
  --chrome-flags="--headless=new" \
  --only-categories=performance,accessibility,best-practices,seo
```

Then interrogate the JSON — never just read the scores:

```bash
node -e "
const r = require('./lh-mobile.json');
for (const [k,v] of Object.entries(r.categories)) console.log(k, Math.round(v.score*100));
// LCP element + phases (audit id varies by LH version):
const lcp = r.audits['lcp-breakdown-insight'] || r.audits['largest-contentful-paint-element'];
console.log(JSON.stringify(lcp?.details?.items, null, 1));
// TBT culprits:
r.audits['bootup-time']?.details?.items?.slice(0,5)
  .forEach(i => console.log('JS:', i.url.split('/').pop(), Math.round(i.total)+'ms'));
// a11y failures with exact selectors:
Object.values(r.audits).filter(a => a.score !== null && a.score < 1 &&
  r.categories.accessibility.auditRefs.some(x => x.id === a.id))
  .forEach(a => console.log('A11Y:', a.id, a.details?.items?.[0]?.node?.selector || ''));
"
```

If `npx lighthouse` is unavailable and cannot be installed in the environment, say so in the report — do not substitute guesses or unmeasured claims. Playwright-based checks are a complementary signal, not a Lighthouse replacement.

## Fix Playbook (by identified cause)

Use this to write the "fix direction" field in the report and SPECs:

| Cause (from JSON) | Fix |
| --- | --- |
| LCP is TEXT with high `elementRenderDelay` | Waiting for a web font swap. Self-host, then instance + subset the font (below). |
| LCP is IMAGE | `<link rel="preload" as="image" fetchpriority="high">` + explicit `width`/`height` + compress (sharp/mozjpeg, resize to display size) |
| High TBT from a JS lib (bootup-time) | Load it after `window` `load` via injected script tags. Animation libs: invert visibility — CSS never hides content; JS hides only below-fold elements right before animating them |
| FCP high, same-origin small page | Inline critical CSS into `<head>` (kills stylesheet round-trip). Trim preloads competing with the LCP resource |
| Fonts from Google/CDN | Self-host woff2 (latin subset), `font-display: swap`, preload only slim critical files. Zero external origins is the end state |
| a11y `color-contrast` | Check CSS specificity bugs, not just palette: a `.nav a { color }` rule can override button classes and paint low-contrast text nobody intended |
| a11y `landmark-one-main` | Wrap page content in `<main>` |
| SEO/BP stragglers | Canonical link, meta description, `theme-color`, explicit image dimensions, HTTPS |
| Blazor WASM slow start | Publish AOT/trimmed build, `BlazorWebAssemblyLazyLoad` for non-essential assemblies, Brotli precompressed assets, avoid large singletons in DI |

## Font Instancing + Subsetting (the usual killer move)

```python
# pip install fonttools brotli
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.subset import Subsetter, Options

f = TTFont("font-variable.woff2")
if "fvar" in f:  # pin variable axes to the ONE weight you actually use
    instantiateVariableFont(f, {"wght": 600, "opsz": 48}, inplace=True)
opt = Options(); opt.flavor = "woff2"; opt.layout_features = ["*"]
s = Subsetter(opt)
s.populate(unicodes=range(0x20, 0x17F))  # latin + latin-ext; add smart quotes U+2013-2026
s.subset(f); f.flavor = "woff2"; f.save("font-600.woff2")
```

Update `@font-face` to `font-weight: 600` and fix any usage relying on other weights. For Blazor WASM: place in `wwwroot/fonts/`, preload in `index.html`/`App.razor` head outlet.

## Traps (each cost a real round)

| Trap | Reality |
| --- | --- |
| "Scores didn't move — my fix failed" | Check you measured the NEW deploy (preview vs production alias) |
| "Preloads are good, add them all" | A 129KB font preload starves the LCP image on 4G. Preload only what LCP needs; slim files first |
| "Optimize images first, it's always images" | The LCP was an H1 waiting on a font. Identify the element first |
| "One run at 95 = done" | Variance. Three consecutive runs ≥95, all categories, or keep going |
| "Hide content in CSS, reveal with JS animations" | JS loads late/never → invisible page, failed LCP. Content visible by default; JS only hides what it will animate |

## When NOT to Use

- **Field data (CrUX / real-user metrics)** — Lighthouse is a lab tool. If the complaint is "Search Console says CWV failing", real-user conditions differ; lab 95+ does not guarantee a field pass.
- **localhost / dev mode** — dev bundles are unminified and unoptimized; scores are meaningless. Only measure deployed, production-built URLs.
- **SPAs measured only on the shell route** — measure the routes users actually land on (landing page, login, main dashboard). List routes measured in the report.

## Verification Gate (for the fixing SPECs, not this audit)

The audit reports evidence; the SPECs it spawns carry the gate. Each performance/a11y SPEC inherits this done-criteria: **3 consecutive runs ≥95 in all four categories on mobile, plus one desktop run ≥95, on the production URL** — with before/after metric tables (FCP/LCP/TBT/CLS), not just scores.
