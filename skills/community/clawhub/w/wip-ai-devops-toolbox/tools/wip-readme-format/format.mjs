#!/usr/bin/env node
// wip-readme-format: reformat a repo's README to follow the WIP Computer standard.
//
// Usage:
//   wip-readme-format /path/to/repo              # generate README-init-*.md section files
//   wip-readme-format /path/to/repo --deploy     # assemble sections into README.md + TECHNICAL.md
//   wip-readme-format /path/to/repo --dry-run    # preview without writing
//   wip-readme-format /path/to/repo --check      # validate existing README, exit 0/1
//
// Generated files:
//   README-init-badges.md       Org header + interface badges
//   README-init-title.md        Title + tagline
//   README-init-teach.md        "Teach Your AI" onboarding block
//   README-init-features.md     Features list
//   README-init-coverage.md     Interface coverage table (toolbox only)
//   README-init-more-info.md    Links to docs
//   README-init-license.md      License block
//   README-init-technical.md    Technical content extracted from old README
//
// Workflow (same pattern as release notes):
//   1. wip-readme-format /path/to/repo        ... generates section files
//   2. Edit any section you want (e.g. README-init-license.md)
//   3. wip-readme-format /path/to/repo --deploy  ... assembles + moves into place

import { existsSync, readFileSync, writeFileSync, mkdirSync, unlinkSync, readdirSync } from 'node:fs';
import { join, resolve, basename, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { detectInterfaces, detectToolbox } from '../wip-universal-installer/detect.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));

if (process.argv.includes('--version') || process.argv.includes('-v')) {
  const pkg = JSON.parse(readFileSync(join(__dirname, 'package.json'), 'utf8'));
  console.log(pkg.version);
  process.exit(0);
}

const args = process.argv.slice(2);
const DRY_RUN = args.includes('--dry-run');
const CHECK = args.includes('--check');
const DEPLOY = args.includes('--deploy');
const target = args.find(a => !a.startsWith('--'));

function log(msg) { console.log(`  ${msg}`); }
function ok(msg) { console.log(`  \u2713 ${msg}`); }
function fail(msg) { console.error(`  \u2717 ${msg}`); }
function warn(msg) { console.log(`  ! ${msg}`); }

function readJSON(path) {
  try { return JSON.parse(readFileSync(path, 'utf8')); } catch { return null; }
}

function readFile(path) {
  try { return readFileSync(path, 'utf8'); } catch { return null; }
}

// Section order for assembly. "coverage" is optional (toolbox only).
// "technical" is separate (becomes TECHNICAL.md, not part of README).
const SECTION_ORDER = ['badges', 'title', 'teach', 'features', 'coverage', 'more-info', 'license'];

function initPath(repoPath, section) {
  return join(repoPath, `README-init-${section}.md`);
}

// ── Badge generation ──

const BADGE_MAP = {
  cli: { label: 'CLI', file: null },
  module: { label: 'Module', file: null },
  mcp: { label: 'MCP Server', file: 'mcp-server.mjs' },
  openclaw: { label: 'OpenClaw Plugin', file: 'openclaw.plugin.json' },
  skill: { label: 'Skill', file: 'SKILL.md' },
  claudeCodeHook: { label: 'Claude Code Hook', file: 'guard.mjs' },
};

function generateBadges(interfaces, repoUrl) {
  const badges = [];
  for (const [key, info] of Object.entries(interfaces)) {
    const meta = BADGE_MAP[key];
    if (!meta) continue;
    const label = meta.label.replace(/ /g, '_');
    const badge = `https://img.shields.io/badge/interface-${label}-black`;
    const link = meta.file && repoUrl
      ? `${repoUrl}/blob/main/${meta.file}`
      : repoUrl || '#';
    badges.push(`[![${meta.label}](${badge})](${link})`);
  }
  return badges.join(' ');
}

// ── Teach Your AI block ──

function generateTeachBlock(toolName, repoUrl, skillPath) {
  const skillUrl = repoUrl
    ? `${repoUrl}/blob/main/${skillPath || 'SKILL.md'}`
    : 'SKILL.md';
  const installCmd = repoUrl
    ? `wip-install ${repoUrl.replace('https://github.com/', '')} --dry-run`
    : `wip-install /path/to/repo --dry-run`;

  return `## Teach Your AI to Use ${toolName}

Open your AI and say:

\`\`\`
Read the SKILL.md at ${skillUrl.replace('https://', '')}.

Then explain to me:
1. What are these tools?
2. What do they do?
3. What would they change about how we work together?

Then ask me:
- Do you have more questions?
- Do you want to install them?

If I say yes, run: ${installCmd}

Show me exactly what will change on my system. When I'm ready, I'll tell you
to install for real.
\`\`\`

Your agent will read the repo, explain everything, and do a dry-run install first so you can see exactly what changes before anything is written to your system.`;
}

// ── Interface coverage table (toolbox mode) ──

function extractSkillName(toolPath) {
  const skillContent = readFile(join(toolPath, 'SKILL.md'));
  if (!skillContent) return null;
  const match = skillContent.match(/^---\s*\n[\s\S]*?^name:\s*(.+)/m);
  return match ? match[1].trim() : null;
}

function generateInterfaceTable(repoPath, subTools) {
  const rows = [];
  let num = 0;
  for (const tool of subTools) {
    num++;
    const { interfaces, pkg: toolPkg } = detectInterfaces(tool.path);
    const skillName = extractSkillName(tool.path);
    const name = skillName || (() => {
      const rawName = toolPkg?.name?.replace(/^@\w+\//, '').replace(/^wip-/, '') || tool.name;
      return rawName.split('-').map(w => {
        const lower = w.toLowerCase();
        if (['ai', 'api', 'cli', 'mcp', 'os', 'devops'].includes(lower)) return lower === 'devops' ? 'DevOps' : lower.toUpperCase();
        return w.charAt(0).toUpperCase() + w.slice(1);
      }).join(' ');
    })();
    const cli = interfaces.cli ? 'Y' : '';
    const mod = interfaces.module ? 'Y' : '';
    const mcp = interfaces.mcp ? 'Y' : '';
    const oc = interfaces.openclaw ? 'Y' : '';
    const skill = interfaces.skill ? 'Y' : '';
    const hook = interfaces.claudeCodeHook ? 'Y' : '';
    rows.push(`| ${num} | ${name} | ${cli} | ${mod} | ${mcp} | ${oc} | ${skill} | ${hook} |`);
  }

  return `## Interface Coverage

| # | Tool | CLI | Module | MCP | OC Plugin | Skill | CC Hook |
|---|------|-----|--------|-----|-----------|-------|---------|
${rows.join('\n')}`;
}

// ── Features extraction ──

function extractToolboxFeatures(subTools) {
  const features = [];
  for (const tool of subTools) {
    const pkg = readJSON(join(tool.path, 'package.json'));
    const name = pkg?.name?.replace(/^@\w+\//, '').replace(/^wip-/, '') || tool.name;
    const displayName = name.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    const desc = pkg?.description || '_No description_';
    features.push({ name: displayName, description: desc });
  }
  return features;
}

// ── License block ──

function generateLicenseBlock(repoPath) {
  const licenseGuard = readJSON(join(repoPath, '.license-guard.json'));
  if (licenseGuard) {
    return `## License

\`\`\`
MIT      All CLI tools, MCP servers, skills, and hooks (use anywhere, no restrictions).
AGPLv3   Commercial redistribution, marketplace listings, or bundling into paid services.
\`\`\`

AGPLv3 for personal use is free. Commercial licenses available.`;
  }

  const license = readFile(join(repoPath, 'LICENSE'));
  if (license) {
    const pkg = readJSON(join(repoPath, 'package.json'));
    return `## License

${pkg?.license || 'See LICENSE file.'}`;
  }

  return `## License

_No license information found. Run \`wip-license-guard init\` to set up licensing._`;
}

// ── More Info section ──

function generateMoreInfo(repoPath, repoUrl) {
  const links = [];

  if (existsSync(join(repoPath, 'TECHNICAL.md')) || existsSync(initPath(repoPath, 'technical'))) {
    const techLink = repoUrl ? `${repoUrl}/blob/main/TECHNICAL.md` : 'TECHNICAL.md';
    links.push(`- [Technical Documentation](${repoUrl ? techLink : 'TECHNICAL.md'}) ... Source code locations, build steps, development setup, architecture details`);
  }

  links.push(`- [Universal Interface Spec](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md) ... The six interfaces every agent-native tool can ship`);

  if (existsSync(join(repoPath, 'DEV-GUIDE-GENERAL-PUBLIC.md'))) {
    links.push(`- [Dev Guide](DEV-GUIDE-GENERAL-PUBLIC.md) ... Best practices for AI-assisted development`);
  }

  return `## More Info

${links.join('\n')}`;
}

// ── Existing README content extraction ──

function extractExistingContent(readmePath) {
  const content = readFile(readmePath);
  if (!content) return {};

  const sections = {};
  let currentSection = '_preamble';
  let currentContent = [];

  for (const line of content.split('\n')) {
    const headingMatch = line.match(/^##\s+(.+)/);
    if (headingMatch) {
      sections[currentSection] = currentContent.join('\n').trim();
      currentSection = headingMatch[1].trim().toLowerCase();
      currentContent = [];
    } else {
      currentContent.push(line);
    }
  }
  sections[currentSection] = currentContent.join('\n').trim();

  return sections;
}

// ── Technical content detection ──

function isTechnicalContent(section) {
  const techKeywords = [
    'architecture', 'api', 'endpoint', 'build', 'development setup',
    'configuration', 'schema', 'database', 'migration', 'deployment',
    'docker', 'environment variable', 'debugging',
  ];
  const lower = section.toLowerCase();
  return techKeywords.some(k => lower.includes(k));
}

// ── Main ──

if (!target || target === '--help' || target === '-h') {
  console.log('');
  console.log('  wip-readme-format ... reformat a README to follow the WIP Computer standard');
  console.log('');
  console.log('  Usage:');
  console.log('    wip-readme-format /path/to/repo              generate README-init-*.md section files');
  console.log('    wip-readme-format /path/to/repo --deploy     assemble sections, back up old, move into place');
  console.log('    wip-readme-format /path/to/repo --dry-run    preview without writing');
  console.log('    wip-readme-format /path/to/repo --check      validate existing README');
  console.log('');
  console.log('  Workflow:');
  console.log('    1. wip-readme-format /path/to/repo              ... generates section files');
  console.log('    2. Edit any section (e.g. README-init-license.md)');
  console.log('    3. wip-readme-format /path/to/repo --deploy     ... assembles into README.md');
  console.log('');
  console.log('  Section files (in assembly order):');
  console.log('    README-init-badges.md       Org header + interface badges');
  console.log('    README-init-title.md        Title + tagline');
  console.log('    README-init-teach.md        "Teach Your AI" onboarding block');
  console.log('    README-init-features.md     Features list');
  console.log('    README-init-coverage.md     Interface coverage table (toolbox only)');
  console.log('    README-init-more-info.md    Links to docs');
  console.log('    README-init-license.md      License block + built-by line');
  console.log('    README-init-technical.md    Technical content (becomes TECHNICAL.md)');
  console.log('');
  process.exit(0);
}

const repoPath = resolve(target);
if (!existsSync(repoPath)) {
  fail(`Path not found: ${repoPath}`);
  process.exit(1);
}

const pkg = readJSON(join(repoPath, 'package.json'));
const { interfaces } = detectInterfaces(repoPath);
const subTools = detectToolbox(repoPath);
const isToolbox = subTools.length > 0;

// Determine repo URL from package.json
let repoUrl = null;
if (pkg?.repository?.url) {
  repoUrl = pkg.repository.url
    .replace('git+', '')
    .replace('.git', '');
}

// Tool name: human-readable
const toolName = pkg?.name?.replace(/^@\w+\//, '').replace(/^wip-/, '') || basename(repoPath);
const ACRONYMS = ['ai', 'api', 'cli', 'mcp', 'os', 'pr', 'ui', 'url', 'devops'];
const displayName = toolName
  .split('-')
  .map(w => {
    const lower = w.toLowerCase();
    if (ACRONYMS.includes(lower)) return lower === 'devops' ? 'DevOps' : lower.toUpperCase();
    return w.charAt(0).toUpperCase() + w.slice(1);
  })
  .join(' ');

const tagline = pkg?.description || '_What it solves in human words. Not what it is technically._';

const readmePath = join(repoPath, 'README.md');
const technicalPath = join(repoPath, 'TECHNICAL.md');
const existing = extractExistingContent(readmePath);

// ── Deploy mode ──

if (DEPLOY) {
  console.log('');
  console.log('  wip-readme-format --deploy');
  console.log(`  Target: ${repoPath}`);
  console.log(`  ${'─'.repeat(40)}`);

  // Check that at least the badges section exists
  if (!existsSync(initPath(repoPath, 'badges'))) {
    fail('No README-init-*.md files found. Run wip-readme-format first to generate them.');
    process.exit(1);
  }

  // Safety: init files must be reviewed (committed or modified) before deploy.
  // If all init files are untracked (just generated, never reviewed), block.
  try {
    const { execSync } = await import('node:child_process');
    const initFiles = readdirSync(repoPath).filter(f => f.startsWith('README-init-'));
    const allUntracked = initFiles.every(f => {
      try {
        const status = execSync(`git status --porcelain "${f}"`, { cwd: repoPath, encoding: 'utf8' }).trim();
        return status.startsWith('??');
      } catch { return false; }
    });
    if (allUntracked && initFiles.length > 0) {
      fail('Init files have not been reviewed. They are all untracked (just generated).');
      console.log('  Review the README-init-*.md files, edit as needed, then git add them before deploying.');
      console.log('  Or commit them first so there is a review trail.');
      process.exit(1);
    }
  } catch {}


  const date = new Date().toISOString().slice(0, 10);
  const aiTrash = join(repoPath, 'ai', '_trash');

  // Back up existing README.md
  const oldReadme = readFile(readmePath);
  if (oldReadme) {
    if (!existsSync(aiTrash)) mkdirSync(aiTrash, { recursive: true });
    writeFileSync(join(aiTrash, `README--before-format--${date}.md`), oldReadme);
    ok('Backed up README.md to ai/_trash/');
  }

  // Back up existing TECHNICAL.md
  const oldTech = readFile(technicalPath);
  if (oldTech) {
    if (!existsSync(aiTrash)) mkdirSync(aiTrash, { recursive: true });
    writeFileSync(join(aiTrash, `TECHNICAL--before-format--${date}.md`), oldTech);
    ok('Backed up TECHNICAL.md to ai/_trash/');
  }

  // Assemble README from sections in order
  const readmeParts = [];
  for (const section of SECTION_ORDER) {
    const sectionPath = initPath(repoPath, section);
    const content = readFile(sectionPath);
    if (content) {
      readmeParts.push(content.trimEnd());
      unlinkSync(sectionPath);
      ok(`  ${section} -> README.md`);
    }
  }

  if (readmeParts.length === 0) {
    fail('No section files found to assemble.');
    process.exit(1);
  }

  writeFileSync(readmePath, readmeParts.join('\n\n') + '\n');
  ok('Assembled README.md');

  // Move technical -> TECHNICAL.md
  const techPath = initPath(repoPath, 'technical');
  if (existsSync(techPath)) {
    const techContent = readFileSync(techPath, 'utf8');
    writeFileSync(technicalPath, techContent);
    unlinkSync(techPath);
    ok('README-init-technical.md -> TECHNICAL.md');
  }

  console.log(`  ${'─'.repeat(40)}`);
  ok('Deployed. Old files in ai/_trash/.\n');
  process.exit(0);
}

// ── Check mode ──

if (CHECK) {
  console.log('');
  console.log('  wip-readme-format --check');
  console.log(`  Target: ${repoPath}`);
  console.log(`  ${'─'.repeat(40)}`);

  const content = readFile(readmePath);
  if (!content) {
    fail('No README.md found');
    process.exit(1);
  }

  let passed = true;
  const required = ['teach your ai', 'features', 'more info', 'license'];
  const sectionNames = Object.keys(existing).filter(k => k !== '_preamble');

  for (const section of required) {
    const found = sectionNames.some(s => s.includes(section));
    if (found) {
      ok(`Has "${section}" section`);
    } else {
      fail(`Missing "${section}" section`);
      passed = false;
    }
  }

  if (content.includes('img.shields.io/badge/interface')) {
    ok('Has interface badges');
  } else {
    fail('Missing interface badges');
    passed = false;
  }

  if (isToolbox) {
    if (content.includes('Interface Coverage') || content.includes('interface coverage')) {
      ok('Has interface coverage table');
    } else {
      fail('Missing interface coverage table (toolbox repo)');
      passed = false;
    }
  }

  // Check for stale staging files
  const stale = SECTION_ORDER.concat(['technical']).filter(s => existsSync(initPath(repoPath, s)));
  if (stale.length > 0) {
    warn(`${stale.length} README-init-*.md file(s) found. Run --deploy to assemble.`);
  }

  console.log(`  ${'─'.repeat(40)}`);
  if (passed) {
    ok('README follows the standard');
    process.exit(0);
  } else {
    fail('README does not follow the standard');
    process.exit(1);
  }
}

// ── Generate mode (default) ──

console.log('');
console.log(`  wip-readme-format${DRY_RUN ? ' (dry run)' : ''}`);
console.log(`  Target: ${repoPath}`);
console.log(`  ${'─'.repeat(40)}`);
log(`Package: ${pkg?.name || 'unknown'}`);
log(`Interfaces: ${Object.keys(interfaces).join(', ') || 'none'}`);
if (isToolbox) log(`Toolbox: ${subTools.length} sub-tools`);
console.log('');

// ── Build each section ──

const sections = {};

// 1. Badges
let allInterfaces = { ...interfaces };
if (isToolbox) {
  for (const tool of subTools) {
    const { interfaces: subIfaces } = detectInterfaces(tool.path);
    for (const key of Object.keys(subIfaces)) {
      if (!allInterfaces[key]) allInterfaces[key] = subIfaces[key];
    }
  }
}
const badges = generateBadges(allInterfaces, repoUrl);
const specBadge = `[![Universal Interface Spec](https://img.shields.io/badge/Universal_Interface_Spec-black?style=flat&color=black)](https://github.com/wipcomputer/wip-ai-devops-toolbox/blob/main/tools/wip-universal-installer/SPEC.md)`;
const badgeLines = ['###### WIP Computer', ''];
if (badges) badgeLines.push(badges + ' ' + specBadge);
else badgeLines.push(specBadge);
sections.badges = badgeLines.join('\n');

// 2. Title + tagline
sections.title = `# ${displayName}\n\n${tagline}`;

// 3. Teach Your AI
const skillPath = interfaces.skill ? 'SKILL.md' : null;
if (skillPath || isToolbox) {
  sections.teach = generateTeachBlock(displayName, repoUrl, skillPath);
}

// 4. Features
const featureKeys = Object.keys(existing).filter(k =>
  k.includes('features') || k.includes('feature')
);
const existingFeatures = featureKeys.length > 0 ? existing[featureKeys[0]] : null;

if (existingFeatures) {
  sections.features = `## Features\n\n${existingFeatures}`;
} else if (isToolbox) {
  const toolFeatures = extractToolboxFeatures(subTools);
  const lines = ['## Features', ''];
  for (const f of toolFeatures) {
    lines.push(`**${f.name}**`);
    lines.push(`- ${f.description}`, '');
  }
  sections.features = lines.join('\n').trimEnd();
} else {
  sections.features = `## Features\n\n_Describe what this tool does for the user. Human-readable. Name, description, stability tag._`;
}

// 5. Interface Coverage (toolbox only)
if (isToolbox) {
  sections.coverage = generateInterfaceTable(repoPath, subTools);
}

// 6. More Info
sections['more-info'] = generateMoreInfo(repoPath, repoUrl);

// 7. License + built-by
sections.license = generateLicenseBlock(repoPath) +
  '\n\nBuilt by Parker Todd Brooks, Lēsa (OpenClaw, Claude Opus 4.6), Claude Code (Claude Opus 4.6).';

// 8. Technical (separate file, becomes TECHNICAL.md)
const techSections = [];
for (const [name, content] of Object.entries(existing)) {
  if (name === '_preamble') continue;
  if (isTechnicalContent(content)) {
    techSections.push(`## ${name.charAt(0).toUpperCase() + name.slice(1)}\n\n${content}`);
  }
}
if (techSections.length > 0) {
  const existingTech = readFile(technicalPath) || `# ${displayName} ... Technical Documentation\n\n`;
  sections.technical = existingTech.trimEnd() + '\n\n' + techSections.join('\n\n');
}

// ── Output ──

if (DRY_RUN) {
  for (const section of SECTION_ORDER) {
    if (!sections[section]) continue;
    console.log(`  ── README-init-${section}.md ──\n`);
    console.log(sections[section]);
    console.log('');
  }
  if (sections.technical) {
    console.log(`  ── README-init-technical.md ──\n`);
    console.log(`  (${techSections.length} section(s) extracted from old README)`);
  }
  console.log(`\n  ${'─'.repeat(40)}`);
  console.log('  Dry run complete. No files written.\n');
} else {
  let count = 0;
  for (const section of SECTION_ORDER) {
    if (!sections[section]) continue;
    writeFileSync(initPath(repoPath, section), sections[section] + '\n');
    ok(`README-init-${section}.md`);
    count++;
  }
  if (sections.technical) {
    writeFileSync(initPath(repoPath, 'technical'), sections.technical + '\n');
    ok('README-init-technical.md');
    count++;
  }

  console.log(`  ${'─'.repeat(40)}`);
  ok(`${count} section files written. Edit any, then run with --deploy.\n`);
}
