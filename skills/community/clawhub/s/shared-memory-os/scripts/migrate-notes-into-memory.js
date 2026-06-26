#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const src=path.join(ROOT,'notes'); const dst=path.join(ROOT,'memory'); fs.mkdirSync(dst,{recursive:true});
const migrated=[]; if(fs.existsSync(src)){ for(const f of fs.readdirSync(src)){ if(!f.endsWith('.md')) continue; const from=path.join(src,f); const to=path.join(dst,`migrated-${f}`); fs.copyFileSync(from,to); migrated.push({from,to}); }}
console.log(JSON.stringify({ok:true, migrated},null,2));
