# Google SEO: Crawling und Indexierung - Komplette Referenz

> **Quelle:** [Google Search Central - Crawling und Indexierung](https://developers.google.com/search/docs/crawling-indexing?hl=de)  
> **Zuletzt aktualisiert:** 2026  
> **Sprache:** Deutsch

---

## Inhaltsverzeichnis

1. [Grundlagen: Wie Google crawlt und indexiert](#1-grundlagen-wie-google-crawlt-und-indexiert)
2. [robots.txt - Steuerung des Crawlings](#2-robotstxt---steuerung-des-crawlings)
3. [Robots-Meta-Tags und X-Robots-Tag](#3-robots-meta-tags-und-x-robots-tag)
4. [Sitemaps (XML-Sitemaps)](#4-sitemaps-xml-sitemaps)
5. [Canonical URLs und Duplicate Content](#5-canonical-urls-und-duplicate-content)
6. [noindex, nofollow und weitere Direktiven](#6-noindex-nofollow-und-weitere-direktiven)
7. [Crawl-Budget-Optimierung](#7-crawl-budget-optimierung)
8. [URL-Struktur und Best Practices](#8-url-struktur-und-best-practices)
9. [Weiterleitungen (Redirects)](#9-weiterleitungen-redirects)
10. [JavaScript-SEO Grundlagen](#10-javascript-seo-grundlagen)
11. [HTTP-Fehler und Netzwerkprobleme](#11-http-fehler-und-netzwerkprobleme)
12. [Google-Crawler (User-Agents)](#12-google-crawler-user-agents)
13. [Indexierungsprobleme beheben](#13-indexierungsprobleme-beheben)

---

## 1. Grundlagen: Wie Google crawlt und indexiert

### Der dreistufige Prozess

```
Crawling → Indexing → Ranking (Serving)
```

#### 1.1 Crawling (Erfassen)
- Google verwendet **Crawler** (auch "Robots" oder "Spider" genannt)
- Der Crawler folgt Links von bekannten Seiten zu neuen Seiten
- URLs werden aus verschiedenen Quellen gesammelt:
  - Sitemaps
  - Interne/externe Links
  - Nutzereingaben
  - Google Search Console

#### 1.2 Indexing (Indexierung)
- Nach dem Crawling wird der Inhalt analysiert und verarbeitet
- Google extrahiert:
  - Textinhalt
  - Meta-Informationen
  - Strukturierte Daten
  - Bilder und Videos
- Nicht jede gecrawlte Seite wird indexiert!

#### 1.3 Ranking (Darstellung)
- Indexierte Seiten können in Suchergebnissen erscheinen
- Die Reihenfolge wird durch Ranking-Systeme bestimmt

### Wichtige Einschränkungen

> **Wichtig:** Bei der Google Suche wird **nicht jede gecrawlte Seite indexiert**. Nach dem Crawling muss jede Seite evaluiert, konsolidiert und bewertet werden, um ihre Eignung für den Index zu bestimmen.

---

## 2. robots.txt - Steuerung des Crawlings

### Was ist robots.txt?

Die `robots.txt`-Datei steuert, welche Bereiche einer Website von Crawlern besucht werden dürfen. Sie muss im Root-Verzeichnis der Domain liegen:

```
https://www.example.com/robots.txt
```

### Grundlegende Syntax

```txt
# Kommentar
User-agent: [Crawler-Name]
Disallow: [Pfad der blockiert werden soll]
Allow: [Pfad der erlaubt ist]
Sitemap: [URL zur Sitemap]
```

### Beispiele fuer robots.txt

#### 2.1 Alle Crawler duerfen alles crawlen

```txt
User-agent: *
Disallow:
```

#### 2.2 Alle Crawler komplett blockieren

```txt
User-agent: *
Disallow: /
```

#### 2.3 Spezifische Bereiche blockieren

```txt
User-agent: *
Disallow: /admin/
Disallow: /private/
Disallow: /tmp/
Disallow: /*.pdf$

# Erlaubt trotzdem bestimmte Pfade
Allow: /admin/public/

# Sitemap angeben
Sitemap: https://www.example.com/sitemap.xml
```

#### 2.4 Verschiedene Regeln fuer verschiedene Crawler

```txt
# Regeln fuer Googlebot
User-agent: Googlebot
Disallow: /private/
Allow: /public/

# Regeln fuer alle anderen
User-agent: *
Disallow: /
```

### Wichtige robots.txt-Befehle

| Befehl | Beschreibung |
|--------|--------------|
| `User-agent` | Gibt an, fuer welchen Crawler die Regel gilt (`*` = alle) |
| `Disallow` | Verhindert das Crawling des angegebenen Pfads |
| `Allow` | Erlaubt das Crawling trotz allgemeiner Disallow-Regel |
| `Sitemap` | Verweist auf die XML-Sitemap |

### Wichtige Warnungen zu robots.txt

> **robots.txt blockiert nur das Crawling, NICHT die Indexierung!**
> 
> Wenn eine Seite durch robots.txt blockiert wird, kann Google sie trotzdem indexieren, wenn:
> - Andere Seiten auf sie verlinken
> - Sie in einer Sitemap gelistet ist
> - Externe Signale auf sie hinweisen
>
> **Loesung:** Verwende `noindex` im Meta-Tag oder X-Robots-Tag, um die Indexierung zu verhindern.

### Technische Details

- **Maximale Groesse:** 500 KiB (alles danach wird ignoriert)
- **Encoding:** UTF-8 empfohlen
- **Zeilenumbruch:** LF oder CRLF
- **Case-Sensitive:** Pfade sind case-sensitive


---

## 3. Robots-Meta-Tags und X-Robots-Tag

### Unterschied: robots.txt vs. Meta-Tags

| Methode | Blockiert Crawling | Blockiert Indexierung |
|---------|-------------------|----------------------|
| robots.txt | Ja | Nein |
| Robots-Meta-Tag | Nein | Ja |
| X-Robots-Tag | Nein | Ja |

### Robots-Meta-Tag (HTML)

Das Meta-Tag wird im `<head>`-Bereich der HTML-Seite platziert:

```html
<!-- Seite nicht indexieren -->
<meta name="robots" content="noindex">

<!-- Seite nicht indexieren und Links nicht folgen -->
<meta name="robots" content="noindex, nofollow">

<!-- Nur Googlebot ansprechen -->
<meta name="googlebot" content="noindex">

<!-- Mehrere Direktiven kombinieren -->
<meta name="robots" content="noindex, nofollow, noarchive">
```

### X-Robots-Tag (HTTP-Header)

Fuer nicht-HTML-Inhalte (PDFs, Bilder, etc.):

```http
X-Robots-Tag: noindex
X-Robots-Tag: noindex, nofollow
X-Robots-Tag: googlebot: noindex
```

### Uebersicht aller Direktiven

| Direktive | Beschreibung |
|-----------|--------------|
| `noindex` | Seite nicht in den Suchindex aufnehmen |
| `nofollow` | Links auf der Seite nicht folgen |
| `none` | Kombination aus `noindex, nofollow` |
| `noarchive` | Keine Cached-Version in den Suchergebnissen anzeigen |
| `nosnippet` | Keinen Text-Snippet in den Suchergebnissen anzeigen |
| `max-snippet:[number]` | Maximale Zeichenanzahl fuer Snippets |
| `max-image-preview:[setting]` | Bildvorschau-Groesse steuern (`none`, `standard`, `large`) |
| `max-video-preview:[number]` | Maximale Sekunden fuer Videovorschau |
| `noimageindex` | Bilder auf der Seite nicht indexieren |
| `notranslate` | Keine Uebersetzung in den Suchergebnissen anbieten |
| `unavailable_after:[date]` | Seite nach Datum nicht mehr anzeigen |
| `index` | Seite indexieren (Standard, optional) |
| `follow` | Links folgen (Standard, optional) |
| `all` | Kombination aus `index, follow` (Standard) |

### Praktische Beispiele

#### Such-Snippets begrenzen

```html
<!-- Snippet auf 150 Zeichen begrenzen -->
<meta name="robots" content="max-snippet:150">

<!-- Keine Bildvorschau -->
<meta name="robots" content="max-image-preview:none">

<!-- Kombinierte Direktiven -->
<meta name="robots" content="max-snippet:200, max-image-preview:large">
```

#### Zeitlich begrenzte Indexierung

```html
<!-- Seite nach bestimmtem Datum nicht mehr anzeigen -->
<meta name="robots" content="unavailable_after: 2024-12-31">
```


---

## 4. Sitemaps (XML-Sitemaps)

### Was ist eine Sitemap?

Eine Sitemap ist eine Datei, die URLs einer Website auflistet und zusatzliche Metadaten zu jeder URL bereitstellt:
- Wann wurde sie zuletzt geaendert?
- Wie oft aendert sie sich?
- Wie wichtig ist sie relativ zu anderen URLs?

### XML-Sitemap-Format

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://www.example.com/produkte/</loc>
    <lastmod>2024-01-10</lastmod>
    <changefreq>daily</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Sitemap-Elemente

| Element | Beschreibung | Pflicht |
|---------|--------------|---------|
| `<loc>` | URL der Seite | Ja |
| `<lastmod>` | Datum der letzten Aenderung (YYYY-MM-DD) | Optional |
| `<changefreq>` | Aenderungshaeufigkeit (`always`, `hourly`, `daily`, `weekly`, `monthly`, `yearly`, `never`) | Optional |
| `<priority>` | Prioritaet 0.0 - 1.0 (Standard: 0.5) | Optional |

### Sitemap-Index (fuer grosse Websites)

Wenn du mehr als 50.000 URLs hast oder die Datei groesser als 50 MiB ist:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://www.example.com/sitemap1.xml</loc>
    <lastmod>2024-01-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://www.example.com/sitemap2.xml</loc>
    <lastmod>2024-01-14</lastmod>
  </sitemap>
</sitemapindex>
```

### Spezielle Sitemap-Typen

#### 4.1 Bilder-Sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">
  <url>
    <loc>https://example.com/seite.html</loc>
    <image:image>
      <image:loc>https://example.com/bild.jpg</image:loc>
      <image:caption>Bildbeschreibung</image:caption>
      <image:title>Bildtitel</image:title>
    </image:image>
  </url>
</urlset>
```

#### 4.2 Video-Sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">
  <url>
    <loc>https://example.com/video-seite.html</loc>
    <video:video>
      <video:thumbnail_loc>https://example.com/thumbnail.jpg</video:thumbnail_loc>
      <video:title>Video-Titel</video:title>
      <video:description>Video-Beschreibung</video:description>
      <video:content_loc>https://example.com/video.mp4</video:content_loc>
      <video:duration>600</video:duration>
    </video:video>
  </url>
</urlset>
```

#### 4.3 News-Sitemap (Google News)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">
  <url>
    <loc>https://example.com/news/artikel.html</loc>
    <news:news>
      <news:publication>
        <news:name>Meine Zeitung</news:name>
        <news:language>de</news:language>
      </news:publication>
      <news:publication_date>2024-01-15</news:publication_date>
      <news:title>Artikel-Titel</news:title>
    </news:news>
  </url>
</urlset>
```

### Sitemap einreichen

1. **In robots.txt verweisen:**
   ```txt
   Sitemap: https://www.example.com/sitemap.xml
   ```

2. **Ueber Google Search Console:**
   - Sitemaps-Bereich -> Sitemap-URL eingeben -> "Einreichen"

3. **HTTP-Ping (optional):**
   ```
   https://www.google.com/ping?sitemap=https://www.example.com/sitemap.xml
   ```

### Technische Limits

| Limit | Wert |
|-------|------|
| Maximale URLs pro Sitemap | 50.000 |
| Maximale Dateigroesse | 50 MiB (ungepackt) |
| Maximale Sitemaps in Index | 50.000 |
| URL-Encoding | UTF-8 |

### Best Practices

> - **Nur kanonische URLs** in der Sitemap auflisten
> - **Keine noindex-Seiten** in die Sitemap aufnehmen
> - **Sitemap aktuell halten** - veraltete `lastmod`-Daten werden ignoriert
> - **Prioritaet nicht ueberbewerten** - hat minimalen Einfluss auf Crawling
> - **Sitemap automatisch generieren** bei dynamischen Websites


---

## 5. Canonical URLs und Duplicate Content

### Was ist Kanonisierung?

Kanonisierung ist der Prozess, bei dem Google die "beste" Version einer Seite auswaehlt, wenn mehrere URLs denselben oder sehr aehnlichen Inhalt haben.

### rel="canonical" Link-Tag

```html
<!-- Auf der Duplikat-Seite: Verweis auf die Original-URL -->
<link rel="canonical" href="https://www.example.com/original-seite/">
```

### HTTP-Header fuer Canonical URLs

Fuer nicht-HTML-Dokumente (PDFs, etc.):

```http
Link: <https://www.example.com/original-dokument.pdf>; rel="canonical"
```

### Sitemap-Canonical

Google verwendet URLs in der Sitemap als kanonische Hinweise.

### 301-Weiterleitung als Canonical-Signal

```
HTTP/1.1 301 Moved Permanently
Location: https://www.example.com/kanonische-url/
```

### Wann Canonical verwenden?

| Szenario | Loesung |
|----------|---------|
| Produktvarianten (Farbe, Groesse) | Canonical auf Hauptprodukt |
| Tracking-Parameter in URLs | Canonical ohne Parameter |
| HTTP/HTTPS Duplikate | Canonical auf HTTPS |
| www/non-www Duplikate | Canonical auf bevorzugte Version |
| Paginierung | Jede Seite canonical auf sich selbst |
| AMP-Seiten | AMP-Seite canonical auf Non-AMP |
| Druckansichten | Canonical auf Originalseite |

### Haeufige Canonical-Fehler

> **Fehler 1: Canonical-Ketten vermeiden**
> ```
> FALSCH: Seite A -> Seite B -> Seite C
> RICHTIG: Seite A -> Seite C
> RICHTIG: Seite B -> Seite C
> ```
>
> **Fehler 2: Canonical auf nicht-existente URLs**
> ```
> FALSCH: <link rel="canonical" href="https://example.com/404">
> ```
>
> **Fehler 3: Canonical auf noindex-Seiten**
> ```
> FALSCH: Seite A (indexierbar) -> Seite B (noindex)
> ```
>
> **Fehler 4: Mehrere Canonical-Tags**
> Google ignoriert alle Canonical-Tags, wenn mehrere vorhanden sind.

---

## 6. noindex, nofollow und weitere Direktiven

### Kombination von Direktiven

```html
<!-- Nicht indexieren, Links nicht folgen -->
<meta name="robots" content="noindex, nofollow">

<!-- Indexieren, aber Links nicht folgen -->
<meta name="robots" content="index, nofollow">

<!-- Nicht indexieren, aber Links folgen -->
<meta name="robots" content="noindex, follow">

<!-- Keine Snippets, keine Archivierung -->
<meta name="robots" content="nosnippet, noarchive">
```

### Unterschied: robots.txt vs. noindex

```
Methode          | Crawling              | Indexierung
-----------------|-----------------------|------------------------
robots.txt       | Blockiert             | Nicht garantiert*
                 | Disallow: /seite      | (kann trotzdem
                 |                       | indexiert werden)
-----------------|-----------------------|------------------------
noindex          | Erlaubt               | Blockiert
Meta-Tag         | (Seite muss gecrawlt  | (Seite erscheint
                 | werden, um Tag zu     | nicht in SERPs)
                 | sehen)                |

* Wenn externe Links auf die Seite verweisen
```

### Link-Level nofollow

```html
<!-- Einzelnen Link als nofollow markieren -->
<a href="https://example.com/seite.html" rel="nofollow">Link-Text</a>

<!-- Sponsored Link (empfohlen fuer bezahlte Links) -->
<a href="https://example.com/" rel="sponsored">Bezahlter Link</a>

<!-- User-generated Content -->
<a href="https://example.com/" rel="ugc">Nutzer-Link</a>

<!-- Kombination -->
<a href="https://example.com/" rel="nofollow sponsored">Link</a>
```

### Moderne rel-Attribute

| Attribut | Verwendung |
|----------|------------|
| `nofollow` | Link nicht als Empfehlung werten |
| `sponsored` | Bezahlte Werbelinks |
| `ugc` | User-generated Content (Kommentare, Foren) |

> **Hinweis:** `nofollow`, `sponsored` und `ugc` sind **hinweise**, keine Befehle. Google kann entscheiden, dem Link dennoch zu folgen.


---

## 7. Crawl-Budget-Optimierung

### Was ist das Crawl-Budget?

Das Crawling-Budget ist die **Zeit und die Ressourcen**, die Google fuer das Crawling einer Website aufwendet. Es besteht aus zwei Faktoren:

1. **Crawling-Kapazitaetslimit:** Maximale Anzahl paralleler Verbindungen
2. **Crawling-Bedarf:** Wie oft Google die Seite crawlen moechte

### Fuer wen ist Crawl-Budget-Optimierung wichtig?

| Website-Typ | Empfohlene Aktion |
|-------------|-------------------|
| Grosse Websites (>1 Mio. Seiten) | Optimierung empfohlen |
| Mittelgrosse (>10.000) mit taeglichen Aenderungen | Optimierung empfohlen |
| Kleine Websites (<10.000 Seiten) | Nicht noetig |
| Viele "Gefunden - nicht indexiert" Fehler | Optimierung empfohlen |

### Crawl-Budget optimieren

#### 7.1 Unwichtige URLs blockieren

```txt
# robots.txt - Unnoetige Bereiche blockieren
User-agent: *
Disallow: /api/
Disallow: /internal/
Disallow: /search?
Disallow: /*?sort=
Disallow: /*?filter=
```

#### 7.2 Facettensuche (Filter) verwalten

```html
<!-- Bei Facettensuche: Canonical auf Hauptseite -->
<link rel="canonical" href="https://example.com/produkte/">

<!-- Oder: Kombination aus noindex und nofollow -->
<meta name="robots" content="noindex, follow">
```

#### 7.3 URL-Parameter in Search Console konfigurieren

- Google Search Console -> Einstellungen -> URL-Parameter
- Parameter definieren, die das Seitenverhalten nicht aendern

#### 7.4 Server-Antwortzeiten optimieren

Schnelle Server = Hoeheres Crawl-Limit

#### 7.5 HTTP-Caching-Header verwenden

```http
Cache-Control: max-age=3600
Last-Modified: Wed, 15 Jan 2024 12:00:00 GMT
ETag: "33a64df5"
```

### Crawl-Rate anpassen

In der Google Search Console kannst du die Crawl-Rate anpassen:
- **Nicht empfohlen** fuer die meisten Websites
- Nur bei Server-Ueberlastung sinnvoll

---

## 8. URL-Struktur und Best Practices

### Grundlegende URL-Regeln

#### 8.1 Einfache, beschreibende URLs

```
GUT:
https://www.example.com/produkte/winterjacke-swarz/
https://www.example.com/blog/seo-tipps-2024/

SCHLECHT:
https://www.example.com/p?id=12345&ref=abc
https://www.example.com/category.php?cat=5&sub=12
```

#### 8.2 Konsistente URL-Struktur

```
GUT (konsistent):
/produkte/kategorie/produkt-name/
/blog/jahr/monat/artikel-titel/

SCHLECHT (inkonsistent):
/produkte/kategorie/produkt-name/
/shop/item.php?id=123
/article.php?p=456
```

#### 8.3 Kleinschreibung verwenden

```
GUT:  https://www.example.com/produkte/
SCHLECHT: https://www.example.com/Produkte/
```

#### 8.4 Bindestriche statt Unterstriche

```
GUT:     https://www.example.com/seo-tipps-2024/
SCHLECHT: https://www.example.com/seo_tipps_2024/
```

### URL-Parameter verwalten

#### Problematische Parameter

```
Zu vermeiden oder zu canonicalisieren:
?utm_source=newsletter
?sessionid=abc123
?sort=price_asc
?page=2
```

#### Loesungen

1. **Canonical Tags:**
   ```html
   <link rel="canonical" href="https://example.com/produkte/">
   ```

2. **robots.txt:**
   ```txt
   Disallow: /*?sessionid=
   Disallow: /*?utm_
   ```

3. **URL-Rewriting (empfohlen):**
   ```apache
   # .htaccess
   RewriteRule ^produkte/([a-z-]+)/$ /product.php?name=$1 [L]
   ```

### Internationalisierung (hreflang)

```html
<!-- Sprach- und Regionsvarianten angeben -->
<link rel="alternate" hreflang="de" href="https://example.com/de/seite/">
<link rel="alternate" hreflang="de-at" href="https://example.com/at/seite/">
<link rel="alternate" hreflang="en" href="https://example.com/en/page/">
<link rel="alternate" hreflang="x-default" href="https://example.com/seite/">
```

### URL-Laenge

| Aspekt | Empfehlung |
|--------|------------|
| Maximale Laenge | ca. 75 Zeichen fuer optimale Darstellung |
| Technisches Limit | ca. 2.000 Zeichen (Browser-abhaengig) |
| Praktisches Limit | So kurz wie moeglich, so lang wie noetig |


---

## 9. Weiterleitungen (Redirects)

### Redirect-Typen

| Status | Typ | Verwendung | SEO-Impact |
|--------|-----|------------|------------|
| 301 | Permanent | Dauerhafte Umleitung | Link-Equity wird weitergegeben |
| 302 | Temporary | Temporaere Umleitung | Link-Equity bleibt bei alter URL |
| 307 | Temporary | Temporaere Umleitung (HTTP/1.1) | Wie 302 |
| 308 | Permanent | Permanente Umleitung (HTTP/1.1) | Wie 301 |
| Meta Refresh | Client-seitig | Nicht empfohlen | Verzoegert, schlechte UX |
| JavaScript | Client-seitig | Nur wenn noetig | Kann Probleme verursachen |

### 301-Redirect implementieren

#### Apache (.htaccess)

```apache
# Einzelne URL
Redirect 301 /alte-seite.html https://www.example.com/neue-seite/

# Mit mod_rewrite
RewriteEngine On
RewriteRule ^alte-seite/$ /neue-seite/ [R=301,L]

# Domain-Umzug
RewriteCond %{HTTP_HOST} ^old-domain\.com$ [NC]
RewriteRule ^(.*)$ https://www.new-domain.com/$1 [R=301,L]
```

#### Nginx

```nginx
# Einzelne URL
location /alte-seite.html {
    return 301 https://www.example.com/neue-seite/;
}

# Domain-Umzug
server {
    listen 80;
    server_name old-domain.com;
    return 301 $scheme://www.new-domain.com$request_uri;
}
```

#### PHP

```php
<?php
header("HTTP/1.1 301 Moved Permanently");
header("Location: https://www.example.com/neue-seite/");
exit();
?>
```

### Redirect-Best-Practices

#### Redirect-Ketten vermeiden

```
SCHLECHT (Kette):
A -> B -> C -> D

GUT (direkt):
A -> D
B -> D
C -> D
```

#### Redirect-Loops vermeiden

```
TOEDLICH:
A -> B -> A -> B -> ... (Loop)
```

### HTTP zu HTTPS

```apache
# .htaccess - Alle HTTP-Anfragen auf HTTPS umleiten
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

### www zu non-www (oder umgekehrt)

```apache
# non-www zu www
RewriteEngine On
RewriteCond %{HTTP_HOST} ^example\.com$ [NC]
RewriteRule ^(.*)$ https://www.example.com/$1 [R=301,L]

# www zu non-www
RewriteEngine On
RewriteCond %{HTTP_HOST} ^www\.example\.com$ [NC]
RewriteRule ^(.*)$ https://example.com/$1 [R=301,L]
```

### Website-Umzug durchfuehren

1. **301-Redirects einrichten:** Alle alten URLs auf neue URLs umleiten
2. **Sitemap aktualisieren:** Neue URLs in Sitemap
3. **Search Console:** Adressaenderungstool verwenden
4. **Interne Links:** Auf neue URLs aktualisieren
5. **Externe Links:** Wenn moeglich aktualisieren lassen
6. **Monitoring:** Traffic und Indexierung ueberwachen

---

## 10. JavaScript-SEO Grundlagen

### Wie Google JavaScript verarbeitet

```
1. Crawling: Googlebot laedt HTML
2. Rendering: Googlebot fuehrt JavaScript aus
3. Indexierung: Gerenderte Seite wird indexiert
```

### Wichtige JavaScript-SEO-Probleme

#### 10.1 Blockierte Ressourcen

```html
SCHLECHT - JavaScript blockiert:
<meta name="robots" content="noindex">  <!-- Im gerenderten HTML -->

GUT - Alle Ressourcen erlauben in robots.txt:
User-agent: Googlebot
Disallow:

User-agent: *
Disallow: /admin/
```

#### 10.2 Client-seitiges Rendering

```javascript
PROBLEMATISCH - Nur per JS gerendert:
document.getElementById('content').innerHTML = '<h1>Mein Titel</h1>';

BESSER - Server-seitiges Rendering:
<!-- Im HTML-Quellcode direkt -->
<h1>Mein Titel</h1>
```

#### 10.3 Lazy Loading

```html
GUT - Native Lazy Loading:
<img src="bild.jpg" loading="lazy" alt="Beschreibung">

GUT - Mit Intersection Observer:
<img data-src="bild.jpg" class="lazy" alt="Beschreibung">
```

### JavaScript SEO Checkliste

- [ ] Wichtige Inhalte im initialen HTML verfuegbar
- [ ] Meta-Tags (Title, Description) server-seitig gerendert
- [ ] Canonical-Links im HTML-Quellcode
- [ ] Strukturierte Daten (JSON-LD) im HTML
- [ ] Alle wichtigen Links als `<a href="...">`
- [ ] Keine `nofollow` fuer interne Links
- [ ] Sitemap enthaelt alle wichtigen URLs
- [ ] Mobile-Friendly Test bestehen


---

## 11. HTTP-Fehler und Netzwerkprobleme

### HTTP-Statuscodes

#### 2xx - Erfolgreich

| Code | Bedeutung | SEO-Relevanz |
|------|-----------|--------------|
| 200 | OK | Seite wird indexiert |
| 204 | No Content | Leere Seite, wird nicht indexiert |

#### 3xx - Umleitungen

| Code | Bedeutung | SEO-Relevanz |
|------|-----------|--------------|
| 301 | Moved Permanently | Link-Equity weitergegeben |
| 302 | Found (Temporary) | Link-Equity bleibt bei alter URL |
| 304 | Not Modified | Crawling effizienter |
| 307 | Temporary Redirect | Wie 302 |
| 308 | Permanent Redirect | Wie 301 |

#### 4xx - Client-Fehler

| Code | Bedeutung | SEO-Relevanz |
|------|-----------|--------------|
| 400 | Bad Request | Seite nicht erreichbar |
| 401 | Unauthorized | Geschuetzter Bereich |
| 403 | Forbidden | Blockiert, wird aus Index entfernt |
| 404 | Not Found | Seite entfernt, nach Zeit aus Index |
| 410 | Gone | Permanente Entfernung, schneller aus Index |
| 429 | Too Many Requests | Rate-Limit, Crawling verzoegert |

#### 5xx - Server-Fehler

| Code | Bedeutung | SEO-Relevanz |
|------|-----------|--------------|
| 500 | Internal Server Error | Crawling reduziert |
| 502 | Bad Gateway | Crawling reduziert |
| 503 | Service Unavailable | Temporaer, Google wartet |
| 504 | Gateway Timeout | Crawling reduziert |

### Soft 404

```
SOFT 404 (Problematisch):
- HTTP 200 OK
- Inhalt: "Seite nicht gefunden"

RICHTIGER 404:
- HTTP 404 Not Found
- Inhalt: "Seite nicht gefunden"
```

### 503 fuer Wartungsarbeiten

```http
HTTP/1.1 503 Service Unavailable
Retry-After: 3600
```

### DNS-Fehler

| Fehler | Bedeutung |
|--------|-----------|
| DNS_ERROR | DNS-Server nicht erreichbar |
| DNS_TIMED_OUT | DNS-Anfrage hat zu lange gedauert |
| DNS_LOOKUP_FAILED | Domain konnte nicht aufgeloest werden |

### Netzwerk-Fehler

| Fehler | Bedeutung |
|--------|-----------|
| CONNECTION_RESET | Verbindung unterbrochen |
| CONNECTION_REFUSED | Server lehnt Verbindung ab |
| TIMEOUT | Anfrage hat zu lange gedauert |
| TRUNCATED_RESPONSE | Antwort unvollstaendig |

---

## 12. Google-Crawler (User-Agents)

### Haupt-Crawler

| Name | User-Agent | Zweck |
|------|------------|-------|
| **Googlebot (Desktop)** | Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) | Desktop-Crawling |
| **Googlebot (Smartphone)** | Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X...) | Mobile-First-Index |
| **Googlebot-Image** | Googlebot-Image/1.0 | Bild-Crawling |
| **Googlebot-Video** | Googlebot-Video/1.0 | Video-Crawling |
| **Googlebot-News** | Googlebot-News | Google News |

### Spezial-Crawler

| Name | User-Agent | Zweck |
|------|------------|-------|
| **AdsBot-Google** | AdsBot-Google (+http://www.google.com/adsbot.html) | Google Ads Quality |
| **AdsBot-Google-Mobile** | AdsBot-Google-Mobile-Apps | App-Ads Quality |
| **Mediapartners-Google** | Mediapartners-Google | AdSense |
| **APIs-Google** | APIs-Google | APIs |
| **Feedfetcher-Google** | FeedFetcher-Google | RSS/Atom Feeds |

### Googlebot verifizieren

```bash
# Reverse DNS Lookup
host 66.249.66.1
# 1.66.249.66.in-addr.arpa domain name pointer crawl-66-249-66-1.googlebot.com.

# Forward DNS Lookup
host crawl-66-249-66-1.googlebot.com
# crawl-66-249-66-1.googlebot.com has address 66.249.66.1
```

### IP-Bereiche

Google crawlt hauptsaechlich von IP-Adressen aus den USA. Wenn eine Website Anfragen aus den USA blockiert, versucht Google ueber IP-Adressen in anderen Laendern zu crawlen.

> **Wichtig:** Blockiere Google-Crawler nicht auf IP-Basis! Die IPs aendern sich regelmaessig.

### Crawling-Frequenz verringern

In der Google Search Console kann die Crawl-Rate angepasst werden:
1. Einstellungen -> Crawling-Statistik
2. "Crawl-Rate anpassen"

Alternative: `Crawl-delay` in robots.txt (nicht von Google unterstuetzt):

```txt
User-agent: *
Crawl-delay: 10
```

---

## 13. Indexierungsprobleme beheben

### Haeufige Indexierungsprobleme

#### 13.1 "Gefunden - zurzeit nicht indexiert"

**Ursachen:**
- Crawl-Budget-Limit erreicht
- Seite als Low-Quality eingestuft
- Duplicate Content
- Kanonisierung auf andere Seite

**Loesungen:**
- Interne Verlinkung verbessern
- Content-Qualitaet erhoehen
- Canonical-Tags pruefen
- Sitemap einreichen

#### 13.2 "Entdeckt - zurzeit nicht indexiert"

**Ursachen:**
- robots.txt blockiert
- noindex-Tag vorhanden
- 4xx/5xx Fehler

**Loesungen:**
- robots.txt pruefen
- Meta-Tags pruefen
- Server-Fehler beheben

#### 13.3 "Soft 404"

**Ursachen:**
- HTTP 200 bei "Nicht gefunden"-Seiten
- Seite existiert aber hat keinen Inhalt

**Loesungen:**
- Richtigen 404-Status zurueckgeben
- Oder 410 fuer permanente Entfernung

#### 13.4 "Duplikat ohne vom Nutzer ausgewaehlten Kanonikalen"

**Ursachen:**
- Google hat andere URL als kanonisch gewaehlt
- Kein Canonical-Tag vorhanden

**Loesungen:**
- Canonical-Tag hinzufuegen
- URL-Parameter in Search Console konfigurieren

### Google um erneutes Crawlen bitten

1. **URL-Pruefung in Search Console:**
   - URL eingeben -> "Testen" -> "Indexierung beantragen"

2. **Sitemap neu einreichen:**
   - Sitemap entfernen -> Neu einreichen

3. **Interne Verlinkung:**
   - Von starken Seiten auf die neue Seite verlinken

### Seiten aus dem Index entfernen

#### Sofortige Entfernung (Search Console)

```
1. Search Console -> Entfernungen
2. "Neue Anfrage"
3. URL eingeben
4. Grund auswaehlen
```

#### Dauerhafte Entfernung

```html
<!-- noindex-Tag hinzufuegen -->
<meta name="robots" content="noindex">
```

Und/oder:

```txt
# robots.txt
User-agent: *
Disallow: /private/
```

#### 410 Gone fuer permanente Entfernung

```http
HTTP/1.1 410 Gone
```

### Indexabdeckung pruefen

In der Google Search Console:
- **Index -> Seiten**
- Filter: "Nicht indexiert"
- Fehler beheben


---

## Anhang: Schnellreferenz

### Meta-Tags Uebersicht

```html
<!-- Standard: Alles erlaubt -->
<meta name="robots" content="index, follow">

<!-- Nicht indexieren -->
<meta name="robots" content="noindex">

<!-- Nicht indexieren, Links nicht folgen -->
<meta name="robots" content="noindex, nofollow">

<!-- Snippet-Steuerung -->
<meta name="robots" content="nosnippet">
<meta name="robots" content="max-snippet:150">
<meta name="robots" content="max-image-preview:large">

<!-- Archivierung verhindern -->
<meta name="robots" content="noarchive">

<!-- Zeitliche Begrenzung -->
<meta name="robots" content="unavailable_after: 2024-12-31">
```

### robots.txt Template

```txt
# robots.txt fuer example.com

# Sitemap
Sitemap: https://www.example.com/sitemap.xml

# Googlebot-spezifische Regeln
User-agent: Googlebot
Disallow: /admin/
Disallow: /api/
Disallow: /internal/
Disallow: /*?sort=
Disallow: /*?filter=
Allow: /admin/public/

# Alle anderen Crawler
User-agent: *
Disallow: /admin/
Disallow: /api/
```

### XML-Sitemap Template

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://www.example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

### robots.txt vs. noindex Entscheidungsmatrix

```
                    | Crawling erlauben | Crawling blockieren
--------------------|-------------------|-------------------
Indexierung erlauben| -                 | robots.txt Allow
--------------------|-------------------|-------------------
Indexierung         | noindex Meta-Tag  | robots.txt
blockieren          | oder X-Robots-Tag | Disallow + noindex*
                    |                   | *nur wenn bereits
                    |                   | indexiert
```

### HTTP-Statuscode Uebersicht

| Code | Bedeutung | Aktion |
|------|-----------|--------|
| 200 | OK | Standard, Seite wird indexiert |
| 301 | Permanent Redirect | Link-Equity weitergeben |
| 302 | Temporary Redirect | Temporaere Umleitung |
| 404 | Not Found | Seite nicht gefunden |
| 410 | Gone | Permanent entfernt |
| 500 | Server Error | Server-Problem beheben |
| 503 | Service Unavailable | Wartungsmodus |

### Crawler User-Agents

| Crawler | User-Agent |
|---------|------------|
| Googlebot | Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html) |
| Googlebot Mobile | Mozilla/5.0 (Linux; Android 6.0.1; Nexus 5X Build/MMB29P)... |
| Googlebot-Image | Googlebot-Image/1.0 |
| AdsBot-Google | AdsBot-Google (+http://www.google.com/adsbot.html) |

---

## Ressourcen

- [Google Search Central](https://developers.google.com/search/docs/crawling-indexing?hl=de)
- [Google Search Console](https://search.google.com/search-console)
- [robots.txt Spezifikation](https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=de)
- [Sitemap-Protokoll](https://www.sitemaps.org/protocol.html)

---

## Zusammenfassung: Wichtigste Punkte

### DO's

- robots.txt verwenden fuer Crawling-Steuerung
- noindex Meta-Tag fuer Indexierungskontrolle
- Sitemaps erstellen und einreichen
- Canonical-Tags bei Duplicate Content
- 301-Redirects bei URL-Aenderungen
- HTTPS und mobile Optimierung

### DON'Ts

- robots.txt ALLEIN fuer Indexierungsblockierung
- Redirect-Ketten erstellen
- Soft 404s verwenden
- Google-Crawler auf IP-Basis blockieren
- Parameter ohne Canonical-Behandlung lassen
- JavaScript-kritische Inhalte ohne SSR

---

*Diese Dokumentation wurde basierend auf der offiziellen Google Search Central Dokumentation erstellt und enthaelt Best Practices fuer Crawling und Indexierung.*

**Quellen:**
- https://developers.google.com/search/docs/crawling-indexing?hl=de
- https://developers.google.com/search/docs/crawling-indexing/robots/intro?hl=de
- https://developers.google.com/search/docs/crawling-indexing/sitemaps/overview?hl=de
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls?hl=de
- https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag?hl=de
- https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget?hl=de
- https://developers.google.com/search/docs/crawling-indexing/url-structure?hl=de
- https://developers.google.com/search/docs/crawling-indexing/301-redirects?hl=de
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics?hl=de
- https://developers.google.com/search/docs/crawling-indexing/http-network-errors?hl=de
- https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers?hl=de
- https://developers.google.com/search/docs/crawling-indexing/block-indexing?hl=de

---

**Erstellt:** 2026  
**Letzte Aktualisierung:** Basierend auf Google Search Central Dokumentation (Deutsch)
