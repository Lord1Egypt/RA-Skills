"use strict";

const fs = require("fs");

function loadBatchItems(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`File not found: ${filePath}`);
  }
  let items;
  try {
    const content = fs.readFileSync(filePath, "utf-8");
    items = JSON.parse(content);
  } catch {
    throw new Error("Failed to parse batch file as JSON.");
  }
  if (!Array.isArray(items)) {
    throw new Error("Batch file must contain a JSON array.");
  }
  return items;
}

module.exports = {
  loadBatchItems
};
