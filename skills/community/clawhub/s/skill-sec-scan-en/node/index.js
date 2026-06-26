#!/usr/bin/env node

/**
 * Skill Security Scanner CLI
 * 用法: node index.js [skills目录]
 */

const { SecurityDetector } = require('./scanner.js');
const path = require('path');

const args = process.argv.slice(2);
const skillsDir = args[0] || path.join(process.env.HOME, '.openclaw/workspace/skills');

async function main() {
    console.log('\n🔒 Skill Security Scanner v3.0 (Node.js)\n');
    
    const detector = new SecurityDetector();
    const results = await detector.scanAll(skillsDir);
    detector.generateReport(results);
}

main().catch(console.error);
