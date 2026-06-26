# Loaders

## LoadingManager (track all loads)
```js
const manager = new THREE.LoadingManager();
manager.onLoad = () => console.log('All done');
manager.onProgress = (url, loaded, total) => { /* progress bar */ };
manager.onError = (url) => console.error('Failed:', url);

const loader = new THREE.TextureLoader(manager); // Pass to any loader
```

## Texture Loaders
```js
// Basic
const tex = new THREE.TextureLoader().load('tex.jpg');
tex.colorSpace = THREE.SRGBColorSpace;          // Color textures
tex.colorSpace = THREE.LinearSRGBColorSpace;    // Normal/roughness/metal/AO maps

// Cubemap
new THREE.CubeTextureLoader().setPath('skybox/')
  .load(['px.jpg','nx.jpg','py.jpg','ny.jpg','pz.jpg','nz.jpg']);

// HDR/EXR environment maps
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { EXRLoader } from 'three/addons/loaders/EXRLoader.js';
new RGBELoader().setDataType(THREE.HalfFloatType).load('env.hdr', tex => {
  tex.mapping = THREE.EquirectangularReflectionMapping;
  scene.environment = tex;
});
```

## GLTFLoader (primary model format)

```js
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { DRACOLoader } from 'three/addons/loaders/DRACOLoader.js';
import { KTX2Loader } from 'three/addons/loaders/KTX2Loader.js';

const loader = new GLTFLoader();

// Draco (mesh compression)
const dracoLoader = new DRACOLoader();
dracoLoader.setDecoderPath('https://www.gstatic.com/draco/versioned/decoders/1.5.7/');
loader.setDRACOLoader(dracoLoader);

// KTX2 (texture compression)
const ktx2Loader = new KTX2Loader();
ktx2Loader.setTranscoderPath('https://unpkg.com/three@0.170.0/examples/jsm/libs/basis/');
ktx2Loader.detectSupport(renderer);
loader.setKTX2Loader(ktx2Loader);

loader.load('model.glb', gltf => {
  scene.add(gltf.scene);
  // gltf.animations, gltf.cameras, gltf.asset
  // Play all: gltf.animations.forEach(c => new THREE.AnimationMixer(gltf.scene).clipAction(c).play());
});
```

### glTF Gotchas
- `.glb` = binary (single file, compact), `.gltf` = JSON + separate assets
- **Artists should clear transforms** before export — scaling/rotating nodes breaks runtime positioning
- Remove unnecessary wrapper nodes (orientation_matrix, model_correction_matrix) from export
- For animated models with broken origins: reparent into fresh Object3D at world position
```js
root.updateMatrixWorld();
for (const child of loadedGroup.children.slice()) {
  const wrapper = new THREE.Object3D();
  child.getWorldPosition(wrapper.position);
  child.position.set(0, 0, 0);
  wrapper.add(child);
  scene.add(wrapper);
}
```

## OBJ Loader

```js
import { OBJLoader } from 'three/addons/loaders/OBJLoader.js';
import { MTLLoader } from 'three/addons/loaders/MTLLoader.js';

new MTLLoader().load('model.mtl', mtl => {
  mtl.preload();
  Object.values(mtl.materials).forEach(m => m.side = THREE.DoubleSide); // Common fix
  const objLoader = new OBJLoader().setMaterials(mtl);
  objLoader.load('model.obj', root => scene.add(root));
});
```

### OBJ/MTL Common Fixes
- `map_Bump` → `norm` in .mtl for normal maps
- Convert TGA textures to JPG/PNG (TGA unsupported, very large)
- Auto-frame after load: `const box = new THREE.Box3().setFromObject(root);` then adjust camera

## Other Model Loaders
```js
import { FBXLoader } from 'three/addons/loaders/FBXLoader.js';
import { STLLoader } from 'three/addons/loaders/STLLoader.js';
import { ColladaLoader } from 'three/addons/loaders/ColladaLoader.js';
import { PLYLoader } from 'three/addons/loaders/PLYLoader.js';
import { PCDLoader } from 'three/addons/loaders/PCDLoader.js';  // Point clouds
```

## SVG / Font / Audio
```js
import { SVGLoader } from 'three/addons/loaders/SVGLoader.js';
import { FontLoader } from 'three/addons/loaders/FontLoader.js';
import { TTFLoader } from 'three/addons/loaders/TTFLoader.js';
new THREE.AudioLoader().load('sound.mp3', buffer => { audio.setBuffer(buffer); audio.play(); });
```

## Serialization
```js
new THREE.BufferGeometryLoader().load('geo.json', geo => {});
new THREE.ObjectLoader().load('obj.json', obj => {});
new THREE.MaterialLoader().load('mat.json', mat => {});
```

## Cache
```js
THREE.Cache.enabled = true;  // Default on
THREE.Cache.clear();         // Clear all
THREE.Cache.remove(key);     // Remove specific
```