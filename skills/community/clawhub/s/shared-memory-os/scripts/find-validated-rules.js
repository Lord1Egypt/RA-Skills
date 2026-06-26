#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const LEARN=path.join(ROOT,'.learnings');
const files=fs.readdirSync(LEARN).filter(f=>f.endsWith('.md')&&f!=='INDEX.md').sort();
function summary(t){ return ((t.match(/### Summary\n([^\n]+)/)||[,''])[1]||'').trim(); }
function logged(t){ return ((t.match(/\*\*Logged\*\*: ([^\n]+)/)||[,''])[1]||'').trim(); }
function norm(s){ return String(s).toLowerCase().replace(/[^a-z0-9\u4e00-\u9fa5]+/g,' ').trim(); }
const map=new Map();
for(const f of files){ const t=fs.readFileSync(path.join(LEARN,f),'utf8'); const k=norm(summary(t)); if(!k) continue; if(!map.has(k)) map.set(k,[]); map.get(k).push({file:f, summary:summary(t), logged:logged(t)}); }
const candidates=[...map.entries()].filter(([,arr])=>arr.length>=2).map(([key,arr])=>({
  normalizedKey:key,
  summary:arr[0].summary,
  occurrences:arr.length,
  evidence:[`repeated in ${arr.length} learning entries`, ...arr.map(x=>`${x.file}:${x.logged}`)],
  confidence: arr.length>=3 ? 'high' : 'medium',
  suggestedAction:'Consider promoting this repeated rule into durable memory or into the relevant skill guidance.',
  suggestedLifecycle:'validated-repeated-rule'
}));
console.log(JSON.stringify({validatedRules:candidates.length,candidates},null,2));
