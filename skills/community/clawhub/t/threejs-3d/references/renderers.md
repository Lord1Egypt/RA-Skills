# Renderers, Post-Processing & Shadows

## WebGLRenderer Setup

```js
const renderer = new THREE.WebGLRenderer({
  antialias: true,           // MSAA
  alpha: false,              // Transparent canvas background
  preserveDrawingBuffer: false, // true for toDataURL/screenshots
  powerPreference: 'high-performance',
});
renderer.setSize(w, h);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // Cap for perf
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.toneMapping = THREE.ACESFilmicToneMapping;   // Recommended
renderer.toneMappingExposure = 1.0;
renderer.outputColorSpace = THREE.SRGBColorSpace;
document.body.appendChild(renderer.domElement);
```

**Tone Mapping options:** `NoToneMapping` | `LinearToneMapping` | `ReinhardToneMapping` | `CineonToneMapping` | `ACESFilmicToneMapping` | `AgXToneMapping` | `NeutralToneMapping`

## WebGPURenderer

```js
import WebGPURenderer from 'three/addons/renderers/webgpu/WebGPURenderer.js';
const renderer = new WebGPURenderer({ antialias: true });
await renderer.init();
renderer.setSize(w, h);
```
Note: WebGPURenderer requires async init. Some classic materials need TSL node variants.

## Performance Tracking
```js
renderer.info.render.calls;       // Draw calls
renderer.info.render.triangles;   // Triangle count
renderer.info.memory.geometries;  // Geometry count in memory
renderer.info.memory.textures;    // Texture count in memory
renderer.info.reset();            // Reset per-frame
```

## Render Targets
```js
const rt = new THREE.WebGLRenderTarget(w, h, {
  minFilter: THREE.LinearFilter,
  magFilter: THREE.LinearFilter,
  format: THREE.RGBAFormat,
  depthBuffer: true,
  samples: 0,              // MSAA (0=off)
});

// Render to texture:
renderer.setRenderTarget(rt);
renderer.render(scene, camera);
renderer.setRenderTarget(null);  // Back to screen

// Use result:
material.map = rt.texture;
rt.dispose();

// Special types:
new THREE.WebGLCubeRenderTarget(256);         // Cubemap
new THREE.WebGL3DRenderTarget(w, h, depth);   // 3D
```

## Post-Processing (EffectComposer)

**Architecture:** Creates two render targets (rtA/rtB), ping-pongs between passes:

```js
import { EffectComposer } from 'three/addons/postprocessing/EffectComposer.js';
import { RenderPass } from 'three/addons/postprocessing/RenderPass.js';
import { OutputPass } from 'three/addons/postprocessing/OutputPass.js';

const composer = new EffectComposer(renderer);
composer.addPass(new RenderPass(scene, camera));
// ... add effect passes here ...
composer.addPass(new OutputPass()); // Must be last: color space + tone mapping

// In loop:
composer.setSize(canvas.width, canvas.height);
composer.render(deltaTime);
// Pass options: pass.enabled, pass.needsSwap, pass.clear, pass.renderToScreen
```

**Custom ShaderPass:**
```js
import { ShaderPass } from 'three/addons/postprocessing/ShaderPass.js';
const myPass = new ShaderPass({
  uniforms: { tDiffuse: {value:null}, uColor: {value: new THREE.Color()} },
  vertexShader: `varying vec2 vUv; void main(){vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1);}`,
  fragmentShader: `varying vec2 vUv; uniform sampler2D tDiffuse; uniform vec3 uColor; void main(){vec4 p=texture2D(tDiffuse,vUv); gl_FragColor=vec4(p.rgb*uColor,p.a);}`,
});
```

**Available passes:** `UnrealBloomPass`, `GlitchPass`, `OutlinePass`, `SAOPass`, `SSAOPass`, `AfterimagePass`, `BokehPass`, `FilmPass`, `LutPass`, `MaskPass`/`ClearMaskPass`, `TexturePass`, `HalftonePass`

**Available built-in shaders:** `RGBShiftShader`, `FXAAShader`, `VignetteShader`, `ColorCorrectionShader`, `SepiaShader`, `DotScreenShader`

## Shadows

### Enable
```js
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Basic | PCF | PCFSoft | VSM

light.castShadow = true;
mesh.castShadow = true;
mesh.receiveShadow = true;
```

### DirectionalLight Shadow (orthographic shadow camera)
```js
light.shadow.mapSize.set(1024, 1024);
light.shadow.camera.near = 0.5;  light.shadow.camera.far = 50;
light.shadow.camera.left = -10;  light.shadow.camera.right = 10;
light.shadow.camera.top = 10;    light.shadow.camera.bottom = -10;
light.shadow.bias = -0.001;       // Reduce acne, increase peter-panning
light.shadow.normalBias = 0.02;
light.shadow.radius = 3;          // PCF soft blur (PCFSoftShadowMap only)
light.shadow.blurSamples = 8;     // VSM samples
```

### SpotLight Shadow (perspective shadow camera)
```js
// fov = light.angle (automatically), aspect = mapSize ratio
light.shadow.mapSize.set(512, 512);
light.shadow.camera.near = 0.5;  light.shadow.camera.far = 50;
light.shadow.bias = -0.0001;
```

### PointLight Shadow (6 renders — expensive!)
```js
// Same properties as SpotLight; internally renders 6 faces (cubemap)
light.shadow.mapSize.set(512, 512);
```

### Debug Shadow Camera Frustum
```js
const helper = new THREE.CameraHelper(light.shadow.camera);
scene.add(helper);
```

### Key Shadow Rules
- **Shadow map size** bigger = sharper but more memory. Keep as small as possible.
- **Shadow camera area** smaller = higher shadow resolution. Tight-fit to visible area.
- **PointLight shadows** are 6x more expensive (one render per face).
- **Only 1 directional light** should cast shadows in most scenes.
- For missing shadows: check `castShadow` on BOTH light and mesh, `receiveShadow` on receiver, and that shadow camera covers the area.

## Fake Shadows (cheap alternative)
```js
// Plane with circular shadow texture, parented to object, positioned just above ground
const shadowTex = loader.load('roundshadow.png');
const shadowMesh = new THREE.Mesh(
  new THREE.PlaneGeometry(1, 1),
  new THREE.MeshBasicMaterial({ map: shadowTex, transparent: true, depthWrite: false })
);
shadowMesh.rotation.x = -Math.PI / 2;
shadowMesh.position.y = 0.001;
shadowMesh.material.opacity = 1; // Fade as object rises
```

## GPU-Based Picking (alternative to Raycaster)
Render each pickable object with unique color ID to 1×1 render target:

```js
const pickRT = new THREE.WebGLRenderTarget(1, 1);
const pixel = new Uint8Array(4);

// Per-object: emissive = ID as hex, color=black, blending=NoBlending
// Render only pixel under cursor with camera.setViewOffset(...)
renderer.setRenderTarget(pickRT);
renderer.render(pickingScene, camera);
renderer.setRenderTarget(null);
renderer.readRenderTargetPixels(pickRT, 0, 0, 1, 1, pixel);
const id = (pixel[0]<<16)|(pixel[1]<<8)|pixel[2];
// Lookup: idToObject[id]
```
Advantage: handles shader deformations and alphaTest transparency.