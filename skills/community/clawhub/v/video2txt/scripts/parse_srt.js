#!/usr/bin/env node
/**
 * parse_srt.js - Parse SRT file to plain text
 * Usage: node parse_srt.js <srt_path> [output_txt_path]
 * Outputs plain text to stdout or file
 */

const fs = require("fs");
const path = require("path");

const srtPath = process.argv[2];
const outPath = process.argv[3];

if (!srtPath) {
  console.error("Usage: node parse_srt.js <srt_path> [output_txt_path]");
  process.exit(1);
}

const content = fs.readFileSync(srtPath, "utf8");
const lines = content.split(/\r?\n/);
const text = [];

for (const line of lines) {
  const l = line.trim();
  if (/^\d+$/.test(l)) continue;
  if (/^\d{2}:\d{2}:\d{2}/.test(l)) continue;
  if (l === "") continue;
  const clean = l.replace(/<[^>]+>/g, "").replace(/[♪♫]/g, "").trim();
  if (clean) text.push(clean);
}

const plain = text.join("\n");

if (outPath) {
  fs.writeFileSync(outPath, plain, "utf8");
  console.log("OK:" + outPath);
} else {
  process.stdout.write(plain);
}
