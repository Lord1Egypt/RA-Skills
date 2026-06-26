---
name: sai-frontend-builder
description: "SAI — frontend builder untuk pipeline intel OJS/PKP. Render candidate yang sudah PASS dari SENKU menjadi tiga deliverable. Pertama, halaman artikel HTML semantic, responsive, SEO-ready dengan meta tags, OG tags, dan JSON-LD schema.org Article. Kedua, carousel 7-slide struktur fix (hook, konteks, tiga key points, implikasi praktis, CTA) dalam dua dimensi 1080x1080 untuk Instagram dan 1200x675 untuk LinkedIn dan X. Ketiga, caption sosial opsional untuk LinkedIn, X, Instagram. Wajib dipicu saat user minta render artikel jurnal, generate carousel berita OJS, buat halaman publikasi, slide IG atau LinkedIn untuk pengelola jurnal, atau saat menerima brief PASS dari SENKU. Stack HTML5 plus Tailwind CDN atau plain CSS, no heavy framework, budget di bawah 100KB inline CSS, lazy-load images, WCAG AA wajib, alt text wajib, kontras minimum 4.5 banding 1. Output handoff JSON ke SENKU dengan article_id, html_artifact_url, carousel_artifact_url, cta_url. CTA selalu ke openjournaltheme.com dengan rotasi varian copy."
metadata:
  clawdbot:
    emoji: "🎨"
    fork_of: "skill-creator@0.1.0"
    sibling_of:
      - "conan-ojs-scout@0.2.0"
      - "senku-qa-validator@0.1.0"
    role: "frontend-builder"
---

# SAI — Frontend Builder

Render candidate intel OJS/PKP yang sudah lolos QA SENKU menjadi tiga artefak siap publish: halaman artikel HTML, carousel 7-slide, caption sosial opsional. Tidak menulis konten dari nol — hanya transform brief tervalidasi menjadi output visual + markup yang konsisten dengan standar editorial.

## Input Contract

SAI menerima `brief_for_next` dari SENKU (saat verdict PASS dari CONAN). Format:

```
TITLE: <title>
AUDIENCE: <editor|reviewer|author|publisher|developer|admin, joined>
TAGS: <relevance_tags joined>
KEY_POINTS:
  - <point 1>
  - <point 2>
  - <point 3..7>
PRIMARY_SOURCE: <url>
SECONDARY_SOURCES:
  - <url>
TONE_CONSTRAINT: factual, no promotional adjectives, ≤15-word quotes max 1 per source
LENGTH_TARGET: 400-700 kata
```

Plus `candidate_json` lengkap (untuk traceability + halusinasi guard di SENKU re-validation).

Jika brief tidak lengkap atau tidak ada `candidate_json` referensi → STOP, kembalikan ke SENKU dengan flag `brief_incomplete`. Jangan tulis konten yang tidak ada di brief.

## Workflow Decision Tree

```
brief_for_next received
        │
        ▼
1. Parse brief + candidate_json
        │
        ▼
2. Generate artikel HTML (assets/article-template.html → render)
        │
        ▼
3. Generate carousel 1080x1080 (assets/carousel-1080.svg.tpl)
        │
        ▼
4. Generate carousel 1200x675 (assets/carousel-1200x675.svg.tpl)
        │
        ▼
5. (Optional) Generate captions (assets/caption-templates.json)
        │
        ▼
6. Validate output (scripts/validate_output.py)
        │  ├─ HTML <100KB inline CSS
        │  ├─ Alt text ada di semua <img>
        │  ├─ Kontras WCAG AA ≥4.5:1
        │  ├─ schema.org/Article valid
        │  └─ CTA URL = https://openjournaltheme.com/
        ▼
7. Emit handoff JSON ke SENKU
```

## Deliverable 1: Artikel HTML

Template: `assets/article-template.html`. Detail lengkap struktur, meta tags wajib, schema.org/Article shape: `references/article-template-spec.md`.

Wajib ada di output:
- `<meta charset>`, `<meta name="viewport">`, `<meta name="description">`
- Open Graph tags: `og:title`, `og:description`, `og:type=article`, `og:image`, `og:url`
- Twitter Card: `twitter:card=summary_large_image`
- JSON-LD `schema.org/Article` dengan `headline`, `datePublished`, `author`, `publisher`, `mainEntityOfPage`
- `<article>` semantic dengan `<header>`, `<section>`, `<footer>`
- Source attribution block: `<aside class="sources">` dengan link `PRIMARY_SOURCE` + `SECONDARY_SOURCES`
- Lazy-load: `<img loading="lazy" decoding="async">`

Tone: factual. Hapus adjektif promosi. Verbatim quotes <15 kata, max 1 per sumber, dalam `<blockquote cite="...">`.

## Deliverable 2: Carousel 7-Slide

Struktur **fix** (tidak boleh diubah):

| Slide | Konten | Sumber data |
|-------|--------|-------------|
| 1 | Hook headline + visual anchor | `TITLE` + visual abstract |
| 2 | Konteks: apa & kapan | `published_at` + 1-2 kalimat ringkas |
| 3 | Key point #1 | `KEY_POINTS[0]` |
| 4 | Key point #2 | `KEY_POINTS[1]` |
| 5 | Key point #3 | `KEY_POINTS[2]` |
| 6 | Implikasi praktis untuk pengelola jurnal | Disimpulkan dari `audience_fit` + `actionable` framing |
| 7 | CTA ke `https://openjournaltheme.com/` | Varian copy dari `references/cta-variants.md` |

Dimensi:
- **1080×1080** (Instagram, Facebook square) → `assets/carousel-1080.svg.tpl`
- **1200×675** (LinkedIn, X/Twitter) → `assets/carousel-1200x675.svg.tpl`

Render via `scripts/render_carousel.py <brief.json> <dimension> <output.svg>`.

Detail tipografi, palette, hierarchy: `references/carousel-spec.md`.

## Deliverable 3: Caption Sosial (opsional)

Template: `assets/caption-templates.json`. Tiga varian: LinkedIn (formal, 1300-1700 char), X/Twitter (≤280 char dengan thread split), Instagram (engaging, 125-2200 char dengan line breaks + hashtag block di akhir).

Generate hanya jika user/SENKU explicit request dengan flag `include_captions: true`.

## Standar Teknis (NON-NEGOTIABLE)

| Aspek | Konstrain |
|-------|-----------|
| Stack | HTML5 + Tailwind CDN **atau** plain CSS. Tidak ada React, Vue, Svelte, jQuery. |
| Inline CSS budget | <100KB total |
| Images | `loading="lazy" decoding="async"`, format WebP/AVIF preferred |
| A11y | WCAG AA: kontras ≥4.5:1 (text), ≥3:1 (UI components), focus ring visible |
| Alt text | Wajib di semua `<img>`, deskriptif (bukan "image" / "photo") |
| Carousel | HTML/SVG only, no Canvas API runtime, no JS animation library |
| Font | System font stack atau Google Fonts via `<link rel="preconnect">` |
| Color tokens | Lihat `references/carousel-spec.md` palette |

## Submission ke SENKU

Setelah validate pass, emit handoff JSON:

```json
{
  "article_id": "uuid candidate dari brief",
  "html_artifact_url": "path atau URL artefak HTML",
  "carousel_artifact_url": {
    "1080x1080": "path/url SVG square",
    "1200x675":  "path/url SVG landscape"
  },
  "captions": {
    "linkedin": "string|null",
    "x":        "string|null",
    "instagram": "string|null"
  },
  "cta_position": "slide-7",
  "cta_url": "https://openjournaltheme.com/",
  "cta_variant_used": "string (label dari cta-variants.md)",
  "validation_report": {
    "html_size_bytes": 0,
    "alt_text_coverage": 1.0,
    "contrast_min_ratio": 4.5,
    "schema_org_valid": true
  },
  "rendered_at": "ISO-8601 UTC"
}
```

SENKU akan re-validate untuk halusinasi (entitas/angka di output harus match `candidate_json`). Iterasi maks 3 sebelum auto-REJECT.

## CTA Rotation

Slide 7 selalu point ke `https://openjournaltheme.com/`. Copy varian dirotasi dari `references/cta-variants.md`. Jangan pakai varian yang sama dalam 5 artikel berturut-turut (track via `cta_variant_used` di handoff log).

## Forbidden Patterns

Auto-fail validation jika output mengandung:

1. Adjektif promosi: "revolutionary", "groundbreaking", "must-have", "ultimate", "best-ever", "wajib", "luar biasa" (di body artikel — boleh di carousel hook hanya jika ada di brief).
2. Klaim/angka/entitas yang tidak ada di `candidate_json` (halusinasi).
3. CTA selain `https://openjournaltheme.com/`.
4. Verbatim quote ≥15 kata atau >1 kutipan per sumber.
5. `<img>` tanpa alt text.
6. Inline `<script>` yang melakukan analytics/tracking pihak ketiga.
7. External CDN selain: `cdn.tailwindcss.com`, `fonts.googleapis.com`, `fonts.gstatic.com`.

## Resources

- `references/article-template-spec.md` — Spec lengkap meta tags, OG, schema.org/Article, semantic HTML structure.
- `references/carousel-spec.md` — Palette, tipografi, hierarchy, A11y carousel.
- `references/cta-variants.md` — Daftar varian copy CTA slide 7.
- `assets/article-template.html` — Boilerplate HTML5 siap-render.
- `assets/carousel-1080.svg.tpl` — Template SVG 1080×1080 (placeholder `{{TITLE}}`, `{{KEY_POINT_N}}`, dll.).
- `assets/carousel-1200x675.svg.tpl` — Template SVG 1200×675.
- `assets/caption-templates.json` — Skeleton caption per platform.
- `scripts/render_carousel.py` — Render template SVG dari brief JSON.
- `scripts/validate_output.py` — Cek size, alt text, kontras, CTA, halusinasi.
- `scripts/package_skill.py` — Inherited dari skill-creator untuk repackaging.
- `scripts/quick_validate.py` — Inherited dari skill-creator untuk validasi struktur skill.

## Best Practices

1. **Tidak menambah konten.** Jika brief kurang detail untuk slide 6 (implikasi), kembalikan ke SENKU dengan REVISE request — jangan improvisasi.
2. **Validate sebelum submit.** Selalu jalankan `scripts/validate_output.py` sebelum emit handoff.
3. **CTA rotation log.** Catat `cta_variant_used` agar SENKU bisa enforce no-repeat-in-5.
4. **Schema.org wajib valid.** Test dengan https://validator.schema.org/ jika ragu.
5. **Carousel adalah SVG, bukan PNG.** Resolution-independent, kecil, accessible (text in `<text>` tetap selectable).
6. **Source attribution di artikel HTML.** `<aside>` dengan link ke PRIMARY_SOURCE + SECONDARY_SOURCES — bukan footnote, bukan tersembunyi.
7. **Tidak ada inline analytics.** Tracking dilakukan di luar artefak (di host page).
