#!/usr/bin/env node
/**
 * wine-import.js — Import a wine-export.json into the wine archive DB.
 *
 * Usage:
 *   node scripts/wine-import.js --in export.json [--labels-dir data/wine/labels] [--dry-run]
 *
 * Options:
 *   --in <path>         Path to the export JSON file (required)
 *   --labels-dir <dir>  Directory to restore label images into
 *                       (default: data/wine/labels next to the DB)
 *   --dry-run           Parse and validate without writing anything
 *
 * Behaviour:
 *   - Wines are matched by (producer, wine_name, region, country, style, color, varietal).
 *     Matched wines are updated; unmatched wines are inserted.
 *   - Wine instances are always inserted as new records (preserving history).
 *   - If the export includes embedded images (--include-images was used on export),
 *     they are written to --labels-dir and instance/wine paths are remapped.
 *   - If the export does not include embedded images, you should manually copy
 *     data/wine/labels/ from the source machine before running this import.
 */

'use strict';

const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

const WORKSPACE = path.resolve(__dirname, '..');
const DATA_DIR = path.join(WORKSPACE, 'data', 'wine');
const DEFAULT_DB_PATH = path.join(DATA_DIR, 'wine.sqlite3');
const DB_PATH = process.env.WINE_DB_PATH ? path.resolve(process.env.WINE_DB_PATH) : DEFAULT_DB_PATH;
const DEFAULT_LABELS_DIR = path.join(DATA_DIR, 'labels');

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

function resolveWineId(db, wine) {
  const existing = db.prepare(`
    SELECT id FROM wines
    WHERE COALESCE(producer,'') = COALESCE(?,'')
      AND COALESCE(wine_name,'') = COALESCE(?,'')
      AND COALESCE(region,'') = COALESCE(?,'')
      AND COALESCE(country,'') = COALESCE(?,'')
      AND COALESCE(style,'') = COALESCE(?,'')
      AND COALESCE(color,'') = COALESCE(?,'')
      AND COALESCE(varietal,'') = COALESCE(?,'')
    LIMIT 1
  `).get(
    wine.producer || null,
    wine.wine_name || null,
    wine.region || null,
    wine.country || null,
    wine.style || null,
    wine.color || null,
    wine.varietal || null,
  );

  if (existing) {
    db.prepare(`
      UPDATE wines SET
        updated_at = datetime('now'),
        official_rating = COALESCE(@official_rating, official_rating),
        official_rating_source = COALESCE(@official_rating_source, official_rating_source),
        default_notes = COALESCE(@default_notes, default_notes),
        default_source_image_path = COALESCE(@default_source_image_path, default_source_image_path)
      WHERE id = @id
    `).run({
      id: existing.id,
      official_rating: wine.official_rating ?? null,
      official_rating_source: wine.official_rating_source ?? null,
      default_notes: wine.default_notes ?? null,
      default_source_image_path: wine.default_source_image_path ?? null,
    });
    return existing.id;
  }

  const result = db.prepare(`
    INSERT INTO wines (
      created_at, updated_at, producer, wine_name, region, country, style, color, varietal,
      official_rating, official_rating_source, default_notes, default_source_image_path
    ) VALUES (
      @created_at, @updated_at, @producer, @wine_name, @region, @country, @style, @color, @varietal,
      @official_rating, @official_rating_source, @default_notes, @default_source_image_path
    )
  `).run({
    created_at: wine.created_at || new Date().toISOString(),
    updated_at: wine.updated_at || new Date().toISOString(),
    producer: wine.producer ?? null,
    wine_name: wine.wine_name ?? null,
    region: wine.region ?? null,
    country: wine.country ?? null,
    style: wine.style ?? null,
    color: wine.color ?? null,
    varietal: wine.varietal ?? null,
    official_rating: wine.official_rating ?? null,
    official_rating_source: wine.official_rating_source ?? null,
    default_notes: wine.default_notes ?? null,
    default_source_image_path: wine.default_source_image_path ?? null,
  });
  return result.lastInsertRowid;
}

function restoreImage(imgPath, images, labelsDir) {
  if (!imgPath) return imgPath;
  const entry = images[imgPath];
  if (!entry) return imgPath; // no embedded image — assume path is accessible or user copied labels dir

  const filename = path.basename(imgPath);
  const dest = path.join(labelsDir, filename);
  if (!fs.existsSync(dest)) {
    fs.writeFileSync(dest, Buffer.from(entry.data, 'base64'));
  }
  return dest;
}

function ensureSchema(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS wines (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      producer TEXT, wine_name TEXT, region TEXT, country TEXT,
      style TEXT, color TEXT, varietal TEXT,
      official_rating REAL, official_rating_source TEXT,
      default_notes TEXT, default_source_image_path TEXT
    );
    CREATE TABLE IF NOT EXISTS wine_instances (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      wine_id INTEGER NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      source_type TEXT NOT NULL,
      source_text TEXT, source_image_path TEXT,
      vintage TEXT, price REAL, currency TEXT,
      place_of_purchase TEXT, purchased_on TEXT, consumed_on TEXT,
      subjective_rating REAL, notes TEXT, raw_extraction_json TEXT,
      FOREIGN KEY (wine_id) REFERENCES wines(id) ON DELETE CASCADE
    );
    CREATE INDEX IF NOT EXISTS idx_wines_name ON wines(wine_name);
    CREATE INDEX IF NOT EXISTS idx_wines_producer ON wines(producer);
    CREATE INDEX IF NOT EXISTS idx_instances_wine_id ON wine_instances(wine_id);
    CREATE INDEX IF NOT EXISTS idx_instances_consumed_on ON wine_instances(consumed_on);
  `);
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const inPath = args.in;
  if (!inPath) {
    process.stderr.write('Error: --in <export.json> is required\n');
    process.exitCode = 1;
    return;
  }

  const resolvedIn = path.resolve(inPath);
  if (!fs.existsSync(resolvedIn)) {
    process.stderr.write(`Error: file not found: ${resolvedIn}\n`);
    process.exitCode = 1;
    return;
  }

  const dryRun = Boolean(args['dry-run']);
  const labelsDir = path.resolve(args['labels-dir'] || DEFAULT_LABELS_DIR);
  const payload = JSON.parse(fs.readFileSync(resolvedIn, 'utf8'));

  if (!payload.version || payload.version !== 1) {
    process.stderr.write(`Error: unsupported export version: ${payload.version}\n`);
    process.exitCode = 1;
    return;
  }

  const wines = payload.wines || [];
  const instances = payload.wine_instances || [];
  const images = payload.images || {};
  const hasEmbeddedImages = Object.keys(images).length > 0;

  process.stdout.write(JSON.stringify({
    status: 'preview',
    dry_run: dryRun,
    wines_to_import: wines.length,
    instances_to_import: instances.length,
    embedded_images: Object.keys(images).length,
    labels_dir: labelsDir,
    db_path: DB_PATH,
  }, null, 2) + '\n');

  if (dryRun) {
    process.stdout.write(JSON.stringify({ status: 'ok', note: 'Dry run complete — nothing written.' }, null, 2) + '\n');
    return;
  }

  fs.mkdirSync(path.dirname(DB_PATH), { recursive: true });
  if (hasEmbeddedImages) fs.mkdirSync(labelsDir, { recursive: true });

  const db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');
  ensureSchema(db);

  // Build old wine_id → new wine_id mapping
  const wineIdMap = new Map();

  const tx = db.transaction(() => {
    for (const wine of wines) {
      const resolvedImagePath = hasEmbeddedImages
        ? restoreImage(wine.default_source_image_path, images, labelsDir)
        : wine.default_source_image_path;

      const newId = resolveWineId(db, { ...wine, default_source_image_path: resolvedImagePath });
      wineIdMap.set(wine.id, newId);
    }

    let inserted = 0;
    for (const inst of instances) {
      const newWineId = wineIdMap.get(inst.wine_id);
      if (newWineId == null) {
        process.stderr.write(`Warning: skipping instance id=${inst.id} — wine_id ${inst.wine_id} not found in import\n`);
        continue;
      }

      const resolvedImagePath = hasEmbeddedImages
        ? restoreImage(inst.source_image_path, images, labelsDir)
        : inst.source_image_path;

      db.prepare(`
        INSERT INTO wine_instances (
          wine_id, created_at, updated_at, source_type, source_text, source_image_path,
          vintage, price, currency, place_of_purchase, purchased_on, consumed_on,
          subjective_rating, notes, raw_extraction_json
        ) VALUES (
          @wine_id, @created_at, @updated_at, @source_type, @source_text, @source_image_path,
          @vintage, @price, @currency, @place_of_purchase, @purchased_on, @consumed_on,
          @subjective_rating, @notes, @raw_extraction_json
        )
      `).run({
        wine_id: newWineId,
        created_at: inst.created_at || new Date().toISOString(),
        updated_at: inst.updated_at || new Date().toISOString(),
        source_type: inst.source_type || 'manual',
        source_text: inst.source_text ?? null,
        source_image_path: resolvedImagePath ?? null,
        vintage: inst.vintage ?? null,
        price: inst.price ?? null,
        currency: inst.currency ?? 'USD',
        place_of_purchase: inst.place_of_purchase ?? null,
        purchased_on: inst.purchased_on ?? null,
        consumed_on: inst.consumed_on ?? null,
        subjective_rating: inst.subjective_rating ?? null,
        notes: inst.notes ?? null,
        raw_extraction_json: inst.raw_extraction_json ?? null,
      });
      inserted += 1;
    }

    return inserted;
  });

  const inserted = tx();
  db.close();

  process.stdout.write(JSON.stringify({
    status: 'ok',
    wines_processed: wines.length,
    instances_inserted: inserted,
    db_path: DB_PATH,
  }, null, 2) + '\n');
}

main();
