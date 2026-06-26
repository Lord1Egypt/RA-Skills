#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');

// ANSI color codes
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  dim: '\x1b[2m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  magenta: '\x1b[35m',
  cyan: '\x1b[36m',
  white: '\x1b[37m',
  bgGreen: '\x1b[42m',
  bgBlue: '\x1b[44m',
};

const c = colors;

function print(text) {
  console.log(text);
}

function printBanner() {
  print('');
  print(`${c.cyan}${c.bright}  ╔══════════════════════════════════════════════════╗${c.reset}`);
  print(`${c.cyan}${c.bright}  ║                                                  ║${c.reset}`);
  print(`${c.cyan}${c.bright}  ║${c.reset}   ${c.yellow}📈  Crypto Trading Advisor${c.reset}                    ${c.cyan}${c.bright}║${c.reset}`);
  print(`${c.cyan}${c.bright}  ║${c.reset}   ${c.dim}A Claude Skill for crypto analysis${c.reset}             ${c.cyan}${c.bright}║${c.reset}`);
  print(`${c.cyan}${c.bright}  ║                                                  ║${c.reset}`);
  print(`${c.cyan}${c.bright}  ╚══════════════════════════════════════════════════╝${c.reset}`);
  print('');
}

function downloadFile(url) {
  return new Promise((resolve, reject) => {
    https.get(url, (response) => {
      // Handle redirects
      if (response.statusCode === 301 || response.statusCode === 302) {
        return downloadFile(response.headers.location).then(resolve).catch(reject);
      }
      
      if (response.statusCode !== 200) {
        reject(new Error(`Failed to download: ${response.statusCode}`));
        return;
      }
      
      let data = '';
      response.on('data', chunk => data += chunk);
      response.on('end', () => resolve(data));
      response.on('error', reject);
    }).on('error', reject);
  });
}

async function main() {
  printBanner();

  const skillUrl = 'https://raw.githubusercontent.com/0xrikt/crypto-skills/main/crypto-trading-advisor/SKILL.md';
  const outputFile = path.join(process.cwd(), 'crypto-trading-advisor.skill.md');

  print(`${c.blue}⬇${c.reset}  Downloading skill file...`);
  print('');

  try {
    const content = await downloadFile(skillUrl);
    fs.writeFileSync(outputFile, content);
    
    print(`${c.green}✓${c.reset}  ${c.bright}Skill file saved to:${c.reset}`);
    print(`   ${c.cyan}${outputFile}${c.reset}`);
    print('');
    print(`${c.yellow}${c.bright}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${c.reset}`);
    print('');
    print(`${c.bright}  Next Steps:${c.reset}`);
    print('');
    print(`  ${c.magenta}1.${c.reset} Open ${c.cyan}https://claude.ai/settings/skills${c.reset}`);
    print(`  ${c.magenta}2.${c.reset} Click ${c.green}"Add Skill"${c.reset}`);
    print(`  ${c.magenta}3.${c.reset} Copy the content from ${c.cyan}crypto-trading-advisor.skill.md${c.reset}`);
    print(`  ${c.magenta}4.${c.reset} Paste it into the skill editor and save`);
    print('');
    print(`${c.yellow}${c.bright}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${c.reset}`);
    print('');
    print(`${c.dim}  Example usage after installation:${c.reset}`);
    print(`  ${c.white}"Is BTC a good trade right now?"${c.reset}`);
    print(`  ${c.white}"Can I long SOL here?"${c.reset}`);
    print(`  ${c.white}"What's the setup for ETH?"${c.reset}`);
    print('');
    print(`${c.green}${c.bright}  Happy trading! 🚀${c.reset}`);
    print('');
    
  } catch (error) {
    print(`${c.yellow}⚠${c.reset}  Could not download from GitHub.`);
    print(`   ${c.dim}${error.message}${c.reset}`);
    print('');
    print(`${c.bright}  Manual installation:${c.reset}`);
    print(`  ${c.cyan}https://github.com/0xrikt/crypto-skills/tree/main/crypto-trading-advisor${c.reset}`);
    print('');
    process.exit(1);
  }
}

main();
