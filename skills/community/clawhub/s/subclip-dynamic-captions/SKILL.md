---
name: subclip-dynamic-captions
description: Turn an existing or newly generated transcript into editable, semantic, high-retention Dynamic Captions using Subclip presets, sparse word-priority tiers, intentional phrase pages, and visual verification. Use when the creator asks for dynamic, viral, animated, emphasized, word-by-word, scroll-stopping, or preset-based captions. Do not use for ordinary subtitle correction or unrelated TextPanel overlays.
---

# Subclip Dynamic Captions

Create native captions that remain editable in Subclip’s Captions panel. Before assigning priorities or pages, read both [references/intelligence-contract.md](references/intelligence-contract.md) and [references/semantic-layout.md](references/semantic-layout.md). The intelligence contract is the authoritative port of Subclip-web’s semantic prompt and normalization behavior; the layout reference chooses the visual preset.

## Workflow

1. Inspect `active-project` and `list_editor_assets`. Read the current caption words, speaker/source ownership, canvas, current style, and director brief.
2. Establish trustworthy word timing without discarding other sources:
   - Reuse existing caption words when present.
   - For host-provided SRT/VTT cues, use `import_caption_cues_for_media_item` on the exact trimmed media item.
   - Otherwise call `transcribe_project` with `purpose: "captions"` for one exact `mediaItemId` or `audioItemId`. Use the user’s requested local/cloud mode; speaker-aware work is cloud-only. End the turn for a background job and let Subclip resume it.
3. Call `list_dynamic_caption_presets`. Honor an explicit preset. Otherwise choose the least distracting preset that matches the voice and content using the reference.
4. Call `apply_dynamic_caption_preset`. This activates Dynamic Captions, applies the editable base/priority styles, and creates a safe initial grouping.
5. Run the complete four-part analysis from the intelligence contract: local summary, Important IDs, Medium IDs, and a selective hook-ID subset of Important. For long material, analyze bounded chronological chunks and normalize the merged result. Call `set_dynamic_caption_priorities` once with exact IDs. Never rewrite spoken text merely to create emphasis.
6. Build pages using the intelligence contract’s template bounds, phrase rules, 250 ms gap handling, hook isolation, and orphan repair. Hook IDs control page rhythm but are not a third saved priority tier. Call `arrange_dynamic_caption_pages` once only after proving every current word ID appears exactly once, in order, within one source owner and the selected preset’s hard page limit.
7. Use `update_caption_style` only for an explicit creator adjustment or a necessary legibility correction after the preset. Preserve the preset hierarchy.
8. Seek and inspect the opening hook, representative middle phrases, every speaker/source boundary, the longest page, and the ending. Correct unsafe placement, unreadably dense lines, weak contrast, excessive emphasis, or collisions, then inspect again.
9. Re-read captions to prove preset, word priorities, complete page coverage, source ownership, and layer visibility. Save the semantic summary, Important/Medium/hook decisions, page strategy, and verification result in the director brief before reporting completion.

Do not replace Dynamic Captions with ordinary TextPanel duplicates, fabricate words, label filler as hooks, clear another item’s caption batch, or use raw project-state writes for controls exposed by these tools.

## Perspective tilt

Use `update_caption_style` with optional `tiltX`, `tiltY`, and `tiltZ` fields in degrees, each from -88 to +88. X tilts vertically, Y tilts horizontally, and Z rotates in the image plane. These static appearance controls preserve existing animation and are editable under Perspective tilt in the layer settings. Use small angles for legibility; never add a back face or substitute a 3D model. Set all three to 0 to reset. For text overlays use update_text_item with the exact itemId; update_caption_style changes project-wide captions.

## Tilt troubleshooting and scope

- Supply only finite numeric degrees for `tiltX` (vertical), `tiltY` (horizontal), and `tiltZ` (in-plane), within -88..88. Never send NaN, Infinity, or unit-suffixed strings.
- Reset with numeric zero on all three axes. Do not replace native layers with a 3D model.
- Caption tilt is rendered by the active DynamicCatptionsLayer renderer. Use update_caption_style for global appearance; existing per-clip styles may override global values. The UI also supports selected-clip scope. Do not claim caption tilt keyframes exist: caption tilt is currently static.
- Distinguish saving settings from visually confirming the effect. Do not claim preview/export validation unless it was performed.
