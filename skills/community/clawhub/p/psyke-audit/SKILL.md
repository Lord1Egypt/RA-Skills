---
name: psyke-audit
description: |
  Produce a branded Psyke SEO & GEO audit deck for any website. Use when asked to
  run an SEO audit, GEO audit, site audit, or website health check for a Psyke client.
  Also use when someone mentions "psyke audit", "run an audit", "audit this site",
  "SEO score", "GEO readiness", or "AI visibility audit". Outputs a single index.html
  slide deck with dual scoring (SEO Health /100 + GEO Readiness /100), competitor
  benchmarking, AI citation analysis, and Psyke-branded dark-mode theme.
---

# Psyke SEO & GEO Audit

Branded audit product for Psyke (psyke.co). Produces a scored, dark-mode slide deck covering technical SEO, GEO readiness, competitor benchmarking, and actionable recommendations.

## Output

A single `index.html` file deployed to Vercel containing:
- SEO Health score (out of 100)
- GEO Readiness score (out of 100)
- Scored breakdown by category
- Issue slides with evidence and fixes
- Competitor benchmark (when Ahrefs data available)
- AI visibility test results
- Prioritised action plan
- Psyke CTA slide

## References

Read these before building an audit:
- `references/scoring.md` — scoring methodology (SEO + GEO rubrics)
- `references/psyke-theme.css` — complete CSS theme (paste into `<style>`)
- `references/slide-structure.md` — fixed slide order and design rules
- `references/geo-framework.md` — GEO assessment process

## Process

### Phase 1: Data Collection

**1. Technical Crawl (always)**
```
- Fetch homepage, robots.txt, sitemap.xml
- Fetch 4-6 key inner pages (services, about, contact, sector pages)
- Use browser to evaluate each page for: title, meta description, canonical, H1s, H2s, H3s, schemas, OG tags, image alt text, viewport meta
- Check for soft 404s on common URL patterns
- Note the CMS/platform if identifiable
```

**2. Ahrefs Data (when MCP connected)**
```
Pull via Ahrefs MCP or have Psyke provide:
- Domain Rating
- Organic keyword count + top keywords
- Monthly organic traffic
- Referring domains count
- Google AI Overview citation count
- ChatGPT citation count
- Branded vs non-branded split (estimate)
- Same metrics for 2-3 competitors
```

**3. AI Visibility Testing (always)**
```
Run 5-8 queries through ChatGPT and/or Perplexity:
- "[client industry] + Australia" query
- "best [service/product]" query
- "how does [client service] work" query
- "[client] vs [competitor]" query
- Location-specific query
Record: was client mentioned? which competitors? what was cited?
```

### Phase 2: Scoring

Apply the rubrics from `references/scoring.md`:
1. Score each SEO category, noting specific evidence for each deduction
2. Score each GEO category, noting specific evidence
3. Calculate totals — do not round

### Phase 3: Build the Deck

**Setup:**
```bash
cd ~/Developer
mkdir [client]-seo-audit
cd [client]-seo-audit
git init
echo "# [Client] SEO & GEO Audit" > README.md
```

**Build `index.html`:**
1. Start with the viewport-base styles from the frontend-slides skill
2. Paste the full Psyke theme CSS from `references/psyke-theme.css`
3. Follow the slide structure from `references/slide-structure.md` exactly
4. Include the SlidePresentation JavaScript class (keyboard nav, touch, progress bar, nav dots, intersection observer)

**Font include:**
```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Key HTML patterns:**

Title slide:
```html
<section class="slide slide-title">
    <div class="glow-orb glow-purple" style="top: -10%; right: -5%;"></div>
    <div class="glow-orb glow-lime" style="bottom: 10%; left: -3%;"></div>
    <div class="content-wrap">
        <p class="psyke-logo reveal">PSYKE</p>
        <h1 class="reveal reveal-delay-1"><span class="accent">[Client Name]</span></h1>
        <p class="subtitle reveal reveal-delay-2">SEO & GEO Audit — [Month Year]</p>
        <p class="label-muted reveal reveal-delay-3">[client-url.com.au]</p>
    </div>
</section>
```

Dual score slide:
```html
<section class="slide">
    <div class="slide-split">
        <div class="split-left">
            <div class="dual-score reveal">
                <div class="score-block">
                    <div class="score-ring" style="--score-pct: 0.XX;">
                        <svg viewBox="0 0 100 100">
                            <circle class="ring-bg" cx="50" cy="50" r="45"/>
                            <circle class="ring-fill" cx="50" cy="50" r="45"/>
                        </svg>
                        <div class="score-number">XX</div>
                    </div>
                    <p class="score-label-big" style="color: var(--psyke-purple);">SEO Health</p>
                </div>
                <div class="score-block">
                    <div class="score-ring" style="--score-pct: 0.XX;">
                        <svg viewBox="0 0 100 100">
                            <circle class="ring-bg" cx="50" cy="50" r="45"/>
                            <circle class="ring-fill ring-fill-lime" cx="50" cy="50" r="45"/>
                        </svg>
                        <div class="score-number">XX</div>
                    </div>
                    <p class="score-label-big" style="color: var(--psyke-lime);">GEO Ready</p>
                </div>
            </div>
        </div>
        <div class="split-right">
            <!-- Breakdown grid -->
        </div>
    </div>
</section>
```

Competitor benchmark:
```html
<div class="competitor-grid">
    <div class="competitor-row header">
        <div class="competitor-cell"></div>
        <div class="competitor-cell">DR</div>
        <div class="competitor-cell">Keywords</div>
        <div class="competitor-cell">Traffic</div>
        <div class="competitor-cell">AI Citations</div>
    </div>
    <div class="competitor-row client">
        <div class="competitor-cell">[Client]</div>
        <div class="competitor-cell">XX</div>
        <!-- etc -->
    </div>
    <!-- competitor rows -->
</div>
```

### Phase 4: Deploy

```bash
git add -A
git commit -m "[Client] SEO & GEO Audit - SEO: XX/100, GEO: XX/100"
gh repo create beebeebot/[client]-seo-audit --public --source=. --push
npx vercel --yes --prod
```

### Phase 5: Deliver

Send the Vercel URL to the requester with:
- Both scores and breakdown summary
- The presentation link
- 2-3 sentence summary of key findings

## Writing Style

- Direct and specific. No filler.
- Evidence before opinion. Show the data, then make the observation.
- One sharp insight per issue, not three paragraphs restating the same point.
- Recommendations must be specific: "Add FAQ schema to /services/ page" not "consider adding structured data".

### AI Writing Patterns to Avoid (mandatory)

These are the most common tells. Fix every instance before deploying:

- **Em dashes (—)**: Replace with periods, commas, or restructure. Use sparingly if at all.
- **AI vocabulary**: Don't use "crucial", "landscape", "delve", "enhance", "foster", "showcase", "underscore", "pivotal", "vibrant", "testament", "garner", "interplay", "tapestry". Use plain words.
- **Rule of three**: Don't force ideas into groups of three. "Buying guides, how-tos, and comparison content" → "buying guides and comparisons".
- **Negative parallelisms**: Don't write "It's not just X, it's Y". Just say what it is.
- **Promotional language**: No "breathtaking", "groundbreaking", "stunning", "nestled", "in the heart of".
- **-ing superficial analysis**: Don't tack on "ensuring...", "highlighting...", "showcasing..." to add fake depth.
- **Vague attributions**: No "experts believe", "industry reports suggest". Cite specifics or don't claim it.
- **Filler phrases**: No "it's important to note that", "in order to", "at the end of the day".
- **Sycophantic tone**: No "Great question!", "Excellent point!", "That's a really good observation".
- **Generic positive conclusions**: No "the future looks bright" or "exciting times ahead".

## What NOT to Do

- Don't improvise the slide order — follow the structure
- Don't use light-mode slides — everything is dark Psyke theme
- Don't skip the GEO assessment, even without Ahrefs — the AI query testing and citability audit always apply
- Don't round scores for optics — 43 is 43
- Don't write generic recommendations — every fix should reference a specific URL or element
- Don't include the Psyke logo on every slide — title and closing only
