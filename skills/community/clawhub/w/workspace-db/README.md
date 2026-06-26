# Workspace Database Manager

SQLite-basierte Dokumentations-Verwaltung für OpenClaw-Workspaces.

## Features

- **docs.db**: Indexiert alle Dokumentationen (256+ Dokumente)
- **Automatische Updates**: Via db-maintainer Sub-Agent
- **Exporte**: CSV und JSON für alle Tabellen
- **Query-Schnittstelle**: SQL-Abfragen für komplexe Suchen

## Datenbank-Schema

### documents Tabelle
```sql
CREATE TABLE documents (
    id INTEGER PRIMARY KEY,
    name TEXT,           -- Dateiname
    path TEXT,           -- Relativer Pfad
    category TEXT,       -- Kategorie (main, websearch, mcp, ...)
    description TEXT,    -- Kurzbeschreibung
    type TEXT,           -- doc, config, guide, symlink
    has_symlink BOOLEAN, -- Hat Symlink im Root?
    symlink_path TEXT,   -- Ziel des Symlinks
    last_update TEXT     -- Letzte Änderung
);
```

### skills Tabelle
```sql
CREATE TABLE skills (
    id INTEGER PRIMARY KEY,
    name TEXT,
    version TEXT,
    status TEXT,         -- installed, local, published
    description TEXT,
    path TEXT
);
```

### symlinks Tabelle
```sql
CREATE TABLE symlinks (
    id INTEGER PRIMARY KEY,
    name TEXT,
    target TEXT,
    source_path TEXT,
    description TEXT
);
```

## Verwendung

```bash
# Abfrage aller WebSearch-Dokumentationen
sqlite3 db/docs.db "SELECT * FROM documents WHERE category='websearch'"

# Suche nach Skills
sqlite3 db/docs.db "SELECT * FROM skills WHERE status='installed'"

# Export nach CSV
python3 scripts/export_csv.py documents
```

## Integration

Dieser Skill arbeitet zusammen mit:
- **db-maintainer**: Automatische Updates (30min Intervall)
- **workspace-db-scripts**: Export-Tools

## Installation

```bash
clawhub install workspace-db
```

## Lizenz

Open Source - für OpenClaw-Workspaces
