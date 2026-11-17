---
name: subtitle-download
description: Batch-download missing subtitles for a media library of organized movie folders.
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
    requires:
      bins: [subliminal]
---

# Subtitle Download (batch, for an organized library)

The library keeps each movie as `Movie Title (Year)/Movie Title (Year) [Quality Codec].ext` + a matching
`Movie Title (Year) [Quality Codec].srt` (same stem). The job is to fill the missing `.srt` files
without breaking that exact-stem rule.

## Working approach (Podman + Subliminal)

Subliminal is the right tool: async provider pool, hash + guessit filename matching, 7 providers,
saves `.srt` next to the video. Run it under **Podman** on a Fedora Atomic host (not Docker — see Pitfalls).

Exact-stem matching requires a 3-step dance, because Subliminal writes `Name.en.srt` (with a
language suffix) and will otherwise re-download movies that already have subs:

1. **Pre-tag existing subs** as `.en.srt` so Subliminal recognizes them as English and skips them.
2. **Run with a READ-WRITE mount** (this is the #1 failure — `:ro` crashes with
   `OSError: [Errno 30] Read-only file system` at save time, after doing all the network work).
3. **Strip the `.en` suffix** from every `.srt` afterward so filenames match the video stems exactly.

See `scripts/run_subliminal.sh` (parameterized, does all three) and `references/workflow-podman.md`.

## Converting stray formats

Subliminal sometimes grabs `.ass` or `.sub` instead of `.srt`. Convert with ffmpeg:
```bash
# .ass often has a UTF-8 BOM that makes ffmpeg autodetect fail with
# 'Invalid data found' — force the format:
ffmpeg -y -f ass -i "Movie (2012)/weird.ass" "Movie (2012)/Movie (2012).srt"
# .sub (MicroDVD/SubRip-ish) -> .srt
ffmpeg -y -i "Movie (2012)/weird.sub" "Movie (2012)/Movie (2012).srt"
```
Then delete the original `.ass`/`.sub`. Always verify the output `.srt` is non-empty.

## Provider reality (important)

In a real run with default config, of Subliminal's three default providers only **OpenSubtitles**
actually returned results:
- `opensubtitles` — worked
- `podnapisi` — failed DNS resolution (`Name does not resolve`)
- `opensubtitlescom` — errored out mid-run

So a single Subliminal pass leaves ~40% of a library without subs. To close the gap, either:
- add OpenSubtitles.com credentials (free account → different catalog, higher limits), or
- use **Bazarr** (Docker; 30+ providers incl. Subscene/YIFY) or **Rustitles** (AppImage; wraps
  Subliminal, multi-instance parallel) — see `references/research-summary.md`.

## Pitfalls

- **Podman, not Docker.** The target machine is a Fedora Atomic host with Podman. Swap `docker` → `podman`;
  CLI is compatible. Never suggest layering Docker via rpm-ostree.
- **Mount must be RW** for Subliminal to save. (`:ro` fails late and wastes the whole run.)
- **Subliminal writes `Name.en.srt`** — strip `.en` after, or your exact-stem convention breaks.
- **Filenames have spaces and brackets.** Verify renames/matches with null-delimited loops:
  `while IFS= read -r -d '' f; do ...; done < <(find ... -print0)`. A plain `for f in $var`
  word-splits on spaces and produces false mismatches; comparing a sub against the *folder*
  name (not the video stem) also produces false mismatches. Always compare video-stem vs srt-stem.
- **Podnapisi/opensubtitlescom may be dead** in default config — don't report 100% coverage
  after one pass; re-check the missing list.

## Tool shortlist (full research in references/research-summary.md)

| Tool | Fit | Install on Fedora Atomic |
|------|-----|--------------------------|
| **Subliminal** | One-shot batch, hash+filename, exact-stem | `podman run ghcr.io/diaoul/subliminal` |
| **Rustitles** | GUI + parallel instances, wraps Subliminal | AppImage (no install) |
| **Bazarr** | Persistent daemon, 30+ providers, web UI | Docker Compose |
