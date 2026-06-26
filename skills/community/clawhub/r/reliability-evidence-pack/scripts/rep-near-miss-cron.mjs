#!/usr/bin/env node
/**
 * REP Near-Miss Detector - Check for near-miss conditions
 * 
 * Usage:
 *   node rep-near-miss-cron.mjs [--output path/to/artifacts.jsonl]
 * 
 * Checks for:
 * - Failed cron jobs
 * - Subagent failures
 * - Validation errors in REP bundle
 * - High error rates
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Configuration
const DEFAULT_BUNDLE = path.join(__dirname, '..', 'rep-bundle', 'artifacts');
const DEFAULT_OUTPUT = path.join(DEFAULT_BUNDLE, 'near_miss_reliability_trailer.jsonl');

// Parse args
const args = process.argv.slice(2);
let outputPath = null;
let verbose = false;

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '--output' || arg === '-o') {
    outputPath = args[++i];
  } else if (arg === '--verbose' || arg === '-v') {
    verbose = true;
  } else if (arg === '--help' || arg === '-h') {
    console.log(`REP Near-Miss Detector

Usage:
  node rep-near-miss-cron.mjs [options]

Options:
  -o, --output <path>   Output file (default: rep-bundle/artifacts/near_miss_reliability_trailer.jsonl)
  -v, --verbose         Show detailed findings
  -h, --help           Show this help

Exit codes:
  0 - No near-misses detected (or emitted successfully)
  1 - Error during execution
`);
    process.exit(0);
  }
}

if (!outputPath) {
  const bundlePath = process.env.REP_BUNDLE_PATH || DEFAULT_BUNDLE;
  outputPath = path.join(bundlePath, 'near_miss_reliability_trailer.jsonl');
}

const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Check for near-miss conditions
async function checkNearMisses() {
  const findings = [];
  const workspace = process.env.OPENCLAW_WORKSPACE || path.join(__dirname, '..');
  
  // 1. Check subagent health log
  const subagentLog = path.join(workspace, 'memory', 'subagent-health.log');
  if (fs.existsSync(subagentLog)) {
    const content = fs.readFileSync(subagentLog, 'utf-8');
    const lines = content.trim().split('\n');
    const recentLines = lines.slice(-20); // Last 20 lines
    
    for (const line of recentLines) {
      if (line.includes('failed') || line.includes('error') || line.includes('timeout')) {
        findings.push({
          source: 'subagent-health',
          issue: line.substring(0, 200),
          severity: 'medium'
        });
      }
    }
  }
  
  // 2. Check openclaw healthchecks log
  const healthLog = path.join(workspace, 'openclaw-healthchecks.log');
  if (fs.existsSync(healthLog)) {
    const content = fs.readFileSync(healthLog, 'utf-8');
    const lines = content.trim().split('\n').filter(l => l.includes('FAIL') || l.includes('ERROR'));
    const recentFails = lines.slice(-10);
    
    for (const line of recentFails) {
      findings.push({
        source: 'healthcheck',
        issue: line.substring(0, 200),
        severity: 'high'
      });
    }
  }
  
  // 3. Check REP validation errors
  const repBundle = path.join(workspace, 'rep-bundle', 'artifacts');
  if (fs.existsSync(repBundle)) {
    const files = fs.readdirSync(repBundle).filter(f => f.endsWith('.jsonl'));
    
    for (const file of files) {
      const filePath = path.join(repBundle, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      const lines = content.trim().split('\n').filter(Boolean);
      
      // Check for malformed JSON
      for (const line of lines) {
        try {
          JSON.parse(line);
        } catch (e) {
          findings.push({
            source: 'rep-validation',
            issue: `Malformed JSON in ${file}: ${e.message}`,
            severity: 'high'
          });
        }
      }
    }
  }
  
  // 4. Check for recent cron failures
  const cronLog = path.join(workspace, 'memory', 'cron-failures.log');
  if (fs.existsSync(cronLog)) {
    const content = fs.readFileSync(cronLog, 'utf-8');
    const lines = content.trim().split('\n').slice(-5);
    
    for (const line of lines) {
      findings.push({
        source: 'cron',
        issue: line.substring(0, 200),
        severity: 'medium'
      });
    }
  }
  
  return findings;
}

// Generate artifact
function generateNearMiss(findings) {
  const incidentId = `nm-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`;
  
  // Assess potential impact based on findings
  const highSeverity = findings.filter(f => f.severity === 'high').length;
  const potentialImpact = highSeverity > 0 
    ? 'Potential system instability or data integrity risk' 
    : 'Minor operational issue, no immediate risk';
  
  const artifact = {
    rep_version: '0.3',
    artifact_type: 'near_miss_reliability_trailer',
    artifact_id: incidentId,
    session_id: process.env.OPENCLAW_SESSION_ID || 'system-cron',
    interaction_id: null,
    created_at: new Date().toISOString(),
    actor: {
      id: 'agent:christine',
      role: 'agent'
    },
    content_hash: '',
    prev_hash: null,
    
    // Near-miss specific fields
    incident_id: incidentId,
    potential_impact: potentialImpact,
    containment_action: 'Automated detection and logging',
    detection_method: 'cron-based near-miss detector',
    findings: findings,
    findings_count: findings.length,
    severity: highSeverity > 0 ? 'elevated' : 'normal'
  };
  
  // Compute content hash
  const canonical = JSON.stringify(artifact, Object.keys(artifact).sort());
  const hash = crypto.createHash('sha256').update(canonical).digest('hex');
  artifact.content_hash = `sha256:${hash.slice(0, 64)}`;
  
  return artifact;
}

// Main
async function main() {
  try {
    const findings = await checkNearMisses();
    
    if (verbose) {
      console.log(`Checked for near-miss conditions...`);
      console.log(`Found ${findings.length} potential issues`);
    }
    
    if (findings.length > 0) {
      const artifact = generateNearMiss(findings);
      fs.appendFileSync(outputPath, JSON.stringify(artifact) + '\n');
      
      console.log(`✓ Emitted near-miss artifact: ${artifact.incident_id}`);
      console.log(`  Findings: ${findings.length}`);
      console.log(`  Severity: ${artifact.severity}`);
      console.log(`  Output: ${outputPath}`);
      
      if (verbose) {
        console.log('\nFindings:');
        findings.forEach((f, i) => {
          console.log(`  ${i + 1}. [${f.severity}] ${f.source}: ${f.issue}`);
        });
      }
    } else {
      if (verbose) {
        console.log('No near-miss conditions detected.');
      }
    }
    
    process.exit(0);
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
