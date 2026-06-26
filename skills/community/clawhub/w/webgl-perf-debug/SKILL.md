---
name: webgl-perf-debug
description: WebGL性能调试与优化速查。当Canvas/WebGL渲染出现性能问题（帧率低、GPU占用高、内存泄漏、渲染闪烁）时使用。包含Chrome DevTools GPU分析、WebGL状态检测、常见性能陷阱、shader优化技巧、纹理压缩方案。

**使用时机**：
(1) Three.js/WebGL场景帧率低于30fps
(2) GPU内存占用过高
(3) shader编译慢或运行时错误
(4) 纹理加载导致卡顿
(5) 用户提到"WebGL卡"、"GPU"、"shader"、"纹理"
---

# WebGL 性能调试速查

## Chrome DevTools GPU 分析

### 打开方式
`F12` → Performance → 勾选 `Screenshots` + `WebGL`
录制 5-10 秒交互，查看 Frame 时间分布。

### 关键指标
| 指标 | 健康值 | 警告值 |
|------|--------|--------|
| Frame 时间 | < 16ms | > 33ms |
| GPU 时间 | < 10ms | > 20ms |
| JS 时间 | < 5ms | > 10ms |
| Draw Calls | < 100/frame | > 300/frame |
| Triangles | < 100k/frame | > 500k/frame |

## 常见性能陷阱

### 1. 纹理未压缩

```typescript
// ❌ PNG/JPG 纹理 — GPU 内存占用大，加载慢
const texture = loader.load('image.png')

// ✅ 压缩纹理 — 减小 50-75% GPU 内存
// 使用 Basis Universal 压缩
import { KTX2Loader } from 'three/examples/jsm/loaders/KTX2Loader'
const ktx2Loader = new KTX2Loader()
ktx2Loader.setTranscoderPath('/basis/')
const texture = ktx2Loader.load('texture.ktx2')
```

### 2. 过多 Draw Calls

```typescript
// ❌ 每个物体一个 draw call
meshes.forEach(mesh => scene.add(mesh))

// ✅ InstancedMesh — 一个 draw call 渲染 N 个相同物体
import { InstancedMesh, Matrix4 } from 'three'

const instancedMesh = new InstancedMesh(geometry, material, count)
const matrix = new Matrix4()

for (let i = 0; i < count; i++) {
  matrix.setPosition(positions[i])
  instancedMesh.setMatrixAt(i, matrix)
}
instancedMesh.instanceMatrix.needsUpdate = true
```

### 3. Shader 中使用 discard

```glsl
// ❌ discard 导致 Early-Z 失效，性能暴跌
if (alpha < 0.5) discard;

// ✅ 使用 alpha 混合
// material.transparent = true; material.depthWrite = false;
```

### 4. 动态创建纹理/GPU 对象

```typescript
// ❌ 每帧创建新纹理
function render() {
  const tex = new THREE.DataTexture(data, w, h, format)
  scene.material.map = tex // GC 压力巨大
}

// ✅ 复用纹理，更新数据
const tex = new THREE.DataTexture(data, w, h, format)
function render() {
  tex.image.data.set(newData)
  tex.needsUpdate = true // 只标记更新，不重新创建
}
```

### 5. 几何体未合并

```typescript
// ❌ 1000 个独立 Mesh = 1000 个 draw call
for (let i = 0; i < 1000; i++) {
  scene.add(new THREE.Mesh(geo, mat))
}

// ✅ 合并几何体 — 1 个 draw call
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils'
const merged = mergeGeometries(geometries)
const mesh = new THREE.Mesh(merged, material)
```

## Shader 优化

### 减少分支

```glsl
// ❌ 复杂分支
void main() {
  if (condition1) { ... }
  else if (condition2) { ... }
  else { ... }
}

// ✅ 使用 mix/step 代替 if-else
void main() {
  vec3 color = mix(colorA, colorB, step(0.5, value));
}
```

### 避免 sin/cos 纹理采样

```glsl
// ❌ 在 shader 中计算 sin/cos（虽然 GPU 快但能省则省）
float s = sin(time * 0.001);

// ✅ 用 uniform 预计算
uniform float sinTime;
```

## 内存泄漏排查

```typescript
// Three.js 常见泄漏点
function disposeMesh(mesh: THREE.Mesh) {
  mesh.geometry.dispose()
  if (mesh.material instanceof THREE.Material) {
    mesh.material.dispose()
    if (mesh.material.map) mesh.material.map.dispose()
  } else {
    mesh.material.forEach(m => {
      m.dispose()
      if (m.map) m.map.dispose()
    })
  }
}

// 监控 GPU 内存
renderer.info.render.triangles  // 三角形数
renderer.info.render.calls      // draw calls
renderer.info.memory.textures   // 纹理数
renderer.info.memory.geometries  // 几何体数
```

## 帧率监控

```typescript
// 简易 FPS 计数器
let frames = 0, lastTime = performance.now()
function updateFPS() {
  frames++
  const now = performance.now()
  if (now - lastTime >= 1000) {
    console.log(`FPS: ${frames}`)
    frames = 0
    lastTime = now
  }
}
// 在渲染循环中调用 updateFPS()
```

## 一句话总结

**减少 draw calls、复用纹理、合并几何体、避免 shader 分支** — WebGL 性能优化的四大原则。
