#!/usr/bin/env node
/**
 * xia-zhuan-audio 交互菜单 - 美化版
 */
const readline = require("readline");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const SCRIPT = path.join(__dirname, "audio-forge.js");

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

let menuColorIdx = 0;
const menuColors = ["\x1b[36m", "\x1b[33m", "\x1b[35m", "\x1b[32m"]; // 轮流颜色

function prompt(question) {
  return new Promise((resolve) => {
    rl.question(question, (answer) => resolve(answer));
  });
}

function clear() {
  console.clear();
}

function sp(n) { return " ".repeat(n); }
function line(w = 50, ch = "─") { return ch.repeat(w); }
function pad(s, len, ch = " ") { return String(s).padEnd(len, ch); }
function padc(s, len, ch = " ") {
  const p = len - String(s).length;
  return p > 0 ? ch.repeat(Math.floor(p/2)) + s + ch.repeat(Math.ceil(p/2)) : s;
}

function printBanner() {
  const w = 50;
  console.log("");
  console.log("\x1b[1m\x1b[36m  ╔" + line(w, "═") + "╗\x1b[0m");
  console.log("\x1b[1m\x1b[36m  ║\x1b[0m" + padc("🎵 xia-zhuan-audio 音频工具箱", w) + "\x1b[1m\x1b[36m║\x1b[0m");
  console.log("\x1b[1m\x1b[36m  ╠" + line(w, "═") + "╣\x1b[0m");
  console.log("\x1b[1m\x1b[36m  ║\x1b[0m" + padc("v1.2  |  FFmpeg + Whisper AI", w) + "\x1b[1m\x1b[36m║\x1b[0m");
  console.log("\x1b[1m\x1b[36m  ╚" + line(w, "═") + "╝\x1b[0m");
  console.log("");
}

function printSection(title, items) {
  const w = 50;
  console.log("\x1b[1m\x1b[33m  ┌" + line(w, "─") + "┐\x1b[0m");
  console.log("\x1b[1m\x1b[33m  │[0m" + padc(title, w) + "\x1b[1m\x1b[33m│\x1b[0m");
  console.log("\x1b[1m\x1b[33m  └" + line(w, "─") + "┘\x1b[0m");
  for (const [key, label, desc] of items) {
    const col = menuColors[menuColorIdx++ % menuColors.length];
    console.log(`  ${col}[${key}]\x1b[0m ${label}  \x1b[90m${desc}\x1b[0m`);
  }
}

function printFooter() {
  const w = 50;
  console.log("");
  console.log("\x1b[90m  ╔" + line(w, "─") + "╗\x1b[0m");
  console.log("\x1b[90m  │\x1b[0m" + padc("输入 Q 退出", w) + "\x1b[90m│\x1b[0m");
  console.log("\x1b[90m  ╚" + line(w, "─") + "╝\x1b[0m");
  console.log("");
}

async function runFF(args) {
  return new Promise((resolve) => {
    const child = spawn("node", [SCRIPT, ...args], { stdio: "inherit" });
    child.on("close", (code) => resolve(code));
  });
}


async function menu() {
  while (true) {
    clear();
    printBanner();
    printSection("  音视频转换", [
      ["1", "格式转换",       "m4a→mp3, wav→flac, ape→flac"],
      ["2", "视频提取音频",   "mp4/mkv/avi → mp3/aac"],
      ["3", "合并多个音频",   "将多个音频拼接成一个"],
      ["4", "分割音频",       "按时间段截取音频片段"],
      ["5", "压缩音频",       "减小文件体积"],
    ]);
    printSection("  高级功能", [
      ["6", "查看音频信息",   "时长/码率/采样率/声道等"],
      ["7", "音频转文字",     "Whisper AI 自动转录，支持 txt/srt/vtt/json"],
    ]);
    printFooter();

    menuColorIdx = 0;
    const choice = await prompt("  请选择功能 [1-8, Q]: ");

    if (choice.toUpperCase() === "Q") {
      clear();
      console.log("\n  \x1b[32m再见！音频工具箱退出中...\x1b[0m\n");
      rl.close();
      process.exit(0);
    }

    switch (choice) {
      case "1": await cmdConvert(); break;
      case "2": await cmdExtract(); break;
      case "3": await cmdMerge(); break;
      case "4": await cmdSplit(); break;
      case "5": await cmdCompress(); break;
      case "6": await cmdInfo(); break;
      case "7": await cmdTranscribe(); break;
      default:
        console.log("\n  \x1b[31m无效选项，请重新选择\x1b[0m");
        await sleep(1200);
    }
  }
}

async function cmdConvert() {
  clear();
  console.log("\n  \x1b[1m\x1b[36m── 格式转换 ──\x1b[0m\n");
  console.log("  \x1b[90m支持: mp3 wav flac aac m4a ogg wma aiff opus\x1b[0m\n");

  const input = await prompt("  📂 请输入源文件路径: ");
  if (!input.trim()) return;

  const format = await prompt("  🎯 请输入目标格式 (如 mp3): ");
  if (!format.trim()) return;

  const bitrate = await prompt("  📊 码率 (直接回车默认 192k): ");

  console.log("");
  const args = ["convert", input.trim(), format.trim()];
  if (bitrate.trim()) args.push("--bitrate", bitrate.trim());
  await runFF(args);
  await prompt("\n  按回车继续...");
}

async function cmdExtract() {
  clear();
  console.log("\n  \x1b[1m\x1b[36m── 视频提取音频 ──\x1b[0m\n");

  const input = await prompt("  🎬 请输入视频文件路径: ");
  if (!input.trim()) return;

  const format = await prompt("  🎯 输出格式 (直接回车默认 mp3): ") || "mp3";
  const bitrate = await prompt("  📊 码率 (直接回车默认 192k): ");

  console.log("");
  const args = ["extract", input.trim(), format.trim()];
  if (bitrate.trim()) args.push("--bitrate", bitrate.trim());
  await runFF(args);
  await prompt("\n  按回车继续...");
}

async function cmdMerge() {
  clear();
  console.log("\n  \x1b[1m\x1b[36m── 合并多个音频 ──\x1b[0m\n");

  const countStr = await prompt("  🔢 要合并几个文件?: ");
  const count = parseInt(countStr);
  if (isNaN(count) || count < 2) {
    console.log("\n  \x1b[31m至少需要2个文件\x1b[0m");
    await sleep(1500);
    return;
  }

  const files = [];
  for (let i = 1; i <= count; i++) {
    const f = await prompt(`  📁 文件 ${i}: `);
    if (f.trim()) files.push(f.trim());
  }

  const output = await prompt("  💾 输出文件名 (如 result.mp3): ");
  if (!output.trim()) return;

  console.log("");
  await runFF(["merge", ...files, output.trim()]);
  await prompt("\n  按回车继续...");
}

async function cmdSplit() {
  clear();
  console.log("\n  \x1b[1m\x1b[36m── 分割音频 ──\x1b[0m\n");
  console.log("  \x1b[90m时间格式: HH:MM:SS 或 秒数，如 00:01:30\x1b[0m\n");

  const input = await prompt("  📂 输入文件: ");
  if (!input.trim()) return;

  const start = await prompt("  ⏱  开始时间 (如 00:01:00): ");
  const end = await prompt("  ⏱  结束时间 (如 00:02:30): ");
  if (!start.trim() || !end.trim()) return;

  const output = await prompt("  💾 输出文件 (直接回车自动命名): ");

  console.log("");
  const args = ["split", input.trim(), start.trim(), end.trim()];
  if (output.trim()) args.push("--output", output.trim());
  await runFF(args);
  await prompt("\n  按回车继续...");
}

async function cmdCompress() {
  clear();
  console.log("\n  \x1b[1m\x1b[36m── 压缩音频 ──\x1b[0m\n");
  console.log("  \x1b[32mlow   = 64kbps\x1b[0m   体积小，音质较差");
  console.log("  \x1b[33mmedium = 128kbps\x1b[0m  平衡（默认）");
  console.log("  \x1b[35mhigh  = 192kbps\x1b[0m  体积大，音质好\n");

  const level = await prompt("  选择级别 [low/medium/high，直接回车默认 medium]: ") || "medium";
  const input = await prompt("  📂 输入文件: ");
  if (!input.trim()) return;

  const output = await prompt("  💾 输出文件 (直接回车自动命名): ");

  console.log("");
  const args = ["compress", input.trim()];
  if (output.trim()) args.push("--output", output.trim());
  args.push("--quality", level.trim());
  await runFF(args);
  await prompt("\n  按回车继续...");
}

async function cmdInfo() {
  clear();
  console.log("\n  \x1b[1m\x1b[36m── 查看音频信息 ──\x1b[0m\n");

  const input = await prompt("  📂 输入音频文件: ");
  if (!input.trim()) return;

  console.log("");
  await runFF(["info", input.trim()]);
  await prompt("\n  按回车继续...");
}

async function cmdTranscribe() {
  clear();
  console.log("\n  \x1b[1m\x1b[36m── 音频转文字 (Whisper AI) ──\x1b[0m\n");
  console.log("  \x1b[90m模型: tiny(最快) / base / small(默认) / medium / large(最慢)\x1b[0m");
  console.log("  \x1b[90m语言: zh(中文) / en(英文) / ja(日文) / auto(自动检测)\x1b[0m");
  console.log("  \x1b[90m格式: txt/srt/vtt/json | 语言: zh/en/auto | 设备: auto/cpu/cuda\x1b[0m\n");

  const input = await prompt("  🎤 请输入音频文件路径: ");
  if (!input.trim()) return;

  const model = await prompt("  🤖 选择模型 (直接回车默认 small): ") || "small";
  const language = await prompt("  🌐 选择语言 (直接回车默认 auto): ") || "auto";
  const format = await prompt("  📝 输出格式 txt/srt/vtt/json (直接回车默认 txt): ") || "txt";

  console.log("\n  开始转录...\n");
  return new Promise((resolve) => {
    const { spawn } = require("child_process");
    const child = spawn("python", [
      "-u",
      path.join(__dirname, "transcribe.py"),
      input.trim(),
      "-m", model.trim(),
      "-l", language.trim(),
      "-f", format.trim(),
    ], { stdio: "inherit" });

    child.on("close", async (code) => {
      if (code === 0) {
        console.log("\n  \x1b[32m✅ 转录完成!\x1b[0m");
      } else {
        console.log("\n  \x1b[31m❌ 转录失败!\x1b[0m");
      }
      await prompt("  按回车继续...");
      resolve();
    });
  });
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

menu().catch((err) => {
  console.error("\n  \x1b[31m错误:\x1b[0m", err.message);
  process.exit(1);
});
