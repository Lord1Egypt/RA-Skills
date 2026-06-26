# Meta-Tags & Structure Reference (V5 Updated)

Meta-tags in [brackets] guide Suno's structure, vocals, and production. V5 honors tags more consistently, especially in Studio Timeline.

## V5 Prompting Best Practices

- **Front-load control**: Put key tags in first 3-5 lines
- **Keep it tight**: 1-2 genres + 1 mood + optional instruments
- **Syllable count**: 6-12 syllables per line for best vocal alignment
- **Use callbacks on Extend**: "continue with same vibe as chorus"
- **Negative prompting**: Add exclusions in style prompt ("no guitars", "no harsh distortion")

## Structure Tags

Place in lyrics field between brackets `[ ]` to control song structure.

### Essential Tags

| Tag | Purpose |
|-----|---------|
| `[Intro]` | Instrumental or soft vocal opening |
| `[Verse]` / `[Verse 1]` | Main narrative section |
| `[Pre-Chorus]` | Tension build before chorus |
| `[Chorus]` | Main hook, most memorable part |
| `[Post-Chorus]` | Energy maintenance after chorus |
| `[Bridge]` | Melodic/harmonic variation |
| `[Break]` | Instrumental pause, drum drop |
| `[Hook]` | Catchy repeated phrase |
| `[Interlude]` | Instrumental passage between sections |
| `[Outro]` | Song conclusion |
| `[End]` | Explicit ending marker |
| `[Fade Out]` | Progressive fade to silence |

### Instrumental Tags

| Tag | Purpose |
|-----|---------|
| `[Instrumental]` | Section without vocals |
| `[Guitar Solo]` | Guitar solo section |
| `[Piano Solo]` | Piano solo section |
| `[Synth Solo]` | Synthesizer solo |
| `[Drum Break]` | Drum-focused section |
| `[Drop]` | EDM-style bass drop |
| `[Build]` | Rising tension section |

## Control Tags

### Energy & Mood

```
[Mood: Uplifting]
[Mood: Dark]
[Mood: Melancholic]
[Mood: Aggressive]
[Mood: Peaceful]
[Mood: Triumphant]
[Energy: Low]
[Energy: Medium]
[Energy: High]
[Energy: Rising]
[Energy: Maximum]
[Energy: Medium→High]
```

### Emotional Verse Tags (V5)

V5 interprets emotional modifiers on sections:
```
[angry verse]
[sad verse]
[whimsical verse]
[hopeful chorus]
[melancholic bridge]
```

### Instrumentation

```
[Instrument: Piano]
[Instrument: Acoustic Guitar]
[Instrument: Electric Guitar (Distorted)]
[Instrument: Electric Guitar (Clean)]
[Instrument: Strings (Legato)]
[Instrument: Strings (Staccato)]
[Instrument: Brass]
[Instrument: Synth Pads]
[Instrument: 808 Bass]
[Instrument: Bright Electric Guitars, Live Drums]
```

### Texture & Era Tags (V5)

```
[Texture: Tape-Saturated]
[Texture: Vinyl Hiss]
[Texture: Lo-fi]
[Texture: Crisp Digital]
```

### Vocal Style

```
[Vocal Style: Whisper]
[Vocal Style: Soft]
[Vocal Style: Power]
[Vocal Style: Raspy]
[Vocal Style: Falsetto]
[Vocal Style: Belt]
[Vocal Style: Spoken Word]
[Vocal Style: Rap]
[Vocal Style: Open, Confident]
```

### V5 Personas (More Consistent)

V5 maintains Persona consistency better than previous versions:
- **Whisper Soul** – lo-fi intimacy
- **Power Praise** – gospel anthems
- **Retro Diva** – synthpop and disco
- **Conversational Flow** – clear hip hop phrasing

### Vocal Effects

```
[Vocal Effect: Reverb]
[Vocal Effect: Delay]
[Vocal Effect: Auto-tune]
[Vocal Effect: Vocoder]
[Vocal Effect: Distortion]
```

### Voice Modulation (V5)

```
[modulate up a key]
[modulate down a key]
```

### Special Effects (V5)

```
[crowd sings]
[echo effect]
[loop-friendly]
```

### Callback Tags (V5 - for Extend)

Use to maintain consistency when extending:
```
[Callback: continue with same vibe as chorus]
[Callback: maintain energy from verse]
```

## Performance Indicators

### Text Formatting

| Format | Effect |
|--------|--------|
| `UPPERCASE TEXT` | Shouted/emphasized |
| `(text in parentheses)` | Backing vocals/harmonies |
| Repeated lines | Sung in loop |
| `~word~` | Elongated note |
| `word-` | Cut off abruptly |

### Timing Hints

```
[Slow]
[Fast]
[Half-time]
[Double-time]
[Breakdown]
[Buildup, 8 bars]
[Instrumental, 4 bars]
```

## Complete Example (V5 Optimized)

Note: 6-12 syllables per line, front-loaded tags, callback ready.

```
[Intro]
[Mood: Uplifting]
[Energy: Medium→High]
[Instrument: Bright Electric Guitars, Live Drums]

[Verse 1]
[Vocal Style: Open, Confident]
Walking through the morning light
Shadows fading out of sight
Every step a new beginning
Feel the world around me spinning

[Pre-Chorus]
[Energy: Rising]
Here it comes, can you feel it now
The moment we've been waiting for

[Chorus]
[Energy: High]
[Vocal Style: Power]
We are RISING, breaking through the sky
Nothing's gonna stop us, born to fly
(Born to fly, born to fly)
This is our time, THIS IS OUR TIME!

[Verse 2]
[Vocal Style: Soft]
Doubt was holding back my dreams
Nothing ever as it seems
Now I see the path before me
Written in the stars, my story

[Pre-Chorus]
[Energy: Rising]
[Callback: continue with same vibe as chorus]
Here it comes, can you feel it now
The moment we've been waiting for

[Chorus]
[Energy: High]
We are RISING, breaking through the sky
Nothing's gonna stop us, born to fly

[Bridge]
[Mood: Triumphant]
[Texture: Tape-Saturated]
[Instrument: Full orchestra]
When they said impossible
We said WATCH US NOW
When they tried to pull us down
We rose above the crowd

[Drop]
[Energy: Maximum]

[Chorus]
[Vocal Style: Belt]
We are RISING, breaking through the sky
NOTHING'S GONNA STOP US!

[Outro]
[Fade Out]
Rising... rising... born to fly...
```

## Tips for Effective Structure

### Song Length Control
- More sections = longer song (V5 supports up to 8 minutes)
- 2 verses + 2 choruses ≈ 2-3 min
- Add bridge and outro for 3-4 min
- Use `[Instrumental, X bars]` for padding

### Energy Management
- Start `[Energy: Medium]` for room to build
- Use `[Energy: Rising]` in pre-chorus
- Use `[Energy: Medium→High]` for gradual transitions
- Peak at `[Energy: High]` or `[Maximum]` in final chorus
- Gradual decrease in outro

### Cohesion
- Repeat chorus structure identically
- Use consistent tag style throughout
- Match mood tags to lyrical content
- V5's persistent memory maintains motifs across full song

### V5-Specific Tips
- Use callbacks when extending: prevents drift
- Negative prompting in style field: "no guitars", "no harsh distortion"
- Emotional verse tags work well: [sad verse], [angry chorus]
- Loop-friendly tag helps for seamless loops
- Remaster (Subtle) for consistent quality across playlist

### Common Mistakes to Avoid
- Too many consecutive tags (confuses AI)
- Contradicting mood indicators
- Overly complex structures for short songs
- Missing essential sections (intro/outro)
- Long Extend chains without callbacks (causes drift)
- Lines over 12 syllables (vocal alignment issues)

### Troubleshooting

| Problem | Solution |
|---------|----------|
| Prompt overload (ignored tags) | Simplify to 1-2 genres; keep mood specific |
| Repetition | Add "variation/dynamic" cues or Replace section |
| Artifacts (hiss/shimmer) | Try Remaster Subtle first |
| Vocals buried | Export stems and rebalance; or Replace with clearer Persona |
| Extend drift | Re-inject genre/mood + use callback phrasing |
