#!/usr/bin/env node
const { execSync } = require('child_process');
const cmds = [
  'node skills/shared-memory-os/scripts/init-shared-memory-os.js',
  'node skills/shared-memory-os/scripts/check-memory-health.js > reports/shared-memory/latest-health.json || true',
  'node skills/shared-memory-os/scripts/rebuild-learnings-index.js',
  'node skills/shared-memory-os/scripts/record-health-snapshot.js',
  'node skills/shared-memory-os/scripts/find-promotion-candidates.js > reports/shared-memory/shared-memory-promotion-candidates.json',
  'node skills/shared-memory-os/scripts/find-duplicate-learnings.js > reports/shared-memory/shared-memory-duplicate-learnings.json || true',
  'node skills/shared-memory-os/scripts/find-stale-durable-memory.js > reports/shared-memory/shared-memory-stale-durable-memory.json',
  'node skills/shared-memory-os/scripts/find-validated-rules.js > reports/shared-memory/shared-memory-validated-rules.json',
  'node skills/shared-memory-os/scripts/find-low-value-learnings.js > reports/shared-memory/shared-memory-low-value-learnings.json',
  'node skills/shared-memory-os/scripts/build-workflow-optimization-suggestions.js > reports/shared-memory/shared-memory-workflow-optimization.json',
  'node skills/shared-memory-os/scripts/build-promotion-suggestions.js',
  'node skills/shared-memory-os/scripts/build-learning-merge-suggestions.js > reports/shared-memory/shared-memory-merge-suggestions.json',
  'node skills/shared-memory-os/scripts/find-skill-upgrade-candidates.js > reports/shared-memory/shared-memory-skill-upgrade-candidates.json',
  'node skills/shared-memory-os/scripts/build-memory-patch-candidates.js',
  'node skills/shared-memory-os/scripts/build-audit-report.js',
  'node skills/shared-memory-os/scripts/build-dashboard.js',
  'node skills/shared-memory-os/scripts/build-conflict-review-report.js',
  'node skills/shared-memory-os/scripts/build-weekly-review.js'
];
for (const c of cmds) execSync(c,{stdio:'inherit',cwd:'/home/zqh2333/.openclaw/workspace'});
console.log(JSON.stringify({ok:true, ran:cmds.length},null,2));
