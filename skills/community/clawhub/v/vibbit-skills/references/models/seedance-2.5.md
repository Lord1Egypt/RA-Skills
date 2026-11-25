# Seedance 2.5 guide

Use the contents to read only the section needed for the current operation. Each section retains its own parameters, authorization, and execution boundaries.

- [Seedance 2.5](#overview)
- [Prompting Seedance 2.5](#prompting)
- [Reference generation](#reference-generation)
- [Frames and storyboards](#frames-and-storyboards)
- [Editing and extension](#editing-and-extension)

<a id="overview"></a>

## Seedance 2.5

Model ID: `doubao-seedance-2-5-260628`. The current entry supports 480p, 720p, and 1080p; adaptive `-1` or 4–30 seconds; and up to 30 image, 10 video, and 10 audio references. Use [the API contract](../api/seedance.md) for the complete compatibility matrix and media limits.

Choose the mode from the requested result, while preserving any explicit model:
- Text and action description: [prompting](#prompting).
- New content informed by assets: [reference generation](#reference-generation).
- Start/end appearance or narrative frames: [frames and storyboards](#frames-and-storyboards).
- Modify an existing video or continue it: [editing and extension](#editing-and-extension).

Reference generation does not guarantee preservation of a source video's structure. Do not label a reference task as a precise edit. Do not carry 2.5-only fields into 2.0. Review complex bindings against the returned video rather than assuming that acceptance proves adherence.

<a id="prompting"></a>

## Prompting Seedance 2.5

Describe visible subjects, actions, camera movement, setting, and required continuity. For staged action, use a small number of integer-second intervals compatible with the requested duration. Time descriptions guide generation; they are not frame-accurate editing controls.

A single movement needs no artificial segmentation. Example for five seconds: from 0–2 seconds steam rises from a blue cup; from 2–5 seconds the camera slowly pulls back. State unwanted speech or captions when their absence matters, and set the actual audio option appropriately.

Reference names must correspond to the real ordered input arrays. A written “first frame” instruction is not a substitute for the first-frame field. Preserve the user's creative wording where possible and avoid adding unrelated action.

Use [reference roles](#reference-generation), [frame modes](#frames-and-storyboards), and [API parameters](../api/seedance.md) as needed.

<a id="reference-generation"></a>

## Reference generation

Use references to create new content with specified visual or audio guidance. Record each asset's type, array index, subject, and role. Preserve the order between the prompt and request.

For example, image 1 can define the product, image 2 the setting, video 1 the camera movement, and audio 1 the sound. A rough motion reference does not establish final product materials or scene appearance: describe those separately.

Use the `reference_*` arrays with `omni_reference_task_type: "reference"` and at least one reference. Do not combine this with single-image or first/last-frame fields. For the separate `auto` mode, use adaptive aspect ratio and duration `-1`; reference videos must meet the 4–30-second constraints in the [API](../api/seedance.md).

Check the returned result for correct subject and role binding. A failed binding is a quality issue, not permission for unlimited paid retries. Editing an existing video has a different [workflow](#editing-and-extension).

<a id="frames-and-storyboards"></a>

## Frames and storyboards

Distinguish narrative reference images from actual first/last-frame inputs. A contact sheet can guide a sequence but does not guarantee that each cell becomes a specific shot.

For real start/end constraints, use the API's first/last-frame fields with adaptive aspect ratio. The last frame requires a first frame; do not mix these fields with other image/reference modes. Match framing and aspect ratio across the endpoints and explain continuity requirements.

For a storyboard reference, identify the ordered images and intended sequence. Do not claim exact shot timing from image order alone. Reuse suitable existing images; do not automatically regenerate them just to split a board.

When exact timing or transitions are required, compose actual clips locally or through media composition. See [API compatibility](../api/seedance.md) and [storyboard production](../workflows/storyboard-video.md).

<a id="editing-and-extension"></a>

## Editing and extension

Use `edit` when the user wants to modify existing video content and `extend` when they want continuation. Both require at least one reference video and adaptive aspect ratio. Editing uses automatic duration `-1`; extension duration semantics require verification rather than assuming the same behavior. Read the [API contract](../api/seedance.md).

For edits, identify the primary source when several videos are present, the subject or property to change, the affected interval, and what must remain. Integer-second prompt ranges are generative guidance, not frame-accurate trim controls. Resolve conflicting aspect-ratio or duration requirements explicitly.

For 1:1 person/product/scene replacement, follow the [remake workflow](../workflows/one-to-one-remake.md) for audio routing and splitting. Edit inputs must be 4–30 seconds, with at most 30 seconds of reference video per request; `duration_seconds=-1` does not waive that limit. For unchanged sound, submit a real silent clip and restore the original audio after visual generation. For requested dialogue/BGM changes, preserve original audio in the input.

For extension, establish direction and whether a requested length means added time or total output time. The generic duration field's range does not prove extension semantics. Do not invent an `output_format` field or claim exact added duration without support from the current contract and returned result.

Review whether the source content is retained, whether the new portion joins naturally, and whether audio and timing are acceptable. Use [local composition](../capabilities/processing/local-composition.md) for precise assembly where appropriate. Preserve source and prior outputs.
