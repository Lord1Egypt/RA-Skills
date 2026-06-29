---
name: image-generation
description: Create or revise document, PDF, web, or review images with the requested format, sharp raster output, and artifact validation.
---

# Image Generation Skill

Use this skill when creating, regenerating, or reviewing images, diagrams, screenshots, or generated graphics for Markdown, PDF, DOCX, web pages, merge requests, or release artifacts.

## What Went Wrong In claw-support !1

The image review loop failed because the work drifted between SVG and PNG, optimized technical metadata before preserving the requested format, and claimed image quality based on checks that did not match the maintainer's desired output. Treat this as the default failure mode to prevent.

## Rules

- Preserve the requested output format. If the reviewer asks for PNG, do not switch to SVG unless they explicitly accept that change.
- Preserve the requested style or earlier format when asked. Do not redesign a diagram as a workaround for readability feedback.
- Render raster images directly at the final source resolution. Never upscale a smaller bitmap and call it high resolution.
- For PDF-bound PNGs, use at least 300 DPI metadata and enough pixels for the printed/displayed size.
- Scale text, line widths, arrows, borders, spacing, and icons together. Large canvases with tiny text still fail review.
- Prefer vector-like drawing primitives rendered into the final PNG canvas for diagrams. Avoid screenshots or nested raster snippets unless the screenshot is the actual subject.
- Keep source-of-truth files clear: if the deliverable is PNG, make the build pipeline consume PNGs directly and avoid hidden SVG dependencies unless SVG is explicitly the editable source.
- Use `*.image.genai` prompt files as the source-of-intent convention for generated repository images. For `example.image.genai`, generate sibling `example.svg`, `example.png`, and `example.webp` files unless the task explicitly narrows the output formats.
- Do not add broad image-generation rules to repository `AGENTS.md` unless asked. Prefer a reusable skill or a task-local note.

## Workflow

1. Read the requested artifact path, target consumer, and exact format from the issue or MR discussion.
2. Inspect existing artifacts before editing: dimensions, format, DPI metadata, source generator, and where each image is embedded.
3. If a `*.image.genai` file exists or a new generated image is needed, treat that file as the editable prompt/brief and create the matching `.svg`, `.png`, and `.webp` siblings next to it.
4. Make the smallest change that satisfies the reviewer: format, resolution, clarity, or embedding.
5. Rebuild every downstream artifact that embeds the image, such as Markdown previews, PDFs, DOCX files, and release bundles.
6. Validate the actual output, not only the source file.

## `*.image.genai` Convention

- Keep the file next to the intended generated assets, for example `docs/architecture.image.genai`.
- Store the image brief, required dimensions, style constraints, text that must appear in the image, and downstream consumers in the prompt file.
- Generate all sibling formats from the same brief: `docs/architecture.svg`, `docs/architecture.png`, and `docs/architecture.webp`.
- Prefer the SVG sibling for diagrams and scalable documentation, the PNG sibling for PDFs or places that need stable raster rendering, and the WebP sibling for web delivery.
- Regenerate all siblings together after prompt changes so the formats do not drift.
- Before final review, run `{baseDir}/scripts/check-image-genai.py --root <workspace>` to find prompt files without generated image siblings and generated images that are older than their prompt.
- Mention the prompt file and the generated sibling dimensions in MR notes.

## Validation Checklist

- Image files have the requested extension and MIME format.
- Every changed `*.image.genai` file has matching `.svg`, `.png`, and `.webp` siblings unless the MR explains why a format is intentionally omitted.
- The generated image checker passes; add `All Images generated` to the final Definition of Done when it does.
- PNG files are generated at source size, not post-upscaled.
- PDF-bound PNG files have sufficient dimensions for their displayed size and about 300 DPI metadata when print quality is requested.
- Text and fine lines are readable after the image is embedded in the final PDF or web page.
- The PDF or DOCX contains the intended image objects and does not silently drop unsupported formats.
- CI checks enforce the important invariants when the repository already has artifact validation.
- MR notes state the exact format, dimensions, validation commands, and any remaining limitation.

## GitLab Review Handling

For image-related MR feedback, answer the latest reviewer request first. If new feedback contradicts an earlier fix, stop extending the previous approach and explicitly revert or narrow it to the latest requested format. Resolve discussions only after the final artifact has been rebuilt and checked.
