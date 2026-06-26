#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { validateDeckContent } from "./content-utils.mjs";

function parseArgs(argv) {
  const args = { content: "", html: "" };
  for (let i = 2; i < argv.length; i += 1) {
    const part = argv[i];
    if (part === "--content") args.content = argv[i + 1] ?? "";
    if (part === "--html") args.html = argv[i + 1] ?? "";
  }
  if (!args.content && !args.html) {
    console.error("Usage: node scripts/qa-deck.mjs [--content deck.json] [--html deck.html]");
    process.exit(1);
  }
  return args;
}

function measureTitleLength(title = "") {
  return Array.from(title).length;
}

function qaContent(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  const content = JSON.parse(raw);
  const errors = validateDeckContent(content);
  const warnings = [];
  const slides = content.slides ?? [];

  if (slides.length < 6) warnings.push("deck has fewer than 6 slides");
  if (slides.length > 24) warnings.push("deck has more than 24 slides");
  if (!slides.some((slide) => slide.layout === "cover")) warnings.push("deck has no cover slide");
  if (!slides.some((slide) => slide.layout === "closing")) warnings.push("deck has no closing slide");

  slides.forEach((slide, index) => {
    if (slide.title && measureTitleLength(slide.title) > 36) {
      warnings.push(`slides[${index}].title is long (${measureTitleLength(slide.title)} chars)`);
    }
    if (Array.isArray(slide.points) && slide.points.length > 5) {
      warnings.push(`slides[${index}] has more than 5 bullet points`);
    }
    if (Array.isArray(slide.leftPoints) && slide.leftPoints.length > 4) {
      warnings.push(`slides[${index}].leftPoints has more than 4 items`);
    }
    if (Array.isArray(slide.rightPoints) && slide.rightPoints.length > 4) {
      warnings.push(`slides[${index}].rightPoints has more than 4 items`);
    }
  });

  return { errors, warnings, slides: slides.length };
}

function qaHtml(filePath) {
  const html = fs.readFileSync(filePath, "utf8");
  const warnings = [];
  const errors = [];

  if (!html.includes('meta name="viewport"')) errors.push("missing viewport meta tag");
  if (!html.includes("@media (max-width: 900px)")) warnings.push("missing mobile media query");
  if (!html.includes("touchstart") || !html.includes("touchend")) warnings.push("missing swipe navigation handlers");
  if (!html.includes("ArrowRight") || !html.includes("ArrowLeft")) warnings.push("missing keyboard navigation handlers");
  if (!html.includes("--primary") || !html.includes("--panel")) warnings.push("missing theme CSS variables");
  if (!html.includes('class="progress"')) warnings.push("missing progress bar");

  return { errors, warnings };
}

const args = parseArgs(process.argv);
const result = { ok: true, content: null, html: null };

if (args.content) {
  result.content = qaContent(path.resolve(process.cwd(), args.content));
  if (result.content.errors.length) result.ok = false;
}

if (args.html) {
  result.html = qaHtml(path.resolve(process.cwd(), args.html));
  if (result.html.errors.length) result.ok = false;
}

console.log(JSON.stringify(result, null, 2));
process.exit(result.ok ? 0 : 1);
