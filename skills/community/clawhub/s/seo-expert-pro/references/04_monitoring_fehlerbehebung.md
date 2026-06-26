# Google SEO: Monitoring und Fehlerbehebung

> **Quelle:** Google Search Central Documentation | Letzte Aktualisierung: 2025

---

## Inhaltsverzeichnis

1. [Überblick](#1-überblick)
2. [Google Search Console - Erste Schritte](#2-google-search-console---erste-schritte)
3. [Index Coverage Report](#3-index-coverage-report)
4. [URL Inspection Tool](#4-url-inspection-tool)
5. [Traffic-Einbrüche debuggen](#5-traffic-einbrüche-debuggen)
6. [Manuelle Maßnahmen (Manual Actions)](#6-manuelle-maßnahmen-manual-actions)
7. [Sicherheitsprobleme](#7-sicherheitsprobleme)
8. [Core Web Vitals Report](#8-core-web-vitals-report)
9. [Rich Results Tests](#9-rich-results-tests)
10. [Mobile-Friendly Test](#10-mobile-friendly-test)
11. [Crawling-Fehler beheben](#11-crawling-fehler-beheben)
12. [Wichtige Tools im Überblick](#12-wichtige-tools-im-überblick)
13. [Häufige Fehler und Lösungen](#13-häufige-fehler-und-lösungen)

---

## 1. Überblick

### Was ist das Monitoring und Troubleshooting?

Das Monitoring und die Fehlerbehebung in der SEO umfassen alle Aktivitäten, die darauf abzielen:

- Die Sichtbarkeit der Website in Google Search zu überwachen
- Technische Probleme frühzeitig zu erkennen
- Crawling- und Indexierungsfehler zu beheben
- Sicherheitsprobleme zu identifizieren und zu lösen
- Die Benutzererfahrung (Page Experience) zu optimieren

### Wichtige Prinzipien

> **Hinweis:** Es ist nicht notwendig, täglich in die Search Console zu schauen. Wenn Google neue Probleme auf der Website findet, werden E-Mail-Benachrichtigungen verschickt.

**Empfohlene Überprüfungsfrequenz:**
- Routinemäßig: ca. einmal pro Monat
- Bei Content-Änderungen: unmittelbar nach Veröffentlichung
- Bei Traffic-Einbrüchen: sofort

---

## 2. Google Search Console - Erste Schritte

### Schritt-für-Schritt Einrichtung

```
Schritt 1: Website-Besitz verifizieren
├── HTML-Datei-Upload
├── HTML-Tag (Meta-Tag)
├── Google Analytics
├── Google Tag Manager
└── Domain-Name-Provider (DNS)

Schritt 2: Index Coverage Report prüfen
├── Überblick über alle indizierten Seiten
├── Fehler identifizieren
└── Warnungen beheben

Schritt 3: Sitemap einreichen (optional)
├── XML-Sitemap erstellen
├── In GSC einreichen
└── Status überwachen

Schritt 4: Performance überwachen
├── Search Performance Report
├── Traffic-Trends analysieren
└── Einbrüche debuggen
```

### Berichte für Webentwickler

| Bericht | Zweck | Priorität |
|---------|-------|-----------|
| Index Coverage | Seitenweite Indexierungsprobleme | Hoch |
| URL Inspection | Seitenspezifische Debugging | Hoch |
| Security Issues | Sicherheitswarnungen | Kritisch |
| Core Web Vitals | Page Experience Metriken | Hoch |

### Berichte für SEO-Spezialisten und Marketer

| Bericht | Zweck | Priorität |
|---------|-------|-----------|
| Manual Actions | Manuelle Google-Maßnahmen | Kritisch |
| Removals | Temporäre Entfernung von URLs | Mittel |
| Change of Address | Domain-Migrationen | Mittel |
| Rich Results Status | Strukturierte Daten-Probleme | Hoch |

---

## 3. Index Coverage Report

### Übersicht

Der Index Coverage Report zeigt:
- Welche Seiten erfolgreich indiziert wurden
- Seiten mit Fehlern
- Warnungen und ausgeschlossene Seiten
- Impression-Daten zur Einordnung der Probleme

### Status-Kategorien

```
┌─────────────────────────────────────────────────────────────┐
│                    INDEX COVERAGE STATUS                    │
├─────────────────────────────────────────────────────────────┤
│ 🟢 Error (Fehler)                                           │
│    └── Seiten konnten nicht indiziert werden               │
│                                                              │
│ 🟡 Warning (Warnung)                                        │
│    └── Seiten sind indiziert, haben aber Probleme          │
│                                                              │
│ ⚪ Excluded (Ausgeschlossen)                                │
│    └── Seiten wurden absichtlich oder aus technischen      │
│        Gründen nicht indiziert                             │
│                                                              │
│ 🟢 Valid (Gültig)                                           │
│    └── Seiten sind erfolgreich indiziert                   │
└─────────────────────────────────────────────────────────────┘
```

### Häufige Fehler und Lösungen

#### 3.1 Serverfehler (5xx)

**Problem:** Der Server antwortet mit einem 5xx-Statuscode

**Ursachen:**
- Server-Überlastung
- Fehlerhafte Server-Konfiguration
- Datenbank-Verbindungsprobleme

**Lösung:**
```
1. Server-Logs prüfen
2. Server-Kapazität überprüfen
3. Datenbank-Verbindungen testen
4. Hosting-Provider kontaktieren falls nötig
```

#### 3.2 Soft 404

**Problem:** Seite zeigt "Nicht gefunden"-Inhalt, aber liefert 200-Statuscode

**Lösung:**
```html
<!-- Falsch: -->
<div>Seite nicht gefunden</div>
<!-- Liefert HTTP 200 -->

<!-- Richtig: -->
<!-- Liefert HTTP 404 -->
```

**Schritte:**
1. Überprüfen, ob die Seite tatsächlich existieren sollte
2. Falls nicht: 404-Statuscode implementieren
3. Falls ja: Korrekten Inhalt bereitstellen

#### 3.3 "Submitted URL not found (404)"

**Problem:** URL in Sitemap führt zu 404-Fehler

**Lösung:**
```
1. URL korrigieren oder aus Sitemap entfernen
2. Falls Seite verschoben: 301-Weiterleitung einrichten
3. Sitemap neu einreichen
```

#### 3.4 "Crawled - currently not indexed"

**Problem:** Seite wurde gecrawlt, aber nicht indiziert

**Mögliche Ursachen:**
- Content-Qualität zu gering
- Duplicate Content
- Kanonisierungsprobleme
- Crawl-Budget-Probleme

**Lösung:**
```
1. Content-Qualität verbessern
2. Prüfen auf Duplicate Content
3. Canonical-Tags überprüfen
4. Interne Verlinkung stärken
```

#### 3.5 "Discovered - currently not indexed"

**Problem:** Google kennt die URL, hat sie aber noch nicht gecrawlt

**Lösung:**
```
1. URL Inspection Tool nutzen für manuelle Indexierung
2. Interne Verlinkung verbessern
3. XML-Sitemap aktualisieren
4. Qualität der Seite verbessern
```

---

## 4. URL Inspection Tool

### Funktionen im Überblick

Das URL Inspection Tool bietet:

1. **Presence on Google** - Status der URL in Google Search
2. **View Crawled Page** - HTML, das Google gecrawlt hat
3. **Request Indexing** - Manuelle Indexierungsanfrage
4. **Coverage** - Detaillierte Crawling- und Indexierungsinformationen
5. **Enhancements** - Mobile Usability und strukturierte Daten
6. **Test Live URL** - Live-Test der aktuellen Seite

### Presence Status

| Status | Bedeutung | Aktion |
|--------|-----------|--------|
| "URL is on Google" | Seite ist indiziert | Keine Aktion nötig |
| "URL is not on Google" | Seite ist nicht indiziert | Problem beheben, Indexierung anfordern |
| "URL is on Google, but has issues" | Indiziert mit Problemen | Warnungen beheben |
| "URL is an alternate version" | AMP oder mobile Version | Keine Aktion nötig |

### Coverage-Abschnitte

#### Discovery (Entdeckung)

```
Sitemaps:              [Liste der Sitemaps mit dieser URL]
Referring page:        [Seite, die auf diese URL verlinkt]
Indexing allowed?:     [Yes / No / N/A]
```

#### Crawl (Crawling)

```
Crawl:                 [Success / Failed]
Crawl date:            [Datum des letzten Crawls]
Googlebot:             [Smartphone / Desktop]
```

#### Indexing (Indexierung)

```
User-declared canonical:    [Selbst definierter Canonical]
Google-selected canonical:  [Von Google gewählter Canonical]
```

### Test Live URL

> **Wichtig:** Der Live-Test zeigt den aktuellen Status der Seite, während die Hauptansicht den letzten Google-Crawl zeigt.

**Verfügbarkeits-Status:**
- "URL is available to Google" - Seite kann gecrawlt werden
- "URL is available to Google, but has issues" - Crawling möglich, aber mit Problemen
- "URL is not available to Google" - Crawling blockiert

### Indexierung anfordern

```
Schritte:
1. URL in das Inspektionsfeld eingeben
2. "Request Indexing" klicken
3. Live-Test wird durchgeführt
4. Bei Erfolg: URL wird in Warteschlange aufgenommen

Limit: ca. 10-12 Anfragen pro Tag pro Property
```

---

## 5. Traffic-Einbrüche debuggen

### Systematischer Ansatz

```
Schritt 1: Problem identifizieren
├── Welche Seiten sind betroffen?
├── Welche Länder/Regionen?
├── Welche Gerätetypen?
└── Welche Queries?

Schritt 2: Zeitliche Einordnung
├── Wann begann der Einbruch?
├── Gab es technische Änderungen?
├── Gab es Content-Updates?
└── Google Algorithmus-Update?

Schritt 3: Mögliche Ursachen prüfen
├── Technische Probleme?
├── Manuelle Maßnahmen?
├── Sicherheitsprobleme?
├── Content-Qualität?
└── Wettbewerbsveränderungen?

Schritt 4: Behebung und Monitoring
├── Probleme beheben
├── Fixes validieren
├── Wiederherstellung überwachen
└── Dokumentation erstellen
```

### Search Performance Report analysieren

**Metriken:**
- **Impressions** - Wie oft wurde die Seite angezeigt?
- **Clicks** - Wie oft wurde geklickt?
- **CTR** - Click-Through-Rate (Clicks / Impressions)
- **Position** - Durchschnittliche Ranking-Position

**Filter-Optionen:**
```
├── Queries (Suchbegriffe)
├── Pages (Seiten)
├── Countries (Länder)
├── Devices (Geräte)
├── Search Appearance (Suchdarstellung)
└── Dates (Zeitraum)
```

### Vergleichsmöglichkeiten

| Vergleich | Nutzen |
|-----------|--------|
| Vorher/Nachher | Einbruch quantifizieren |
| Jahr über Jahr | Saisonalität ausschließen |
| Desktop vs Mobile | Gerätespezifische Probleme |
| Brand vs Non-Brand | Sichtbarkeitsverlust einordnen |

---

## 6. Manuelle Maßnahmen (Manual Actions)

### Was sind Manuelle Maßnahmen?

Manuelle Maßnahmen werden von Google-Mitarbeitern verhängt, wenn eine Website gegen die Google-Richtlinien verstößt.

> **⚠️ WARNUNG:** Manuelle Maßnahmen können dazu führen, dass die gesamte Website oder Teile davon nicht mehr in den Google-Suchergebnissen angezeigt werden.

### Arten von Manuellen Maßnahmen

#### 6.1 Link-basierte Maßnahmen

| Maßnahme | Beschreibung |
|----------|--------------|
| Unnatural links to your site | Kauf oder Manipulation von Backlinks |
| Unnatural links from your site | Verkauf von Links oder linkbasierte Manipulation |

**Behebung:**
```
1. Problem-Links identifizieren
2. Links entfernen oder disavow
3. Dokumentation erstellen
4. Reconsideration Request einreichen
```

#### 6.2 Content-basierte Maßnahmen

| Maßnahme | Beschreibung |
|----------|--------------|
| Thin content | Zu wenig oder wertloser Content |
| Auto-generated content | Automatisch generierter Content |
| Scraped content | Geklauter/duplizierter Content |

**Behebung:**
```
1. Problem-Seiten identifizieren
2. Content verbessern oder entfernen
3. Qualitätsrichtlinien befolgen
4. Reconsideration Request einreichen
```

#### 6.3 Technische Manipulation

| Maßnahme | Beschreibung |
|----------|--------------|
| Cloaking | Unterschiedlicher Content für Google und User |
| Sneaky redirects | Täuschende Weiterleitungen |
| Hidden text | Versteckter Text/Links |

#### 6.4 Spam

| Maßnahme | Beschreibung |
|----------|--------------|
| Pure spam | Aggressive Spam-Techniken |
| User-generated spam | Spam in Kommentaren/Foren |
| Keyword stuffing | Übermäßige Keyword-Nutzung |

### Reconsideration Request (Wiederaufnahmeantrag)

```
Voraussetzungen:
✓ Alle Probleme wurden vollständig behoben
✓ Dokumentation der Behebung vorhanden
✓ Sicherstellung, dass Probleme nicht wieder auftreten

Prozess:
1. Search Console → Security & Manual Actions
2. Manual Actions Report öffnen
3. "Request a review" klicken
4. Detaillierte Beschreibung der Behebung
5. Beweise für die Korrektur anfügen

Wartezeit: Tage bis Wochen
```

---

## 7. Sicherheitsprobleme

### Überblick

Der Security Issues Report zeigt Warnungen, wenn Google feststellt, dass eine Website:
- Gehackt wurde
- Malware verteilt
- Phishing betreibt
- Andere schädliche Aktivitäten ausführt

### Arten von Sicherheitsproblemen

```
🔴 Hacked Content (Gehackter Content)
   ├── Injected content (Eingeschleuster Content)
   ├── Added pages (Hinzugefügte Seiten)
   └── Redirects (Weiterleitungen zu bösartigen Seiten)

🔴 Malware & Unwanted Software
   ├── Malware-Downloads
   ├── Trojaner
   └── Unerwünschte Software

🔴 Social Engineering
   ├── Phishing-Seiten
   └── Deceptive content (Täuschender Content)
```

### Sofortmaßnahmen bei einem Hack

```
NOTFALL-PLAN: WEBSITE GEHACKT

Stunde 0-1: Kontainment
├── Website offline nehmen (falls nötig)
├── Backup der infizierten Version erstellen
├── Passwörter ändern (alle!)
└── Hosting-Provider informieren

Stunde 1-4: Analyse
├── Server-Logs analysieren
├── Malware-Scans durchführen
├── Angriffsvektor identifizieren
└── Betroffene Dateien/Seiten dokumentieren

Stunde 4-8: Bereinigung
├── Malware entfernen
├── Backdoors schließen
├── Verwundbare Plugins/Themes aktualisieren
└── Sicherheitslücken patchen

Stunde 8+: Wiederherstellung
├── Website wieder online
├── Google Search Console prüfen
├── Sicherheits-Review beantragen
└── Monitoring einrichten
```

### Bereinigungsschritte

#### Schritt 1: Backup erstellen
```bash
# Bevor Änderungen vorgenommen werden!
mysqldump -u username -p database > backup.sql
tar -czf files_backup.tar.gz /var/www/html/
```

#### Schritt 2: Malware identifizieren
```
Tools:
- Google Safe Browsing
- Sucuri SiteCheck
- Wordfence (für WordPress)
- ClamAV (Server-seitig)
```

#### Schritt 3: Dateien bereinigen
```bash
# Vergleich mit sauberer Version
diff -qr /current-site/ /clean-backup/

# Suche nach verdächtigem Code
grep -r "eval(base64_decode" /var/www/html/
grep -r "preg_replace.*\/e" /var/www/html/
```

#### Schritt 4: Datenbank bereinigen
```sql
-- Beispiel: Suche nach Spam in Posts
SELECT * FROM wp_posts WHERE post_content LIKE '%viagra%';

-- Beispiel: Ungewöhnliche Admin-User
SELECT * FROM wp_users WHERE user_registered > '2024-01-01';
```

### Google Review Request

```
Nach der Bereinigung:

1. Search Console öffnen
2. Security Issues Tab
3. "I have fixed these issues" bestätigen
4. "Request a review" klicken
5. Detaillierte Beschreibung der Behebung:
   - Was war das Problem?
   - Wie wurde es behoben?
   - Welche Maßnahmen verhindern Wiederholung?

⚠️ WICHTIG: Nur eine Review-Anfrage alle 30 Tage möglich!
```

### Präventive Maßnahmen

```
SICHERHEITS-CHECKLISTE

□ Regelmäßige Backups (automatisieren)
□ CMS und Plugins aktuell halten
□ Starke Passwörter + 2FA
□ Web Application Firewall (WAF)
□ File Integrity Monitoring
□ Regelmäßige Sicherheits-Scans
□ Begrenzte Login-Versuche
□ Nicht verwendete Themes/Plugins löschen
□ Server-Hardening
□ SSL-Zertifikat (HTTPS)
```

---

## 8. Core Web Vitals Report

### Überblick

Core Web Vitals sind eine Reihe von Metriken, die Google verwendet, um die Benutzererfahrung auf einer Website zu bewerten.

> **Hinweis:** Core Web Vitals sind ein Ranking-Faktor in Google Search.

### Die drei Core Web Vitals

```
┌─────────────────────────────────────────────────────────────┐
│                  CORE WEB VITALS METRIKEN                  │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🎯 LCP - Largest Contentful Paint                          │
│     → Ladegeschwindigkeit des Hauptinhalts                  │
│     → Ziel: < 2,5 Sekunden                                  │
│     → Schlecht: > 4,0 Sekunden                              │
│                                                             │
│  ⚡ INP - Interaction to Next Paint                          │
│     → Reaktionszeit auf Benutzerinteraktionen               │
│     → Ziel: < 200 Millisekunden                             │
│     → Schlecht: > 500 Millisekunden                         │
│     → Seit März 2024 FID ersetzt                           │
│                                                             │
│  📐 CLS - Cumulative Layout Shift                           │
│     → Visuelle Stabilität                                   │
│     → Ziel: < 0,1                                           │
│     → Schlecht: > 0,25                                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Bewertungsskala

| Metrik | Gut | Verbesserung nötig | Schlecht |
|--------|-----|-------------------|----------|
| LCP | ≤ 2,5s | 2,5s - 4,0s | > 4,0s |
| INP | ≤ 200ms | 200ms - 500ms | > 500ms |
| CLS | ≤ 0,1 | 0,1 - 0,25 | > 0,25 |

### Report-Struktur

Der Report ist in zwei Abschnitte unterteilt:
- **Mobile** - Mobile-Performance
- **Desktop** - Desktop-Performance

### Häufige Probleme und Lösungen

#### 8.1 LCP-Probleme

**Ursachen:**
- Langsame Server-Antwortzeit
- Render-blocking JavaScript/CSS
- Langsam ladende Bilder
- Unoptimierte Schriftarten

**Lösungen:**
```html
<!-- Bilder optimieren -->
<img src="image.webp" width="800" height="600" alt="...">

<!-- Preload für kritische Ressourcen -->
<link rel="preload" as="image" href="hero-image.webp">

<!-- Critical CSS inline -->
<style>/* kritisches CSS */</style>
```

#### 8.2 CLS-Probleme

**Ursachen:**
- Bilder ohne Dimensionen
- Dynamisch eingefügter Content
- Web Fonts ohne Fallback
- Spät ladende Werbebanner

**Lösungen:**
```html
<!-- Bilder mit Dimensionen -->
<img src="image.jpg" width="800" height="600">

<!-- Aspect Ratio für responsive Bilder -->
<div style="aspect-ratio: 16/9;">
  <img src="image.jpg" style="width: 100%; height: auto;">
</div>

<!-- Font Display -->
<style>
@font-face {
  font-family: 'MyFont';
  src: url('font.woff2') format('woff2');
  font-display: swap;
}
</style>
```

#### 8.3 INP-Probleme

**Ursachen:**
- Lange JavaScript-Ausführung
- Komplexe DOM-Strukturen
- Drittanbieter-Skripte
- Hauptthread-Blockierung

**Lösungen:**
```javascript
// Code in kleinere Tasks aufteilen
await scheduler.yield();

// Oder: setTimeout für nicht-kritische Operationen
setTimeout(() => {
  // Nicht-kritische Arbeit
}, 0);

// Event Handler optimieren
element.addEventListener('click', () => {
  // Sofortiges visuelles Feedback
  updateUI();
  
  // Dann: Schwere Arbeit
  requestIdleCallback(() => {
    heavyComputation();
  });
});
```

### Validierung von Fixes

```
1. Optimierungen implementieren
2. PageSpeed Insights testen
3. Live URL Test in GSC durchführen
4. "Validate Fix" in GSC klicken
5. 28 Tage warten (Daten aus CrUX)
6. Ergebnis überprüfen
```

---

## 9. Rich Results Tests

### Übersicht

Rich Results sind erweiterte Suchergebnisse, die durch strukturierte Daten (Schema Markup) ermöglicht werden.

### Rich Results Test Tool

**URL:** https://search.google.com/test/rich-results

**Funktionen:**
- Test von strukturierten Daten
- Vorschau der Rich Results
- Fehler- und Warnungsanzeige
- Live-Test und Code-Test

### Unterstützte Rich Result Typen

```
┌────────────────────────────────────────────────────────────┐
│              RICH RESULT TYPEN (Auswahl)                  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  📰 Article             │  🛒 Product                     │
│  📚 Book                │  ❓ FAQ                         │
│  🍞 Breadcrumb          │  📖 How-to                      │
│  🎠 Carousel            │  💼 Job Posting                 │
│  🎓 Course              │  🎬 Video                       │
│  ⭐ Review Snippet      │  🔍 Sitelinks Searchbox         │
│  📅 Event               │  🍽️ Recipe                       │
│  ✅ Fact Check          │  🏢 Local Business              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### Test durchführen

```
Schritt 1: URL oder Code eingeben
├── Website-URL einfügen
└── Oder: Code-Snippet einfügen

Schritt 2: Test starten
├── Google ruft die Seite ab
├── Strukturierte Daten analysieren
└── Ergebnisse anzeigen

Schritt 3: Ergebnisse interpretieren
├── Erkannte strukturierte Daten-Elemente
├── Fehler (müssen behoben werden)
└── Warnungen (sollten behoben werden)

Schritt 4: Preview ansehen
├── Wie sieht das Rich Result aus?
└── Mobile und Desktop-Vorschau
```

### Häufige Fehler

| Fehler | Beschreibung | Lösung |
|--------|--------------|--------|
| Missing field | Pflichtfeld fehlt | Erforderliche Eigenschaft hinzufügen |
| Invalid value | Wert entspricht nicht dem erwarteten Format | Format korrigieren |
| Incorrect value type | Falscher Datentyp | Z.B. Text statt Number |
| Unspecified type | Typ nicht angegeben | @type definieren |

### Best Practices

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Artikel-Titel",
  "author": {
    "@type": "Person",
    "name": "Autor Name"
  },
  "datePublished": "2024-01-15",
  "image": "https://example.com/image.jpg"
}
```

> **Wichtig:** Der Content auf der Seite muss mit den strukturierten Daten übereinstimmen. Andernfalls kann es als Spam markiert werden.

---

## 10. Mobile-Friendly Test

### Überblick

Der Mobile-Friendly Test überprüft, ob eine Seite für mobile Geräte optimiert ist.

> **Hinweis:** Google verwendet Mobile-First Indexing für die meisten Websites.

### Test durchführen

**URL:** https://search.google.com/test/mobile-friendly

```
Eingabe: URL oder Code-Snippet

Ergebnis:
✅ Page is mobile-friendly
   └── Keine Aktion nötig

❌ Page is not mobile-friendly
   └── Spezifische Probleme werden aufgelistet
```

### Häufige Probleme

| Problem | Beschreibung | Lösung |
|---------|--------------|--------|
| Viewport not set | Meta viewport fehlt | `<meta name="viewport" content="width=device-width, initial-scale=1">` |
| Text too small | Text ist zu klein | Mindestens 16px für Body-Text |
| Content wider than screen | Horizontales Scrollen | Responsive Design implementieren |
| Clickable elements too close | Elemente zu nah beieinander | Mindestens 48x48px Touch-Targets |
| Incompatible plugins | Nicht unterstützte Plugins | Flash etc. entfernen |

### Best Practices für Mobile

```html
<!-- Viewport Meta-Tag -->
<meta name="viewport" content="width=device-width, initial-scale=1">

<!-- Responsive Images -->
<img src="image.jpg" style="max-width: 100%; height: auto;">

<!-- Touch-Targets -->
<button style="min-width: 48px; min-height: 48px;">
  Klick mich
</button>
```

### Alternative: URL Inspection Tool

Der Mobile-Friendly Test und das URL Inspection Tool verwenden dieselbe Core-Technologie. Unterschiede:

| Feature | Mobile-Friendly Test | URL Inspection |
|---------|---------------------|----------------|
| Zugang | Ohne GSC möglich | GSC-Zugang nötig |
| Vergleich | Live-Version nur | Letzter Crawl vs Live |
| Details | Einfach | Ausführlich |

---

## 11. Crawling-Fehler beheben

### Systematische Fehlerbehebung

```
CRAWLING-FEHLER-DEBUGGING

Phase 1: Identifizierung
├── Index Coverage Report prüfen
├── Server-Logs analysieren
└── Crawl Stats Report (falls verfügbar)

Phase 2: Kategorisierung
├── Server-Fehler (5xx)
├── Client-Fehler (4xx)
├── Weiterleitungsprobleme (3xx)
└── Zugangsprobleme (robots.txt)

Phase 3: Behebung
├── Einzelne Probleme lösen
├── Systematische Fehler beheben
└── Tests durchführen

Phase 4: Validierung
├── Live URL Test
├── Indexierung anfordern
└── Monitoring
```

### robots.txt Probleme

```
Häufige Fehler:

❌ Unbeabsichtigtes Blockieren:
   Disallow: /
   → Blockiert die gesamte Website

❌ Falsche Syntax:
   Disallow: /folder
   → Sollte sein: Disallow: /folder/

❌ Render-kritische Ressourcen blockiert:
   Disallow: /css/
   Disallow: /js/
   → Kann Rendering verhindern

✅ Korrekte Verwendung:
   User-agent: *
   Allow: /
   Disallow: /admin/
   Disallow: /private/
   
   Sitemap: https://example.com/sitemap.xml
```

### Meta Robots Probleme

```html
<!-- Falsche Verwendung: -->
<meta name="robots" content="noindex, nofollow">
<!-- Sollte nur noindex sein, wenn Links gecrawlt werden sollen -->

<!-- Richtig: -->
<meta name="robots" content="noindex">
<!-- Google kann Links folgen, indexiert die Seite aber nicht -->

<!-- Für nicht-HTML-Dateien (HTTP Header): -->
X-Robots-Tag: noindex
```

### Canonical-Probleme

```html
<!-- Falsche Selbstreferenz: -->
<link rel="canonical" href="https://example.com/wrong-url">

<!-- Richtig: -->
<link rel="canonical" href="https://example.com/correct-page">

<!-- Bei Paginierung: -->
<link rel="canonical" href="https://example.com/category">
<link rel="next" href="https://example.com/category?page=2">
```

### Redirect-Ketten

```
Problem:
/page-a → /page-b → /page-c → /final-page

Lösung:
/page-a → /final-page
/page-b → /final-page
/page-c → /final-page

Status-Code: 301 (Permanent)
```

---

## 12. Wichtige Tools im Überblick

### Google-Tools

| Tool | URL | Zweck |
|------|-----|-------|
| Search Console | search.google.com/search-console | Haupt-Monitoring-Tool |
| Rich Results Test | search.google.com/test/rich-results | Strukturierte Daten testen |
| Mobile-Friendly Test | search.google.com/test/mobile-friendly | Mobile Optimierung testen |
| PageSpeed Insights | pagespeed.web.dev | Geschwindigkeit analysieren |
| Safe Browsing | transparencyreport.google.com/safe-browsing/search | Sicherheitsstatus prüfen |
| Schema Validator | validator.schema.org | Schema-Markup validieren |

### Browser-Extensions

```
Web Vitals Extension
├── Chrome Web Store
├── Zeigt LCP, INP, CLS in Echtzeit
└── Hilft beim Debugging

Lighthouse
├── In Chrome DevTools integriert
├── Umfassende Performance-Analyse
└── SEO-, Accessibility-, Best Practices-Checks
```

### Kommandozeilen-Tools

```bash
# cURL für Header-Checks
curl -I https://example.com/page

# wget für Crawling-Simulation
wget --spider -r -nd -nv -o crawl.log https://example.com

# grep für Log-Analyse
grep "Googlebot" access.log | awk '{print $7}' | sort | uniq -c | sort -rn
```

---

## 13. Häufige Fehler und Lösungen

### Fehler-Quick-Reference

| Fehler | Ursache | Lösung |
|--------|---------|--------|
| 404 in Sitemap | URL existiert nicht | Sitemap aktualisieren oder Seite erstellen |
| Soft 404 | Seite gibt 200 statt 404 | Korrekten Statuscode implementieren |
| Duplicate without canonical | Duplizierter Content | Canonical-Tag setzen |
| Crawled - not indexed | Qualitätsproblem | Content verbessern |
| Discovered - not indexed | Crawl-Budget | Verlinkung verbessern |
| Server Error (5xx) | Server-Problem | Hosting/Server prüfen |
| Redirect error | Redirect-Problem | Redirect-Ketten beheben |
| Blocked by robots.txt | robots.txt blockiert | robots.txt korrigieren |
| Blocked by meta noindex | noindex-Tag | Tag entfernen falls gewünscht |
| Not followed | Nicht gefolgt | Prüfen ob Seite existiert |

### Checkliste: Monatliches Monitoring

```
MONATLICHE SEO-CHECKLISTE

□ Search Console
  □ Index Coverage Report prüfen
  □ Core Web Vitals überprüfen
  □ Security Issues checken
  □ Manual Actions prüfen
  □ Performance-Trends analysieren

□ Technisch
  □ Crawl-Fehler beheben
  □ Sitemap auf Fehler prüfen
  □ robots.txt validieren
  □ Interne Links checken

□ Content
  □ Neue Seiten indexieren lassen
  □ Veraltete Seiten entfernen
  □ Canonical-Probleme prüfen

□ Performance
  □ Core Web Vitals überwachen
  □ Mobile Usability prüfen
  □ Seitengeschwindigkeit testen
```

### Checkliste: Traffic-Einbruch

```
AKTIONEN BEI TRAFFIC-EINBRUCH

Sofort:
□ Search Console auf Warnungen prüfen
□ Manuelle Maßnahmen checken
□ Sicherheitsprobleme ausschließen

Kurzfristig (Tag 1-3):
□ Index Coverage auf Fehler prüfen
□ Technische Probleme identifizieren
□ Robots.txt/Sitemap validieren
□ Wettbewerber analysieren

Mittelfristig (Woche 1-2):
□ Algorithmus-Update prüfen
□ Content-Qualität bewerten
□ Backlink-Profil analysieren
□ Recovery-Plan erstellen
```

---

## Zusammenfassung

### Die wichtigsten Monitoring-Aktivitäten

1. **Google Search Console regelmäßig prüfen**
   - Index Coverage für technische Probleme
   - Core Web Vitals für Performance
   - Security Issues für Sicherheit
   - Manual Actions für Penalties

2. **Proaktives Monitoring einrichten**
   - E-Mail-Benachrichtigungen aktivieren
   - Regelmäßige Audits durchführen
   - Alerts für kritische Fehler

3. **Schnelle Reaktion bei Problemen**
   - Systematisches Debugging
   - Dokumentation der Änderungen
   - Validierung von Fixes

4. **Prävention vor Kur**
   - Sicherheitsmaßnahmen implementieren
   - Regelmäßige Backups
   - Qualitätsrichtlinien befolgen

---

## Weiterführende Ressourcen

- Google Search Central: https://developers.google.com/search
- Search Console Hilfe: https://support.google.com/webmasters
- PageSpeed Insights: https://pagespeed.web.dev
- Schema.org: https://schema.org

---

> **Hinweis:** Diese Dokumentation basiert auf der offiziellen Google Search Central Dokumentation und wurde für LLM-Optimierung strukturiert. Für die aktuellsten Informationen immer die offizielle Dokumentation konsultieren.
