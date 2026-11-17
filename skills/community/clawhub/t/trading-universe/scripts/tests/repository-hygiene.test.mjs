import test from "node:test";
import assert from "node:assert/strict";
import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, extname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const testDir = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(testDir, "../..");
const repositoryRoot = resolve(skillRoot, "../..");
const textExtensions = new Set([
  ".cmd", ".js", ".json", ".md", ".mjs", ".ps1", ".txt", ".vbs", ".yaml", ".yml",
]);

function textFiles(root) {
  const files = [];
  for (const name of readdirSync(root)) {
    if (name === ".git" || name === "node_modules") continue;
    const path = join(root, name);
    if (statSync(path).isDirectory()) files.push(...textFiles(path));
    else if (textExtensions.has(extname(name).toLowerCase())) files.push(path);
  }
  return files;
}

test("public package contains no retired broker integration or stale build attribution", () => {
  const files = textFiles(skillRoot);
  const repositoryReadme = join(repositoryRoot, "README.md");
  if (existsSync(join(repositoryRoot, ".git")) && existsSync(repositoryReadme)) {
    files.push(repositoryReadme);
  }

  const retiredBroker = new RegExp(["oan", "da"].join(""), "i");
  const staleModel = new RegExp(["fable", "5"].join("\\s*"), "i");
  const staleAttribution = new RegExp(["engineered", "with", "anthropic"].join("\\s+"), "i");
  const violations = [];

  for (const path of files) {
    const content = readFileSync(path, "utf8");
    if (retiredBroker.test(content) || staleModel.test(content) || staleAttribution.test(content)) {
      violations.push(path.replace(repositoryRoot, "").replace(/^[/\\]+/, ""));
    }
  }

  assert.deepEqual(violations, []);
});
