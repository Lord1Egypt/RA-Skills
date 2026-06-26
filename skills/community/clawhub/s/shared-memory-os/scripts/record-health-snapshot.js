#!/usr/bin/env node
const fs=require('fs'); const path=require('path');
const ROOT='/home/zqh2333/.openclaw/workspace'; const OUTDIR=path.join(ROOT,'reports','shared-memory'); fs.mkdirSync(OUTDIR,{recursive:true});
let data={history:[]}; const p=path.join(OUTDIR,'shared-memory-health-history.json'); try{data=JSON.parse(fs.readFileSync(p,'utf8'));}catch{}
const latestPath=path.join(OUTDIR,'latest-health.json'); const latest=JSON.parse(fs.readFileSync(latestPath,'utf8'));
data.history.push({at:new Date().toISOString(), score:latest.score, fail:latest.fail});
if(data.history.length>180) data.history=data.history.slice(-180);
fs.writeFileSync(p, JSON.stringify(data,null,2)); console.log(JSON.stringify({entries:data.history.length,out:p},null,2));
