---
name: tv-size-viewing-distance-planner
description: Use when buying a TV or projector and unsure what size fits the room, when a 65" vs 77" debate needs geometry instead of vibes, or when sizing a projector screen and lumens — computes exact viewing angles (SMPTE 30° reference, THX 40° cinematic), the distance at which 4K resolution actually becomes distinguishable from 1080p (1.56× diagonal) so nobody pays an 8K premium from across the room, recommends a size band per distance and content mix, checks whether a current TV is undersized, and prices size upgrades per square inch of image; projector mode does screen-gain × ambient-light lumens math and throw-distance checks.
version: 1.0.0
author: Denis Voronin
license: MIT
tags: [tv-size, viewing-distance, home-theater, projector, geometry, buying-guide]
---

# TV Size & Viewing Distance Planner

## Overview
TV size advice on the internet is astrology: "65 inch is good for most rooms." The real answer is angular geometry: what matters is the **angle the screen subtends at your eyes**, and the standards are explicit — SMPTE's reference is 30°, THX's cinematic recommendation is 40°. From a couch distance, both map to exact diagonal bands. On top of that sits the most abused fact in TV retail: **resolution is a distance question**. A 4K panel only differs from 1080p closer than ~1.56× the diagonal, and 8K is invisible at any normal couch distance — which prices the "resolution upgrade" at zero for most rooms.

This skill computes the geometry honestly (16:9 width/height factors, angle from distance × diagonal, per-pixel acuity limit at 1 arc-minute), recommends a size band tuned by content (movies love 40°+, daytime sports tolerate 30°, PC-monitor use wants 50°+), checks an existing TV for undersizing, and does the two upgrades people actually agonize over: 55"→65" and 65"→77" priced **per square inch of image gained**. Projector mode sizes lumens against screen gain and ambient light, and checks throw distance against the room.

## When to Use
- Buying a TV and stuck between sizes at a given couch/wall distance
- "Is 4K/8K worth it from my distance?" — the acuity math, not marketing
- Wall-mount height and a sanity check that the room can even host the recommended band
- Projector: screen size, gain, needed lumens, throw ratio
- Deciding whether to move the couch closer instead of buying bigger (free upgrade)

**Don't use for:** OLED-vs-LCD panel tech choice, HDMI/audio gear, or monitor workflow ergonomics (32" at 80 cm is a desk-calibration question — close cousin, different standard: see references §7).

## Quick Start
```bash
# Couch is 8.5 ft from the wall, mostly movies
python3 scripts/tv_size_advisor.py recommend --distance 8.5 --use movies

# The eternal 65 vs 77 debate at 10 ft, with real prices
python3 scripts/tv_size_advisor.py compare --sizes 65:1099 77:2199 --distance 10

# Is 4K distinguishable from 1080p at 9 ft on a 65"?
python3 scripts/tv_size_advisor.py resolution --diagonal 65 --distance 9

# Projector: 120" screen, 1.0 gain, HDR dark room
python3 scripts/tv_size_advisor.py projector --screen 120 --gain 1.0 --mode hdr

python3 scripts/tv_size_advisor.py --demo
```

## The Geometry (exact, not folklore)
For 16:9: width = 0.8716 × diagonal, height = 0.4903 × diagonal.
Viewing angle θ = 2 · atan(width / 2 / distance).

| Standard | Angle | Distance ÷ diagonal | Feels like |
|---|---|---|---|
| "Too small" floor | < 24° | > 2.0× | watching a laptop |
| SMPTE reference | 30° | ~1.62× | comfortable general TV |
| THX cinematic | 40° | ~1.20× | immersive movies |
| Front-row / monitor | 50°+ | < 0.94× | fills vision; subtitles near edges |

**Resolution acuity** (20/20 vision, 1 arc-minute per pixel): 1080p fully resolved beyond **1.56× diagonal**, 4K beyond **0.78× diagonal**. Between those distances you're paying for pixels you can't count. 8K's threshold (0.39×) is closer than any couch.

## Verdicts
- `UNDERSIZED` — current TV subtends < 24° at the seat: the room wants bigger (or the couch closer — printed with the free-upgrade distance)
- `IN BAND` — inside 30–40°: correct for stated use
- `IMMERSIVE` — 40°+: great for movies, verify wall/mount and motion tolerance
- `4K WASTED` / `4K VISIBLE` — resolution verdict from acuity math
- `NEEDS X LUMENS` — projector brightness requirement, with an honest "no projector survives direct sunlight" gate

## Common Pitfalls
1. **Shopping by diagonal, living by area.** 55→65" is +40% image area, 65→77" is +40% again; price-per-square-inch is the honest comparator (`compare` command).
2. **Distance from the wall vs from the screen.** Measure eye-to-panel: TV depth + stand/mount setback ≈ 1 ft; mounts reclaim it.
3. **Mounting too high.** Center of screen at seated eye level (~40 in); above a fireplace = neck extension (references §6 gives the tilt math if unavoidable).
4. **Trusting showroom perception.** Retail walls put you at 0.8× diagonal — every TV looks huge and every 4K demo is visible. Re-anchor to your actual distance.
5. **Projector lumens vs ambient.** A 3,000-lumen projector on a 120" 1.0-gain screen in a sunlit room still looks like a gray ghost; the needed-lumens math says why, and says "curtains first."

## Verification Checklist
- [ ] Distance measured eye-to-screen (not wall-to-wall)
- [ ] Content mix stated — the band shifts with it
- [ ] Resolution verdict checked before paying a 4K/8K premium
- [ ] For mounts: stud location, center-at-eye-height, and tilt < 15° if elevated
- [ ] Projector: throw distance ÷ screen width within the projector's throw ratio

## Example
Couch 8.5 ft, movies. Geometry: SMPTE 30° needs 63"; THX 40° wants 85"; the movies band prints as **72"–97"** with shelf sizes 70–98. A 65" sits at 31° (small side for movies); a 55" subtends 26.4° → **UNDERSIZED for movies** — free fix: couch at 7.4 ft hits SMPTE 30°. Resolution: 1080p's pixels vanish beyond ~1.56× diagonal, so 4K beats 1080p on anything ≥ ~66" at this distance (visible on the 77" pick), and 8K needs the couch inside ~5 ft — a non-couch.
