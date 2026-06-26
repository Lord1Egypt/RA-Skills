/**
 * Weibull Decay Model for Memory Lifecycle
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

const DEFAULT_CONFIG = {
  baseHalfLifeDays: 30,
  reinforcementFactor: 0.5,
  maxMultiplier: 3.0,
};

let config = { ...DEFAULT_CONFIG };

function parseDate(dateStr) {
  if (!dateStr) return new Date();
  try { return new Date(dateStr.replace('Z', '+00:00')); }
  catch { return new Date(); }
}

function calculateHalfLife(memory) {
  const importance = memory.importance ?? 0.5;
  const accessCount = memory.access_count ?? 1;
  const importanceFactor = 0.5 + importance;
  const accessFactor = Math.min(1.0 + config.reinforcementFactor * Math.log1p(accessCount), config.maxMultiplier);
  return config.baseHalfLifeDays * importanceFactor * accessFactor;
}

export function calculateDecayScore(memory, currentTime) {
  const now = currentTime ?? new Date();
  const createdAt = parseDate(memory.created_at || memory.timestamp);
  const ageDays = (now.getTime() - createdAt.getTime()) / (1000 * 60 * 60 * 24);
  const beta = memory.decay_beta ?? 1.0;
  const halfLife = calculateHalfLife(memory);
  if (halfLife <= 0) return memory.importance ?? 0.5;
  const ratio = ageDays / halfLife;
  const decay = Math.exp(-Math.pow(ratio, beta));
  const baseScore = memory.importance ?? 0.5;
  return Math.max(0, baseScore * decay);
}

export function getTier(memory) {
  const score = calculateDecayScore(memory);
  const accessCount = memory.access_count ?? 0;
  if (score > 0.6 && accessCount > 10) return 'core';
  if (score > 0.3) return 'working';
  return 'peripheral';
}

export function applyDecay(memories) {
  const results = [];
  for (const mem of memories) {
    const decayScore = calculateDecayScore(mem);
    const halfLife = calculateHalfLife(mem);
    const createdAt = parseDate(mem.created_at || mem.timestamp);
    const ageDays = (Date.now() - createdAt.getTime()) / (1000 * 60 * 60 * 24);
    results.push({
      memoryId: mem.id || 'unknown',
      originalScore: mem.importance ?? 0.5,
      decayScore,
      halfLifeDays: Math.round(halfLife * 10) / 10,
      ageDays: Math.round(ageDays * 10) / 10,
      tier: getTier(mem),
    });
  }
  results.sort((a, b) => b.decayScore - a.decayScore);
  return results;
}

export function analyzeDecay(memories) {
  const results = applyDecay(memories);
  const tiers = { core: 0, working: 0, peripheral: 0 };
  let totalScore = 0;
  for (const r of results) {
    tiers[r.tier]++;
    totalScore += r.decayScore;
  }
  return {
    total: memories.length,
    tiers,
    avgScore: memories.length > 0 ? Math.round(totalScore / memories.length * 100) / 100 : 0,
  };
}

export function printDecayAnalysis() {
  const file = join(MEMORY_DIR, 'memories.json');
  let memories = [];
  if (existsSync(file)) { try { memories = JSON.parse(readFileSync(file, 'utf-8')); } catch {} }
  
  const analysis = analyzeDecay(memories);
  
  console.log('\n🔥 Weibull Decay Analysis\n');
  console.log(`  Config: base_half_life=${config.baseHalfLifeDays} days`);
  console.log(`  Total Memories: ${analysis.total}`);
  console.log(`  Average Decay Score: ${analysis.avgScore}\n`);
  console.log('  📊 Tier Distribution:');
  console.log(`    Core: ${analysis.tiers.core}`);
  console.log(`    Working: ${analysis.tiers.working}`);
  console.log(`    Peripheral: ${analysis.tiers.peripheral}`);
  console.log('');
}

if (require.main === module) {
  printDecayAnalysis();
}
