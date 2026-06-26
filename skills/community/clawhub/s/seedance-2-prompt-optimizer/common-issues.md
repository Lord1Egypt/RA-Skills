# Common Issues & Workarounds — Seedance 2.0

This file documents known Seedance 2.0 issues, their causes, prompt-level fixes,
and post-production workarounds where needed. Reference this when building prompts
or responding to user complaints about generation quality.

---

## V-1: Character ID Drift ("Face Swap" Mid-Video)

**Symptom**: Generated character looks different from the reference image, or the
face changes midway through the video. Can also cause unintended celebrity likeness matches.

**Root cause**: Face reference image is too small relative to the input, or is mixed
with full-body/costume reference images in the same file, diluting the model's focus.

### Prompt-level fix
```
@image1 is the face close-up reference for <Subject1>. Use @image1 as the strict
identity anchor. @image2 is the costume/full-body reference. Face must remain
consistent throughout.
```

### Input preparation fix
- Crop the face region to a **dedicated image** — face only, minimal neck/shoulder
- Submit the face close-up as a **separate image slot** (e.g. @image3)
- Place the most important reference **first** in the prompt — earlier = higher weight
- Recommended input order: `face close-up → full body → scene/background`

### Prompt structure
```
@image1 (face, identity anchor), @image2 (full body costume reference), @image3 (scene).
Facial features must strictly follow @image1 throughout all shots.
```

### What to tell the user
> Add a separate face-only crop of your character as an extra reference image.
> A head-only portrait (no shoulders) gives the model the clearest identity signal.
> Three-view diagrams are NOT ideal — use face close-up + full body shot instead.

---

## V-2: Unwanted Subtitles Generated

**Symptom**: Generated video contains subtitles or on-screen text that wasn't requested,
often with errors or wrong language.

**Root cause**: Model trained on subtitle-heavy video data; vertical (9:16) aspect ratio
significantly increases subtitle probability.

### Prompt-level fix (reduces probability by ~50–70%)
Add to negative constraints:
```
no subtitles, no on-screen text, no captions, subtitle-free
```

### Input fix
- Remove text/watermarks from reference images/videos before uploading
  (use Seedream or similar tool to erase text from inputs)
- Reduce number of cuts/scenes in a single generation

### Aspect ratio fix (most effective)
- Switch from **9:16 (vertical) → 16:9 (horizontal)** — drops subtitle rate to <10%
- Crop to vertical in post-production if needed

### Post-production fix
- Use subtitle erasure tool (e.g. Volcano Engine Video VOD subtitle erasure)

### What to tell the user
> Unfortunately there is no 100% guarantee of subtitle-free output — only probability
> reduction. Use 16:9 aspect ratio and add "no subtitles, no on-screen text" to your
> prompt. If subtitles still appear, try regenerating (re-roll) or use a subtitle
> removal tool in post.

---

## V-3: Unwanted Platform Logos / Watermarks

**Symptom**: Generated video contains logos from video platforms (Bilibili, Mango TV, etc.)
that were not requested.

**Root cause**: Model trained on watermarked platform content; can inherit watermarks
from reference videos that contain them.

### Prompt-level fix
```
no watermark, no logo, no platform branding, no copyright marks
```

### Input fix
- Check reference videos for existing platform watermarks and remove before uploading

### What to tell the user
> Always include "no watermark, no logo" in your negative constraints. If the
> reference video has a platform watermark, remove it before using it as input.

---

## V-4: Style Drift (Animation → Realistic)

**Symptom**: Prompt asks for 2D anime or 3D CG animation style, but generated video
partially or fully drifts to live-action realistic style.

**Root cause**: Reference images are too photorealistic or mixed with realistic photos,
pulling the model toward live-action output.

### Prompt-level fix
Explicitly state the art style and reinforce it per shot:
```
2D Japanese anime style throughout. Maintain flat cel-shading, bold outlines,
no photorealism, no live-action aesthetics.
```

For 3D CG:
```
3D Chinese fantasy CG style, consistent with @image1. Maintain CG rendering
throughout, no photorealistic drift.
```

### Input fix
- Replace photorealistic reference images with ones that match the target art style
- Use AI-generated images in target style as references instead of photos

### What to tell the user
> Convert your reference images to the target art style (e.g. using an image
> generation tool) before uploading. Then reinforce the style name in every shot
> description.

---

## V-5: Periodic Flickering / Horizontal Banding

**Symptom**: Regularly repeating flicker or horizontal stripes across the entire video,
especially visible in large flat colour areas.

**Root cause**: Invisible watermarking algorithm embedded in the current model version.

### Status
Model update with fix was planned for early April 2026. Check if current version resolves it.

### Prompt-level fix
None currently available.

### Workaround
- Request an "invisible watermark bypass" flag from the platform (enterprise/API users)
- If customer-facing: note the known issue and wait for updated model version

### What to tell the user
> This is a known platform-side issue caused by the invisible watermarking algorithm.
> A model update was expected to fix this. Try regenerating with the latest model version.
> If it persists, contact platform support about the watermark bypass option.

---

## V-6: Video Extension Join Stutters / Frame Jump

**Symptom**: When multiple "extend" clips are stitched together, there is a visible
jump, stutter, or content regression at each join point.

**Root cause**: The first and last frames of extended segments overlap slightly,
causing a double-frame or rollback effect when concatenated directly.

### Post-production fix (frame alignment)
1. Import all segments into editing software (CapCut / Premiere / DaVinci Resolve)
2. At each join point:
   - Delete the **last 6 frames** of the preceding clip
   - Delete the **first 1 frame** of the following clip
3. Repeat for all join points
4. Export and verify smoothness

### Prompt-level prevention
End each segment at a scene cut or transition:
```
Segment 1 ends: [whip pan left] — cut to black.
Segment 2 begins: [fade in] new scene — living room, daytime.
```
This makes join points feel intentional even if there is minor variance.

### What to tell the user
> When stitching extended clips, you'll need to trim 6 frames from the end of
> each preceding clip and 1 frame from the start of each following clip in your
> editing software. This aligns the frame overlap and removes the stutter.

---

## V-7: Duplicate / Twin Characters

**Symptom**: Two identical-looking characters appear in the same frame when only
one was intended. Common when input includes multi-angle (three-view) character sheets.

**Root cause**: Model interprets multiple angles of the same character as multiple
distinct characters.

### Prompt-level fix
Add to end of prompt:
```
Throughout the entire video, there must be exactly one instance of <Subject1>
visible at any time. Do not duplicate, clone, or mirror any character.
No twin subjects, no split-screen doubles, no identical characters in the same frame.
```

### Subject clarification fix (for multi-angle reference sheets)
```
@image1, @image2, @image3 are three different angles of the SAME character <Subject1>.
Only one <Subject1> should ever appear in any frame.
```

### Character naming fix
When multiple characters exist, label each one clearly at every mention:
```
Subject1 (CEO, @image1) enters from the left.
Subject2 (assistant, @image2) stands at the desk.
```

### What to tell the user
> Always tell the model that multi-angle character reference images show the
> SAME person. Add an explicit instruction that only one instance of the character
> may appear at any time.

---

## A-1: Audio Click / Pop at Video End

**Symptom**: A sudden "click", "pop", or audio cutoff sound at the very end of
the generated video. More common in videos with TTS narration.

**Root cause**: Audio track is being hard-cut at the generation boundary.

### Prompt-level mitigation
Avoid ending a sentence at the very last moment of the clip:
```
Voiceover finishes: {line here.} — followed by 1s ambient silence before clip ends.
```

### Post-production fix (CapCut / Premiere)
1. Import video into editor
2. Select the audio track
3. Go to audio envelope / volume keyframe editor
4. Add a keyframe ~0.5s before the end
5. Drag the final keyframe to 0 dB (silence) — creates a fade-out ramp
6. Export

### What to tell the user
> The click at the end is a known audio boundary issue. You can fix it by adding
> an audio fade-out in your editing software — fade the volume to zero over the
> last 0.5s of the clip. CapCut has this under "Audio Envelope" in the track editor.

---

## A-2: Incorrect Chinese Pronunciation / Polyphone Errors

**Symptom**: Specific characters are mispronounced; polyphonic characters (多音字)
use the wrong reading.

**Root cause**: Model TTS does not reliably resolve context-dependent pronunciation.

### Prompt-level fix
Replace problematic characters with phonetic equivalents:
- `螭` (chī) → use `吃` (same sound, common character)
- `棪` → use `燕` (yàn, common character)
- For rare/literary characters: write the pinyin in parentheses after the character

### What to tell the user
> Replace rare or polyphonic characters with common homophones in your dialogue text.
> For example, replace literary characters with everyday characters that sound the same.
> This doesn't guarantee 100% correct pronunciation but significantly improves accuracy.

---

## A-3: Voice Timbre Reference Not Matched

**Symptom**: The reference audio clip has a specific voice quality (e.g. soft, young female)
but the generated voice sounds completely different (e.g. mature, husky).

**Root cause**: Audio timbre reference signal is weak; dialogue script style may
conflict with the reference voice's natural register.

### Prompt-level fix
Describe the voice explicitly alongside the audio reference:
```
@audio1 is the voice timbre reference: young female voice, soft and bright tone,
light and airy delivery, conversational register.
```

Reference the Seedance 1.5 Pro prompt guide for full voice descriptor vocabulary.

### Script alignment fix
Match the register and tone of the dialogue script to the reference audio:
- If @audio1 is casual and playful → write casual, short dialogue lines
- If @audio1 is formal and measured → write formal, longer dialogue
- Mismatched register degrades timbre adherence significantly

### What to tell the user
> Add a text description of the voice quality (age, gender, tone, register) alongside
> your audio reference. Also make sure your dialogue script matches the style and
> mood of the reference audio — the closer the match, the more stable the voice output.

---

## Quick Reference Table

| Code | Issue | Quick fix |
|---|---|---|
| V-1 | Character face changes | Add face-only close-up as separate image; state "strict identity anchor" |
| V-2 | Unwanted subtitles | Add "no subtitles" to constraints; use 16:9 ratio |
| V-3 | Platform logos/watermarks | Add "no watermark, no logo" to constraints |
| V-4 | Style drifts to realistic | State art style explicitly per shot; use style-matched reference images |
| V-5 | Periodic flickering | Platform bug — regenerate with latest model; ask for watermark bypass |
| V-6 | Stutter at clip joins | Trim last 6 frames of clip A + first 1 frame of clip B |
| V-7 | Duplicate characters | Add "exactly one instance" constraint; label multi-angle refs as same person |
| A-1 | Audio click at end | Fade audio to 0 in last 0.5s using editing software |
| A-2 | Wrong Chinese pronunciation | Replace rare characters with common homophones |
| A-3 | Wrong voice timbre | Describe voice in text; match script register to reference audio style |
