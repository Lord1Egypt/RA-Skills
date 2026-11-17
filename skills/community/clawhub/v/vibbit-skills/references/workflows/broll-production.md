# B-roll and overlays

Use this for supporting shots, charts, numbers, cards, interface animation, and annotations. A complete video can keep these in one project without forced intermediate clips.

Record the element's purpose, real data/media, duration, ratio, audio, insertion point, and whether it replaces the full frame or overlays it. B-roll need not be newly generated video.

| Visual need | Production route |
| --- | --- |
| Suitable existing image, video, or chart | Reuse and crop/layout as needed |
| Static product, concept, or scene | [Image generation](../capabilities/generation/image-generation.md), with optional light pan/zoom during assembly; no forced video generation |
| Action, changing scenes, or camera movement | [Video generation](../capabilities/generation/video-generation.md) from text, images, or supported references |
| Charts, numerical comparisons, exact text, or interface animation | [Programmatic video](../capabilities/generation/programmatic-video.md), preferably an available HyperFrames template/environment; preserve existing projects and explicit engine choices |
| Simple labels, assembly, or overlays | Existing composition tools without a new animation project |

Use real data for charts; generated images do not supply precise numerical/text layout. An existing Matplotlib environment can produce suitable static plots, but routine talking-head charts should not trigger installing a plotting library. Reuse a fitting template. Check the selected environment once and recheck on change/failure; follow [dependency setup](../runtime/external-render-dependencies.md) when installation is actually needed.

After script adoption, prepare assets without final-timing dependencies alongside audio. Bind their real placement after audio adoption. Share an applicable [transcript record](../runtime/transcript-tools.md) with captions: sentence ranges support passage-based B-roll; word-triggered graphics/sounds need valid word boundaries. ASR does not establish visual action. Establish data and a representative chart layout before reusing it across charts.

For a user template, select an actual clip/overlay [template](../resources/render-templates.md) and load only its engine/project. Without a template, an official engine workflow can create a custom composition; do not claim a nonexistent business template was applied.

For local full-video delivery, use existing FFmpeg for simple assembly or keep animation, main video, and audio in the same project. Avoid unnecessary transparent intermediates or upload/download round trips.

For cloud assembly, reuse available clips or completed exports. If installation is declined, proceed with available cloud media and identify missing animation capabilities through [hybrid production](hybrid-video.md). Verify upload, complete composition configuration, and account access before making dependent assets.

Overlays require real alpha support through export, upload/transcoding, and composition. A filename extension does not prove it. If compatible with the user's editing needs, precompose an overlay with its background locally when the receiver cannot preserve alpha.

Decide whether to retain B-roll sound and main speech; avoid competing narration. Insertions that change duration affect later captions/timing, while visual replacement may preserve the main soundtrack. Record purpose, version, real output, and placement in the [artifact record](../contracts/render-artifact.md). Revise the affected element and necessary final export while retaining unrelated media.
