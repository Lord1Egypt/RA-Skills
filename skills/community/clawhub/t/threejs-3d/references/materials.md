# Materials

## Quick Selection Guide

| Need | Use | Notes |
|---|---|---|
| Unlit / wireframe / background | `MeshBasicMaterial` | No lights, fastest |
| Diffuse only | `MeshLambertMaterial` | Per-vertex, fast |
| Specular highlights | `MeshPhongMaterial` | `shininess` (0–150) |
| Toon/cel shading | `MeshToonMaterial` | Needs `gradientMap` (3-pixel texture) |
| PBR (standard) | `MeshStandardMaterial` | `roughness` + `metalness` (0–1) |
| PBR + clearcoat/glass/aniso | `MeshPhysicalMaterial` | Adds `clearcoat`, `transmission`, `sheen`, `iridescence`, `anisotropy` |
| MatCap (view-dependent) | `MeshMatcapMaterial` | No lights needed, uses `matcap` texture |
| Normals debug | `MeshNormalMaterial` | RGB = XYZ normals |
| Depth visualization | `MeshDepthMaterial` | Near=black, far=white |
| Shadow receiver only | `ShadowMaterial` | `opacity` controls shadow darkness |
| Custom GLSL | `ShaderMaterial` | Full control, must declare uniforms |
| Custom GLSL (no builtins) | `RawShaderMaterial` | Must declare ALL uniforms |
| Particles | `PointsMaterial` | `size`, `sizeAttenuation`, `map` (sprite sheet) |
| Lines | `LineBasicMaterial` | `linewidth` often ignored (WebGL limit) |
| Dashed lines | `LineDashedMaterial` | Requires `geometry.computeLineDistances()` |
| Sprites (billboards) | `SpriteMaterial` | Always faces camera |

**Speed ranking:** Basic → Lambert → Phong → Standard → Physical

## Key Material Properties

```js
material.side = THREE.FrontSide | THREE.BackSide | THREE.DoubleSide;
material.transparent = true;     // Enable opacity/alpha
material.opacity = 0.5;
material.alphaTest = 0.5;       // Discard fragments below threshold (no depth issues)
material.blending = THREE.NormalBlending | THREE.AdditiveBlending | THREE.MultiplyBlending;
material.depthWrite = true;      // false for transparent to avoid z-fighting
material.depthTest = true;
material.wireframe = false;
material.flatShading = false;
material.fog = true;             // false for interior objects
material.clippingPlanes = [plane1, plane2];
material.clipIntersection = false;

// Textures on Standard/Phong:
material.map;                     // Diffuse/albedo
material.normalMap;               // RGB normal
material.roughnessMap;            // Grayscale (Standard only)
material.metalnessMap;            // Grayscale (Standard only)
material.aoMap;                   // Ambient occlusion
material.emissiveMap;
material.bumpMap;                 // Grayscale
material.displacementMap;
material.envMap;                  // Environment reflection
material.alphaMap;

// Physical material extras:
material.clearcoat;               // 0–1
material.clearcoatRoughness;      // 0–1
material.transmission;            // 0–1 (glass)
material.thickness;               // Volume thickness
material.ior;                     // Index of refraction (default 1.5)
material.sheen;                   // 0–1 (fabric)
material.iridescence;             // 0–1 (thin film)
material.anisotropy;              // 0–1 (brushed metal)
```

## Texture Color Space (critical!)

```js
// Color textures → sRGB
texture.colorSpace = THREE.SRGBColorSpace;

// Data textures (normal, roughness, metalness, AO, displacement) → Linear
texture.colorSpace = THREE.LinearSRGBColorSpace;
```

## Transparency Gotchas

**Problem:** Transparent objects at object level are sorted back→front, but individual triangles within an object are NOT sorted → back faces disappear.

**Fix 1 — Double render (convex objects):**
```js
[THREE.BackSide, THREE.FrontSide].forEach(side => {
  scene.add(new THREE.Mesh(geo, new THREE.MeshPhongMaterial({opacity:0.5, transparent:true, side})));
});
```

**Fix 2 — alphaTest (textured objects):**
```js
material.alphaTest = 0.5;  // Discard below threshold → no depth sorting needed
// Best for: leaves, grass, decals, text
```

**Fix 3 — Split intersecting planes** into non-overlapping halves with shared parent Object3D.

## Multi-Material (per-group)
```js
const mesh = new THREE.Mesh(geometry, [mat0, mat1, mat2]);
// geometry.groups: [{start, count, materialIndex}, ...]
// BoxGeometry has 6 groups (one per face), Cylinder has 3, Cone has 2
```

## ShaderMaterial Pattern
```js
new THREE.ShaderMaterial({
  uniforms: { time: {value:0}, uColor: {value: new THREE.Color()} },
  vertexShader: `varying vec2 vUv; void main() { vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.0); }`,
  fragmentShader: `uniform float time; uniform vec3 uColor; varying vec2 vUv; void main(){gl_FragColor=vec4(uColor,1.0);}`,
});
// builtin uniforms: projectionMatrix, modelViewMatrix, normalMatrix, cameraPosition, viewMatrix
// builtin attributes: position, normal, uv
```