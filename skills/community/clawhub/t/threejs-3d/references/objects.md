# Objects & Scene Graph

## Object3D (base class for everything)

```js
// Transform
obj.position.set(x, y, z);
obj.rotation.set(x, y, z);          // Euler, radians
obj.quaternion.set(x, y, z, w);     // No gimbal lock
obj.scale.set(x, y, z);

// Hierarchy
parent.add(child);                   // Add child (local space)
parent.remove(child);                // Remove
parent.attach(child);                // Reparent preserving world transform
obj.parent;                          // Access parent
obj.children;                        // Array

// Space conversion
obj.localToWorld(v);                 // Local → world
obj.worldToLocal(v);                 // World → local
obj.getWorldPosition(target);        // World position
obj.getWorldQuaternion(target);      // World rotation
obj.getWorldDirection(target);       // -Z direction in world

// Transform helpers
obj.lookAt(x,y,z | vector | object); // -Z points at target, +Y up
obj.translateX(d); obj.translateY(d); obj.translateZ(d);
obj.translateOnAxis(axis, d);
obj.rotateX(r); obj.rotateY(r); obj.rotateZ(r);

// Visibility
obj.visible = true;
obj.castShadow = false;
obj.receiveShadow = false;
obj.frustumCulled = true;            // Skip if outside camera frustum
obj.renderOrder = 0;                 // Sort order (higher = later)
obj.layers.set(0);                   // Camera must share a layer to see

// Traversal
obj.traverse(cb);                    // Visit all descendants
obj.traverseVisible(cb);             // Skip invisible
obj.traverseAncestors(cb);           // Upward
scene.getObjectByName('name');       // First match, recursive
scene.getObjectById(id);             // By numeric ID

// Manual matrix update
obj.updateMatrix();
obj.updateMatrixWorld();
obj.matrixAutoUpdate = true;         // Default; set false for static objects
obj.applyMatrix4(matrix4);           // Apply transform to object

// Lifecycle callbacks
obj.onBeforeRender = (renderer, scene, camera, geometry, material, group) => {};
obj.onAfterRender = (renderer, scene, camera, geometry, material, group) => {};
```

## Mesh
```js
new THREE.Mesh(geometry, material);   // Single material
new THREE.Mesh(geometry, [m0, m1]);   // Per-group materials
mesh.geometry; mesh.material;
```

## Group
```js
const group = new THREE.Group();
group.add(obj1, obj2, obj3);
// Group has no geometry/material — just a transform node
```

## Line / Points / Sprite
```js
new THREE.Line(geo, mat);                     // Line
new THREE.LineLoop(geo, mat);                 // Closed loop
new THREE.LineSegments(geo, mat);             // Paired vertices

new THREE.Points(geo, new THREE.PointsMaterial({size:1}));  // Particles
new THREE.Sprite(new THREE.SpriteMaterial({map:tex}));       // Always faces camera
sprite.center.set(0.5, 0.5);                                 // Anchor (default bottom-left)
```

## InstancedMesh (many copies, 1 draw call)
```js
const mesh = new THREE.InstancedMesh(geo, mat, count);
mesh.setMatrixAt(i, matrix4);
mesh.setColorAt(i, color);
mesh.instanceMatrix.needsUpdate = true;
mesh.instanceColor.needsUpdate = true;  // if using colors
```

## BatchedMesh (many different geometries, 1 draw call)
```js
const batch = new THREE.BatchedMesh(maxGeos, maxVerts, maxIndices, mat);
const geoId = batch.addGeometry(geo);
const instId = batch.addInstance(geoId);
batch.setMatrixAt(instId, matrix);
batch.deleteInstance(instId); // Can delete and reuse slots
```

## SkinnedMesh (bone animation)
```js
const skinnedMesh = new THREE.SkinnedMesh(geo, mat);
skinnedMesh.bind(skeleton);
skinnedMesh.skeleton.bones;          // Bone array
skinnedMesh.skeleton.pose();         // Reset to rest pose
```

## LOD (Level of Detail)
```js
const lod = new THREE.LOD();
lod.addLevel(highMesh, 0);            // Show when distance < 10
lod.addLevel(medMesh, 10);            // Show when distance < 50
lod.addLevel(lowMesh, 50);            // Show when distance >= 50
lod.autoUpdate = true;
```

## Scene Graph Patterns

### Reparent preserving world transform
```js
parent2.attach(child);  // One-liner
// Equivalent:
const wp = new THREE.Vector3(), wq = new THREE.Quaternion(), ws = new THREE.Vector3();
child.getWorldPosition(wp); child.getWorldQuaternion(wq); child.getWorldScale(ws);
child.removeFromParent();
parent2.add(child);
child.position.copy(wp); child.quaternion.copy(wq); child.scale.copy(ws);
```

### Debug: force all objects to one material
```js
scene.overrideMaterial = new THREE.MeshNormalMaterial();
// Remove: scene.overrideMaterial = null;
```

### EventDispatcher (base class)
```js
obj.addEventListener('change', cb);
obj.hasEventListener('change', cb);
obj.removeEventListener('change', cb);
obj.dispatchEvent({type: 'change'});
```