#!/usr/bin/env node
'use strict';

const path = require('path');
const fs = require('fs');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8'));

console.log('🗓️  Setting up workday-music-greet cron jobs...\n');

for (const [key, scene] of Object.entries(config.scenes)) {
  const [h, m] = scene.time.split(':').map(Number);
  const expr = `${m} ${h} * * 1-5`; // Mon-Fri only
  const scriptPath = path.join(__dirname, 'scene-trigger.js');

  // We output the openclaw cron commands for the agent to register
  console.log(`Scene: ${key} | Time: ${scene.time} (${config.cronTimezone}) | Cron: ${expr}`);
  console.log(`  → openclaw cron add "${expr}" "node ${scriptPath} ${key}"\n`);
}

console.log('💡 Run the commands above or let the agent register them via the cron tool.');