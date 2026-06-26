# Frame Preparation Guide

The talking-circle skill requires 4 PNG images of your avatar character. Each image represents a different mouth/eye state used for lip-sync and blink animation.

## Required Frames

### 1. `neutral.png` — Mouth closed, eyes open
The default resting state. Shown when audio amplitude is low (silence or quiet).

### 2. `mouth-slight-open.png` — Mouth slightly open, eyes open
Shown during moderate speech volume. The mouth should be noticeably open but not at maximum.

### 3. `mouth-wide-open.png` — Mouth wide open, eyes open
Shown during loud speech. The mouth should be at its widest natural opening.

### 4. `eyes-closed.png` — Mouth closed, eyes closed
Used for periodic blink animation. Same as neutral but with eyes closed.

## Image Requirements

- **Format:** PNG
- **Resolution:** All 4 images must be the same resolution
- **Recommended size:** 2048x2048 pixels (will be downscaled for the video)
- **Aspect ratio:** Square (1:1)
- **Style consistency:** All frames should have the same art style, colors, and character positioning
- **Background:** Can be any color — the skill crops to a circle automatically

## Generating Frames with Image AI

If you don't have hand-drawn frames, use an image generation API (DALL-E, Midjourney, Flux, etc.):

1. **Generate the neutral frame first.** This is the base — all other frames must match it exactly.
   - Use a shoulder-up portrait prompt with mouth closed, eyes open.
   - Example: `"Shoulder-up portrait of [character], square, clean background, mouth closed, eyes open, looking at camera"`

2. **Generate remaining frames as edits of the neutral image.**
   - Use image editing / inpainting to modify only the mouth or eyes.
   - Do NOT regenerate the full image — this causes style and position drift.

   | Frame | Region to edit | Prompt hint |
   |-------|---------------|-------------|
   | Slight open | Mouth | `"Mouth slightly open, teeth barely visible"` |
   | Wide open | Mouth | `"Mouth wide open as if saying 'ah'"` |
   | Blink | Eyes | `"Eyes gently closed, mouth closed"` |

3. **Verify consistency.** Overlay all 4 images to check that head/body position hasn't shifted. If any frame drifts, regenerate it from the neutral base.

## Tips

- Keep the character's head position identical across all 4 frames — only the mouth and eyes should change
- Use clean, high-contrast artwork for best results at small circle sizes
- If using AI-generated art, generate all 4 frames via inpainting from the same base image
- Test with a short audio clip first to verify the frames look natural in motion
- See `examples/sbercat/` for a reference character with all 4 frame images
