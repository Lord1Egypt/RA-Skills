#!/usr/bin/env node
/**
 * see-video: 영상에서 LLM용 프레임 그리드 추출
 * Usage: node inject.mjs <video_path> [--mode uniform|highlight] [--start N] [--end N]
 * Output: JSON stdout { gridPath, description, duration, frameCount, layout, videoWidth, videoHeight, inputSizeMb }
 */
import { extract } from "llm-frames";
import { writeFile, stat } from "fs/promises";
import { tmpdir } from "os";
import { join, basename, extname } from "path";
import { randomBytes } from "crypto";

const args = process.argv.slice(2);

if (!args[0] || args[0] === "--help") {
  console.error("Usage: inject.mjs <video_path> [--mode uniform|highlight] [--start N] [--end N]");
  process.exit(1);
}

const opts = { input: args[0] };

for (let i = 1; i < args.length; i++) {
  if (args[i] === "--mode"  && args[i + 1]) opts.mode      = args[++i];
  if (args[i] === "--start" && args[i + 1]) opts.startTime = Number(args[++i]);
  if (args[i] === "--end"   && args[i + 1]) opts.endTime   = Number(args[++i]);
}

// Pre-flight: 파일 존재 및 크기 확인
let inputSizeMb;
try {
  const s = await stat(opts.input);
  inputSizeMb = parseFloat((s.size / 1024 / 1024).toFixed(1));
} catch {
  console.error(`ERROR: Input file not found: ${opts.input}`);
  console.error(`Hint: If the file was received via a messaging channel, it may have been dropped due to the channel's media size limit. Ask the user to share the file path directly as text.`);
  process.exit(1);
}

try {
  const result = await extract(opts);

  const name = basename(opts.input, extname(opts.input));
  const suffix = randomBytes(6).toString("hex");
  const gridPath = join(tmpdir(), `${name}_llm-frames_${suffix}.jpg`);
  await writeFile(gridPath, result.grid);

  const isLong = result.duration > 600 && !opts.startTime && !opts.endTime && opts.mode !== "highlight";

  console.log(JSON.stringify({
    gridPath,
    description: result.description,
    duration: result.duration,
    frameCount: result.frames.length,
    layout: result.metadata.layout,
    videoWidth: result.videoWidth,
    videoHeight: result.videoHeight,
    inputSizeMb,
    ...(isLong && {
      hint: `Video is ${Math.round(result.duration / 60)} minutes long. This is a uniform overview. For better scene coverage re-run with --mode highlight, or use --start/--end to zoom into a specific section.`,
    }),
  }, null, 2));
} catch (e) {
  const msg = e.message ?? String(e);

  if (/ENOENT|not found|No such file/i.test(msg)) {
    console.error(`ERROR: Could not access input file: ${opts.input}`);
    console.error(`Hint: Check file path and permissions.`);
  } else if (/Invalid data|moov atom|codec|decoder|format/i.test(msg)) {
    console.error(`ERROR: Could not read video — file may be corrupt, incomplete, or in an unsupported format.`);
    console.error(`Detail: ${msg}`);
    console.error(`Hint: Try a different file, or use --start/--end to skip problematic sections.`);
  } else if (/spawn.*ffmpeg|ffmpeg.*not found|ENOENT.*ffmpeg/i.test(msg)) {
    console.error(`ERROR: ffmpeg not found. Install ffmpeg and ensure it is in PATH.`);
  } else {
    console.error(`ERROR: ${msg}`);
  }
  process.exit(1);
}
