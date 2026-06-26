#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const OUTDIR=path.join(ROOT,'reports','shared-memory'); fs.mkdirSync(OUTDIR,{recursive:true});
const latest=JSON.parse(fs.readFileSync(path.join(OUTDIR,'latest-health.json'),'utf8'));
const promo=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-promotion-candidates.json'),'utf8'));
const dup=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-duplicate-learnings.json'),'utf8'));
const stale=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-stale-durable-memory.json'),'utf8'));
const skill=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-skill-upgrade-candidates.json'),'utf8'));
const validated=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-validated-rules.json'),'utf8'));
const low=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-low-value-learnings.json'),'utf8'));
const workflow=JSON.parse(fs.readFileSync(path.join(OUTDIR,'shared-memory-workflow-optimization.json'),'utf8'));
let md='# Shared Memory Audit Report\n\n';
md+=`- Health score: ${latest.score}\n- Failed checks: ${latest.fail}\n- Promotion candidates: ${promo.promotionCandidates||0}\n- Duplicate groups: ${dup.duplicateGroups||0}\n- Stale durable entries: ${stale.candidates||0}\n- Validated repeated rules: ${validated.validatedRules||0}\n- Low-value learnings: ${low.lowValueCandidates||0}\n- Workflow optimizations: ${workflow.workflowSuggestions||0}\n- Cross-skill upgrade candidates: ${skill.candidates||0}\n\n`;
if((promo.candidates||[]).length){ md+='## Promotion Review Queue\n'; for(const c of promo.candidates) md+=`- ${c.summary} | confidence=${c.confidence} | review=${c.reviewStatus}\n`; md+='\n'; }
if((dup.duplicates||[]).length){ md+='## Duplicate Review Queue\n'; for(const d of dup.duplicates) md+=`- ${d.normalizedKey} | confidence=${d.confidence} | lifecycle=${d.suggestedLifecycle}\n`; md+='\n'; }
if((stale.entries||[]).length){ md+='## Stale Durable Memory Review\n'; for(const s of stale.entries) md+=`- ${s.line} | confidence=${s.confidence} | lifecycle=${s.suggestedLifecycle}\n`; md+='\n'; }
if((validated.candidates||[]).length){ md+='## Validated Repeated Rules\n'; for(const v of validated.candidates) md+=`- ${v.summary} | confidence=${v.confidence} | occurrences=${v.occurrences}\n`; md+='\n'; }
if((low.items||[]).length){ md+='## Low-Value Learnings\n'; for(const l of low.items) md+=`- ${l.file} | confidence=${l.confidence} | issues=${l.issues.join(', ')}\n`; md+='\n'; }
if((workflow.suggestions||[]).length){ md+='## Workflow Optimization Suggestions\n'; for(const w of workflow.suggestions) md+=`- ${w.area} | confidence=${w.confidence} | ${w.suggestion}\n`; md+='\n'; }
if((skill.suggestions||[]).length){ md+='## Cross-Skill Collaboration Opportunities\n'; for(const s of skill.suggestions) md+=`- ${s.skill} | confidence=${s.confidence} | evidence=${(s.evidence||[]).join(', ')}\n`; md+='\n'; }
fs.writeFileSync(path.join(OUTDIR,'shared-memory-audit-report.md'), md);
console.log(JSON.stringify({out:path.join(OUTDIR,'shared-memory-audit-report.md')},null,2));
