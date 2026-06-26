import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';

const execFileAsync = promisify(execFile);
const scriptContent = await fs.readFile(path.resolve('scripts/prepare-staging-skill.sh'), 'utf8');

async function writeFile(filePath, content) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, content, 'utf8');
}

describe('prepare-staging-skill.sh', () => {
  it('creates an isolated staging copy without git metadata, dependencies, or output artifacts', async () => {
    const root = await fs.mkdtemp(path.join(os.tmpdir(), 'weread-stage-src-'));
    const repo = path.join(root, 'repo');
    const dest = path.join(root, 'stage');

    await writeFile(path.join(repo, 'scripts/prepare-staging-skill.sh'), scriptContent);
    await writeFile(path.join(repo, 'src/cli.mjs'), 'console.log("ok");\n');
    await writeFile(path.join(repo, 'README.md'), '# demo\n');
    await writeFile(path.join(repo, '.git/HEAD'), 'ref: refs/heads/main\n');
    await writeFile(path.join(repo, 'node_modules/demo/index.js'), 'module.exports = 1;\n');
    await writeFile(path.join(repo, 'out/demo.txt'), 'artifact\n');
    await writeFile(path.join(repo, '.env'), 'SECRET=1\n');

    const scriptPath = path.join(repo, 'scripts/prepare-staging-skill.sh');
    await fs.chmod(scriptPath, 0o755);

    const { stdout } = await execFileAsync('bash', [scriptPath, dest]);
    assert.equal(stdout.trim(), dest);

    assert.equal(await fs.readFile(path.join(dest, 'src/cli.mjs'), 'utf8'), 'console.log("ok");\n');
    await assert.rejects(fs.readFile(path.join(dest, '.git/HEAD'), 'utf8'));
    await assert.rejects(fs.readFile(path.join(dest, 'node_modules/demo/index.js'), 'utf8'));
    await assert.rejects(fs.readFile(path.join(dest, 'out/demo.txt'), 'utf8'));
    await assert.rejects(fs.readFile(path.join(dest, '.env'), 'utf8'));
  });
});
