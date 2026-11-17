#!/usr/bin/env node
/*
 * lib/png-palette.js — 零依赖 PNG 主色调提取（只依赖 Node 内置 zlib）
 * 用途：用户给一张参考图说「以这张图为准生成皮肤」时，从图里提取
 *       主色(accent) / 主背景色(dominant) / 深或浅(mode)，喂给皮肤生成器。
 * 支持 8-bit 非隔行 PNG（RGB / RGBA / 灰度 / 灰度+alpha）。
 */
const zlib = require('zlib');
const fs = require('fs');

function decodePng(buf) {
  if (buf.length < 8 || buf.readUInt32BE(0) !== 0x89504e47) throw new Error('不是有效的 PNG 文件');
  let off = 8;
  let width = 0, height = 0, bitDepth = 0, colorType = 0;
  const idat = [];
  while (off < buf.length) {
    const len = buf.readUInt32BE(off);
    const type = buf.toString('ascii', off + 4, off + 8);
    const data = buf.slice(off + 8, off + 8 + len);
    if (type === 'IHDR') {
      width = data.readUInt32BE(0);
      height = data.readUInt32BE(4);
      bitDepth = data[8];
      colorType = data[9];
    } else if (type === 'IDAT') {
      idat.push(data);
    } else if (type === 'IEND') {
      break;
    }
    off += 12 + len;
  }
  if (bitDepth !== 8) throw new Error('只支持 8-bit PNG（当前 bitDepth=' + bitDepth + '），请先转成 PNG-8');
  let channels;
  if (colorType === 0) channels = 1;
  else if (colorType === 2) channels = 3;
  else if (colorType === 4) channels = 2;
  else if (colorType === 6) channels = 4;
  else throw new Error('不支持的 colorType=' + colorType);

  const raw = zlib.inflateSync(Buffer.concat(idat));
  const stride = width * channels;
  const out = Buffer.alloc(height * stride);
  let prev = Buffer.alloc(stride);
  let p = 0;
  for (let y = 0; y < height; y++) {
    const filter = raw[p++];
    const line = raw.slice(p, p + stride); p += stride;
    const cur = Buffer.alloc(stride);
    for (let i = 0; i < stride; i++) {
      const a = i >= channels ? cur[i - channels] : 0;
      const b = prev[i];
      const c = i >= channels ? prev[i - channels] : 0;
      let v;
      switch (filter) {
        case 0: v = line[i]; break;
        case 1: v = line[i] + a; break;
        case 2: v = line[i] + b; break;
        case 3: v = line[i] + ((a + b) >> 1); break;
        case 4: {
          const pa = Math.abs(b - c), pb = Math.abs(a - c), pc = Math.abs(a + b - 2 * c);
          const pr = pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
          v = line[i] + pr; break;
        }
        default: v = line[i];
      }
      cur[i] = v & 0xff;
    }
    cur.copy(out, y * stride);
    prev = cur;
  }
  return { width, height, channels, data: out };
}

function rgbToHex(r, g, b) {
  const h = (v) => Math.max(0, Math.min(255, Math.round(v))).toString(16).padStart(2, '0');
  return '#' + h(r) + h(g) + h(b);
}
function sat(c) {
  const mx = Math.max(c.r, c.g, c.b), mn = Math.min(c.r, c.g, c.b);
  return mx === 0 ? 0 : (mx - mn) / mx;
}
function lum(c) { return (0.2126 * c.r + 0.7152 * c.g + 0.0722 * c.b) / 255; }

function pickAccent(colors) {
  let best = -1, res = colors[0];
  for (const c of colors.slice(0, 20)) {
    const s = sat(c), l = lum(c);
    // 跳过过暗/过亮（接近黑或白的不适合做强调色）
    if (l < 0.18 || l > 0.85) continue;
    // 偏好高饱和 + 中等亮度
    const score = s * 1.3 + 0.25 * (1 - Math.abs(l - 0.5));
    if (score > best) { best = score; res = c; }
  }
  return res;
}

function extractPalette(filePath, topN = 8) {
  const buf = fs.readFileSync(filePath);
  const img = decodePng(buf);
  const { width, height, channels, data } = img;
  const buckets = new Map();
  const total = width * height;
  const step = Math.max(1, Math.floor(total / 6000));
  for (let i = 0; i < total; i += step) {
    const o = i * channels;
    if (channels >= 4 && data[o + 3] < 24) continue; // 跳过透明像素
    const r = data[o], g = data[o + 1], b = data[o + 2];
    const key = (r >> 4) + ',' + (g >> 4) + ',' + (b >> 4);
    let e = buckets.get(key);
    if (!e) { e = { r: 0, g: 0, b: 0, n: 0 }; buckets.set(key, e); }
    e.r += r; e.g += g; e.b += b; e.n++;
  }
  const colors = [...buckets.values()].map((e) => ({
    r: Math.round(e.r / e.n), g: Math.round(e.g / e.n), b: Math.round(e.b / e.n), n: e.n,
  }));
  colors.sort((a, b) => b.n - a.n);
  const accent = pickAccent(colors);
  const dominant = colors[0];
  const mode = lum(dominant) < 0.5 ? 'dark' : 'light';
  return {
    accent: rgbToHex(accent.r, accent.g, accent.b),
    dominant: rgbToHex(dominant.r, dominant.g, dominant.b),
    mode,
    colors: colors.slice(0, topN).map((c) => ({ hex: rgbToHex(c.r, c.g, c.b), n: c.n })),
  };
}

module.exports = { decodePng, extractPalette, rgbToHex };
