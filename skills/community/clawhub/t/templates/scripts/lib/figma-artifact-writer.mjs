import fs from 'node:fs/promises';
import path from 'node:path';

import { redactObject, redactString } from './redact.mjs';

const ARTIFACT_SCHEMA = 'figma-context-artifact/v1';

async function pathExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

function slashPath(filePath) {
  return filePath.split(path.sep).join('/');
}

function issueRunName(issue) {
  return issue?.identifier || issue?.id || `manual-${new Date().toISOString().replace(/[:.]/g, '-')}`;
}

function jsonCloneRedacted(value) {
  return redactObject(value);
}

async function writeJson(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, `${JSON.stringify(jsonCloneRedacted(value), null, 2)}\n`);
}

async function writeText(filePath, value) {
  await fs.mkdir(path.dirname(filePath), { recursive: true });
  await fs.writeFile(filePath, redactString(value));
}

async function copyFileIfPresent(sourcePath, destinationPath) {
  if (!sourcePath) {
    return false;
  }
  await fs.mkdir(path.dirname(destinationPath), { recursive: true });
  await fs.copyFile(sourcePath, destinationPath);
  return true;
}

async function directorySizeBytes(dir) {
  let total = 0;
  async function walk(current) {
    const entries = await fs.readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const fullPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
        continue;
      }
      if (!entry.isFile()) {
        continue;
      }
      const stat = await fs.stat(fullPath);
      total += stat.size;
    }
  }
  if (await pathExists(dir)) {
    await walk(dir);
  }
  return total;
}

export async function ensureGitArtifactIgnore(repo) {
  if (!repo) {
    return {
      verified: false,
      warning: 'artifact_ignore_unverified',
      reason: 'repo_not_provided',
    };
  }

  const gitDir = path.join(repo, '.git');
  const infoDir = path.join(gitDir, 'info');
  if (!(await pathExists(gitDir))) {
    return {
      verified: false,
      warning: 'artifact_ignore_unverified',
      reason: 'repo_not_git',
    };
  }

  try {
    await fs.mkdir(infoDir, { recursive: true });
    const excludePath = path.join(infoDir, 'exclude');
    const existing = (await pathExists(excludePath)) ? await fs.readFile(excludePath, 'utf8') : '';
    const lines = ['.multica/figma-context/', '.multica/tmp/'];
    const missing = lines.filter((line) => !existing.split(/\r?\n/).includes(line));
    if (missing.length > 0) {
      const prefix = existing.length > 0 && !existing.endsWith('\n') ? '\n' : '';
      await fs.appendFile(excludePath, `${prefix}${missing.join('\n')}\n`);
    }
    return {
      verified: true,
      warning: null,
      reason: null,
    };
  } catch {
    return {
      verified: false,
      warning: 'artifact_ignore_unverified',
      reason: 'exclude_write_failed',
    };
  }
}

function portableArtifactPath(filePath, repo) {
  if (!filePath) {
    return null;
  }
  if (repo) {
    const relative = path.relative(repo, filePath);
    if (relative && !relative.startsWith('..') && !path.isAbsolute(relative)) {
      return slashPath(relative);
    }
  }
  return null;
}

function manifestArtifactRoot(artifactRoot, runDir, repo) {
  return portableArtifactPath(artifactRoot, repo) ?? slashPath(path.relative(runDir, artifactRoot) || '.');
}

function manifestRunDir(runDir, repo) {
  return portableArtifactPath(runDir, repo) ?? '.';
}

function manifestUrlEntry(urlResult) {
  const artifactDir = urlResult.artifactDir ?? `urls/${String(urlResult.ordinal).padStart(3, '0')}`;
  return {
    ordinal: urlResult.ordinal,
    sourceUrl: urlResult.sourceUrl,
    fileKey: urlResult.fileKey ?? null,
    originalNodeId: urlResult.originalNodeId ?? null,
    canonicalNodeId: urlResult.canonicalNodeId ?? null,
    figmaFileVersion: urlResult.figmaFileVersion ?? null,
    status: urlResult.status,
    errorCode: urlResult.errorCode ?? null,
    errorMessage: urlResult.errorMessage ? redactString(urlResult.errorMessage) : null,
    retryable: Boolean(urlResult.retryable),
    blocking: Boolean(urlResult.blocking),
    duplicateOf: urlResult.duplicateOf ?? null,
    artifactDir,
    targetScreenshot: urlResult.screenshots?.target?.artifactPath ?? null,
    parentScreenshot: urlResult.screenshots?.parent?.artifactPath ?? null,
    candidateScreenshots: (urlResult.screenshots?.candidates ?? []).map((screenshot) => ({
      nodeId: screenshot.nodeId ?? null,
      name: screenshot.name ?? null,
      source: screenshot.source ?? null,
      path: screenshot.artifactPath ?? null,
    })),
    codeConnectStatus: urlResult.codeConnect?.status ?? null,
  };
}

function buildManifest({ artifactRoot, runDir, repo, issue, source, inputShape, urlResults, generatedAt, artifactIgnore, emptyReason }) {
  const urls = urlResults.map(manifestUrlEntry);
  const figmaFileVersions = {};
  for (const entry of urls) {
    if (entry.fileKey && entry.figmaFileVersion) {
      figmaFileVersions[entry.fileKey] = entry.figmaFileVersion;
    }
  }
  const failures = urls
    .filter((entry) => entry.status === 'failed')
    .map((entry) => ({
      ordinal: entry.ordinal,
      sourceUrl: entry.sourceUrl,
      errorCode: entry.errorCode,
      errorMessage: entry.errorMessage,
      retryable: entry.retryable,
      blocking: entry.blocking,
    }));
  if (emptyReason) {
    failures.push({
      ordinal: null,
      sourceUrl: null,
      errorCode: emptyReason,
      errorMessage: emptyReason,
      retryable: false,
      blocking: false,
    });
  }

  return {
    schemaVersion: ARTIFACT_SCHEMA,
    generatedAt,
    issueId: issue?.identifier ?? issue?.id ?? null,
    issueIdentifier: issue?.identifier ?? null,
    issueUUID: issue?.id ?? null,
    artifactRoot: manifestArtifactRoot(artifactRoot, runDir, repo),
    runDir: manifestRunDir(runDir, repo),
    source: source ?? null,
    inputShape: inputShape ?? null,
    figmaFileVersions,
    artifactIgnore,
    urls,
    failures,
  };
}

function formatNullable(value) {
  return value === null || value === undefined || value === '' ? 'null' : String(value);
}

function visualRequirements(urlResult) {
  const formatted = [];
  if (Array.isArray(urlResult.summary?.visualRequirements) && urlResult.summary.visualRequirements.length > 0) {
    formatted.push(...urlResult.summary.visualRequirements);
  }
  const nodes = urlResult.designProperties?.nodes ?? [];
  const first = nodes[0]?.normalized ?? {};
  const requirements = formatted;
  if (first.fontFamily) requirements.push(`font-family: ${first.fontFamily}`);
  if (first.fontSize) requirements.push(`font-size: ${first.fontSize}`);
  const background = formatBackgroundRequirement(first.backgroundColor);
  if (background) requirements.push(`background: ${background}`);
  if (first.padding) requirements.push(`padding: ${first.padding}`);
  if (first.borderRadius) requirements.push(`border-radius: ${first.borderRadius}`);
  return requirements.length > 0 ? requirements.map((item) => `  - ${item}`).join('\n') : '  - 暂无可确定视觉属性';
}

function formatBackgroundRequirement(backgroundColor) {
  if (!backgroundColor) {
    return null;
  }
  const alpha = backgroundColor.figma?.a;
  if (typeof alpha === 'number' && alpha === 0) {
    return `transparent (${backgroundColor.css ?? 'rgba(0, 0, 0, 0)'})`;
  }
  return backgroundColor.css ?? backgroundColor.hex ?? null;
}

function candidateNodes(urlResult) {
  const candidates = urlResult.contextTree?.candidates ?? [];
  if (candidates.length === 0) {
    return '  - 暂无候选节点';
  }
  return candidates
    .map((candidate) => `  - ${formatNullable(candidate.id)} / ${formatNullable(candidate.name)} / ${formatNullable(candidate.source)}`)
    .join('\n');
}

function candidateScreenshots(urlResult) {
  const screenshots = urlResult.screenshots?.candidates ?? [];
  if (screenshots.length === 0) {
    return '  - 暂无候选截图';
  }
  return screenshots
    .map(
      (screenshot) =>
        `  - ${formatNullable(screenshot.nodeId)} / ${formatNullable(screenshot.name)} / ${formatNullable(screenshot.source)} / ${formatNullable(screenshot.artifactPath)}`,
    )
    .join('\n');
}

function codeConnectSummary(urlResult) {
  const codeConnect = urlResult.codeConnect;
  if (!codeConnect) {
    return 'unavailable（未生成 Code Connect 线索；仍需优先搜索本地设计系统组件）';
  }
  const mappings = codeConnect.mappings ?? [];
  if (mappings.length === 0) {
    return `${codeConnect.status}（仍需优先搜索本地设计系统组件）`;
  }
  return `${codeConnect.status}: ${mappings
    .map((mapping) => `${mapping.codeComponentName} (${mapping.sourcePath}, ${mapping.confidence})`)
    .join(', ')}`;
}

function buildSummary({ urlResults, manifest, emptyReason }) {
  const lines = ['# Figma Context Summary', ''];
  if (emptyReason) {
    lines.push(`当前 Issue 没有可读取的 Figma URL：${emptyReason}`, '');
  }
  if (manifest.artifactIgnore?.verified === false) {
    lines.push(`注意：${manifest.artifactIgnore.warning}，请在提交前确认 .multica/figma-context/ 和 .multica/tmp/ 不会进入 MR。`, '');
  }

  for (const urlResult of urlResults) {
    const artifactDir = urlResult.artifactDir ?? `urls/${String(urlResult.ordinal).padStart(3, '0')}`;
    lines.push(`## URL ${urlResult.ordinal}`);
    lines.push('');
    lines.push(`- Source URL: ${formatNullable(urlResult.sourceUrl)}`);
    lines.push(`- Input shape: ${formatNullable(manifest.inputShape)}`);
    lines.push(`- Duplicate of: ${formatNullable(urlResult.duplicateOf)}`);
    lines.push(`- File key: ${formatNullable(urlResult.fileKey)}`);
    lines.push(`- Canonical node id: ${formatNullable(urlResult.canonicalNodeId)}`);
    lines.push(`- Read status: ${formatNullable(urlResult.status)}`);
    lines.push(`- Error code: ${formatNullable(urlResult.errorCode)}`);
    lines.push(`- Target screenshot: ${formatNullable(urlResult.screenshots?.target?.artifactPath)}`);
    lines.push(`- Parent screenshot: ${formatNullable(urlResult.screenshots?.parent?.artifactPath)}`);
    lines.push(`- Best target interpretation: ${formatNullable(urlResult.summary?.bestTargetInterpretation ?? urlResult.contextTree?.bestTargetInterpretation?.reason)}`);
    lines.push('- Candidate nodes:');
    lines.push(candidateNodes(urlResult));
    lines.push('- Candidate screenshots:');
    lines.push(candidateScreenshots(urlResult));
    lines.push(`- Code Connect: ${codeConnectSummary(urlResult)}`);
    lines.push('- Visual requirements:');
    lines.push(visualRequirements(urlResult));
    lines.push(`- CSS hints: ${urlResult.status === 'succeeded' || urlResult.status === 'partial_succeeded' ? `${artifactDir}/css-hints.css` : 'null'}`);
    lines.push('- Implementation notes: 优先使用业务仓库已有设计系统组件、CSS token、Tailwind token 或现有样式变量；不要直接照抄 css-hints.css。');
    const openQuestions = urlResult.summary?.openQuestions ?? [];
    lines.push(`- Open questions: ${openQuestions.length > 0 ? openQuestions.join('; ') : 'null'}`);
    lines.push('');
  }
  return `${lines.join('\n')}\n`;
}

async function writeUrlArtifacts(runDir, urlResult) {
  if (urlResult.status !== 'succeeded' && urlResult.status !== 'partial_succeeded') {
    return;
  }
  const ordinalName = String(urlResult.ordinal).padStart(3, '0');
  const relativeDir = `urls/${ordinalName}`;
  urlResult.artifactDir = relativeDir;
  const urlDir = path.join(runDir, relativeDir);
  await fs.mkdir(path.join(urlDir, 'screenshots', 'candidates'), { recursive: true });
  await writeText(path.join(urlDir, 'source-url.txt'), `${urlResult.sourceUrl}\n`);
  await writeJson(path.join(urlDir, 'target-node.json'), urlResult.targetNode);
  await writeJson(path.join(urlDir, 'context-tree.json'), urlResult.contextTree);
  await writeJson(path.join(urlDir, 'design-properties.json'), urlResult.designProperties);
  await writeJson(path.join(urlDir, 'code-connect.json'), urlResult.codeConnect);
  await writeText(path.join(urlDir, 'css-hints.css'), urlResult.cssHints ?? '');

  if (urlResult.screenshots?.target?.sourcePath) {
    await copyFileIfPresent(urlResult.screenshots.target.sourcePath, path.join(runDir, urlResult.screenshots.target.artifactPath));
  }
  if (urlResult.screenshots?.parent?.sourcePath) {
    await copyFileIfPresent(urlResult.screenshots.parent.sourcePath, path.join(runDir, urlResult.screenshots.parent.artifactPath));
  }
  for (const screenshot of urlResult.screenshots?.candidates ?? []) {
    if (screenshot.sourcePath && screenshot.artifactPath) {
      await copyFileIfPresent(screenshot.sourcePath, path.join(runDir, screenshot.artifactPath));
    }
  }
}

function artifactBudgetFailure(urlResult, maxBytes, actualBytes) {
  return {
    ordinal: urlResult.ordinal,
    sourceUrl: urlResult.sourceUrl,
    fileKey: urlResult.fileKey ?? null,
    originalNodeId: urlResult.originalNodeId ?? null,
    canonicalNodeId: urlResult.canonicalNodeId ?? null,
    figmaFileVersion: urlResult.figmaFileVersion ?? null,
    status: 'failed',
    errorCode: 'artifact_budget_exceeded',
    errorMessage: `Per-URL artifact exceeded budget (${actualBytes} bytes > ${maxBytes} bytes)`,
    retryable: false,
    blocking: true,
    duplicateOf: urlResult.duplicateOf ?? null,
  };
}

export async function writeFigmaContextArtifacts({
  artifactRoot,
  repo,
  issue,
  source,
  inputShape,
  urlResults,
  generatedAt = new Date().toISOString(),
  emptyReason = null,
  maxArtifactMiBPerUrl = null,
}) {
  const runName = issueRunName(issue);
  const runDir = path.join(artifactRoot, runName);
  await fs.mkdir(runDir, { recursive: true });

  const artifactIgnore = await ensureGitArtifactIgnore(repo);
  const normalizedResults = urlResults.map((urlResult) => ({
    artifactDir: `urls/${String(urlResult.ordinal).padStart(3, '0')}`,
    ...urlResult,
    errorMessage: urlResult.errorMessage ? redactString(urlResult.errorMessage) : null,
  }));

  const maxArtifactBytesPerUrl =
    typeof maxArtifactMiBPerUrl === 'number' && Number.isFinite(maxArtifactMiBPerUrl) && maxArtifactMiBPerUrl > 0
      ? maxArtifactMiBPerUrl * 1024 * 1024
      : null;

  for (let index = 0; index < normalizedResults.length; index += 1) {
    const urlResult = normalizedResults[index];
    await writeUrlArtifacts(runDir, urlResult);
    if (!maxArtifactBytesPerUrl || (urlResult.status !== 'succeeded' && urlResult.status !== 'partial_succeeded')) {
      continue;
    }
    const urlDir = path.join(runDir, urlResult.artifactDir);
    const artifactBytes = await directorySizeBytes(urlDir);
    if (artifactBytes > maxArtifactBytesPerUrl) {
      await fs.rm(urlDir, { recursive: true, force: true });
      normalizedResults[index] = artifactBudgetFailure(urlResult, Math.floor(maxArtifactBytesPerUrl), artifactBytes);
    }
  }

  const manifest = buildManifest({
    artifactRoot,
    runDir,
    repo,
    issue,
    source,
    inputShape,
    urlResults: normalizedResults,
    generatedAt,
    artifactIgnore,
    emptyReason,
  });

  await writeJson(path.join(runDir, 'manifest.json'), manifest);
  await writeText(path.join(runDir, 'summary.md'), buildSummary({ urlResults: normalizedResults, manifest, emptyReason }));

  return {
    runDir,
    manifest,
  };
}
