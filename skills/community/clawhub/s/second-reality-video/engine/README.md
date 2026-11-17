# second-reality-video

> A deterministic video pipeline. Persistent world state becomes film; the camera picks framing, never story: `frame = render(state, shot)`. Same seed and shots give byte-identical pixels anyone can recompute.

Projects a persistent world's state into video, without ever letting the director script what happens.

## Why it exists

Most "AI video" is unrepeatable: run it twice, get two different films. This pipeline takes the opposite stance. The world evolves under its own rules, the camera only decides *where to look*, and the finished frames can be recomputed byte-for-byte by a third party who trusts nothing but the source.

## Design

- **The world drives; the camera only observes.** A shot file chooses position, target and zoom — never events.
- **Deterministic by construction.** Same `(world_id, genesis_seed, agent_count, tick range, shot file, renderer source)` yields a byte-identical state layer and pixel layer. No wall-clock reads, no unordered dict iteration, no `random` module, no write-back into world state.
- **Independently verifiable.** `attest` rebuilds the world from genesis, runs a real 25-dimension constitutional audit, and Ed25519-signs a `RenderManifest`. `verify` lets anyone recompute and compare.

## What it guarantees

| Layer | Anchor | Nature |
|---|---|---|
| State | `content_digest` sequence | Deterministic, byte-verifiable |
| Structure | `scene_ir_digest` | Deterministic, byte-verifiable (entities / identity / camera) |
| Pixels (R1) | per-frame `sha256` | Deterministic, byte-verifiable |
| Container | `world.mp4` sha256 | **Corroborative only** — not stable across ffmpeg versions |
| Pixels (R2) | weights / sampling seed / hardware | Not implemented (Phase 2) |
| Render contract | `render_is_frame_independent` | Deterministic — static check, **FAIL level**: the render layer takes a single-frame IR and never a cross-frame context |

## Quick start

```bash
pip install pygame pyyaml cryptography     # ffmpeg must be on PATH
ffmpeg -version                            # missing ffmpeg is rejected up front

# 1) extract world state -- --world must point at an EMPTY directory
python -m video.cli extract \
    --world-id sr-video-demo --world .tmp_world \
    --seed 42 --agents 10 --ticks 0-899 \
    --out out/states.jsonl

# 1.5) compile to Scene IR + structural audit (no pixels, no ffmpeg)
python -m video.cli scene \
    --state out/states.jsonl --shot video/shots/demo.yaml \
    --out out/scene_ir.jsonl --report out/structure_report.txt

# 1.6) optional: freeze appearance assets as hashed constants (Tier 2 asset bake)
python -m video.cli bake-assets --state out/states.jsonl --out-dir out/baked_assets

# 2) render + encode, piped straight to ffmpeg as rawvideo
python -m video.cli render \
    --state out/states.jsonl --shot video/shots/demo.yaml \
    --tier R1 --samples 3 --out out/world.mp4

# 2b) same thing with live captions read from the ledger event stream
#     (overlay.caption_from: ledger) — see video/shots/demo_captioned.yaml
python -m video.cli render \
    --state out/states.jsonl --shot video/shots/demo_captioned.yaml \
    --tier R1 --samples 3 --out out/world_captioned.mp4

# 3) attest -- real 25-dimension audit + Ed25519 signature
python -m video.cli attest \
    --video out/world.mp4 --hashes out/hashes.txt \
    --state out/states.jsonl --shot video/shots/demo.yaml \
    --manifest out/manifest.json

# 4) verify -- independent recomputation (for you and for third parties)
python -m video.cli verify \
    --manifest out/manifest.json --hashes out/hashes.txt \
    --shot video/shots/demo.yaml --frames out/rerender.mp4
```

**Timing.** `tps` is fixed at 10; `fps` must be an integer multiple of it.

```
frames = (tick_to - tick_from + 1) * (fps / tps)
```

So `--ticks 0-899` at `fps=30` = 2700 frames = 90.0 s. Values such as 24 / 25 / 29.97 are rejected outright.

## Hard constraints

- **The world store directory must be empty.** World storage is stateful; reusing a populated directory makes the second run read already-registered souls, and every `content_digest` changes.
- **Render in one continuous pass.** Never stitch segments with ffmpeg's concat demuxer — the seam is exactly what segmentation creates.
- **Shot files cannot contain plot instructions.** Fields such as `action`, `set_needs`, `move_agent`, `force_event`, `spawn`, `kill`, `teleport`, `script` and `dialogue` are rejected at any nesting depth.

## Outputs

| File | Produced by | Contents |
|---|---|---|
| `states.jsonl` | `extract` | one `FrameState` per tick |
| `scene_ir.jsonl` | `scene` | one Scene IR per tick (entities / identity hash / camera / framing) |
| `structure_report.txt` | `scene` | structural PASS/FAIL: duplicate ids, illegal camera, identity drift, motion outliers |
| `baked_assets.json` | `bake-assets` | frozen appearance assets (hashed constants) |
| `baked_assets.manifest.json` | `bake-assets` | per-asset sha256 + collection digest |
| `world.mp4` | `render` | H.264 film |
| `hashes.txt` | `render` | per-frame sha256, one line per frame |
| `frames.jsonl` | `render` | per-frame backing record |
| `identity_assets.json` | `render` | `soul_hash` → appearance asset evidence |
| `sample_NNNNN.png` | `render` | sampled frames spread across the film |
| `manifest.json` | `attest` | signed reproducibility anchor + boundary declarations |
| `audit_report.txt` | `attest` | per-dimension audit verdicts |

## Requirements

Python 3.8+, with `pygame` (R1 offscreen rendering), `pyyaml` (shot files), `cryptography` (Ed25519). `ffmpeg` on `PATH`. **No GPU** — R1 is pure CPU.

## Zero-cost, offline rendering

The whole `extract → render → attest → verify` pipeline runs on your own CPU. **No model is called, so nothing is billed per frame, per second, or per token.**

| You don't need | Because |
|---|---|
| A model API key | The renderer is plain code — `pygame` offscreen + local `ffmpeg` |
| A GPU | Pure CPU rasterization (`SDL_VIDEODRIVER=dummy`) |
| A network | `smoke_video.py` passes byte-for-byte with the socket layer disabled |
| Paid credits | No inference, no metering — the cost is your own CPU time |

The `system/` engine ships an optional `OpenAIProvider`, but it is never wired up: `llm_provider` defaults to `None`, `set_llm_provider()` has no call site, and the LLM path is inert. R2 (neural rendering) is not implemented — today there is no code path in this repository that can consume credits.

**Free is not the only thing you keep.** Off-the-shelf tools can compose frames too. What they cannot hand you is a signed manifest proving the pixels came from the world state: `frame_hashes_digest` is recomputable by a third party from source alone.

**Where the ceiling is.** R1 draws isometric geometry and state-driven bars — not photographic faces, real scenery, or cinematic lighting. *Composition is not generation*: this pipeline saves the orchestration and the audit trail, not pixels it cannot synthesize. For photoreal work you need your own footage or a model — and the moment a model enters the frame, credits come back.

Measured on one CPU: ~54 frames/s of rendering; a 90-second film (2700 frames) costs ~74 s of extract + render combined.

## What you can actually make with it

### The tiers

| Tier | How | What it looks like | Reproducibility | Cost |
|---|---|---|---|---|
| **0 — R1 today** | local `pygame` + `ffmpeg`, no model | A *world dashboard you can watch*: coloured rectangles are souls, ellipses are shadows, the bar on top is a need value, the diamond is the world | Byte-for-byte, plus a signed 25-dimension audit | Zero credits, ~54 frames/s on CPU |
| **1 — R1 + asset pack** | Swap `pygame` for three.js headless / Blender / Remotion; add buildings, terrain, character models; 4K | Stylised low-poly 3D. Still not photographic, but presentable | **Byte-for-byte, unchanged** — swapping the renderer does not touch the determinism contract | Same as Tier 0 |
| **2 — a model as the asset source** | Bulk-generate sprites, textures and portraits with a closed model; hash them into the repository; R1 keeps rendering | Model-grade art, style-consistent | **Byte-for-byte** — assets become constants, so the pixels stay reproducible | One-off generation, plus a human re-bake per asset update |
| **3 — a frame renderer (R2, no temporal context)** | Train a small **per-frame** renderer on R1's `(scene_ir, frame)` pairs — no temporal attention, no `prev_frames`, no cross-frame state | Photoreal, cinematic, and temporally consistent **by construction** | State + structure byte-for-byte; pixel layer *reproducible in the same environment* (`weights_sha256` + seed + hardware) | GPU training + per-frame inference (2700 frames × 1–5 s) |
| **4 — a model as promotional material** | Straight from the model, off the pipeline | Film-grade | **None** — and it never enters the reproducibility chain | Per-generation credits |

**A video model is deliberately absent from this ladder.** It cannot be the render layer: it takes prompts instead of `(state, shot)`, and silent platform upgrades would invalidate the reproduction anchor. It belongs at Tier 2 (asset source) or Tier 4 (promotional material) — see [HLD §4.6](video/HLD-SecondRealityVideo-20261015.md).

**Tier 2 is the recommended path.** Phase 1's real bottleneck is assets and the renderer, not R2: an art-grade pipeline that keeps the byte-for-byte anchor is worth more than a photoreal pipeline that trades it away. Tier 3 is a research-grade project — see [`video/HLD-SecondRealityVideo-20261015.md`](video/HLD-SecondRealityVideo-20261015.md) §4.

A closed model can **never** be the render layer: it takes prompts instead of `(state, shot)`, and silent platform upgrades would invalidate `frame_hashes_digest`.

### Tier 0 in detail — be honest about it

| | |
|---|---|
| Look | Flat green diamond, no buildings, no terrain, no textures, no lighting |
| Scene | 60×60 world; `static` / `follow` / `orbit` / `aoi` cameras, adjustable zoom |
| Identity | One deterministic colour per soul (`palette[0]`) — `ref_images` and the 16-dim `embedding` are **not read by the renderer** |
| Behaviour | **Decision-driven**: the need that is most deficient picks an action, the action picks a target point, and the agent walks there. Measured `cos(step, target) ≈ 0.98` — movement is not a random walk |
| Social | `relationships` records who each soul actually interacted with, and how strongly; belonging is only restored by real proximity, never by self-scoring |
| Overlays | `caption_from: ledger` **is implemented** — captions are generated live from the ledger event stream (built-in 5×7 bitmap font, no external font file). `hud` / `state_panel` are still declared-but-not-drawn |
| Resolution | 720p verified; 4K needs Phase 1 |

Treat it as evidence, not as footage.

### Where the value actually is

Four capabilities that have nothing to do with how pretty the frame is:

1. **The picture is projected, not generated.** Same state + same shot = same pixels, and anyone can recompute them from source alone.
2. **The behaviour is caused, not animated.** A soul's most deficient need selects an action; the action selects a target point; the agent walks to it and stays there until the goal completes. Personality — derived deterministically from `soul_hash + genesis_seed` — tilts which need wins near-ties, so no two souls behave alike.
3. **It cannot be staged.** `no_scripted_plot` rejects `action` / `set_needs` / `move_agent` / `force_event` / `spawn` / `kill` / `teleport` / `script` / `dialogue` at any nesting depth. You cannot fake a world to look better — what you film is what happened.
4. **The film carries a credential.** A real 25-dimension constitutional audit, an Ed25519 signature, and a manifest a third party can check independently.
5. **It is an unlimited, annotated dataset — and the teacher.** R1 emits perfectly paired `(Scene IR, frame)` samples at zero credit cost (~54 frames/s on CPU): the teaching signal for the no-temporal frame renderer of Tier 3.

### The hard line

- **Composition is not generation.** R1 cannot draw a photographic face, real scenery or cinematic light. It saves the orchestration and the audit trail, not pixels it cannot synthesise.
- **The moment a model enters the frame, credits come back.** "Zero-cost" covers only the part that uses no model.
- **A video model can never be the render layer.** It takes prompts, not `(state, shot)`, and version drift breaks the anchor — a drifting anchor is worse than no anchor. The render layer must be a **frame renderer**: single-frame input, no cross-frame state.
- **The schema promises more than the code delivers.** `hud` / `state_panel`, `ref_images` and `embedding` are not wired up — do not promise them externally.
- **A drifting anchor is worse than no anchor.** That is the whole reason a closed model stays out of the render layer.

**In one line:** this is not a video generator. It is a reproducible, auditable projector from world state to picture — decide which tier you are buying before you promise anyone a frame.

## Documentation

- [`video/HLD-SecondRealityVideo-20261015.md`](video/HLD-SecondRealityVideo-20261015.md) — design rationale
- [`video/MANUAL-SecondRealityVideo-20261016.md`](video/MANUAL-SecondRealityVideo-20261016.md) — operator manual

This repository is not open source. Dual-track model: free for personal non-commercial research; paid commercial license required for government / enterprise use. Contact: ai@nohnlins.com (international) / lin@secondai.top (China).
