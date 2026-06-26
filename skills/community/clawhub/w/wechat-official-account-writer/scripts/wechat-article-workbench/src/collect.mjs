import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "./args.mjs";
import { config, ensureDirs, pendingPath, sourcesDir } from "./config.mjs";
import { fetchAihotFeaturedItems } from "./source-aihot.mjs";
import { extractArticle } from "./extract.mjs";
import { loadState, saveState, updateItem } from "./state.mjs";

const args = parseArgs();
const limit = Number.parseInt(args.limit || config.curatedAihotLimit || "3", 10);
const minScore = args["min-score"] ? Number.parseInt(args["min-score"], 10) : 0;

ensureDirs();

const state = loadState();
const featured = await fetchAihotFeaturedItems(config.curatedAihotUrl);
const candidates = featured
  .filter((item) => item.score === null || item.score >= minScore)
  .filter((item) => state.items[item.sourceId]?.status !== "drafted")
  .slice(0, limit);

const pending = [];

for (const item of candidates) {
  const extracted = await extractArticle(item);
  const sourcePayload = {
    ...item,
    ...extracted
  };

  const sourcePath = path.join(sourcesDir, `${item.sourceId}.json`);
  fs.writeFileSync(sourcePath, `${JSON.stringify(sourcePayload, null, 2)}\n`);

  updateItem(state, item.sourceId, {
    url: item.url,
    title: item.title,
    sourceName: item.sourceName,
    status: state.items[item.sourceId]?.status || "collected",
    sourcePath
  });

  pending.push({
    sourceId: item.sourceId,
    title: item.title,
    url: item.url,
    sourceName: item.sourceName,
    score: item.score,
    sourcePath,
    extractionStatus: extracted.extractionStatus
  });
}

state.runs.push({
  type: "collect:aihot",
  at: new Date().toISOString(),
  totalFeatured: featured.length,
  pending: pending.length
});
saveState(state);

fs.writeFileSync(pendingPath, `${JSON.stringify({ generatedAt: new Date().toISOString(), items: pending }, null, 2)}\n`);

console.log(JSON.stringify({
  ok: true,
  totalFeatured: featured.length,
  pending: pending.length,
  pendingPath
}, null, 2));
