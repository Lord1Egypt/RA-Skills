---
name: seamproof
description: Make a texture or a whole PBR texture set tile seamlessly, with a measured seam score. Use when asked to make a texture seamless or tileable, fix visible seams or a repeating grid on a game texture, or process PBR maps (albedo/basecolor, normal, roughness, height, metallic/AO) so the whole set stays in register — for example "make this texture tile", "fix the seams on these maps", "why does my texture show a grid when tiled", or "score how seamless this texture is". Not for finding 9-slice borders in UI panels (that is patchproof) or recovering the grid of damaged pixel art (that is snapgrid).
license: MIT
compatibility: Requires Python 3.10+; pip installs numpy and Pillow. CPU only, no network or ML at run time; network is needed only to install.
---

# seamproof

## What this tool does

seamproof makes a single texture — or a whole PBR map set — tile seamlessly. It applies one shared geometric fix (roll, mirror cross-fade, roll back, plus a vignette/gradient detrend for colour maps only) to every map in a set, so the set stays in register, and reports a measured seam score per map before and after. It does not fake a pass: a texture whose content cannot be hidden gets a poor verdict and a band-repaint warning instead.

## Install

```bash
pip install git+https://github.com/RakTikoo/seamproof
```

This provides the `seamproof` command.

## Run

Fix a folder of textures (sets are detected automatically), writing results to another folder:

```bash
seamproof fix textures/ --out fixed/
```

Measure one texture without writing anything:

```bash
seamproof fix textures/ground_albedo.png --score-only
```

Files that share a base name and differ only by a map suffix (`_albedo`, `_normal`, `_roughness`, `_height`, `_metallic`, and similar) form one set; a file with no known suffix is a standalone colour image. All maps in a set must be the same size. Useful flags: `--no-detrend` skips the gradient removal on colour maps; `--band N` sets the blend band width in pixels (default: 1/8 of the smaller side).

## Reading the results

Each map gets one line: its name, the seam score before -> after, a 3x3 tiled re-score (the fixed texture actually tiled and re-measured), and a verdict. Scores are in 0–255 intensity units: ≤ 2 is *good* (seam not visible in practice), ≤ 8 is *fair* (faint on close inspection), above 8 is *poor*. If the blend repainted the seam band heavily (band repaint above 25), the line says so and the verdict is downgraded to *poor* — a low score with a high band repaint is not a clean pass.

Exit codes: `0` means the run completed — it does not mean every texture scored *good*, so read the per-map verdicts. `2` means the run stopped with a clean error (the message on stderr says why, for example maps in a set with different sizes, or an unsupported image); do not treat any partial output as a finished set. Images smaller than 8x8 are reported and copied unchanged — there is no room to blend them.

## Limits

- Seamless is not repetition-free: seamproof removes the seam and the vignette grid, but a texture with one memorable feature will still show a repeating pattern when tiled.
- Strong, unique content crossing an edge (a face, a trunk, a logo) cannot be hidden by the blend; expect a mediocre score and a high band repaint, not a clean fix.
- The mirror cross-fade can leave faint symmetric "ghost" shapes inside the blend band on busy textures; the band repaint number is the warning light.
- Detrend flattens all low frequency in a colour map, including deliberate broad shading. Use `--no-detrend` to keep an intentional gradient (the seam score will show what that costs).
- Formats: 8-bit PNG/JPEG/TGA/BMP/WebP/TIFF and 16-bit grayscale PNG without transparency (an unlabelled 16-bit grayscale image is treated as a data map and skips detrend). Other high-bit-depth images produce an error. Alpha channels pass through unchanged — alpha seams are not fixed. Normal maps are assumed tangent-space OpenGL (Y+); a DirectX (Y−) map's green channel is not flipped for you.
