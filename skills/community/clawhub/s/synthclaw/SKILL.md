---
name: synthclaw
license: MIT
metadata:
  version: 0.2.3
description: Render Blender files with agent-controlled procedural parameters for synthetic data generation. A key capability of this skill is returning dynamic quality metrics (Naturalness and LPIPS) upon generation and measuring dataset-wide diversity (Shannon entropy), allowing agents to be guided by the metric results to iteratively optimize parameter ranges and improve synthetic data usefulness. Supports CYCLES (production) and EEVEE (fast testing) render engines.
---

## Agent Rules & Guidelines (CRITICAL)

> [!IMPORTANT]
> To ensure correct execution and environment compatibility, any agent ingesting this skill MUST adhere to the following rules:
> 1. **Strictly Use Provided Tools**: You MUST use the provided high-level python tools (`render_procedural_scene`, `render_procedural_dataset`, `analyze_blend`, `analyze_dataset`) for all Blender rendering and analysis tasks.
> 2. **Prohibition of Custom Python Scripts**: Do NOT write custom Python scripts that import `bpy` (Blender Python API) or write manual file-writing rendering loops. The environment does not support direct `bpy` imports outside of the provided headless context wrapper.
> 3. **Prohibition of Direct CLI Calls**: Do NOT execute raw `blender` commands directly in the shell (e.g. `blender -b -P ...`). Always use the designated tool calls.
> 4. **Mandatory Discovery Phase**: You MUST call `analyze_blend` first before attempting to render any `.blend` file. This is required to discover the exact names of the available Value Nodes, materials, objects, and collections in the scene.
> 5. **Handling Heavy Scenes & Timeouts**: For heavy scenes with complex compositing pipelines or large file sizes (e.g. over 200 MB), EEVEE may time out. If EEVEE runs exceed the 60-second limit, pass a custom, larger `timeout` argument to `render_procedural_scene` or run production Cycles rendering (which automatically configures Metal GPU on macOS and CUDA elsewhere).

## When to Use

- Generate synthetic training data with controlled parameter variations
- Create procedural image datasets with ground truth metadata
- Automate rendering workflows for ML training data
- When you need parameter-sweep renders without manual Blender interaction

## When NOT to Use

- Real-time rendering or interactive preview needs (this is batch/offline)
- Complex scene manipulation beyond Value Node adjustments
- If Blender is not installed or unavailable in PATH

## Requirements

- Blender 4.0+ / 5.0+ installed and available in `$PATH` (fully compatible with Blender 5.0+ compositor APIs)
- Python 3.10+ for the synthclaw package
- Cycles or EEVEE render engine (auto-selected, Cycles utilizes GPU acceleration natively via Metal on macOS and CUDA elsewhere)

## Configuration

No additional configuration required. Ensure `blender` command is available:

```bash
blender --version
```

## Tools

### render_procedural_scene

Adjusts procedural Value Nodes and renders a frame in Blender.

**Parameters:**
- `blend_file` (string, required): Absolute path to the .blend file
- `parameters` (object, required): Key-value pairs of Value Node names and float values (e.g., `{"GrainScale": 2.5, "Roughness": 0.3}`)
- `output_path` (string, required): Where to save the rendered image (e.g., `/path/to/output.png`)
- `samples` (integer, optional): Cycles samples (default: 128). Ignored for EEVEE.
- `engine` (string, optional): Render engine - `"CYCLES"` (default) or `"EEVEE"`
- `timeout` (integer, optional): Custom timeout in seconds. Defaults: 1800 for CYCLES, 60 for EEVEE.
- `reference_image` (string, optional): Complete path to a real-world reference image. Used for computing LPIPS similarity and Naturalness Delta.
- `compute_metrics` (boolean, optional): Set to `true` to compute Naturalness/LPIPS metrics after rendering. Default `false`.

**Returns:**
- On success: `{"status": "success", "output": "/path/to/output.png", "log": "...", "engine": "CYCLES", "samples": 128, "metrics": {"naturalness_mean": 0.85, "lpips_alex": 0.12}}`
- On error: `{"status": "error", "message": "..."}`

**Examples:**

*Production quality (CYCLES):*
```json
{
  "blend_file": "/home/user/project/assets/test.blend",
  "output_path": "/home/user/output/render_01.png",
  "parameters": {
    "GrainScale": 3.0,
    "DisplacementStrength": 1.5
  },
  "engine": "CYCLES",
  "samples": 256
}
```

*Fast testing (EEVEE):*
```json
{
  "blend_file": "/home/user/project/assets/test.blend",
  "output_path": "/home/user/output/test_render.png",
  "parameters": {
    "GrainScale": 3.0
  },
  "engine": "EEVEE"
}
```

### render_procedural_scene_fast

Convenience function for fast EEVEE rendering. Same as `render_procedural_scene` with `engine="EEVEE"`.

**Parameters:**
- `blend_file` (string, required): Absolute path to the .blend file
- `parameters` (object, required): Key-value pairs of Value Node names and float values
- `output_path` (string, required): Where to save the rendered image

### render_procedural_scene_production

Convenience function for production Cycles rendering. Same as `render_procedural_scene` with `engine="CYCLES"` and higher samples.

**Parameters:**
- `blend_file` (string, required): Absolute path to the .blend file
- `parameters` (object, required): Key-value pairs of Value Node names and float values
- `output_path` (string, required): Where to save the rendered image
- `samples` (integer, optional): Cycles samples (default: 512)

### render_procedural_dataset

Generates a procedural dataset from any `.blend` file by applying dynamic randomization rules frame-by-frame and routing compositor file outputs automatically.

**Parameters:**
- `blend_file` (string, required): Absolute path to the .blend file
- `output_dir` (string, required): Absolute path where generated images/masks will be saved
- `num_images` (integer, optional): Number of images to render (default: 2)
- `randomizations` (array of objects, optional): List of randomization rules specifying target elements and distribution parameters
- `engine` (string, optional): `"CYCLES"` (default) or `"EEVEE"`
- `samples` (integer, optional): Cycles samples per frame (default: 128)

### analyze_blend

Analyzes a .blend file and returns available Value Nodes that can be manipulated.

**Parameters:**
- `blend_file` (string, required): Absolute path to the .blend file

**Returns:** Dict containing:
- `status` (string): `"success"` or `"error"`
- `parameters` (object): Contains:
  - `complexity` (object): Scene realism evaluation (rating, score, polygon/light counts)
  - `value_nodes` (object): Available parameter node names, current values, and their assigned materials/node groups
  - `collections` (object): Hierarchical tree of scene collections and their direct object memberships
  - `objects` (object): Detailed dictionary of scene objects (type, location, rotation, scale, visibility in render, and assigned materials)
  - `materials` (object): Detailed dictionary of materials (use_nodes status, user count)
- `blend_file` (string): Path to the analyzed file

### analyze_dataset

Computes dataset-wide diversity (Shannon entropy) and average Naturalness across a list of generated images. Together with Naturalness, Diversity allows iterative improvement of the synthetic data's usefulness.

**Parameters:**
- `image_paths` (array of strings, required): List of absolute paths to images in the dataset

**Returns:** Dict containing `status`, `diversity` (overall Shannon entropy across all images), `naturalness_mean` (average naturalness factor), and `individual_metrics` (per-image naturalness details).

## Engine Comparison

| Feature | CYCLES | EEVEE |
|---------|--------|-------|
| Quality | Photorealistic | Real-time |
| Speed | Slow (minutes) | Fast (seconds) |
| Timeout | 30 minutes | 1 minute |
| Use case | Production | Testing |
| Samples | Configurable | N/A |

## Safety & Limitations

- **Headless execution:** Blender runs with `-b` flag for security
- **Parameter validation:** Only float values accepted; non-numeric input is rejected
- **No shell injection:** Uses `subprocess.run(shell=False)` with `--` separator
- **GPU Acceleration:** Automatically configures Metal (Apple Silicon) or CUDA/OptiX GPU rendering for Cycles, fallback to CPU is automatic if no compatible GPU is active
- **Timeout protection:** Long renders are killed after timeout to prevent hanging

## Files

| File | Purpose |
|------|---------|
| `src/synthclaw/blender_skill.py` | OpenClaw execution wrapper with engine selection |
| `src/synthclaw/analyze_skill.py` | Dataset metrics and file analysis wrapper |
| `scripts/agent_bridge.py` | Blender-side Python script (handles both engines) |
| `scripts/render_dataset.py` | Blender-side script for generic procedural dataset rendering |
| `scripts/analyze_blends.py` | Blender-side analysis script |
| `assets/config/render_schema.json` | Tool schema for LLM function calling |
| `assets/config/render_dataset_schema.json` | Tool schema for procedural dataset rendering function calling |
| `assets/config/analyze_schema.json` | Schema for blend file analysis |
| `assets/config/dataset_analysis_schema.json` | Schema for dataset diversity and naturalness analysis |

## Example Workflow (Metric-Guided Optimization)

1. User: "Render a realistic surface texture matching this real-world reference image"
2. Agent calls `analyze_blend` to see available parameters.
3. Agent renders a fast test image passing `compute_metrics=true` and a `reference_image` path.
4. Agent receives feedback metrics (e.g. `lpips_alex` similarity score and `naturalness_mean`).
5. Guided by these metric results, the agent iteratively adjusts parameters (e.g., grain scale, roughness) to optimize realism.
6. The agent performs a few iterations of this optimization loop until the metric values reach the desired threshold.
7. Agent calls `render_procedural_scene_production` (CYCLES) to render the final optimized output.

## Version

Compatible with Blender 4.0+. Not backwards compatible with 2.7x.
