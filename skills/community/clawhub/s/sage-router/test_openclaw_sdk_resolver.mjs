import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

import { findOpenClawPackageDir } from './openclaw_sdk_resolver.mjs';

const root = mkdtempSync(join(tmpdir(), 'openclaw-sdk-resolver-'));
const packageDir = join(root, '.local', 'lib', 'node_modules', 'openclaw');
mkdirSync(join(packageDir, 'dist'), { recursive: true });
writeFileSync(join(packageDir, 'package.json'), '{"name":"openclaw"}\n');
writeFileSync(join(packageDir, 'dist', 'call-BA3do6C0.js'), 'module.exports={};\n');

assert.equal(findOpenClawPackageDir({ homeDir: root }), packageDir);
