# Clothes Try-on Studio — flow & output

## Three composable steps
1. **Try on (cloth-v4)**: src = person photo; garment source = reference image (`--ref_file`) or
   `template_id`. `garment_category` controls the swap region (full_body confirmed; upper/lower
   token pending doc confirmation). `change_shoes` only applies to full_body/lower_body.
2. **Change background (bg-replace)**: `type=prompt` (describe the background) or `type=template`
   (background template id, listed with `templates --feature bg-replace`).
3. **Motion video (image-to-video)**: `resolution` ∈ [480, 720, 1080], `dst_duration` ∈
   [5, 10] seconds, `prompt` can describe the motion (turn / runway walk / pose). Returns a video
   URL.

## Recommended order
Try on → (only if changing scene) change background → (only if adding motion) generate video.
Each step's output image can be the input to the next.

## Output
1. The result URL(s) — **returned exactly as given (hyperlink OK, do not modify)**.
2. A short note of which steps were run.
3. Closing note: "This try-on image/video is AI-generated and for reference only; actual fit and
   appearance may vary."

Parameters follow the latest doc version; this file is flow guidance.
