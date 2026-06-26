---
name: splat-transform-workflow-for-lcc
description: Use when converting XGRIDS/其域 `.lcc` or PLY Gaussian splat scenes for SuperSplat, producing streamed LOD, SOG, voxel collision data, merging viewer settings, mounting local routes, or explaining LCC/SuperSplat workflow concepts to Chinese or English users.
---

# Splat Transform Workflow for LCC / LCC 转 SuperSplat 工作流

Use this skill for LCC/PLY to SuperSplat conversion work. It explains the formats, chooses precision-preserving defaults, and uses the bundled scripts instead of retyping fragile `splat-transform` commands by hand.

本 skill 用于把 LCC 或 PLY 高斯泼溅场景转换成 SuperSplat 可加载的网页资产。它不仅记录命令，还解释每种格式的价值、坐标差异和默认参数，避免因为 1.9.x/2.x 行为变化导致场景转歪、精度降低或体素碰撞错位。

## Language Policy / 多语言规则

- If the user writes in Chinese, answer in Chinese and keep command flags, file names, JSON keys, and format names in English.
- If the user writes in English, answer in English and optionally add short Chinese labels for domain terms when helpful.
- Preserve exact technical names: `LCC`, `SuperSplat`, `SOG`, `PLY`, `streamed LOD`, `voxel`, `splat-transform`.
- When introducing a format for a new user, explain both what it is and why it matters before giving commands.

## Value / 作用和价值

This workflow turns trained or vendor-delivered Gaussian splat scenes into deployable SuperSplat viewer assets. It handles three practical problems that raw conversion commands do not solve by themselves:

- Precision: use original PLY for high-quality SOG and voxel output when available, because PLY usually preserves float32 training attributes while LCC may already be compressed or quantized.
- Delivery: use LCC for true streamed multi-LOD output when the web viewer needs progressive loading.
- Alignment: apply different rotations for PLY, LCC 1.9.2, and LCC 2.x so visual content and walkable voxel collision stay in the same space.

这个工作流的价值是把“能转换”变成“可稳定上线”：SOG 用于高质量显示，streamed LOD 用于大场景渐进加载，voxel 用于行走/碰撞，settings 用于保留 viewer 配置。skill 会帮用户判断应该从 PLY 还是 LCC 生成对应资产，并解释为什么。

## Glossary / 名词解释

| Term | 中文解释 | What it means / Why it matters |
| --- | --- | --- |
| Gaussian splat / 3DGS | 三维高斯泼溅 | A scene representation made of many anisotropic Gaussian points. It is not a mesh; visual quality depends on attributes such as position, scale, rotation, opacity, color, and SH coefficients. |
| PLY | 原始训练点云/高斯属性文件 | Usually the highest-precision source produced by training. Prefer PLY for `scene.sog` and voxel generation when available. |
| LCC | XGRIDS/其域场景容器 | A vendor scene package used here as the source for true streamed LOD. It can include multiple LOD levels and environment data, but may already contain compressed or quantized attributes. |
| SuperSplat | PlayCanvas 的高斯泼溅编辑器/查看器生态 | The target viewer/editor ecosystem. It can load SOG, streamed LOD metadata, settings JSON, and this repo's voxel route integration. |
| `splat-transform` | 转换命令行工具 | Converts between PLY/LCC/SOG/LOD/voxel formats. This repo keeps both 1.9.2 and 2.1.1 because LCC coordinate handling and voxel flags changed. |
| SOG | Super-compressed Gaussian splat | A compact SuperSplat asset, commonly emitted as `scene.sog` or an unbundled `meta.json` plus binary chunks. Good for high-quality single-asset display. |
| streamed LOD | 流式多层级加载 | Output centered on `lod-meta.json`. It lets large scenes load progressively by LOD/chunks. Use LCC as the default source for real multi-LOD streamed output. |
| voxel / voxel collision | 体素碰撞数据 | Sparse voxel data, usually `walk.voxel.json` plus `walk.voxel.bin`, used by the viewer for walking and collision. It is not the visual splat itself. |
| settings JSON | viewer 配置文件 | SuperSplat viewer settings: camera, background, annotations, tonemapping, post effects, content paths, and optional voxel paths. |
| LOD0 | 最精细主层级 | The finest main LOD in legacy LCC workflows. It is often used as the LCC voxel source when reproducing older output. |
| environment layer | 环境层 | Optional sky/background/environment splat data inside LCC streamed output. Keep it unless the user explicitly asks to remove it. |
| baked rotation | 烘焙外参 | Rotation applied during conversion so the emitted asset is already aligned. Do not add viewer-side `voxelRotation` when voxel rotation is baked. |
| `meta.json.version` | 输出格式版本 | `meta.json.version: 2` describes the SOG/LOD data format, not the installed `splat-transform` CLI version. |

## When to Use / 什么时候用

Use this skill when a user needs to:

- Convert `.lcc` into true streamed LOD output for SuperSplat.
- Generate high-precision `scene.sog` from original PLY.
- Generate `walk.voxel.json` and `walk.voxel.bin` from original PLY.
- Merge a simple `settings.json` with a version 2 settings JSON.
- Mount streamed LOD, SOG, and voxel files into `supersplat-viewer/public/<scene>`.
- Explain why PLY, LCC, SOG, streamed LOD, and voxel outputs are different.
- Reuse this workflow from a repo-local Codex skill or a top-level `skills/` directory.

## Coordinate-Space Rules / 坐标规则

- PLY, SOG, SPZ, KSplat, and splat inputs are PLY-space sources.
- In `splat-transform` 2.x, LCC is read with an internal source transform of `90,0,180`; do not blindly add the old LCC `90,0,0` rotation on top of it.
- PLY did not receive that LCC-specific reader correction. In this workflow, `splat-transform` 2.x PLY -> SOG and PLY -> streamed LOD use baked `-r -90,0,0`.
- For `splat-transform` 2.x LCC -> voxel, the empirically aligned single conversion rotation is `-r 0,0,180`. Do not infer this by multiplying only the explicit query rotations: the viewer's unrotated voxel path and explicit `voxelRotation=0,0,0` path differ because the viewer has a default content rotation of `0,0,180`.
- `meta.json.version: 2` is the output data format version, not the `splat-transform` CLI version.
- Per-file transforms must come after the input file:

```bash
splat-transform input.ply -r -90,0,0 -t 0,0,0 output.sog
```

## Preferred Defaults / 推荐默认策略

- `--splat-transform`: repo-local `splat-transform-2.1.1/` when available, unless `SPLAT_TRANSFORM_DIR` or an explicit flag overrides it.
- Prefer GPU. Run `splat-transform --list-gpus` first when possible, then pass `-g 0` for the first GPU adapter. Use `-g cpu` only when GPU enumeration or GPU conversion fails.
- Streamed source: LCC for true multi-LOD streamed output.
- SOG source: original PLY when available.
- Voxel source: original PLY when available.
- `--stream-rotation auto`: LCC on 2.x uses no extra `-r`; PLY on 2.x uses `-90,0,0`; legacy LCC and PLY use `90,0,0`.
- `--sog-rotation auto`: PLY on 2.x uses `-90,0,0`; LCC on 2.x uses no extra `-r`; legacy PLY uses `90,0,0`.
- `--voxel-rotation auto`: PLY on 2.x uses `-90,0,180`; LCC on 2.x uses `0,0,180`; legacy inputs use `90,0,0`.
- Voxel defaults: size `0.08`, opacity threshold `0.20`.
- Mounted voxel names: `walk.voxel.json` and `walk.voxel.bin`.
- Mounted LOD directory name: `streamed`.

2.x rotation table:

```text
LCC -> streamed: no extra -r
PLY -> SOG:      -r -90,0,0
PLY -> streamed: -r -90,0,0
PLY -> voxel:    -r -90,0,180
LCC -> voxel:    -r 0,0,180
```

## Preferred Scripts / 推荐脚本

### End-to-end deployment / 完整部署

Use:

```bash
python3 ../../scripts/scene_workflow.py deploy-scene ...
```

This will merge settings, convert streamed LOD, generate SOG, generate voxel output, and mount the result into `supersplat-viewer/public/<scene>`.

When original PLY exists, pass it as both SOG and voxel input:

```bash
python3 ../../scripts/scene_workflow.py deploy-scene \
  scene-key \
  /path/to/meta.lcc \
  /path/to/output \
  /path/to/supersplat-viewer/public \
  /path/to/settings.json \
  --sog-input /path/to/point_cloud.ply \
  --voxel-input /path/to/point_cloud.ply
```

The positional input remains the streamed LOD source. Use LCC there for true multi-LOD streamed output. Use PLY there only when single-layer streamed output is acceptable, or when the PLY already has a `lod` column.

### Standalone conversion / 只转换资产

```bash
python3 ../../scripts/scene_workflow.py convert-scene \
  /path/to/meta.lcc \
  /path/to/output \
  --sog-input /path/to/point_cloud.ply \
  --voxel-input /path/to/point_cloud.ply
```

### Settings merge / 合并配置

```bash
python3 ../../scripts/merge_settings.py v1.json output.json --base-v2 base-v2.json
```

Use the base v2 file when you need to preserve annotations, post effects, tonemapping, and other viewer configuration.

## Direct `splat-transform` Examples / 直接命令示例

For `splat-transform` 2.x with original PLY:

```bash
splat-transform -g 0 input.ply -r -90,0,0 output/scene.sog
splat-transform -g 0 input.ply -l 0 -r -90,0,0 output/lod-meta.json
splat-transform -g 0 --voxel-params 0.08,0.20 input.ply -r -90,0,180 output/walk.voxel.json
```

For `splat-transform` 2.x with LCC streamed LOD:

```bash
splat-transform -g 0 input.lcc output/lod-meta.json
```

For `splat-transform` 2.x LCC voxel:

```bash
splat-transform -g 0 --lod-select 0 --voxel-params 0.08,0.20 input.lcc -r 0,0,180 output/walk.voxel.json
```

For legacy 1.9.2 LCC:

```bash
splat-transform input.lcc -r 90,0,0 output/lod-meta.json
splat-transform -O 0 -R 0.08 -A 0.20 input.lcc -r 90,0,0 output/walk.voxel.json
```

## First-Use Parameters / 首次使用参数说明

- `--sog-input`: high-precision source for `scene.sog`; use original PLY when available.
- `--voxel-input`: high-precision source for `walk.voxel.json`; use original PLY when available.
- `--splat-transform`: use `splat-transform-2.1.1/` for new conversions. Use `splat-transform-1.9.2/` only when reproducing legacy results.
- positional stream input: source for streamed LOD. Use LCC for true multi-LOD. PLY streamed output is single-layer unless the PLY already has LOD labels.
- `--stream-ply-lod = 0`: when streamed input is PLY, the script tags it with `-l 0` by default so `lod-meta.json` can be written.
- `--voxel-resolution = 0.08`: voxel size in meters. Smaller values are more detailed but produce larger collision files.
- `--voxel-alpha = 0.20`: alpha threshold for voxelization. Higher values ignore more weak or semi-transparent edges.

## Settings Workflows / 配置工作流

Two settings workflows are supported:

- `v1 + base v2 -> merged version 2 settings`
- `v1 -> version 2 settings`

Use:

```bash
python3 ../../scripts/merge_settings.py settings.json settings-merged.json --base-v2 settings-v2.json
```

or:

```bash
python3 ../../scripts/merge_settings.py settings.json settings-v2.json
```

## When to Remove Environment / 什么时候移除环境层

Add `--remove-environment` only when the user explicitly wants the environment stripped. Otherwise keep the generated `env/` directory and `environment` entry in `lod-meta.json`.

## Generated Viewer Route / 生成的查看器路由

The mount step creates:

- `public/<scene>/settings-merged.json` or the original settings filename
- `public/<scene>/streamed/`
- `public/<scene>/voxel/walk.voxel.json`
- `public/<scene>/voxel/walk.voxel.bin`
- `public/<scene>/index.html`

The route redirects to the root viewer with `settings`, `content`, and `voxel` query params. Do not append a `voxelRotation` query param when using baked PLY voxel output. For 2.x LCC voxel, prefer the single baked conversion (`input.lcc -r 0,0,180`) instead of relying on a viewer-side `voxelRotation`.

## Skill Locations / Skill 文件位置

- Plugin skill: `plugins/splat-transform-for-lcc/skills/splat-transform-workflow-for-lcc/SKILL.md`
- Top-level copy: `skills/splat-transform-workflow-for-lcc/SKILL.md`
- Keep these two files in sync when updating workflow guidance.
