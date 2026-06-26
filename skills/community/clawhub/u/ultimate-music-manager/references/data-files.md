# Data Files Reference

Every JSON artifact the Sonic Phoenix pipeline produces or consumes. All files
live under `DATA_DIR` (default: `<MUSIC_ROOT>/.data/`). This directory is safe
to delete between runs — everything in it can be regenerated.

---

## Phase 1 — Extraction and Identification

### `metadata_catalog.json`

| Field | Value |
| ----- | ----- |
| Written by | `01A_extract_metadata.py` |
| Read by | `01B_shazam_identify.py`, `05I_finalize_catalog.py` |
| Config key | `config.METADATA_CATALOG` |

**Schema:**

```json
{
  "tagged_files": [
    {
      "path": "<absolute path>",
      "metadata": {
        "artist": "Adele",
        "title": "Hello",
        "album": "25"
      }
    }
  ],
  "untagged_files": [
    {
      "path": "<absolute path>",
      "metadata": {}
    }
  ]
}
```

Files are split based on whether Mutagen found valid ID3/FLAC/MP4 tags.

---

### `shazam_final_results.json`

| Field | Value |
| ----- | ----- |
| Written by | `01D_shazam_all_files.py` |
| Read by | `05I_finalize_catalog.py` |
| Config key | `config.SHAZAM_RESULTS` |

**Schema:**

```json
{
  "<absolute path>": {
    "success": true,
    "artist": "Adele",
    "title": "Hello",
    "album": "25",
    "genre": "Pop",
    "label": "XL Recordings",
    "shazam_url": "https://..."
  }
}
```

Keyed by absolute file path. Failed identifications have `"success": false`.
The file is append-safe — re-running 01D skips paths already present.

---

### `shazam_hash_results.json`

| Field | Value |
| ----- | ----- |
| Written by | `01C_shazam_by_hash.py` |
| Read by | `02D_organize_music.py`, `03A_consolidate_by_artist.py`, `03E_scan_remnants.py`, `04E_art_decorator.py`, `05A_repair_json.py`, `05B_sanitize_results_json.py`, `05G_final_migration.py`, `05H_final_vacuum.py` |
| Config key | `config.SHAZAM_HASH_RESULTS` |

**Schema:**

```json
{
  "<sha256 hex>": {
    "success": true,
    "artist": "Adele",
    "title": "Hello",
    "album": "25"
  }
}
```

Same shape as `shazam_final_results.json` but keyed by SHA-256 hash instead
of file path. This lets one Shazam match propagate to all byte-identical copies.

---

## Phase 2 — Cataloguing and Deduplication

### `catalog.json`

| Field | Value |
| ----- | ----- |
| Written by | `02A_catalog_music.py` |
| Read by | `01C_shazam_by_hash.py`, `02B_analyze_catalog.py`, `02C_organize_files.py`, `02D_organize_music.py`, `04E_art_decorator.py`, `05G_final_migration.py` |
| Config key | `config.HASH_CATALOG` |

**Schema:**

```json
{
  "files": [
    {
      "path": "<absolute path>",
      "name": "Hello.mp3",
      "size": 8429312,
      "suffix": ".mp3",
      "hash": "<sha256 hex>"
    }
  ],
  "hashes": {
    "<sha256 hex>": ["<path1>", "<path2>"]
  }
}
```

Any hash with more than one path in its list is a duplicate group.

---

## Phase 3 — Consolidation

### `consolidation_log.json`

| Field | Value |
| ----- | ----- |
| Written by | `03A_consolidate_by_artist.py` |
| Read by | (audit trail — not consumed by other scripts) |
| Config key | `config.DATA_DIR / "consolidation_log.json"` |

**Schema:**

```json
[
  {
    "timestamp": "2025-01-15T14:30:00",
    "action": "MOVE",
    "source": "<path>",
    "destination": "<path>",
    "rationale": "Shazam match",
    "confidence": "High"
  }
]
```

Actions: `MOVE`, `PROPOSED_MOVE` (dry run), `SKIP`, `FLAGGED`.

---

### `mismatch_report.json`

| Field | Value |
| ----- | ----- |
| Written by | `03A_consolidate_by_artist.py` |
| Read by | (audit trail — not consumed by other scripts) |
| Config key | `config.MISMATCH_REPORT` |

**Schema:**

```json
[
  {
    "file": "English/Eminem feat Dr Dre/Track.mp3",
    "current_folder": "Eminem feat Dr Dre",
    "proposed_artist": "Dr. Dre",
    "rationale": "Shazam match"
  }
]
```

Contains files where the proposed artist failed the safe-consolidation check
(would have moved the file to an unrelated artist). Review manually.

---

## Phase 4 — Enrichment

### `enrichment_report.json`

| Field | Value |
| ----- | ----- |
| Written by | `04I_polish_and_enrich_v6.py` |
| Read by | (audit trail) |
| Config key | `config.ENRICHMENT_REPORT` |

Contains per-file enrichment outcomes: which fields were updated, whether
artwork was embedded, whether lyrics were fetched, and any errors encountered.

---

## Phase 5 — Finalization

### `final_catalog.json`

| Field | Value |
| ----- | ----- |
| Written by | `05I_finalize_catalog.py` |
| Read by | `02C_organize_files.py`, `06D_spotify_sync_engine.py`, `06E_spotify_discovery_sync.py` |
| Config key | `config.FINAL_CATALOG` |

**Schema:**

```json
{
  "<absolute path>": {
    "artist": "Adele",
    "title": "Hello",
    "album": "25",
    "language": "English",
    "source": "ID3"
  }
}
```

Source values: `"ID3"` (tags were clean), `"Shazam"` (acoustic match),
`"Filename_Fallback"` (last resort — stem of the filename).

This is the read-only master snapshot. Downstream phases (especially Phase 6)
read from this file, not from live file scans.

---

## Phase 6 — Spotify Sync

### `.spotify_token_cache`

| Field | Value |
| ----- | ----- |
| Written by | `06B_spotify_setup.py` (via `spotify_auth.py`) |
| Read by | All `06*` scripts (via `spotify_auth.py`) |
| Config key | `config.SPOTIFY_TOKEN_CACHE` |

Spotipy's cached OAuth token. Not JSON you'd read manually — managed
automatically by the `spotipy.oauth2.SpotifyOAuth` class.

---

### `spotify_sync_state.json`

| Field | Value |
| ----- | ----- |
| Written by | `06D_spotify_sync_engine.py` |
| Read by | `06D_spotify_sync_engine.py` (resumable) |
| Config key | `config.SPOTIFY_SYNC_STATE` |

Tracks which files have been synced to which Spotify playlists. Allows the
script to resume after interruption without re-querying the full library.

---

### `discovery_sync_state.json`

| Field | Value |
| ----- | ----- |
| Written by | `06E_spotify_discovery_sync.py` |
| Read by | `06E_spotify_discovery_sync.py` (resumable) |
| Config key | `config.SPOTIFY_DISCOVERY_STATE` |

Tracks which artists have been cross-referenced with Spotify listening history
and which genre playlists have been created.

---

### `spotify_backups/`

| Field | Value |
| ----- | ----- |
| Written by | `06C_spotify_backup.py` |
| Read by | (manual rollback) |
| Config key | `config.SPOTIFY_BACKUP_DIR` |

Contains one JSON file per Spotify playlist (full track list) plus a
`manifest.json` listing all backed-up playlists. Created as a safety net
before any mutation scripts (06D, 06E) touch Spotify.

---

## Data Flow Diagram

```
01A ──► metadata_catalog.json ──────────────────────────► 05I
                                                           │
01D ──► shazam_final_results.json ─────────────────────► 05I
                                                           │
01C ──► shazam_hash_results.json ──► 02D, 03A, 04E        │
                                                           │
02A ──► catalog.json ──────────────► 01C, 02D, 04E        │
                                                           │
03A ──► consolidation_log.json (audit)                     │
03A ──► mismatch_report.json (audit)                       │
                                                           │
04I ──► enrichment_report.json (audit)                     │
                                                           │
05I ──► final_catalog.json ────────► 06D, 06E             ▼
                                                    master snapshot
06B ──► .spotify_token_cache ──────► 06C, 06D, 06E
06C ──► spotify_backups/ (rollback)
06D ──► spotify_sync_state.json (resume)
06E ──► discovery_sync_state.json (resume)
```
