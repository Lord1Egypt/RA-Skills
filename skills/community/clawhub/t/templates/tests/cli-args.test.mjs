import assert from 'node:assert/strict';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import { formatHelp, formatVersion, parseCliArgs } from '../scripts/lib/cli-args.mjs';

const cwd = '/repo/repair-target';
const skillRoot = '/repo/multica/outer-skills/read-figma-design';

describe('parseCliArgs', () => {
  it('requires exactly one of --issue-json and --url unless --help or --version is used', () => {
    assert.deepEqual(
      {
        ok: parseCliArgs(['node', 'script'], {}, cwd, skillRoot).ok,
        errorCode: parseCliArgs(['node', 'script'], {}, cwd, skillRoot).errorCode,
      },
      { ok: false, errorCode: 'figma_input_required' },
    );

    const both = parseCliArgs(
      ['node', 'script', '--issue-json', 'issue.json', '--url', 'https://figma.com/design/a/b?node-id=1-2'],
      {},
      cwd,
      skillRoot,
    );
    assert.equal(both.ok, false);
    assert.equal(both.errorCode, 'figma_input_conflict');

    assert.equal(parseCliArgs(['node', 'script', '--help'], {}, cwd, skillRoot).ok, true);
    assert.equal(parseCliArgs(['node', 'script', '--version'], {}, cwd, skillRoot).ok, true);
  });

  it('does not touch env files, token store, or network for --help and --version', () => {
    const hostileEnv = {
      FIGMA_ENV_FILE: {
        toString() {
          throw new Error('env file should not be read');
        },
      },
      FIGMA_TOKEN_STORE: {
        toString() {
          throw new Error('token store should not be read');
        },
      },
    };

    const help = parseCliArgs(['node', 'script', '--help'], hostileEnv, cwd, skillRoot);
    const version = parseCliArgs(['node', 'script', '--version'], hostileEnv, cwd, skillRoot);

    assert.equal(help.ok, true);
    assert.equal(help.mode, 'help');
    assert.equal(version.ok, true);
    assert.equal(version.mode, 'version');
  });

  it('uses env-file defaults in precedence order without reading those files', () => {
    const fromEnv = parseCliArgs(
      ['node', 'script', '--url', 'https://figma.com/design/a/b?node-id=1-2', '--out', '.multica/figma-context'],
      { FIGMA_ENV_FILE: '/custom/.env' },
      cwd,
      skillRoot,
    );
    const fallback = parseCliArgs(
      ['node', 'script', '--url', 'https://figma.com/design/a/b?node-id=1-2', '--out', '.multica/figma-context'],
      {},
      cwd,
      skillRoot,
    );

    assert.equal(fromEnv.ok, true);
    assert.deepEqual(fromEnv.envFiles, ['/custom/.env']);
    assert.equal(fallback.ok, true);
    assert.deepEqual(fallback.envFiles, [
      path.resolve(skillRoot, '../../.env'),
      path.resolve(cwd, '.env'),
    ]);
  });

  it('uses token-store defaults from env and then user home', () => {
    const fromEnv = parseCliArgs(
      ['node', 'script', '--url', 'https://figma.com/design/a/b?node-id=1-2', '--out', '.multica/figma-context'],
      { FIGMA_TOKEN_STORE: '/custom/token.json' },
      cwd,
      skillRoot,
    );
    const fallback = parseCliArgs(
      ['node', 'script', '--url', 'https://figma.com/design/a/b?node-id=1-2', '--out', '.multica/figma-context'],
      {},
      cwd,
      skillRoot,
    );

    assert.equal(fromEnv.ok, true);
    assert.equal(fromEnv.tokenStore, '/custom/token.json');
    assert.equal(fallback.ok, true);
    assert.equal(fallback.tokenStore, path.join(os.homedir(), '.multica/secrets/figma-oauth.json'));
  });

  it('uses spec budget defaults', () => {
    const parsed = parseCliArgs(
      ['node', 'script', '--url', 'https://figma.com/design/a/b?node-id=1-2', '--out', '.multica/figma-context'],
      {},
      cwd,
      skillRoot,
    );

    assert.equal(parsed.ok, true);
    assert.deepEqual(parsed.budgets, {
      maxParentDepth: 6,
      maxChildDepth: 4,
      maxSiblings: 16,
      maxNodesPerUrl: 600,
      maxScreenshotsPerUrl: 24,
      maxArtifactMiBPerUrl: 100,
      screenshotScale: 2,
    });
  });

  it('parses direct URL and issue JSON modes with output paths', () => {
    const direct = parseCliArgs(
      [
        'node',
        'script',
        '--url',
        'https://figma.com/design/a/b?node-id=1-2',
        '--out',
        '.multica/figma-context',
        '--repo',
        '.',
      ],
      {},
      cwd,
      skillRoot,
    );
    const issue = parseCliArgs(
      ['node', 'script', '--issue-json', '.multica/tmp/MUL-1.json', '--out', '.multica/figma-context'],
      {},
      cwd,
      skillRoot,
    );

    assert.equal(direct.ok, true);
    assert.equal(direct.mode, 'url');
    assert.equal(direct.url, 'https://figma.com/design/a/b?node-id=1-2');
    assert.equal(direct.out, path.resolve(cwd, '.multica/figma-context'));
    assert.equal(direct.repo, cwd);
    assert.equal(issue.ok, true);
    assert.equal(issue.mode, 'issue-json');
    assert.equal(issue.issueJson, path.resolve(cwd, '.multica/tmp/MUL-1.json'));
  });
});

describe('help and version output', () => {
  it('formats offline help text', () => {
    const help = formatHelp();

    assert.match(help, /read-figma-design/);
    assert.match(help, /--issue-json/);
    assert.match(help, /--url/);
  });

  it('formats offline version text with schema versions', () => {
    const version = formatVersion();

    assert.match(version, /read-figma-design/);
    assert.match(version, /artifact schema/i);
  });
});
