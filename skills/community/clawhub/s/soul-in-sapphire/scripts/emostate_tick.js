#!/usr/bin/env node
// Subjective payload in; validated, retry-safe persistence out.
import fs from 'node:fs';
import path from 'node:path';
import {httpJson} from './notionctl_bridge.js';
import {loadIds,withFileLock,atomicJson} from './soul_io.js';
import {writeTick,payloadHash} from './emostate_service.js';
async function main(){
 const args={};
 for(let i=2;i<process.argv.length;i++){
  const raw=process.argv[i],equal=raw.indexOf('='),key=equal>=0?raw.slice(0,equal):raw;
  if(key==='--help'||key==='-h'){console.log('emostate_tick.js --ids-file <json> --payload-file <json> [--receipt-file <json>] [--mirror-file <now-state.json>]\nPayload scale_version:2; emotion level -5..5. Explicit --events-dbid --emotions-dbid --state-dbid --state-dsid are also accepted.');return;}
  const value=equal>=0?raw.slice(equal+1):process.argv[++i];
  if(!['--ids-file','--payload-file','--payload-json','--receipt-file','--mirror-file','--heartbeat-file','--events-dbid','--emotions-dbid','--state-dbid','--state-dsid'].includes(key)||!value||value.startsWith('--'))throw Error('Unknown/missing argument: '+key);
  args[key.slice(2)]=value;
 }
 if(args['payload-file']&&args['payload-json'])throw Error('Choose payload file or JSON, not both');
 const payload=JSON.parse(args['payload-json']??fs.readFileSync(args['payload-file']||0,'utf8'));
 const ids=loadIds(args['ids-file']);
 for(const lane of ['events','emotions','state']){
  ids[lane]??={};
  ids[lane].database_id=args[lane+'-dbid']||ids[lane].database_id;
 }
 ids.state.data_source_id=args['state-dsid']||ids.state.data_source_id;
 const receiptFile=args['receipt-file']||path.resolve('memory/soul-in-sapphire/ticks/'+payloadHash(payload,ids)+'.json');
 const noteAttempt=(result,error)=>{
  if(!args['heartbeat-file'])return;
  const file=args['heartbeat-file'];let prior={};try{prior=JSON.parse(fs.readFileSync(file));}catch{}
  atomicJson(file,{...prior,lastSnapshotAttemptAt:Math.floor(Date.now()/1000),lastSnapshotResult:error?'error':'success',
   lastSnapshotError:error?{stage:error.details?.stage||'input',receipt_file:receiptFile}:null,
   ...(result&&Math.floor(Date.parse(result.when)/1000)>=(prior.lastSnapshotAt||0)?{lastSnapshotAt:Math.floor(Date.parse(result.when)/1000),lastSnapshotSource:payload.state?.source||payload.event?.source||'soul:tick'}:{})});
 };
 let result;
 try{result=await withFileLock(path.resolve('memory/soul-in-sapphire/locks/'+ids.state.database_id+'.lock'),
  ()=>writeTick(payload,ids,{request:httpJson,receiptFile,mirrorFile:args['mirror-file']}));noteAttempt(result,null);}
 catch(e){noteAttempt(null,e);throw e;}
 console.log(JSON.stringify(result,null,2));
}
main().catch(e=>{console.log(JSON.stringify(e.details||{ok:false,stage:'input',partial:null}));console.error(e.message);process.exitCode=1;});
