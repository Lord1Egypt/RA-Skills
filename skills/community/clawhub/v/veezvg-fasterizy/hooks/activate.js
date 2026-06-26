#!/usr/bin/env node

const { enable, disable, defaultEnabled } = require('./flag');
const SKILL = require('./skill-content');

if (!defaultEnabled()) {
  disable();
  process.exit(0);
}

enable();
process.stdout.write('FASTERIZY ACTIVE\n\n' + SKILL);
