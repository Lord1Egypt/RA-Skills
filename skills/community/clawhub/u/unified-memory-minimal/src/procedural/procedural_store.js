/**
 * Procedural Store - Persistent storage for procedural memories
 *
 * A procedural memory stores "how to do something" as a step-by-step procedure,
 * distinct from declarative facts stored elsewhere.
 *
 * Storage: ~/.openclaw/workspace/memory/procedurals.json
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';
import { config } from '../config.js';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const PROCEDURAL_FILE = join(config.memoryDir, 'procedurals.json');

// In-memory cache
let cache = null;
let cacheDirty = false;

// ─── File I/O ────────────────────────────────────────────────────────────────

function ensureDir() {
  const dir = config.memoryDir;
  if (!existsSync(dir)) {
    mkdirSync(dir, { recursive: true });
  }
}

function loadStore() {
  if (cache) return cache;
  ensureDir();
  if (!existsSync(PROCEDURAL_FILE)) {
    cache = createEmptyStore();
    return cache;
  }
  try {
    const raw = JSON.parse(readFileSync(PROCEDURAL_FILE, 'utf-8'));
    cache = {
      procedurals: Array.isArray(raw.procedurals) ? raw.procedurals : [],
      metadata: raw.metadata || { version: '1.0', lastUpdated: Date.now(), count: 0 },
    };
    return cache;
  } catch {
    cache = createEmptyStore();
    return cache;
  }
}

function createEmptyStore() {
  return {
    procedurals: [],
    metadata: { version: '1.0', lastUpdated: Date.now(), count: 0 },
  };
}

function saveStore(store) {
  ensureDir();
  store.metadata.lastUpdated = Date.now();
  store.metadata.count = store.procedurals.length;
  writeFileSync(PROCEDURAL_FILE, JSON.stringify(store, null, 2), 'utf-8');
  cache = store;
  cacheDirty = false;
}

// ─── Core CRUD ───────────────────────────────────────────────────────────────

/**
 * Load all procedurals from store
 * @returns {any[]}
 */
export function loadProcedurals() {
  return loadStore().procedurals;
}

/**
 * Save the full procedurals array to store
 * @param {any[]} procedurals
 */
export function saveProcedurals(procedurals) {
  const store = loadStore();
  store.procedurals = procedurals;
  saveStore(store);
}

/**
 * Add a new procedural memory
 * @param {string} procedureName
 * @param {Array<{step: number, action: string, tool: string|null}>} steps
 * @param {string} trigger - regex pattern to match user queries
 * @returns {object} the created procedural
 */
export function addProcedure(procedureName, steps, trigger) {
  const procedurals = loadProcedurals();
  const id = 'proc_' + crypto.randomUUID().replace(/-/g, '').slice(0, 16);
  const now = new Date().toISOString();
  const proc = {
    id,
    procedure_name: procedureName,
    steps: steps.map(s => ({
      step: s.step,
      action: s.action,
      tool: s.tool || null,
    })),
    trigger,
    confidence: 0.8,
    usage_count: 0,
    last_used: now,
  };
  procedurals.push(proc);
  saveProcedurals(procedurals);
  return proc;
}

/**
 * Find procedurals matching a trigger string
 * @param {string} triggerText
 * @returns {any[]} matching procedurals
 */
export function findProcedure(triggerText) {
  const procedurals = loadProcedurals();
  return procedurals.filter(p => {
    try {
      const re = new RegExp(p.trigger, 'i');
      return re.test(triggerText);
    } catch {
      return p.trigger.toLowerCase().includes(triggerText.toLowerCase());
    }
  });
}

/**
 * Delete a procedural by id
 * @param {string} id
 * @returns {boolean} true if deleted
 */
export function deleteProcedure(id) {
  const procedurals = loadProcedurals();
  const idx = procedurals.findIndex(p => p.id === id);
  if (idx === -1) return false;
  procedurals.splice(idx, 1);
  saveProcedurals(procedurals);
  return true;
}

/**
 * Increment usage counter and update last_used for a procedural
 * @param {string} id
 */
export function touchProcedure(id) {
  const procedurals = loadProcedurals();
  const proc = procedurals.find(p => p.id === id);
  if (proc) {
    proc.usage_count = (proc.usage_count || 0) + 1;
    proc.last_used = new Date().toISOString();
    saveProcedurals(procedurals);
  }
}
