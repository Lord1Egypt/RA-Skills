---
name: resize-for-banner
description: >
  Resize an image into a Twitter/X header banner (5:2, 1500x600) using
  ImageMagick. The image is rescaled to fit and the leftover space is padded
  black — never cropped, so no content is lost. Use when the user wants a
  Twitter/X banner for an article or infographic. Twitter/X is the only target:
  LinkedIn and blog headers accept the original image, so never generate a
  derivative for them. Never overwrites the original — writes a new file beside it.
---

# Resize for Banner (Twitter/X only)

Turn one image into a Twitter/X header banner with ImageMagick, keeping the original file untouched and writing a new file beside it. The image is **rescaled to fit and black-padded**, never cropped, so no content is lost.

## Target — Twitter/X only

| Platform | Ratio | Dimensions | Notes |
|----------|-------|------------|-------|
| Twitter / X | 5:2 | 1500x600 | Header photo. The only supported target. |

**Not supported, on purpose:**

- **LinkedIn article headers** accept the original image — a 16:9 infographic can be uploaded as-is. A `-banner-linkedin.png` derivative is never needed.
- **Blog / article headers** also take the original image. No derivative.
- **YouTube channel art** (2560x1440 with a safe area) is out of scope for this skill.

## Approval gate

- **Never touch the original image.** Output goes to a new file named after the original (suffix added, base name unchanged).
- Confirm the plan with the user before converting: the source image and the exact output filename.
- **Never produce a non-Twitter variant.** If the user asks for LinkedIn, a blog header, or "other platforms", say that those accept the original image and stop. Do not invent a size for them.

## Inputs

- `source` — Path to the original image, e.g. `ai-thoughts/imgs/260806-1656.png`. Required.
- Target — fixed at 1500x600 (Twitter/X 5:2). Not configurable.

## Outputs

- `imgs/<base>-banner-twitter.png` — e.g. `260806-1656-banner-twitter.png`.
- `<base>` keeps the original filename exactly. The original file is never modified.

## Procedure

1. **Confirm the plan** with the user: source image and output filename. Get a go-ahead before writing the file.
2. **Check the original dimensions** with `magick identify "<source>"` so you can predict which axis will be padded.
3. **Resize to fit, then pad with black** with ImageMagick 7 `magick`:

   ```sh
   magick <source> -resize "1500x600" -background black -gravity center \
     -extent 1500x600 imgs/<base>-banner-twitter.png
   ```

   - `-resize "1500x600"` (no bang) scales to fit inside the box, preserving the aspect ratio — the image is never distorted or cropped.
   - `-extent 1500x600` then pads the leftover space; `-background black` makes the padding dark and `-gravity center` centers the image.
   - A 16:9 source (most infographics) becomes 1075x600 inside the frame, with about 212 px of black on each side. That is expected — never crop to avoid it.
   - If the source is wider than 5:2, the padding appears on the top and bottom instead.
   - Padding color is black; ask the user if they want a different background.
4. **Verify** the output with `identify` — dimensions must be exactly 1500x600.
5. **Report** the output path and confirm the original is untouched (git status shows the new file as untracked, the original unmodified).

## Quality rules

- Never overwrite or rename the source image.
- **Never crop the image.** Resize to fit and pad — cropping loses content.
- **Never generate `-banner-linkedin.png`, `-banner-youtube.png`, or any other non-Twitter variant.** Those platforms accept the original image. One target only.
- Do not use a size other than 1500x600.

## Verification

- `identify` reports exactly 1500x600.
- The source image inside the banner is undistorted (aspect ratio preserved).
- Black padding appears on the expected axis and the content is centered.
- The original file is byte-identical (unchanged `identify` output / git status).
- The output sits beside the original in the same directory.
- A re-render matches the existing banner pixel for pixel: `magick compare -metric AE <new> <existing> null:` prints `0`. Do **not** compare renders with `md5sum` — ImageMagick writes per-path metadata, so two identical images hash differently.

## Error Handling

- **Source not found**: list candidate images in `imgs/` and ask which to use.
- **Output already exists**: stop and ask whether to overwrite.
- **User asks for another platform**: explain that LinkedIn and blog headers accept the original image, and that this skill produces Twitter/X only. Do not generate anything.
- **No ImageMagick**: `magick` is always installed on the user's machines — skip checking for it and run the commands directly.
