#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const LEARN=path.join(ROOT,'.learnings');
const files=fs.readdirSync(LEARN).filter(f=>f.endsWith('.md')&&f!=='INDEX.md');
function summary(t){ return ((t.match(/### Summary\n([^\n]+)/)||[,''])[1]||'').trim(); }
function norm(s){ return String(s).toLowerCase().replace(/[^a-z0-9\u4e00-\u9fa5]+/g,' ').trim(); }
const map=new Map(); for(const f of files){ const t=fs.readFileSync(path.join(LEARN,f),'utf8'); const k=norm(summary(t)); if(!k) continue; if(!map.has(k)) map.set(k,[]); map.get(k).push({file:f,summary:summary(t)});} 
const merges=[...map.entries()].filter(([,arr])=>arr.length>1).map(([normalizedKey,entries])=>({
  normalizedKey,
  files: entries.map(x=>x.file),
  mergedSummary: entries[0].summary,
  reason:'Duplicate learnings should be collapsed into one stronger reusable rule.',
  evidence:[`duplicate group size ${entries.length}`,...entries.map(x=>x.file)],
  confidence: entries.length >= 3 ? 'high' : 'medium',
  suggestedLifecycle:'supersede-duplicates',
  suggestedMergedEntry: {
    summary: entries[0].summary,
    supersedes: entries.map(x=>x.file)
  }
}));
console.log(JSON.stringify({mergeSuggestions:merges.length, merges},null,2));
