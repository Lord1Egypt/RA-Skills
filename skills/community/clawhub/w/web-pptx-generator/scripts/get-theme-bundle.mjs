#!/usr/bin/env node

import { findThemeByScene, getTheme, listThemes } from "./theme-bundles.mjs";

function parseArgs(argv) {
  const args = { list: false, theme: "", scene: "" };
  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--list") args.list = true;
    if (part === "--theme") args.theme = argv[i + 1] ?? "";
    if (part === "--scene") args.scene = argv[i + 1] ?? "";
  }
  return args;
}

const args = parseArgs(process.argv);

if (args.list) {
  console.log(JSON.stringify(listThemes(), null, 2));
  process.exit(0);
}

if (args.theme) {
  const theme = getTheme(args.theme);
  if (!theme) {
    console.error(`unknown theme: ${args.theme}`);
    process.exit(1);
  }
  console.log(JSON.stringify({ [args.theme]: theme }, null, 2));
  process.exit(0);
}

if (args.scene) {
  const theme = findThemeByScene(args.scene);
  if (!theme) {
    console.error(`unknown scene: ${args.scene}`);
    process.exit(1);
  }
  const { name, ...rest } = theme;
  console.log(JSON.stringify({ [name]: rest }, null, 2));
  process.exit(0);
}

console.log("Usage: node scripts/get-theme-bundle.mjs --list | --theme <name> | --scene <scene>");
