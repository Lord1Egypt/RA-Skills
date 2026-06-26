'use strict';

const assert = require('node:assert');
const fs = require('node:fs');

// wow:mobile was removed in v1.7.1 to prevent legacy demo routing in Telegram/OpenClaw.
// These assertions confirm the script is gone and no longer routes demo traffic.

{
  const pkg = JSON.parse(fs.readFileSync('package.json', 'utf8'));
  assert.ok(!pkg.scripts['wow:mobile'], 'package.json: wow:mobile script must not exist (removed in v1.7.1)');
  assert.ok(!pkg.scripts['test:wow-mobile'], 'package.json: test:wow-mobile script must not exist');
  console.log('demoWowMobile: wow:mobile removed from package.json — all assertions passed');
}
