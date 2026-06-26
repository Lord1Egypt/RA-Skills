// solarstone-ptr-477-clone.js
// Clone of Solarstone — Pure Trance Radio Ep. 477, segment ~35:00–41:00
// Progressive trance, 128 BPM, C# minor
// Demucs 4-stem separation → WAV samples → simultaneous playback
// dandelion cult 🌻🌫️🩸 — 2026-02-25
//
// Credit: Solarstone — https://www.solarstone.co.uk/
// Source: Pure Trance Radio Episode 477
//
// This is a reconstruction clone: all 4 stems play simultaneously
// from start to finish with no manipulation. The recombined output
// should be perceptually identical to the original segment.
// The clone proves the pipeline works; the remix transforms it.

setcpm(32) // 128 BPM → CPS = 32/60 ≈ 0.5333

// Each stem triggers once across 192 cycles (360s).
// .slow(192) stretches one event to span the full piece.
// .clip(1) tells the renderer to let the sample play its natural duration.

stack(
  // Drums — the backbone
  s("solardrum")
    .slow(192)
    .clip(1)
    .gain(0.8),

  // Bass — the low end
  s("solarbass")
    .slow(192)
    .clip(1)
    .gain(0.8),

  // Other (synths, pads, FX) — the atmosphere
  s("solarother")
    .slow(192)
    .clip(1)
    .gain(0.75),

  // Vocals — sparse in trance, but present
  s("solarvox")
    .slow(192)
    .clip(1)
    .gain(0.7)
)
