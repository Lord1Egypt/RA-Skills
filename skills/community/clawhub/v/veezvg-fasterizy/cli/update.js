const { spawnSync } = require('child_process');
const {
  REPO_SLUG,
  claudePluginCacheGlob,
  codexPluginCacheGlob,
  findNpxSkillsInstalls,
  defaultSearchRoots,
} = require('./common');

function runNpxSkillsUpdate(agentFlag) {
  const r = spawnSync(
    process.platform === 'win32' ? 'npx.cmd' : 'npx',
    ['skills', 'add', REPO_SLUG, '-a', agentFlag],
    { stdio: 'inherit', shell: process.platform === 'win32' }
  );
  return r.status === 0;
}

module.exports = function update() {
  console.log(`Updating fasterizy from github.com/${REPO_SLUG} (main)...\n`);

  const roots = defaultSearchRoots();
  const installs = findNpxSkillsInstalls(roots);
  let auto = 0;

  const seen = new Set();
  for (const inst of installs) {
    const key = `${inst.npxFlag}:${inst.root}`;
    if (seen.has(key)) continue;
    seen.add(key);
    process.stdout.write(`${inst.id.padEnd(10)}${inst.path}  `);
    if (runNpxSkillsUpdate(inst.npxFlag)) {
      console.log('[updated via npx skills]');
      auto++;
    } else {
      console.log('[failed]');
    }
  }

  if (installs.length === 0) {
    console.log('No npx-skills rule files found under cwd or home (expected fasterizy in content).');
  }

  const claudeCaches = claudePluginCacheGlob();
  for (const p of claudeCaches) {
    console.log('\nClaude Code plugin cache:', p);
    console.log('  -> Run /plugin update fasterizy inside Claude Code');
  }

  const codexCaches = codexPluginCacheGlob();
  for (const p of codexCaches) {
    console.log('\nCodex plugin cache:', p);
    console.log('  -> Run /plugin update fasterizy inside Codex (if supported)');
  }

  console.log('');
  console.log(
    `Done. ${auto} path(s) refreshed via npx skills. Plugin installs need the agent UI.`
  );
  console.log('To update this CLI: npm update -g fasterizy');
};
