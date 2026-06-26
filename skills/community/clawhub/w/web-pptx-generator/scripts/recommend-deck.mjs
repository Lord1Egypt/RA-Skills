#!/usr/bin/env node

import { DEFAULT_DECK_LENGTH, recommendTheme } from "./theme-bundles.mjs";

function parseArgs(argv) {
  const args = { scene: "", density: "medium", mobile: false };
  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--scene") args.scene = argv[i + 1] ?? "";
    if (part === "--density") args.density = argv[i + 1] ?? "medium";
    if (part === "--mobile") args.mobile = true;
  }
  return args;
}

const args = parseArgs(process.argv);
const recommendation = recommendTheme(args);

if (!recommendation) {
  console.error("could not recommend a theme");
  process.exit(1);
}

const result = {
  scene: args.scene,
  density: args.density,
  mobile: args.mobile,
  recommendedTheme: recommendation.themeName,
  engine: recommendation.engine,
  tone: recommendation.tone,
  suggestedLayouts: recommendation.layouts,
  suggestedSlideCount: DEFAULT_DECK_LENGTH[args.density] ?? DEFAULT_DECK_LENGTH.medium,
};

console.log(JSON.stringify(result, null, 2));
