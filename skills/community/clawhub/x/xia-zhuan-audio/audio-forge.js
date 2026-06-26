#!/usr/bin/env node
/**
 * xia-zhuan-audio - 音频格式转换与处理工具
 * 基于 FFmpeg，支持格式转换、视频提取音频、合并、分割、压缩
 *
 * 环境变量配置（可选，不设置则自动查找）：
 *   XZA_FFMPEG   - FFmpeg/FFprobe 路径
 *   XZA_SCRIPTDIR - 技能脚本目录（包含 um.exe 和 transcribe.py）
 *
 * 自动查找顺序：
 *   1. 环境变量指定的路径
 *   2. 系统 PATH 中的 ffmpeg/ffprobe
 *   3. winget 安装的路径
 */

const { execSync, spawn, execFile } = require("child_process");
const path = require("path");
const fs = require("fs");

// ---------- 路径配置 ----------
function findFFmpeg() {
  // 1. 环境变量
  if (process.env.XZA_FFMPEG) return process.env.XZA_FFMPEG;

  // 2. 系统 PATH
  const sys = require("child_process");
  try {
    const out = sys.execSync("where ffmpeg", { encoding: "utf8", shell: true }).trim().split("\n")[0];
    if (out && fs.existsSync(out)) return out;
  } catch {}

}

function findFFprobe() {
  if (process.env.XZA_FFPROBE) return process.env.XZA_FFPROBE;
  if (process.env.XZA_FFMPEG) {
    const fp = process.env.XZA_FFMPEG.replace("ffmpeg.exe", "ffprobe.exe");
    if (fs.existsSync(fp)) return fp;
  }
  const ff = findFFmpeg();
  return ff.replace("ffmpeg.exe", "ffprobe.exe");
}

function getScriptDir() {
  // 优先用环境变量
  if (process.env.XZA_SCRIPTDIR) return process.env.XZA_SCRIPTDIR;
  // 默认：取当前脚本所在目录
  return __dirname;
}

const FFMPEG = findFFmpeg();
const FFPROBE = findFFprobe();
const SCRIPT_DIR = getScriptDir();
const UM = path.join(SCRIPT_DIR, "um.exe");

// ---------- 辅助函数 ----------
function getDuration(file) {
  try {
    const info = execFile(FFPROBE, ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", "--", file], { encoding: "utf8" });
    return parseFloat(info.trim());
  } catch {
    return null;
  }
}

function formatTime(seconds) {
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  return `${h.toString().padStart(2, "0")}:${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
}

function runFFmpeg(args) {
  // Strip extra quotes from args (added by callers for shell safety) since spawn passes them literally
  const cleanArgs = args.map(a => typeof a === 'string' && a.startsWith('"') && a.endsWith('"') ? a.slice(1, -1) : a);
  const { spawn } = require("child_process");
  console.log("  执行: ffmpeg -y " + cleanArgs.join(" "));
  spawn(FFMPEG, ["-y", ...cleanArgs], { stdio: "inherit" }).on("close", (code) => {
    if (code !== 0) console.log("  ffmpeg 错误，退出码:", code);
  });
}

function ensureExtension(file, ext) {
  return file.replace(/\.[^.]+$/, "") + "." + ext;
}

function formatBytes(bytes) {
  if (bytes < 1024) return bytes + " B";
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + " KB";
  return (bytes / (1024 * 1024)).toFixed(2) + " MB";
}

// ---------- 命令处理 ----------

/**
 * 格式转换
 * node audio-forge.js convert <input> <output-format> [--bitrate 192k]
 */
function cmdConvert(input, outputFormat, options = {}) {
  const output = options.output || ensureExtension(input, outputFormat);
  const bitrate = options.bitrate || "192k";

  console.log(`\n  音频格式转换`);
  console.log(`  输入: ${input}`);
  console.log(`  输出: ${output}`);
  console.log(`  目标格式: ${outputFormat.toUpperCase()}`);
  console.log(`  码率: ${bitrate}`);

  const args = [
    "-i", `"${input}"`,
    "-vn",
    "-ar", "44100",
    "-ac", "2",
    "-b:a", bitrate
  ];

  if (outputFormat === "mp3") {
    args.push("-id3v2_version", "3", `"${output}"`);
  } else if (outputFormat === "aac" || outputFormat === "m4a") {
    args.push("-c:a", "aac", "-b:a", bitrate, `"${output}"`);
  } else if (outputFormat === "flac") {
    args.push("-c:a", "flac", `"${output}"`);
  } else if (outputFormat === "wav") {
    args.push("-c:a", "pcm_s16le", `"${output}"`);
  } else {
    args[args.length - 1] = `"${output}"`;
  }

  runFFmpeg(args);
  console.log(`\n  转换完成: ${output}`);
}

/**
 * 从视频提取音频
 * node audio-forge.js extract <video> [output-format] [--bitrate 192k]
 */
function cmdExtract(video, outputFormat = "mp3", options = {}) {
  const output = options.output || ensureExtension(video, outputFormat);
  const bitrate = options.bitrate || "192k";

  console.log(`\n  视频提取音频`);
  console.log(`  视频: ${video}`);
  console.log(`  音频: ${output}`);

  const args = [
    "-i", `"${video}"`,
    "-vn",
    "-ac", "2",
    "-ar", "44100",
    "-b:a", bitrate
  ];

  if (outputFormat === "mp3") {
    args.push("-id3v2_version", "3", `"${output}"`);
  } else if (outputFormat === "aac" || outputFormat === "m4a") {
    args.push("-c:a", "aac", `"${output}"`);
  } else if (outputFormat === "wav") {
    args.push("-c:a", "pcm_s16le", `"${output}"`);
  } else {
    args.push(`"${output}"`);
  }

  runFFmpeg(args);
  console.log(`\n  提取完成: ${output}`);
}

/**
 * 合并多个音频文件
 * node audio-forge.js merge <file1> <file2> [...] <output>
 */
function cmdMerge(files, output) {
  const listFile = path.join(process.env.TEMP || "/tmp", "xza_merge_list.txt");
  console.log(`\n  音频合并`);
  console.log(`  文件数量: ${files.length}`);

  const content = files.map(f => `file '${f.replace(/\\/g, "/")}'`).join("\n");
  fs.writeFileSync(listFile, content, "utf8");

  const args = [
    "-f", "concat",
    "-safe", "0",
    "-i", `"${listFile}"`,
    "-c", "copy",
    `"${output}"`
  ];

  runFFmpeg(args);
  fs.unlinkSync(listFile);
  console.log(`\n  合并完成: ${output}`);
}

/**
 * 分割音频
 * node audio-forge.js split <input> <start> <end> [--output <file>]
 */
function cmdSplit(input, start, end, output) {
  const out = output || ensureExtension(input, "mp3");
  console.log(`\n  音频分割`);
  console.log(`  输入: ${input}`);
  console.log(`  范围: ${start} → ${end}`);
  console.log(`  输出: ${out}`);

  const args = [
    "-i", `"${input}"`,
    "-ss", start,
    "-to", end,
    "-c", "copy",
    `"${out}"`
  ];

  runFFmpeg(args);
  console.log(`\n  分割完成: ${out}`);
}

/**
 * 压缩音频
 * node audio-forge.js compress <input> [--quality low|medium|high] [--output <file>]
 */
function cmdCompress(input, output, options = {}) {
  const out = output || ensureExtension(input, "mp3");
  const quality = options.quality || "medium";

  const qualityMap = {
    low:    { bitrate: "64k" },
    medium: { bitrate: "128k" },
    high:   { bitrate: "192k" }
  };
  const q = qualityMap[quality] || qualityMap.medium;

  console.log(`\n  音频压缩`);
  console.log(`  输入: ${input}`);
  console.log(`  输出: ${out}`);
  console.log(`  压缩级别: ${quality}`);
  console.log(`  输出码率: ${q.bitrate}`);

  const args = [
    "-i", `"${input}"`,
    "-vn",
    "-ac", "2",
    "-ar", "44100",
    "-b:a", q.bitrate,
    `"${out}"`
  ];

  runFFmpeg(args);

  const inputSize = fs.statSync(input).size;
  const outputSize = fs.statSync(out).size;
  const ratio = ((1 - outputSize / inputSize) * 100).toFixed(1);
  console.log(`\n  压缩率: ${ratio}% (${formatBytes(inputSize)} → ${formatBytes(outputSize)})`);
  console.log(`  压缩完成: ${out}`);
}

/**
 * 查看音频信息
 * node audio-forge.js info <file>
 */
function cmdInfo(file) {
  console.log(`\n  音频信息: ${file}`);
  try {
    const raw = execFile(FFPROBE, ["-v", "error", "-show_format", "-show_streams", "--", file], { encoding: "utf8" });
    console.log(parseAudioInfo(raw, file));
  } catch (e) {
    console.log("无法获取音频信息:", e.message);
  }
}

function parseAudioInfo(raw, filePath) {
  const lines = raw.split('\n').map(l => l.trim());
  const info = { streams: [], format: {} };
  let current = null;

  for (const line of lines) {
    if (line === '[STREAM]') { current = {}; info.streams.push(current); }
    else if (line === '[/STREAM]') { current = null; }
    else if (line === '[FORMAT]') { current = info.format; }
    else if (line === '[/FORMAT]') { current = null; }
    else if (current && line.includes('=')) {
      const [k, ...v] = line.split('=');
      current[k] = v.join('=');
    }
  }

  const stream = info.streams.find(s => s.codec_type === 'audio') || info.streams[0] || {};
  const fmt = info.format;
  const duration = parseFloat(fmt.duration || stream.duration || 0);
  const size = parseInt(fmt.size || 0);
  const bitrate = parseInt(fmt.bit_rate || stream.bit_rate || 0);

  const durStr = formatDuration(duration);
  const sizeStr = formatBytes(size);
  const brStr = bitrate >= 1000 ? Math.round(bitrate / 1000) + ' kbps' : bitrate + ' bps';
  const sampleStr = stream.sample_rate ? (parseInt(stream.sample_rate) / 1000) + ' kHz' : 'N/A';
  const channels = stream.channels === '1' ? '单声道' : stream.channels === '2' ? '立体声' : (stream.channels || 'N/A');
  const codec = stream.codec_name ? stream.codec_name.toUpperCase() : 'N/A';

  const name = filePath.split('\\').pop();
  let out = `\n  +-- 基本信息 ----------------------------------+`;
  out += `\n  | 文件名: ${name}`;
  out += `\n  +-----------------------------------------------+`;
  out += `\n  | 时长:   ${durStr}`;
  out += `\n  | 大小:   ${sizeStr}`;
  out += `\n  +-----------------------------------------------+`;
  out += `\n  | 编码:   ${codec}`;
  out += `\n  | 码率:   ${brStr}`;
  out += `\n  | 采样率: ${sampleStr}`;
  out += `\n  | 声道:   ${channels}`;
  out += `\n  +-----------------------------------------------+`;
  if (fmt.TAG_title) out += `\n  | 标题:   ${fmt.TAG_title}`;
  if (fmt.TAG_artist) out += `\n  | 艺术家: ${fmt.TAG_artist}`;
  if (fmt.TAG_album) out += `\n  | 专辑:   ${fmt.TAG_album}`;
  if (fmt.TAG_date) out += `\n  | 日期:   ${fmt.TAG_date}`;
  out += `\n  +-----------------------------------------------+`;
  return out;
}

function formatDuration(seconds) {
  if (!seconds || isNaN(seconds)) return 'N/A';
  const h = Math.floor(seconds / 3600);
  const m = Math.floor((seconds % 3600) / 60);
  const s = Math.floor(seconds % 60);
  if (h > 0) return h + '小时 ' + m + '分 ' + s + '秒';
  if (m > 0) return m + '分 ' + s + '秒';
  return s + '秒';
}

// ---------- CLI 入口 ----------

const [,, cmd, ...args] = process.argv;

function showHelp() {
  console.log(`
xia-zhuan-audio - 音频格式转换与处理工具

用法:
  node audio-forge.js <命令> [参数]

命令:
  convert <输入文件> <输出格式> [选项]    格式转换
    支持格式: mp3 wav flac aac m4a ogg wma aiff opus
    例: audio-forge.js convert song.m4a mp3
        audio-forge.js convert song.m4a mp3 --bitrate 320k

  extract <视频文件> [输出格式]          从视频提取音频
    例: audio-forge.js extract video.mp4 mp3

  merge <文件1> <文件2> [...] <输出>     合并多个音频
    例: audio-forge.js merge a.mp3 b.mp3 c.mp3 output.mp3

  split <输入文件> <开始时间> <结束时间> [选项]
                                            分割音频
    例: audio-forge.js split song.mp3 00:01:00 00:02:30

  compress <输入文件> [选项]               压缩音频
    例: audio-forge.js compress large.mp3 --quality high

  info <音频文件>                        查看音频信息

环境变量:
  XZA_FFMPEG    FFmpeg/FFprobe 路径（不设置则自动查找）
  XZA_FFPROBE   FFprobe 路径（默认从 XZA_FFMPEG 推断）
  XZA_SCRIPTDIR 脚本所在目录（包含 um.exe 和 transcribe.py）
`);
}

if (!cmd || cmd === "help" || cmd === "--help") {
  showHelp();
  process.exit(0);
}

(async () => {
  try {
    switch (cmd) {
      case "convert": {
        const input = args[0];
        const format = args[1];
        const opts = parseArgs(args.slice(2));
        if (!input || !format) { console.log("缺少参数"); showHelp(); process.exit(1); }
        cmdConvert(input, format, opts);
        break;
      }
      case "extract": {
        const input = args[0];
        const format = args[1] || "mp3";
        const opts = parseArgs(args.slice(2));
        if (!input) { console.log("缺少参数"); showHelp(); process.exit(1); }
        cmdExtract(input, format, opts);
        break;
      }
      case "merge": {
        if (args.length < 3) { console.log("合并至少需要2个文件"); showHelp(); process.exit(1); }
        const output = args[args.length - 1];
        const files = args.slice(0, -1);
        cmdMerge(files, output);
        break;
      }
      case "split": {
        const [input, start, end, ...rest] = args;
        const opts = parseArgs(rest);
        if (!input || !start || !end) { console.log("缺少参数"); showHelp(); process.exit(1); }
        cmdSplit(input, start, end, opts.output || null);
        break;
      }
      case "compress": {
        const [input, ...rest] = args;
        const opts = parseArgs(rest);
        if (!input) { console.log("缺少参数"); showHelp(); process.exit(1); }
        cmdCompress(input, opts.output || null, opts);
        break;
      }
      case "info": {
        const input = args[0];
        if (!input) { console.log("缺少参数"); showHelp(); process.exit(1); }
        cmdInfo(input);
        break;
      }
      default:
        console.log(`未知命令: ${cmd}`);
        showHelp();
        process.exit(1);
    }
  } catch (err) {
    console.error(`\n错误: ${err.message}`);
    process.exit(1);
  }
})();

function parseArgs(args) {
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === "--output" && args[i + 1]) {
      opts.output = args[++i];
    } else if (args[i] === "--bitrate" && args[i + 1]) {
      opts.bitrate = args[++i];
    } else if (args[i] === "--quality" && args[i + 1]) {
      opts.quality = args[++i];
    }
  }
  return opts;
}
