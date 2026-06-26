# Strudel Syntax Guide for AI DJs

Strudel is the JavaScript port of Tidal Cycles, a pattern language designed for live coding music. The core idea: **everything is a pattern**, and patterns divide time into cycles. Your goal is to create **authentic, genre-appropriate music** on the first try.

If you need deeper documentation, use context7: `/websites/strudel_cc` (1000+ code examples).

## The Cycle Concept

In Strudel, time is measured in **cycles**, not beats. A cycle is one complete iteration of a pattern. By default, one cycle takes 2 seconds (30 cycles per minute).

```javascript
// This pattern plays 4 sounds in one cycle
s("bd sd hh cp")  // Each sound gets 1/4 of the cycle

// This plays 1 sound per cycle
s("<bd sd hh cp>")  // Each sound alternates across cycles
```

The power of cycles: patterns with different numbers of elements still align because they share cycle boundaries.

---

# Mini-Notation: The Pattern Language

Mini-notation is Strudel's shorthand for writing patterns. Master these operators:

## Sequencing

| Syntax | Name | What It Does | Example |
|--------|------|--------------|---------|
| `space` | Sequence | Events divide the cycle equally | `"bd sd hh cp"` → 4 events per cycle |
| `~` | Rest | Silent gap in pattern | `"bd ~ sd ~"` → kick, silence, snare, silence |
| `[ ]` | Group | Subdivide time further | `"bd [sd sd] hh"` → 3 slots, middle has 2 sounds |
| `[[ ]]` | Nested Group | Deep subdivision | `"bd [[sd sd] hh]"` |

**Key insight**: Spaces divide the current time slot equally. `"a b c"` gives each element 1/3. `"a [b c]"` gives `a` half, and `b` and `c` each 1/4.

## Speed Modifiers

| Syntax | Name | What It Does | Example |
|--------|------|--------------|---------|
| `*` | Multiply | Play faster/more times | `"hh*8"` → 8 hi-hats per cycle |
| `/` | Divide | Play slower, span cycles | `"bd/2"` → once every 2 cycles |
| `@` | Elongate | Stretch duration (weight) | `"c@3 e"` → c gets 3/4, e gets 1/4 |
| `!` | Replicate | Repeat without speeding | `"c!3 e"` → c c c e in same time as c e |

## Alternation & Randomness

| Syntax | Name | What It Does | Example |
|--------|------|--------------|---------|
| `< >` | Slow Sequence | One item per cycle | `"<c3 e3 g3>"` → c3 cycle 1, e3 cycle 2, etc. |
| `\|` | Random Choice | Pick one randomly each cycle | `"bd \| sd \| cp"` |
| `?` | Random Drop | 50% chance to play (or `?0.1` = 10%) | `"hh*8?"` → random gaps |

## Polyphony

| Syntax | Name | What It Does | Example |
|--------|------|--------------|---------|
| `,` | Parallel/Stack | Play simultaneously | `"bd sd, hh*4"` → drums + hi-hats together |
| `:` | Sample Select | Pick sample variation | `"hh:0 hh:1 hh:2"` |

## Euclidean Rhythms

Euclidean rhythms distribute beats as evenly as possible across steps:

| Syntax | What It Does | Example |
|--------|--------------|---------|
| `(beats,steps)` | Distribute beats across steps | `"bd(3,8)"` → 3 kicks across 8 slots |
| `(beats,steps,offset)` | With rotation | `"bd(3,8,2)"` → rotated by 2 |

Common Euclidean patterns:
- `(3,8)` → Cuban tresillo
- `(5,8)` → Cinquillo
- `(7,16)` → West African bell

## Advanced Mini-Notation

| Syntax | Meaning | Example |
|--------|---------|---------|
| `!n` | Repeat previous element n times | `"c3!3 e3"` = `"c3 c3 c3 e3"` |
| `@n` | Give element n units of time | `"c3@3 e3"` = c3 gets 3/4, e3 gets 1/4 |
| `{a b c}%n` | Polyrhythm (n steps) | `"{c3 e3 g3}%8"` |
| `,` | Parallel patterns in mini-notation | `"c3,e3,g3"` = chord |

**Mini-notation confusion to avoid:**
- `"a b"` = sequence (a then b, equal time)
- `"[a b]"` = sub-sequence (a and b squeezed into one step)
- `"<a b>"` = alternate (a on cycle 1, b on cycle 2)
- `","` = parallel (use inside `sound()` or wrap with `stack()`)

---

# Core Functions

## Playing Sounds

### s() / sound() - Sample Playback
The foundation of drum programming. Plays audio samples by name.

```javascript
s("bd sd hh cp")                    // Basic drum pattern
s("bd:0 bd:1 bd:2")                 // Different kick variations (: selects)
s("bd sd").bank("RolandTR909")      // Use specific drum machine
```

### note() - Pitched Notes
Sets pitch using letter notation with optional octave (0-8) and accidentals.

```javascript
note("c3 e3 g3 b3")                 // C major 7 arpeggio
note("c#4 eb4 f#4")                 // Sharps and flats
note("c2").s("sawtooth")            // Synth bass note
note("[c3,e3,g3]")                  // Chord (comma = simultaneous)
note("c2 c3").s("piano")            // Piano with octaves
```

### n() - Numeric Selection
Two uses: select sample variations OR play scale degrees with `.scale()`.

```javascript
// Sample selection (0-indexed)
n("0 1 2 3").s("jazz")              // Cycle through jazz samples

// Scale degrees (0 = root, 1 = 2nd, 2 = 3rd, etc.)
n("0 2 4 7").scale("C:minor")       // C Eb G Bb
n("<0 1 2 3 4 5 6 7>").scale("D:dorian")
```

### scale() - Harmonic Context
Interpret n() values as scale degrees. Format: `"root:mode"`.

**Common scales:**
- Major modes: major, dorian, phrygian, lydian, mixolydian, aeolian, locrian
- Minor variants: minor, harmonic_minor, melodic_minor
- Pentatonics: pentatonic, minor_pentatonic
- Other: blues, chromatic, whole_tone, diminished

```javascript
n("0 2 4 6").scale("C:minor")
n("0 1 2 3").scale("<C:major D:mixolydian>/4")  // Changing scales
```

---

# Layered Composition

## Using `stack()` — Required for The Clawb

In The Clawb, always wrap all patterns in `stack()`. Strudel only plays the last top-level expression — multiple top-level patterns = only the last one plays.

```javascript
// ❌ WRONG — only bass plays
note("c3 e3").sound("sine")
s("hh*8")
s("bd*2")

// ✅ CORRECT — all layers play
stack(
  note("c3 e3").sound("sine"),
  s("hh*8"),
  s("bd*2")
)
```

## Using `$name:` — Named Layers (standalone Strudel)

The `$name:` syntax creates named layers that play simultaneously. Useful outside The Clawb:

```javascript
$kick: s("bd ~ bd ~").bank("RolandTR909")

$snare: s("~ sd ~ sd").bank("RolandTR909").room(0.2)

$hats: s("hh*8").gain("[.4 .6]*4")

$bass: note("g1 ~ g1 g1, ~ ~ eb1 ~").s("sawtooth").lpf(400)
```

**Why layers matter:**
1. Each layer can have different timing/patterns
2. You can mute individual layers with `_$name:`
3. Layers make complex music readable
4. Changes to one layer don't affect others

---

# Sound Sources

## Built-in Synth Oscillators (always available)
- **Basic waves:** sine, triangle, square, sawtooth (or sin, tri, sqr, saw)
- **Super (detuned):** supersaw
- **Other:** pulse, sbd (synthetic bass drum), bytebeat
- **Noise:** white, pink, brown, crackle

## Always-Available Drums
`bd`, `sd`, `hh`, `oh`, `cp`, `rim` (use with `.bank()` for specific machines)

## Common Drum Banks
`RolandTR808`, `RolandTR909`, `LinnDrum`, `AlesisHR16`

## Sample Categories (use listSamples to get exact names)
- **Drum machines:** TR-808, TR-909, LinnDrum, and many more via `.bank()`
- **GM Soundfonts:** Piano, strings, brass, woodwinds, synths, etc.
- **Orchestral (VCSL):** Timpani, strings, recorders, organs
- **World instruments:** Mridangam, balafon, kalimba, etc.
- **Dirt samples:** casio, jazz, metal, space, and more

---

# Audio Effects

## Filters

Filters shape the frequency content of sounds:

```javascript
.lpf(800)              // Low-pass: cut frequencies above 800Hz (darker)
.hpf(200)              // High-pass: cut frequencies below 200Hz (thinner)
.bpf(1000)             // Band-pass: keep only around 1000Hz
.lpq(5)                // Resonance/Q: boost at cutoff (1-20)
.vowel("a e i o u")    // Vowel formant filter
```

### Filter Envelopes

Shape the filter cutoff over each note's lifetime. This is the secret to acid bass, plucky synths, and evolving pads.

```javascript
// Acid bass — high envelope depth, fast decay
note("c2 <eb2 g2>").s("sawtooth")
  .lpf(300)        // base cutoff
  .lpq(8)          // high resonance
  .lpenv(4)        // envelope depth (multiplier of lpf)
  .lpa(0.01)       // attack
  .lpd(0.15)       // decay
  .lps(0)          // sustain at 0 = plucky
  .ftype("24db")   // steeper filter slope

// Slow pad filter
note("c3 e3 g3 b3").s("sawtooth")
  .lpf(sine.slow(8).range(400, 2000))
  .lpq(2)

// Dynamic sweep shorthand
.lpf(2000).lpattack(0.1).lpdecay(0.3).lpsustain(0.2).lpenv(4)
```

## Amplitude

```javascript
.gain(0.7)             // Volume (0-1, can exceed 1 carefully)
.velocity(0.8)         // Velocity multiplier
.postgain(1.2)         // Gain after all effects
```

## ADSR Envelope

Controls how sound evolves over time:

```javascript
.attack(0.1)           // Fade-in time (seconds)
.decay(0.2)            // Time to fall to sustain level
.sustain(0.5)          // Held level (0-1)
.release(0.3)          // Fade-out after note ends
.adsr(".1:.2:.5:.3")   // Shorthand for all four

// Plucky sound
note("c3 e3 g3").s("triangle")
  .attack(0.01).decay(0.2).sustain(0).release(0.1)

// Pad
note("c3 e3 g3").s("sawtooth")
  .attack(0.5).decay(0.3).sustain(0.7).release(1)

// .clip(value) — hard clip note duration (0-1 of cycle step)
note("c3*8").s("sawtooth").clip(0.5)   // staccato
```

## Spatial Effects

```javascript
.pan(0.3)              // Stereo position (0=left, 0.5=center, 1=right)
.room(0.5)             // Reverb amount (0-1)
.roomsize(0.8)         // Reverb size
.delay(0.5)            // Delay wet amount
.delaytime(0.25)       // Delay time (fractions of cycle)
.delayfeedback(0.4)    // Delay feedback (< 1 to avoid runaway)
```

## Distortion

```javascript
.distort(0.5)          // Waveshaping distortion
.crush(4)              // Bit crusher (1-16, lower = crunchier)
.coarse(8)             // Sample rate reduction
.shape(0.5)            // Wave shaping distortion (alternative)
```

## FM Synthesis

```javascript
.fm(2)                 // FM modulation index (brightness)
.fmh(1.5)              // Harmonicity ratio (whole = musical, decimal = metallic)
.fmattack(0.01)        // FM envelope attack
.fmdecay(0.1)          // FM envelope decay

// Evolving FM
note("c3 e3 g3").s("sine")
  .fm(sine.range(1, 6).slow(8))
```

## Additional Effects

| Effect | Range | Description |
|--------|-------|-------------|
| `.phaser(speed)` | 0.1-10 | Phaser modulation speed |
| `.phaserdepth(d)` | 0-1 | Phaser sweep depth |
| `.compressor(threshold)` | -60 to 0 | Dynamic compression (dB) |
| `.bpq(q)` | 0.1-20 | Bandpass filter Q |
| `.hpq(q)` | 0.1-20 | Highpass filter Q/resonance |
| `.noise(amount)` | 0-1 | Add noise to oscillator |
| `.vib(pattern)` | `"rate:depth"` | Vibrato, e.g. `"4:.2"` |
| `.cut(group)` | integer | Cut group — new note in same group cuts previous |

### `.cut()` — Cut Groups

Useful for open/closed hihats and monophonic bass:

```javascript
stack(
  s("hh*8").cut(1),       // closed hihat
  s("oh*2").cut(1),       // open hihat — cuts closed, and vice versa
  note("c2 ~ eb2 ~").s("sawtooth").cut(2)  // mono bass
)
```

## Signal Modulation

Automate any parameter with continuous signals:

```javascript
.lpf(sine.range(200, 2000).slow(4))   // Filter sweep
.gain(saw.range(0.3, 0.8).fast(2))    // Tremolo effect
.pan(sine.range(0, 1).slow(2))        // Auto-pan
.lpf(perlin.slow(2).range(100, 2000)) // Organic, natural movement
```

**Available signals:** sine, cosine, saw, square, tri, rand, perlin

**perlin** is especially useful for organic, evolving textures — it creates smooth random movement that sounds natural and alive.

### Signal Modifiers

```javascript
sine.range(200, 2000)           // Scale to frequency range
perlin.range(0.3, 0.8).slow(4)  // Slow organic movement
saw.segment(8)                  // Quantize to 8 steps
```

### All Signal Types

```javascript
sine                            // 0 to 1, smooth wave
cosine                          // 0 to 1, phase-shifted sine
saw                             // 0 to 1, ramp up
tri                             // 0 to 1, triangle
square                          // 0 or 1, pulse

sine2, saw2, tri2, square2      // -1 to 1 versions

rand                            // Random 0 to 1
perlin                          // Smooth random (organic)
irand(8)                        // Random integer 0-7
```

### Interactive Signals

```javascript
.lpf(mouseX.range(200, 4000))   // Filter follows mouse X
.gain(mouseY.range(0, 1))       // Volume follows mouse Y
```

---

# Advanced Sound Design

### superimpose() — Layer variations
Creates a copy of the pattern with modifications, playing both simultaneously:

```javascript
note("c3 e3 g3").s("supersaw")
  .superimpose(x => x.detune(0.5))     // Detuned copy for thickness
  .superimpose(x => x.add(12))          // Octave up copy

// Slight detune for chorus effect
note("c3 e3 g3").s("sawtooth")
  .superimpose(x => x.add(0.05))

// Delayed fifth above
note("c3 e3 g3").s("sine")
  .superimpose(x => x.add(7).delay(0.25).gain(0.4))
```

### detune() — Analog warmth
Slightly detunes the sound for a thicker, more analog feel:

```javascript
.detune("<0.5>")                        // Subtle detuning
.detune(0.7)                            // More pronounced
```

### layer() — Multiple transformations
Apply different effect chains to the same pattern:

```javascript
note("c2").layer(
  x => x.s("sawtooth").lpf(400),
  x => x.s("square").lpf(800).gain(0.5)
)
```

### .off(time, fn) — Offset echo with transformation

Creates a time-shifted copy with a transformation. Great for call-and-response and canon-like effects.

```javascript
// Echo an octave up, offset by 1/8 cycle
note("c3 e3 g3").s("triangle")
  .off(1/8, x => x.add(12).gain(0.5))

// Multiple offsets for arpeggiated texture
note("c3 e3 g3")
  .off(1/8, x => x.add(7))
  .off(1/4, x => x.add(12).gain(0.3))
```

### .struct(pattern) — Apply rhythmic structure

Imposes a rhythmic template onto a pattern. `x` = play, `~` = rest.

```javascript
// Offbeat pattern
note("c3 e3 g3 bb3").struct("~ x ~ x")

// Complex rhythm
chord("<Am7 Dm7>").voicing().struct("x ~ [x x] ~ x x ~ ~")
```

### .mask(pattern) — Toggle pattern on/off over time

Like struct but uses `1`/`0` and applies across cycles for longer-form arrangement.

```javascript
// Only plays in the second half of a 16-cycle phrase
s("hh*8").gain(0.5).mask("<0@8 1@8>")

// Gradual introduction
s("bd*4").mask("<0@4 1@16>")
```

---

# Pattern Combinators

## Stacking & Sequencing

```javascript
stack(pattern1, pattern2, pattern3)    // Play all simultaneously
cat(pattern1, pattern2)                // Play sequentially, one per cycle
seq(pattern1, pattern2)                // Play sequentially, all in one cycle
polymeter(pattern1, pattern2)          // Align by steps, creates polyrhythm
```

## arrange() — Song Structure
Build full songs with sections:

```javascript
arrange(
  [4, seq(intro)],
  [8, seq(verse)],
  [8, seq(chorus)],
  [4, seq(outro)]
)
```

---

# Probability & Randomness

## Random Modifiers

```javascript
.sometimes(x => x.fast(2))      // 50% chance to apply
.often(x => x.rev())            // 75% chance
.rarely(x => x.add(12))         // 25% chance
.almostAlways(x => x.crush(4))  // 90% chance
.almostNever(x => x.speed(-1))  // 10% chance
```

## Degrading Patterns

```javascript
.degrade()                      // Randomly drop 50% of events
.degradeBy(0.3)                 // Drop 30% of events
```

## Random Selection

```javascript
choose("a", "b", "c")           // Random pick each event
chooseCycles("a", "b", "c")     // Random pick each cycle
wchoose(["a", 3], ["b", 1])     // Weighted: "a" 3x more likely
```

---

# Time & Rhythm Manipulation

## Swing & Groove

```javascript
.swing(3)                       // Add swing to triplet grid
.swingBy(1/6, 4)                // Custom swing amount and subdivision
```

## Pattern Rotation

```javascript
.iter(4)                        // Rotate pattern each cycle
.iterBack(4)                    // Rotate backwards
.palindrome()                   // Play forward then backward
```

## Time Windows

```javascript
.linger(0.25)                   // Loop first 1/4 of pattern
.zoom(0.5, 1)                   // Play only second half
.compress(0.25, 0.75)           // Squeeze into middle 50%
.clip(0.5)                      // Shorten note durations by half
```

## Euclidean Rhythms (Function Form)

```javascript
.euclid(3, 8)                   // 3 hits across 8 steps
.euclidRot(3, 8, 2)             // With rotation
.euclidLegato(5, 8)             // Held notes, no gaps
```

---

# Conditional & Structural

## chunk() — Divide and Transform

```javascript
.chunk(4, x => x.fast(2))       // Apply to 1/4 of pattern, rotating each cycle
.chunkBack(4, x => x.rev())     // Same but backwards
```

## every() — Periodic Transforms

```javascript
.every(4, x => x.rev())         // Apply every 4th cycle
.every(3, x => x.fast(2))       // Every 3rd cycle
.firstOf(4, x => x.crush(4))    // Apply on 1st of every 4
.lastOf(4, x => x.speed(-1))    // Apply on last of every 4
```

## Arpeggiation

```javascript
note("[c3,e3,g3]").arp("0 1 2 1")   // Arpeggiate chord
note("[c3,e3,g3]").arp("<0 [1 2]>") // Pattern the arpeggio
```

## pick() — Select from Lists

Essential for song sections and variations:

```javascript
"<0 1 2>".pick([
  s("bd sd"),           // Index 0
  s("hh*4"),            // Index 1
  s("cp ~ cp ~")        // Index 2
])

// With restart — patterns restart when selected
"<0 1 0 2>".pickRestart([patternA, patternB, patternC])
```

---

# Core Pattern Transforms

```javascript
.fast(2)                        // Double speed
.slow(2)                        // Half speed
.early(0.25)                    // Shift earlier by 1/4 cycle
.late(0.125)                    // Shift later
.rev()                          // Reverse the pattern
.ply(2)                         // Repeat each event N times
.add("<0 2 4>")                 // Add to note values (transpose)
```

## Stereo & Layering

```javascript
.jux(rev)                       // Original left, modified right
.juxBy(0.5, x => x.fast(2))     // Partial stereo width
.off(1/8, x => x.add(7))        // Delayed, modified copy
```

---

# Tonal & Harmonic Functions

## Chord Symbols

```javascript
chord("Am7")                    // A minor 7
chord("<C Am F G>")             // Chord progression
chord("Bb^7")                   // Bb major 7
chord("F#m7b5")                 // Half-diminished
```

### Common Chord Symbols

| Symbol | Meaning | Example |
|--------|---------|---------|
| `C` | Major triad | `chord("C")` |
| `Cm` / `Cm7` | Minor / minor 7th | `chord("Cm7")` |
| `C^7` | Major 7th | `chord("C^7")` |
| `C7` | Dominant 7th | `chord("C7")` |
| `C7b13` | Dominant with alterations | `chord("C7b13")` |
| `Cdim` / `Co` | Diminished | `chord("Co")` |
| `Cm7b5` | Half-diminished | `chord("Cm7b5")` |
| `Csus4` | Suspended 4th | `chord("Csus4")` |

## Automatic Voicing

```javascript
chord("<Cm7 Fm7 G7>")
  .voicing()                    // Auto voice leading
  .anchor("G3")                 // Keep voicing near G3

chord("<Am F C G>")
  .dict("lefthand")             // Use left-hand voicing dictionary
  .voicing()
```

### Voicing Controls

```javascript
// .anchor() sets the target pitch center for voice leading
chord("<C Am F G>").anchor("D5").voicing()

// .mode() controls voicing placement relative to anchor
//   "below" — top note at/below anchor
//   "above" — bottom note at/above anchor
//   "root"  — root of chord near anchor
chord("<C^7 A7b13 Dm7 G7>").mode("root:g2").voicing()

// .n() selects individual chord tones (0 = root, 1 = third, etc.)
n("0 1 2 3").chord("<C Am F G>").voicing()

// .set() inherits chord context for melodic lines
n("<0!3 1*2>").set(chords).mode("root:g2").voicing().s("gm_acoustic_bass")
```

### Scales & Melodic Lines

```javascript
// Scale-based melodies — n() picks scale degree, .scale() sets the scale
n("<3 0 -2 -1>*4")
  .scale("G:minor")
  .s("gm_synth_bass_1")

// .scaleTranspose() shifts through scale degrees
n("0 2 4 6").scale("C:major")
  .scaleTranspose("<0 -1 2 1>*4")

// Combine scales with chords for melodic movement over changes
"[-8 [2,4,6]]*4"
  .scale("C major")
  .scaleTranspose("<0 -1 2 1>*4")
```

## Root Notes for Bass

```javascript
"<Cm7 Fm7 G7 Cm7>".rootNotes(2)  // Extract roots at octave 2
  .struct("x ~ x ~")
  .s("sawtooth")
```

## Transposition

```javascript
.transpose(12)                  // Up one octave
.transpose(-5)                  // Down a fourth
.scaleTranspose(2)              // Up 2 scale degrees (stays in key)
```

## Complete Harmonic Example

```javascript
// Jazz-influenced electronic — chords + bass + melody from same progression
let chords = chord("<Am7 Dm7 G7 C^7>").dict('ireal')
stack(
  // Chords — rhythmic stabs
  chords.struct("[~ x]*2").voicing()
    .s("sawtooth").lpf(600).room(0.5).gain(0.3),
  // Bass — root notes
  n("0").set(chords).mode("root:g2").voicing()
    .s("sawtooth").lpf(400).gain(0.5),
  // Melody — scale tones over changes
  n("[0 <4 3 <2 5>>*2](<3 5>,8)")
    .set(chords).anchor("D5").voicing()
    .s("sine").delay(0.3).room(0.4).gain(0.4)
)
```

---

# Sample Manipulation

## Granular / Choppy Effects

```javascript
.chop(16)                       // Chop sample into 16 pieces
.striate(8)                     // Granular playback across 8 slices
.slice(8, "0 3 2 1 5 4 7 6")    // Reorder 8 slices
```

## Sample Regions

```javascript
.begin(0.25)                    // Start at 25% of sample
.end(0.75)                      // End at 75%
.loopAt(2)                      // Fit sample to 2 cycles
.speed(2)                       // Double speed (octave up)
.speed(-1)                      // Reverse playback
```

---

# Tempo

Strudel uses **cycles per minute (cpm)**, not beats per minute.

**Conversion:** For 4/4 music, `cpm = bpm / 4`

```javascript
setCpm(120/4)          // 120 BPM = 30 cpm (global)
setCpm(90/4)           // 90 BPM
setCpm(140/4)          // 140 BPM techno
.cpm(140/4)            // Pattern-specific tempo
```

Default: 30 cpm (one cycle every 2 seconds, effectively 120 BPM in 4/4).

---

# Visual Feedback

Strudel has built-in visualization functions. **Always use `.pianoroll()` on your patterns** — it gives the audience (and you) visual feedback of what's playing. There are two rendering modes:

- **Global (background):** `.pianoroll()` — renders behind the code editor
- **Inline (embedded):** `._pianoroll()` — renders below the pattern in the code

### `.pianoroll(options?)`

Scrolling piano roll showing note events over time. This is the primary visual feedback tool.

```javascript
// Basic pianoroll
note("c3 e3 g3 b3").s("sawtooth").pianoroll()

// With labels showing note names
note("c2 a2 eb2").euclid(5,8).s("sawtooth")
  .lpenv(4).lpf(300)
  .pianoroll({ labels: 1 })

// Inline pianoroll (below the pattern)
note("c3 e3 g3")._pianoroll()
```

#### Pianoroll Options

| Option | Type | Description |
|--------|------|-------------|
| `labels` | 0/1 | Show note name labels |
| `vertical` | 0/1 | Vertical orientation |
| `fold` | 0/1 | Fold notes into single octave |
| `smear` | 0/1 | Trail effect on notes |
| `cycles` | number | How many cycles to show |
| `autorange` | 0/1 | Auto-fit to note range |
| `active` | string | Color for active notes |
| `inactive` | string | Color for past notes |
| `background` | string | Background color |
| `playheadColor` | string | Playhead line color |

### Other Visualizations

```javascript
._scope({ height: 120, scale: 0.5 })  // Oscilloscope (reliable)
._pianoroll({ fold: 1 })               // Folded pianoroll (reliable)
._punchcard()                          // Pattern events as dots
```

---

# Transition Techniques

These are essential for smooth DJ sets:

### Filter Sweep

```javascript
// Gradually open the filter over several pushes:
note("c3 e3 g3").sound("sawtooth").lpf(400)   // push 1: muffled
note("c3 e3 g3").sound("sawtooth").lpf(800)   // push 2: opening up
note("c3 e3 g3").sound("sawtooth").lpf(2000)  // push 3: bright
```

### Volume Fade

```javascript
// Bring in a new element quietly, then raise it:
sound("hh*8").gain(0.1)   // push 1: barely audible
sound("hh*8").gain(0.3)   // push 2: present
sound("hh*8").gain(0.6)   // push 3: prominent
```

### Gradual Complexity

```javascript
// Start simple, add layers:
sound("bd bd bd bd")                                    // push 1: just kicks
stack(sound("bd bd bd bd"), sound("hh*8").gain(0.3))   // push 2: add hats
```

---

# Common Pitfalls (AI-specific)

These are frequent mistakes LLMs make with Strudel:

| Wrong | Correct | Why |
|---|---|---|
| `bpm(120)` | `setcpm(120/4)` | No `bpm()` function in Strudel |
| `setcps(2)` for 120 BPM | `setcpm(120/4)` | `setcps` is Hz, not intuitive |
| `{bd sd}` | `[bd sd]` | `{}` is TidalCycles polyrhythm, not Strudel |
| `note("c4") # gain 0.5` | `note("c4").gain(0.5)` | `#` is Haskell, not JS |
| `d1 $ sound "bd"` | `sound("bd")` | `d1 $` is TidalCycles, not Strudel |
| `note("c")` | `note("c4")` | Always include octave number |
| `.sound("sawtooth wave")` | `.sound("sawtooth")` | No "wave" suffix |
| `stack([pat1, pat2])` | `stack(pat1, pat2)` | `stack` takes spread args, not array |

---

# Genre Reference

When a user requests a specific genre, nail the authentic sound immediately. Here are the key characteristics:

## 80s Synthwave / Stranger Things
```javascript
setcps(0.7)  // Slower tempo feels more cinematic

$arp: n("0 2 4 6 7 6 4 2")
  .scale("c3:major")
  .s("supersaw")
  .distort(0.7)
  .superimpose(x => x.detune("<0.5>"))
  .lpf(perlin.slow(2).range(100, 2000))
  .lpenv(perlin.slow(3).range(1, 4))
  .gain(0.3)
```
**Key elements:** supersaw with detuning, perlin-modulated filter, distortion, slow arpeggios

## House / Four-on-the-floor
```javascript
setCpm(124/4)
$kick: s("bd*4").bank("RolandTR909").gain(0.95)
$hats: s("~ hh ~ hh, hh*8").bank("RolandTR909").gain(0.4)
$bass: note("c2 c2 ~ c2").s("sawtooth").lpf(600).gain(0.6)
```
**Key elements:** TR-909, steady kick, offbeat hats, punchy bass

## Techno
```javascript
setCpm(130/4)
$kick: s("bd*4").bank("RolandTR909").gain(0.95)
$synth: note("a1").s("sawtooth").lpf(sine.range(300, 1500).slow(8)).gain(0.5).distort(0.2)
```
**Key elements:** Driving kick, modulated filter sweeps, minimal but intense

## Lo-fi Hip Hop
```javascript
setCpm(85/4)
$drums: s("bd ~ [~ bd] ~, ~ sd ~ sd").bank("RolandTR808").gain(0.8).room(0.3)
$keys: note("<[e3,g3,b3] [d3,f#3,a3]>").s("piano").lpf(2000).room(0.5).gain(0.3)
```
**Key elements:** Slow tempo, TR-808, jazzy chords, lots of reverb, warm lo-pass filter

## Drum & Bass
```javascript
setCpm(174/4)
$kick: s("bd ~ ~ ~, ~ ~ bd ~").bank("RolandTR909")
$snare: s("~ sd ~ sd").bank("RolandTR909")
$bass: note("e1 ~ [e1 g1] ~").s("sawtooth").lpf(sine.range(200, 800).slow(4)).distort(0.15)
```
**Key elements:** Fast tempo (170-180 BPM), syncopated kick, rolling bass

## Ambient
```javascript
setCpm(70/4)
$pad: note("<[c3,e3,g3,b3] [a2,c3,e3,g3]>")
  .s("supersaw")
  .lpf(sine.range(800, 2000).slow(16))
  .attack(0.5).release(1)
  .room(0.8).gain(0.2)
```
**Key elements:** Slow evolving pads, long attack/release, heavy reverb, subtle movement

---

# Mix Guidelines

## Level Balancing

Getting gain levels right is critical for a professional sound:

| Layer | Gain Range | Notes |
|-------|-----------|-------|
| **Drums** | 0.7 – 1.0 | Foundation, keep prominent |
| **Bass** | 0.5 – 0.7 | Present but not overpowering |
| **Pads / Chords** | 0.2 – 0.4 | Fill space without competing |
| **Leads / Melodies** | 0.3 – 0.5 | Cut through but sit in the mix |

## Making It Sound Professional

1. **Add movement** with `perlin` or `sine` modulation on filters — static sounds are boring
2. **Use `superimpose()` + `detune()`** for thickness and analog warmth
3. **Use `perlin.range()` on filter cutoffs** for organic, evolving textures
4. **Shape every sound** with filter envelopes and ADSR — don't play raw oscillators
5. **Set tempo** with `setCpm(bpm/4)` at the start
6. **Use advanced techniques freely** — `superimpose`, `detune`, `perlin` modulation make music sound alive

---

# Complete Examples

### Full Track Example

```javascript
setCpm(128/4)

stack(
  // Kick
  s("bd ~ bd ~, ~ ~ ~ bd:1").bank("RolandTR909").gain(0.95),

  // Snare
  s("~ sd ~ sd").bank("RolandTR909").gain(0.8).room(0.2),

  // Hi-hats
  s("hh*8").bank("RolandTR909").gain("[.4 .6]*4").pan(sine.range(0.3, 0.7)),

  // Bass — sawtooth with filter modulation
  note("g1 ~ g1 g1, ~ ~ eb1 ~")
    .s("sawtooth")
    .lpf(sine.range(200, 800).slow(4))
    .gain(0.6)
    .distort(0.15),

  // Pad — supersaw chords
  note("<[g3,bb3,d4] [eb3,g3,bb3] [c3,eb3,g3] [d3,f3,a3]>")
    .s("supersaw")
    .lpf(1200)
    .gain(0.25)
    .attack(0.2)
    .release(0.5)
    .room(0.6),

  // Lead — scale-based melody with delay
  n("0 ~ 2 3 ~ 5 7 ~")
    .scale("G:minor")
    .s("triangle")
    .lpf(2000)
    .gain(0.35)
    .delay(0.3)
    .delaytime(3/8)
    .delayfeedback(0.3)
).pianoroll({ labels: 1 })
```

### Coastline by Eddyflux

```javascript
// "coastline" @by eddyflux
samples('github:eddyflux/crate')
setcps(.75)
let chords = chord("<Bbm9 Fm9>/4").dict('ireal')
stack(
  stack( // DRUMS
    s("bd").struct("<[x*<1 2> [~@3 x]] x>"),
    s("~ [rim, sd:<2 3>]").room("<0 .2>"),
    n("[0 <1 3>]*<2!3 4>").s("hh"),
    s("rd:<1!3 2>*2").mask("<0 0 1 1>/16").gain(.5)
  ).bank('crate')
  .mask("<[0 1] 1 1 1>/16".early(.5))
  , // CHORDS
  chords.offset(-1).voicing().s("gm_epiano1:1")
  .phaser(4).room(.5)
  , // MELODY
  n("<0!3 1*2>").set(chords).mode("root:g2")
  .voicing().s("gm_acoustic_bass"),
  chords.n("[0 <4 3 <2 5>>*2](<3 5>,8)")
  .anchor("D5").voicing()
  .segment(4).clip(rand.range(.4,.8))
  .room(.75).shape(.3).delay(.25)
  .fm(sine.range(3,8).slow(8))
  .lpf(sine.range(500,1000).slow(8)).lpq(5)
  .rarely(ply("2")).chunk(4, fast(2))
  .gain(perlin.range(.6, .9))
  .mask("<0 1 1 0>/16")
)
.late("[0 .01]*4").late("[0 .01]*2").size(4)
```

### Break Beat

```javascript
// "broken cut 1" @by froos
samples('github:tidalcycles/dirt-samples')
samples({
  'slap': 'https://cdn.freesound.org/previews/495/495416_10350281-lq.mp3',
  'whirl': 'https://cdn.freesound.org/previews/495/495313_10350281-lq.mp3',
  'attack': 'https://cdn.freesound.org/previews/494/494947_10350281-lq.mp3'
})

setcps(1.25)

note("[c2 ~](3,8)*2,eb,g,bb,d").s("sawtooth")
  .noise(0.3)
  .lpf(perlin.range(800,2000).mul(0.6))
  .lpenv(perlin.range(1,5)).lpa(.25).lpd(.1).lps(0)
  .add.mix(note("<0!3 [1 <4!3 12>]>")).late(.5)
  .vib("4:.2")
  .room(1).roomsize(4).slow(4)
  .stack(
    s("bd").late("<0.01 .251>"),
    s("breaks165:1/2").fit()
    .chop(4).sometimesBy(.4, ply("2"))
    .sometimesBy(.1, ply("4")).release(.01)
    .gain(1.5).sometimes(mul(speed("1.05"))).cut(1)
    ,
    s("<whirl attack>?").delay(".8:.1:.8").room(2).slow(8).cut(2),
  ).reset("<x@30 [x*[8 [8 [16 32]]]]@2>".late(2))
```

### Acid House

```javascript
// "acidic tooth" @by eddyflux
  setcps(1)
  stack(
    note("[<g1 f1>/8](<3 5>,8)")
    .clip(perlin.range(.15,1.5))
    .release(.1)
    .s("sawtooth")
    .lpf(sine.range(400,800).slow(16))
    .lpq(cosine.range(6,14).slow(3))
    .lpenv(sine.mul(4).slow(4))
    .lpd(.2).lpa(.02)
    .ftype('24db')
    .rarely(add(note(12)))
    .room(.2).shape(.3).postgain(.5)
    .superimpose(x=>x.add(note(12)).delay(.5).bpf(1000))
    .gain("[.2 1@3]*2") // fake sidechain
    ,
    stack(
      s("bd*2").mask("<0@4 1@16>"),
      s("hh*8").gain(saw.mul(saw.fast(2))).clip(sine)
      .mask("<0@8 1@16>")
    ).bank('RolandTR909')
  )
```

### Deep House with Chord Progression

```javascript
// "deep house foundation" — chord-driven with bass and percussion
setcpm(124/4)
let chords = chord("<Fm9 Bbm7 Eb7 Ab^7>").dict('ireal')
stack(
  // Pad — voiced chords with phaser
  chords.struct("[~ x]*2").voicing()
    .s("sawtooth").lpf(900).room(0.5).phaser(2)
    .superimpose(x => x.add(0.04))
    .gain(0.2),
  // Bass — root notes, filter envelope
  n("0").set(chords).mode("root:g2").voicing()
    .s("sawtooth").lpf(300).lpq(6)
    .lpenv(3).lpd(0.2).lps(0)
    .gain(0.5),
  // Melody — chord tones with delay
  n("[0 <4 3 2>*2](<3 5>,8)")
    .set(chords).anchor("D5").voicing()
    .s("sine").delay(0.3).room(0.4)
    .clip(perlin.range(0.3, 0.8))
    .gain(0.35),
  // Drums
  stack(
    s("bd*4"),
    s("~ sd").room(0.2),
    s("hh*8").gain(saw.mul(saw.fast(2))).degradeBy(0.2)
  ).bank('RolandTR909')
).pianoroll({ labels: 1 })
```

### Ambient Techno with Scales

```javascript
// "ambient pulse" — scale-based melody over evolving texture
setcpm(118/4)
stack(
  // Melodic sequence — scale degrees
  n("<0 2 4 7 9 11 7 4>")
    .scale("D:dorian")
    .s("triangle")
    .off(1/8, x => x.add(12).gain(0.3))
    .lpf(sine.range(500, 3000).slow(16))
    .delay(0.4).delaytime(3/8).delayfeedback(0.5)
    .room(0.6).gain(0.35),
  // Sub bass
  n("<0 3>/2").scale("D:dorian")
    .s("sine").gain(0.5)
    .lpf(200),
  // Percussion
  stack(
    s("bd ~ [bd ~] ~"),
    s("~ cp").room(0.3).delay(0.25),
    s("hh*8").struct("x ~ x x ~ x ~ x").gain(0.3)
  ).sometimes(ply(2))
).pianoroll({ labels: 1, smear: 1 })
```
