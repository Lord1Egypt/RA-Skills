#!/usr/bin/env node
"use strict";

const { spawnSync } = require("child_process");
const path = require("path");

const root = path.resolve(__dirname, "..");
const installScript = path.join(root, "install.py");
const args = process.argv.slice(2);

if (args[0] === "install.py" || args[0] === "./install.py" || args[0] === "install") {
  args.shift();
}

function candidateCommands() {
  if (process.platform === "win32") {
    return [
      { command: "py", args: ["-3"] },
      { command: "python", args: [] },
      { command: "python3", args: [] }
    ];
  }
  return [
    { command: "python3", args: [] },
    { command: "python", args: [] }
  ];
}

function works(candidate) {
  const result = spawnSync(candidate.command, [...candidate.args, "--version"], {
    encoding: "utf8",
    stdio: "pipe"
  });
  return result.status === 0;
}

const python = candidateCommands().find(works);
if (!python) {
  console.error("Python 3 is required. Install Python 3, then run this npx command again.");
  process.exit(1);
}

const result = spawnSync(python.command, [...python.args, installScript, ...args], {
  cwd: process.cwd(),
  stdio: "inherit"
});

if (result.error) {
  console.error(result.error.message);
  process.exit(1);
}

process.exit(result.status ?? 1);
