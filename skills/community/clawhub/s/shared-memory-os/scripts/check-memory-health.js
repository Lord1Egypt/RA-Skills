#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const ROOT = '/home/zqh2333/.openclaw/workspace';
const memoryPath = path.join(ROOT, 'MEMORY.md');
const dailyDir = path.join(ROOT, 'memory');
const learnDir = path.join(ROOT, '.learnings');
const today = new Date().toISOString().slice(0,10);
const todayFile = path.join(dailyDir, `${today}.md`);

function exists(p){ try { fs.accessSync(p); return true; } catch { return false; } }
function mtimeDays(p){ try { return (Date.now()-fs.statSync(p).mtimeMs)/86400000; } catch { return null; } }
function listFiles(dir, pred){ try { return fs.readdirSync(dir).filter(pred).map(x=>path.join(dir,x)); } catch { return []; } }
function score(checks){ return Math.round((checks.filter(x=>x.ok).length / checks.length) * 100); }

const learningFiles = listFiles(learnDir, x => x.endsWith('.md') && x !== 'INDEX.md');
const dailyFiles = listFiles(dailyDir, x => /^\d{4}-\d{2}-\d{2}.*\.md$/.test(x));
const recentLearningDays = learningFiles.map(mtimeDays).filter(x => x!=null);
const staleLearn = recentLearningDays.length ? Math.min(...recentLearningDays) > 7 : true;
const staleMemory = mtimeDays(memoryPath) != null ? mtimeDays(memoryPath) > 30 : true;

const checks = [
  {name:'durable_memory_exists', ok: exists(memoryPath), weight:20},
  {name:'daily_memory_dir_exists', ok: exists(dailyDir), weight:10},
  {name:'today_memory_exists', ok: exists(todayFile), weight:10},
  {name:'daily_memory_has_history', ok: dailyFiles.length > 0, weight:10},
  {name:'learnings_dir_exists', ok: exists(learnDir), weight:15},
  {name:'learnings_has_entries', ok: learningFiles.length > 0, weight:15},
  {name:'learnings_recently_updated', ok: !staleLearn, weight:10},
  {name:'durable_memory_not_stale', ok: !staleMemory, weight:10},
];

const weighted = checks.reduce((s,c)=>s+(c.ok?c.weight:0),0);
const fail = checks.filter(x=>!x.ok).length;
console.log(JSON.stringify({
  fail,
  score: weighted,
  checks,
  stats:{
    learningFiles: learningFiles.length,
    dailyFiles: dailyFiles.length,
    memoryAgeDays: mtimeDays(memoryPath),
    todayFile,
  }
}, null, 2));
process.exitCode = fail ? 1 : 0;
