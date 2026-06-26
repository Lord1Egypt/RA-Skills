/**
 * TokenFlow Configuration Manager
 * Handles persistent user preferences across sessions
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_DIR = __dirname;
const CONFIG_PATH = join(CONFIG_DIR, 'config.json');

const DEFAULTS = {
  apiKey: '',
  apiUrl: 'https://tokenflow.fly.dev',
  filetypeBehavior: {
    docx:   { action: 'convert', askEachTime: false },
    xlsx:   { action: 'convert', askEachTime: true },
    pdf:    { action: 'convert', askEachTime: false },
    audio:  { action: 'convert', askEachTime: false },
  },
  outputFormat: 'markdown',
  maxRetries: 1,
  fallbackBehavior: 'use_file',
  firstRunComplete: false,
};

/**
 * Load config from disk, merging with defaults
 * @returns {Object}
 */
export function loadConfig() {
  try {
    if (existsSync(CONFIG_PATH)) {
      const raw = readFileSync(CONFIG_PATH, 'utf-8');
      const saved = JSON.parse(raw);
      return { ...DEFAULTS, ...saved };
    }
  } catch (err) {
    console.warn('TokenFlow config read failed, using defaults:', err.message);
  }
  return { ...DEFAULTS };
}

/**
 * Save config to disk atomically
 * @param {Object} prefs
 */
export function saveConfig(prefs) {
  try {
    if (!existsSync(CONFIG_DIR)) {
      mkdirSync(CONFIG_DIR, { recursive: true });
    }
    const merged = { ...loadConfig(), ...prefs };
    writeFileSync(CONFIG_PATH, JSON.stringify(merged, null, 2), { mode: 0o600 });
  } catch (err) {
    console.error('TokenFlow config save failed:', err.message);
    throw err;
  }
}

/**
 * Check if this is the first time the skill is being used
 * @returns {boolean}
 */
export function isFirstRun() {
  const config = loadConfig();
  return !config.firstRunComplete;
}

/**
 * Mark onboarding as complete
 */
export function markOnboardingComplete() {
  saveConfig({ firstRunComplete: true });
}

/**
 * Get filetype behavior for a given file
 * @param {string} filename
 * @returns {{action: string, askEachTime: boolean}}
 */
export function getFiletypeBehavior(filename) {
  const config = loadConfig();
  const ext = filename.split('.').pop()?.toLowerCase();
  const behaviors = config.filetypeBehavior || DEFAULTS.filetypeBehavior;

  let key = null;
  if (['docx', 'pptx'].includes(ext)) key = 'docx';
  else if (['xlsx', 'xls', 'csv'].includes(ext)) key = 'xlsx';
  else if (ext === 'pdf') key = 'pdf';
  // Note: standalone images are not supported; images are only extracted from PDFs
  else if (['wav', 'mp3', 'ogg', 'flac', 'm4a'].includes(ext)) key = 'audio';

  return key && behaviors[key] ? behaviors[key] : { action: 'convert', askEachTime: false };
}

/**
 * Get AGENTS.md formatted preference summary
 * @returns {string}
 */
export function getAgentsMdSummary() {
  const c = loadConfig();
  const b = c.filetypeBehavior || DEFAULTS.filetypeBehavior;
  return `## TokenFlow Preferences
- API: ${c.apiUrl}
- Output format: ${c.outputFormat}
- Filetype behaviors:
  - DOCX: ${b.docx?.action || 'convert'} (ask: ${b.docx?.askEachTime ? 'yes' : 'no'})
  - XLSX: ${b.xlsx?.action || 'convert'} (ask: ${b.xlsx?.askEachTime ? 'yes' : 'no'})
  - PDF: ${b.pdf?.action || 'convert'} (ask: ${b.pdf?.askEachTime ? 'yes' : 'no'})
  - Note: standalone images are not supported; images are only extracted from PDFs
  - Audio: ${b.audio?.action || 'convert'} (ask: ${b.audio?.askEachTime ? 'yes' : 'no'})
- Fallback: ${c.fallbackBehavior}
`;
}

export { DEFAULTS };
export default { loadConfig, saveConfig, isFirstRun, markOnboardingComplete, getFiletypeBehavior, getAgentsMdSummary };
