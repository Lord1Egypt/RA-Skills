---
name: ultimate-music-manager
description: "Organises a messy local music library into a clean Language/Artist/Album hierarchy using acoustic fingerprinting, deduplication, metadata enrichment, and optional Spotify sync. Use when: (1) User wants to sort or clean up a folder of audio files, (2) User has untagged or badly-tagged MP3/FLAC/M4A files, (3) User wants to identify unknown songs via Shazam fingerprinting, (4) User wants to deduplicate audio files by content hash, (5) User wants to enrich metadata with iTunes artwork and LrcLib lyrics, (6) User wants to sync their local library to Spotify playlists."
metadata:
  openclaw:
    requires:
      env:
        - MUSIC_ROOT
      optionalEnv:
        - SPOTIFY_CLIENT_ID
        - SPOTIFY_CLIENT_SECRET
        - SPOTIFY_REDIRECT_URI
        - SHAZAM_CONCURRENCY
        - ITUNES_COUNTRIES
        - SORTED_ROOT
        - DATA_DIR
        - FFMPEG_BIN
      bins:
        - python3.12
        - git
      optionalBins:
        - ffmpeg
    primaryEnv: MUSIC_ROOT
    source: https://github.com/drajb/sonic-phoenix
---

# Sonic Phoenix

A multi-phase pipeline that transforms a disorganised local music collection into a pristine, fully-tagged library sorted by `<Language>/<Artist>/<Album>/<Artist> - <Title>.<ext>`. Works with any language — Hindi, English, Japanese, Spanish, or anything else your collection contains.

The pipeline never deletes audio files. Suspected duplicates are moved to a staging folder for manual review.

## Quick Reference

| Situation | Action |
|-----------|--------|
| First-time setup | [Environment Setup](#environment-setup) |
| Sort a messy music folder | Run Phases 1-5 in order |
| Identify unknown songs | Run Phase 1 (Shazam fingerprinting) |
| Find and remove duplicates | Run Phase 2 (SHA-256 catalog) |
| Fix bad/missing ID3 tags | Run Phase 4 (iTunes enrichment) |
| Sync library to Spotify | Run Phase 6 (requires Spotify app credentials) |
| Add language classification hints | Create hint files in `config/language_hints/` |
| Check current configuration | `python config.py` |

## Environment Setup

### Prerequisites

- **Python 3.12** (required — `shazamio-core` only ships wheels for 3.10-3.12)
- **Git** (to clone the repo)
- **FFmpeg** (optional — only needed if your collection contains non-MP3 formats like FLAC, OGG, or WMA that Shazam needs to decode)

### Installation

```bash
# Clone into your music folder (recommended) or anywhere else
cd /path/to/your/music
git clone https://github.com/drajb/sonic-phoenix.git
cd sonic-phoenix

# Create virtual environment with Python 3.12
python3.12 -m venv .venv

# Activate
source .venv/bin/activate          # macOS / Linux
# .venv\Scripts\activate           # Windows PowerShell
# .venv\Scripts\activate.bat       # Windows cmd

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the repo root (copy from `.env.example`):

```dotenv
# REQUIRED — absolute path to the root of your music collection
MUSIC_ROOT=/path/to/your/music

# OPTIONAL — override any of these defaults:
# SORTED_ROOT=/path/to/your/music/Sorted
# DATA_DIR=/path/to/your/music/.data
# SHAZAM_CONCURRENCY=20
# ITUNES_COUNTRIES=US,GB
```

Verify configuration:

```bash
python config.py
```

This prints all resolved paths and confirms `MUSIC_ROOT` exists.

### Directory Layout After Setup

```
<MUSIC_ROOT>/
├── sonic-phoenix/           # This repo
│   ├── config.py            # Central configuration (single source of truth)
│   ├── .env                 # Your local overrides (gitignored)
│   ├── 01A_extract_metadata.py
│   ├── 01D_shazam_all_files.py
│   ├── ...
│   └── config/
│       └── language_hints/  # Optional language classification overrides
│           └── examples/    # Templates to copy and customise
├── Sorted/                  # Pipeline output (auto-created)
│   ├── English/
│   │   ├── Adele/
│   │   │   └── 25/
│   │   │       └── Adele - Hello.mp3
│   │   └── ...
│   ├── Hindi/
│   └── <any language langdetect finds>/
├── .data/                   # Machine-generated JSON artifacts (auto-created)
│   ├── metadata_catalog.json
│   ├── shazam_final_results.json
│   ├── catalog.json
│   ├── final_catalog.json
│   └── ...
└── <your unsorted audio files>
```

## The Pipeline

### Happy Path (Minimum Viable Run)

For a quick, effective sort of your library, run these scripts in order:

```bash
python 01A_extract_metadata.py     # Extract ID3/FLAC tags
python 01D_shazam_all_files.py     # Acoustic fingerprint every file via Shazam
python 02A_catalog_music.py        # SHA-256 hash catalog + duplicate detection
python 02D_organize_music.py         # Sort into Language/Artist/Album hierarchy
python 03A_consolidate_by_artist.py --dry-run   # Preview artist folder merges
python 03A_consolidate_by_artist.py              # Execute merges
python 03D_titanium_resort.py      # Final structural enforcement pass
python 04I_polish_and_enrich_v6.py # Enrich tags via iTunes + embed artwork
python 05I_finalize_catalog.py     # Lock the master catalog
```

Each script is resumable — if interrupted, re-run it and it picks up where it left off.

### Phase 1: Extraction and Identification

| Script | Status | Purpose |
|--------|--------|---------|
| `01A_extract_metadata.py` | CANONICAL | Reads existing ID3/FLAC/MP4 tags via Mutagen. Splits files into `tagged_files` and `untagged_files` in `metadata_catalog.json`. |
| `01B_shazam_identify.py` | UTILITY | Shazam-identify only the untagged files from 01A. |
| `01C_shazam_by_hash.py` | UTILITY | Propagate a single Shazam match to all byte-identical copies (via hash groups from Phase 2). |
| `01D_shazam_all_files.py` | CANONICAL | Force every audio file through Shazam regardless of existing tags. Use this when tags are unreliable. 20-way concurrent by default. |
| `01E_test_matching.py` | UTILITY | Spot-check a handful of files against Shazam to verify the pipeline is working. |

**When to use 01B vs 01D:** If your collection has clean tags on most files, use 01A then 01B (faster — only fingerprints untagged files). If tags are unreliable (generic names like "Track 01", meaningless album fields, garbled metadata), use 01D to fingerprint everything and cross-validate against the acoustic results.

**Shazam rate limiting:** If you see HTTP 429 errors, lower `SHAZAM_CONCURRENCY` in your `.env` (try 5-10).

### Phase 2: Cataloguing and Deduplication

| Script | Status | Purpose |
|--------|--------|---------|
| `02A_catalog_music.py` | CANONICAL | SHA-256 hash every audio file. Writes `catalog.json` with duplicate groups. |
| `02B_analyze_catalog.py` | UTILITY | Analyses the hash catalog and prints duplicate statistics. Read-only reporter. |
| `02C_organize_files.py` | UTILITY | Organises files using the hash catalog and final catalog. Alternative to 02D. |
| `02D_organize_music.py` | CANONICAL | The main sorter. Reads Shazam results and moves files into `<SORTED_ROOT>/<Language>/<Artist>/<Album>/`. |

### Phase 3: Consolidation and Structural Cleanup

| Script | Status | Purpose |
|--------|--------|---------|
| `03A_consolidate_by_artist.py` | UTILITY | Merge fragmented artist folders (e.g. "Akon feat Eminem" into "Akon"). Supports `--dry-run`. |
| `03D_titanium_resort.py` | CANONICAL | Final structural enforcer. Any file not matching `Language/Artist/Album/` gets re-sorted. |
| `03F_reorganize_binary.py` | UTILITY | Resolve near-duplicate files via binary comparison. |

### Phase 4: Metadata Enrichment

| Script | Status | Purpose |
|--------|--------|---------|
| `04I_polish_and_enrich_v6.py` | CANONICAL | The single enrichment entry point. Cleans junk from tags (quality markers, description artifacts, miscellaneous noise), enriches via iTunes Search API (artist, title, album, release date, artwork), fetches synchronized lyrics from LrcLib, embeds cover art into ID3 tags. |

**iTunes rate limiting:** The script rotates queries across country codes (default: US, GB). Add more via `ITUNES_COUNTRIES=US,GB,AU,CA` in `.env`.

### Phase 5: Finalization

| Script | Status | Purpose |
|--------|--------|---------|
| `05I_finalize_catalog.py` | CANONICAL | Merges ID3 tags, Shazam results, and NLP language classification into `final_catalog.json`. This is the read-only master snapshot of the library. |

Supporting utilities: `05A` (JSON repair), `05B` (sanitize results), `05C` (confidence audit), `05D` (residue purge), `05E`/`05H` (empty-folder vacuum).

### Phase 6: Spotify Sync (Optional)

Requires a free Spotify Developer account.

| Script | Status | Purpose |
|--------|--------|---------|
| `06B_spotify_setup.py` | CANONICAL | OAuth handshake — run once to cache the token. |
| `06C_spotify_backup.py` | CANONICAL | Snapshot all existing playlists before making changes. |
| `06D_spotify_sync_engine.py` | CANONICAL | Creates per-language playlists mirroring your local library. Resumable. |
| `06E_spotify_discovery_sync.py` | CANONICAL | Cross-references local artists with Spotify listening history and generates genre-based "Essentials" playlists. |

**Spotify setup:**

1. Create an app at https://developer.spotify.com/dashboard
2. Set Redirect URI to `http://127.0.0.1:8888/callback`
3. Add to `.env`:
   ```dotenv
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   ```
4. Run `python 06B_spotify_setup.py` — browser opens, approve scopes, token is cached.

## Language Classification

The pipeline uses `langdetect` (NLP) to classify tracks by language automatically. No hardcoded language list — it creates whatever folders your collection needs.

### Language Hints (Optional)

For artists that NLP can't classify from Latin-script titles (e.g. Bollywood artists romanised as "Arijit Singh"), create hint files:

```
config/language_hints/
├── examples/           # Copy and customise these templates
│   ├── English.json
│   ├── Hindi.json
│   └── README.md       # Full schema reference
├── Hindi.json          # Your custom hints (create from examples)
└── Spanish.json
```

**Hint file schema:**

```json
{
  "artists": ["Arijit Singh", "A.R. Rahman", "Shreya Ghoshal"],
  "dna": ["bollywood", "bhangra", "desi"],
  "keywords": ["ishq", "dil", "pyaar"],
  "lang_codes": ["hi", "pa"]
}
```

- `artists` — exact artist names to classify into this language
- `dna` — substrings to match in folder/file paths
- `keywords` — substrings to match in track titles
- `lang_codes` — ISO 639-1 codes that `langdetect` might return for this language

## Configuration Reference

All configuration lives in `config.py` and is driven by environment variables (set in `.env` or your shell).

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `MUSIC_ROOT` | Yes | Parent of repo dir | Root of your music collection |
| `SORTED_ROOT` | No | `<MUSIC_ROOT>/Sorted` | Destination for sorted files |
| `DATA_DIR` | No | `<MUSIC_ROOT>/.data` | Machine-generated JSON artifacts |
| `DUPLICATES_STAGING` | No | `<repo>/Duplicates_Staging` | Quarantine for suspected duplicates |
| `UNIDENTIFIED_DIR` | No | `<SORTED_ROOT>/Unidentified` | Files Shazam couldn't identify |
| `FFMPEG_BIN` | No | `<MUSIC_ROOT>/ffmpeg/bin` | Portable FFmpeg path (Windows) |
| `SHAZAM_CONCURRENCY` | No | `20` | Parallel Shazam calls (lower if rate-limited) |
| `ITUNES_COUNTRIES` | No | `US,GB` | Country codes for iTunes API rotation |
| `SPOTIFY_CLIENT_ID` | Phase 6 only | — | Spotify app client ID |
| `SPOTIFY_CLIENT_SECRET` | Phase 6 only | — | Spotify app client secret |
| `SPOTIFY_REDIRECT_URI` | No | `http://127.0.0.1:8888/callback` | Spotify OAuth redirect |

## Supported Audio Formats

`.mp3`, `.m4a`, `.flac`, `.wav`, `.ogg`, `.wma`, `.aac`, `.opus`

## Safety Guarantees

- **No deletion.** Audio files are never deleted. Duplicates are moved to `Duplicates_Staging/` for manual review.
- **No writes into the music hierarchy.** All working state lives in `<DATA_DIR>` or the repo directory.
- **Resumable.** Every script can be interrupted and re-run safely.
- **Non-destructive tags.** Enrichment writes new tags but does not remove existing valid data.

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `shazamio-core` fails to install | You're on Python 3.13+. Use Python 3.12: `python3.12 -m venv .venv` |
| Shazam returns HTTP 429 | Lower `SHAZAM_CONCURRENCY` to 5-10 in `.env` |
| iTunes returns 403 | Add more country codes: `ITUNES_COUNTRIES=US,GB,AU,CA,DE` |
| `MUSIC_ROOT does not exist` | Set `MUSIC_ROOT` in `.env` to the absolute path of your music folder |
| Tags still show junk after enrichment | Re-run `04I_polish_and_enrich_v6.py` — it's idempotent |
| Spotify 403 on playlist creation | Add your Spotify account under "Users and Access" in the Developer Dashboard (Development Mode restriction) |
| `langdetect` misclassifies a language | Create a hint file in `config/language_hints/` for that language |
| Empty artist/album folders after sorting | Run `05E_final_cleanup.py` or `05H_final_vacuum.py` to vacuum empties |

## Scripts

Helper scripts that automate common workflows. Run from the repo root.

| Script | Purpose |
| ------ | ------- |
| `ultimate-music-manager/scripts/preflight.sh` | Validates Python 3.12, venv, dependencies, `.env`, `MUSIC_ROOT`, FFmpeg. Run before first pipeline execution. |
| `ultimate-music-manager/scripts/run-pipeline.sh` | Executes the happy-path sequence (Phases 1-5) with progress and timing. Supports `--skip-shazam`, `--spotify`, `--dry-run`. |
| `ultimate-music-manager/scripts/status.sh` | Dashboard showing file counts, language breakdown, data file status, and pipeline progress. |

### Usage

```bash
# Check environment is ready
bash ultimate-music-manager/scripts/preflight.sh

# Preview what the pipeline will do
bash ultimate-music-manager/scripts/run-pipeline.sh --dry-run

# Run the full pipeline
bash ultimate-music-manager/scripts/run-pipeline.sh

# Run including Spotify sync
bash ultimate-music-manager/scripts/run-pipeline.sh --spotify

# Check pipeline status at any time
bash ultimate-music-manager/scripts/status.sh
```

## Hook Integration

A safety guard hook prevents accidental execution of destructive utility scripts.

### Setup (Claude Code)

Add to `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{
        "type": "command",
        "command": "./ultimate-music-manager/hooks/safety-guard.sh"
      }]
    }]
  }
}
```

The hook intercepts commands referencing `05D_force_delete_residue`, `05F_final_scrub`, `total_scrub`, or `absolute_zero_sort` and injects a warning requiring explicit user confirmation. Silent (zero overhead) for all other commands.

See `hooks/HOOK.md` for details.

## References

Detailed documentation for deeper dives:

| Document | Contents |
| -------- | -------- |
| `references/data-files.md` | Schema and lineage for every JSON artifact — which script writes it, which scripts read it, full data flow diagram. |
| `references/language-hints-guide.md` | How to create language hint files, full schema, examples for Hindi/Japanese/Spanish, tips for getting classification right. |

## Design Principles

1. **Config-driven.** One `config.py` module, one `.env` file. No hardcoded paths anywhere.
2. **Language-agnostic.** No baked-in language lists. `langdetect` + optional hint files handle any language.
3. **Phased and incremental.** Each phase builds on the previous. You can stop after any phase and have a useful result.
4. **Auditable.** Every move, merge, and enrichment decision is logged to JSON in `<DATA_DIR>`.
5. **Zero-config happy path.** Clone into your music folder, create a `.env` with `MUSIC_ROOT`, and run.
