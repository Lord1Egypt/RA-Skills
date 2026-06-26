#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const OUTDIR=path.join(ROOT,'reports','shared-memory'); fs.mkdirSync(OUTDIR,{recursive:true});
const now=new Date(); const week=`${now.getUTCFullYear()}-W${String(Math.ceil((((now - new Date(Date.UTC(now.getUTCFullYear(),0,1)))/86400000)+1)/7)).padStart(2,'0')}`;
function readJson(p){ try{return JSON.parse(fs.readFileSync(p,'utf8'));}catch{return null;} }
const health=readJson(path.join(OUTDIR,'latest-health.json'))||{};
const dup=readJson(path.join(OUTDIR,'shared-memory-duplicate-learnings.json'))||{};
const promo=readJson(path.join(OUTDIR,'shared-memory-promotion-candidates.json'))||{};
let md=`# Shared Memory Weekly Review ${week}\n\n`;
md+=`- Health score: ${health.score ?? 'n/a'}\n`;
md+=`- Failed checks: ${health.fail ?? 'n/a'}\n`;
md+=`- Duplicate groups: ${dup.duplicateGroups ?? 0}\n`;
md+=`- Promotion candidates: ${promo.promotionCandidates ?? 0}\n\n`;
if ((promo.candidates||[]).length){ md+='## Promotion Candidates\n'; for(const c of promo.candidates) md+=`- ${c.summary} (${c.occurrences})\n`; md+='\n'; }
if ((dup.duplicates||[]).length){ md+='## Duplicate Learning Groups\n'; for(const d of dup.duplicates) md+=`- ${d.summary} (${d.files.length})\n`; md+='\n'; }
const out=path.join(OUTDIR,`shared-memory-weekly-review-${week}.md`); fs.writeFileSync(out,md); console.log(JSON.stringify({out},null,2));
