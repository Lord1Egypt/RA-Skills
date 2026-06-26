import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const skillRoot = path.resolve(__dirname, '..');
const openclawConfigPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');

function expandHome(p) {
  if (!p) return p;
  if (p === '~') return os.homedir();
  if (p.startsWith('~/')) return path.join(os.homedir(), p.slice(2));
  return p;
}

function deepMerge(base, extra) {
  if (!extra || typeof extra !== 'object' || Array.isArray(extra)) return base;
  const out = { ...base };
  for (const [k, v] of Object.entries(extra)) {
    if (v && typeof v === 'object' && !Array.isArray(v) && out[k] && typeof out[k] === 'object' && !Array.isArray(out[k])) {
      out[k] = deepMerge(out[k], v);
    } else {
      out[k] = v;
    }
  }
  return out;
}

function tryLoadOpenClawSkillConfig() {
  try {
    if (!fs.existsSync(openclawConfigPath)) return {};
    const raw = fs.readFileSync(openclawConfigPath, 'utf8');
    const parsed = vm.runInNewContext(`(${raw})`, {});
    return parsed?.skills?.entries?.['voice-tts']?.config || {};
  } catch {
    return {};
  }
}

export function getSkillRoot() {
  return skillRoot;
}

export function loadConfig() {
  const defaultPath = path.join(skillRoot, 'config.default.json');
  const userPath = process.env.VOICE_TTS_CONFIG || path.join(skillRoot, 'config.json');
  const defaults = JSON.parse(fs.readFileSync(defaultPath, 'utf8'));
  const openclawSkillConfig = tryLoadOpenClawSkillConfig();
  const user = fs.existsSync(userPath) ? JSON.parse(fs.readFileSync(userPath, 'utf8')) : {};
  const merged = deepMerge(deepMerge(defaults, openclawSkillConfig), user);
  merged.paths = Object.fromEntries(Object.entries(merged.paths || {}).map(([k, v]) => [k, expandHome(v)]));
  return merged;
}

export function resolveVoice({ agentId, explicitVoice, config }) {
  const ttsConfig = config.tts || {};
  if (explicitVoice) return explicitVoice;
  if (agentId && ttsConfig.agentVoices?.[agentId]) return ttsConfig.agentVoices[agentId];
  if (agentId && config.agentVoices?.[agentId]) return config.agentVoices[agentId];
  return ttsConfig.defaultVoice || config.defaultVoice;
}
