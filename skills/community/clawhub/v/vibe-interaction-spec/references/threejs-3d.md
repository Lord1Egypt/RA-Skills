# three.js 三维

3D 在网页里的定位是**叙事与空间感**，不是炫技。判断标准很硬：这个 3D 是否承担了「说不清但看得懂」的信息？如果换成图片也能表达，就换成图片——3D 的代价是启动时间、电量和低端机崩溃率。

## 1. 什么时候值得上 3D

| 值得 | 不值得 |
| --- | --- |
| 产品内部结构需要被「转着看」 | 一个可以拍成照片的物体 |
| 空间关系本身就是信息（户型、机房、数据场） | 纯装饰的旋转立方体 |
| 品牌片头、发布会首屏，一次性冲击 | 内容页的常驻背景 |
| 需要随滚动推进的叙事 | 交互复杂到用户学不会 |

**判断句**：把 3D 换成一张静态图，信息有没有损失？没有 → 用图。

## 2. 最小可运行骨架

```js
import * as THREE from 'three';

const canvas = document.querySelector('#stage');
const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2)); // 上限 2，别跟着 3x 屏跑

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(45, 1, 0.1, 100);
camera.position.set(0, 0, 6);

const geo = new THREE.IcosahedronGeometry(1.4, 4);
const mat = new THREE.MeshStandardMaterial({ color: 0x1b3a2e, roughness: 0.35, metalness: 0.1 });
const mesh = new THREE.Mesh(geo, mat);
scene.add(mesh);
scene.add(new THREE.HemisphereLight(0xfaf8f5, 0x2c2c2a, 1.2));

function resize() {
  const { clientWidth: w, clientHeight: h } = canvas.parentElement;
  renderer.setSize(w, h, false);
  camera.aspect = w / h;
  camera.updateProjectionMatrix();
}
new ResizeObserver(resize).observe(canvas.parentElement);
resize();

const clock = new THREE.Clock();
renderer.setAnimationLoop(() => {
  mesh.rotation.y += clock.getDelta() * 0.4;
  renderer.render(scene, camera);
});
```

四条容易漏的：

- `setPixelRatio(Math.min(dpr, 2))`：不设上限，3x 手机上像素量是 1x 的 9 倍
- `ResizeObserver` 而不是 `window.onresize`：容器变化（侧栏折叠）也要响应
- `setAnimationLoop` 而不是裸 `requestAnimationFrame`：XR 与后台暂停都靠它
- `alpha: true` 且不给 `scene.background`：让 3D 融进页面底色，而不是贴一块黑

## 3. 相机与构图

| 参数 | 手感 | 建议 |
| --- | --- | --- |
| `fov` 35–45 | 克制、像长焦，产品显得规整 | 产品展示、编辑风格页面 |
| `fov` 50–60 | 接近人眼，空间感自然 | 场景漫游 |
| `fov` 75+ | 广角夸张，边缘拉伸 | 强冲击力，慎用 |

- **透视 vs 正交**：正交相机（`OrthographicCamera`）没有近大远小，适合等距（isometric）风格、图表化 3D；透视适合真实空间。
- **主体不居中**：居中 = 证件照。把主体偏到 1/3 处，留出负空间给标题。
- **别让相机静止**：哪怕 0.2°/s 的极慢环绕，也比完全静止有生命力；但 `prefers-reduced-motion` 下必须停。

## 4. 光照决定「贵不贵」

3D 的廉价感八成来自光照，而不是模型。

| 方案 | 成本 | 观感 |
| --- | --- | --- |
| `HemisphereLight` + 一盏 `DirectionalLight` | 极低 | 干净、平，适合扁平风格 |
| 环境贴图（HDRI）+ `MeshStandardMaterial` | 中 | 有真实反射，最显「质感」 |
| 多盏灯 + 阴影（`castShadow`） | 高 | 戏剧化，但阴影贴图很贵 |
| `MeshPhysicalMaterial` + `clearcoat` / `transmission` | 高 | 玻璃、车漆、陶瓷 |

```js
// 环境光照：一行代码把「塑料」变成「有反射的材质」
import { RoomEnvironment } from 'three/addons/environments/RoomEnvironment.js';
const pmrem = new THREE.PMREMGenerator(renderer);
scene.environment = pmrem.fromScene(new RoomEnvironment(), 0.04).texture;
```

**阴影三条**：能不用就不用；要用就把 `shadow.mapSize` 控制在 1024；`shadow.camera` 范围收紧到主体，别覆盖整个场景。

## 5. 材质与配色

- `MeshStandardMaterial` 是默认选择：`roughness` 0.3–0.7、`metalness` 0–0.2 最像真实材质。
- **全金属 + 全反射 = 廉价**（像十年前的渲染图）。留一处高光就够。
- 颜色不要用纯 `0xffffff` / `0x000000`，用带色相的白（`0xfaf8f5`）和暖黑（`0x2c2c2a`）。
- 半透明要开 `transparent: true` 并接受排序问题；能用 `opacity` 渐变就别用真透明。

## 6. 性能预算

| 指标 | 桌面 | 移动 |
| --- | --- | --- |
| 三角面 | < 500k | < 100k |
| draw call | < 150 | < 60 |
| 纹理 | 2k 够用 | 1k |
| 帧率 | 60fps | 30fps 可接受 |

优化顺序（按性价比）：

1. **InstancedMesh** 批量渲染同几何体（粒子、网格、树木）
2. 合并静态几何体（`BufferGeometryUtils.mergeGeometries`）
3. 纹理压缩与 `texture.anisotropy` 收敛
4. 视锥剔除默认开启，别手动关
5. 按需渲染：静止时不跑 `setAnimationLoop`，只在交互/动画时渲染

```js
// 静止即停：省电，也省风扇
let running = true;
renderer.setAnimationLoop(() => {
  if (!running) return;
  renderer.render(scene, camera);
});
observer = new IntersectionObserver(([e]) => { running = e.isIntersecting; });
observer.observe(canvas);
```

**内存泄漏**是 3D 项目最常见的线上事故：切路由时 `geometry.dispose()`、`material.dispose()`、`texture.dispose()`、`renderer.dispose()` 必须调用，否则显存一路涨到崩。

## 7. 与滚动、GSAP 结合

3D 的编排交给 GSAP，别自己算缓动：

```js
import gsap from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

// 相机运镜跟着滚动走
gsap.to(camera.position, {
  z: 2.2, y: 0.4,
  ease: 'none',                       // scrub 场景必须 none，否则滚动与画面脱节
  scrollTrigger: { trigger: '#stage', start: 'top top', end: '+=1200', scrub: 1 }
});

// 材质参数也能补间
gsap.to(mat, { roughness: 0.1, duration: 1.2, scrollTrigger: { trigger: '#stage', scrub: true } });
```

**scrub 场景禁用 `ease`**：滚动本身就是时间轴，再加缓动会出现「手停了画面还在跑」。

## 8. 交互

```js
const raycaster = new THREE.Raycaster();
const pointer = new THREE.Vector2();

canvas.addEventListener('pointermove', (e) => {
  const r = canvas.getBoundingClientRect();
  pointer.x = ((e.clientX - r.left) / r.width) * 2 - 1;
  pointer.y = -((e.clientY - r.top) / r.height) * 2 + 1;
  raycaster.setFromCamera(pointer, camera);
  const hit = raycaster.intersectObject(mesh, false)[0];
  canvas.style.cursor = hit ? 'pointer' : 'default';
});
```

拾取只在 `pointermove` 里做，别放进渲染循环（每帧射线检测是纯浪费）。移动端没有 hover，改用 `pointerdown` 命中后直接切换状态。

## 9. 无障碍与降级（硬要求）

1. `prefers-reduced-motion: reduce` 时**停止自动旋转、视差运镜、循环动画**，保留静态一帧。
2. 必须准备**静态兜底图**：`<canvas>` 里先放一张 poster，WebGL 不可用时它就是内容。
3. 3D 不能是唯一的信息载体：结构说明要同时给文字或图注。
4. 键盘用户：可交互 3D 元素要有对应的 DOM 按钮，不要指望用 Tab 走进 canvas。

```html
<canvas id="stage" aria-hidden="true"></canvas>
<p class="sr-only">产品外观：墨绿色哑光外壳，圆角矩形，顶部有一圈古铜色装饰线。</p>
```

## 10. 廉价信号清单

- [ ] 黑底 + 荧光绿线框 + 无限旋转 —— 2015 年科技感
- [ ] 纯 `0xffffff` 高光、`metalness: 1`、`roughness: 0` 的「不锈钢球」
- [ ] 相机永远在正前方，物体永远在正中
- [ ] 加了三盏以上灯但没有主次，画面全亮没有阴影层次
- [ ] 阴影贴图边缘锯齿明显（`mapSize` 太小或范围太大）
- [ ] 页面滚动时 3D 抖动（用了 `window.scrollY` + 非 `passive` 监听）
- [ ] 移动端直接白屏（没做 WebGL 检测与降级）
