import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const scriptPath = path.resolve('scripts/open-chrome-debug.sh');

async function writeFile(filePath, content) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, content, 'utf8');
}

async function makeFakeChrome(root, logPath) {
  const fakeChrome = path.join(root, 'fake-chrome.sh');
  await fs.writeFile(fakeChrome, `#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "${logPath}"\n`, 'utf8');
  await fs.chmod(fakeChrome, 0o755);
  return fakeChrome;
}

async function makeFakeCurl(root, body = '#!/usr/bin/env bash\nexit 0\n') {
  const fakeCurl = path.join(root, 'curl');
  await fs.writeFile(fakeCurl, body, 'utf8');
  await fs.chmod(fakeCurl, 0o755);
  return fakeCurl;
}

describe('open-chrome-debug.sh', () => {
  it('launches an isolated managed Chrome profile without syncing default login data by default', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-open-chrome-'));
    const source = path.join(root, 'source');
    const profile = path.join(root, 'profile');
    const logPath = path.join(root, 'chrome.log');
    const fakeChrome = await makeFakeChrome(root, logPath);
    const fakeCurl = await makeFakeCurl(root, '#!/usr/bin/env bash\nexit 1\n');
    const fakeBinDir = path.dirname(fakeCurl);

    await writeFile(path.join(source, 'Default/Cookies'), 'source-cookie');
    await writeFile(path.join(source, 'Default/Login Data For Account'), 'source-account');
    await writeFile(path.join(source, 'Default/Preferences'), 'source-preferences');
    await writeFile(path.join(source, 'Local State'), 'source-local-state');

    await execFileAsync('bash', [scriptPath, '9333'], {
      env: {
        ...process.env,
        PATH: `${fakeBinDir}:${process.env.PATH}`,
        WEREAD_CHROME_BIN: fakeChrome,
        WEREAD_CHROME_DEFAULT: source,
        WEREAD_PROFILE_DIR: profile,
      },
    });

    await assert.rejects(fs.readFile(path.join(profile, 'Default/Cookies'), 'utf8'));
    await assert.rejects(fs.readFile(path.join(profile, 'Default/Login Data For Account'), 'utf8'));

    const log = await fs.readFile(logPath, 'utf8');
    assert.match(log, /--remote-debugging-port=9333/);
    assert.match(log, /https:\/\/weread\.qq\.com\//);
    assert.match(log, new RegExp(`--user-data-dir=${profile.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
  });

  it('syncs newer profile files only when legacy sync mode is enabled', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-open-chrome-'));
    const source = path.join(root, 'source');
    const profile = path.join(root, 'profile');
    const logPath = path.join(root, 'chrome.log');
    const fakeChrome = await makeFakeChrome(root, logPath);
    const fakeCurl = await makeFakeCurl(root, '#!/usr/bin/env bash\nexit 1\n');
    const fakeBinDir = path.dirname(fakeCurl);

    await writeFile(path.join(source, 'Default/Cookies'), 'source-cookie');
    await writeFile(path.join(source, 'Default/Login Data For Account'), 'source-account');
    await writeFile(path.join(source, 'Default/Preferences'), 'source-preferences');
    await writeFile(path.join(source, 'Default/Secure Preferences'), 'source-secure-preferences');
    await writeFile(path.join(source, 'Local State'), 'source-local-state');

    await writeFile(path.join(profile, 'Default/Cookies'), 'old-cookie');
    await writeFile(path.join(profile, 'Default/Login Data For Account'), 'old-account');
    await writeFile(path.join(profile, 'Default/Preferences'), 'old-preferences');
    await writeFile(path.join(profile, 'Default/Secure Preferences'), 'old-secure-preferences');
    await writeFile(path.join(profile, 'Local State'), 'old-local-state');

    const older = new Date('2026-04-08T01:00:00Z');
    const newer = new Date('2026-04-08T02:00:00Z');
    await fs.utimes(path.join(profile, 'Default/Cookies'), older, older);
    await fs.utimes(path.join(profile, 'Default/Login Data For Account'), older, older);
    await fs.utimes(path.join(profile, 'Default/Preferences'), older, older);
    await fs.utimes(path.join(profile, 'Default/Secure Preferences'), older, older);
    await fs.utimes(path.join(profile, 'Local State'), older, older);
    await fs.utimes(path.join(source, 'Default/Cookies'), newer, newer);
    await fs.utimes(path.join(source, 'Default/Login Data For Account'), newer, newer);
    await fs.utimes(path.join(source, 'Default/Preferences'), newer, newer);
    await fs.utimes(path.join(source, 'Default/Secure Preferences'), newer, newer);
    await fs.utimes(path.join(source, 'Local State'), newer, newer);

    await execFileAsync('bash', [scriptPath, '9334'], {
      env: {
        ...process.env,
        PATH: `${fakeBinDir}:${process.env.PATH}`,
        WEREAD_CHROME_BIN: fakeChrome,
        WEREAD_CHROME_DEFAULT: source,
        WEREAD_PROFILE_DIR: profile,
        WEREAD_PROFILE_SYNC_MODE: 'legacy',
      },
    });

    assert.equal(await fs.readFile(path.join(profile, 'Default/Cookies'), 'utf8'), 'source-cookie');
    assert.equal(await fs.readFile(path.join(profile, 'Default/Login Data For Account'), 'utf8'), 'source-account');
    assert.equal(await fs.readFile(path.join(profile, 'Local State'), 'utf8'), 'source-local-state');

    const log = await fs.readFile(logPath, 'utf8');
    assert.match(log, /--remote-debugging-port=9334/);
    assert.match(log, new RegExp(`--user-data-dir=${profile.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}`));
  });

  it('exits without launching Chrome when an up-to-date CDP instance is already listening', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-open-chrome-'));
    const source = path.join(root, 'source');
    const profile = path.join(root, 'profile');
    const logPath = path.join(root, 'chrome.log');
    const fakeChrome = await makeFakeChrome(root, logPath);
    const fakeCurl = await makeFakeCurl(root);
    const fakeBinDir = path.dirname(fakeCurl);

    await writeFile(path.join(source, 'Default/Cookies'), 'same-cookie');
    await writeFile(path.join(profile, 'Default/Cookies'), 'same-cookie');

    const now = new Date('2026-04-08T02:30:00Z');
    await fs.utimes(path.join(source, 'Default/Cookies'), now, now);
    await fs.utimes(path.join(profile, 'Default/Cookies'), now, now);

    await execFileAsync('bash', [scriptPath, '9334'], {
      env: {
        ...process.env,
        PATH: `${fakeBinDir}:${process.env.PATH}`,
        WEREAD_CHROME_BIN: fakeChrome,
        WEREAD_CHROME_DEFAULT: source,
        WEREAD_PROFILE_DIR: profile,
      },
    });

    await assert.rejects(fs.readFile(logPath, 'utf8'));
  });
});
