#!/usr/bin/env node
/**
 * Print SocialEcho platform publish limits (reference markdown) to stdout.
 * Usage: node platform-limits.js [--lang cn|en] [--help]
 */
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

const args = parseArgs(process.argv);

if (args.help) {
  console.log(`Usage: node platform-limits.js [--lang cn|en]

Print platform publish limits (copy, media, formats) to stdout.

  --lang cn   Chinese (default)
  --lang en   English
`);
  process.exit(0);
}

const raw = String(args.lang ?? "cn").toLowerCase();
const lang = raw === "en" ? "en" : "cn";
const fileName =
  lang === "en" ? "platform-publish-limits_en.md" : "platform-publish-limits_cn.md";
const filePath = path.join(__dirname, fileName);

if (!fs.existsSync(filePath)) {
  console.error(`Missing bundled doc: ${fileName}`);
  process.exit(1);
}

process.stdout.write(fs.readFileSync(filePath, "utf8"));
