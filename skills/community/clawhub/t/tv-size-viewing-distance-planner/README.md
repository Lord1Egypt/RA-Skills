# TV Size & Viewing Distance Planner

**Buys the right TV size with geometry, not showroom vibes: SMPTE/THX angular bands, the distance where 4K is actually visible, price-per-square-inch upgrades, and projector lumens/throw math.**

## The problem
"TV too small for the room" is the most common home-theater mistake, and the second is paying for pixels that can't be resolved from the couch. Size advice online is folklore ("65 inch for most rooms"); meanwhile screen area grows with the square of diagonal, so upgrade decisions (55→65→77) are really +40%-image decisions, and 4K only beats 1080p inside ~1.56× the diagonal — a fact retailers never mention because showroom walls put you at 0.8×. Projector buyers get burned separately: 3,000 "marketing lumens" into a sunlit 120" screen still looks like a gray ghost.

## What this skill does
- **Exact angular geometry**: viewing angle from any diagonal × distance; size bands per SMPTE 30° / THX 40°, tuned by content mix (movies/mixed/sports/monitor)
- **Resolution-acuity math**: 1-arcminute-per-pixel thresholds for 1080p/4K/8K → `4K VISIBLE` / `4K WASTED` verdicts before you pay the premium
- **Current-TV check**: UNDERSIZED / IN BAND / IMMERSIVE verdict + the free upgrade (move the couch to the distance that hits 30°)
- **Price-per-square-inch comparisons** including cost per ADDED square inch for upgrades
- **Projector mode**: needed lumens = target fL × screen area ÷ gain (SDR 16 / HDR 40 / sports 60 fL), throw-distance check, ambient-light contrast loss

## Quick example
```bash
python3 scripts/tv_size_advisor.py recommend --distance 8.5 --use movies --current 55
# → band 66"–95"; 55" subtends 24.6° → UNDERSIZED; couch at 7.4 ft = free SMPTE 30°
python3 scripts/tv_size_advisor.py compare --sizes 65:1099 77:2199 --distance 10
# → 77" is +40% image; $X per added square inch named
```

## Who needs this
- Anyone between two TV sizes at a retailer or speculating on Black Friday
- New-living-room setups where the wall allows more than the old TV did
- Projector first-timers sizing screen, lumens, and throw before cutting into drywall
- Mount/placement sanity checks (eye-height centering reminders included)

## Install
Python 3.9+, stdlib only, offline.

```bash
git clone https://github.com/voronindenis5/tv-size-viewing-distance-planner
cd tv-size-viewing-distance-planner
python3 scripts/tv_size_advisor.py --demo
```

## License
MIT © Denis Voronin
