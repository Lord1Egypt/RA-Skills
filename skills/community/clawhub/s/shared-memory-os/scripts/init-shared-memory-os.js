#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace';
const dirs=[path.join(ROOT,'memory'), path.join(ROOT,'.learnings'), path.join(ROOT,'reports','shared-memory')];
for(const d of dirs) fs.mkdirSync(d,{recursive:true});
const readme=path.join(ROOT,'.learnings','README.md'); if(!fs.existsSync(readme)) fs.writeFileSync(readme,'# learnings\n');
console.log(JSON.stringify({ok:true, created:dirs},null,2));
