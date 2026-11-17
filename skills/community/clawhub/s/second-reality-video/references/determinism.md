# The boundary of determinism

Three categories, stated separately because they are not equally strong. Do not present a
corroboration as a guarantee.

## Guaranteed byte-verifiable

| Layer | Anchor | Note |
|---|---|---|
| World state | `content_digest` sequence | one digest per tick; equal sequences mean equal states |
| Pixels (R1) | per-frame `sha256` in `hashes.txt` | equal hash sequences mean equal pixels |
| Identity | `identity_assets.json` (`soul_hash` → appearance asset) | the auditable evidence behind the "identity constancy" dimension |
| Attestation | Ed25519 signature in `manifest.json` | binds genesis parameters, state digests and renderer provenance together |

The same `(world_id, genesis_seed, agent_count, tick range, shot file, renderer source)` yields the
same state layer and the same pixel layer — provided the genesis directory is empty, the render is a
single pass, and the ffmpeg build and renderer source are unchanged.

## Corroborative only

| Anchor | Why it is weaker |
|---|---|
| `world.mp4` sha256 | H.264 containers are not bit-stable across ffmpeg builds; the same frames can produce different bytes |
| `state_root` | embeds an HLC wall-clock timestamp — auxiliary information only, never a reproduction criterion |

**Identical container hashes do not mean the film is reproducible.** The frame hashes are the anchor.

## Not implemented

- **R2 pixel layer** (model weights / sampling seed / hardware-dependent rendering).
- Any generative rendering path other than R1.

## How verification works

`manifest.json` records every genesis parameter, so a third party who trusts nothing but the source
can:

1. rebuild the world from those parameters → obtain the `content_digest` sequence;
2. compare it with `content_digest_start` / `content_digest_end`;
3. re-render from the same shot file → obtain per-frame sha256 values;
4. compare them line by line with `hashes.txt` (or compare `frame_hashes_digest`);
5. verify the manifest's Ed25519 signature.

A conforming service exposes this as the `verify` tier (`mode=verify` → `verify_report.txt`); the
same check can also be run entirely locally.

## The audit

Every attestation runs a **real** 25-dimension constitutional audit — not a pre-computed verdict.
The per-dimension results land in `audit_report.txt`, and the dimension count plus the overall
verdict are written into the manifest. The audit judges what the world *did* in that interval, not
how the film looks.

## Time base

`tps` is fixed at 10 and `fps` must be an integer multiple of it:

```text
frames = (tick_to - tick_from + 1) * (fps / tps)
```
