import fs from "node:fs";
import path from "node:path";
import { parseArgs } from "./args.mjs";
import { generatedDir } from "./config.mjs";
import { validateGeneratedArticle } from "./generated-schema.mjs";

function readArticle(filePath) {
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

const args = parseArgs();
const files = args.all
  ? fs.readdirSync(generatedDir).filter((name) => name.endsWith(".json")).map((name) => path.join(generatedDir, name))
  : (args._ || []).map((file) => path.resolve(file));

if (!files.length) {
  console.log("No generated files to validate.");
  process.exit(0);
}

let failed = 0;
for (const file of files) {
  const article = readArticle(file);
  const errors = validateGeneratedArticle(article);
  if (errors.length) {
    failed += 1;
    console.error(`${file}:`);
    for (const error of errors) console.error(`  - ${error}`);
  } else {
    console.log(`${file}: ok`);
  }
}

if (failed) process.exit(1);
