---
name: reports-creator
description: Automated report generation for self-reflection and system analysis. Creates daily, weekly, and monthly reports from logs, databases, and system metrics.
---

# Reports Creator

Automatisierte Berichtserstellung für Selbstreflexion und Systemanalyse.

## Berichtstypen

| Typ | Intervall | Inhalt | Ziel |
|-----|-----------|--------|------|
| **Daily** | Täglich | Logs, Fehler, Änderungen | Operatives Monitoring |
| **Weekly** | Wöchentlich | Trends, Statistiken, Performance | Wochenreview |
| **Monthly** | Monatlich | Archivierung, Langzeitanalyse | Strategieplanung |
| **Ad-hoc** | On-Demand | Spezialanalysen | Troubleshooting |

## Datenquellen

### Lokale Datenbanken
- **docs.db** - Dokumentationsänderungen
- **tree.db** - Dateisystem-Änderungen
- **logs.db** - System- und Node-Logs

### Log-Dateien
- `logs/db-maintainer/` - DB-Wartung
- `logs/log-collector/` - Log-Sammlung
- `memory/*.md` - Tagesprotokolle

### System-Metriken
- Node-Status (online/offline)
- VPN-Verbindungsqualität
- Backup-Status

## Berichtstruktur

```markdown
# Bericht 2026-04-18 - Tageszusammenfassung

## Übersicht
- **Zeitraum:** 2026-04-18 00:00 - 23:59
- **Nodes:** 5 total, 3 online, 2 offline
- **Neue Dokumente:** 12
- **Geänderte Dateien:** 47

## System-Events
| Zeit | Event | Node | Status |
|------|-------|------|--------|
| 03:00 | DB-Backup | node1 | ✅ OK |
| 06:00 | Health-Check | node1 | ✅ OK |
| 12:14 | Config-Fehler | node1 | ⚠️ Behoben |

## Fehler & Warnungen
- [x] Config: Ungültiger Key "contextWindow" - behoben
- [ ] Node 3: fail2ban blockiert Node 1 IP (offen)

## Neue Skills
- log-collector@1.0.0 veröffentlicht

## Empfohlene Aktionen
1. Node 3 fail2ban prüfen
2. VPN-Tunnel Node 2 testen
```

## Automatisierung

### Täglicher Bericht (6:00 Uhr)
```bash
0 6 * * * python3 skills/reports-creator/scripts/daily_report.py
```

### Wöchentlicher Bericht (Sonntag 8:00)
```bash
0 8 * * 0 python3 skills/reports-creator/scripts/weekly_report.py
```

## Nutzung

### Manueller Report
```bash
openclaw reports create --type daily --date 2026-04-18
openclaw reports create --type weekly --week 16
openclaw reports create --type monthly --month 4
```

### Auto-Generierung
```bash
# Bericht für gestern
reports-creator --yesterday

# Wochenbericht
reports-creator --last-week
```

## Integration

- **db-maintainer:** Nutzt DB-Änderungen für Reports
- **log-collector:** Integriert Node-Logs
- **workspace-db:** Greift auf Dokumentations-Index zu

## Ausgabe

```
reports/
├── 2026/
│   ├── 04/
│   │   ├── 2026-04-18-daily.md
│   │   ├── 2026-04-18-weekly.md
│   │   └── 2026-04-monthly.md
```

## Konfiguration

```json
{
  "reports-creator": {
    "enabled": true,
    "output_dir": "reports/",
    "retention_days": 90,
    "auto_generate": ["daily", "weekly"],
    "email_on_error": true
  }
}
```
