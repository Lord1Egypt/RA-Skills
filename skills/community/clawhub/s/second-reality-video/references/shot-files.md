# Shot files (ShotGraph)

A shot file says **where the camera looks**, never **what the world does**. That is the whole
point of the `no_scripted_plot` audit dimension: once a plot is written into the shot file, the film
is no longer something the world produced.

## Structure

```yaml
shots:
  - id: wide-static
    tick_from: 0
    tick_to: 300
    camera:
      mode: static          # follow | orbit | static | aoi
      origin: [0.0, 0.0]
      zoom: 3.0
    framing:
      aspect: "16:9"
      resolution: [1280, 720]
      fps: 30
    tier: R1
    overlay:
      hud: false
      state_panel: false
      caption_from: none
```

| Field | Required | Meaning |
|---|---|---|
| `id` | yes | shot identifier |
| `tick_from` / `tick_to` | yes | covered tick range (inclusive) |
| `camera.mode` | yes | `follow` / `orbit` / `static` / `aoi` |
| `camera.origin` | mode-dependent | static camera position |
| `camera.target_soul` | mode-dependent | follow/orbit target (`auto` = the engine picks) |
| `camera.period_ticks` | mode-dependent | orbit period |
| `camera.zoom` / `camera.fov` / `camera.height` | no | framing parameters |
| `framing.resolution` | no | must be identical across all shots (a rawvideo stream carries one pixel format) |
| `framing.fps` | no | must be an integer multiple of 10 |
| `tier` | no | `R1` (CPU-only offscreen rendering) |
| `overlay` | no | HUD / state panel / caption source |

## Forbidden fields

These keys are rejected **at any nesting depth**:

```text
action, set_needs, move_agent, force_event, spawn, kill, teleport, script, dialogue
```

A top-level-only check is not enough — `camera.action` or `overlay.script` would slip through, so
validation is recursive. A hit produces:

```text
Shot 0 contains forbidden field 'camera.action' (violates no_scripted_plot audit dimension)
```

## Hard constraints

1. **The world directory must be empty.** World storage is stateful: reusing a populated directory
   makes the second run read already-registered souls and changes every `content_digest`. A
   conforming service creates a fresh `world/` subdirectory per job.
2. **Render in one continuous pass.** Do not stitch segments with ffmpeg's concat demuxer — the seam
   is exactly what segmentation creates.
3. **Frame count**: `frames = (tick_to - tick_from + 1) * (fps / 10)`. The time base is fixed at
   10 ticks per second, so `--ticks 0-899` at `fps=30` is 2700 frames = 90.0 s. Values such as
   24 / 25 / 29.97 are rejected, because the frame sequence could not be recovered from the ticks
   unambiguously.
4. **One resolution for the whole film.**
