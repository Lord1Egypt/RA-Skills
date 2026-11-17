# Subtitle Download Tools — Research Summary

Top 3 recommendations from an async-delegated research pass (2026-08-28), for a
media library on Fedora Atomic (Podman, no rpm-ostree layering).

## 1. Subliminal (chosen)
- Native async (`AsyncProviderPool`), hash + guessit filename matching.
- 7 providers: opensubtitles, opensubtitlescom, podnapisi, addic7ed, napiprojekt, gestdown, tvsubtitles.
- Saves `.srt` next to video. CLI: `subliminal download -l en <path>`.
- Podman: `podman run --rm -v cache:/usr/src/cache -v $MOVIES:/movies ghcr.io/diaoul/subliminal download -l en /movies`
- Reality: only `opensubtitles` returned results in a default-config run;
  `podnapisi` DNS-failed, `opensubtitlescom` errored. ~40% of library stayed missing.

## 2. Rustitles (AppImage)
- Native Linux AppImage (no install) — ideal for Fedora Atomic.
- Wraps Subliminal; recursive folder scan; GUI + headless; run 7+ instances in parallel
  (Reddit user processed 8500 movies in <1hr by splitting the tree).
- https://github.com/fosterbarnes/rustitles

## 3. Bazarr (Docker Compose)
- Persistent daemon + web UI; 30+ providers (incl. Subscene, YIFY, OpenSubtitles).
- Background queue, scheduled rescans. Best for ongoing automation after the initial batch.
- https://github.com/morpheus65535/bazarr

## Provider setup priority (best movie coverage)
| Provider | Needs account? | Notes |
|----------|----------------|-------|
| OpenSubtitles | Yes (free VIP) | Largest DB, hash matching |
| OpenSubtitles.com | Yes | Newer API, better uptime, different catalog |
| Podnapisi | Optional | Quality subs; DNS was flaky in this env |
| Subscene | No | Community uploads, rare titles |
| YIFY | No | Movie-specific, good naming |

## Avoiding provider bans
- Use a persistent cache (`dogpile.cache.dbm`) — survives restarts.
- Add OpenSubtitles credentials (200/day vs 30/day anonymous).
- `--age` on recurring runs (e.g. `--age 30d`) so you don't re-scan the whole library.

## Full report
A 387-line research report was generated locally during the original investigation; it
is not included in this package.
