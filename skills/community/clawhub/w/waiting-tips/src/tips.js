/**
 * OpenClaw Waiting Tips - Core Module
 * Load tips from tips/*.txt and provide random selection
 */
const fs = require('fs');
const path = require('path');

const TIPS_DIR = path.join(__dirname, '..', 'tips');

let cachedTips = null;

function loadTips() {
  if (cachedTips) return cachedTips;

  const tips = [];
  const files = fs.readdirSync(TIPS_DIR).filter(f => f.endsWith('.txt'));

  for (const file of files) {
    const content = fs.readFileSync(path.join(TIPS_DIR, file), 'utf-8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('##')) continue;
      tips.push(trimmed);
    }
  }

  cachedTips = tips;
  return tips;
}

function getRandomTip() {
  const tips = loadTips();
  return tips[Math.floor(Math.random() * tips.length)];
}

function getRandomTips(count = 3) {
  const tips = loadTips();
  const shuffled = [...tips].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, tips.length));
}

function formatTip(tip, style = 'plain') {
  const [zh, en] = tip.split(' | ');
  switch (style) {
    case 'emoji':
      return `💡 ${tip}`;
    case 'zh-only':
      return `💡 ${zh || tip}`;
    case 'en-only':
      return `💡 ${en || tip}`;
    case 'card':
      return `━━━━━━━━━━━━━━━\n💡 Tips while you wait\n\n${zh || tip}\n${en ? `\n${en}` : ''}\n━━━━━━━━━━━━━━━`;
    default:
      return `💡 ${tip}`;
  }
}

function reloadTips() {
  cachedTips = null;
  return loadTips();
}

module.exports = { loadTips, getRandomTip, getRandomTips, formatTip, reloadTips };
