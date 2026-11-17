import { readFileSync } from 'node:fs';

const DEFAULT_SIZE = { width: 1024, height: 1024 };

/** 读取 PNG / JPEG / WebP 的像素尺寸（无第三方依赖） */
export function imageSize(path) {
  let buf;
  try {
    buf = readFileSync(path);
  } catch {
    return { ...DEFAULT_SIZE };
  }

  // PNG：IHDR 在 8..24
  if (buf.length > 24 && buf.toString('ascii', 1, 4) === 'PNG') {
    return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
  }

  // JPEG：扫 SOF 标记
  if (buf.length > 4 && buf[0] === 0xff && buf[1] === 0xd8) {
    let i = 2;
    while (i < buf.length - 9) {
      if (buf[i] !== 0xff) { i++; continue; }
      const marker = buf[i + 1];
      const len = buf.readUInt16BE(i + 2);
      if ([0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf].includes(marker)) {
        return { height: buf.readUInt16BE(i + 5), width: buf.readUInt16BE(i + 7) };
      }
      i += 2 + len;
    }
  }

  // WebP
  if (buf.length > 30 && buf.toString('ascii', 0, 4) === 'RIFF' && buf.toString('ascii', 8, 12) === 'WEBP') {
    const chunk = buf.toString('ascii', 12, 16);
    if (chunk === 'VP8X') {
      return {
        width: 1 + buf.readUIntLE(24, 3),
        height: 1 + buf.readUIntLE(27, 3),
      };
    }
    if (chunk === 'VP8 ') {
      return { width: buf.readUInt16LE(26) & 0x3fff, height: buf.readUInt16LE(28) & 0x3fff };
    }
    if (chunk === 'VP8L') {
      const b = buf.readUInt32LE(21);
      return { width: (b & 0x3fff) + 1, height: ((b >> 14) & 0x3fff) + 1 };
    }
  }

  return { ...DEFAULT_SIZE };
}

/** 按 cover 方式计算缩放，铺满目标框 */
export function coverScale(srcW, srcH, dstW, dstH) {
  return Math.max(dstW / srcW, dstH / srcH);
}

/** 按 contain 方式计算缩放，完整放进目标框 */
export function containScale(srcW, srcH, dstW, dstH) {
  return Math.min(dstW / srcW, dstH / srcH);
}
