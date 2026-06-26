# SEO Expert – reference index

Skill id **`seo-expert-pro`**. Load this file first, then open the smallest reference that matches the task.

German excerpts from **Google Search Central** (see blockquote in each file for source / date). Order **01 → 04** follows a typical workflow; **03** is the Appearance / ranking & presentation cluster (split into hub + parts); **05** is the web-specific guides cluster (hub + `05.1`–`05.8`).

| File | Content |
| ---- | ------- |
| [01_seo_grundlagen.md](01_seo_grundlagen.md) | SEO-Grundlagen: wie Google Search funktioniert, On-/Off-Page, technisches SEO, E-E-A-T |
| [02_crawling_indexierung.md](02_crawling_indexierung.md) | Crawling & Indexierung: robots.txt, Meta/X-Robots, Sitemaps, Canonicals, Removals, JavaScript |
| [04_monitoring_fehlerbehebung.md](04_monitoring_fehlerbehebung.md) | Monitoring & Fehlerbehebung: Search Console, Index Coverage, URL Inspection, Traffic, Manual Actions, Sicherheit |
| [AUTH.md](AUTH.md) | Env / Geheimnisse: keine Tokens in Chat; optional `SEO_SITE_BASE_URL` |

## Google Search Central: Ranking und Darstellung (03)

| File | Content |
| ---- | ------- |
| [03_ranking_darstellung.md](03_ranking_darstellung.md) | **Hub:** source citation + TOC links to parts `03.1`–`03.7` only |
| [03.1_ranking_darstellung_grundlagen.md](03.1_ranking_darstellung_grundlagen.md) | Darstellung in der Suche, Einführung strukturierte Daten, angereicherte Ergebnisse, allgemeine Richtlinien |
| [03.2_ranking_darstellung_titel_snippets_meta.md](03.2_ranking_darstellung_titel_snippets_meta.md) | Hervorgehobene Snippets, Snippets, Titellinks |
| [03.3_ranking_darstellung_sitelinks_navigation.md](03.3_ranking_darstellung_sitelinks_navigation.md) | Sitelinks, Navigationspfad (Breadcrumb) / strukturierte Daten |
| [03.4_ranking_darstellung_bild_video.md](03.4_ranking_darstellung_bild_video.md) | Google Bilder, Video-SEO |
| [03.5_ranking_darstellung_strukturierte_daten_inhaltstypen.md](03.5_ranking_darstellung_strukturierte_daten_inhaltstypen.md) | Produkt, Artikel, Rezepte, Events, FAQ, LocalBusiness, Organization, Reviews, Video, Q&A, Jobs, Karussell, Software, Kurs |
| [03.6_ranking_darstellung_spezielle_features.md](03.6_ranking_darstellung_spezielle_features.md) | Websitename, Discover, Favicon, KI-Funktionen, Web Stories |
| [03.7_ranking_darstellung_referenz.md](03.7_ranking_darstellung_referenz.md) | Unterstütztes Markup, Galerie visueller Elemente, Anhang/Checklisten |

**03 split:** `python3 scripts/seo_skill/split_ranking_darstellung.py` (`--verify` for lossless check vs `____ablage/03_ranking_darstellung.md` from line 63).

## Google Search Central: Webspezifische Leitfäden (05)

| File | Content |
| ---- | ------- |
| [05_webspezifische_leitfaeden.md](05_webspezifische_leitfaeden.md) | **Hub:** source citation + TOC links to parts `05.1`–`05.8` only |
| [05.1_webspezifische_leitfaeden_javascript_seo.md](05.1_webspezifische_leitfaeden_javascript_seo.md) | JavaScript SEO |
| [05.2_webspezifische_leitfaeden_ecommerce.md](05.2_webspezifische_leitfaeden_ecommerce.md) | E-Commerce SEO |
| [05.3_webspezifische_leitfaeden_international.md](05.3_webspezifische_leitfaeden_international.md) | Internationale & Multiregionale SEO |
| [05.4_webspezifische_leitfaeden_video.md](05.4_webspezifische_leitfaeden_video.md) | Video SEO |
| [05.5_webspezifische_leitfaeden_bilder.md](05.5_webspezifische_leitfaeden_bilder.md) | Bilder SEO |
| [05.6_webspezifische_leitfaeden_news.md](05.6_webspezifische_leitfaeden_news.md) | News SEO |
| [05.7_webspezifische_leitfaeden_mobile_first.md](05.7_webspezifische_leitfaeden_mobile_first.md) | Mobile-First Indexing |
| [05.8_webspezifische_leitfaeden_zusammenfassung.md](05.8_webspezifische_leitfaeden_zusammenfassung.md) | Zusammenfassung / Best Practices |

**05 split:** `python3 scripts/seo_skill/split_webspezifische_leitfaeden.py` (`--verify` for lossless check vs `____ablage/05_webspezifische_leitfaeden.md` from line 43).

**Maintainer:** [docs/openclaw-seo/README.md](../../docs/openclaw-seo/README.md).
