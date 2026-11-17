---
name: yaps-video-clipping
description: "Shorten a talking-head video with Yaps Auto Cut. Review the pauses, adjust the cut, and export. New users: install Yaps and sign in."
---

# Yaps Auto Cut

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.848 or newer. Check installed command help for later capabilities.

Feature readiness: Auto Cut, available in Yaps 2.3.848 or newer. Inspect cut --help, cut presets, and features list. No model download of its own; rendering requires the platform media dependencies.

## Workflow

Verify `<yaps> cut --help` exists before processing. Run `cut verify <video> --pretty`; stop on source_missing, not_video, no_audio, too_long, or too_big. Inspect `cut presets` and choose `natural` for ambiguous intent, `tight` for punchy social pacing, or `relaxed` for light trimming.

Create with `cut create <video> --preset natural`. Inspect the returned project with `cut show <id>`, `cut plan <id>`, and `cut export-plan <id>`. Report source/kept duration, removed percentage, cut count, and longest retained gap. If the user requested a review or plan, present it before rendering.

Tune with `cut set <id> --preset relaxed` or deliberate lead-in/lead-out adjustments. A custom `--pause-budget-ms` must not conflict with a named preset. Detection changes require `cut redetect <id>` when `requires_redetect` is true; plan-only settings do not. Avoid aggressive thresholds that remove speech merely to maximize the removed percentage.

Render `cut render <id> --output <new-cut.mp4>` and verify the result with `cut verify <output>`. Never target the source, preview proxy, or existing output; never run simultaneous renders for one project. Treat nothing_to_cut, no_speech, and render_failed honestly. Resume through cut list/show; never delete a project as routine cleanup. Deletion needs intent for the exact project and its managed artifacts.

## Boundaries

- Auto Cut removes pauses; it does not choose semantic highlights or rearrange scenes.
- Preserve source speech and check cut boundaries by listening.
- Do not substitute ad-hoc FFmpeg trimming when the installed Yaps command is missing.
