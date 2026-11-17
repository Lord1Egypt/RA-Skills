---
name: tesla-wrap-workflow
description: Create, modify, or repair Tesla in-car custom wrap PNGs (UV unwrapped textures) — handling vehicle template selection, on-car orientation, mirrored numerals, logo removal, graphic cropping, incomplete images, the 1 MB per-image limit, and batch ZIP delivery. Use when the user asks for Tesla custom wraps, Model Y wraps, or editing an existing wrap; not for physical vinyl production cutter templates or for generating car render photos only.
---

# Tesla In-Car Wrap Workflow

Turn the user's theme into an inspectable in-car UV texture. Treat "looks good", "file is valid", "template matches", and "correct orientation on the car" as four separate goals — do not substitute render photos for actual verification.

## 1. Fixed Inputs and Acceptance Criteria

- Extract from context: vehicle model, year, exact variant, theme, quantity, logo policy, and per-file size limit. The latest explicit instruction overrides earlier ones; e.g. "remove all Tesla logos" overrides an earlier "keep the logos", but that does not mean removing themed badges.
- Consult the current instructions in the official repository https://github.com/teslamotors/custom-wraps and obtain the original template for the matching model and variant. Do not assume Premium, Standard, Performance, or long-range variants share a template based on year alone.
- If inputs are insufficient, complete the theme design first; ask only when a key vehicle detail or the original template is missing. Screenshots can illustrate defects but cannot serve as precise cutter templates. When a readable source file already exists, do not ask the user to re-upload it.
- By default interpret "1 MB" as no more than 1,000,000 bytes per PNG; if the user demands strictly "less than 1 MB", set the validation limit to 999999. Report the total ZIP size separately. Do not treat old software versions, dimension ranges, or upload counts as permanent rules.
- Record current constraints in a batch manifest listing file name, theme, template source, dimensions, logo requirements, and orientation status to be verified. Never write personal chat screenshots, account information, or private file paths into publicly released material.

## 2. Establish Panel and Orientation Mapping First

- Read the original template; identify UV islands for front, rear, both sides, mirrors, and blank areas. A large black central area may be an empty void — do not fill it in as a roof. Preserve small islands such as pillars and mirror shells.
- For orientation-sensitive graphics record: UV island, vehicle forward direction, up direction, rotation, whether mirrored, evidence source, and verification status.
- Determine orientation from official examples, UV correspondences from trusted models, or user in-car testing. Left and right sides may need different rotations, but do not codify unverified rules such as "left 90°, right -90°" or "hood is always 180°".
- Digits and text must not be mirrored along with the overall graphic; handle rotation and mirroring separately. Fossil heads, dinosaur heads, and badges must be confirmed in on-car viewing orientation — a motif that looks upright in a flat preview does not meet acceptance.
- Without a reliable mapping, use non-directional textures first, or deliver direction-test versions clearly labeled as unverified. Do not claim verified on-car results.

## 3. Generation and Localized Editing

Use available image generation tools to create or edit; follow each tool's requirements for reference images, transparency, and editing methods. Prompt examples are in [references/prompt-patterns.md](references/prompt-patterns.md).

- Use the original template as the structural reference; place themed designs inside UV islands. Preserve canvas aspect ratio, island positions, gaps, blank areas, and transparency; do not produce car photos, phone UI screenshots, or collages in place of texture files.
- Prompts cannot guarantee pixel-level template locking. Always check boundaries after generation; when precise mask compositing is needed, use deterministic processing per the tool and with user authorization — do not call approximate AI outlines an exact match to the official template.
- Place heads, roundels, and text inside panel safe zones, away from wheel arches and cut edges. Plan cross-seam patterns only after UV continuity is confirmed.
- Localized repairs change only the specified part; e.g. remove the Tesla T emblem and wordmark while keeping the dinosaur badge, colors, and lines. After editing, check that no other region was accidentally altered.
- Batch output: save file by file per the manifest; do not pack multiple designs into one collage as a deliverable. Keep original source images fully intact.

## 4. Export and Validation

Detailed failure modes are in [references/pitfalls.md](references/pitfalls.md).

1. Export PNGs from the complete source image at the current official dimensions. Optimize losslessly first; reduce palette colors only if necessary; check gradient banding and detail loss. Renaming a JPEG to PNG is forbidden.
2. Write to a temporary file, fully encode, then atomically replace the target; keep file names uniquely versioned to avoid concurrent overwrites. Do not enable "allow truncated image loading" to mask corruption.
3. Run on final deliverables:
   ```bash
   python scripts/validate_wrap.py output.png --width 1024 --height 1024 --max-bytes 1000000
   python scripts/validate_wrap.py batch.zip --width 1024 --height 1024 --max-bytes 1000000
   ```
   Replace width and height with the actual acceptance dimensions. Requires Python 3 and Pillow. The script is read-only — it never modifies images; it checks PNG signature, chunk CRCs, IEND, full decode, dimensions, byte size, and every PNG inside ZIP archives, and outputs SHA256. It does not validate vehicle model, template boundaries, or graphic orientation.
4. Separately perform visual/mask checks on template boundaries, blank areas, cropping, and logos. A valid PNG may still have an empty lower half, unwanted transparency, or missing content; compare visible content against the complete source image — full decode does not mean a complete picture. Record the method used; never treat file validation as UV validation.
5. After packaging, reopen the ZIP and verify the final bytes inside. After upload/save, if read-back is possible, compare SHA256 and decode results again; if read-back is not possible, state that this stage is unverified. Do not claim to have located the root cause of truncation.

## 5. Delivery and Iteration

- Deliver individual images plus a ZIP if the user needs one, saved and linked per the tool's delivery rules.
- Summarize: number of designs, per-image size, and the three-layer status: file format, template geometry, real in-car mapping. Claim only checks actually performed; if no in-car testing was done, say so explicitly.
- On "the second image is flipped / incomplete", locate the specific file and panel, check the final bytes, then fix the actual cause; do not blindly redo everything. But batch requirements such as "remove all logos" must cover the whole batch — keep localized defect fixes separate from full-batch changes.
- When the user asks to publish the workflow publicly, release only generic instructions, original code, and example prompts; cite official template sources, and do not bundle unauthorized assets or personal records.
