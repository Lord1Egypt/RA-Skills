#!/usr/bin/env node
// 虾盘云音乐 · 纯音乐 / BGM（MiniMax music，约 ¥1/首）
//
// 两段式（扣费前先看制作卡）：
//   node scripts/bgm.mjs --prompt "轻快温馨的钢琴背景音乐，适合短视频结尾"            → 只出卡，不扣费
//   node scripts/bgm.mjs --prompt "同上" --confirm                                  → 提交并下载 mp3
//
// 退出码：0 成功 / 1 远端失败 / 2 用法、Key、余额或需要确认。

import { join } from "node:path";
import { COST_HINT, DEFAULT_BGM_MODEL, buildNextSteps, defaultSongOutDir, generateBgm, resolveKey } from "./lib/xiapan-music.mjs";
import {
  EXIT,
  bool,
  emit,
  exitCodeForError,
  failWith,
  formatBytes,
  formatNextSteps,
  int,
  makeLogger,
  parseArgs,
  printHelp,
  resolveSource,
  str,
} from "./lib/cli.mjs";

const USAGE = `虾盘云音乐 · 纯音乐 / BGM

用法（两段式，先卡后提交）：
  node scripts/bgm.mjs --prompt "轻快温馨的钢琴背景音乐，适合短视频结尾"           # 1. 出制作卡（不扣费）
  node scripts/bgm.mjs --prompt "同上" --confirm                                 # 2. 确认后提交（约 ¥1/首）

选项：
  --prompt <str>    音乐风格/情绪/场景描述（必填）
  --model <id>      默认 minimax-music-v2.6
  --out <file>      输出 mp3 路径（默认 ~/Music/虾盘云音乐/bgm-<时间戳>.mp3）
  --out-dir <dir>   输出目录（--out 未指定时生效）
  --key <sk-...>    虾盘云 Key（也可 XIAPAN_API_KEY / device.json）
  --json            机器可读输出
  --source <name>   UTM 来源（默认 cli）
  --interval <ms>   轮询间隔（默认 5000）
  --timeout <ms>    等待上限（默认 600000）
  --quiet           不输出进度
  -h, --help        显示帮助

退出码：0 成功；1 远端失败；2 用法、Key、余额或需要确认。`;

function buildCard(prompt, model) {
  return {
    title: "纯音乐 / BGM",
    tags: prompt,
    instrumental: true,
    model,
    costHint: COST_HINT.bgm,
  };
}

function humanCard(card) {
  return [
    "┌─ 制作卡（确认后才会提交、只提交一次）─────────────",
    `│ 类型：纯音乐 / BGM（无人声）`,
    `│ 风格描述：${card.tags}`,
    `│ 模型：${card.model}`,
    `│ 成本：${card.costHint}`,
    "└────────────────────────────────────────────",
    "",
    "确认无误后加 --confirm 再运行同一条命令即可提交（不加则只出卡、不扣费）。",
  ].join("\n");
}

async function main() {
  const { flags } = parseArgs(process.argv.slice(2));
  if (bool(flags, "help")) { printHelp(USAGE); return; }
  const log = makeLogger(flags);
  const source = resolveSource(flags);
  const prompt = str(flags, "prompt") || str(flags, "theme");
  if (!prompt) {
    const err = new Error("缺少 --prompt（音乐风格/情绪/场景描述）");
    err.code = "BAD_REQUEST";
    throw err;
  }
  const model = str(flags, "model") || DEFAULT_BGM_MODEL;
  const card = buildCard(prompt, model);
  const key = resolveKey({ key: str(flags, "key") || undefined });
  const nextSteps = buildNextSteps({ source, key });

  const confirm = bool(flags, "confirm");
  const cardOnly = bool(flags, "card");
  if (cardOnly || !confirm) {
    const payload = {
      ok: false,
      error: {
        code: "NEEDS_CONFIRMATION",
        message: "把制作卡给用户确认；用户同意后，同一条命令加 --confirm 再运行一次即可提交（只提交一次）。",
      },
      card,
      costHint: card.costHint,
      nextSteps,
      nextAction: "用户确认后：同一条命令加 --confirm 重跑",
    };
    if (bool(flags, "json")) emit(flags, payload, []);
    else process.stdout.write(`${humanCard(card)}\n${formatNextSteps(nextSteps).join("\n")}\n`);
    process.exitCode = cardOnly ? EXIT.OK : EXIT.USAGE;
    return;
  }

  const outFile = str(flags, "out")
    || join(str(flags, "out-dir") || defaultSongOutDir(), `bgm-${new Date().toISOString().replace(/[-:T]/g, "").slice(0, 14)}.mp3`);
  log(`提交 BGM 任务（模型 ${model}）…`);
  const result = await generateBgm(
    {
      prompt,
      model,
      outFile,
      source,
      onProgress: (p) => log(`  生成中 ${p.status || "…"}（${Math.round(p.elapsedMs / 1000)}s）`),
    },
    key,
    { intervalMs: int(flags, "interval", 5000), timeoutMs: int(flags, "timeout", 600000) },
  );
  const payload = {
    ok: true,
    taskId: result.taskId,
    model: result.model,
    file: result.file,
    bytes: result.bytes,
    elapsedMs: result.elapsedMs,
    costHint: result.costHint,
    nextSteps: result.nextSteps,
  };
  const human = [
    `✅ 纯音乐已生成（taskId=${result.taskId}，用时 ${Math.round(result.elapsedMs / 1000)}s，${formatBytes(result.bytes)}）`,
    `   ${result.file}`,
    "",
    `成本：${result.costHint}`,
    ...formatNextSteps(result.nextSteps),
  ];
  emit(flags, payload, human);
}

main().catch((err) => failWith(parseArgs(process.argv.slice(2)).flags, err, exitCodeForError(err)));
