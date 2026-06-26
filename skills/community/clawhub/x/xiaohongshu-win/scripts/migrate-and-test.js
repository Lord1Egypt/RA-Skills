// 迁移旧 cookies 到新目录，并测试 status
const fs = require('fs');
const path = require('path');

const oldCookieFile = path.join(process.env.USERPROFILE, '.xiaohongshu', 'cookies.json');
const newDir = path.join(process.env.USERPROFILE, '.xiaohongshu-win');
const newCookieFile = path.join(newDir, 'cookies.json');

if (!fs.existsSync(newDir)) fs.mkdirSync(newDir, { recursive: true });

if (fs.existsSync(oldCookieFile) && !fs.existsSync(newCookieFile)) {
  fs.copyFileSync(oldCookieFile, newCookieFile);
  console.log('[OK] Migrated cookies from old location');
}

// Now check status
process.argv = ['node', 'xhs.js', 'status'];
require('./xhs.js');
