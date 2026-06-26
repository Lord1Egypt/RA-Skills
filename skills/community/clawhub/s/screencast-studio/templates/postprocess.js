// Post-process: raw.webm + events.json + cursor.png + ripple.png -> final.mp4
//   - Synthetic cursor (cursor.png) overlaid via ffmpeg, with 2-ghost trail (decreasing alpha)
//   - Click ripples (Material-style expanding rings, 2 staggered frames)
//   - Burned subtitles (CJK-capable font, platform-detected)
//
// events.json schema:
//   { t, kind: "subtitle"|"move"|"click", x?, y?, label? }
//
// Magic numbers (CALIBRATION / REST_LEAD / cursor tip / ripple sizes) are tuned for the
// 1440x900 viewport with the included cursor.png and ripple.png assets. If you change
// the viewport size or replace the assets, you may need to retune these.

const ffmpegPath = require('ffmpeg-static');
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const CALIBRATION = 0.65; // events.t lags video.t by ~0.65s (newPage→tStart gap)
const REST_LEAD = 0.45;   // cursor stays still until this long before next click

// Cursor: rendered @2x deviceScaleFactor, so PNG is ~44x56 px and tip is at (3,3).
const CURSOR_TIP_X = 3;
const CURSOR_TIP_Y = 3;

// Material-style ripple: 2 concentric rings with staggered timing + decreasing alpha.
const RIPPLE_FRAMES = [
  { size: 32, alpha: 0.92, dt0: 0.00, dt1: 0.28 }, // bright inner pulse
  { size: 80, alpha: 0.30, dt0: 0.08, dt1: 0.42 }, // outer expanding fade
];

// Trail: 2 ghost cursors trailing the main cursor with decreasing alpha + time offset.
const GHOSTS = [
  { dt: 0.20, alpha: 0.20 },
  { dt: 0.10, alpha: 0.45 },
];

function shiftedEvents(events, dt) {
  return events.map((e) => ({ ...e, t: +(e.t + dt).toFixed(3) }));
}

function addRestEvents(cursorEvents) {
  const out = [];
  for (let i = 0; i < cursorEvents.length; i++) {
    out.push(cursorEvents[i]);
    const cur = cursorEvents[i];
    const nxt = cursorEvents[i + 1];
    if (nxt && nxt.t - cur.t > REST_LEAD * 2) {
      out.push({
        t: +(nxt.t - REST_LEAD).toFixed(3),
        x: cur.x,
        y: cur.y,
        kind: 'move',
      });
    }
  }
  return out;
}

function lerpExpr(events, dim, offset) {
  if (events.length === 0) return '0';
  if (events.length === 1) return String(events[0][dim] + offset);
  let expr = String(events[events.length - 1][dim] + offset);
  for (let i = events.length - 2; i >= 0; i--) {
    const a = events[i];
    const b = events[i + 1];
    const av = a[dim] + offset;
    const bv = b[dim] + offset;
    const dt = (b.t - a.t) || 0.001;
    const lerp = `(${av}+(${bv}-${av})*((t-${a.t})/${dt}))`;
    expr = `if(lt(t,${b.t}),${lerp},${expr})`;
  }
  const first = events[0];
  expr = `if(lt(t,${first.t}),${first[dim] + offset},${expr})`;
  return expr;
}

function rippleOverlayChains(events, startInLabel, rippleInputIdx) {
  const clicks = events.filter((e) => e.kind === 'click');
  const chains = [];
  const N = clicks.length;
  if (N === 0) return { chains, finalLabel: startInLabel };

  RIPPLE_FRAMES.forEach((f, fi) => {
    const outputs = Array.from({ length: N }, (_, i) => `[rf${fi}_${i}]`).join('');
    chains.push(
      `[${rippleInputIdx}:v]scale=${f.size}:${f.size},format=rgba,colorchannelmixer=aa=${f.alpha},split=${N}${outputs}`
    );
  });

  let inLabel = startInLabel;
  let counter = 0;
  clicks.forEach((c, ci) => {
    RIPPLE_FRAMES.forEach((f, fi) => {
      const ox = Math.round(c.x - f.size / 2);
      const oy = Math.round(c.y - f.size / 2);
      const t0 = (c.t + f.dt0).toFixed(3);
      const t1 = (c.t + f.dt1).toFixed(3);
      const out = `[rp${counter}]`;
      chains.push(
        `${inLabel}[rf${fi}_${ci}]overlay=x=${ox}:y=${oy}:enable='between(t,${t0},${t1})'${out}`
      );
      inLabel = out;
      counter++;
    });
  });

  return { chains, finalLabel: inLabel };
}

function fmtSrt(t) {
  const hh = String(Math.floor(t / 3600)).padStart(2, '0');
  const mm = String(Math.floor((t % 3600) / 60)).padStart(2, '0');
  const ss = String(Math.floor(t % 60)).padStart(2, '0');
  const ms = String(Math.floor((t - Math.floor(t)) * 1000)).padStart(3, '0');
  return `${hh}:${mm}:${ss},${ms}`;
}

function buildSrt(events) {
  const labeled = events.filter((e) => e.label).slice().sort((a, b) => a.t - b.t);
  let out = '';
  let counter = 0;
  for (let i = 0; i < labeled.length; i++) {
    const e = labeled[i];
    const nextOriginal = labeled[i + 1];
    if (nextOriginal && nextOriginal.t - e.t < 0.5) continue;
    const start = e.t;
    const end = nextOriginal ? nextOriginal.t - 0.05 : start + 3.0;
    out += `${counter + 1}\n${fmtSrt(start)} --> ${fmtSrt(end)}\n${e.label}\n\n`;
    counter++;
  }
  return out;
}

function run(args) {
  console.log('> ffmpeg', args.length, 'args');
  const r = spawnSync(ffmpegPath, args, { stdio: 'inherit', cwd: __dirname });
  if (r.status !== 0) throw new Error('ffmpeg failed: ' + r.status);
}

function main() {
  const eventsPath = path.join(__dirname, 'events.json');
  const rawPath = path.join(__dirname, 'raw.webm');
  const cursorPath = path.join(__dirname, 'cursor.png');
  const ripplePath = path.join(__dirname, 'ripple.png');
  const srtPath = path.join(__dirname, 'subs.srt');
  const outPath = path.join(__dirname, 'final.mp4');

  if (!fs.existsSync(eventsPath)) throw new Error('events.json missing — run record.js first');
  if (!fs.existsSync(rawPath)) throw new Error('raw.webm missing — run record.js first');
  if (!fs.existsSync(cursorPath)) throw new Error('cursor.png missing — run gen-cursor.js first');
  if (!fs.existsSync(ripplePath)) throw new Error('ripple.png missing — run gen-ripple.js first');

  const events = JSON.parse(fs.readFileSync(eventsPath, 'utf8'));
  events.forEach((e) => { e.t = Math.max(0, +(e.t - CALIBRATION).toFixed(3)); });
  events.sort((a, b) => a.t - b.t);

  let cursorEvents = events.filter((e) => e.kind === 'move' || e.kind === 'click');
  cursorEvents = addRestEvents(cursorEvents);

  fs.writeFileSync(srtPath, buildSrt(events));

  const chains = [];
  const rippleResult = rippleOverlayChains(cursorEvents, '[0:v]', 2);
  chains.push(...rippleResult.chains);
  let inLabel = rippleResult.finalLabel;

  GHOSTS.forEach((g, i) => {
    chains.push(`[1:v]format=rgba,colorchannelmixer=aa=${g.alpha}[g${i}]`);
  });

  GHOSTS.forEach((g, i) => {
    const gx = lerpExpr(shiftedEvents(cursorEvents, g.dt), 'x', -CURSOR_TIP_X);
    const gy = lerpExpr(shiftedEvents(cursorEvents, g.dt), 'y', -CURSOR_TIP_Y);
    const out = `[gh${i}]`;
    chains.push(`${inLabel}[g${i}]overlay=x='${gx}':y='${gy}':eval=frame${out}`);
    inLabel = out;
  });

  const mx = lerpExpr(cursorEvents, 'x', -CURSOR_TIP_X);
  const my = lerpExpr(cursorEvents, 'y', -CURSOR_TIP_Y);
  chains.push(`${inLabel}[1:v]overlay=x='${mx}':y='${my}':eval=frame[main]`);
  inLabel = '[main]';

  // Subtitles — pick a CJK-capable font available on the host OS.
  // Override via env SUBTITLE_FONT to use a specific face (e.g. SUBTITLE_FONT="SimHei").
  // libass takes a single FontName; if it isn't installed, CJK characters render as boxes,
  // so we platform-detect rather than relying on libass fallback.
  const pickFont = () => {
    if (process.env.SUBTITLE_FONT) return process.env.SUBTITLE_FONT;
    if (process.platform === 'win32') return 'Microsoft YaHei';
    if (process.platform === 'darwin') return 'PingFang SC';
    return 'Noto Sans CJK SC'; // linux: usually present via fonts-noto-cjk
  };
  const subStyle =
    `FontName=${pickFont()},Fontsize=16,PrimaryColour=&Hffffff&,OutlineColour=&H00000000&,BackColour=&H99000000&,BorderStyle=4,Outline=1.5,Shadow=0,MarginV=42,Alignment=2`;
  chains.push(`${inLabel}subtitles=subs.srt:force_style='${subStyle}'[subbed]`);
  inLabel = '[subbed]';

  // Persistent masks — applied LAST so they cover cursor, ripples, AND subtitles.
  // Each mask: split → crop+boxblur the region → overlay back at original coords.
  const persistentMasks = events.filter((e) => e.kind === 'mask_persistent');
  persistentMasks.forEach((m, i) => {
    const mainTag = `[m${i}main]`;
    const cropTag = `[m${i}crop]`;
    const blurTag = `[m${i}blur]`;
    const ovTag = `[m${i}out]`;
    chains.push(`${inLabel}split=2${mainTag}${cropTag}`);
    // boxblur split: luma (lr/lp) can go higher than chroma (cr capped at 15 by ffmpeg).
    chains.push(`${cropTag}crop=${m.w}:${m.h}:${m.x}:${m.y},boxblur=lr=20:lp=2:cr=15:cp=2${blurTag}`);
    chains.push(`${mainTag}${blurTag}overlay=x=${m.x}:y=${m.y}${ovTag}`);
    inLabel = ovTag;
  });

  // Ensure ffmpeg's -map [out] target exists regardless of mask count.
  if (inLabel !== '[out]') {
    chains.push(`${inLabel}null[out]`);
  }

  const filterComplex = chains.join(';');

  run([
    '-y',
    '-i', 'raw.webm',
    '-i', 'cursor.png',
    '-i', 'ripple.png',
    '-filter_complex', filterComplex,
    '-map', '[out]',
    '-c:v', 'libx264',
    '-pix_fmt', 'yuv420p',
    '-preset', 'medium',
    '-crf', '20',
    '-r', '30',
    'final.mp4',
  ]);

  console.log('OUTPUT:', outPath, fs.statSync(outPath).size, 'bytes');
}

main();
