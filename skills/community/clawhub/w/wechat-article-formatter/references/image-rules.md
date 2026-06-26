# Image Rules

- Use static image sources only.
- If an image is part of the final article, make sure its `src` is already materialized as a real URL, local file, or `data:image/*` during preparation.
- Do not assume a downstream step will execute JavaScript to build image sources.
- Preserve chosen article images as durable `figure` / `img` / `figcaption` content when the upstream writing step has selected source-backed images.
- Do not add decorative images during formatting. Formatting may style selected images, but editorial selection belongs to the writing or research step.
- **For local preview pages intended for manual copy-paste into the WeChat backend, all local image files MUST be pre-converted and inlined as Base64 Data URLs (`data:image/*;base64,...`) directly in the `src` attribute of the HTML draft.** Do not use local relative paths (like `./image.png`). Under the local `file://` protocol, browser CORS policies will block script-based `fetch` or canvas `toDataURL` calls to local files during the clipboard copying phase, causing local relative images to copy as broken links. You can use [convert_cover_to_base64.py](../scripts/convert_cover_to_base64.py) to convert standalone cover images to Base64, or run [inline_images.py](../scripts/inline_images.py) to batch inline body images in HTML.
- When the deliverable is only a local preview HTML page, include image-copy handling inside that page to gracefully process external HTTPS sources, but do not rely on it to dynamically resolve local filesystem files.
- Treat base64 image copy as a preview-and-copy convenience. Before formal publication, verify in the WeChat backend that every copied image is visible and stable.
- Do not require a backend image upload service for normal preview-and-copy tasks.
