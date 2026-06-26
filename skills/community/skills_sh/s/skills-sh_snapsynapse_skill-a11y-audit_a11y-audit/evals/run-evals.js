#!/usr/bin/env node
/*
skill_bundle: a11y-audit
file_role: evals
version: 2
version_date: 2026-05-31
previous_version: 1
change_summary: Added scanner, discovery origin policy, and Markdown escaping hardening regressions.
*/

const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const repoRoot = path.resolve(__dirname, '..', '..');
const tmpRoot = '/tmp/a11y-audit-evals';
const validateMode = process.argv.includes('--validate');
const results = [];

function repoPath(...parts) {
  return path.join(repoRoot, ...parts);
}

function tmpPath(...parts) {
  return path.join(tmpRoot, ...parts);
}

function readJson(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function runNode(args, opts = {}) {
  const run = spawnSync(process.execPath, args, {
    cwd: repoRoot,
    encoding: 'utf8',
    ...opts,
  });
  if (run.status !== 0) {
    throw new Error([
      `$ node ${args.join(' ')}`,
      run.stdout.trim(),
      run.stderr.trim(),
    ].filter(Boolean).join('\n'));
  }
  return run;
}

function runCommand(command, args) {
  const run = spawnSync(command, args, {
    cwd: repoRoot,
    encoding: 'utf8',
  });
  if (run.status !== 0) {
    throw new Error([
      `$ ${command} ${args.join(' ')}`,
      run.stdout.trim(),
      run.stderr.trim(),
    ].filter(Boolean).join('\n'));
  }
  return run;
}

function resetDir(dir) {
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
}

function findGeneratedFile(dir, ext) {
  const matches = fs.readdirSync(dir)
    .filter((entry) => entry.startsWith('audit-') && entry.endsWith(ext))
    .map((entry) => path.join(dir, entry));
  assert.strictEqual(matches.length, 1, `expected one generated ${ext} file in ${dir}`);
  return matches[0];
}

function assertAuditJsonShape(json) {
  for (const key of ['date', 'tool', 'pages', 'summary', 'violations', 'matrix', 'lighthouse']) {
    assert.ok(Object.prototype.hasOwnProperty.call(json, key), `audit JSON missing ${key}`);
  }
  assert.match(json.date, /^\d{4}-\d{2}-\d{2}$/);
  assert.ok(Array.isArray(json.pages), 'pages must be an array');
  assert.ok(Array.isArray(json.violations), 'violations must be an array');
  for (const level of ['critical', 'serious', 'moderate', 'minor']) {
    assert.strictEqual(typeof json.summary[level], 'number', `summary.${level} must be numeric`);
  }
  assert.strictEqual(typeof json.matrix, 'object', 'matrix must be an object');
  assert.strictEqual(typeof json.lighthouse, 'object', 'lighthouse must be an object');
}

function summarizeImpacts(scan) {
  const summary = { critical: 0, serious: 0, moderate: 0, minor: 0 };
  for (const result of scan.results || []) {
    for (const violation of result.axe?.violations || []) {
      const impact = violation.impact || 'minor';
      summary[impact] += (violation.nodes || []).length;
    }
  }
  return summary;
}

function test(name, fn) {
  try {
    fn();
    results.push({ name, ok: true });
    console.log(`PASS ${name}`);
  } catch (error) {
    results.push({ name, ok: false, error });
    console.error(`FAIL ${name}`);
    console.error(error.stack || String(error));
  }
}

function validateSyntax() {
  const files = [
    'a11y-audit/scripts/discover.js',
    'a11y-audit/scripts/scan.js',
    'a11y-audit/scripts/report.js',
    'a11y-audit/scripts/bootstrap-context.js',
    'a11y-audit/scripts/plan-issues.js',
    'a11y-audit/evals/run-discover-fixture.js',
    'a11y-audit/evals/run-evals.js',
  ];
  for (const file of files) runNode(['--check', file]);
}

function validateJsonFiles() {
  const files = [
    'a11y-audit/evals/evals.json',
    'a11y-audit/references/output-schema.json',
    'a11y-audit/assets/sample-output/audit-sample.json',
  ];
  for (const file of files) readJson(repoPath(file));
  assertAuditJsonShape(readJson(repoPath('a11y-audit/assets/sample-output/audit-sample.json')));
}

function validateYamlFiles() {
  const files = [
    'a11y-audit/SKILL.md',
    'a11y-audit/HANDOFF.md',
    'a11y-audit/CHANGELOG.md',
    'a11y-audit/MANIFEST.yaml',
    'a11y-audit/references/claude-code.md',
    'a11y-audit/references/codex.md',
    'a11y-audit/references/project-context-template.md',
    'a11y-audit/references/output-contract.md',
    'a11y-audit/references/issue-trackers.md',
    'a11y-audit/agents/openai.yaml',
    'a11y-audit/assets/ci/github-actions/accessibility-audit.yml',
  ];
  const code = [
    'require "yaml"',
    'require "date"',
    `files=${JSON.stringify(files)}`,
    'files.each do |f|',
    'text=File.read(f, encoding:"UTF-8")',
    'payload=(f.end_with?(".md") && text.start_with?("---\\n")) ? text.split(/^---\\n/,3)[1] : text',
    'YAML.safe_load(payload, permitted_classes:[Date])',
    'end',
  ].join('; ');
  runCommand('ruby', ['-e', code]);
}

function validateBootstrapSmoke() {
  const dir = tmpPath('bootstrap');
  resetDir(dir);
  const run = runNode([
    'a11y-audit/scripts/bootstrap-context.js',
    '--workspace', dir,
    '--name', 'Demo',
    '--base_url', 'http://127.0.0.1:3001',
    '--routes', '/,/about',
    '--priority_routes', '/',
    '--output_mode', 'markdown',
  ]);
  const outputPath = run.stdout.trim();
  assert.strictEqual(outputPath, path.join(dir, '.a11y-audit', 'PROJECT_CONTEXT.md'));
  const context = fs.readFileSync(outputPath, 'utf8');
  assert.match(context, /- name: Demo/);
  assert.match(context, /- output_mode: markdown/);
}

function runDiscoverFixture(id) {
  const fixture = `a11y-audit/evals/fixtures/${id}`;
  const run = runNode(['a11y-audit/evals/run-discover-fixture.js', '--fixture', fixture]);
  const actual = JSON.parse(run.stdout);
  const expected = readJson(repoPath(fixture, 'expected.json'));
  assert.deepStrictEqual(actual, expected);
}

function eval2IssuePlanning() {
  const dir = tmpPath('eval-2');
  resetDir(dir);
  const output = path.join(dir, 'issue-plan.md');
  runNode([
    'a11y-audit/scripts/plan-issues.js',
    '--input', 'a11y-audit/evals/fixtures/eval-2/current-scan.json',
    '--context', 'a11y-audit/evals/fixtures/eval-2/context.md',
    '--existing', 'a11y-audit/evals/fixtures/eval-2/existing-keys.json',
    '--output', output,
  ]);
  const plan = fs.readFileSync(output, 'utf8');
  assert.match(plan, /Threshold: `P1`/);
  assert.match(plan, /Planned tickets: 1/);
  assert.match(plan, /Skipped duplicates: 1/);
  assert.match(plan, /Additional standards: CAN-ASC-6\.2/);
  assert.match(plan, /accessibility-p0-critical, accessibility-new, wcag-perceivable, wcag-understandable/);
  assert.match(plan, /<!-- a11y-audit-key: color-contrast::\/ -->/);
  assert.match(plan, /<!-- a11y-audit-key: label::\/checkout -->/);
}

function eval3QuickScan() {
  const dir = tmpPath('eval-3');
  resetDir(dir);
  const scan = readJson(repoPath('a11y-audit/evals/fixtures/eval-3/current-scan.json'));
  assert.strictEqual(scan.results.length, 1, 'quick scan should include exactly one page');
  assert.strictEqual(scan.results[0].url, 'http://localhost:8080/');
  const summary = summarizeImpacts(scan);
  assert.deepStrictEqual(summary, { critical: 1, serious: 0, moderate: 0, minor: 0 });
  assert.strictEqual(scan.results[0].axe.violations[0].id, 'button-name');
  assert.strictEqual(scan.results[0].lighthouse.status, 'skipped');
  assert.ok(!fs.readdirSync(dir).some((entry) => entry.endsWith('.md')), 'quick scan eval must not generate markdown');
}

function eval4SkippedLighthouseReport() {
  const dir = tmpPath('eval-4');
  resetDir(dir);
  runNode([
    'a11y-audit/scripts/report.js',
    '--input', 'a11y-audit/evals/fixtures/eval-4/current-scan.json',
    '--project-name', 'Eval 4 Lighthouse Fixture',
    '--runtime-url', 'https://example.com',
    '--expected-url', 'https://example.com',
    '--output-dir', dir,
  ]);
  const md = fs.readFileSync(findGeneratedFile(dir, '.md'), 'utf8');
  const json = readJson(findGeneratedFile(dir, '.json'));
  assert.match(md, /Lighthouse was skipped: Lighthouse CLI unavailable in fixture environment\./);
  assert.match(md, /\| Lighthouse \| Skipped: Lighthouse CLI unavailable in fixture environment \|/);
  assert.strictEqual(json.lighthouse.status, 'skipped');
  assert.strictEqual(json.lighthouse.reason, 'Lighthouse CLI unavailable in fixture environment');
  assert.strictEqual(json.lighthouse.score, undefined);
  assertAuditJsonShape(json);
}

function eval11ReportDelta() {
  const dir = tmpPath('eval-11');
  resetDir(dir);
  runNode([
    'a11y-audit/scripts/report.js',
    '--input', 'a11y-audit/evals/fixtures/eval-11/current-scan.json',
    '--previous', 'a11y-audit/evals/fixtures/eval-11/previous-audit.json',
    '--discover', 'a11y-audit/evals/fixtures/eval-11/discover.json',
    '--project-name', 'Eval 11 Delta Fixture',
    '--runtime-url', 'https://example.com',
    '--expected-url', 'https://example.com',
    '--output-dir', dir,
  ]);
  const md = fs.readFileSync(findGeneratedFile(dir, '.md'), 'utf8');
  const json = readJson(findGeneratedFile(dir, '.json'));
  assertAuditJsonShape(json);
  assert.ok(json.delta, 'expected delta output');
  const changed = json.delta.changed.find((entry) => entry.rule === 'color-contrast');
  assert.ok(changed, 'color-contrast should be changed');
  assert.deepStrictEqual(changed.previousPages, [
    'https://example.com/blog/post-a',
    'https://example.com/blog/post-b',
  ]);
  assert.deepStrictEqual(changed.currentPages, [
    'https://example.com/docs/guide-a',
    'https://example.com/docs/guide-b',
  ]);
  assert.deepStrictEqual(changed.addedPages, [
    'https://example.com/docs/guide-a',
    'https://example.com/docs/guide-b',
  ]);
  assert.deepStrictEqual(changed.removedPages, [
    'https://example.com/blog/post-a',
    'https://example.com/blog/post-b',
  ]);
  assert.ok(!json.delta.changed.some((entry) => entry.rule === 'region'), 'region should not be changed');
  assert.match(md, /## Delta from Previous Audit/);
  assert.match(md, /\*\*Changed\*\*:/);
  assert.match(md, /color-contrast:/);
  assert.match(md, /\*\*Unchanged\*\*: region/);
}

function scannerBrowserValidation() {
  const scan = require(repoPath('a11y-audit/scripts/scan.js'));
  assert.strictEqual(scan.validateBrowserLib('puppeteer'), 'puppeteer');
  assert.throws(
    () => scan.validateBrowserLib('puppeteer; echo injected'),
    /Unsupported browser library/
  );
  const scanSource = fs.readFileSync(repoPath('a11y-audit/scripts/scan.js'), 'utf8');
  assert.match(scanSource, /spawnSync\('npm', \['install', '--prefix', SKILL_DEPS_DIR, packageName\]/);
  assert.doesNotMatch(scanSource, /execSync\(`npm install/);
}

function markdownEscapingRegression() {
  const dir = tmpPath('markdown-escaping');
  resetDir(dir);
  const inputPath = path.join(dir, 'scan.json');
  fs.writeFileSync(inputPath, JSON.stringify({
    generated_at: '2026-05-31T00:00:00Z',
    urls: ['https://example.com/a|b'],
    results: [
      {
        url: 'https://example.com/a|b',
        axe: {
          violations: [
            {
              id: 'color-contrast',
              impact: 'serious',
              description: 'desc',
              help: 'Fix | this\nnow',
              helpUrl: 'javascript:alert(1)',
              tags: ['wcag111'],
              nodes: [
                {
                  target: ['main` | td'],
                  html: '<main></main>',
                  any: [{ data: { fgColor: '#000', bgColor: '#fff', contrastRatio: 1.2, expectedContrastRatio: 4.5 } }],
                },
              ],
            },
          ],
          passes: [],
          incomplete: [],
          inapplicable: [],
        },
        lighthouse: { status: 'skipped', reason: 'not | run\nnow' },
      },
    ],
  }, null, 2));
  runNode([
    'a11y-audit/scripts/report.js',
    '--input', inputPath,
    '--project-name', 'Demo | Project',
    '--runtime-url', 'https://example.com/a|b',
    '--output-dir', dir,
  ]);
  const md = fs.readFileSync(findGeneratedFile(dir, '.md'), 'utf8');
  assert.match(md, /Demo \\| Project/);
  assert.match(md, /not \\| run now/);
  assert.match(md, /color-contrast/);
  assert.doesNotMatch(md, /\]\(javascript:alert/);
  assert.match(md, /main\\` \\| td/);
}

function issuePlanEscapingRegression() {
  const dir = tmpPath('issue-plan-escaping');
  resetDir(dir);
  const inputPath = path.join(dir, 'scan.json');
  const outputPath = path.join(dir, 'issue-plan.md');
  fs.writeFileSync(inputPath, JSON.stringify({
    results: [
      {
        url: 'https://example.com/route--><script>|x',
        axe: {
          violations: [
            {
              id: 'label|bad',
              impact: 'critical',
              help: 'Do | not\nexecute',
              tags: ['wcag131'],
              nodes: [{ target: ['input'] }],
            },
          ],
        },
      },
    ],
  }, null, 2));
  runNode([
    'a11y-audit/scripts/plan-issues.js',
    '--input', inputPath,
    '--output', outputPath,
  ]);
  const plan = fs.readFileSync(outputPath, 'utf8');
  assert.match(plan, /label\\|bad/);
  assert.match(plan, /Do \\| not execute/);
  assert.doesNotMatch(plan, /--><script>/);
}

function dependencyPolicyCheck() {
  const scanSource = fs.readFileSync(repoPath('a11y-audit/scripts/scan.js'), 'utf8');
  const skill = fs.readFileSync(repoPath('a11y-audit/SKILL.md'), 'utf8');
  assert.match(scanSource, /spawnSync\('npm'/);
  assert.match(scanSource, /skill-deps \(auto-installed\)/);
  assert.match(skill, /`scan\.js` may auto-install missing dependencies/);
  assert.match(skill, /ask before invoking scan\.js/);
}

resetDir(tmpRoot);

if (validateMode) {
  test('syntax checks cover bundled scripts and eval harnesses', validateSyntax);
  test('JSON files parse and sample output matches audit shape', validateJsonFiles);
  test('YAML and frontmatter files parse', validateYamlFiles);
  test('bootstrap-context smoke test creates workspace context', validateBootstrapSmoke);
}

test('eval-9 preserves cross-origin sitemap URLs', () => runDiscoverFixture('eval-9'));
test('eval-10 keeps discovery deterministic', () => runDiscoverFixture('eval-10'));
test('eval-12 blocks cross-origin sitemaps unless explicitly allowed', () => runDiscoverFixture('eval-12'));
test('eval-2 plans issues with labels and deduplication', eval2IssuePlanning);
test('eval-3 quick scan summarizes one plain HTML page', eval3QuickScan);
test('eval-4 reports skipped Lighthouse without inventing scores', eval4SkippedLighthouseReport);
test('eval-11 reports page-aware delta movement', eval11ReportDelta);
test('scan.js rejects unsupported browser package names before install', scannerBrowserValidation);
test('report.js escapes target-derived markdown fields', markdownEscapingRegression);
test('plan-issues.js escapes target-derived markdown fields', issuePlanEscapingRegression);
test('scan.js dependency auto-install policy is documented', dependencyPolicyCheck);

const failed = results.filter((result) => !result.ok);
console.log(`\n${results.length - failed.length}/${results.length} checks passed`);
if (failed.length > 0) process.exit(1);
