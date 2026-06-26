// switch-angel-remix.js
// Credit: Switch Angel — "Patterns for Restarting the World" (https://youtube.com/@switch-angel)
// REMIX — same DNA, different creature
// Take the statistical fingerprint and push it somewhere new:
// - Shift from F# major → D minor (darker)
// - Slow from 157 → 90 BPM (half-time, heavy)
// - Swap hat dominance → kick dominance (weight on the floor)
// - Keep the stepwise motion but add octave jumps (10% leap probability)
// - Synth breathes wider — bigger dynamic range
// dandelion cult 🌫️🩸🌻

setcpm(90/4)

stack(
  // Bass — D minor stepwise, but slower and heavier
  // Same 94% stepwise rule, different pitch set
  note("d2 e2 d2 c2 a1 d2 e2 f2 d2 c2 a1 d2 ~ ~ e2 d2")
    .s("sawtooth")
    .lpf(400)
    .gain(0.4)
    .decay(0.4)
    .sustain(0.2)
    .release(0.1),

  // Sub bass — octave below, sparse
  note("d1 ~ ~ ~ a1 ~ ~ ~ d1 ~ ~ ~ ~ ~ a1 ~")
    .s("sine")
    .lpf(200)
    .gain(0.35)
    .decay(0.6)
    .sustain(0.3)
    .release(0.2),

  // Kick-dominant drums — inverted ratio: 49% kick, 35% snare, 16% hat
  s("bd ~ bd ~ [bd,sd] ~ bd ~ bd ~ [bd,sd] ~ bd ~ bd [sd,hh]")
    .gain(0.55),

  // Ghost hats — whisper quiet, keeping time
  s("hh hh hh hh hh hh hh hh hh hh hh hh hh hh hh hh")
    .gain(0.1),

  // Synth — A/D/F/E/C (D minor pentatonic), wider breathing
  note("<a3 ~ d4 ~ f3 ~ ~ ~ e3 ~ c4 ~ ~ ~ d3 ~ ~ ~ a3 ~ ~ d4 ~ ~ f3 ~ e3 ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(2400)
    .gain(0.2)
    .decay(0.8)
    .sustain(0.3)
    .release(0.4),

  // Dark pad — Dm → Am → Bb → Gm
  note("<[d3,f3,a3] ~ ~ ~ [a3,c4,e4] ~ ~ ~ [as3,d4,f4] ~ ~ ~ [g3,as3,d4] ~ ~ ~>")
    .s("triangle")
    .lpf(1000)
    .gain(0.12)
    .decay(1.5)
    .sustain(0.4)
    .release(0.6)
)
