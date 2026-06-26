#!/usr/bin/env node
/**
 * 🔍 Storage Node Discovery
 * 
 * Discovers available storage nodes from the FilStream network.
 * Uses the index server's seeder registry + memory-store health probes.
 * 
 * Usage:
 *   node discover.mjs                    — discover and list available storage nodes
 *   node discover.mjs --register         — register local memory-store as a storage node
 *   node discover.mjs --update-config    — auto-update config.json with discovered nodes
 *   node discover.mjs --min-nodes 10     — require at least N healthy nodes
 * 
 * How it works:
 *   1. Query FilStream index server for registered seeders
 *   2. Probe each seeder's IP for a memory-store on port 8081
 *   3. Score nodes by: uptime, storage capacity, region diversity, latency
 *   4. Return top N nodes sorted by score
 * 
 * Created: 2026-03-03
 * Author: Rick 🦞 (Cortex Protocol)
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const CONFIG_PATH = resolve(__dirname, '..', 'config.json');

// FilStream index server — the bootstrap point for discovery
const INDEX_URL = process.env.FILSTREAM_INDEX || 'http://[2a05:a00:2::10:11]:8080';
const MEMORY_STORE_PORT = 8081;

// ── HTTP helper ──

async function probe(url, timeoutMs = 5000) {
  const start = Date.now();
  try {
    const resp = await fetch(url, { signal: AbortSignal.timeout(timeoutMs) });
    const latency = Date.now() - start;
    const text = await resp.text();
    try { return { ok: resp.ok, latency, data: JSON.parse(text) }; }
    catch { return { ok: resp.ok, latency, data: text }; }
  } catch (e) {
    return { ok: false, latency: Date.now() - start, error: e.message };
  }
}

// ── Discovery ──

async function discoverNodes(opts = {}) {
  const maxNodes = opts.maxNodes || 20;
  const probeTimeout = opts.probeTimeout || 5000;
  
  console.error(`🔍 Discovering storage nodes from ${INDEX_URL}...`);
  
  // Step 1: Get all seeders from the index
  const seedersResp = await probe(`${INDEX_URL}/api/seeders`, 10000);
  if (!seedersResp.ok) {
    console.error(`❌ Could not reach index server: ${seedersResp.error || 'unknown'}`);
    return [];
  }
  
  const seeders = seedersResp.data.seeders || [];
  console.error(`   Found ${seeders.length} registered seeders (${seeders.filter(s => s.status === 'active').length} active)`);
  
  // Step 2: Deduplicate by IPv6 (multiple seeders can run on same IP)
  const uniqueIPs = new Map();
  for (const seeder of seeders) {
    const ip = seeder.ipv6 || seeder.gateway_url;
    if (!ip) continue;
    // Keep the most recently active one per IP
    const existing = uniqueIPs.get(ip);
    if (!existing || new Date(seeder.last_seen) > new Date(existing.last_seen)) {
      uniqueIPs.set(ip, seeder);
    }
  }
  
  console.error(`   Unique IPs: ${uniqueIPs.size}`);
  
  // Step 3: Probe each unique IP for a memory-store on :8081
  const probeResults = await Promise.allSettled(
    [...uniqueIPs.entries()].map(async ([ip, seeder]) => {
      const url = `http://[${ip}]:${MEMORY_STORE_PORT}/health`;
      const health = await probe(url, probeTimeout);
      
      let stats = null;
      if (health.ok) {
        const statsResp = await probe(`http://[${ip}]:${MEMORY_STORE_PORT}/api/v1/stats`, probeTimeout);
        if (statsResp.ok) stats = statsResp.data;
      }
      
      return {
        ip,
        seeder,
        health,
        stats,
        hasStorage: health.ok,
      };
    })
  );
  
  // Step 4: Score and rank nodes
  const nodes = [];
  for (const result of probeResults) {
    if (result.status !== 'fulfilled') continue;
    const r = result.value;
    
    let score = 0;
    
    // Has a working memory store (+100)
    if (r.hasStorage) score += 100;
    
    // Active seeder status (+50)
    if (r.seeder.status === 'active') score += 50;
    
    // Low latency bonus (+30 for <100ms, +20 for <500ms, +10 for <1s)
    if (r.health.latency < 100) score += 30;
    else if (r.health.latency < 500) score += 20;
    else if (r.health.latency < 1000) score += 10;
    
    // Storage capacity bonus
    const storageGB = r.seeder.storage_gb || 0;
    if (storageGB >= 500) score += 20;
    else if (storageGB >= 100) score += 10;
    
    // Region diversity bonus (tracked by caller)
    const region = r.seeder.region || 'unknown';
    
    // Recent activity bonus
    const lastSeen = new Date(r.seeder.last_seen);
    const hoursSince = (Date.now() - lastSeen.getTime()) / (1000 * 60 * 60);
    if (hoursSince < 1) score += 20;
    else if (hoursSince < 24) score += 10;
    
    nodes.push({
      ip: r.ip,
      seederId: r.seeder.id,
      peerId: r.seeder.peer_id,
      region,
      storageGB,
      status: r.seeder.status,
      lastSeen: r.seeder.last_seen,
      hasStorage: r.hasStorage,
      latencyMs: r.health.latency,
      storageStats: r.stats,
      score,
      // Generate a config-ready node entry
      configEntry: r.hasStorage ? {
        id: `filstream-${r.ip.replace(/[^a-zA-Z0-9]/g, '-').replace(/-+/g, '-')}`,
        type: 'memory-store',
        url: `http://[${r.ip}]:${MEMORY_STORE_PORT}`,
        location: `${region} (${r.ip})`,
        priority: 10, // discovered nodes get lower priority than manually configured
        enabled: true,
        discovered: true,
        discoveredAt: new Date().toISOString(),
        seederId: r.seeder.id,
      } : null,
    });
  }
  
  // Sort by score descending
  nodes.sort((a, b) => b.score - a.score);
  
  // Apply region diversity: prefer spreading across regions
  const regionCounts = {};
  const diversified = [];
  const sameRegion = [];
  for (const node of nodes) {
    regionCounts[node.region] = (regionCounts[node.region] || 0) + 1;
    if (regionCounts[node.region] <= 3) { // max 3 per region
      diversified.push(node);
    } else {
      sameRegion.push(node);
    }
  }
  
  return [...diversified, ...sameRegion].slice(0, maxNodes);
}

// ── Update Config ──

async function updateConfig(discoveredNodes) {
  let config;
  if (existsSync(CONFIG_PATH)) {
    config = JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
  } else {
    config = { version: 1, replication: { min_replicas: 2, write_quorum: 1 }, nodes: [] };
  }
  
  // Keep manually configured nodes (not discovered)
  const manualNodes = config.nodes.filter(n => !n.discovered);
  
  // Extract all IPs already covered by manual nodes (including their URL)
  const manualIPs = new Set();
  for (const n of manualNodes) {
    const url = n.url || n.index_url || '';
    // Extract IPv6 from URL like http://[2a05:a00:2::10:11]:8081
    const ipMatch = url.match(/\[([^\]]+)\]/);
    if (ipMatch) manualIPs.add(ipMatch[1]);
  }
  
  // Add discovered nodes that DON'T overlap with manual ones
  const newNodes = discoveredNodes
    .filter(n => n.hasStorage && n.configEntry && !manualIPs.has(n.ip))
    .map(n => n.configEntry);
  
  const skipped = discoveredNodes.filter(n => n.hasStorage && manualIPs.has(n.ip)).length;
  if (skipped > 0) {
    console.error(`   Skipped ${skipped} discovered nodes (already in manual config)`);
  }
  
  config.nodes = [...manualNodes, ...newNodes];
  config.lastDiscovery = new Date().toISOString();
  config.discoveredNodeCount = newNodes.length;
  
  writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2));
  return config;
}

// ── CLI ──

function parseArgs() {
  const flags = {};
  const args = process.argv.slice(2);
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--update-config') flags.updateConfig = true;
    else if (args[i] === '--register') flags.register = true;
    else if (args[i] === '--max-nodes' && args[i + 1]) { flags.maxNodes = parseInt(args[++i]); }
    else if (args[i] === '--min-nodes' && args[i + 1]) { flags.minNodes = parseInt(args[++i]); }
    else if (args[i] === '--json') flags.json = true;
  }
  return flags;
}

async function main() {
  const flags = parseArgs();
  
  const nodes = await discoverNodes({ maxNodes: flags.maxNodes || 20 });
  
  const storageNodes = nodes.filter(n => n.hasStorage);
  const nonStorageNodes = nodes.filter(n => !n.hasStorage);
  
  if (flags.json) {
    console.log(JSON.stringify({ discovered: nodes, storage_capable: storageNodes.length, total_probed: nodes.length }, null, 2));
    return;
  }
  
  console.error(`\n📊 Discovery Results:`);
  console.error(`   Probed: ${nodes.length} unique IPs`);
  console.error(`   Storage-capable: ${storageNodes.length}`);
  console.error(`   Seeders only: ${nonStorageNodes.length}\n`);
  
  if (storageNodes.length > 0) {
    console.error(`🟢 Storage Nodes (have memory-store on :${MEMORY_STORE_PORT}):`);
    for (const n of storageNodes) {
      console.error(`   ${n.ip} | ${n.region} | ${n.latencyMs}ms | ${n.storageGB}GB | score: ${n.score} | ${n.storageStats ? `${n.storageStats.total_memories} memories` : 'empty'}`);
    }
  }
  
  if (nonStorageNodes.length > 0) {
    console.error(`\n⚪ Seeders Without Storage (need memory-store deployment):`);
    for (const n of nonStorageNodes) {
      console.error(`   ${n.ip} | ${n.region} | ${n.status} | ${n.storageGB}GB capacity`);
    }
  }
  
  if (flags.minNodes && storageNodes.length < flags.minNodes) {
    console.error(`\n⚠️  Only ${storageNodes.length} storage nodes found, need ${flags.minNodes}`);
    console.error(`   Deploy memory-store on more seeders to increase redundancy`);
  }
  
  if (flags.updateConfig) {
    const config = await updateConfig(nodes);
    console.error(`\n✅ Updated config.json: ${config.nodes.length} total nodes (${config.discoveredNodeCount} discovered)`);
  }
  
  // Output JSON summary to stdout for programmatic use
  console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    storage_nodes: storageNodes.length,
    seeders_without_storage: nonStorageNodes.length,
    total_probed: nodes.length,
    regions: [...new Set(nodes.map(n => n.region))],
    nodes: storageNodes.map(n => ({
      ip: n.ip, region: n.region, latencyMs: n.latencyMs, 
      storageGB: n.storageGB, score: n.score, seederId: n.seederId,
    })),
  }, null, 2));
}

main().catch(e => { console.error(`❌ ${e.message}`); process.exit(1); });
