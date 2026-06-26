---
name: resource-hunter
version: 2.1.1
description: "Find the best public route to pan links, magnets, torrents, and public video URLs for movies, TV, anime, music, software, and books. Uses layered success-first retrieval, public HTML/RSS/no-API sources, and direct/actionable/clue result ranking."
metadata: {"openclaw":{"emoji":"🔎"}}
---

# Resource Hunter

A success-first public resource retrieval skill for:
- movies
- TV
- anime
- music
- software
- books
- public pan links
- magnets
- torrents
- public video URLs

## What makes it useful

### Stronger real-source coverage
- Pan/direct-or-clue: `2fun`, `dalipan`, `hunhepan`, `pansou.vip`, `tieba`
- Torrent/direct: `nyaa`, `animetosho`, `dmhy`, `eztv`, `tpb`, `torlock`, `yts`, `1337x`
- Indexed discovery fallback: `search-index:ddg`, `search-index:bing`, `search-index:brave`

### Layered retrieval
- `direct-structured-pan`
- `direct-structured-torrent`
- `community-clue`
- `indexed-discovery`
- `authenticated-connector` (reserved)

### Better result semantics
Results are ranked into:
- `direct`
- `actionable`
- `clue`

That makes it easier to distinguish:
- immediately usable links/magnets
- results that still need light follow-up
- clue-only records that point you in the right direction

## Important limitations

### Dalipan
`dalipan` is currently a **token-only clue source** in release semantics.

- anonymous search is confirmed
- runtime emits `dalipan://provider/eu-token`
- these records are structured clue output
- they are **not guaranteed final share URLs** yet

### Bing / Brave
- public HTML fallback only
- useful for recall and indexed discovery
- still best-effort providers, not stable structured direct sources

## Main entrypoint

```bash
SKILL_ROOT="$(openclaw skills path resource-hunter)"
SKILL_DIR="$SKILL_ROOT/scripts"
python3 "$SKILL_DIR/hunt.py" search "<query>"
```

## Common commands

```bash
python3 "$SKILL_DIR/hunt.py" search "Oppenheimer 2023" --4k
python3 "$SKILL_DIR/hunt.py" search "Breaking Bad S01E01" --tv
python3 "$SKILL_DIR/hunt.py" search "进击的巨人 Attack on Titan" --anime --sub
python3 "$SKILL_DIR/hunt.py" search "周杰伦 无损" --music
python3 "$SKILL_DIR/hunt.py" sources --probe --json
python3 "$SKILL_DIR/hunt.py" video probe "https://www.bilibili.com/video/BV..."
```

## Validation snapshot

- focused runtime/source regression set: `96 passed, 1 skipped`
- `ruff check skills/resource-hunter`: passed
- latest GitHub `resource-hunter-ci`: green

## Notes for agent behavior

- Prefer the main `hunt.py` entrypoint
- Use `--quick` for short chat answers
- Use `--json` for machine-consumable output
- Do not oversell Dalipan as a fully direct final-link source in the current release
- Do not oversell Bing/Brave as stable structured providers
