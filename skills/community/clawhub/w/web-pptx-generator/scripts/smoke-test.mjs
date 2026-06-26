#!/usr/bin/env node

import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { execFileSync } from "node:child_process";
import { listThemes } from "./theme-bundles.mjs";

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), "web-slides-smoke-"));
const repoRoot = process.cwd();

function runNode(script, args) {
  execFileSync(process.execPath, [path.join(repoRoot, script), ...args], {
    stdio: "inherit",
    cwd: repoRoot,
  });
}

runNode("scripts/validate-content.mjs", ["examples/investor-pitch.json"]);
runNode("scripts/markdown-to-content.mjs", [
  "--input",
  "examples/investor-pitch.md",
  "--output",
  path.join(tmpDir, "investor-pitch.json"),
  "--scene",
  "investor-pitch",
  "--mobile",
]);
runNode("scripts/validate-content.mjs", [path.join(tmpDir, "investor-pitch.json")]);
runNode("scripts/generate-slide-html.mjs", [
  "--content",
  path.join(tmpDir, "investor-pitch.json"),
  "--out",
  path.join(tmpDir, "investor-pitch.html"),
]);
runNode("scripts/qa-deck.mjs", [
  "--content",
  path.join(tmpDir, "investor-pitch.json"),
  "--html",
  path.join(tmpDir, "investor-pitch.html"),
]);

for (const theme of listThemes()) {
  runNode("scripts/generate-slide-html.mjs", [
    "--theme",
    theme,
    "--scene",
    theme === "startup-pitch" ? "investor-pitch" : "project-report",
    "--title",
    theme,
    "--out",
    path.join(tmpDir, `${theme}.html`),
  ]);
}

console.log(JSON.stringify({
  ok: true,
  tmpDir,
  themes: listThemes().length,
}, null, 2));
