import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { listFilesRecursive } from "./files.mjs";

async function fingerprints(directory) {
  const result = new Map();
  for (const file of await listFilesRecursive(directory)) {
    const content = await readFile(file.absolute);
    result.set(file.relative, createHash("sha256").update(content).digest("hex"));
  }
  return result;
}

export async function diffPackages(beforeDirectory, afterDirectory) {
  const before = await fingerprints(beforeDirectory);
  const after = await fingerprints(afterDirectory);
  const names = [...new Set([...before.keys(), ...after.keys()])].sort();
  const added = [];
  const removed = [];
  const changed = [];
  const unchanged = [];
  for (const name of names) {
    if (!before.has(name)) added.push(name);
    else if (!after.has(name)) removed.push(name);
    else if (before.get(name) !== after.get(name)) changed.push(name);
    else unchanged.push(name);
  }
  return { added, removed, changed, unchanged };
}

export function formatPackageDiff(result) {
  return [
    "# AI Soul Package Diff",
    "",
    `- Added: ${result.added.length}`,
    `- Removed: ${result.removed.length}`,
    `- Changed: ${result.changed.length}`,
    `- Unchanged: ${result.unchanged.length}`,
    "",
    "## Added",
    ...(result.added.length ? result.added.map((item) => `- ${item}`) : ["- None"]),
    "",
    "## Removed",
    ...(result.removed.length ? result.removed.map((item) => `- ${item}`) : ["- None"]),
    "",
    "## Changed",
    ...(result.changed.length ? result.changed.map((item) => `- ${item}`) : ["- None"]),
    "",
  ].join("\n");
}
