import crypto from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "./args.mjs";
import { ensureDirs, pendingPath, sourcesDir } from "./config.mjs";
import { extractArticle } from "./extract.mjs";
import { loadState, saveState, updateItem } from "./state.mjs";

function stableId(seed) {
  return crypto.createHash("sha1").update(seed).digest("hex").slice(0, 14);
}

function readPending() {
  if (!fs.existsSync(pendingPath)) return { generatedAt: new Date().toISOString(), items: [] };
  try {
    const parsed = JSON.parse(fs.readFileSync(pendingPath, "utf8"));
    return {
      generatedAt: parsed.generatedAt || new Date().toISOString(),
      items: Array.isArray(parsed.items) ? parsed.items : []
    };
  } catch {
    return { generatedAt: new Date().toISOString(), items: [] };
  }
}

function readTextInput(args) {
  if (args.file) return fs.readFileSync(path.resolve(args.file), "utf8");
  return args.text || "";
}

const args = parseArgs();
const mode = args.mode || (args.url ? "rewrite" : "original");
const title = args.title || args.url || "手动选题";
const text = readTextInput(args);
const seed = args.id || args.url || `${title}\n${text}`;
const sourceId = args.id || `manual_${stableId(seed)}`;

ensureDirs();

const base = {
  sourceId,
  url: args.url || "",
  title,
  sourceName: args["source-name"] || "manual",
  mode,
  userIntent: args.intent || "",
  collectedAt: new Date().toISOString()
};

const extracted = args.url
  ? await extractArticle(base)
  : {
      extractionStatus: "manual-input",
      extractedTitle: title,
      extractedExcerpt: args.summary || "",
      extractedText: text
    };

const sourcePayload = {
  ...base,
  ...extracted
};

const sourcePath = path.join(sourcesDir, `${sourceId}.json`);
fs.writeFileSync(sourcePath, `${JSON.stringify(sourcePayload, null, 2)}\n`);

const state = loadState();
updateItem(state, sourceId, {
  url: base.url,
  title: base.title,
  sourceName: base.sourceName,
  mode,
  status: state.items[sourceId]?.status || "collected",
  sourcePath
});
state.runs.push({
  type: "add-source",
  at: new Date().toISOString(),
  sourceId,
  mode
});
saveState(state);

const pending = readPending();
const pendingItem = {
  sourceId,
  title: base.title,
  url: base.url,
  sourceName: base.sourceName,
  mode,
  sourcePath,
  extractionStatus: extracted.extractionStatus
};
pending.items = pending.items.filter((item) => item.sourceId !== sourceId).concat(pendingItem);
pending.generatedAt = new Date().toISOString();
fs.writeFileSync(pendingPath, `${JSON.stringify(pending, null, 2)}\n`);

console.log(JSON.stringify({
  ok: true,
  sourceId,
  mode,
  sourcePath,
  pendingPath
}, null, 2));
