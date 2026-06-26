#!/usr/bin/env node
const { execSync } = require('child_process');
const path = require('path');

const args = process.argv.slice(2);

if (args.length === 0) {
  console.log('Usage:');
  console.log('  npx github:BODYsuperman/Youtube-Transcriber-Skill <URL> [language]');
  console.log('  python3 transcribe.py <URL> [language]');
  console.log('');
  console.log('Example:');
  console.log('  npx github:BODYsuperman/Youtube-Transcriber-Skill "https://youtube.com/watch?v=VIDEO_ID" zh');
  console.log('  python3 transcribe.py "URL" zh');
  process.exit(0);
}

const url = args.find(a => a.includes('youtube.com') || a.includes('youtu.be'));
const lang = args.find(a => ['zh','en','ja','ko','auto'].includes(a)) || 'auto';

if (!url) {
  console.error('Error: Please provide a YouTube URL');
  process.exit(1);
}

const script = path.join(__dirname, '..', 'transcribe.py');
execSync(`python3 ${script} ${url} ${lang}`, { stdio: 'inherit' });
