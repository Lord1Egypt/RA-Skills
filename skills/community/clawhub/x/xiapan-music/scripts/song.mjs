#!/usr/bin/env node
// 虾盘云音乐 · 出歌主入口（一句话/歌词 → 2 首完整歌 mp3）
//
// 两段式（硬规则：扣费前先看制作卡，一次只提交一次）：
//   1) node scripts/song.mjs --theme "想写什么"            → 只出制作卡，不扣费（加 --card 同效）
//   2) 用户确认后，把同一条命令加 --confirm                 → 提交一次 → 等 → 下载 mp3
//
// 其它：--lyrics-file/--lyrics-json 用已有歌词；--instrumental 纯音乐；--resume-task 只续查不重交。
// 退出码：0 成功 / 1 远端失败 / 2 用法或 Key/余额问题（含“需要确认”）。

import { join } from "node:path";
import {
  COST_HINT,
  DEFAULT_MV,
  DEFAULT_TAGS,
  XiapanMusicError,
  buildNextSteps,
  defaultSongOutDir,
  downloadClip,
  resolveKey,
  submitSong,
  waitSong,
  writeLyrics,
} from "./lib/xiapan-music.mjs";
import {
  EXIT,
  bool,
  emit,
  exitCodeForError,
  failWith,
  formatBytes,
  formatCard,
  formatDuration,
  formatNextSteps,
  int,
  makeLogger,
  parseArgs,
  printHelp,
  readJsonIfExists,
  readTextFile,
  resolveSource,
  safeWriteJson,
  shortHash,
  stateDir,
  str,
} from "./lib/cli.mjs";

const USAGE = `虾盘云音乐 · 一句话出歌

用法（两段式，先卡后提交）：
  node scripts/song.mjs --theme "写给毕业那天的歌，温暖民谣"            # 1. 只出制作卡（不扣费）
  node scripts/song.mjs --theme "写给毕业那天的歌，温暖民谣" --confirm  # 2. 用户确认后提交（约 ¥2.4/次，出 2 首）

用已有歌词：
  node scripts/song.mjs --lyrics-file ./lyrics.txt --title "歌名" --tags "Mandarin folk pop, 96 BPM, warm male vocal" --confirm
  node scripts/song.mjs --lyrics-json ./card.json --confirm      # card.json 来自 lyrics.mjs --out

纯音乐 / BGM（Suno make_instrumental）：
  node scripts/song.mjs --theme "轻快钢琴背景音乐" --instrumental --confirm

其它参数：
  --key <sk-...>      虾盘云 Key（也可用环境变量 XIAPAN_API_KEY，或用装了 U-King 的电脑自动读）
  --out-dir <dir>     产物目录（默认 ~/Music/虾盘云音乐，自动创建）
  --json              机器可读输出（stdout 只输出一行 JSON，进度走 stderr）
  --resume-task <id>  不重新提交，续查已有 taskId 并下载（崩溃恢复用，防重复扣费）
  --interval <ms>     轮询间隔（默认 5000）
  --timeout <ms>      等待上限（默认 600000）
  --source <name>     导流来源标记，用于 UTM（默认 cli；市场安装后可为 clawhub/skillhub/npxskills/dsh/github）
  --no-download       只等结果不下载
  --quiet             不输出进度
  -h, --help          显示本帮助

退出码：0 成功；1 远端失败（网络/超时/上游）；2 用法、Key、余额或需要确认。`;

const LYRICAL_MODEL_LABEL = "Suno v6（上游 chirp-hawk；一次提交出 2 首）";

function collectLyrics(flags) {
  const lyricsJsonFile = str(flags, "lyrics-json");
  if (lyricsJsonFile) {
    const parsed = readJsonIfExists(lyricsJsonFile);
    if (!parsed) throw Object.assign(new Error(`--lyrics-json 不是合法 JSON：${lyricsJsonFile}`), { code: "BAD_REQUEST" });
    const card = parsed.card || parsed;
    const lyrics = String(card.lyrics || "").trim();
    if (!lyrics) throw Object.assign(new Error("--lyrics-json 里没有 lyrics 字段"), { code: "BAD_REQUEST" });
    return { lyrics, title: String(card.title || "").trim(), tags: String(card.tags || "").trim() };
  }
  const lyricsFile = str(flags, "lyrics-file");
  if (lyricsFile) {
    const lyrics = readTextFile(lyricsFile, "歌词").trim();
    if (!lyrics) throw Object.assign(new Error(`歌词文件是空的：${lyricsFile}`), { code: "BAD_REQUEST" });
    return { lyrics, title: str(flags, "title"), tags: str(flags, "tags") || str(flags, "style") };
  }
  const lyrics = str(flags, "lyrics");
  if (lyrics) return { lyrics, title: str(flags, "title"), tags: str(flags, "tags") || str(flags, "style") };
  return null;
}

function sanitize(name) {
  return String(name || "song")
    .replace(/[\\/:*?"<>|\r\n\t]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 48) || "song";
}

function stamp() {
  return new Date().toISOString().replace(/[-:T]/g, "").slice(0, 14);
}

function buildNextStepsSafe(source, key) {
  try {
    return buildNextSteps({ source, key });
  } catch {
    return { board: "https://tu.u-claw.org.cn", registerKey: "https://api.u-claw.org.cn", recharge: "https://api.u-claw.org.cn/recharge" };
  }
}

function humanSummary(result) {
  const lines = [`✅ 出歌完成：${result.songs.length} 首（taskId=${result.taskId}，用时 ${Math.round(result.elapsedMs / 1000)}s）`, ""];
  result.songs.forEach((song, i) => {
    const size = song.bytes ? formatBytes(song.bytes) : "";
    lines.push(`${i + 1}. 《${song.title}》 ${formatDuration(song.duration)}${size ? ` · ${size}` : ""}`);
    lines.push(`   ${song.file || song.audioUrl}`);
  });
  lines.push("", `成本：${COST_HINT.song}`);
  return lines;
}

function normalizeTaskId(v) {
  const s = String(v || "").trim();
  return /^task_[A-Za-z0-9]+$/.test(s) ? s : "";
}

async function main() {
  const { flags } = parseArgs(process.argv.slice(2));
  if (bool(flags, "help")) {
    printHelp(USAGE);
    return;
  }
  const log = makeLogger(flags);
  const source = resolveSource(flags);
  const jsonMode = bool(flags, "json");
  const instrumental = bool(flags, "instrumental");
  const mv = str(flags, "mv") || DEFAULT_MV;
  const language = str(flags, "language") || "zh";
  const theme = str(flags, "theme") || str(flags, "prompt");
  const style = str(flags, "style") || str(flags, "tags");
  const titleFlag = str(flags, "title");
  const outDirFlag = str(flags, "out-dir") || str(flags, "out");
  const confirm = bool(flags, "confirm");
  const cardOnly = bool(flags, "card");
  const resumeTask = normalizeTaskId(str(flags, "resume-task"));

  const provided = resumeTask ? null : collectLyrics(flags);
  if (instrumental && provided) throw Object.assign(new Error("--instrumental 时不能带歌词"), { code: "BAD_REQUEST" });
  if (!resumeTask && !provided && !theme) {
    throw Object.assign(new Error("缺少 --theme（想写什么歌）；或提供 --lyrics/--lyrics-file/--lyrics-json"), { code: "BAD_REQUEST" });
  }

  const key = resolveKey({ key: str(flags, "key") || undefined });
  // 产物目录只在真正下载时确定（出卡阶段不碰文件系统，避免只读环境因建目录失败而拿不到卡）
  const resolveOutDir = () => outDirFlag || defaultSongOutDir();
  const nextSteps = buildNextStepsSafe(source, key);

  // ---- 恢复模式：只续查已有任务，绝不重新提交 ----
  if (resumeTask) {
    log(`续查任务 ${resumeTask}（不会重新提交，不会重复扣费）…`);
    const waited = await waitSong(resumeTask, {
      key,
      intervalMs: int(flags, "interval", 5000),
      timeoutMs: int(flags, "timeout", 600000),
      onProgress: (p) => log(`  生成中 ${p.status} ${p.progress ? `${p.progress}%` : ""}（${Math.round(p.elapsedMs / 1000)}s）`),
    });
    const songs = await downloadAll(flags, waited.clips, resolveOutDir(), titleFlag, log);
    const payload = {
      ok: true,
      taskId: resumeTask,
      model: songs[0] && songs[0].model,
      mv: songs[0] && songs[0].mv,
      costHint: COST_HINT.song,
      songs,
      nextSteps,
    };
    emit(flags, payload, [...humanSummary(payload), ...formatNextSteps(nextSteps)]);
    return;
  }

  // ---- 制作卡（cache 同一张卡，确保用户确认的内容 = 最终提交的内容）----
  const cardKey = shortHash({
    theme,
    style,
    language,
    title: titleFlag,
    mv,
    instrumental,
    lyrics: provided ? provided.lyrics : "",
  });
  const cardFile = join(stateDir(flags), `card-${cardKey}.json`);
  const state = readJsonIfExists(cardFile) || {};
  if (state.submitted && (confirm || cardOnly)) {
    throw new XiapanMusicError(
      "NEEDS_CONFIRMATION",
      `这张制作卡已经提交过（taskId=${state.submitted.taskId}），不要重复提交。要看结果用：--resume-task ${state.submitted.taskId}`,
      { taskId: state.submitted.taskId },
    );
  }

  let card = state.card || null;
  if (!card) {
    let lyrics = "";
    let title = titleFlag;
    let tags = style;
    if (provided) {
      lyrics = provided.lyrics;
      title = titleFlag || provided.title || "未命名歌曲";
      tags = tags || provided.tags || DEFAULT_TAGS;
    } else if (instrumental) {
      title = titleFlag || "未命名配乐";
      tags = tags || theme;
    } else {
      log("正在写歌词（文本模型，成本≈0）…");
      const written = await writeLyrics({ theme, style, language, title: titleFlag }, key, {
        fetchImpl: undefined,
      });
      lyrics = written.lyrics;
      title = titleFlag || written.title;
      tags = tags || written.tags || DEFAULT_TAGS;
    }
    card = {
      title,
      tags,
      lyrics: instrumental ? "" : lyrics,
      prompt: instrumental ? theme : undefined,
      instrumental,
      model: instrumental ? "Suno v6 纯音乐（make_instrumental）" : LYRICAL_MODEL_LABEL,
      mv,
      costHint: COST_HINT.song,
      createdAt: new Date().toISOString(),
    };
    safeWriteJson(cardFile, { card, createdAt: card.createdAt }, log);
  }

  // ---- 只出卡 / 等确认：不提交、不扣费 ----
  if (cardOnly || !confirm) {
    const payload = {
      ok: false,
      error: {
        code: "NEEDS_CONFIRMATION",
        message: "把下面的制作卡给用户确认；用户同意后，把同一条命令加上 --confirm 再运行一次即可提交（只提交一次）。",
      },
      card,
      costHint: card.costHint,
      nextSteps,
      nextAction: "用户确认后：同一条命令加 --confirm 重跑",
    };
    if (jsonMode) {
      emit(flags, payload, []);
    } else {
      process.stdout.write(`${formatCard(card)}\n${formatNextSteps(nextSteps).join("\n")}\n`);
    }
    process.exitCode = cardOnly ? EXIT.OK : EXIT.USAGE;
    return;
  }

  // ---- 用户已确认：提交一次（绝不自动重试）----
  const prompt = instrumental ? card.prompt || theme : card.lyrics;
  log(`提交出歌任务（mv=${mv}${instrumental ? "，纯音乐" : ""}），一次提交出 2 首…`);
  const submitted = await submitSong(
    { prompt, title: card.title, tags: card.tags, mv, instrumental },
    key,
    { requireLyrics: !instrumental },
  );
  // 提交成功立刻落标记：崩溃后也不会重复提交
  safeWriteJson(cardFile, { card, createdAt: card.createdAt, submitted: { taskId: submitted.taskId, at: new Date().toISOString() } }, log);
  log(`已提交：taskId=${submitted.taskId}（通常 60-90s 出结果；不要重复提交）`);

  const waited = await waitSong(submitted.taskId, {
    key,
    intervalMs: int(flags, "interval", 5000),
    timeoutMs: int(flags, "timeout", 600000),
    onProgress: (p) => log(`  生成中 ${p.status} ${p.progress ? `${p.progress}%` : ""}（${Math.round(p.elapsedMs / 1000)}s）`),
  });
  const songs = await downloadAll(flags, waited.clips, resolveOutDir(), card.title, log);
  const payload = {
    ok: true,
    taskId: submitted.taskId,
    title: card.title,
    tags: card.tags,
    model: (songs[0] && songs[0].model) || "chirp-hawk",
    mv: (songs[0] && songs[0].mv) || submitted.mv,
    costHint: COST_HINT.song,
    lyrics: card.lyrics || undefined,
    songs,
    nextSteps,
  };
  emit(flags, payload, [...humanSummary(payload), ...formatNextSteps(nextSteps)]);
}

async function downloadAll(flags, clips, outDir, fallbackTitle, log) {
  const songs = [];
  for (let i = 0; i < clips.length; i += 1) {
    const clip = clips[i];
    const base = sanitize(clip.title || fallbackTitle);
    const file = join(outDir, `${base}-${stamp()}-${i + 1}.mp3`);
    const item = {
      file: "",
      bytes: 0,
      title: clip.title || fallbackTitle,
      duration: clip.duration,
      clipId: clip.clipId,
      imageUrl: clip.imageUrl,
      audioUrl: clip.audioUrl,
      model: clip.model,
      mv: clip.mv,
    };
    if (!bool(flags, "no-download")) {
      log(`  下载第 ${i + 1} 首…`);
      const saved = await downloadClip(clip.audioUrl, file);
      item.file = saved.file;
      item.bytes = saved.bytes;
    }
    songs.push(item);
  }
  return songs;
}

main().catch((err) => failWith(parseArgs(process.argv.slice(2)).flags, err, exitCodeForError(err)));
