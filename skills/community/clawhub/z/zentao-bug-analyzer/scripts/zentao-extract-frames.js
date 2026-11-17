#!/usr/bin/env node
/**
 * zentao-extract-frames.js — 视频抽帧 + ffprobe 一体化脚本
 *
 * 用法:
 *   node zentao-extract-frames.js --video=<path> --dir=<output_dir> [--mode=coarse|fine|probe]
 *
 *   --mode=coarse  2 秒 1 帧抽帧（用于粗扫确认 BUG 是否可见）
 *   --mode=fine    1 秒 1 帧抽帧（用于读取状态栏时间）
 *   --mode=probe   仅输出视频元数据（时长/分辨率/帧率），不需要 --dir
 *
 * 输出文件名格式（与 SKILL.md 4b 章节对齐）:
 *   coarse 模式 → <dir>/coarse_%03d.png   (coarse_001.png, coarse_002.png ...)
 *   fine   模式 → <dir>/sec_%04d.png      (sec_0001.png, sec_0002.png ...)
 *
 * 依赖: scripts/ 已 npm install @ffmpeg-installer/ffmpeg
 *   首次安装见 SKILL.md「环境依赖」章节。
 */

const { execSync } = require('child_process');
const ff = require('@ffmpeg-installer/ffmpeg').path;
const fs = require('fs');

// 兼容 PowerShell 调用方式：
//   1. node script.js --key=val --key2=val2     (类 Unix 风格)
//   2. node script.js -- key1=val key2=val2      (PowerShell 兼容，规避 argv 解析 bug)
const argv = process.argv.slice(2);
const _hasSep = argv[0] === '--';
const args = _hasSep ? argv.slice(1) : argv;

function getArg(name) {
  // 先扫 --name=val 形式
  for (const a of args) {
    if (a.startsWith(`--${name}=`)) return a.slice(name.length + 3);
  }
  // 再扫 --name val 形式
  for (let i = 0; i < args.length - 1; i++) {
    if (args[i] === `--${name}`) return args[i + 1];
  }
  return null;
}

const video = getArg('video');
const dir = getArg('dir');
const mode = getArg('mode') || 'probe';

if (!video) {
  console.error('[ERROR] --video 参数必填');
  process.exit(1);
}
if (mode !== 'probe' && !dir) {
  console.error('[ERROR] --dir 参数必填（仅 probe 模式可省略）');
  process.exit(1);
}

if (!fs.existsSync(video)) {
  console.error(`[ERROR] 视频文件不存在: ${video}`);
  process.exit(1);
}

// probe 模式：用 ffmpeg -i 输出元数据到 stderr（execSync 失败时 stderr 里有内容）
if (mode === 'probe') {
  console.error(`[INFO] ffprobe: ${video}`);
  let meta = '';
  try {
    meta = execSync(`"${ff}" -i "${video}"`, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
  } catch (e) {
    // ffmpeg -i 无输出文件时 exit code 非 0，但 stderr 有完整元数据
    meta = (e.stderr || '') + (e.stdout || '');
  }
  if (meta) {
    console.log(meta);
    console.error('[INFO] ffprobe 完成');
    process.exit(0);
  } else {
    console.error('[ERROR] ffprobe 未返回任何元数据');
    process.exit(1);
  }
}

// coarse / fine 模式：实际抽帧
fs.mkdirSync(dir, { recursive: true });

const fps = mode === 'coarse' ? '1/2' : '1';
const prefix = mode === 'coarse' ? 'coarse_' : 'sec_';
const width = mode === 'coarse' ? 3 : 4; // 文件名编号位数：coarse%03d / sec%04d
const pattern = `${prefix}%0${width}d.png`;
const outPath = `${dir.replace(/[\\/]+$/, '')}/${pattern}`;

console.error(`[INFO] 抽帧 (${mode}, fps=${fps}): ${video} → ${outPath}`);

try {
  execSync(`"${ff}" -i "${video}" -vf "fps=${fps}" "${outPath}" -y`, { stdio: 'inherit' });
  const count = fs.readdirSync(dir).filter(f => f.startsWith(prefix)).length;
  console.error(`[INFO] 完成: ${count} 帧`);
  console.log(`OK ${count}`);
} catch (e) {
  console.error(`[ERROR] 抽帧失败: ${e.message}`);
  process.exit(1);
}