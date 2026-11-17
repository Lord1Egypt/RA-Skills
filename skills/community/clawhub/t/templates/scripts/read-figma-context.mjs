#!/usr/bin/env node

import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

import { formatHelp, formatVersion, parseCliArgs } from './lib/cli-args.mjs';
import { resolveCodeConnectExitCode, scanCodeConnect } from './lib/figma-code-connect.mjs';
import { writeFigmaContextArtifacts } from './lib/figma-artifact-writer.mjs';
import { expandFigmaNodeContext } from './lib/figma-node-expander.mjs';
import { createFigmaRestClient } from './lib/figma-rest-client.mjs';
import { buildCssHints, normalizeDesignProperties } from './lib/figma-style-normalizer.mjs';
import { withFigmaTokenRetry } from './lib/figma-token-store.mjs';
import {
  dedupeParsedUrls,
  extractFigmaUrlsFromIssue,
  parseFigmaDesignUrl,
} from './lib/figma-url.mjs';
import { createStableError, redactString } from './lib/redact.mjs';
import { validateArtifactDir } from './validate-artifact.mjs';

const scriptPath = fileURLToPath(import.meta.url);
const skillRoot = path.resolve(path.dirname(scriptPath), '..');

async function readIssueJson(filePath) {
  const raw = await fs.readFile(filePath, 'utf8');
  return JSON.parse(raw);
}

function issueMetaFromMode(mode, issue) {
  if (mode === 'url') {
    return {
      identifier: null,
      id: null,
    };
  }
  return {
    identifier: issue?.identifier ?? issue?.issueIdentifier ?? null,
    id: issue?.id ?? issue?.uuid ?? issue?.issueUUID ?? null,
  };
}

function slashPath(filePath) {
  return filePath.split(path.sep).join('/');
}

function relativeRunDir(runDir, config) {
  if (config.repo) {
    const relativeToRepo = path.relative(config.repo, runDir);
    if (relativeToRepo && !relativeToRepo.startsWith('..') && !path.isAbsolute(relativeToRepo)) {
      return slashPath(relativeToRepo);
    }
  }
  return slashPath(path.relative(config.out, runDir) || '.');
}

function asStableFailure(error) {
  return {
    code: error?.code ?? 'figma_read_failed',
    message: redactString(error?.message ?? 'Figma read failed'),
    retryable: Boolean(error?.retryable),
  };
}

function targetNodeArtifact({ parsedUrl, nodeResult }) {
  return {
    schemaVersion: 'figma-target-node/v1',
    sourceUrl: parsedUrl.url,
    fileKey: parsedUrl.fileKey,
    canonicalNodeId: parsedUrl.nodeId,
    rawNode: nodeResult.document,
  };
}

function traverseNodes(node, visitor) {
  if (!node) {
    return;
  }
  visitor(node);
  for (const child of node.children ?? []) {
    traverseNodes(child, visitor);
  }
}

function findNodeById(rootNode, nodeId) {
  let match = null;
  traverseNodes(rootNode, (node) => {
    if (!match && node?.id === nodeId) {
      match = node;
    }
  });
  return match;
}

function countNodes(rootNode, limit = Number.POSITIVE_INFINITY) {
  let count = 0;
  traverseNodes(rootNode, () => {
    if (count <= limit) {
      count += 1;
    }
  });
  return count;
}

function isLeafLikeTarget(node) {
  const leafTypes = new Set(['TEXT', 'VECTOR', 'BOOLEAN_OPERATION', 'LINE', 'ELLIPSE', 'POLYGON', 'STAR', 'IMAGE']);
  return leafTypes.has(node?.type) || !Array.isArray(node?.children) || node.children.length === 0;
}

function mergeTargetSubtree(rootNode, targetNodeId, targetSubtree) {
  if (!rootNode || rootNode.id === targetNodeId) {
    return targetSubtree;
  }
  if (!Array.isArray(rootNode.children) || rootNode.children.length === 0) {
    return rootNode;
  }
  return {
    ...rootNode,
    children: rootNode.children.map((child) => mergeTargetSubtree(child, targetNodeId, targetSubtree)),
  };
}

async function resolveContextRoot({ client, parsedUrl, nodeResult, config }) {
  const warnings = [];
  try {
    const fileResult = await client.getFile({
      fileKey: parsedUrl.fileKey,
      depth: config.budgets.maxParentDepth,
    });
    if (nodeResult.fileVersion && fileResult.fileVersion && nodeResult.fileVersion !== fileResult.fileVersion) {
      warnings.push('figma_file_version_changed');
    }
    if (!findNodeById(fileResult.document, parsedUrl.nodeId)) {
      warnings.push('parent_context_target_not_found');
      const expandedDepth = config.budgets.maxParentDepth + config.budgets.maxChildDepth;
      if (isLeafLikeTarget(nodeResult.document) && expandedDepth > config.budgets.maxParentDepth) {
        try {
          const expandedFileResult = await client.getFile({
            fileKey: parsedUrl.fileKey,
            depth: expandedDepth,
          });
          if (nodeResult.fileVersion && expandedFileResult.fileVersion && nodeResult.fileVersion !== expandedFileResult.fileVersion) {
            warnings.push('figma_file_version_changed');
          }
          if (countNodes(expandedFileResult.document, config.budgets.maxNodesPerUrl) > config.budgets.maxNodesPerUrl) {
            warnings.push('expansion_budget_exceeded');
            return {
              rootNode: nodeResult.document,
              warnings,
            };
          }
          if (findNodeById(expandedFileResult.document, parsedUrl.nodeId)) {
            warnings.push('parent_context_expanded_search_used');
            return {
              rootNode: mergeTargetSubtree(expandedFileResult.document, parsedUrl.nodeId, nodeResult.document),
              warnings,
            };
          }
          warnings.push('parent_context_expanded_target_not_found');
        } catch (error) {
          warnings.push(`parent_context_expanded_read_failed:${error?.code ?? 'unknown'}`);
        }
      }
      return {
        rootNode: nodeResult.document,
        warnings,
      };
    }
    return {
      rootNode: mergeTargetSubtree(fileResult.document, parsedUrl.nodeId, nodeResult.document),
      warnings,
    };
  } catch (error) {
    warnings.push(`parent_context_read_failed:${error?.code ?? 'unknown'}`);
    return {
      rootNode: nodeResult.document,
      warnings,
    };
  }
}

function nodesForDesignProperties(contextTree, nodeResult, contextRoot) {
  const byId = new Map();
  const indexedNodes = new Map();
  function add(node) {
    if (node?.id) {
      byId.set(node.id, node);
    }
  }
  traverseNodes(contextRoot, (node) => {
    if (node?.id) {
      indexedNodes.set(node.id, node);
    }
  });
  traverseNodes(nodeResult.document, (node) => {
    if (node?.id) {
      indexedNodes.set(node.id, node);
    }
  });
  add(nodeResult.document);
  for (const summary of [
    contextTree.target,
    ...(contextTree.parents ?? []),
    ...(contextTree.children ?? []),
    ...(contextTree.siblings ?? []),
    ...(contextTree.candidates ?? []),
  ]) {
    const indexed = indexedNodes.get(summary?.id);
    if (indexed) {
      add(indexed);
    }
  }
  return [...byId.values()];
}

function screenshotArtifactPrefix(ordinal) {
  return `urls/${String(ordinal).padStart(3, '0')}/screenshots`;
}

async function exportScreenshot({ client, fileKey, node, artifactPath, tempPath, scale }) {
  await client.exportNodeImage({
    fileKey,
    nodeId: node.id,
    outPath: tempPath,
    scale,
  });
  return {
    nodeId: node.id,
    name: node.name ?? null,
    source: node.source ?? null,
    sourcePath: tempPath,
    artifactPath,
  };
}

async function exportContextScreenshots({ client, parsedUrl, contextTree, config, tempDir }) {
  const ordinalName = String(parsedUrl.ordinal).padStart(3, '0');
  const artifactPrefix = screenshotArtifactPrefix(parsedUrl.ordinal);
  const warnings = [];
  const screenshots = {
    target: null,
    parent: null,
    candidates: [],
  };
  let targetError = null;
  let attempts = 0;

  const targetNode = contextTree.target?.id ? contextTree.target : { id: parsedUrl.nodeId, source: 'target' };
  try {
    attempts += 1;
    screenshots.target = await exportScreenshot({
      client,
      fileKey: parsedUrl.fileKey,
      node: targetNode,
      artifactPath: `${artifactPrefix}/target.png`,
      tempPath: path.join(tempDir, `url-${ordinalName}-target.png`),
      scale: config.budgets.screenshotScale,
    });
  } catch (error) {
    targetError = asStableFailure(error);
  }

  const seenNodeIds = new Set([targetNode.id]);
  const parentNode = contextTree.parents?.[0];
  if (parentNode?.id && attempts < config.budgets.maxScreenshotsPerUrl) {
    attempts += 1;
    seenNodeIds.add(parentNode.id);
    try {
      screenshots.parent = await exportScreenshot({
        client,
        fileKey: parsedUrl.fileKey,
        node: parentNode,
        artifactPath: `${artifactPrefix}/parent.png`,
        tempPath: path.join(tempDir, `url-${ordinalName}-parent.png`),
        scale: config.budgets.screenshotScale,
      });
    } catch (error) {
      warnings.push(`parent_screenshot_failed:${error?.code ?? 'unknown'}`);
    }
  }

  let candidateIndex = 1;
  for (const candidate of contextTree.candidates ?? []) {
    if (!candidate?.id || seenNodeIds.has(candidate.id)) {
      continue;
    }
    if (attempts >= config.budgets.maxScreenshotsPerUrl) {
      warnings.push('screenshot_budget_exceeded');
      break;
    }
    attempts += 1;
    seenNodeIds.add(candidate.id);
    const screenshotName = String(candidateIndex).padStart(3, '0');
    try {
      screenshots.candidates.push(
        await exportScreenshot({
          client,
          fileKey: parsedUrl.fileKey,
          node: candidate,
          artifactPath: `${artifactPrefix}/candidates/${screenshotName}.png`,
          tempPath: path.join(tempDir, `url-${ordinalName}-candidate-${screenshotName}.png`),
          scale: config.budgets.screenshotScale,
        }),
      );
      candidateIndex += 1;
    } catch (error) {
      warnings.push(`candidate_screenshot_failed:${candidate.id}:${error?.code ?? 'unknown'}`);
    }
  }

  return {
    screenshots,
    targetError,
    warnings,
  };
}

async function processParsedUrl({ parsedUrl, config, client, tempDir }) {
  if (!parsedUrl.ok) {
    return {
      ordinal: parsedUrl.ordinal,
      sourceUrl: parsedUrl.url,
      fileKey: parsedUrl.fileKey ?? null,
      originalNodeId: parsedUrl.originalNodeId ?? null,
      canonicalNodeId: parsedUrl.nodeId ?? null,
      figmaFileVersion: null,
      status: 'failed',
      errorCode: parsedUrl.errorCode,
      errorMessage: parsedUrl.errorCode,
      retryable: false,
      blocking: true,
      duplicateOf: parsedUrl.duplicateOf ?? null,
    };
  }

  if (parsedUrl.duplicateOf) {
    return {
      ordinal: parsedUrl.ordinal,
      sourceUrl: parsedUrl.url,
      fileKey: parsedUrl.fileKey,
      originalNodeId: parsedUrl.originalNodeId,
      canonicalNodeId: parsedUrl.nodeId,
      figmaFileVersion: null,
      status: 'skipped',
      errorCode: null,
      errorMessage: null,
      retryable: false,
      blocking: false,
      duplicateOf: parsedUrl.duplicateOf,
    };
  }

  try {
    const nodeResult = await client.getNode({
      fileKey: parsedUrl.fileKey,
      nodeId: parsedUrl.nodeId,
      depth: config.budgets.maxChildDepth,
    });
    const contextRoot = await resolveContextRoot({ client, parsedUrl, nodeResult, config });
    const contextTree = expandFigmaNodeContext({
      targetNodeId: parsedUrl.nodeId,
      rootNode: contextRoot.rootNode,
      budgets: config.budgets,
    });
    contextTree.warnings = [...new Set([...(contextTree.warnings ?? []), ...contextRoot.warnings])];
    const designProperties = normalizeDesignProperties({
      nodes: nodesForDesignProperties(contextTree, nodeResult, contextRoot.rootNode),
      contextTree,
    });
    const cssHints = buildCssHints(designProperties);
    const codeConnect = await scanCodeConnect({
      repo: config.repo,
      targetNode: {
        id: parsedUrl.nodeId,
        name: nodeResult.document?.name,
        type: nodeResult.document?.type,
        componentKey: nodeResult.document?.componentKey,
        componentName: nodeResult.document?.componentName ?? nodeResult.document?.name,
      },
      maxFiles: 5000,
    });

    const screenshotResult = await exportContextScreenshots({
      client,
      parsedUrl,
      contextTree,
      config,
      tempDir,
    });
    const screenshotError = screenshotResult.targetError;

    const codeConnectExit = resolveCodeConnectExitCode(codeConnect, {
      requireCodeConnect: config.requireCodeConnect,
    });
    const status = screenshotError ? 'partial_succeeded' : 'succeeded';
    const blocking = Boolean((config.requireScreenshots && screenshotError) || codeConnectExit === 7);
    return {
      ordinal: parsedUrl.ordinal,
      sourceUrl: parsedUrl.url,
      fileKey: parsedUrl.fileKey,
      originalNodeId: parsedUrl.originalNodeId,
      canonicalNodeId: parsedUrl.nodeId,
      figmaFileVersion: nodeResult.fileVersion,
      status,
      errorCode: screenshotError?.code ?? null,
      errorMessage: screenshotError?.message ?? null,
      retryable: Boolean(screenshotError?.retryable),
      blocking,
      duplicateOf: null,
      targetNode: targetNodeArtifact({ parsedUrl, nodeResult }),
      contextTree,
      designProperties,
      codeConnect,
      cssHints,
      screenshots: screenshotResult.screenshots,
      summary: {
        bestTargetInterpretation: contextTree.bestTargetInterpretation?.reason ?? 'target_node',
        visualRequirements: [],
        openQuestions: [
          ...(contextTree.warnings ?? []),
          ...screenshotResult.warnings,
          ...(screenshotError ? ['screenshot_failed'] : []),
          ...(codeConnectExit === 7 ? ['code_connect_required_but_unavailable'] : []),
        ],
      },
    };
  } catch (error) {
    const failure = asStableFailure(error);
    return {
      ordinal: parsedUrl.ordinal,
      sourceUrl: parsedUrl.url,
      fileKey: parsedUrl.fileKey,
      originalNodeId: parsedUrl.originalNodeId,
      canonicalNodeId: parsedUrl.nodeId,
      figmaFileVersion: null,
      status: 'failed',
      errorCode: failure.code,
      errorMessage: failure.message,
      retryable: failure.retryable,
      blocking: true,
      duplicateOf: null,
    };
  }
}

function chooseExitCode(urlResults, config) {
  if (urlResults.length === 0) {
    return 0;
  }
  const successes = urlResults.filter((result) => result.status === 'succeeded' || result.status === 'partial_succeeded');
  if (urlResults.some((result) => result.errorCode === 'artifact_budget_exceeded')) {
    return 6;
  }
  if (successes.length === 0) {
    const firstCode = urlResults[0]?.errorCode;
    if (firstCode?.startsWith('missing_') || firstCode?.includes('url') || firstCode === 'unsupported_figma_url_kind') {
      return 2;
    }
    if (
      firstCode?.startsWith('figma_token') ||
      firstCode?.startsWith('figma_env') ||
      firstCode === 'figma_api_unauthorized'
    ) {
      return 3;
    }
    return 4;
  }
  if (config.requireScreenshots && successes.some((result) => result.status === 'partial_succeeded')) {
    return 5;
  }
  if (
    config.requireCodeConnect &&
    successes.some((result) => {
      const codeConnect = result.codeConnect ?? { status: result.codeConnectStatus };
      return resolveCodeConnectExitCode(codeConnect, { requireCodeConnect: true }) === 7;
    })
  ) {
    return 7;
  }
  return 0;
}

export function defaultCreateClient(config) {
  const tokenProvider = {
    withTokenRetry(operation) {
      return withFigmaTokenRetry(
        {
          tokenStorePath: config.tokenStore,
          envFiles: config.envFiles,
        },
        operation,
      );
    },
  };
  return createFigmaRestClient({ tokenProvider });
}

export async function runReadFigmaContext({
  argv = process.argv,
  env = process.env,
  cwd = process.cwd(),
  createClient = defaultCreateClient,
  now = () => new Date(),
} = {}) {
  const config = parseCliArgs(argv, env, cwd, skillRoot);
  if (!config.ok) {
    return {
      exitCode: 1,
      code: config.errorCode,
      message: config.message ?? config.errorCode,
    };
  }

  if (config.mode === 'help') {
    return {
      exitCode: 0,
      code: 'help',
      output: formatHelp(),
    };
  }

  if (config.mode === 'version') {
    return {
      exitCode: 0,
      code: 'version',
      output: formatVersion(),
    };
  }

  let urls;
  let source = config.mode;
  let inputShape = config.mode;
  let issue = null;

  if (config.mode === 'url') {
    urls = [config.url];
  } else {
    issue = await readIssueJson(config.issueJson);
    const extracted = extractFigmaUrlsFromIssue(issue);
    if (!extracted.ok) {
      const artifact = await writeFigmaContextArtifacts({
        artifactRoot: config.out,
        repo: config.repo,
        issue: issueMetaFromMode(config.mode, issue),
        source: null,
        inputShape: null,
        urlResults: [],
        generatedAt: now().toISOString(),
        emptyReason: extracted.errorCode,
      });
      await validateArtifactDir(artifact.runDir);
      return {
        exitCode: 0,
        code: extracted.errorCode,
        runDir: artifact.runDir,
        runDirRelative: relativeRunDir(artifact.runDir, config),
      };
    }
    urls = extracted.urls;
    source = extracted.source;
    inputShape = extracted.inputShape;
  }

  const parsedUrls = dedupeParsedUrls(urls.map((url) => parseFigmaDesignUrl(url)));
  const hasReadableUrl = parsedUrls.some((entry) => entry.ok && !entry.duplicateOf);
  const client = hasReadableUrl ? createClient(config) : null;
  const tempDir = await fs.mkdtemp(path.join(os.tmpdir(), 'read-figma-context-'));
  const urlResults = [];
  try {
    for (const parsedUrl of parsedUrls) {
      urlResults.push(await processParsedUrl({ parsedUrl, config, client, tempDir }));
    }

    const artifact = await writeFigmaContextArtifacts({
      artifactRoot: config.out,
      repo: config.repo,
      issue: issueMetaFromMode(config.mode, issue),
      source,
      inputShape,
      urlResults,
      generatedAt: now().toISOString(),
      maxArtifactMiBPerUrl: config.budgets.maxArtifactMiBPerUrl,
    });
    const validation = await validateArtifactDir(artifact.runDir);
    if (!validation.ok) {
      return {
        exitCode: 6,
        code: 'artifact_validation_failed',
        runDir: artifact.runDir,
        runDirRelative: relativeRunDir(artifact.runDir, config),
        errors: validation.errors,
      };
    }

    return {
      exitCode: chooseExitCode(artifact.manifest.urls, config),
      code: 'completed',
      runDir: artifact.runDir,
      runDirRelative: relativeRunDir(artifact.runDir, config),
      urlResults,
    };
  } finally {
    await fs.rm(tempDir, { recursive: true, force: true });
  }
}

async function main() {
  const result = await runReadFigmaContext();
  if (result.output) {
    process.stdout.write(result.output);
    return;
  }
  if (result.exitCode === 0) {
    process.stdout.write(`${JSON.stringify({ code: result.code, runDir: result.runDir, runDirRelative: result.runDirRelative }, null, 2)}\n`);
    return;
  }
  console.error(result.code);
  if (result.message) {
    console.error(result.message);
  }
  if (result.runDir) {
    console.error(`runDir: ${result.runDir}`);
  }
  if (result.runDirRelative) {
    console.error(`runDirRelative: ${result.runDirRelative}`);
  }
  if (result.errors) {
    console.error(JSON.stringify(result.errors, null, 2));
  }
  process.exitCode = result.exitCode;
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => {
  console.error(error instanceof Error ? error.message : String(error));
  process.exitCode = 1;
  });
}
