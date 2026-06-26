#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const dir=path.join(ROOT,'reports','shared-memory','conflicts'); fs.mkdirSync(dir,{recursive:true});
const files=fs.readdirSync(dir).filter(f=>f.endsWith('.md')).sort();
let md='# Shared Memory Conflict Review\n\n'; md+=`- Conflict records: ${files.length}\n\n`;
for(const f of files.slice(-20)) md+=`- ${f}\n`;
const out=path.join(ROOT,'reports','shared-memory','shared-memory-conflict-review.md'); fs.writeFileSync(out,md); console.log(JSON.stringify({out, count:files.length},null,2));
