---
name: subclip-review-safety
description: Review, verify, undo, redo, and safely recover Subclip video edits using rendered frame inspection, project state, native history, and saved revisions. Use after multi-step edits or when the user reports a visual, timing, caption, asset, undo, or project-state problem.
---

# Subclip Review and Safety

1. Read the active project and call `list_editor_assets`.
2. Confirm item IDs, timings, canvas bounds, asset references, caption order, and project duration. Treat a canvas-background-only interval after the last intentional item as a blank-tail defect, not as content. Preserve deliberate holds; otherwise use `set_project_duration` to collapse the project clock to the intended endpoint and verify the saved duration again.
3. For more than one moment, prefer one `get_timeline_contact_sheet` call with all the changed times (see `$subclip-timeline-contact-sheet`) over separate frame calls; it is the same composed render with many labelled tiles. For a single targeted check, seek to the moment and call `view_current_frame` with the same active `projectId` at each one. For an explicitly timed payoff or spectacle beat, inspect before, inside the visible peak, and after the beat; do not use a source read or the exact tween start as proof of its peak state. This is a live capture; if the requested project is not visible, open it instead of accepting a saved thumbnail.
4. Inspect pixels for black bars, clipping, off-canvas placement, distorted media, text collisions, unsafe margins, missing layers, and incorrect stacking.
5. Correct every visible defect, then re-read state and re-inspect the corrected frames. Do not stop after issuing a correction.
6. Use `undo_editor_change` for the latest in-session mistake and `redo_editor_change` only when clearly intended.
7. Use `list_project_history` before considering recovery. Call `restore_project_history` only after explicit confirmation because it replaces the current saved state, and pass `confirmed: true` with that exact approved revision. The displaced current state is preserved in history.

Treat successful tool output as necessary but not sufficient. `get_runtime_layer` returns source, not pixels, and must never be described as frame review. Never claim completion without rendered-frame evidence after the final mutation. A cancelled correction means the edit is unverified, not completed. Never delete projects, export, or consume cloud credits during review without permission.

Use `seek_timeline` with `projectId` before `view_current_frame` with that same `projectId` when checking exact beginning, middle, and ending moments. Do not emulate a seek through raw state paths or terminal commands.
