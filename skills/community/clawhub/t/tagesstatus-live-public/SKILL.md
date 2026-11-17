---
name: tagesstatus-live-public
description: >-
  Öffentliche, umgebungs-unabhängige Version des Tagesstatus-Reports. KEINE
  eingebetteten Keys, NICHT mit einer Umgebung verbunden. Tokens werden beim Lauf
  abgefragt bzw. aus keys.env gelesen; fehlt ein Key, wird die Quelle übersprungen
  ("keine Daten"). Quellen: GitHub, Vercel, Docker Hub, OpenRouter, OpenAI,
  Anthropic/Claude, Tailscale, ClawHub (plus Perplexity/Codex nur als Hinweis).
  Wichtig: Je nach Quelle sind neben dem Token zusätzlich Identifikatoren nötig –
  Anmeldename/Namespace (Docker), Repo owner/repo (GitHub), Team- und Projekt-ID
  (Vercel), Tailnet (Tailscale), Skill-Slugs (ClawHub); manche Logins erfolgen mit
  Benutzername/E-Mail + Token (z. B. Docker-Login).
---

# Tagesstatus Live — Public

Generischer Statusreport ohne fest hinterlegte Zugangsdaten.
1. Werte aus `keys.env` lesen (Tokens UND Identifikatoren wie Namespace/IDs/Repo/Tailnet); fehlt etwas, Nutzer fragen.
2. Leerer Pflichtwert → Quelle überspringen, "kein Token/keine ID — keine Daten" (nichts erfinden).
3. Ausgabe: TL;DR + Abschnitt je Quelle + Fehlerprotokoll. Keys nie ausgeben.

## Quellen, benötigte Angaben & Endpunkte
- GitHub — `GH_REPO` (owner/repo, Pflicht), `GH_TOKEN` (optional für privat/Codespaces): pulls?state=open, branches, commits/{branch}/check-runs, user/codespaces.
- Vercel — `VERCEL_TOKEN` + `VERCEL_PROJECT_ID` (+ opt. `VERCEL_TEAM_ID`): GET https://api.vercel.com/v6/deployments?projectId={proj}&limit=10[&teamId={team}] → state (ERROR hervorheben), Commit, Branch.
- Docker Hub — `DOCKER_NAMESPACE` (= Anmeldename) + `DOCKER_PAT`: POST https://hub.docker.com/v2/users/login {username:NAMESPACE, password:PAT} → .token; dann GET https://hub.docker.com/v2/repositories/{namespace}/?page_size=50 mit Bearer JWT → name, is_private, pull_count. Pulls summieren.
- OpenRouter — `OPENROUTER_API_KEY`: /v1/key, /v1/credits.
- OpenAI — `OPENAI_ADMIN_KEY` (Admin-Key): /v1/organization/costs?start_time=<unix-30d>.
- Anthropic/Claude — `CLAUDE_ADMIN_KEY` (x-api-key + anthropic-version 2023-06-01): cost_report, usage_report/messages.
- Tailscale — `TAILSCALE_TOKEN` + `TAILSCALE_TAILNET`: /api/v2/tailnet/{tailnet}/devices (Token max. 90 Tage; sonst OAuth-Client).
- ClawHub — kein Token, `CLAWHUB_SLUGS`: je Slug https://clawhub.ai/api/v1/skills/{slug} → Version, Downloads, Scan.
- Perplexity / Codex / ChatGPT-Abo: kein Usage-API-Endpunkt — nur "manuell prüfen".

## keys.env (Vorlage)
Nur gewünschte Werte eintragen. Leere Pflichtfelder = Quelle übersprungen. Privat halten, Keys rotieren.

## Dashboard-HTML
Eine fertige, eigenständige Dashboard-HTML (gleiche Quellen, Eingabe von Tokens UND IDs im Browser, localStorage) wird separat als Datei `tagesstatus-live-public.html` bereitgestellt — zum lokalen Öffnen oder Hosten.

## Beispiel-Konfiguration (Bild)
Siehe `keys-beispiel.png` — zeigt Dummy-Beispieleinträge für alle möglichen Abfragen
(GitHub, Vercel, Docker Hub, OpenRouter, OpenAI, Anthropic/Claude, Tailscale, ClawHub)
sowie den Hinweis, dass Perplexity/Codex/ChatGPT keinen Usage-Endpunkt haben.

## Beispiel-Screenshot der Status-Seite
Siehe `statusseite-beispiel.png` — zeigt die Live-Seite mit aktiven Abfragen (Slack,
Linear, Notion, GitHub, Vercel), einer deaktivierten Quelle (Zoom, per Schalter aus)
und dem Hinweis auf den automatischen Lauf täglich um 05:00 Uhr bzw. "Report jetzt erzeugen".

## Für fremde Nutzer / KI
Siehe `README.md` — Architektur und Schritt-für-Schritt-Anleitung, wie eine KI (z. B. Claude)
neue/unbekannte Quellen und Anbieter ergänzt (Dashboard-Loader-Muster + Server-/CI-Muster).
