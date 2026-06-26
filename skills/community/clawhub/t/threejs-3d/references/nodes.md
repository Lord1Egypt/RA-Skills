# Node Materials & TSL (Three.js Shading Language)

TSL = composable JS-level shader nodes. Compiles to both GLSL (WebGL) and WGSL (WebGPU).

## Core Imports
```js
import {
  // Values
  float, int, uint, bool, vec2, vec3, vec4, ivec2, ivec3, ivec4, mat3, mat4, color,

  // Inputs
  uniform, attribute, varying, output,
  positionLocal, positionWorld, positionView,
  normalLocal, normalWorld, normalView,
  uv, vertexIndex, instanceIndex, frontFacing, faceDirection,

  // Math ops (chainable)
  add, sub, mul, div, rem, pow, sqrt, abs, sign, floor, ceil, round,
  fract, mod, min, max, clamp, saturate, negate,
  sin, cos, tan, asin, acos, atan, atan2,
  exp, exp2, log, log2, radians, degrees,
  cross, dot, normalize, length, distance, reflect, refract,
  transpose, determinant, inverse, mix, step, smoothstep,
  equal, notEqual, lessThan, lessThanEqual, greaterThan, greaterThanEqual,
  and, or, not, xor, select,

  // Textures
  texture, textureLoad, textureStore, textureSample, cubeTexture,

  // Environment
  time, deltaTime, frameId, resolution,
  cameraNear, cameraFar, cameraPosition,
  cameraViewMatrix, cameraProjectionMatrix,
  modelWorldMatrix, modelNormalMatrix, modelViewMatrix,

  // Functions
  Fn, tslFn, func, wgslFn, glslFn, glsl,
  If, Else, ElseIf, loop, Break, Continue, Discard, Return,

  // Materials
  MeshStandardNodeMaterial, MeshPhysicalNodeMaterial,
  MeshPhongNodeMaterial, MeshLambertNodeMaterial, MeshToonNodeMaterial,
  MeshBasicNodeMaterial, MeshNormalNodeMaterial, MeshMatcapNodeMaterial,
  PointsNodeMaterial, SpriteNodeMaterial,
  LineBasicNodeMaterial, LineDashedNodeMaterial,
  ShadowNodeMaterial, VolumeNodeMaterial, MeshSSSNodeMaterial,
  NodeMaterial,

  // Compute
  compute, workgroupSize,
} from 'three/tsl';
```

## Basic Usage

```js
// Set nodes on material
const mat = new MeshStandardNodeMaterial();
mat.colorNode = color(0xff0000);           // Constant color
mat.roughnessNode = float(0.2);
mat.metalnessNode = float(0.8);

// Uniforms (update at runtime)
const myColor = uniform(new THREE.Color(0x00ff00));
mat.colorNode = myColor;
myColor.value.set(0xff0000); // Update later

// Texture
mat.colorNode = texture(loadedTexture);

// Animated color
mat.colorNode = vec3(sin(time.mul(2)), sin(time.mul(3).add(1)), sin(time.mul(4).add(2))).mul(0.5).add(0.5);

// Mix with position
mat.colorNode = mix(color(0xff0000), color(0x0000ff), positionLocal.y.add(1).mul(0.5));
```

## Custom TSL Functions

```js
const myFn = Fn(({ normal, lightDir, lightColor }) => {
  const NdotL = dot(normalize(normal), normalize(lightDir)).max(0);
  return vec4(lightColor.mul(NdotL), 1.0);
});
// Call: myFn({ normal: ..., lightDir: ..., lightColor: ... })
```

## Vertex Displacement
```js
mat.positionNode = positionLocal.add(
  vec3(0, sin(time.mul(3).add(positionLocal.x.mul(5))).mul(0.2), 0)
);
```

## Custom NodeMaterial (full shader)
```js
const mat = new NodeMaterial();
mat.vertexNode = ...;    // Custom vertex
mat.fragmentNode = ...;  // Custom fragment
mat.lights = true;       // Include lighting
mat.normals = true;      // Include normals
```

## Compute Shaders
```js
const computeShader = Fn(() => {
  // ... GPU computation ...
})();
const computeNode = compute(computeShader, workgroupSize(64));
renderer.compute(computeNode);
```

## TSL Tips
- TSL compiles to both GLSL and WGSL = works with WebGLRenderer AND WebGPURenderer
- Use `uniform()` for runtime-changeable values
- Classic materials (MeshStandardMaterial) can't use TSL — use `MeshStandardNodeMaterial` instead
- Node materials can be slower to initialize (compile time) but offer richer customization