// 4-pass review pipeline for the latest final.mp4. Each pass has a different focus:
//   - flow      : each click event, sampled at pre/mid/post — verify cursor on target,
//                 ripple firing, UI reaction. Catches misclicks, dead-state stages.
//   - visual    : each subtitle event, sampled mid-display — verify subtitle text
//                 matches what UI shows, no stale/stacked subs.
//   - coverage  : each stage's settled frame — verify the stage actually executed
//                 (modal opened, content rendered, no missing functionality).
//   - sensitive : two checks for sensitive-content leakage:
//                 (a) every PERSISTENT_MASK sampled at 10/50/90% of video — verify the
//                     blur is actually applied and the region looks unreadable.
//                 (b) full-frame scans every 10s — agent reads these to find PII that
//                     was NOT masked (usernames, version numbers, internal data).
//
// Major errors should surface in any of the 4 passes; the passes complement each other.
// Outputs go to ./review/{flow,visual,coverage,sensitive}/ and a report.txt summary in each.
//
// Usage:
//   node review.js              — run all 4 passes
//   node review.js flow         — only flow
//   node review.js visual       — only visual
//   node review.js coverage     — only coverage
//   node review.js sensitive    — only sensitive (mask + PII scan)
const ffmpegPath = require('ffmpeg-static');
const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const ROOT = __dirname;
const REVIEW_DIR = path.join(ROOT, 'review');
const CAL = 0.65; // matches postprocess.js CALIBRATION
const FINAL = path.join(ROOT, 'final.mp4');
const EVENTS = path.join(ROOT, 'events.json');

if (!fs.existsSync(FINAL)) { console.error('final.mp4 missing — run `npm run demo` first.'); process.exit(1); }
if (!fs.existsSync(EVENTS)) { console.error('events.json missing.'); process.exit(1); }

const events = JSON.parse(fs.readFileSync(EVENTS, 'utf8'));

const ensure = (dir) => { if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true }); };
const wipe = (dir) => {
  if (!fs.existsSync(dir)) return;
  for (const f of fs.readdirSync(dir)) fs.unlinkSync(path.join(dir, f));
};
const grab = (t, name, dir) => {
  const dst = path.join(dir, name);
  const r = spawnSync(ffmpegPath, ['-y', '-ss', String(t), '-i', FINAL, '-frames:v', '1', dst], { stdio: ['ignore', 'ignore', 'pipe'] });
  return r.status === 0;
};
const fmt = (n) => Number(n).toFixed(2);

function reviewFlow() {
  const dir = path.join(REVIEW_DIR, 'flow');
  ensure(dir); wipe(dir);
  const lines = [
    '=== FLOW REVIEW ===',
    'Each click sampled 3 times: pre (cursor approaching), mid (click+ripple), react (0.35s after).',
    `${'#'.padStart(3)}  ${'video.t'.padEnd(8)}  ${'pos'.padEnd(11)}  label`,
    '',
  ];
  const clicks = events.filter((e) => e.kind === 'click');
  clicks.forEach((c, i) => {
    const ct = Math.max(0, c.t - CAL);
    const ix = String(i).padStart(2, '0');
    grab(+(ct - 0.20).toFixed(2), `click-${ix}-A-pre.png`, dir);
    grab(+(ct + 0.05).toFixed(2), `click-${ix}-B-mid.png`, dir);
    grab(+(ct + 0.35).toFixed(2), `click-${ix}-C-react.png`, dir);
    lines.push(`${String(i).padStart(3)}  ${fmt(ct).padEnd(8)}  (${c.x},${c.y})`.padEnd(35) + `  ${c.label}`);
  });
  fs.writeFileSync(path.join(dir, 'report.txt'), lines.join('\n'));
  console.log(`✓ flow      ${clicks.length} clicks → ${clicks.length * 3} frames`);
}

function reviewVisual() {
  const dir = path.join(REVIEW_DIR, 'visual');
  ensure(dir); wipe(dir);
  const lines = [
    '=== VISUAL REVIEW ===',
    'Each subtitle sampled mid-display. Verify subtitle text matches what UI shows.',
    `${'#'.padStart(3)}  ${'video.t'.padEnd(8)}  text`,
    '',
  ];
  const subs = events.filter((e) => e.kind === 'subtitle');
  subs.forEach((s, i) => {
    const st = Math.max(0, s.t - CAL);
    const ix = String(i).padStart(2, '0');
    grab(+(st + 0.5).toFixed(2), `sub-${ix}.png`, dir);
    lines.push(`${String(i).padStart(3)}  ${fmt(st).padEnd(8)}  ${s.label}`);
  });
  fs.writeFileSync(path.join(dir, 'report.txt'), lines.join('\n'));
  console.log(`✓ visual    ${subs.length} subtitles → ${subs.length} frames`);
}

function reviewCoverage() {
  const dir = path.join(REVIEW_DIR, 'coverage');
  ensure(dir); wipe(dir);
  const lines = [
    '=== COVERAGE REVIEW ===',
    'Each stage = subtitle event. Sampled 1s after start (UI should be settled).',
    `${'#'.padStart(3)}  ${'video.t'.padEnd(8)}  stage`,
    '',
  ];
  const subs = events.filter((e) => e.kind === 'subtitle');
  subs.forEach((s, i) => {
    const st = Math.max(0, s.t - CAL);
    const ix = String(i).padStart(2, '0');
    grab(+(st + 1.0).toFixed(2), `stage-${ix}.png`, dir);
    lines.push(`${String(i).padStart(3)}  ${fmt(st).padEnd(8)}  ${s.label}`);
  });
  fs.writeFileSync(path.join(dir, 'report.txt'), lines.join('\n'));
  console.log(`✓ coverage  ${subs.length} stages → ${subs.length} frames`);
}

function reviewSensitive() {
  const dir = path.join(REVIEW_DIR, 'sensitive');
  ensure(dir); wipe(dir);

  // Estimate video length from the latest event timestamp.
  const lastT = events.length > 0 ? Math.max(...events.map((e) => e.t || 0)) : 60;
  const videoLen = Math.max(1, lastT - CAL) + 2;

  const masks = events.filter((e) => e.kind === 'mask_persistent');
  const lines = [
    '=== SENSITIVE / MASK REVIEW ===',
    '',
    'Two checks:',
    '  (a) Each PERSISTENT_MASK sampled at 10/50/90% of video — verify region is blurred unreadable.',
    '  (b) Full-frame scans every 10s — read these to find PII that was NOT masked.',
    '',
    'IMPORTANT: subtitle counts and ship success do NOT prove privacy. Only this pass does.',
    '',
  ];

  // (a) Per-mask region samples (cropped to mask area)
  lines.push('--- mask regions (cropped to verify blur) ---');
  if (masks.length === 0) {
    lines.push('(no PERSISTENT_MASKS configured)');
  } else {
    masks.forEach((m, i) => {
      const ix = String(i).padStart(2, '0');
      [0.10, 0.50, 0.90].forEach((frac) => {
        const t = (videoLen * frac).toFixed(2);
        const pct = String(Math.round(frac * 100)).padStart(2, '0');
        const dst = path.join(dir, `mask-${ix}-${m.label}-${pct}pct.png`);
        spawnSync(ffmpegPath, [
          '-y', '-ss', t, '-i', FINAL,
          '-vf', `crop=${m.w}:${m.h}:${m.x}:${m.y}`,
          '-frames:v', '1', dst,
        ], { stdio: ['ignore', 'ignore', 'pipe'] });
      });
      lines.push(`  ${ix}  "${m.label}"  region=${m.x},${m.y} ${m.w}x${m.h}  → 3 cropped samples`);
    });
  }
  lines.push('');

  // (b) Full-frame scans
  lines.push('--- full-frame scans (read for unmasked PII) ---');
  const SCAN_INTERVAL = 10;
  let scanCount = 0;
  for (let t = 5; t < videoLen; t += SCAN_INTERVAL) {
    const ix = String(scanCount).padStart(2, '0');
    const tStr = t.toFixed(0).padStart(3, '0');
    grab(+t.toFixed(2), `scan-${ix}-t${tStr}s.png`, dir);
    lines.push(`  scan-${ix}  t=${t.toFixed(0)}s`);
    scanCount++;
  }
  lines.push('');
  lines.push('Agent self-check after reading all images:');
  lines.push('  1. For every mask-XX-*.png — is the region unreadable (blurred to noise)?');
  lines.push('  2. For every scan-XX-*.png — any PII visible? (usernames, real names,');
  lines.push('     emails, UUIDs, version numbers, internal project codenames, business strategy text)');
  lines.push('  3. If answer to (2) is yes — STOP. Add a mask via box {x,y,w,h} and re-render');
  lines.push('     (no need to re-record). Run review:sensitive again until clean.');

  fs.writeFileSync(path.join(dir, 'report.txt'), lines.join('\n'));
  console.log(`✓ sensitive ${masks.length} masks × 3 + ${scanCount} scans → ${masks.length * 3 + scanCount} frames`);
}

const mode = (process.argv[2] || 'all').toLowerCase();
ensure(REVIEW_DIR);
if (mode === 'all' || mode === 'flow')      reviewFlow();
if (mode === 'all' || mode === 'visual')    reviewVisual();
if (mode === 'all' || mode === 'coverage')  reviewCoverage();
if (mode === 'all' || mode === 'sensitive') reviewSensitive();
console.log(`\nreview output → ${REVIEW_DIR}`);
