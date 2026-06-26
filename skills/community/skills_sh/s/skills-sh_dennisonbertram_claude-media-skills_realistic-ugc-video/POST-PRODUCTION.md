# Post-Production: Audio & Editing

After generating all your video clips, post-production makes the difference between "obviously AI" and "wait, is that real?"

## Audio Fixes (Most Important)

**The voice is the #1 tell.** AI-generated audio often sounds:
- Too studio-clean
- Unnaturally smooth
- Missing room tone
- Robotic cadence

### Option 1: Adobe Podcast (Minimum)

**What it does:** AI-powered audio cleaning that removes noise while preserving naturalness.

**When to use:** Every single time, at minimum. This is non-negotiable.

**How:**
1. Go to podcast.adobe.com/enhance
2. Upload your audio track (or full video)
3. Process
4. Replace audio in your edit

**Why it works:** Cleans up the "raw AI" sound without making it sound too polished. Unlike studio-quality tools, it preserves some natural imperfection.

**Cost:** Free tier available

### Option 2: Resemble AI (Voice Swap)

**What it does:** Changes the AI voice to a different, more natural-sounding voice.

**When to use:** When the AI voice is too obviously synthetic, even after Adobe Podcast.

**How:**
1. Create account at resemble.ai
2. Upload target voice samples (or use stock voices)
3. Process your audio through voice conversion
4. Replace in your edit

**Why it works:** Different from ElevenLabs—Resemble produces less "studio-polished" output that sounds more authentically recorded.

**Cost:** Pay per minute processed

### Option 3: Manual Room Tone

**What it does:** Adds subtle background noise that real recordings have.

**How:**
1. Record 10 seconds of silence in a real room
2. Layer under your AI audio at -20dB to -30dB
3. This adds the "presence" that AI audio lacks

**Room tone characteristics:**
- Slight HVAC hum
- Distant traffic
- Electronic buzz
- General "air"

### Audio Processing Order

```
Raw AI Audio
    ↓
Adobe Podcast (clean but preserve naturalness)
    ↓
[Optional] Resemble AI (voice swap if needed)
    ↓
Add room tone layer
    ↓
Final audio
```

## Handling Jump Cuts

When you splice 8-10 second clips together, you get jump cuts. The character's position shifts slightly between clips.

### Strategy 1: B-Roll Coverage

Cover the cut with relevant imagery:
- Screenshots of what you're discussing
- Product shots
- Stock footage
- Animated graphics
- Screen recordings

**Timing:** Start B-roll 0.5s before the cut, end 0.5s after.

### Strategy 2: Zoom Punch

Cut to a slightly zoomed version:
1. Scale up to 110-120% at the cut point
2. Return to 100% naturally
3. Creates intentional "emphasis" feeling

### Strategy 3: Text/Graphic Overlay

Add text or graphics that naturally draw attention away from the cut:
- Key point text
- Animated bullet
- Logo/brand element

### Strategy 4: Match Action

Choose clips that happen to have similar positions at cut points:
- If Clip 1 ends with forward lean, start Clip 2 with forward lean
- This requires some luck or regeneration

## Editing Workflow

### Step 1: Import All Clips

Import all generated clips into your editor (CapCut, Premiere, DaVinci, etc.)

### Step 2: Rough Assembly

Place all clips in order on timeline. Don't worry about cuts yet.

### Step 3: Audio Extraction & Processing

1. Export combined audio track
2. Run through Adobe Podcast
3. [Optional] Run through Resemble AI
4. Re-import cleaned audio

### Step 4: Sync Cleaned Audio

Replace original audio with processed version. Verify sync.

### Step 5: Handle Jump Cuts

For each cut point:
1. Watch the transition
2. Decide: B-roll, zoom, graphic, or leave?
3. Apply chosen technique

### Step 6: Remove Filler

Remember those filler sentences you added to hit syllable targets? Now's the time to evaluate:
- Does it sound natural? Keep it.
- Does it sound forced? Cut it and cover with B-roll.

### Step 7: Final Polish

- Color grade for consistency across clips
- Add subtle grain if clips vary
- Normalize audio levels
- Add music bed if appropriate (very low, -25dB)

## CapCut-Specific Tips

CapCut is popular for UGC editing. Some specific features:

### Auto Captions
- Use auto-caption feature
- Style: Bold, high contrast, TikTok-style
- Position: Lower third, not dead center

### Transitions
- Avoid flashy transitions—they scream "edited"
- Use: Jump cut (none), Zoom, Slight dissolve (0.1s)
- Don't use: Swipe, Spin, Glitch effects

### Speed Ramping
- Can help smooth cuts
- Slight slow-mo (0.9x) before cut
- Normal speed after
- Subtle, don't overdo

### Export Settings
- 1080p minimum, 4K if source allows
- 30fps (matches typical phone recording)
- High bitrate to preserve quality

## Color Consistency

AI-generated clips can have slight color variations. Fix with:

### Method 1: Match Frame Reference
1. Choose one clip as "hero" color
2. Apply correction to other clips to match

### Method 2: LUT Application
1. Apply same LUT to all clips
2. Adjust intensity per clip for consistency

### Method 3: Slightly Desaturate
1. Reduce saturation 10-15%
2. Add slight warmth
3. Mimics iPhone camera processing

## Sound Design

### Background Music
- Very subtle, -20dB to -25dB
- Lo-fi, acoustic, or ambient
- Avoid: Upbeat stock music (screams "ad")
- Good: Gentle acoustic guitar, ambient pads

### Sound Effects
- Subtle room tone (as described above)
- Occasional mouse click or keyboard tap if showing screens
- Don't: Add whooshes, dings, or attention-getters

## Final Quality Check

Before export, verify:

- [ ] Audio sounds natural (not too clean)
- [ ] No obvious jump cuts visible
- [ ] Color consistent across all clips
- [ ] Pacing feels natural throughout
- [ ] Filler sentences either work or are removed
- [ ] Captions (if used) are accurate
- [ ] Music doesn't overpower voice

## Export Settings

### For Social Media (TikTok, Reels, Shorts)
```
Resolution: 1080x1920 (9:16)
Frame rate: 30fps
Codec: H.264
Bitrate: 12-15 Mbps
Audio: AAC, 320kbps
```

### For YouTube/Longer Form
```
Resolution: 1920x1080 (16:9) or 1080x1920 (Shorts)
Frame rate: 30fps
Codec: H.264 or H.265
Bitrate: 20+ Mbps
Audio: AAC, 320kbps
```

### For Ads/Commercial Use
```
Resolution: Highest available
Frame rate: Match platform specs
Codec: ProRes or DNxHD for quality
Provide multiple aspect ratios
```

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Clips don't match | Character drift | Use same seed image, regenerate |
| Audio sync off | Processing shifted timing | Manual realign in editor |
| Obvious AI voice | Insufficient processing | Add more room tone, try Resemble |
| Jarring cuts | Position mismatch | Cover with B-roll |
| Video looks "flat" | AI's neutral grading | Add subtle contrast, warmth |
| Pacing inconsistent | Syllable count was off | Cut filler or regenerate clips |
