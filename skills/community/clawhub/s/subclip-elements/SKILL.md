---
name: subclip-elements
description: "Create and revise native editable Elements in Subclip: shapes, arrows, highlights, blur, paper textures, gradients, ordered effects, layer placement, and keyframed transforms."
---

# Subclip Elements

Use native `elementData.items` through the named Element tools. Elements are editable in ElementsPanel, on the canvas, and on UnifiedTimeline. They are the preferred primitive for simple shapes and effect layers; do not create HTML merely to draw a rectangle, circle, arrow, highlight, blur layer, or textured surface.

## Workflow

1. Call `list_editor_assets` and `list_element_catalog` for the exact active project. Reuse existing Element IDs when revising.
2. If the project is empty and untitled, follow `$subclip-video-editor` and rename it before the first Element write.
3. Call `add_element` once per intentional primitive. The default placement is `above-media`. Placement is a strict visual hierarchy, highest to lowest: `above-captions`, `above-text`, `above-motion`, `above-media`, then `behind-media`. Thus `above-captions` is above every editable visual track, while `above-text` is above text, motion graphics, and media but below captions.
4. Use `update_element` for timing, position, size, fill, stroke, opacity, rotation, corner radius, placement, order, and shape-specific corrections (`points`, `innerRadiusRatio`, `direction`, or pie `progress`). Blur-preset `blurIntensity` is a Gaussian radius measured from 0 to 200 pixels. Do not add corrected duplicates.
5. Use `add_element_effect` only with a type returned by `list_element_catalog`. Effects are ordered; use `update_element_effect` to change parameters or toggle visibility and `delete_element_effect` for one obsolete effect. `outline` follows the Element's alpha silhouette; place it after any transparency-producing effect and leave enough transparent padding for the requested width.
6. Use Element keyframes for motion. A simple move from A to B requires two keyframes. Use additional points only for a real intermediate change. The final keyframe holds until the Element ends; never add a redundant final hold keyframe.
7. Highlighter is a native preset intended to multiply over content. Paper is a shape with the paper effect. The Blur preset is a pure Gaussian backdrop mask with no glass tint, border, shadow, or pixelation mode: place it above the content to affect, then adjust `blurIntensity`. **Censor Blur** is a separate editable mosaic mask; use `censorBlockSize` for censor-block scale and `censorSoftness` only for optional background softening. A Blur effect added to an ordinary shape still processes only that shape's own pixels.
8. Re-list assets and verify every intended `elementItem` and effect ID. Seek to representative times and call `view_current_frame`; correct clipping, unsafe placement, contrast, stacking, or effect artifacts before reporting completion.
9. Delete only exact superseded Element/effect IDs created during the current run. Preserve pre-existing creator work.

For a composed multi-part mechanism whose layout cannot be represented as a small set of Elements and keyframes, route to `$subclip-motion-graphics` instead.

## Perspective tilt

Use `update_element` with optional `tiltX`, `tiltY`, and `tiltZ` fields in degrees, each from -88 to +88. X tilts vertically, Y tilts horizontally, and Z rotates in the image plane. These static appearance controls preserve existing animation and are editable under Perspective tilt in the layer settings. Use small angles for legibility; never add a back face or substitute a 3D model. Set all three to 0 to reset. For text overlays use update_text_item with the exact itemId; update_caption_style changes project-wide captions.

Keyframes: use `add_element_keyframe` for animated `tiltX`, `tiltY`, `tiltZ` (-88..88 degrees) and `scale` (multiplier). These values interpolate with the keyframe easing, preserve omitted settings, and remain editable in the keyframe UI.

## Tilt troubleshooting and scope

- Supply only finite numeric degrees for `tiltX` (vertical), `tiltY` (horizontal), and `tiltZ` (in-plane), within -88..88. Never send NaN, Infinity, or unit-suffixed strings.
- Reset with numeric zero on all three axes. Do not replace native layers with a 3D model.
- Use `add_element_keyframe` on the exact existing item ID and absolute project time to animate tilt and scale. Omitted tilt inherits the previous keyframe or base style; missing base tilt is zero. Keep existing scale unless the user requests a change.
- Changing base tilt alone will not override explicit tilt keyframes. Update the relevant keyframes instead. Older media keyframes need no recreation merely because they lack tilt fields; the sampler provides defaults.
- Distinguish saving settings from visually confirming the effect. Do not claim preview/export validation unless it was performed.
