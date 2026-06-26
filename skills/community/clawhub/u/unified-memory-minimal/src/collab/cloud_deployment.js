/**
 * Cloud Deployment - Multi-node memory synchronization
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const CLOUD_DIR = join(MEMORY_DIR, 'cloud');

function getConfigFile() {
  mkdirSync(CLOUD_DIR, { recursive: true });
  return join(CLOUD_DIR, 'cloud_config.json');
}

function loadConfig() {
  const file = getConfigFile();
  if (!existsSync(file)) return { enabled: false, nodes: [], syncInterval: 60000 };
  try { return JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return { enabled: false, nodes: [], syncInterval: 60000 }; }
}

function saveConfig(config) {
  writeFileSync(getConfigFile(), JSON.stringify(config, null, 2), 'utf-8');
}

export function addNode(nodeId, endpoint) {
  const config = loadConfig();
  const node = { nodeId, endpoint, lastSync: new Date().toISOString(), status: 'offline', memoryCount: 0 };
  config.nodes.push(node);
  saveConfig(config);
  return node;
}

export function removeNode(nodeId) {
  const config = loadConfig();
  const idx = config.nodes.findIndex(n => n.nodeId === nodeId);
  if (idx === -1) return false;
  config.nodes.splice(idx, 1);
  saveConfig(config);
  return true;
}

export function getNodes() { return loadConfig().nodes; }

export function getSyncStatus() {
  const config = loadConfig();
  const online = config.nodes.filter(n => n.status === 'online').length;
  return { enabled: config.enabled, nodes: config.nodes.length, online };
}

export function printCloudStatus() {
  const status = getSyncStatus();
  console.log('\n☁️  Cloud Sync Status\n');
  console.log(`  Enabled: ${status.enabled ? '✅' : '❌'}`);
  console.log(`  Nodes: ${status.online}/${status.nodes} online`);
  console.log('');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'add' && args[1] && args[2]) { const node = addNode(args[1], args[2]); console.log(`✅ Added: ${node.nodeId}`); }
  else if (args[0] === 'remove' && args[1]) { const ok = removeNode(args[1]); console.log(ok ? '✅ Removed' : '❌ Not found'); }
  else printCloudStatus();
}
