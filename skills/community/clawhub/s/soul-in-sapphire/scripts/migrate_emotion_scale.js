#!/usr/bin/env node
// Plan from a complete snapshot; guarded/idempotent apply or rollback.
import fs from 'node:fs';
import {httpJson} from './notionctl_bridge.js';
import {planScaleMigration,applyScalePlan} from './emotion_scale_migration.js';
import {atomicJson} from './soul_io.js';
const args=process.argv.slice(2),mode=args[0],file=args[1];
try{
 if(mode==='plan'){
  const rows={state:JSON.parse(fs.readFileSync(file+'/all-state.json')),emotions:JSON.parse(fs.readFileSync(file+'/all-emotions.json'))};
  const plan=planScaleMigration(rows);atomicJson(args[2],plan);
  console.log(JSON.stringify({ok:true,operations:plan.operations.length,plan:args[2]}));
 }else if(['apply','rollback'].includes(mode)){
  const plan=JSON.parse(fs.readFileSync(file));
  const result=await applyScalePlan(plan,{request:httpJson,progressFile:args[2],direction:mode==='apply'?'forward':'rollback',
   onProgress:(completed,total)=>{if(completed%10===0||completed===total)console.error(JSON.stringify({completed,total}));}});
  console.log(JSON.stringify(result));
 }else throw Error('Usage: migrate_emotion_scale.js plan <snapshot-directory> <plan.json> | apply/rollback <plan.json> <progress.json>');
}catch(e){console.error(e.message);process.exitCode=1;}
