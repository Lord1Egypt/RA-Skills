---
name: tavily-search
description: "Tavily API ile güvenli web arama ve URL içerik çıkarma yap. Use when: hızlı web araştırması, kaynaklı sonuç toplama, belirli URL'lerden metin çekme ve özetleme gerektiğinde."
---

# Tavily Search (Secure)

Tavily API ile güvenli arama/extract akışı çalıştır.

## Gereksinim

- `TAVILY_API_KEY` ortam değişkeni tanımlı olmalı.
- API anahtarını dosyaya yazma, commit etme veya çıktıda gösterme.

## Arama

```bash
node {baseDir}/scripts/search.mjs "query"
node {baseDir}/scripts/search.mjs "query" -n 8 --deep
node {baseDir}/scripts/search.mjs "query" --topic news --days 3
```

## URL içerik çıkarma

```bash
node {baseDir}/scripts/extract.mjs "https://example.com/article"
node {baseDir}/scripts/extract.mjs "https://a.com" "https://b.com"
```

## Güvenlik kuralları

- Sadece `http` / `https` URL kabul et.
- Localhost, loopback, private IP ve `.local/.internal` alan adlarını reddet.
- Tek istekte URL sayısını sınırlı tut (script varsayılanı uygular).
- Hata durumunda kısa ve temiz hata ver; anahtar veya hassas veri dökme.
