# Resource Hunter Sources

## Current source roles

### Direct structured pan
- `2fun`
  - Channel: `pan`
  - Priority: `1`
  - Role: primary structured pan aggregator
- `dalipan`
  - Channel: `pan`
  - Priority: `1`
  - Role: API-backed structured search source
  - Current limitation: runtime currently exposes Dalipan as **token-only clue output** (`dalipan://provider/eu-token`) because anonymous `detail/url` resolution is not fully open yet
- `hunhepan`
  - Channel: `pan`
  - Priority: `2`
  - Role: fallback pan source
- `pansou.vip`
  - Channel: `pan`
  - Priority: `3`
  - Role: extra fallback pan source

### Community clue
- `tieba`
  - Channel: `pan`
  - Priority: `4`
  - Role: public thread clue mining for pan links, passwords, magnets, and manual follow-up hints

### Direct structured torrent
- `nyaa`
  - Channel: `torrent`
  - Priority: `1`
  - Best for anime
- `animetosho`
  - Channel: `torrent`
  - Priority: `1`
  - Role: RSS-style torrent/magnet discovery, especially useful for anime
- `dmhy`
  - Channel: `torrent`
  - Priority: `1`
  - Role: public HTML torrent/magnet source, especially useful for anime and Chinese-tagged releases
- `eztv`
  - Channel: `torrent`
  - Priority: `1`
  - Best for TV episodes
- `tpb`
  - Channel: `torrent`
  - Priority: `2`
  - General fallback
- `torlock`
  - Channel: `torrent`
  - Priority: `2`
  - Role: HTML search + detail magnet extraction fallback
- `yts`
  - Channel: `torrent`
  - Priority: `2`
  - Best for movies
- `1337x`
  - Channel: `torrent`
  - Priority: `3`
  - General supplementary source

### Indexed discovery fallback
- `search-index:ddg`
  - Channel: `mixed`
  - Role: indexed discovery fallback via public DuckDuckGo HTML
- `search-index:bing`
  - Channel: `mixed`
  - Role: indexed discovery fallback via public Bing HTML
  - Stability note: best-effort only; HTML structure and region behavior may drift
- `search-index:brave`
  - Channel: `mixed`
  - Role: indexed discovery fallback via public Brave Search HTML
  - Stability note: best-effort only; HTML structure and rate limits may drift

## Retrieval layers

- `direct-structured-pan`
  - Sources: `2fun -> dalipan -> hunhepan -> pansou.vip`
  - Goal: first-pass structured pan results
- `direct-structured-torrent`
  - Sources: `nyaa -> animetosho -> dmhy -> eztv -> tpb -> torlock -> yts -> 1337x`
  - Goal: first-pass structured torrent and magnet results
- `community-clue`
  - Sources: `tieba`
  - Goal: public-thread clue extraction and follow-up hints
- `indexed-discovery`
  - Sources: `search-index:ddg -> search-index:bing -> search-index:brave`
  - Goal: best-effort fallback when structured retrieval does not surface a confident result
- `authenticated-connector`
  - Reserved for future work

## Default routing matrix

- Movie: prefer pan sources first, then movie/general torrent sources
- TV: prefer TV-capable torrent sources first, then pan supplement
- Anime: prefer `nyaa -> animetosho -> dmhy -> torlock`, then pan supplement
- Music/software/book/general: pan sources first, torrent second
- Public video URL: no pan/torrent search; route directly to the video workflow

## Health and caveats

- Every active search stores `source_status` snapshots for direct sources
- `sources --probe` actively tests registered pan/torrent adapters
- Indexed discovery providers are fallback providers and are not equivalent to stable structured direct-source guarantees
- External public sources may throttle, change formats, break without notice, or vary by region
- `dalipan` is currently a release with an explicit limitation: anonymous search works, but final detail/url resolution is not yet fully anonymous in current runtime
