/* ============================================================
 * export.js — 导出 SVG / PNG
 * SVG 是矢量母版；PNG 用于直接发微信、发朋友圈。
 * ============================================================ */

import { renderMenu } from './render.js';

/** 生成 SVG 文本（导出用，剔除点击热区） */
export const toSvgText = (menu) => renderMenu(menu, { hitAreas: false }).svg;

function saveBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

const safeName = (s) => String(s || '菜单').replace(/[\\/:*?"<>|]/g, '_').slice(0, 30);

/** 下载 SVG */
export function downloadSvg(menu) {
  const svg = toSvgText(menu);
  saveBlob(new Blob([svg], { type: 'image/svg+xml;charset=utf-8' }), `${safeName(menu.name)}.svg`);
}

/** SVG → PNG Blob */
export async function svgToPngBlob(menu, scale = 2) {
  const svg = toSvgText(menu);
  const { width, height } = renderMenu(menu).layout;
  const url = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(svg)}`;

  const img = await new Promise((resolve, reject) => {
    const i = new Image();
    i.onload = () => resolve(i);
    i.onerror = () => reject(new Error('SVG 渲染失败'));
    i.src = url;
  });

  const c = document.createElement('canvas');
  c.width = Math.round(width * scale);
  c.height = Math.round(height * scale);
  const g = c.getContext('2d');
  g.fillStyle = '#ffffff';
  g.fillRect(0, 0, c.width, c.height);
  g.imageSmoothingQuality = 'high';
  g.drawImage(img, 0, 0, c.width, c.height);

  return new Promise((resolve) => {
    c.toBlob((b) => resolve(b), 'image/png');
  });
}

/** 下载 PNG */
export async function downloadPng(menu, scale = 2) {
  const blob = await svgToPngBlob(menu, scale);
  saveBlob(blob, `${safeName(menu.name)}.png`);
}

/**
 * 复制 PNG 到剪贴板。不支持时回落为下载，并返回状态说明。
 * @returns {Promise<'copied'|'downloaded'|'failed'>}
 */
export async function copyPng(menu, scale = 2) {
  try {
    const blob = await svgToPngBlob(menu, scale);
    if (!blob) throw new Error('生成图片失败');
    if (!navigator.clipboard || !window.ClipboardItem) throw new Error('浏览器不支持图片剪贴板');
    await navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]);
    return 'copied';
  } catch (e) {
    console.warn('[export] 复制失败，改为下载', e);
    try {
      await downloadPng(menu, scale);
      return 'downloaded';
    } catch (e2) {
      console.error('[export] 下载也失败', e2);
      return 'failed';
    }
  }
}
