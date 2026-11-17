#!/usr/bin/env node
/**
 * Workspace Architect Skill - Create, Analyze, Optimize OpenClaw workspaces
 *
 * This skill helps create, analyze, and optimize OpenClaw workspace configuration files.
 * All work is done in a sandbox area without modifying originals.
 *
 * Guided workflows for:
 * - CREATE: New workspace files with structured questionnaires
 * - ANALYZE: Existing files for patterns and violations
 * - OPTIMIZE: Suggest improvements based on best practices
 *
 * See SKILL.md for complete workflows, guardrails, and examples.
 */

const fs = require('fs');
const path = require('path');

const SKILL_PATH = path.join(__dirname, 'SKILL.md');
const SANDBOX_DIR = path.join(__dirname, 'sandbox');
const REFERENCES_DIR = path.join(__dirname, 'references');

/**
 * Show help/documentation
 */
function showHelp() {
  if (fs.existsSync(SKILL_PATH)) {
    console.log(fs.readFileSync(SKILL_PATH, 'utf8'));
  } else {
    console.log('Workspace Architect - Create, Analyze, Optimize OpenClaw workspaces');
    console.log('');
    console.log('Capabilities:');
    console.log('  CREATE   - Create new workspace files with guided questionnaires');
    console.log('  ANALYZE  - Analyze existing files for patterns and violations');
    console.log('  OPTIMIZE - Suggest improvements based on best practices');
    console.log('');
    console.log('All work is done in a sandbox area without modifying originals.');
  }
}

/**
 * Show status information
 */
function showStatus() {
  console.log('🏗️  Workspace Architect Status');
  console.log('');
  console.log('Sandbox: ' + (fs.existsSync(SANDBOX_DIR) ? '✅ exists' : '❌ not found'));
  console.log('References: ' + (fs.existsSync(REFERENCES_DIR) ? '✅ exists' : '❌ not found'));
  console.log('');

  if (fs.existsSync(SANDBOX_DIR)) {
    const files = fs.readdirSync(SANDBOX_DIR);
    console.log('Files in sandbox: ' + files.length);
    files.forEach(file => {
      const filePath = path.join(SANDBOX_DIR, file);
      const stats = fs.statSync(filePath);
      console.log(`  ${file} (${stats.size} bytes)`);
    });
  }
}

/**
 * Show sizes of workspace files
 */
function analyzeWorkspace() {
  const workspacePath = path.join(process.env.HOME, '.openclaw', 'workspace');
  const files = ['SOUL.md', 'IDENTITY.md', 'USER.md', 'MEMORY.md', 'TOOLS.md'];

  console.log('📊 Workspace File Sizes');
  console.log('');

  if (!fs.existsSync(workspacePath)) {
    console.log('⚠️  Workspace not found: ' + workspacePath);
    return;
  }

  files.forEach(file => {
    const filePath = path.join(workspacePath, file);
    if (fs.existsSync(filePath)) {
      const stats = fs.statSync(filePath);
      console.log(`${file}: ${stats.size} bytes`);
    }
  });
}

// CLI handler
const args = process.argv.slice(2);
const command = args[0] || 'help';

switch (command) {
  case 'help':
  case '--help':
  case '-h':
    showHelp();
    break;

  case 'info':
  case 'status':
    showStatus();
    break;

  case 'analyze':
    analyzeWorkspace();
    break;

  case 'version':
    console.log('1.0.0');
    break;

  default:
    console.log(`Unknown command: ${command}`);
    console.log('Use "workspace-architect help" for usage information.');
    process.exit(1);
}
