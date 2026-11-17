# Loft, sweep and text

Read this before using `loft`, `sweep` or `text`. `{baseDir}` and the request format are described in SKILL.md.

## Loft and sweep

Use these for organic and curved parts instead of approximating them with booleans of primitives.

```json
{"op": "loft", "name": "Shell", "sections": [
  {"shape": {"rect": [-20, -15, 20, 15], "corner_radius": 4}, "plane": "XY", "offset": 0},
  {"shape": {"circle": [0, 0], "radius": 12}, "plane": "XY", "offset": 30},
  {"shape": {"circle": [0, 0], "radius": 6}, "plane": "XY", "offset": 50}]}
```

- **Loft:**
  - Each section is one closed shape (no holes) in a plane at an `offset`, drawn like an extrude profile.
  - A smooth loft bulges between very different sections; add intermediate sections, or set `ruled: true`.
  - Edit with `set` and `{"sections": [...]}`, keeping the same number of sections.

```json
{"op": "sweep", "name": "Handle", "shapes": [{"circle": [0, 0], "radius": 6}, {"circle": [0, 0], "radius": 4}],
 "path": [[0, 0, 0], [0, 0, 40], [60, 0, 40], [60, 0, 0]], "corner_radius": 12}
```

- **Sweep:**
  - The path is `[x, y, z]` points: straight segments by default, `corner_radius` for bent-tube corners, or
    `smooth: true` for a curve through the points. Alternatively, a `helix`
    (`{"radius", "pitch", "height", "left_handed", "center", "axis"}`).
  - The profile is drawn in 2D around the start of the path. (0, 0) sits on the path, y points `up`
    (default +Z), and x points to the right when looking along the path (outward on a helix). The response
    reports this `profile_frame`.
  - A profile may have holes (a tube).
  - Spring: a circle swept along a helix. Thread: a triangle such as
    `{"polygon": [[-0.1, -1], [1.5, 0], [-0.1, 1]]}` swept along a helix at the core radius, in a body with
    `mode` add (external) or remove (internal).
  - Edit with `set`: `path`, `corner_radius`, `helix`, `up` or `shapes`.
- Both work in a PartDesign body (`body`, `mode`); coordinates are then body coordinates.

## Text

```json
{"op": "text", "name": "Label", "text": "V2.1", "size": 8, "height": 2, "position": [40, 25, 9], "align": "center"},
{"op": "cut", "name": "Engraved", "base": "Plate", "tool": "Label"}
```

- `size` is the height of capital letters; `height` is the depth of the letters. `position` is where the
  `align` point goes (`bottom_left` default, `center`, `top_right`, ...; bottom is the baseline).
- The text lies in `plane` and is extruded along its normal, like `extrude`: XY reads from above and goes
  +Z; XZ reads from the front and goes +Y (into a front face); YZ reads from the right and goes +X (out of a
  right face). `angle` turns it in its plane; `reversed` flips the extrusion.
- **Engrave:** start below the face and pass through it, then `cut`. The example engraves 1 mm into a 10 mm
  plate: z from 9 to 11. **Emboss:** start just inside the face (z = 9.9 for a top face at 10) and `fuse`.
- The default font is FreeCAD's bundled osifont; `font` takes a `.ttf`/`.otf` file in the workspace.
- Edit with `set`: `text`, `size`, `font`, `align`, `height`.
