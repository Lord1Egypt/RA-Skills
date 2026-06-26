# SEOwlsClaw — SEO Plan File Format
# File: SEO_PLANS/plan-template.md
# Purpose: Defines the exact structure of every saved plan file.
#          Also serves as a filled-in example (vintage analog cameras, DE).
# Copy this → rename to SEO_PLANS/<plan-id>.md → replace all values.

---

# SEO Plan — [Niche] ([lang])
# ══════════════════════════════════════════════════════════════════════════════
# HEADER — machine-parsed by /seobrief --plan and /write --plan
# ══════════════════════════════════════════════════════════════════════════════
plan_id: [your-plan-id]
niche: [niche label]
mode: [cluster / site]
lang: [de / en / fr / es / pt]
brand: [brand-id or none]
date: [YYYY-MM-DD]
priority_focus: [balanced / quickwins / strategic]
total_nodes: [n]

---

# ══════════════════════════════════════════════════════════════════════════════
# NODE FORMAT — each node uses this exact structure
# ══════════════════════════════════════════════════════════════════════════════
# TIER: PILLAR | QUICKWIN | FOUNDATION | STRATEGIC | FAQ
# Copy a node block → change tier + values → add to the correct tier section.

### node: [node-id]
tier: [PILLAR / QUICKWIN / FOUNDATION / STRATEGIC / FAQ]
slug: /[suggested-url-path]
title: [H1 suggestion — include primary keyword]
primary_kw: [main target keyword]
secondary_kw: [kw1], [kw2], [kw3]
page_type: [Blogpost / Landingpage / Productnew / Productused / FAQ]
intent: [informational / commercial / transactional / navigational]
difficulty: [1–100]
volume: [est. monthly searches]
words: [target word count]
persona_zone_a: [blogger / researcher / vintage-expert / creative-writer]
persona_zone_b: [ecommerce-manager / creative-writer / none]
serp_targets: [featured-snippet-type], [paa], [image-pack] (comma-separated)
links_to: [node-id], [node-id]     ← this page links TO these nodes
links_from: [node-id], [node-id]   ← these nodes link TO this page
seobrief_cmd: /seobrief [Type] "[title]" --plan [plan-id].[node-id] --lang [lang]

---

# ══════════════════════════════════════════════════════════════════════════════
# EXAMPLE PLAN (filled in): Vintage Analog Cameras — Germany
# ══════════════════════════════════════════════════════════════════════════════

plan_id: vintage-analog-cameras-de
niche: Vintage & Analog Cameras (Germany)
mode: cluster
lang: de
brand: jbv-foto
date: 2026-04-05
priority_focus: balanced
total_nodes: 11

---

## TOPICAL MAP (text overview)

Pillar: "Analogkamera kaufen" (1 page)
  ├── Quick Wins (4 pages):  film-einlegen, rangefinder-erklaert, sw-film-vergleich, kamera-anfaenger
  ├── Foundation (3 pages):  analogfotografie-grundlagen, kamera-pflege, leica-m-mount
  └── Strategic (3 pages):   beste-analogkameras-2026, leica-m6-kaufen, analog-vs-digital

---

## TIER: PILLAR

### node: pillar-01
tier: PILLAR
slug: /blog/analogkamera-kaufen-guide
title: Analogkamera kaufen: Der vollständige Ratgeber 2026
primary_kw: analogkamera kaufen
secondary_kw: analoge kamera kaufen, beste analogkamera, analoge kamera empfehlung
page_type: Blogpost
intent: commercial
difficulty: 52
volume: 1200
words: 2500
persona_zone_a: researcher
persona_zone_b: ecommerce-manager
serp_targets: featured-snippet-comparison-table, paa, image-pack
links_to: qw-01, qw-02, qw-03, qw-04, fnd-01, fnd-02, str-01, str-02
links_from: qw-01, qw-02, qw-03, qw-04, fnd-01, fnd-02, fnd-03, str-01, str-02, str-03
seobrief_cmd: /seobrief Blogpost "Analogkamera kaufen Guide 2026" --plan vintage-analog-cameras-de.pillar-01 --lang de

---

## TIER: QUICKWIN
# Difficulty < 25 | Can rank within 2–6 weeks | Execute FIRST

### node: qw-01
tier: QUICKWIN
slug: /blog/analogkamera-film-einlegen-anleitung
title: Analogkamera Film einlegen: Schritt-für-Schritt Anleitung
primary_kw: analogkamera film einlegen
secondary_kw: film einlegen anleitung, 35mm film einlegen
page_type: Blogpost
intent: informational
difficulty: 14
volume: 320
words: 1200
persona_zone_a: blogger
persona_zone_b: none
serp_targets: featured-snippet-steps, paa
links_to: pillar-01, fnd-01
links_from: pillar-01
seobrief_cmd: /seobrief Blogpost "Analogkamera Film einlegen Anleitung" --plan vintage-analog-cameras-de.qw-01 --lang de

### node: qw-02
tier: QUICKWIN
slug: /blog/rangefinder-kamera-erklaert
title: Rangefinder Kamera erklärt: Was ist das und wie funktioniert sie?
primary_kw: rangefinder kamera
secondary_kw: messsucher kamera, rangefinder vs spiegelreflex
page_type: Blogpost
intent: informational
difficulty: 11
volume: 210
words: 1200
persona_zone_a: researcher
persona_zone_b: none
serp_targets: featured-snippet-definition, paa
links_to: pillar-01, str-02
links_from: pillar-01, str-02
seobrief_cmd: /seobrief Blogpost "Rangefinder Kamera erklärt" --plan vintage-analog-cameras-de.qw-02 --lang de

### node: qw-03
tier: QUICKWIN
slug: /blog/schwarzweiss-film-vergleich
title: Schwarzweiß Film Vergleich 2026: Die besten Filme für Einsteiger und Profis
primary_kw: schwarzweiss film vergleich
secondary_kw: bester sw film analog, ilford hp5 vs kodak tmax
page_type: Blogpost
intent: commercial
difficulty: 17
volume: 180
words: 1500
persona_zone_a: researcher
persona_zone_b: none
serp_targets: featured-snippet-comparison-table, paa
links_to: pillar-01, qw-01
links_from: pillar-01
seobrief_cmd: /seobrief Blogpost "Schwarzweiß Film Vergleich 2026" --plan vintage-analog-cameras-de.qw-03 --lang de

### node: qw-04
tier: QUICKWIN
slug: /blog/analoge-kamera-anfaenger
title: Analoge Kamera für Anfänger: Welche ist die beste Einstiegskamera?
primary_kw: analoge kamera für anfänger
secondary_kw: einstiegskamera analog, erste analogkamera empfehlung
page_type: Blogpost
intent: commercial
difficulty: 19
volume: 240
words: 1500
persona_zone_a: blogger
persona_zone_b: none
serp_targets: featured-snippet-list, paa, image-pack
links_to: pillar-01, str-01
links_from: pillar-01
seobrief_cmd: /seobrief Blogpost "Analoge Kamera für Anfänger" --plan vintage-analog-cameras-de.qw-04 --lang de

---

## TIER: FOUNDATION
# Medium difficulty | Builds topical authority | Execute after Quick Wins

### node: fnd-01
tier: FOUNDATION
slug: /blog/analogfotografie-grundlagen
title: Analogfotografie Grundlagen: Belichtung, Blende und Verschlusszeit einfach erklärt
primary_kw: analogfotografie grundlagen
secondary_kw: analogfotografie lernen, belichtungsdreieck analog
page_type: Blogpost
intent: informational
difficulty: 28
volume: 390
words: 2000
persona_zone_a: blogger
persona_zone_b: none
serp_targets: paa, featured-snippet-steps
links_to: pillar-01, qw-01, fnd-02
links_from: pillar-01, qw-01, qw-04
seobrief_cmd: /seobrief Blogpost "Analogfotografie Grundlagen" --plan vintage-analog-cameras-de.fnd-01 --lang de

### node: fnd-02
tier: FOUNDATION
slug: /blog/analogkamera-reinigen-pflegen
title: Analogkamera reinigen und pflegen: So bleibt deine Kamera in Top-Zustand
primary_kw: analogkamera reinigen
secondary_kw: kamera pflegen, objektiv reinigen analog
page_type: Blogpost
intent: informational
difficulty: 22
volume: 150
words: 1200
persona_zone_a: vintage-expert
persona_zone_b: none
serp_targets: featured-snippet-steps, paa
links_to: pillar-01, fnd-01
links_from: pillar-01, fnd-01
seobrief_cmd: /seobrief Blogpost "Analogkamera reinigen und pflegen" --plan vintage-analog-cameras-de.fnd-02 --lang de

### node: fnd-03
tier: FOUNDATION
slug: /faq/leica-m-mount-system
title: Leica M-Mount FAQ: Alles zu Objektiven, Adaptern und Kompatibilität
primary_kw: leica m mount
secondary_kw: leica m objektiv kompatibilität, m mount adapter
page_type: FAQ
intent: informational
difficulty: 31
volume: 280
words: 1000
persona_zone_a: researcher
persona_zone_b: none
serp_targets: paa, faq-accordion
links_to: pillar-01, str-02
links_from: pillar-01, str-02, qw-02
seobrief_cmd: /seobrief FAQ "Leica M-Mount FAQ" --plan vintage-analog-cameras-de.fnd-03 --lang de

---

## TIER: STRATEGIC
# High difficulty | High value | Execute after pillar is indexed

### node: str-01
tier: STRATEGIC
slug: /blog/beste-analogkameras-2026
title: Die besten Analogkameras 2026: Top 10 Empfehlungen für jeden Etatrahmen
primary_kw: beste analogkamera
secondary_kw: beste analoge kamera 2026, top analogkameras vergleich
page_type: Blogpost
intent: commercial
difficulty: 48
volume: 680
words: 3000
persona_zone_a: researcher
persona_zone_b: ecommerce-manager
serp_targets: featured-snippet-list, image-pack, paa
links_to: pillar-01, str-02, qw-04
links_from: pillar-01, qw-04
seobrief_cmd: /seobrief Blogpost "Beste Analogkameras 2026" --plan vintage-analog-cameras-de.str-01 --lang de --depth deep

### node: str-02
tier: STRATEGIC
slug: /leica-m6-kaufen
title: Leica M6 kaufen: Preise, Varianten und worauf du achten solltest
primary_kw: leica m6 kaufen
secondary_kw: leica m6 gebraucht kaufen, leica m6 preis 2026
page_type: Productused
intent: transactional
difficulty: 55
volume: 520
words: 800
persona_zone_a: vintage-expert
persona_zone_b: ecommerce-manager
serp_targets: shopping-results, paa
links_to: pillar-01, fnd-03, qw-02
links_from: pillar-01, str-01, qw-02, fnd-03
seobrief_cmd: /seobrief Productused "Leica M6 kaufen" --plan vintage-analog-cameras-de.str-02 --lang de

### node: str-03
tier: STRATEGIC
slug: /blog/analog-vs-digital-kamera
title: Analoge Kamera vs. Digitalkamera: Was ist besser für welchen Fotografen?
primary_kw: analoge kamera vs digitalkamera
secondary_kw: analog oder digital fotografie, vor und nachteile analogfotografie
page_type: Blogpost
intent: commercial
difficulty: 44
volume: 410
words: 2000
persona_zone_a: creative-writer
persona_zone_b: none
serp_targets: featured-snippet-comparison-table, paa
links_to: pillar-01, str-01, qw-04
links_from: pillar-01
seobrief_cmd: /seobrief Blogpost "Analoge vs. Digitale Kamera Vergleich" --plan vintage-analog-cameras-de.str-03 --lang de

---

## INTERNAL LINK MATRIX

| From \ To | pillar-01 | qw-01 | qw-02 | qw-03 | qw-04 | fnd-01 | fnd-02 | fnd-03 | str-01 | str-02 | str-03 |
|-----------|-----------|-------|-------|-------|-------|--------|--------|--------|--------|--------|--------|
| pillar-01 | — | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | — | ✅ | ✅ | — |
| qw-01 | ✅ | — | — | — | — | ✅ | — | — | — | — | — |
| qw-02 | ✅ | — | — | — | — | — | — | — | — | ✅ | — |
| qw-03 | ✅ | ✅ | — | — | — | — | — | — | — | — | — |
| qw-04 | ✅ | — | — | — | — | — | — | — | ✅ | — | — |
| fnd-01 | ✅ | ✅ | — | — | — | — | ✅ | — | — | — | — |
| fnd-02 | ✅ | — | — | — | — | ✅ | — | — | — | — | — |
| fnd-03 | ✅ | — | ✅ | — | — | — | — | — | — | ✅ | — |
| str-01 | ✅ | — | — | — | ✅ | — | — | — | — | ✅ | — |
| str-02 | ✅ | — | ✅ | — | — | — | — | ✅ | — | — | — |
| str-03 | ✅ | — | — | — | ✅ | — | — | — | ✅ | — | — |

---

## EXECUTION ORDER

# Rule: Quick Wins first → build topical signal and internal link anchors
#       Pillar second → now benefits from internal links from Quick Wins
#       Foundation after pillar → supports pillar authority
#       Strategic last → push with full internal link network behind them

1.  qw-01   /blog/analogkamera-film-einlegen-anleitung     Diff 14 — Execute immediately
2.  qw-02   /blog/rangefinder-kamera-erklaert              Diff 11 — Execute immediately
3.  qw-03   /blog/schwarzweiss-film-vergleich              Diff 17 — Execute immediately
4.  qw-04   /blog/analoge-kamera-anfaenger                 Diff 19 — Execute immediately
5.  fnd-01  /blog/analogfotografie-grundlagen              Diff 28 — After QWs indexed (4–6 weeks)
6.  fnd-02  /blog/analogkamera-reinigen-pflegen            Diff 22 — After QWs indexed
7.  pillar-01 /blog/analogkamera-kaufen-guide              Diff 52 — After QWs + fnd-01/02 live
8.  fnd-03  /faq/leica-m-mount-system                     Diff 31 — Supports str-02 launch
9.  str-01  /blog/beste-analogkameras-2026                Diff 48 — After pillar indexed
10. str-02  /leica-m6-kaufen                              Diff 55 — After pillar + fnd-03
11. str-03  /blog/analog-vs-digital-kamera                Diff 44 — After str-01 indexed

---

## NEXT STEP

Start with the first Quick Win. Run this command:

/seobrief Blogpost "Analogkamera Film einlegen Anleitung" --plan vintage-analog-cameras-de.qw-01 --lang de

---

*Plan version: v0.1 — 2026-04-05*
*Maintainer: Chris*
