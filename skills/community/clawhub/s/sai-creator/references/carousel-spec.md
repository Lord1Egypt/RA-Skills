# Carousel Spec

Spesifikasi tipografi, palette, dimensi, dan A11y untuk carousel 7-slide SAI.

## Dimensi (FIXED)

| Target | Width | Height | Aspect | File |
|--------|-------|--------|--------|------|
| Instagram, Facebook square | 1080 | 1080 | 1:1 | `assets/carousel-1080.svg.tpl` |
| LinkedIn, X/Twitter | 1200 | 675 | 16:9 | `assets/carousel-1200x675.svg.tpl` |

Format output: SVG. Bukan PNG. Bukan Canvas. SVG memberi: text selectable (a11y), resolution-independent, file kecil, mudah di-tweak.

## Palette (Color Tokens)

```
--bg-primary:    #0F172A   /* slate-900, latar slide 1, 7 */
--bg-secondary:  #FFFFFF   /* putih, latar slide 2-6 */
--accent:        #2563EB   /* blue-600, brand OJS Intel */
--accent-hover:  #1D4ED8   /* blue-700 */
--text-primary:  #0F172A   /* slate-900 di latar putih */
--text-on-dark:  #F8FAFC   /* slate-50 di latar gelap */
--text-muted:    #64748B   /* slate-500 untuk meta info */
--border:        #E2E8F0   /* slate-200 */
--cta-bg:        #F59E0B   /* amber-500, urgency CTA slide 7 */
--cta-text:      #0F172A   /* slate-900 */
```

Kontras yang sudah dihitung (semua memenuhi WCAG AA ≥4.5:1):

| Foreground | Background | Ratio | Pass? |
|------------|------------|-------|-------|
| #F8FAFC | #0F172A | 16.1:1 | AAA |
| #0F172A | #FFFFFF | 16.1:1 | AAA |
| #2563EB | #FFFFFF | 5.15:1 | AA |
| #0F172A | #F59E0B | 9.2:1 | AAA |
| #64748B | #FFFFFF | 4.6:1 | AA |

## Tipografi

Font stack (system-first, no external load):
```
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

Untuk impact lebih, optional Google Font: `Inter` 600/700/800 — jika dipakai, preload via `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>`.

### Type Scale (1080×1080)

| Element | Size (px) | Weight | Line-height |
|---------|-----------|--------|-------------|
| Slide 1 hook headline | 72 | 800 | 1.1 |
| Slide 2-6 heading | 56 | 700 | 1.15 |
| Slide 2-6 body | 36 | 400 | 1.4 |
| Slide 7 CTA headline | 64 | 800 | 1.1 |
| Slide 7 CTA URL/button | 32 | 600 | 1.2 |
| Footer/page indicator | 24 | 500 | 1.2 |

### Type Scale (1200×675)

Skala 0.75× dari 1080×1080:

| Element | Size (px) | Weight |
|---------|-----------|--------|
| Slide 1 hook | 54 | 800 |
| Heading | 42 | 700 |
| Body | 27 | 400 |
| CTA | 48 | 800 |

## Slide-by-Slide Structure

### Slide 1 — Hook Headline + Visual

- Latar: `--bg-primary` (gelap)
- Text: `--text-on-dark`
- Layout: headline center-aligned, max 8 kata, judul dari `TITLE` (truncate jika perlu, tambah ellipsis)
- Visual anchor: SVG icon abstract relevan dengan `relevance_tags` (lihat icon table di bawah)
- Page indicator: "1/7" pojok kanan bawah, `--text-muted`
- Brand mark: "OJS Intel" pojok kiri bawah, kecil, `--text-on-dark`

### Slide 2 — Konteks (Apa & Kapan)

- Latar: `--bg-secondary`
- Heading: "Konteks" — `--accent`
- Body 2-3 kalimat: kapan + apa singkat (1 kalimat = "Pada {published_at_human}, {what_happened}").
- Source pill di bawah: chip kecil dengan `source_url` domain only (mis. "pkp.sfu.ca")

### Slide 3-5 — Key Points

Tiga slide independen, satu key point per slide.

- Latar: `--bg-secondary`
- Heading: "Poin {N}" (1, 2, 3) — `--accent`
- Body: `KEY_POINTS[N-3]` rephrased ke 1-2 kalimat penuh (jangan paste raw bullet)
- Optional: ikon kecil di pojok atas kiri

### Slide 6 — Implikasi Praktis

- Latar: `--bg-secondary`
- Heading: "Untuk Editor & Pengelola Jurnal" — `--accent`
- Body: 2-3 kalimat actionable, derived dari `audience_fit` + `actionable` framing brief
- Bullet list (opsional, max 3 item)

### Slide 7 — CTA

- Latar: `--bg-primary`
- Headline: copy varian dari `references/cta-variants.md` — `--text-on-dark`
- Sub-headline: 1 kalimat penjelas
- CTA button: latar `--cta-bg`, text `--cta-text`, rounded 12px, padding 24px 48px
- URL display: `openjournaltheme.com` (tanpa https:// di visual, simpan di metadata SVG)
- Brand mark + page "7/7"

## A11y Carousel

1. **Text dalam SVG**: pakai `<text>` element, bukan path. Ini memberi screen reader access + selectable.
2. **Title & desc**: setiap SVG punya `<title>` dan `<desc>` di root untuk konteks AT.
   ```svg
   <svg ...>
     <title>Slide 1: Hook headline</title>
     <desc>{{TITLE}} — slide pembuka carousel OJS Intel</desc>
     ...
   </svg>
   ```
3. **Tab order**: jika carousel di-embed dengan navigation, semua slide accessible via keyboard.
4. **Page indicator**: text "N/7", bukan hanya dot graphic.
5. **Color contrast**: semua kombinasi sudah dihitung di atas. Jangan pakai warna lain tanpa cek ulang.
6. **Font size minimum**: 24px untuk body teks di 1080×1080 — tidak boleh lebih kecil.

## Icon Mapping (untuk visual anchor slide 1 dan 3-5)

Pakai icon Heroicons outline (CC-BY licensed, embeddable inline SVG):

| relevance_tag | Icon |
|---------------|------|
| `security` | shield-exclamation |
| `release` | rocket-launch |
| `feature` | sparkles |
| `tutorial` | academic-cap |
| `community` | users |
| `integration` | link |
| `policy` | document-text |

Inline SVG (no external request). Source: heroicons.com.

## Render Process

```bash
scripts/render_carousel.py \
  --brief brief.json \
  --candidate candidate.json \
  --dimension 1080x1080 \
  --output out/slide-{n}.svg
```

Atau combined single-file:

```bash
scripts/render_carousel.py \
  --brief brief.json \
  --candidate candidate.json \
  --dimension 1080x1080 \
  --combined \
  --output out/carousel.svg
```
