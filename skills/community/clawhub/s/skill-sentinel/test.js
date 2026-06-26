import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { runCli, scanSkill, toSarif } from './src/index.js';

const cleanSkill = new URL('./fixtures/clean-skill', import.meta.url);
const maliciousSkill = new URL('./fixtures/malicious-skill', import.meta.url);

const cleanResult = scanSkill(cleanSkill.pathname);
assert.equal(cleanResult.riskLevel, 'Safe');
assert.equal(cleanResult.findingCount, 0);

const badResult = scanSkill(maliciousSkill.pathname);
assert.equal(badResult.riskLevel, 'Avoid');
assert.equal(badResult.findings.some((f) => f.ruleId === 'CS001_CURL_PIPE_SH'), true);

const sarif = toSarif(badResult);
assert.equal(sarif.version, '2.1.0');
assert.equal(Array.isArray(sarif.runs[0].results), true);

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'clawshield-'));
const supFile = path.join(tmp, '.clawshield-suppressions.json');
fs.writeFileSync(
  supFile,
  JSON.stringify([
    {
      ruleId: 'CS001_CURL_PIPE_SH',
      file: 'scripts/install.sh',
      line: 2,
      justification: 'testing suppression behavior'
    }
  ], null, 2)
);
const suppressed = scanSkill(maliciousSkill.pathname, { suppressionsPath: supFile });
assert.equal(suppressed.findings.some((f) => f.ruleId === 'CS001_CURL_PIPE_SH'), false);

const blockedCode = await runCli(['scan', maliciousSkill.pathname, '--fail-on', 'caution']);
assert.equal(blockedCode, 2);

const okCode = await runCli(['scan', cleanSkill.pathname, '--format', 'json']);
assert.equal(okCode, 0);

console.log('clawshield tests passed');
