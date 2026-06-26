# Black Screen Checklist

Use this when the user says:

- “shader 黑屏”
- “编译过了但没显示”
- “Three.js ShaderMaterial 什么都没有”
- “ShaderToy 改过去以后是空白”

## 1. Prove the draw path works

- Replace the fragment shader with a constant visible color.
- For material shaders, use a simple plane or known-good mesh first.
- For full-screen effects, verify the quad or pass is rendered at all.

## 2. Prove data reaches the shader

- Output UV as color.
- Output normal as color if normals are relevant.
- Output time-driven sine as grayscale.
- Output one texture sample directly before any processing.

## 3. Check stage boundaries

- Vertex shader varyings must match fragment shader names and types exactly.
- Geometry must actually contain attributes like `uv` and `normal`.
- If deformation is involved, reduce vertex logic until the mesh reappears.

## 4. Check math hazards

Look for:

- division by zero
- `normalize` on a zero vector
- bad `pow` inputs
- invalid `acos` / `asin` domains
- thresholds that discard everything
- UVs far outside expected range

## 5. Check host integration

- Are all uniforms passed from JS?
- Does the code update `uTime` every frame?
- Is `uResolution` non-zero and current?
- Is the texture loaded before sampling?
- Is the shader written for WebGL1 while the project expects different syntax?

## 6. Narrow the failure precisely

Ask:

- Does compile fail or only runtime output fail?
- Is the output blank, white, black, transparent, or flickering?
- Is the issue only on one mesh or all meshes?
- Did the bug appear after adding one specific term?

The goal is not to inspect every line at once. The goal is to cut the shader back to the smallest version that still fails.
