# The traps that cost the most, and the fix for each

Ordered by how much time they have actually taken, not by how exotic they are.

## 1. The GPU is a single resource and something else is holding it

A Unity editor, a local LLM engine, and a diffusion/video renderer all want the same card. On one 8 GB
card, a loaded local model left **719 MiB free of 8188 MiB VRAM** - and separately, with a video engine
holding **5,232 MB loaded**, the same machine's LLM could not load at all (`brain: booting` for 15+
minutes, turns hanging with no reply). Both directions happen.

**Fix:** know what holds the card *before* starting heavy work (`nvidia-smi`), and ask the operator
before pausing anything - suspending another program is their call, not the agent's. With their
agreement: park -> work -> wake, with the wake in a `finally` so a failure never leaves the machine dark. If a turn hangs with no output, check the GPU before you
check your own code.

## 2. Slow work outlives the tool call that started it

A WebGL build (~8-12 min), an editor import of a large library, and a multi-gigabyte download all
outlive a normal call ceiling. A killed build leaves a half-written output folder and `exitCode: 143`
in `unity-build.provenance.json`; a killed download leaves a partial tree.

**Fix:** run them as tracked background processes and poll for evidence - the log file, the output
folder, growing artifact directories. Re-run only when nothing is growing; relaunching a live job races
the first copy. Never conclude failure from one early read.

## 3. A timeout wrapper on a build

Wrapping the build in a shell `timeout` (or a call ceiling) kills it mid-compile and produces the
half-written state above.

**Fix:** no timeout around the build. The build's own `--log-file` plus the output directory is how you
know what happened.

## 4. `git add -A` in a shared repo

A game repo usually shares a working tree with other projects or a live site. A blanket add sweeps
unrelated dirty files into the push, and that push is often the one that publishes.

**Fix:** commit the named paths the build touched (`Build/*`, the page, the specific art). Review the
diff before committing.

## 5. The DoNotShip folder

Unity writes `<Game>_BurstDebugInformation_DoNotShip/` into the build output. Its name is the
instruction and it bloats the repo.

**Fix:** delete it as a build step, every build.

## 6. A deformed imported mesh

An FBX/GLB model can import with bad scale, flipped or missing normals, or shape keys that visibly
deform the body. It loads, it looks wrong, and it never behaves - a car with deformations will never
drive no matter how the controller is tuned.

**Fix:** verify the mesh before wiring anything to it (dimensions, bounds, normals). If the mesh is
deformed, fix or replace the asset; do not tune physics around a broken source.

## 7. Torn sprites and misunderstood rects

A cutout that draws as a fragment usually has a sprite rect that does not cover its texture, or a source
file that is genuinely torn. Unity's sprite origin is the bottom-left of the texture;
`SpriteMeshType.FullRect` is `0` and `Tight` is `1`.

**Fix:** make the rect cover the whole texture, leave mesh type at `0` for full cutouts, and confirm the
alpha: a vision model will call a torn texture a complete object, so fill the empty alpha with a flat
colour and look.

## 8. A vision model's description is not proof

Descriptions of generated or imported images are frequently wrong about edges, transparency and
orientation. Building on the description ships the error.

**Fix:** measure pixels - opaque bounds, dimensions, alpha preview.

## 9. WebGL shader footguns

`pow()` can return NaN on a WebGL build, and a shader is stripped from the player unless a material
asset references it, so `Shader.Find` on an unreferenced shader will not save it.

**Fix:** write `x * x` instead of `pow()`; ship the `.mat` with the `.shader`.

## 10. The page that eats its own chrome

A deploy that copies Unity's template over the site's page re-applies chrome that was already there, or
destroys it; a canvas centred with both `top: 50%` and `translate(-50%,-50%)` shows only a strip if you
override one and not the other.

**Fix:** sync `Build/*` only, and treat the page as the site's file - see `references/webgl-shipping.md`.

## 11. A deploy judged too early

CDN lag has been one to three minutes, with different edges disagreeing in between.

**Fix:** poll the served document for a changed marker and compare the served wasm's byte size with the
local build before concluding anything.

## 12. Reporting a number that was never counted

"Imported as many assets as possible" and "downloaded the library" are claims that get checked.

**Fix:** count files on disk per category and report those numbers; name the gaps (audio and fonts are
the classic missing category in a model-only library).

## 13. A second copy of the method

Pasting a style guide or a method log into the project repo guarantees drift: two files claiming to be
current, neither authoritative.

**Fix:** one home per method. The project points at it; the project does not contain a copy.

## 14. Editing a live site to change a look

A look lives in the view layer and the art. Changing the shipped site to fix a picture puts presentation
work into the deploy path.

**Fix:** change the project, rebuild, re-ship. Do not hand-edit the live output.
