#!/usr/bin/env node
import { existsSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const home = mkdtempSync(join(tmpdir(), 'ldm-skill-dir-home-'));
const source = mkdtempSync(join(tmpdir(), 'ldm-skill-dir-source-'));

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

try {
  process.env.HOME = home;

  for (const dir of ['.claude', '.openclaw', '.codex', '.agents']) {
    mkdirSync(join(home, dir), { recursive: true });
  }

  const skillDir = join(source, 'skills', 'wip-ai-chat-ui');
  mkdirSync(join(skillDir, 'references'), { recursive: true });
  mkdirSync(join(skillDir, 'agents'), { recursive: true });
  writeFileSync(join(skillDir, 'SKILL.md'), '---\nname: wip-ai-chat-ui\ndescription: "test skill"\n---\n\n# Test Skill\n');
  writeFileSync(join(skillDir, 'references', 'stack.md'), '# Stack\n');
  writeFileSync(join(skillDir, 'agents', 'openai.yaml'), 'display_name: "WIP AI Chat UI"\n');

  const { detectInterfacesJSON } = await import('../lib/detect.mjs');
  const detected = detectInterfacesJSON(source);
  assert(detected.interfaceCount === 1, 'skill directory repo should expose one interface');
  assert(detected.interfaces.skill?.skills?.[0]?.name === 'wip-ai-chat-ui', 'skill directory name should be detected');

  const { installFromPath } = await import('../lib/deploy.mjs');
  const result = await installFromPath(source);
  assert(result.interfaces === 1, 'skill directory install should process one interface');

  for (const target of [
    join(home, '.claude', 'skills', 'wip-ai-chat-ui'),
    join(home, '.openclaw', 'skills', 'wip-ai-chat-ui'),
    join(home, '.codex', 'skills', 'wip-ai-chat-ui'),
    join(home, '.agents', 'skills', 'wip-ai-chat-ui'),
  ]) {
    assert(existsSync(join(target, 'SKILL.md')), `${target} should include SKILL.md`);
    assert(existsSync(join(target, 'references', 'stack.md')), `${target} should include references`);
    assert(existsSync(join(target, 'agents', 'openai.yaml')), `${target} should include agents metadata`);
    assert(!lstatSync(target).isSymbolicLink(), `${target} should be a deployed directory, not a symlink`);
  }

  const codexSkill = readFileSync(join(home, '.codex', 'skills', 'wip-ai-chat-ui', 'SKILL.md'), 'utf8');
  assert(codexSkill.includes('name: wip-ai-chat-ui'), 'Codex target should contain the expected skill');

  console.log('installer skill directory regression passed');
} finally {
  rmSync(home, { recursive: true, force: true });
  rmSync(source, { recursive: true, force: true });
}
