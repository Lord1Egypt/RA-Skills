#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const LEARN=path.join(ROOT,'.learnings');
const learn=fs.readdirSync(LEARN).filter(f=>f.endsWith('.md')&&f!=='INDEX.md').map(f=>fs.readFileSync(path.join(LEARN,f),'utf8')).join('\n').toLowerCase();
const suggestions=[];
if(learn.includes('browser')||learn.includes('web_fetch')) suggestions.push({area:'web-retrieval', suggestion:'When web_fetch fails, default to browser-based retrieval and record the successful fallback path.', confidence:'high', collaboration:['safe-smart-web-fetch','agent-browser']});
if(learn.includes('retry')||learn.includes('installation')) suggestions.push({area:'execution', suggestion:'For install/setup tasks, retry automatically and switch methods before reporting failure.', confidence:'high', collaboration:['shared-memory-os']});
if(learn.includes('fallback')||learn.includes('model')) suggestions.push({area:'model-routing', suggestion:'Feed repeated fallback patterns back into model-registry-manager and related routing policy docs.', confidence:'medium', collaboration:['model-registry-manager','thinking-policy']});
if(learn.includes('trigger')) suggestions.push({area:'skill-quality', suggestion:'Promote repeated trigger misses into skill trigger regression coverage.', confidence:'medium', collaboration:['thinking-policy','skill-creator']});
console.log(JSON.stringify({workflowSuggestions:suggestions.length, suggestions},null,2));
