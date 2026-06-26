/**
 * Multi-Tenant Memory - Isolated memory spaces
 */

import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';

const WORKSPACE = join(process.env.HOME || '/root', '.openclaw', 'workspace');
const MEMORY_DIR = join(WORKSPACE, 'memory');
const TENANT_DIR = join(MEMORY_DIR, 'tenants');

function getConfigFile() {
  mkdirSync(TENANT_DIR, { recursive: true });
  return join(TENANT_DIR, 'tenant_config.json');
}

function loadConfig() {
  const file = getConfigFile();
  if (!existsSync(file)) return { currentTenant: 'default', tenants: {} };
  try { return JSON.parse(readFileSync(file, 'utf-8')); }
  catch { return { currentTenant: 'default', tenants: {} }; }
}

function saveConfig(config) {
  writeFileSync(getConfigFile(), JSON.stringify(config, null, 2), 'utf-8');
}

function getTenantMemoryFile(tenantId) {
  return join(TENANT_DIR, `${tenantId}.json`);
}

export function createTenant(id, name) {
  const config = loadConfig();
  const tenant = { id, name, memoryFile: getTenantMemoryFile(id), createdAt: new Date().toISOString(), memoryCount: 0 };
  config.tenants[id] = tenant;
  saveConfig(config);
  writeFileSync(tenant.memoryFile, JSON.stringify([], null, 2), 'utf-8');
  return tenant;
}

export function switchTenant(tenantId) {
  const config = loadConfig();
  if (!config.tenants[tenantId]) return false;
  config.currentTenant = tenantId;
  saveConfig(config);
  return true;
}

export function getCurrentTenant() {
  const config = loadConfig();
  return config.tenants[config.currentTenant] || null;
}

export function listTenants() {
  return Object.values(loadConfig().tenants);
}

export function printTenantStatus() {
  const current = getCurrentTenant();
  const tenants = listTenants();
  console.log('\n🏢 Multi-Tenant Status\n');
  console.log(`  Current: ${current?.name || 'none'} (${current?.id || 'none'})`);
  console.log(`  Total Tenants: ${tenants.length}\n`);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args[0] === 'create' && args[1] && args[2]) { const t = createTenant(args[1], args[2]); console.log(`✅ Created: ${t.name}`); }
  else if (args[0] === 'switch' && args[1]) { const ok = switchTenant(args[1]); console.log(ok ? `✅ Switched to ${args[1]}` : '❌ Not found'); }
  else printTenantStatus();
}
