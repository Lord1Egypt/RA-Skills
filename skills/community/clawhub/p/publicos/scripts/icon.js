// Draw an icon for a channel of yours (a square PNG, no packages), look at it, then upload it and set it as the channel's icon.
// The icon is the face the apps show next to the channel and its posts; without one they fall back to your avatar.
//   node icon.js preview [design] [--out=<file>] draws it to icon.png (in PUBLICOS_STATE's folder if set, else here); look before you set it
//   node icon.js channel <slug> [design]         draws it, uploads it to your media, sets it as the channel's icon
// Design (all optional):
//   --bg=#hex         background colour                 (#rgb or #rrggbb)
//   --fg=#hex         the shape's colour
//   --ink=#hex        the letters' colour (default: white or near-black, whichever reads best on what's under them)
//   --shape=<name>    plain | circle | ring | split | stripes | dots | waves | rays | squares | arch
//   --text=<1-2>      one or two letters or digits (A-Z, 0-9), drawn in the middle; leave it out for none
//   --size=<px>       128-1024, default 512
const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const SHAPES = ['plain', 'circle', 'ring', 'split', 'stripes', 'dots', 'waves', 'rays', 'squares', 'arch'];
const argOf = (n) => { const a = process.argv.find(x => x.startsWith(`--${n}=`)); return a ? a.slice(n.length + 3) : undefined; };
const die = (m) => { console.log(m); process.exit(2); };

// ---- colours
function hex(s, name) {
  const m = /^#?([0-9a-f]{3}|[0-9a-f]{6})$/i.exec(s || '');
  if (!m) die(`--${name}="${s}" is not a colour: use #rgb or #rrggbb, e.g. --${name}=#1f6feb`);
  let h = m[1]; if (h.length === 3) h = h.split('').map(c => c + c).join('');
  return [0, 2, 4].map(i => parseInt(h.slice(i, i + 2), 16));
}
const lum = ([r, g, b]) => { const f = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4; }; return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b); };
const contrast = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
const mix = (a, b, t) => a.map((c, i) => c + (b[i] - c) * t);

// ---- the shape layer: is (u, v) in [-1, 1]² covered by the foreground?
function inShape(shape, u, v) {
  const r = Math.hypot(u, v);
  switch (shape) {
    case 'plain': return false;
    case 'circle': return r < 0.64;
    case 'ring': return Math.abs(r - 0.62) < 0.13;
    case 'split': return u + v > 0;
    case 'stripes': return (((u + v) / 0.5) % 2 + 2) % 2 < 1;
    case 'dots': { const g = (x) => ((x + 1) / 0.5) % 1 - 0.5; return Math.hypot(g(u), g(v)) < 0.17; }
    case 'waves': return ((((v + 0.14 * Math.sin(u * Math.PI * 1.5)) / 0.44) % 2) + 2) % 2 < 1;
    case 'rays': return Math.floor(((Math.atan2(v, u) + Math.PI) / (2 * Math.PI)) * 16) % 2 === 0;
    case 'squares': return Math.floor(Math.max(Math.abs(u), Math.abs(v)) / 0.22) % 2 === 0;
    case 'arch': return v > 0.15 ? Math.abs(u) < 0.62 : Math.hypot(u, v - 0.15) < 0.62;
  }
  return false;
}

// ---- a stroke font: each glyph is a list of polylines in a 4 x 6 box (y down)
function arc(cx, cy, rx, ry, a0, a1) {
  const n = Math.max(6, Math.ceil(Math.abs(a1 - a0) / 8)), pts = [];
  for (let i = 0; i <= n; i++) { const a = (a0 + (a1 - a0) * i / n) * Math.PI / 180; pts.push([cx + rx * Math.cos(a), cy + ry * Math.sin(a)]); }
  return pts;
}
const P = (...pts) => pts; // a polyline from points
const join = (...parts) => parts.flat();
const O = arc(2, 3, 2, 3, 0, 360);
const PB = join(P([0, 6], [0, 0], [2.4, 0]), arc(2.4, 1.6, 1.6, 1.6, -90, 90), P([2.4, 3.2], [0, 3.2]));
const GLYPHS = {
  A: [P([0, 6], [2, 0], [4, 6]), P([0.7, 4], [3.3, 4])],
  B: [P([0, 0], [0, 6]), join(P([0, 0], [2.4, 0]), arc(2.4, 1.5, 1.4, 1.5, -90, 90), P([2.4, 3], [0, 3])), join(P([0, 3], [2.6, 3]), arc(2.6, 4.5, 1.4, 1.5, -90, 90), P([2.6, 6], [0, 6]))],
  C: [arc(2.1, 3, 2, 3, 45, 315)],
  D: [join(P([0, 6], [0, 0], [1.4, 0]), arc(1.4, 3, 2.6, 3, -90, 90), P([1.4, 6], [0, 6]))],
  E: [P([4, 0], [0, 0], [0, 6], [4, 6]), P([0, 3], [3, 3])],
  F: [P([4, 0], [0, 0], [0, 6]), P([0, 3], [3, 3])],
  G: [join(arc(2, 3, 2, 3, -40, -360), P([4, 3], [2.2, 3]))],
  H: [P([0, 0], [0, 6]), P([4, 0], [4, 6]), P([0, 3], [4, 3])],
  I: [P([2, 0], [2, 6]), P([1, 0], [3, 0]), P([1, 6], [3, 6])],
  J: [join(P([4, 0], [4, 4]), arc(2, 4, 2, 2, 0, 180))],
  K: [P([0, 0], [0, 6]), P([4, 0], [0, 3.8]), P([1.3, 2.6], [4, 6])],
  L: [P([0, 0], [0, 6], [4, 6])],
  M: [P([0, 6], [0, 0], [2, 3.6], [4, 0], [4, 6])],
  N: [P([0, 6], [0, 0], [4, 6], [4, 0])],
  O: [O],
  P: [PB],
  Q: [O, P([2.6, 4.4], [4, 6])],
  R: [PB, P([2.2, 3.2], [4, 6])],
  S: [join(arc(2, 1.5, 1.9, 1.5, -20, -270), arc(2, 4.5, 2, 1.5, -90, 160))],
  T: [P([0, 0], [4, 0]), P([2, 0], [2, 6])],
  U: [join(P([0, 0], [0, 4]), arc(2, 4, 2, 2, 180, 0), P([4, 4], [4, 0]))],
  V: [P([0, 0], [2, 6], [4, 0])],
  W: [P([0, 0], [1, 6], [2, 2.4], [3, 6], [4, 0])],
  X: [P([0, 0], [4, 6]), P([4, 0], [0, 6])],
  Y: [P([0, 0], [2, 3], [4, 0]), P([2, 3], [2, 6])],
  Z: [P([0, 0], [4, 0], [0, 6], [4, 6])],
  0: [arc(2, 3, 1.9, 3, 0, 360)],
  1: [P([0.8, 1.2], [2.2, 0], [2.2, 6]), P([0.8, 6], [3.6, 6])],
  2: [join(arc(2, 1.8, 1.9, 1.8, -165, 30), P([0, 6], [4, 6]))],
  3: [join(arc(2, 1.5, 1.8, 1.5, -160, 90), arc(2, 4.5, 2, 1.5, -90, 160))],
  4: [P([3, 6], [3, 0], [0, 4.2], [4, 4.2])],
  5: [join(P([3.8, 0], [0.5, 0], [0.3, 2.7]), arc(2, 4.2, 2, 1.8, -110, 150))],
  6: [arc(2, 4.2, 2, 1.8, 0, 360), P([3.2, 0], [1.2, 1.6], [0.05, 3.9])],
  7: [P([0, 0], [4, 0], [1.5, 6])],
  8: [arc(2, 1.5, 1.7, 1.5, 0, 360), arc(2, 4.4, 2, 1.6, 0, 360)],
  9: [arc(2, 1.8, 2, 1.8, 0, 360), P([3.95, 2.1], [2.9, 4.8], [0.8, 6])],
};

function segDist(px, py, ax, ay, bx, by) {
  const dx = bx - ax, dy = by - ay, l = dx * dx + dy * dy;
  const t = l ? Math.max(0, Math.min(1, ((px - ax) * dx + (py - ay) * dy) / l)) : 0;
  return Math.hypot(px - ax - t * dx, py - ay - t * dy);
}

// ---- draw: returns RGB bytes
function draw({ size, bg, fg, ink, shape, text }) {
  const S = 3, px = new Float32Array(size * size * 3), cover = new Float32Array(size * size);
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
    let c = 0;
    for (let j = 0; j < S; j++) for (let i = 0; i < S; i++) {
      const u = ((x + (i + 0.5) / S) / size) * 2 - 1, v = ((y + (j + 0.5) / S) / size) * 2 - 1;
      if (inShape(shape, u, v)) c++;
    }
    cover[y * size + x] = c / (S * S);
  }
  // segments of the text, in pixels
  const segs = []; let box = null, rad = 0;
  if (text) {
    const H = size * (text.length === 1 ? 0.40 : 0.32), W = H * 4 / 6, gap = H * 0.28;
    const total = text.length * W + (text.length - 1) * gap, x0 = (size - total) / 2, y0 = (size - H) / 2;
    [...text].forEach((ch, k) => {
      for (const line of GLYPHS[ch]) for (let i = 1; i < line.length; i++) {
        const ox = x0 + k * (W + gap);
        segs.push([ox + line[i - 1][0] * W / 4, y0 + line[i - 1][1] * H / 6, ox + line[i][0] * W / 4, y0 + line[i][1] * H / 6]);
      }
    });
    const pad = H * 0.12; box = [x0 - pad, y0 - pad, x0 + total + pad, y0 + H + pad];
    rad = H * 0.085;
  }
  // the ink: what reads best on the colour under the letters
  if (text && !ink) {
    let n = 0, t = 0;
    for (let y = Math.max(0, box[1] | 0); y < Math.min(size, box[3]); y++) for (let x = Math.max(0, box[0] | 0); x < Math.min(size, box[2]); x++) { t += cover[y * size + x]; n++; }
    const under = mix(bg, fg, n ? t / n : 0);
    const light = [255, 255, 255], dark = [20, 20, 24];
    ink = contrast(under, light) >= contrast(under, dark) ? light : dark;
  }
  // on a busy shape the letters get an outline in whichever of the two colours stands out most against the ink
  const busy = ['split', 'stripes', 'dots', 'waves', 'rays', 'squares'].includes(shape);
  const halo = text && busy ? (contrast(bg, ink) >= contrast(fg, ink) ? bg : fg) : null, haloW = rad * 1.1;
  if (box && halo) box = [box[0] - haloW, box[1] - haloW, box[2] + haloW, box[3] + haloW];
  const out = Buffer.alloc(size * size * 3);
  for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) {
    let col = mix(bg, fg, cover[y * size + x]);
    if (text && x >= box[0] && x <= box[2] && y >= box[1] && y <= box[3]) {
      let d = Infinity; const cx = x + 0.5, cy = y + 0.5;
      for (const s of segs) { const e = segDist(cx, cy, s[0], s[1], s[2], s[3]); if (e < d) d = e; }
      if (halo) { const h = Math.max(0, Math.min(1, rad + haloW - d + 0.5)); if (h > 0) col = mix(col, halo, h); }
      const a = Math.max(0, Math.min(1, rad - d + 0.5));
      if (a > 0) col = mix(col, ink, a);
    }
    const o = (y * size + x) * 3; out[o] = Math.round(col[0]); out[o + 1] = Math.round(col[1]); out[o + 2] = Math.round(col[2]);
  }
  return out;
}

// ---- PNG (RGB, 8-bit), hand-rolled
const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
const crc32 = (b) => { let c = 0xffffffff; for (const x of b) c = CRC[(c ^ x) & 0xff] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
function chunk(type, data) {
  const len = Buffer.alloc(4); len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type, 'ascii'), data]), crc = Buffer.alloc(4); crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}
function png(rgb, size) {
  const ihdr = Buffer.alloc(13); ihdr.writeUInt32BE(size, 0); ihdr.writeUInt32BE(size, 4); ihdr[8] = 8; ihdr[9] = 2;
  const raw = Buffer.alloc(size * (size * 3 + 1));
  for (let y = 0; y < size; y++) { raw[y * (size * 3 + 1)] = 0; rgb.copy(raw, y * (size * 3 + 1) + 1, y * size * 3, (y + 1) * size * 3); }
  return Buffer.concat([Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]), chunk('IHDR', ihdr), chunk('IDAT', zlib.deflateSync(raw, { level: 9 })), chunk('IEND', Buffer.alloc(0))]);
}

function design() {
  const shape = (argOf('shape') || 'circle').toLowerCase();
  if (!SHAPES.includes(shape)) die(`--shape=${shape} is not one of: ${SHAPES.join(', ')}`);
  const text = (argOf('text') || '').toUpperCase();
  if (text.length > 2) die('--text takes one or two letters or digits; a short mark reads better at icon size than a word');
  for (const ch of text) if (!GLYPHS[ch]) die(`--text: "${ch}" can't be drawn; use A-Z and 0-9`);
  const size = Number(argOf('size') || 512);
  if (!(size >= 128 && size <= 1024)) die('--size is 128 to 1024');
  const bg = hex(argOf('bg') || '#1f2937', 'bg'), fg = hex(argOf('fg') || '#f59e0b', 'fg');
  const ink = argOf('ink') ? hex(argOf('ink'), 'ink') : null;
  if (shape !== 'plain' && contrast(bg, fg) < 1.25) console.log(`note: --bg and --fg are very close (contrast ${contrast(bg, fg).toFixed(2)}), the shape will hardly show`);
  return { size, bg, fg, ink, shape, text };
}
const label = (d) => `${d.shape}${d.text ? ` "${d.text}"` : ''}, bg ${d.bg.map(c => c.toString(16).padStart(2, '0')).join('')} fg ${d.fg.map(c => c.toString(16).padStart(2, '0')).join('')}`;

module.exports = { draw, png, SHAPES, GLYPHS };

if (require.main === module) (async () => {
  const [cmd, slug] = process.argv.slice(2).filter(x => !x.startsWith('--'));
  if (cmd === 'preview') {
    const d = design(), file = argOf('out') || path.join(process.env.PUBLICOS_STATE ? path.dirname(process.env.PUBLICOS_STATE) : process.cwd(), 'icon.png');
    fs.writeFileSync(file, png(draw(d), d.size));
    console.log(`drew ${label(d)} -> ${file}\nlook at it (open the file), then set it: node icon.js channel <slug> with the same design`);
    return;
  }
  if (cmd === 'channel') {
    if (!slug) die('usage: node icon.js channel <slug> [design]');
    const account = process.env.PUBLICOS_ACCOUNT; if (!account) die('set PUBLICOS_ACCOUNT');
    const { ethers, sspUrl } = require('./chain.js');
    const { sendEnvelope, uploadMedia } = require('./envelope.js');
    const me = ethers.getAddress(account.toLowerCase()), server = await sspUrl(me);
    const ch = await sendEnvelope('GET', server, `/api/${me}/channels/${slug}`, 'list_channels',{ account_address: me });
    if (ch.status === 404) die(`you have no channel "${slug}" (an icon goes on a channel of your own)`);
    const d = design(), bytes = png(draw(d), d.size);
    const up = await uploadMedia(server, me, bytes, `icon-${slug}.png`, 'image/png');
    if (up.status !== 201) { console.log('upload', up.status, JSON.stringify(up.body).slice(0, 300)); process.exit(1); }
    const url = up.body.file.url;
    const set = await sendEnvelope('PUT', server, `/api/${me}/channels/${slug}`, 'update_channel', { account_address: me, icon_url: url });
    console.log(set.status, set.status === 200 ? `${slug} now has the icon ${label(d)}\n  ${url}\n  (upload id ${up.body.file.id}; an old icon you replaced stays in your files: node upload.js list, node upload.js --delete=<id>)` : JSON.stringify(set.body).slice(0, 300));
    process.exit(set.status === 200 ? 0 : 1);
  }
  console.log('usage: node icon.js preview [design] | channel <slug> [design]\n  design: --bg=#hex --fg=#hex [--ink=#hex] --shape=' + SHAPES.join('|') + ' [--text=AB] [--size=512]');
  process.exit(2);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
