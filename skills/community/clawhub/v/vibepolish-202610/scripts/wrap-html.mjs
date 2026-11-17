#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

function usage() {
  console.error('Usage: node <wrap-html.mjs> <source.html> -o <output.html> | --project-url <url> --source-name <name> -o <output.html>');
  process.exit(2);
}

const args = process.argv.slice(2);
if (!args.length) usage();

const projectUrlFlag = args.indexOf('--project-url');
const projectUrl = projectUrlFlag >= 0 ? args[projectUrlFlag + 1] : null;
const sourceNameFlag = args.indexOf('--source-name');
const configuredSourceName = sourceNameFlag >= 0 ? args[sourceNameFlag + 1] : null;
const runtimeModeFlag = args.indexOf('--mode');
const runtimeMode = runtimeModeFlag >= 0 && args[runtimeModeFlag + 1] === 'review' ? 'review' : 'edit';
const sessionFileFlag = args.indexOf('--session');
const sessionFile = sessionFileFlag >= 0 ? args[sessionFileFlag + 1] : null;
const sourcePath = projectUrl ? null : args[0];
const outputFlag = args.indexOf('-o');
const outputPath = outputFlag >= 0 ? args[outputFlag + 1] : null;
if ((!sourcePath && !projectUrl) || !outputPath) usage();

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const rootDir = findProjectRoot(scriptDir);
const assetsDir = findAssetsDir(scriptDir, rootDir);
const runtimePath = findFirstExisting([
  path.join(assetsDir, 'vibepolish-runtime.js')
]);
const templatePath = findFirstExisting([
  path.join(assetsDir, 'vibepolish.html')
]);
const iroSourcePath = findFirstExisting([
  path.join(assetsDir, 'iro-color-picker.js')
]);

const sourceHtml = sourcePath ? fs.readFileSync(sourcePath, 'utf8') : '';
const session = sessionFile ? JSON.parse(fs.readFileSync(path.resolve(sessionFile), 'utf8')) : null;
const runtime = fs.readFileSync(runtimePath, 'utf8');
const template = fs.readFileSync(templatePath, 'utf8');
const iroSource = fs.readFileSync(iroSourcePath, 'utf8');
const sourceName = configuredSourceName || (sourcePath ? path.basename(sourcePath) : 'index.html');
const runtimeSource = projectUrl
  ? { kind: 'project', projectRoot: '', entryFile: sourceName, url: projectUrl }
  : { kind: 'single-html', file: sourceName };

const wrapper = template
  .replaceAll('{{SOURCE_NAME_HTML}}', () => escapeHtml(sourceName))
  .replaceAll('{{SOURCE_NAME_JSON}}', () => JSON.stringify(sourceName))
  .replaceAll('{{RUNTIME_SOURCE_JSON}}', () => JSON.stringify(runtimeSource))
  .replaceAll('{{IRO_SOURCE_JSON}}', () => JSON.stringify(iroSource))
  .replaceAll('{{RUNTIME_MODE_JSON}}', () => JSON.stringify(runtimeMode))
  .replaceAll('{{SESSION_JSON}}', () => escapeScriptJsonValue(session))
  .replaceAll('{{SOURCE_HTML_JSON}}', () => escapeScriptJson(sourceHtml))
  .replaceAll('{{RUNTIME_JS}}', () => runtime);

fs.mkdirSync(path.dirname(path.resolve(outputPath)), { recursive: true });
fs.writeFileSync(outputPath, wrapper, 'utf8');
console.log(`Wrote ${outputPath}`);

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function escapeScriptJson(value) {
  return JSON.stringify(value)
    .replaceAll('<', '\\u003c')
    .replaceAll('>', '\\u003e')
    .replaceAll('&', '\\u0026')
    .replaceAll('\u2028', '\\u2028')
    .replaceAll('\u2029', '\\u2029');
}

function escapeScriptJsonValue(value) {
  return JSON.stringify(value)
    .replaceAll('<', '\\u003c')
    .replaceAll('>', '\\u003e')
    .replaceAll('&', '\\u0026')
    .replaceAll('\u2028', '\\u2028')
    .replaceAll('\u2029', '\\u2029');
}

function findProjectRoot(startDir) {
  let current = startDir;
  while (true) {
    if (fs.existsSync(path.join(current, 'package.json')) || fs.existsSync(path.join(current, 'skills'))) return current;
    const parent = path.dirname(current);
    if (parent === current) return startDir;
    current = parent;
  }
}

function findAssetsDir(scriptDir, rootDir) {
  const candidates = [
    scriptDir,
    path.join(scriptDir, 'assets'),
    path.join(scriptDir, '..', 'assets'),
    path.join(scriptDir, '..'),
    path.join(rootDir, 'dist', 'vibepolish-standalone'),
    path.join(rootDir, 'skills', 'vibepolish', 'assets')
  ];
  for (const candidate of candidates) {
    if (hasRuntimeAndTemplate(candidate)) return candidate;
  }
  throw new Error(`Cannot find VibePolish assets near ${scriptDir}`);
}

function hasRuntimeAndTemplate(dir) {
  const hasRuntime = fs.existsSync(path.join(dir, 'vibepolish-runtime.js'));
  const hasTemplate = fs.existsSync(path.join(dir, 'vibepolish.html'));
  return hasRuntime && hasTemplate;
}

function findFirstExisting(candidates, required = true) {
  const found = candidates.find(file => fs.existsSync(file));
  if (!found && required) throw new Error(`Missing required file. Tried:\n${candidates.join('\n')}`);
  return found || '';
}
