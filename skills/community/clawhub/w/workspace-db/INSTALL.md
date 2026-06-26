# Installation

## Voraussetzungen

- Python 3.8+
- SQLite3
- OpenClaw Gateway

## Schritt 1: Skill installieren

```bash
clawhub install workspace-db
```

## Schritt 2: Datenbanken initialisieren

```bash
cd ~/.openclaw/workspace

# docs.db erstellen
python3 scripts/db_manager.py

# Erste Befüllung
python3 scripts/update_docs_db.py
```

## Schritt 3: Optional - Maintainer installieren

Für automatische Updates:
```bash
clawhub install db-maintainer
python3 skills/db-maintainer/scripts/install_cron.py
```

## Verifizierung

```bash
# Datenbank-Größe prüfen
ls -lh db/*.db

# Dokumente zählen
sqlite3 db/docs.db "SELECT COUNT(*) FROM documents"

# Export testen
ls -lh export_*.csv
```

## Troubleshooting

**Problem**: `docs.db` nicht gefunden
**Lösung**: `python3 scripts/db_manager.py` ausführen

**Problem**: Keine Exporte
**Lösung**: `python3 scripts/update_docs_db.py` ausführen
