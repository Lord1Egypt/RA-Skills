#!/usr/bin/env node
// render-video.mjs: deterministic, frame-stepped MP4 of a deck, with offline-rendered music and sound effects.
//
// How it stays deterministic: Playwright's fake clock replaces setTimeout, requestAnimationFrame,
// performance.now and Date, and the script advances it by exactly 1000/fps ms per frame. CSS animations
// and transitions run on the browser's own clock, so each one is paused when it first appears and
// seeked to (virtual now - its virtual start) before every screenshot.
import fs from 'node:fs';
import path from 'node:path';
import { spawn, spawnSync } from 'node:child_process';
import {
  parseArgs, say, die, rel, baseName, fmtBytes, requireHtmlFile, requirePlaywright, launchChromium,
  watchPage, fileUrl, isMain,
} from './_lib.mjs';

const TARGET = { I: -16, TP: -1.5, LRA: 11 };
const STAMP_LAND = 0.25; // seconds from a stamp's delay to the moment it hits the paper (sk-slam reaches scale 1 at 70% of 360 ms)
const TAIL = 1;          // seconds of held last frame

const spec = {
  name: 'sketchy render-video', file: 'render-video.mjs', usage: '<deck.html> [-o out.mp4] [--fps 30] [--width 1920 --height 1080] [--music mood|none] [--seed s] [--no-sound]',
  summary: 'frame-stepped MP4 of a deck: virtual clock, offline-rendered sound, FFmpeg mux, loudness -16 LUFS.',
  details: [
    'Opens the deck with ?video (autoplay, clean) on a virtual clock, steps it 1000/fps ms per frame and',
    'screenshots every frame, so the same deck and seed give the same video. Length: the deck timeline',
    '(data-duration per slide, default 6 s) plus 1 s.',
    'Sound: SketchySound.renderOffline builds the music (data-music, data-seed) with a page sound at each',
    'slide, a pencil at each step and a stamp at each [data-slam]; FFmpeg normalizes it to -16 LUFS,',
    '-1.5 dBTP in two passes. Needs ffmpeg on PATH (libx264 and aac).',
    'Frames go to <name>.partial/ beside the output (about 0.3 MB per frame as JPEG) and are removed on success.',
    'After encoding it measures the file and writes four spot-check PNGs beside it: open them and look.',
    'Known limit: the audio is identical from run to run, and short renders gave byte-identical frames, but two',
    'full-length renders of one deck were not byte-identical (cause not isolated; the pictures look the same).',
  ],
  options: [
    { name: 'out', short: 'o', type: 'string', arg: 'file', help: 'output file (default: out/<name>.mp4 next to the input)' },
    { name: 'fps', type: 'number', default: 30, help: 'frames per second, 1 to 60 (default 30)' },
    { name: 'width', type: 'number', default: 1920, help: 'video width in px, even (default 1920)' },
    { name: 'height', type: 'number', default: 1080, help: 'video height in px, even (default 1080)' },
    { name: 'music', type: 'string', arg: 'mood|none', help: 'music mood: sketchbook, ledger, focus, calm, or none (default: the deck data-music, else sketchbook)' },
    { name: 'seed', type: 'string', arg: 'text', help: 'music seed (default: the deck data-seed)' },
    { name: 'no-sound', type: 'boolean', help: 'no audio track at all' },
    { name: 'max-seconds', type: 'number', arg: 'n', help: 'stop after n seconds (quick test renders)' },
    { name: 'format', type: 'string', arg: 'jpeg|png', default: 'jpeg', help: 'frame format: jpeg (quality 92, default) or png (lossless, slower, larger)' },
    { name: 'keep-frames', type: 'boolean', help: 'keep <name>.partial/ (frames and audio.wav) after a successful render' },
  ],
  positionals: { min: 1, max: 1, name: '<deck.html>' },
  examples: [
    'node render-video.mjs out/deck.html',
    'node render-video.mjs out/deck.html --fps 10 --max-seconds 12 -o preview.mp4',
    'node render-video.mjs out/deck.html --music calm --seed launch-2026',
    'node render-video.mjs out/deck.html --no-sound',
  ],
};

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const pad6 = (n) => String(n).padStart(6, '0');
const fmtSec = (s) => `${s.toFixed(1)} s`;

/* ---------- ffmpeg ---------- */
function perOs(win, mac, linux) {
  return [`Windows:        ${win}`, `macOS:          ${mac}`, `Debian/Ubuntu:  ${linux}`];
}
const FFMPEG_FIX = perOs('winget install Gyan.FFmpeg   (then open a new terminal)', 'brew install ffmpeg', 'sudo apt install ffmpeg   (or your distro package)');

function probeFfmpeg() {
  const v = spawnSync('ffmpeg', ['-version'], { encoding: 'utf8', windowsHide: true });
  if (v.error || v.status !== 0) return { ok: false };
  const enc = spawnSync('ffmpeg', ['-hide_banner', '-encoders'], { encoding: 'utf8', windowsHide: true });
  const list = `${enc.stdout || ''}`;
  const missing = ['libx264', 'aac'].filter((n) => !new RegExp(`\\b${n}\\b`).test(list));
  return { ok: true, version: (/ffmpeg version (\S+)/.exec(v.stdout) || [])[1] || '?', missing };
}

/** Run a program without a shell; resolve with exit code and both streams. */
function run(cmd, args, opts = {}) {
  return new Promise((resolve) => {
    const child = spawn(cmd, args, { windowsHide: true, stdio: ['ignore', 'pipe', 'pipe'], ...opts });
    let stdout = '', stderr = '';
    child.stdout.on('data', (d) => { stdout += d; });
    child.stderr.on('data', (d) => { stderr += d; });
    child.on('error', (e) => resolve({ code: -1, stdout, stderr: String(e && e.message ? e.message : e) }));
    child.on('close', (code) => resolve({ code, stdout, stderr }));
  });
}
const lastLines = (s, n = 6) => String(s).trim().split(/\r?\n/).slice(-n).join('\n      ');

/** Pass 1 of loudnorm: measure the WAV. Returns the measured_* filter fragment, or null for silence. */
async function measureLoudness(wav) {
  const af = `loudnorm=I=${TARGET.I}:TP=${TARGET.TP}:LRA=${TARGET.LRA}:print_format=json`;
  const r = await run('ffmpeg', ['-hide_banner', '-nostats', '-i', wav, '-af', af, '-f', 'null', '-']);
  const m = /\{[^{}]*"input_i"[^{}]*\}/.exec(r.stderr);
  if (!m) throw new Error(`loudnorm pass 1 gave no result: ${lastLines(r.stderr, 2)}`);
  const j = JSON.parse(m[0]);
  const num = (x) => Number.parseFloat(x);
  if (!Number.isFinite(num(j.input_i)) || num(j.input_i) < -69) return null; // silence: nothing to normalize
  return { i: num(j.input_i), tp: num(j.input_tp), lra: num(j.input_lra), thresh: num(j.input_thresh), offset: num(j.target_offset), filter:
    `loudnorm=I=${TARGET.I}:TP=${TARGET.TP}:LRA=${TARGET.LRA}:measured_I=${j.input_i}:measured_TP=${j.input_tp}:measured_LRA=${j.input_lra}:measured_thresh=${j.input_thresh}:offset=${j.target_offset}:linear=true:print_format=summary` };
}

/** Measure the finished file: integrated loudness, true peak, and the stream facts. */
async function inspectVideo(file) {
  const out = {};
  const probe = await run('ffprobe', ['-v', 'error', '-show_entries', 'format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate,nb_frames,sample_rate', '-of', 'json', file]);
  try {
    const j = JSON.parse(probe.stdout);
    out.duration = Number.parseFloat(j.format && j.format.duration);
    out.size = Number.parseInt(j.format && j.format.size, 10);
    const v = (j.streams || []).find((s) => s.codec_type === 'video');
    const a = (j.streams || []).find((s) => s.codec_type === 'audio');
    if (v) {
      const [n, d] = String(v.avg_frame_rate || '0/1').split('/').map(Number);
      out.video = { codec: v.codec_name, width: v.width, height: v.height, fps: d ? n / d : 0, frames: Number.parseInt(v.nb_frames, 10) || null };
    }
    if (a) out.audio = { codec: a.codec_name, sampleRate: Number.parseInt(a.sample_rate, 10) };
  } catch { /* leave what we have */ }
  if (out.audio) {
    const r = await run('ffmpeg', ['-hide_banner', '-nostats', '-i', file, '-vn', '-af', 'ebur128=peak=true:framelog=quiet', '-f', 'null', '-']);
    const lufs = /Integrated loudness:\s*\n\s*I:\s*(-?[\d.]+|-?inf)\s*LUFS/i.exec(r.stderr);
    const peak = /True peak:\s*\n\s*Peak:\s*(-?[\d.]+|-?inf)\s*dBFS/i.exec(r.stderr);
    out.lufs = lufs ? Number.parseFloat(lufs[1]) : null;
    out.truePeak = peak ? Number.parseFloat(peak[1]) : null;
  }
  return out;
}

/* ---------- in the page ---------- */
/** Installed before the page loads: video time starts at the ready event, and CSS animations are caught the moment they are created. */
function pageInit() {
  const base = performance.now.bind(performance);
  let zero = 0;
  performance.now = () => base() - zero;
  document.addEventListener('sk:ready', () => { zero = base(); window.__skReady = true; });

  const starts = new WeakMap();
  // CSS animations and transitions run on the browser clock. Pause each the moment it exists and
  // seek it to (virtual now - virtual start) before every screenshot.
  const adopt = () => {
    const t = performance.now();
    for (const a of document.getAnimations()) {
      if (!starts.has(a)) { starts.set(a, t); try { a.pause(); a.currentTime = 0; } catch (e) { /* finished already */ } }
    }
  };
  new MutationObserver(adopt).observe(document, { subtree: true, childList: true, attributes: true });
  window.__skSeek = () => {
    const t = performance.now();
    for (const a of document.getAnimations()) {
      let s = starts.get(a);
      if (s === undefined) { s = t; starts.set(a, s); try { a.pause(); } catch (e) { /* ignore */ } }
      try { a.currentTime = t - s; } catch (e) { /* ignore */ }
    }
    return t;
  };
}

function probeDeck() {
  const D = window.SketchyDeck;
  const main = document.querySelector('main.sk-deck, .sk-deck');
  const slides = [...document.querySelectorAll('main.sk-deck > .sk-slide, .sk-deck .sk-slide')];
  const stamps = [];
  slides.forEach((s, i) => s.querySelectorAll('[data-slam]').forEach((el) => {
    const raw = getComputedStyle(el).getPropertyValue('--delay').trim();
    const m = /^(-?[\d.]+)(ms|s)?$/.exec(raw);
    stamps.push({ index: i, delay: (m ? Number.parseFloat(m[1]) * (m[2] === 's' ? 1000 : 1) : 600) / 1000 });
  }));
  return {
    rows: D.timeline(), stamps, count: D.count,
    seed: (main && main.getAttribute('data-seed')) || '', music: (main && main.getAttribute('data-music')) || '',
    hasSound: Boolean(window.SketchySound && window.SketchySound.renderOffline),
    moods: (window.SketchySound && window.SketchySound.moods) || [],
  };
}

async function renderAudio(browser, file, job) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, locale: 'en-US' });
  try {
    const page = await context.newPage();
    page.setDefaultTimeout(180000);
    await page.goto(fileUrl(file, 'static'), { waitUntil: 'load' });
    const meta = await page.evaluate(async (j) => {
      if (window.SketchyDeck && window.SketchyDeck.ready) await window.SketchyDeck.ready;
      const buf = await window.SketchySound.renderOffline(j);
      window.__wav = new Uint8Array(window.SketchySound.toWav(buf));
      return { bytes: window.__wav.length, seconds: buf.length / buf.sampleRate, channels: buf.numberOfChannels, sampleRate: buf.sampleRate };
    }, job);
    const chunks = [];
    const STEP = 3 * 1024 * 1024; // a multiple of 3, so every chunk is whole base64
    for (let off = 0; off < meta.bytes; off += STEP) {
      const b64 = await page.evaluate(({ off, len }) => {
        const a = window.__wav.subarray(off, off + len);
        let s = '';
        for (let i = 0; i < a.length; i += 0x8000) s += String.fromCharCode.apply(null, a.subarray(i, i + 0x8000));
        return btoa(s);
      }, { off, len: STEP });
      chunks.push(Buffer.from(b64, 'base64'));
    }
    return { wav: Buffer.concat(chunks), meta };
  } finally {
    await context.close();
  }
}

/* ---------- cues ---------- */
export function buildCues(rows, stamps, duration) {
  const cues = [];
  rows.forEach((row, i) => {
    if (i > 0) cues.push({ t: row.start, name: 'page' });
    (row.steps || []).forEach((t) => cues.push({ t, name: 'pencil' }));
  });
  for (const st of stamps) {
    const row = rows[st.index];
    if (!row) continue;
    const t = row.start + st.delay + STAMP_LAND;
    if (t < row.start + row.duration) cues.push({ t, name: 'stamp' });
  }
  return cues.filter((c) => c.t >= 0 && c.t < duration).sort((a, b) => a.t - b.t);
}

export function buildSections(rows, duration) {
  return rows.filter((r) => r.musicSection && r.start < duration).map((r) => ({ t: r.start, name: r.musicSection }));
}

/** Pick four moments worth looking at: first slide, a middle slide, a step reveal (or a page turn), the last slide. */
export function spotTimes(rows, duration) {
  const clamp = (t) => Math.max(0, Math.min(duration - 0.05, t));
  const settle = (row, want) => row.start + Math.min(want, Math.max(0.2, row.duration - 0.3));
  const spots = [];
  spots.push({ label: 'first', t: clamp(settle(rows[0], 1.6)) });
  const mid = rows[Math.floor(rows.length / 2)];
  spots.push({ label: 'middle', t: clamp(settle(mid, 3.5)) });
  const withSteps = rows.find((r) => r.steps && r.steps.length && r.steps[0] < duration);
  if (withSteps) spots.push({ label: 'step', t: clamp(withSteps.steps[0] + 0.5) });
  else if (rows.length > 1) spots.push({ label: 'turn', t: clamp(rows[1].start + 0.35) });
  const last = rows[rows.length - 1];
  spots.push({ label: 'last', t: clamp(Math.min(settle(last, 4), duration - 0.1)) });
  return spots;
}

/* ---------- main ---------- */
async function main() {
  const { values, positionals } = parseArgs(process.argv.slice(2), spec);
  const file = requireHtmlFile(positionals[0], 'deck html file');
  const fps = values.fps, width = values.width, height = values.height;
  if (!Number.isInteger(fps) || fps < 1 || fps > 60) die(`--fps must be a whole number from 1 to 60, got ${values.fps}`, 'for example --fps 30');
  if (![width, height].every((n) => Number.isInteger(n) && n >= 16 && n % 2 === 0)) die(`--width and --height must be even whole numbers, got ${width}x${height}`, 'for example --width 1920 --height 1080');
  if (!/^(jpeg|png)$/.test(values.format)) die(`--format must be jpeg or png, got "${values.format}"`, 'for example --format jpeg');
  if (values.maxSeconds !== undefined && !(values.maxSeconds > 0)) die(`--max-seconds must be above 0, got ${values.maxSeconds}`, 'for example --max-seconds 12');
  if (values.music !== undefined && !/^[a-z0-9_-]+$/i.test(values.music)) die(`bad --music "${values.music}"`, 'use a mood name (sketchbook, ledger, focus, calm) or none');

  let out;
  if (values.out) out = path.resolve(values.out);
  else if (path.basename(path.dirname(file)) === 'out') out = path.join(path.dirname(file), `${baseName(file)}.mp4`);
  else out = path.join(path.dirname(file), 'out', `${baseName(file)}.mp4`);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const stem = path.join(path.dirname(out), path.basename(out, path.extname(out)));
  const partialDir = `${stem}.partial`;
  const partialMp4 = `${stem}.partial.mp4`;

  const ff = probeFfmpeg();
  if (!ff.ok) {
    say.warn('ffmpeg is not on PATH: frames and audio.wav will be kept, but no MP4 is made');
    say.fix(FFMPEG_FIX);
  } else if (ff.missing.length) {
    say.warn(`ffmpeg ${ff.version} has no ${ff.missing.join(' or ')} encoder: no MP4 can be made`);
    say.fix(FFMPEG_FIX);
  }
  const canEncode = ff.ok && !ff.missing.length;

  const pw = requirePlaywright();
  const browser = await launchChromium(pw);
  const state = { errors: new Map(), failed: new Map(), external: new Map() };
  const started = Date.now();
  let info, frames, duration, wavBuf = null, wavMeta = null, drift = 0;

  let partialReady = false; // the folder is made only once the deck has passed the checks
  const ensurePartial = () => { if (!partialReady) { fs.rmSync(partialDir, { recursive: true, force: true }); fs.mkdirSync(partialDir, { recursive: true }); partialReady = true; } };

  try {
    const context = await browser.newContext({
      viewport: { width, height }, deviceScaleFactor: 1, reducedMotion: 'no-preference', locale: 'en-US', colorScheme: 'light',
    });
    const page = await context.newPage();
    page.setDefaultTimeout(60000);
    watchPage(page, state);
    await page.clock.install({ time: 0 });
    await page.clock.pauseAt(1000);            // paused before the page exists: nothing runs on real time
    await page.addInitScript(pageInit);
    await page.goto(fileUrl(file, 'video'), { waitUntil: 'load' });

    if (!(await page.evaluate(() => Boolean(document.querySelector('main.sk-deck, .sk-deck') && window.SketchyDeck && window.SketchyDeck.timeline)))) {
      die('this file is not a sketchy deck', ['video needs <main class="sk-deck"> with <section class="sk-slide"> pages and sketchy-deck.js', 'make one with: node new.mjs deck <folder>']);
    }
    // fonts load on real time; then the engine needs two animation frames, which only the clock can give it
    for (let i = 0; i < 1500 && (await page.evaluate(() => document.fonts.status)) !== 'loaded'; i++) await sleep(10);
    let ready = false;
    for (let i = 0; i < 400 && !ready; i++) { await page.clock.runFor(2); ready = await page.evaluate(() => window.__skReady === true); }
    if (!ready) die('the deck did not become ready on the virtual clock', ['open the deck in a browser and check the console', 'node shoot.mjs <deck.html>'], 1);

    info = await page.evaluate(probeDeck);
    if (!info.count || !info.rows.length) die('the deck has no slides', 'add <section class="sk-slide"> elements inside main.sk-deck', 1);
    const end = info.rows[info.rows.length - 1].start + info.rows[info.rows.length - 1].duration;
    duration = Math.min(end + TAIL, values.maxSeconds || Infinity);
    frames = Math.max(1, Math.round(duration * fps));
    duration = frames / fps;

    /* ----- sound: rendered offline in a plain page, so the virtual clock cannot touch it ----- */
    let soundOn = !values.noSound;
    if (soundOn && !info.hasSound) {
      say.warn('this deck does not load sketchy-sound.js: the video will have no audio');
      say.fix('add <script src="engine/sketchy-sound.js"></script> before sketchy-deck.js, or pass --no-sound');
      soundOn = false;
    }
    if (soundOn) {
      let mood = values.music !== undefined ? values.music : (info.music || 'sketchbook');
      if (mood !== 'none' && info.moods.length && !info.moods.includes(mood)) {
        if (values.music !== undefined) die(`unknown music mood "${mood}"`, `use one of: ${info.moods.join(', ')}, none`);
        say.warn(`the deck asks for data-music="${mood}", which does not exist: no music in the video`);
        say.fix(`use one of: ${info.moods.join(', ')}, none`);
        mood = 'none';
      }
      const seed = values.seed !== undefined ? values.seed : (info.seed || 'sketchy');
      const cues = buildCues(info.rows, info.stamps, duration);
      const sections = buildSections(info.rows, duration);
      say.info(`sound: mood ${mood}, seed "${seed}", ${cues.length} cues, ${sections.length} music sections`);
      const t0 = Date.now();
      const audio = await renderAudio(browser, file, { duration, seed, mood, cues, sections, sampleRate: 48000 });
      wavBuf = audio.wav; wavMeta = audio.meta;
      ensurePartial();
      fs.writeFileSync(path.join(partialDir, 'audio.wav'), wavBuf);
      say.info(`audio rendered: ${fmtSec(wavMeta.seconds)}, ${fmtBytes(wavBuf.length)} in ${((Date.now() - t0) / 1000).toFixed(1)} s`);
    }

    /* ----- frames ----- */
    ensurePartial();
    const eta = Math.max(1, Math.round((frames * 0.17) / 60));
    say.info(`capturing ${frames} frames at ${fps} fps, ${width}x${height} (${fmtSec(duration)}), about ${eta} min`);
    const ext = values.format === 'png' ? 'png' : 'jpg';
    const shot = values.format === 'png' ? { type: 'png' } : { type: 'jpeg', quality: 92 };
    let now = await page.evaluate(() => performance.now());
    const mark = new Set([0.25, 0.5, 0.75].map((f) => Math.floor(frames * f)));
    const lap = { clock: 0, seek: 0, shot: 0 };
    let t = performance.now();
    const tick = (key) => { const n = performance.now(); lap[key] += n - t; t = n; };
    for (let k = 0; k < frames; k++) {
      const target = Math.round((k * 1000) / fps);
      t = performance.now();
      if (target > now) await page.clock.runFor(target - now);
      tick('clock');
      now = await page.evaluate(() => window.__skSeek());
      tick('seek');
      if (k > 0 && Math.abs(now - target) > 1) drift++;
      await page.screenshot({ path: path.join(partialDir, `frame-${pad6(k)}.${ext}`), ...shot });
      tick('shot');
      if (mark.has(k)) say.info(`  ${Math.round((k / frames) * 100)}%  frame ${k}/${frames}  ${((Date.now() - started) / 1000).toFixed(0)} s`);
    }
    if (process.env.SKETCHY_VERBOSE) say.info(`timing per frame: clock ${(lap.clock / frames).toFixed(0)} ms, seek ${(lap.seek / frames).toFixed(0)} ms, screenshot ${(lap.shot / frames).toFixed(0)} ms`);
    await context.close();
  } catch (e) {
    await browser.close().catch(() => {});
    throw e;
  }
  await browser.close();
  say.ok(`captured ${frames} frames in ${((Date.now() - started) / 1000).toFixed(0)} s${drift ? `  (virtual clock drifted on ${drift} frames)` : ''}`);

  /* ----- encode ----- */
  const ext = values.format === 'png' ? 'png' : 'jpg';
  const framePattern = path.join(partialDir, `frame-%06d.${ext}`);
  if (!canEncode) {
    say.line();
    say.info(`frames:  ${rel(partialDir)}${wavBuf ? `  (audio.wav inside)` : ''}`);
    say.info('encode later with:');
    say.line(`  ffmpeg -framerate ${fps} -start_number 0 -i "${framePattern}"${wavBuf ? ` -i "${path.join(partialDir, 'audio.wav')}"` : ''} -c:v libx264 -pix_fmt yuv420p -crf 18 -preset medium${wavBuf ? ' -c:a aac -b:a 192k' : ''} -movflags +faststart "${out}"`);
    for (const [msg] of state.failed) say.warn(`request failed: ${msg}`);
    process.exit(2);
  }

  let normalize = null;
  if (wavBuf) {
    say.info('loudness: measuring (pass 1)');
    normalize = await measureLoudness(path.join(partialDir, 'audio.wav'));
    if (normalize) say.info(`  input ${normalize.i.toFixed(1)} LUFS, true peak ${normalize.tp.toFixed(1)} dBTP, LRA ${normalize.lra.toFixed(1)}`);
    else say.warn('the soundtrack is silent: skipping loudness normalization');
  }
  const args = [
    '-y', '-hide_banner', '-loglevel', 'error', '-nostats',
    '-framerate', String(fps), '-start_number', '0', '-i', framePattern,
    ...(wavBuf ? ['-i', path.join(partialDir, 'audio.wav')] : []),
    '-map', '0:v', ...(wavBuf ? ['-map', '1:a'] : []),
    '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p',
    '-c:v', 'libx264', '-crf', '18', '-preset', 'medium',
    '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
    ...(wavBuf ? ['-af', `${normalize ? `${normalize.filter},` : ''}aresample=48000`, '-c:a', 'aac', '-b:a', '192k', '-ar', '48000'] : ['-an']),
    '-t', duration.toFixed(3), '-movflags', '+faststart', '-f', 'mp4', partialMp4,
  ];
  say.info('encoding (H.264, AAC)');
  const enc = await run('ffmpeg', args);
  if (enc.code !== 0) {
    try { fs.unlinkSync(partialMp4); } catch { /* nothing written */ }
    die(`ffmpeg failed (exit ${enc.code})`, [`      ${lastLines(enc.stderr)}`, `frames are kept in ${rel(partialDir)}; fix the cause and run the same command again`], 1);
  }
  try { fs.rmSync(out, { force: true }); } catch { /* replaced by the rename below */ }
  fs.renameSync(partialMp4, out);

  /* ----- measure ----- */
  const res = await inspectVideo(out);
  say.ok(`video  ${rel(out)}`);
  const v = res.video || {};
  say.ok(`${fmtSec(res.duration || 0)}, ${fmtBytes(res.size || fs.statSync(out).size)}, ${v.width}x${v.height} at ${v.fps ? v.fps.toFixed(2) : '?'} fps${v.frames ? `, ${v.frames} frames` : ''}, ${v.codec || '?'}${res.audio ? ` + ${res.audio.codec} ${res.audio.sampleRate} Hz` : ', no audio'}`);
  if (res.audio) {
    say.ok(`loudness  ${res.lufs === null ? '?' : `${res.lufs.toFixed(1)} LUFS`} integrated (target ${TARGET.I}), true peak ${res.truePeak === null ? '?' : `${res.truePeak.toFixed(1)} dBTP`} (limit ${TARGET.TP})`);
    if (res.lufs !== null && Math.abs(res.lufs - TARGET.I) > 1.5 && normalize) say.warn(`loudness is ${res.lufs.toFixed(1)} LUFS, more than 1.5 off the ${TARGET.I} target`);
    if (res.truePeak !== null && res.truePeak > -1) say.warn(`true peak ${res.truePeak.toFixed(1)} dBTP is above -1 dBTP`);
  }
  if (res.duration && Math.abs(res.duration - duration) > 0.15) say.warn(`file is ${res.duration.toFixed(2)} s, expected ${duration.toFixed(2)} s`);
  if (v.frames && v.frames !== frames) say.warn(`file has ${v.frames} frames, expected ${frames}`);

  /* ----- spot frames ----- */
  const spots = spotTimes(info.rows, duration).map((s) => {
    const fi = Math.min(frames - 1, Math.max(0, Math.round(s.t * fps))); // a real frame, so the seek always finds one
    return { label: s.label, t: fi / fps, ss: (Math.floor((fi / fps) * 1000) / 1000).toFixed(3) };
  });
  const written = [];
  for (const f of fs.readdirSync(path.dirname(out))) { // spot files of an earlier render with other labels
    if (f.startsWith(`${path.basename(stem)}.spot-`) && f.endsWith('.png')) fs.rmSync(path.join(path.dirname(out), f), { force: true });
  }
  for (let i = 0; i < spots.length; i++) {
    const png = `${stem}.spot-${i + 1}-${spots[i].label}.png`;
    const r = await run('ffmpeg', ['-y', '-hide_banner', '-loglevel', 'error', '-ss', spots[i].ss, '-i', out, '-frames:v', '1', '-an', png]);
    if (r.code === 0 && fs.existsSync(png)) written.push({ png, t: spots[i].t, label: spots[i].label });
    else say.warn(`could not extract the ${spots[i].label} frame at ${spots[i].t.toFixed(2)} s`);
  }
  for (const w of written) say.ok(`look  ${w.png}   (${w.label}, ${w.t.toFixed(1)} s)`);

  if (values.keepFrames) say.info(`frames kept in ${rel(partialDir)}`);
  else fs.rmSync(partialDir, { recursive: true, force: true });

  for (const [msg] of state.errors) say.warn(`console: ${msg}`);
  for (const [msg] of state.failed) say.warn(`request failed: ${msg}`);
  for (const [url] of state.external) say.warn(`external request: ${url}`);
  if (state.errors.size || state.failed.size || state.external.size) say.fix('run lint.mjs and shoot.mjs, fix the deck, render again');
  say.ok(`done in ${((Date.now() - started) / 1000).toFixed(0)} s. Open the PNGs above and check transitions, stamps and text before you report.`);
}

if (isMain(import.meta.url)) main().catch((e) => die(`render failed: ${String(e && e.message ? e.message : e).split('\n')[0]}`, 'node doctor.mjs', 1));
