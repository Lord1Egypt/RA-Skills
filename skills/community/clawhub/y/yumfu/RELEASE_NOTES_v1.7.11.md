# YumFu v1.7.11 — Canon Reference Files for Source-Based Worlds

**Release date:** 2026-06-18

## What's new

Added **fan-authored canon reference files** for YumFu's source-based (IP) worlds, so story turns stay faithful to the original setting instead of drifting into generic atmosphere.

### New: `worlds/canon/<world-id>.md`

A human-readable "original-work background file" for each sourced world — world overview, era, faction/house/clan structure, a staged plot scaffold, character roster, magic/system anchors, themes, and an **"anchor vs. free-to-diverge"** guide.

Shipped canon files:

| world id | work | author |
|---|---|---|
| `xiaoao` | 笑傲江湖 The Smiling, Proud Wanderer | 金庸 Jin Yong |
| `yitian` | 倚天屠龙记 Heaven Sword & Dragon Saber | 金庸 Jin Yong |
| `game-of-thrones` | A Song of Ice and Fire / Game of Thrones | George R. R. Martin |
| `lotr` | The Lord of the Rings | J.R.R. Tolkien |
| `harry-potter` | Harry Potter | J.K. Rowling |
| `warrior-cats` | Warriors | Erin Hunter |

### How it's used
SKILL.md's **"World grounding rule"** now instructs the engine to load `worlds/canon/<world-id>.md` alongside `worlds/<world-id>.json` for these worlds. The JSON drives systems/mechanics; the canon.md keeps the *story* on-source (real geography, factions, characters, plot beats, artifacts, themes).

## Copyright / legal stance

These canon files are **transformative, in-our-own-words digests** — **not** reproductions of the original novels/scripts. No copyrighted source text is bundled. They are for non-commercial fan play, and plot may diverge from canon. Public-domain classics may carry fuller source text where appropriate; in-copyright IPs get digests only. See `worlds/canon/README.md`.

## Files
- `worlds/canon/README.md` — what these are / legal stance / usage
- `worlds/canon/{xiaoao,yitian,game-of-thrones,lotr,harry-potter,warrior-cats}.md`
- `SKILL.md` — World grounding rule updated to reference canon files
- `package.json` — version 1.7.11
