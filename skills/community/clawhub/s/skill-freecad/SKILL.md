---
name: freecad-skill
description: "Create, edit, verify and export parametric FreeCAD models (STEP, STL, 3MF) and DXF drawings from JSON; STL import; mass and stress checks; parts from GitHub."
version: 3.0.1
homepage: https://clawhub.ai/ninja7v/skills/freecad-skill
metadata: {"openclaw":{"emoji":"📐","homepage":"https://clawhub.ai/ninja7v/skills/freecad-skill","requires":{"anyBins":["python3","python"]},"envVars":[{"name":"FCSKILL_FREECAD","required":false,"description":"Path or command of FreeCAD's command-line executable (freecadcmd) if auto-detection fails, e.g. '/path/FreeCAD.AppImage freecadcmd'."},{"name":"FCSKILL_WORKSPACE","required":false,"description":"Root folder for documents and exports. Default: the current directory. Paths outside it are refused."},{"name":"FCSKILL_LIBRARY","required":false,"description":"Path to a local clone of the FreeCAD parts library; library parts are then copied from it instead of downloaded."},{"name":"FCSKILL_OFFLINE","required":false,"description":"Set to 1 to forbid all network access. Otherwise the only network use is the optional parts library: anonymous GET requests to api.github.com and raw.githubusercontent.com for FreeCAD/FreeCAD-library, made only by the library command and by import steps that name a library part."}]}}
---

# FreeCAD skill

Build parametric CAD models with FreeCAD by sending a JSON request to one command. Every operation creates a
native FreeCAD feature (`Part::Box`, `Part::Cut`, `Part::Fillet`, ...), so the model stays editable: change a
dimension later and everything downstream updates. After every step the response reports volumes and bounding
boxes, and failures name the step, the cause and a fix.

`{baseDir}` below means the directory that contains this SKILL.md.

## Run

Write the request to a file and run:

```bash
python3 {baseDir}/scripts/fcskill.py run request.json
```

On Windows, use `python` instead of `python3`. The launcher needs Python 3.12 or newer; if it reports
`PYTHON_VERSION`, run it with a newer interpreter (e.g. `python3.12`).

The request can also be inline JSON or come from stdin (`run -`). Use a file for anything non-trivial, because
it avoids shell-quoting problems. The working directory is the workspace. Documents and exports are relative
to it and cannot leave it.

Other commands:
- `python3 {baseDir}/scripts/fcskill.py library <keywords>`: search ready-made parts (see below).
- `python3 {baseDir}/scripts/fcskill.py describe`: list every op with its parameters (`*` = required).
- `python3 {baseDir}/scripts/fcskill.py describe fillet shell`: full parameter details for those ops.
- `python3 {baseDir}/scripts/fcskill.py doctor`: check the FreeCAD installation.

If `doctor` says FreeCAD is missing, ask the user to install FreeCAD 1.1+ or to set `FCSKILL_FREECAD` to its
`freecadcmd` executable. Do not try to model without it.

## Request

```json
{
  "doc": "bracket.FCStd",
  "steps": [
    {"op": "box", "name": "Plate", "length": 80, "width": 50, "height": 6},
    {"op": "cylinder", "name": "Hole", "radius": 3.25, "height": 8, "position": [10, 10, -1]},
    {"op": "cut", "name": "Drilled", "base": "Plate", "tool": "Hole"},
    {"op": "fillet", "name": "Bracket", "target": "Drilled", "radius": 5, "edges": "|Z and %LINE",
     "expect": {"bbox_size": [80, 50, 6], "solids": 1}},
    {"op": "export", "filename": "bracket.step"}
  ]
}
```

- `doc`: the `.FCStd` file (default `model.FCStd`). It is created if missing and re-opened on later requests.
- `new: true`: start from an empty document, replacing the file's content.
- `dry_run: true`: run and report without saving or exporting.
- `brief: true`: leave volume and bounding box out of the per-step entries. Use it for long requests;
  `results`, `warnings` and errors are reported as usual.
- **All or nothing:** if any step fails, nothing is saved or exported and the file on disk is unchanged.
  Fix the reported step and resend the whole request.
- Before anything runs, the whole request is validated. Unknown ops or parameters, typos and missing
  values are all reported at once.

## Response

Actual output for the request above (abridged):

```json
{"status": "success", "doc": "bracket.FCStd", "saved": true,
 "steps": [{"index": 0, "op": "box", "object": "Plate", "volume": 24000.0,
            "bbox": {"min": [0,0,0], "max": [80,50,6], "size": [80,50,6]}, "solids": 1},
           {"index": 2, "op": "cut", "object": "Drilled", "volume": 23800.902, "...": "..."},
           {"index": 3, "op": "fillet", "object": "Bracket", "volume": 23672.14, "...": "..."},
           {"index": 4, "op": "export", "data": {"file": "bracket.step"}}],
 "results": [{"name": "Bracket", "type": "Part::Fillet", "role": "result", "inputs": ["Drilled"],
              "volume": 23672.14, "bbox": {"min": [0,0,0], "max": [80,50,6], "size": [80,50,6]}, "solids": 1, "valid": true}],
 "intermediates": ["Plate", "Hole", "Drilled"],
 "exports": [{"file": "bracket.step", "format": "step", "objects": ["Bracket"], "bytes": 13775,
              "verified": {"faces": 11, "bbox_size": [80,50,6], "solids": 1, "volume": 23672.14}}],
 "files_written": ["bracket.FCStd", "bracket.step"]}
```

When something is wrong, `warnings` appears, e.g.
`{"step": 2, "code": "NO_EFFECT", "message": "cut removed no material from 'Plate'; ['Hole'] do not overlap it. ..."}`.

- `results` are the finished parts: objects that no other feature consumes. Exports default to these.
- **Read `warnings`.** For example, `NO_EFFECT` means a cut missed the part, and `DISJOINT` means a fusion
  produced separate pieces. These are geometry mistakes even though the status is success.
- `OVERLAPPING_RESULTS` means two finished parts occupy the same space. Usually one is a leftover helper (a
  cutter you never used, which then hides the part in renders), or two parts that should touch are sized wrong.
  Every result is rendered and exported, so delete leftovers before trusting a render.
- `SELF_INTERSECTION` means a result passes through itself (e.g. a spring whose wire is thicker than its
  pitch). Its volume and mass are wrong and other CAD systems may reject it: fix it, don't deliver it.
- `SELF_INTERSECTION_UNCHECKED` means that check could not give an answer for a result (the message says
  why: too many faces, invalid geometry, or the checker failed). The result is then **unconfirmed, not
  clean**: tell the user, or simplify or repair the part and run again.
- `DEEP_CHAIN` means many booleans are stacked one on another, which gets slow. See Workflow, step 3.
- On failure, `error` has `code`, `message`, `hint`, `step`, `op` and often `details` (available names,
  measured values). Exit code is 0 on success, 1 when the request failed, 2 when FreeCAD is missing or crashed.

## Conventions

- Units are **mm** and **degrees**, and the axes are right-handed X/Y/Z with +Z up.
- `box`: `position` is the **minimum corner**; the box extends along +X/+Y/+Z. To centre a 40×20 box on
  (0, 0), use `position: [-20, -10, z]`.
- `cylinder`, `cone`, `prism`: `position` is the **centre of the bottom face**; the axis is +Z unless you
  give `direction` (e.g. `[1, 0, 0]`). `sphere`, `torus`: `position` is the centre.
- `extrude`, `revolve`: the profile lies in `plane` (`XY` default, `XZ`, `YZ`), with 2D coordinates.
  Extrusion goes along the plane normal: XY→+Z, XZ→+Y, YZ→+X. See [Profiles](#profiles).
- Names are identifiers (`Base_plate`, not `base plate`) and must be unique. Name every object you will
  refer to later.
- Make cutting tools **pass through** the faces they cut: a hole in a 6 mm plate should run from z = -1
  to z = 7. Exactly coincident faces make booleans fail or leave skins.

## Operations

| Op | Purpose | Key parameters (`*` required) |
|---|---|---|
| `box` | Box | `length*` `width*` `height*` `position` `rotation` |
| `cylinder` | Cylinder | `radius*` `height*` `position` `direction` |
| `sphere` | Sphere | `radius*` `position` |
| `cone` | Cone / frustum | `radius1*` (bottom) `radius2*` (top) `height*` `position` `direction` |
| `torus` | Torus | `radius1*` (ring) `radius2*` (tube) `position` `direction` |
| `prism` | Regular polygon prism | `sides*` `circumradius*` `height*` `position` `direction` |
| `extrude` | Profile → solid (pad/pocket in a body) | `shapes` or `points`, `height` or `direction`, `plane` `offset` `symmetric`; in a body: `body` `mode` `through_all` `reversed` |
| `revolve` | Profile → solid of revolution (revolution/groove in a body) | `shapes` or `points`, `plane` `axis` `center` `angle`; in a body: `body` `mode` |
| `loft` | Smooth solid through cross-sections (organic shells, bottles, square-to-round) | `sections*` `ruled` `closed`; in a body: `body` `mode` |
| `sweep` | Profile along a path or helix (tubes, handles, springs, threads) | `shapes*`, `path` (+`smooth`, `corner_radius`) or `helix`, `up`; in a body: `body` `mode` |
| `text` | Lettering as a solid, to engrave (cut) or emboss (fuse) | `text*` `size*` `height*` `position` `plane` `align` `angle` `reversed` `font` |
| `body` | PartDesign body: one solid built feature by feature | `name` `position` `rotation` |
| `assembly` | Assembly of parts (links to solids/bodies); first part grounded; returns a bill of materials (`bom`) | `parts*` (`object`, `name`, `position`, `ground`) |
| `joint` | Connect two assembly parts and solve: fixed, revolute, cylindrical, slider, ball, parallel, perpendicular | `assembly*` `type*` `a*` `b*` (`{"part", "face"/"edge"}`) `offset` |
| `hole` | Drilled holes in a body: simple, counterbore, countersink, threaded | `body*` `at*` `offset` `size` (`M2`…`M20`) or `diameter`, `fit` `threaded` `type` `depth` |
| `cut` | Subtract | `base*` `tool` or `tools` |
| `fuse` | Union | `objects*` (≥2) |
| `common` | Intersection | `objects*` (≥2) |
| `fillet` | Round edges | `target*` `radius*` `edges` (selector, default all) |
| `chamfer` | Bevel edges | `target*` `size*` `edges` |
| `shell` | Hollow out, open faces | `target*` `thickness*` `open_faces*` (selector) `outward` |
| `linear_array` | Repeat along a vector | `target*` `count*` `step*` (offset between copies) |
| `grid_array` | Repeat on a grid | `target*` `count_x*` `count_y*` `step_x*` `step_y*` |
| `polar_array` | Repeat around an axis | `target*` `count*` `angle` `axis` `center` |
| `move` | Translate | `target*` `offset*` |
| `rotate` | Rotate about an axis through a point | `target*` `angle*` `axis` `center` |
| `place` | Absolute position/rotation | `target*` `position` `rotation` |
| `mirror` | Mirrored copy (of a solid, or of a feature inside its body) | `target*` `plane` (`XY`/`XZ`/`YZ`) or `normal`, `point` |
| `copy` | Linked copy that follows the original | `target*` `offset` |
| `scale` | Scaled version (about origin) | `target*` `factor*` (number or `[sx, sy, sz]`) |
| `set` | Change properties, recompute downstream | `target*` `properties*` |
| `set_params` | Named parameters (`Params` spreadsheet) | `values*` |
| `delete` | Delete objects | `targets` or `all`, `with_dependents` |
| `rename` | Change label | `target*` `label*` |
| `inspect` | Document tree, or one object in detail | `target` `topology` |
| `check` | Assert geometry | `target*` `expect*` |
| `measure` | Clearance, interference, closest points; mass, centre of mass, inertia | `objects` `require` (`min_clearance`, `no_interference`) `material` `density` |
| `import` | Solid from a STEP/IGES/BREP/FCStd file or a closed STL/OBJ/3MF mesh, or a ready-made part from the FreeCAD library | `library` or `file`, `anchor` `position` `rotation` `refine` `name` |
| `material` | Material and/or colour of finished parts (FreeCAD material, GUI colour, renders, masses) | `targets*` `material` `color` `transparency` |
| `fem_static` | Stress analysis: displacement, von Mises stress, safety factor | `target*` `fixed*` `loads*` `material` `require` `report` `mesh_size` |
| `export` | STEP/IGES/BREP/STL/OBJ/3MF, or a flat DXF/SVG outline (laser/CNC), verified | `filename*` `targets` `tolerance` `view` |
| `drawing` | Technical drawing (DXF): views, verified dimensions, hole table, title | `filename*` `sheet` `projection` `scale` `dimensions` `title` `author` `preview` |
| `render` | Shaded PNG views for a visual check | `filename*` `views` (default iso, front, top, right) `size` |

`rotation` is `{"axis": [x, y, z], "angle": deg}`. Full details are in `describe <op>` or
[docs/OPERATIONS.md](docs/OPERATIONS.md). Complete, tested requests to start from are in `{baseDir}/examples/`:
`pd_bracket.json` (PartDesign body, counterbored holes, fillet), `mounting_plate.json`, `gasket.json` (sketch
profile with holes), `enclosure.json`, `flanged_bushing.json`, `l_bracket.json`, `wheel.json` and `table.json`.

### Profiles

`shapes` builds a real, editable FreeCAD sketch from closed shapes. Shapes inside another shape become holes:

```json
{"op": "extrude", "name": "Gasket", "height": 2, "shapes": [
  {"rect": [0, 0, 90, 60], "corner_radius": 8},
  {"slot": [[30, 30], [60, 30]], "radius": 9},
  {"circle": [10, 10], "radius": 3.5},
  {"polygon": [[40, 5], [50, 5], [45, 12]], "corner_radius": 1},
  {"path": [[70, 40], [80, 40], {"arc_to": [80, 50], "center": [80, 45]}, [70, 50]]}
]}
```

- `rect`: `[x_min, y_min, x_max, y_max]`, optional `corner_radius`.
- `circle`: centre plus `radius`.
- `slot`: the centres of its two rounded ends plus `radius`.
- `polygon`: corners plus optional `corner_radius`, or `radii` with one radius per corner.
- `spline`: a smooth closed curve through 3 or more points, e.g. `{"spline": [[58, 0], [40, 22], [0, 30], [-45, 24], [-58, 0], [-45, -24], [0, -30], [40, -22]]}`.
- `path`: a start point, then `[x, y]` (a line to that point),
  `{"arc_to": [x, y], "center": [cx, cy], "clockwise": false}`, or
  `{"spline_to": [x, y], "through": [[x, y], ...], "start_tangent": [dx, dy], "end_tangent": [dx, dy]}`
  (a smooth curve; tangents are optional). The path closes back to its start automatically.

Splines pass exactly through their points but can bulge between them. Use more points where the curve must be
controlled, and a `path` with straight segments for flat sides, e.g. a flat-bottomed dome:
`{"path": [[-30, 0], [30, 0], {"spline_to": [-30, 0], "through": [[20, 25], [0, 32], [-20, 25]], "start_tangent": [0, 1], "end_tangent": [0, -1]}]}`.

Shapes must be separate or fully nested; partial overlaps are rejected. `offset` moves the profile plane
along its normal. To change the outline later, use `set` with `{"shapes": [...]}`. `points` is a shortcut for
a plain polygon.

**Parametric profiles.** The numbers of `rect`, `circle` and `slot` (coordinates, `radius`,
`corner_radius`) can be expressions, so the outline follows the parameters:

```json
{"op": "set_params", "values": {"width": 90, "depth": 50, "bore": 12}},
{"op": "extrude", "name": "Plate", "height": 6, "shapes": [
  {"rect": [0, 0, "=Params.width", "=Params.depth"], "corner_radius": 5},
  {"circle": ["=Params.width / 2", "=Params.depth / 2"], "radius": "=Params.bore / 2"}]}
```

Changing `width` with `set_params` then resizes the plate and keeps the bore centred. These three shapes
are stored as fully dimensioned sketches (one named dimension per number), so they also stay put when a
person opens the sketch in FreeCAD. `polygon`, `spline` and `path` take numbers only; so do sweep profiles
and loft sections.

### More operations (read the guide first)

These need more than the table above. Read the guide before the first use in a session:

- `loft`, `sweep` (springs, tubes, threads) and `text` (engraving, embossing): [docs/SHAPES.md](docs/SHAPES.md).
- `import` of STEP/IGES/BREP/FCStd files and closed meshes, and ready-made parts from the FreeCAD library
  (`library` command): [docs/PARTS.md](docs/PARTS.md). The library is the skill's only network use: anonymous
  downloads from github.com/FreeCAD/FreeCAD-library, off with `FCSKILL_OFFLINE=1`. Library parts are CC-BY 3.0:
  pass the reported `attribution` on to the user.
- `assembly` and `joint`: [docs/ASSEMBLIES.md](docs/ASSEMBLIES.md).
- `fem_static` (stress analysis): [docs/ANALYSIS.md](docs/ANALYSIS.md).

### PartDesign bodies

A body is one solid built feature by feature: the way FreeCAD users model mechanical parts, and the most
editable kind of model. Prefer a body for a single part, and stand-alone solids plus booleans for quick
shapes or multi-part layouts.

```json
{"op": "body", "name": "Bracket"},
{"op": "extrude", "body": "Bracket", "name": "Base", "height": 8, "shapes": [{"rect": [0, 0, 90, 50], "corner_radius": 6}]},
{"op": "extrude", "body": "Bracket", "name": "Boss", "height": 12, "offset": "=Base.Length", "shapes": [{"circle": [45, 25], "radius": 12}]},
{"op": "extrude", "body": "Bracket", "mode": "remove", "through_all": true, "offset": "=Base.Length + Boss.Length", "shapes": [{"circle": [45, 25], "radius": 6}]},
{"op": "hole", "body": "Bracket", "at": [[10, 10], [80, 10]], "offset": "=Base.Length", "size": "M5", "type": "counterbore"},
{"op": "fillet", "target": "Bracket", "radius": 2, "edges": "%CIRCLE and r=12 and not >Z"}
```

- **Placing features:**
  - Profiles always use body coordinates. `offset` places the profile plane, e.g. on top of `Base`.
  - Use an expression (`"=Base.Length"`) so the feature follows when dimensions change.
- **Directions:**
  - `mode: "add"` (pad) goes along the plane normal: XY→+Z, XZ→+Y, YZ→+X.
  - `mode: "remove"` (pocket) and `hole` go against it, so they cut down into a part from a profile on its top face.
  - For the bottom, back or left faces, use `reversed: true`.
  - A feature that misses the part gets a `NO_EFFECT` warning, and a hole that starts in air gets `HOLE_OUTSIDE`.
- **The first feature must add material.** A body stays one solid, so added material must touch the existing part.
- **Dress-ups and patterns:**
  - `fillet`, `chamfer` and `shell` take the **body** as `target` and are added at the end of its feature tree.
  - `linear_array`, `grid_array`, `polar_array` and `mirror` take a **feature** of the body (e.g. a pocket,
    hole or pad) as `target` and repeat it inside the body. A pattern or mirror can't be repeated again:
    name the original feature (one `grid_array` gives a grid).
- **Holes:**
  - `size` uses ISO tables: `fit: "clearance"` (default) for a screw to pass, `"tap"` for a tap drill.
  - `threaded: true` (with `size`, type `simple`) models a real ISO metric thread over the hole depth. Give
    `depth` for a blind hole. Prefer a plain hole for small printed threads (below about M5).
  - Counterbores fit ISO 4762 socket heads; countersinks fit ISO 10642 (90°).
- **Editing:**
  - Use `set` on a feature for native properties (`Length`, `Diameter`, ...), or for `shapes`, `offset` and `at` (holes).
  - Fillet and chamfer selectors are re-evaluated after every edit.
  - Move the whole part by moving the body; features have no placement of their own.
- **Combining with other solids:** a body can be used like any solid in `cut`, `fuse`, `mirror`, `copy` and `export`.

### Edge and face selectors

`edges` (fillet/chamfer) and `open_faces` (shell) accept `"all"`, 1-based indices `[1, 3]`, or an expression:

| Selector | Meaning |
|---|---|
| `>Z` / `<Z` | elements whose centre is highest / lowest in Z (same for X, Y) |
| `\|Z` | straight edges parallel to Z; planar faces whose normal is parallel to Z |
| `#Z` | straight edges / face normals perpendicular to Z |
| `+Z` / `-Z` | planar faces facing +Z / -Z |
| `%LINE` `%CIRCLE` `%PLANE` `%CYLINDER` | geometry type |
| `r<5` `r=3` `r>2` | radius of circular edges / cylindrical faces |
| `face(>Z)` | edges bounding the selected faces (e.g. all top edges) |
| `and` `or` `not` `( )` | combine |

Examples: vertical corners of a plate `"|Z and %LINE"`, top outline `"face(>Z)"`, hole edges `"%CIRCLE and r<4"`,
open top of a box `">Z"`. Prefer selectors to indices. They are re-evaluated when upstream dimensions change,
while indices can point at different edges after an edit. Use `inspect` with `"topology": true` to see faces and
edges with their type, centre, normal, direction and radius.

## Workflow

1. **Plan** the part as solids, profiles, booleans, then features: fillets and chamfers last, after the cuts
   they should round.
2. **Parametrise** dimensions the user may change: `{"op": "set_params", "values": {"wall": 2}}`, then use
   `"height": "=Params.wall * 3"`. Expressions can also reference other objects: `"=Plate.Length - 10"`.
   Parameter names must not be unit symbols or constants: `h`, `l`, `t`, `s`, `g`, `e`, `W`, `H`, `mm`, `in`,
   `deg` and similar are rejected (`L` happens to be allowed). Use descriptive names such as `height`,
   `length`, `thickness` or `wall`; the error suggests one.
3. **Send one request per coherent change**, with `expect` on the steps that matter (`volume`, `bbox_size`,
   `bbox_min`, `bbox_max`, `solids`, `self_intersecting`). An expectation that doesn't hold is an error, so mistakes never slip
   through as a success.
   - **Batch repeated features.** Don't cut 30 holes with 30 `cut` steps: each boolean stacked on the last
     is slower than the one before (50 chained cuts take about 20 s, the same holes in one step about 1 s).
     Use one `hole` with all centres in `at` (in a body), several circles in one profile, one `cut` with all
     the `tools`, or an array of the tool.
4. **Read the response:** per-step `bbox`/`volume`, `results`, `warnings`.
5. **Modify existing models in place** rather than rebuilding them:
   `{"doc": "bracket.FCStd", "steps": [{"op": "set_params", "values": {"wall": 3}}]}` or
   `{"op": "set", "target": "Plate", "properties": {"Length": 120}}`. For an unfamiliar document, start with
   `{"doc": "x.FCStd", "op": "inspect"}`, then `inspect` the objects you need. Their `properties` are exactly
   what `set` accepts.
6. **Check fits between parts** with `measure`, e.g.
   `{"op": "measure", "objects": ["Lid", "Box"], "require": {"min_clearance": 0.3}}`. It fails if any gap is
   smaller, and `closest` gives the points where the gap is smallest. Each pair is reported as `clear`,
   `touching` or `interfering` (with the overlap volume).
   - **Mass properties:** `{"op": "measure", "objects": ["Bracket"]}` gives volume, area, centre of mass and
     the inertia tensor (about the centre of mass, global axes) in `properties`; with a material assigned
     (or `material`/`density` given) also the mass, and for several parts the `total` mass and centre of mass.
7. **Check strength** with `fem_static` when the user cares whether a part will hold. Read
   [docs/ANALYSIS.md](docs/ANALYSIS.md) first: loads need units, and every result comes with checks
   (`equilibrium`, `convergence`) that you must report to the user when they did not pass.
8. **Look at it.** Numbers can't show a hole on the wrong face. Add `{"op": "render", "filename": "preview.png"}`
   and view the PNG if you can read images.
   - It shows a 2×2 grid: iso, front (looking along +Y), top (looking down), right (looking along -X).
   - Each view has an axis triad: X red, Y green, Z blue.
   - `mm_per_pixel` in the result lets you estimate sizes.
9. **Drawings and cutting files:**
   - For laser, waterjet or CNC cutting, use `{"op": "export", "filename": "plate.dxf"}`: a 1:1 outline in mm,
     viewed from `top` by default.
   - For a dimensioned workshop drawing, use `{"op": "drawing", "filename": "part.dxf", "title": "...", "preview": "part.png"}`.
     It places front, plan and side views (ISO first angle by default) at a standard scale. Its overall and hole
     dimensions are checked against the model, and the `dimensions` list in the result gives their values.
     Equal holes get one diameter with a count (`4x ⌀5.5`), and a hole table on the sheet (also `holes` in
     the result) gives each vertical hole's X/Y from the lower-left corner of the plan view.
   - Re-run `drawing` after editing the model; it regenerates the page.
   - PDF and SVG pages need the FreeCAD GUI: the page is kept in the `.FCStd`.
10. **Give finished parts a material** so they look right when opened in FreeCAD and in renders, and so
    `measure` reports masses: `{"op": "material", "targets": ["Rim"], "material": "aluminium"}`,
    `{"op": "material", "targets": ["Tire"], "material": "rubber"}`, or a colour for prints:
    `{"op": "material", "targets": ["Case"], "material": "pla", "color": "#E03020"}`. Presets: steel
    (+ _s235, _s355), stainless_steel, stainless_304, cast_iron, aluminium (+ _6061, _7075, _5754), titanium,
    copper, brass, bronze, gold, silver, chrome, pla, abs, petg, nylon, nylon_pa12, pom, polypropylene,
    polycarbonate, acrylic, ptfe, pvc, rubber, glass, wood, concrete; or any FreeCAD library material name.
    Materials of assembly parts go to their source objects. `fem_static` uses the assigned material when it
    is a specific grade (e.g. `steel_s235`, `aluminium_6061`).
11. **Export** at the end. Each export is read back and verified. STEP files carry each part's name, and an
    assembly as a product structure (`verified.part_names`). Mesh exports report `closed`, `non_manifold` and
    `self_intersections`. The extension sets the format.

## Fixing errors

| `error.code` | What to do |
|---|---|
| `INVALID_REQUEST` | Fix every item in `details.problems` (each names its `step` and `param`) and resend. |
| `OBJECT_NOT_FOUND` | Use a name from `details.available`. Names are case-sensitive. |
| `NAME_CONFLICT` | Choose a new name, or edit the existing object with `set`. |
| `RECOMPUTE_FAILED` / `GEOMETRY_INVALID` | Read `hint` and `details.freecad_message`. Typical causes: fillet radius too large (hint gives the shortest edge), coincident boolean faces, self-intersecting profile. |
| `EMPTY_RESULT` | The cut removed everything, or the objects of a `common` don't overlap. Check positions. |
| `EXPECTATION_FAILED` | Compare `details.failures` (expected vs actual) to find the wrong dimension or position. |
| `INVALID_SELECTOR` | The selector matched nothing. `inspect` the base with `topology: true`. |
| `DEPENDENCY` | Delete the dependents first, or pass `with_dependents: true`. |
| `PATH_NOT_ALLOWED` | Use a path inside the workspace. |
| `FREECAD_NOT_FOUND` / `FREECAD_VERSION` / `FREECAD_CRASHED` / `TIMEOUT` | Environment problem (FreeCAD missing, older than 1.1, or crashed): run `doctor` and tell the user. |
| `DOCUMENT_BUSY` | Another request is editing the same document. Wait for it, then retry. |

Don't resend an unchanged request after an error. Change what the error points at.

## Limits

- Only `rect`, `circle` and `slot` profiles are dimensioned and can take expressions; `polygon`, `spline` and
  `path` profiles are fixed outlines, edited by resending `shapes`. Profiles lie in the XY, XZ or YZ plane
  (with an `offset`), not on inclined planes.
- Assemblies: no nested assemblies, no motion (gear, belt, screw) joints, and no limits. FEM is linear static only (no contact, buckling, thermal or modal analysis). Drawings are DXF only (PDF/SVG from the GUI); automatic dimensions
  are the overall sizes and hole diameters, with hole positions in a table rather than as dimension lines, and
  there are no section views or tolerances: tell the user when a drawing needs them. PartDesign supports pad, pocket, revolution, groove, hole,
  fillet, chamfer, shell, loft, sweep, mirror and linear/grid/polar patterns. No surface modelling (free-form
  patches, blends between arbitrary faces). Imported meshes stay faceted.
- If a request needs something these operations can't do, tell the user it isn't supported. Don't work around
  the skill with your own FreeCAD scripts: they skip validation and checks.
- Placement (`position`) values are literal numbers; expressions apply to dimensions.
- The self-intersection check is skipped on results with more than 3000 faces, and cannot run on invalid
  geometry. A result it did not clear is never reported as clean: it carries `self_intersection_check: "not
  checked (reason)"`, the response has a `SELF_INTERSECTION_UNCHECKED` warning, and a STEP/BREP export lists
  it under `verified.self_intersection_unchecked`. When a part must be confirmed free of self-intersection,
  put `"expect": {"self_intersecting": false}` on its step: the request then fails unless the check ran and
  passed. Shapes are checked when a request makes or changes them: a request that only reads (`inspect`,
  `measure`, `export`, `render`) reports `results` without `valid`, and `inspect` of a whole document lists
  objects without it. `inspect` one object for `valid` and `self_intersecting`.
- A STEP import becomes one fixed solid (or compound): part names, colours and assembly structure of the
  file are not kept.

## Scope

What the skill does on the machine, and nothing else:

- **Commands:** it is used through one command, `python3 {baseDir}/scripts/fcskill.py`. The launcher starts
  FreeCAD's command-line program (found automatically, or the one named by `FCSKILL_FREECAD`) with the
  environment it was started in; `fem_static` makes FreeCAD run its bundled Gmsh and CalculiX. No shell, no
  other program, and requests cannot carry code.
- **Files:** it reads and writes inside the workspace only (documents, exports, renders, and the parts cache
  `.fcskill/library`), plus temporary files it removes afterwards (in the system temporary folder, or in
  `~/snap/freecad/common/fcskill` when FreeCAD is a snap). Paths that leave the workspace are refused, and
  the parts cache is never used through links.
- **Network:** only the optional parts library, as anonymous downloads of fixed GitHub URLs
  (`api.github.com` and `raw.githubusercontent.com`, repository FreeCAD/FreeCAD-library), each checked
  against the library's index. Nothing is uploaded. `FCSKILL_OFFLINE=1` turns it off.
- **Environment variables:** it reads the four `FCSKILL_*` settings (FreeCAD command, workspace, local
  library clone, offline switch); on Windows it also reads the standard program-folder variables to find
  FreeCAD. It uses no credentials and stores none.

## Compatibility

Version 3 changes from version 2:

- `export` has no `format` parameter any more: the file extension sets the format.
- `fem_static`: `material` is optional (default: the part's assigned material) and must be a specific grade;
  `aluminium_6061_t6` and `titanium_gr5` are still accepted as names for `aluminium_6061` and `titanium`.
- A part added to an `assembly` without `position` stays where it was modelled (it used to move to the origin).
- `inspect` without a target no longer reports `valid` per object, nor do the `results` of a request that
  changes nothing.

v1 requests (`{"operation": ..., "parameters": ...}`) and `scripts/cad_engine.py` are not supported, and there
is no `python` op: requests use only the operations above. Use only the format described here.
