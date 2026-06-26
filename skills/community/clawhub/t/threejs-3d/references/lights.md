# Lights & Environments

## Light Types

| Light | Constructor | Shadow | Notes |
|---|---|---|---|
| AmbientLight | `(color, intensity)` | No | Uniform omnidirectional |
| HemisphereLight | `(skyColor, groundColor, intensity)` | No | Sky/ground gradient |
| DirectionalLight | `(color, intensity)` | Yes (ortho) | Parallel rays (sun) |
| PointLight | `(color, intensity, distance, decay)` | Yes (cubemap, 6x render!) | Omnidirectional from point |
| SpotLight | `(color, intensity, distance, angle, penumbra, decay)` | Yes (persp) | Cone with falloff |
| RectAreaLight | `(color, intensity, width, height)` | No | Realistic soft, needs `RectAreaLightUniformsLib.init()` |
| IESSpotLight | `(color, intensity, distance, angle, penumbra, decay)` | No | IES profile via `iesMap` texture |
| ProjectorLight | `(color, intensity, distance)` | No | Projects texture like video projector |

All lights extend `Object3D` — use `position`/`rotation`, `lookAt` (except RectAreaLight uses rotation).

## DirectionalLight (most common for shadows)
```js
const light = new THREE.DirectionalLight(0xffffff, 3); // color, intensity
light.position.set(2, 5, 3);
light.target.position.set(0, 0, 0); scene.add(light.target);
scene.add(light);
scene.add(new THREE.DirectionalLightHelper(light, 0.5));
```

## SpotLight
```js
const light = new THREE.SpotLight(0xffffff, 50, 0, Math.PI/6, 0.3, 2);
// intensity, distance (0=infinite), angle, penumbra (0–1), decay
light.target.position.set(0, 0, 0); scene.add(light.target);
```

## PointLight
```js
new THREE.PointLight(color, intensity, distance, decay);
// Shadows: 6 renders per light (cubemap) — very expensive; use sparingly
```

## RectAreaLight
```js
import { RectAreaLightUniformsLib } from 'three/addons/lights/RectAreaLightUniformsLib.js';
RectAreaLightUniformsLib.init();  // Required before use
const light = new THREE.RectAreaLight(color, 5, 12, 4); // w, h
light.rotation.x = -Math.PI/2;  // Use rotation, not target
```

## Lighting Patterns

**Three-point:**
```js
const key = new THREE.DirectionalLight(0xffffff, 3); key.position.set(2,5,3);
const fill = new THREE.DirectionalLight(0x8888ff, 1); fill.position.set(-2,3,-1);
const rim = new THREE.DirectionalLight(0xff8888, 1.5); rim.position.set(0,2,-3);
scene.add(new THREE.AmbientLight(0x404040, 0.5));
```

## Environment Maps (PBR)
```js
const pmrem = new THREE.PMREMGenerator(renderer);
pmrem.compileCubemapShader(); // Pre-compile

// From equirectangular HDR
const tex = new RGBELoader().load('env.hdr', t => {
  scene.environment = pmrem.fromEquirectangular(t).texture;
  scene.background = t; // Optional
  t.dispose();
});

// From cubemap
const cubeTex = new THREE.CubeTextureLoader().load(['px.jpg',...]);
scene.environment = pmrem.fromCubemap(cubeTex).texture;

// Bake current scene as environment (for reflections)
scene.environment = pmrem.fromScene(scene, 0.04).texture;
```

## Backgrounds
```js
// Solid color
scene.background = new THREE.Color(0x222222);

// Cubemap skybox
scene.background = new THREE.CubeTextureLoader().load(['px.jpg','nx.jpg','py.jpg','ny.jpg','pz.jpg','nz.jpg']);

// Equirectangular
loader.load('env.jpg', t => { t.mapping = THREE.EquirectangularReflectionMapping; scene.background = t; });

// Aspect-correct texture background (needs update in loop):
const canvasAsp = canvas.clientWidth / canvas.clientHeight;
const imgAsp = t.image?.width / t.image?.height || 1;
const asp = imgAsp / canvasAsp;
t.repeat.set(asp>1 ? 1/asp : 1, asp>1 ? 1 : asp);
t.offset.set(asp>1 ? (1-1/asp)/2 : 0, asp>1 ? 0 : (1-asp)/2);
```

## Light Helpers
```js
scene.add(new THREE.DirectionalLightHelper(light, 0.5));
scene.add(new THREE.PointLightHelper(light, 0.5));
scene.add(new THREE.SpotLightHelper(light));
scene.add(new THREE.HemisphereLightHelper(light, 0.5));
// For shadow camera frustum: scene.add(new THREE.CameraHelper(light.shadow.camera));
```