# Script Chunking: The Syllable Method

The biggest telltale of AI videos is **inconsistent pacing**. The character speaks too fast in one clip, too slow in another. When spliced together, it feels robotic.

The fix: **55-60 syllables per 10-second video generation**.

## Why Syllables, Not Words?

Words vary wildly in length:
- "I" = 1 syllable
- "productivity" = 5 syllables
- "entrepreneurship" = 5 syllables

A 10-word sentence could be 10 syllables or 35 syllables. Syllable count gives consistent timing.

## The Rules

### Rule 1: 55-60 Syllables Per Chunk
This produces natural, slightly energetic pacing—perfect for UGC content.

| Syllables | Result |
|-----------|--------|
| < 45 | Too slow, feels AI |
| 45-54 | Acceptable, slightly slow |
| **55-60** | **Sweet spot** |
| 61-70 | Slightly fast |
| > 70 | Too fast, unintelligible |

### Rule 2: Never Cut Mid-Sentence
Always end on a complete sentence. Cutting mid-thought creates unnatural pauses.

**WRONG:**
```
Chunk 1: "The key to success is understanding that you need to..."
Chunk 2: "...work harder than everyone else around you."
```

**RIGHT:**
```
Chunk 1: "The key to success is understanding your competition."
Chunk 2: "You need to work harder than everyone else around you."
```

### Rule 3: Add Fillers to Reach Target
If a natural break lands at 40 syllables, add a short filler sentence to reach 55-60.

**Before (42 syllables):**
```
"I've been doing this for ten years and I've learned one crucial lesson."
```

**After (58 syllables):**
```
"I've been doing this for ten years and I've learned one crucial lesson. Let me share it with you."
```

**Good filler phrases:**
- "Let me explain." (4 syllables)
- "Here's the thing." (3 syllables)
- "This is important." (5 syllables)
- "I want you to really get this." (8 syllables)
- "Stay with me here." (4 syllables)
- "And here's why." (3 syllables)

## Syllable Counting Guide

### Quick Counting Method
Clap as you speak. Each clap = 1 syllable.

### Common Words Reference

| Word | Syllables |
|------|-----------|
| the | 1 |
| important | 3 |
| actually | 4 |
| productivity | 5 |
| opportunity | 6 |
| responsibility | 6 |
| entrepreneurship | 5 |

### Numbers
| Number | Syllables |
|--------|-----------|
| one | 1 |
| eleven | 3 |
| fifteen | 2 |
| twenty | 2 |
| hundred | 2 |
| thousand | 2 |
| million | 2 |
| billion | 2 |

## Example: Full Script Breakdown

**Original 60-second script (320 syllables):**
```
Hey everyone, I wanted to share something that completely changed how I think about productivity. It's not another app or system. It's actually about understanding your own energy patterns throughout the day. Once I figured this out, everything clicked into place. Most people try to force themselves to work at their lowest energy times. That's a recipe for burnout. Instead, match your hardest tasks to your peak hours. For me, that's usually between nine and eleven in the morning. I save easy tasks like email for the afternoon slump. Try tracking your energy for one week and you'll see the patterns emerge.
```

**Chunked (6 clips):**

| Chunk | Text | Syllables |
|-------|------|-----------|
| 1 | "Hey everyone, I wanted to share something that completely changed how I think about productivity. It's not another app or system." | 58 |
| 2 | "It's actually about understanding your own energy patterns throughout the day. Once I figured this out, everything clicked into place." | 56 |
| 3 | "Most people try to force themselves to work at their lowest energy times. That's a recipe for burnout. Here's what I do instead." | 57 |
| 4 | "Match your hardest tasks to your peak hours. For me, that's usually between nine and eleven in the morning. That's my golden window." | 58 |
| 5 | "I save easy tasks like email for the afternoon slump. You know that two PM feeling? That's when I handle the simple stuff." | 56 |
| 6 | "Try tracking your energy for one week and you'll see the patterns emerge. Trust me, this is going to change everything for you." | 57 |

**Note:** Chunks 3, 5, and 6 have added filler to reach target syllables.

## Chunking Workflow

### Step 1: Write Full Script
Write naturally, don't worry about chunking yet.

### Step 2: Count Total Syllables
This tells you how many clips you'll need:
- 60 syllables = ~1 clip (10 seconds)
- 300 syllables = ~5 clips (50 seconds)
- 600 syllables = ~10 clips (100 seconds)

### Step 3: Mark Natural Breaks
Identify sentence endings that fall near 55-60 syllables.

### Step 4: Adjust with Fillers
Add short phrases to reach target when natural breaks fall short.

### Step 5: Verify Each Chunk
Count syllables for each chunk. Adjust if outside 55-60 range.

## Tone Markers

Mark tone shifts within the script to inform video prompts:

```
[Chunk 1] (Tone: Friendly, Conversational)
"Hey everyone, I wanted to share something that completely changed how I think about productivity."

[Chunk 2] (Tone: Revelatory, Building)
"It's actually about understanding your own energy patterns throughout the day."

[Chunk 3] (Tone: Warning, Serious)
"Most people try to force themselves to work at their lowest energy times. That's a recipe for burnout."
```

## Script Template

```markdown
# Video Script: [Title]
Total syllables: [X]
Estimated length: [X] seconds
Number of clips: [X]

---

## Chunk 1 (X syllables)
**Tone:** [Friendly/Urgent/Professional/etc.]
**Text:** "[Script text here]"

---

## Chunk 2 (X syllables)
**Tone:** [...]
**Text:** "[...]"

---
[Continue for all chunks]
```

## Common Issues

| Issue | Cause | Fix |
|-------|-------|-----|
| Pacing feels slow | Under 55 syllables | Add filler phrase |
| Pacing feels rushed | Over 60 syllables | Split into smaller sentences |
| Awkward pause at cut | Cut mid-thought | Rework to end on complete idea |
| Filler sounds weird | Forced addition | Choose more natural filler or rework sentence |
| Clips don't flow | Tonal mismatch between chunks | Add transition phrases |

## Automating Syllable Count

Ask Claude to count syllables:
```
Count the syllables in this text and tell me if it's within 55-60:
"[Your text here]"
```

Or use online tools:
- syllablecounter.net
- howmanysyllables.com
