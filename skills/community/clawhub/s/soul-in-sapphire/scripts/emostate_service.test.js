import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {writeTick} from './emostate_service.js';
import {nowIso} from './soul_io.js';
import {spawnSync} from 'node:child_process';
const ids=Object.fromEntries(['events','emotions','state'].map(l=>[l,{database_id:l+'-db',data_source_id:l+'-ds'}]));
const payload={scale_version:2,event:{title:'Synthetic experience',when:'2026-10-05T09:00:00Z'},emotions:[{axis:'joy',level:1,comment:'Synthetic subjective meaning'}],state:{mood_label:'aligned',reason:'Fixture'}};
function scene(){
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'sis-write-')),calls=[];let fail='',seq=0;
 const request=async(method,p,body)=>{
  calls.push({method,p,body});
  if(method==='GET'&&p.includes('/databases/')){const l=p.split('/').at(-1).split('-')[0];return {data_sources:[{id:l+'-ds'}]};}
  if(method==='GET'&&p.includes('/data_sources/')){
   const l=p.split('/').at(-1).split('-')[0];
   const types=l==='events'?{Name:'title',when:'date',context:'rich_text'}:l==='emotions'?{axis:'select',level:'number',scale_version:'number',event:'relation'}:{state_json:'rich_text',when:'date',event:'relation'};
   return {parent:{database_id:l+'-db'},properties:Object.fromEntries(Object.entries(types).map(([k,type])=>[k,{type,...(type==='relation'?{relation:{data_source_id:'events-ds'}}:{})}]))};
  }
  if(p.endsWith('/query'))return {results:[]};
  if(p==='/v1/pages'){
   if(body.parent.database_id===fail)throw Error(fail==='state-db'?'validation_error fixture':'transport unavailable');
   return {id:'page-'+(++seq),url:'https://example.invalid/'+seq};
  }
  throw Error('Unexpected request');
 };
 return {root,calls,request,receiptFile:path.join(root,'receipt.json'),mirrorFile:path.join(root,'mirror.json'),setFail:x=>{fail=x;}};
}
test('preflight rejects target mismatch with zero mutations',async()=>{
 const s=scene(),bad=structuredClone(ids);bad.state.database_id='journal-db';
 await assert.rejects(writeTick(payload,bad,s),/mismatch/);
 assert.equal(s.calls.filter(c=>c.p==='/v1/pages').length,0);
});
test('partial state rejection resumes without duplicating event/emotion; completed retry restores mirror',async()=>{
 const s=scene();s.setFail('state-db');
 await assert.rejects(writeTick(payload,ids,s),e=>e.details.stage==='state'&&e.details.partial.emotions.length===1);
 const r=JSON.parse(fs.readFileSync(s.receiptFile));assert.equal(r.pending,null);
 s.setFail('');const done=await writeTick(payload,ids,s);assert.equal(done.ok,true);
 assert.equal(s.calls.filter(c=>c.p==='/v1/pages'&&c.body.parent.database_id==='events-db').length,1);
 assert.equal(s.calls.filter(c=>c.p==='/v1/pages'&&c.body.parent.database_id==='emotions-db').length,1);
 assert.equal(JSON.parse(fs.readFileSync(s.mirrorFile)).scale_version,2);
 fs.unlinkSync(s.mirrorFile);const n=s.calls.length;
 assert.equal((await writeTick(payload,ids,s)).replayed,true);assert.equal(s.calls.length,n);assert.ok(fs.existsSync(s.mirrorFile));
});
test('transport ambiguity blocks automatic retry and changed receipt payload',async()=>{
 const s=scene();s.setFail('events-db');await assert.rejects(writeTick(payload,ids,s),/transport/);
 const n=s.calls.length;await assert.rejects(writeTick(payload,ids,s),/Ambiguous/);assert.equal(s.calls.length,n);
 await assert.rejects(writeTick({...payload,state:{reason:'changed'}},ids,s),/different payload/);
});
test('missing/null levels are not converted to a negative impulse; invalid scale/range fail before API',async()=>{
 const s=scene();const p=structuredClone(payload);p.emotions[0]={axis:'joy',level:null,comment:'uncertain'};
 const r=await writeTick(p,ids,s);assert.equal(r.state_json.joy,0);
 const s2=scene();await assert.rejects(writeTick({...payload,scale_version:1},ids,s2),/scale_version/);assert.equal(s2.calls.length,0);
 const p2=structuredClone(payload);p2.emotions[0].level=6;
 await assert.rejects(writeTick(p2,ids,s2),/range|-5/);assert.equal(s2.calls.length,0);
});
test('automatic timestamps identify the same instant in UTC and JST',()=>{
 const moduleUrl=new URL('./soul_io.js',import.meta.url).href;
 for(const TZ of ['UTC','Asia/Tokyo','Asia/Kolkata']){
  const r=spawnSync(process.execPath,['--input-type=module','-e','import {nowIso} from '+JSON.stringify(moduleUrl)+';console.log(JSON.stringify({a:Date.now(),b:Date.parse(nowIso())}))'],{encoding:'utf8',env:{...process.env,TZ}});
  const v=JSON.parse(r.stdout);assert.ok(Math.abs(v.a-v.b)<1000);
 }
 assert.ok(nowIso().endsWith('Z'));
});

test('all select lanes reject commas before writes without changing semantic text or creating a receipt',async()=>{
 for(const [lane,field] of [['event','trigger'],['event','source'],['state','mood_label'],['state','intent'],['state','need_stack'],['state','source'],['emotion','need'],['emotion','coping'],['emotion','body_signal'],['state','avoid']]){
  const s=scene(),p=structuredClone(payload),target=lane==='emotion'?p.emotions[0]:p[lane];
  target[field]=['body_signal','avoid'].includes(field)?['one,two']:'one,two';
  await assert.rejects(writeTick(p,ids,s),/Invalid Notion/);assert.equal(s.calls.length,0);assert.equal(fs.existsSync(s.receiptFile),false);assert.deepEqual(target[field],['body_signal','avoid'].includes(field)?['one,two']:'one,two');
 }
});
test('legacy partial receipt cannot be reused with a corrected payload',async()=>{
 const s=scene(),p=structuredClone(payload);s.setFail('state-db');await assert.rejects(writeTick(p,ids,s));
 p.state.intent='changed';const n=s.calls.length;await assert.rejects(writeTick(p,ids,s),/different payload/);assert.equal(s.calls.length,n);
});
