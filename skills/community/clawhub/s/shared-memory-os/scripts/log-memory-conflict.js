#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const dir=path.join(ROOT,'reports','shared-memory','conflicts'); fs.mkdirSync(dir,{recursive:true});
const now=new Date().toISOString().replace(/[:.]/g,'-');
const body=`# Shared Memory Conflict\n\n- Date: ${new Date().toISOString()}\n- Sources in conflict:\n- Chosen source:\n- Reason:\n- Temporary or permanent:\n- Follow-up needed:\n`;
const out=path.join(dir,`conflict-${now}.md`); fs.writeFileSync(out,body); console.log(JSON.stringify({out},null,2));
