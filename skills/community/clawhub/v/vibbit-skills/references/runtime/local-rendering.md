# Local rendering

Use local rendering for an entire video, a generated clip, or an overlay within [hybrid production](../workflows/hybrid-video.md). Existing FFmpeg is suitable for simple composition. If installation is declined, use an appropriate cloud path.

1. Check [external dependencies](external-render-dependencies.md) on the actual execution host. Node 18 supports this skill's client; it does not establish compatibility with every render engine.
2. Use the user's real project directory outside the skill. Copy a selected template into a working project and preserve the original and its version. Input media must be the actual assets, not thumbnails.
3. Inspect available space, engine versions, dimensions, frame rate, duration, and audio requirements. Choose which stage owns subtitles and which existing text must remain.
4. Use real user data and audio. Preview through the selected official engine and inspect the exported result. An HTML preview is not a rendered video.

Track the process, logs, inputs, and output version. Inspect a running process before starting a duplicate. Verify a nonempty output file and its real duration, streams, dimensions, frame rate, and alpha when relevant, using ffprobe or an available equivalent.

## Timing and composition

Distinguish full videos, clips, overlays, and source previews. Record both an asset's own timeline and its placement in the final timeline. Keep subtitles aligned with the final audio. Verify synchronization after frame-rate conversion. Test transparent exports against contrasting backgrounds and confirm that the receiving pipeline preserves alpha.

Ordinary subtitles can be rendered locally. Use cloud packaging when the task specifically needs its templates or capabilities.

## Revisions and failures

Render revisions to new paths and preserve previous approved outputs. Do not promise incremental rendering unless the chosen engine supports it. Reuse completed exports when only upload or downstream assembly failed.

Classify failures as dependency, project code, parameters, media, rendering, or upload problems. Inspect uncertain process state before a bounded retry. Resume a cloud task by its existing ID rather than submitting again.

Deliver according to the [render artifact contract](../contracts/render-artifact.md). If only the source project is ready, report it as source, not as a finished video. Review the actual export with [video review](../capabilities/analysis/video-review.md).
