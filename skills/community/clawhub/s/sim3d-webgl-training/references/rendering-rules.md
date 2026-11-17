# rendering-rules.md — 渲染、叠加与交互规范（零推导，直接复制）

## §1 双通道渲染（防遮挡铁律）

**Pass 1 不透明 → Pass 2 半透明**。所有 drawMesh 调用按 alpha 分组：

```js
function renderSceneFrame() {
  // ---------- PASS 1: 不透明实心部件 ----------
  gl.depthMask(true);
  gl.disable(gl.BLEND);
  // 地面（uIsFloor=1）
  drawMesh(meshes.floor, Mat4.trs(0, -0.82, 0), [0.08, 0.12, 0.18], 0.55, 0.35, 1.0, 0.0, 1);
  // 所有 alpha === 1.0 的部件……
  renderOpaquePass();

  // ---------- PASS 2: 半透明外壳 / 粒子 / 光效 ----------
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
  gl.depthMask(false);                  // ★ 不写深度 → 不会挡死 Pass1 已画好的内部件
  renderTransparentPass();              // 透明外壳按"从远到近"排序绘制
  renderParticles();

  // ---------- 恢复状态 ----------
  gl.depthMask(true);
  gl.disable(gl.BLEND);
}
```

**外壳中空规范**（适用于机身/舱体/缸体/防护罩）：
1. 用 `addTubeSection` 弧段或 `buildLoftedShellMesh` 只建侧面+剖面，**不封整体端盖**
2. 正面（面向默认相机一侧）剖开 30%~50% 弧度：`arc0 = 0.92π, arc1 = 2.08π`
3. 剖切端面必须有面板（addTubeSection 自动生成），否则看到背面剔除破洞
4. 透明度用滑杆可调（0~1），默认 0.6~0.8

## §2 粒子系统（烟/气流/冷却液/火花）

```js
const NUM_PARTICLES = 220;
const particles = [];
let particleVAO = null, particlePosBuf = null, particleColBuf = null, particleSizeBuf = null;

function initParticles(gl) {
  for (let i = 0; i < NUM_PARTICLES; i++) {
    particles.push({
      rFrac: Math.sqrt(Math.random()) * 0.88,   // 均匀圆盘分布
      angle: Math.random() * Math.PI * 2,
      yFrac: Math.random(),
      speed: 0.6 + Math.random() * 1.4,
      phase: Math.random() * Math.PI * 2,
      sizeBase: 15.0 + Math.random() * 24.0
    });
  }
  particleVAO = gl.createVertexArray();
  gl.bindVertexArray(particleVAO);
  particlePosBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, particlePosBuf);
  gl.bufferData(gl.ARRAY_BUFFER, NUM_PARTICLES * 3 * 4, gl.DYNAMIC_DRAW);
  gl.enableVertexAttribArray(0);
  gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
  particleColBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, particleColBuf);
  gl.bufferData(gl.ARRAY_BUFFER, NUM_PARTICLES * 4 * 4, gl.DYNAMIC_DRAW);
  gl.enableVertexAttribArray(1);
  gl.vertexAttribPointer(1, 4, gl.FLOAT, false, 0, 0);
  particleSizeBuf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, particleSizeBuf);
  gl.bufferData(gl.ARRAY_BUFFER, NUM_PARTICLES * 1 * 4, gl.DYNAMIC_DRAW);
  gl.enableVertexAttribArray(2);
  gl.vertexAttribPointer(2, 1, gl.FLOAT, false, 0, 0);
  gl.bindVertexArray(null);
}

// 每帧：CPU 算位置颜色 → bufferSubData → POINTS 绘制（加法混合发光感）
function renderParticles(timeSec, stateFn) {
  const posArr = new Float32Array(NUM_PARTICLES * 3);
  const colArr = new Float32Array(NUM_PARTICLES * 4);
  const sizeArr = new Float32Array(NUM_PARTICLES);
  let ptr = 0;
  for (let i = 0; i < NUM_PARTICLES; i++) {
    const p = particles[i];
    // ★ stateFn(i, p, timeSec) 返回 {x,y,z, r,g,b,a, size} —— 业务粒子运动逻辑集中在这一个函数
    const s = stateFn(i, p, timeSec);
    posArr[ptr*3] = s.x; posArr[ptr*3+1] = s.y; posArr[ptr*3+2] = s.z;
    colArr[ptr*4] = s.r; colArr[ptr*4+1] = s.g; colArr[ptr*4+2] = s.b; colArr[ptr*4+3] = s.a;
    sizeArr[ptr] = s.size; ptr++;
  }
  gl.useProgram(partProg);
  gl.uniformMatrix4fv(gl.getUniformLocation(partProg, 'uViewProj'), false, Camera.viewProj);
  gl.uniform1f(gl.getUniformLocation(partProg, 'uViewportScale'), gl.canvas.height * 0.085);
  gl.bindVertexArray(particleVAO);
  gl.bindBuffer(gl.ARRAY_BUFFER, particlePosBuf);
  gl.bufferSubData(gl.ARRAY_BUFFER, 0, posArr);
  gl.bindBuffer(gl.ARRAY_BUFFER, particleColBuf);
  gl.bufferSubData(gl.ARRAY_BUFFER, 0, colArr);
  gl.bindBuffer(gl.ARRAY_BUFFER, particleSizeBuf);
  gl.bufferSubData(gl.ARRAY_BUFFER, 0, sizeArr);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE);   // 加法混合 = 火焰/能量流发光感
  gl.depthMask(false);
  gl.drawArrays(gl.POINTS, 0, ptr);
  gl.depthMask(true);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
}
```

**常用粒子配方**：
| 效果 | 颜色轨迹 | 混合 |
|---|---|---|
| 进气气流 | 蓝 rgb(0.12,0.72,0.98) 螺旋下沉 | 加法 |
| 压缩升温 | 蓝→黄红插值 + 半径收缩 | 加法 |
| 燃烧 | 白亮核心 + 橙红扩散 | 加法 |
| 排气 | 灰褐 rgb(0.52,0.45,0.40) 上浮消散 | 普通 |
| 冷却液流 | 青蓝沿管道路径 buildTubeMesh 顶点插值流动 | 加法 |
| 电弧/火花 | 白青高频抖动 `sin(t*90+i*7.3)*0.035` | 加法 |

## §3 2D 引线标注（hud-canvas 上绘制）

**数据结构**（3D 锚点每帧记录）：

```js
const leaderAnchors3D = [];   // 每帧由场景渲染函数重填
// 推入格式：
leaderAnchors3D.push({
  id: 'piston',                       // 对应部件 id（联动选中/悬停高亮）
  label: '锻造铝合金活塞',             // 主标签（≤10 字）
  sub: `瞬时速度 ${v.toFixed(1)} m/s`, // 副标签（实时数据/状态）
  pos: [x, y, z],                     // 3D 锚点（跟部件动！）
  side: 'left'                        // 引线拉向左/右栏
});
```

**布局与绘制**（列去重叠 + 折线引线 + 胶囊卡）：

```js
const projectedChips = [];   // 每帧记录屏幕包围盒 → hover/click 拾取用

function render2DOverlay() {
  const canvas = document.getElementById('hud-canvas');
  const ctx = canvas.getContext('2d');
  const dpr = window.devicePixelRatio || 1;
  const viewW = canvas.clientWidth, viewH = canvas.clientHeight;   // ★ 命名 viewW/viewH，禁用 h/w
  if (canvas.width !== viewW * dpr || canvas.height !== viewH * dpr) {
    canvas.width = viewW * dpr; canvas.height = viewH * dpr;
  }
  ctx.save();
  ctx.scale(dpr, dpr);
  ctx.clearRect(0, 0, viewW, viewH);

  projectedChips.length = 0;

  // 分左右两列
  const leftItems = [], rightItems = [];
  for (const item of leaderAnchors3D) {
    const scr = Mat4.projectPoint(item.pos, Camera.viewProj, viewW, viewH);
    if (!scr) continue;
    if (scr[0] < 340 || scr[0] > viewW - 350 || scr[1] < 80 || scr[1] > viewH - 100) continue;  // 视锥+面板外剔除
    const entry = { ...item, sx: scr[0], sy: scr[1] };
    (item.side === 'left' ? leftItems : rightItems).push(entry);
  }

  const boxW = 150, boxH = 34;
  const layoutColumn = (list, isLeft) => {
    list.sort((a, b) => a.sy - b.sy);
    for (let i = 0; i < list.length; i++) {
      let ly = list[i].sy;
      if (i > 0 && ly - list[i-1].ly < 44) ly = list[i-1].ly + 44;   // 垂直去重叠
      list[i].ly = Math.max(128, Math.min(viewH - 135, ly));
      list[i].lx = isLeft ? (356 + boxW) : (viewW - 372 - boxW);     // 对齐侧板内侧
    }
  };
  layoutColumn(leftItems, true);
  layoutColumn(rightItems, false);

  for (const it of [...leftItems, ...rightItems]) {
    const isSel = SimState.selectedPart === it.id;
    const isHov = SimState.hoveredPart === it.id;
    const col = isSel ? '#38bdf8' : (isHov ? '#fbbf24' : 'rgba(148, 163, 184, 0.65)');

    // 锚点圆
    ctx.beginPath();
    ctx.arc(it.sx, it.sy, isSel ? 4.5 : 3.2, 0, Math.PI * 2);
    ctx.fillStyle = isSel ? '#38bdf8' : '#e2e8f0';
    ctx.fill();

    // 折线引线（锚点 → 肘点 → 水平段）
    const elbowX = it.side === 'left' ? it.lx + 14 : it.lx - 14;
    ctx.beginPath();
    ctx.moveTo(it.sx, it.sy);
    ctx.lineTo(elbowX, it.ly);
    ctx.lineTo(it.lx, it.ly);
    ctx.strokeStyle = col;
    ctx.lineWidth = isSel ? 1.8 : 1.1;
    ctx.stroke();

    // 标签卡
    const bx = it.side === 'left' ? it.lx - boxW : it.lx;
    const by = it.ly - boxH * 0.5;
    ctx.fillStyle = isSel ? 'rgba(14, 116, 144, 0.88)' : 'rgba(10, 15, 25, 0.84)';
    ctx.strokeStyle = isSel ? '#38bdf8' : 'rgba(56, 189, 248, 0.28)';
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.roundRect(bx, by, boxW, boxH, 5);
    ctx.fill(); ctx.stroke();

    ctx.fillStyle = '#f8fafc';
    ctx.font = '600 11px -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif';
    ctx.fillText(it.label, bx + 7, by + 14);
    ctx.fillStyle = isSel ? '#bae6fd' : '#94a3b8';
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText(it.sub, bx + 7, by + 27);

    projectedChips.push({ id: it.id, name: it.label, x: bx, y: by, w: boxW, h: boxH, sx: it.sx, sy: it.sy });
  }
  ctx.restore();
}
```

## §4 交互：轨道/平移/缩放/拾取（含 5px 防误触阈值，全量复制）

```js
function setupViewportInteractions(canvas) {
  let dragging = false;
  let panMode = false;
  let startX = 0, startY = 0;
  let lastX = 0, lastY = 0;

  canvas.addEventListener('mousedown', (e) => {
    dragging = true;
    panMode = (e.button === 2 || e.button === 1 || e.shiftKey);
    startX = lastX = e.clientX;
    startY = lastY = e.clientY;
    Camera.autoOrbit = false;
  });

  window.addEventListener('mousemove', (e) => {
    const dx = e.clientX - lastX;
    const dy = e.clientY - lastY;
    lastX = e.clientX;
    lastY = e.clientY;

    if (dragging) {
      if (panMode) {
        Camera.goalTarget[0] -= dx * 0.006;
        Camera.goalTarget[1] += dy * 0.006;
      } else {
        Camera.goalYaw -= dx * 0.0075;
        Camera.goalPitch = Math.max(-1.35, Math.min(1.35, Camera.goalPitch + dy * 0.0075));
      }
      return;
    }

    // 悬停检测：优先 2D 标签卡，其次命中半径 28px 的锚点
    const rect = canvas.getBoundingClientRect();
    const mx = e.clientX - rect.left;
    const my = e.clientY - rect.top;
    let found = null;
    for (const ch of projectedChips) {
      if ((mx >= ch.x && mx <= ch.x + ch.w && my >= ch.y && my <= ch.y + ch.h) ||
          Math.hypot(mx - ch.sx, my - ch.sy) < 28) { found = ch; break; }
    }
    const tip = document.getElementById('hover-tooltip');
    if (found) {
      SimState.hoveredPart = found.id;
      canvas.style.cursor = 'pointer';
      tip.style.display = 'block';
      tip.style.left = `${e.clientX + 14}px`;
      tip.style.top = `${e.clientY + 14}px`;
      tip.textContent = `点击聚焦：${found.name}`;
    } else {
      SimState.hoveredPart = null;
      canvas.style.cursor = dragging ? 'grabbing' : 'grab';
      tip.style.display = 'none';
    }
  });

  window.addEventListener('mouseup', (e) => {
    // ★ 防误触铁律：位移 < 5px 才算"点击"，旋转视角不会误选零件
    if (dragging && Math.hypot(e.clientX - startX, e.clientY - startY) < 5) {
      if (SimState.hoveredPart) selectComponent(SimState.hoveredPart, true);
    }
    dragging = false;
  });

  canvas.addEventListener('contextmenu', e => e.preventDefault());

  canvas.addEventListener('wheel', (e) => {
    e.preventDefault();
    Camera.goalDist = Math.max(3.2, Math.min(20.0, Camera.goalDist + e.deltaY * 0.005));
  }, { passive: false });

  window.addEventListener('keydown', (e) => {
    if (e.code === 'Space') { e.preventDefault(); togglePlay(); }
    else if (e.code === 'ArrowRight') stepAngle(2);
    else if (e.code === 'ArrowLeft') stepAngle(-2);
  });
}
```

## §5 爆炸视图（拆解教学）

每个部件在渲染时叠加爆炸位移向量，幅度由 `SimState.explode (0..1)` 驱动：

```js
// 在部件组装函数里为每件定义爆炸方向（沿装配轴线向外）
const ex = SimState.explode;
const expPiston = [0, ex * 0.65, zOffset];     // 活塞沿缸轴上移
const expRod    = [0, 0, zOffset + ex * 0.95]; // 连杆沿轴向抽出
const expCrank  = [0, -ex * 1.05, zOffset];    // 曲轴下沉
const expHead   = [0, ex * 1.65, zOffset];     // 缸盖上移
const expBlock  = [-ex * 0.85, 0, zOffset - ex * 0.55]; // 缸体斜后方退开

let mPiston = Mat4.translate(Mat4.identity(), expPiston[0], st.yPin + expPiston[1], expPiston[2]);

// UI：滑杆 0-100% + 一键切换按钮
function toggleQuickExplode() {
  const target = SimState.explode > 0.2 ? 0 : 58;
  document.getElementById('slider-explode').value = target;
  updateExplode(target);
}
```

## §6 材质参数速查表

| 材质 | baseColor (RGB 0-1) | metallic | roughness | 用途 |
|---|---|---|---|---|
| 抛光钢 | [0.76, 0.79, 0.84] | 0.92 | 0.22 | 曲轴/轴类 |
| 铝合金 | [0.88, 0.91, 0.95] | 0.92 | 0.18 | 活塞/壳体 |
| 铸铁 | [0.34, 0.39, 0.46] | 0.78 | 0.34 | 缸体（配 surfaceType=3） |
| 黄铜/铜 | [0.92, 0.62, 0.22] | 0.94 | 0.16 | 轴瓦/接头/排气 |
| 橡胶 | [0.09, 0.10, 0.12] | 0.15 | 0.85 | 轮胎/密封圈/皮带 |
| 喷塑钢 | [0.04, 0.42, 0.78] | 0.75 | 0.32 | 举升机/设备外罩 |
| 安全黄 | [0.95, 0.62, 0.05] | 0.65 | 0.35 | 吊臂/警示/工具 |
| 高压橙 | [1.0, 0.42, 0.0] | 0.4 | 0.35 | HV 线缆/绝缘手套（emissive 0.1） |
| 玻璃/面屏 | [0.2, 0.9, 1.0] | 0.9 | 0.1 | alpha 0.55 半透明 Pass2 |
| 车漆 | [0.85, 0.86, 0.88] | 0.85 | 0.25 | 车身（可换任意色） |

## §7 场景组装套路（以车间为例）

```js
function renderWorkshop(liftY) {
  // 地面（唯一 uIsFloor=1）
  drawMesh(meshes.floor, Mat4.trs(0, -0.82, 0), [0.08, 0.12, 0.18], 0.55, 0.35, 1.0, 0.0, 1);

  // 双柱举升机：立柱 + 液压缸铬杆 + 黄色摆臂 + 橡胶垫块
  [-1.46, 1.46].forEach(lx => {
    drawMesh(meshes.unitBox, Mat4.trs(lx, 0.22, 0, 0,0,0, 0.22, 2.08, 0.26), [0.04, 0.42, 0.78], 0.75, 0.32);
    drawMesh(meshes.unitBox, Mat4.trs(lx, -0.79, 0, 0,0,0, 0.44, 0.04, 0.52), [0.18, 0.24, 0.32], 0.8, 0.4);
    drawMesh(meshes.cylY, Mat4.trs(lx*0.92, -0.15 + liftY*0.4, 0, 0,0,0, 0.045, 1.35, 0.045), [0.85, 0.90, 0.95], 0.95, 0.12);
    // 黄色摆臂 + 垫块……
  });
  // 顶部横梁
  drawMesh(meshes.unitBox, Mat4.trs(0, 1.28, 0, 0,0,0, 3.14, 0.12, 0.18), [0.04, 0.42, 0.78], 0.75, 0.32);

  // 工具车 / 剪叉平台 / 安全桩链……按同理拼装
}
```

**布局口诀**：主体设备居中（世界原点附近），左侧设备 x<0、右侧 x>0、人物站位在设备包围盒外 0.3~0.5 单位；相机 target 默认对准主体质心，dist ≈ 主体对角线 × 1.8。

## §8 质感细节清单（irb_6700 高分验证，P1 必需全覆盖）

"精致感"来自这些**可数据驱动的小细节**，每项 3–10 行代码，全部进渲染循环：

| # | 细节 | 实现要点 |
|---|---|---|
| 1 | **故障件呼吸高亮** | `em(id)`：激活故障件 emissive = 0.42+sin(now·0.008)·0.22；选中件 emissive 0.34 |
| 2 | **三色状态灯** | 柜顶圆柱叠 3 色：故障红 / LOTO断电黄 / 运行绿，`drawMesh(cylY, ..., color, 0.3, 0.2, 1.0, 0.55)` |
| 3 | **断路器手柄动画** | QF1 手柄 `mat4TRS(..., 0, rotY, 0, ...)`：合闸 rz=1.2 红柄，LOTO rz=0 绿柄 |
| 4 | **激光 TCP 光束** | 末端细长圆柱 + 高 emissive 0.85 + alpha 0.9，仅 powerOff=false 时绘制 |
| 5 | **电缆走线** | `buildTubeMesh([控制点...], 0.02~0.03, 10)` 预建 floorPower/floorEncoder/armDressLoop/forearmLoop 四条 |
| 6 | **透明 cowling 罩** | `buildLoftedShellMesh(stations)` 做电机整流罩，Pass2 alpha 0.28 半透明 + 爆炸时上移 |
| 7 | **外壳透视滑块** | `sl-alpha` range 8–95% → `state.shellAlpha` → Pass2 统一 alpha（含柜门/围栏/检视罩） |
| 8 | **爆炸虚线引导线** | HUD 层：explode>0.04 时对每部件画 (原位→爆炸位) `setLineDash([4,4])` 虚线 |
| 9 | **HUD 徽章避重叠** | `leaderOffset` 预调 + 4 轮 `screenCallouts` 包围盒下推算法（参照 §3） |
| 10 | **TCP 空间轨迹** | tcpHistory 55 点环形缓冲，HUD 层 polyline 3D 投影连线 |
| 11 | **螺栓/细节阵列** | 底座 8 螺栓 `for (b=0;b<8;b++)` 圆周布点；栅格/翅片用循环 addBox |
| 12 | **设备名牌/编号** | HUD 徽章含 `comp-code`（如 J1-BASE / ERR-2041），左栏列表同码 |

**实现模式**：全部通过 `em(id)` / `setLivePos(id, pt)` 两个闭包函数接入数据驱动——
`em` 供 drawMesh 的 emissive 参数，`setLivePos` 把部件实时世界坐标写回 `comp._livePos` 供 HUD 引线与相机飞跃使用。
