#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const TEMPLATES = {
  'session-state': {
    current_task: '',
    key_context: [],
    pending_actions: [],
    recent_decisions: [],
    last_updated: new Date().toISOString()
  },

  'memory-md': `# MEMORY.md — Long-Term Memory

## About the User
[Add user preferences, communication style, etc.]

## Projects
[Active projects and their status]

## Decisions Log
[Important decisions and why they were made]

## Lessons Learned
[Mistakes to avoid, patterns that work]

## Preferences
[Tools, frameworks, workflows the user prefers]

---
*Curated memory — distill insights from daily logs*
`
};

function main() {
  console.log('🧠 Initializing Simple Local Memory...\n');

  // Create SESSION-STATE.json
  if (!fs.existsSync('SESSION-STATE.json')) {
    fs.writeFileSync(
      'SESSION-STATE.json',
      JSON.stringify(TEMPLATES['session-state'], null, 2)
    );
    console.log('✓ Created SESSION-STATE.json (Hot RAM)');
  } else {
    console.log('• SESSION-STATE.json already exists');
  }

  // Create MEMORY.md
  if (!fs.existsSync('MEMORY.md')) {
    fs.writeFileSync('MEMORY.md', TEMPLATES['memory-md']);
    console.log('✓ Created MEMORY.md (Curated Archive)');
  } else {
    console.log('• MEMORY.md already exists');
  }

  // Create memories directory
  if (!fs.existsSync('memories')) {
    fs.mkdirSync('memories', { recursive: true });
    console.log('✓ Created memories/ directory');
  } else {
    console.log('• memories/ directory already exists');
  }

  // Create .gitignore for memories
  const gitignorePath = path.join('memories', '.gitignore');
  if (!fs.existsSync(gitignorePath)) {
    fs.writeFileSync(gitignorePath, '# Ignore individual daily files if desired\n# *.json\n');
    console.log('✓ Created memories/.gitignore');
  }

  console.log('\n🎉 Simple Local Memory initialized!');
  console.log('\nNext steps:');
  console.log('1. Add SESSION-STATE.json to your AI agent context');
  console.log('2. Review SKILL.md for usage guide');
  console.log('3. Start storing memories: memory-store --type preference --content "..."');
}

main();
