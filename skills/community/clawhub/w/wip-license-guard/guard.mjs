#!/usr/bin/env node
// wip-license-guard/hook.mjs
// PreToolUse hook for Claude Code.
// Blocks commits/pushes when license compliance fails.
// Checks: LICENSE file, copyright, CLA.md, README license section.

import { existsSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

function deny(reason) {
  const output = {
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: reason,
    },
  };
  process.stdout.write(JSON.stringify(output));
}

function findRepoRoot(startPath) {
  let dir = startPath;
  for (let i = 0; i < 20; i++) {
    if (existsSync(join(dir, '.git'))) return dir;
    const parent = join(dir, '..');
    if (parent === dir) break;
    dir = parent;
  }
  return null;
}

function checkLicenseCompliance(repoPath) {
  const issues = [];
  const configPath = join(repoPath, '.license-guard.json');

  // No config means license-guard hasn't been set up. Don't block.
  if (!existsSync(configPath)) return [];

  const config = JSON.parse(readFileSync(configPath, 'utf8'));

  // 1. LICENSE file must exist
  const licensePath = join(repoPath, 'LICENSE');
  if (!existsSync(licensePath)) {
    issues.push('LICENSE file is missing');
  } else {
    const licenseText = readFileSync(licensePath, 'utf8');

    // 2. Copyright must match
    if (!licenseText.includes(config.copyright)) {
      issues.push(`LICENSE copyright does not match "${config.copyright}"`);
    }

    // 3. Dual-license must include AGPL
    if (config.license === 'MIT+AGPL' && !licenseText.includes('AGPL') && !licenseText.includes('GNU Affero')) {
      issues.push('LICENSE is MIT-only but config requires MIT+AGPL');
    }
  }

  // 4. CLA.md should exist for repos with contributors
  if (!existsSync(join(repoPath, 'CLA.md'))) {
    issues.push('CLA.md is missing');
  }

  // 5. README must have license section
  const readmePath = join(repoPath, 'README.md');
  if (existsSync(readmePath)) {
    const readme = readFileSync(readmePath, 'utf8');
    if (!readme.includes('## License')) {
      issues.push('README.md missing ## License section');
    }
    if (config.license === 'MIT+AGPL' && !readme.includes('AGPL')) {
      issues.push('README.md License section missing AGPL reference');
    }
  }

  return issues;
}

// CLI mode: node hook.mjs --check [path]
if (process.argv.includes('--check')) {
  const path = process.argv[process.argv.indexOf('--check') + 1] || '.';
  const issues = checkLicenseCompliance(path);
  if (issues.length === 0) {
    console.log('  All license checks passed.');
    process.exit(0);
  } else {
    console.log('  License compliance issues:');
    for (const issue of issues) console.log(`    - ${issue}`);
    console.log('\n  Run `wip-license-guard check --fix` to auto-repair.');
    process.exit(1);
  }
}

async function main() {
  let raw = '';
  for await (const chunk of process.stdin) {
    raw += chunk;
  }

  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    process.exit(0);
  }

  const toolName = input.tool_name || '';

  // Only check on Bash tool calls that look like git commit or git push
  if (toolName !== 'Bash') {
    process.exit(0);
  }

  const command = input.tool_input?.command || '';

  // Check if this is a git commit or git push
  const isCommit = /\bgit\s+commit\b/.test(command);
  const isPush = /\bgit\s+push\b/.test(command);

  if (!isCommit && !isPush) {
    process.exit(0);
  }

  // Find repo root from cwd
  const cwd = input.tool_input?.cwd || process.cwd();
  const repoRoot = findRepoRoot(cwd);

  if (!repoRoot) {
    process.exit(0);
  }

  const issues = checkLicenseCompliance(repoRoot);

  if (issues.length > 0) {
    const issueList = issues.map(i => `  - ${i}`).join('\n');
    deny(
      `BLOCKED: License compliance check failed.\n${issueList}\n\nFix these issues before committing. Run \`wip-license-guard check --fix\` to auto-repair.`
    );
    process.exit(0);
  }

  // All good
  process.exit(0);
}

main().catch(() => process.exit(0));
