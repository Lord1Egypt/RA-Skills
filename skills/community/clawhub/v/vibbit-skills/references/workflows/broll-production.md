# B-roll and overlays

For recorded or previously generated footage, use [material reuse](../resources/materials.md) to search the action/scene supporting the script, read detail and inspect the adopted interval. Trim suitable footage directly; generate a shot only when the candidate serves as a reference or leaves a gap. Map source intervals onto the adopted main audio, not directly onto its subtitle timeline.

B-roll can come directly from the material library. Use [Agent semantic mixcut](semantic-mixcut.md) to compare candidates against the visual need and inspect actions, product identity, and usable intervals. Search supplies candidates; the Agent makes the final decision. Full-video assembly defaults to cloud editing, continuing the primary speech across picture changes and routing source sound separately. A B-roll-only request ends with the selected clip.

Use this for supporting shots, charts, numbers, cards, interface animation, and annotations. A complete video can keep these in one project without forced intermediate clips.

Record the element's purpose, real data/media, duration, ratio, audio, insertion point, and whether it replaces the full frame or overlays it. B-roll need not be newly generated video.

Standalone B-roll discovery and adding inserts to an avatar both use the library directly, without reference analysis or a saved viral template. Fetch detail for selected assets; otherwise retrieve candidates within the allowed pool by media type, group, name/tags, or content. The Agent inspects subjects, actions, product variants, and usable intervals. A suitable still can be used directly without forced video generation.

For avatar inserts, retain adopted audio, valid transcripts, and generated performance, mapping chosen pictures to actual speech timing. Default to cloud picture replacement while continuing the voice; mute incidental B-roll speech and declare any wanted source sound separately. Changing inserts does not regenerate speech or the avatar. Generate authorized gaps when the pool is insufficient, while honoring explicit requests for newly generated visuals. For discovery-only requests, deliver usable media, IDs, source intervals, and selection reasons without full-video composition. Reuse only the relevant selection/timing steps of [Agent semantic mixcut](semantic-mixcut.md).

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
