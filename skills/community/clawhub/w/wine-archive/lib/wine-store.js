const fs = require('fs');
const path = require('path');
const Database = require('better-sqlite3');

const WORKSPACE = path.resolve(__dirname, '..');
const DATA_DIR = path.join(WORKSPACE, 'data', 'wine');
const LABELS_DIR = path.join(DATA_DIR, 'labels');
const AUDIT_LOG_PATH = path.join(DATA_DIR, 'audit.log');
const DEFAULT_DB_PATH = path.join(DATA_DIR, 'wine.sqlite3');
const DB_PATH = process.env.WINE_DB_PATH ? path.resolve(process.env.WINE_DB_PATH) : DEFAULT_DB_PATH;

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function ensureDataDirs() {
  ensureDir(DATA_DIR);
  ensureDir(LABELS_DIR);
}

function appendAudit(event) {
  ensureDataDirs();
  const line = `${JSON.stringify({ ts: new Date().toISOString(), ...event })}\n`;
  fs.appendFileSync(AUDIT_LOG_PATH, line, 'utf8');
}

function fileDigest(filePath) {
  const data = fs.readFileSync(filePath);
  let h = 2166136261;
  for (let i = 0; i < data.length; i++) {
    h = Math.imul(h ^ data[i], 16777619) >>> 0;
  }
  return h.toString(16).padStart(8, '0');
}

// Image normalization (resizing) is intentionally omitted from this package.
// Images are stored as-is. If you need auto-resizing, add it in your own
// wrapper using ImageMagick (convert -resize) or the sharp npm package.
function normalizeImageInPlace(_filePath, _maxDimension = 1200) {
  return { changed: false };
}

function resolveImagePath(imagePath) {
  if (!imagePath) return null;
  const resolved = path.resolve(imagePath);

  // If the path exists, use it as-is
  if (fs.existsSync(resolved)) return resolved;

  // Handle migration from old workspace paths to skill directory.
  // Old path format: /Users/simon/.openclaw/workspace/data/wine/labels/filename
  // New path format: /Users/simon/.openclaw/workspace/skills/wine-archive/data/wine/labels/filename
  if (resolved.includes('/.openclaw/workspace/data/wine/labels/')) {
    const filename = path.basename(resolved);
    const newPath = path.join(LABELS_DIR, filename);
    if (fs.existsSync(newPath)) {
      return newPath;
    }
  }

  // Path doesn't exist; return it as-is (caller will handle missing file)
  return resolved;
}

function persistImagePath(imagePath, preferredStem = 'label') {
  if (!imagePath) return null;
  const resolved = resolveImagePath(imagePath);
  if (!fs.existsSync(resolved)) return resolved;

  ensureDataDirs();
  if (resolved.startsWith(`${LABELS_DIR}${path.sep}`) || resolved === LABELS_DIR) return resolved;

  const ext = path.extname(resolved) || '.jpg';
  const safeStem = String(preferredStem || 'label')
    .normalize('NFKD')
    .replace(/[^a-zA-Z0-9_-]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .toLowerCase() || 'label';
  const digest = fileDigest(resolved);
  const target = path.join(LABELS_DIR, `${safeStem}-${digest}${ext.toLowerCase()}`);

  if (!fs.existsSync(target)) {
    fs.copyFileSync(resolved, target);
    normalizeImageInPlace(target, 1200);
    appendAudit({ action: 'persist-image', source: resolved, target });
  }

  return target;
}

function safeParseJson(value) {
  if (!value) return null;
  try {
    return typeof value === 'string' ? JSON.parse(value) : value;
  } catch {
    return null;
  }
}

function openDb() {
  ensureDataDirs();
  const db = new Database(DB_PATH);
  db.pragma('journal_mode = WAL');
  db.exec(`
    CREATE TABLE IF NOT EXISTS wines (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      producer TEXT,
      wine_name TEXT,
      region TEXT,
      country TEXT,
      style TEXT,
      color TEXT,
      varietal TEXT,
      official_rating REAL,
      official_rating_source TEXT,
      default_notes TEXT,
      default_source_image_path TEXT
    );

    CREATE TABLE IF NOT EXISTS wine_instances (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      wine_id INTEGER NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now')),
      updated_at TEXT NOT NULL DEFAULT (datetime('now')),
      source_type TEXT NOT NULL,
      source_text TEXT,
      source_image_path TEXT,
      vintage TEXT,
      price REAL,
      currency TEXT,
      place_of_purchase TEXT,
      purchased_on TEXT,
      consumed_on TEXT,
      subjective_rating REAL,
      notes TEXT,
      raw_extraction_json TEXT,
      FOREIGN KEY (wine_id) REFERENCES wines(id) ON DELETE CASCADE
    );

    CREATE INDEX IF NOT EXISTS idx_wines_name ON wines(wine_name);
    CREATE INDEX IF NOT EXISTS idx_wines_producer ON wines(producer);
    CREATE INDEX IF NOT EXISTS idx_instances_wine_id ON wine_instances(wine_id);
    CREATE INDEX IF NOT EXISTS idx_instances_purchased_on ON wine_instances(purchased_on);
    CREATE INDEX IF NOT EXISTS idx_instances_consumed_on ON wine_instances(consumed_on);
    CREATE INDEX IF NOT EXISTS idx_instances_price ON wine_instances(price);
  `);

  migrateLegacyWineEntries(db);
  migrateImagePaths(db);
  return db;
}

function migrateLegacyWineEntries(db) {
  const legacyExists = db.prepare(`SELECT name FROM sqlite_master WHERE type='table' AND name='wine_entries'`).get();
  if (!legacyExists) return;

  const migratedFlag = db.prepare(`SELECT name FROM sqlite_master WHERE type='table' AND name='wine_entries_legacy_migrated'`).get();
  if (migratedFlag) return;

  const legacyRows = db.prepare(`SELECT * FROM wine_entries ORDER BY id`).all();
  const upsertWine = db.prepare(`
    INSERT INTO wines (producer, wine_name, region, country, style, color, varietal, official_rating, official_rating_source, default_notes, default_source_image_path)
    VALUES (@producer, @wine_name, @region, @country, @style, @color, @varietal, @official_rating, @official_rating_source, @default_notes, @default_source_image_path)
  `);
  const insertInstance = db.prepare(`
    INSERT INTO wine_instances (wine_id, created_at, updated_at, source_type, source_text, source_image_path, vintage, price, currency, place_of_purchase, purchased_on, consumed_on, subjective_rating, notes, raw_extraction_json)
    VALUES (@wine_id, @created_at, @updated_at, @source_type, @source_text, @source_image_path, @vintage, @price, @currency, @place_of_purchase, @purchased_on, @consumed_on, @subjective_rating, @notes, @raw_extraction_json)
  `);
  const findWine = db.prepare(`
    SELECT id FROM wines
    WHERE COALESCE(producer,'') = COALESCE(@producer,'')
      AND COALESCE(wine_name,'') = COALESCE(@wine_name,'')
      AND COALESCE(region,'') = COALESCE(@region,'')
      AND COALESCE(country,'') = COALESCE(@country,'')
      AND COALESCE(style,'') = COALESCE(@style,'')
      AND COALESCE(color,'') = COALESCE(@color,'')
      AND COALESCE(varietal,'') = COALESCE(@varietal,'')
    LIMIT 1
  `);

  const tx = db.transaction(() => {
    for (const row of legacyRows) {
      const wineKey = {
        producer: row.producer || null,
        wine_name: row.wine_name || null,
        region: row.region || null,
        country: row.country || null,
        style: row.style || null,
        color: row.color || null,
        varietal: row.varietal || null,
      };
      let wine = findWine.get(wineKey);
      if (!wine) {
        const result = upsertWine.run({
          ...wineKey,
          official_rating: row.official_rating || null,
          official_rating_source: row.official_rating_source || null,
          default_notes: null,
          default_source_image_path: row.source_image_path || null,
        });
        wine = { id: result.lastInsertRowid };
      }

      insertInstance.run({
        wine_id: wine.id,
        created_at: row.created_at,
        updated_at: row.updated_at,
        source_type: row.source_type || 'manual',
        source_text: row.source_text || null,
        source_image_path: row.source_image_path || null,
        vintage: row.vintage || null,
        price: row.price == null ? null : row.price,
        currency: row.currency || 'USD',
        place_of_purchase: row.place_of_purchase || null,
        purchased_on: row.purchased_on || null,
        consumed_on: row.consumed_on || null,
        subjective_rating: row.subjective_rating == null ? null : row.subjective_rating,
        notes: row.notes || null,
        raw_extraction_json: row.raw_extraction_json || null,
      });
    }

    db.exec(`ALTER TABLE wine_entries RENAME TO wine_entries_legacy_migrated`);
  });

  tx();
  appendAudit({ action: 'migrate-legacy-wine-entries', count: legacyRows.length });
}

function migrateImagePaths(db) {
  // Migrate old workspace paths to skill-relative paths after skill installation.
  // Old: /Users/simon/.openclaw/workspace/data/wine/labels/filename
  // New: /Users/simon/.openclaw/workspace/skills/wine-archive/data/wine/labels/filename
  const oldPathPattern = '/.openclaw/workspace/data/wine/labels/';
  const newPathPattern = '/.openclaw/workspace/skills/wine-archive/data/wine/labels/';

  // Also handle wines table
  const winesWithOldPaths = db.prepare(
    `SELECT id, default_source_image_path FROM wines WHERE default_source_image_path LIKE ?`
  ).all(`%${oldPathPattern}%`);

  if (winesWithOldPaths.length > 0) {
    const updateWine = db.prepare(`UPDATE wines SET default_source_image_path = ? WHERE id = ?`);
    const tx = db.transaction(() => {
      for (const wine of winesWithOldPaths) {
        const newPath = wine.default_source_image_path.replace(oldPathPattern, newPathPattern);
        updateWine.run(newPath, wine.id);
      }
    });
    tx();
    appendAudit({ action: 'migrate-image-paths-wines', count: winesWithOldPaths.length });
  }

  // Migrate wine_instances table
  const instancesWithOldPaths = db.prepare(
    `SELECT id, source_image_path FROM wine_instances WHERE source_image_path LIKE ?`
  ).all(`%${oldPathPattern}%`);

  if (instancesWithOldPaths.length > 0) {
    const updateInstance = db.prepare(`UPDATE wine_instances SET source_image_path = ? WHERE id = ?`);
    const tx = db.transaction(() => {
      for (const instance of instancesWithOldPaths) {
        const newPath = instance.source_image_path.replace(oldPathPattern, newPathPattern);
        updateInstance.run(newPath, instance.id);
      }
    });
    tx();
    appendAudit({ action: 'migrate-image-paths-instances', count: instancesWithOldPaths.length });
  }
}

function normalizeEntry(entry = {}) {
  const preferredStem = [entry.producer, entry.wine_name, entry.vintage].filter(Boolean).join('-') || 'label';
  return {
    source_type: entry.source_type || 'manual',
    source_text: entry.source_text || null,
    source_image_path: persistImagePath(entry.source_image_path, preferredStem),
    wine_name: entry.wine_name || null,
    producer: entry.producer || null,
    varietal: entry.varietal || null,
    region: entry.region || null,
    country: entry.country || null,
    style: entry.style || null,
    color: entry.color || null,
    vintage: entry.vintage || null,
    price: entry.price == null || entry.price === '' ? null : Number(entry.price),
    currency: entry.currency || 'USD',
    place_of_purchase: entry.place_of_purchase || null,
    purchased_on: entry.purchased_on || null,
    consumed_on: entry.consumed_on || null,
    subjective_rating: entry.subjective_rating == null || entry.subjective_rating === '' ? null : Number(entry.subjective_rating),
    official_rating: entry.official_rating == null || entry.official_rating === '' ? null : Number(entry.official_rating),
    official_rating_source: entry.official_rating_source || null,
    notes: entry.notes || null,
    raw_extraction_json: entry.raw_extraction_json ? JSON.stringify(entry.raw_extraction_json) : null,
  };
}

function resolveWineId(db, normalized) {
  const findWine = db.prepare(`
    SELECT * FROM wines
    WHERE COALESCE(producer,'') = COALESCE(@producer,'')
      AND COALESCE(wine_name,'') = COALESCE(@wine_name,'')
      AND COALESCE(region,'') = COALESCE(@region,'')
      AND COALESCE(country,'') = COALESCE(@country,'')
      AND COALESCE(style,'') = COALESCE(@style,'')
      AND COALESCE(color,'') = COALESCE(@color,'')
      AND COALESCE(varietal,'') = COALESCE(@varietal,'')
    LIMIT 1
  `);
  const insertWine = db.prepare(`
    INSERT INTO wines (producer, wine_name, region, country, style, color, varietal, official_rating, official_rating_source, default_notes, default_source_image_path)
    VALUES (@producer, @wine_name, @region, @country, @style, @color, @varietal, @official_rating, @official_rating_source, NULL, @source_image_path)
  `);
  const updateWine = db.prepare(`
    UPDATE wines
    SET updated_at = datetime('now'),
        producer = @producer,
        wine_name = @wine_name,
        region = @region,
        country = @country,
        style = @style,
        color = @color,
        varietal = @varietal,
        official_rating = @official_rating,
        official_rating_source = @official_rating_source,
        default_source_image_path = COALESCE(@source_image_path, default_source_image_path)
    WHERE id = @id
  `);

  let wine = findWine.get(normalized);
  if (!wine) {
    const result = insertWine.run(normalized);
    return result.lastInsertRowid;
  }

  updateWine.run({ ...normalized, id: wine.id });
  return wine.id;
}

function projectJoinedRow(row) {
  if (!row) return null;
  return {
    id: row.instance_id,
    wine_id: row.wine_id,
    created_at: row.instance_created_at,
    updated_at: row.instance_updated_at,
    source_type: row.source_type,
    source_text: row.source_text,
    source_image_path: row.source_image_path || row.default_source_image_path || null,
    wine_name: row.wine_name,
    producer: row.producer,
    varietal: row.varietal,
    region: row.region,
    country: row.country,
    style: row.style,
    color: row.color,
    vintage: row.vintage,
    price: row.price,
    currency: row.currency,
    place_of_purchase: row.place_of_purchase,
    purchased_on: row.purchased_on,
    consumed_on: row.consumed_on,
    subjective_rating: row.subjective_rating,
    official_rating: row.official_rating,
    official_rating_source: row.official_rating_source,
    notes: row.notes,
    raw_extraction_json: row.raw_extraction_json,
  };
}

function joinedSelect(where = '', orderLimit = '') {
  return `
    SELECT
      wi.id AS instance_id,
      wi.wine_id AS wine_id,
      wi.created_at AS instance_created_at,
      wi.updated_at AS instance_updated_at,
      wi.source_type,
      wi.source_text,
      wi.source_image_path,
      wi.vintage,
      wi.price,
      wi.currency,
      wi.place_of_purchase,
      wi.purchased_on,
      wi.consumed_on,
      wi.subjective_rating,
      wi.notes,
      wi.raw_extraction_json,
      w.producer,
      w.wine_name,
      w.varietal,
      w.region,
      w.country,
      w.style,
      w.color,
      w.official_rating,
      w.official_rating_source,
      w.default_source_image_path
    FROM wine_instances wi
    JOIN wines w ON w.id = wi.wine_id
    ${where}
    ${orderLimit}
  `;
}

function insertWineEntry(entry) {
  const db = openDb();
  const normalized = normalizeEntry(entry);
  const wineId = resolveWineId(db, normalized);
  const stmt = db.prepare(`
    INSERT INTO wine_instances (
      wine_id, source_type, source_text, source_image_path, vintage, price, currency,
      place_of_purchase, purchased_on, consumed_on, subjective_rating, notes, raw_extraction_json
    ) VALUES (
      @wine_id, @source_type, @source_text, @source_image_path, @vintage, @price, @currency,
      @place_of_purchase, @purchased_on, @consumed_on, @subjective_rating, @notes, @raw_extraction_json
    )
  `);
  const result = stmt.run({ ...normalized, wine_id: wineId });
  const created = getWineById(result.lastInsertRowid);
  appendAudit({ action: 'insert', id: created.id, wine_id: created.wine_id, wine_name: created.wine_name, producer: created.producer, source_image_path: created.source_image_path });
  return created;
}

function updateWineEntry(id, patch = {}) {
  const existing = getWineById(id);
  if (!existing) return null;

  const merged = {
    ...existing,
    ...patch,
    raw_extraction_json: patch.raw_extraction_json || safeParseJson(existing.raw_extraction_json) || null,
  };
  const normalized = normalizeEntry(merged);
  const db = openDb();
  const wineId = resolveWineId(db, normalized);

  db.prepare(`
    UPDATE wine_instances
    SET
      updated_at = datetime('now'),
      wine_id = @wine_id,
      source_type = @source_type,
      source_text = @source_text,
      source_image_path = @source_image_path,
      vintage = @vintage,
      price = @price,
      currency = @currency,
      place_of_purchase = @place_of_purchase,
      purchased_on = @purchased_on,
      consumed_on = @consumed_on,
      subjective_rating = @subjective_rating,
      notes = @notes,
      raw_extraction_json = @raw_extraction_json
    WHERE id = @id
  `).run({ ...normalized, wine_id: wineId, id });

  const updated = getWineById(id);
  appendAudit({ action: 'update', id: updated.id, wine_id: updated.wine_id, wine_name: updated.wine_name, producer: updated.producer, source_image_path: updated.source_image_path });
  return updated;
}

function deleteWineEntry(id) {
  const existing = getWineById(id);
  if (!existing) return null;
  const db = openDb();
  db.prepare('DELETE FROM wine_instances WHERE id = ?').run(id);
  appendAudit({ action: 'delete', id: existing.id, wine_id: existing.wine_id, wine_name: existing.wine_name, producer: existing.producer, source_image_path: existing.source_image_path });
  return existing;
}

function getWineById(id) {
  const db = openDb();
  const row = db.prepare(joinedSelect('WHERE wi.id = ?', 'LIMIT 1')).get(id);
  return projectJoinedRow(row);
}

function listWineEntries(limit = 25) {
  const db = openDb();
  const numericLimit = Number(limit);
  const safeLimit = Number.isFinite(numericLimit) ? Math.max(1, Math.min(numericLimit, 200)) : 25;
  const rows = db.prepare(joinedSelect('', `ORDER BY COALESCE(wi.consumed_on, wi.purchased_on, wi.created_at) DESC LIMIT ${safeLimit}`)).all();
  return rows.map(projectJoinedRow);
}

function summarizeWine(entry) {
  const parts = [];
  const title = [entry.producer, entry.wine_name, entry.vintage].filter(Boolean).join(' ');
  if (title) parts.push(title);
  const profile = [entry.color, entry.style, entry.varietal].filter(Boolean).join(' ');
  if (profile) parts.push(profile);
  const origin = [entry.region, entry.country].filter(Boolean).join(', ');
  if (origin) parts.push(origin);
  if (entry.place_of_purchase) parts.push(`bought at ${entry.place_of_purchase}`);
  if (entry.consumed_on) parts.push(`drank ${entry.consumed_on}`);
  else if (entry.purchased_on) parts.push(`bought ${entry.purchased_on}`);
  if (entry.subjective_rating != null) parts.push(`rated ${entry.subjective_rating}/5`);
  return parts.join(' · ');
}

function queryWineEntries(criteria = {}) {
  const db = openDb();
  const clauses = [];
  const params = {};

  const textFields = ['w.wine_name', 'w.producer', 'w.varietal', 'w.region', 'w.country', 'w.style', 'w.color', 'wi.place_of_purchase', 'wi.notes', 'wi.source_text'];
  if (criteria.text) {
    clauses.push(`(${textFields.map((f) => `${f} LIKE @text`).join(' OR ')})`);
    params.text = `%${criteria.text}%`;
  }

  for (const [field, column] of Object.entries({
    varietal: 'w.varietal',
    region: 'w.region',
    style: 'w.style',
    color: 'w.color',
    place_of_purchase: 'wi.place_of_purchase',
    producer: 'w.producer',
    country: 'w.country',
    wine_name: 'w.wine_name',
    vintage: 'wi.vintage',
  })) {
    if (criteria[field]) {
      clauses.push(`${column} LIKE @${field}`);
      params[field] = `%${criteria[field]}%`;
    }
  }

  if (criteria.purchased_after) {
    clauses.push('wi.purchased_on >= @purchased_after');
    params.purchased_after = criteria.purchased_after;
  }
  if (criteria.purchased_before) {
    clauses.push('wi.purchased_on <= @purchased_before');
    params.purchased_before = criteria.purchased_before;
  }
  if (criteria.consumed_after) {
    clauses.push('wi.consumed_on >= @consumed_after');
    params.consumed_after = criteria.consumed_after;
  }
  if (criteria.consumed_before) {
    clauses.push('wi.consumed_on <= @consumed_before');
    params.consumed_before = criteria.consumed_before;
  }
  if (criteria.min_subjective_rating != null) {
    clauses.push('wi.subjective_rating >= @min_subjective_rating');
    params.min_subjective_rating = Number(criteria.min_subjective_rating);
  }

  const where = clauses.length ? `WHERE ${clauses.join(' AND ')}` : '';
  const numericLimit = Number(criteria.limit);
  const safeLimit = Number.isFinite(numericLimit) ? Math.max(1, Math.min(numericLimit, 100)) : 10;
  const rows = db.prepare(joinedSelect(where, `ORDER BY COALESCE(wi.consumed_on, wi.purchased_on, wi.created_at) DESC LIMIT ${safeLimit}`)).all(params);

  return rows.map(projectJoinedRow);
}

function recallWineEntries(criteria = {}) {
  const entries = queryWineEntries(criteria);
  return {
    criteria,
    count: entries.length,
    entries,
    summary: entries.map((entry) => ({ id: entry.id, summary: summarizeWine(entry) })),
  };
}

function listWineCatalog(limit = 100) {
  const db = openDb();
  const rows = db.prepare(`
    SELECT
      w.id,
      w.producer,
      w.wine_name,
      w.varietal,
      w.region,
      w.country,
      w.style,
      w.color,
      w.official_rating,
      w.official_rating_source,
      w.default_source_image_path,
      COUNT(wi.id) AS instance_count,
      MIN(wi.price) AS min_price,
      MAX(wi.price) AS max_price,
      MAX(wi.purchased_on) AS latest_purchased_on,
      MAX(wi.consumed_on) AS latest_consumed_on
    FROM wines w
    LEFT JOIN wine_instances wi ON wi.wine_id = w.id
    GROUP BY w.id
    ORDER BY LOWER(COALESCE(w.wine_name, '')), LOWER(COALESCE(w.producer, ''))
    LIMIT ?
  `).all(Math.max(1, Math.min(Number(limit) || 100, 500)));
  return rows;
}

function getWineWithInstancesByWineId(wineId) {
  const db = openDb();
  const wine = db.prepare(`SELECT * FROM wines WHERE id = ?`).get(wineId);
  if (!wine) return null;
  const instances = db.prepare(joinedSelect('WHERE w.id = ?', 'ORDER BY COALESCE(wi.consumed_on, wi.purchased_on, wi.created_at) DESC')).all(wineId).map(projectJoinedRow);
  return { wine, instances };
}

function recallWineCatalog(criteria = {}) {
  const entries = queryWineEntries({ ...criteria, limit: criteria.limit || 200 });
  const grouped = new Map();
  for (const entry of entries) {
    if (!grouped.has(entry.wine_id)) grouped.set(entry.wine_id, []);
    grouped.get(entry.wine_id).push(entry);
  }

  const wines = Array.from(grouped.entries()).map(([wine_id, instances]) => {
    const first = instances[0];
    return {
      wine_id,
      producer: first.producer,
      wine_name: first.wine_name,
      varietal: first.varietal,
      region: first.region,
      country: first.country,
      style: first.style,
      color: first.color,
      official_rating: first.official_rating,
      official_rating_source: first.official_rating_source,
      source_image_path: first.source_image_path,
      instance_count: instances.length,
      instances,
    };
  });

  return {
    criteria,
    count: wines.length,
    wines,
  };
}

function findRecentWineEntryByImagePath(imagePath) {
  if (!imagePath) return null;
  const db = openDb();
  const row = db.prepare(joinedSelect('WHERE wi.source_image_path = ?', 'ORDER BY datetime(wi.created_at) DESC LIMIT 1')).get(imagePath);
  return projectJoinedRow(row);
}

module.exports = {
  DB_PATH,
  LABELS_DIR,
  AUDIT_LOG_PATH,
  openDb,
  insertWineEntry,
  updateWineEntry,
  deleteWineEntry,
  getWineById,
  listWineEntries,
  queryWineEntries,
  recallWineEntries,
  listWineCatalog,
  getWineWithInstancesByWineId,
  recallWineCatalog,
  summarizeWine,
  findRecentWineEntryByImagePath,
  persistImagePath,
};
