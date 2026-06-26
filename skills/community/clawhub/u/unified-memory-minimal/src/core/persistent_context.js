/**
 * Persistent Context - Maintain context across sessions
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const CONTEXT_DIR = join(MEMORY_DIR, 'context');

function getContextFile() {
  mkdirSync(CONTEXT_DIR, { recursive: true });
  return join(CONTEXT_DIR, 'context.json');
}

function loadContext() {
  const file = getContextFile();
  if (!existsSync(file)) return { currentContext: {}, recentMemories: [], sessionHistory: [], lastUpdated: new Date().toISOString() };
  try { return JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return { currentContext: {}, recentMemories: [], sessionHistory: [], lastUpdated: new Date().toISOString() }; }
}

function saveContext(ctx) {
  ctx.lastUpdated = new Date().toISOString();
  writeFileSync(getContextFile(), JSON.stringify(ctx, null, 2), 'utf-8');
}

export function setContext(key, value) {
  const ctx = loadContext();
  ctx.currentContext[key] = value;
  saveContext(ctx);
}

export function getContext(key) {
  return loadContext().currentContext[key];
}

export function getAllContext() {
  return loadContext().currentContext;
}

export function deleteContext(key) {
  const ctx = loadContext();
  delete ctx.currentContext[key];
  saveContext(ctx);
}

export function addRecentMemory(memoryId, maxRecent = 50) {
  const ctx = loadContext();
  ctx.recentMemories = ctx.recentMemories.filter(id => id !== memoryId);
  ctx.recentMemories.unshift(memoryId);
  if (ctx.recentMemories.length > maxRecent) ctx.recentMemories = ctx.recentMemories.slice(0, maxRecent);
  saveContext(ctx);
}

export function getRecentMemories(limit = 10) {
  return loadContext().recentMemories.slice(0, limit);
}

export function startSession() {
  const ctx = loadContext();
  const sessionId = `session_${Date.now()}`;
  ctx.sessionHistory.push({ sessionId, startedAt: new Date().toISOString(), memoryCount: 0 });
  if (ctx.sessionHistory.length > 100) ctx.sessionHistory = ctx.sessionHistory.slice(-100);
  saveContext(ctx);
  return sessionId;
}

export function getSessionHistory(limit = 10) {
  const ctx = loadContext();
  return ctx.sessionHistory.slice(-limit).reverse();
}

export function printContextStatus() {
  const ctx = loadContext();
  console.log('\n📋 Persistent Context Status\n');
  console.log(`  Last Updated: ${ctx.lastUpdated}`);
  console.log(`  Context Keys: ${Object.keys(ctx.currentContext).length}`);
  console.log(`  Recent Memories: ${ctx.recentMemories.length}`);
  console.log(`  Sessions: ${ctx.sessionHistory.length}`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'sessions') {
    const sessions = getSessionHistory();
    console.log('\n📜 Session History:\n');
    for (const s of sessions) console.log(`  ${s.sessionId}: ${s.startedAt} - ${s.endedAt || 'ongoing'}`);
  }
  else printContextStatus();
}
