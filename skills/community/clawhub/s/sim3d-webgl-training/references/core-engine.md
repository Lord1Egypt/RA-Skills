# core-engine.md — 引擎核心（零推导，直接复制）

> 全部代码提取自已验证的 9 个高逼真样本。复制后**只改业务参数**（部件几何、颜色、文案），不改架构。

## §1 HTML 骨架 + CSS（双画布三栏工作台）

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>【业务名称】3D高仿真虚拟仿真实训系统</title>
<link rel="icon" href="data:,">
<style>
  :root {
    --bg-dark: #070a0f;
    --panel-bg: rgba(11, 16, 25, 0.88);
    --panel-border: rgba(64, 156, 255, 0.24);
    --text-main: #e2e8f0;
    --text-muted: #94a3b8;
    --accent-cyan: #38bdf8;
    --accent-blue: #3b82f6;
    --accent-amber: #f59e0b;
    --accent-red: #ef4444;
    --accent-emerald: #10b981;
    --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
    --font-mono: "JetBrains Mono", Consolas, Menlo, monospace;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; user-select: none; -webkit-user-select: none; }
  html, body { width: 100vw; height: 100vh; overflow: hidden; background: var(--bg-dark); color: var(--text-main); font-family: var(--font-sans); font-size: 13px; }

  /* 3D 视口容器：底层 WebGL + 顶层 2D 叠加 */
  #viewport-container {
    position: absolute; inset: 0; overflow: hidden;
    background: radial-gradient(circle at 50% 46%, #18263a 0%, #0b121e 56%, #05070b 100%);
  }
  #gl-canvas { width: 100%; height: 100%; display: block; cursor: grab; }
  #gl-canvas:active { cursor: grabbing; }
  #hud-canvas { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; z-index: 2; }

  /* 蓝图网格背景 */
  .blueprint-grid {
    position: absolute; inset: 0; pointer-events: none; z-index: 1;
    background-image:
      linear-gradient(rgba(56, 189, 248, 0.035) 1px, transparent 1px),
      linear-gradient(90deg, rgba(56, 189, 248, 0.035) 1px, transparent 1px);
    background-size: 40px 40px;
  }

  /* 顶栏 */
  #top-bar {
    position: absolute; top: 12px; left: 16px; right: 16px; height: 52px;
    background: var(--panel-bg); backdrop-filter: blur(16px);
    border: 1px solid var(--panel-border); border-radius: 10px;
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 16px; z-index: 10; box-shadow: 0 8px 32px rgba(0,0,0,0.55);
  }
  .btn-chip {
    background: rgba(30, 41, 59, 0.78); color: #cbd5e1;
    border: 1px solid rgba(148, 163, 184, 0.22);
    padding: 5px 9px; border-radius: 6px; font-size: 11px; cursor: pointer;
    display: inline-flex; align-items: center; gap: 4px; white-space: nowrap;
  }
  .btn-chip:hover { background: rgba(56,189,248,0.18); color: #fff; border-color: rgba(56,189,248,0.5); }
  .btn-chip.active {
    background: linear-gradient(135deg, rgba(14,165,233,0.34), rgba(37,99,235,0.34));
    color: #38bdf8; border-color: #38bdf8; box-shadow: 0 0 10px rgba(56,189,248,0.25);
  }

  /* 左右侧板 */
  .side-panel {
    position: absolute; top: 74px; bottom: 92px; width: 326px;
    background: var(--panel-bg); backdrop-filter: blur(16px);
    border: 1px solid var(--panel-border); border-radius: 10px;
    z-index: 10; display: flex; flex-direction: column; overflow: hidden;
  }
  #left-panel { left: 16px; }
  #right-panel { right: 16px; }

  /* 底部坞 */
  #bottom-dock {
    position: absolute; left: 16px; right: 16px; bottom: 12px; height: 68px;
    background: var(--panel-bg); backdrop-filter: blur(16px);
    border: 1px solid var(--panel-border); border-radius: 10px; z-index: 10;
    display: flex; align-items: center; gap: 14px; padding: 0 16px;
  }
  input[type="range"] { accent-color: var(--accent-cyan); flex: 1; }

  /* KPI 卡片网格 */
  .kpi-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 6px; }
  .kpi-card { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(148,163,184,0.14); border-radius: 7px; padding: 6px 9px; }
  .kpi-label { font-size: 10px; color: var(--text-muted); }
  .kpi-val { font-size: 16px; font-weight: 700; font-family: var(--font-mono); color: #f8fafc; }
  .kpi-unit { font-size: 10px; color: var(--text-muted); margin-left: 3px; }

  /* 部件树 */
  .comp-item {
    display: flex; align-items: center; gap: 7px; padding: 5px 8px; border-radius: 6px;
    font-size: 11.5px; cursor: pointer; border: 1px solid transparent;
  }
  .comp-item:hover { background: rgba(56,189,248,0.1); }
  .comp-item.selected { background: rgba(14,116,144,0.3); border-color: var(--accent-cyan); color: #bae6fd; }
  .comp-dot { width: 8px; height: 8px; border-radius: 2px; flex-shrink: 0; }

  /* 悬浮提示 */
  #hover-tooltip {
    position: fixed; display: none; z-index: 50; pointer-events: none;
    background: rgba(10,15,25,0.94); border: 1px solid rgba(56,189,248,0.4);
    padding: 5px 10px; border-radius: 6px; font-size: 11.5px; color: #e2e8f0;
  }
</style>
</head>
<body>
<div id="viewport-container">
  <canvas id="gl-canvas"></canvas>
  <div class="blueprint-grid"></div>
  <canvas id="hud-canvas"></canvas>
</div>

<header id="top-bar">
  <div class="brand-group">
    <div class="brand-badge">3D</div>
    <div>
      <h1>【系统名称】 <span class="spec-tag">WebGL PBR</span></h1>
      <div class="brand-subtitle">【副标题/专业名】</div>
    </div>
  </div>
  <div class="top-actions">
    <button class="btn-chip" data-cam onclick="setCameraPreset('iso', this)">等轴视</button>
    <button class="btn-chip" data-cam onclick="setCameraPreset('detail', this)">细节视</button>
    <button class="btn-chip" id="btn-auto-orbit" onclick="toggleAutoOrbit(this)">自动旋转</button>
  </div>
</header>

<aside class="side-panel" id="left-panel">
  <!-- 模块 1：结构认知与拆解（部件树 + 详情卡） -->
</aside>

<aside class="side-panel" id="right-panel">
  <!-- 模块 2-4：原理仿真图表 / SOP 工卡 / 考核面板 -->
</aside>

<footer id="bottom-dock">
  <!-- 播放控制 / 相位滑块 / 全局参数 -->
</footer>

<div id="hover-tooltip"></div>
<script>
/* ======== 以下按 §2→§5 顺序组装 ======== */
</script>
</body>
</html>
```

**布局变体**：
- 原理仿真型（内燃机式）：左=部件树+特征开关，右=KPI+实时图表（P-V 图/相位盘/波形），底=播放控制+相位滑块
- SOP 实操型（Model Y 式）：左=实训模块列表+SOP 步骤卡，右=虚拟仪器（万用表/示波器/OBD 标签页），底=PPE 穿戴坞+工具开关
- 场景漫游型（安检/空港式）：顶部 nav-tabs 切换工位模块（1→6 编号），左=岗位 SOP 知识卡，右=考核反馈

## §2 Mat4 数学库（全量复制）

```js
const Mat4 = {
  identity() { return new Float32Array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]); },
  multiply(a, b) {
    const out = new Float32Array(16);
    for (let i = 0; i < 4; i++) {
      const ai0 = a[i], ai1 = a[i+4], ai2 = a[i+8], ai3 = a[i+12];
      out[i]    = ai0*b[0]  + ai1*b[1]  + ai2*b[2]  + ai3*b[3];
      out[i+4]  = ai0*b[4]  + ai1*b[5]  + ai2*b[6]  + ai3*b[7];
      out[i+8]  = ai0*b[8]  + ai1*b[9]  + ai2*b[10] + ai3*b[11];
      out[i+12] = ai0*b[12] + ai1*b[13] + ai2*b[14] + ai3*b[15];
    }
    return out;
  },
  perspective(fovyRad, aspect, near, far) {
    const f = 1.0 / Math.tan(fovyRad * 0.5);
    const nf = 1.0 / (near - far);
    return new Float32Array([
      f / aspect, 0, 0, 0,
      0, f, 0, 0,
      0, 0, (far + near) * nf, -1,
      0, 0, (2 * far * near) * nf, 0
    ]);
  },
  lookAt(eye, center, up) {
    let zx = eye[0]-center[0], zy = eye[1]-center[1], zz = eye[2]-center[2];
    let len = Math.hypot(zx, zy, zz) || 1;
    zx /= len; zy /= len; zz /= len;
    let xx = up[1]*zz - up[2]*zy, xy = up[2]*zx - up[0]*zz, xz = up[0]*zy - up[1]*zx;
    len = Math.hypot(xx, xy, xz) || 1;
    xx /= len; xy /= len; xz /= len;
    const yx = zy*xz - zz*xy, yy = zz*xx - zx*xz, yz = zx*xy - zy*xx;
    return new Float32Array([
      xx, yx, zx, 0,
      xy, yy, zy, 0,
      xz, yz, zz, 0,
      -(xx*eye[0] + xy*eye[1] + xz*eye[2]),
      -(yx*eye[0] + yy*eye[1] + yz*eye[2]),
      -(zx*eye[0] + zy*eye[1] + zz*eye[2]),
      1
    ]);
  },
  translate(m, x, y, z) { const t = Mat4.identity(); t[12]=x; t[13]=y; t[14]=z; return Mat4.multiply(m, t); },
  rotateX(m, rad) { const c=Math.cos(rad), s=Math.sin(rad); const r=Mat4.identity(); r[5]=c; r[6]=s; r[9]=-s; r[10]=c; return Mat4.multiply(m, r); },
  rotateY(m, rad) { const c=Math.cos(rad), s=Math.sin(rad); const r=Mat4.identity(); r[0]=c; r[2]=-s; r[8]=s; r[10]=c; return Mat4.multiply(m, r); },
  rotateZ(m, rad) { const c=Math.cos(rad), s=Math.sin(rad); const r=Mat4.identity(); r[0]=c; r[1]=s; r[4]=-s; r[5]=c; return Mat4.multiply(m, r); },
  scale(m, sx, sy, sz) { const s=Mat4.identity(); s[0]=sx; s[5]=sy; s[10]=sz; return Mat4.multiply(m, s); },
  // TRS 一步到位（位置+欧拉角+缩放）。⚠️ 非均匀缩放安全：顶点着色器已做法线矩阵重归一化（§3）
  trs(tx, ty, tz, rx = 0, ry = 0, rz = 0, sx = 1, sy = 1, sz = 1) {
    const cx=Math.cos(rx), sx_=Math.sin(rx), cy=Math.cos(ry), sy_=Math.sin(ry), cz=Math.cos(rz), sz_=Math.sin(rz);
    return new Float32Array([
      (cy*cz)*sx, (cz*sx_*sy_ + cx*sz_)*sx, (-cx*cz*sy_ + sx_*sz_)*sx, 0,
      (-cy*sz_)*sy, (cx*cz - sx_*sy_*sz_)*sy, (cz*sx_ + cx*sy_*sz_)*sy, 0,
      (sy_)*sz, (-cy*sx_)*sz, (cx*cy)*sz, 0,
      tx, ty, tz, 1
    ]);
  },
  // 3D 点 → 2D 屏幕坐标（供引线标注/热点用）
  projectPoint(pt3, mvp, width, height) {
    const x = pt3[0], y = pt3[1], z = pt3[2];
    const cx = mvp[0]*x + mvp[4]*y + mvp[8]*z + mvp[12];
    const cy = mvp[1]*x + mvp[5]*y + mvp[9]*z + mvp[13];
    const cw = mvp[3]*x + mvp[7]*y + mvp[11]*z + mvp[15];
    if (cw <= 0.05) return null;
    return [
      ((cx / cw) * 0.5 + 0.5) * width,
      (1.0 - ((cy / cw) * 0.5 + 0.5)) * height,
      cw
    ];
  }
};
```

## §3 着色器（WebGL2 GLSL ES 3.0，含法线矩阵重归一化 + 三点工业布光）

**顶点着色器**——法线矩阵重归一化写法（A320 已验证样本原版），**不可删**：

```js
const PBR_VS = `#version 300 es
precision highp float;
layout(location = 0) in vec3 aPosition;
layout(location = 1) in vec3 aNormal;

uniform mat4 uModel;
uniform mat4 uViewProj;

out vec3 vWorldPos;
out vec3 vNormal;
out vec3 vLocalPos;

void main() {
  vec4 wp = uModel * vec4(aPosition, 1.0);
  vWorldPos = wp.xyz;
  // 法线矩阵重归一化：normalize 作用于"变换后的法线向量"（⚠️ normalize(mat3(...)) 是非法 GLSL，会编译报错）
  vNormal = normalize(mat3(uModel[0].xyz, uModel[1].xyz, uModel[2].xyz) * aNormal);
  vLocalPos = aPosition;
  gl_Position = uViewProj * wp;
}
`;
```

**片元着色器**——GGX PBR + 程序化工作室环境反射 + Fresnel 边缘光 + 4 种程序化表面细节：

```js
const PBR_FS = `#version 300 es
precision highp float;

in vec3 vWorldPos;
in vec3 vNormal;
in vec3 vLocalPos;

uniform vec3 uCameraPos;
uniform vec3 uBaseColor;
uniform float uMetallic;
uniform float uRoughness;
uniform float uAlpha;
uniform float uEmissive;
uniform float uHighlight;
uniform int uSurfaceType;   // 0纯色 1珩磨网纹 2车削纹 3铸造颗粒
uniform int uIsFloor;       // 1 = 程序化车间网格地面

out vec4 fragColor;

const float PI = 3.14159265359;

// 程序化工作室环境反射（天光渐变 + 两条面光带 + 边缘补光）
vec3 sampleStudioEnv(vec3 R, float rough) {
  float y = clamp(R.y, -1.0, 1.0);
  vec3 skyTop = vec3(0.35, 0.48, 0.68);
  vec3 horizon = vec3(0.85, 0.90, 0.98);
  vec3 ground = vec3(0.06, 0.08, 0.12);
  vec3 env = y > 0.0 ? mix(horizon, skyTop, pow(y, 0.55)) : mix(horizon * 0.4, ground, pow(-y, 0.6));
  float sb1 = pow(max(0.0, dot(R, normalize(vec3(0.6, 0.75, 0.4)))), mix(28.0, 4.0, rough));
  float sb2 = pow(max(0.0, dot(R, normalize(vec3(-0.7, 0.4, 0.6)))), mix(24.0, 4.0, rough));
  float rim = pow(max(0.0, dot(R, normalize(vec3(0.0, 0.3, -0.95)))), mix(18.0, 3.0, rough));
  env += vec3(1.2, 1.15, 1.05) * sb1 * (1.0 - rough * 0.6);
  env += vec3(0.65, 0.82, 1.1) * sb2 * (1.0 - rough * 0.6);
  env += vec3(0.4, 0.65, 1.0) * rim * 0.7;
  return env;
}

float DistributionGGX(vec3 N, vec3 H, float roughness) {
  float a = roughness * roughness;
  float a2 = a * a;
  float NdotH = max(dot(N, H), 0.0);
  float denom = (NdotH * NdotH * (a2 - 1.0) + 1.0);
  return a2 / max(PI * denom * denom, 0.0001);
}

float GeometrySchlickGGX(float NdotV, float roughness) {
  float r = roughness + 1.0;
  float k = (r * r) / 8.0;
  return NdotV / (NdotV * (1.0 - k) + k);
}

void main() {
  vec3 N = normalize(vNormal);
  vec3 V = normalize(uCameraPos - vWorldPos);
  if (dot(N, V) < 0.0 && uAlpha < 0.99) N = -N;   // 半透明件背面翻转，避免双面黑

  // 车间环氧地坪：程序化网格线 + 中心渐亮
  if (uIsFloor == 1) {
    vec2 g = abs(fract(vWorldPos.xz * 0.5) - 0.5) / fwidth(vWorldPos.xz * 0.5);
    float line = 1.0 - min(min(g.x, g.y), 1.0);
    vec3 floorCol = mix(uBaseColor, vec3(0.13, 0.35, 0.55), line * 0.7);
    float vign = 1.0 - 0.35 * length(vWorldPos.xz) * 0.08;
    fragColor = vec4(floorCol * (0.85 + 0.3 * max(dot(N, normalize(vec3(0.4, 0.9, 0.2))), 0.0)) * vign, 1.0);
    return;
  }

  float rough = clamp(uRoughness, 0.05, 0.98);
  vec3 albedo = uBaseColor;

  // 程序化表面细节（按 uSurfaceType 叠加法线/粗糙度扰动）
  if (uSurfaceType == 1) {          // 珩磨交叉网纹（缸套/研磨面）
    float angle = atan(vLocalPos.z, vLocalPos.x);
    float h1 = sin(angle * 36.0 + vLocalPos.y * 55.0);
    float h2 = sin(angle * 36.0 - vLocalPos.y * 55.0);
    float crossHatch = (h1 * h2) * 0.035;
    N = normalize(N + vec3(crossHatch, crossHatch * 0.5, crossHatch));
    albedo *= (0.96 + 0.06 * crossHatch);
  } else if (uSurfaceType == 2) {   // 车削环形纹（轴类/盘类）
    float groove = sin(vLocalPos.y * 140.0 + length(vLocalPos.xz) * 90.0) * 0.02;
    rough = clamp(rough + groove, 0.05, 0.95);
  } else if (uSurfaceType == 3) {   // 铸造颗粒（缸体/壳体）
    float grain = fract(sin(dot(floor(vLocalPos * 65.0), vec3(12.9898, 78.233, 37.719))) * 43758.5453);
    rough = clamp(rough + (grain - 0.5) * 0.08, 0.1, 0.95);
    albedo *= (0.95 + 0.08 * grain);
  }

  vec3 F0 = mix(vec3(0.04), albedo, uMetallic);
  vec3 Lo = vec3(0.0);

  // 三点工业布光：主光(暖白) + 冷色补光(左上) + 底部轮廓光
  vec3 lightDirs[3] = vec3[3](
    normalize(vec3(0.55, 0.75, 0.62)),
    normalize(vec3(-0.68, 0.35, 0.48)),
    normalize(vec3(0.15, -0.65, -0.75))
  );
  vec3 lightCols[3] = vec3[3](
    vec3(2.4, 2.35, 2.25),
    vec3(1.15, 1.35, 1.65),
    vec3(0.65, 0.75, 0.95)
  );

  for (int i = 0; i < 3; i++) {
    vec3 L = lightDirs[i];
    vec3 H = normalize(V + L);
    float NdotL = max(dot(N, L), 0.0);
    float NdotV = max(dot(N, V), 0.001);
    float D = DistributionGGX(N, H, rough);
    float G = GeometrySchlickGGX(NdotV, rough) * GeometrySchlickGGX(NdotL, rough);
    vec3 F = F0 + (1.0 - F0) * pow(clamp(1.0 - max(dot(H, V), 0.0), 0.0, 1.0), 5.0);
    vec3 spec = (D * G * F) / max(4.0 * NdotV * NdotL, 0.001);
    vec3 kD = (vec3(1.0) - F) * (1.0 - uMetallic);
    Lo += (kD * albedo / PI + spec) * lightCols[i] * NdotL;
  }

  // IBL 环境反射 + Fresnel
  vec3 R = reflect(-V, N);
  vec3 envLight = sampleStudioEnv(R, rough);
  vec3 F_ibl = F0 + (max(vec3(1.0 - rough), F0) - F0) * pow(clamp(1.0 - max(dot(N, V), 0.0), 0.0, 1.0), 5.0);
  vec3 ambient = (1.0 - uMetallic) * albedo * vec3(0.22, 0.25, 0.30) + envLight * F_ibl * mix(0.95, 0.25, rough);

  vec3 color = ambient + Lo + albedo * uEmissive;

  // 选中/悬停青色描边高亮
  if (uHighlight > 0.01) {
    float rim = pow(1.0 - max(dot(N, V), 0.0), 2.0);
    color += vec3(0.22, 0.74, 0.98) * (0.32 + 0.85 * rim) * uHighlight;
  }

  // ACES 色调映射 + gamma 校正
  color = (color * (2.51 * color + 0.03)) / (color * (2.43 * color + 0.59) + 0.14);
  color = pow(clamp(color, 0.0, 1.0), vec3(1.0 / 2.2));

  fragColor = vec4(color, uAlpha);
}
`;
```

**粒子着色器**（烟/气流/火花/冷却液流）：

```js
const PARTICLE_VS = `#version 300 es
precision highp float;
layout(location = 0) in vec3 aPos;
layout(location = 1) in vec4 aColor;
layout(location = 2) in float aSize;
uniform mat4 uViewProj;
uniform float uViewportScale;
out vec4 vColor;
void main() {
  vColor = aColor;
  vec4 clip = uViewProj * vec4(aPos, 1.0);
  gl_Position = clip;
  gl_PointSize = clamp(aSize * uViewportScale / max(clip.w, 0.2), 2.0, 95.0);
}
`;
const PARTICLE_FS = `#version 300 es
precision highp float;
in vec4 vColor;
out vec4 fragColor;
void main() {
  vec2 uv = gl_PointCoord * 2.0 - 1.0;
  float r2 = dot(uv, uv);
  if (r2 > 1.0) discard;
  fragColor = vec4(vColor.rgb, vColor.a * pow(1.0 - r2, 1.75));
}
`;
```

**着色器编译辅助**（带错误日志，禁止静默失败）：

```js
function createShaderProgram(gl, vsSource, fsSource) {
  const compile = (type, src) => {
    const s = gl.createShader(type);
    gl.shaderSource(s, src);
    gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) {
      console.error('Shader compile error:', gl.getShaderInfoLog(s));
    }
    return s;
  };
  const prog = gl.createProgram();
  gl.attachShader(prog, compile(gl.VERTEX_SHADER, vsSource));
  gl.attachShader(prog, compile(gl.FRAGMENT_SHADER, fsSource));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
    console.error('Program link error:', gl.getProgramInfoLog(prog));
  }
  return prog;
}
```

**WebGL2 初始化（带 WebGL1 兜底提示）**：

```js
const canvas = document.getElementById('gl-canvas');
const gl = canvas.getContext('webgl2', { antialias: true, alpha: false, depth: true })
        || canvas.getContext('webgl', { antialias: true, alpha: false, depth: true });
if (!gl) {
  document.getElementById('viewport-container').innerHTML =
    '<div style="display:flex;height:100%;align-items:center;justify-content:center;color:#94a3b8;">当前浏览器不支持 WebGL，请使用 Chrome / Edge 浏览器打开</div>';
}
```

## §4 主循环（固定骨架）

```js
window.addEventListener('DOMContentLoaded', () => {
  // gl 初始化 → createShaderProgram ×2 → buildAllMeshes(gl) → initParticles(gl)
  // → initUI() → setupViewportInteractions(canvas)
  gl.enable(gl.DEPTH_TEST);
  gl.enable(gl.BLEND);
  gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);

  let lastTime = performance.now();

  function renderScene(now, dt) {
    // 1. DPR 自适应 resize
    const dpr = window.devicePixelRatio || 1;
    const viewW = canvas.clientWidth, viewH = canvas.clientHeight;
    if (canvas.width !== viewW * dpr || canvas.height !== viewH * dpr) {
      canvas.width = viewW * dpr;
      canvas.height = viewH * dpr;
    }
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 0.0, 0.0);
    gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

    // 2. 推进模拟状态（业务：角度/动画时钟/人物插值）
    stepSimulation(dt);

    // 3. 相机阻尼更新
    Camera.update(dt, viewW / Math.max(1, viewH));

    // 4. Pass 1：不透明实心部件（depthMask(true)）
    renderOpaquePass();

    // 5. Pass 2：半透明外壳 / 粒子（depthMask(false)）
    renderTransparentPass();

    // 6. 2D 叠加层（引线标注 / 力矢量 / 图例）
    render2DOverlay();

    // 7. HUD DOM 更新（KPI / 图表）——每帧或降频
    updateLiveHUD();
  }

  function frame(now) {
    const dt = Math.min(0.05, (now - lastTime) / 1000.0);
    lastTime = now;
    renderScene(now, dt);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
});
```

## §5 相机控制器（阻尼轨道相机，全量复制）

```js
const Camera = {
  yaw: 0.24, pitch: 0.14, dist: 9.6, target: [0, 1.32, 0],
  goalYaw: 0.24, goalPitch: 0.14, goalDist: 9.6, goalTarget: [0, 1.32, 0],
  eye: [0, 0, 9.6],
  viewProj: Mat4.identity(),
  autoOrbit: false,

  update(dt, aspect) {
    if (this.autoOrbit) this.goalYaw += dt * 0.38;
    const lerp = Math.min(1.0, dt * 8.5);   // 阻尼系数：所有运动平滑插值
    this.yaw += (this.goalYaw - this.yaw) * lerp;
    this.pitch += (this.goalPitch - this.pitch) * lerp;
    this.dist += (this.goalDist - this.dist) * lerp;
    for (let i = 0; i < 3; i++) this.target[i] += (this.goalTarget[i] - this.target[i]) * lerp;
    const cp = Math.cos(this.pitch), sp = Math.sin(this.pitch);
    const cy = Math.cos(this.yaw), sy = Math.sin(this.yaw);
    this.eye = [
      this.target[0] + this.dist * cp * sy,
      this.target[1] + this.dist * sp,
      this.target[2] + this.dist * cp * cy
    ];
    const view = Mat4.lookAt(this.eye, this.target, [0, 1, 0]);
    const proj = Mat4.perspective(38.0 * Math.PI / 180.0, aspect, 0.15, 65.0);
    this.viewProj = Mat4.multiply(proj, view);
  }
};

function setCameraPreset(preset, btnEl) {
  document.querySelectorAll('[data-cam]').forEach(b => b.classList.remove('active'));
  if (btnEl) btnEl.classList.add('active');
  Camera.autoOrbit = false;
  // 业务自定义预设位，示例：
  if (preset === 'iso')      { Camera.goalYaw = 0.52; Camera.goalPitch = 0.22; Camera.goalDist = 9.8; Camera.goalTarget = [0, 1.3, 0]; }
  else if (preset === 'detail') { Camera.goalYaw = 0.14; Camera.goalPitch = 0.06; Camera.goalDist = 5.2; Camera.goalTarget = [0, 2.3, 0]; }
}
```

## §6 Web Audio 音效合成（无音频文件）

```js
let audioCtx = null;

function playSynthSound(kind) {
  const AC = window.AudioContext || window.webkitAudioContext;
  if (!AC) return;
  if (!audioCtx) audioCtx = new AC();
  if (audioCtx.state === 'suspended') audioCtx.resume();
  const now = audioCtx.currentTime;
  const osc = audioCtx.createOscillator();
  const gain = audioCtx.createGain();

  if (kind === 'engine-pulse') {        // 发动机做功脉冲（低频轰鸣）
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(52, now);
    osc.frequency.exponentialRampToValueAtTime(28, now + 0.075);
    gain.gain.setValueAtTime(0.11, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08);
    osc.stop(now + 0.085);
  } else if (kind === 'beep') {         // 金属探测器/按键提示音
    osc.type = 'square';
    osc.frequency.setValueAtTime(880, now);
    gain.gain.setValueAtTime(0.06, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
    osc.stop(now + 0.13);
  } else if (kind === 'alarm') {        // 报警（安全违规）
    osc.type = 'sawtooth';
    osc.frequency.setValueAtTime(660, now);
    osc.frequency.setValueAtTime(520, now + 0.12);
    gain.gain.setValueAtTime(0.09, now);
    gain.gain.exponentialRampToValueAtTime(0.001, now + 0.3);
    osc.stop(now + 0.32);
  }
  osc.connect(gain);
  gain.connect(audioCtx.destination);
  osc.start(now);
}
```

> 必须在首次用户点击/按键后再创建 AudioContext（浏览器自动播放策略）。
