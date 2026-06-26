// peace-piece-silas.js
// Silas's voicing diagnostic — decomposing Bill Evans "Peace Piece" (1958)
// using Strudel's theory tools: chord(), voicing(), anchor(), arrange(), sine envelopes
//
// Credit: Bill Evans — Peace Piece [Everybody Digs Bill Evans, Riverside Records, 1958]
//
// The two-chord vamp: Cmaj7 → G9sus (G dominant 9 suspended)
// If we can't extract harmonic intent from a two-chord piece, nothing harder will work.
//
// This is a LEARNING exercise — practicing the new theory patterns,
// not cloning Evans's playing. The voicing system handles voice-leading;
// we handle form and texture.
//
// dandelion cult 🌫️ — 2026-02-26

// ═══════════════════════════════════════════════════════════════════
// TEMPO: ~50 BPM effective. Peace Piece is rubato, but we need
// a clock. Each cycle = one bar of the vamp (2 beats per chord).
// At CPS 0.2, one cycle = 5 seconds. 80 cycles = 6:40.
// We'll use 48 cycles at CPS 0.25 → 4 sec/cycle → 3:12.
// ═══════════════════════════════════════════════════════════════════
setcps(0.25)

// ═══════════════════════════════════════════════════════════════════
// THE HARMONIC AUTHORITY
//
// chord() creates a pattern of chord symbols. This is the single
// source of truth — every layer derives from this progression.
// The angle brackets make it a slowcat: one chord per half-cycle.
//
// C^7 = Cmaj7 (C E G B)
// G9sus = G9 suspended (G C D F A) — the Evans voicing
// ═══════════════════════════════════════════════════════════════════
const prog = chord("<C^7 G9sus>")

// ═══════════════════════════════════════════════════════════════════
// LAYER 1: PAD — voice-led chords
//
// .anchor("C4") sets the center of gravity for voicings.
// .voicing() resolves chord symbols into actual notes with
// minimal voice movement between changes. This is the magic —
// instead of manually spelling out inversions, the system
// finds the smoothest path.
//
// .s("triangle") uses a warm triangle wave oscillator.
// .gain(sine.range().slow()) creates a breathing energy curve
// that rises and falls over many cycles.
// ═══════════════════════════════════════════════════════════════════
const pad = prog
  .anchor("C4")
  .voicing()
  .s("triangle")
  .gain(sine.range(0.04, 0.12).slow(24))
  .attack(0.8)
  .decay(0.3)
  .sustain(0.5)
  .release(1.0)
  .clip(1)
  .pan(sine.range(0.35, 0.65).slow(32))

// ═══════════════════════════════════════════════════════════════════
// LAYER 2: BASS — root notes derived from the progression
//
// .rootNotes(octave) extracts just the root of each chord
// at the specified octave. No manual note spelling needed.
// The progression IS the bass line.
// ═══════════════════════════════════════════════════════════════════
const bass = prog
  .rootNotes(2)
  .s("sine")
  .gain(sine.range(0.06, 0.18).slow(20))
  .attack(0.1)
  .decay(0.2)
  .sustain(0.6)
  .release(0.4)
  .clip(1)

// ═══════════════════════════════════════════════════════════════════
// LAYER 3: HIGH PAD — same voicings, higher register
//
// By changing anchor to C5, we get the same voice-leading logic
// but in a higher register. The voicing system maintains smooth
// movement at both octaves independently.
// ═══════════════════════════════════════════════════════════════════
const highPad = prog
  .anchor("C5")
  .voicing()
  .s("sine")
  .gain(sine.range(0.01, 0.06).slow(28))
  .attack(1.2)
  .decay(0.5)
  .sustain(0.4)
  .release(1.5)
  .clip(1)
  .pan(sine.range(0.2, 0.8).slow(20))

// ═══════════════════════════════════════════════════════════════════
// LAYER 4: MELODIC FRAGMENT — fifths from the chord
//
// Using the voicing but only taking the top note creates
// a melodic line that follows the harmony. The .struct()
// creates rhythmic variation — not every beat sounds.
// ═══════════════════════════════════════════════════════════════════
const melody = prog
  .anchor("C5")
  .voicing()
  .s("triangle")
  .struct("~ t ~ ~ t ~ t ~")
  .gain(sine.range(0.02, 0.08).slow(16))
  .attack(0.05)
  .decay(0.3)
  .sustain(0.3)
  .release(0.6)
  .pan(sine.range(0.3, 0.7).slow(12))

// ═══════════════════════════════════════════════════════════════════
// LAYER 5: PEACE PIECE SAMPLES — Evans's actual recording
//
// Using slices of the original as textural ground.
// .n() selects which 30-second slice to play.
// These are long samples, so clip(1) lets them ring for one cycle.
// The gain envelope fades them in during the middle section.
// ═══════════════════════════════════════════════════════════════════
const sampleLayer = s("peace")
  .n("<0 1 2 3 4 5 6 7>")
  .clip(1)
  .gain(sine.range(0.0, 0.08).slow(16))
  .speed(1)

// ═══════════════════════════════════════════════════════════════════
// MACRO FORM: arrange()
//
// arrange() replaces the old 120-value per-bar gain arrays.
// Each section is [numCycles, pattern]. The patterns play for
// exactly that many cycles, then the next section begins.
// This is WAY cleaner than manual gain tables.
//
// Form:
//   Intro (8 cycles, 32s):  Bass alone — establishing the vamp
//   Build (8 cycles, 32s):  Pad enters — harmony opens up
//   Body  (16 cycles, 64s): Full texture — all layers, samples
//   Peak  (8 cycles, 32s):  Maximum density, high pad prominent
//   Decay (8 cycles, 32s):  Layers withdraw, melody fragments remain
//   Outro (4 cycles, 16s):  Bass alone again — symmetry with intro
//
// Total: 52 cycles × 4 sec = 3:28
// ═══════════════════════════════════════════════════════════════════
arrange(
  // ─── INTRO: bass alone, the root establishes itself ───
  [8, stack(
    bass.gain(sine.range(0.08, 0.14).slow(16))
  )],

  // ─── BUILD: pad enters, breathing slowly ───
  [8, stack(
    bass.gain(sine.range(0.10, 0.16).slow(16)),
    pad.gain(sine.range(0.02, 0.08).slow(12))
  )],

  // ─── BODY: full texture, Evans's piano underneath ───
  [16, stack(
    bass.gain(sine.range(0.12, 0.18).slow(20)),
    pad.gain(sine.range(0.06, 0.14).slow(16)),
    melody.gain(sine.range(0.02, 0.06).slow(10)),
    sampleLayer.gain(sine.range(0.02, 0.06).slow(12))
  )],

  // ─── PEAK: high pad enters, maximum harmonic density ───
  [8, stack(
    bass.gain(sine.range(0.14, 0.20).slow(16)),
    pad.gain(sine.range(0.08, 0.16).slow(12)),
    highPad.gain(sine.range(0.03, 0.08).slow(10)),
    melody.gain(sine.range(0.04, 0.08).slow(8)),
    sampleLayer.gain(sine.range(0.01, 0.04).slow(8))
  )],

  // ─── DECAY: layers fall away ───
  [8, stack(
    bass.gain(sine.range(0.06, 0.12).slow(16)),
    pad.gain(sine.range(0.02, 0.06).slow(12)),
    melody.gain(sine.range(0.01, 0.03).slow(8))
  )],

  // ─── OUTRO: bass alone, returning to silence ───
  [4, stack(
    bass.gain(sine.range(0.04, 0.08).slow(16))
  )]
)
