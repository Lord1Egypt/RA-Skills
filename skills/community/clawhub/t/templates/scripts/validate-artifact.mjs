#!/usr/bin/env node

import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const REQUIRED_ROOT_FILES = ['manifest.json', 'summary.md'];
const REQUIRED_URL_FILES = [
  ['target-node.json', 'figma-target-node/v1'],
  ['context-tree.json', 'figma-context-tree/v1'],
  ['design-properties.json', 'figma-design-properties/v1'],
  ['code-connect.json', 'figma-code-connect-context/v1'],
  ['css-hints.css', null],
  ['source-url.txt', null],
];

async function exists(filePath) {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

async function readJson(filePath, errors) {
  try {
    return JSON.parse(await fs.readFile(filePath, 'utf8'));
  } catch {
    errors.push(`${filePath}: invalid_json`);
    return null;
  }
}

function containsForbiddenSecret(text) {
  return (
    /figd_[A-Za-z0-9_-]+/.test(text) ||
    /Authorization\s*:\s*Bearer\s+(?!\[REDACTED\])\S+/i.test(text) ||
    /[?&](?:sig|signature|X-Amz-Signature)=(?!\[REDACTED\])[^&\s"']+/i.test(text) ||
    /refresh_token\s*[:=]\s*(?!\[REDACTED\])\S+/i.test(text) ||
    /client_secret\s*[:=]\s*(?!\[REDACTED\])\S+/i.test(text)
  );
}

async function scanForbiddenContent(dir, errors) {
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
      if (!/\.(json|md|css|txt)$/.test(entry.name)) {
        continue;
      }
      const text = await fs.readFile(fullPath, 'utf8');
      if (containsForbiddenSecret(text)) {
        errors.push(`${fullPath}: forbidden_secret_or_temp_url`);
      }
    }
  }
  await walk(dir);
}

export async function validateArtifactDir(runDir) {
  const errors = [];

  for (const fileName of REQUIRED_ROOT_FILES) {
    const filePath = path.join(runDir, fileName);
    if (!(await exists(filePath))) {
      errors.push(`${fileName}: missing`);
    }
  }

  const manifestPath = path.join(runDir, 'manifest.json');
  const manifest = (await exists(manifestPath)) ? await readJson(manifestPath, errors) : null;
  if (manifest && manifest.schemaVersion !== 'figma-context-artifact/v1') {
    errors.push('manifest.json: invalid_schemaVersion');
  }

  const summaryPath = path.join(runDir, 'summary.md');
  const summary = (await exists(summaryPath)) ? await fs.readFile(summaryPath, 'utf8') : '';
  if (manifest?.urls?.length > 0) {
    for (const url of manifest.urls) {
      if (!summary.includes(`## URL ${url.ordinal}`)) {
        errors.push(`summary.md: missing_url_${url.ordinal}`);
      }
      if (url.status !== 'succeeded' && url.status !== 'partial_succeeded') {
        continue;
      }
      for (const [fileName, schemaVersion] of REQUIRED_URL_FILES) {
        const filePath = path.join(runDir, url.artifactDir, fileName);
        if (!(await exists(filePath))) {
          errors.push(`${url.artifactDir}/${fileName}: missing`);
          continue;
        }
        if (schemaVersion) {
          const json = await readJson(filePath, errors);
          if (json?.schemaVersion !== schemaVersion) {
            errors.push(`${url.artifactDir}/${fileName}: invalid_schemaVersion`);
          }
        }
      }
      if (url.targetScreenshot && !(await exists(path.join(runDir, url.targetScreenshot)))) {
        errors.push(`${url.targetScreenshot}: missing`);
      }
      if (url.parentScreenshot && !(await exists(path.join(runDir, url.parentScreenshot)))) {
        errors.push(`${url.parentScreenshot}: missing`);
      }
      for (const candidateScreenshot of url.candidateScreenshots ?? []) {
        if (candidateScreenshot?.path && !(await exists(path.join(runDir, candidateScreenshot.path)))) {
          errors.push(`${candidateScreenshot.path}: missing`);
        }
      }
    }
  }

  await scanForbiddenContent(runDir, errors);

  return {
    ok: errors.length === 0,
    errors,
  };
}

async function main() {
  const runDir = process.argv[2];
  if (!runDir) {
    console.error('Usage: node scripts/validate-artifact.mjs <artifact-run-dir>');
    process.exitCode = 2;
    return;
  }
  const result = await validateArtifactDir(path.resolve(process.cwd(), runDir));
  if (!result.ok) {
    console.error(JSON.stringify(result, null, 2));
    process.exitCode = 6;
    return;
  }
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch((error) => {
    console.error(error instanceof Error ? error.message : String(error));
    process.exitCode = 6;
  });
}
