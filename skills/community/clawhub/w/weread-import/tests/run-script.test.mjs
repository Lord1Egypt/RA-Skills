import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const scriptPath = path.resolve('scripts/run.sh');

async function writeExecutable(filePath, content) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, content, 'utf8');
  await fs.chmod(filePath, 0o755);
}

async function readFileEventually(filePath, timeoutMs = 2000) {
  const startedAt = Date.now();
  while (true) {
    try {
      return await fs.readFile(filePath, 'utf8');
    } catch (error) {
      if (error.code !== 'ENOENT' || Date.now() - startedAt >= timeoutMs) throw error;
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
  }
}

describe('run.sh', () => {
  it('launches the managed browser via nohup in browser-managed mode', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-run-script-'));
    const binDir = path.join(root, 'bin');
    const stagingScriptsDir = path.join(root, 'scripts');
    const logPath = path.join(root, 'run.log');
    const nodeLogPath = path.join(root, 'node.log');
    const nohupLogPath = path.join(root, 'nohup.log');
    const curlCountPath = path.join(root, 'curl-count');
    const runScriptPath = path.join(stagingScriptsDir, 'run.sh');
    const managedScriptPath = path.join(stagingScriptsDir, 'open-chrome-debug.sh');

    await writeExecutable(path.join(binDir, 'curl'), `#!/usr/bin/env bash
count=0
if [ -f "${curlCountPath}" ]; then
  count=$(cat "${curlCountPath}")
fi
count=$((count + 1))
printf "%s" "$count" > "${curlCountPath}"
if [ "$count" -ge 2 ]; then
  exit 0
fi
exit 1
`);
    await writeExecutable(path.join(binDir, 'node'), `#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "${nodeLogPath}"\n`);
    await writeExecutable(path.join(binDir, 'nohup'), `#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "${nohupLogPath}"\nexec "$@"\n`);
    await fs.mkdir(stagingScriptsDir, { recursive: true });
    await fs.copyFile(scriptPath, runScriptPath);
    await writeExecutable(managedScriptPath, `#!/usr/bin/env bash\nprintf "managed:%s\\n" "$1" >> "${logPath}"\n`);

    await execFileAsync('bash', [runScriptPath, '--book-id', '33628204', '--mode', 'api', '--cookie-from', 'browser-managed'], {
      cwd: path.resolve('.'),
      env: {
        ...process.env,
        PATH: `${binDir}:${process.env.PATH}`,
      },
    });

    const nohupArgs = await readFileEventually(nohupLogPath);
    assert.match(nohupArgs, /open-chrome-debug\.sh/);
    assert.match(nohupArgs, /9222/);
    const managedLog = await readFileEventually(logPath);
    assert.match(managedLog, /managed:9222/);
    const nodeArgs = await fs.readFile(nodeLogPath, 'utf8');
    assert.match(nodeArgs, /wait-browser-managed-ready\.mjs --cdp http:\/\/127\.0\.0\.1:9222 --timeout-ms 8000/);
    assert.match(nodeArgs, /--cookie-from browser-managed/);
  });

  it('skips the managed browser readiness probe when CDP is already warm', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-run-script-'));
    const binDir = path.join(root, 'bin');
    const stagingScriptsDir = path.join(root, 'scripts');
    const logPath = path.join(root, 'run.log');
    const nodeLogPath = path.join(root, 'node.log');
    const nohupLogPath = path.join(root, 'nohup.log');
    const runScriptPath = path.join(stagingScriptsDir, 'run.sh');
    const managedScriptPath = path.join(stagingScriptsDir, 'open-chrome-debug.sh');

    await writeExecutable(path.join(binDir, 'curl'), '#!/usr/bin/env bash\nexit 0\n');
    await writeExecutable(path.join(binDir, 'node'), `#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "${nodeLogPath}"\n`);
    await writeExecutable(path.join(binDir, 'nohup'), `#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "${nohupLogPath}"\nexec "$@"\n`);
    await fs.mkdir(stagingScriptsDir, { recursive: true });
    await fs.copyFile(scriptPath, runScriptPath);
    await writeExecutable(managedScriptPath, `#!/usr/bin/env bash\nprintf "managed:%s\\n" "$1" >> "${logPath}"\n`);

    await execFileAsync('bash', [runScriptPath, '--book-id', '33628204', '--mode', 'api', '--cookie-from', 'browser-managed'], {
      cwd: path.resolve('.'),
      env: {
        ...process.env,
        PATH: `${binDir}:${process.env.PATH}`,
      },
    });

    const nodeArgs = await fs.readFile(nodeLogPath, 'utf8');
    assert.doesNotMatch(nodeArgs, /wait-browser-managed-ready\.mjs/);
    assert.match(nodeArgs, /--cookie-from browser-managed/);
  });

  it('does not launch the managed browser in browser-live mode', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-run-script-'));
    const binDir = path.join(root, 'bin');
    const stagingScriptsDir = path.join(root, 'scripts');
    const logPath = path.join(root, 'run.log');
    const nodeLogPath = path.join(root, 'node.log');
    const runScriptPath = path.join(stagingScriptsDir, 'run.sh');
    const managedScriptPath = path.join(stagingScriptsDir, 'open-chrome-debug.sh');

    await writeExecutable(path.join(binDir, 'curl'), '#!/usr/bin/env bash\nexit 0\n');
    await writeExecutable(path.join(binDir, 'node'), `#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "${nodeLogPath}"\n`);
    await fs.mkdir(stagingScriptsDir, { recursive: true });
    await fs.copyFile(scriptPath, runScriptPath);
    await writeExecutable(managedScriptPath, `#!/usr/bin/env bash\nprintf "managed\\n" >> "${logPath}"\n`);

    await execFileAsync('bash', [runScriptPath, '--book-id', '33628204', '--mode', 'api', '--cookie-from', 'browser-live'], {
      cwd: path.resolve('.'),
      env: {
        ...process.env,
        PATH: `${binDir}:${process.env.PATH}`,
      },
    });

    await assert.rejects(fs.readFile(logPath, 'utf8'));
    const nodeArgs = await fs.readFile(nodeLogPath, 'utf8');
    assert.match(nodeArgs, /--cookie-from browser-live/);
  });
});
