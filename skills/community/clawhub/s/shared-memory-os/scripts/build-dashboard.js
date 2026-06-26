#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const OUTDIR=path.join(ROOT,'reports','shared-memory'); fs.mkdirSync(OUTDIR,{recursive:true});
const latest=JSON.parse(fs.readFileSync(path.join(OUTDIR,'latest-health.json'),'utf8'));
const promo=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-promotion-candidates.json'),'utf8'));
const dup=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-duplicate-learnings.json'),'utf8'));
const stale=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-stale-durable-memory.json'),'utf8'));
const history=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-health-history.json'),'utf8'));
const dashboard={
  health:{score:latest.score, fail:latest.fail, trend:(history.history||[]).slice(-5)},
  counts:{promotionCandidates:promo.promotionCandidates||0, duplicateGroups:dup.duplicateGroups||0, staleEntries:stale.candidates||0},
  nextActions:[
    'Review high-confidence promotion candidates',
    'Merge duplicate learnings or mark them superseded',
    'Review dated durable-memory entries for lifecycle changes',
    'Inspect skill-upgrade candidates for cross-skill collaboration'
  ]
};
fs.writeFileSync(path.join(OUTDIR,'dashboard.json'), JSON.stringify(dashboard,null,2));
let md='# Shared Memory Dashboard\n\n';
md+=`- Health score: ${dashboard.health.score}\n- Failed checks: ${dashboard.health.fail}\n- Promotion candidates: ${dashboard.counts.promotionCandidates}\n- Duplicate groups: ${dashboard.counts.duplicateGroups}\n- Stale durable entries: ${dashboard.counts.staleEntries}\n\n## Next Actions\n`;
for(const x of dashboard.nextActions) md+=`- ${x}\n`;
fs.writeFileSync(path.join(OUTDIR,'dashboard.md'), md);
console.log(JSON.stringify({json:path.join(OUTDIR,'dashboard.json'), md:path.join(OUTDIR,'dashboard.md')},null,2));
