---
name: subclip-style-sampling
description: Learn the production style of a reference the user supplies (their own footage, brand, or a video they have rights to study) and build new original Subclip scenes in that style, using the AI model the user picks. Use for "in the style of", "match this look", or "sample this style".
---

# Subclip style sampling

Goal: take the look, pacing and motion of a reference and apply those patterns to new work on the user's own topic. Output is new, original scenes. Study patterns, never copy material.

## Hard limits

- Never import, reuse or re-render frames, footage, logos, captions, music, copy or characters from the reference. Use the reference only to measure patterns.
- Never imitate a named creator's identity: their face, voice, presenter, catchphrases, series names or signature characters. If the user names a channel or creator, work only from the features the user describes or from a reference they supply.
- Never clone a template from a third party's catalog. Build new scenes with Subclip's own runtime-layer tools.
- Use only fonts, media and audio that Subclip can load. Import user media through the native Media or Audio library first.

## Steps

1. **Get the reference.** Ask for the user's own file (video or images), or a description if they have no file. A link to a video they do not own is for pattern study only. Say so once.
2. **Choose the model.** Call `list_ai_models` and show the options that can read images. Ask the user to pick one. Use that model for the analysis. Do not pick one silently.
3. **Sample frames.** Call `extract_video_frames` every 1 to 2 seconds, plus at each hard cut. Inspect key frames with `view_current_frame` if they are in the editor.
   Then make a contact sheet of the whole reference: a grid of small, labelled thumbnails, one per sampled frame, in time order, with timestamps. Keep it in the project's media library as a study aid for the brief. Use it to read the pacing, cuts and layout at a glance, not to reuse any frame.
4. **Write the brief.** Record these fields:
   - palette: 5 to 6 dominant colours as hex, with roles (background, ink, accent)
   - type: style category (sans, serif, mono), weight range, size ratio between title and body
   - layout: grid, margins, how much empty space is used
   - motion: easing family, typical entry and exit length in frames, stagger pattern
   - pacing: average shot length in seconds, and how long text is held
   - graphic vocabulary: shapes, lines, grain or texture, how cuts and transitions happen
   Store the brief as project data with `set_project_data` so later scenes can read it.
5. **Confirm once.** Show the brief in short form and wait for the user to approve or change it. This is the only planned stop.
6. **Build original scenes.** Split the video into short beats, one runtime layer per beat, using `add_runtime_layer`. Read the brief values from the stored data. Validate each layer with `validate_html_motion_source` or `validate_runtime_layer_source`, then check its frames with `view_current_frame`.
7. **Preview and report.** Export a short preview with `export_video`. List what was taken from the brief and what the user should check.

## Fallbacks

- If no image-capable model is available, ask the user to describe the look in words, or to supply a few example frames they own. Build the brief from those.
- If frame extraction fails, use the user's written description and say the brief is not measured from the reference.
- If a requested style depends on material Subclip cannot load, such as a specific licensed font or a presenter's likeness, say which item is missing and offer the closest supported option.
