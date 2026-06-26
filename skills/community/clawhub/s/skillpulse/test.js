import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {
  analyzeBottlenecks,
  collectPerformanceData,
  compareSessions,
  renderHtmlReport,
  runCli
} from './src/index.js';

const samplesA = JSON.parse(fs.readFileSync(new URL('./fixtures/samples-a.json', import.meta.url), 'utf8'));
const samplesB = JSON.parse(fs.readFileSync(new URL('./fixtures/samples-b.json', import.meta.url), 'utf8'));

const profileA = collectPerformanceData(samplesA);
assert.equal(profileA.totalRuns, 4);
assert.equal(profileA.skills.length, 3);
assert.equal(profileA.p95LatencyMs >= 1300, true);

const analysisA = analyzeBottlenecks(profileA);
assert.equal(analysisA.level, 'warning');
assert.equal(analysisA.bottlenecks.some((b) => b.skill === 'clawshield'), true);

const profileB = collectPerformanceData(samplesB);
const cmp = compareSessions(profileA, profileB);
assert.equal(Array.isArray(cmp.deltas), true);
assert.equal(cmp.deltas.some((d) => d.skill === 'clawshield'), true);

const html = renderHtmlReport({ profile: profileA, analysis: analysisA });
assert.equal(html.includes('<html>'), true);

const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'skill-profiler-'));
const aPath = path.join(tmpDir, 'a.json');
const bPath = path.join(tmpDir, 'b.json');
fs.writeFileSync(aPath, JSON.stringify(samplesA, null, 2));
fs.writeFileSync(bPath, JSON.stringify(samplesB, null, 2));

const runCode = await runCli(['run', '--input', aPath]);
assert.equal(runCode, 2);

const reportJsonCode = await runCli(['report', '--input', aPath, '--out', path.join(tmpDir, 'report.json'), '--type', 'json', '--format', 'json']);
assert.equal(reportJsonCode, 0);

const reportHtmlCode = await runCli(['report', '--input', aPath, '--out', path.join(tmpDir, 'report.html')]);
assert.equal(reportHtmlCode, 0);

const compareCode = await runCli(['compare', '--left', aPath, '--right', bPath, '--format', 'json']);
assert.equal(compareCode, 0);

console.log('skill-profiler tests passed');
