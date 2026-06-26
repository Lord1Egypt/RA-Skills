const fs = require('node:fs');
const os = require('node:os');
const path = require('node:path');
const { spawnSync } = require('node:child_process');

function assert(condition, message) {
  if (!condition) {
    throw new Error(message);
  }
}

function main() {
  const scriptPath = path.resolve(__dirname, 'build-seedance-prompt-pack.cjs');
  const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'seedance-prompt-pack-test-'));
  const outPath = path.join(tempDir, 'prompt-pack.json');

  const run = spawnSync(process.execPath, [
    scriptPath,
    '--topic', '孙悟空大战天兵天将',
    '--duration', '10',
    '--mode', 'first-last-frame',
    '--scenario', 'narrative',
    '--has-reference-image', 'true',
    '--result-json', outPath,
  ], {
    encoding: 'utf8',
    stdio: 'pipe',
  });

  assert(run.status === 0, `script exit code ${run.status}; stderr=${run.stderr || ''}`);
  assert(fs.existsSync(outPath), 'result json not generated');

  const data = JSON.parse(fs.readFileSync(outPath, 'utf8'));
  assert(data.ok === true, 'ok should be true');
  assert(data.mode === 'first-last-frame', `unexpected mode: ${data.mode}`);
  assert(Array.isArray(data.beats) && data.beats.length >= 3, 'beats should be generated');
  assert(typeof data.prompt === 'string' && data.prompt.includes('[目标]'), 'prompt should contain structured sections');
  assert(data.assets && data.assets.referenceImage && data.assets.referenceImage.required === true, 'reference image requirement should be true');
  assert(data.scenario === 'narrative', `unexpected scenario: ${data.scenario}`);
  assert(Array.isArray(data.negatives) && data.negatives.length >= 2, 'negatives should be generated');

  console.log(JSON.stringify({ ok: true, outPath, beats: data.beats.length, scenario: data.scenario }, null, 2));
}

try {
  main();
} catch (error) {
  console.error(error && error.stack ? error.stack : String(error));
  process.exit(1);
}
