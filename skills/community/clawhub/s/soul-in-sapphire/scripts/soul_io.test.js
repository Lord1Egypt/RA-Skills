import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {withFileLock} from './soul_io.js';
const root=fs.mkdtempSync(path.join(os.tmpdir(),'sis-current-'));
test('writer lock excludes concurrent work and releases on success/failure',async()=>{
 const file=path.join(root,'writer.lock');let release;
 const held=withFileLock(file,()=>new Promise(r=>{release=r;}));
 await assert.rejects(withFileLock(file,()=>{}),/lock already/);release();await held;
 assert.equal(fs.existsSync(file),false);
 await assert.rejects(withFileLock(file,()=>{throw Error('fixture');}),/fixture/);
 assert.equal(fs.existsSync(file),false);
});
test('current recall adds projection without overwriting the historical zero snapshot',()=>{
 const mock=path.join(root,'notionctl.mjs');
 fs.writeFileSync(mock,`console.log(JSON.stringify({ok:true,result:{results:[{id:'fixture',properties:{
 when:{type:'date',date:{start:'2026-10-04T09:00:00Z'}},
 state_json:{type:'rich_text',rich_text:[{plain_text:'{"stress":0,"joy":9,"__meta":{"version":1}}'}]}
 }}]}}));`);
 const env={...process.env,NOTIONCTL_PATH:mock};for(const k of ['NOTION_API_KEY','NOTION_TOKEN','NOTION_API_TOKEN'])delete env[k];
 const file=new URL('./state_recall.js',import.meta.url);
 const r=spawnSync(process.execPath,[file.pathname,'--state-dsid','fixture','--current','--at','2026-10-05T09:00:00Z'],{encoding:'utf8',env});
 assert.equal(r.status,0,r.stderr);const row=JSON.parse(r.stdout)[0];
 assert.equal(row.state_json.stress,0);assert.equal(row.state_json.joy,9);
 assert.equal(row.projected_state.stress,-2.5);assert.equal(row.projected_state.joy,2);
 assert.equal(row.temporal_scope,'projection_now_from_recorded_snapshot');
});
