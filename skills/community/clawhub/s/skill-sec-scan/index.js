#!/usr/bin/env node

const { execSync } = require('child_process');
const path = require('path');

const args = process.argv.slice(2).join(' ');
const scriptDir = path.dirname(__filename);
const result = execSync(`"${scriptDir}/scripts/scan.sh" ${args}`, {
    encoding: 'utf8',
    stdio: 'inherit'
});

console.log(result);
