#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const OUTDIR=path.join(ROOT,'reports','shared-memory'); fs.mkdirSync(OUTDIR,{recursive:true});
const promo=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-promotion-candidates.json'),'utf8'));
let out='# MEMORY Patch Candidates\n\n';
for(const c of (promo.candidates||[])){
  out+=`## Candidate: ${c.summary}\n\n- Suggested section: durable-rules\n- Confidence: medium\n- Evidence: repeated ${c.occurrences} times in learnings\n\nSuggested patch line:\n- ${c.summary}\n\n`;
}
const p=path.join(OUTDIR,'shared-memory-memory-patch-candidates.md'); fs.writeFileSync(p,out); console.log(JSON.stringify({out:p},null,2));
