#!/usr/bin/env node

/**
 * fetch-onnx-model.js
 *
 * One-shot bootstrap that downloads the quantized ONNX bundle for
 * Xenova/all-MiniLM-L6-v2 into data/models/all-MiniLM-L6-v2/. Wires
 * into update-registry.yml so registry.db and the JS runtime model
 * ship in the same commit.
 *
 * Idempotent: if the model dir already exists with files, exits 0
 * without re-fetching. The CI cache key on data/models keeps this a
 * no-op on most runs.
 *
 * Why bundle: @xenova/transformers lazy-downloads from HuggingFace on
 * first call by default. Bundling makes the npm package work offline
 * and on zero-egress hosts (some MCP runners) — and removes a
 * first-call latency tax on agents.
 */

import { existsSync, mkdirSync, readdirSync } from "fs";
import { join, dirname } from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const REPO_ROOT = join(__dirname, "..");
const TARGET_DIR = join(REPO_ROOT, "data", "models");
const MODEL_NAME = "Xenova/all-MiniLM-L6-v2";

// Skip if already cached. Look for the onnx subdir which is the
// load-time required path.
const localDir = join(TARGET_DIR, "all-MiniLM-L6-v2");
if (existsSync(localDir) && readdirSync(localDir).length > 0) {
  console.log(`model already cached at ${localDir} — skipping download`);
  process.exit(0);
}

mkdirSync(TARGET_DIR, { recursive: true });

const { pipeline, env } = await import("@xenova/transformers");
env.cacheDir = TARGET_DIR;
env.localModelPath = TARGET_DIR;
// Allow remote on this one-shot — we're fetching INTO the local cache.
env.allowRemoteModels = true;

console.log(`fetching ${MODEL_NAME} into ${TARGET_DIR}...`);
const t0 = Date.now();
await pipeline("feature-extraction", MODEL_NAME, { quantized: true });
console.log(`done in ${((Date.now() - t0) / 1000).toFixed(1)}s`);
