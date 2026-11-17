# Viewing Standards & Acuity — Reference

## 1. Where the angles come from
- **SMPTE EG-18-1994**: recommends a minimum viewing angle of 30° for theatrical presentation; widely adopted as the "comfortable reference" for home TV.
- **THX certification**: 40° recommended for the last row of cinemas; THX home guidance uses 40° as the immersive target.
- General TV engineering practice: below ~24° feels small (image stops filling attention), above ~50° is front-row territory (edge distortion awareness, eye travel, motion discomfort for some viewers).

## 2. The distance factors (16:9), derived
θ = 2·atan(0.4358·D / d), so:
- 24° → d ≈ 2.03×D
- 30° → d ≈ 1.62×D
- 40° → d ≈ 1.20×D
- 45° → d ≈ 1.07×D
- 50° → d ≈ 0.94×D

Where D = diagonal and d = eye-to-panel distance, same units.

## 3. Resolution acuity (the 1-arc-minute rule)
20/20 vision resolves ~1 arc-minute per line pair element. A pixel subtends 1 arc-min at:
`d = (0.8716·D / N) / (2·tan(0.5'))` where N = horizontal pixels.
- 1080p (N=1920): d ≈ 1.56×D — closer than this, 1080p pixels/screendoor become visible
- 4K (N=3840): d ≈ 0.78×D — 4K's own pixels visible only this close
- 8K (N=7680): d ≈ 0.39×D — roughly 3 ft for a 77" panel

Consequences:
- **4K beats 1080p only inside 1.56×D**; pay for 4K only if the seat is closer than that.
- **8K beats 4K only inside 0.78×D** — almost never a couch; 8K's honest use is monitor-distance work or huge screens.
- Visual acuity varies: 20/15 vision shifts thresholds ~25% farther; sitting farther with glasses off shifts them closer.

## 4. Content-mix band table (as encoded in the script)
| Use | lo angle | hi angle | Rationale |
|---|---|---|---|
| movies | 34° | 45° | immersion is the point; subtitles at edges are acceptable |
| mixed | 30° | 40° | SMPTE floor to THX target |
| sports (daytime groups) | 28° | 36° | longer sessions, wider groups, motion comfort |
| monitor/PC | 45° | 55° | text legibility; note: at these angles use display scaling, check font rendering |

## 5. Placement
- Screen center at seated eye height (typical 38–42 in). Every 5° of vertical gaze elevation above horizontal measurably increases neck strain (ergonomic guidance caps sustained gaze elevation ~15°).
- Above-fireplace installs typically force 20–30° tilt-up: the reference math and a full-motion mount pull-out are the mitigations; short of that, accept the strain or relocate.
- Measure eye-to-PANEL: a stand adds 8–12 in of setback, a flush mount ~2 in. At 0.94–1.6×D, one foot of measurement error shifts the angle band a full size class.

## 6. Projector math
- Brightness: needed lumens = target fL × screen area (sq ft) ÷ gain.
  - SDR dark room: 14–16 fL (SMPTE theatrical reference is 16 fL for the screen center)
  - HDR home target: 40+ fL (highlights depend on headroom)
  - Sports/daytime with lights: 60+ fL effective
- Ambient wash fL adds to black level: contrast ratio ≈ target / (target + ambient). 3 fL wash on a 16 fL image → ~84% contrast; 10 fL wash → 62%; direct sun through a window (50+ fL) → no consumer projector competes.
- Throw ratio = throw distance ÷ screen width. Typical long-throws 1.2–1.5; short-throws 0.4–0.7; UST < 0.25. Mount distance = ratio × width — check against the room before buying either piece.

## 7. Sources / anchors
- SMPTE Engineering Guideline EG-18-1994 (viewing angle)
- THX home theater certification guidance (40° target)
- ITU-R BT.500 viewing-distance recommendations (ratio bands by height)
- Human visual acuity literature (1 arc-min ≈ 0.000291 rad for 20/20)
