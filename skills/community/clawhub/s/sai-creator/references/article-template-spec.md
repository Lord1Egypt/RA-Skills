# Article Template Spec

Spesifikasi lengkap halaman artikel HTML SAI. Konsumsi referensi ini saat render artikel.

## File Skeleton

Lihat `assets/article-template.html`. Placeholder variables (mustache-style) yang harus di-substitute:

| Placeholder | Sumber dari brief / candidate_json |
|-------------|------------------------------------|
| `{{TITLE}}` | `title` |
| `{{DESCRIPTION}}` | `summary_raw` (trim ke 155 char untuk meta description) |
| `{{CANONICAL_URL}}` | URL host SAI (bukan `source_url`) |
| `{{SOURCE_URL}}` | `source_url` (untuk attribution block) |
| `{{PUBLISHED_AT}}` | `published_at` (ISO-8601) |
| `{{AUTHOR}}` | `author` atau "Redaksi" jika null |
| `{{ARTICLE_BODY}}` | Body artikel hasil expand `key_points` + `summary_raw` (400-700 kata) |
| `{{HERO_IMAGE_URL}}` | URL hero image (1200×630 untuk OG) |
| `{{HERO_IMAGE_ALT}}` | Deskripsi alt text — wajib non-kosong, deskriptif |
| `{{KEYWORDS}}` | `relevance_tags` joined dengan koma |
| `{{SECONDARY_SOURCES_HTML}}` | `<ul>` dari `secondary_sources[]` |

## Mandatory Meta Tags

```html
<!-- Charset & viewport -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<!-- SEO -->
<title>{{TITLE}}</title>
<meta name="description" content="{{DESCRIPTION}}">
<meta name="keywords" content="{{KEYWORDS}}">
<link rel="canonical" href="{{CANONICAL_URL}}">

<!-- Open Graph -->
<meta property="og:type" content="article">
<meta property="og:title" content="{{TITLE}}">
<meta property="og:description" content="{{DESCRIPTION}}">
<meta property="og:url" content="{{CANONICAL_URL}}">
<meta property="og:image" content="{{HERO_IMAGE_URL}}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="article:published_time" content="{{PUBLISHED_AT}}">
<meta property="article:author" content="{{AUTHOR}}">

<!-- Twitter Card -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{{TITLE}}">
<meta name="twitter:description" content="{{DESCRIPTION}}">
<meta name="twitter:image" content="{{HERO_IMAGE_URL}}">
```

## JSON-LD schema.org/Article

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{{TITLE}}",
  "description": "{{DESCRIPTION}}",
  "image": "{{HERO_IMAGE_URL}}",
  "datePublished": "{{PUBLISHED_AT}}",
  "dateModified": "{{PUBLISHED_AT}}",
  "author": {
    "@type": "Person",
    "name": "{{AUTHOR}}"
  },
  "publisher": {
    "@type": "Organization",
    "name": "OJS Intel",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "mainEntityOfPage": {
    "@type": "WebPage",
    "@id": "{{CANONICAL_URL}}"
  },
  "keywords": "{{KEYWORDS}}",
  "isBasedOn": "{{SOURCE_URL}}"
}
</script>
```

`isBasedOn` wajib menunjuk ke `source_url` dari candidate_json — ini transparency mark untuk pembaca + crawler bahwa artikel adalah derived work.

## Semantic HTML Body Structure

```html
<article itemscope itemtype="https://schema.org/Article">
  <header>
    <h1 itemprop="headline">{{TITLE}}</h1>
    <p class="meta">
      <time datetime="{{PUBLISHED_AT}}" itemprop="datePublished">{{PUBLISHED_AT_HUMAN}}</time>
      <span itemprop="author">{{AUTHOR}}</span>
    </p>
  </header>

  <figure>
    <img src="{{HERO_IMAGE_URL}}" alt="{{HERO_IMAGE_ALT}}" loading="lazy" decoding="async" width="1200" height="630">
    <figcaption>{{HERO_IMAGE_ALT}}</figcaption>
  </figure>

  <section itemprop="articleBody">
    {{ARTICLE_BODY}}
  </section>

  <aside class="sources" aria-label="Sumber">
    <h2>Sumber</h2>
    <p>Sumber utama: <a href="{{SOURCE_URL}}" rel="noopener external" target="_blank">{{SOURCE_URL}}</a></p>
    <h3>Sumber sekunder</h3>
    {{SECONDARY_SOURCES_HTML}}
  </aside>
</article>
```

## Body Generation Rules

Saat expand `key_points` + `summary_raw` menjadi `{{ARTICLE_BODY}}` 400-700 kata:

1. Paragraf pembuka: rephrase `summary_raw` (jangan copy verbatim) — 2-3 kalimat konteks.
2. Sub-section per `key_points[]` dengan `<h2>` heading. Tiap section 80-150 kata.
3. Verbatim quote (jika ada): `<blockquote cite="{{SOURCE_URL}}">"<text <15 kata>"</blockquote>` — max 1 per sumber.
4. Closing paragraph: implikasi praktis untuk `audience_fit` — 50-100 kata, factual, tanpa CTA.
5. **Tidak ada** kalimat yang menambah klaim/angka/entitas yang tidak ada di brief atau `candidate_json`.
6. **Tidak ada** adjektif promosi di body. Carousel hook boleh hyperbolic jika ada di brief.

## Accessibility Checklist

- [ ] `<html lang="id">` atau `lang="en"` sesuai `language_detected`
- [ ] Heading hierarchy: satu `<h1>`, lalu `<h2>` per section, tidak skip level
- [ ] `<img>` semua punya alt text non-kosong, deskriptif
- [ ] Link external punya `rel="noopener"` dan icon/text indicator
- [ ] Kontras text/background ≥4.5:1
- [ ] Focus ring visible pada semua interactive element
- [ ] `<time datetime="...">` machine-readable
- [ ] `lang` attribute switch jika ada paragraf bahasa lain (`<span lang="en">`)

## SEO Checklist

- [ ] Title ≤60 char (untuk SERP)
- [ ] Description 120-160 char
- [ ] Canonical URL set
- [ ] Hero image 1200×630 minimum (OG spec)
- [ ] JSON-LD valid (test: validator.schema.org)
- [ ] Internal anchor links di TOC jika artikel >700 kata
