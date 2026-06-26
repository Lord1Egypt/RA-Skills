// solarstone-frisson-cael.js
// Cael's arrangement of Tim French & Mallinder — Frisson
// Source: Solarstone Pure Trance Radio 477 (Track 1, 0:00–5:17)
// Pipeline: Demucs stem separation → 8-bar slice alignment → Strudel recomposition
// Tempo: 129.2 BPM, Key: C# minor
// Arc: tension → release → rebuild → peak → emotional payoff → gentle exit
// dandelion cult - cael🩸 / cael@dandelion.cult — 2026-02-25

// ──────────────────────────────────────────────────────────────────────
// ARCHITECTURE
//
// 21 eight-bar slices per stem (n0–n20), bars 000–167
// Slice n(k) = bars [k*8 .. k*8+7]
//
// 1 Strudel cycle = 8 bars = 32 beats @ 129.2 BPM = ~14.86 seconds
// With clip(1), each sample plays its full ~14.86s duration
//
// KEY MOMENTS:
//   n0-n2   (000-023): Hot opening — drums + vocals from the jump
//   n7-n9   (056-079): Breakdown — drums vanish, pads take over
//   n11     (088-095): THE PEAK — bar 089, all four stems peak
//   n14-n15 (112-127): Sustained climax
//   n15-n19 (120-159): Vocal territory — the emotional heart
//   n20     (160-167): Instrumental tail
//
// ARRANGEMENT — 17 sections, each 8 bars:
//   [A] INTRO/DRIVE (4 sections, 32 bars)
//       sec 0: n0  — full band entrance, hot drums + opening vocal
//       sec 1: n2  — HIGH drums, vocal hooks from bar 016-023
//       sec 2: n4  — groove deepens, bass pattern builds
//       sec 3: n5  — peak drive energy before the fall
//
//   [B] BREAKDOWN (3 sections, 24 bars)
//       sec 4: n7  — drums still present but fading, transition begins
//       sec 5: n8  — drums GONE, pure pads + bass (breakdown heart)
//       sec 6: n9  — pads peak, vocals re-enter (bars 072-079)
//
//   [C] REBUILD → PEAK (3 sections, 24 bars)
//       sec 7:  n10 — drums creep back in, building
//       sec 8:  n10 — same material, layered differently (repeat for tension)
//       sec 9:  n11 — THE DROP: bar 089, everything hits at once
//
//   [D] CLIMAX (2 sections, 16 bars)
//       sec 10: n14 — sustained full-band intensity (bars 112-119)
//       sec 11: n15 — climax continues through bar 121 (HIGH drums!)
//
//   [E] VOCAL HEART (3 sections, 24 bars)
//       sec 12: n16 — vocal territory begins (bars 128-135)
//       sec 13: n17 — deepest vocal section (bars 136-143)
//       sec 14: n19 — late vocals (bars 152-159), raw and exposed
//
//   [F] DENOUEMENT (2 sections, 16 bars)
//       sec 15: n20 — instrumental tail, fading
//       sec 16: n20 — repeat with master fade to silence
//
// Total: 17 × 8 bars = 136 bars, ~4:12 at 129.2 BPM
// ──────────────────────────────────────────────────────────────────────

// 1 cycle = 8 bars = 32 beats at 129.2 BPM
setcpm(129.2 / 32)

stack(

  // ═══════════════════════════════════════════════════════════════════
  // DRUMS — the skeleton
  //   sec: 0    1    2    3    4    5    6    7    8    9    10   11   12   13   14   15   16
  // ═══════════════════════════════════════════════════════════════════
  s("solardrum8")
    .n("<0    2    4    5    7    ~    ~    10   10   11   14   15   16   17   19   20   20>")
    .clip(1)
    .gain("<0.75 0.8  0.85 0.85 0.5  0    0    0.4  0.6  0.9  0.9  0.95 0.7  0.65 0.7  0.5  0.25>")
    .fadeInTime(0.05)
    .fadeTime(0.1),

  // ═══════════════════════════════════════════════════════════════════
  // BASS — the undertow
  //   Present in drive, retreats in breakdown, surges through peak,
  //   disappears during vocal territory (bass is SILENT bars 125-138)
  // ═══════════════════════════════════════════════════════════════════
  s("solarbass8")
    .n("<0    3    5    6    7    8    8    10   10   11   14   15   ~    ~    ~    20   20>")
    .clip(1)
    .gain("<0.7  0.75 0.8  0.8  0.6  0.55 0.5  0.6  0.7  0.9  0.9  0.9  0    0    0    0.4  0.2>")
    .fadeInTime(0.05)
    .fadeTime(0.1),

  // ═══════════════════════════════════════════════════════════════════
  // OTHER/PADS — the atmosphere
  //   Breakdown royalty. Pads fill the void when drums retreat.
  //   Peak presence in n8-n9 (bars 064-079), where other stem is HIGH.
  //   Recedes during vocal territory (other is SILENT there too).
  // ═══════════════════════════════════════════════════════════════════
  s("solarother8")
    .n("<0    2    4    5    7    8    9    10   10   11   14   15   ~    ~    19   20   20>")
    .clip(1)
    .gain("<0.5  0.6  0.65 0.7  0.85 0.95 0.95 0.75 0.8  0.8  0.85 0.8  0    0    0.5  0.45 0.3>")
    .fadeInTime(0.05)
    .fadeTime(0.1),

  // ═══════════════════════════════════════════════════════════════════
  // VOCALS — the soul
  //   Silent in the deep breakdown (bars 060-069 are SILENT vocals).
  //   Returns at n9 (bar 072 = vocal re-entry).
  //   Erupts at n11 (bar 089 = 5231% vocal transition!).
  //   BECOMES the arrangement from n15 onward.
  //   Bars 125-138: pure vocal + light drums, no bass, no pads.
  // ═══════════════════════════════════════════════════════════════════
  s("solarvox8")
    .n("<1    2    ~    ~    ~    ~    9    10   10   11   14   15   16   17   19   20   20>")
    .clip(1)
    .gain("<0.55 0.65 0    0    0    0    0.5  0.55 0.6  0.85 0.8  0.9  0.95 0.95 0.85 0.45 0.2>")
    .fadeInTime(0.05)
    .fadeTime(0.1)

)
// ── Master fade-out ──
// Gentle 2-section (30s) fade at the end of the arrangement
// gainEnvelope: full gain for 15/17 of the piece, then linear fade to 0
.gain("<1    1    1    1    1    1    1    1    1    1    1    1    1    1    1    0.5  0.15>")
