#!/usr/bin/env node
// Render a short from a short.json file.
//
//   node render.mjs short.json            check, review sheet, cover and video
//   node render.mjs short.json --stills   check, review sheet and cover only (fast)
//   node render.mjs short.json --force    render even with warnings
//   node render.mjs short.json --out dir  output folder (default: out/<name of the json>)
//   node render.mjs short.json --concurrency 1   fewer parallel frames (if a render is killed for memory)
//
// Exit code 2 means there are warnings to fix (the sheet and cover are still written).

import { bundle } from "@remotion/bundler";
import { ensureBrowser, renderMedia, renderStill, selectComposition } from "@remotion/renderer";
import { createHash } from "node:crypto";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const args = process.argv.slice(2);
const flag = (f) => args.includes(f);
const opt = (f) => {
  const i = args.indexOf(f);
  return i >= 0 ? args[i + 1] : undefined;
};
const jsonPath = args.find((a, i) => !a.startsWith("--") && args[i - 1] !== "--out" && args[i - 1] !== "--concurrency");
if (!jsonPath) {
  console.log(fs.readFileSync(fileURLToPath(import.meta.url), "utf8").split("\n").slice(1, 9).join("\n").replace(/^\/\/ ?/gm, ""));
  process.exit(1);
}

const fail = (msg) => {
  console.error(`\nError: ${msg}`);
  process.exit(1);
};
// Show the cause in one line, not a stack trace.
const firstLine = (e) => String(e?.message ?? e).split("\n")[0].replace(/^Error:\s*/, "");
process.on("uncaughtException", (e) => fail(firstLine(e)));
process.on("unhandledRejection", (e) => fail(firstLine(e)));

const abs = path.resolve(jsonPath);
let props;
try {
  props = JSON.parse(fs.readFileSync(abs, "utf8"));
} catch (e) {
  fail(`could not read ${jsonPath}: ${e.message}`);
}
const name = path.basename(abs).replace(/\.json$/i, "");
const outDir = path.resolve(opt("--out") ?? path.join(here, "out", name));
fs.mkdirSync(outDir, { recursive: true });

// Copy every local file the short uses into public/assets so Remotion can serve it.
// Each short gets its own folder, so two renders at once never touch each other's files.
const assetsDir = path.join(here, "public", "assets", name.replace(/[^\w-]+/g, "-"));
const bring = (src, what) => {
  if (!src) return src;
  if (/^https?:\/\//i.test(src)) fail(`${what} is a URL (${src}). Download the file first and point to the local copy.`);
  const file = path.resolve(path.dirname(abs), src);
  if (!fs.existsSync(file)) fail(`${what} not found: ${file}`);
  const ext = path.extname(file).toLowerCase();
  const ok = [".mp3", ".wav", ".m4a", ".aac", ".ogg", ".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".webm", ".m4v"];
  if (!ok.includes(ext)) fail(`${what} has an unsupported file type (${ext}).`);
  const hash = createHash("sha1").update(fs.readFileSync(file)).digest("hex").slice(0, 10);
  fs.mkdirSync(assetsDir, { recursive: true });
  const dest = `${path.basename(file, ext).replace(/[^\w-]+/g, "-")}-${hash}${ext}`;
  if (!fs.existsSync(path.join(assetsDir, dest))) fs.copyFileSync(file, path.join(assetsDir, dest));
  return `assets/${path.basename(assetsDir)}/${dest}`;
};
// Remotion merges the Studio sample's props under these; null every option this file leaves out.
for (const k of ["theme", "font", "fps", "pace", "bpm", "music", "background", "footer", "handle", "highlightStyle", "progress", "sfx", "sfxVolume"]) {
  if (!(k in props)) props[k] = null;
}
if (props.music) props.music = { ...props.music, src: bring(props.music.src, "music.src") };
props.background = bring(props.background, "background");
(props.scenes ?? []).forEach((s, i) => (s.image = bring(s.image, `scenes[${i}].image`)));
// Keep this short's asset folder to the files it uses now.
const used = new Set([props.music?.src, props.background, ...(props.scenes ?? []).map((s) => s.image)].filter(Boolean).map((p) => path.basename(p)));
if (fs.existsSync(assetsDir)) for (const f of fs.readdirSync(assetsDir)) if (!used.has(f)) fs.rmSync(path.join(assetsDir, f), { force: true });

const t0 = Date.now();
const secs = () => `${((Date.now() - t0) / 1000).toFixed(0)}s`;

console.log("Preparing the renderer (the first run downloads a headless browser, about 100 MB)...");
await ensureBrowser();
console.log("Bundling...");
const serveUrl = await bundle({ entryPoint: path.join(here, "src", "index.ts"), publicDir: path.join(here, "public") });

const comp = await selectComposition({ serveUrl, id: "Short", inputProps: props, logLevel: "error" });
const planned = comp.props;
const fps = comp.fps;
const total = comp.durationInFrames / fps;
const warnings = [...(planned.warnings ?? [])];

// Platform limits (see references/platform-specs.md).
if (total > 59)
  warnings.push(`The short is ${total.toFixed(1)}s. Keep it under 60s: YouTube blocks Shorts over a minute worldwide if any copyright claim lands on them, and text shorts lose people long before that.`);
if (total < 5) warnings.push(`The short is only ${total.toFixed(1)}s. Add a scene or two.`);

console.log(`\nPlan: ${planned.scenes.length} scenes, ${total.toFixed(1)}s at ${fps} fps${planned.layout[0].blocks.footer ? `, footer ${planned.layout[0].blocks.footer.fontSize}px` : ""}\n`);
planned.layout.forEach((l, i) => {
  const s = planned.scenes[i];
  const sizes = Object.entries(l.blocks)
    .filter(([k]) => k !== "footer")
    .map(([k, b]) => `${k} ${b.fontSize}px/${b.lines.length} line${b.lines.length > 1 ? "s" : ""}`)
    .join(", ");
  console.log(`  ${String(i + 1).padStart(2)}. ${s.type.padEnd(5)} ${(l.frames / fps).toFixed(1).padStart(4)}s  ${sizes}`);
});

for (const [id, file] of [["Sheet", "sheet.jpg"], ["Cuts", "cuts.jpg"]]) {
  const c = await selectComposition({ serveUrl, id, inputProps: props, logLevel: "error" });
  await renderStill({ composition: c, serveUrl, inputProps: props, output: path.join(outDir, file), imageFormat: "jpeg", jpegQuality: 85, logLevel: "error" });
}
// The hook once its highlight and punch have landed.
const coverFrame = Math.min(planned.layout[0].frames - 1, 30);
await renderStill({ composition: comp, serveUrl, inputProps: props, frame: coverFrame, output: path.join(outDir, "cover.jpg"), imageFormat: "jpeg", jpegQuality: 92, logLevel: "error" });
console.log(`\nReview sheet: ${path.join(outDir, "sheet.jpg")} (last frame of every scene; dashed line = safe area, text must stay inside)`);
console.log(`Cut sheet: ${path.join(outDir, "cuts.jpg")} (frame 0 and the frames around every cut)`);
console.log(`Cover: ${path.join(outDir, "cover.jpg")} (frame ${coverFrame}, ${(coverFrame / fps).toFixed(2)}s)`);

const report = {
  source: path.relative(outDir, abs).split(path.sep).join("/"),
  seconds: Number(total.toFixed(2)),
  fps,
  width: comp.width,
  height: comp.height,
  coverFrame,
  scenes: planned.layout.map((l, i) => ({
    type: planned.scenes[i].type,
    start: Number((l.from / fps).toFixed(2)),
    seconds: Number((l.frames / fps).toFixed(2)),
    blocks: Object.fromEntries(Object.entries(l.blocks).map(([k, b]) => [k, { fontSize: b.fontSize, lines: b.lines.map((w) => w.join(" ")) }])),
  })),
  warnings,
};
const writeReport = (extra = {}) =>
  fs.writeFileSync(path.join(outDir, "report.json"), JSON.stringify({ ...report, ...extra }, null, 2) + "\n");

if (warnings.length) {
  console.log(`\n${warnings.length} warning${warnings.length > 1 ? "s" : ""}:`);
  warnings.forEach((w) => console.log(`  - ${w}`));
}
if (warnings.length && !flag("--force")) {
  writeReport({ video: null });
  console.log("\nFix the warnings in the JSON and run again, or add --force to render anyway.");
  process.exit(2);
}
if (flag("--stills")) {
  writeReport({ video: null });
  console.log(`\nStills done in ${secs()}. Run without --stills to render the video.`);
  process.exit(0);
}

const video = path.join(outDir, `${name}.mp4`);
const concurrency = opt("--concurrency")
  ? Math.max(1, Number(opt("--concurrency")) || 1)
  : os.totalmem() <= 8 * 2 ** 30
    ? 2
    : Math.max(1, Math.min(6, Math.floor(os.cpus().length / 2)));
let last = -1;
await renderMedia({
  composition: comp,
  serveUrl,
  inputProps: props,
  codec: "h264",
  crf: 18,
  pixelFormat: "yuv420p",
  colorSpace: "bt709",
  imageFormat: "jpeg",
  jpegQuality: 92,
  audioCodec: "aac",
  audioBitrate: "192k",
  enforceAudioTrack: true,
  concurrency,
  outputLocation: video,
  logLevel: "error",
  onProgress: ({ progress }) => {
    const p = Math.floor(progress * 10);
    if (p !== last) {
      last = p;
      process.stdout.write(`\rRendering ${p * 10}%`);
    }
  },
});
const bytes = fs.statSync(video).size;
writeReport({ video: path.basename(video), bytes });
console.log(`\n\nVideo: ${video} (${(bytes / 1e6).toFixed(1)} MB, ${total.toFixed(1)}s) in ${secs()}`);
console.log(`Report: ${path.join(outDir, "report.json")}`);
