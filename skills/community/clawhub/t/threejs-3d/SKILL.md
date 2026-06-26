---
name: threejs-3d
description: Comprehensive Three.js 3D graphics reference. Use when building 3D web apps, games, or visualizations with Three.js. Covers: scene setup, cameras, geometries, materials, lights, shadows, post-processing, controls, animation, loaders, textures, TSL/node materials, math utils, and debugging.
---

# Three.js 3D

## Quick Start

```js
import * as THREE from 'three';
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, innerWidth/innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);
scene.add(new THREE.Mesh(
  new THREE.BoxGeometry(1,1,1),
  new THREE.MeshStandardMaterial({color: 0x44aa88})
));
scene.add(new THREE.DirectionalLight(0xffffff, 3));
scene.add(new THREE.AmbientLight(0x404040, 0.5));
camera.position.z = 5;
function animate() { requestAnimationFrame(animate); renderer.render(scene, camera); }
animate();
```

## Import
```bash
npm install three
```
```js
import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
```

## Key Patterns

### Object3D (everything extends this)
```js
obj.position.set(x,y,z); obj.rotation.set(x,y,z); obj.scale.set(x,y,z); // Euler rad
obj.quaternion.set(x,y,z,w);       // No gimbal lock
obj.lookAt(target);                // -Z → target, +Y up
parent.add(child); parent.remove(child); parent.attach(child); // Reparent w/o visual change
obj.getWorldPosition(v); obj.localToWorld(v); obj.worldToLocal(v);
```

### Color
```js
new THREE.Color(0xff0000); new THREE.Color('#ff0000'); new THREE.Color(1,0,0);
color.setHSL(hue, saturation, lightness); // 0–1
```

### Dispose (always!)
```js
geometry.dispose(); material.dispose(); texture.dispose(); renderTarget.dispose();
```

## Reference Files

Read the relevant file based on the task — each is concise and domain-focused:

| File | Topic |
|---|---|
| [getting-started.md](references/getting-started.md) | Responsive design, multi-canvas, render-on-demand, fog, disposal |
| [cameras.md](references/cameras.md) | PerspectiveCamera, OrthographicCamera, CubeCamera, gotchas |
| [geometries.md](references/geometries.md) | All built-in primitives, BufferGeometry, merge, vertex colors |
| [materials.md](references/materials.md) | Material selection guide, properties, transparency fixes, ShaderMaterial |
| [lights.md](references/lights.md) | Light types, three-point lighting, environment maps, skyboxes |
| [objects.md](references/objects.md) | Object3D API, Mesh, InstancedMesh, SkinnedMesh, LOD, scene graph |
| [textures.md](references/textures.md) | Properties, types, color space, KTX2, memory management |
| [loaders.md](references/loaders.md) | GLTF/OBJ/FBX, Draco, KTX2, loading manager, gotchas |
| [animation.md](references/animation.md) | AnimationMixer/Action, skeletal, morph targets, crossfading |
| [controls.md](references/controls.md) | OrbitControls, TransformControls, HTML labels, sprites/facades |
| [math.md](references/math.md) | Vector/Matrix/Quat/Color/Raycaster patterns + gotchas |
| [renderers.md](references/renderers.md) | WebGL/WebGPU setup, post-processing, shadows, render targets, GPU picking |
| [nodes.md](references/nodes.md) | TSL node materials, compute shaders |
| [helpers.md](references/helpers.md) | Debug helpers, scene graph dump, GLSL debugging, lil-gui patterns |