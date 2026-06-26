# Textures

## Core Properties
```js
const t = new THREE.Texture(image);
t.wrapS = THREE.ClampToEdgeWrapping | THREE.RepeatWrapping | THREE.MirroredRepeatWrapping;
t.wrapT = /* same */;
t.repeat.set(u, v);              // Tile repeat
t.offset.set(u, v);              // UV offset
t.rotation = Math.PI/4;          // Radians
t.center.set(0.5, 0.5);         // Rotation pivot

t.magFilter = THREE.LinearFilter | THREE.NearestFilter;
t.minFilter = THREE.LinearMipmapLinearFilter | THREE.NearestFilter | ...;
t.generateMipmaps = true;        // false for NPOT textures
t.anisotropy = 4;               // >1 needs EXT_texture_filter_anisotropic

t.format = THREE.RGBAFormat | THREE.RGBFormat | THREE.RedFormat | ...;
t.type = THREE.UnsignedByteType | THREE.HalfFloatType | THREE.FloatType | ...;

// CRITICAL: color space
t.colorSpace = THREE.SRGBColorSpace;         // Color textures (maps)
t.colorSpace = THREE.LinearSRGBColorSpace;   // Data (normal, roughness, metalness, AO, displacement)
t.flipY = true;                              // Default; false for render-to-texture
t.needsUpdate = true;                        // After modifying image data
```

## Texture Sources

```js
// Image
const t = new THREE.TextureLoader().load('img.jpg');

// Canvas
const t = new THREE.CanvasTexture(canvas);
t.needsUpdate = true;  // After canvas drawing

// Video
const t = new THREE.VideoTexture(videoElement);
t.minFilter = THREE.LinearFilter; t.magFilter = THREE.LinearFilter;

// Data (raw typed array)
const t = new THREE.DataTexture(data, w, h, format, type);
t.needsUpdate = true;

// Render target result
const t = renderTarget.texture;
```

## Cubemap / Environment
```js
// 6 separate images
new THREE.CubeTextureLoader().load(['px.jpg','nx.jpg','py.jpg','ny.jpg','pz.jpg','nz.jpg']);

// Equirectangular (360° photo)
const t = loader.load('equirect.jpg');
t.mapping = THREE.EquirectangularReflectionMapping; // or RefractionMapping
t.colorSpace = THREE.SRGBColorSpace;
```

## Compressed Textures (KTX2)
```js
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';
const loader = new KTX2Loader();
loader.setTranscoderPath('https://unpkg.com/three@0.170.0/examples/jsm/libs/basis/');
loader.detectSupport(renderer);
loader.load('texture.ktx2', t => { material.map = t; material.needsUpdate = true; });
```

## Texture Gotchas

- **Power-of-two (POT) dimensions** (256, 512, 1024) required for mipmaps. NPOT textures: set `generateMipmaps=false`, use `LinearFilter`
- **Memory:** `width × height × 4 × 1.33 = bytes`. A 3024×3761 JPEG = 60MB in VRAM despite 157KB download
- **Normal maps** must use `LinearSRGBColorSpace` (not sRGB)
- **White 1×1 pixel fallback:** `new THREE.DataTexture(new Uint8Array([255,255,255,255]), 1, 1)` for materials switching from no-texture to textured
- **CanvasTexture** for labels: set `minFilter=LinearFilter, wrapS=ClampToEdgeWrapping` since canvas is usually NPOT
- **VideoTexture**: set `colorSpace=SRGBColorSpace`, use `LinearFilter` to avoid mipmap issues

## Memory Management
```js
texture.dispose();          // Free GPU memory
// Track: renderer.info.memory.textures
```