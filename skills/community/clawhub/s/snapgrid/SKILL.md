---
name: snapgrid
description: Recover the pixel grid from damaged "fake pixel art" — sprites upscaled with smoothing, AI-generated, or blur/JPEG-damaged — and snap them back to pixel art. Use when asked to fix smoothed or blurry pixel art, recover a sprite's original resolution and palette, or clean up a sprite sheet or animation frames — for example "this pixel art was upscaled with smoothing, snap it back", "recover the original grid of this sprite", or "fix these animation frames so they share one grid and palette". Not for making textures tile seamlessly (that is seamproof) or finding 9-slice borders in UI panels (that is patchproof). A sheet or folder of frames is processed jointly, with one shared grid and one shared palette.
license: MIT
compatibility: Requires Python 3.10+; pip installs Pillow and NumPy. CPU only, classical algorithms, no ML; network is needed only to install.
---

# snapgrid

## What this tool does

snapgrid recovers the original pixel grid of a damaged pixel-art image — one upscaled with smoothing instead of nearest-neighbour, AI-generated, or blur/JPEG-damaged — and rewrites it as clean pixel art on that grid, with a recovered palette. A sprite sheet or a folder of animation frames is estimated jointly, so every frame lands on one shared grid with one shared palette and frames cannot flicker or drift. If no clean grid can be proven, snapgrid abstains and writes nothing: a wrong grid is treated as worse than no answer.

## Install

```bash
pip install git+https://github.com/RakTikoo/snapgrid
```

This provides the `snapgrid` command.

## Run

Snap a single image:

```bash
snapgrid fix damaged.png --out fixed.png
```

Snap a sheet (frames in a grid) or a folder of frames, jointly:

```bash
snapgrid sheet sheet.png --rows 2 --cols 4 --out fixed_frames/
snapgrid sheet frames_folder/ --out fixed_frames/
```

`--max-colors N` caps the palette (default 256) on both subcommands. Every successful run also writes the shared palette next to the output as `.palette.gpl` (GIMP palette) and `.palette.json` sidecars.

## Reading the results

A successful run prints the input size, the recovered grid (for example `recovered grid: 24x24 (cell ~4.29x4.29px, offset 0,0)`), a confidence value with its resynthesis fit error, the palette size, and the file written. Judge a result by the grid and confidence, not by the exit code alone. The exit code is the verdict:

- `0` — a grid was recovered and the snapped image(s) and palette sidecars were written.
- `3` — **abstained**: no clean grid found, nothing written, and the message says why (for example the image looks like a smooth gradient or photo, or it may already be clean native pixel art). The reason is printed to **stderr**, not stdout — stdout is empty on an abstention, so an agent must read stderr; stdout alone shows only the bare exit code. Treat exit 3 as "this tool cannot honestly answer", not as a failure to retry.
- `2` — bad input: a clean one-line error (missing file, not an image, unusable arguments), nothing written.

## Limits

- Grid recovery is much improved, not solved. Very sparse sprites — a few flat shapes in few colours on a large flat background — can still be explained almost as well by a coarser grid; wrong grids are rare on the published suites (0/36 harsh, 1/56 gentle, 1/92 held-out) but not impossible.
- Square cells are assumed: the damage must be a uniform upscale, the same factor on both axes. Non-uniformly resized images are detected and abstained on in every measured benchmark, but that is not a guarantee — on deliberately adversarial probes (mild stretch ratios around 1.25–1.9x between axes, hard high-detail sprites) a wrong grid can still slip through.
- Very small damaged images (short side 24 px or less) are emitted only when both axes' own evidence positively confirms the grid; otherwise they are refused. Recovering the refused tiny sprites was investigated and measured to be impossible on the evidence in the image.
- Some large sprites with very sparse edges may abstain through the edge-density gate even though they are in scope — a safe failure, but a recovery the tool could in principle make.
- Exact colours under smooth (blur/noise) damage are rare: expect the right grid and colours within a few levels, and nudge the palette by hand if the values must be perfect.
- One uniform grid per image or sheet. A partial-cell crop offset is handled; two different grids composited into one image are not, and a sheet or folder whose frames genuinely use different grids abstains with an explanation.
- Cells smaller than about 1.8 px in the damaged image (very light upscales, or huge sprites) are out of scope. Semi-transparent alpha is preserved approximately; fully transparent cells stay transparent and binary alpha stays binary. Runs take from ~0.1 s on small sprites to a few seconds on large ones.
