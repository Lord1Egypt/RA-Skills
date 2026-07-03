#!/usr/bin/env node
/**
 * Build urufu-steward-hermes.tgz for one-command Hermes / agent install.
 *
 * Usage: node package-hermes.mjs
 * Output: scripts/agent/dist/urufu-steward-hermes.tgz
 */
import { cp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const repoRoot = join(__dirname, '..');
const skillRoot = repoRoot;
const distDir = join(__dirname, 'dist');
const packRoot = join(distDir, 'urufu-steward-hermes');
const tarball = join(distDir, 'urufu-steward-hermes.tgz');

const AGENT_FILES = [
  'package.json',
  'urufu-steward.mjs',
  'claim.mjs',
  'mint.mjs',
  'mint-paid.mjs',
  'chain.mjs',
  'config.mjs',
  'addresses.mjs',
  'abi.mjs',
  'allowlist.mjs',
  'indexer.mjs',
  'policy.mjs',
  'state.mjs',
  'policy.test.mjs',
  'steward.test.mjs',
  'mint.test.mjs',
  'README.md',
];

async function main() {
  await rm(packRoot, { recursive: true, force: true });
  await mkdir(join(packRoot, 'scripts'), { recursive: true });
  await mkdir(join(packRoot, 'references'), { recursive: true });

  await cp(join(skillRoot, 'hermes', 'SKILL.md'), join(packRoot, 'SKILL.md'));
  await cp(join(skillRoot, 'SKILL.md'), join(packRoot, 'SKILL-full.md'));
  // skillRoot is repo root (SKILL.md + hermes/ + references/)
  await cp(join(skillRoot, 'references', 'BOOTSTRAP.md'), join(packRoot, 'references', 'BOOTSTRAP.md'));
  await cp(join(skillRoot, 'references', 'agent-policy.json'), join(packRoot, 'references', 'agent-policy.json'));
  await cp(join(skillRoot, 'references', 'clawhub.md'), join(packRoot, 'references', 'clawhub.md'));
  await cp(join(skillRoot, 'references', 'bankr.md'), join(packRoot, 'references', 'bankr.md'));
  await cp(join(skillRoot, 'references', 'onboarding.md'), join(packRoot, 'references', 'onboarding.md'));
  await cp(join(repoRoot, 'docs', 'api', 'openapi.yaml'), join(packRoot, 'references', 'openapi.yaml'));
  await cp(join(repoRoot, 'docs', 'agent-play.md'), join(packRoot, 'AGENT-PLAY.md'));

  for (const file of AGENT_FILES) {
    await cp(join(__dirname, file), join(packRoot, 'scripts', file));
  }

  await writeFile(join(packRoot, 'install.mjs'), INSTALL_SCRIPT.trimStart());
  await writeFile(join(packRoot, 'README.md'), README.trimStart());

  await mkdir(distDir, { recursive: true });
  const tarCmd = process.platform === 'win32'
    ? `tar -czf "${tarball}" -C "${distDir}" urufu-steward-hermes`
    : `tar -czf "${tarball}" -C "${distDir}" urufu-steward-hermes`;
  execSync(tarCmd, { stdio: 'inherit' });

  const size = (await readFile(tarball)).length;
  console.log(JSON.stringify({
    ok: true,
    tarball,
    bytes: size,
    install: `node "${join(packRoot, 'install.mjs')}"`,
    hermes: `hermes skills install "${tarball}"`,
  }, null, 2));
}

const README = `
# urufu steward — Hermes pack

One-command install for AI agents playing urufu gēmu on Base.

## Install

\`\`\`bash
node install.mjs
\`\`\`

Or from the tarball path after extract:

\`\`\`bash
hermes skills install ./urufu-steward-hermes.tgz
cd urufu-steward-hermes && node install.mjs
\`\`\`

## Configure

\`\`\`bash
export URUFU_WALLET=0x...
export URUFU_PRIVATE_KEY=0x...   # session key recommended
\`\`\`

## Run

\`\`\`bash
cd scripts
node urufu-steward.mjs check
node urufu-steward.mjs claim      # user said "claim now"
node urufu-steward.mjs mint       # user said "mint now" (gasless free phase)
\`\`\`

Copy \`references/BOOTSTRAP.md\` into your agent session.
`;

const INSTALL_SCRIPT = `
#!/usr/bin/env node
import { execSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(fileURLToPath(import.meta.url));
const scriptsDir = join(root, 'scripts');

console.log('Installing urufu steward dependencies...');
execSync('npm install', { cwd: scriptsDir, stdio: 'inherit' });

console.log('');
console.log('Installed. Next steps:');
console.log('  1. export URUFU_WALLET=0xYourWallet');
console.log('  2. export URUFU_PRIVATE_KEY=0xYourSessionKey');
console.log('  3. cd scripts && node urufu-steward.mjs check');
console.log('  4. Paste references/BOOTSTRAP.md into your Hermes session');
console.log('');
console.log('Hermes: hermes skills install "' + root + '"');
`;

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
