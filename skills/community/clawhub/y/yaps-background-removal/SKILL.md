---
name: yaps-background-removal
description: "Remove an image background with Yaps. Save a transparent PNG, solid background, or outlined sticker. New users: install Yaps and sign in."
---

# Yaps Background Removal

Read [the runtime guide](references/runtime.md) before the first operation. It defines `<yaps>`, account readiness, local permissions, and file handling.

Required Yaps version: 2.3.124 or newer. Check installed command help for later capabilities.

Feature readiness: Background Removal model, installed only after authorization when missing. Check media remove-background help for current platform support.

## Workflow

Select the exact JPG, PNG, WebP, or BMP source and a new PNG destination. Run `<yaps> media remove-background <input> --output <new.png> --pretty`. Transparent output is the default.

For a solid background use `--mode color --color #RRGGBB`. For a die-cut sticker use `--mode sticker --color #ffffff`; here colour means the outline, not the background. Accept only a literal # followed by exactly six hex digits.

Verify the file, dimensions, device, and mask coverage reported by Yaps. Coverage below 0.005 indicates no clear subject and must not be described as a clean successful cutout. Where preview is available, inspect alpha edges, hair, holes, fine detail, and any unwanted background islands. Preserve the original and previous exports.

## Boundaries

- Do not replace the source or silently change the requested output mode.
- An empty mask or unreadable output is not success.
- Use Yaps's processing, not an unrequested hosted image API.
