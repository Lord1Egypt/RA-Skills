---
name: teaching-diagram-maker
description: |
  Create, edit, and visually verify durable teaching diagrams for study notes and technical explanations. Use for mechanisms, pathways, causal chains, timelines, protocols, model comparisons, spatial layouts, annotated evidence maps, or broken SVGs with clipping, overlap, or text-encoding problems. Trigger phrases include "draw a diagram", "explain this visually", "make a pathway map", "compare these models", and "fix this SVG".
license: MIT-0
---

# Teaching Diagram Maker

Create diagrams that teach one idea clearly and remain editable. A diagram is
complete only when it is saved beside the relevant note, embedded at the point
of use, rendered, and visually inspected.

## Scope

Use this skill for:

- mechanisms, pathways, causal chains, and feedback loops;
- temporal protocols and before/after sequences;
- spatial or circuit layouts;
- comparisons that benefit from repeated visual grammar;
- input, parameter, and output relationships;
- annotated evidence maps when a source figure is hard to read;
- SVG clipping, overlap, font, encoding, and preview failures.

When used with `illustrated-paper-guide`, that skill decides which checkpoint
needs a diagram and where it belongs. This skill owns diagram craft and QA.

## Workflow

1. **Locate the explanation.** Read the surrounding note and improve it in
   place. Do not create an orphan image.
2. **Define one learning job.** Write the question the diagram should answer in
   one sentence.
3. **Choose the medium.** Prefer SVG for editable conceptual diagrams. Use a
   plot or raster image when the source data or visual texture requires it.
4. **Design the reading order.** Make the first, next, and final visual targets
   unambiguous.
5. **Create the asset.** Save it under the note's `images/` directory with a
   descriptive kebab-case filename.
6. **Embed it at the point of use.** Add a short “How to read this” explanation
   beside the image.
7. **Validate the file.** Confirm UTF-8 text, valid markup, and resolvable links.
8. **Render and inspect.** Check the actual output, not only the source code.
9. **Iterate.** Fix clipping, overlap, density, contrast, and misleading visual
   claims before finishing.

## Diagram Selection

| Learning problem | Useful diagram |
| --- | --- |
| Competing explanations | Side-by-side hypothesis cards |
| Multi-step mechanism | Directed causal chain |
| Timing or protocol | Timeline or sequence comic |
| Anatomy or circuit placement | Spatial map with labeled regions |
| Parameter changes an outcome | Small-multiple comparison or response curve |
| Evidence vs interpretation | Layered evidence map |
| Dense source panel | Annotated overlay with boxes and arrows |

Skip a diagram when the content is only a naming fact and no relationship is
made clearer visually.

## SVG Standards

Start SVG files with an explicit UTF-8 declaration and view box:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="700" viewBox="0 0 1200 700">
```

Use these defaults unless the surrounding note already has a visual system:

| Element | Default |
| --- | --- |
| Background | `#f8fafc` |
| Title | `#0f172a`, 16–18 px, weight 700 |
| Body | `#334155`, 11–13 px |
| Secondary text | `#64748b` |
| Card | white fill, `#cbd5e1` stroke, rounded corners |
| Font | `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif` |

Craft rules:

- Give each diagram one job.
- Use a limited palette and consistent colors for repeated meanings.
- Prefer large, spaced panels over one crowded canvas.
- Put the meaningful contrast directly on the panels when useful.
- Keep labels readable at the size used in the note.
- Use arrows only when direction or causality is intended.
- Distinguish measured evidence from explanatory analogy.
- Avoid decorative elements that compete with the lesson.

## Annotating Source Figures

Only annotate a source figure when the user's context and the intended output
permit reuse. Preserve the source citation and do not present the annotation as
original evidence.

Use boxes, arrows, and short labels to identify the exact visual evidence. Do
not cover axes, legends, scale bars, uncertainty marks, or controls. If reuse
rights are unclear for a public output, provide a source link and create an
original schematic instead.

## UTF-8 and Rendering

For diagrams containing non-ASCII text:

- write and read the file explicitly as UTF-8;
- include `encoding="UTF-8"` in SVG;
- verify the file can be decoded after writing;
- render the SVG to an image or open it in a visual preview;
- if a preview cache is stale, use a new filename and update the note link.

A file that exists but renders as a broken image may have invalid XML, damaged
encoding, an unsupported font reference, or a bad embedded asset. Inspect those
before assuming the Markdown path is wrong.

## Visual QA Checklist

Before finishing, verify:

- no text is clipped or hidden behind shapes;
- arrows do not cross labels or imply the wrong direction;
- margins prevent canvas-edge cropping;
- font size and contrast work at normal note width;
- repeated concepts use consistent colors and shapes;
- the visual conclusion matches the accompanying text;
- the image link resolves from the note;
- non-ASCII text survives a UTF-8 round trip;
- at least one rendered output has been inspected visually.

Report the asset path, where it was embedded, how it was rendered, and any
remaining limitation.
