# Content Scaffolding — Slide Structure Templates

Standard page structures for common presentation scenarios.
Agent picks the matching template in Step 0, then fills content per page.

---

## Template: `pitch-deck`

**Target:** Investor / VC meetings  
**Slide count:** 10–12  
**Tone:** Confident, data-driven, concise

| # | Page Title | Required Content |
|---|-----------|-----------------|
| 1 | Cover | Company name, tagline, logo, presenter name |
| 2 | Problem | Pain point — 1 headline stat + 2–3 bullets |
| 3 | Solution | Product/offer in one sentence, visual if possible |
| 4 | Market Size | TAM / SAM / SOM with source |
| 5 | Product | Key features — 3 cards max |
| 6 | Traction | GMV / users / growth chart — real numbers |
| 7 | Business Model | How money is made — simple diagram |
| 8 | Competitive Landscape | 2×2 matrix or feature comparison |
| 9 | Team | Photos + name + 1-line credential each |
| 10 | Roadmap | 3–4 milestones on a timeline |
| 11 | Financials | Burn, runway, key projections |
| 12 | Ask | Round size, use of funds, CTA |

---

## Template: `conference-keynote`

**Target:** Public talk, conference stage, summit  
**Slide count:** 8–15  
**Tone:** Engaging, narrative, punchy

| # | Page Title | Required Content |
|---|-----------|-----------------|
| 1 | Cover | Talk title, speaker name + title, event name |
| 2 | Hook / Opening | Bold statement or question to grab attention |
| 3 | Context | Why this topic matters now — 1 key stat |
| 4–N | Main Points | 3–5 key ideas, each on 1–2 slides |
| N+1 | Case Study / Demo | Real example with outcome |
| N+2 | Takeaways | 3 actionable bullets |
| Last | Thank You / CTA | Next step, QR code, contact info |

**Rule:** Each slide body ≤ 3 bullets, each bullet ≤ 12 words.

---

## Template: `product-launch`

**Target:** Press, launch event, social media-ready  
**Slide count:** 8–10  
**Tone:** Exciting, visual-first, benefit-led

| # | Page Title | Required Content |
|---|-----------|-----------------|
| 1 | Cover | Product name, hero visual, launch date |
| 2 | The Problem | What was broken before |
| 3 | Introducing [Product] | Hero feature / one big visual |
| 4–6 | Key Features | One feature per slide, icon + headline + 1 line |
| 7 | Comparison | Before vs After, or vs competitors |
| 8 | Social Proof | Quotes, beta users, partner logos |
| 9 | Pricing / Access | Tiers or access URL |
| 10 | CTA | Sign up / try free / join waitlist |

---

## Template: `research-report`

**Target:** Internal team, policy makers, analysts  
**Slide count:** 12–20  
**Tone:** Authoritative, data-heavy, neutral

| # | Page Title | Required Content |
|---|-----------|-----------------|
| 1 | Cover | Report title, org/author, date |
| 2 | Executive Summary | 3–5 key findings in bullets |
| 3 | Methodology | Data sources, timeframe, scope |
| 4–N | Findings | One finding per slide — chart + insight sentence |
| N+1 | Implications | What this means — 3 bullets |
| N+2 | Recommendations | Actionable next steps |
| Last | Appendix / Source | Citations, data tables |

**Rule:** Every data point must have a source label (bottom of slide, small text).

---

## Bilingual Layout Guide

Use when audience is bilingual (HK, Singapore, TW, global Chinese events) or user mentions two languages.

### Heading structure
```html
<h1 class="slide-title">Main Title in English</h1>
<p class="slide-subtitle">Chinese subtitle or explanation</p>
```

### Body bullets
- Primary language: Chinese (larger, --text-primary)
- Secondary: English in parentheses or smaller line below (--text-muted, 0.85em)

### CSS for bilingual
```css
.slide-subtitle {
  font-size: 18px;
  color: var(--text-muted);
  margin-top: 4px;
  font-weight: 400;
}
.bullet-en {
  font-size: 14px;
  color: var(--text-muted);
  margin-top: 2px;
}
```

### When to use each mode

| Signal from user | Layout |
|-----------------|--------|
| "Chinese + English" / "bilingual" / "dual-language" | Full bilingual |
| Audience is HK / SG / TW / Chinese-speaking diaspora | Default bilingual unless told otherwise |
| "English only" / explicitly request English only | English only |
| Audience is pure Mainland CN | Chinese only |
| International / Western audience | English only |
