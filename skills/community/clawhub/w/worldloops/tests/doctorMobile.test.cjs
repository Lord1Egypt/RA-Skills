'use strict';

const assert = require('node:assert');
const { spawnSync } = require('node:child_process');

function runDoctorMobile() {
  return spawnSync(process.execPath, ['dist/scripts/doctorMobile.js'], { encoding: 'utf8' });
}

{
  const result = runDoctorMobile();
  assert.ok(result.stdout.includes('Safe to try'), 'doctor:mobile includes Safe to try');
  assert.ok(result.stdout.includes('externalWrite:false enforced'), 'doctor:mobile includes externalWrite:false enforced');
  assert.ok(result.stdout.includes('No emails will be sent'), 'doctor:mobile includes email safety');
  assert.ok(result.stdout.includes('No chat messages will be posted'), 'doctor:mobile includes chat safety');
  console.log('doctor:mobile: all assertions passed');
}
