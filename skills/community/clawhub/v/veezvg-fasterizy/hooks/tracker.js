#!/usr/bin/env node

const { enable, disable, isEnabled } = require('./flag');

let input = '';
process.stdin.on('data', (chunk) => {
  input += chunk;
});
process.stdin.on('end', () => {
  try {
    const data = JSON.parse(input);
    const prompt = (data.prompt || '').trim();
    const lower = prompt.toLowerCase();

    if (lower.startsWith('/fasterizy off')) {
      disable();
    } else if (lower.startsWith('/fasterizy on')) {
      enable();
    } else if (/^\/fasterizy(\s|$)/i.test(prompt)) {
      if (isEnabled()) {
        disable();
      } else {
        enable();
      }
    }
  } catch (e) {}
});
