#!/usr/bin/env node
// gen-icons.mjs —— 生成 extension/icons 四张珊瑚橙 PNG（零依赖，无需任何第三方包）
//
// 分享包刻意不含任何 *.png（图标由 agent / 本脚本在需要时现生成）。
// 用法：
//   node gen-icons.mjs                 # 生成脚本同级 ./extension/icons/{16,32,48,128}.png
//   node gen-icons.mjs assets/extension # 指定目标目录（如 skill 源）
//
// 生成的图标是珊瑚橙纯色占位图，加载扩展不会因缺图标失败。
// 想换成正式品牌图标，部署/生成后直接替换这四个 png 即可。
import { join, dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import fs from "node:fs";
import zlib from "node:zlib";

const __dirname = dirname(fileURLToPath(import.meta.url));
const targetArg = process.argv[2];
const extDir = resolve(targetArg ? targetArg : join(__dirname, "extension"));

function crc32(buf) {
  let c = ~0;
  for (let i = 0; i < buf.length; i++) {
    c ^= buf[i];
    for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xedb88320 & -(c & 1));
  }
  return (~c) >>> 0;
}
function pngChunk(type, data) {
  const t = Buffer.from(type, "ascii");
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length, 0);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(Buffer.concat([t, data])), 0);
  return Buffer.concat([len, t, data, crc]);
}
function writePng(filePath, size, [r, g, b]) {
  const stride = size * 3 + 1;
  const raw = Buffer.alloc(stride * size);
  for (let y = 0; y < size; y++) {
    raw[y * stride] = 0; // filter type 0
    for (let x = 0; x < size; x++) {
      const o = y * stride + 1 + x * 3;
      raw[o] = r; raw[o + 1] = g; raw[o + 2] = b;
    }
  }
  const sig = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(size, 0);
  ihdr.writeUInt32BE(size, 4);
  ihdr[8] = 8;   // bit depth
  ihdr[9] = 2;   // color type RGB
  const idat = zlib.deflateSync(raw, { level: 9 });
  fs.writeFileSync(filePath, Buffer.concat([
    sig,
    pngChunk("IHDR", ihdr),
    pngChunk("IDAT", idat),
    pngChunk("IEND", Buffer.alloc(0)),
  ]));
}

const sizes = [16, 32, 48, 128];
const iconsDir = join(extDir, "icons");
fs.mkdirSync(iconsDir, { recursive: true });
for (const s of sizes) writePng(join(iconsDir, `icon${s}.png`), s, [255, 122, 69]); // 珊瑚橙
console.log(`✓ 已生成 ${sizes.length} 张珊瑚橙图标 → ${iconsDir}`);
console.log(`  (可替换成正式品牌图标：icon16/32/48/128.png)`);
