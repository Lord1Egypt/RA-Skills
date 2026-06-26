/**
 * Memory Analytics - Usage analysis and insights
 */

import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const ANALYTICS_DIR = join(MEMORY_DIR, 'analytics');

export function generateAnalytics() {
  const memories = getAllMemories();
  
  const byCategory = {};
  const byDate = {};
  const tagCounts = {};
  let importanceHigh = 0, importanceMedium = 0, importanceLow = 0;
  let confidenceSum = 0, confidenceMin = 1, confidenceMax = 0;
  let totalAccess = 0;
  
  for (const mem of memories) {
    const cat = mem.category || 'unknown';
    
    if (!byCategory[cat]) {
      byCategory[cat] = { count: 0, avgImportance: 0, avgConfidence: 0, totalAccess: 0 };
    }
    byCategory[cat].count++;
    byCategory[cat].avgImportance += mem.importance || 0.5;
    byCategory[cat].avgConfidence += mem.confidence || 0.8;
    byCategory[cat].totalAccess += mem.access_count || 0;
    
    const date = (mem.created_at || mem.timestamp || '').substring(0, 10);
    if (date) byDate[date] = (byDate[date] || 0) + 1;
    
    if (Array.isArray(mem.tags)) {
      for (const tag of mem.tags) {
        tagCounts[tag] = (tagCounts[tag] || 0) + 1;
      }
    }
    
    const imp = mem.importance || 0.5;
    if (imp >= 0.7) importanceHigh++;
    else if (imp >= 0.4) importanceMedium++;
    else importanceLow++;
    
    const conf = mem.confidence || 0.8;
    confidenceSum += conf;
    confidenceMin = Math.min(confidenceMin, conf);
    confidenceMax = Math.max(confidenceMax, conf);
    
    totalAccess += mem.access_count || 0;
  }
  
  for (const cat in byCategory) {
    const stats = byCategory[cat];
    stats.avgImportance = Math.round(stats.avgImportance / stats.count * 100) / 100;
    stats.avgConfidence = Math.round(stats.avgConfidence / stats.count * 100) / 100;
  }
  
  const total = memories.length;
  
  return {
    totalMemories: total,
    byCategory,
    byDate,
    tagCounts,
    importanceDistribution: { high: importanceHigh, medium: importanceMedium, low: importanceLow },
    confidenceStats: {
      avg: total > 0 ? Math.round(confidenceSum / total * 100) / 100 : 0,
      min: confidenceMin,
      max: confidenceMax,
    },
    generatedAt: new Date().toISOString(),
  };
}

export function saveAnalytics() {
  mkdirSync(ANALYTICS_DIR, { recursive: true });
  const report = generateAnalytics();
  const file = join(ANALYTICS_DIR, `analytics_${Date.now()}.json`);
  writeFileSync(file, JSON.stringify(report, null, 2), 'utf-8');
  console.log(`📊 Analytics saved: ${file}`);
}

export function printAnalytics() {
  const report = generateAnalytics();
  
  console.log('\n📊 Memory Analytics\n');
  console.log(`  Total Memories: ${report.totalMemories}`);
  console.log(`  Generated: ${report.generatedAt}\n`);
  
  console.log('  📈 By Category:');
  for (const [cat, stats] of Object.entries(report.byCategory)) {
    console.log(
      `    ${cat.padEnd(12)} ${stats.count.toString().padStart(4)} memories  ` +
      `avg_imp: ${stats.avgImportance.toFixed(2)}  ` +
      `avg_conf: ${stats.avgConfidence.toFixed(2)}`
    );
  }
  
  console.log('\n  ⭐ Importance Distribution:');
  const dist = report.importanceDistribution;
  const total = dist.high + dist.medium + dist.low || 1;
  console.log(`    High (>=0.7):   ${dist.high.toString().padStart(4)} (${(dist.high / total * 100).toFixed(1)}%)`);
  console.log(`    Medium (0.4-0.7): ${dist.medium.toString().padStart(4)} (${(dist.medium / total * 100).toFixed(1)}%)`);
  console.log(`    Low (<0.4):    ${dist.low.toString().padStart(4)} (${(dist.low / total * 100).toFixed(1)}%)`);
  
  console.log('\n  🎯 Confidence Stats:');
  console.log(`    Average: ${report.confidenceStats.avg}`);
  console.log(`    Range:   ${report.confidenceStats.min} - ${report.confidenceStats.max}`);
  
  if (Object.keys(report.tagCounts).length > 0) {
    const topTags = Object.entries(report.tagCounts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5);
    
    console.log('\n  🏷️ Top Tags:');
    for (const [tag, count] of topTags) {
      console.log(`    ${tag.padEnd(20)} ${count}`);
    }
  }
  
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'generate' || args[0] === 'save') saveAnalytics();
  else printAnalytics();
}
