import fs from "node:fs";
import path from "node:path";

export const ensureDir = (dirPath) => fs.mkdirSync(dirPath, { recursive: true });

export const writeJSON = (filepath, data, log = null) => {
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2));
  if (typeof log === "function") log(`  -> Wrote ${filepath}`);
};

export const writeJSONMin = (filepath, data, log = null) => {
  fs.writeFileSync(filepath, JSON.stringify(data));
  if (typeof log === "function") log(`  -> Wrote ${filepath}`);
};

export const writeText = (filepath, content, log = null) => {
  fs.writeFileSync(filepath, content, "utf-8");
  if (typeof log === "function") log(`  -> Wrote ${filepath}`);
};

export const sanitizeFileName = (input = "") => String(input)
  .normalize("NFKD")
  .replace(/[\u0300-\u036f]/g, "")
  .replace(/[^a-zA-Z0-9@._-]+/g, "_")
  .replace(/_{2,}/g, "_")
  .replace(/^_+|_+$/g, "")
  || "asset";

export const toPosixPath = (filePath) => filePath.split(path.sep).join("/");
