#!/usr/bin/env node

import { DEFAULT_DECK_LENGTH, recommendTheme } from "./theme-bundles.mjs";

function parseArgs(argv) {
  const args = {
    title: "Untitled Deck",
    scene: "",
    density: "medium",
    mobile: false,
  };

  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--title") args.title = argv[i + 1] ?? args.title;
    if (part === "--scene") args.scene = argv[i + 1] ?? args.scene;
    if (part === "--density") args.density = argv[i + 1] ?? args.density;
    if (part === "--mobile") args.mobile = true;
  }

  return args;
}

function buildOutline(layouts, slideCount) {
  const seed = layouts.length ? layouts : ["cover", "insight", "closing"];
  const opening = seed[0] ?? "cover";
  const ending = seed[seed.length - 1] ?? "closing";
  const middlePool = seed.slice(1, -1).length ? seed.slice(1, -1) : ["insight", "two-column", "metrics"];

  return Array.from({ length: slideCount }, (_, index) => {
    if (index === 0) {
      return { index: 1, layout: opening, purpose: "opening" };
    }

    if (index === slideCount - 1) {
      return { index: slideCount, layout: ending, purpose: "closing" };
    }

    return {
      index: index + 1,
      layout: middlePool[(index - 1) % middlePool.length],
      purpose: "content",
    };
  });
}

const args = parseArgs(process.argv);
const recommendation = recommendTheme(args);

if (!recommendation) {
  console.error("could not scaffold deck");
  process.exit(1);
}

const slideCount = DEFAULT_DECK_LENGTH[args.density] ?? DEFAULT_DECK_LENGTH.medium;

const scaffold = {
  title: args.title,
  scene: args.scene,
  density: args.density,
  mobile: args.mobile,
  engine: recommendation.engine,
  theme: recommendation.themeName,
  tone: recommendation.tone,
  slideCount,
  layouts: recommendation.layouts,
  outline: buildOutline(recommendation.layouts, slideCount),
};

console.log(JSON.stringify(scaffold, null, 2));
