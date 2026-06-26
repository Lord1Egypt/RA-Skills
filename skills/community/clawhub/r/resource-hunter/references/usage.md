# Resource Hunter Usage

## Search

Main command:

```bash
python3 scripts/hunt.py search "<query>" [options]
```

Key options:

- `--kind movie|tv|anime|music|software|book|general`
- `--channel both|pan|torrent`
- `--quick`
- `--sub`
- `--4k`
- `--json`
- `--page`
- `--limit`

Examples:

```bash
python3 scripts/hunt.py search "Oppenheimer 2023" --kind movie --4k
python3 scripts/hunt.py search "Breaking Bad S01E01" --tv
python3 scripts/hunt.py search "进击的巨人 Attack on Titan" --anime --sub
python3 scripts/hunt.py search "三体 epub" --book --channel pan
python3 scripts/hunt.py search "周杰伦 无损" --music --quick
python3 scripts/hunt.py search "Adobe Photoshop 2024" --software --json
```

## Current retrieval behavior

- Movie: pan first, torrents as supplement
- TV: TV-capable torrents first, pan as supplement
- Anime: prefer `nyaa -> animetosho -> dmhy -> torlock`, then pan sources
- Music/software/book/general: pan first
- When direct retrieval does not surface a confident result, indexed discovery fallback may run through `search-index:ddg`, `search-index:bing`, and `search-index:brave`

## Important result semantics

- `direct`: intended to be immediately usable
- `actionable`: likely useful but may still need small follow-up
- `clue`: pointer or structured hint that still requires manual follow-up

### Dalipan-specific note

Dalipan is currently integrated as a **public anonymous search clue source**.

- Anonymous search is confirmed via the public search API
- Final anonymous `detail/url` resolution is still incomplete
- Runtime currently outputs Dalipan records as `dalipan://provider/eu-token`
- Treat those as structured clue records, not guaranteed final share URLs

### Bing / Brave note

`search-index:bing` and `search-index:brave` are best-effort indexed-discovery fallbacks.

- They are useful for recall
- They are not the same stability class as structured direct adapters
- HTML layout, throttling, or regional differences may affect them

## Video

Public video URLs go through the `video` subcommands:

```bash
python3 scripts/hunt.py video info "https://youtu.be/..."
python3 scripts/hunt.py video probe "https://www.bilibili.com/video/BV..."
python3 scripts/hunt.py video download "https://youtu.be/..." best
python3 scripts/hunt.py video download "https://youtu.be/..." balanced
python3 scripts/hunt.py video download "https://youtu.be/..." small
python3 scripts/hunt.py video download "https://youtu.be/..." audio
python3 scripts/hunt.py video subtitle "https://youtu.be/..." --lang zh-Hans,zh,en
```

## Legacy wrappers

These remain available for one compatibility cycle:

```bash
python3 scripts/pansou.py "Oppenheimer 2023" --max 5
python3 scripts/torrent.py "Breaking Bad S01E01" --tv --limit 8
python3 scripts/video.py info "https://youtu.be/..."
```

## Source and health inspection

```bash
python3 scripts/hunt.py sources
python3 scripts/hunt.py sources --probe --json
python3 scripts/hunt.py doctor --json
```

Notes:

- `sources --probe` actively probes registered pan/torrent adapters
- indexed discovery providers are shown through retrieval-layer metadata, but they should still be understood as fallback providers

## Packaging smoke

Packaging/report/gate/verify commands are still supported for installability and CI workflows.

Common examples:

```bash
python3 scripts/hunt.py doctor --json --require-packaging-ready
python3 scripts/hunt.py packaging-smoke --json
python3 scripts/hunt.py packaging-baseline --project-root /path/to/repo --python auto --bootstrap-build-deps --output-dir artifacts/packaging-baseline --require-expected-outcomes
python3 scripts/hunt.py packaging-baseline-report artifacts/packaging-baseline/packaging-baseline.json
python3 scripts/packaging_report.py --json artifacts/downloaded-gh-artifacts
python3 scripts/packaging_gate.py artifacts/downloaded-gh-artifacts --json
python3 scripts/packaging_verify.py --github-run latest --output-dir artifacts/packaging-baseline-gh-verify --require-artifact-count 6
```

## Operational notes

- The engine caches recent normalized responses and source health in SQLite
- Public HTML/RSS sources may throttle, block, or change structure without notice
- Hard cases such as same-title different-year films are improved but not fully solved yet
- `The Merry Widow 1952` remains a known difficult live case
