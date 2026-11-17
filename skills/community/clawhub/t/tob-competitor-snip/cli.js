#!/usr/bin/env node
// tob-competitor-snip CLI wrapper
const { spawn } = require('child_process');
const path = require('path');

const generator = path.join(__dirname, 'src', 'generator.js');
const child = spawn('node', [generator, ...process.argv.slice(2)], {
  stdio: 'inherit',
  cwd: __dirname,
});

child.on('close', (code) => process.exit(code));
