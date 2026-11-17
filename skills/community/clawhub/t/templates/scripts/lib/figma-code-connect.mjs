import fs from 'node:fs/promises';
import path from 'node:path';

const CODE_CONNECT_FILE_RE = /(\.figma\.(ts|tsx)$|\.connect\.(ts|tsx)$|^figma\.config\.)/;
const SOURCE_EXT_RE = /\.(ts|tsx|js|jsx)$/;

function emptyResult(status, source, scanBudget, warnings = []) {
  return {
    schemaVersion: 'figma-code-connect-context/v1',
    status,
    source,
    scanBudget,
    mappings: [],
    warnings,
  };
}

function canonicalDashNodeId(nodeId) {
  return String(nodeId ?? '').replaceAll(':', '-');
}

function componentNameCandidates(targetNode) {
  const names = new Set();
  for (const value of [targetNode?.componentName, targetNode?.name]) {
    if (typeof value !== 'string') {
      continue;
    }
    names.add(value);
    const parts = value.split('/').map((part) => part.trim()).filter(Boolean);
    if (parts.length > 0) {
      for (const part of parts) {
        names.add(part);
      }
      names.add(parts.at(-1));
    }
  }
  return [...names];
}

function extractCodeComponentName(contents, fallbackPath) {
  const connectMatch = contents.match(/figma\.connect\s*\(\s*([A-Za-z0-9_$]+)/);
  if (connectMatch) {
    return connectMatch[1];
  }
  const exportFunctionMatch = contents.match(/export\s+function\s+([A-Za-z0-9_$]+)/);
  if (exportFunctionMatch) {
    return exportFunctionMatch[1];
  }
  return path.basename(fallbackPath).replace(/\.(figma|connect)?\.(tsx?|jsx?)$/, '').replace(/\.(tsx?|jsx?)$/, '');
}

async function walkFiles(root, maxFiles) {
  const files = [];
  const warnings = [];

  async function walk(dir) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const entry of entries) {
      if (entry.name === 'node_modules' || entry.name === '.git' || entry.name === 'dist' || entry.name === '.next') {
        continue;
      }
      const fullPath = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        await walk(fullPath);
        if (files.length > maxFiles) {
          return;
        }
        continue;
      }
      if (entry.isFile()) {
        files.push(fullPath);
        if (files.length > maxFiles) {
          warnings.push('code_connect_scan_budget_exceeded');
          return;
        }
      }
    }
  }

  await walk(root);
  return {
    files: files.slice(0, maxFiles),
    exceeded: files.length > maxFiles,
    warnings,
  };
}

function directMappingEvidence(contents, targetNode) {
  const nodeId = targetNode?.id ?? '';
  const dashNodeId = canonicalDashNodeId(nodeId);
  const componentKey = targetNode?.componentKey;
  const componentName = targetNode?.componentName ?? targetNode?.name;
  if (!contents.includes('figma.connect(') && !contents.includes('@figma/code-connect')) {
    return null;
  }
  if (nodeId && contents.includes(nodeId)) {
    return 'matched canonical node id in Code Connect file';
  }
  if (dashNodeId && contents.includes(`node-id=${dashNodeId}`)) {
    return 'matched Figma component URL node-id in figma.connect()';
  }
  if (componentKey && contents.includes(componentKey)) {
    return 'matched component key in figma.connect()';
  }
  if (componentName && contents.includes(componentName)) {
    return 'matched Figma component name in Code Connect file';
  }
  return null;
}

function weakComponentNameEvidence(filePath, contents, targetNode) {
  const names = componentNameCandidates(targetNode);
  for (const name of names) {
    const safeName = name.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    const exportRe = new RegExp(`export\\s+(?:function|const|class)\\s+${safeName}\\b`);
    if (exportRe.test(contents) || path.basename(filePath).replace(/\.[^.]+$/, '') === name) {
      return `weak component name match: ${name}`;
    }
  }
  return null;
}

function toRelative(repo, filePath) {
  return path.relative(repo, filePath).split(path.sep).join('/');
}

async function fileExists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function scanCodeConnect({ repo, targetNode, maxFiles = 5000 } = {}) {
  const baseBudget = {
    maxFiles,
    scannedFiles: 0,
    exceeded: false,
  };
  if (!repo || !(await fileExists(repo))) {
    return emptyResult('unavailable', 'local-code-connect-scan', baseBudget, ['repo_unavailable']);
  }

  let scan;
  try {
    scan = await walkFiles(repo, maxFiles);
  } catch {
    return emptyResult('failed', 'local-code-connect-scan', baseBudget, ['code_connect_scan_failed']);
  }

  const scanBudget = {
    maxFiles,
    scannedFiles: scan.files.length,
    exceeded: scan.exceeded,
  };
  if (scan.exceeded) {
    return emptyResult('unavailable', 'local-code-connect-scan', scanBudget, [
      ...new Set(scan.warnings.concat('code_connect_scan_budget_exceeded')),
    ]);
  }

  const codeConnectFiles = scan.files.filter((filePath) => CODE_CONNECT_FILE_RE.test(path.basename(filePath)));
  const sourceFiles = scan.files.filter((filePath) => SOURCE_EXT_RE.test(filePath));
  const mappings = [];

  for (const filePath of codeConnectFiles) {
    let contents;
    try {
      contents = await fs.readFile(filePath, 'utf8');
    } catch {
      return emptyResult('failed', 'local-code-connect-scan', scanBudget, ['code_connect_file_read_failed']);
    }
    const evidence = directMappingEvidence(contents, targetNode);
    if (!evidence) {
      continue;
    }
    mappings.push({
      figmaNodeId: targetNode?.id ?? null,
      figmaComponentName: targetNode?.componentName ?? targetNode?.name ?? null,
      codeComponentName: extractCodeComponentName(contents, filePath),
      sourcePath: toRelative(repo, filePath),
      confidence: 'high',
      evidence,
    });
  }

  if (mappings.length > 0) {
    return {
      schemaVersion: 'figma-code-connect-context/v1',
      status: 'mapped',
      source: 'local-code-connect-scan',
      scanBudget,
      mappings,
      warnings: [],
    };
  }

  for (const filePath of sourceFiles) {
    if (CODE_CONNECT_FILE_RE.test(path.basename(filePath))) {
      continue;
    }
    let contents;
    try {
      contents = await fs.readFile(filePath, 'utf8');
    } catch {
      return emptyResult('failed', 'local-code-connect-scan', scanBudget, ['code_connect_file_read_failed']);
    }
    const evidence = weakComponentNameEvidence(filePath, contents, targetNode);
    if (!evidence) {
      continue;
    }
    mappings.push({
      figmaNodeId: targetNode?.id ?? null,
      figmaComponentName: targetNode?.componentName ?? targetNode?.name ?? null,
      codeComponentName: extractCodeComponentName(contents, filePath),
      sourcePath: toRelative(repo, filePath),
      confidence: 'low',
      evidence,
    });
    break;
  }

  if (mappings.length > 0) {
    return {
      schemaVersion: 'figma-code-connect-context/v1',
      status: 'mapped',
      source: 'local-code-connect-scan',
      scanBudget,
      mappings,
      warnings: ['weak_component_name_match_only'],
    };
  }

  if (codeConnectFiles.length > 0) {
    return emptyResult('unmapped', 'local-code-connect-scan', scanBudget, []);
  }

  return emptyResult('unavailable', 'local-code-connect-scan', scanBudget, ['code_connect_files_not_found']);
}

export function resolveCodeConnectExitCode(codeConnect, options = {}) {
  if (!options.requireCodeConnect) {
    return 0;
  }
  return codeConnect?.status === 'unavailable' || codeConnect?.status === 'failed' ? 7 : 0;
}
