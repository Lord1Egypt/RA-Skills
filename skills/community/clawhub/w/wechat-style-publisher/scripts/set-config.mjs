#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (!arg.startsWith("--")) {
      continue;
    }
    if (!next || next.startsWith("--")) {
      args[arg.slice(2)] = true;
    } else {
      args[arg.slice(2)] = next;
      i += 1;
    }
  }
  return args;
}

function coerceValue(raw, typeHint) {
  if (typeHint === "json") {
    return JSON.parse(raw);
  }
  if (typeHint === "number") {
    return Number(raw);
  }
  if (typeHint === "boolean") {
    return raw === "true";
  }
  if (raw === "true") {
    return true;
  }
  if (raw === "false") {
    return false;
  }
  if (raw === "null") {
    return null;
  }
  return raw;
}

function ensurePath(root, dottedPath) {
  const parts = dottedPath.split(".").filter(Boolean);
  let current = root;
  for (let index = 0; index < parts.length - 1; index += 1) {
    const key = parts[index];
    if (typeof current[key] !== "object" || current[key] === null || Array.isArray(current[key])) {
      current[key] = {};
    }
    current = current[key];
  }
  return { parent: current, key: parts[parts.length - 1] };
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.config || !args.path) {
    throw new Error("Usage: node scripts/set-config.mjs --config config.json --path publishing.defaultTheme --value fresh-green");
  }

  const configPath = path.resolve(args.config);
  const raw = await fs.readFile(configPath, "utf8");
  const config = JSON.parse(raw);

  if (args.delete) {
    const { parent, key } = ensurePath(config, args.path);
    delete parent[key];
  } else {
    if (typeof args.value === "undefined") {
      throw new Error("Provide --value when not using --delete");
    }
    const { parent, key } = ensurePath(config, args.path);
    parent[key] = coerceValue(args.value, args.type || "");
  }

  await fs.writeFile(configPath, `${JSON.stringify(config, null, 2)}\n`, "utf8");
  process.stdout.write(`${args.path}\n`);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
