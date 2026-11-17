// 虾盘云音乐 skill · CLI 公共小工具（零依赖）
// 只做参数解析 / 输出约定 / 制作卡文案 / 退出码映射，不直接发 HTTP。

import { createHash } from "node:crypto";
import { mkdirSync, readFileSync, writeFileSync, existsSync, rmSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { join } from "node:path";

/** 退出码约定：0 = 成功；1 = 远端执行失败（网络/超时/上游）；2 = 用法/Key/余额/需要确认 */
export const EXIT = { OK: 0, RUNTIME: 1, USAGE: 2 };

/** 把 XiapanMusicError.code 映射成退出码 */
export function exitCodeForError(err) {
  const code = err && err.code;
  if (code === "BAD_KEY" || code === "BAD_REQUEST" || code === "NO_BALANCE" || code === "NEEDS_CONFIRMATION") return EXIT.USAGE;
  return EXIT.RUNTIME;
}

const BOOLEAN_FLAGS = new Set([
  "json", "quiet", "help", "confirm", "card", "instrumental", "version",
  "dry-run", "no-download", "with-key-link",
]);

/**
 * 解析 argv：支持 `--flag value`、`--flag=value`、布尔 flag、`-h`。
 * @param {string[]} argv
 * @returns {{flags: Record<string, string|true>, help: boolean}}
 */
export function parseArgs(argv) {
  const flags = {};
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "-h") {
      flags.help = true;
      continue;
    }
    if (!arg.startsWith("--")) continue;
    let key = arg.slice(2);
    let value = true;
    const eq = key.indexOf("=");
    if (eq >= 0) {
      value = key.slice(eq + 1);
      key = key.slice(0, eq);
    } else if (!BOOLEAN_FLAGS.has(key) && i + 1 < argv.length && !argv[i + 1].startsWith("--")) {
      value = argv[++i];
    }
    flags[key] = value;
  }
  return { flags };
}

export function str(flags, name) {
  const v = flags[name];
  return typeof v === "string" ? v.trim() : "";
}

export function bool(flags, name) {
  return flags[name] === true || flags[name] === "true";
}

export function int(flags, name, fallback) {
  const v = Number.parseInt(str(flags, name), 10);
  return Number.isFinite(v) ? v : fallback;
}

/** 统一日志（进度走 stderr，永远不打印 Key） */
export function makeLogger(flags) {
  const quiet = bool(flags, "quiet") || bool(flags, "json");
  return (msg) => {
    if (!quiet) process.stderr.write(`${msg}\n`);
  };
}

/**
 * 状态来源（UTM source）：--source > env XIAPAN_SOURCE > env XIAPAN_UTM_SOURCE > cli。
 * 返回空串时由 core.buildNextSteps 按 env/默认值兜底（DSH 插件注入 XIAPAN_UTM_SOURCE=dsh）。
 */
export function resolveSource(flags) {
  return str(flags, "source") || process.env.XIAPAN_SOURCE || process.env.XIAPAN_UTM_SOURCE || "";
}

/** 统一的成功/失败输出 */
export function emit(flags, payload, humanLines) {
  if (bool(flags, "json")) {
    process.stdout.write(`${JSON.stringify(payload)}\n`);
    return;
  }
  const lines = Array.isArray(humanLines) ? humanLines : [];
  process.stdout.write(`${lines.join("\n")}\n`);
}

export function failWith(flags, err, exitCode) {
  const code = err && err.code ? err.code : "UNKNOWN";
  const message = (err && err.message) || String(err);
  const details = (err && err.details) || {};
  const payload = { ok: false, error: { code, message, ...details } };
  if (bool(flags, "json")) {
    process.stdout.write(`${JSON.stringify(payload)}\n`);
  } else {
    process.stderr.write(`❌ ${message}\n`);
  }
  // 用 exitCode 而不是 process.exit：Windows 上 process.exit 会与 undici 收尾竞态，
  // 偶发 "Assertion failed: !(handle->flags & UV_HANDLE_CLOSING)"（libuv async.c）。
  process.exitCode = exitCode == null ? EXIT.RUNTIME : exitCode;
}

/** 读文件文本（用于 --lyrics-file / --lyrics-json） */
export function readTextFile(file, label) {
  if (!existsSync(file)) {
    const err = new Error(`${label} 文件不存在：${file}`);
    err.code = "BAD_REQUEST";
    throw err;
  }
  return readFileSync(file, "utf8");
}

/** 生成短 hash（用于制作卡缓存键；不含 Key） */
export function shortHash(obj) {
  return createHash("sha1").update(JSON.stringify(obj)).digest("hex").slice(0, 16);
}

/**
 * 制作卡状态目录：--state-dir > env XIAPAN_STATE_DIR > ~/.cache/xiapan-music > 系统临时目录 > 当前目录。
 * 逐级 fallback，保证只读/受限环境也能生成制作卡（缓存只是防重复提交的保险，不是硬依赖）。
 */
export function stateDir(flags) {
  const candidates = [
    str(flags, "state-dir"),
    process.env.XIAPAN_STATE_DIR,
    join(homedir(), ".cache", "xiapan-music"),
    join(tmpdir(), "xiapan-music"),
    join(process.cwd(), ".xiapan-cache"),
  ].filter(Boolean);
  for (const dir of candidates) {
    try {
      mkdirSync(dir, { recursive: true });
      return dir;
    } catch {
      // 换下一级
    }
  }
  return candidates[candidates.length - 1];
}

/** 写 JSON（失败不致命：制作卡缓存写不了时仍可继续，但会提示） */
export function safeWriteJson(file, obj, log) {
  try {
    writeJson(file, obj);
    return true;
  } catch (err) {
    if (typeof log === "function") log(`⚠️ 无法写入制作卡缓存（${(err && err.message) || err}），本次仍可继续，但请勿重复提交`);
    return false;
  }
}

export function readJsonIfExists(file) {
  try {
    return JSON.parse(readFileSync(file, "utf8"));
  } catch {
    return null;
  }
}

export function writeJson(file, obj) {
  writeFileSync(file, `${JSON.stringify(obj, null, 2)}\n`, "utf8");
}

export function removeFile(file) {
  try {
    rmSync(file, { force: true });
  } catch {
    // 忽略清理失败
  }
}

/** 数字时长 → mm:ss */
export function formatDuration(seconds) {
  const s = Math.round(Number(seconds) || 0);
  const m = Math.floor(s / 60);
  const r = s % 60;
  return `${m}:${String(r).padStart(2, "0")}`;
}

export function formatBytes(bytes) {
  const n = Number(bytes) || 0;
  if (n >= 1024 * 1024) return `${(n / (1024 * 1024)).toFixed(1)} MB`;
  if (n >= 1024) return `${(n / 1024).toFixed(0)} KB`;
  return `${n} B`;
}

/**
 * 制作卡（扣费前必须给用户看的内容）。歌词全文一定放进去。
 * @param {{title:string, tags:string, lyrics?:string, model:string, mv?:string, costHint:string, instrumental?:boolean}} card
 */
export function formatCard(card) {
  const lines = [
    "┌─ 制作卡（确认后才会提交、只提交一次）─────────────",
    `│ 歌名：${card.title || "（待定）"}`,
    `│ 风格：${card.tags || "（未指定，将用默认流行风格）"}`,
    `│ 模型：${card.model}${card.mv ? `（mv=${card.mv}）` : ""}`,
  ];
  if (card.instrumental) {
    lines.push("│ 类型：纯音乐 / 无人声");
  } else {
    lines.push("│ 类型：完整歌曲（一次出 2 首，约 2 分钟/首）");
  }
  lines.push(`│ 成本：${card.costHint}`);
  lines.push("└────────────────────────────────────────────");
  if (card.lyrics) {
    lines.push("", "歌词：", card.lyrics);
  }
  lines.push("", "确认无误后加 --confirm 再运行同一条命令即可提交（不加则只出卡、不扣费）。");
  return lines.join("\n");
}

/** CTA 文案（带 UTM） */
export function formatNextSteps(nextSteps) {
  if (!nextSteps) return [];
  return [
    "",
    "下一步：",
    `  · 去虾盘云画板做 MV / 继续创作：${nextSteps.board}`,
    `  · 没有 Key / 想再领一把：${nextSteps.registerKey}`,
    `  · 充值：${nextSteps.recharge}`,
  ];
}

/** 标准 --help 输出（不调用 process.exit，调用方写完直接 return，让进程自然退出） */
export function printHelp(usage, details) {
  const lines = [usage, "", details || "", ""];
  process.stdout.write(`${lines.join("\n")}\n`);
  process.exitCode = EXIT.OK;
}
