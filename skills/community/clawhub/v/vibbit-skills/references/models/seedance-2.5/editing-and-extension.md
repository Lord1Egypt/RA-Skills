# Editing and extension

Use `edit` when the user wants to modify existing video content and `extend` when they want continuation. Both require at least one reference video and adaptive aspect ratio. Editing uses automatic duration `-1`; extension duration semantics require verification rather than assuming the same behavior. Read the [API contract](../../api/seedance.md).

For edits, identify the primary source when several videos are present, the subject or property to change, the affected interval, and what must remain. Integer-second prompt ranges are generative guidance, not frame-accurate trim controls. Resolve conflicting aspect-ratio or duration requirements explicitly.

For 1:1 person/product/scene replacement, follow the [remake workflow](../../workflows/one-to-one-remake.md) for audio routing and splitting. Edit inputs must be 4–30 seconds, with at most 30 seconds of reference video per request; `duration_seconds=-1` does not waive that limit. For unchanged sound, submit a real silent clip and restore the original audio after visual generation. For requested dialogue/BGM changes, preserve original audio in the input.

For extension, establish direction and whether a requested length means added time or total output time. The generic duration field's range does not prove extension semantics. Do not invent an `output_format` field or claim exact added duration without support from the current contract and returned result.

Review whether the source content is retained, whether the new portion joins naturally, and whether audio and timing are acceptable. Use [local composition](../../capabilities/processing/local-composition.md) for precise assembly where appropriate. Preserve source and prior outputs.
