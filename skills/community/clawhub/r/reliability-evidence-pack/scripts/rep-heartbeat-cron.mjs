#!/usr/bin/env node
/**
 * REP Heartbeat Cron - Emit agent_heartbeat_record artifacts
 * 
 * Usage:
 *   node rep-heartbeat-cron.mjs [--output path/to/artifacts.jsonl]
 * 
 * Integrates with REP system to record agent health automatically.
 */

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Configuration
const DEFAULT_BUNDLE = path.join(__dirname, '..', 'rep-bundle', 'artifacts');
const DEFAULT_OUTPUT = path.join(DEFAULT_BUNDLE, 'agent_heartbeat_record.jsonl');

// Parse args
const args = process.argv.slice(2);
const opts = {
  output: null,
  bundle: null,
  status: 'healthy',
  seq: null
};

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '--output' || arg === '-o') {
    opts.output = args[++i];
  } else if (arg === '--bundle' || arg === '-b') {
    opts.bundle = args[++i];
  } else if (arg === '--status' || arg === '-s') {
    opts.status = args[++i];
  } else if (arg === '--seq') {
    opts.seq = parseInt(args[++i], 10);
  } else if (arg === '--help' || arg === '-h') {
    console.log(`REP Heartbeat Cron

Usage:
  node rep-heartbeat-cron.mjs [options]

Options:
  -o, --output <path>   Output file (default: rep-bundle/artifacts/agent_heartbeat_record.jsonl)
  -b, --bundle <dir>   Bundle directory (infers output path)
  -s, --status <status> Health status (default: healthy)
  -s, --seq <n>        Heartbeat sequence number
  -h, --help           Show this help

Environment:
  REP_BUNDLE_PATH      Override default bundle path
`);
    process.exit(0);
  }
}

// Determine output path
let outputPath = opts.output;
if (!outputPath) {
  const bundlePath = opts.bundle || process.env.REP_BUNDLE_PATH || DEFAULT_BUNDLE;
  outputPath = path.join(bundlePath, 'agent_heartbeat_record.jsonl');
}

// Ensure directory exists
const outputDir = path.dirname(outputPath);
if (!fs.existsSync(outputDir)) {
  fs.mkdirSync(outputDir, { recursive: true });
}

// Get existing artifact count for sequence
function getNextSequence(filePath) {
  if (!fs.existsSync(filePath)) return 1;
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.trim().split('\n').filter(Boolean);
  if (lines.length === 0) return 1;
  
  // Find max sequence
  let maxSeq = 0;
  for (const line of lines) {
    try {
      const artifact = JSON.parse(line);
      if (artifact.heartbeat_seq && artifact.heartbeat_seq > maxSeq) {
        maxSeq = artifact.heartbeat_seq;
      }
    } catch (e) {}
  }
  return maxSeq + 1;
}

// Get system uptime
function getUptime() {
  const uptime = process.uptime();
  return Math.floor(uptime);
}

// Generate artifact
function generateHeartbeat(status, seq) {
  const artifact = {
    rep_version: '0.3',
    artifact_type: 'agent_heartbeat_record',
    artifact_id: `hb-${Date.now()}-${Math.random().toString(36).slice(2, 6)}`,
    session_id: process.env.OPENCLAW_SESSION_ID || 'system-cron',
    interaction_id: null,
    created_at: new Date().toISOString(),
    actor: {
      id: 'agent:christine',
      role: 'agent'
    },
    content_hash: '',
    prev_hash: null,
    
    // Heartbeat-specific fields
    status: status,
    heartbeat_seq: seq,
    uptime_sec: getUptime(),
    last_activity: new Date().toISOString(),
    
    // Additional metadata
    node: process.env.HOSTNAME || 'unknown',
    pid: process.pid,
    memory_usage_mb: Math.round(process.memoryUsage().heapUsed / 1024 / 1024)
  };
  
  // Compute content hash
  const canonical = JSON.stringify(artifact, Object.keys(artifact).sort());
  const hash = crypto.createHash('sha256').update(canonical).digest('hex');
  artifact.content_hash = `sha256:${hash.slice(0, 64)}`;
  
  return artifact;
}

// Main execution
const status = opts.status || 'healthy';
const seq = opts.seq || getNextSequence(outputPath);
const artifact = generateHeartbeat(status, seq);

// Append to file
fs.appendFileSync(outputPath, JSON.stringify(artifact) + '\n');

console.log(`✓ Emitted heartbeat #${seq} to ${outputPath}`);
console.log(`  artifact_id: ${artifact.artifact_id}`);
console.log(`  status: ${artifact.status}`);
console.log(`  uptime: ${artifact.uptime_sec}s`);
