# Math Utilities

Three.js math classes are standard. Key notes:

## Common Patterns

```js
// position/rotation/scale
obj.position.set(x, y, z);
obj.rotation.set(x, y, z);         // Euler, radians
obj.quaternion.set(x, y, z, w);    // Avoids gimbal lock
obj.scale.set(x, y, z);
obj.lookAt(target);                // Points -Z at target, +Y as up
```

## Matrix4 Composition
```js
// Compose/decompose transforms
const m = new THREE.Matrix4();
m.compose(position, quaternion, scale);
m.decompose(position, quaternion, scale);
m.makePerspective(left, right, top, bottom, near, far); // for shadow cameras
m.makeRotationFromQuaternion(q);  // Quaternion → Matrix
```

## Quaternion
```js
q.setFromAxisAngle(axis, angle);   // Axis-angle rotation
q.slerp(qb, t);                    // Spherical interpolation (no gimbal lock)
q.setFromUnitVectors(from, to);    // Rotation between two directions
q.rotateTowards(target, step);     // Step-limited rotation
```

## Color
```js
new THREE.Color(0xff0000);        // Hex
new THREE.Color('#ff0000');       // CSS
new THREE.Color('rgb(255,0,0)');  // CSS
new THREE.Color(1, 0, 0);         // RGB 0-1
color.setHSL(h, s, l);            // h=0..1, s=0..1, l=0..1

// Color space conversion (for proper PBR rendering)
color.convertSRGBToLinear();
color.convertLinearToSRGB();
```

## Raycaster

```js
const raycaster = new THREE.Raycaster();

// Mouse → ray:
const mouse = new THREE.Vector2();
mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
mouse.y = -(e.clientY / window.innerHeight) * 2 + 1; // flip Y
raycaster.setFromCamera(mouse, camera);
const hits = raycaster.intersectObjects(scene.children, true);

// Each hit: { distance, point, face, faceIndex, object, uv, normal, instanceId }

// Intersection with specific object types:
raycaster.params.Points.threshold = 1;  // point size tolerance
raycaster.params.Line.threshold = 1;    // line width tolerance
```

## Box3 / Sphere (Bounding Volumes)

```js
// Auto-compute bounding box of hierarchy
const box = new THREE.Box3().setFromObject(root);
const size = box.getSize(new THREE.Vector3());
const center = box.getCenter(new THREE.Vector3());

// Frustum culling check
const frustum = new THREE.Frustum();
frustum.setFromProjectionMatrix(
  new THREE.Matrix4().multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse)
);
frustum.intersectsObject(obj);     // true if visible
frustum.containsPoint(point);
```

## MathUtils

```js
THREE.MathUtils.clamp(v, min, max);
THREE.MathUtils.lerp(a, b, t);
THREE.MathUtils.mapLinear(x, a1, a2, b1, b2);
THREE.MathUtils.smoothstep(x, min, max);
THREE.MathUtils.degToRad(d);     // degrees → radians
THREE.MathUtils.radToDeg(r);     // radians → degrees
THREE.MathUtils.damp(x, y, lambda, dt);  // Smooth damping
THREE.MathUtils.randFloat(low, high);
THREE.MathUtils.randFloatSpread(range);
THREE.MathUtils.generateUUID();
THREE.MathUtils.DEG2RAD;         // Math.PI / 180
THREE.MathUtils.RAD2DEG;         // 180 / Math.PI
```

## Gotchas

- **all angles are radians** except PerspectiveCamera.fov (degrees)
- **Euler order** defaults to `'XYZ'` — change with `new Euler(x,y,z,'YXZ')` for FPS-style
- **Color.setRGB/setHSL** takes 0–1, not 0–255
- **Vector3.project(camera)** returns NDC: x,y in [-1,1], z in [-1,1] (not [0,1]!)
- **lookAt** points -Z axis at target with +Y up — adjust with `camera.up.set()` before
- **SplineCurve** is 2D — feeding into Vector3.set gives NaN on z → use CatmullRomCurve3 for 3D