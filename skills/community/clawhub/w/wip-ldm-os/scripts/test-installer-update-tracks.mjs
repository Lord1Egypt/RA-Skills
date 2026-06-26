#!/usr/bin/env node
import { readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const cli = readFileSync(join(root, 'bin', 'ldm.js'), 'utf8');

const marker = '// Check parent packages for toolbox-style repos (#132)';
const idx = cli.indexOf(marker);
if (idx === -1) {
  throw new Error('Could not find toolbox parent update block');
}

const parentBlock = cli.slice(idx, cli.indexOf('const totalUpdates = npmUpdates.length;', idx));
if (!parentBlock.includes("const npmTag = ALPHA_FLAG ? 'alpha' : BETA_FLAG ? 'beta' : 'latest';")) {
  throw new Error('Toolbox parent update block does not select the requested release track');
}

if (!parentBlock.includes('dist-tags.${npmTag}')) {
  throw new Error('Toolbox parent update block does not query alpha/beta dist-tags');
}

if (/const latest = execSync\(`npm view \$\{comp\.npm\} version 2>\/dev\/null`/.test(parentBlock)) {
  throw new Error('Toolbox parent update block still hardcodes the stable npm version query');
}

const installMarker = '// For parent packages, installFromPath already refreshes each sub-tool';
const installIdx = cli.indexOf(installMarker);
if (installIdx === -1) {
  throw new Error('Could not find parent registry refresh block');
}

const installBlock = cli.slice(installIdx, cli.indexOf('} catch (e) {', installIdx));
if (installBlock.includes('= entry.latestVersion')) {
  throw new Error('Parent update block must not stamp parent versions onto sub-tool registry entries');
}

console.log('installer update-track regression checks passed');
