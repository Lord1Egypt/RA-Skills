---
name: subclip-asset-creation
description: Create or revise images, illustrations, textures, plates, and backgrounds locally, then import them as ordinary editable Subclip MediaPanel and timeline assets. Use when the user asks to generate an image/background or change its colors, subject, composition, or style.
---

# Subclip Local Asset Creation

For music or songs, use `$subclip-music-generation` or `$subclip-songwriting` and the first-party `generate_music` tool. Music is an Audio asset; do not create image projects or use speech synthesis for it.

You may create images (or video and audio) with ANY provider you have access to: your own image generation (for example Codex image generation, or a Grok bot), a local tool, or a model you call yourself. Subclip's cloud generation (`$subclip-image-generation`, which uses the user's AI credits and cloud storage) is optional. Use it when the user asks for Subclip generation or when its models are clearly the best fit; otherwise generate with what you have and import the result.

Asset creation happens locally; timeline placement happens through Subclip.

1. Inspect the canvas aspect ratio and the user's visual request.
2. Use the best locally available image-generation or image-editing skill/tool. It does not need to be a Subclip skill.
3. Save every result as a real file. Anywhere you can write is fine: you do not need to write inside the project. Use PNG, JPEG, or WebP for stills. Give files descriptive, revisioned names such as `warm-paper-background-v1.png`.
4. Never overwrite an existing generated or imported source. A requested revision creates `v2`, `v3`, and so on, preserving rollback and comparison.
5. Import it with `import_external_media`. Pass exactly one of `path` (an absolute file path on the computer running Subclip), `url` (a public https link) or `base64` (inline content, up to 64 MB, for when you cannot share a path), plus `startTime` and optionally `durationSeconds`. It works for images, video and audio, validates the file, copies it into the project and creates a normal MediaPanel file and native timeline item. `import_generated_media_to_timeline` remains available for files already inside the project workspace and is the tool for `replaceItemId` (below).
6. For a revision of an existing timeline visual, put the new file inside the project workspace and call `import_generated_media_to_timeline` with `replaceItemId`. This swaps the source while preserving that item's timing, position, crop, size, roundness, opacity, and other manual controls.
7. Seek to the edited time and inspect the composed frame. If the user dislikes a color, background, or image, edit the local source into a new revision and import/replace again.

Do not use HTML, CSS, SVG markup embedded as code, TSX, or a separate Remotion composition as a shortcut for an ordinary image or background. Do not claim a generated asset is editable pixel-by-pixel inside Subclip; it is editable as a normal media layer, while semantic image revisions are made locally and re-imported.

For generative changes to clip content (objects, colors, environment), route to `$subclip-video-generation` and discover `flux-video-edit`. Use ordinary timeline tools for trims/reframes. Talking portraits route to `$subclip-avatar-generation`; Avatar IV needs portrait AND supplied speech audio.

## Let the creator choose

When several results could work (images, a clip, an AI output), show them before importing: `$subclip-asset-options` (`get_asset_options`, `preview_asset`). One numbered options sheet lets the creator answer "number 3" without any project being open.
