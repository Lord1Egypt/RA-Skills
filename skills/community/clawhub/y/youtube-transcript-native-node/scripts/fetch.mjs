#!/usr/bin/env node
// youtube-transcript-native-node/scripts/fetch.mjs
// Fetch a YouTube transcript via yt-dlp — native Node.js, zero npm dependencies.
// Usage: node fetch.mjs --url <youtube-url> [--lang en] [--timestamps] [--json]
// Requires Node 18+ and the yt-dlp binary on PATH.

// Audit note: this intentionally invokes the trusted yt-dlp binary from PATH
// with an argv array and no shell, after allowlisting YouTube URL hosts.
import { spawn } from "node:child_process";
import { mkdtempSync, readdirSync, readFileSync, rmSync } from "node:fs";
import { homedir, tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const TEST_HOOKS = process.env.YOUTUBE_TRANSCRIPT_SELFTEST === "1";
const YTDLP_TIMEOUT_MS = TEST_HOOKS && process.env.YOUTUBE_TRANSCRIPT_TEST_TIMEOUT_MS
  ? Number(process.env.YOUTUBE_TRANSCRIPT_TEST_TIMEOUT_MS)
  : 120_000;
const MAX_TRANSCRIPT_CHARS = TEST_HOOKS && process.env.YOUTUBE_TRANSCRIPT_TEST_MAX_CHARS
  ? Number(process.env.YOUTUBE_TRANSCRIPT_TEST_MAX_CHARS)
  : 2_000_000;

function enforceTranscriptSize(text) {
  if (text.length > MAX_TRANSCRIPT_CHARS) {
    die(`transcript exceeds max output size (${text.length} chars > ${MAX_TRANSCRIPT_CHARS}). Use a shorter video or add a smaller extraction workflow.`);
  }
  return text;
}

function die(msg, code = 1) {
  process.stderr.write(`error: ${msg}\n`);
  process.exit(code);
}

function escapeRegExp(s) {
  return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function scrubLocalPaths(text, tempDir = "") {
  let out = String(text || "");
  const replacements = [
    [tempDir, "<tmp>"],
    [tmpdir(), "<tmp>"],
    [homedir(), "<home>"],
  ];
  for (const [needle, replacement] of replacements) {
    if (!needle) continue;
    const trimmed = needle.replace(/[\\/]+$/, "");
    const slashFlexible = escapeRegExp(trimmed).replace(/(?:\\\\|\/)+/g, "[\\\\/]");
    out = out.replace(new RegExp(`(?:file:\\/\\/\\/?)?${slashFlexible}(?:[\\\\/][^\\s\"'<>]+)*`, "g"), replacement);
    out = out.split(needle).join(replacement);
  }
  return out;
}

function ytDlpErrorTail(stderr, tempDir = "") {
  const sanitizedStderr = scrubLocalPaths(stderr, tempDir);
  return sanitizedStderr.trim().split("\n").slice(-5).join("\n");
}

function rateLimitHint(stderr) {
  return /429|too many requests/i.test(stderr || "")
    ? " YouTube may be rate-limiting this IP; wait before retrying."
    : "";
}

function printHelp() {
  process.stdout.write(
    "Usage: fetch.mjs --url <youtube-url> [flags]\n" +
    "\n" +
    "Required:\n" +
    "  --url URL         YouTube video URL\n" +
    "\n" +
    "Optional:\n" +
    "  --lang CODE       subtitle language (default: en)\n" +
    "  --timestamps      keep [hh:mm:ss] prefixes in plain-text or JSON transcript output\n" +
    "  --json            output JSON with title + transcript + metadata\n" +
    "  --no-dedup        disable rolling-window dedup for auto-captions\n" +
    "  -h, --help        show this help\n" +
    "\n" +
    "Requires yt-dlp on PATH. Install/verify using the official yt-dlp project instructions.\n" +
    "Common package-manager examples:\n" +
    "  Windows:        winget install yt-dlp\n" +
    "  macOS:          brew install yt-dlp\n"
  );
}

// -------- arg parser --------

export function isAllowedYouTubeUrl(rawUrl) {
  let parsed;
  try {
    parsed = new URL(rawUrl);
  } catch {
    return false;
  }
  if (!/^https?:$/i.test(parsed.protocol)) return false;
  const host = parsed.hostname.toLowerCase();
  return ["youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"].includes(host);
}

export function parseArgs(argv) {
  const out = {
    url: "",
    lang: "en",
    timestamps: false,
    json: false,
    noDedup: false,
  };
  const stringFlags = new Set(["--url", "--lang"]);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--timestamps") { out.timestamps = true; continue; }
    if (a === "--json") { out.json = true; continue; }
    if (a === "--no-dedup") { out.noDedup = true; continue; }
    if (a === "-h" || a === "--help") { printHelp(); process.exit(0); }
    if (stringFlags.has(a)) {
      const v = argv[++i];
      if (v === undefined) die(`flag ${a} needs a value`);
      switch (a) {
        case "--url":  out.url  = v.trim(); break;
        case "--lang": out.lang = v.trim(); break;
      }
      continue;
    }
    die(`unknown arg: ${a}. Try --help.`);
  }
  if (!out.url) die("--url is required. Try --help.");
  if (!isAllowedYouTubeUrl(out.url)) die(`--url must be a YouTube URL on youtube.com or youtu.be, got: ${out.url}`);
  if (!out.lang) die("--lang must not be empty");
  if (!/^[A-Za-z0-9._-]{1,32}$/.test(out.lang)) die("--lang must be a simple subtitle language code, e.g. en or en-US");
  return out;
}

// -------- yt-dlp invocation --------

let activeYtDlpProc = null;

function runYtDlp(args, opts = {}) {
  return new Promise((resolve) => {
    let proc;
    let timer;
    let settled = false;
    let timedOut = false;
    const finish = (result) => {
      if (settled) return;
      settled = true;
      if (timer) clearTimeout(timer);
      if (activeYtDlpProc === proc) activeYtDlpProc = null;
      resolve(result);
    };
    try {
      const testScript = TEST_HOOKS ? (process.env.YOUTUBE_TRANSCRIPT_TEST_YTDLP_SCRIPT || "") : "";
      const command = testScript ? process.execPath : "yt-dlp";
      const spawnArgs = testScript ? [testScript, ...args] : args;
      proc = spawn(command, spawnArgs, { stdio: ["ignore", "pipe", "pipe"] });
      activeYtDlpProc = proc;
    } catch (e) {
      finish({ code: -1, stdout: "", stderr: String(e && e.message || e), spawnError: true, timedOut: false });
      return;
    }
    timer = setTimeout(() => {
      timedOut = true;
      try { proc.kill("SIGTERM"); } catch { /* best effort */ }
      setTimeout(() => { try { if (!settled) proc.kill("SIGKILL"); } catch { /* best effort */ } }, 1500).unref?.();
    }, opts.timeoutMs || YTDLP_TIMEOUT_MS);
    timer.unref?.();
    let stdout = "";
    let stderr = "";
    proc.stdout.on("data", (b) => { stdout += b.toString("utf8"); });
    proc.stderr.on("data", (b) => { stderr += b.toString("utf8"); });
    proc.on("error", (e) => {
      finish({ code: -1, stdout, stderr: stderr + String(e && e.message || e), spawnError: true, timedOut });
    });
    proc.on("close", (code) => {
      finish({ code: code == null ? -1 : code, stdout, stderr, spawnError: false, timedOut });
    });
  });
}

// -------- .vtt parser --------

// Strip an inline HTML/VTT tag set like <c>, </c>, <c.colorE5E5E5>, <00:00:01.000>
function stripInlineTags(s) {
  return s.replace(/<[^>]+>/g, "");
}

// Decode the small set of HTML entities that show up in YouTube captions.
function decodeEntities(s) {
  return s
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, "\"")
    .replace(/&#39;/g, "'")
    .replace(/&nbsp;/g, " ");
}

const TIMING_RE = /^((?:\d{2}:)?\d{2}:\d{2})\.\d{3}\s+-->\s+((?:\d{2}:)?\d{2}:\d{2})\.\d{3}/;

function normalizeVttTimestamp(s) {
  return s.length === 5 ? `00:${s}` : s;
}

// Parse a .vtt file into an array of cues: { start: "hh:mm:ss", text: "..." }.
// We deliberately ignore styling, regions, and cue identifiers.
export function parseVtt(vttText) {
  const lines = vttText.replace(/\r\n/g, "\n").split("\n");
  const cues = [];
  let i = 0;

  // Skip WEBVTT header and any leading metadata block until first blank line.
  if (lines[i] && lines[i].startsWith("WEBVTT")) {
    while (i < lines.length && lines[i].trim() !== "") i++;
  }

  while (i < lines.length) {
    // Skip blank lines between cues.
    while (i < lines.length && lines[i].trim() === "") i++;
    if (i >= lines.length) break;

    // Optional cue identifier line (no "-->"). Skip it.
    if (!TIMING_RE.test(lines[i]) && i + 1 < lines.length && TIMING_RE.test(lines[i + 1])) {
      i++;
    }

    const timing = lines[i] && lines[i].match(TIMING_RE);
    if (!timing) {
      // Not a timing line — skip until next blank to resync.
      while (i < lines.length && lines[i].trim() !== "") i++;
      continue;
    }
    const start = normalizeVttTimestamp(timing[1]);
    i++;

    const textLines = [];
    while (i < lines.length && lines[i].trim() !== "") {
      textLines.push(lines[i]);
      i++;
    }
    const text = decodeEntities(stripInlineTags(textLines.join(" "))).replace(/\s+/g, " ").trim();
    if (text) cues.push({ start, text });
  }

  // De-duplicate consecutive identical cue text (common with YouTube auto-captions
  // that repeat a line as it scrolls into the next cue).
  const dedup = [];
  for (const cue of cues) {
    const prev = dedup[dedup.length - 1];
    if (prev && prev.text === cue.text) continue;
    dedup.push(cue);
  }
  return dedup;
}

// YouTube auto-captions emit a rolling N-line window where the same phrase
// appears repeated across overlapping cues (a 3-line scroll is typical). Cue-
// level dedup above only catches strict consecutive duplicates; this pass walks
// the full transcript word stream and collapses any consecutive identical N-word
// phrase (for N from 3 to 15). Multiple passes handle nested/overlapping repeats.
export function dedupRollingPhrases(text, maxPasses = 6) {
  let cur = text.replace(/\s+/g, " ").trim();
  for (let p = 0; p < maxPasses; p++) {
    const words = cur.split(" ");
    const out = [];
    let i = 0;
    while (i < words.length) {
      let skip = 0;
      // Prefer longer matches so we collapse the largest repeated unit first.
      for (let n = 15; n >= 3; n--) {
        if (i + 2 * n > words.length) continue;
        const a = words.slice(i, i + n).join(" ").toLowerCase();
        const b = words.slice(i + n, i + 2 * n).join(" ").toLowerCase();
        if (a === b) { skip = n; break; }
      }
      if (skip > 0) {
        for (let k = 0; k < skip; k++) out.push(words[i + k]);
        i += skip * 2;
      } else {
        out.push(words[i]);
        i++;
      }
    }
    const next = out.join(" ");
    if (next === cur) break;
    cur = next;
  }
  return cur;
}

function normalizeWord(w) {
  return w.toLowerCase().replace(/^[^\p{L}\p{N}/]+|[^\p{L}\p{N}/%-]+$/gu, "");
}

function wordsOf(text) {
  return text.replace(/\s+/g, " ").trim().split(" ").filter(Boolean);
}

function findTailPrefixOverlap(tailWords, nextWords, maxOverlap = 80, minOverlap = 3) {
  const max = Math.min(tailWords.length, nextWords.length, maxOverlap);
  for (let n = max; n >= minOverlap; n--) {
    let ok = true;
    for (let i = 0; i < n; i++) {
      if (normalizeWord(tailWords[tailWords.length - n + i]) !== normalizeWord(nextWords[i])) {
        ok = false;
        break;
      }
    }
    if (ok) return n;
  }
  return 0;
}

// YouTube auto captions often emit an overlapping scrolling window: cue A has
// "foo bar", cue B has "foo bar baz qux", cue C has "baz qux next words".
// For timestamped output, phrase-level dedup is not enough because each cue is
// separate. This converts cue text into only the newly-introduced words while
// keeping useful timestamps. Require a 3+ word overlap so ordinary repeated
// single words at cue boundaries are preserved.
export function dedupRollingCues(cues) {
  const out = [];
  const transcriptWords = [];
  for (const cue of cues) {
    const cueWords = wordsOf(cue.text);
    if (!cueWords.length) continue;
    const overlap = findTailPrefixOverlap(transcriptWords, cueWords);
    const freshWords = cueWords.slice(overlap);
    if (!freshWords.length) continue;
    const text = freshWords.join(" ").trim();
    if (!text) continue;
    const prev = out[out.length - 1];
    if (prev && normalizeWord(prev.text) === normalizeWord(text)) continue;
    out.push({ start: cue.start, text });
    transcriptWords.push(...freshWords);
    // Bound memory/comparison cost for long videos; only the tail is needed for
    // rolling-window overlap detection.
    if (transcriptWords.length > 500) transcriptWords.splice(0, transcriptWords.length - 500);
  }
  return out;
}

// -------- main --------

async function main() {
  if (TEST_HOOKS && process.env.YOUTUBE_TRANSCRIPT_TEST_THROW_PATH) {
    throw new Error(`synthetic path failure at ${process.env.YOUTUBE_TRANSCRIPT_TEST_THROW_PATH}`);
  }
  const args = parseArgs(process.argv.slice(2));

  // Make a fresh temp dir; ensure cleanup on any exit path.
  const tempDir = mkdtempSync(join(tmpdir(), "yt-transcript-"));
  let cleaned = false;
  const cleanup = () => {
    if (cleaned) return;
    cleaned = true;
    try { rmSync(tempDir, { recursive: true, force: true }); } catch { /* best effort */ }
  };
  process.on("exit", cleanup);
  process.on("SIGINT", () => { try { activeYtDlpProc?.kill("SIGKILL"); } catch { /* best effort */ } cleanup(); process.exit(130); });
  process.on("SIGTERM", () => { try { activeYtDlpProc?.kill("SIGKILL"); } catch { /* best effort */ } cleanup(); process.exit(143); });

  // Ask yt-dlp for subtitles + JSON metadata, no media download.
  const outTemplate = join(tempDir, "%(id)s.%(ext)s");
  const ytArgs = [
    "--skip-download",
    "--write-subs",
    "--write-auto-subs",
    "--sub-lang", args.lang,
    "--sub-format", "vtt",
    "--no-playlist",
    "--no-warnings",
    "--ignore-config",
    "--print-json",
    "-o", outTemplate,
    "--",
    args.url,
  ];

  const result = await runYtDlp(ytArgs);

  if (result.spawnError && /ENOENT/i.test(result.stderr)) {
    die("yt-dlp not found on PATH. Install/verify using the official yt-dlp project instructions, then reopen your shell.");
  }
  if (result.timedOut) {
    die(`yt-dlp timed out after ${Math.round(YTDLP_TIMEOUT_MS / 1000)} seconds. Retry later or use a shorter/public video.`);
  }
  // Find any .vtt file in the temp dir. Some yt-dlp versions have returned a
  // nonzero exit after still writing usable subtitles; prefer parseable captions
  // over failing hard when the requested caption artifact exists.
  let vttFiles;
  try {
    if (TEST_HOOKS && process.env.YOUTUBE_TRANSCRIPT_TEST_REMOVE_TEMP_BEFORE_READDIR) rmSync(tempDir, { recursive: true, force: true });
    vttFiles = readdirSync(tempDir).filter(n => n.toLowerCase().endsWith(".vtt"));
  } catch (e) {
    die(`could not read temp dir: ${scrubLocalPaths(e.message || e, tempDir)}`);
  }

  if (result.code !== 0) {
    const tail = ytDlpErrorTail(result.stderr, tempDir);
    if (vttFiles.length) {
      process.stderr.write(`warning: yt-dlp exited with code ${result.code}.${rateLimitHint(result.stderr)} continuing because subtitle file(s) were produced. stderr tail:\n${tail || "(empty)"}\n`);
    } else {
      die(`yt-dlp exited with code ${result.code}.${rateLimitHint(result.stderr)} stderr tail:\n${tail || "(empty)"}`);
    }
  }

  // Parse the metadata JSON yt-dlp printed on stdout (last line that parses).
  let meta = null;
  const stdoutLines = result.stdout.split(/\r?\n/).filter(l => l.trim().length);
  for (let k = stdoutLines.length - 1; k >= 0; k--) {
    const line = stdoutLines[k].trim();
    if (!line.startsWith("{")) continue;
    try { meta = JSON.parse(line); break; } catch { /* keep looking */ }
  }

  // Prefer a .vtt file matching the requested lang.
  if (!vttFiles.length) {
    die(`no subtitles available for lang=${args.lang}. Try a different --lang or check that the video has captions.`);
  }

  const langTag = args.lang.toLowerCase();
  const preferred =
    vttFiles.find(n => n.toLowerCase().includes(`.${langTag}.vtt`)) ||
    vttFiles.find(n => n.toLowerCase().includes(`.${langTag}-`)) ||
    vttFiles[0];

  // Auto-detection: yt-dlp's --print-json output exposes `subtitles` (manual
  // captions) and `automatic_captions` (YouTube's auto-generated captions) as
  // separate maps. A track is auto-generated when the requested language is
  // missing from `subtitles` but present in `automatic_captions`. Fall back to
  // a filename heuristic only when metadata isn't available.
  let auto = false;
  if (meta) {
    const manual = meta.subtitles && meta.subtitles[args.lang];
    const autoCap = meta.automatic_captions && meta.automatic_captions[args.lang];
    const hasManual = Array.isArray(manual) ? manual.length > 0 : !!manual;
    const hasAuto = Array.isArray(autoCap) ? autoCap.length > 0 : !!autoCap;
    if (!hasManual && hasAuto) auto = true;
  } else if (/auto/i.test(preferred)) {
    auto = true;
  }

  let vttText;
  try {
    if (TEST_HOOKS && process.env.YOUTUBE_TRANSCRIPT_TEST_REMOVE_VTT_BEFORE_READ) rmSync(join(tempDir, preferred), { force: true });
    vttText = readFileSync(join(tempDir, preferred), "utf8");
  } catch (e) {
    die(`could not read .vtt file: ${scrubLocalPaths(e.message || e, tempDir)}`);
  }

  const cues = parseVtt(vttText);
  if (!cues.length) {
    die(`subtitle file was empty after parsing: ${preferred}`);
  }

  const title = (meta && (meta.title || meta.fulltitle)) || "";

  // For auto-captions, run rolling dedup. Manual captions don't need it (no
  // scrolling-window emit). Timestamped output uses cue-level overlap trimming;
  // non-timestamp output also gets phrase-level dedup. --no-dedup is the user
  // escape hatch when dedup eats deliberate verbatim repetition.
  const shouldDedupRolling = auto && !args.noDedup;
  const outputCues = shouldDedupRolling ? dedupRollingCues(cues) : cues;

  if (args.json) {
    let transcript;
    if (args.timestamps) {
      transcript = outputCues.map(c => `[${c.start}] ${c.text}`).join("\n");
    } else {
      transcript = outputCues.map(c => c.text).join(" ");
      if (shouldDedupRolling) transcript = dedupRollingPhrases(transcript);
    }
    const payload = {
      url: args.url,
      title,
      lang: args.lang,
      auto,
      timestamps: args.timestamps,
      transcript: enforceTranscriptSize(transcript),
    };
    process.stdout.write(JSON.stringify(payload, null, 2) + "\n");
    return;
  }

  // Plain text output.
  if (args.timestamps) {
    process.stdout.write(enforceTranscriptSize(outputCues.map(c => `[${c.start}] ${c.text}`).join("\n")) + "\n");
  } else {
    let plain = outputCues.map(c => c.text).join(" ");
    if (shouldDedupRolling) plain = dedupRollingPhrases(plain);
    process.stdout.write(enforceTranscriptSize(plain) + "\n");
  }
}

if (process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1]) {
  main().catch((e) => die(`unexpected error: ${scrubLocalPaths(e && (e.message || e.stack) || e)}`));
}
