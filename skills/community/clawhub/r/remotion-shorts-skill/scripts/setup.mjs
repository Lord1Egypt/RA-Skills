#!/usr/bin/env node
// Create or update a Remotion shorts project.
//
//   node <skill>/scripts/setup.mjs [folder]     default folder: ./remotion-shorts
//
// Copies the template, installs the pinned packages and downloads the headless browser
// Remotion renders with. Run it again after the skill updates: it refreshes the template
// files (any you changed are kept as <file>.bak) and leaves your scripts, assets and
// output alone.

import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const template = path.resolve(here, "..", "template");
const target = path.resolve(process.argv[2] ?? "remotion-shorts");

const major = Number(process.versions.node.split(".")[0]);
if (major < 20) {
  console.error(`Node ${process.versions.node} is too old. Install Node 20 or newer from https://nodejs.org and run this again.`);
  process.exit(1);
}

// Never touched: the user's own files.
const skip = new Set(["node_modules", "out", "assets", ".DS_Store"]);
let lockChanged = !fs.existsSync(path.join(target, "node_modules", "@remotion", "renderer"));
let updated = 0;

const copy = (from, to) => {
  for (const entry of fs.readdirSync(from, { withFileTypes: true })) {
    if (skip.has(entry.name)) continue;
    const a = path.join(from, entry.name);
    const b = path.join(to, entry.name);
    if (entry.isDirectory()) {
      fs.mkdirSync(b, { recursive: true });
      copy(a, b);
      continue;
    }
    const next = fs.readFileSync(a);
    if (fs.existsSync(b)) {
      const cur = fs.readFileSync(b);
      if (cur.equals(next)) continue;
      fs.copyFileSync(b, `${b}.bak`);
      updated += 1;
      if (entry.name === "package-lock.json" || entry.name === "package.json") lockChanged = true;
    }
    fs.writeFileSync(b, next);
  }
};

fs.mkdirSync(target, { recursive: true });
copy(template, target);
console.log(`Project: ${target}${updated ? ` (${updated} template file${updated > 1 ? "s" : ""} updated; old copies saved as .bak)` : ""}`);

const run = (cmd, args) => {
  const r = spawnSync(cmd, args, { cwd: target, stdio: "inherit", shell: process.platform === "win32" });
  if (r.status !== 0) {
    console.error(`\n"${cmd} ${args.join(" ")}" failed. Fix the error above and run setup again.`);
    process.exit(1);
  }
};

if (lockChanged) {
  console.log("Installing packages (about 260 MB, 1 to 2 minutes)...");
  run("npm", ["ci", "--no-audit", "--no-fund"]);
}
console.log("Checking the headless browser (downloads 100 to 150 MB the first time)...");
run("npx", ["remotion", "browser", "ensure"]);

console.log(`
Ready. Next:
  1. Write a short.json (see the skill's references/short-json.md).
  2. cd "${target}"
  3. node render.mjs short.json --stills    review sheets and cover in a few seconds
  4. node render.mjs short.json             the MP4
`);
