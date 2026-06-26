#!/usr/bin/env node
/**
 * Quick sanity checks for Reanimated v4 + RNGH in Expo/Bare projects.
 *
 * Usage (from a React Native project root):
 *   node {baseDir}/scripts/check-setup.mjs
 */

import fs from 'node:fs';
import path from 'node:path';

const cwd = process.cwd();

function readText(p) {
  try {
    return fs.readFileSync(p, 'utf8');
  } catch {
    return null;
  }
}

function readJson(p) {
  const t = readText(p);
  if (!t) return null;
  try {
    return JSON.parse(t);
  } catch {
    return null;
  }
}

function hasDep(pkg, name) {
  return Boolean(pkg?.dependencies?.[name] || pkg?.devDependencies?.[name]);
}

function warn(msg) {
  console.log(`[33mWARN[0m  ${msg}`);
}
function ok(msg) {
  console.log(`[32mOK[0m    ${msg}`);
}
function info(msg) {
  console.log(`INFO  ${msg}`);
}

let exitCode = 0;

const pkg = readJson(path.join(cwd, 'package.json'));
if (!pkg) {
  console.error('ERROR: package.json not found (run from project root).');
  process.exit(2);
}

const isExpo = hasDep(pkg, 'expo');
info(`Detected: ${isExpo ? 'Expo-managed' : 'non-Expo / possibly bare'} project`);

// Core deps
const need = [
  'react-native-reanimated',
  'react-native-worklets',
  'react-native-gesture-handler',
];

for (const dep of need) {
  if (hasDep(pkg, dep)) ok(`Dependency present: ${dep}`);
  else {
    warn(`Missing dependency: ${dep}`);
    exitCode = 1;
  }
}

// Babel plugin heuristic
const babelConfigPath = path.join(cwd, 'babel.config.js');
const babelText = readText(babelConfigPath);
if (!babelText) {
  info('No babel.config.js found (this is normal for some setups).');
} else {
  const hasWorkletsPlugin = babelText.includes('react-native-worklets/plugin');
  const hasReanimatedPlugin = babelText.includes('react-native-reanimated/plugin');

  if (isExpo) {
    info('Expo note: Reanimated plugin is usually configured by babel-preset-expo when installed via expo install.');
    if (hasWorkletsPlugin || hasReanimatedPlugin) {
      ok('Babel plugin string found in babel.config.js (fine even if redundant in Expo).');
    } else {
      info('No explicit Reanimated/Worklets plugin found in babel.config.js (often OK in Expo).');
    }
  } else {
    // Bare RN: Reanimated 4 expects the worklets plugin.
    if (hasWorkletsPlugin) ok('Found react-native-worklets/plugin in babel.config.js');
    else {
      warn('Expected react-native-worklets/plugin in babel.config.js for Reanimated 4 (bare RN).');
      if (hasReanimatedPlugin) info('Found react-native-reanimated/plugin (Reanimated <=3 style). Migration may be needed.');
      exitCode = 1;
    }
  }
}

// GestureHandlerRootView reminder (can’t reliably auto-detect)
info('Reminder: wrap your app root with GestureHandlerRootView (RNGH docs).');
info('Docs: https://docs.swmansion.com/react-native-gesture-handler/docs/fundamentals/installation/');

// Reanimated 4 architecture reminder
info('Reminder: Reanimated 4 works only with the React Native New Architecture.');
info('Docs: https://docs.swmansion.com/react-native-reanimated/docs/guides/compatibility/');

process.exit(exitCode);
