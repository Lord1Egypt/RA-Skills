#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const OUTDIR=path.join(ROOT,'reports','shared-memory'); fs.mkdirSync(OUTDIR,{recursive:true});
const promo=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-promotion-candidates.json'),'utf8'));
let out='# Promotion Suggestions\n\n';
for(const c of (promo.candidates||[])){
  out+=`## ${c.summary}\n\nSuggested durable wording:\n- ${c.summary}\n\nSuggested action:\n${c.suggested || 'Review and promote into MEMORY.md if still stable.'}\n\n`;
}
const p=path.join(OUTDIR,'shared-memory-promotion-suggestions.md'); fs.writeFileSync(p,out); console.log(JSON.stringify({out:p},null,2));
