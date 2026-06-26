#!/usr/bin/env node
/**
 * Skill Factory — Builds and publishes OpenClaw skills from pain point descriptions.
 * 
 * Usage:
 *   node factory.js build "description of the pain point"
 *   node factory.js from-error ERR-20260316    # build from .learnings entry
 *   node factory.js scan                        # find learnings ready for extraction
 *   node factory.js publish <skill-dir>         # package + publish to ClawHub
 * 
 * The factory generates: SKILL.md, scripts, tests, packages, and publishes.
 * It uses the LLM (you) as the engine — this script structures the workflow.
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

function getOptGlobal(name) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx !== -1 && process.argv[idx + 1] ? process.argv[idx + 1] : null;
}
const WORKSPACE = getOptGlobal('workspace') || process.env.WORKSPACE || process.cwd();
const SKILLS_DIR = path.join(WORKSPACE, 'skills/public');
const LEARNINGS_DIR = path.join(WORKSPACE, '.learnings');

const args = process.argv.slice(2);
const command = args[0];

// Scan .learnings/ for entries with 3+ recurrences
function scan() {
  const files = ['ERRORS.md', 'LEARNINGS.md'];
  const candidates = [];

  for (const file of files) {
    const filePath = path.join(LEARNINGS_DIR, file);
    if (!fs.existsSync(filePath)) continue;

    const content = fs.readFileSync(filePath, 'utf8');
    const entries = content.split(/^## \[/m).slice(1);

    for (const entry of entries) {
      const idMatch = entry.match(/^([\w-]+)\]/);
      const recMatch = entry.match(/\*\*Recurrences:\*\*\s*(\d+)/);
      const titleMatch = entry.match(/\]\s*(.+)/);
      const fixMatch = entry.match(/\*\*Fix:\*\*\s*(.+)/);
      const lessonMatch = entry.match(/\*\*The lesson:\*\*\s*(.+)/);

      if (!idMatch) continue;

      const recurrences = recMatch ? parseInt(recMatch[1]) : 1;
      const id = idMatch[1];
      const title = titleMatch ? titleMatch[1].trim() : 'Unknown';
      const fix = fixMatch ? fixMatch[1].trim() : lessonMatch ? lessonMatch[1].trim() : null;

      candidates.push({
        id,
        title,
        recurrences,
        fix,
        source: file,
        extractable: recurrences >= 3 && fix,
      });
    }
  }

  return candidates;
}

// Generate a slug from a description
function slugify(text) {
  return text.toLowerCase()
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .slice(0, 40)
    .replace(/-$/, '');
}

// Generate skill scaffold
function scaffold(slug, description) {
  const skillDir = path.join(SKILLS_DIR, slug);

  if (fs.existsSync(skillDir)) {
    console.error(`Skill directory already exists: ${skillDir}`);
    process.exit(1);
  }

  fs.mkdirSync(path.join(skillDir, 'scripts'), { recursive: true });

  // Generate SKILL.md prompt for the LLM
  const prompt = `
SKILL FACTORY — Generate a complete skill from this pain point:

"${description}"

GENERATE:
1. SKILL.md with frontmatter (name, description) and instructions
2. A Node.js script in scripts/ that solves the problem
3. Keep it zero-dependency (Node.js stdlib only)
4. Make it useful for ANY OpenClaw agent, not just the author

OUTPUT STRUCTURE:
  ${skillDir}/SKILL.md
  ${skillDir}/scripts/<name>.js

CONSTRAINTS:
- SKILL.md under 200 lines
- Script under 300 lines
- CLI interface with --help
- Exit codes: 0=success, 1=problem, 2=error
- Store data in .<slug>/ directory (relative to cwd)
`;

  // Write the prompt so the LLM can read it
  const promptPath = path.join(skillDir, '.factory-prompt.md');
  fs.writeFileSync(promptPath, prompt);

  console.log(`SCAFFOLD CREATED: ${skillDir}`);
  console.log(`\nNext steps:`);
  console.log(`1. Read ${promptPath}`);
  console.log(`2. Write SKILL.md and scripts based on the prompt`);
  console.log(`3. Test the script`);
  console.log(`4. Run: node factory.js publish ${skillDir}`);

  return { skillDir, promptPath };
}

// Package and publish
function publish(skillDir) {
  const resolvedDir = path.resolve(skillDir);
  
  if (!fs.existsSync(path.join(resolvedDir, 'SKILL.md'))) {
    console.error(`No SKILL.md found in ${resolvedDir}`);
    process.exit(2);
  }

  // Clean up factory files
  const promptFile = path.join(resolvedDir, '.factory-prompt.md');
  if (fs.existsSync(promptFile)) fs.unlinkSync(promptFile);

  // Extract slug from directory name
  const slug = path.basename(resolvedDir);

  // Read SKILL.md to get name
  const skillMd = fs.readFileSync(path.join(resolvedDir, 'SKILL.md'), 'utf8');
  const nameMatch = skillMd.match(/^name:\s*(.+)$/m);
  const name = nameMatch ? nameMatch[1].trim().replace(/^["']|["']$/g, '') : slug;

  console.log(`Publishing ${slug}...`);

  // Package
  try {
    const packageOut = execSync(
      `python3 /opt/homebrew/lib/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py "${resolvedDir}"`,
      { encoding: 'utf8', cwd: WORKSPACE }
    );
    console.log(packageOut);
  } catch (e) {
    console.error('Package failed:', e.message);
    process.exit(2);
  }

  // Publish
  try {
    const publishOut = execSync(
      `npx clawhub@latest publish "${resolvedDir}" --slug "${slug}" --name "${name}" --version 1.0.0 --tags "latest,agents"`,
      { encoding: 'utf8', cwd: WORKSPACE, timeout: 30000 }
    );
    console.log(publishOut);
  } catch (e) {
    console.error('Publish failed:', e.message);
    process.exit(2);
  }
}

// Main
switch (command) {
  case 'scan': {
    const candidates = scan();
    if (candidates.length === 0) {
      console.log('No learnings found.');
      break;
    }

    const extractable = candidates.filter(c => c.extractable);
    const pending = candidates.filter(c => !c.extractable);

    if (args.includes('--count')) {
      console.log(extractable.length);
      process.exit(extractable.length > 0 ? 2 : 0);
    }

    if (extractable.length > 0) {
      console.log(`\n🔧 READY FOR EXTRACTION (3+ recurrences + fix known):\n`);
      extractable.forEach(c => {
        console.log(`  [${c.id}] ${c.title} (${c.recurrences}x)`);
        console.log(`    Fix: ${c.fix}`);
        console.log(`    → node factory.js from-error ${c.id}\n`);
      });
    }

    if (pending.length > 0) {
      console.log(`\n📋 TRACKING (not yet extractable):\n`);
      pending.forEach(c => {
        console.log(`  [${c.id}] ${c.title} (${c.recurrences}x)${c.fix ? '' : ' — no fix yet'}`);
      });
    }

    console.log(`\n${extractable.length} ready, ${pending.length} tracking`);
    break;
  }

  case 'build': {
    const description = args.slice(1).join(' ');
    if (!description) {
      console.error('Usage: factory.js build "description of the pain point"');
      process.exit(2);
    }
    const slug = slugify(description);
    scaffold(slug, description);
    break;
  }

  case 'from-error': {
    const errorId = args[1];
    if (!errorId) {
      console.error('Usage: factory.js from-error <error-id>');
      process.exit(2);
    }

    const candidates = scan();
    const entry = candidates.find(c => c.id === errorId);
    if (!entry) {
      console.error(`Error ${errorId} not found in .learnings/`);
      process.exit(2);
    }

    const slug = slugify(entry.title);
    console.log(`Building skill from: [${entry.id}] ${entry.title}`);
    console.log(`Fix: ${entry.fix}`);
    scaffold(slug, `${entry.title}. Known fix: ${entry.fix}`);
    break;
  }

  case 'publish': {
    const dir = args[1];
    if (!dir) {
      console.error('Usage: factory.js publish <skill-directory>');
      process.exit(2);
    }
    publish(dir);
    break;
  }

  default:
    console.log(`Skill Factory — Build and publish OpenClaw skills from pain points

Commands:
  scan                          Scan .learnings/ for extractable patterns
  build "pain point"            Scaffold a new skill from a description
  from-error <id>               Build from a .learnings/ entry
  publish <dir>                 Package and publish to ClawHub

Workflow:
  1. Pain points accumulate in .learnings/ERRORS.md
  2. 'scan' identifies entries with 3+ recurrences
  3. 'from-error' scaffolds a skill from the entry
  4. You write the SKILL.md and script (LLM does this)
  5. 'publish' packages and ships to ClawHub

The factory builds the factory.`);
}
// Note: --count flag handled inline in scan case
