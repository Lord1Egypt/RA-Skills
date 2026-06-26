/**
 * Version Control for Memories
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const VERSION_DIR = join(MEMORY_DIR, 'versions');

function getVersionFile(memoryId) {
  mkdirSync(VERSION_DIR, { recursive: true });
  return join(VERSION_DIR, `${memoryId}.json`);
}

function getHistoryFile() {
  mkdirSync(VERSION_DIR, { recursive: true });
  return join(VERSION_DIR, 'history.json');
}

export function createVersion(memory, action) {
  const versionId = `v_${Date.now()}_${Math.random().toString(36).substring(2, 6)}`;
  const version = {
    versionId,
    memoryId: memory.id || 'unknown',
    data: memory,
    timestamp: new Date().toISOString(),
    action,
  };
  
  const versionFile = getVersionFile(version.memoryId);
  let versions = [];
  if (existsSync(versionFile)) { try { versions = JSON.parse(readFileSync(versionFile, 'utf-8')); } catch {} }
  versions.push(version);
  if (versions.length > 100) versions = versions.slice(-100);
  writeFileSync(versionFile, JSON.stringify(versions, null, 2), 'utf-8');
  
  return version;
}

export function getVersionHistory(memoryId) {
  const file = getVersionFile(memoryId);
  if (!existsSync(file)) return [];
  try { return JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return []; }
}

export function getVersionStats() {
  const historyFile = getHistoryFile();
  if (!existsSync(historyFile)) return { totalMemories: 0, totalVersions: 0 };
  
  try {
    const history = JSON.parse(readFileSync(historyFile, 'utf-8'));
    const ids = Object.keys(history);
    let totalVersions = 0;
    for (const id of ids) totalVersions += history[id].length;
    return { totalMemories: ids.length, totalVersions };
  } catch {
    return { totalMemories: 0, totalVersions: 0 };
  }
}

export function printVersionStatus() {
  const stats = getVersionStats();
  console.log('\n📜 Version Control Status\n');
  console.log(`  Memories with versions: ${stats.totalMemories}`);
  console.log(`  Total versions: ${stats.totalVersions}`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'history' && args[1]) {
    const history = getVersionHistory(args[1]);
    console.log(`\n📜 History for ${args[1]}:\n`);
    for (const v of history) console.log(`  ${v.versionId} [${v.action}] ${v.timestamp}`);
  } else printVersionStatus();
}
