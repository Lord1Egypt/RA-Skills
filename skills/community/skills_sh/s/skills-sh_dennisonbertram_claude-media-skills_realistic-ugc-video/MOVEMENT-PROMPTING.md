# Movement Prompting for Natural Video

The biggest giveaway in AI talking head videos: **the character is too still**.

## IMPORTANT: Hands Limitation

**AI video models cannot reliably generate natural hand movements.** Fingers morph, gestures look alien, and hands are the #1 tell that a video is AI.

**Recommended approach:**
- Frame the shot to **exclude hands entirely** (head/shoulders only)
- Or keep hands **completely static and out of focus**
- Use head movements, facial expressions, and body sway instead
- Cover any hand weirdness with B-roll in post-production

The movement prompts below include hand choreography for reference, but **use at your own risk** - results vary widely.

Real people have:
- Constant micro-sway (spinal movement)
- Hand fidgeting
- Head tilts and nods
- Spontaneous blinks
- Weight shifts
- Breath-related movement

Your video prompts must choreograph these movements at specific timestamps.

## The "Active Idle" Concept

Even when "still," humans are never truly static. Define a **base state** that includes subtle movement.

### Hand "Home Base" Protocol

```
Hand "Home Base" Protocol: Hands default to a relaxed but alive position (Active Idle).
Fingers shift, thumbs rub, or wrists rotate slightly while anchored.
Gestures occur only to emphasize key moments, then return to base.
```

**Home base variations:**
| Position | Description |
|----------|-------------|
| Interlocked | Fingers woven together, thumbs pressing or tapping |
| Resting | Palms flat on surface, fingers occasionally drumming |
| Clasped | Hands loosely holding each other, periodic grip changes |
| One hand active | One hand gestures while other anchors |

## Timestamp-Based Movement Prompts

For 10-second video generation, choreograph movements at intervals:

### Basic Template
```
[0.0s-0.5s] [Pre-roll buffer: minimal movement, eye lock to camera]
[0.5s-3.0s] [Movement cluster A]
[3.0s-6.0s] [Movement cluster B]
[6.0s-8.0s] [Movement cluster C]
[8.0s-10.0s] [Movement cluster D + natural close]
```

### Movement Cluster Structure
Each cluster combines 2-3 simultaneous micro-movements:
```
[Timestamp] [Simultaneous Cluster:
  [Hand action] +
  [Head action] +
  [Facial expression]]
```

## Movement Vocabulary

### Head Movements
| Action | When to Use |
|--------|-------------|
| `head tilts slightly right/left` | Showing consideration |
| `head nods encouragingly` | Affirming point |
| `head drifts forward` | Building intensity |
| `chin lifts` | Confidence, conclusion |
| `head shakes slightly` | Negation, disbelief |
| `quick micro-nod` | Punctuating statement |

### Eye/Brow Movements
| Action | When to Use |
|--------|-------------|
| `natural blink` | Every 3-5 seconds |
| `brows furrow slightly` | Seriousness |
| `brows raise` | Surprise, emphasis |
| `eyes narrow slightly` | Focus, skepticism |
| `eyes widen` | Revelation, excitement |
| `eyes lock to lens` | Direct address |

### Hand Movements
| Action | When to Use |
|--------|-------------|
| `fingers shift/adjust` | Continuous idle |
| `thumbs tap/rub` | Nervous energy |
| `hands break clasp for open-palm rotation` | Explaining |
| `one hand raises briefly` | Emphasis |
| `wrist shifts position` | Restlessness |
| `fingers interlace tighter` | Intensity |

### Body Micro-Movements
| Action | When to Use |
|--------|-------------|
| `slight forward lean` | Engagement |
| `micro-sway left/right` | Natural breathing |
| `shoulders relax/tense` | Emotional shift |
| `chest rises with breath` | Before speaking |

## Example: Full Movement Prompt

```
Hand "Home Base" Protocol: Hands default to Active Idle (fingers interlocked,
thumbs occasionally pressing). Gestures occur only for key emphasis.

[Action]:
[0.0s-0.5s] [Simultaneous Cluster:
  Sharp inhale +
  Eyes lock instantly to lens +
  Head is still (Pre-roll Buffer)]

[0.5s-3.0s] [Simultaneous Cluster:
  Hands in Active Idle (fingers interlocked, tight grip, thumbs pressing down) +
  Head tilts slightly right +
  Brows furrow slightly in seriousness]

[3.0s-6.0s] [Simultaneous Cluster:
  Hands break clasp for a quick, contained open-palm rotation then return to base +
  Head drifts forward +
  Natural blink]

[6.0s-8.0s] [Simultaneous Cluster:
  Hands return to Active Idle (loose clasp, thumbs tapping) +
  Head nods encouragingly +
  Cheeks lift in a natural smile]

[8.0s-10.0s] [Simultaneous Cluster:
  Hands anchored (wrist shifts position) +
  Chin lifts in a quick, final nod +
  Natural blink]
```

## Matching Movement to Tone

### Conversational/Friendly
```
- More head tilts, nods
- Relaxed hand idle (loose clasp)
- Frequent natural smiles
- Open gestures
- Slower, gentler movements
```

### Urgent/Scarcity
```
- Forward lean
- Tighter hand clasp
- Minimal smiling
- Quick, decisive gestures
- Head shakes for negation
```

### Professional/Authority
```
- Measured movements
- Controlled gestures
- Deliberate nods
- Steady eye contact
- Minimal fidgeting
```

### Excited/Enthusiastic
```
- More frequent gestures
- Raised brows often
- Wide eyes moments
- Faster movement tempo
- More pronounced expressions
```

## Pacing and Audio Markers

Include pacing direction with movement:
```
[Mood and Audio Pacing]:
Rapid fire delivery, high energy, viral UGC style, confident,
speaks fast the pacing [audio] should be at 2x speed
```

**Pacing options:**
| Descriptor | Effect |
|------------|--------|
| `2x speed` | Fast, energetic, TikTok style |
| `1.5x speed` | Brisk, professional |
| `normal pace` | Conversational |
| `deliberate pace` | Serious, weighty |

## Movement Patterns by Content Type

### Sales/Pitch Video
```
[0-3s] Build credibility: steady gaze, slight forward lean, confident nod
[3-6s] Present problem: brows furrow, head shake, tighter hand clasp
[6-8s] Offer solution: hands open gesture, eyes widen, smile emerges
[8-10s] Call to action: direct gaze, decisive nod, hands return to confident rest
```

### Tutorial/Educational
```
[0-3s] Hook attention: engaging smile, raised brows, inviting head tilt
[3-6s] Explain concept: hand gestures to illustrate, natural blinks
[6-8s] Emphasize key point: forward lean, brief pause, direct gaze
[8-10s] Transition: relaxed expression, small nod, reset position
```

### Testimonial/Story
```
[0-3s] Set scene: thoughtful expression, eyes drift briefly, slight smile
[3-6s] Build narrative: animated expression, varied head movements
[6-8s] Emotional beat: authentic reaction (joy/relief/surprise)
[8-10s] Conclusion: warm smile, direct address, settled posture
```

## Continuity Across Clips

When generating multiple clips for one video:

1. **End position → Start position**
   - Last frame of Clip 1 should roughly match first frame of Clip 2
   - Avoid drastic position changes between clips

2. **Emotional continuity**
   - If Clip 1 ends serious, Clip 2 should start serious
   - Build emotional arcs across clips

3. **Hand position continuity**
   - Track where hands end in each clip
   - Start next clip with hands in similar position

## Common Movement Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| No idle movement | Character looks frozen | Add constant micro-fidgets |
| Too many big gestures | Looks theatrical | Reserve gestures for key moments |
| Same movement pattern | Predictable, robotic | Vary cluster combinations |
| No blinks | Uncanny valley | Add blink every 3-5 seconds |
| Perfectly smooth | Too polished | Add micro-hesitations |

## Movement Prompt Checklist

- [ ] Hand "Home Base" defined
- [ ] Pre-roll buffer (0-0.5s) included
- [ ] 4-5 distinct movement clusters
- [ ] Each cluster has 2-3 simultaneous actions
- [ ] Natural blinks distributed throughout
- [ ] Movement matches tone of script
- [ ] Pacing/audio direction included
