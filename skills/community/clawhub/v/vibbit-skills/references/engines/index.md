# Render engine selection

Use an existing FFmpeg installation for simple trimming, joining, cropping, subtitles, and mixing. API resource queries do not require a render engine.

For programmatic video, preserve the user's selected engine or the existing template's engine and version. Otherwise, React compositions suit [Remotion](remotion/index.md); HTML/CSS compositions suit [Hyperframes](hyperframes/index.md). Both can produce full videos, clips, or overlays when the actual project supports them.

Official engine skills are external dependencies. Keep project packages in the video project, not in Vibbit Skills. Read [dependency checks](../runtime/external-render-dependencies.md) and only the selected engine's relevant official modules.

Cloud `MEDIA_PRODUCTION` composes media; it does not execute either local engine or deploy a third-party render service. Follow the [render artifact contract](../contracts/render-artifact.md).
