#!/usr/bin/env node
/**
 * setup-check.js
 * 
 * Validates environment setup for x-bookmark-triage skill.
 * Checks Node.js version, required env vars, and optional configuration.
 * 
 * Exit codes:
 *   0 = all checks passed
 *   1 = required var missing
 * 
 * Usage: node scripts/setup-check.js
 */

const nodeVersion = parseInt(process.version.slice(1).split('.')[0], 10);
let passed = 0;
let failed = 0;

console.log('\n═══ x-bookmark-triage Setup Check ═══\n');

// Check Node.js version
if (nodeVersion >= 18) {
  console.log('✓ Node.js version:', process.version);
  passed++;
} else {
  console.error('✗ Node.js >= 18 required (found:', process.version + ')');
  console.error('  Fix: Install Node.js 18 or later from https://nodejs.org');
  failed++;
}

// Required env vars
const required = [
  'DISCORD_BOT_TOKEN',
  'ANTHROPIC_DEFAULT_KEY',
  'X_OAUTH2_CLIENT_ID',
  'X_OAUTH2_CLIENT_SECRET',
  'X_OAUTH2_REFRESH_TOKEN'
];

for (const varName of required) {
  if (process.env[varName]) {
    console.log(`✓ ${varName}`);
    passed++;
  } else {
    console.error(`✗ ${varName} — REQUIRED`);
    failed++;
  }
}

// Optional but recommended env vars
const optional = [
  'KNOWLEDGE_INTAKE_CHANNEL_ID',
  'OPENCLAW_WORKSPACE'
];

console.log('\nOptional (recommended):');
for (const varName of optional) {
  if (process.env[varName]) {
    console.log(`✓ ${varName}`);
    passed++;
  } else {
    console.log(`○ ${varName} (will use default)`);
  }
}

// Summary
console.log(`\n═══ Summary ═══`);
console.log(`Passed: ${passed}`);
console.log(`Failed: ${failed}`);

if (failed > 0) {
  console.log('\n⚠️  Setup incomplete. Required env vars missing.');
  console.log('\nFix instructions:');
  console.log('1. Ensure all REQUIRED vars are set in your plist or environment');
  console.log('2. For launchd on macOS:');
  console.log('   - Edit: ~/Library/LaunchAgents/ai.openclaw.gateway.plist');
  console.log('   - Add missing env vars under EnvironmentVariables dict');
  console.log('   - Reload: launchctl unload ... && launchctl load ...');
  console.log('3. For cron/shell: export the vars before running scripts');
  process.exit(1);
}

console.log('\n✅ All required checks passed!\n');
process.exit(0);
