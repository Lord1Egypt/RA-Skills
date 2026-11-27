# Image pack
Layer 1: resolution/aspect, format, alpha channel, file size; brand palette ΔE when a palette is given.
Layer 1 for images that contain copy: compare the required text against the rendered text (OCR, or a careful letter-by-letter reading labelled `visual-read` when OCR is unavailable); check for confusable glyphs (O/0, l/1, S/5); check that no text touches or crosses the canvas edge (text bbox inside a safe margin of 5% or more); measure text/background contrast (WCAG ratio of at least 4.5).
Layer 2: prompt alignment with VQAScore (preferred over CLIPScore for compositional prompts); aesthetic predictor or ImageReward as a soft signal, never a sole gate.
Judge checklist (vision model, one item per finding, cite region coordinates): hands/limbs/anatomy; text rendered correctly; every prompt subject/attribute/relation present; composition and negative space; style consistency with references; artifacts/watermarks; safety policy.
For multiple candidates: compare pairwise with swapped order.
