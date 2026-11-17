'use strict';

/**
 * 元阁本地使用记录（M1 特征来源之一）。
 *
 * 边界：
 * - 只记录技能 slug、信号类型、路由 playbook / confidence 与组合对。
 * - 不记录需求原文、记忆正文、文件内容、用户名、主机名或路径。
 * - 自动路由记录默认关闭；显式 mark 不要求先 enable。
 * - 文件默认 ~/.yottaskills/usage.json，YOTTA_SKILLS_USAGE_FILE 可覆盖。
 */

const fs = require('fs');
const os = require('os');
const path = require('path');

const SCHEMA = 1;
const SIGNALS = ['used', 'named', 'accepted'];
const MAX_COUNT = 999999;
const SLUG_RE = /^[a-z0-9][a-z0-9-]*$/;

function defaultState() {
  return {
    schema: SCHEMA,
    enabled: false,
    updated_at: '',
    skills: {},
    last_route: null,
  };
}

function usageFilePath(options) {
  const opts = options || {};
  if (opts.file) return path.resolve(opts.file);
  const fromEnv = String(process.env.YOTTA_SKILLS_USAGE_FILE || '').trim();
  if (fromEnv) return path.resolve(fromEnv);
  return path.join(opts.homeDir || os.homedir(), '.yottaskills', 'usage.json');
}

function bump(value) {
  const n = Number.isFinite(value) ? Math.floor(value) : 0;
  return Math.min(MAX_COUNT, Math.max(0, n) + 1);
}

function normalizeSkill(raw) {
  const skill = raw && typeof raw === 'object' && !Array.isArray(raw) ? raw : {};
  const pairs = {};
  if (skill.pairs && typeof skill.pairs === 'object' && !Array.isArray(skill.pairs)) {
    for (const key of Object.keys(skill.pairs)) {
      if (!SLUG_RE.test(key)) continue;
      const n = Number(skill.pairs[key]);
      if (Number.isFinite(n) && n > 0) pairs[key] = Math.min(MAX_COUNT, Math.floor(n));
    }
  }
  return {
    used: Math.min(MAX_COUNT, Math.max(0, Math.floor(Number(skill.used) || 0))),
    named: Math.min(MAX_COUNT, Math.max(0, Math.floor(Number(skill.named) || 0))),
    accepted: Math.min(MAX_COUNT, Math.max(0, Math.floor(Number(skill.accepted) || 0))),
    route_hits: Math.min(MAX_COUNT, Math.max(0, Math.floor(Number(skill.route_hits) || 0))),
    last_signal_at: typeof skill.last_signal_at === 'string' ? skill.last_signal_at : '',
    pairs,
  };
}

function normalizeState(raw) {
  if (!raw || typeof raw !== 'object' || Array.isArray(raw) || raw.schema !== SCHEMA) {
    return defaultState();
  }
  const state = defaultState();
  state.enabled = raw.enabled === true;
  state.updated_at = typeof raw.updated_at === 'string' ? raw.updated_at : '';
  if (raw.skills && typeof raw.skills === 'object' && !Array.isArray(raw.skills)) {
    for (const slug of Object.keys(raw.skills)) {
      if (!SLUG_RE.test(slug)) continue;
      state.skills[slug] = normalizeSkill(raw.skills[slug]);
    }
  }
  if (raw.last_route && typeof raw.last_route === 'object' && !Array.isArray(raw.last_route)) {
    const skills = Array.isArray(raw.last_route.skills)
      ? raw.last_route.skills.filter((slug) => typeof slug === 'string' && SLUG_RE.test(slug))
      : [];
    state.last_route = {
      at: typeof raw.last_route.at === 'string' ? raw.last_route.at : '',
      playbook: typeof raw.last_route.playbook === 'string' ? raw.last_route.playbook : '',
      confidence: typeof raw.last_route.confidence === 'string' ? raw.last_route.confidence : '',
      skills,
    };
  }
  return state;
}

function readUsage(options) {
  const file = usageFilePath(options);
  try {
    return normalizeState(JSON.parse(fs.readFileSync(file, 'utf8')));
  } catch (_) {
    return defaultState();
  }
}

function writeUsage(state, options) {
  const file = usageFilePath(options);
  const next = normalizeState(Object.assign(defaultState(), state));
  next.updated_at = new Date().toISOString();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  const tmp = file + '.tmp-' + process.pid + '-' + Date.now();
  fs.writeFileSync(tmp, JSON.stringify(next, null, 2) + '\n', 'utf8');
  try {
    fs.renameSync(tmp, file);
  } catch (_) {
    fs.rmSync(file, { force: true });
    fs.renameSync(tmp, file);
  }
  return file;
}

function setEnabled(enabled, options) {
  const state = readUsage(options);
  state.enabled = enabled === true;
  writeUsage(state, options);
  return state;
}

function ensureSkill(state, slug) {
  if (!state.skills[slug]) {
    state.skills[slug] = normalizeSkill({});
  }
  return state.skills[slug];
}

function markUsage(skill, signal, options) {
  const slug = String(skill || '').trim().toLowerCase();
  if (!SLUG_RE.test(slug)) throw new Error('非法 skill slug：' + String(skill || ''));
  if (SIGNALS.indexOf(signal) === -1) throw new Error('非法 signal：' + String(signal || ''));
  const state = readUsage(options);
  const record = ensureSkill(state, slug);
  record[signal] = bump(record[signal]);
  record.last_signal_at = new Date().toISOString();
  writeUsage(state, options);
  return state;
}

function uniqueSkills(skills) {
  const seen = new Set();
  const out = [];
  for (const item of Array.isArray(skills) ? skills : []) {
    const slug = String(item || '').trim().toLowerCase();
    if (!SLUG_RE.test(slug) || seen.has(slug)) continue;
    seen.add(slug);
    out.push(slug);
  }
  return out;
}

function recordRoute(input, options) {
  const state = readUsage(options);
  if (!state.enabled) return { recorded: false, reason: 'disabled' };
  const data = input && typeof input === 'object' ? input : {};
  const skills = uniqueSkills(data.skills);
  if (!skills.length) return { recorded: false, reason: 'empty' };
  for (const slug of skills) {
    const record = ensureSkill(state, slug);
    record.route_hits = bump(record.route_hits);
  }
  for (let i = 0; i < skills.length; i++) {
    for (let j = i + 1; j < skills.length; j++) {
      const left = ensureSkill(state, skills[i]);
      const right = skills[j];
      left.pairs[right] = bump(left.pairs[right]);
      const rightRecord = ensureSkill(state, right);
      rightRecord.pairs[skills[i]] = bump(rightRecord.pairs[skills[i]]);
    }
  }
  state.last_route = {
    at: new Date().toISOString(),
    playbook: typeof data.playbook === 'string' ? data.playbook : '',
    confidence: typeof data.confidence === 'string' ? data.confidence : '',
    skills,
  };
  writeUsage(state, options);
  return { recorded: true, skills };
}

function resetUsage(options) {
  const file = usageFilePath(options);
  fs.rmSync(file, { force: true });
  return file;
}

module.exports = {
  SCHEMA,
  SIGNALS,
  usageFilePath,
  defaultState,
  readUsage,
  writeUsage,
  setEnabled,
  markUsage,
  recordRoute,
  resetUsage,
};
