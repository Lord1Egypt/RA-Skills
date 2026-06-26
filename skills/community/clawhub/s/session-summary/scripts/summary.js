#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const OBSIDIAN_VAULT = '/mnt/c/Users/milky/Documents/OpenClaw-Obsidian/openclaw';
const DAILY_FOLDER = '10_Daily';

function generateSummary(sessionData) {
  const now = new Date();
  const dateStr = now.toISOString().split('T')[0];
  const timeStr = now.toLocaleTimeString('ja-JP', { hour: '2-digit', minute: '2-digit' });
  
  const summary = `# ${dateStr} Session Summary

## Generated
- Time: ${timeStr}

## Key Achievements
${sessionData.achievements.map(a => `- ${a}`).join('\n')}

## Skills Installed
${sessionData.skills.map(s => `- ${s}`).join('\n')}

## Next Actions
${sessionData.nextActions.map(n => `- [ ] ${n}`).join('\n')}
`;
  
  return summary;
}

const sessionData = {
  achievements: [
    'Memory Harness v1.0.0 published to ClawHub',
    '8 skills installed via ClawHub',
    'Security risks addressed',
    'Long conversation test completed (8+ hours)'
  ],
  skills: [
    'byterover 2.0.0',
    'automation-workflows 0.1.0',
    'video-frames 1.0.0',
    'note 2.1.0',
    'x-twitter 2.3.1',
    'openclaw-cli',
    'schedule',
    'memory-harness (self-made)'
  ],
  nextActions: [
    'Test Memory Harness in new session',
    'Use installed skills for real tasks'
  ]
};

const summary = generateSummary(sessionData);
console.log(summary);
