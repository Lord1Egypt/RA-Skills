#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const src = path.join(__dirname, '..', 'SKILL.md');
const dst = path.join(__dirname, '..', 'skills', 'fasterizy', 'SKILL.md');
fs.mkdirSync(path.dirname(dst), { recursive: true });
fs.copyFileSync(src, dst);
console.log('synced', dst);
