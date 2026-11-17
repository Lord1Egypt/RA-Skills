---
name: seewo-courseware-generator
description: "Generate a multi-page, editable courseware file (.enbx) that opens natively in the Seewo Whiteboard (希沃白板) desktop client, starting only from a topic/outline or free-form description of lesson content. Use whenever a user asks to 生成课件 / 做一份希沃白板课件 / 把内容做成能在希沃白板打开的课件, or provides teaching material and wants a 希沃白板-ready multi-page slideshow. The skill produces a real native .enbx (希沃私有格式, a ZIP of XML plus media), not a PPTX, so the result opens directly in 希沃白板."
---

# Seewo Courseware Generator（希沃白板课件生成）

## Overview

This skill turns a teaching description (topic, outline, article, or bullet points) into a
**native 希沃白板 (Seewo Whiteboard) courseware file** with the `.enbx` extension. The
`.enbx` format is a ZIP archive of XML descriptors plus media; this skill writes that
package directly so the output opens in the 希沃白板 client without conversion.

The skill ships two scripts:
- `scripts/generate_enbx.py` — builds the `.enbx` from a JSON spec.
- `scripts/validate_enbx.py` — verifies the output against the same structural checks a
  real `.enbx` sample passes (ZIP integrity, XML well-formedness, resource resolution,
  Slide↔Board id mapping).

Read `references/enbx_format.md` for the full format specification and the generator's
input schema whenever detail is needed.

## When to use

Trigger on requests such as:
- "帮我生成一份关于《光合作用》的希沃白板课件"
- "把这段课文做成多页课件，能直接拖进希沃白板打开"
- "根据下面的大纲，做一份 10 页的复习课件"
- Any task where the deliverable must be **openable in 希沃白板** (not just a PPT/PDF).

Do **not** use this skill for plain PPTX/PDF generation — those are different formats.
(Note: 希沃白板 can also *import* PPTX, so if a user only needs import compatibility and
not the native `.enbx`, a PPTX path is an acceptable alternative; but the native `.enbx`
is the primary goal here.)

## Workflow

### Step 1 — Collect / clarify the content
Gather the lesson topic and the per-page content. Accept a free-form description, an
outline, or pasted text. If the user gave only a topic, propose a sensible outline
(title slide + several content slides) and confirm or proceed. Keep it light — one
round of clarification is enough; otherwise infer a reasonable structure.

### Step 2 — Author the JSON spec
Write a JSON spec file (e.g. `/workspace/spec.json`) describing the courseware. Use the
schema from `references/enbx_format.md`. Two authoring modes:

**Convenience mode** (recommended for most lessons) — let the skill auto-layout the page:
```json
{
  "courseware_name": "光合作用 单元复习",
  "pages": [
    {"layout":"title_slide","background":"#1565C0","background2":"#0D47A1",
     "title":"光合作用","subtitle":"初中生物 单元复习"},
    {"layout":"content","background":"#FFFFFF","title":"一、概念","subtitle":"...",
     "bullets":["场所：叶绿体","条件：光照","原料：CO₂ + H₂O"]},
    {"layout":"content","background":"#FFFFFF","title":"二、对比","table":{
       "header":true,"rows":[["项目","光反应","暗反应"],["场所","类囊体","基质"]]}}
  ]
}
```
**Explicit mode** — provide `elements` per page for full control (title/text/bullets/table/
box/picture with exact x/y/w/h). When `elements` is present, convenience fields are ignored.

Design notes:
- Canvas is 1280×720 by default; coordinates are in pixels from the top-left.
- Use `background` (and optional `background2` for a gradient) per page for visual variety.
- `box` (colored rectangle) and `picture` (from an image file path) enable title bars,
  highlight boxes, diagrams, and photos.
- Keep text concise; the generator auto-wraps body text and computes element height.

### Step 3 — Generate the .enbx
Run the generator with the managed Python (this script uses only the standard library):
```bash
/Users/juno/.workbuddy/binaries/python/versions/3.13.12/bin/python3 \
  /Users/juno/.workbuddy/skills/seewo-courseware-generator/scripts/generate_enbx.py \
  /workspace/spec.json /workspace/课件名.enbx
```
This emits a single `.enbx` file. Report the output path to the user.

### Step 4 — Validate
Always validate the result before delivering:
```bash
/Users/juno/.workbuddy/binaries/python/versions/3.13.12/bin/python3 \
  /Users/juno/.workbuddy/skills/seewo-courseware-generator/scripts/validate_enbx.py \
  /workspace/课件名.enbx
```
Expect `✅ 校验通过`. If errors appear, fix the spec or the generator and regenerate.

### Step 5 — Deliver
Hand the `.enbx` to the user. Tell them to double-click it (or drag it into 希沃白板) to
open. Mention that the file is the native 希沃 format and is fully editable in the client.

## Important compatibility notes

- The `.enbx` writer replicates the exact structure of a real 希沃白板 5.1 sample
  (UTF-8 BOM on every XML, `id://` resource references, `Board`↔`Slide` id mapping,
  `Reference.xml`, `SaveInfoMetadataFile.xml`, `thumbnail.png`). The validator confirms
  the generated file passes the *same* checks as that real sample.
- The skill has been verified structurally; it has **not** been opened inside a live
  希沃白板 instance in this environment. If a user reports a version-specific issue,
  the safest fallback is to also export the same content as PPTX (希沃白板 imports PPTX
  natively) — or to open the `.enbx` in the 希沃白板 web/desktop client and re-save.
- Element types supported: text/title, bullets, tables, colored boxes (as pictures), and
  embedded images. Audio/video can be added by the user inside 希沃白板 after opening.

## Reference

For the precise XML schema of each element and the full input spec, read
`references/enbx_format.md`.
