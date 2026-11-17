#!/usr/bin/env node
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const home = mkdtempSync(join(tmpdir(), 'ldm-skill-dry-run-home-'));
const source = mkdtempSync(join(tmpdir(), 'ldm-skill-dry-run-source-'));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

try {
  process.env.HOME = home;

  for (const dir of ['.claude', '.openclaw', '.codex', '.agents']) {
    mkdirSync(join(home, dir), { recursive: true });
  }

  const workspace = join(home, 'workspace');
  mkdirSync(workspace, { recursive: true });
  mkdirSync(join(home, '.ldm'), { recursive: true });
  writeFileSync(join(home, '.ldm', 'config.json'), JSON.stringify({
    workspace,
    harnesses: {
      'claude-code': {
        detected: true,
        home: join(home, '.claude'),
        skills: join(home, '.claude', 'skills'),
      },
      openclaw: {
        detected: true,
        home: join(home, '.openclaw'),
        skills: join(home, '.openclaw', 'skills'),
      },
      codex: {
        detected: true,
        home: join(home, '.codex'),
        skills: join(home, '.codex', 'skills'),
      },
      'wip-agents': {
        detected: true,
        home: join(home, '.agents'),
        skills: join(home, '.agents', 'skills'),
      },
    },
  }, null, 2));

  mkdirSync(join(source, 'references'), { recursive: true });
  mkdirSync(join(source, 'agents'), { recursive: true });
  writeFileSync(join(source, 'package.json'), JSON.stringify({
    name: '@wipcomputer/wip-ai-chat-ui',
    version: '0.1.1',
  }, null, 2));
  writeFileSync(join(source, 'SKILL.md'), '---\nname: wip-ai-chat-ui\ndescription: "test skill"\n---\n\n# Test Skill\n');
  writeFileSync(join(source, 'references', 'stack.md'), '# Stack\n');
  writeFileSync(join(source, 'agents', 'openai.yaml'), 'display_name: "WIP AI Chat UI"\n');

  const { setFlags, installFromPath } = await import('../lib/deploy.mjs');

  const lines = [];
  const originalLog = console.log;
  console.log = (...args) => lines.push(args.join(' '));

  try {
    setFlags({ dryRun: true, jsonOutput: false });
    const result = await installFromPath(source);
    assert(result.interfaces === 1, 'dry run should process one skill interface');
  } finally {
    console.log = originalLog;
  }

  const output = lines.join('\n');

  for (const expected of [
    'Would copy:',
    '- SKILL.md',
    '- references/',
    '- agents/',
    'Permanent copy:',
    join(home, '.ldm', 'extensions', 'wip-ai-chat-ui', 'SKILL.md'),
    join(home, '.ldm', 'extensions', 'wip-ai-chat-ui', 'references/'),
    'Agent skill targets:',
    `claude-code: ${join(home, '.claude', 'skills', 'wip-ai-chat-ui')}`,
    join(home, '.claude', 'skills', 'wip-ai-chat-ui', 'SKILL.md'),
    `openclaw: ${join(home, '.openclaw', 'skills', 'wip-ai-chat-ui')}`,
    join(home, '.openclaw', 'skills', 'wip-ai-chat-ui', 'references/'),
    `codex: ${join(home, '.codex', 'skills', 'wip-ai-chat-ui')}`,
    `wip-agents: ${join(home, '.agents', 'skills', 'wip-ai-chat-ui')}`,
    'Workspace docs target:',
    `${join(workspace, 'settings', 'docs', 'skills', 'wip-ai-chat-ui')} (references/ only)`,
  ]) {
    assert(output.includes(expected), `dry-run output should include ${expected}\n\n${output}`);
  }

  console.log('installer skill dry-run destinations regression passed');
} finally {
  rmSync(home, { recursive: true, force: true });
  rmSync(source, { recursive: true, force: true });
}
