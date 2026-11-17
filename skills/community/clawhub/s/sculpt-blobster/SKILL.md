---
name: sculpt-blobster
description: Design, surgically refine, compile, and QA-verify an OpenClaw Blobster Tier 1 visual pack (24px layered SVG + 512x512 3D vinyl hero PNG + 2x2 #FF00FF chroma-key looping GIFs + automated dark/light QA contact sheet).
---

# Sculpt Blobster (`sculpt-blobster`)

Use this skill to craft, refine, compile, and visually verify the character art for any **OpenClaw Agent Template**—including upgrading a template freshly forged by **`Blobster Smith` (`blobster-smith`)** from its default unpainted **"Proto-Blob (Fresh Out of the Box)"** starter avatar:
- **Required by Upstream OpenClaw & ClawHub**: `avatars/blobster.svg` (`256×256` — the single live avatar rendered inside OpenClaw chat today) + `assets/icon.png` (`256×256` PNG `<= 512 KiB` for ClawHub catalog cards).
- **Optional Fun Extras (for GitHub READMEs, Websites, Showcase Cards & Codex Pets)**: `hero-512.png`, `sprite-2x2.png`, `cutout-256.png`, and hydrated looping `blobster-idle.gif` / `blobster-wave.gif`.

## Prompt Rubric: Fresh Generate vs. Surgical Edit

Never mix initial generation prompts with refinement prompts—save each prompt alongside its working image in your scratch/work folder and follow this split:

### 1. Fresh Generate (`1:1` 3D Hero or `2×2` `#FF00FF` Chroma Sheet)

Write **4–6 crisp sentences** covering:
1. **Character & Silhouette**: Lobster vinyl toy (`BODY` + claws + 1 bold hat/headpiece + 1–2 readable claw props), naming each material texture **once** (matte soft-touch vinyl, brushed brass, stitched leather, woven denim).
2. **Background Contract**:
   - **Hero (`1:1`)**: Clean neutral studio plinth with subtle contact shadow.
   - **Animation Sheet (`1:1`, `2×2` grid)**: `Idle A` (top-left), `Idle B` (top-right), `Wave/Action A` (bottom-left), `Wave/Action B` (bottom-right) on a **100% flat, unlit `#FF00FF` (`RGB 255, 0, 255`) background** with zero floor shadows, zero text labels, and zero divider lines.
3. **Clean Lighting**: Bright, even three-point studio key + rim light—explicitly avoid floating dust motes, chromatic aberration, color fringing, lens bloom, or crushed black shadows.
4. **Full-Body Margin**: Centered full-body framing with at least `8–10%` breathing room around tall hats, antennae, hammers, and brushes so nothing touches cell borders.

### 2. Surgical Edit (Fixing Prop Grips, Apron Text, Paint Split, or Fringe)

When an existing hero or `2×2` sheet is 90% right and needs a targeted fix:
1. **Lead with 1–3 concrete part-level replacements**: State the exact delta first (e.g., `"Replace the unlabeled resin blank in the left claw with a miniature lobster figurine painted glossy cyan (#38BDF8) on the upper half over white primer on the lower half"` or `"Reposition the left claw so its pincer wraps cleanly around the iron tong handles"`).
2. **Add 1 short anchor sentence**: Explicitly name the preserved camera angle, full-body crop, lighting, and untouched props (`"Preserve the three-quarter front camera angle, full-body centering, charred leather apron, and glowing amber hammer in the right claw."`).
3. **Hard Bans**:
   - **Never** write vague `"keep everything else the same"` instructions without naming the anchored pose/crop.
   - **Never** repaste the full 5-sentence generation prompt into an edit call (causes duplicate props, shifted scale, and muddied textures).

### 3. Pre-Render 5-Point Prompt Checklist

- [ ] Zero conflicting pose or lighting instructions.
- [ ] Every material/texture named once (no adjective stacking).
- [ ] Surgical edits contain `<= 3` concrete part deltas + `1` explicit anchor sentence.
- [ ] `2×2` sprite prompts forbid floor shadows, gradients, grid lines, and text on `#FF00FF`.
- [ ] `blobster-design.json` keeps `back: ""`, `< 20` bold vector shapes, and leaves eyes at `(45,32)` & `(75,32)` unobstructed.

## Tier 1: Compile & Run Deterministic Visual QA

`scripts/compile_blobster_pack.py` is bundled directly in this workspace (`svg` uses Python 3 stdlib only; `tier1`, `gifs`, and `qa` require `Pillow>=10.0`).

0. **Runtime Preflight (`check` / `setup`)**:
   ```bash
   # Check: verify Python 3 + Pillow before raster/GIF compilation or QA
   python3 -c "import PIL; print('ok')"
   # Setup (only if missing):
   python3 -m pip install "Pillow>=10.0"
   ```
1. **Author `<avatars-dir>/blobster-design.json`** (`version: 1`, `palette` 6-digit hex colors, 5 allowed SVG fragment layers — e.g. `avatars/blobster-design.json` in a standalone workspace or `templates/<id>/workspace/avatars/blobster-design.json` in a multi-template workshop repo).
2. **Compile the Pack + Emit QA Contact Sheet** (use `--omit-gifs` for Git-tracked template `avatars/` folders so Git tracks single-frame `sprite-2x2.png` + `cutout-256.png`, and keep `--qa-out` in a `work/` or `proof/` path outside any `templates/<id>/` package root so `CLAW.md` maintains zero unlisted files):
   ```bash
   # Required OpenClaw SVG + ClawHub catalog icon.png only (fast path):
   python3 scripts/compile_blobster_pack.py svg \
     --design <avatars-dir>/blobster-design.json \
     --out <avatars-dir>/blobster.svg \
     --icon-out <template-root>/assets/icon.png

   # Or full Tier 1 showcase pack (SVG + ClawHub icon.png + optional 3D vinyl hero & 2x2 sheet):
   python3 scripts/compile_blobster_pack.py tier1 \
     --design <avatars-dir>/blobster-design.json \
     --hero work/hero.png \
     --sheet work/chromakey-2x2.png \
     --out-dir <avatars-dir> \
     --icon-out <template-root>/assets/icon.png \
     --omit-gifs \
     --qa-out work/<id>-qa-contact-sheet.png

   # Hydrate blobster-idle.gif & blobster-wave.gif from sprite-2x2.png into dist/avatars/<id>/:
   python3 scripts/compile_blobster_pack.py gifs --avatars-dir <avatars-dir>
   ```
   Or audit an existing avatar directory (such as the standalone `avatars` folder) without recompiling assets:
   ```bash
   python3 scripts/compile_blobster_pack.py qa \
     --avatars-dir avatars \
     --out work/qa-contact-sheet.png
   ```
3. **Inspect `<id>-qa-contact-sheet.png` Directly (`view_image`)**:
   - Confirm **`24px` chat pill** + `4×` pixel loupe silhouette legibility on both Dark (`#0D1117`) and Light (`#F8FAFC`) panels.
   - Confirm **`0` border-clipped pixels** across `cutout-256.png` and all GIF frames.
   - Confirm **`<= 1.5%` `#FF00FF` residual fringe spill**, synchronized `blobster-design.json` <-> `blobster.svg`, and `< 1 MiB` per template managed file (`< 2 MiB` per hydrated GIF).

## Tier 2: Downstream Extended Pet Rig Specification (Roadmap — Not in `compile_blobster_pack.py` v1)

When a locked Tier 1 character is later promoted to **Codex Pets** or an external desktop/sidebar interactive pet host (`sprite_version: 2`), design 3 reference sheets (hero, 4-angle turnaround, 6-state expression grid) plus 6 `2×2` `#FF00FF` pose sheets targeting the external `1536×2288` (`8×11` × `192×208`, `73`-frame) atlas pipeline (`compile_blobster_pack.py` v1 implements `svg`, `tier1`, `gifs`, and `qa` only).
