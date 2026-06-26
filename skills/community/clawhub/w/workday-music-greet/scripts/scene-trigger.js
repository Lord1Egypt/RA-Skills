#!/usr/bin/env node
'use strict';

const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const config = JSON.parse(fs.readFileSync(path.join(__dirname, 'config.json'), 'utf8'));

const sceneKey = process.argv[2];
if (!sceneKey) {
  console.error('Usage: node scene-trigger.js <scene-key>');
  console.error(`Available scenes: ${Object.keys(config.scenes).join(', ')}`);
  process.exit(1);
}

const scene = config.scenes[sceneKey];
if (!scene) {
  console.error(`Unknown scene: ${sceneKey}`);
  process.exit(1);
}

const now = new Date();
const day = now.getDay(); // 0=Sun, 6=Sat
if (config.weekdaysOnly && (day === 0 || day === 6)) {
  console.log(`⏭️  Weekend detected — skipping "${sceneKey}" scene`);
  process.exit(0);
}

console.log(`🎵 Switching music to "${scene.musicScene}" for scene "${sceneKey}"...`);

// Try home-music command
try {
  execSync(`home-music ${scene.musicScene}`, { stdio: 'inherit', timeout: 15000 });
} catch (err) {
  console.warn(`⚠️  home-music command failed (scene may not exist yet): ${err.message}`);
  console.log('   Continuing with email greeting...');
}

// Send greeting email
console.log(`📧 Sending greeting email for "${sceneKey}"...`);
try {
  execSync(`node ${path.join(__dirname, 'send-greet.js')} ${sceneKey}`, { stdio: 'inherit', timeout: 30000 });
} catch (err) {
  console.error(`❌ Greeting email failed: ${err.message}`);
  process.exit(1);
}

console.log(`✅ Scene "${sceneKey}" complete — music + greeting dispatched`);