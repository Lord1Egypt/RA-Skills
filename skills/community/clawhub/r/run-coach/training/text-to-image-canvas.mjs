// Usage: node text-to-image-canvas.mjs "标题" "line1\nline2\n..."
// Renders text to PNG using @napi-rs/canvas (no browser needed)
// Sends via Telegram Bot API

import { createCanvas, GlobalFonts } from '@napi-rs/canvas';
import { writeFileSync } from 'fs';

// Register CJK fonts (standard Noto path on Debian/Ubuntu; skill works with
// latin-only fonts if these are absent)
GlobalFonts.registerFromPath('/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc', 'NotoSansCJK');
GlobalFonts.registerFromPath('/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', 'NotoSansCJKBold');

const FONT = '"Noto Sans CJK SC"';
// Credentials come from the skill's chmod-600 dotfile (.credentials at the
// skill root, same pattern as garmin/.credentials) — never from argv (visible
// in process listings) and never from environment variables.
import { readFileSync as _readCreds } from 'node:fs';
const _credsPath = new URL('../.credentials', import.meta.url).pathname;
let CHAT_ID, BOT_TOKEN;
try {
  ({ chat_id: CHAT_ID, bot_token: BOT_TOKEN } = JSON.parse(_readCreds(_credsPath, 'utf8')));
} catch {
  console.error(`Missing/invalid ${_credsPath} — create it per SKILL.md Setup and chmod 600 it.`);
  process.exit(1);
}

const [, , title = 'Training Plan', rawContent = ''] = process.argv;
const lines = rawContent.split('\n');

const W = 1000;
const pad = 50;
const contentW = W - pad * 2;

// Parse lines into structured items
const items = [];
for (const raw of lines) {
  const l = raw.trim();
  if (!l) { items.push({ type: 'gap' }); continue; }
  if (l.startsWith('## ')) { items.push({ type: 'h3', text: l.replace(/^##\s*/, '') }); continue; }
  if (l.startsWith('# ')) { items.push({ type: 'h2', text: l.replace(/^#\s*/, '') }); continue; }
  if (l.startsWith('- ') || l.startsWith('• ')) { items.push({ type: 'bullet', text: l.replace(/^[-•]\s*/, '') }); continue; }
  if (/^\d+[.．]/.test(l)) { items.push({ type: 'numbered', text: l }); continue; }
  if (l.startsWith('⚠') || l.startsWith('⛔')) { items.push({ type: 'warn', text: l }); continue; }
  if (l.startsWith('💡') || l.startsWith('📅') || l.startsWith('✅') || l.startsWith('📌')) { items.push({ type: 'info', text: l }); continue; }
  items.push({ type: 'text', text: l });
}

// Calculate height
let totalH = pad + 90; // header
for (const it of items) {
  if (it.type === 'gap') totalH += 12;
  else if (it.type === 'h2') totalH += 46;
  else if (it.type === 'h3') totalH += 40;
  else if (it.type === 'warn' || it.type === 'info') totalH += 52;
  else totalH += 32;
}
totalH += pad + 20;

const canvas = createCanvas(W, totalH);
const ctx = canvas.getContext('2d');

function roundRect(x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

// Background
ctx.fillStyle = '#0f0f0f';
ctx.fillRect(0, 0, W, totalH);

let cy = pad;

// Header
const grd = ctx.createLinearGradient(pad, cy, pad + contentW, cy);
grd.addColorStop(0, '#1a4a6e');
grd.addColorStop(1, '#2d7ab4');
ctx.fillStyle = grd;
roundRect(pad, cy, contentW, 70, 14);
ctx.fill();

ctx.fillStyle = '#fff';
ctx.font = `bold 26px ${FONT}`;
ctx.fillText(title, pad + 28, cy + 45);
cy += 90;

// Content background
ctx.fillStyle = '#1a1a1a';
roundRect(pad, cy, contentW, totalH - cy - pad, 14);
ctx.fill();
ctx.fillStyle = '#2d7ab4';
ctx.fillRect(pad, cy + 14, 4, totalH - cy - pad - 28);

const cx = pad + 24;
cy += 20;

for (const it of items) {
  if (it.type === 'gap') { cy += 12; continue; }
  if (it.type === 'h2') {
    ctx.fillStyle = '#fff';
    ctx.font = `bold 22px ${FONT}`;
    ctx.fillText(it.text, cx, cy + 28);
    cy += 46;
  } else if (it.type === 'h3') {
    ctx.fillStyle = '#64b5f6';
    ctx.font = `bold 19px ${FONT}`;
    ctx.fillText(it.text, cx, cy + 26);
    cy += 40;
  } else if (it.type === 'bullet') {
    ctx.fillStyle = '#e6a317';
    ctx.beginPath(); ctx.arc(cx + 6, cy + 14, 4, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#e0e0e0';
    ctx.font = `16px ${FONT}`;
    ctx.fillText(it.text, cx + 20, cy + 20);
    cy += 32;
  } else if (it.type === 'numbered') {
    ctx.fillStyle = '#e0e0e0';
    ctx.font = `16px ${FONT}`;
    ctx.fillText(it.text, cx + 8, cy + 20);
    cy += 32;
  } else if (it.type === 'warn') {
    ctx.fillStyle = '#2a2215';
    roundRect(cx, cy, contentW - 48, 40, 8);
    ctx.fill();
    ctx.fillStyle = '#ffd54f';
    ctx.font = `15px ${FONT}`;
    ctx.fillText(it.text, cx + 14, cy + 26);
    cy += 52;
  } else if (it.type === 'info') {
    ctx.fillStyle = '#1a2230';
    roundRect(cx, cy, contentW - 48, 40, 8);
    ctx.fill();
    ctx.fillStyle = '#90caf9';
    ctx.font = `15px ${FONT}`;
    ctx.fillText(it.text, cx + 14, cy + 26);
    cy += 52;
  } else {
    ctx.fillStyle = '#e0e0e0';
    ctx.font = `16px ${FONT}`;
    ctx.fillText(it.text, cx, cy + 20);
    cy += 32;
  }
}

// Output next to this script; no shell, no child_process — native fetch only
const outPath = new URL('./text-img-out.png', import.meta.url).pathname;
const pngBuffer = canvas.toBuffer('image/png');
writeFileSync(outPath, pngBuffer);

// Send via Telegram Bot API (multipart form, no shell interpolation)
const form = new FormData();
form.append('chat_id', CHAT_ID);
form.append('caption', title);
form.append('photo', new Blob([pngBuffer], { type: 'image/png' }), 'plan.png');
const res = await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendPhoto`, {
  method: 'POST',
  body: form
});
const data = await res.json();
if (!data.ok) throw new Error(data.description);
console.log('done');
