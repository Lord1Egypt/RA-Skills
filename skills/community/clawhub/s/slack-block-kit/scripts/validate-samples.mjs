#!/usr/bin/env node

import { readdirSync, readFileSync } from "node:fs";
import { join } from "node:path";

const skillDir = new URL("..", import.meta.url).pathname.replace(/\/$/, "");
const samplesDir = join(skillDir, "samples");
const errors = [];

function walk(dir, out = []) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const filePath = join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(filePath, out);
    } else if (filePath.endsWith(".json")) {
      out.push(filePath);
    }
  }
  return out;
}

const urlFields = new Set([
  "url",
  "image_url",
  "video_url",
  "thumbnail_url",
  "title_url",
  "provider_icon_url",
]);

function rememberUnique(state, kind, id, filePath, path) {
  const seen = state[kind];
  if (seen.has(id)) {
    errors.push({ filePath, path, message: `duplicate ${kind.slice(0, -1)} "${id}"` });
  } else {
    seen.add(id);
  }
}

function visit(value, filePath, path = [], state = { blockIds: new Set(), actionIds: new Set() }) {
  if (Array.isArray(value)) {
    value.forEach((item, index) => visit(item, filePath, path.concat(index), state));
    return;
  }
  if (!value || typeof value !== "object") return;

  for (const [key, child] of Object.entries(value)) {
    if (urlFields.has(key) && typeof child === "string") {
      if (child.startsWith("<") || child.endsWith(">")) {
        errors.push({ filePath, path: path.concat(key), message: `${key} must be a plain URL string, not mrkdwn angle-bracket syntax` });
      }
      if (child.includes("&amp;")) {
        errors.push({ filePath, path: path.concat(key), message: `${key} contains HTML-encoded &amp;` });
      }
    }
  }

  if (typeof value.block_id === "string") {
    rememberUnique(state, "blockIds", value.block_id, filePath, path.concat("block_id"));
  }
  if (typeof value.action_id === "string") {
    rememberUnique(state, "actionIds", value.action_id, filePath, path.concat("action_id"));
  }

  if (value.type === "raw_text") {
    if (!Object.hasOwn(value, "text")) {
      errors.push({ filePath, path, message: "raw_text cell is missing text" });
    }
    if (value.text === "") {
      errors.push({ filePath, path, message: "raw_text text must be non-empty" });
    }
    if (Object.hasOwn(value, "elements")) {
      errors.push({ filePath, path, message: "raw_text cell must not use elements" });
    }
  }

  if (value.type === "rich_text" && !Array.isArray(value.elements)) {
    errors.push({ filePath, path, message: "rich_text block is missing elements[]" });
  }

  if ((value.type === "container" || value.type === "callout") && !Array.isArray(value.child_blocks)) {
    errors.push({ filePath, path, message: `${value.type} block is missing child_blocks[]` });
  }

  if (value.type === "image") {
    if (typeof value.image_url !== "string" || !value.image_url) {
      errors.push({ filePath, path, message: "image block is missing image_url" });
    }
    if (typeof value.alt_text !== "string" || !value.alt_text) {
      errors.push({ filePath, path, message: "image block is missing alt_text" });
    }
  }

  if (value.type === "data_visualization") {
    const chart = value.chart ?? {};
    if (!chart.type) {
      errors.push({ filePath, path, message: "data_visualization is missing chart.type" });
    } else if (chart.type === "pie") {
      if (!Array.isArray(chart.segments)) {
        errors.push({ filePath, path, message: "pie chart is missing segments[]" });
      } else {
        chart.segments.forEach((segment, index) => {
          if (typeof segment?.label !== "string") {
            errors.push({ filePath, path: path.concat("chart", "segments", index, "label"), message: "pie segment is missing label" });
          }
          if (typeof segment?.value !== "number") {
            errors.push({ filePath, path: path.concat("chart", "segments", index, "value"), message: "pie segment value must be a number" });
          }
        });
      }
    } else if (!Array.isArray(chart.series)) {
      errors.push({ filePath, path, message: `${chart.type} chart is missing series[]` });
    } else {
      chart.series.forEach((series, seriesIndex) => {
        if (typeof series?.name !== "string") {
          errors.push({ filePath, path: path.concat("chart", "series", seriesIndex, "name"), message: `${chart.type} series is missing name` });
        }
        if (!Array.isArray(series?.data)) {
          errors.push({ filePath, path: path.concat("chart", "series", seriesIndex, "data"), message: `${chart.type} series is missing data[]` });
        } else {
          series.data.forEach((point, pointIndex) => {
            if (typeof point?.label !== "string") {
              errors.push({ filePath, path: path.concat("chart", "series", seriesIndex, "data", pointIndex, "label"), message: `${chart.type} data point is missing label` });
            }
            if (typeof point?.value !== "number") {
              errors.push({ filePath, path: path.concat("chart", "series", seriesIndex, "data", pointIndex, "value"), message: `${chart.type} data point value must be a number` });
            }
          });
        }
      });
    }
  }

  if (value.type === "table" || value.type === "data_table") {
    if (!Array.isArray(value.rows)) {
      errors.push({ filePath, path, message: `${value.type} block is missing rows[]` });
    } else {
      if (value.rows.length > 100) {
        errors.push({ filePath, path, message: `${value.type} block exceeds 100 rows` });
      }
      const expectedCols = Array.isArray(value.rows[0]) ? value.rows[0].length : undefined;
      if (expectedCols !== undefined && expectedCols > 20) {
        errors.push({ filePath, path, message: `${value.type} block exceeds 20 columns` });
      }
      value.rows.forEach((row, index) => {
        if (!Array.isArray(row)) {
          errors.push({ filePath, path: path.concat("rows", index), message: `${value.type} row must be an array` });
        } else if (expectedCols !== undefined && row.length !== expectedCols) {
          errors.push({ filePath, path: path.concat("rows", index), message: `${value.type} row has ${row.length} columns; expected ${expectedCols}` });
        }
      });
    }
  }

  for (const [key, child] of Object.entries(value)) {
    visit(child, filePath, path.concat(key), state);
  }
}

for (const filePath of walk(samplesDir)) {
  try {
    visit(JSON.parse(readFileSync(filePath, "utf8")), filePath, [], { blockIds: new Set(), actionIds: new Set() });
  } catch (error) {
    errors.push({ filePath, path: [], message: error.message });
  }
}

if (errors.length > 0) {
  console.error(JSON.stringify({ ok: false, errors }, null, 2));
  process.exit(1);
}

console.log(JSON.stringify({ ok: true, checked: walk(samplesDir).length }, null, 2));
