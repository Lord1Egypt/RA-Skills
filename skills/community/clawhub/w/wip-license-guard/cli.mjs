#!/usr/bin/env node
// wip-license-guard
// License compliance for your own repos.
// Ensures correct copyright, dual-license blocks, and LICENSE files.

import { existsSync, readFileSync, writeFileSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createInterface } from 'node:readline';
import { generateLicense, generateCLA, generateReadmeBlock, replaceReadmeLicenseSection, removeReadmeLicenseSection } from './core.mjs';

if (process.argv.includes('--version') || process.argv.includes('-v')) {
  const __dirname = dirname(fileURLToPath(import.meta.url));
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}

const args = process.argv.slice(2);
const HELP_FLAGS = ['--help', '-h', 'help'];
const command = HELP_FLAGS.some(f => args.includes(f)) ? 'help' : (args.find(a => !a.startsWith('--')) || 'check');
const target = args.find((a, i) => i > 0 && !a.startsWith('--')) || '.';
const FIX = args.includes('--fix');
const DRY_RUN = args.includes('--dry-run');
const QUIET = args.includes('--quiet');
const FROM_STANDARD = args.includes('--from-standard');

function log(msg) { if (!QUIET) console.log(msg); }
function ok(msg) { if (!QUIET) console.log(`  \u2713 ${msg}`); }
function warn(msg) { console.log(`  \u2717 ${msg}`); }

function ask(question) {
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(question, answer => {
      rl.close();
      resolve(answer.trim());
    });
  });
}

// WIP Computer standard defaults
const WIP_STANDARD = {
  copyright: 'WIP Computer, Inc.',
  license: 'MIT+AGPL',
  year: String(new Date().getFullYear()),
  attribution: 'Built by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).',
};

async function init(repoPath) {
  const configPath = join(repoPath, '.license-guard.json');

  // --from-standard: apply WIP Computer defaults without prompting
  if (FROM_STANDARD) {
    log('\n  wip-license-guard init --from-standard\n');

    const config = { ...WIP_STANDARD, created: new Date().toISOString() };

    writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
    ok(`Config saved to .license-guard.json`);

    const licensePath = join(repoPath, 'LICENSE');
    writeFileSync(licensePath, generateLicense(config, repoPath));
    ok(`LICENSE file generated (dual MIT+AGPLv3)`);

    const claPath = join(repoPath, 'CLA.md');
    if (!existsSync(claPath)) {
      writeFileSync(claPath, generateCLA(repoPath));
      ok(`CLA.md generated`);
    } else {
      ok(`CLA.md already exists`);
    }

    log(`\n  Standard: ${config.copyright}, ${config.license}, ${config.year}`);
    log(`  Done. Run \`wip-license-guard check\` to audit.\n`);
    return config;
  }

  if (existsSync(configPath)) {
    const existing = JSON.parse(readFileSync(configPath, 'utf8'));
    log(`\nLicense guard already configured:`);
    log(`  Copyright: ${existing.copyright}`);
    log(`  License: ${existing.license}`);
    log(`  Year: ${existing.year}`);
    const update = await ask('\nUpdate? (y/N) ');
    if (update.toLowerCase() !== 'y') {
      log('Keeping existing config.');
      return existing;
    }
  }

  log('\n  wip-license-guard init\n');

  const copyright = await ask('  Copyright holder (e.g. WIP Computer, Inc.): ');
  if (!copyright) {
    console.error('Copyright holder is required.');
    process.exit(1);
  }

  log('\n  License types:');
  log('    1. MIT only');
  log('    2. AGPLv3 only');
  log('    3. MIT + AGPLv3 dual-license (recommended for WIP repos)');
  const licenseChoice = await ask('\n  Choose (1/2/3): ');

  const licenseMap = { '1': 'MIT', '2': 'AGPL-3.0', '3': 'MIT+AGPL' };
  const license = licenseMap[licenseChoice] || 'MIT+AGPL';

  const currentYear = new Date().getFullYear();
  const yearInput = await ask(`  Copyright year (${currentYear}): `);
  const year = yearInput || String(currentYear);

  const attribution = await ask('  Attribution (e.g. Built by Parker Todd Brooks, ...): ');

  const config = { copyright, license, year, attribution, created: new Date().toISOString() };

  writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
  ok(`Config saved to .license-guard.json`);

  const licensePath = join(repoPath, 'LICENSE');
  const licenseText = generateLicense(config, repoPath);
  writeFileSync(licensePath, licenseText);
  ok(`LICENSE file generated`);

  // Generate CLA.md if it doesn't exist
  const claPath = join(repoPath, 'CLA.md');
  if (!existsSync(claPath)) {
    writeFileSync(claPath, generateCLA(repoPath));
    ok(`CLA.md generated`);
  }

  log(`\nDone. Run \`wip-license-guard check\` to audit.`);
  return config;
}

async function check(repoPath) {
  const configPath = join(repoPath, '.license-guard.json');

  if (!existsSync(configPath)) {
    log('\n  No .license-guard.json found.');
    const doInit = await ask('  Initialize license guard? (Y/n) ');
    if (doInit.toLowerCase() !== 'n') {
      await init(repoPath);
      return 0;
    }
    process.exit(1);
  }

  const config = JSON.parse(readFileSync(configPath, 'utf8'));
  let issues = 0;

  log(`\n  wip-license-guard check\n`);
  log(`  Copyright: ${config.copyright}`);
  log(`  License: ${config.license}\n`);

  // Check LICENSE file
  const licensePath = join(repoPath, 'LICENSE');
  if (!existsSync(licensePath)) {
    warn('LICENSE file missing');
    issues++;
    if (FIX) {
      writeFileSync(licensePath, generateLicense(config, repoPath));
      ok('LICENSE file created (--fix)');
      issues--;
    }
  } else {
    const licenseText = readFileSync(licensePath, 'utf8');

    if (!licenseText.includes(config.copyright)) {
      warn(`LICENSE copyright does not match "${config.copyright}"`);
      issues++;
      if (FIX) {
        writeFileSync(licensePath, generateLicense(config, repoPath));
        ok('LICENSE file updated (--fix)');
        issues--;
      }
    } else {
      ok('LICENSE copyright correct');
    }

    if (config.license === 'MIT+AGPL') {
      if (!licenseText.includes('AGPL') && !licenseText.includes('GNU Affero')) {
        warn('LICENSE file is MIT-only but config says MIT+AGPL');
        issues++;
        if (FIX) {
          writeFileSync(licensePath, generateLicense(config, repoPath));
          ok('LICENSE file updated to dual-license (--fix)');
          issues--;
        }
      } else {
        ok('LICENSE includes AGPLv3 terms');
      }
    }
  }

  // Check CLA.md
  const claPath = join(repoPath, 'CLA.md');
  if (!existsSync(claPath)) {
    warn('CLA.md missing');
    issues++;
    if (FIX) {
      writeFileSync(claPath, generateCLA(repoPath));
      ok('CLA.md created (--fix)');
      issues--;
    }
  } else {
    ok('CLA.md exists');
  }

  // Check README (license + structure standard)
  const readmePath = join(repoPath, 'README.md');
  if (existsSync(readmePath)) {
    const readme = readFileSync(readmePath, 'utf8');

    // License checks
    if (!readme.includes('## License')) {
      warn('README.md missing ## License section');
      issues++;
    } else {
      ok('README.md has License section');
    }

    if (config.license === 'MIT+AGPL' && !readme.includes('AGPL')) {
      warn('README.md License section missing AGPL reference');
      issues++;
    } else if (config.license === 'MIT+AGPL') {
      ok('README.md references AGPL');
    }

    // README structure standard checks
    if (!readme.match(/^#\s+\S/m)) {
      warn('README.md missing # title');
      issues++;
    } else {
      ok('README.md has title');
    }

    if (config.attribution && !readme.includes(config.attribution.split(',')[0])) {
      warn('README.md missing attribution');
      issues++;
    } else if (config.attribution) {
      ok('README.md has attribution');
    }

    // Warn if README contains content that belongs in TECHNICAL.md
    const technicalPatterns = [
      /## (Architecture|API|Config|Configuration|Build|Development Setup|Quick Start)/i,
      /```json\s*\n\s*\{[\s\S]*?"command"/,  // MCP config blocks
      /npm install -g /,  // install commands belong in TECHNICAL.md
    ];
    for (const pattern of technicalPatterns) {
      if (pattern.test(readme)) {
        warn('README.md contains technical content (move to TECHNICAL.md)');
        issues++;
        break;
      }
    }
  } else {
    warn('README.md not found');
    issues++;
  }

  // Check sub-tools (toolbox mode)
  const toolsDir = join(repoPath, 'tools');
  if (existsSync(toolsDir)) {
    try {
      const entries = readdirSync(toolsDir, { withFileTypes: true });
      for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        const toolPath = join(toolsDir, entry.name);
        const toolLicense = join(toolPath, 'LICENSE');

        if (!existsSync(toolLicense)) {
          warn(`tools/${entry.name}/LICENSE missing`);
          issues++;
          if (FIX) {
            writeFileSync(toolLicense, generateLicense(config, repoPath));
            ok(`tools/${entry.name}/LICENSE created (--fix)`);
            issues--;
          }
        } else {
          const text = readFileSync(toolLicense, 'utf8');
          if (!text.includes(config.copyright)) {
            warn(`tools/${entry.name}/LICENSE wrong copyright`);
            issues++;
            if (FIX) {
              writeFileSync(toolLicense, generateLicense(config, repoPath));
              ok(`tools/${entry.name}/LICENSE updated (--fix)`);
              issues--;
            }
          } else {
            ok(`tools/${entry.name}/LICENSE correct`);
          }
        }
      }
    } catch {}
  }

  log('');
  if (issues === 0) {
    log('  All checks passed.\n');
  } else {
    log(`  ${issues} issue(s) found. Run with --fix to auto-repair.\n`);
  }

  return issues;
}

async function readmeLicense(targetPath) {
  const mode = FIX ? '--fix' : DRY_RUN ? '--dry-run' : '';
  log(`\n  wip-license-guard readme-license${mode ? ' ' + mode : ''}\n`);

  // Detect if targetPath is a single repo or a directory of repos
  const repos = [];
  const configPath = join(targetPath, '.license-guard.json');
  if (existsSync(configPath)) {
    // Single repo
    repos.push(targetPath);
  } else {
    // Directory of repos (or nested categories like ldm-os/components/)
    const scanDir = (dir) => {
      try {
        for (const entry of readdirSync(dir, { withFileTypes: true })) {
          if (!entry.isDirectory() || entry.name.startsWith('.') || entry.name === 'node_modules' || entry.name === '_trash') continue;
          const sub = join(dir, entry.name);
          if (existsSync(join(sub, '.license-guard.json'))) {
            repos.push(sub);
          } else if (existsSync(join(sub, 'package.json')) || existsSync(join(sub, 'README.md'))) {
            repos.push(sub);
          } else {
            scanDir(sub); // recurse into category folders
          }
        }
      } catch {}
    };
    scanDir(targetPath);
  }

  if (repos.length === 0) {
    warn('No repos found. Point at a repo or a directory containing repos.');
    return 1;
  }

  log(`  Found ${repos.length} repo(s)\n`);

  let totalIssues = 0;

  for (const repoPath of repos) {
    const repoName = repoPath.split('/').pop();
    const repoConfig = join(repoPath, '.license-guard.json');
    const config = existsSync(repoConfig)
      ? JSON.parse(readFileSync(repoConfig, 'utf8'))
      : WIP_STANDARD;

    // 1. Check main README
    const readmePath = join(repoPath, 'README.md');
    if (existsSync(readmePath)) {
      const content = readFileSync(readmePath, 'utf8');
      const expected = generateReadmeBlock(config);

      if (content.includes('### Can I use this?') && content.includes('Dual-license model')) {
        ok(`${repoName}/README.md ... standard license block`);
      } else if (content.includes('## License')) {
        warn(`${repoName}/README.md ... non-standard license section`);
        totalIssues++;
        if (DRY_RUN) {
          // Extract current license section for preview
          const match = content.match(/## License[\s\S]*?(?=\n## [^#]|$)/);
          if (match) {
            log(`    current: ${match[0].split('\n').slice(0, 3).join(' | ').substring(0, 80)}...`);
          }
          log(`    would replace with: standard dual MIT/AGPLv3 block`);
        }
        if (FIX) {
          const updated = replaceReadmeLicenseSection(content, config, repoPath);
          writeFileSync(readmePath, updated);
          ok(`${repoName}/README.md ... updated to standard (--fix)`);
          totalIssues--;
        }
      } else {
        warn(`${repoName}/README.md ... missing ## License`);
        totalIssues++;
        if (DRY_RUN) {
          log(`    would add: standard dual MIT/AGPLv3 block at end of README`);
        }
        if (FIX) {
          const updated = replaceReadmeLicenseSection(content, config, repoPath);
          writeFileSync(readmePath, updated);
          ok(`${repoName}/README.md ... added standard block (--fix)`);
          totalIssues--;
        }
      }
    } else {
      warn(`${repoName}/README.md ... not found`);
      totalIssues++;
    }

    // 2. Check sub-tool READMEs (should NOT have license sections)
    const toolsDir = join(repoPath, 'tools');
    if (existsSync(toolsDir)) {
      try {
        for (const tool of readdirSync(toolsDir, { withFileTypes: true })) {
          if (!tool.isDirectory()) continue;
          const subReadme = join(toolsDir, tool.name, 'README.md');
          if (!existsSync(subReadme)) continue;

          const subContent = readFileSync(subReadme, 'utf8');
          if (subContent.includes('## License')) {
            warn(`${repoName}/tools/${tool.name}/README.md ... has license section (should be removed)`);
            totalIssues++;
            if (DRY_RUN) {
              log(`    would remove: ## License section from sub-tool README`);
            }
            if (FIX) {
              const cleaned = removeReadmeLicenseSection(subContent);
              writeFileSync(subReadme, cleaned);
              ok(`${repoName}/tools/${tool.name}/README.md ... license section removed (--fix)`);
              totalIssues--;
            }
          }
        }
      } catch {}
    }
  }

  log('');
  if (totalIssues === 0) {
    log('  All README license sections are correct.\n');
  } else if (DRY_RUN) {
    log(`  ${totalIssues} issue(s) found. Dry run complete. No changes made.`);
    log(`  Run with --fix to apply changes.\n`);
  } else {
    log(`  ${totalIssues} issue(s) found. Run with --dry-run to preview or --fix to apply.\n`);
  }

  return totalIssues;
}

// Main
if (command === 'init') {
  await init(target === 'init' ? '.' : target);
} else if (command === 'check') {
  const repoPath = (target === 'check') ? '.' : target;
  const issues = await check(repoPath);
  process.exit(issues > 0 ? 1 : 0);
} else if (command === 'readme-license') {
  const repoPath = (target === 'readme-license') ? '.' : target;
  const issues = await readmeLicense(repoPath);
  process.exit(issues > 0 ? 1 : 0);
} else if (command === '--help' || command === '-h' || command === 'help') {
  console.log(`
  wip-license-guard

  Commands:
    init [path]                Interactive setup. Asks license type, copyright, year.
    init --from-standard       Apply WIP Computer defaults (MIT+AGPL, CLA, attribution).
    check [path]               Audit repo against saved config. Exit 1 if issues found.
    check --fix [path]         Auto-fix issues (update LICENSE files, wrong copyright).
    readme-license [path]      Scan README license sections. Works on one repo or a directory of repos.
    readme-license --dry-run   Preview what would change. Shows current vs standard for each README.
    readme-license --fix       Apply standard license block to all READMEs. Remove from sub-tools.
    help                       Show this help.

  On first run, if no config exists, check will offer to run init.
  Use --from-standard for new WIP Computer repos (no prompts, just works).

  Config file: .license-guard.json (commit this to your repo)
  `);
} else {
  console.error(`Unknown command: ${command}. Run wip-license-guard help.`);
  process.exit(1);
}
