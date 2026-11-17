import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';

import {
  ensureGitArtifactIgnore,
  writeFigmaContextArtifacts,
} from '../scripts/lib/figma-artifact-writer.mjs';
import { validateArtifactDir } from '../scripts/validate-artifact.mjs';

async function makeTempDir() {
  return fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-artifact-test-'));
}

async function readJson(filePath) {
  return JSON.parse(await fs.readFile(filePath, 'utf8'));
}

function successfulUrlResult(overrides = {}) {
  return {
    ordinal: 1,
    sourceUrl: 'https://www.figma.com/design/fileKey123/File?node-id=1-2',
    fileKey: 'fileKey123',
    originalNodeId: '1-2',
    canonicalNodeId: '1:2',
    figmaFileVersion: '123456',
    status: 'succeeded',
    errorCode: null,
    errorMessage: null,
    retryable: false,
    blocking: false,
    duplicateOf: null,
    targetNode: {
      schemaVersion: 'figma-target-node/v1',
      sourceUrl: 'https://www.figma.com/design/fileKey123/File?node-id=1-2',
      fileKey: 'fileKey123',
      canonicalNodeId: '1:2',
      rawNode: { id: '1:2', name: 'Target', type: 'FRAME' },
    },
    contextTree: {
      schemaVersion: 'figma-context-tree/v1',
      target: { id: '1:2', name: 'Target', type: 'FRAME' },
      parents: [],
      children: [],
      siblings: [],
      candidates: [{ id: '1:2', name: 'Target', type: 'FRAME', source: 'target' }],
      warnings: [],
    },
    designProperties: {
      schemaVersion: 'figma-design-properties/v1',
      nodes: [
        {
          id: '1:2',
          name: 'Target',
          type: 'FRAME',
          raw: {},
          normalized: {
            width: '120px',
            height: '40px',
            backgroundColor: { css: 'rgba(26, 51, 77, 1)', hex: '#1A334D' },
            padding: '10px 12px 10px 12px',
            borderRadius: '6px',
          },
          warnings: [],
        },
      ],
      warnings: [],
      missingFields: [],
    },
    codeConnect: {
      schemaVersion: 'figma-code-connect-context/v1',
      status: 'mapped',
      source: 'local-code-connect-scan',
      scanBudget: { maxFiles: 5000, scannedFiles: 1, exceeded: false },
      mappings: [
        {
          figmaNodeId: '1:2',
          figmaComponentName: 'Button / Primary',
          codeComponentName: 'Button',
          sourcePath: 'packages/ui/button.tsx',
          confidence: 'high',
          evidence: 'matched component key in figma.connect()',
        },
      ],
      warnings: [],
    },
    cssHints: '.figma-target-1-2 {\\n  width: 120px;\\n}\\n',
    screenshots: {
      target: { sourcePath: null, artifactPath: 'urls/001/screenshots/target.png' },
      parent: null,
      candidates: [],
    },
    summary: {
      bestTargetInterpretation: 'Target node',
      visualRequirements: [],
      openQuestions: [],
    },
    ...overrides,
  };
}

describe('ensureGitArtifactIgnore', () => {
  it('writes generated artifact paths to .git/info/exclude without touching tracked .gitignore', async () => {
    const repo = await makeTempDir();
    await fs.mkdir(path.join(repo, '.git', 'info'), { recursive: true });
    await fs.writeFile(path.join(repo, '.gitignore'), 'tracked-rule\\n');

    const result = await ensureGitArtifactIgnore(repo);

    assert.equal(result.verified, true);
    const exclude = await fs.readFile(path.join(repo, '.git', 'info', 'exclude'), 'utf8');
    assert.equal(exclude.includes('.multica/figma-context/'), true);
    assert.equal(exclude.includes('.multica/tmp/'), true);
    assert.equal(await fs.readFile(path.join(repo, '.gitignore'), 'utf8'), 'tracked-rule\\n');
  });

  it('marks artifact ignore as unverified when repo is not a Git repository', async () => {
    const repo = await makeTempDir();

    const result = await ensureGitArtifactIgnore(repo);

    assert.equal(result.verified, false);
    assert.equal(result.warning, 'artifact_ignore_unverified');
  });
});

describe('writeFigmaContextArtifacts', () => {
  it('writes manifest, summary, per-url JSON, CSS hints, screenshots, and validates the artifact dir', async () => {
    const repo = await makeTempDir();
    const out = path.join(repo, '.multica', 'figma-context');
    await fs.mkdir(path.join(repo, '.git', 'info'), { recursive: true });
    await fs.mkdir(out, { recursive: true });
    const screenshotSource = path.join(out, 'source-target.png');
    await fs.writeFile(screenshotSource, Buffer.from([1, 2, 3]));

    const result = await writeFigmaContextArtifacts({
      artifactRoot: out,
      repo,
      issue: { identifier: 'MUL-123', id: 'issue-uuid-1' },
      source: 'figma_urls',
      inputShape: 'top-level',
      urlResults: [
        successfulUrlResult({
          screenshots: {
            target: { sourcePath: screenshotSource, artifactPath: 'urls/001/screenshots/target.png' },
            parent: null,
            candidates: [],
          },
        }),
        {
          ordinal: 2,
          sourceUrl: 'https://www.figma.com/design/fileKey123/File?node-id=9-9',
          fileKey: 'fileKey123',
          originalNodeId: '9-9',
          canonicalNodeId: '9:9',
          figmaFileVersion: null,
          status: 'failed',
          errorCode: 'figma_node_not_found',
          errorMessage: 'node missing',
          retryable: false,
          blocking: true,
          duplicateOf: null,
        },
      ],
      generatedAt: '2026-07-22T00:00:00.000Z',
    });

    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    const summary = await fs.readFile(path.join(result.runDir, 'summary.md'), 'utf8');
    const targetNode = await readJson(path.join(result.runDir, 'urls', '001', 'target-node.json'));
    const contextTree = await readJson(path.join(result.runDir, 'urls', '001', 'context-tree.json'));
    const designProperties = await readJson(path.join(result.runDir, 'urls', '001', 'design-properties.json'));
    const codeConnect = await readJson(path.join(result.runDir, 'urls', '001', 'code-connect.json'));
    const cssHints = await fs.readFile(path.join(result.runDir, 'urls', '001', 'css-hints.css'), 'utf8');
    const screenshot = await fs.readFile(path.join(result.runDir, 'urls', '001', 'screenshots', 'target.png'));

    assert.equal(manifest.schemaVersion, 'figma-context-artifact/v1');
    assert.equal(manifest.issueIdentifier, 'MUL-123');
    assert.equal(manifest.issueUUID, 'issue-uuid-1');
    assert.equal(manifest.artifactRoot, '.multica/figma-context');
    assert.equal(manifest.runDir, '.multica/figma-context/MUL-123');
    assert.equal(path.isAbsolute(manifest.artifactRoot), false);
    assert.equal(path.isAbsolute(manifest.runDir), false);
    assert.equal(manifest.urls.length, 2);
    assert.equal(manifest.urls[0].status, 'succeeded');
    assert.equal(manifest.urls[0].targetScreenshot, 'urls/001/screenshots/target.png');
    assert.equal(manifest.urls[0].codeConnectStatus, 'mapped');
    assert.equal(manifest.urls[1].status, 'failed');
    assert.equal(manifest.failures[0].errorCode, 'figma_node_not_found');
    assert.equal(manifest.artifactIgnore.verified, true);
    assert.match(summary, /## URL 1/);
    assert.match(summary, /## URL 2/);
    assert.match(summary, /figma_node_not_found/);
    assert.match(summary, /background: rgba\(26, 51, 77, 1\)/);
    assert.equal(targetNode.schemaVersion, 'figma-target-node/v1');
    assert.equal(contextTree.schemaVersion, 'figma-context-tree/v1');
    assert.equal(designProperties.schemaVersion, 'figma-design-properties/v1');
    assert.equal(codeConnect.schemaVersion, 'figma-code-connect-context/v1');
    assert.match(cssHints, /width: 120px/);
    assert.deepEqual([...screenshot], [1, 2, 3]);

    assert.deepEqual(await validateArtifactDir(result.runDir), {
      ok: true,
      errors: [],
    });
  });

  it('validator fails when manifest parent or candidate screenshot paths are missing on disk', async () => {
    const out = await makeTempDir();
    const parentSource = path.join(out, 'source-parent.png');
    const candidateSource = path.join(out, 'source-candidate.png');
    await fs.writeFile(parentSource, Buffer.from([4, 5, 6]));
    await fs.writeFile(candidateSource, Buffer.from([7, 8, 9]));

    const result = await writeFigmaContextArtifacts({
      artifactRoot: out,
      repo: null,
      issue: { identifier: 'MUL-SCREENSHOTS', id: null },
      source: 'figma_urls',
      inputShape: 'top-level',
      urlResults: [
        successfulUrlResult({
          screenshots: {
            target: null,
            parent: {
              nodeId: '1:1',
              name: 'Parent',
              source: 'parent',
              sourcePath: parentSource,
              artifactPath: 'urls/001/screenshots/parent.png',
            },
            candidates: [
              {
                nodeId: '1:4',
                name: 'Candidate',
                source: 'sibling',
                sourcePath: candidateSource,
                artifactPath: 'urls/001/screenshots/candidates/001.png',
              },
            ],
          },
        }),
      ],
      generatedAt: '2026-07-22T00:00:00.000Z',
    });

    await fs.rm(path.join(result.runDir, 'urls', '001', 'screenshots', 'parent.png'));
    await fs.rm(path.join(result.runDir, 'urls', '001', 'screenshots', 'candidates', '001.png'));

    const validation = await validateArtifactDir(result.runDir);

    assert.equal(validation.ok, false);
    assert.equal(validation.errors.some((error) => error.includes('screenshots/parent.png: missing')), true);
    assert.equal(validation.errors.some((error) => error.includes('screenshots/candidates/001.png: missing')), true);
  });

  it('summarizes transparent backgrounds without converting them to black hex', async () => {
    const out = await makeTempDir();

    const result = await writeFigmaContextArtifacts({
      artifactRoot: out,
      repo: null,
      issue: { identifier: 'MUL-TRANSPARENT', id: null },
      source: 'figma_urls',
      inputShape: 'top-level',
      urlResults: [
        successfulUrlResult({
          designProperties: {
            schemaVersion: 'figma-design-properties/v1',
            nodes: [
              {
                id: '1:2',
                name: 'Target',
                type: 'FRAME',
                raw: {},
                normalized: {
                  backgroundColor: {
                    css: 'rgba(0, 0, 0, 0)',
                    hex: '#000000',
                    figma: { r: 0, g: 0, b: 0, a: 0 },
                  },
                },
                warnings: [],
              },
            ],
            warnings: [],
            missingFields: [],
          },
          summary: {
            bestTargetInterpretation: 'Target node',
            visualRequirements: [],
            openQuestions: [],
          },
        }),
      ],
      generatedAt: '2026-07-22T00:00:00.000Z',
    });

    const summary = await fs.readFile(path.join(result.runDir, 'summary.md'), 'utf8');

    assert.match(summary, /background: transparent \(rgba\(0, 0, 0, 0\)\)/);
    assert.doesNotMatch(summary, /background: #000000/);
  });

  it('marks a URL as failed when its artifact directory exceeds the configured budget', async () => {
    const out = await makeTempDir();

    const result = await writeFigmaContextArtifacts({
      artifactRoot: out,
      repo: null,
      issue: { identifier: 'MUL-BUDGET', id: null },
      source: 'figma_urls',
      inputShape: 'top-level',
      urlResults: [successfulUrlResult()],
      generatedAt: '2026-07-22T00:00:00.000Z',
      maxArtifactMiBPerUrl: 0.00001,
    });

    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    const summary = await fs.readFile(path.join(result.runDir, 'summary.md'), 'utf8');

    assert.equal(manifest.urls[0].status, 'failed');
    assert.equal(manifest.urls[0].errorCode, 'artifact_budget_exceeded');
    assert.equal(manifest.urls[0].blocking, true);
    assert.equal(manifest.failures[0].errorCode, 'artifact_budget_exceeded');
    assert.match(summary, /artifact_budget_exceeded/);
    assert.deepEqual(await validateArtifactDir(result.runDir), { ok: true, errors: [] });
  });

  it('redacts tokens and temporary signed image URLs from every artifact', async () => {
    const out = await makeTempDir();
    const run = await writeFigmaContextArtifacts({
      artifactRoot: out,
      repo: null,
      issue: { identifier: 'MUL-124', id: null },
      source: 'figma_urls',
      inputShape: 'top-level',
      urlResults: [
        successfulUrlResult({
          targetNode: {
            schemaVersion: 'figma-target-node/v1',
            sourceUrl: 'https://www.figma.com/design/fileKey123/File?node-id=1-2',
            fileKey: 'fileKey123',
            canonicalNodeId: '1:2',
            rawNode: {
              id: '1:2',
              token: 'figd_access_token_secret',
              temporaryUrl: 'https://figma-image.example.com/tmp.png?sig=secret',
              headers: { Authorization: 'Bearer figd_access_token_secret' },
            },
          },
          errorMessage: 'Authorization: Bearer figd_access_token_secret',
        }),
      ],
      generatedAt: '2026-07-22T00:00:00.000Z',
    });

    const artifactText = await fs.readFile(path.join(run.runDir, 'manifest.json'), 'utf8')
      + await fs.readFile(path.join(run.runDir, 'summary.md'), 'utf8')
      + await fs.readFile(path.join(run.runDir, 'urls', '001', 'target-node.json'), 'utf8');

    assert.equal(artifactText.includes('figd_access_token_secret'), false);
    assert.equal(artifactText.includes('sig=secret'), false);
    assert.match(artifactText, /artifact_ignore_unverified/);
  });

  it('validator rejects generic temporary signed URL query parameters in text artifacts', async () => {
    const out = await makeTempDir();
    const run = await writeFigmaContextArtifacts({
      artifactRoot: out,
      repo: null,
      issue: { identifier: 'MUL-125', id: null },
      source: 'figma_urls',
      inputShape: 'top-level',
      urlResults: [successfulUrlResult()],
      generatedAt: '2026-07-22T00:00:00.000Z',
    });

    const sourceUrlPath = path.join(run.runDir, 'urls', '001', 'source-url.txt');
    await fs.appendFile(
      sourceUrlPath,
      '\nhttps://figma-image.example.com/tmp.png?sig=abc123\nhttps://figma-image.example.com/tmp.png?signature=abc123\nhttps://figma-image.example.com/tmp.png?X-Amz-Signature=abc123\n',
    );

    const validation = await validateArtifactDir(run.runDir);

    assert.equal(validation.ok, false);
    assert.equal(validation.errors.some((error) => error.includes('forbidden_secret_or_temp_url')), true);
  });

  it('writes an empty successful artifact when figma_urls is empty', async () => {
    const out = await makeTempDir();

    const result = await writeFigmaContextArtifacts({
      artifactRoot: out,
      repo: null,
      issue: { identifier: 'MUL-EMPTY', id: null },
      source: null,
      inputShape: null,
      urlResults: [],
      generatedAt: '2026-07-22T00:00:00.000Z',
      emptyReason: 'figma_urls_empty',
    });

    const manifest = await readJson(path.join(result.runDir, 'manifest.json'));
    const summary = await fs.readFile(path.join(result.runDir, 'summary.md'), 'utf8');

    assert.deepEqual(manifest.urls, []);
    assert.match(summary, /figma_urls_empty/);
    assert.deepEqual(await validateArtifactDir(result.runDir), { ok: true, errors: [] });
  });
});
