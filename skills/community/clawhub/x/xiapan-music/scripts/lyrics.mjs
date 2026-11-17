#!/usr/bin/env node
// 虾盘云音乐 · 写歌词（文本模型，成本≈0；不提交任何付费任务）
//
// 用法：
//   node scripts/lyrics.mjs --theme "写给毕业那天的歌" [--style "民谣"] [--language zh] [--out card.json]
// 输出：制作卡 JSON/文本（title/tags/lyrics + 成本与下一步）。拿到歌词后：
//   node scripts/song.mjs --lyrics-json card.json --confirm    # 用户确认后提交（约 ¥2.4/次，出 2 首）
//
// 退出码：0 成功 / 1 远端失败 / 2 用法或 Key 问题。

import { COST_HINT, buildNextSteps, resolveKey, writeLyrics } from "./lib/xiapan-music.mjs";
import {
  bool,
  emit,
  exitCodeForError,
  failWith,
  formatCard,
  formatNextSteps,
  makeLogger,
  parseArgs,
  printHelp,
  resolveSource,
  str,
  writeJson,
} from "./lib/cli.mjs";

const USAGE = `虾盘云音乐 · 写歌词（免费，仅文本模型）

用法：
  node scripts/lyrics.mjs --theme "写给毕业那天的歌，温暖民谣" [选项]

选项：
  --theme/--prompt <str>  主题/需求（必填）
  --style <str>           想要的风格（可中文，如「民谣」「city pop」）
  --language <zh|en|ja>   歌词语言（默认 zh）
  --title <str>           指定歌名（可选，模型会给一个）
  --out <file>            把制作卡 JSON 写进文件（供 song.mjs --lyrics-json 使用）
  --key <sk-...>          虾盘云 Key（也可 XIAPAN_API_KEY / device.json）
  --json                  机器可读输出
  --source <name>         UTM 来源（默认 cli）
  -h, --help              显示帮助

退出码：0 成功；1 远端失败；2 用法或 Key 问题。
提示：歌词免费；确认歌词后出歌约 ¥2.4/次（一次 2 首）。`;

async function main() {
  const { flags } = parseArgs(process.argv.slice(2));
  if (bool(flags, "help")) { printHelp(USAGE); return; }
  const log = makeLogger(flags);
  const source = resolveSource(flags);
  const theme = str(flags, "theme") || str(flags, "prompt");
  if (!theme) {
    const err = new Error("缺少 --theme（想写什么歌的主题/需求）");
    err.code = "BAD_REQUEST";
    throw err;
  }
  const key = resolveKey({ key: str(flags, "key") || undefined });
  log("正在写歌词（文本模型，成本≈0）…");
  const written = await writeLyrics(
    {
      theme,
      style: str(flags, "style") || str(flags, "tags"),
      language: str(flags, "language") || "zh",
      title: str(flags, "title"),
    },
    key,
  );
  const card = {
    title: str(flags, "title") || written.title,
    tags: written.tags,
    lyrics: written.lyrics,
    model: "Suno v6（出歌时使用）",
    costHint: COST_HINT.song,
  };
  const nextSteps = buildNextSteps({ source, key });
  const outFile = str(flags, "out");
  if (outFile) {
    writeJson(outFile, { ok: true, ...card, costHint: COST_HINT.song, savedAt: new Date().toISOString() });
    log(`制作卡已写入：${outFile}`);
  }
  const payload = {
    ok: true,
    ...card,
    lyricsCostHint: COST_HINT.lyrics,
    nextSteps,
    nextAction: "把制作卡给用户确认；确认后运行 song.mjs --lyrics-json <卡文件> --confirm 提交（约 ¥2.4/次，出 2 首）",
  };
  const human = [
    formatCard(card),
    "",
    "（歌词已生成，未提交、未扣费。确认后：song.mjs --lyrics-json <卡文件> --confirm）",
    ...formatNextSteps(nextSteps),
  ];
  emit(flags, payload, human);
}

main().catch((err) => failWith(parseArgs(process.argv.slice(2)).flags, err, exitCodeForError(err)));
