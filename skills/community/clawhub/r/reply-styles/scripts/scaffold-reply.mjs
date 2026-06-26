#!/usr/bin/env node

import { buildReplyBundle, recommendStyle } from "./style-bundles.mjs";

function parseArgs(argv) {
  const args = {
    style: "",
    scene: "",
    goal: "",
    intent: "",
    intensity: "",
    channel: "wechat",
    persona: "",
    mode: "",
  };
  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--style") args.style = argv[i + 1] ?? "";
    if (part === "--scene") args.scene = argv[i + 1] ?? "";
    if (part === "--goal") args.goal = argv[i + 1] ?? "";
    if (part === "--intent") args.intent = argv[i + 1] ?? "";
    if (part === "--intensity") args.intensity = argv[i + 1] ?? "";
    if (part === "--channel") args.channel = argv[i + 1] ?? "wechat";
    if (part === "--persona") args.persona = argv[i + 1] ?? "";
    if (part === "--mode") args.mode = argv[i + 1] ?? "";
  }
  return args;
}

const args = parseArgs(process.argv);
const styleName = args.style || recommendStyle(args);
const bundle = buildReplyBundle({ ...args, style: styleName });

if (!bundle) {
  console.error(`unknown style: ${styleName}`);
  process.exit(1);
}

console.log(JSON.stringify({
  style: styleName,
  cn: bundle.styleCn,
  intensity: bundle.intensity,
  channel: bundle.channel,
  persona: bundle.persona,
  personaCn: bundle.personaCn,
  mode: bundle.mode,
  modeCn: bundle.modeCn,
  signature: bundle.compositeSignature,
  outline: [
    `Opening: ${bundle.opening}`,
    `Body: ${bundle.body}`,
    `Closing: ${bundle.closing}`,
  ],
  modeStructure: bundle.modeStructure,
  personaBias: bundle.personaBias,
  channelRules: bundle.channelRules,
  intensityRules: bundle.intensityRules,
  do: bundle.do,
  avoid: bundle.avoid,
  intent: args.intent || "",
}, null, 2));
