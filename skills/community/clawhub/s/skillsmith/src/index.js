import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';

export const TOOL = 'skill-starter';
export const VERSION = '0.1.0';

function nowIso() {
  return new Date().toISOString();
}

function makeEnvelope(status, data = {}, errors = []) {
  return {
    tool: TOOL,
    version: VERSION,
    timestamp: nowIso(),
    status,
    data,
    errors
  };
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

function sanitizeName(raw) {
  return raw
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9-_]+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '');
}

function ensureDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function writeFile(projectRoot, relativePath, content) {
  const target = path.join(projectRoot, relativePath);
  ensureDir(target);
  fs.writeFileSync(target, content, 'utf8');
  return relativePath;
}

async function prompt(question, fallback) {
  const rl = readline.createInterface({ input, output });
  try {
    const answer = await rl.question(`${question}${fallback ? ` (${fallback})` : ''}: `);
    const value = answer.trim();
    return value || fallback;
  } finally {
    rl.close();
  }
}

function toSingleLine(value) {
  return String(value ?? '').replace(/\s+/g, ' ').trim();
}

function buildSkillMd({ name, description }) {
  const normalizedDescription = JSON.stringify(toSingleLine(description));
  return `---
name: ${name}
description: ${normalizedDescription}
metadata: {"openclaw":{"emoji":"🛠️","requires":{"bins":["node"]}}}
---

# ${name}

Provide purpose-built instructions for ${name}.

## When to use

- Use when a task clearly matches the scope of ${name}.
- Use when the caller needs the local scripts, fixtures, or docs that ship with this skill.
- Do not use when a generic skill already covers the job better.

## Local references

- Skill root: \`{baseDir}\`
- Docs: \`{baseDir}/docs/README.md\`
- Scripts: \`{baseDir}/scripts\`
- Fixtures: \`{baseDir}/fixtures\`

## Validation examples

\`\`\`bash
node {baseDir}/tests/smoke.test.js
node {baseDir}/scripts/profile-target.js {baseDir}/fixtures/profile-input.json
\`\`\`

## Safety

- Principle of least privilege
- Explicitly document side effects and external calls
- Keep requirements in frontmatter metadata so OpenClaw can evaluate availability
`;
}

function buildCiWorkflow() {
  return `name: security-scan

on:
  pull_request:
  push:
    branches: [ main ]

jobs:
  clawshield:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx clawshield scan . --format table --fail-on caution
`;
}

function buildProfileTarget() {
  return `#!/usr/bin/env node
import fs from 'node:fs';

const inputPath = process.argv[2];
const payload = JSON.parse(fs.readFileSync(inputPath, 'utf8'));
const base = payload && typeof payload === 'object' ? payload : {};
const steps = Array.isArray(base.steps) ? base.steps : [
  { name: 'bootstrap', durationMs: 25, memoryMb: 8, apiCalls: 0, ioReadBytes: 512, ioWriteBytes: 64 }
];

const metrics = steps.map((step) => ({
  key: step.name,
  scope: step.name,
  value: Number(step.durationMs || 0),
  unit: 'ms'
}));

console.log(JSON.stringify({
  steps,
  metrics,
  apiCalls: steps.reduce((acc, item) => acc + Number(item.apiCalls || 0), 0),
  ioReadBytes: steps.reduce((acc, item) => acc + Number(item.ioReadBytes || 0), 0),
  ioWriteBytes: steps.reduce((acc, item) => acc + Number(item.ioWriteBytes || 0), 0)
}));
`;
}

export function generateProject(options) {
  const warnings = [];
  const files = [];

  const template = options.template || 'standard';
  const includeCI = Boolean(options.includeCI || template === 'strict-security');

  files.push(
    writeFile(
      options.projectRoot,
      'package.json',
      `${JSON.stringify(
        {
          name: options.name,
          version: '0.1.0',
          private: true,
          type: 'module',
          scripts: {
            lint: "node -e \"console.log('lint placeholder')\"",
            test: "node tests/smoke.test.js"
          }
        },
        null,
        2
      )}\n`
    )
  );

  files.push(writeFile(options.projectRoot, 'SKILL.md', buildSkillMd(options)));
  files.push(writeFile(options.projectRoot, 'docs/README.md', '# Docs\n\nAdd architecture and security notes.\n'));
  files.push(writeFile(options.projectRoot, 'scripts/README.md', '# Scripts\n\nPlace executable scripts here.\n'));
  files.push(writeFile(options.projectRoot, '.env.example', 'OPENCLAW_API_KEY=\n'));
  files.push(writeFile(options.projectRoot, 'CHANGELOG.md', '# Changelog\n\n## 0.1.0\n- Initial scaffold\n'));
  files.push(
    writeFile(
      options.projectRoot,
      'tests/smoke.test.js',
      "import assert from 'node:assert/strict';\nassert.equal(1 + 1, 2);\nconsole.log('smoke test passed');\n"
    )
  );
  files.push(writeFile(options.projectRoot, 'scripts/profile-target.js', buildProfileTarget()));
  files.push(
    writeFile(
      options.projectRoot,
      'fixtures/profile-input.json',
      `${JSON.stringify({
        steps: [
          { name: 'load', durationMs: 35, memoryMb: 10, apiCalls: 1, ioReadBytes: 1024, ioWriteBytes: 128 },
          { name: 'process', durationMs: 55, memoryMb: 18, apiCalls: 2, ioReadBytes: 512, ioWriteBytes: 256 }
        ]
      }, null, 2)}\n`
    )
  );

  if (includeCI) {
    files.push(writeFile(options.projectRoot, '.github/workflows/security-scan.yml', buildCiWorkflow()));
  }

  if (template === 'strict-security') {
    files.push(
      writeFile(
        options.projectRoot,
        '.openclaw-tools/safe-install.policy.json',
        `${JSON.stringify(
          {
            defaultAction: 'prompt',
            blockedPatterns: ['curl\\\\s*\\\\|\\\\s*sh'],
            allowedSources: ['verified'],
            forceRequiredForAvoid: true
          },
          null,
          2
        )}\n`
      )
    );
    files.push(
      writeFile(
        options.projectRoot,
        'docs/security.md',
        '# Security\n\nThis template is strict-security. Integrate ClawShield and Safe Install policy checks.\n'
      )
    );
  }

  if (!includeCI) {
    warnings.push('CI workflow was not generated. Use --ci to include security scanning workflow.');
  }

  return {
    projectRoot: options.projectRoot,
    template,
    files,
    warnings
  };
}

function printHelp() {
  console.log(`create-openclaw-skill usage:
  create-openclaw-skill <name> [--template <standard|strict-security>] [--ci] [--no-prompts] [--force] [--out <dir>] [--format <table|json>]`);
}

export async function runCli(argv) {
  const args = parseArgs(argv);
  const format = args.format || 'table';
  if (!args._[0] || args.help) {
    printHelp();
    return args.help ? 0 : 1;
  }

  try {
    const noPrompts = Boolean(args['no-prompts']);
    const template = args.template || 'standard';
    if (!['standard', 'strict-security'].includes(template)) {
      console.error(JSON.stringify(makeEnvelope('error', {}, ['--template must be standard|strict-security']), null, 2));
      return 1;
    }

    const sanitized = sanitizeName(args._[0]);
    if (!sanitized) {
      console.error(JSON.stringify(makeEnvelope('error', {}, ['Invalid skill name']), null, 2));
      return 1;
    }

    const rootOut = path.resolve(args.out || process.cwd());
    const projectRoot = path.join(rootOut, sanitized);

    if (fs.existsSync(projectRoot) && !args.force) {
      console.error(
        JSON.stringify(
          makeEnvelope('error', {}, [`Target directory already exists: ${projectRoot}. Use --force to overwrite.`]),
          null,
          2
        )
      );
      return 1;
    }

    if (fs.existsSync(projectRoot) && args.force) {
      fs.rmSync(projectRoot, { recursive: true, force: true });
    }

    const description = noPrompts
      ? args.description || `${sanitized} skill generated by Skill Starter`
      : await prompt('Description', args.description || `${sanitized} skill generated by Skill Starter`);

    const category = noPrompts ? args.category || 'AI Skills' : await prompt('Category', args.category || 'AI Skills');

    const includeCI = noPrompts ? Boolean(args.ci) : /^y(es)?$/i.test(await prompt('Include CI workflow? y/N', args.ci ? 'y' : 'n'));

    const manifest = generateProject({
      name: sanitized,
      description,
      category,
      template,
      includeCI,
      projectRoot
    });

    if (format === 'json') {
      console.log(JSON.stringify(makeEnvelope(manifest.warnings.length ? 'warning' : 'ok', manifest), null, 2));
    } else {
      console.log(`Created ${sanitized} at ${projectRoot}`);
      console.log(`Template: ${template}`);
      console.log(`Files: ${manifest.files.length}`);
      if (manifest.warnings.length) {
        for (const warning of manifest.warnings) {
          console.log(`Warning: ${warning}`);
        }
      }
    }

    return 0;
  } catch (error) {
    console.error(
      JSON.stringify(
        makeEnvelope('error', {}, [error instanceof Error ? error.message : String(error)]),
        null,
        2
      )
    );
    return 1;
  }
}
