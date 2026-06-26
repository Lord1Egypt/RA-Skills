#!/usr/bin/env node

import { promises as fs } from "node:fs";
import { createWriteStream } from "node:fs";
import os from "node:os";
import path from "node:path";
import { randomBytes } from "node:crypto";

const DEFAULT_MAX_BYTES = 15 * 1024 * 1024;
const DEFAULT_TIMEOUT_MS = 20_000;

function parseArgs(argv) {
  const args = {
    home: process.env.OPENCLAW_HOME?.trim() || path.join(os.homedir(), ".openclaw"),
    dir: "",
    download: true,
    dryRun: false,
    maxBytes: DEFAULT_MAX_BYTES,
    timeoutMs: DEFAULT_TIMEOUT_MS,
    limit: 0,
    topic: "",
    verbose: false,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    const next = argv[i + 1];

    if (token === "--help" || token === "-h") {
      args.help = true;
      continue;
    }
    if (token === "--dry-run") {
      args.dryRun = true;
      continue;
    }
    if (token === "--no-download") {
      args.download = false;
      continue;
    }
    if (token === "--verbose") {
      args.verbose = true;
      continue;
    }
    if (token === "--home" && next) {
      args.home = next;
      i += 1;
      continue;
    }
    if (token === "--dir" && next) {
      args.dir = next;
      i += 1;
      continue;
    }
    if (token === "--topic" && next) {
      args.topic = next;
      i += 1;
      continue;
    }
    if (token === "--limit" && next) {
      args.limit = Number(next) || 0;
      i += 1;
      continue;
    }
    if (token === "--max-bytes" && next) {
      args.maxBytes = Number(next) || DEFAULT_MAX_BYTES;
      i += 1;
      continue;
    }
    if (token === "--timeout-ms" && next) {
      args.timeoutMs = Number(next) || DEFAULT_TIMEOUT_MS;
      i += 1;
      continue;
    }
  }

  args.home = path.resolve(args.home);
  args.dir = args.dir ? path.resolve(args.dir) : path.join(args.home, "topic-memory");
  return args;
}

function printHelp() {
  console.log(`Usage: openclaw-wtt-topic-memory-backfill [options]\n\nOptions:\n  --home <path>         OpenClaw home (default: ~/.openclaw)\n  --dir <path>          Topic-memory dir (default: <home>/topic-memory)\n  --topic <topicId>     Backfill only one topic file\n  --limit <n>           Process at most n files\n  --dry-run             Preview without writing files\n  --no-download         Don't download media to local paths\n  --max-bytes <n>       Max bytes per media file (default: 15728640)\n  --timeout-ms <n>      Per-media timeout in ms (default: 20000)\n  --verbose             Print per-file details\n  -h, --help            Show help\n`);
}

function compactDiscussionContent(raw) {
  const source = String(raw || "");
  return source
    .replace(/┌─\s*来源标识[\s\S]*?└[^\n]*\n?/g, "")
    .replace(/\[回复上下文\][\s\S]*?(?:---|$)/g, "")
    .replace(/<br\s*\/?>/gi, "\n")
    .replace(/<\/p>/gi, "\n")
    .replace(/<[^>]+>/g, "")
    .replace(/!\[[^\]]*\]\(([^)]+)\)/g, "[image:$1]")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function detectMediaUrls(rawText) {
  const text = String(rawText || "");
  const out = new Set();

  const imageTagRe = /\[image:([^\]]+)\]/gi;
  let m;
  while ((m = imageTagRe.exec(text)) !== null) {
    const u = String(m[1] || "").trim();
    if (u) out.add(u);
  }

  const mdImgRe = /!\[[^\]]*\]\(([^)]+)\)/gi;
  while ((m = mdImgRe.exec(text)) !== null) {
    const u = String(m[1] || "").trim();
    if (u) out.add(u);
  }

  const urlRe = /https?:\/\/[^\s)\]]+/gi;
  while ((m = urlRe.exec(text)) !== null) {
    const u = String(m[0] || "").replace(/[),.;]+$/, "").trim();
    if (/\.(?:png|jpe?g|gif|webp|bmp|svg|heic|heif)(?:\?|$)/i.test(u) || /\/media\//i.test(u)) {
      out.add(u);
    }
  }

  return Array.from(out);
}

function parseTopicFile(raw) {
  const lines = String(raw || "").split("\n");
  const topicNameLine = lines.find((line) => /^topic_name:\s*/.test(line));
  const topicName = topicNameLine ? topicNameLine.replace(/^topic_name:\s*/, "").trim() : "";

  const entryRe = /^- \[([^\]]*)\]\s+([\w]+):(\S+?)(?:\(([^)]*)\))?\s+id=(\S+?)(?:\s+reply_to=(\S+))?(?:\s+.*)?$/;

  const messages = [];
  let i = 0;
  while (i < lines.length) {
    const match = lines[i].match(entryRe);
    if (!match) {
      i += 1;
      continue;
    }

    const [, createdAt, senderType, senderId, displayName, id, replyTo] = match;
    i += 1;

    const bodyLines = [];
    while (i < lines.length && !entryRe.test(lines[i])) {
      if (lines[i].startsWith("  ")) bodyLines.push(lines[i].slice(2));
      i += 1;
    }

    let text = "";
    const mediaPaths = [];
    const mediaUrls = [];
    let replyExcerpt = "";

    for (const row of bodyLines) {
      const line = row.trim();
      if (!line) continue;

      if (line.startsWith("text:")) {
        text = line.slice("text:".length).trim();
        continue;
      }
      if (line.startsWith("media_paths:")) {
        const payload = line.slice("media_paths:".length).trim();
        for (const part of payload.split("|").map((v) => v.trim()).filter(Boolean)) mediaPaths.push(part);
        continue;
      }
      if (line.startsWith("media_urls:")) {
        const payload = line.slice("media_urls:".length).trim();
        for (const part of payload.split("|").map((v) => v.trim()).filter(Boolean)) mediaUrls.push(part);
        continue;
      }
      if (line.startsWith("reply_excerpt:")) {
        replyExcerpt = line.slice("reply_excerpt:".length).trim();
        continue;
      }

      if (!text) text = line;
      else text += ` ${line}`;
    }

    if (!mediaUrls.length && text) {
      mediaUrls.push(...detectMediaUrls(text));
    }

    messages.push({
      id,
      senderId,
      senderDisplayName: displayName || "",
      senderType: senderType || "unknown",
      createdAt: createdAt || "",
      replyTo: replyTo || "",
      text: compactDiscussionContent(text),
      mediaPaths: Array.from(new Set(mediaPaths)),
      mediaUrls: Array.from(new Set(mediaUrls)),
      replyExcerpt: replyExcerpt || "",
    });
  }

  return { topicName, messages };
}

function extensionFromContentType(contentType) {
  const normalized = String(contentType || "").toLowerCase();
  if (!normalized) return "";
  if (normalized.includes("jpeg") || normalized.includes("jpg")) return ".jpg";
  if (normalized.includes("png")) return ".png";
  if (normalized.includes("gif")) return ".gif";
  if (normalized.includes("webp")) return ".webp";
  if (normalized.includes("bmp")) return ".bmp";
  if (normalized.includes("svg")) return ".svg";
  if (normalized.includes("heic")) return ".heic";
  if (normalized.includes("heif")) return ".heif";
  if (normalized.includes("mp4")) return ".mp4";
  return "";
}

function extensionFromUrl(urlRaw) {
  try {
    const parsed = new URL(urlRaw);
    const ext = path.extname(parsed.pathname || "").toLowerCase();
    if (/^\.[a-z0-9]{1,8}$/.test(ext)) return ext;
    return "";
  } catch {
    return "";
  }
}

async function downloadOneMedia(url, inboundDir, opts) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), Math.max(1000, opts.timeoutMs));

  try {
    const resp = await fetch(url, {
      method: "GET",
      redirect: "follow",
      signal: controller.signal,
      headers: { Accept: "image/*,*/*;q=0.8" },
    });

    if (!resp.ok) {
      throw new Error(`http_${resp.status}`);
    }

    const contentType = (resp.headers.get("content-type") || "").split(";")[0].trim().toLowerCase();
    const ext = extensionFromContentType(contentType) || extensionFromUrl(url) || ".bin";

    const fileName = `wtt-backfill-${Date.now()}-${randomBytes(6).toString("hex")}${ext}`;
    const filePath = path.join(inboundDir, fileName);

    await fs.mkdir(inboundDir, { recursive: true });

    const stream = createWriteStream(filePath);
    let total = 0;
    for await (const chunk of resp.body) {
      const buf = Buffer.from(chunk);
      total += buf.length;
      if (total > opts.maxBytes) {
        stream.destroy();
        await fs.rm(filePath, { force: true }).catch(() => {});
        throw new Error(`media_too_large_${total}`);
      }
      stream.write(buf);
    }
    stream.end();

    return filePath;
  } finally {
    clearTimeout(timer);
  }
}

function renderTopicFile(topicId, topicName, messages) {
  const lines = [];
  lines.push(`# topic_id_${topicId}`);
  if (topicName && topicName.trim()) lines.push(`topic_name: ${topicName.trim()}`);
  lines.push(`updated_at: ${new Date().toISOString()}`);
  lines.push("");

  for (const msg of messages) {
    const nameTag = msg.senderDisplayName ? `(${msg.senderDisplayName})` : "";
    const who = `${msg.senderType || "unknown"}:${msg.senderId}${nameTag}`;
    const mediaCount = (msg.mediaPaths?.length || 0) + (msg.mediaUrls?.length || 0);
    const header = `- [${msg.createdAt || ""}] ${who} id=${msg.id}${msg.replyTo ? ` reply_to=${msg.replyTo}` : ""}${mediaCount > 0 ? ` media_count=${mediaCount}` : ""}`;
    lines.push(header);
    lines.push(`  text: ${compactDiscussionContent(msg.text || "")}`);
    if (msg.mediaPaths && msg.mediaPaths.length > 0) {
      lines.push(`  media_paths: ${msg.mediaPaths.join(" | ")}`);
    }
    if (msg.mediaUrls && msg.mediaUrls.length > 0) {
      lines.push(`  media_urls: ${msg.mediaUrls.join(" | ")}`);
    }
    if (msg.replyExcerpt) {
      lines.push(`  reply_excerpt: ${compactDiscussionContent(msg.replyExcerpt).slice(0, 220)}`);
    }
  }

  return `${lines.join("\n")}\n`;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    printHelp();
    return;
  }

  const topicDir = args.dir;
  const inboundDir = path.join(args.home, "media", "inbound");

  let files;
  try {
    files = await fs.readdir(topicDir);
  } catch (err) {
    console.error(`[backfill] topic-memory dir not found: ${topicDir}`);
    process.exitCode = 1;
    return;
  }

  let targets = files
    .filter((name) => /^topic_id_.+\.md$/.test(name))
    .map((name) => path.join(topicDir, name))
    .sort();

  if (args.topic) {
    const wanted = path.join(topicDir, `topic_id_${args.topic}.md`);
    targets = targets.filter((p) => p === wanted);
  }

  if (args.limit > 0) {
    targets = targets.slice(0, args.limit);
  }

  const downloadCache = new Map();
  let scanned = 0;
  let updated = 0;
  let downloaded = 0;

  for (const filePath of targets) {
    scanned += 1;
    const fileName = path.basename(filePath);
    const topicId = fileName.replace(/^topic_id_/, "").replace(/\.md$/, "");

    const raw = await fs.readFile(filePath, "utf8");
    const parsed = parseTopicFile(raw);

    if (!parsed.messages.length) {
      if (args.verbose) console.log(`[backfill] skip empty ${fileName}`);
      continue;
    }

    const messageById = new Map(parsed.messages.map((m) => [m.id, m]));

    for (const msg of parsed.messages) {
      if (msg.replyTo && !msg.replyExcerpt) {
        const target = messageById.get(msg.replyTo);
        if (target) {
          msg.replyExcerpt = compactDiscussionContent(target.text || "").slice(0, 220);
        }
      }

      if (!Array.isArray(msg.mediaUrls) || msg.mediaUrls.length === 0) {
        msg.mediaUrls = detectMediaUrls(msg.text || "");
      }

      if (!args.download || !msg.mediaUrls.length) continue;

      const nextPaths = Array.isArray(msg.mediaPaths) ? [...msg.mediaPaths] : [];
      for (const url of msg.mediaUrls) {
        if (!/^https?:\/\//i.test(url)) continue;
        if (downloadCache.has(url)) {
          const cached = downloadCache.get(url);
          if (cached) nextPaths.push(cached);
          continue;
        }

        try {
          const localPath = await downloadOneMedia(url, inboundDir, {
            maxBytes: args.maxBytes,
            timeoutMs: args.timeoutMs,
          });
          downloaded += 1;
          downloadCache.set(url, localPath);
          nextPaths.push(localPath);
        } catch (err) {
          downloadCache.set(url, "");
          if (args.verbose) {
            const reason = err instanceof Error ? err.message : String(err);
            console.log(`[backfill] media download failed topic=${topicId} url=${url} reason=${reason}`);
          }
        }
      }

      msg.mediaPaths = Array.from(new Set(nextPaths.filter(Boolean)));
    }

    const nextContent = renderTopicFile(topicId, parsed.topicName, parsed.messages);
    if (nextContent !== raw) {
      updated += 1;
      if (!args.dryRun) {
        await fs.writeFile(filePath, nextContent, "utf8");
      }
      if (args.verbose || args.dryRun) {
        console.log(`[backfill] updated ${fileName}`);
      }
    } else if (args.verbose) {
      console.log(`[backfill] unchanged ${fileName}`);
    }
  }

  console.log(`[backfill] done scanned=${scanned} updated=${updated} downloaded=${downloaded} dry_run=${args.dryRun}`);
}

main().catch((err) => {
  const msg = err instanceof Error ? err.stack || err.message : String(err);
  console.error(`[backfill] fatal: ${msg}`);
  process.exitCode = 1;
});
