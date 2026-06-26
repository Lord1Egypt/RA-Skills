import fs from "node:fs";
import path from "node:path";

const IGNORED_DIRS = new Set([
  ".git",
  "node_modules",
  "dist",
  "build",
  "coverage",
  ".next",
  ".nuxt",
  "out",
  "target",
  "venv",
  ".venv",
  "__pycache__",
]);

const GUILLOTINE_MARKERS = [
  "guillotine",
  "queryDsl",
  "queryDslConnection",
  "queryConnection",
  "HeadlessCms",
  "X-Guillotine-SiteKey",
  "getChildren",
  "getChildrenConnection",
  "/lib/guillotine",
  "guillotineLib",
];

const SCAN_EXTENSIONS = new Set([
  ".ts",
  ".tsx",
  ".js",
  ".jsx",
  ".mjs",
  ".graphql",
  ".gql",
  ".vue",
  ".svelte",
  ".xml",
  ".es6",
]);

function toPosixRelative(root, targetPath) {
  return path.relative(root, targetPath).split(path.sep).join("/");
}

function readDirEntries(directoryPath) {
  try {
    return fs.readdirSync(directoryPath, { withFileTypes: true });
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    process.stderr.write(`Warning: Skipping unreadable directory ${directoryPath}: ${message}\n`);
    return [];
  }
}

function walkFiles(root) {
  const files = [];
  const pending = [root];

  while (pending.length > 0) {
    const current = pending.pop();
    for (const entry of readDirEntries(current)) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        if (!IGNORED_DIRS.has(entry.name)) {
          pending.push(fullPath);
        }
      } else if (entry.isFile()) {
        const ext = path.extname(entry.name).toLowerCase();
        if (SCAN_EXTENSIONS.has(ext)) {
          files.push(fullPath);
        }
      }
    }
  }

  return files;
}

function scanForMarkers(filePath) {
  let content;
  try {
    content = fs.readFileSync(filePath, "utf-8");
  } catch {
    return [];
  }

  const found = [];
  for (const marker of GUILLOTINE_MARKERS) {
    if (content.includes(marker)) {
      found.push(marker);
    }
  }
  return found;
}

function main() {
  const rootArg = process.argv[2];
  if (!rootArg) {
    process.stderr.write("Usage: node find-guillotine-targets.mjs <root-directory>\n");
    process.exit(1);
  }

  const root = path.resolve(rootArg);
  if (!fs.existsSync(root)) {
    process.stderr.write(`Error: Directory not found: ${root}\n`);
    process.exit(1);
  }

  const files = walkFiles(root);
  const results = [];

  for (const filePath of files) {
    const markers = scanForMarkers(filePath);
    if (markers.length > 0) {
      results.push({
        file: toPosixRelative(root, filePath),
        markers,
      });
    }
  }

  if (results.length === 0) {
    console.log("No Guillotine usage markers found in the workspace.");
  } else {
    console.log(`Found ${results.length} file(s) with Guillotine markers:\n`);
    for (const result of results) {
      console.log(`  ${result.file}`);
      console.log(`    markers: ${result.markers.join(", ")}`);
    }
  }
}

main();
