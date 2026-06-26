/**
 * Temperature Model + GC (Garbage Collection / Archival)
 *
 * 🔥 Hot  — < 7 days, high frequency access
 * 🟡 Warm — 7-30 days, moderate access
 * ❄️ Cold — > 30 days, auto-archive candidates
 */

'use strict';
const fs = require('fs');
const path = require('path');

const DAY_MS = 86400000;

/**
 * Classify a file by temperature based on modification time.
 */
function classifyFile(filePath) {
  try {
    const stat = fs.statSync(filePath);
    const age = Date.now() - stat.mtime.getTime();
    if (age < 7 * DAY_MS) return 'hot';
    if (age < 30 * DAY_MS) return 'warm';
    return 'cold';
  } catch {
    return 'unknown';
  }
}

/**
 * Run GC: archive cold daily logs (>30 days) to .archive/YYYY-MM/
 * Returns { archived: string[], stats: { hot, warm, cold } }
 */
function runGC(memoryDir) {
  const archiveDir = path.join(memoryDir, '.archive');
  const archived = [];
  const stats = { hot: 0, warm: 0, cold: 0 };

  // Only process daily log files (YYYY-MM-DD.md pattern)
  const datePattern = /^\d{4}-\d{2}-\d{2}\.md$/;

  let files;
  try {
    files = fs.readdirSync(memoryDir).filter(f => datePattern.test(f));
  } catch {
    return { archived, stats };
  }

  for (const f of files) {
    const filePath = path.join(memoryDir, f);
    const temp = classifyFile(filePath);

    if (temp === 'hot') stats.hot++;
    else if (temp === 'warm') stats.warm++;
    else if (temp === 'cold') {
      stats.cold++;
      // Archive it
      const month = f.slice(0, 7); // YYYY-MM
      const destDir = path.join(archiveDir, month);
      fs.mkdirSync(destDir, { recursive: true });
      const destPath = path.join(destDir, f);
      try {
        fs.renameSync(filePath, destPath);
        archived.push(f);
      } catch {}
    }
  }

  return { archived, stats };
}

/**
 * Get temperature distribution for all daily logs.
 */
function getTemperatureReport(memoryDir) {
  const datePattern = /^\d{4}-\d{2}-\d{2}\.md$/;
  const report = { hot: [], warm: [], cold: [] };

  try {
    const files = fs.readdirSync(memoryDir).filter(f => datePattern.test(f));
    for (const f of files) {
      const temp = classifyFile(path.join(memoryDir, f));
      if (report[temp]) report[temp].push(f);
    }
  } catch {}

  return report;
}

module.exports = { classifyFile, runGC, getTemperatureReport };
