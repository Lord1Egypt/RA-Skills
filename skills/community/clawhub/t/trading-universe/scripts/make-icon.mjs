#!/usr/bin/env node
// Zero-dependency icon generator — rasterizes the Trading Universe three-bar logo
// (the same mark used for the browser-window/header icon and favicon) and packs a
// multi-size Windows .ico at ../assets/trading-universe.ico. Pure Node: it renders
// each size supersampled for clean anti-aliased edges, PNG-encodes with zlib, and
// wraps the PNGs in an ICO container. Re-run after any logo change.
import { deflateSync } from "node:zlib";
import { writeFile, mkdir } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const OUT = join(HERE, "..", "assets", "trading-universe.ico");

// --- logo geometry in a 64x64 design space (matches the favicon SVG) ---
const BG = [10, 13, 19];               // #0a0d13 rounded-square background
const G0 = [139, 92, 246];             // #8b5cf6 violet (gradient start)
const G1 = [34, 211, 238];             // #22d3ee cyan  (gradient end)
const BARS = [                          // x, y, w, h, r, opacity
  [13, 30, 9, 21, 2, 0.75],
  [27.5, 21, 9, 30, 2, 0.90],
  [42, 12, 9, 39, 2, 1.0],
];
const lerp = (a, b, t) => a + (b - a) * t;
const grad = (t) => [lerp(G0[0], G1[0], t), lerp(G0[1], G1[1], t), lerp(G0[2], G1[2], t)];
// signed "inside" test for a rounded rect (design space)
function inRoundRect(X, Y, x, y, w, h, r) {
  if (X < x || X > x + w || Y < y || Y > y + h) return false;
  const cx = Math.min(Math.max(X, x + r), x + w - r);
  const cy = Math.min(Math.max(Y, y + r), y + h - r);
  const dx = X - cx, dy = Y - cy;
  return dx * dx + dy * dy <= r * r;
}
// diagonal gradient (bottom-left -> top-right), normalized 0..1
const gradT = (X, Y) => Math.min(1, Math.max(0, (X / 64 + (1 - Y / 64)) / 2));

// Render one size to an RGBA buffer, supersampled SSxSS then box-downsampled.
function render(N, SS = 4) {
  const hi = N * SS;
  const out = Buffer.alloc(N * N * 4);
  // accumulate premultiplied RGBA per output pixel
  const acc = new Float64Array(N * N * 4);
  for (let py = 0; py < hi; py++) {
    for (let px = 0; px < hi; px++) {
      const X = (px + 0.5) / hi * 64, Y = (py + 0.5) / hi * 64;
      let r = 0, g = 0, b = 0, a = 0; // straight alpha, composited
      if (inRoundRect(X, Y, 0, 0, 64, 64, 14)) { r = BG[0]; g = BG[1]; b = BG[2]; a = 1; }
      for (const [bx, by, bw, bh, br, op] of BARS) {
        if (inRoundRect(X, Y, bx, by, bw, bh, br)) {
          const c = grad(gradT(X, Y));
          // src over dst with src alpha = op
          const sa = op, da = a;
          const oa = sa + da * (1 - sa);
          r = (c[0] * sa + r * da * (1 - sa)) / (oa || 1);
          g = (c[1] * sa + g * da * (1 - sa)) / (oa || 1);
          b = (c[2] * sa + b * da * (1 - sa)) / (oa || 1);
          a = oa;
        }
      }
      const ox = (px / SS) | 0, oy = (py / SS) | 0, oi = (oy * N + ox) * 4;
      acc[oi] += r * a; acc[oi + 1] += g * a; acc[oi + 2] += b * a; acc[oi + 3] += a; // premultiplied
    }
  }
  const per = SS * SS;
  for (let i = 0; i < N * N; i++) {
    const a = acc[i * 4 + 3] / per;
    const oi = i * 4;
    if (a <= 0) { out[oi] = out[oi + 1] = out[oi + 2] = out[oi + 3] = 0; continue; }
    out[oi] = Math.round(acc[oi] / per / a);
    out[oi + 1] = Math.round(acc[oi + 1] / per / a);
    out[oi + 2] = Math.round(acc[oi + 2] / per / a);
    out[oi + 3] = Math.round(a * 255);
  }
  return out;
}

// --- PNG encode (RGBA) ---
const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
function crc32(buf) { let c = 0xffffffff; for (let i = 0; i < buf.length; i++) c = CRC[(c ^ buf[i]) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; }
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length, 0);
  const t = Buffer.from(type, "ascii");
  const crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(Buffer.concat([t, data])), 0);
  return Buffer.concat([len, t, data, crc]);
}
function pngEncode(rgba, N) {
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(N, 0); ihdr.writeUInt32BE(N, 4);
  ihdr[8] = 8; ihdr[9] = 6; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0; // 8-bit RGBA
  const raw = Buffer.alloc(N * (N * 4 + 1));
  for (let y = 0; y < N; y++) { raw[y * (N * 4 + 1)] = 0; rgba.copy(raw, y * (N * 4 + 1) + 1, y * N * 4, y * N * 4 + N * 4); }
  const idat = deflateSync(raw, { level: 9 });
  return Buffer.concat([sig, chunk("IHDR", ihdr), chunk("IDAT", idat), chunk("IEND", Buffer.alloc(0))]);
}

// --- ICO pack (PNG-compressed entries; Windows Vista+ / 10 / 11) ---
function ico(images) { // images: [{N, png}]
  const count = images.length;
  const dir = Buffer.alloc(6 + count * 16);
  dir.writeUInt16LE(0, 0); dir.writeUInt16LE(1, 2); dir.writeUInt16LE(count, 4);
  let offset = 6 + count * 16;
  const blobs = [];
  images.forEach((im, i) => {
    const e = 6 + i * 16;
    dir[e] = im.N >= 256 ? 0 : im.N; dir[e + 1] = im.N >= 256 ? 0 : im.N;
    dir[e + 2] = 0; dir[e + 3] = 0;
    dir.writeUInt16LE(1, e + 4); dir.writeUInt16LE(32, e + 6);
    dir.writeUInt32LE(im.png.length, e + 8); dir.writeUInt32LE(offset, e + 12);
    offset += im.png.length; blobs.push(im.png);
  });
  return Buffer.concat([dir, ...blobs]);
}

const SIZES = [16, 24, 32, 48, 64, 128, 256];
const images = SIZES.map((N) => ({ N, png: pngEncode(render(N), N) }));
await mkdir(dirname(OUT), { recursive: true });
await writeFile(OUT, ico(images));
console.log("wrote", OUT, "sizes:", SIZES.join(","), "bytes:", (await import("node:fs")).statSync(OUT).size);
