#!/usr/bin/env node

import {
  buildReplyBundle,
  getStyle,
  listStyles,
  recommendStyle,
  PERSONAS,
  MODES,
} from "./style-bundles.mjs";

function parseArgs(argv) {
  const args = {
    list: false,
    listPersonas: false,
    listModes: false,
    style: "",
    scene: "",
    goal: "",
    intensity: "",
    channel: "wechat",
    persona: "",
    mode: "",
  };
  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--list") args.list = true;
    if (part === "--list-personas") args.listPersonas = true;
    if (part === "--list-modes") args.listModes = true;
    if (part === "--style") args.style = argv[i + 1] ?? "";
    if (part === "--scene") args.scene = argv[i + 1] ?? "";
    if (part === "--goal") args.goal = argv[i + 1] ?? "";
    if (part === "--intensity") args.intensity = argv[i + 1] ?? "";
    if (part === "--channel") args.channel = argv[i + 1] ?? "wechat";
    if (part === "--persona") args.persona = argv[i + 1] ?? "";
    if (part === "--mode") args.mode = argv[i + 1] ?? "";
  }
  return args;
}

const args = parseArgs(process.argv);

if (args.list) {
  console.log(JSON.stringify(listStyles(), null, 2));
  process.exit(0);
}

if (args.listPersonas) {
  console.log(JSON.stringify(Object.keys(PERSONAS).sort(), null, 2));
  process.exit(0);
}

if (args.listModes) {
  console.log(JSON.stringify(Object.keys(MODES).sort(), null, 2));
  process.exit(0);
}

if (args.style) {
  const style = getStyle(args.style);
  if (!style) {
    console.error(`unknown style: ${args.style}`);
    process.exit(1);
  }
  console.log(JSON.stringify(buildReplyBundle(args), null, 2));
  process.exit(0);
}

if (args.scene || args.goal) {
  const styleName = recommendStyle(args);
  console.log(JSON.stringify(buildReplyBundle({ ...args, style: styleName }), null, 2));
  process.exit(0);
}

console.log("Usage: node scripts/get-style-bundle.mjs --list | --list-personas | --list-modes | --style <name> [--persona <name>] [--mode <name>] [--intensity <level>] [--channel <name>] | --scene <scene> [--goal <goal>]");
