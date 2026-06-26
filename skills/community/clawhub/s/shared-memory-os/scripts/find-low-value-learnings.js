#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const LEARN=path.join(ROOT,'.learnings');
const files=fs.readdirSync(LEARN).filter(f=>f.endsWith('.md')&&f!=='INDEX.md').sort();
function summary(t){ return ((t.match(/### Summary\n([^\n]+)/)||[,''])[1]||'').trim(); }
function suggested(t){ return ((t.match(/### Suggested Action\n([\s\S]*?)(\n## |$)/)||[,''])[1]||'').trim(); }
const items=[];
for(const f of files){ const t=fs.readFileSync(path.join(LEARN,f),'utf8'); const s=summary(t); const a=suggested(t); const issues=[]; if(!s||s.length<12) issues.push('summary-too-short'); if(!a) issues.push('missing-suggested-action'); if(/临时|一次性|仅本次|this one time/i.test(t)) issues.push('likely-one-off'); if(issues.length) items.push({file:f, summary:s||'(missing)', issues, confidence: issues.length>=2 ? 'medium' : 'low', suggestedLifecycle:'review-for-archive-or-prune'}); }
console.log(JSON.stringify({lowValueCandidates:items.length, items},null,2));
