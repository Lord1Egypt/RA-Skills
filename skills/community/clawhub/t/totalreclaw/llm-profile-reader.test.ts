/**
 * Tests for llm-profile-reader.ts — 3.3.1 auth-profiles.json harvester.
 *
 * Covers:
 *   - parseAuthProfilesFile accepts well-formed OpenClaw auth-profiles.json
 *   - Rejects malformed JSON / missing "profiles" field silently
 *   - Maps provider-namespace aliases (google → gemini, z.ai → zai)
 *   - Skips non-default profile ids (e.g. `openai:work`)
 *   - findAuthProfilesFiles walks agent subdirectories
 *   - readAllAuthProfileKeys + dedupeByProvider compose correctly
 *
 * Run with: npx tsx llm-profile-reader.test.ts
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import {
  parseAuthProfilesFile,
  findAuthProfilesFiles,
  readAllAuthProfileKeys,
  dedupeByProvider,
  defaultAuthProfilesRoot,
  parseModelsJsonFile,
  findModelsJsonFiles,
  readAllModelsJsonKeys,
  readAllProfileKeys,
} from './llm-profile-reader.js';

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

function mkTmp(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'tr-authprof-'));
}

// ---------------------------------------------------------------------------
// defaultAuthProfilesRoot
// ---------------------------------------------------------------------------

{
  assert(
    defaultAuthProfilesRoot('/home/alice') === path.join('/home/alice', '.openclaw', 'agents'),
    'defaultAuthProfilesRoot: builds $HOME/.openclaw/agents',
  );
  assert(defaultAuthProfilesRoot(undefined) === '', 'defaultAuthProfilesRoot: empty when home unset');
}

// ---------------------------------------------------------------------------
// parseAuthProfilesFile — happy path
// ---------------------------------------------------------------------------

{
  const tmp = mkTmp();
  const file = path.join(tmp, 'auth-profiles.json');
  fs.writeFileSync(
    file,
    JSON.stringify({
      profiles: {
        'openai:default': { key: 'sk-openai-xyz' },
        'anthropic:default': { key: 'sk-ant-xyz' },
        'zai:default': { key: 'zai-xyz' },
        'google:default': { key: 'gemini-xyz' },
      },
    }),
  );
  const entries = parseAuthProfilesFile(file);
  const byProvider = dedupeByProvider(entries);
  assert(byProvider['openai']?.apiKey === 'sk-openai-xyz', 'parse: openai:default captured');
  assert(byProvider['anthropic']?.apiKey === 'sk-ant-xyz', 'parse: anthropic:default captured');
  assert(byProvider['zai']?.apiKey === 'zai-xyz', 'parse: zai:default captured');
  assert(byProvider['gemini']?.apiKey === 'gemini-xyz', 'parse: google:default mapped to gemini provider');
}

// ---------------------------------------------------------------------------
// parseAuthProfilesFile — skips non-default profiles
// ---------------------------------------------------------------------------

{
  const tmp = mkTmp();
  const file = path.join(tmp, 'auth-profiles.json');
  fs.writeFileSync(
    file,
    JSON.stringify({
      profiles: {
        'openai:work': { key: 'sk-work' },
        'openai:default': { key: 'sk-default' },
        'openai:personal': { key: 'sk-personal' },
      },
    }),
  );
  const entries = parseAuthProfilesFile(file);
  assert(entries.length === 1, 'parse: only default profiles kept');
  assert(entries[0].apiKey === 'sk-default', 'parse: default key selected');
}

// ---------------------------------------------------------------------------
// parseAuthProfilesFile — tolerates malformed input
// ---------------------------------------------------------------------------

{
  const tmp = mkTmp();
  const file = path.join(tmp, 'auth-profiles.json');

  // Not JSON
  fs.writeFileSync(file, 'not json at all');
  assert(parseAuthProfilesFile(file).length === 0, 'parse: invalid JSON returns []');

  // Wrong shape — no "profiles" field
  fs.writeFileSync(file, JSON.stringify({ something_else: {} }));
  assert(parseAuthProfilesFile(file).length === 0, 'parse: missing "profiles" field returns []');

  // Empty keys dropped
  fs.writeFileSync(file, JSON.stringify({ profiles: { 'openai:default': { key: '' } } }));
  assert(parseAuthProfilesFile(file).length === 0, 'parse: empty key dropped');

  // File that does not exist
  const missing = path.join(tmp, 'nope.json');
  assert(parseAuthProfilesFile(missing).length === 0, 'parse: missing file returns []');
}

// ---------------------------------------------------------------------------
// findAuthProfilesFiles — walks one level of agent subdirectories
// ---------------------------------------------------------------------------

{
  const tmp = mkTmp();
  const root = path.join(tmp, '.openclaw', 'agents');
  fs.mkdirSync(path.join(root, 'agent-a', 'agent'), { recursive: true });
  fs.mkdirSync(path.join(root, 'agent-b', 'agent'), { recursive: true });
  fs.mkdirSync(path.join(root, 'agent-c'), { recursive: true });
  fs.writeFileSync(path.join(root, 'agent-a', 'agent', 'auth-profiles.json'), '{}');
  fs.writeFileSync(path.join(root, 'agent-b', 'agent', 'auth-profiles.json'), '{}');
  // agent-c has no nested agent/auth-profiles.json

  const files = findAuthProfilesFiles(root);
  assert(files.length === 2, 'findAuthProfilesFiles: returns 2 files for 2 agents-with-profiles');
  assert(files[0].endsWith('/agent-a/agent/auth-profiles.json'), 'findAuthProfilesFiles: first is agent-a (alphabetical)');
  assert(files[1].endsWith('/agent-b/agent/auth-profiles.json'), 'findAuthProfilesFiles: second is agent-b');

  // Missing root — returns [] not throw
  const missingRoot = path.join(tmp, 'does-not-exist');
  assert(findAuthProfilesFiles(missingRoot).length === 0, 'findAuthProfilesFiles: missing root returns []');
}

// ---------------------------------------------------------------------------
// readAllAuthProfileKeys — aggregate across multiple files, dedupe last-wins
// ---------------------------------------------------------------------------

{
  const tmp = mkTmp();
  const root = path.join(tmp, '.openclaw', 'agents');
  fs.mkdirSync(path.join(root, 'alpha-agent', 'agent'), { recursive: true });
  fs.mkdirSync(path.join(root, 'beta-agent', 'agent'), { recursive: true });

  // alpha-agent has an openai key
  fs.writeFileSync(
    path.join(root, 'alpha-agent', 'agent', 'auth-profiles.json'),
    JSON.stringify({
      profiles: { 'openai:default': { key: 'sk-alpha' } },
    }),
  );

  // beta-agent has an openai key AND an anthropic key; beta wins on openai
  // because alphabetical order puts it after alpha.
  fs.writeFileSync(
    path.join(root, 'beta-agent', 'agent', 'auth-profiles.json'),
    JSON.stringify({
      profiles: {
        'openai:default': { key: 'sk-beta' },
        'anthropic:default': { key: 'sk-ant' },
      },
    }),
  );

  const all = readAllAuthProfileKeys({ root });
  assert(all.length === 3, 'readAllAuthProfileKeys: 3 entries (1 from alpha, 2 from beta)');

  const byProvider = dedupeByProvider(all);
  assert(byProvider['openai']?.apiKey === 'sk-beta', 'dedupeByProvider: later file wins for openai');
  assert(byProvider['anthropic']?.apiKey === 'sk-ant', 'dedupeByProvider: anthropic only in beta');
}

// ---------------------------------------------------------------------------
// 3.3.1-rc.2 — legacy models.json reader
// ---------------------------------------------------------------------------

{
  const tmp = mkTmp();
  const file = path.join(tmp, 'models.json');
  fs.writeFileSync(
    file,
    JSON.stringify({
      providers: {
        zai: { apiKey: 'zai-legacy' },
        openai: { apiKey: 'sk-legacy' },
        anthropic: { apiKey: 'sk-ant-legacy' },
      },
    }),
  );
  const entries = parseModelsJsonFile(file);
  const byProvider = dedupeByProvider(entries);
  assert(byProvider['zai']?.apiKey === 'zai-legacy', 'models.json: zai captured');
  assert(byProvider['openai']?.apiKey === 'sk-legacy', 'models.json: openai captured');
  assert(byProvider['anthropic']?.apiKey === 'sk-ant-legacy', 'models.json: anthropic captured');
  assert(byProvider['zai']?.profileId?.includes('models-json-legacy') ?? false, 'models.json: profileId marks legacy source');
}

{
  // Accepts apiKey / api_key / key
  const tmp = mkTmp();
  const file = path.join(tmp, 'models.json');
  fs.writeFileSync(
    file,
    JSON.stringify({
      providers: {
        zai: { api_key: 'snake-case' },
        openai: { key: 'plain-key' },
      },
    }),
  );
  const entries = parseModelsJsonFile(file);
  const byProvider = dedupeByProvider(entries);
  assert(byProvider['zai']?.apiKey === 'snake-case', 'models.json: api_key snake_case variant accepted');
  assert(byProvider['openai']?.apiKey === 'plain-key', 'models.json: plain "key" variant accepted');
}

{
  // Missing / malformed — graceful null
  const tmp = mkTmp();
  const file = path.join(tmp, 'models.json');
  fs.writeFileSync(file, 'not json');
  assert(parseModelsJsonFile(file).length === 0, 'models.json: invalid JSON → []');

  fs.writeFileSync(file, JSON.stringify({ something_else: {} }));
  assert(parseModelsJsonFile(file).length === 0, 'models.json: missing "providers" field → []');
}

{
  // findModelsJsonFiles
  const tmp = mkTmp();
  const root = path.join(tmp, '.openclaw', 'agents');
  fs.mkdirSync(path.join(root, 'agent-x', 'agent'), { recursive: true });
  fs.writeFileSync(path.join(root, 'agent-x', 'agent', 'models.json'), '{}');
  const files = findModelsJsonFiles(root);
  assert(files.length === 1, 'findModelsJsonFiles: finds agent-x/agent/models.json');
}

{
  // Combined reader: auth-profiles wins over models.json on overlap
  const tmp = mkTmp();
  const root = path.join(tmp, '.openclaw', 'agents');
  fs.mkdirSync(path.join(root, 'agent-a', 'agent'), { recursive: true });
  fs.writeFileSync(
    path.join(root, 'agent-a', 'agent', 'auth-profiles.json'),
    JSON.stringify({
      profiles: { 'openai:default': { key: 'sk-from-auth' } },
    }),
  );
  fs.writeFileSync(
    path.join(root, 'agent-a', 'agent', 'models.json'),
    JSON.stringify({
      providers: {
        openai: { apiKey: 'sk-from-models-legacy' },
        anthropic: { apiKey: 'sk-ant-from-models' },
      },
    }),
  );
  const merged = readAllProfileKeys({ root });
  const byProvider = dedupeByProvider(merged);
  assert(
    byProvider['openai']?.apiKey === 'sk-from-auth',
    'readAllProfileKeys: auth-profiles wins over models.json on overlap',
  );
  assert(
    byProvider['anthropic']?.apiKey === 'sk-ant-from-models',
    'readAllProfileKeys: models.json-only provider is picked up',
  );
}

{
  // Combined reader: models.json alone works when auth-profiles absent
  const tmp = mkTmp();
  const root = path.join(tmp, '.openclaw', 'agents');
  fs.mkdirSync(path.join(root, 'agent-b', 'agent'), { recursive: true });
  fs.writeFileSync(
    path.join(root, 'agent-b', 'agent', 'models.json'),
    JSON.stringify({
      providers: { zai: { apiKey: 'zai-only' } },
    }),
  );
  const merged = readAllProfileKeys({ root });
  const byProvider = dedupeByProvider(merged);
  assert(
    byProvider['zai']?.apiKey === 'zai-only',
    'readAllProfileKeys: models.json-only root yields its keys',
  );
}

{
  const allKeys = readAllModelsJsonKeys({ root: '/path/that/does/not/exist' });
  assert(allKeys.length === 0, 'readAllModelsJsonKeys: missing root → []');
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
