# Geometries

## Built-in Primitives

| Geometry | Constructor | Default |
|---|---|---|
| Box | `BoxGeometry(w, h, d, segW, segH, segD)` | `(1,1,1,1,1,1)` |
| Sphere | `SphereGeometry(r, segW, segH, phiS, phiL, thetaS, thetaL)` | `(1,32,16,0,2π,0,π)` |
| Plane | `PlaneGeometry(w, h, segW, segH)` | `(1,1,1,1)` |
| Circle | `CircleGeometry(r, seg, thetaS, thetaL)` | `(1,32,0,2π)` |
| Cylinder | `CylinderGeometry(rTop, rBot, h, segR, segH, open)` | `(1,1,1,32,1,false)` |
| Cone | `ConeGeometry(r, h, segR, segH, open)` | `(1,1,32,1,false)` |
| Capsule | `CapsuleGeometry(r, len, capSeg, radSeg)` | `(1,1,4,8)` |
| Ring | `RingGeometry(inR, outR, segT, segP, tS, tL)` | `(0.5,1,32,1,0,2π)` |
| Torus | `TorusGeometry(R, r, segR, segT, arc)` | `(1,0.4,12,48,2π)` |
| TorusKnot | `TorusKnotGeometry(R, r, segT, segR, p, q)` | `(1,0.4,64,8,2,3)` |
| Tube | `TubeGeometry(path, seg, r, segR, closed)` | path is Curve |
| Lathe | `LatheGeometry(points, seg, phiS, phiL)` | spin points around Y |
| Shape | `ShapeGeometry(shapes, seg)` | 2D shapes |
| Extrude | `ExtrudeGeometry(shapes, opts)` | depth + bevel |

**Polyhedra:** `IcosahedronGeometry(r, detail)`, `DodecahedronGeometry(r, detail)`, `OctahedronGeometry(r, detail)`, `TetrahedronGeometry(r, detail)`, `PolyhedronGeometry(verts, indices, r, detail)`

**Wireframe:** `EdgesGeometry(geo, thresholdAngle)` — boundary edges only | `WireframeGeometry(geo)` — all edges

## BufferGeometry (custom)

```js
const geo = new THREE.BufferGeometry();
const verts = new Float32Array([...]);                // Flat array [x,y,z, x,y,z, ...]
geo.setAttribute('position', new THREE.BufferAttribute(verts, 3));
geo.setIndex([0,1,2, 2,1,3, ...]);                    // Indexed triangles (optional)
geo.computeVertexNormals();                            // Auto normals if not provided
geo.computeBoundingBox(); geo.computeBoundingSphere();

// Named attributes: position, normal, uv, color, uv2
// Each is a BufferAttribute(typedArray, componentsPerVertex)

// Transform geometry in place:
geo.translate(x,y,z); geo.scale(x,y,z);
geo.rotateX(r); geo.rotateY(r); geo.rotateZ(r);
geo.center();
geo.applyMatrix4(matrix);
geo.applyQuaternion(q);

// Dynamic update:
const posAttr = new THREE.BufferAttribute(positions, 3);
posAttr.setUsage(THREE.DynamicDrawUsage);
geo.setAttribute('position', posAttr);
// In loop: modify positions array, then posAttr.needsUpdate = true;
```

## Optimize: Merge Geometries (1 draw call)
```js
import { mergeGeometries } from 'three/addons/utils/BufferGeometryUtils.js';
const merged = mergeGeometries(geos, false);

// For per-object colors in merged geometry:
const colors = new Uint8Array(3 * numVerts);
const rgb = [r*255, g*255, b*255];
for (let i=0; i<colors.length; i++) colors[i] = rgb[i%3];
geo.setAttribute('color', new THREE.BufferAttribute(colors, 3, true));
// Then: new THREE.MeshBasicMaterial({ vertexColors: true })
```

## Sphere Positioning Helper
```js
// Efficiently place N objects on sphere surface:
const lonH = new THREE.Object3D(), latH = new THREE.Object3D(), posH = new THREE.Object3D();
lonH.add(latH); latH.add(posH); posH.position.z = radius;
// For each point: lonH.rotation.y = long; latH.rotation.x = lat; posH.updateWorldMatrix(true,false);
// mesh.applyMatrix4(posH.matrixWorld);
```

## Disposal
```js
geometry.dispose();
// Also disposes underlying buffer attributes
```