const fs = require('fs');
const path = require('path');
const { isEnabled } = require('../hooks/flag');
const {
  packageRoot,
  findNpxSkillsInstalls,
  defaultSearchRoots,
  claudePluginCacheGlob,
  codexPluginCacheGlob,
} = require('./common');

module.exports = function status() {
  const on = isEnabled();
  console.log('fasterizy flag (runtime):', on ? 'ON' : 'OFF');

  let pkgJson = path.join(packageRoot(), 'package.json');
  try {
    const v = JSON.parse(fs.readFileSync(pkgJson, 'utf8'));
    console.log('package version:', v.version || '(unknown)');
  } catch (e) {
    console.log('package version: (unknown)');
  }

  const roots = defaultSearchRoots();
  const installs = findNpxSkillsInstalls(roots);
  console.log('\nnpx-skills installs detected:', installs.length);
  for (const i of installs) {
    console.log(' ', i.id, i.path);
  }

  const cc = claudePluginCacheGlob();
  const cx = codexPluginCacheGlob();
  if (cc.length) console.log('\nClaude plugin cache:', cc.join(', '));
  if (cx.length) console.log('Codex plugin cache:', cx.join(', '));
};
