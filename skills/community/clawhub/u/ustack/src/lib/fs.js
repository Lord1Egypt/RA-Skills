import fs from 'node:fs';
import path from 'node:path';

export function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

export function writeJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

export function writeText(filePath, text) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  fs.writeFileSync(filePath, text, 'utf8');
}

export function readText(filePath) {
  return fs.readFileSync(filePath, 'utf8');
}

export function fileExists(filePath) {
  return fs.existsSync(filePath);
}

export function ensureDir(dirPath) {
  fs.mkdirSync(dirPath, { recursive: true });
}

export function getUstackDir(cwd) {
  return path.join(cwd, '.ustack');
}

export function getUpstreamDir(cwd, upstreamId) {
  return path.join(getUstackDir(cwd), 'upstreams', upstreamId);
}

export function getRunDir(cwd, upstreamId, timestamp) {
  return path.join(getUstackDir(cwd), 'runs', upstreamId, timestamp);
}

export function listRunDirs(cwd, upstreamId) {
  const runsBase = path.join(getUstackDir(cwd), 'runs', upstreamId);
  if (!fileExists(runsBase)) return [];
  return fs.readdirSync(runsBase).sort().reverse(); // newest first
}
