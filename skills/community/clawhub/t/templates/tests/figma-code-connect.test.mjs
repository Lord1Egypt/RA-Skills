import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import {
  resolveCodeConnectExitCode,
  scanCodeConnect,
} from '../scripts/lib/figma-code-connect.mjs';

async function makeRepo() {
  return fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-code-connect-test-'));
}

async function writeFile(filePath, contents) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, contents);
}

const targetNode = {
  id: '6127:21193',
  name: 'Button / Primary',
  type: 'COMPONENT',
  componentKey: 'component-key-123',
  componentName: 'Button / Primary',
};

describe('scanCodeConnect', () => {
  it('returns mapped when a local Code Connect file has direct figma.connect evidence', async () => {
    const repo = await makeRepo();
    await writeFile(
      path.join(repo, 'packages/ui/button.figma.tsx'),
      `
import figma from '@figma/code-connect';
import { Button } from './button';
figma.connect(Button, 'https://www.figma.com/design/file/Button?node-id=6127-21193', {
  props: {},
});
// component-key-123
`,
    );

    const result = await scanCodeConnect({
      repo,
      targetNode,
      maxFiles: 5000,
    });

    assert.equal(result.schemaVersion, 'figma-code-connect-context/v1');
    assert.equal(result.status, 'mapped');
    assert.equal(result.source, 'local-code-connect-scan');
    assert.equal(result.scanBudget.exceeded, false);
    assert.equal(result.mappings[0].figmaNodeId, '6127:21193');
    assert.equal(result.mappings[0].codeComponentName, 'Button');
    assert.equal(result.mappings[0].confidence, 'high');
  });

  it('returns unmapped only after fully scanning known Code Connect files within budget', async () => {
    const repo = await makeRepo();
    await writeFile(
      path.join(repo, 'packages/ui/card.connect.ts'),
      `
import figma from '@figma/code-connect';
figma.connect(Card, 'https://www.figma.com/design/file/Card?node-id=1-2', {});
`,
    );

    const result = await scanCodeConnect({
      repo,
      targetNode,
      maxFiles: 5000,
    });

    assert.equal(result.status, 'unmapped');
    assert.equal(result.scanBudget.exceeded, false);
    assert.equal(result.mappings.length, 0);
  });

  it('returns unavailable when repo is missing or scan exceeds the file budget', async () => {
    const missing = await scanCodeConnect({
      repo: null,
      targetNode,
      maxFiles: 5000,
    });
    assert.equal(missing.status, 'unavailable');

    const repo = await makeRepo();
    await writeFile(path.join(repo, 'a.txt'), 'a');
    await writeFile(path.join(repo, 'b.txt'), 'b');
    const exceeded = await scanCodeConnect({
      repo,
      targetNode,
      maxFiles: 1,
    });
    assert.equal(exceeded.status, 'unavailable');
    assert.equal(exceeded.scanBudget.exceeded, true);
    assert.equal(exceeded.warnings.includes('code_connect_scan_budget_exceeded'), true);
  });

  it('uses weak component-name matches only as low confidence mapped evidence', async () => {
    const repo = await makeRepo();
    await writeFile(
      path.join(repo, 'packages/ui/Button.tsx'),
      `
export function Button() {
  return null;
}
`,
    );

    const result = await scanCodeConnect({
      repo,
      targetNode,
      maxFiles: 5000,
    });

    assert.equal(result.status, 'mapped');
    assert.equal(result.mappings[0].confidence, 'low');
    assert.match(result.mappings[0].evidence, /weak component name/i);
  });

  it('returns failed instead of throwing when a Code Connect file cannot be read', async () => {
    const repo = await makeRepo();
    const filePath = path.join(repo, 'packages/ui/broken.figma.tsx');
    await writeFile(filePath, 'figma.connect(Button, "https://www.figma.com/design/file/Button?node-id=6127-21193", {});');
    await fs.chmod(filePath, 0o000);

    try {
      const result = await scanCodeConnect({
        repo,
        targetNode,
        maxFiles: 5000,
      });

      assert.equal(result.status, 'failed');
      assert.equal(result.warnings.includes('code_connect_file_read_failed'), true);
    } finally {
      await fs.chmod(filePath, 0o600);
    }
  });

  it('does not block by default but returns exit code 7 when require mode sees unavailable or failed', () => {
    assert.equal(resolveCodeConnectExitCode({ status: 'unavailable' }, { requireCodeConnect: false }), 0);
    assert.equal(resolveCodeConnectExitCode({ status: 'unmapped' }, { requireCodeConnect: true }), 0);
    assert.equal(resolveCodeConnectExitCode({ status: 'unavailable' }, { requireCodeConnect: true }), 7);
    assert.equal(resolveCodeConnectExitCode({ status: 'failed' }, { requireCodeConnect: true }), 7);
  });
});
