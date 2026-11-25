---
name: shaderfx-effects
description: "Write your own GPU effects for Levea in WGSL (ShaderFX ABI v2 + v3): filters that read and rewrite the footage, transitions that read clip A and clip B, and generators like light leaks, plus (ABI v3) named textures, feedback trails, multi-pass bloom, data-driven charts and instanced particles / sprites, with real alpha, typed reusable parameters, server-side validation with line/column errors, and an effect library. The same shader runs in the WebGPU preview and the Vulkan export."
version: 1.1.0
author: brajendrak00068
license: MIT
---

# ShaderFX: custom GPU filters, transitions and generators (ABI v2)

ShaderFX lets an agent write a small WGSL function, `fx(c: FxCtx) -> vec4<f32>`, and run it on the GPU as part of a Levea edit. The server wraps it in a harness (bindings, helpers, output handling), validates it with naga before anything is saved or rendered, and the WebGPU preview and the Vulkan export compile the same wrapped shader with the same bindings, so what `render_preview` shows is what the export renders.

Use a built-in effect first when one fits: `search_tools` with `catalog: "vfx"` (368 GPU effects) or `catalog: "transitions"` (168). Write a ShaderFX effect when the look you need does not exist, when it has to read the footage in a specific way, or when you want a reusable house effect with its own parameters.

## Setup

This skill calls the Levea (livecore.ai) editing service, which requires a Levea account and API key.

1. Sign up and generate an API key at https://livecore.ai/?openclaw=1&utm_source=clawhub&utm_medium=skill&utm_campaign=shaderfx-effects
2. Provide the key to the tool you use:
   - MCP server `levea-mcp-server` (npm): set `LEVEA_API_KEY` in the MCP server config. `LEVEA_API_URL` is optional and defaults to `https://api.livecore.ai`.
   - Hosted MCP (`https://api.livecore.ai/api/v1/misc/mcp`): OAuth, no key needed.
   - OpenClaw plugin `openclaw-ai-video-editor` (ClawHub): set `apiKey` in the plugin config.

## Tools

| MCP tool | Canonical action (also callable via `execute_action` / `execute_batch`) | What it does |
|---|---|---|
| `create_shader_effect` | `CREATE_SHADER_EFFECT { name, source, manifest, description?, is_public?, overwrite? }` | Validates and saves an effect to your library; returns `effect_id` and the parameter table (name, type, slot, accessor), or `errors: [{ line, column, message }]` and saves nothing. `overwrite: true` replaces your effect of the same name |
| `list_shader_effects` | `LIST_SHADER_EFFECTS { include_public?, query?, limit? }` | Your saved effects (id, name, kind, output, params) |
| (via `execute_action`) | `GET_SHADER_EFFECT { effect_id }` | One effect with its source, manifest and parameter table |
| `apply_shader_effect` | `APPLY_SHADER_EFFECT` (fields below) | Adds a ShaderFX layer to the project |
| `delete_shader_effect` | `DELETE_SHADER_EFFECT { effect_id }` | Removes it from the library; layers it was applied to keep their compiled shader |

`APPLY_SHADER_EFFECT` fields:

| field | meaning |
|---|---|
| `effect_id` or `source` + `manifest` | a saved effect, or inline code (validated the same way) |
| `kind` | `filter` \| `transition` \| `generator`. Optional: the request's, else the manifest's, else `transition` when `from_layer_id` + `to_layer_id` are given, `filter` when `target_layer_id` is |
| `target_layer_id` | filter: the layer whose picture is `src()`; the effect layer goes just above it and spans its window. Omit to filter everything composited below (the effect goes above the top picture layer) |
| `from_layer_id` + `to_layer_id` | transition: outgoing clip A and incoming clip B (see Transitions below) |
| `params` | values by manifest name: `{ "strength": 0.8, "tint": "#ff8800", "direction": [0, 1] }`. Unknown names or wrong shapes are errors; floats are clamped to the param's min/max |
| `param_keyframes` | animate params over time (see Parameter keyframes below) |
| `start_time`, `end_time` | filter / generator window in timeline seconds (default: the target's window, else the whole timeline). Ignored for transitions |
| `duration_sec`, `easing` | transition length (default 0.8 s) and the easing of its progress (default `linear`) |
| `output` | overrides the manifest's output mode |
| `intensity`, `opacity`, `z_index` | the layer's `c.intensity` (default 1), opacity (default 1) and stacking override |

The result names the new layer (`layer_id`, `createdLayerIds`), its window and the parameter table. Failure codes: `SHADER_FX_INVALID` (shader or manifest errors, with `errors`), `SHADER_FX_INVALID_PARAMS`, `SHADER_FX_TARGET_NOT_FOUND`, `SHADER_FX_CLIPS_NOT_ADJACENT`, `SHADER_FX_NO_HANDLES`, `SHADER_FX_NOT_FOUND`.

The old path still works: `APPLY_VFX` / `TRANSITION` with `custom_shader_frag` is ABI v1 (`evaluate_pixel(uv, time, res, progress, intensity)`, no picture input, light-only output). Use ABI v2 for anything new.

### Workflow

1. Write `source` + `manifest`. Call `create_shader_effect`.
2. If it returns `errors`, fix those lines (they are numbered in YOUR source, not the wrapped shader) and call again.
3. `apply_shader_effect` with the returned `effect_id`, the layers, the window and `params`.
4. `render_preview` at 2-4 timestamps inside the window (for a transition: start, middle, end) and look at the frames. A shader the GPU could not build is reported there (`customShaderErrors`). Adjust `params` or the source and re-apply.
5. Export with `execute_action` `EXPORT_VIDEO`.

You can skip the library and pass `source` + `manifest` straight to `apply_shader_effect` for one-off effects.

```json
{
  "project_id": "proj_123",
  "effect_id": "fx_abc",
  "kind": "transition",
  "from_layer_id": "clip_1",
  "to_layer_id": "clip_2",
  "duration_sec": 0.6,
  "easing": "ease_in_out",
  "params": { "strength": 0.7 }
}
```

### Transitions: the overlap

A transition layer draws across the time where clip A and clip B overlap. `c.progress` runs 0 → 1 across that overlap (keyed on the layer, with `easing`).

- Clips that already overlap: the existing overlap is used (with `duration_sec`, only its last `duration_sec`).
- Clips that meet at a cut: an overlap of `duration_sec` (default 0.8 s, at most half the shorter clip) is created from media handles, without changing the program length. If clip A has media after its out point, A plays on under B (tail handle, the transition starts at the cut). Otherwise, if B has media before its in point, B starts earlier on that earlier media (head handle, the transition ends at the cut).
- Neither clip has enough media beyond the cut: `SHADER_FX_NO_HANDLES`. Overlap the clips first (`TRIM_LAYER` / `SET_SOURCE_RANGE`) or pass a shorter `duration_sec`.
- Clips with a gap between them: `SHADER_FX_CLIPS_NOT_ADJACENT`. `from_layer_id` is the outgoing clip, `to_layer_id` the incoming one.

The effect layer sits above both clips, and `replace` output (the usual choice) covers them for the overlap.

### Parameter keyframes

`param_keyframes` animates manifest params: `{ "<param name>": [ { "time": <timeline seconds>, "value": <the param's own type>, "easing": "<optional>" }, ... ] }`, at least 2 keyframes per param. Each param becomes `fx_param_<slot>` tracks. A `vec2` / `vec3` / `color` gets one track per component. A `bool` steps. Values are encoded like `params` (hex or `[r, g, b(, a)]` for colors, clamped to min/max). Keyed params override the static `params` value while the keyframes apply.

```json
{
  "project_id": "proj_123",
  "effect_id": "fx_streak",
  "target_layer_id": "@primary",
  "start_time": 2, "end_time": 6,
  "params": { "tint": "#66ccff" },
  "param_keyframes": {
    "strength": [ { "time": 2, "value": 0 }, { "time": 3, "value": 1, "easing": "ease_out" }, { "time": 6, "value": 0.2 } ],
    "direction": [ { "time": 2, "value": [1, 0] }, { "time": 6, "value": [0, 1] } ]
  }
}
```

## The author contract

### What you write

```wgsl
fn fx(c: FxCtx) -> vec4<f32> {
    // return STRAIGHT (non-premultiplied) rgba
}
```

You may add your own helper functions, structs and `const`s above `fx`. The server adds the bindings and the entry point. Rejected before compiling:

- any `@fragment`, `@vertex`, `@compute`, `@group` or `@binding`;
- a module-scope `fn` / `struct` / `var` / `const` / `alias` named like a harness symbol: `fs_main`, `vs_main`, `FxCtx`, `FxParams`, `LayerUniforms`, `VertexOutput`, `VertexInput`, `u`, `fxp`, `t_src`, `s_linear`, `t_backdrop`, `t_b`, `src`, `backdrop`, `clip_a`, `clip_b`, `param`, `param_color`, `hash2`, `noise2`, `fbm`, `luma`, `rotate2`, your `P_<name>` accessors, or anything starting with `_fx_` / `_harness_`. A local `let` / `var` inside a function may reuse these names.

### FxCtx

| field | type | meaning |
|---|---|---|
| `uv` | `vec2<f32>` | the effect layer's texture coordinate. The layer is a full-canvas quad, so this is 0..1 across the canvas, top-left origin (y grows downward), and `src(c.uv)` is the pixel under the fragment |
| `px` | `vec2<f32>` | `uv * res` |
| `res` | `vec2<f32>` | render-target size in pixels: the bound backdrop's size (on export, canvas × supersample), else the layer size. It is not the scene canvas size, so build resolution-independent detail from `uv` and use `res` for aspect (`res.x / res.y`) |
| `time` | `f32` | the layer clock: seconds since the effect layer started |
| `local_time` | `f32` | the same layer clock (equal to `time`) |
| `progress` | `f32` | transition: the keyed transition progress, 0 → 1 across the overlap. Filter / generator: `time / layer length`, clamped to 0..1 |
| `intensity` | `f32` | the layer's `fx_intensity` (default 1); multiply your strength by it |

Aspect-correct anything round: `var p = c.uv - vec2<f32>(0.5, 0.5); p.x = p.x * (c.res.x / c.res.y);`

### Pictures you can read (all in canvas space, straight rgba)

| helper | filter | transition | generator |
|---|---|---|---|
| `src(uv)` | the target layer (`target_layer_id`) rendered alone, transparent elsewhere; without a target, everything composited below this layer | clip A | transparent |
| `backdrop(uv)` | everything composited below this layer this frame | same | same |
| `clip_a(uv)` | same as `src` | outgoing clip (`from_layer_id`) | transparent |
| `clip_b(uv)` | transparent | incoming clip (`to_layer_id`) | transparent |

Pictures are full-canvas and the same resolution as the render target. Offset the uv to displace, blur or split. Sampling is linear with clamp-to-edge, so uvs outside 0..1 repeat the edge pixel; mask them yourself if you need transparency there. The helpers sample at mip level 0 (`textureSampleLevel`), so they can be called anywhere, including inside branches and loops.

### Other helpers

| helper | signature | notes |
|---|---|---|
| `P_<name>` | `P_strength()` … | one per manifest param: `float` → `f32`, `vec2` → `vec2<f32>`, `vec3` → `vec3<f32>`, `color` → `vec4<f32>` (straight rgba, 0..1), `bool` → `f32` 0.0 or 1.0 (test `P_flag() > 0.5`). Prefer these over indices |
| `param` | `param(i: u32) -> f32` | raw slot i (0..31, clamped) |
| `param_color` | `param_color(i: u32) -> vec4<f32>` | 4 consecutive slots from i |
| `hash2` | `hash2(p: vec2<f32>) -> f32` | white noise in 0..1 |
| `noise2` | `noise2(p: vec2<f32>) -> f32` | smooth gradient noise, signed (about -0.5..0.5); add 0.5 for 0..1 |
| `fbm` | `fbm(p: vec2<f32>) -> f32` | 4 octaves of `noise2`, also signed |
| `luma` | `luma(rgb: vec3<f32>) -> f32` | Rec. 709 luma (0.2126, 0.7152, 0.0722) |
| `rotate2` | `rotate2(v: vec2<f32>, angle: f32) -> vec2<f32>` | rotate by radians |

### Output modes (`manifest.output`, or `output` on apply)

The harness clamps what `fx` returns to 0..1, multiplies by the layer opacity, and composites premultiplied "over":

- `normal` (default): your rgba over what is below, with real alpha. Alpha 1 black is black, so vignettes, shadows, letterboxes, darkening and full re-renders of a layer all work. For filters that rewrite a picture, return the picture's own alpha (`src(uv).a`) so the area outside the layer stays untouched.
- `add`: `rgb × a` is added onto what is below (light only; nothing is covered). Glows, leaks, sparks, flares. Alpha works as a light mask.
- `replace`: your rgb replaces what is below, with alpha set to the layer opacity (1 by default), over the whole canvas. Use it for transitions between full-frame clips and for generators that paint every pixel. Do not use it for a filter on a layer that does not cover the frame: the transparent area outside the layer would turn black.

### Manifest and parameter slots

```json
{ "abi": 2, "kind": "filter", "output": "normal",
  "params": [ { "name": "strength", "type": "float", "min": 0, "max": 1, "default": 0.5 },
              { "name": "tint", "type": "color", "default": "#ffcc66" },
              { "name": "direction", "type": "vec2", "default": [1, 0] } ] }
```

- `abi`, if given, is 2 or 3 (the features used decide; see ABI v3 below). `kind`: `filter` (default) | `transition` | `generator`. `output`: `normal` (default) | `add` | `replace`.
- Param names start with a letter and use letters, digits and `_`, at most 40 characters, unique. They become accessors: `P_strength()`, `P_tint()`, `P_direction()`. Optional `min`, `max`, `description`.
- Slot sizes: `float` 1, `bool` 1, `vec2` 2, `vec3` 4 (xyz plus padding), `color` 4 (rgba). Slots are assigned in declaration order, and `vec3` / `color` start on the next multiple of 4. Above: `strength` → 0, slots 1-3 unused, `tint` → 4-7, `direction` → 8-9. Declare 4-slot params first to avoid gaps. Total ≤ 32 slots.
- Value formats: `float` a number; `bool` `true` / `false`; `vec2` `[x, y]` or `{x, y}`; `vec3` `[x, y, z]`; `color` `"#rgb"`, `"#rgba"`, `"#rrggbb"`, `"#rrggbbaa"`, `[r, g, b(, a)]` or `{ r, g, b, a? }` in 0..1.
- Without a `default`: `float` 0 (clamped to min/max), `bool` false, vectors 0, `color` opaque white.

### Validation and limits

- The wrapped shader is compiled with the renderer's own naga (wasm build on the server) before anything is saved or rendered. Errors come back as `{ line, column, message }` on your own lines. An error inside the generated harness has line 0 and usually means `fx` has the wrong signature or a name collides.
- Author source ≤ 24 KB.
- Keep every loop bounded by a constant (`for (var i = 0; i < 8; i = i + 1)`). A layer whose pipeline fails to build or that stalls the GPU is skipped (picture unchanged) and reported.
- The same WGSL runs in preview (WebGPU) and export (Vulkan): no renderer-specific code.

### WGSL pitfalls that fail validation

- Float literals: `1.0`, not `1`, in float math. `let k = 1;` is an `i32` and `k * 0.5` will not compile. Convert with `f32(i)`.
- Vector constructors need the type: `vec2<f32>(0.5, 0.5)`, `vec3<f32>(1.0)` (a single value splats), `vec4<f32>(rgb, a)`.
- `let` is immutable; use `var` for anything you assign to (including swizzle writes like `p.x = ...`).
- There is no `?:`; use `select(if_false, if_true, cond)` or `mix`/`step`.
- No recursion, no implicit conversions between `i32`, `u32` and `f32`; `param(2u)` takes a `u32`.
- `smoothstep(e0, e1, x)` needs `e0 < e1`.

## ABI v3: textures, feedback, multi-pass, data, geometry

ABI v3 (ADR 0002) adds five optional features to the v2 contract above. Every v2 effect keeps working unchanged. The server picks the ABI automatically: v3 when an effect uses any feature below, else v2. A v3 effect that uses none of them renders exactly like v2. Everything above (FxCtx, helpers, output modes, params, `param_keyframes`, transitions) still applies.

`FxCtx` gains one field in v3: `frame: u32` = `floor(local_time × scene fps)`, the frame index since the layer started (the scene fps is baked in at apply time; 30 when the scene names none).

You can leave `abi` out of a v3 manifest: the server switches to v3 by itself when a feature below is present. `"abi": 2` and `"abi": 3` are both accepted (saved v3 effects come back from `GET_SHADER_EFFECT` with `abi: 3`), but the features you use decide the ABI, not this field.

| feature | manifest declares | apply / create supplies | author uses |
|---|---|---|---|
| Named textures (≤ 4) | `textures: [{ name }]` | `textures: [{ name, layer_id \| asset_url, space? }]` | `tex_<name>(uv)`, `tex_size_<name>()` |
| Feedback | `feedback: { enabled: true, warmup_sec?, clear? }` (or `true`) | `feedback` (same shape) | `prev(uv)`, `c.frame` |
| Multi-pass (≤ 4) | `passes: [{ name, scale? }]` | (source defines the passes) | `fn pass_<name>(c: FxCtx)`, `buf_<name>(uv)` |
| Data buffer | optional `data` / `data_url` | `data: number[]`, or `data_url` (+ `data_columns` for CSV) | `data(i)`, `data_len()`, `data_vec2(i)`, `data_vec4(i)` |
| Geometry | `geometry: { mode, count }` | `geometry` (same shape) | `fn instance(i, c)`, optional `fn shade(p, c)` |

`CREATE_SHADER_EFFECT` and `APPLY_SHADER_EFFECT` both accept `textures`, `feedback`, `data` / `data_url` and `geometry`. A saved effect stores all of them, and apply-time values replace the saved ones: feedback, geometry and data replace outright, and a texture entry with a source replaces the declared texture of the same name. The manifest gains `passes`, `textures` (the declared names), `feedback`, `geometry` and optionally `data` / `data_url`. Inline `data` wins over `data_url`.

### Named textures (bindings 6-9)

Up to 4 named pictures besides `src` / `backdrop` / clips. Names match `[a-z][a-z0-9_]{0,23}`, and their order is the slot order. Each entry gives `layer_id` OR `asset_url`, not both.

- `{ "name": "logo", "layer_id": "logo_1" }`: that layer rendered alone (its transform, crop and grade; transparent elsewhere), the same way v2 renders clip pictures. Text, image / logo, motion-graphics and video layers all work. Hidden layers work too: hide the source layer (`visible: false`) when only the shader's version should show. Default `space: "canvas"`: a canvas-space picture, so `tex_logo(c.uv)` is the pixel under the fragment.
- `{ "name": "sheet", "asset_url": "https://…/walk.png" }`: a png / jpg / webp image (≤ 4096 × 4096, public URL only) decoded once. Default `space: "image"`: sampled in the image's own 0..1 UV, for sprite sheets, logos, LUT strips and noise textures.
- Helpers (generated per name): `tex_<name>(uv: vec2<f32>) -> vec4<f32>` (straight rgba, linear, clamp-to-edge) and `tex_size_<name>() -> vec2<f32>` (pixels).
- A declared texture still needs a source by apply time: apply fails with `SHADER_FX_INVALID_INPUT` ("texture … has no source") if neither the saved effect nor the request gives one. A `layer_id` that is not on the timeline fails with `SHADER_FX_TARGET_NOT_FOUND`, and a non-public `asset_url` with `SHADER_FX_PRIVATE_URL`.

### Feedback (binding 10)

`feedback: { "enabled": true, "warmup_sec": 1.0, "clear": [0, 0, 0, 0] }` gives the shader `prev(uv) -> vec4<f32>`: THIS layer's own output from the previous frame (straight rgba, render-target size), cleared to `clear` (default transparent) on the layer's first frame. `feedback: true` is shorthand for `{ enabled: true }`, and `{ enabled: false }` turns a saved effect's feedback off. Use it for trails, echoes, smears, accumulation and reaction-diffusion-style looks.

- Export renders sequentially, so feedback is exact.
- `render_preview` and seeking re-render the layer alone from `max(start_time, t − warmup_sec)` up to `t` at the scene fps, then show frame `t`. Same `t`, same pixels. Choose `warmup_sec` (default 1.0, 0..4) at least as long as your trail takes to fade, or previews will show a shorter trail than the export.
- What you return is what `prev` gives back next frame, so a decay factor below 1 is what keeps trails from saturating.
- Not available in geometry mode.

### Multi-pass (bindings 11-14)

Declare `passes: [{ "name": "bright", "scale": 0.5 }, { "name": "blur", "scale": 0.25 }]` (≤ 4; `scale` 1, 0.5 or 0.25, default 1) and define one function per pass in the source:

```wgsl
fn pass_bright(c: FxCtx) -> vec4<f32> { ... }
fn pass_blur(c: FxCtx) -> vec4<f32> { ... }   // may read buf_bright(uv)
fn fx(c: FxCtx) -> vec4<f32> { ... }          // final pass, may read every buf_
```

- Passes run in declaration order every frame, before the final `fx`. Each renders a full-target quad into its own rgba16float buffer (render target × scale), cleared each frame.
- A pass's return value is stored RAW: not clamped, not premultiplied or converted, in rgba16float. Values above 1 and negative values survive, so a pass can carry HDR light, vectors or masks. `buf_<name>(uv) -> vec4<f32>` reads it back raw, with linear filtering, so a lower-scale buffer upsamples smoothly. A pass reading itself or a later pass gets transparent. Only the final `fx` is clamped to 0..1 and goes through the output mode.
- Inside `pass_<name>`, `c.res` and `c.px` are the pass buffer's size (render target × scale). `c.uv` is still 0..1 over the frame.
- Every pass can use every input: `src`, `backdrop`, clips, textures, `prev`, `data`, params.
- Offsets in uv units look the same at any scale and on a supersampled export. Use `1.0 / c.res` inside a pass only when you want exactly one texel of that pass's buffer.
- Each pass adds a full-target render per frame. Use 0.5 / 0.25 scale for blurs and glows.

### Data buffer (binding 15)

`data: [12, 30, 18, 44]` (≤ 16384 floats), or `data_url`: a public http(s) / gs:// URL the server reads at apply time and stores as floats.

- JSON: an array (or `{ "data": [...] }`). Nested arrays and row objects are flattened in order, and non-numbers are skipped.
- CSV (`,` `;` or tab): a header row is detected when the first row has a non-numeric cell. Numbers are read row by row. With `data_columns: ["revenue", 3]` (header names or 0-based indexes) only those columns are read, in that order, per row. Without it, every numeric cell is read.
- Fetch problems or no numbers: `SHADER_FX_DATA_UNAVAILABLE`.

 Helpers: `data(i: u32) -> f32` (returns 0 past the end, never out of bounds), `data_len() -> u32`, `data_vec2(i: u32) -> vec2<f32>`, `data_vec4(i: u32) -> vec4<f32>` (2 / 4 consecutive floats from `i`). Use it for charts, per-particle state, lookup tables and keyed positions. Pack records with a fixed stride (e.g. 4 floats per point: x, y, size, hue) and read them with `data_vec4(i * 4u)`.

### Geometry mode (instanced quads / points)

`geometry: { "mode": "quads", "count": 2000 }` (`mode` default `quads`; `count` an integer 1..65536; in `"points"` mode an instance whose `size` is not positive is drawn 4 × 4 px) draws `count` instances of a quad instead of one full-target quad. The source defines (no `fx` is needed in geometry mode):

```wgsl
fn instance(i: u32, c: FxCtx) -> FxInstance { ... }      // required, runs per vertex
fn shade(p: FxPixel, c: FxCtx) -> vec4<f32> { ... }      // optional, per pixel
```

- `FxInstance { pos: vec2<f32> /* canvas uv of the centre */, size: vec2<f32> /* pixels */, rotation: f32 /* radians, about the centre */, color: vec4<f32> /* straight */, uv_rect: vec4<f32> /* x, y, w, h in a texture */, alive: f32 /* <= 0 culls */ }`.
- `FxPixel { local_uv: vec2<f32> /* 0..1 across the quad, (0, 0) = its top-left corner before rotation */, uv: vec2<f32> /* canvas uv */, color: vec4<f32>, uv_rect: vec4<f32>, instance: u32 }`.
- Without `shade`: with no texture, a soft round point, alpha `1 − smoothstep(0.42, 0.5, distance(local_uv, 0.5))` × `color`. With a texture, the FIRST texture sampled at `uv_rect.xy + local_uv × uv_rect.zw` × `color` (the whole texture when `uv_rect` has zero width or height).
- In `instance()`, `c.uv` is (0.5, 0.5) and `c.res` the render-target size. In `shade()`, `c.uv` / `p.uv` is the pixel's canvas uv.
- `instance()` runs in the vertex stage: compute motion in closed form from `i` and `c.local_time` (hash the index for randomness), or read per-instance state from `data`. Do not use `prev`: feedback is per-pixel and unavailable here. A closed-form system renders any frame on its own, so previews and seeks are exact.
- `size` is in render-target pixels: scale by `c.res.y / 1080.0` to keep the same look on supersampled exports. Set `alive = 0.0` (anything <= 0) for particles not yet born or already dead.
- `fx_output` still applies (`add` for glowing sparks, `normal` for solid sprites).

### Limits (v3)

≤ 4 textures, ≤ 4 passes, ≤ 16384 data floats, ≤ 65536 instances, author source ≤ 48 KB in total, asset images ≤ 4096² and fetched from public addresses only. Every generated module is validated: each pass, the final pass, and the vertex + fragment stages in geometry mode. Errors map to your own lines and name the module that failed, e.g. `(pass blur)`, `(geometry vertex)`, `(final pass)`. Also reserved in v3 (module scope): `prev`, `data`, `data_len`, `data_vec2`, `data_vec4`, `FxData`, `FxInstance`, `FxPixel`, `FxGeoOut`, `fxd`, `FX_FPS`, `t_tex0`…`t_tex3`, `t_prev`, `t_pass0`…`t_pass3`, and the generated `tex_<name>`, `tex_size_<name>` and `buf_<name>`. A layer whose shaders fail to build is skipped and reported (`custom_shader_errors`). Feedback warm-up and passes multiply per-frame cost, so keep counts and scales as low as the look allows.

## Examples (ABI v2)

Each example is complete: `source` is what you pass to `create_shader_effect` / `apply_shader_effect`, together with its manifest.

### 1. Filter: chromatic split + barrel distortion of the footage

Manifest: `{ "abi": 2, "kind": "filter", "output": "normal", "params": [] }`. Apply with `target_layer_id` to treat one clip, or without it to treat everything below.

```wgsl
// Barrel-distort uv around the centre, aspect-correct. Corners stay on corners,
// so the frame is never pulled in from the edges.
fn barrel(uv: vec2<f32>, k: f32, aspect: f32) -> vec2<f32> {
    var p = uv * 2.0 - 1.0;
    p.x = p.x * aspect;
    let r2 = dot(p, p);
    let corner_r2 = aspect * aspect + 1.0;
    p = p * (1.0 + k * r2) / (1.0 + k * corner_r2);
    p.x = p.x / aspect;
    return p * 0.5 + 0.5;
}

fn fx(c: FxCtx) -> vec4<f32> {
    let aspect = c.res.x / c.res.y;
    let k = 0.18 * c.intensity;
    let uv = barrel(c.uv, k, aspect);

    // Radial RGB split, strongest at the edges, breathing slowly.
    let dir = uv - vec2<f32>(0.5, 0.5);
    let split = (0.012 + 0.004 * sin(c.time * 2.0)) * c.intensity;
    let r = src(uv + dir * split);
    let g = src(uv);
    let b = src(uv - dir * split);

    let alpha = max(r.a, max(g.a, b.a));
    return vec4<f32>(r.r, g.g, b.b, alpha);
}
```

### 2. Filter: dark cinematic vignette with real alpha

Manifest: `{ "abi": 2, "kind": "filter", "output": "normal", "params": [] }`. Apply without `target_layer_id`, above the footage. It only paints near-black with alpha, so it darkens (impossible with ABI v1's light-only output).

```wgsl
fn fx(c: FxCtx) -> vec4<f32> {
    let aspect = c.res.x / c.res.y;
    var p = c.uv - vec2<f32>(0.5, 0.5);
    p.x = p.x * aspect;
    // 0 at the centre, 1 at the corners.
    let d = length(p) / length(vec2<f32>(0.5 * aspect, 0.5));
    let falloff = smoothstep(0.35, 1.05, d);

    // A touch of animated grain in the dark area breaks up banding. Built from uv
    // (not px), so the grain size is the same in preview and supersampled export.
    let grain_cell = floor(c.uv * vec2<f32>(720.0 * aspect, 720.0));
    let grain = (hash2(grain_cell + vec2<f32>(c.time * 61.0, c.time * 17.0)) - 0.5) * 0.06;
    let alpha = clamp((falloff * 0.9 + grain * falloff) * c.intensity, 0.0, 1.0);

    // Slightly cool shadow colour reads as a lens, not a black overlay.
    return vec4<f32>(0.01, 0.012, 0.02, alpha);
}
```

### 3. Transition: displacement morph A→B driven by progress and noise

Manifest: `{ "abi": 2, "kind": "transition", "output": "replace", "params": [] }`. Apply with `from_layer_id` + `to_layer_id`; 0.6-1.0 s works well.

```wgsl
fn fx(c: FxCtx) -> vec4<f32> {
    let t = smoothstep(0.0, 1.0, c.progress);
    let aspect = c.res.x / c.res.y;
    let q = vec2<f32>(c.uv.x * aspect, c.uv.y) * 3.0;

    // A flowing 2D noise field used as the displacement direction.
    let n = vec2<f32>(
        fbm(q + vec2<f32>(c.time * 0.4, 0.0)),
        fbm(q + vec2<f32>(17.3, 9.1) - vec2<f32>(0.0, c.time * 0.4))
    );
    let amount = 0.25 * c.intensity;

    // A is pushed away as t grows; B settles in from the opposite push.
    // At t = 0 A is untouched, at t = 1 B is untouched.
    let a = clip_a(c.uv + n * amount * t);
    let b = clip_b(c.uv - n * amount * (1.0 - t));

    // Noise-dependent local progress: some areas morph earlier than others.
    let key = clamp(n.x + 0.5, 0.0, 1.0);
    let m = smoothstep(0.0, 1.0, clamp(t * 1.6 - key * 0.6, 0.0, 1.0));
    return mix(a, b, m);
}
```

### 4. Transition: ink-bleed wipe using the luma of clip B

Manifest: `{ "abi": 2, "kind": "transition", "output": "replace", "params": [] }`. Bright areas of the incoming shot bleed in first, with a ragged dark ink edge.

```wgsl
fn fx(c: FxCtx) -> vec4<f32> {
    let t = c.progress;
    let a = clip_a(c.uv);
    let b = clip_b(c.uv);

    // Reveal order: bright parts of B first, with fbm making the edge ragged.
    let ink = fbm(c.uv * 7.0 + vec2<f32>(0.0, t * 1.5)) + 0.5;
    let key = clamp((1.0 - luma(b.rgb)) * 0.7 + ink * 0.3, 0.0, 1.0);

    // Sweep a soft threshold from below 0 to above 1 so both ends are exact.
    let soft = 0.08;
    let sweep = t * (1.0 + 2.0 * soft) - soft;
    let m = smoothstep(key - soft, key + soft, sweep);

    // Dark ink rim where the two shots meet.
    let rim = 1.0 - abs(m * 2.0 - 1.0);
    let col = mix(a, b, m);
    let shade = 1.0 - 0.65 * rim * c.intensity;
    return vec4<f32>(col.rgb * shade, 1.0);
}
```

### 5. Generator: animated light leaks

Manifest: `{ "abi": 2, "kind": "generator", "output": "add", "params": [] }`. Apply with `start_time` / `end_time` over the section; it fades itself in and out with `c.progress` (time through the layer).

```wgsl
fn blob(p: vec2<f32>, centre: vec2<f32>, radius: vec2<f32>) -> f32 {
    let d = (p - centre) / radius;
    return exp(-dot(d, d));
}

fn fx(c: FxCtx) -> vec4<f32> {
    let t = c.local_time;
    let aspect = c.res.x / c.res.y;
    let p = vec2<f32>(c.uv.x * aspect, c.uv.y);

    // Slow drifting warp so the leaks feel like light through glass.
    let warp = fbm(p * 1.5 + vec2<f32>(t * 0.12, -t * 0.08));

    let c1 = vec2<f32>(aspect * (0.10 + 0.20 * sin(t * 0.35)), 0.15 + 0.12 * cos(t * 0.27));
    let c2 = vec2<f32>(aspect * (0.90 + 0.15 * cos(t * 0.22 + 1.3)), 0.80 + 0.15 * sin(t * 0.31 + 0.7));
    let l1 = blob(p + warp * 0.20, c1, vec2<f32>(0.55, 0.35));
    let l2 = blob(p - warp * 0.15, c2, vec2<f32>(0.45, 0.30));

    let warm = vec3<f32>(1.0, 0.42, 0.12);
    let gold = vec3<f32>(1.0, 0.78, 0.35);
    let flicker = 0.85 + 0.3 * noise2(vec2<f32>(t * 3.0, 0.0));
    let fade = smoothstep(0.0, 0.15, c.progress) * (1.0 - smoothstep(0.85, 1.0, c.progress));

    let light = (warm * l1 + gold * l2 * 0.8) * flicker * fade * c.intensity;
    return vec4<f32>(light, 1.0);
}
```

### 6. Parameterized reusable effect: tinted directional streak

Manifest (save once with `create_shader_effect`, then re-apply anywhere with different `params`):

```json
{ "abi": 2, "kind": "filter", "output": "normal",
  "params": [ { "name": "strength", "type": "float", "min": 0, "max": 1, "default": 0.5 },
              { "name": "tint", "type": "color", "default": "#ffcc66" },
              { "name": "direction", "type": "vec2", "default": [1, 0] } ] }
```

```wgsl
fn fx(c: FxCtx) -> vec4<f32> {
    let s = P_strength() * c.intensity;
    let tint = P_tint();                       // rgba; tint.a scales how much tint is used
    let dir_raw = P_direction();
    let dir = dir_raw / max(length(dir_raw), 0.0001);
    let aspect = c.res.x / c.res.y;
    let step_uv = vec2<f32>(dir.x / aspect, dir.y) * 0.04 * s;

    // Directional streak: 9 taps along the direction (constant loop bound).
    let base = src(c.uv);
    var acc = vec4<f32>(0.0);
    for (var i = 0; i < 9; i = i + 1) {
        let o = f32(i) / 8.0 - 0.5;
        acc = acc + src(c.uv + step_uv * o);
    }
    acc = acc / 9.0;

    // Highlights streak and pick up the tint; shadows stay put.
    let hi = smoothstep(0.45, 1.0, luma(acc.rgb));
    let streak = mix(base.rgb, acc.rgb, s);
    let tinted = mix(streak, streak * tint.rgb * 1.3, hi * tint.a * s);

    // A soft wash along the direction ties the frame together.
    let along = clamp(dot(c.uv - vec2<f32>(0.5, 0.5), dir) + 0.5, 0.0, 1.0);
    let wash = tint.rgb * along * 0.12 * s;

    return vec4<f32>(clamp(tinted + wash, vec3<f32>(0.0), vec3<f32>(1.0)), base.a);
}
```

The same effect with raw slots (what the accessors expand to with this manifest): `P_strength()` = `param(0u)`, `P_tint()` = `param_color(4u)`, `P_direction()` = `vec2<f32>(param(8u), param(9u))`.

Apply it twice with different looks:

```json
{ "project_id": "proj_123", "effect_id": "fx_streak", "kind": "filter", "target_layer_id": "@primary",
  "start_time": 0, "end_time": 3, "params": { "strength": 0.8, "tint": "#66ccff", "direction": [0, 1] } }
```

## ABI v3 examples

All six pass the server's real `compileShaderFx` (v3 harness + naga validator), including every pass and the geometry vertex / fragment stages.

### 7. Logo reveal: texture from a layer, light sweep + dissolve

Manifest: `{ "kind": "generator", "output": "normal", "textures": [{ "name": "logo" }], "params": [{ "name": "glow", "type": "color", "default": "#ffd27a" }] }`

Apply over the logo's window, binding the logo layer:

```json
{ "effect_id": "fx_logo_reveal", "kind": "generator", "start_time": 0, "end_time": 2.5,
  "textures": [{ "name": "logo", "layer_id": "logo_1" }], "params": { "glow": "#9fd8ff" } }
```

Hide the logo layer itself (`UPDATE_LAYER { layer_id: "logo_1", properties: { visible: false } }`): hidden layers still render into a texture, so only the shader's revealed copy shows.

```wgsl
// Diagonal light sweep + noisy dissolve that reveals the logo.
fn fx(c: FxCtx) -> vec4<f32> {
    let logo = tex_logo(c.uv);
    let t = c.progress;
    let reveal = smoothstep(0.0, 0.6, t);

    // Dissolve: fbm threshold sweeps from fully hidden to fully shown.
    let n = fbm(c.uv * 9.0) + 0.5;
    let soft = 0.06;
    let shown = smoothstep(n - soft, n + soft, reveal * (1.0 + 2.0 * soft) - soft);

    // Hot edge where the dissolve is happening.
    let edge = (1.0 - abs(shown * 2.0 - 1.0)) * step(0.001, logo.a);
    let edge_col = P_glow().rgb * edge * 1.5;

    // Light sweep: a soft diagonal band crossing the logo after the reveal.
    let aspect = c.res.x / c.res.y;
    let diag = (c.uv.x * aspect + c.uv.y) / (aspect + 1.0);
    let sweep_pos = mix(-0.2, 1.2, smoothstep(0.45, 1.0, t));
    let k = (diag - sweep_pos) / 0.05;
    let band = exp(-k * k);
    let sweep_col = P_glow().rgb * band * 0.9 * logo.a;

    let a = clamp(logo.a * shown + edge * logo.a, 0.0, 1.0);
    let rgb = logo.rgb + edge_col + sweep_col;
    return vec4<f32>(clamp(rgb, vec3<f32>(0.0), vec3<f32>(1.0)), a * c.intensity);
}
```

### 8. Motion trails / echo with feedback

Manifest: `{ "kind": "filter", "output": "normal", "feedback": { "enabled": true, "warmup_sec": 1.5 }, "params": [{ "name": "decay", "type": "float", "min": 0, "max": 0.99, "default": 0.9 }, { "name": "tint", "type": "color", "default": "#ffffff" }, { "name": "drift", "type": "vec2", "default": [0, 0] }] }`

Apply with `target_layer_id` set to a moving subject (a cut-out, a title, a product shot) so only it leaves trails. `drift` is in pixels per frame, e.g. `[0, -2]` makes the trail rise. With `decay` 0.9 a trail fades to about 4 % in 30 frames (1 s at 30 fps), so `warmup_sec` 1.5 covers it.

```wgsl
// Echo trails: the current picture over a decaying, drifting copy of the
// last output frame.
fn fx(c: FxCtx) -> vec4<f32> {
    let cur = src(c.uv);

    // Sample last frame slightly displaced so the trail drifts.
    let drift = P_drift() / c.res;
    let echo_raw = prev(c.uv - drift);
    let decay = clamp(P_decay(), 0.0, 0.99);
    let echo = vec4<f32>(echo_raw.rgb * P_tint().rgb, echo_raw.a * decay);

    // Straight-alpha "over": cur over echo.
    let a = cur.a + echo.a * (1.0 - cur.a);
    let rgb_p = cur.rgb * cur.a + echo.rgb * echo.a * (1.0 - cur.a);
    let rgb = select(vec3<f32>(0.0), rgb_p / max(a, 0.0001), a > 0.0001);
    return vec4<f32>(rgb, a);
}
```

### 9. Bloom: bright-pass (0.5) → blur (0.25) → composite

Manifest: `{ "kind": "filter", "output": "normal", "passes": [{ "name": "bright", "scale": 0.5 }, { "name": "blur", "scale": 0.25 }], "params": [{ "name": "threshold", "type": "float", "min": 0, "max": 1, "default": 0.7 }, { "name": "radius", "type": "float", "min": 0, "max": 0.05, "default": 0.012 }, { "name": "strength", "type": "float", "min": 0, "max": 2, "default": 0.8 }] }`

Three renders per frame, two of them at reduced size: about 1.3× the cost of a single full-size pass. The passes store raw values, so the bright pass keeps its exact intensity and the final pass does the only clamp.

```wgsl
// Pass "bright" (0.5 scale): keep only what is brighter than the threshold.
fn pass_bright(c: FxCtx) -> vec4<f32> {
    let s = src(c.uv);
    let l = luma(s.rgb);
    let k = smoothstep(P_threshold(), P_threshold() + 0.2, l);
    return vec4<f32>(s.rgb * k, k * s.a);
}

// Pass "blur" (0.25 scale): 5x5 Gaussian of the bright pass. Offsets are in
// uv, so the blur radius is the same whatever the buffer size.
fn pass_blur(c: FxCtx) -> vec4<f32> {
    let aspect = c.res.x / c.res.y;
    let r = vec2<f32>(P_radius() / aspect, P_radius());
    var acc = vec4<f32>(0.0);
    var wsum = 0.0;
    for (var y = -2; y <= 2; y = y + 1) {
        for (var x = -2; x <= 2; x = x + 1) {
            let o = vec2<f32>(f32(x), f32(y));
            let w = exp(-dot(o, o) / 4.5);
            acc = acc + buf_bright(c.uv + o * r * 0.5) * w;
            wsum = wsum + w;
        }
    }
    return acc / wsum;
}

// Final: the picture plus the blurred highlights (screen-style add).
fn fx(c: FxCtx) -> vec4<f32> {
    let base = src(c.uv);
    let bloom = buf_blur(c.uv).rgb * P_strength() * c.intensity;
    let rgb = 1.0 - (1.0 - base.rgb) * (1.0 - clamp(bloom, vec3<f32>(0.0), vec3<f32>(1.0)));
    return vec4<f32>(rgb, base.a);
}
```

### 10. Data-driven bar chart from `data`

Manifest: `{ "kind": "generator", "output": "normal", "params": [{ "name": "max_value", "type": "float", "default": 100 }, { "name": "color", "type": "color", "default": "#4cc9f0" }] }`

```json
{ "effect_id": "fx_bars", "kind": "generator", "start_time": 3, "end_time": 8,
  "data": [42, 67, 88, 51, 95, 73], "params": { "max_value": 100, "color": "#f72585" } }
```

Or `"data_url": "https://…/q3.csv", "data_columns": ["revenue"]` to read one CSV column at apply time. The bar count is `data_len()`. Each pixel works out the one bar it can belong to, so there is no per-bar loop. Bars grow with `local_time`, each starting 0.08 s after the previous one. Add labels and values as `TITLE_CARD` / text layers above it.

```wgsl
// Signed distance to a rounded box (centre p, half-size b, corner radius r).
fn sd_round_box(p: vec2<f32>, b: vec2<f32>, r: f32) -> f32 {
    let q = abs(p) - b + vec2<f32>(r, r);
    return length(max(q, vec2<f32>(0.0))) + min(max(q.x, q.y), 0.0) - r;
}

fn fx(c: FxCtx) -> vec4<f32> {
    let n = data_len();
    if (n == 0u) {
        return vec4<f32>(0.0);
    }
    let aspect = c.res.x / c.res.y;
    // Chart area in uv: x 0.1..0.9, baseline at y 0.85, max height 0.6.
    let x0 = 0.1;
    let width = 0.8;
    let base_y = 0.85;
    let max_h = 0.6;
    let slot = width / f32(n);

    // The one bar this pixel can belong to.
    let fi = clamp(floor((c.uv.x - x0) / slot), 0.0, f32(n - 1u));
    let i = u32(fi);
    let value = clamp(data(i) / max(P_max_value(), 0.0001), 0.0, 1.0);

    // Staggered growth: bar i starts 0.08 s after bar i-1, grows over 0.7 s.
    let t = clamp((c.local_time - fi * 0.08) / 0.7, 0.0, 1.0);
    let grow = 1.0 - pow(1.0 - t, 3.0);
    let h = max(value * max_h * grow, 0.002);

    // Work in aspect-corrected space so the corner radius stays round.
    let centre = vec2<f32>(x0 + (fi + 0.5) * slot, base_y - h * 0.5);
    let half = vec2<f32>(slot * 0.35, h * 0.5);
    let p = vec2<f32>((c.uv.x - centre.x) * aspect, c.uv.y - centre.y);
    let d = sd_round_box(p, vec2<f32>(half.x * aspect, half.y), min(0.012, half.x * aspect));

    let aa = 1.5 / c.res.y;
    let fill = 1.0 - smoothstep(-aa, aa, d);
    // Lighter top edge for depth.
    let top = smoothstep(centre.y - half.y + 0.02, centre.y - half.y, c.uv.y);
    let col = mix(P_color().rgb, min(P_color().rgb * 1.35, vec3<f32>(1.0)), top);
    return vec4<f32>(col, fill * P_color().a * c.intensity);
}
```

### 11. Particle fountain: geometry quads, closed-form motion

Manifest: `{ "kind": "generator", "output": "add", "geometry": { "mode": "quads", "count": 1500 } }`. No `shade`: the default soft round point × `color` is used. Every particle is a pure function of its index and time (seek-safe, no feedback). Size and colour change over each particle's life, and particles stay hidden (`alive = 0`) until their first birth.

```wgsl
// Closed-form particle fountain: every particle's state is a pure function of
// its index and time, so any frame renders correctly on its own (seek-safe).
fn instance(i: u32, c: FxCtx) -> FxInstance {
    var o: FxInstance;
    let fi = f32(i);
    let seed = hash2(vec2<f32>(fi, 3.7));
    let seed2 = hash2(vec2<f32>(fi, 11.3));
    let seed3 = hash2(vec2<f32>(fi, 29.1));

    let lifetime = mix(1.4, 2.6, seed2);
    let born = seed * lifetime;                 // spread first births over one lifetime
    let since = c.local_time - born;
    let age_sec = since - floor(since / lifetime) * lifetime;   // repeats every lifetime
    let age = age_sec / lifetime;               // 0..1 over the particle's life

    // Launch from the bottom centre with an upward cone, then gravity.
    let aspect = c.res.x / c.res.y;
    let angle = (seed3 - 0.5) * 0.9;
    let speed = mix(0.55, 0.95, seed2);
    let vel = vec2<f32>(sin(angle) * speed / aspect, -cos(angle) * speed);
    let gravity = vec2<f32>(0.0, 0.7);
    let origin = vec2<f32>(0.5, 0.92);

    o.pos = origin + vel * age_sec + 0.5 * gravity * age_sec * age_sec;
    let scale = c.res.y / 1080.0;
    o.size = vec2<f32>(mix(22.0, 3.0, age) * scale);
    o.rotation = 0.0;
    // Colour over life: hot yellow -> orange -> deep red, fading out.
    let warm = mix(vec3<f32>(1.0, 0.9, 0.5), vec3<f32>(1.0, 0.45, 0.1), smoothstep(0.0, 0.5, age));
    let col = mix(warm, vec3<f32>(0.6, 0.05, 0.02), smoothstep(0.5, 1.0, age));
    o.color = vec4<f32>(col, (1.0 - age) * c.intensity);
    o.uv_rect = vec4<f32>(0.0, 0.0, 1.0, 1.0);
    o.alive = select(0.0, 1.0, since >= 0.0);
    return o;
}
```

### 12. Sprite-sheet animation: geometry quads + `asset_url` texture

Manifest: `{ "kind": "generator", "output": "normal", "geometry": { "mode": "quads", "count": 6 }, "textures": [{ "name": "sheet" }], "params": [{ "name": "fps", "type": "float", "min": 1, "max": 60, "default": 12 }] }`

```json
{ "effect_id": "fx_walkers", "kind": "generator", "start_time": 0, "end_time": 6,
  "textures": [{ "name": "sheet", "asset_url": "https://example.com/walk_4x2.png" }] }
```

The sheet is 4 columns × 2 rows, read top-left first. An `asset_url` texture is in image space, so `uv_rect` selects a cell in 0..1 of the sheet. The explicit `shade` below matches the default for a bound texture; replace it to add outlines, flashes or palette swaps.

```wgsl
// A row of characters walking across the frame, each playing an 8-frame
// walk cycle from a 4 x 2 sprite sheet, offset so they are out of step.
const COLS: u32 = 4u;
const ROWS: u32 = 2u;
const FRAMES: u32 = 8u;

fn instance(i: u32, c: FxCtx) -> FxInstance {
    var o: FxInstance;
    let fi = f32(i);
    let count = 6.0;

    // Walk left to right, wrapping, spaced evenly.
    let speed = 0.12;
    let x = fract(fi / count + c.local_time * speed) * 1.2 - 0.1;
    o.pos = vec2<f32>(x, 0.78 + 0.01 * sin(fi * 2.3));
    let px = 220.0 * (c.res.y / 1080.0);
    o.size = vec2<f32>(px, px);
    o.rotation = 0.0;
    o.color = vec4<f32>(1.0, 1.0, 1.0, c.intensity);

    // Sprite frame: steps at P_fps(), each instance offset by its index.
    let frame = (u32(max(c.local_time, 0.0) * P_fps()) + i * 3u) % FRAMES;
    let col = f32(frame % COLS);
    let row = f32(frame / COLS);
    o.uv_rect = vec4<f32>(col / f32(COLS), row / f32(ROWS), 1.0 / f32(COLS), 1.0 / f32(ROWS));
    o.alive = 1.0;
    return o;
}

// What the default shade does when a texture is bound, written out:
// sample the sheet through uv_rect and tint by the instance colour.
fn shade(p: FxPixel, c: FxCtx) -> vec4<f32> {
    let s = tex_sheet(p.uv_rect.xy + p.local_uv * p.uv_rect.zw);
    return vec4<f32>(s.rgb * p.color.rgb, s.a * p.color.a);
}
```

## Quality checklist

- Every frame of the window looks right in `render_preview`, not just the middle one. For transitions check progress 0, 0.5 and 1: the ends must match clip A and clip B exactly.
- Strength scales with `c.intensity`, so the effect can be dialled down without editing source.
- Round things are aspect-corrected; the effect looks the same in 9:16 and 16:9.
- Filters that rewrite a layer return `src(uv).a`; only full-frame work uses `replace`.
- Light-only looks use `add`; anything that darkens uses `normal` with alpha.
- Motion uses the layer clock (`c.time` = `c.local_time`, 0 when the effect layer starts) or `c.progress`; to stay in sync with something on the timeline, place the layer so its start lines up.
- Detail sizes (grain, noise scale) come from `uv`, not `px`: `res` is the render-target size and is larger on a supersampled export.
- To animate a param over time, use `param_keyframes` rather than hard-coding time curves in the shader, so the same effect stays reusable.
- v3: feedback trails look the same in `render_preview` and export only if `warmup_sec` covers the trail length; particle and sprite sizes scale with `c.res.y / 1080.0`; pass offsets are in uv.
