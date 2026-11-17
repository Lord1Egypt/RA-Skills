import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import { runReadFigmaContext } from '../scripts/read-figma-context.mjs';
import { validateArtifactDir } from '../scripts/validate-artifact.mjs';

async function makeTempDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-context-integration-test-'));
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, 'utf8'));
}

function figmaNode(id = '1:2') {
  return {
    id,
    name: 'Primary button',
    type: 'FRAME',
    absoluteBoundingBox: { x: 20, y: 30, width: 120, height: 40 },
    layoutMode: 'HORIZONTAL',
    itemSpacing: 8,
    paddingTop: 10,
    paddingRight: 12,
    paddingBottom: 10,
    paddingLeft: 12,
    cornerRadius: 6,
    fills: [{ type: 'SOLID', visible: true, color: { r: 0.1, g: 0.2, b: 0.3, a: 1 } }],
    children: [
      {
        id: '1:3',
        name: 'Label',
        type: 'TEXT',
        characters: 'Continue',
        style: { fontFamily: 'Inter', fontWeight: 600, fontSize: 14, lineHeightPx: 20 },
        fills: [{ type: 'SOLID', visible: true, color: { r: 1, g: 1, b: 1, a: 1 } }],
        absoluteBoundingBox: { x: 30, y: 40, width: 70, height: 16 },
      },
    ],
  };
}

function createFakeClient({ screenshotFails = false, nodeFails = false } = {}) {
  const rootNode = figmaNode();
  const siblingNode = {
    id: '1:4',
    name: 'Secondary button',
    type: 'FRAME',
    absoluteBoundingBox: { x: 150, y: 30, width: 120, height: 40 },
    layoutMode: 'HORIZONTAL',
  };
  const parentNode = {
    id: '1:1',
    name: 'Button group',
    type: 'FRAME',
    absoluteBoundingBox: { x: 10, y: 20, width: 280, height: 60 },
    layoutMode: 'HORIZONTAL',
    itemSpacing: 10,
    children: [rootNode, siblingNode],
  };
  const fileDocument = {
    id: '0:0',
    name: 'Document',
    type: 'DOCUMENT',
    children: [
      {
        id: '0:1',
        name: 'Page',
        type: 'CANVAS',
        children: [parentNode],
      },
    ],
  };
  const exportedNodeIds = [];
  return {
    exportedNodeIds,
    async getMe() {
      return { id: 'user-1', email: 'designer@example.com' };
    },
    async getNode({ nodeId }) {
      if (nodeFails) {
        const error = new Error('node missing');
        error.code = 'figma_node_not_found';
        error.retryable = false;
        throw error;
      }
      return {
        fileVersion: '123456',
        document: { ...rootNode, id: nodeId },
        node: { document: { ...rootNode, id: nodeId } },
      };
    },
    async getFile() {
      return {
        fileVersion: '123456',
        document: fileDocument,
      };
    },
    async exportNodeImage({ nodeId, outPath }) {
      if (screenshotFails) {
        const error = new Error('screenshot failed');
        error.code = 'screenshot_failed';
        throw error;
      }
      exportedNodeIds.push(nodeId);
      await fs.mkdir(path.dirname(outPath), { recursive: true });
      await fs.writeFile(outPath, Buffer.from([1, 2, 3]));
      return { path: outPath, byteLength: 3 };
    },
  };
}

describe('runReadFigmaContext', () => {
  it('writes an empty successful artifact for issue JSON without figma_urls', async () => {
    const tempDir = await makeTempDir();
    const issueJson = path.join(tempDir, 'issue.json');
    const out = path.join(tempDir, '.multica', 'figma-context');
    await fs.writeFile(issueJson, JSON.stringify({ identifier: 'MUL-EMPTY', figma_urls: [] }));

    const result = await runReadFigmaContext({
      argv: ['node', 'script', '--issue-json', issueJson, '--out', out],
      cwd: tempDir,
      env: {},
      createClient: () => {
        throw new Error('should not create client for empty figma_urls');
      },
    });

    assert.equal(result.exitCode, 0);
    assert.equal(result.code, 'figma_urls_empty');
    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    assert.deepEqual(manifest.urls, []);
  });

  it('reads a direct URL, writes artifacts, validates them, and records Code Connect status', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');
    const repo = path.join(tempDir, 'repo');
    await fs.mkdir(path.join(repo, '.git', 'info'), { recursive: true });
    await fs.mkdir(path.join(repo, 'packages', 'ui'), { recursive: true });
    await fs.writeFile(
      path.join(repo, 'packages', 'ui', 'button.figma.tsx'),
      "import figma from '@figma/code-connect';\nfigma.connect(Button, 'https://www.figma.com/design/fileKey123/File?node-id=1-2', {});\n",
    );
    const fakeClient = createFakeClient();

    const result = await runReadFigmaContext({
      argv: [
        'node',
        'script',
        '--url',
        'https://www.figma.com/design/fileKey123/File?node-id=1-2',
        '--out',
        out,
        '--repo',
        repo,
      ],
      cwd: tempDir,
      env: {},
      createClient: () => fakeClient,
    });

    assert.equal(result.exitCode, 0);
    assert.equal(result.runDirRelative, path.relative(out, result.runDir));
    assert.equal(path.isAbsolute(result.runDirRelative), false);
    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    const contextTree = await readJson(path.join(result.runDir, 'urls', '001', 'context-tree.json'));
    assert.equal(manifest.artifactRoot, '..');
    assert.equal(manifest.runDir, '.');
    assert.equal(path.isAbsolute(manifest.artifactRoot), false);
    assert.equal(path.isAbsolute(manifest.runDir), false);
    assert.equal(manifest.urls[0].status, 'succeeded');
    assert.equal(manifest.urls[0].codeConnectStatus, 'mapped');
    assert.equal(manifest.urls[0].targetScreenshot, 'urls/001/screenshots/target.png');
    assert.equal(manifest.urls[0].parentScreenshot, 'urls/001/screenshots/parent.png');
    assert.equal(manifest.urls[0].candidateScreenshots.length, 1);
    assert.equal(manifest.urls[0].candidateScreenshots[0].nodeId, '1:4');
    assert.deepEqual(fakeClient.exportedNodeIds, ['1:2', '1:1', '1:4']);
    assert.deepEqual(
      contextTree.parents.map((entry) => entry.id),
      ['1:1', '0:1', '0:0'],
    );
    assert.deepEqual(
      contextTree.siblings.map((entry) => entry.id),
      ['1:4'],
    );
    await fs.access(path.join(result.runDir, 'urls', '001', 'screenshots', 'parent.png'));
    await fs.access(path.join(result.runDir, 'urls', '001', 'screenshots', 'candidates', '001.png'));
    assert.deepEqual(await validateArtifactDir(result.runDir), { ok: true, errors: [] });
  });

  it('keeps node artifacts when screenshots fail by default and fails with exit code 5 when required', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');
    const baseArgv = [
      'node',
      'script',
      '--url',
      'https://www.figma.com/design/fileKey123/File?node-id=1-2',
      '--out',
      out,
    ];

    const defaultResult = await runReadFigmaContext({
      argv: baseArgv,
      cwd: tempDir,
      env: {},
      createClient: () => createFakeClient({ screenshotFails: true }),
    });

    assert.equal(defaultResult.exitCode, 0);
    let manifest = await readJson(path.join(defaultResult.runDir, 'manifest.json'));
    assert.equal(manifest.urls[0].status, 'partial_succeeded');
    assert.equal(manifest.urls[0].targetScreenshot, null);

    const requiredResult = await runReadFigmaContext({
      argv: [...baseArgv, '--require-screenshots'],
      cwd: tempDir,
      env: {},
      createClient: () => createFakeClient({ screenshotFails: true }),
    });

    assert.equal(requiredResult.exitCode, 5);
    manifest = await readJson(path.join(requiredResult.runDir, 'manifest.json'));
    assert.equal(manifest.urls[0].status, 'partial_succeeded');
  });

  it('does not fail Figma reads when best-effort Code Connect scanning fails', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');
    const repo = path.join(tempDir, 'repo');
    const brokenCodeConnectFile = path.join(repo, 'packages', 'ui', 'broken.figma.tsx');
    await fs.mkdir(path.dirname(brokenCodeConnectFile), { recursive: true });
    await fs.writeFile(
      brokenCodeConnectFile,
      "figma.connect(Button, 'https://www.figma.com/design/fileKey123/File?node-id=1-2', {});\n",
    );
    await fs.chmod(brokenCodeConnectFile, 0o000);

    try {
      const result = await runReadFigmaContext({
        argv: [
          'node',
          'script',
          '--url',
          'https://www.figma.com/design/fileKey123/File?node-id=1-2',
          '--out',
          out,
          '--repo',
          repo,
        ],
        cwd: tempDir,
        env: {},
        createClient: () => createFakeClient(),
      });

      assert.equal(result.exitCode, 0);
      const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
      const codeConnect = await readJson(path.join(result.runDir, 'urls', '001', 'code-connect.json'));
      assert.equal(manifest.urls[0].status, 'succeeded');
      assert.equal(manifest.urls[0].blocking, false);
      assert.equal(manifest.urls[0].codeConnectStatus, 'failed');
      assert.equal(codeConnect.status, 'failed');
    } finally {
      await fs.chmod(brokenCodeConnectFile, 0o600);
    }
  });

  it('marks the URL as blocking when require-code-connect sees unavailable or failed evidence', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');
    const repo = path.join(tempDir, 'repo');
    await fs.mkdir(path.join(repo, '.git', 'info'), { recursive: true });

    const result = await runReadFigmaContext({
      argv: [
        'node',
        'script',
        '--url',
        'https://www.figma.com/design/fileKey123/File?node-id=1-2',
        '--out',
        out,
        '--repo',
        repo,
        '--require-code-connect',
      ],
      cwd: tempDir,
      env: {},
      createClient: () => createFakeClient(),
    });

    assert.equal(result.exitCode, 7);
    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    assert.equal(manifest.urls[0].status, 'succeeded');
    assert.equal(manifest.urls[0].codeConnectStatus, 'unavailable');
    assert.equal(manifest.urls[0].blocking, true);
  });

  it('uses a bounded expanded file read when shallow parent context misses a leaf target', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');
    const targetNode = {
      id: '9:9',
      name: 'Title',
      type: 'TEXT',
      characters: 'Age gating',
      style: { fontFamily: 'Inter', fontWeight: 500, fontSize: 16, lineHeightPx: 24 },
      absoluteBoundingBox: { x: 24, y: 32, width: 90, height: 24 },
      children: [],
    };
    const parentNode = {
      id: '9:8',
      name: 'Alert row',
      type: 'FRAME',
      layoutMode: 'HORIZONTAL',
      absoluteBoundingBox: { x: 16, y: 24, width: 300, height: 48 },
      children: [targetNode],
    };
    const shallowDocument = {
      id: '0:0',
      name: 'Document',
      type: 'DOCUMENT',
      children: [{ id: '0:1', name: 'Page', type: 'CANVAS', children: [] }],
    };
    const expandedDocument = {
      id: '0:0',
      name: 'Document',
      type: 'DOCUMENT',
      children: [{ id: '0:1', name: 'Page', type: 'CANVAS', children: [parentNode] }],
    };
    const getFileDepths = [];
    const client = {
      async getNode() {
        return { fileVersion: '123456', document: targetNode };
      },
      async getFile({ depth }) {
        getFileDepths.push(depth);
        return {
          fileVersion: '123456',
          document: getFileDepths.length === 1 ? shallowDocument : expandedDocument,
        };
      },
      async exportNodeImage({ outPath }) {
        await fs.mkdir(path.dirname(outPath), { recursive: true });
        await fs.writeFile(outPath, Buffer.from([1, 2, 3]));
        return { path: outPath, byteLength: 3 };
      },
    };

    const result = await runReadFigmaContext({
      argv: [
        'node',
        'script',
        '--url',
        'https://www.figma.com/design/fileKey123/File?node-id=9-9',
        '--out',
        out,
      ],
      cwd: tempDir,
      env: {},
      createClient: () => client,
    });

    assert.equal(result.exitCode, 0);
    assert.deepEqual(getFileDepths, [6, 10]);
    const contextTree = await readJson(path.join(result.runDir, 'urls', '001', 'context-tree.json'));
    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    assert.equal(contextTree.parents[0].id, '9:8');
    assert.equal(contextTree.bestTargetInterpretation.id, '9:8');
    assert.equal(contextTree.warnings.includes('parent_context_expanded_search_used'), true);
    assert.equal(contextTree.warnings.includes('target_may_be_child_node'), true);
    assert.equal(manifest.urls[0].parentScreenshot, 'urls/001/screenshots/parent.png');
  });

  it('fails the URL when artifact output exceeds the per-url artifact budget', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');
    const result = await runReadFigmaContext({
      argv: [
        'node',
        'script',
        '--url',
        'https://www.figma.com/design/fileKey123/File?node-id=1-2',
        '--out',
        out,
        '--max-artifact-mib-per-url',
        '0.00001',
      ],
      cwd: tempDir,
      env: {},
      createClient: () => createFakeClient(),
    });

    assert.equal(result.exitCode, 6);
    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    assert.equal(manifest.urls[0].status, 'failed');
    assert.equal(manifest.urls[0].errorCode, 'artifact_budget_exceeded');
    assert.equal(manifest.urls[0].blocking, true);
    assert.equal(manifest.failures[0].errorCode, 'artifact_budget_exceeded');
  });

  it('returns non-zero when every URL node read fails', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');

    const result = await runReadFigmaContext({
      argv: [
        'node',
        'script',
        '--url',
        'https://www.figma.com/design/fileKey123/File?node-id=1-2',
        '--out',
        out,
      ],
      cwd: tempDir,
      env: {},
      createClient: () => createFakeClient({ nodeFails: true }),
    });

    assert.equal(result.exitCode, 4);
    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    assert.equal(manifest.urls[0].status, 'failed');
    assert.equal(manifest.urls[0].errorCode, 'figma_node_not_found');
  });

  it('returns exit code 3 when every URL fails before Figma reads because token env is missing', async () => {
    const tempDir = await makeTempDir();
    const out = path.join(tempDir, '.multica', 'figma-context');
    const client = {
      async getNode() {
        const error = new Error('figma_env_missing: missing or invalid Figma token fields');
        error.code = 'figma_env_missing';
        error.retryable = false;
        throw error;
      },
    };

    const result = await runReadFigmaContext({
      argv: [
        'node',
        'script',
        '--url',
        'https://www.figma.com/design/fileKey123/File?node-id=1-2',
        '--out',
        out,
      ],
      cwd: tempDir,
      env: {},
      createClient: () => client,
    });

    assert.equal(result.exitCode, 3);
    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    assert.equal(manifest.urls[0].status, 'failed');
    assert.equal(manifest.urls[0].errorCode, 'figma_env_missing');
  });
});
