#!/usr/bin/env node

import { buildReplyBundle, recommendStyle } from "./style-bundles.mjs";

function parseArgs(argv) {
  const args = {
    scene: "",
    goal: "",
    relationship: "",
    intensity: "",
    channel: "wechat",
    persona: "",
    mode: "",
  };
  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--scene") args.scene = argv[i + 1] ?? "";
    if (part === "--goal") args.goal = argv[i + 1] ?? "";
    if (part === "--relationship") args.relationship = argv[i + 1] ?? "";
    if (part === "--intensity") args.intensity = argv[i + 1] ?? "";
    if (part === "--channel") args.channel = argv[i + 1] ?? "wechat";
    if (part === "--persona") args.persona = argv[i + 1] ?? "";
    if (part === "--mode") args.mode = argv[i + 1] ?? "";
  }
  return args;
}

const args = parseArgs(process.argv);
const styleName = recommendStyle(args);
const bundle = buildReplyBundle({ ...args, style: styleName });

console.log(JSON.stringify({
  scene: args.scene,
  goal: args.goal,
  relationship: args.relationship,
  recommendedStyle: styleName,
  summary: bundle.styleCn,
  intensity: bundle.intensity,
  channel: bundle.channel,
  persona: bundle.persona,
  personaSummary: bundle.personaCn,
  mode: bundle.mode,
  modeSummary: bundle.modeCn,
  signature: bundle.compositeSignature,
  opening: bundle.opening,
  body: bundle.body,
  closing: bundle.closing,
}, null, 2));
