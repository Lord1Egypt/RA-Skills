---
name: yaps-image-generate
description: "Create an image from a written prompt with Yaps. Save the result or make a sticker. New users: install Yaps and sign in."
---

# Yaps Image Generation

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Image generation; query supported hardware, memory requirements, and installed model. Sticker output additionally requires Background Removal.

## Workflow

Inspect `features list` and `media generate-image --help` for supported hardware, model availability, sizes, and options. Do not promise operation on every Mac or Windows device. Download models only after authorization using `features image-generation --enable`.

Choose a new `.png` path. Run `<yaps> media generate-image --prompt <prompt> --output <new.png> --pretty`. Use the installed default size unless the user requests higher resolution; `--size 1024` is available on supporting builds. Add `--seed <integer>` only for a requested reproducibility control. Add `--sticker` only when requested and the separate background-removal dependency is ready.

Distinguish initial model loading from inference in progress reports without promising a fixed runtime. Verify the actual image, dimensions, seed, steps, duration, and device returned by Yaps. Compare the result with the requested subject and composition. A valid PNG alone is not a quality pass. Do not loop through generations indefinitely or silently switch services.

## Boundaries

- This generates a new image; do not promise arbitrary image editing from this command.
- No unsupported hardware claim or silent sticker downgrade.
- No automatic overwrite or uncapped regeneration loop.
