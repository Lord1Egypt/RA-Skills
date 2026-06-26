import fs from "node:fs";
import { generatedDir, pendingPath } from "./config.mjs";
import { loadState } from "./state.mjs";

const state = loadState();
const counts = {};
for (const item of Object.values(state.items)) {
  const status = item.status || "unknown";
  counts[status] = (counts[status] || 0) + 1;
}

const pending = fs.existsSync(pendingPath)
  ? JSON.parse(fs.readFileSync(pendingPath, "utf8")).items?.length || 0
  : 0;

const generated = fs.existsSync(generatedDir)
  ? fs.readdirSync(generatedDir).filter((name) => name.endsWith(".json")).length
  : 0;

console.log(JSON.stringify({
  counts,
  pending,
  generated,
  recentRuns: state.runs.slice(-5)
}, null, 2));
