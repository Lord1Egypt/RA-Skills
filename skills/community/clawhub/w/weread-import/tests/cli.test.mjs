import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import { assignOutputTitles, parseArgs } from '../src/cli.mjs';

const execFileAsync = promisify(execFile);

describe('cli gateway defaults', () => {
  it('prompts for WEREAD_API_KEY by default and shows selectable fallback options', async () => {
    const outputDir = path.join(os.tmpdir(), 'weread-cli-missing-key');
    await assert.rejects(
      execFileAsync('node', ['src/cli.mjs', '--book-id', '1', '--output', outputDir], {
        cwd: path.resolve('.'),
        env: {
          ...process.env,
          WEREAD_API_BACKEND: 'gateway',
          WEREAD_API_KEY: '',
        },
      }),
      (error) => {
        assert.match(error.stderr, /未配置 WEREAD_API_KEY/);
        assert.match(error.stderr, /export WEREAD_API_KEY=<你的apikey>/);
        assert.match(error.stderr, /微信读书 Skill/);
        assert.match(error.stderr, /快速配置第 2 步/);
        assert.match(error.stderr, /可选操作/);
        assert.match(error.stderr, /--cookie-from browser-managed/);
        assert.match(error.stderr, /--cookie-from browser-live/);
        assert.match(error.stderr, /--cookie '完整 cookie 字符串'/);
        assert.match(error.stderr, /不要自行切换到 Cookie/);
        return true;
      },
    );
  });

  it('prints help with gateway and legacy backend guidance', async () => {
    const { stdout } = await execFileAsync('node', ['src/cli.mjs', '--help'], {
      cwd: path.resolve('.'),
    });
    assert.match(stdout, /默认使用微信读书官方 Gateway/);
    assert.match(stdout, /WEREAD_API_KEY/);
    assert.match(stdout, /微信读书 Skill/);
    assert.match(stdout, /快速配置第 2 步/);
    assert.match(stdout, /--no-gateway --cookie-from browser-managed/);
    assert.match(stdout, /显式传入 --cookie-from 或 --cookie/);
  });

  it('runs when invoked through a symlinked path like staging packages on macOS', async () => {
    const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-cli-symlink-'));
    const linkedRepo = path.join(tempDir, 'repo');
    await fs.symlink(path.resolve('.'), linkedRepo, 'dir');
    const cliPath = path.join(linkedRepo, 'src', 'cli.mjs');
    const { stdout } = await execFileAsync('node', [cliPath, '--help'], {
      cwd: path.resolve('.'),
    });
    assert.match(stdout, /默认使用微信读书官方 Gateway/);
  });

  it('treats explicit cookie-from as legacy web backend unless gateway is explicit', () => {
    const args = parseArgs(['--book-id', '1', '--cookie-from', 'browser-managed']);
    assert.equal(args.apiBackend, 'web');
    assert.equal(args.legacyBackendRequested, true);
  });

  it('treats explicit cookie as legacy web backend unless gateway is explicit', () => {
    const args = parseArgs(['--book-id', '1', '--cookie', 'a=b']);
    assert.equal(args.apiBackend, 'web');
    assert.equal(args.legacyBackendRequested, true);
  });

  it('lets explicit gateway override legacy cookie options', () => {
    const args = parseArgs(['--book-id', '1', '--api-backend', 'gateway', '--cookie-from', 'browser-managed']);
    assert.equal(args.apiBackend, 'gateway');
    assert.equal(args.legacyBackendRequested, false);
  });

  it('preserves normal output titles and disambiguates duplicate sanitized titles', () => {
    const first = { bookId: 'book-a', title: '同名书' };
    const second = { bookId: 'book-b', title: '同名书' };
    const unique = { bookId: 'book-c', title: '唯一书名' };
    const outputTitles = assignOutputTitles([first, second, unique]);

    assert.equal(outputTitles.get(first), '同名书 (book-a)');
    assert.equal(outputTitles.get(second), '同名书 (book-b)');
    assert.equal(outputTitles.get(unique), '唯一书名');
  });
});
