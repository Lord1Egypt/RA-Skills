/**
 * Memory Quality Assessment
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';
import { getAllMemories } from '../storage.js';


const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');

function evaluateContent(memory) {
  const text = memory.text || '';
  let score = 50;
  const issues = [];
  
  if (text.length < 10) { issues.push('Content too short'); score -= 20; }
  else if (text.length >= 50 && text.length <= 500) { score += 20; }
  else if (text.length > 1000) { issues.push('Content may be too long'); score -= 10; }
  
  if (text.length > 20) score += 10;
  if (/[。！？.!?]$/.test(text)) score += 10;
  else if (/[，,]$/.test(text)) { issues.push('Content appears truncated'); score -= 15; }
  
  return { score: Math.max(0, Math.min(100, score)), issues };
}

function evaluateStructure(memory) {
  let score = 50;
  const issues = [];
  
  if (memory.category && memory.category !== 'unknown') score += 20;
  else issues.push('Missing category');
  
  if (memory.importance !== undefined && memory.importance !== null) {
    if (memory.importance >= 0.3 && memory.importance <= 1.0) score += 15;
    else { issues.push('Importance out of range'); score -= 10; }
  } else issues.push('Missing importance');
  
  if (Array.isArray(memory.tags) && memory.tags.length > 0) score += 15;
  else issues.push('No tags');
  
  return { score: Math.max(0, Math.min(100, score)), issues };
}

export function evaluateMemory(memory) {
  const contentEval = evaluateContent(memory);
  const structEval = evaluateStructure(memory);
  
  const overall = Math.round(contentEval.score * 0.5 + structEval.score * 0.5);
  const allIssues = [...contentEval.issues, ...structEval.issues];
  
  return {
    memoryId: memory.id || 'unknown',
    overall,
    issues: allIssues,
    suggestions: allIssues.length > 0 ? allIssues.map(i => `Fix: ${i}`) : [],
  };
}

export function evaluateAll() {
  const memories = getAllMemories();
  const scored = memories.map(evaluateMemory);
  
  const distribution = { excellent: 0, good: 0, fair: 0, poor: 0 };
  const commonIssues = {};
  let totalScore = 0;
  
  for (const score of scored) {
    totalScore += score.overall;
    if (score.overall >= 90) distribution.excellent++;
    else if (score.overall >= 70) distribution.good++;
    else if (score.overall >= 50) distribution.fair++;
    else distribution.poor++;
    
    for (const issue of score.issues) commonIssues[issue] = (commonIssues[issue] || 0) + 1;
  }
  
  return {
    total: memories.length,
    averageScore: memories.length > 0 ? Math.round(totalScore / memories.length) : 0,
    distribution,
    commonIssues,
    scoredMemories: scored,
    generatedAt: new Date().toISOString(),
  };
}

export function getQualitySummary() {
  const report = evaluateAll();
  const score = report.averageScore;
  let grade, status;
  if (score >= 90) { grade = 'A'; status = 'Excellent'; }
  else if (score >= 80) { grade = 'B'; status = 'Good'; }
  else if (score >= 70) { grade = 'C'; status = 'Fair'; }
  else if (score >= 60) { grade = 'D'; status = 'Needs Improvement'; }
  else { grade = 'F'; status = 'Poor'; }
  return { score, grade, status };
}

export function printQualityReport() {
  const report = evaluateAll();
  
  console.log('\n📊 Memory Quality Report\n');
  console.log(`  Total Memories: ${report.total}`);
  console.log(`  Average Score: ${report.averageScore}/100\n`);
  
  console.log('  📈 Distribution:');
  const dist = report.distribution;
  const total = report.total || 1;
  console.log(`    Excellent (>=90): ${dist.excellent.toString().padStart(4)} (${(dist.excellent / total * 100).toFixed(1)}%)`);
  console.log(`    Good (70-89):     ${dist.good.toString().padStart(4)} (${(dist.good / total * 100).toFixed(1)}%)`);
  console.log(`    Fair (50-69):    ${dist.fair.toString().padStart(4)} (${(dist.fair / total * 100).toFixed(1)}%)`);
  console.log(`    Poor (<50):       ${dist.poor.toString().padStart(4)} (${(dist.poor / total * 100).toFixed(1)}%)`);
  
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'summary') {
    const { score, grade, status } = getQualitySummary();
    console.log(`\n📊 Quality Grade: ${grade} (${score}/100) - ${status}\n`);
  } else printQualityReport();
}
