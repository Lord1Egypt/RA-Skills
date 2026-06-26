/**
 * config.js — Skill configuration loader
 *
 * Priority: environment variables > data/config.json > defaults
 */

const fs = require('fs');
const path = require('path');

const CONFIG_FILE = path.join(__dirname, 'data', 'config.json');

let _cache = null;

function loadFileConfig() {
  if (_cache) return _cache;
  try {
    _cache = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf-8'));
  } catch {
    _cache = {};
  }
  return _cache;
}

function get(key, defaultValue) {
  // 1. Environment variable (e.g. EMAIL_SKILL_DEEPSEEK_API_KEY)
  const envKey = 'EMAIL_SKILL_' + key.toUpperCase().replace(/\./g, '_');
  if (process.env[envKey]) return process.env[envKey];

  // 2. Config file
  const file = loadFileConfig();
  if (file[key] !== undefined) return file[key];

  // 3. Default
  return defaultValue;
}

function set(key, value) {
  const file = loadFileConfig();
  file[key] = value;
  const dir = path.dirname(CONFIG_FILE);
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(file, null, 2));
  _cache = file;
}

function getAll() {
  return { ...loadFileConfig() };
}

module.exports = { get, set, getAll };
