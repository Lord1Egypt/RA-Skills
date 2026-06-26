#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const LAYOUT_ALIASES = new Map([
  ["cover", "cover"],
  ["封面", "cover"],
  ["agenda", "agenda"],
  ["目录", "agenda"],
  ["section", "section-break"],
  ["section-break", "section-break"],
  ["章节", "section-break"],
  ["insight", "insight"],
  ["观点", "insight"],
  ["two-column", "two-column"],
  ["双栏", "two-column"],
  ["metrics", "metrics"],
  ["指标", "metrics"],
  ["chart", "chart-focus"],
  ["chart-focus", "chart-focus"],
  ["图表", "chart-focus"],
  ["timeline", "timeline"],
  ["时间线", "timeline"],
  ["comparison", "comparison"],
  ["对比", "comparison"],
  ["quote", "quote"],
  ["引用", "quote"],
  ["closing", "closing"],
  ["结尾", "closing"],
]);

function parseArgs(argv) {
  const args = {
    input: "",
    output: "",
    scene: "",
    density: "medium",
    mobile: false,
    title: "",
    subtitle: "",
  };

  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--input") args.input = argv[i + 1] ?? args.input;
    if (part === "--output") args.output = argv[i + 1] ?? args.output;
    if (part === "--scene") args.scene = argv[i + 1] ?? args.scene;
    if (part === "--density") args.density = argv[i + 1] ?? args.density;
    if (part === "--mobile") args.mobile = true;
    if (part === "--title") args.title = argv[i + 1] ?? args.title;
    if (part === "--subtitle") args.subtitle = argv[i + 1] ?? args.subtitle;
  }

  if (!args.input) {
    console.error("Usage: node scripts/markdown-to-content.mjs --input outline.md [--output deck.json]");
    process.exit(1);
  }

  return args;
}

function normalizeLayout(raw) {
  if (!raw) return "insight";
  return LAYOUT_ALIASES.get(raw.trim().toLowerCase()) ?? "insight";
}

function cleanText(line) {
  return line.replace(/^\s*[-*]\s*/, "").trim();
}

function parseKeyValue(line) {
  const match = line.match(/^([A-Za-z\u4e00-\u9fa5][^:：]{0,20})[:：]\s*(.+)$/);
  if (!match) return null;
  return { key: match[1].trim().toLowerCase(), value: match[2].trim() };
}

function parseMetricItems(lines) {
  return lines
    .map(cleanText)
    .map((line) => line.match(/^(.+?)[:：]\s*(.+)$/))
    .filter(Boolean)
    .map(([, label, value]) => ({ value: value.trim(), label: label.trim() }));
}

function parseChartItems(lines) {
  return lines
    .map(cleanText)
    .map((line) => line.match(/^(.+?)[:：]\s*(\d+(?:\.\d+)?)$/))
    .filter(Boolean)
    .map(([, label, value]) => ({ label: label.trim(), value: Number(value) }));
}

function parseSection(heading, bodyLines) {
  const rawTitle = heading.replace(/^##\s*/, "").trim();
  const [, maybeLayout, maybeTitle] = rawTitle.match(/^([^:：]+)[:：]?\s*(.*)$/) ?? [];
  const layout = normalizeLayout(maybeLayout);
  const title = maybeTitle || rawTitle;
  const textLines = bodyLines.filter((line) => line.trim().length > 0);
  const bulletLines = textLines.filter((line) => /^\s*[-*]\s+/.test(line));
  const blockQuotes = textLines.filter((line) => /^\s*>\s*/.test(line)).map((line) => line.replace(/^\s*>\s*/, "").trim());
  const subheads = [];
  let currentSubhead = null;

  for (const line of textLines) {
    if (/^###\s+/.test(line)) {
      currentSubhead = { title: line.replace(/^###\s+/, "").trim(), bullets: [] };
      subheads.push(currentSubhead);
      continue;
    }
    if (currentSubhead && /^\s*[-*]\s+/.test(line)) {
      currentSubhead.bullets.push(cleanText(line));
    }
  }

  const kv = new Map();
  for (const line of textLines) {
    const pair = parseKeyValue(line);
    if (pair) kv.set(pair.key, pair.value);
  }

  if (layout === "cover") {
    return {
      layout,
      eyebrow: kv.get("eyebrow") ?? kv.get("眉标") ?? "",
      title: kv.get("title") ?? kv.get("标题") ?? title,
      subtitle: kv.get("subtitle") ?? kv.get("副标题") ?? textLines.find((line) => !line.startsWith("Eyebrow")) ?? "",
    };
  }

  if (layout === "agenda") {
    return { layout, title, points: bulletLines.map(cleanText) };
  }

  if (layout === "section-break") {
    return { layout, title, subtitle: kv.get("subtitle") ?? kv.get("副标题") ?? textLines.find((line) => !/^###|^\s*[-*]\s+/.test(line)) ?? "" };
  }

  if (layout === "insight") {
    return {
      layout,
      title,
      points: bulletLines.map(cleanText),
      stat: kv.get("stat") ?? kv.get("数字") ?? "",
      statLabel: kv.get("statlabel") ?? kv.get("数字说明") ?? "",
    };
  }

  if (layout === "two-column") {
    return {
      layout,
      title,
      leftTitle: subheads[0]?.title ?? "Left",
      leftPoints: subheads[0]?.bullets ?? [],
      rightTitle: subheads[1]?.title ?? "Right",
      rightPoints: subheads[1]?.bullets ?? [],
    };
  }

  if (layout === "metrics") {
    return { layout, title, metrics: parseMetricItems(bulletLines) };
  }

  if (layout === "chart-focus") {
    return {
      layout,
      title,
      chartBars: parseChartItems(bulletLines),
      conclusion: kv.get("conclusion") ?? kv.get("结论") ?? textLines.find((line) => !/^\s*[-*]\s+/.test(line)) ?? "",
    };
  }

  if (layout === "timeline") {
    return { layout, title, steps: bulletLines.map(cleanText) };
  }

  if (layout === "comparison") {
    return {
      layout,
      title,
      leftTitle: subheads[0]?.title ?? "Option A",
      leftPoints: subheads[0]?.bullets ?? [],
      rightTitle: subheads[1]?.title ?? "Option B",
      rightPoints: subheads[1]?.bullets ?? [],
    };
  }

  if (layout === "quote") {
    return {
      layout,
      title: blockQuotes[0] ?? title,
      subtitle: kv.get("author") ?? kv.get("署名") ?? kv.get("subtitle") ?? "",
    };
  }

  if (layout === "closing") {
    return { layout, title: kv.get("title") ?? kv.get("标题") ?? title, subtitle: kv.get("subtitle") ?? kv.get("副标题") ?? "" };
  }

  return {
    layout: "insight",
    title,
    points: bulletLines.map(cleanText),
  };
}

function parseMarkdown(markdown, args) {
  const lines = markdown.split(/\r?\n/);
  const sections = [];
  let title = args.title;
  let subtitle = args.subtitle;
  let currentHeading = null;
  let currentBody = [];

  for (const line of lines) {
    if (/^#\s+/.test(line) && !title) {
      title = line.replace(/^#\s+/, "").trim();
      continue;
    }
    if (!subtitle && /^>\s+/.test(line) && !currentHeading) {
      subtitle = line.replace(/^>\s+/, "").trim();
      continue;
    }
    if (/^##\s+/.test(line)) {
      if (currentHeading) {
        sections.push(parseSection(currentHeading, currentBody));
      }
      currentHeading = line;
      currentBody = [];
      continue;
    }
    if (currentHeading) currentBody.push(line);
  }

  if (currentHeading) {
    sections.push(parseSection(currentHeading, currentBody));
  }

  if (!sections.length || sections[0].layout !== "cover") {
    sections.unshift({
      layout: "cover",
      eyebrow: args.scene || "web-slides",
      title: title || "Untitled Deck",
      subtitle: subtitle || "",
    });
  }

  return {
    title: title || sections[0].title || "Untitled Deck",
    subtitle: subtitle || "",
    scene: args.scene,
    density: args.density,
    mobile: args.mobile,
    slides: sections,
  };
}

const args = parseArgs(process.argv);
const inputPath = path.resolve(process.cwd(), args.input);
const outputPath = path.resolve(process.cwd(), args.output || inputPath.replace(/\.md$/i, ".json"));
const markdown = fs.readFileSync(inputPath, "utf8");
const content = parseMarkdown(markdown, args);

fs.mkdirSync(path.dirname(outputPath), { recursive: true });
fs.writeFileSync(outputPath, JSON.stringify(content, null, 2), "utf8");

console.log(JSON.stringify({
  input: inputPath,
  output: outputPath,
  slides: content.slides.length,
  title: content.title,
}, null, 2));
