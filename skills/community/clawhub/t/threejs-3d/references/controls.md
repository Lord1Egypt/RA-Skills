# Controls & Labels

## OrbitControls (most common)

```js
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';
const controls = new OrbitControls(camera, renderer.domElement);

// Setup
controls.target.set(0, 0, 0);
controls.enableDamping = true;     // Inertia (requires controls.update() in loop)
controls.dampingFactor = 0.05;

// Limits
controls.minDistance = 1;  controls.maxDistance = Infinity;
controls.minPolarAngle = 0; controls.maxPolarAngle = Math.PI;        // Vertical
controls.minAzimuthAngle = -Infinity; controls.maxAzimuthAngle = Infinity; // Horizontal
controls.enableZoom = true;  controls.zoomSpeed = 1.0;
controls.enableRotate = true; controls.rotateSpeed = 0.5;
controls.enablePan = true;    controls.panSpeed = 0.5;
controls.autoRotate = false;  controls.autoRotateSpeed = 2.0;

// State
controls.saveState();
controls.reset();    // Restore saved state
controls.dispose();

// Button mapping
controls.mouseButtons = { LEFT: THREE.MOUSE.ROTATE, MIDDLE: THREE.MOUSE.DOLLY, RIGHT: THREE.MOUSE.PAN };
controls.touches = { ONE: THREE.TOUCH.ROTATE, TWO: THREE.TOUCH.DOLLY_PAN };
```

## Other Controls
```js
import { TrackballControls } from 'three/addons/controls/TrackballControls.js';    // Free rotation
import { MapControls } from 'three/addons/controls/MapControls.js';                // Map-style (same API as Orbit)
import { FlyControls } from 'three/addons/controls/FlyControls.js';                // WASD flight
import { FirstPersonControls } from 'three/addons/controls/FirstPersonControls.js'; // FPS
import { PointerLockControls } from 'three/addons/controls/PointerLockControls.js'; // FPS + pointer lock
import { ArcballControls } from 'three/addons/controls/ArcballControls.js';        // Advanced with gizmos
import { TransformControls } from 'three/addons/controls/TransformControls.js';    // Move/rotate/scale gizmo
import { DragControls } from 'three/addons/controls/DragControls.js';              // Drag objects on plane
```

## TransformControls (editor gizmo)
```js
const gizmo = new TransformControls(camera, renderer.domElement);
gizmo.attach(targetObject);
gizmo.setMode('translate' | 'rotate' | 'scale');
gizmo.space = 'world' | 'local';
scene.add(gizmo);  // Add to scene to render

// Disable orbit during transform:
gizmo.addEventListener('dragging-changed', e => { orbitControls.enabled = !e.value; });
```

## DragControls
```js
const drag = new DragControls(objects, camera, renderer.domElement);
drag.addEventListener('dragstart', e => { orbitControls.enabled = false; });
drag.addEventListener('dragend', e => { orbitControls.enabled = true; });
```

## HTML Labels Aligned to 3D

Position DOM elements over 3D points via `Vector3.project()`:

```js
// Container: <div id="c"><canvas/><div id="labels"/></div>
// CSS: #c{position:relative} #labels{position:absolute;left:0;top:0}
// Labels: #labels>div{position:absolute;left:0;top:0;white-space:nowrap;text-shadow:...}

const tempV = new THREE.Vector3();
function updateLabel(obj, elem, camera, canvas) {
  obj.getWorldPosition(tempV);
  tempV.project(camera);

  if (Math.abs(tempV.z) > 1) { elem.style.display = 'none'; return; }
  elem.style.display = '';

  const x = (tempV.x * 0.5 + 0.5) * canvas.clientWidth;
  const y = (tempV.y * -0.5 + 0.5) * canvas.clientHeight;
  elem.style.transform = `translate(-50%,-50%) translate(${x}px,${y}px)`;
  elem.style.zIndex = ((-tempV.z * 0.5 + 0.5) * 100000) | 0;
}
```

**Occlusion check:** Raycaster from camera through projected point — hide if not first hit.
**Sphere backface cull:** `dot(relativePos, cameraToPoint) < 0.2` → hide label.

## Sprites (billboards — always face camera)
```js
const mat = new THREE.SpriteMaterial({ map: texture, transparent: true });
const sprite = new THREE.Sprite(mat);
sprite.position.set(x, y, z);
sprite.scale.set(w, h, 1);
sprite.center.set(0.5, 0.5);
```

### Facade (render 3D object to sprite texture)
```js
const rt = new THREE.WebGLRenderTarget(size, size);
const cam = new THREE.PerspectiveCamera(fov, 1, 0.1, 1000);
// Position cam to frame object, render to rt, use rt.texture as SpriteMaterial.map
// Saves draw calls for distant objects
```