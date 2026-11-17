#!/usr/bin/env node
import { mkdtempSync, mkdirSync, writeFileSync, readFileSync, existsSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { tmpdir } from 'node:os';

const tempHome = mkdtempSync(join(tmpdir(), 'ldm-hook-toolname-home-'));
const tempPkg = mkdtempSync(join(tmpdir(), 'ldm-npm-pack-'));

try {
  process.env.HOME = tempHome;

  mkdirSync(join(tempHome, '.claude'), { recursive: true });
  writeFileSync(join(tempHome, '.claude', 'settings.json'), JSON.stringify({ hooks: {} }, null, 2) + '\n');
  const staleExtDir = join(tempHome, '.ldm', 'extensions', 'wip-branch-guard');
  mkdirSync(staleExtDir, { recursive: true });
  writeFileSync(join(staleExtDir, 'guard.mjs'), 'console.log("stale guard");\n');
  writeFileSync(join(staleExtDir, 'package.json'), JSON.stringify({
    name: '@wipcomputer/wip-branch-guard',
    version: '1.9.89',
  }, null, 2) + '\n');
  writeFileSync(join(tempHome, '.ldm', 'extensions', 'registry.json'), JSON.stringify({
    _format: 'v2',
    extensions: {
      'wip-branch-guard': {
        version: '1.9.89',
        ldmPath: staleExtDir,
        paths: { ldm: staleExtDir },
        interfaces: ['module', 'skill', 'claudeCodeHook'],
      },
    },
  }, null, 2) + '\n');

  const extractedPackageDir = join(tempPkg, 'package');
  mkdirSync(extractedPackageDir, { recursive: true });
  writeFileSync(join(extractedPackageDir, 'package.json'), JSON.stringify({
    name: '@wipcomputer/wip-branch-guard',
    version: '1.9.90',
    type: 'module',
    main: 'guard.mjs',
    claudeCode: {
      hooks: [
        { event: 'PreToolUse', matcher: 'Write|Edit|Bash', command: 'node guard.mjs', timeout: 5 },
      ],
    },
  }, null, 2) + '\n');
  writeFileSync(join(extractedPackageDir, 'guard.mjs'), 'console.log("guard 1.9.90");\n');
  writeFileSync(join(extractedPackageDir, 'SKILL.md'), '---\nname: wip-branch-guard\ndescription: "test skill"\n---\n');

  const { installSingleTool } = await import('../lib/deploy.mjs');
  const installed = installSingleTool(extractedPackageDir);
  if (installed === 0) throw new Error('installer did not process the test package');

  const expectedDir = join(tempHome, '.ldm', 'extensions', 'wip-branch-guard');
  const wrongDir = join(tempHome, '.ldm', 'extensions', 'package');
  if (!existsSync(join(expectedDir, 'guard.mjs'))) {
    throw new Error('guard.mjs was not deployed under the package-derived tool name');
  }
  if (!existsSync(join(expectedDir, 'package.json'))) {
    throw new Error('package.json was not deployed under the package-derived tool name');
  }
  if (existsSync(wrongDir)) {
    throw new Error('hook deployment used basename(repoPath) instead of package-derived tool name');
  }

  const settings = JSON.parse(readFileSync(join(tempHome, '.claude', 'settings.json'), 'utf8'));
  const command = settings.hooks?.PreToolUse?.[0]?.hooks?.[0]?.command || '';
  if (!command.includes('/wip-branch-guard/guard.mjs')) {
    throw new Error(`hook command points at the wrong extension path: ${command}`);
  }

  const deployedPkg = JSON.parse(readFileSync(join(expectedDir, 'package.json'), 'utf8'));
  if (deployedPkg.version !== '1.9.90') {
    throw new Error(`deployed package version mismatch: ${deployedPkg.version}`);
  }

  console.log('installer hook tool-name regression check passed');
} finally {
  rmSync(tempHome, { recursive: true, force: true });
  rmSync(tempPkg, { recursive: true, force: true });
}
