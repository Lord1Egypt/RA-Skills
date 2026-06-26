/**
 * clip-lib.js - 共享工具库
 * 供 markdown-clip.js 和 batch-clip.js 共用
 *
 * 路径说明：
 * - 优先使用 OPENCLAW_WORKSPACE 环境变量（跨平台兼容）
 * - 其次使用 USERPROFILE（Windows）/ HOME（Linux/Mac）
 * - 配置文件：~/.clips/config.json
 * - Clip 日志：~/.clips/clips.json
 */

const fs = require('fs');
const path = require('path');
const url = require('url');

// ─── 路径配置（修复硬编码）───────────────────────────────

function getClipsBaseDir() {
  // 优先 OPENCLAW_WORKSPACE（技能运行环境标准变量）
  const envDir = process.env.OPENCLAW_WORKSPACE
              || process.env.OPENCLAW_CLIPS
              || process.env.USERPROFILE
              || process.env.HOME
              || '';
  return envDir || path.dirname(__dirname); // 降级：技能目录
}

function getClipsDir() {
  return path.join(getClipsBaseDir(), '.clips');
}

function getConfigPath() {
  return path.join(getClipsDir(), 'config.json');
}

function getClipsLogPath() {
  return path.join(getClipsDir(), 'clips.json');
}

// ─── 配置文件 ─────────────────────────────────────────────────

const DEFAULT_CONFIG = {
  outputDir: '',
  skipDuplicates: true,
  autoOpen: false,
};

function loadConfig() {
  const cfgPath = getConfigPath();
  if (fs.existsSync(cfgPath)) {
    try {
      return { ...DEFAULT_CONFIG, ...JSON.parse(fs.readFileSync(cfgPath, 'utf8')) };
    } catch {}
  }
  return DEFAULT_CONFIG;
}

function saveConfig(cfg) {
  const dir = getClipsDir();
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(getConfigPath(), JSON.stringify(cfg, null, 2), 'utf8');
}

// ─── Clip Log ─────────────────────────────────────────────────

function loadClipsLog() {
  const logPath = getClipsLogPath();
  if (!fs.existsSync(logPath)) return {};
  try {
    return JSON.parse(fs.readFileSync(logPath, 'utf8'));
  } catch {
    return {};
  }
}

function saveClipsLog(log) {
  const dir = getClipsDir();
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(getClipsLogPath(), JSON.stringify(log, null, 2), 'utf8');
}

function recordClip(pageUrl, result) {
  const log = loadClipsLog();
  const key = normalizeUrl(pageUrl);
  log[key] = {
    url: pageUrl,
    path: result.path,
    title: result.metadata?.title || '',
    clippedAt: new Date().toISOString(),
  };
  saveClipsLog(log);
  return log[key].path;
}

function findClip(pageUrl) {
  const log = loadClipsLog();
  return log[normalizeUrl(pageUrl)] || null;
}

function isAlreadyClipped(pageUrl) {
  return findClip(pageUrl) !== null;
}

// ─── URL 工具 ─────────────────────────────────────────────────

function normalizeUrl(rawUrl) {
  try {
    const u = new url.URL(rawUrl);
    u.hash = '';
    const paramsToRemove = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content'];
    const searchParams = new URLSearchParams(u.search);
    paramsToRemove.forEach(p => searchParams.delete(p));
    const newSearch = searchParams.toString();
    // 修复：如果所有参数都被移除，不留尾随 ?
    u.search = newSearch;
    return u.toString().replace(/\?$/, '');
  } catch {
    return rawUrl;
  }
}

// ─── 文件名处理 ───────────────────────────────────────────────

function sanitizeFilename(name) {
  if (!name || !name.trim()) return 'untitled';
  return name
    .replace(/[<>:"/\\|?*\x00-\x1f]/g, '')
    .replace(/\s+/g, '-')
    .substring(0, 80)
    .trim('-');
}

function sanitizeFilenameRelaxed(name) {
  if (!name || !name.trim()) return 'untitled';
  return name
    .replace(/[<>:"/\\|?*\x00-\x1f]/g, '')
    .replace(/\n+/g, ' ')
    .replace(/\s+/g, '-')
    .substring(0, 80)
    .trim('-');
}

function buildFilename(pageUrl, title, ext) {
  const parsed = new url.URL(pageUrl);
  const domain = parsed.hostname.replace('www.', '').replace(/^m\./, '').replace(/\./g, '-');
  const date = new Date().toISOString().slice(0, 10);

  if (title) {
    const safeTitle = sanitizeFilenameRelaxed(title);
    return `${date}-${domain}-${safeTitle}${ext}`;
  }
  return `${date}-${domain}${ext}`;
}

// ─── 反爬 UA ─────────────────────────────────────────────────

const USER_AGENTS = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0',
];

function randomUA() {
  return USER_AGENTS[Math.floor(Math.random() * USER_AGENTS.length)];
}

module.exports = {
  getClipsDir,
  getConfigPath,
  getClipsLogPath,
  loadConfig,
  saveConfig,
  loadClipsLog,
  saveClipsLog,
  recordClip,
  findClip,
  isAlreadyClipped,
  normalizeUrl,
  sanitizeFilename,
  sanitizeFilenameRelaxed,
  buildFilename,
  randomUA,
  USER_AGENTS,
};
