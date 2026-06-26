#!/usr/bin/env node
/**
 * wine-export.js — Export the wine archive DB to a portable JSON file.
 *
 * Usage:
 *   node scripts/wine-export.js [--out export.json] [--include-images]
 *
 * Options:
 *   --out <path>       Output file path (default: wine-export-<date>.json)
 *   --include-images   Base64-encode label images into the export file
 *
 * Output format:
 *   {
 *     exported_at: ISO timestamp,
 *     version: 1,
 *     wines: [...],           // wine identity records
 *     wine_instances: [...],  // tasting/purchase instances
 *     images: {               // only when --include-images is set
 *       "<original path>": { data: "<base64>", ext: ".jpg" }
 *     }
 *   }
 */

'use strict';

const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

const WORKSPACE = path.resolve(__dirname, '..');
const DATA_DIR = path.join(WORKSPACE, 'data', 'wine');
const DEFAULT_DB_PATH = path.join(DATA_DIR, 'wine.sqlite3');
const DB_PATH = process.env.WINE_DB_PATH ? path.resolve(process.env.WINE_DB_PATH) : DEFAULT_DB_PATH;

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (token.startsWith('--')) {
      const key = token.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) {
        args[key] = true;
      } else {
        args[key] = next;
        i += 1;
      }
    }
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const includeImages = Boolean(args['include-images']);
  const dateStamp = new Date().toISOString().slice(0, 10);
  const outPath = path.resolve(args.out || `wine-export-${dateStamp}.json`);

  if (!fs.existsSync(DB_PATH)) {
    process.stderr.write(`Error: DB not found at ${DB_PATH}\n`);
    process.exitCode = 1;
    return;
  }

  const db = new Database(DB_PATH, { readonly: true });
  db.pragma('journal_mode = WAL');

  const wines = db.prepare('SELECT * FROM wines ORDER BY id').all();
  const instances = db.prepare('SELECT * FROM wine_instances ORDER BY id').all();

  const images = {};
  if (includeImages) {
    const imagePaths = new Set();
    for (const w of wines) {
      if (w.default_source_image_path) imagePaths.add(w.default_source_image_path);
    }
    for (const inst of instances) {
      if (inst.source_image_path) imagePaths.add(inst.source_image_path);
    }
    for (const imgPath of imagePaths) {
      if (fs.existsSync(imgPath)) {
        const data = fs.readFileSync(imgPath);
        images[imgPath] = {
          data: data.toString('base64'),
          ext: path.extname(imgPath).toLowerCase() || '.jpg',
        };
      }
    }
  }

  const payload = {
    exported_at: new Date().toISOString(),
    version: 1,
    db_path: DB_PATH,
    wines,
    wine_instances: instances,
    ...(includeImages ? { images } : {}),
  };

  fs.writeFileSync(outPath, JSON.stringify(payload, null, 2), 'utf8');

  const imageSummary = includeImages ? `, ${Object.keys(images).length} images embedded` : '';
  process.stdout.write(
    JSON.stringify({
      status: 'ok',
      out: outPath,
      wines: wines.length,
      instances: instances.length,
      note: `Export written to ${outPath}${imageSummary}. Transfer this file (and data/wine/labels/ if not using --include-images) to the target machine.`,
    }, null, 2) + '\n'
  );

  db.close();
}

main();
