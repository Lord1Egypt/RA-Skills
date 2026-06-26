#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { buildArticleHtml } from "../lib/style.mjs";

function printHelp() {
  process.stdout.write(`Usage:
  node scripts/apply-style.mjs --input article.html [--output out.html] [--theme modern-minimal]
  cat article.html | node scripts/apply-style.mjs --stdin [--theme chinese-style]
  node scripts/apply-style.mjs --input article.html --template-name growth-weekly --registry assets/template-variables.example.json
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--stdin" || arg === "--help") {
      args[arg.slice(2)] = true;
      continue;
    }
    args[arg.slice(2)] = argv[i + 1];
    i += 1;
  }
  return args;
}

async function readStdin() {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString("utf8");
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help) {
    printHelp();
    return;
  }

  let templateVariable = null;
  if (args["template-name"] && args.registry) {
    const raw = await fs.readFile(path.resolve(args.registry), "utf8");
    templateVariable = JSON.parse(raw)?.templates?.[args["template-name"]] || null;
    if (!templateVariable) {
      throw new Error(`Template variable not found: ${args["template-name"]}`);
    }
  }

  const html = args.stdin
    ? await readStdin()
    : await fs.readFile(path.resolve(args.input), "utf8");

  const output = await buildArticleHtml({
    html,
    theme: args.theme || "modern-minimal",
    cssFile: templateVariable?.customCss ? "" : (args["css-file"] || ""),
    customCss: [templateVariable?.customCss || "", args["custom-css"] || ""].filter(Boolean).join("\n"),
    introHtml: templateVariable?.introHtml || (args["intro-template"] ? await fs.readFile(path.resolve(args["intro-template"]), "utf8") : ""),
    outroHtml: templateVariable?.outroHtml || (args["outro-template"] ? await fs.readFile(path.resolve(args["outro-template"]), "utf8") : "")
  });

  if (args.output) {
    await fs.writeFile(path.resolve(args.output), output, "utf8");
    process.stdout.write(`${path.resolve(args.output)}\n`);
    return;
  }

  process.stdout.write(output);
}

main().catch((error) => {
  process.stderr.write(`${error.message}\n`);
  process.exitCode = 1;
});
