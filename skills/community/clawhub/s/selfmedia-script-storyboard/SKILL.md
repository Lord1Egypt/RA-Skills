---
name: selfmedia-script-storyboard
description: Align a user's narration, measured subtitles, audio, preview, and frame-based timeline while preserving the selected composition and source facts.
license: MIT-0
metadata:
  version: "1.0.0"
---

# Script and Storyboard Timeline

Use this skill to calibrate narration, captions, visuals, and scene timing in a video project. The user chooses the workspace and the actual file paths; do not assume a particular directory layout. Do not rewrite factual claims, the approved script, or the chosen composition while adjusting timing.

## Gather and compare inputs

Read the approved narration, generated SRT, audio file, visual preview, render data/props, and existing timeline from their user-specified locations. Confirm that each file belongs to the same task/version. Treat the existing timeline format as project-specific: preserve its schema, project identifiers, composition ID, and fields the renderer needs. Do not replace a native timeline with the sample schema in this package.

Use measured audio and subtitle timing, not estimated speech speed. When needed, obtain media duration from the installed `ffprobe`:

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 /path/to/media.mp4
```

If the final voiceover or subtitles changed, use those final files for calibration. Do not distribute narration beyond the measured audio, invent scene time to fit an estimate, or silently stretch a short segment. Clearly record any intentional silence or visual hold according to the project's existing schema.

## Time and edit rules

- A timeline is the single authority for scene timing. Confirm the project's frame rate and time unit before editing.
- Scenes must be ordered, continuous, and non-overlapping unless the existing renderer explicitly represents a planned gap or overlay separately.
- The final scene and captions must fit the preview/video duration. Voiceover must fit the intended narration interval; music-only work may have no voiceover file.
- Captions, rankings, names, and visible text must match the approved script and frozen source facts. Flag mismatches; do not resolve them by guessing which version is right.
- Edit only the user's explicitly selected timeline file. Never modify neighboring tasks or overwrite a prior successful render.

## Optional generic contract checker

The sample checker validates a small, documented frame-based JSON contract with half-open scene intervals `[start_frame, end_frame)`. It is useful for projects that adopt that format; it does not parse or rewrite every renderer's native timeline format.

```bash
python3 scripts/validate_timeline.py examples/timeline.json \
  --voiceover-duration 2.8 --preview-duration 3.0 --captions examples/captions.srt
python3 scripts/self_test.py
```

Keep project-specific adaptation explicit and inspect the resulting video after any timing change.
