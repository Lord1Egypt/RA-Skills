#!/usr/bin/env node
// 虾盘云音乐 · 查余额（不扣费）
//
// 用法：node scripts/balance.mjs [--json] [--key sk-...]
// 退出码：0 成功 / 1 远端失败 / 2 用法或 Key 问题。

import { COST_HINT, buildNextSteps, queryBalance, resolveKey } from "./lib/xiapan-music.mjs";
import {
  bool,
  emit,
  exitCodeForError,
  failWith,
  formatNextSteps,
  makeLogger,
  parseArgs,
  printHelp,
  resolveSource,
  str,
} from "./lib/cli.mjs";

const USAGE = `虾盘云音乐 · 查余额（不扣费）

用法：node scripts/balance.mjs [选项]

选项：
  --key <sk-...>    虾盘云 Key（也可 XIAPAN_API_KEY / device.json）
  --json            机器可读输出
  --source <name>   UTM 来源（默认 cli）
  --quiet           不输出进度
  -h, --help        显示帮助

退出码：0 成功；1 远端失败；2 用法或 Key 问题。`;

async function main() {
  const { flags } = parseArgs(process.argv.slice(2));
  if (bool(flags, "help")) { printHelp(USAGE); return; }
  const log = makeLogger(flags);
  const source = resolveSource(flags);
  const key = resolveKey({ key: str(flags, "key") || undefined });
  log("查询余额…");
  const balance = await queryBalance(key);
  const nextSteps = buildNextSteps({ source, key });
  const payload = {
    ok: true,
    remainCny: balance.remainCny,
    remainToken: balance.remainToken,
    totalToken: balance.totalToken,
    usedToken: balance.usedToken,
    costHints: { song: COST_HINT.song, bgm: COST_HINT.bgm },
    nextSteps,
  };
  const human = [
    `💰 余额：约 ¥${balance.remainCny}（剩余 ${balance.remainToken} token；已用 ${balance.usedToken} / ${balance.totalToken}）`,
    `出歌一次约 ¥2.4（2 首）、BGM 约 ¥1/首；余额不足就去充值。`,
    ...formatNextSteps(nextSteps),
  ];
  emit(flags, payload, human);
}

main().catch((err) => failWith(parseArgs(process.argv.slice(2)).flags, err, exitCodeForError(err)));
