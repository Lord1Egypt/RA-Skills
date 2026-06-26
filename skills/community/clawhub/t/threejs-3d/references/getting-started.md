# Getting Started — Advanced Patterns

## Minimal Scene

```js
import * as THREE from 'three';
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, innerWidth/innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
document.body.appendChild(renderer.domElement);

const mesh = new THREE.Mesh(
  new THREE.BoxGeometry(1,1,1),
  new THREE.MeshStandardMaterial({color: 0x44aa88})
);
scene.add(mesh);
scene.add(new THREE.DirectionalLight(0xffffff, 3));
scene.add(new THREE.AmbientLight(0x404040, 0.5));
camera.position.z = 5;

function animate() {
  requestAnimationFrame(animate);
  mesh.rotation.x += 0.01; mesh.rotation.y += 0.01;
  renderer.render(scene, camera);
}
animate();
```

## Installation
```js
// npm
import * as THREE from 'three';

// Addons
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
```

## Responsive Design
```js
function resizeRendererToDisplaySize(renderer) {
  const canvas = renderer.domElement;
  const w = canvas.clientWidth, h = canvas.clientHeight;
  const need = canvas.width !== w || canvas.height !== h;
  if (need) renderer.setSize(w, h, false);
  return need;
}

// In render loop:
if (resizeRendererToDisplaySize(renderer)) {
  camera.aspect = canvas.clientWidth / canvas.clientHeight;
  camera.updateProjectionMatrix();
}
// Pass `false` to setSize — let CSS control display size, match drawingBuffer to CSS
```

### HD-DPI
```js
const pr = window.devicePixelRatio;
const w = Math.floor(canvas.clientWidth * pr);
const h = Math.floor(canvas.clientHeight * pr);
if (canvas.width !== w || canvas.height !== h) renderer.setSize(w, h, false);

// Cap resolution to prevent GPU overload:
const maxPixels = 3840 * 2160;
const scale = w*h > maxPixels ? Math.sqrt(maxPixels/(w*h)) : 1;
renderer.setSize(Math.floor(w*scale), Math.floor(h*scale), false);
```

## Rendering on Demand (no continuous loop)
```js
let renderRequested = false;
function requestRenderIfNotRequested() {
  if (!renderRequested) { renderRequested = true; requestAnimationFrame(render); }
}
function render() { renderRequested = false; /* ... render ... */ }
render(); // Initial
controls.addEventListener('change', requestRenderIfNotRequested);
window.addEventListener('resize', requestRenderIfNotRequested);
// For damped controls: call controls.update() inside render()
```

## Multiple Canvases (single WebGL context)
Browser limits WebGL contexts (~8). Use one canvas with scissor/viewport per "virtual" canvas:

```js
const sceneElems = [];
function addScene(elem, fn) { sceneElems.push({elem, fn}); }

function render(time) {
  renderer.setScissorTest(false); renderer.clear(true, true); renderer.setScissorTest(true);
  renderer.domElement.style.transform = `translateY(${scrollY}px)`; // scroll sync

  for (const {elem, fn} of sceneElems) {
    const r = elem.getBoundingClientRect();
    if (r.bottom < 0 || r.top > innerHeight || r.right < 0 || r.left > innerWidth) continue;
    const y = renderer.domElement.clientHeight - r.bottom;
    renderer.setScissor(r.left, y, r.width, r.height);
    renderer.setViewport(r.left, y, r.width, r.height);
    fn(time, r);
  }
  requestAnimationFrame(render);
}
```

## Fog
```js
scene.fog = new THREE.Fog(color, near, far);       // Linear (most common)
scene.fog = new THREE.FogExp2(color, density);     // Exponential (realistic)
scene.background = new THREE.Color(fogColor);       // Must match fog color!
// Per-material exclusion:
material.fog = false;  // For interiors viewed from inside
```

## Clock / Timer
```js
const clock = new THREE.Clock();
// In loop: const delta = clock.getDelta(); // seconds, auto-start
// Timer (new): timer.update(timestamp); timer.getDelta(); timer.getElapsed();
```

## Disposal (prevent memory leaks)
```js
geometry.dispose();
material.dispose();
texture.dispose();
renderTarget.dispose();

// Dispose materials includes textures:
function disposeMaterial(mat) {
  for (const k of Object.keys(mat)) {
    if (mat[k]?.isTexture) mat[k].dispose();
  }
  mat.dispose();
}
// Full scene:
scene.traverse(obj => {
  if (obj.geometry) obj.geometry.dispose();
  if (obj.material) { /* disposeMaterial */ }
});
renderer.dispose();
```

## Capacibilities / WebXR
```js
import { WebGL } from 'three/addons/capabilities/WebGL.js';
if (!WebGL.isWebGL2Available()) document.body.appendChild(WebGL.getErrorMessage());

// VR:
renderer.xr.enabled = true;
renderer.setAnimationLoop(() => renderer.render(scene, camera));
```