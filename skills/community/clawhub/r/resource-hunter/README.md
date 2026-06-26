# Resource Hunter

Find the best public route to public pan links, magnets, torrents, and public video URLs for movies, TV, anime, music, software, and books.

`resource-hunter` is a success-first retrieval skill focused on **real public no-API sources** and **usable result quality**, not just broad source counting.

## Highlights

- **Broader real-source coverage**
  - Pan/direct-or-clue: `2fun`, `dalipan`, `hunhepan`, `pansou.vip`, `tieba`
  - Torrent/direct: `nyaa`, `animetosho`, `dmhy`, `eztv`, `tpb`, `torlock`, `yts`, `1337x`
  - Indexed discovery fallback: `search-index:ddg`, `search-index:bing`, `search-index:brave`
- **Layered retrieval**
  - direct structured pan
  - direct structured torrent
  - community clue mining
  - indexed discovery fallback
- **Better precision for tricky titles**
  - year-conflict downgrade
  - evidence fusion and corroboration
  - actionability split into `direct`, `actionable`, and `clue`
- **No API keys required**
  - public HTML, RSS, magnet, and public page flows only
- **Installable and scriptable**
  - `resource-hunter`
  - `python -m resource_hunter`
  - `scripts/hunt.py`

## What changed in 2.1.1

- polished the GitHub / ClawHub surface copy for a clearer first impression
- kept the success-first source expansion release intact
- improved release-facing wording around:
  - AnimeTosho / DMHY / Torlock integration
  - Dalipan token-only clue semantics
  - Bing / Brave indexed-discovery fallback role
  - current validation and known limits

## Important semantics and limits

### Dalipan
Dalipan is currently integrated as a **public anonymous search clue source**.

- anonymous search is confirmed
- current runtime emits `dalipan://provider/eu-token`
- those records are structured clue outputs, **not guaranteed final share URLs**
- anonymous `detail/url` completion is still incomplete

### Bing / Brave
- public HTML fallback only
- useful for recall
- still best-effort indexed-discovery providers, not the same stability class as structured direct sources

## Validation snapshot

- focused runtime/source regression set: `96 passed, 1 skipped`
- `ruff check skills/resource-hunter`: passed
- GitHub `resource-hunter-ci`: green after Python 3.12 packaging-probe test stabilization

## Common commands

```bash
python3 scripts/hunt.py search "Oppenheimer 2023" --kind movie --4k
python3 scripts/hunt.py search "Breaking Bad S01E01" --tv
python3 scripts/hunt.py search "进击的巨人 Attack on Titan" --anime --sub
python3 scripts/hunt.py search "周杰伦 无损" --music --quick
python3 scripts/hunt.py sources --probe --json
python3 scripts/hunt.py video probe "https://www.bilibili.com/video/BV..."
```

## Current known limits

- public HTML/RSS sources can drift, throttle, or region-block without notice
- same-title different-year disambiguation is improved but still not perfect
- `The Merry Widow 1952` remains a known hard live case
- `PanSearch` looks promising but is not yet integrated because content-card link extraction is still unfinished

## References

- Skill-focused usage: [SKILL.md](./SKILL.md)
- Source matrix: [references/sources.md](./references/sources.md)
- Architecture: [references/architecture.md](./references/architecture.md)
- Usage notes: [references/usage.md](./references/usage.md)
