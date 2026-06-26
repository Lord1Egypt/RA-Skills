#!/usr/bin/env node
/**
 * zalo-multi-send: Send multiple images/files in one Zalo message.
 *
 * Usage:
 *   node send.mjs --to <userId> --files <f1,f2,...> [--caption "text"] [--group]
 *
 * --to       Zalo user ID or group ID
 * --files    Comma-separated list of local file paths or URLs
 * --caption  Optional message text (default: "")
 * --group    Pass this flag if --to is a group ID
 * --profile  Zalo credential profile (default: "default")
 *
 * Exit codes: 0 = success, 1 = error
 */

import { createRequire } from "module";
import { readFileSync, existsSync } from "fs";
import { join, extname, basename } from "path";
import os from "os";

const require = createRequire(import.meta.url);
const ZCA_PATH =
  "/home/tuan/.nvm/versions/node/v22.21.1/lib/node_modules/openclaw/extensions/zalouser/node_modules/zca-js";
const { Zalo, ThreadType } = require(ZCA_PATH);

// --- arg parsing ---
function parseArgs(argv) {
  const args = { to: "", files: [], caption: "", group: false, profile: "default" };
  for (let i = 2; i < argv.length; i++) {
    if (argv[i] === "--to") args.to = argv[++i];
    else if (argv[i] === "--files") args.files = argv[++i].split(",").map((s) => s.trim()).filter(Boolean);
    else if (argv[i] === "--caption") args.caption = argv[++i];
    else if (argv[i] === "--group") args.group = true;
    else if (argv[i] === "--profile") args.profile = argv[++i];
  }
  return args;
}

function resolveCredentialsPath(profile) {
  const name = !profile || profile === "default" ? "credentials.json" : `credentials-${encodeURIComponent(profile.trim().toLowerCase())}.json`;
  return join(os.homedir(), ".openclaw/credentials/zalouser", name);
}

function guessMime(filename) {
  const ext = extname(filename).toLowerCase();
  return { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif", ".webp": "image/webp", ".mp4": "video/mp4", ".pdf": "application/pdf" }[ext] ?? "application/octet-stream";
}

async function loadFile(source) {
  if (/^https?:\/\//.test(source)) {
    const res = await fetch(source);
    if (!res.ok) throw new Error(`HTTP ${res.status} fetching ${source}`);
    const buf = Buffer.from(await res.arrayBuffer());
    const name = basename(new URL(source).pathname) || "file.bin";
    return { buf, name };
  }
  if (!existsSync(source)) throw new Error(`File not found: ${source}`);
  const buf = readFileSync(source);
  return { buf, name: basename(source) };
}

async function main() {
  const args = parseArgs(process.argv);

  if (!args.to) { console.error("Error: --to is required"); process.exit(1); }
  if (!args.files.length) { console.error("Error: --files is required"); process.exit(1); }

  const credsPath = resolveCredentialsPath(args.profile);
  if (!existsSync(credsPath)) { console.error(`Error: No Zalo credentials at ${credsPath}`); process.exit(1); }
  const creds = JSON.parse(readFileSync(credsPath, "utf-8"));

  console.log(`Logging in (profile: ${args.profile})...`);
  const zalo = new Zalo({ logging: false, selfListen: false });
  const api = await zalo.login({ imei: creds.imei, cookie: creds.cookie, userAgent: creds.userAgent, language: creds.language });
  console.log("Logged in.");

  console.log(`Loading ${args.files.length} file(s)...`);
  const attachments = await Promise.all(
    args.files.map(async (src) => {
      const { buf, name } = await loadFile(src);
      console.log(`  + ${name} (${buf.length} bytes)`);
      const ext = extname(name) || ".bin";
      const safeName = name.includes(".") ? name : `${name}${ext}`;
      return { data: buf, filename: safeName, metadata: { totalSize: buf.length } };
    })
  );

  const threadType = args.group ? ThreadType.Group : ThreadType.User;
  console.log(`Sending to ${args.to} (${args.group ? "group" : "user"})...`);

  const result = await api.sendMessage(
    { msg: args.caption, attachments },
    args.to,
    threadType
  );

  const msgId = result?.message?.msgId ?? result?.msgId ?? "?";
  const attachCount = result?.attachment?.length ?? 0;
  console.log(`✅ Sent! msgId=${msgId}, attachments=${attachCount}`);
  console.log(JSON.stringify(result, null, 2));
  process.exit(0);
}

main().catch((err) => { console.error("Error:", err.message); process.exit(1); });
