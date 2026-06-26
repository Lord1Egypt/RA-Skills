#!/usr/bin/env node
/**
 * OpenClaw Installation Diagnostics
 * Run this script to identify common installation issues
 */

const { execSync, existsSync, readFileSync } = require('fs');
const fs = require('fs');
const path = require('path');
const os = require('os');

const CHECKS = [];
const HOME = os.homedir();
const OPENCLAW_DIR = path.join(HOME, '.openclaw');
const CONFIG_FILE = path.join(OPENCLAW_DIR, 'gateway.json');

function check(name, fn) {
  try {
    const result = fn();
    CHECKS.push({ name, status: '✅', message: result || 'OK' });
  } catch (err) {
    CHECKS.push({ name, status: '❌', message: err.message });
  }
}

console.log('\n🔍 OpenClaw Installation Diagnostics\n');
console.log('='.repeat(50));

// Check 1: Node.js version
check('Node.js Version', () => {
  const version = process.version;
  const major = parseInt(version.slice(1).split('.')[0]);
  if (major < 18) throw new Error(`Node ${version} - requires 18+`);
  return `Node ${version} ✓`;
});

// Check 2: OpenClaw directory
check('OpenClaw Directory', () => {
  if (!existsSync(OPENCLAW_DIR)) throw new Error('Directory not found');
  return `Found at ${OPENCLAW_DIR}`;
});

// Check 3: Gateway config
check('Gateway Config', () => {
  if (!existsSync(CONFIG_FILE)) throw new Error('gateway.json not found');
  const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
  return `Config exists with ${Object.keys(config).length} settings`;
});

// Check 4: Gateway status
check('Gateway Status', () => {
  try {
    const result = execSync('pgrep -f "openclaw gateway" || echo "not_running"', { encoding: 'utf8' });
    if (result.includes('not_running')) {
      return 'Gateway not running (run: openclaw gateway start)';
    }
    return 'Gateway running ✓';
  } catch {
    return 'Gateway not running (run: openclaw gateway start)';
  }
});

// Check 5: Port 3000
check('Port 3000', () => {
  try {
    const result = execSync('lsof -i :3000 2>/dev/null || echo "free"', { encoding: 'utf8' });
    if (result.includes('free')) return 'Port 3000 available ✓';
    return 'Port 3000 in use (check for conflicts)';
  } catch {
    return 'Port check skipped (lsof not available)';
  }
});

// Check 6: Environment
check('Environment', () => {
  const env = process.env;
  const hasModel = env.OPENAI_API_KEY || env.ANTHROPIC_API_KEY || env.DEEPSEEK_API_KEY;
  if (!hasModel) return 'No API keys detected (optional)';
  return 'API keys configured ✓';
});

// Print results
console.log('\n');
CHECKS.forEach(c => {
  console.log(`${c.status} ${c.name}: ${c.message}`);
});

const failed = CHECKS.filter(c => c.status === '❌');
console.log('\n' + '='.repeat(50));

if (failed.length === 0) {
  console.log('\n✅ All checks passed! OpenClaw looks healthy.\n');
} else {
  console.log(`\n⚠️  ${failed.length} issue(s) found:\n`);
  failed.forEach(c => console.log(`  - ${c.name}: ${c.message}`));
  console.log('\n💡 Need help? Visit: https://yang1002378395-cmyk.github.io/openclaw-install-service/\n');
}
