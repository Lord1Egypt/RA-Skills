# Templates

File and header templates for site launches. Apply per the matrices in `decisions.md`.

## robots.txt

### Template: doc site for OSS lib (allow AI scrapers)

```
User-agent: *
Allow: /

Sitemap: https://EXAMPLE.com/sitemap.xml

# AI scrapers (per decisions.md: doc-site policy)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: CCBot
Allow: /

User-agent: Applebot-Extended
Allow: /

# Blocked low-value scrapers
User-agent: Bytespider
Disallow: /

User-agent: Amazonbot
Disallow: /
```

### Template: marketing / lead-gen (block all AI scrapers)

```
User-agent: *
Allow: /

Sitemap: https://EXAMPLE.com/sitemap.xml

# Block all AI scrapers (per decisions.md: marketing policy)
User-agent: GPTBot
Disallow: /

User-agent: ChatGPT-User
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: anthropic-ai
Disallow: /

User-agent: PerplexityBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Applebot-Extended
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: Amazonbot
Disallow: /
```

Note: regular search engine crawlers (Googlebot, Bingbot) are not in the AI bot list and remain governed by the `User-agent: *` rule.

---

## llms.txt

Per llmstxt.org spec. Place at root.

```
# Project Name

> One-line description of the project, written for an LLM consumer.

Markdown paragraph giving more context on what the project does, who it's for, and why it exists.

## Docs

- [Getting started](https://example.com/docs/getting-started): how to install and run the first example
- [API reference](https://example.com/docs/api): full API documentation
- [Examples](https://example.com/docs/examples): working code samples

## Optional

- [Changelog](https://example.com/changelog): version history
- [Contributing](https://github.com/owner/repo/blob/main/CONTRIBUTING.md): how to contribute
```

For richer LLM consumption, also publish `llms-full.txt` with the full content of all documentation pages concatenated.

---

## manifest.json

Minimum modern PWA manifest. Place at root or `/manifest.json`.

```json
{
  "name": "Site Full Name",
  "short_name": "Site",
  "description": "One-line description matching meta description.",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#000000",
  "icons": [
    {
      "src": "/web-app-manifest-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/web-app-manifest-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "maskable"
    },
    {
      "src": "/web-app-manifest-192x192.png",
      "sizes": "192x192",
      "type": "image/png",
      "purpose": "any"
    },
    {
      "src": "/web-app-manifest-512x512.png",
      "sizes": "512x512",
      "type": "image/png",
      "purpose": "any"
    }
  ]
}
```

HTML `<head>` references:

```html
<link rel="icon" href="/favicon.ico" sizes="any" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="apple-touch-icon" href="/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#000000" />
```

---

## CSP templates

Three tightness levels. Pick per the matrix in `decisions.md`.

### `strict-default-src-none`

For doc sites, personal portfolio, SaaS apps with bundled assets only.

```
default-src 'none';
script-src 'self' 'nonce-{NONCE}' https://hogpost.samber.dev;
style-src 'self' 'unsafe-inline';
img-src 'self' data: https:;
font-src 'self' data:;
connect-src 'self' https://hogpost.samber.dev https://eu.i.posthog.com;
manifest-src 'self';
base-uri 'self';
form-action 'self';
frame-ancestors 'none';
object-src 'none';
upgrade-insecure-requests;
```

Notes:

- `style-src 'unsafe-inline'` is unfortunately required by most modern frameworks (Tailwind in dev, styled-components, etc.). Tighten with hashes if feasible.
- Replace `{NONCE}` with a per-request random value generated server-side (Next.js middleware can do this).
- `connect-src` includes `eu.i.posthog.com` as a fallback if `hogpost.samber.dev` proxy is unavailable.

### `balanced-allow-self`

For marketing pages with embeds.

```
default-src 'self';
script-src 'self' 'nonce-{NONCE}' https://hogpost.samber.dev https://www.youtube.com https://assets.calendly.com;
style-src 'self' 'unsafe-inline' https://assets.calendly.com;
img-src 'self' data: https:;
font-src 'self' data:;
connect-src 'self' https://hogpost.samber.dev https://*.calendly.com;
frame-src 'self' https://www.youtube.com https://calendly.com;
frame-ancestors 'none';
object-src 'none';
upgrade-insecure-requests;
```

Adjust embed origins as needed.

### `permissive-for-marketing`

Legacy fallback. Add a TODO comment in the codebase to tighten in the next iteration.

```
default-src 'self' https:;
script-src 'self' 'unsafe-inline' 'unsafe-eval' https:;
style-src 'self' 'unsafe-inline' https:;
img-src 'self' data: https:;
font-src 'self' data: https:;
connect-src 'self' https:;
frame-ancestors 'none';
upgrade-insecure-requests;
```

---

## Full security headers reference

Apply all of these in addition to CSP. Add to Vercel's `vercel.json` or Next.js `next.config.js` `headers()`.

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "Strict-Transport-Security",
          "value": "max-age=31536000; includeSubDomains; preload"
        },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        {
          "key": "Referrer-Policy",
          "value": "strict-origin-when-cross-origin"
        },
        {
          "key": "Permissions-Policy",
          "value": "camera=(), microphone=(), geolocation=(), payment=(), usb=(), magnetometer=(), gyroscope=()"
        },
        { "key": "Cross-Origin-Opener-Policy", "value": "same-origin" },
        { "key": "Cross-Origin-Embedder-Policy", "value": "credentialless" },
        { "key": "Cross-Origin-Resource-Policy", "value": "same-origin" }
      ]
    }
  ]
}
```

Notes:

- `Cross-Origin-Embedder-Policy: credentialless` is safer than `require-corp` for sites with third-party embeds.
- `Permissions-Policy` should enumerate every feature you want to deny, not rely on defaults.

Verify with:

```bash
curl -sI https://example.com | grep -iE 'strict-transport|x-content-type|x-frame|referrer-policy|permissions-policy|cross-origin'
```

---

## Sitemap.xml structure

For multilingual sites, use a sitemap index referencing per-locale sitemaps.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap><loc>https://example.com/sitemap-en.xml</loc></sitemap>
  <sitemap><loc>https://example.com/sitemap-fr.xml</loc></sitemap>
</sitemapindex>
```

Each per-locale sitemap declares `xhtml:link` alternates with `hreflang`:

```xml
<url>
  <loc>https://example.com/en/page</loc>
  <xhtml:link rel="alternate" hreflang="en" href="https://example.com/en/page"/>
  <xhtml:link rel="alternate" hreflang="fr" href="https://example.com/fr/page"/>
  <xhtml:link rel="alternate" hreflang="x-default" href="https://example.com/en/page"/>
</url>
```

---

## TONE.md template

Place at `.agents/TONE.md` or repo root. Fill in based on the user's writing samples and preferences.

```markdown
# Tone of voice: [Site name]

## Audience

- Primary: [e.g., senior Go developers shipping production systems]
- Secondary: [e.g., engineering managers evaluating libraries]
- Reading level: [e.g., technical, no hand-holding]
- Language: [e.g., English, with some French for FR-specific pages]

## Voice

- Direct, dense, no filler.
- Contrarian when warranted.
- Data-grounded: claims need numbers or links.
- Concrete over abstract: prefer "200ms p95" to "fast".
- Assume reader has context, skip primers.

## Forbidden words and patterns

- AI-sounding openers: "In today's fast-paced world", "Let's dive into", "It's worth noting that".
- Vague adjectives: "crucial", "essential", "powerful", "robust", "comprehensive", "seamless", "innovative".
- Empty verbs: "delve into", "leverage", "utilize", "facilitate".
- Hedging: "might potentially", "may possibly", "kind of", "sort of".
- Em dash character ("—") forbidden. Use commas, parentheses, or two sentences.
- Marketing fluff: "game-changing", "revolutionary", "next-generation", "world-class".

## Required patterns

- One concrete example per claim.
- Numbers when possible. Prefer "20% faster" over "much faster".
- Code samples for technical content. Short, runnable, idiomatic.

## Sentence and paragraph rules

- Average sentence length: 12-18 words.
- Max paragraph length: 4 sentences.
- One idea per paragraph.
- Section headers are statements, not questions.

## Good examples (from existing content)

- "Product XYZ hit $1m ARR without paying for ads. The community wants feature-ABC done right."
- "Tool XYZ gives 50× benchmark speedups and 5% production gains. Both numbers are true. Only one matters."

## Bad examples (to avoid)

- "Product XYZ is a powerful, comprehensive productivity tool that leverages documentation to seamlessly empower designers."
- "In today's fast-paced development landscape, choosing the right productivity tool is crucial."

## Address form (FR only)

- `tu` vs `vous` must be chosen deliberately and applied consistently site-wide. Mixed forms on the same site are a copywriting error.
- Default by site type:
  - `doc-site` (OSS lib, developer tools): **tu** — developer community is informal; "vous" feels corporate and creates distance.
  - `SaaS-app` (B2B, enterprise): **vous** — default to formal unless the product targets solo developers or the brand is explicitly casual.
  - `marketing/lead-gen` (consumer-facing): **tu** if the audience is young or tech-savvy; **vous** if the audience is professional or older.
  - `training/paid-course`: **tu** — learning context is personal; "vous" creates unnecessary formality.
  - `personal-portfolio`: **vous** — professional register by default.
- Ask the user explicitly if the default does not fit: "Which address form?" (`tu` | `vous` | `already-specified-in-TONE.md`)
- Record the chosen form in TONE.md under `Address form: tu | vous` and enforce it in every copy review and humanizer pass.

## Localization notes

- FR content: use guillemets « » not quotes, use non-breaking spaces before `: ; ? !`, avoid anglicisms ("faire du sens", "adresser un problème").
- EN content: US spelling.
```

The skill should read TONE.md at the start of any copywriting task and pass its constraints to any delegated copywriting skill. After drafting, run the humanizer in the matching language.
