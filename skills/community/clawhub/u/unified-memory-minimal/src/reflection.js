/**
 * Self-Improvement / Reflection System
 * Records learning from failures and successes into .learnings/
 * LRN entries: positive lessons
 * ERR entries: mistakes and corrections
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import crypto from 'crypto';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const LEARNINGS_DIR = path.join(__dirname, '..', '.learnings');
const LEARNINGS_FILE = path.join(LEARNINGS_DIR, 'learnings.md');
const ERRORS_FILE = path.join(LEARNINGS_DIR, 'errors.md');

function ensureLearningsDir() {
  if (!fs.existsSync(LEARNINGS_DIR)) fs.mkdirSync(LEARNINGS_DIR, { recursive: true });
}
function readFile(p) {
  try { return fs.readFileSync(p, 'utf8'); } catch { return ''; }
}
function writeFile(p, content) {
  ensureLearningsDir();
  fs.writeFileSync(p, content, 'utf8');
}

let _seq = 0;
function nextId(prefix = 'LRN') {
  const d = new Date();
  _seq++;
  return `${prefix}-${d.getFullYear()}${String(d.getMonth()+1).padStart(2,'0')}${String(d.getDate()).padStart(2,'0')}-${String(_seq).padStart(3,'0')}`;
}

/**
 * Add a learning entry (success pattern / best practice)
 * @param {string} text
 * @param {string} [category]
 * @param {object} [metadata]
 */
export function addLearning(text, category = 'general', metadata = {}) {
  const id = nextId('LRN');
  const entry = { id, type: 'LRN', category, text, metadata, createdAt: new Date().toISOString() };
  const content = readFile(LEARNINGS_FILE);
  const newContent = content
    ? content.trimEnd() + '\n' + JSON.stringify(entry)
    : JSON.stringify(entry);
  writeFile(LEARNINGS_FILE, newContent + '\n');
  return entry;
}

/**
 * Add an error entry (failure / mistake to avoid)
 * @param {string} text
 * @param {string} [errorType]
 * @param {object} [metadata]
 */
export function addError(text, errorType = 'unknown', metadata = {}) {
  const id = nextId('ERR');
  const entry = { id, type: 'ERR', category: errorType, text, metadata, createdAt: new Date().toISOString() };
  const content = readFile(ERRORS_FILE);
  const newContent = content
    ? content.trimEnd() + '\n' + JSON.stringify(entry)
    : JSON.stringify(entry);
  writeFile(ERRORS_FILE, newContent + '\n');
  return entry;
}

/**
 * Get all learnings
 * @returns {Array}
 */
export function getLearnings() {
  const content = readFile(LEARNINGS_FILE);
  if (!content.trim()) return [];
  return content.trim().split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
}

/**
 * Get all errors
 * @returns {Array}
 */
export function getErrors() {
  const content = readFile(ERRORS_FILE);
  if (!content.trim()) return [];
  return content.trim().split('\n').filter(Boolean).map(l => { try { return JSON.parse(l); } catch { return null; } }).filter(Boolean);
}

/**
 * Get stats summary
 */
export function getStats() {
  const learnings = getLearnings();
  const errors = getErrors();
  return {
    learnings: learnings.length,
    errors: errors.length,
    categories: [...new Set([...learnings.map(l=>l.category), ...errors.map(e=>e.category)])],
  };
}

/**
 * Auto-record a retrieval failure
 * @param {string} query
 * @param {string} [reason]
 */
export function recordRetrievalFailure(query, reason = 'no_results') {
  return addError(`Retrieval failure for query: "${query}" | reason: ${reason}`, 'retrieval_failure', { query });
}

/**
 * Auto-record a storage failure
 * @param {string} text
 * @param {string} [error]
 */
export function recordStorageFailure(text, error = 'unknown') {
  return addError(`Storage failure: "${text?.slice(0,50)}..." | error: ${error}`, 'storage_failure', { text: text?.slice(0, 100) });
}

export default { addLearning, addError, getLearnings, getErrors, getStats, recordRetrievalFailure, recordStorageFailure };
