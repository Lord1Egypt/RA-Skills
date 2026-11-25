/* ============================================================
 * measure.js — 文本测量与折行
 * SVG 没有自动折行，必须在排版阶段自己算。这里用字符宽度模型：
 * CJK 按 1 个字宽，西文按 0.55 左右，并对窄字符单独处理。
 * ============================================================ */

const NARROW = /[iIlj.,:;'!|']/;
const WIDE = /[mwMW@%]/;

/** 单字符相对字号的宽度系数 */
export function charRatio(ch) {
  const code = ch.codePointAt(0);
  // CJK、全角标点、假名、谚文
  if (
    (code >= 0x4e00 && code <= 0x9fff) ||
    (code >= 0x3000 && code <= 0x303f) ||
    (code >= 0xff00 && code <= 0xffef) ||
    (code >= 0x3040 && code <= 0x30ff) ||
    (code >= 0xac00 && code <= 0xd7af)
  ) return 1;
  if (ch === ' ') return 0.3;
  if (NARROW.test(ch)) return 0.3;
  if (WIDE.test(ch)) return 0.85;
  if (/[0-9]/.test(ch)) return 0.55;
  if (/[a-zA-Z]/.test(ch)) return 0.56;
  return 0.5;
}

/** 估算一行文本宽度 */
export function measureText(str, fontSize) {
  if (!str) return 0;
  let w = 0;
  for (const ch of String(str)) w += charRatio(ch) * fontSize;
  return w;
}

/** 切成排版 token：CJK 单字、西文单词、空格 */
function tokenize(str) {
  const tokens = [];
  let buf = '';
  for (const ch of str) {
    const code = ch.codePointAt(0);
    const isCJK =
      (code >= 0x4e00 && code <= 0x9fff) ||
      (code >= 0x3000 && code <= 0x303f) ||
      (code >= 0xff00 && code <= 0xffef) ||
      (code >= 0x3040 && code <= 0x30ff);
    if (isCJK) {
      if (buf) { tokens.push(buf); buf = ''; }
      tokens.push(ch);
    } else if (ch === ' ') {
      if (buf) { tokens.push(buf); buf = ''; }
      tokens.push(' ');
    } else {
      buf += ch;
    }
  }
  if (buf) tokens.push(buf);
  return tokens;
}

/** 贪心折行 */
export function wrapText(str, maxWidth, fontSize) {
  const s = String(str || '').trim();
  if (!s) return [];
  if (maxWidth <= 0) return [s];
  const lines = [];
  let line = '';
  let w = 0;
  for (const t of tokenize(s)) {
    const tw = measureText(t, fontSize);
    if (w + tw > maxWidth + 0.01 && line.trim()) {
      lines.push(line.replace(/\s+$/, ''));
      line = t === ' ' ? '' : t;
      w = measureText(line, fontSize);
    } else {
      line += t;
      w += tw;
    }
  }
  if (line.trim()) lines.push(line.replace(/\s+$/, ''));
  return lines;
}

/** 折行并限制行数，超出部分以省略号收尾 */
export function wrapClamp(str, maxWidth, fontSize, maxLines) {
  const all = wrapText(str, maxWidth, fontSize);
  if (all.length <= maxLines) return { lines: all, truncated: false };
  const kept = all.slice(0, maxLines);
  let last = kept[maxLines - 1];
  while (last.length > 1 && measureText(`${last}…`, fontSize) > maxWidth) {
    last = last.slice(0, -1);
  }
  kept[maxLines - 1] = `${last.replace(/[，、。；：,.;:]$/, '')}…`;
  return { lines: kept, truncated: true };
}

/** 金额/价格的显示宽度（用于右侧对齐） */
export const priceWidth = (price, fontSize) => measureText(String(price || ''), fontSize);
