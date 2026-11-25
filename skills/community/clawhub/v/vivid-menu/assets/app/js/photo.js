/* ============================================================
 * photo.js — 照片输入、压缩与局部放大
 * 原图只存在浏览器里，不上传。压缩后再进存档，避免撑爆 localStorage。
 * ============================================================ */

/** 读取文件为 dataURL */
function readAsDataUrl(file) {
  return new Promise((resolve, reject) => {
    const r = new FileReader();
    r.onload = () => resolve(r.result);
    r.onerror = () => reject(new Error('读取文件失败'));
    r.readAsDataURL(file);
  });
}

function loadImage(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('图片解码失败'));
    img.src = src;
  });
}

/**
 * 读入图片并压缩。长边超过 maxEdge 时等比缩小。
 * @returns {{dataUrl:string,width:number,height:number,name:string}}
 */
export async function readImageFile(file, maxEdge = 1400, quality = 0.82) {
  if (!file.type.startsWith('image/')) throw new Error('这不是图片文件');
  const raw = await readAsDataUrl(file);
  const img = await loadImage(raw);
  const scale = Math.min(1, maxEdge / Math.max(img.width, img.height));
  const w = Math.round(img.width * scale);
  const h = Math.round(img.height * scale);

  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  const g = c.getContext('2d');
  g.imageSmoothingQuality = 'high';
  g.drawImage(img, 0, 0, w, h);

  return {
    dataUrl: c.toDataURL('image/jpeg', quality),
    width: w,
    height: h,
    name: file.name || 'menu.jpg',
  };
}

/**
 * 按归一化区域裁切放大，用于辨认细节。
 * @param {{dataUrl:string}} source
 * @param {{x:number,y:number,w:number,h:number}} box 0~1
 */
export async function cropRegion(source, box, outWidth = 1000) {
  const img = await loadImage(source.dataUrl);
  const sx = box.x * img.width;
  const sy = box.y * img.height;
  const sw = Math.max(8, box.w * img.width);
  const sh = Math.max(8, box.h * img.height);
  const scale = Math.min(3, outWidth / sw);
  const w = Math.round(sw * scale);
  const h = Math.round(sh * scale);

  const c = document.createElement('canvas');
  c.width = w;
  c.height = h;
  const g = c.getContext('2d');
  g.imageSmoothingQuality = 'high';
  g.drawImage(img, sx, sy, sw, sh, 0, 0, w, h);

  return { dataUrl: c.toDataURL('image/png'), width: w, height: h };
}

/** 从粘贴事件里取图片文件 */
export function fileFromPaste(e) {
  const items = e.clipboardData?.items || [];
  for (const it of items) {
    if (it.type && it.type.startsWith('image/')) return it.getAsFile();
  }
  return null;
}
