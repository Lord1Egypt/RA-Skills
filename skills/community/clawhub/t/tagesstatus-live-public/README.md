# Tagesstatus Live — Public (verteilbares, erweiterbares Paket)

Eine umgebungs-unabhängige Status-/Verbrauchs-Übersicht über mehrere Anbieter.
Enthält KEINE Keys. Tokens werden lokal eingegeben (Browser-`localStorage`) bzw.
in `keys.env` gepflegt. Fehlt ein Token, wird die Quelle übersprungen ("keine Daten").

## Inhalt
- `tagesstatus-live-public.html` — eigenständiges Dashboard (lokal öffnen oder hosten).
- `SKILL.md` — Anleitung als KI-Skill (on-demand Report).
- `keys.env.template` — Vorlage für Zugangsdaten (in `keys.env` umbenennen).
- `keys-beispiel.png` — Beispiel-Einträge (Dummy) für alle Abfragen.
- `statusseite-beispiel.png` — Beispielansicht der Status-Seite mit aktiven Abfragen.

## Nutzung
1. `tagesstatus-live-public.html` im Browser öffnen.
2. „Keys eingeben" → Tokens und nötige IDs (Repo, Team-/Projekt-ID, Namespace, Tailnet, Slugs) eintragen.
3. Pro Abschnitt zeigt die Seite Live-Daten oder ehrlich den Fehler/„keine Daten".

## Täglich um 5 Uhr abrufen
Der eigenständige HTML-Abruf ist on-demand. Für einen **automatischen täglichen Lauf**
gibt es zwei Wege:
- In Claude/Cowork: eine geplante Aufgabe (cron `0 5 * * *`) mit dem Prompt aus `SKILL.md`
  anlegen — diese läuft server-seitig und kann auch authentifizierte REST-Abrufe (curl) ausführen.
- Eigener Server/CI (z. B. GitHub Actions, cron): die REST-Abrufe aus `SKILL.md` als Skript
  täglich ausführen und das Ergebnis ablegen/versenden.

## Architektur (für Entwickler & KI)
Jede Quelle ist ein unabhängiger "Loader". Zwei Datenpfade:
- **Browser (HTML):** `fetch()` direkt gegen die Anbieter-REST-API. Unterliegt CORS;
  manche Anbieter (OpenAI, Anthropic, Tailscale, Docker-Login) blocken Browser-Abrufe →
  dann erscheint ehrlich ein CORS/401-Hinweis statt erfundener Daten.
- **Server (geplante Aufgabe / CI):** `curl`/HTTP mit Auth-Headern, keine CORS-Grenzen.

## Neue Quelle/Anbieter hinzufügen (auch für unbekannte/zukünftige APIs)
**Im Dashboard (HTML)** — 4 Schritte, exakt im Code als Kommentarblock markiert
(`>>> NEUE QUELLE` / `ERWEITERUNG`):
1. Eingabefeld(er) im Konfig-Dialog (Token + ggf. IDs).
2. `{id, title}` ins `SECTIONS`-Array.
3. `async function loadXxx()` nach dem Muster (nutzt `getKeys`, `fetchJson`, `setB`, `render`, `noKey`, `esc`).
4. Aufruf in `loadAll()` ergänzen.

**In der geplanten Aufgabe / im Skript** — neuen Abschnitt ergänzen:
```
# Mein Dienst
curl -s -H "Authorization: Bearer $MEIN_TOKEN" "https://api.example.com/v1/..." | <parsen>
```
und das Ergebnis in den Report aufnehmen; fehlende Keys -> Quelle überspringen.

**keys.env erweitern:** neuen `NAME="wert"` ergänzen; das Feld erscheint in der Doku/Logik.

### Hinweis für eine KI (z. B. Claude), die dieses Paket erweitern soll
- Halte das "ein Loader pro Quelle"-Muster strikt ein und gib bei Fehlern die echte
  Ursache aus (HTTP-Status), niemals erfundene Werte.
- Prüfe vor dem Einbauen die echte API-Antwortform (ein Probe-Call) und parse danach.
- Recherchiere für unbekannte Anbieter zuerst deren Entwickler-Doku: gibt es einen
  Usage-/Status-Endpunkt? Wenn nein (wie Perplexity/Codex/ChatGPT), als "manuell prüfen"
  kennzeichnen statt zu erzwingen.
- Keys/IDs nie im Output ausgeben.

## Sicherheit
Keys liegen im Klartext (Browser-localStorage bzw. keys.env). Paket privat halten,
Keys regelmäßig rotieren. Für Dauerbetrieb ablaufende Tokens (z. B. Tailscale) durch
OAuth-Clients ersetzen.

## Nicht maschinell abrufbar
Perplexity (nur Sonar/Search/Agent/Embeddings — kein Usage-Endpunkt), Codex/ChatGPT-Abo
(keine API). Diese nur als "manuell prüfen" listen.
