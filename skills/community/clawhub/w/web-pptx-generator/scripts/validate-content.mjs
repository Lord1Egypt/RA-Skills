#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { validateDeckContent } from "./content-utils.mjs";

const input = process.argv[2];

if (!input) {
  console.error("Usage: node scripts/validate-content.mjs <path/to/deck.json>");
  process.exit(1);
}

const filePath = path.resolve(process.cwd(), input);
const raw = fs.readFileSync(filePath, "utf8");
const content = JSON.parse(raw);
const errors = validateDeckContent(content);

if (errors.length) {
  console.error(JSON.stringify({ ok: false, errors }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({ ok: true, file: filePath, slides: content.slides?.length ?? 0 }, null, 2));
