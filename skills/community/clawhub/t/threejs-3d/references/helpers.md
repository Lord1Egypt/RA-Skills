# Helpers & Debugging

## Visualization Helpers
```js
scene.add(new THREE.AxesHelper(5));                           // RGB axes
scene.add(new THREE.GridHelper(10, 10));                      // XZ grid
scene.add(new THREE.BoxHelper(mesh, 0xffff00));               // Wireframe bounds
scene.add(new THREE.Box3Helper(box3, 0xffff00));              // Visualize Box3
scene.add(new THREE.CameraHelper(camera));                    // Frustum
scene.add(new THREE.DirectionalLightHelper(light, 0.5));
scene.add(new THREE.PointLightHelper(light, 0.5));
scene.add(new THREE.SpotLightHelper(light));
scene.add(new THREE.SkeletonHelper(skinnedMesh));
const arrow = new THREE.ArrowHelper(dir, origin, length, color); // Debug vectors
```

All helpers need `.update()` after their target changes.

## Stats (FPS Monitor)
```js
import Stats from 'three/addons/libs/stats.module.js';
const stats = new Stats(); stats.showPanel(0);
document.body.appendChild(stats.dom);
// In loop: stats.begin(); renderer.render(...); stats.end();
```

## Debugging

### Nothing Renders? Check:
1. Camera near/far too tight? → temporarily `near=0.001, far=1000000`
2. Object behind camera? → add OrbitControls
3. Needs lights? → try `MeshBasicMaterial` first
4. NaN in transforms? → `console.log(mesh.matrixWorld)`
5. `requestAnimationFrame` at **end** of render (errors stop loop → bugs visible)
6. Unit mismatch: Three.js assumes 1 unit = 1 meter

### On-Screen Logger (per-frame self-clearing)
```js
class ClearingLogger {
  constructor(elem) { this.elem = elem; this.lines = []; }
  log(...args) { this.lines.push(args.join(' ')); }
  render() { this.elem.textContent = this.lines.join('\n'); this.lines = []; }
}
```

### Dump Scene Graph
```js
function dumpObject(obj, lines=[], isLast=true, prefix='') {
  const m = isLast ? '└─' : '├─';
  lines.push(`${prefix}${m}${obj.name||'*no-name*'} [${obj.type}]`);
  const p = prefix + (isLast?'  ':'│ ');
  obj.children.forEach((c,i)=>dumpObject(c,lines,i===obj.children.length-1,p));
  return lines;
}
console.log(dumpObject(scene).join('\n'));
```

### GLSL Shader Debugging
1. **Solid color test:** `gl_FragColor = vec4(1,0,0,1);` → if object appears, bug is in fragment shader
2. **Visualize inputs:**
   ```glsl
   gl_FragColor = vec4(vNormal * 0.5 + 0.5, 1);   // Normals → RGB
   gl_FragColor = vec4(fract(vUv), 0, 1);           // UVs → RG
   ```
3. **Shader Editor** extension (Chrome) for live shader editing
4. **Simplify:** Can you draw with MeshBasicMaterial? Add shader changes incrementally.

### NaN Sources
- `SplineCurve` (2D) fed to `Vector3.set()` → z=NaN → use `CatmullRomCurve3`
- Division by zero in custom shaders
- Uninitialized `Vector3` components

### Memory Leak Check
```js
setInterval(() => {
  console.log('geometries:', renderer.info.memory.geometries, 'textures:', renderer.info.memory.textures);
}, 2000);
// Always dispose: geo.dispose(), mat.dispose(), tex.dispose(), rt.dispose()
```

### Debug UI (lil-gui)
```js
import GUI from 'lil-gui';
const gui = new GUI();
gui.addColor(params, 'color').onChange(v => material.color.set(v));
gui.add(params, 'speed', 0, 0.1);
gui.add(mesh.position, 'x', -5, 5);
gui.add(mesh, 'visible');
```
**lil-gui helpers for Three.js:**
- `ColorGUIHelper` — bridges hex string ↔ THREE.Color
- `DegRadHelper` — bridges degrees ↔ radians
- `MinMaxGUIHelper` — enforces near<far, etc.

## Renderer Capabilities
```js
renderer.capabilities.maxTextureSize;         // Max texture resolution
renderer.capabilities.maxTextures;            // Texture units
renderer.capabilities.isWebGL2;               // WebGL 2.0 available

// Check WebGL/WebGPU support:
import { WebGL } from 'three/addons/capabilities/WebGL.js';
if (!WebGL.isWebGL2Available()) document.body.appendChild(WebGL.getErrorMessage());
```