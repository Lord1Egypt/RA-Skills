// switch-angel-clone.js
// Credit: Switch Angel — "Patterns for Restarting the World" (https://youtube.com/@switch-angel)
// CLONE — faithful reproduction of Switch Angel's statistical DNA
// Same scale, same rhythm density, same stepwise motion, same hat dominance
// The closest we can get to "playing back" the original's feel
// dandelion cult 🌫️🩸🌻

setcpm(157/4)

stack(
  // Bass — C#/D/F#/C/B emphasis, 94.6% stepwise, granular 16th notes
  note("cs2 d2 cs2 c2 b1 cs2 d2 cs2 fs1 cs2 d2 c2 b1 cs2 d2 b1")
    .s("sawtooth")
    .lpf(500)
    .gain(0.3)
    .decay(0.15)
    .sustain(0.1)
    .release(0.05),

  // Hat-dominant drums — 49% hat, 35% snare, 16% kick, uniform subdivision
  s("hh hh [sd,hh] hh hh hh [sd,hh] hh hh [sd,hh] hh hh hh [sd,hh] hh hh")
    .gain(0.35),

  // Kick — sparse anti-grid placement (not on downbeats)
  s("~ ~ ~ bd ~ ~ ~ ~ ~ ~ bd ~ ~ ~ ~ bd")
    .gain(0.5),

  // Synth — D#/B/F#/C#/D pentatonic, stepwise, drone
  note("ds2 b1 fs2 cs2 d2 ~ b1 ds2 cs2 ~ d2 ~ b1 ds2 ~ cs2")
    .s("triangle")
    .lpf(1800)
    .gain(0.15)
    .decay(0.7)
    .sustain(0.4)
    .release(0.3),

  // Pad — F# major sustained
  note("<[fs3,as3,cs4] ~ ~ ~ ~ ~ ~ ~ [b3,ds4,fs4] ~ ~ ~ ~ ~ ~ ~>")
    .s("triangle")
    .lpf(1200)
    .gain(0.08)
    .decay(1.2)
    .sustain(0.5)
    .release(0.5)
)
