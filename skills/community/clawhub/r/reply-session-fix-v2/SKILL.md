---
name: reply-session-fix-43ytnoa-xzc0tc
description: "Diagnose und dauerhaft fixen von 'reply session initialization conflicted' Errors in OpenClaw via 3-Layer-Setup (Client-Heal JS, Server Watchdog, Retry-Patch)."
tags: [openclaw, gateway, sessions, debugging, watchdog, reliability]
version: 0.1.0
author: raumkommer
license: MIT
---

# Reply-Session-Conflict Fix

Diagnose und dauerhafte Behebung von `reply session initialization conflicted for <session-key> (after N retries)` in OpenClaw.

## Wann anwenden
- User meldet: `Error: reply session initialization conflicted for agent:main:dashboard:<uuid> (after 8 retries)`
- Watchdog-Log zeigt wiederholte `HEAL_FAILED`
- Nach Gateway-Restart mitten in Turn → Sessions "transcript tail not resumable"

## Root-Cause (auswendig)
1. Gateway wird mitten in laufendem Turn neu gestartet (Config-Reload, Crash, systemctl restart).
2. Die Session-Snapshot-Revision im In-Memory-Store passt nicht mehr zum persistierten Transcript.
3. `commitReplySessionInitialization()` in `dist/get-reply-*.js` bekommt `committed.ok === false`.
4. Retry-Loop (8x mit Backoff) findet die Session immer noch stale → wirft finalen Error.
5. Browser-Tab hat die UUID lokal in `localStorage` und schickt sie beim nächsten Send WEITER → gleicher Error, weil der Server die Session zwar löschen kann, der Client aber die tote UUID re-benutzt.

Deswegen brauchen wir **drei Layer** — nur einer reicht nicht.

## Layer 1: Client-Side Auto-Heal (die entscheidende Ebene)

**Warum:** Ohne diesen Layer sendet der Browser-Tab immer wieder die tote UUID. Server-side löschen hilft nur einmal.

**Datei:** `/var/www/openclaw-downloads/reply-conflict-heal.js`

**Was es tut:** Fetch + XHR responses abfangen, bei 2+ Konflikt-Errors in 30s → `localStorage`-Session-Keys clearen + `window.location.reload()`. Cooldown: 1 Reload pro 5 Min (verhindert Reload-Loops).

**Injection über Nginx sub_filter** in `/etc/nginx/sites-enabled/openclaw.raumkommander.at` im HTTPS-`server`-Block (Port 443, NICHT im Port-80-Redirect-Block!):

```nginx
location / {
    proxy_pass http://127.0.0.1:18789;
    ...
    sub_filter_once off;
    sub_filter_types text/html;
    sub_filter '</body>' '<script src="https://openclaw.raumkommander.at/reply-conflict-heal.js?v=1"></script></body>';
}

location = /reply-conflict-heal.js {
    alias /var/www/openclaw-downloads/reply-conflict-heal.js;
    default_type application/javascript;
    add_header Cache-Control "no-store, no-cache, must-revalidate";
}
```

Nach jeder Änderung: `nginx -t && systemctl reload nginx` und Verify per `curl -sSI https://openclaw.raumkommander.at/reply-conflict-heal.js` → muss `200` liefern.

**Version-Bump:** Wenn du das Script änderst, `?v=1` → `?v=2` in der sub_filter-Zeile hochzählen (Cache-Bust).

## Layer 2: Server-Side Watchdog (Backup)

**Datei:** `/root/.openclaw/workspace/scripts/reply-session-conflict-watchdog.sh`
**Timer:** `/etc/systemd/system/openclaw-reply-session-watchdog.timer`

**Aggressive Einstellungen (aktuell, 2026-07-04 v2):**
- Timer: `OnUnitActiveSec=60s` (alle 60 Sekunden)
- `WINDOW_MIN=5` (letzte 5 Min journalctl)
- `THRESHOLD=1` (1 Konflikt reicht schon)
- Cooldown pro Key: 60s

**Was er tut:** Liest `journalctl --user -u openclaw-gateway` letzte 5 Min, findet `reply session initialization conflicted for <key>`, ruft für `dashboard:*` / `subagent:*` Keys `POST http://127.0.0.1:18791/api/openclaw/sessions/delete` auf. **Fasst `agent:main:main` NIEMALS an** (hard rule im Script).

**Log:** `memory/reply-session-heal.log` (AUTO_HEAL / HEALED / HEAL_FAILED Einträge)

**Alarm nur bei HEAL_FAILED:** Wenn stats-server nicht antwortet, wird `memory/reply-session-ALARM.md` geschrieben. Sonst silent.

**Test manuell:** `bash /root/.openclaw/workspace/scripts/reply-session-conflict-watchdog.sh`

## Layer 3: Retry-Patch im Gateway-Code

**Reapply-Script:** `/root/.openclaw/workspace/scripts/reapply-reply-session-retry-patch.sh`

Muss nach jedem OpenClaw-Update laufen (idempotent, überspringt wenn schon gepatcht). Der Patch erhöht Retries von 1 auf 8 mit exponential Backoff (25ms → 400ms max, mit Jitter) in `dist/get-reply-*.js`.

**Wichtige Konstanten im gepatchten Code:**
```js
const REPLY_SESSION_INIT_MAX_RETRIES = 8;
const REPLY_SESSION_INIT_BACKOFF_BASE_MS = 25;
const REPLY_SESSION_INIT_BACKOFF_MAX_MS = 400;
```

Verify: `grep REPLY_SESSION_INIT_MAX_RETRIES /home/linuxbrew/.linuxbrew/lib/node_modules/openclaw/dist/get-reply-*.js`

## Manueller Sofort-Fix (wenn User gerade jammert)

```bash
# 1. Zombie-Session serverseitig loskicken (nur EINE Session, nie main!)
curl -sS -X POST http://127.0.0.1:18791/api/openclaw/sessions/delete \
  -H "Content-Type: application/json" \
  -d '{"key":"agent:main:dashboard:<UUID>","deleteTranscript":true}'

# 2. User muss den Tab reloaden (F5) — wenn Layer 1 nicht aktiv ist,
#    kommt sonst der gleiche Error wieder, weil localStorage die tote UUID hält.
```

**Merke:** `agent:main:dashboard:*` / `agent:main:subagent:*` sind Browser-Tabs, safe zum Löschen. `agent:main:main` ist die Haupt-Session — NIEMALS anfassen.

## Diagnose-Kommandos

```bash
# Aktuelle Konflikte
XDG_RUNTIME_DIR=/run/user/0 journalctl --user -u openclaw-gateway --since "10 min ago" | grep "initialization conflict"

# Heal-Log
tail -30 /root/.openclaw/workspace/memory/reply-session-heal.log

# Watchdog-Status
systemctl status openclaw-reply-session-watchdog.timer

# Verify alle 3 Layer aktiv
grep 'reply-conflict-heal.js' /etc/nginx/sites-enabled/openclaw.raumkommander.at
systemctl is-active openclaw-reply-session-watchdog.timer
grep REPLY_SESSION_INIT_MAX_RETRIES /home/linuxbrew/.linuxbrew/lib/node_modules/openclaw/dist/get-reply-*.js
```

## Fallstricke

- **Nginx sub_filter im falschen server-Block:** Wenn `location = /reply-conflict-heal.js` im HTTP-Port-80-Block statt HTTPS-Block landet → 404. Immer im HTTPS/443-Block platzieren.
- **DeepSeek als Fallback:** `huggingface/deepseek-ai/DeepSeek-V3.1` liefert häufig empty-response → triggert retry-loop, der die Session in Konflikt schießt. DeepSeek deshalb IMMER als letzten Fallback in `agents.list[main].model.fallbacks` und `agents.defaults.model.fallbacks`. Die Config-Paths sind `protected`, direkt in `/root/.openclaw/openclaw.json` editieren, nicht via `gateway config.patch`.
- **stats-server:** Läuft als `/root/.openclaw/workspace/stats-server.py` (nicht `scripts/stats-server.py`, das ist ein alter Stub). Der Delete-Endpoint proxied per `openclaw gateway call sessions.delete` — braucht Gateway-Auth aus openclaw.json.
- **Watchdog-Timer:** Wenn er ausgeschaltet ist, greift Layer 2 nicht. Verify mit `systemctl is-active openclaw-reply-session-watchdog.timer`.

## Files-Referenz

| Zweck | Pfad |
|---|---|
| Client-Heal JS | `/var/www/openclaw-downloads/reply-conflict-heal.js` |
| Nginx-Config | `/etc/nginx/sites-enabled/openclaw.raumkommander.at` |
| Watchdog-Script | `/root/.openclaw/workspace/scripts/reply-session-conflict-watchdog.sh` |
| Watchdog-Timer | `/etc/systemd/system/openclaw-reply-session-watchdog.timer` |
| Retry-Patch-Reapply | `/root/.openclaw/workspace/scripts/reapply-reply-session-retry-patch.sh` |
| Gepatchtes Gateway-JS | `/home/linuxbrew/.linuxbrew/lib/node_modules/openclaw/dist/get-reply-*.js` |
| Heal-Log | `/root/.openclaw/workspace/memory/reply-session-heal.log` |
| ALARM (nur wenn Auto-Heal fehlschlägt) | `/root/.openclaw/workspace/memory/reply-session-ALARM.md` |
| Session-Store | `/root/.openclaw/agents/main/sessions/` |
| stats-server (aktiver) | `/root/.openclaw/workspace/stats-server.py` |

## Nach OpenClaw-Update PFLICHT

```bash
bash /root/.openclaw/workspace/scripts/reapply-reply-session-retry-patch.sh
XDG_RUNTIME_DIR=/run/user/0 systemctl --user restart openclaw-gateway
```

Client-Heal und Watchdog überleben Updates automatisch (Nginx-Config und systemd-Timer werden von OpenClaw-Update nicht angetastet).
