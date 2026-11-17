# 2D, 3D, or 2D art over a 3D stage

## The decision

| | Use it when | What it costs |
|---|---|---|
| **2D** | side view or top-down, flat art, precise silhouettes, painted cutouts | camera orthographic, sprites + Physics2D, sorting order; real lighting is out |
| **3D** | the camera moves, lighting carries the mood, physics matters | meshes + materials + LOD, heavier WebGL payload, longer iteration |
| **2D art over a 3D stage** | a painted look that still needs depth, or one hero mesh in a flat scene | both pipelines at once, and the mesh must be verified before it is wired |

Two is not "easier 3D" and 3D is not "better 2D". They are different authoring pipelines, and mixing
them without a reason is how a project acquires two half-finished art directions.

## Rules that hold in both

- **Decide the render pipeline at the start.** Built-in vs URP changes every material and every shader.
  Switching later is a re-shade, not a checkbox. A WebGL build wants the smallest shader surface that
  does the job; the worked style in this skill is built-in.
- **Measure assets, do not trust descriptions.** A vision model will describe a torn texture as a
  complete object. Fill the empty alpha with a flat colour and look; the opaque pixel bounds are the
  asset.
- **Verify an imported mesh before it carries anything.** FBX/GLB models arrive with bad scale, flipped
  or missing normals, and shape keys that deform the body. Measured case: a car model whose mesh was
  deformed loaded fine, looked wrong, and could never drive - the fault was the asset, not the
  controller. Check dimensions, bounds and normals first; if the mesh is deformed, fix or replace the
  asset instead of tuning physics around it.
- **Name the frame budget out loud** for a web build: what runs at 60 fps on the desktop may not on a
  laptop iGPU. A WebGL build's cost is shader variety and payload more than polycount.

## Sprites in Unity, without the classic mistakes

- **Unity's sprite origin is the bottom-left of the texture, and the sprite rect must cover the whole
  texture** when the art is a single cutout. `SpriteMeshType.FullRect` is `0`; `Tight` is `1`. A torn
  picture with mesh type `0` is a bad rect or a torn source file - it is not a tight mesh. Setting the
  mesh type and leaving a cropped `spriteSheet` rect still draws the fragment.
- **Frames delivered as individual PNGs should not be pushed through a sprite-sheet extractor.** Import
  them as they are; an extractor's re-crop is a new source of torn edges.
- **Pivots carry meaning.** An idle pivot at the feet keeps a character planted; a strike frame's pivot
  shifts so the leading edge is the fist. Getting this wrong reads as sliding, not as animation.
- **Sorting in a stack is sibling order.** In the worked style: ring back, bodies, planted prop, ring
  front, spark. A prop parented to the wrong parent - e.g. to a canvas whose coordinates were computed
  for the stage plate - lands in the wrong place no matter what its transform says.
- **A cropped prop must be searched in its own region.** Cropping an object out of a character frame by
  colour grabs everything of that colour: search inside the region you already know it occupies.

## 3D pieces inside a 2D look

- A mesh, baker or 3D scene joins a painted style **only after a watched frame matches the existing
  art**. Otherwise the result is a render that looks like two projects.
- Do not change the project's pipeline to accommodate one effect. If an effect needs a different
  pipeline, the effect is the thing to replace.
- Do not replace a hand-made or generated art asset with a marketplace pack mid-project: the pack's
  style becomes the new bar and the rest of the art is now wrong.

## Shaders, on a WebGL build

- **No `pow()` in a shader that runs in a WebGL build** - it can return NaN. Write `x * x`.
- **A shader is stripped from the player unless a material asset references it.** Ship the `.mat`
  together with the `.shader`; `Shader.Find` on an unreferenced shader will not save it from stripping.
- Additive overlay shaders commonly use `Blend SrcAlpha One` with unpremultiplied RGB.
- **Tumble vs spin is a transform decision:** an ellipse drawn flat in a shader and spun *inside the
  shader* reads as a ring; rotating the RectTransform instead makes the ellipse tumble out of plane.
