# YumFu v1.7.0 — Sengoku Chaos + Stronger Opening Flow 🏯

## Highlights

This release expands YumFu beyond Dynamic Daily Evolution and introduces a new fully integrated world direction:

# **战国乱世 / Sengoku Chaos**

A late-Sengoku alternate-history sandbox with:
- Oda / Toyotomi / Tokugawa / Takeda / Uesugi / Mori / Shimazu power blocks
- Ming / Joseon cross-sea influence
- European gun merchants and artillery technicians
- courtesan politics, espionage, shipping, ledgers, and black-market money
- maritime rise paths, including a new **sea merchant boss** progression line

## New World: Sengoku Chaos

### Added world scaffold + playable start flow
- New `worlds/sengoku.json`
- Character creation framework for Sengoku roles
- Opening scenario hooks including:
  - Kyoto night fire
  - Azuchi banquet
  - Osaka grain crisis
  - Sakai gun deal
  - Kai cavalry muster
  - Tsushima sea letter

### New role density
Sengoku now supports stronger differentiated openings for:
- Ashigaru Captain
- Ronin Boss
- Shinobi Master
- Gunsmith & Artillery Engineer
- Courtesan Power Broker
- Foreign Adventurer
- **Maritime Merchant Boss**

### Maritime rise path
Added a dedicated economic-power route focused on:
- shipping
- smuggling
- firearms arbitrage
- black-market cargo
- debt networks
- merchant credit and port control

## Stronger Opening Experience

### `/yumfu start` now treated as a real game turn
Opening scenes should no longer feel like setup-only text.
This release reinforces that:
- `/yumfu start` must generate an opening image
- opening scene should be sent as the first playable game turn
- first-turn options should already feel like real decisions, not just onboarding

### Sengoku opening rendering
Added scripts to make Sengoku starts feel immediately playable:
- `scripts/init_sengoku_save.py`
- `scripts/start_sengoku_game.py`
- `scripts/render_sengoku_opening.py`

These now support:
- save initialization
- daily evolution yes/no handling
- rendered first-scene payloads
- world-specific first-turn NPCs and actions

## Stronger Sengoku Daily Evolution

Sengoku no longer falls back to generic daily evolution.
It now has dedicated update generation with world-flavored hooks such as:
- hidden gun purchases
- courtesan whispers
- shifting grain and trade routes
- pre-meeting assassinations
- port rumors and sea-letter crises

## Visual Direction Update

### Sengoku = ukiyo-e by default
The world now uses **Japanese ukiyo-e woodblock print style** as its primary image direction:
- bold ink outlines
- washi-paper texture
- flat layered colors
- Sengoku banners, lacquer armor, castles, smoke, matchlocks, and torchlight

This applies to:
- opening scenes
- first-turn scenes
- daily evolution images

## Core YumFu Rule Reinforcement

This release also reaffirms two important global rules:
- every `/yumfu start` must generate an opening image
- every active gameplay turn should produce exactly **one** primary scene image, not zero and not duplicates

## Release Focus

**Main theme of v1.7.0:**
> Sengoku Chaos becomes a real playable YumFu world, with stronger starts, better density, and world-matched visual identity.
