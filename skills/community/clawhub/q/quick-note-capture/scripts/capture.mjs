#!/usr/bin/env node
import { appendFileSync, mkdirSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const args = process.argv.slice(2);
let text = "";
let tags = [];
for (let i = 0; i < args.length; i++) {
  if (args[i] === "--text") text = args[++i] ?? "";
  else if (args[i] === "--tags") tags = (args[++i] ?? "").split(",").filter(Boolean);
}
if (!text) {
  console.error("missing --text");
  process.exit(1);
}
const dir = join(homedir(), "notes");
mkdirSync(dir, { recursive: true });
const file = join(dir, "inbox.md");
const ts = new Date().toISOString();
const tagStr = tags.map((t) => `#${t.replace(/\s/g, "")}`).join(" ");
const line = `- [${ts}]${tagStr ? " " + tagStr : ""} ${text}\n`;
appendFileSync(file, line, "utf8");
console.log("captured ->", file);
