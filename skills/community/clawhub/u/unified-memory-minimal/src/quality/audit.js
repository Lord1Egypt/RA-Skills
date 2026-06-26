/**
 * Memory Audit - Track all memory operations
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const AUDIT_DIR = join(MEMORY_DIR, 'audit');

function getAuditFile() {
  mkdirSync(AUDIT_DIR, { recursive: true });
  return join(AUDIT_DIR, 'audit.json');
}

function loadAudit() {
  const file = getAuditFile();
  if (!existsSync(file)) {
    return { entries: [], stats: { totalOperations: 0, byAction: {}, byDate: {} } };
  }
  try { return JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return { entries: [], stats: { totalOperations: 0, byAction: {}, byDate: {} } }; }
}

function saveAudit(log) {
  writeFileSync(getAuditFile(), JSON.stringify(log, null, 2), 'utf-8');
}

export function audit(action, options = {}) {
  const log = loadAudit();
  
  const entry = {
    timestamp: new Date().toISOString(),
    action,
    memoryId: options.memoryId,
    userId: options.userId,
    sessionId: options.sessionId,
    details: options.details,
    metadata: options.metadata,
    success: options.success !== false,
    error: options.error,
  };
  
  log.entries.push(entry);
  log.stats.totalOperations++;
  log.stats.byAction[action] = (log.stats.byAction[action] || 0) + 1;
  const date = entry.timestamp.substring(0, 10);
  log.stats.byDate[date] = (log.stats.byDate[date] || 0) + 1;
  
  if (log.entries.length > 10000) log.entries = log.entries.slice(-10000);
  saveAudit(log);
}

export function queryAudit(options = {}) {
  const log = loadAudit();
  let entries = log.entries;
  
  if (options.action) entries = entries.filter(e => e.action === options.action);
  if (options.memoryId) entries = entries.filter(e => e.memoryId === options.memoryId);
  if (options.userId) entries = entries.filter(e => e.userId === options.userId);
  if (options.startDate) entries = entries.filter(e => e.timestamp >= options.startDate);
  if (options.endDate) entries = entries.filter(e => e.timestamp <= options.endDate);
  
  entries.sort((a, b) => b.timestamp.localeCompare(a.timestamp));
  if (options.limit) entries = entries.slice(0, options.limit);
  return entries;
}

export function getAuditStats() {
  return loadAudit().stats;
}

export function printAudit(limit = 20) {
  const entries = queryAudit({ limit });
  
  console.log('\n📋 Memory Audit Log\n');
  console.log('─'.repeat(80));
  console.log('Time'.padEnd(22), 'Action'.padEnd(14), 'Memory ID'.padEnd(12), 'Details');
  console.log('─'.repeat(80));
  
  for (const entry of entries) {
    console.log(
      entry.timestamp.padEnd(22),
      entry.action.padEnd(14),
      (entry.memoryId || '-').padEnd(12),
      (entry.details || '-').substring(0, 40)
    );
  }
  
  console.log('─'.repeat(80));
  const stats = getAuditStats();
  console.log(`\n📊 Total: ${stats.totalOperations} operations`);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'log' || args[0] === 'show') printAudit(parseInt(args[1] || '20'));
  else if (args[0] === 'stats') {
    const stats = getAuditStats();
    console.log('\n📊 Audit Statistics\n');
    console.log(`  Total Operations: ${stats.totalOperations}`);
    console.log('\n  By Action:');
    for (const [action, count] of Object.entries(stats.byAction)) console.log(`    ${action}: ${count}`);
  }
  else printAudit(20);
}
