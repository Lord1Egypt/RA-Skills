# cad-library.md — 程序化 CAD 建模库（零推导，直接复制）

> 6 类曲面生成器 + 关节化 3D 技师人物。告别"积木方盒 Minecraft 感"。

## §1 MeshBuilder 类（内燃机样本全量版，推荐首选）

带法线的索引化网格累加器：先向 builder 里"添加基本体"，可对子块 `transformAll` / `appendBuilder` 做矩阵变换拼接，最后 `compile(gl)` 上传 GPU（VAO + Uint32 索引，支持大网格）。

```js
class MeshBuilder {
  constructor() { this.positions = []; this.normals = []; this.indices = []; }

  addVertex(px, py, pz, nx, ny, nz) {
    const idx = this.positions.length / 3;
    this.positions.push(px, py, pz);
    const len = Math.hypot(nx, ny, nz) || 1.0;
    this.normals.push(nx / len, ny / len, nz / len);
    return idx;
  }

  addQuad(i0, i1, i2, i3) { this.indices.push(i0, i1, i2, i0, i2, i3); }

  // 圆柱/圆台（可开弧段 arcStart..arcEnd 做剖切；capEnds 控制端盖）
  addCylinder(rTop, rBot, height, yCenter = 0, radialSegs = 40, arcStart = 0, arcEnd = Math.PI * 2, capEnds = true) {
    const y0 = yCenter - height * 0.5;
    const y1 = yCenter + height * 0.5;
    const slope = (rBot - rTop) / (height || 1);
    const baseIdx = this.positions.length / 3;
    for (let i = 0; i <= radialSegs; i++) {
      const u = i / radialSegs;
      const a = arcStart + u * (arcEnd - arcStart);
      const ca = Math.cos(a), sa = Math.sin(a);
      this.addVertex(rBot * ca, y0, rBot * sa, ca, slope, sa);
      this.addVertex(rTop * ca, y1, rTop * sa, ca, slope, sa);
    }
    for (let i = 0; i < radialSegs; i++) {
      const b = baseIdx + i * 2;
      this.addQuad(b, b + 1, b + 3, b + 2);
    }
    if (capEnds) {
      const cTop = this.addVertex(0, y1, 0, 0, 1, 0);
      for (let i = 0; i <= radialSegs; i++) {
        const a = arcStart + (i / radialSegs) * (arcEnd - arcStart);
        this.addVertex(rTop * Math.cos(a), y1, rTop * Math.sin(a), 0, 1, 0);
      }
      for (let i = 0; i < radialSegs; i++) this.indices.push(cTop, cTop + 1 + i + 1, cTop + 1 + i);
      const cBot = this.addVertex(0, y0, 0, 0, -1, 0);
      for (let i = 0; i <= radialSegs; i++) {
        const a = arcStart + (i / radialSegs) * (arcEnd - arcStart);
        this.addVertex(rBot * Math.cos(a), y0, rBot * Math.sin(a), 0, -1, 0);
      }
      for (let i = 0; i < radialSegs; i++) this.indices.push(cBot, cBot + 1 + i, cBot + 1 + i + 1);
    }
    return this;
  }

  // ★ 中空管段（内外壁+顶底环面+弧段端面）：缸体/套筒/剖切壳的万能件。
  // 弧段 < 2π 时自动生成剖切端面板 → 内部结构 100% 可见
  addTubeSection(rInner, rOuter, y0, y1, segs = 48, arcStart = 0, arcEnd = Math.PI * 2) {
    const bOut = this.positions.length / 3;
    for (let i = 0; i <= segs; i++) {
      const a = arcStart + (i / segs) * (arcEnd - arcStart);
      const c = Math.cos(a), s = Math.sin(a);
      this.addVertex(rOuter * c, y0, rOuter * s, c, 0, s);
      this.addVertex(rOuter * c, y1, rOuter * s, c, 0, s);
    }
    for (let i = 0; i < segs; i++) { const k = bOut + i * 2; this.addQuad(k, k + 1, k + 3, k + 2); }
    const bIn = this.positions.length / 3;
    for (let i = 0; i <= segs; i++) {
      const a = arcStart + (i / segs) * (arcEnd - arcStart);
      const c = Math.cos(a), s = Math.sin(a);
      this.addVertex(rInner * c, y0, rInner * s, -c, 0, -s);
      this.addVertex(rInner * c, y1, rInner * s, -c, 0, -s);
    }
    for (let i = 0; i < segs; i++) { const k = bIn + i * 2; this.addQuad(k, k + 2, k + 3, k + 1); }
    const bTop = this.positions.length / 3;
    for (let i = 0; i <= segs; i++) {
      const a = arcStart + (i / segs) * (arcEnd - arcStart);
      const c = Math.cos(a), s = Math.sin(a);
      this.addVertex(rInner * c, y1, rInner * s, 0, 1, 0);
      this.addVertex(rOuter * c, y1, rOuter * s, 0, 1, 0);
    }
    for (let i = 0; i < segs; i++) { const k = bTop + i * 2; this.addQuad(k, k + 1, k + 3, k + 2); }
    const bBot = this.positions.length / 3;
    for (let i = 0; i <= segs; i++) {
      const a = arcStart + (i / segs) * (arcEnd - arcStart);
      const c = Math.cos(a), s = Math.sin(a);
      this.addVertex(rInner * c, y0, rInner * s, 0, -1, 0);
      this.addVertex(rOuter * c, y0, rOuter * s, 0, -1, 0);
    }
    for (let i = 0; i < segs; i++) { const k = bBot + i * 2; this.addQuad(k, k + 2, k + 3, k + 1); }
    if (Math.abs((arcEnd - arcStart) - Math.PI * 2) > 0.02) {
      for (const [ang, nSign] of [[arcStart, -1], [arcEnd, 1]]) {
        const c = Math.cos(ang), s = Math.sin(ang);
        const nx = -s * nSign, nz = c * nSign;
        const i0 = this.addVertex(rInner * c, y0, rInner * s, nx, 0, nz);
        const i1 = this.addVertex(rOuter * c, y0, rOuter * s, nx, 0, nz);
        const i2 = this.addVertex(rOuter * c, y1, rOuter * s, nx, 0, nz);
        const i3 = this.addVertex(rInner * c, y1, rInner * s, nx, 0, nz);
        if (nSign > 0) this.addQuad(i0, i1, i2, i3);
        else this.addQuad(i0, i3, i2, i1);
      }
    }
    return this;
  }

  // 轴对齐盒（中心+尺寸）
  addBox(cx, cy, cz, sx, sy, sz) {
    const x0 = cx - sx*0.5, x1 = cx + sx*0.5;
    const y0 = cy - sy*0.5, y1 = cy + sy*0.5;
    const z0 = cz - sz*0.5, z1 = cz + sz*0.5;
    const faces = [
      { n: [0,0,1],  v: [[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]] },
      { n: [0,0,-1], v: [[x1,y0,z0],[x0,y0,z0],[x0,y1,z0],[x1,y1,z0]] },
      { n: [0,1,0],  v: [[x0,y1,z1],[x1,y1,z1],[x1,y1,z0],[x0,y1,z0]] },
      { n: [0,-1,0], v: [[x0,y0,z0],[x1,y0,z0],[x1,y0,z1],[x0,y0,z1]] },
      { n: [1,0,0],  v: [[x1,y0,z1],[x1,y0,z0],[x1,y1,z0],[x1,y1,z1]] },
      { n: [-1,0,0], v: [[x0,y0,z0],[x0,y0,z1],[x0,y1,z1],[x0,y1,z0]] }
    ];
    for (const f of faces) {
      const i0 = this.addVertex(...f.v[0], ...f.n);
      const i1 = this.addVertex(...f.v[1], ...f.n);
      const i2 = this.addVertex(...f.v[2], ...f.n);
      const i3 = this.addVertex(...f.v[3], ...f.n);
      this.addQuad(i0, i1, i2, i3);
    }
    return this;
  }

  // 螺旋弹簧（气门弹簧/回位弹簧/线缆盘绕）
  addHelicalSpring(R, wireR, turns, height, segsPerTurn = 24, tubeSegs = 10) {
    const totalSteps = Math.floor(turns * segsPerTurn);
    const baseIdx = this.positions.length / 3;
    for (let i = 0; i <= totalSteps; i++) {
      const u = i / totalSteps;
      const theta = u * turns * Math.PI * 2;
      const cx = R * Math.cos(theta);
      const cz = R * Math.sin(theta);
      const cy = u * height;
      const tx = -R * Math.sin(theta);
      const tz = R * Math.cos(theta);
      const ty = height / (turns * Math.PI * 2);
      const tLen = Math.hypot(tx, ty, tz) || 1;
      const nx = Math.cos(theta), nz = Math.sin(theta);
      const bx = -ty * nz / tLen;
      const by = (tz * nx - tx * nz) / tLen;
      const bz = ty * nx / tLen;
      for (let j = 0; j <= tubeSegs; j++) {
        const phi = (j / tubeSegs) * Math.PI * 2;
        const cp = Math.cos(phi), sp = Math.sin(phi);
        const vnx = cp * nx + sp * bx;
        const vny = sp * by;
        const vnz = cp * nz + sp * bz;
        this.addVertex(cx + wireR * vnx, cy + wireR * vny, cz + wireR * vnz, vnx, vny, vnz);
      }
    }
    const ringStride = tubeSegs + 1;
    for (let i = 0; i < totalSteps; i++) {
      for (let j = 0; j < tubeSegs; j++) {
        const a = baseIdx + i * ringStride + j;
        const b = a + ringStride;
        this.addQuad(a, b, b + 1, a + 1);
      }
    }
    return this;
  }

  // 2D 轮廓挤出体（凸轮桃形/曲柄平衡重/散热翅片/加强筋）
  addExtrudedPolygon(pts2d, z0, z1) {
    const n = pts2d.length;
    for (let i = 0; i < n; i++) {
      const p0 = pts2d[i];
      const p1 = pts2d[(i + 1) % n];
      const dx = p1[0] - p0[0], dy = p1[1] - p0[1];
      const nx = dy, ny = -dx;
      const i0 = this.addVertex(p0[0], p0[1], z1, nx, ny, 0);
      const i1 = this.addVertex(p1[0], p1[1], z1, nx, ny, 0);
      const i2 = this.addVertex(p1[0], p1[1], z0, nx, ny, 0);
      const i3 = this.addVertex(p0[0], p0[1], z0, nx, ny, 0);
      this.addQuad(i0, i1, i2, i3);
    }
    let cx = 0, cy = 0;
    for (const p of pts2d) { cx += p[0]; cy += p[1]; }
    cx /= n; cy /= n;
    const cFront = this.addVertex(cx, cy, z1, 0, 0, 1);
    for (let i = 0; i < n; i++) this.addVertex(pts2d[i][0], pts2d[i][1], z1, 0, 0, 1);
    for (let i = 0; i < n; i++) this.indices.push(cFront, cFront + 1 + i, cFront + 1 + ((i + 1) % n));
    const cBack = this.addVertex(cx, cy, z0, 0, 0, -1);
    for (let i = 0; i < n; i++) this.addVertex(pts2d[i][0], pts2d[i][1], z0, 0, 0, -1);
    for (let i = 0; i < n; i++) this.indices.push(cBack, cBack + 1 + ((i + 1) % n), cBack + 1 + i);
    return this;
  }

  transformAll(mat4) {
    for (let i = 0; i < this.positions.length; i += 3) {
      const x = this.positions[i], y = this.positions[i+1], z = this.positions[i+2];
      this.positions[i]   = mat4[0]*x + mat4[4]*y + mat4[8]*z + mat4[12];
      this.positions[i+1] = mat4[1]*x + mat4[5]*y + mat4[9]*z + mat4[13];
      this.positions[i+2] = mat4[2]*x + mat4[6]*y + mat4[10]*z + mat4[14];
      const nx = this.normals[i], ny = this.normals[i+1], nz = this.normals[i+2];
      const rnx = mat4[0]*nx + mat4[4]*ny + mat4[8]*nz;
      const rny = mat4[1]*nx + mat4[5]*ny + mat4[9]*nz;
      const rnz = mat4[2]*nx + mat4[6]*ny + mat4[10]*nz;
      const len = Math.hypot(rnx, rny, rnz) || 1;
      this.normals[i] = rnx / len; this.normals[i+1] = rny / len; this.normals[i+2] = rnz / len;
    }
    return this;
  }

  // 拼接另一个 builder（可带变换矩阵）
  appendBuilder(other, mat4 = null) {
    const offset = this.positions.length / 3;
    for (let i = 0; i < other.positions.length; i += 3) {
      let x = other.positions[i], y = other.positions[i+1], z = other.positions[i+2];
      let nx = other.normals[i], ny = other.normals[i+1], nz = other.normals[i+2];
      if (mat4) {
        const tx = mat4[0]*x + mat4[4]*y + mat4[8]*z + mat4[12];
        const ty = mat4[1]*x + mat4[5]*y + mat4[9]*z + mat4[13];
        const tz = mat4[2]*x + mat4[6]*y + mat4[10]*z + mat4[14];
        x = tx; y = ty; z = tz;
        const rnx = mat4[0]*nx + mat4[4]*ny + mat4[8]*nz;
        const rny = mat4[1]*nx + mat4[5]*ny + mat4[9]*nz;
        const rnz = mat4[2]*nx + mat4[6]*ny + mat4[10]*nz;
        const len = Math.hypot(rnx, rny, rnz) || 1;
        nx = rnx / len; ny = rny / len; nz = rnz / len;
      }
      this.positions.push(x, y, z);
      this.normals.push(nx, ny, nz);
    }
    for (let i = 0; i < other.indices.length; i++) this.indices.push(other.indices[i] + offset);
    return this;
  }

  compile(gl) {
    const vao = gl.createVertexArray();
    gl.bindVertexArray(vao);
    const posBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.positions), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);
    const normBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, normBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(this.normals), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(1);
    gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 0, 0);
    const idxBuf = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, idxBuf);
    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint32Array(this.indices), gl.STATIC_DRAW);
    gl.bindVertexArray(null);
    return { vao, count: this.indices.length };
  }
}
```

## §2 复用网格函数（Model Y 样本版——unit 网格 + mat4TRS 缩放布景）

场景型项目（车间/客舱/安检通道）用"单位网格 × TRS 缩放"铺场更高效：

```js
function uploadMesh(verts, norms, indices) {
  const vbo = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(verts), gl.STATIC_DRAW);
  const nbo = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, nbo);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(norms), gl.STATIC_DRAW);
  const ibo = gl.createBuffer();
  gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, ibo);
  gl.bufferData(gl.ELEMENT_ARRAY_BUFFER, new Uint16Array(indices), gl.STATIC_DRAW);
  return { vbo, nbo, ibo, count: indices.length };
}

// 圆柱（axis: 'Y'|'X'|'Z'，rTop/rBot 支持圆台锥度）
function buildCylinderMesh(rTop, rBot, len, segs = 24, axis = 'Y') {
  const verts = [], norms = [], idx = [];
  const half = len / 2;
  for (let i = 0; i <= segs; i++) {
    const a = (i / segs) * Math.PI * 2;
    const c = Math.cos(a), s = Math.sin(a);
    const pTop = axis === 'X' ? [half, rTop*c, rTop*s] : (axis === 'Z' ? [rTop*c, rTop*s, half] : [rTop*c, half, rTop*s]);
    const pBot = axis === 'X' ? [-half, rBot*c, rBot*s] : (axis === 'Z' ? [rBot*c, rBot*s, -half] : [rBot*c, -half, rBot*s]);
    const nVec = axis === 'X' ? [0, c, s] : (axis === 'Z' ? [c, s, 0] : [c, 0, s]);
    verts.push(...pTop, ...pBot);
    norms.push(...nVec, ...nVec);
  }
  for (let i = 0; i < segs; i++) {
    const a = i * 2, b = a + 1, c = a + 2, d = a + 3;
    idx.push(a, b, c, b, d, c);
  }
  const topCenterIdx = verts.length / 3;
  const nTop = axis === 'X' ? [1,0,0] : (axis === 'Z' ? [0,0,1] : [0,1,0]);
  const nBot = axis === 'X' ? [-1,0,0] : (axis === 'Z' ? [0,0,-1] : [0,-1,0]);
  verts.push(...(axis === 'X' ? [half,0,0] : (axis === 'Z' ? [0,0,half] : [0,half,0])));
  norms.push(...nTop);
  for (let i = 0; i <= segs; i++) {
    const a = (i / segs) * Math.PI * 2;
    const c = Math.cos(a), s = Math.sin(a);
    const p = axis === 'X' ? [half, rTop*c, rTop*s] : (axis === 'Z' ? [rTop*c, rTop*s, half] : [rTop*c, half, rTop*s]);
    verts.push(...p); norms.push(...nTop);
  }
  for (let i = 0; i < segs; i++) idx.push(topCenterIdx, topCenterIdx + 1 + i, topCenterIdx + 2 + i);
  const botCenterIdx = verts.length / 3;
  verts.push(...(axis === 'X' ? [-half,0,0] : (axis === 'Z' ? [0,0,-half] : [0,-half,0])));
  norms.push(...nBot);
  for (let i = 0; i <= segs; i++) {
    const a = (i / segs) * Math.PI * 2;
    const c = Math.cos(a), s = Math.sin(a);
    const p = axis === 'X' ? [-half, rTop*c, rTop*s] : (axis === 'Z' ? [rBot*c, rBot*s, -half] : [rBot*c, -half, rBot*s]);
    verts.push(...p); norms.push(...nBot);
  }
  for (let i = 0; i < segs; i++) idx.push(botCenterIdx, botCenterIdx + 2 + i, botCenterIdx + 1 + i);
  return uploadMesh(verts, norms, idx);
}

// UV 球（技师头/关节/粒子球/圆顶）
function buildSphereMesh(radius, latSegs = 16, lonSegs = 20) {
  const verts = [], norms = [], idx = [];
  for (let y = 0; y <= latSegs; y++) {
    const v = y / latSegs;
    const phi = v * Math.PI;
    for (let x = 0; x <= lonSegs; x++) {
      const u = x / lonSegs;
      const theta = u * Math.PI * 2;
      const nx = Math.sin(phi) * Math.cos(theta);
      const ny = Math.cos(phi);
      const nz = Math.sin(phi) * Math.sin(theta);
      verts.push(nx * radius, ny * radius, nz * radius);
      norms.push(nx, ny, nz);
    }
  }
  for (let y = 0; y < latSegs; y++) {
    for (let x = 0; x < lonSegs; x++) {
      const i0 = y * (lonSegs + 1) + x;
      const i1 = i0 + 1;
      const i2 = i0 + (lonSegs + 1);
      const i3 = i2 + 1;
      idx.push(i0, i2, i1, i1, i2, i3);
    }
  }
  return uploadMesh(verts, norms, idx);
}

// 折线路径弯管（Frenet 标架）：高压线束/液压管/冷却液管/扶手栏杆
function buildTubeMesh(pts, radius = 0.024, segs = 10) {
  const verts = [], norms = [], idx = [];
  for (let i = 0; i < pts.length; i++) {
    const p = pts[i];
    const prev = pts[Math.max(0, i - 1)];
    const next = pts[Math.min(pts.length - 1, i + 1)];
    let tx = next[0]-prev[0], ty = next[1]-prev[1], tz = next[2]-prev[2];
    let tLen = Math.hypot(tx, ty, tz) || 1;
    tx /= tLen; ty /= tLen; tz /= tLen;
    let ux = 0, uy = 1, uz = 0;
    if (Math.abs(ty) > 0.9) { ux = 1; uy = 0; }
    let nx = ty*uz - tz*uy, ny = tz*ux - tx*uz, nz = tx*uy - ty*ux;
    let nLen = Math.hypot(nx, ny, nz) || 1;
    nx /= nLen; ny /= nLen; nz /= nLen;
    const bx = ty*nz - tz*ny, by = tz*nx - tx*nz, bz = tx*ny - ty*nx;
    for (let s = 0; s <= segs; s++) {
      const a = (s / segs) * Math.PI * 2;
      const ca = Math.cos(a), sa = Math.sin(a);
      const rnx = nx * ca + bx * sa;
      const rny = ny * ca + by * sa;
      const rnz = nz * ca + bz * sa;
      verts.push(p[0] + rnx * radius, p[1] + rny * radius, p[2] + rnz * radius);
      norms.push(rnx, rny, rnz);
    }
  }
  const ring = segs + 1;
  for (let i = 0; i < pts.length - 1; i++) {
    for (let s = 0; s < segs; s++) {
      const a = i * ring + s;
      const b = a + 1;
      const c = (i + 1) * ring + s;
      const d = c + 1;
      idx.push(a, c, b, b, c, d);
    }
  }
  return uploadMesh(verts, norms, idx);
}

// 倒角盒（六面平面盒即可，配合 PBR 高光已有工程感；需要真圆角用 MeshBuilder+多段挤出）
function buildChamferBox(wx, wy, wz) {
  const hx = wx/2, hy = wy/2, hz = wz/2;
  const faces = [
    { n:[0,0,1],  v:[[-hx,-hy,hz],[hx,-hy,hz],[hx,hy,hz],[-hx,hy,hz]] },
    { n:[0,0,-1], v:[[hx,-hy,-hz],[-hx,-hy,-hz],[-hx,hy,-hz],[hx,hy,-hz]] },
    { n:[0,1,0],  v:[[-hx,hy,hz],[hx,hy,hz],[hx,hy,-hz],[-hx,hy,-hz]] },
    { n:[0,-1,0], v:[[-hx,-hy,-hz],[hx,-hy,-hz],[hx,-hy,hz],[-hx,-hy,hz]] },
    { n:[1,0,0],  v:[[hx,-hy,hz],[hx,-hy,-hz],[hx,hy,-hz],[hx,hy,hz]] },
    { n:[-1,0,0], v:[[-hx,-hy,-hz],[-hx,-hy,hz],[-hx,hy,hz],[-hx,hy,-hz]] }
  ];
  const verts = [], norms = [], idx = [];
  let base = 0;
  faces.forEach(f => {
    f.v.forEach(p => { verts.push(p[0], p[1], p[2]); norms.push(f.n[0], f.n[1], f.n[2]); });
    idx.push(base, base+1, base+2, base, base+2, base+3);
    base += 4;
  });
  return uploadMesh(verts, norms, idx);
}

// 放样流线外壳（机身/舱体/整流罩）：沿纵轴每站取轮廓环，环间连四边形。
// ★ 中空侧板结构：环只定义外侧面点，内舱另用内缩环 + 不封端盖 → 内部永不遮挡
function buildLoftedShellMesh(profileAt /* fn(z) => [{x,y,nx,ny},...] */, zStations) {
  const verts = [], norms = [], idx = [];
  const ptsPer = profileAt(zStations[0]).length;
  zStations.forEach((z, zi) => {
    const ring = profileAt(z);
    ring.forEach(p => { verts.push(p.x, p.y, z); norms.push(p.nx, p.ny, 0); });
  });
  for (let zi = 0; zi < zStations.length - 1; zi++) {
    for (let j = 0; j < ptsPer - 1; j++) {
      const a = zi * ptsPer + j;
      const b = a + 1;
      const c = a + ptsPer;
      const d = c + 1;
      idx.push(a, c, b, b, c, d);
    }
  }
  return uploadMesh(verts, norms, idx);
}
```

**标准 meshes 清单**（场景型项目启动即建）：

```js
const meshes = {
  unitBox: buildChamferBox(1, 1, 1),
  cylY: buildCylinderMesh(1, 1, 1, 24, 'Y'),
  cylX: buildCylinderMesh(1, 1, 1, 28, 'X'),
  cylZ: buildCylinderMesh(1, 1, 1, 24, 'Z'),
  coneY: buildCylinderMesh(0.15, 1, 1, 20, 'Y'),
  sphere: buildSphereMesh(1, 16, 20),
  floor: buildChamferBox(30, 0.04, 30)   // 地面单独用 uIsFloor=1 着色
};
```

## §3 关节化 3D 技师人物（含 PPE 装备动态穿戴）

Model Y 样本全量版。人物由 Boots/Legs/Torso/Head/Helmet/Arms/Gloves/Probes 八段拼装，`localPt()` 让所有部件绕人物脚底 `faceAngle` 旋转——**自动面向目标零件**：

```js
// tx, tz: 人物脚底世界坐标（必须设在设备包围盒外侧！）
// lookAtTarget: [x,y,z] 当前选中部件位置 → 人物自动转向
// ppe: { gloves, goggles, shoes, sign } PPE 穿戴状态 → 人物外观实时联动
function render3DTechnician(tx, tz, lookAtTarget, ppe) {
  const groundY = -0.80;                       // 本场景地面高度，按业务调整
  const dx = lookAtTarget[0] - tx;
  const dz = lookAtTarget[2] - tz;
  const faceAngle = Math.atan2(dx, dz);        // ★ 固化公式：朝向目标
  const cosA = Math.cos(faceAngle), sinA = Math.sin(faceAngle);

  // 局部坐标 → 世界坐标（绕 Y 轴旋转 faceAngle）
  function localPt(lx, ly, lz) {
    return [tx + lx * cosA + lz * sinA, groundY + ly, tz - lx * sinA + lz * cosA];
  }

  // 1. 绝缘靴 + 工作裤腿
  const bootCol = ppe.shoes ? [0.95, 0.68, 0.05] : [0.15, 0.17, 0.20];
  [-0.11, 0.11].forEach(lx => {
    const pBoot = localPt(lx, 0.08, 0.03);
    drawMesh(meshes.unitBox, Mat4.trs(pBoot[0], pBoot[1], pBoot[2], 0, faceAngle, 0, 0.10, 0.14, 0.22), bootCol, 0.3, 0.5);
    const pLeg = localPt(lx, 0.42, 0.0);
    drawMesh(meshes.cylY, Mat4.trs(pLeg[0], pLeg[1], pLeg[2], 0, 0, 0, 0.068, 0.58, 0.068), [0.12, 0.18, 0.28], 0.2, 0.7);
  });

  // 2. 躯干（工装 + 反光条）
  const pTorso = localPt(0, 0.94, 0);
  drawMesh(meshes.unitBox, Mat4.trs(pTorso[0], pTorso[1], pTorso[2], 0, faceAngle, 0, 0.34, 0.48, 0.20), [0.14, 0.24, 0.42], 0.3, 0.6);
  const pStripe = localPt(0, 1.02, 0.01);
  drawMesh(meshes.unitBox, Mat4.trs(pStripe[0], pStripe[1], pStripe[2], 0, faceAngle, 0, 0.35, 0.06, 0.21), [0.95, 0.55, 0.08], 0.6, 0.3, 1.0, 0.25);

  // 3. 头部 + 安全帽 + 防电弧面屏
  const pHead = localPt(0, 1.32, 0);
  drawMesh(meshes.sphere, Mat4.trs(pHead[0], pHead[1], pHead[2], 0, 0, 0, 0.11, 0.12, 0.11), [0.92, 0.76, 0.64], 0.1, 0.7);
  if (ppe.goggles) {
    const pHelm = localPt(0, 1.37, 0);
    drawMesh(meshes.sphere, Mat4.trs(pHelm[0], pHelm[1], pHelm[2], 0, 0, 0, 0.13, 0.11, 0.135), [0.05, 0.58, 0.92], 0.7, 0.25);
    const pVisor = localPt(0, 1.31, 0.09);
    drawMesh(meshes.unitBox, Mat4.trs(pVisor[0], pVisor[1], pVisor[2], 0, faceAngle, 0, 0.20, 0.13, 0.04), [0.2, 0.9, 1.0], 0.9, 0.1, 0.55);
  } else {
    const pHair = localPt(0, 1.37, -0.01);
    drawMesh(meshes.sphere, Mat4.trs(pHair[0], pHair[1], pHair[2], 0, 0, 0, 0.115, 0.08, 0.115), [0.15, 0.15, 0.18], 0.2, 0.8);
  }

  // 4. 手臂 + 绝缘手套 + 红黑万用表表笔
  const gloveCol = ppe.gloves ? [1.0, 0.42, 0.0] : [0.92, 0.76, 0.64];
  [-0.22, 0.22].forEach((lx, idx) => {
    const pShoulder = localPt(lx, 1.10, 0.05);
    drawMesh(meshes.sphere, Mat4.trs(pShoulder[0], pShoulder[1], pShoulder[2], 0, 0, 0, 0.06, 0.06, 0.06), [0.14, 0.24, 0.42], 0.3, 0.6);
    const pForearm = localPt(lx * 0.85, 0.98, 0.22);
    drawMesh(meshes.unitBox, Mat4.trs(pForearm[0], pForearm[1], pForearm[2], 0.55, faceAngle, 0, 0.08, 0.08, 0.32), [0.14, 0.24, 0.42], 0.3, 0.6);
    const pHand = localPt(lx * 0.72, 0.92, 0.38);
    drawMesh(meshes.sphere, Mat4.trs(pHand[0], pHand[1], pHand[2], 0, 0, 0, 0.065, 0.055, 0.085), gloveCol, 0.4, 0.35, 1.0, ppe.gloves ? 0.2 : 0.0);
    const pProbe = localPt(lx * 0.65, 0.94, 0.50);
    const probeCol = idx === 0 ? [0.95, 0.18, 0.18] : [0.22, 0.25, 0.30];
    drawMesh(meshes.unitBox, Mat4.trs(pProbe[0], pProbe[1], pProbe[2], 0.3, faceAngle, 0, 0.025, 0.025, 0.22), probeCol, 0.7, 0.25);
  });
}

// 人物平滑走动（主循环里每帧调用）
// simState.techCurrPos / techTargetPos = [x, z]
simState.techCurrPos[0] += (simState.techTargetPos[0] - simState.techCurrPos[0]) * 0.08;
simState.techCurrPos[1] += (simState.techTargetPos[1] - simState.techCurrPos[1]) * 0.08;
```

**行业换装指南**（只改颜色/部件）：
- 机务维修：深蓝工装 + 耳罩（两 sphere）+ 手电筒（cylY + emissive）
- 安检员：藏蓝制服 + 白手套 + 手持金属探测器（盒 + 环）
- 客舱乘务：航司制服色 + 丝巾色块 + 无表笔
- 焊工：皮围裙色块 + 焊接面罩（深色盒盖脸）+ 焊枪

## §4 部件建模范例（从部件数据库到 mesh 的映射套路）

```js
const Meshes = {};
function buildAllMeshes(gl) {
  // 范例 1：活塞——同轴多段圆柱堆叠（裙部开窗用弧段 tube）
  {
    const mb = new MeshBuilder();
    mb.addCylinder(0.83, 0.84, 0.14, 0.62, 48);          // 顶面
    mb.addCylinder(0.90, 0.90, 0.05, 0.525, 40);         // 环槽 ×3
    mb.addCylinder(0.975, 0.975, 0.07, 0.465, 48);
    mb.addTubeSection(0.82, 0.972, -0.38, 0.13, 24, -0.95, 0.95);       // 裙部开窗（留背面弧板）
    mb.addTubeSection(0.82, 0.972, -0.38, 0.13, 24, Math.PI - 0.95, Math.PI + 0.95);
    const boss = new MeshBuilder();                       // 活塞销座
    boss.addTubeSection(0.21, 0.36, -0.74, -0.26, 28);
    boss.transformAll(Mat4.rotateX(Mat4.identity(), Math.PI * 0.5));
    mb.appendBuilder(boss);
    Meshes.piston = mb.compile(gl);
  }

  // 范例 2：齿轮/齿圈——圆柱 + 循环 addBox 齿牙
  {
    const gear = new MeshBuilder();
    gear.addTubeSection(0.52, 0.68, -0.09, 0.09, 36);
    gear.addCylinder(0.22, 0.22, 0.18, 0, 24);
    for (let i = 0; i < 6; i++) {
      const spoke = new MeshBuilder().addBox(0, 0, 0, 0.09, 0.14, 0.62);   // 辐条
      gear.appendBuilder(spoke, Mat4.rotateY(Mat4.identity(), (i / 6) * Math.PI * 2));
    }
    for (let i = 0; i < 32; i++) {                                          // 齿牙
      const t = new MeshBuilder().addBox(0, 0, 0, 0.055, 0.18, 0.09);
      let mt = Mat4.rotateY(Mat4.identity(), (i / 32) * Math.PI * 2);
      mt = Mat4.translate(mt, 0, 0, 0.70);
      gear.appendBuilder(t, mt);
    }
    gear.transformAll(Mat4.rotateX(Mat4.identity(), Math.PI * 0.5));
    Meshes.gear = gear.compile(gl);
  }

  // 范例 3：剖切缸体——弧段 tube（0.92π..2.08π = 正面敞开）+ 散热翅片循环
  {
    const blk = new MeshBuilder();
    const arc0 = 0.92 * Math.PI, arc1 = 2.08 * Math.PI;
    blk.addTubeSection(0.86, 1.02, -0.15, 2.38, 48, arc0, arc1);   // 主套筒（剖切）
    for (let fy = 0.45; fy <= 2.15; fy += 0.34) {                  // 散热翅片
      blk.addTubeSection(1.25, 1.42, fy, fy + 0.07, 48, arc0, arc1);
    }
    blk.addBox(-1.42, -0.68, -0.15, 0.18, 1.15, 1.25);             // 曲轴箱支脚
    blk.addBox( 1.42, -0.68, -0.15, 0.18, 1.15, 1.25);
    Meshes.block = blk.compile(gl);
  }

  // 范例 4：凸轮轴——2D 轮廓挤出（升程函数生成桃形）
  {
    const cam = new MeshBuilder();
    const lobePts = [];
    for (let i = 0; i < 40; i++) {
      const a = (i / 40) * Math.PI * 2;
      const lift = Math.pow(Math.max(0, Math.sin(a)), 2.8) * 0.25;  // 余弦加速度升程
      lobePts.push([(0.27 + lift) * Math.cos(a), (0.27 + lift) * Math.sin(a)]);
    }
    cam.addExtrudedPolygon(lobePts, -0.14, 0.14);
    const shaft = new MeshBuilder().addCylinder(0.16, 0.16, 1.25, 0, 28);
    shaft.transformAll(Mat4.rotateX(Mat4.identity(), Math.PI * 0.5));
    cam.appendBuilder(shaft);
    Meshes.camLobe = cam.compile(gl);
  }

  // 范例 5：力矢量箭头（杆+锥头，教学标注用）
  {
    const arr = new MeshBuilder();
    arr.addCylinder(0.038, 0.038, 0.72, 0.36, 16);
    arr.addCylinder(0.0, 0.11, 0.28, 0.86, 18);
    Meshes.arrow = arr.compile(gl);
  }
}
```

**建模口诀**：旋转体 → `addCylinder`/`addTubeSection`；平板/支脚/齿 → `addBox`；弹簧/绕线 → `addHelicalSpring`；非圆截面杆/凸轮/平衡重 → `addExtrudedPolygon`；线缆/弯管 → `buildTubeMesh`；壳体/机身 → `buildLoftedShellMesh`（中空！）；人物 → `render3DTechnician`。
