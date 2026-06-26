#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { renderHtmlToPng } from "./chrome-utils.mjs";

function parseArgs(argv) {
  const args = {
    input: "",
    output: "",
    mobile: false,
    fullPage: false,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--input") args.input = argv[i + 1] ?? args.input;
    if (part === "--output") args.output = argv[i + 1] ?? args.output;
    if (part === "--mobile") args.mobile = true;
    if (part === "--full-page") args.fullPage = true;
  }

  if (!args.input) {
    console.error("Usage: node scripts/render-preview.mjs --input deck.html [--output deck.png] [--mobile]");
    process.exit(1);
  }

  return args;
}

const args = parseArgs(process.argv);
const inputPath = path.resolve(process.cwd(), args.input);
const outputPath = path.resolve(process.cwd(), args.output || inputPath.replace(/\.html?$/i, args.mobile ? ".mobile.png" : ".png"));

fs.mkdirSync(path.dirname(outputPath), { recursive: true });

renderHtmlToPng({
  inputUrl: `file://${inputPath}`,
  outputPath,
  width: args.mobile ? 430 : 1600,
  height: args.mobile ? 932 : 900,
  fullPage: args.mobile || args.fullPage,
});

console.log(JSON.stringify({
  input: inputPath,
  output: outputPath,
  mode: args.mobile ? "mobile" : "desktop",
}, null, 2));
