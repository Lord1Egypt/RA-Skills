import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {buildVent,decodeVent,writeVent,recallVents,main} from './vent_journal.js';

const ids = {journal:{database_id:'journal-db',data_source_id:'journal-ds'}};
const input = {entry_id:'11111111-1111-4111-8111-111111111111',when:'2026-10-11T23:25:00+09:00',
  title:'注文の多い愚痴',trigger:'手加減なしの記録を頼まれた。',context_ref:'fixture:turn',
  body:`  悪口まで注文つけるのか。面倒くさい奴だな。
丸めず残す。  `};
function page(props,id='22222222-2222-4222-8222-222222222222') {
  return {id,url:'https://example.invalid/'+id,parent:{data_source_id:'journal-ds'},
    properties:Object.fromEntries(Object.entries(props).map(([k,v])=>[k,{type:Object.keys(v)[0],...structuredClone(v)}]))};
}
function fixture(options={}) {
  const calls=[], pages=[...(options.pages || [])];
  const request=async(method,url,body)=>{
    calls.push({method,url,body});
    if (url==='/v1/databases/journal-db') return {data_sources:[{id:options.wrongDs?'other':'journal-ds'}]};
    if (url==='/v1/data_sources/journal-ds') return {parent:{database_id:'journal-db'},
      properties:Object.fromEntries(Object.entries({Name:'title',when:'date',body:options.badSchema?'number':'rich_text',worklog:'rich_text'}).map(([k,type])=>[k,{type}]))};
    if (url.endsWith('/query')) return {results:pages,has_more:!!options.more};
    if (url==='/v1/pages' && method==='POST') {
      if (options.failCreate) throw Error('fixture timeout');
      const created=page(body.properties); pages.push(created); return created;
    }
    if (url.startsWith('/v1/pages/') && method==='GET') {
      if (options.failRead) throw Error('fixture read failed');
      const found=pages.find(p=>url.endsWith(p.id));
      if (!found) throw Error('fixture not found');
      const copy=structuredClone(found);
      if (options.mismatch) copy.properties.body.rich_text[0].text.content='silently softened';
      return copy;
    }
    throw Error('Unexpected '+method+' '+url);
  };
  return {request,calls,pages,options};
}
function receipt() {return path.join(fs.mkdtempSync(path.join(os.tmpdir(),'sis-vent-')),'receipt.json');}
const posts=f=>f.calls.filter(c=>c.method==='POST'&&c.url==='/v1/pages');

test('raw Japanese, whitespace, swearing, and no reconciliation survive round trip',()=>{
  const props=buildVent(input); const decoded=decodeVent(page(props));
  assert.equal(decoded.body,input.body);
  assert.equal(decoded.trigger,input.trigger);
  assert.equal(decoded.kind,'subjective_vent');
  assert.equal(decoded.follow_up_to,null);
  assert.match(decoded.interpretation,/not a user fact/);
  assert.deepEqual(Object.keys(props),['Name','when','body','worklog']);
});
test('long Unicode body is split losslessly within Notion text limits',()=>{
  const body='怒💢'.repeat(6000); const p=buildVent({...input,body});
  assert.equal(decodeVent(page(p)).body,body);
  assert.ok(p.body.rich_text.every(x=>x.text.content.length<=2000&&x.text.content.isWellFormed()));
});
for (const [name,patch] of Object.entries({blank:{body:'  '},oversized:{body:'x'.repeat(20001)},
  noTrigger:{trigger:''},noContext:{context_ref:''},badId:{entry_id:'new'},badDate:{when:'yesterday'},
  noTimezone:{when:'2026-10-11T23:25:00'},invalidLink:{follow_up_to:'guess'},unknown:{user_fact:'bad'}})) {
  test('rejects '+name+' rather than inventing/truncating input',()=>assert.throws(()=>buildVent({...input,...patch})));
}
test('write validates target, creates only journal row, verifies exact body, and records receipt',async()=>{
  const f=fixture(), file=receipt();
  const result=await writeVent({input,ids,receiptFile:file,request:f.request});
  assert.equal(result.verified,true); assert.equal(posts(f).length,1);
  assert.deepEqual(posts(f)[0].body.parent,{type:'data_source_id',data_source_id:'journal-ds'});
  assert.equal(JSON.parse(fs.readFileSync(file)).verified,true);
  assert.equal(fs.existsSync(file+'.lock'),false);
  const repeated=await writeVent({input,ids,receiptFile:file,request:f.request});
  assert.equal(repeated.reused,true); assert.equal(posts(f).length,1);
});
test('existing identical remote row is reused even without local receipt',async()=>{
  const f=fixture({pages:[page(buildVent(input))]});
  assert.equal((await writeVent({input,ids,receiptFile:receipt(),request:f.request})).reused,true);
  assert.equal(posts(f).length,0);
});
test('Notion minute precision is accepted but a different minute is not',async()=>{
  const precise={...input,when:'2026-10-11T23:25:42.123+09:00'};
  const p=page(buildVent(precise)); p.properties.when.date.start='2026-10-11T14:25:00.000+00:00';
  const f=fixture({pages:[p]});
  assert.equal((await writeVent({input:precise,ids,receiptFile:receipt(),request:f.request})).verified,true);
  p.properties.when.date.start='2026-10-11T14:26:00.000+00:00';
  await assert.rejects(writeVent({input:precise,ids,receiptFile:receipt(),request:f.request}),/different content/);
  assert.equal(posts(f).length,0);
});
test('receipt rejects changed payload before API access',async()=>{
  const f=fixture(), file=receipt();
  await writeVent({input,ids,receiptFile:file,request:f.request});
  const n=f.calls.length;
  await assert.rejects(writeVent({input:{...input,body:'changed'},ids,receiptFile:file,request:f.request}),/another payload/);
  assert.equal(f.calls.length,n);
});
test('remote ID conflict does not overwrite or create',async()=>{
  const f=fixture({pages:[page(buildVent({...input,body:'other'}))]});
  await assert.rejects(writeVent({input,ids,receiptFile:receipt(),request:f.request}),/different content/);
  assert.equal(posts(f).length,0);
});
for (const option of ['wrongDs','badSchema']) test(option+' prevents writes',async()=>{
  const f=fixture({[option]:true});
  await assert.rejects(writeVent({input,ids,receiptFile:receipt(),request:f.request}));
  assert.equal(posts(f).length,0);
});
test('ambiguous create failure stops retries without blind duplicate write',async()=>{
  const f=fixture({failCreate:true}), file=receipt();
  await assert.rejects(writeVent({input,ids,receiptFile:file,request:f.request}),/timeout/);
  assert.equal(JSON.parse(fs.readFileSync(file)).verified,false);
  f.options.failCreate=false;
  await assert.rejects(writeVent({input,ids,receiptFile:file,request:f.request}),/ambiguous/);
  assert.equal(posts(f).length,1);
});
test('readback failure recovers the remote row without creating another',async()=>{
  const f=fixture({failRead:true}),file=receipt();
  await assert.rejects(writeVent({input,ids,receiptFile:file,request:f.request}),/read failed/);
  f.options.failRead=false;
  assert.equal((await writeVent({input,ids,receiptFile:file,request:f.request})).reused,true);
  assert.equal(posts(f).length,1);
});
test('readback text mismatch is not success',async()=>{
  const f=fixture({mismatch:true}),file=receipt();
  await assert.rejects(writeVent({input,ids,receiptFile:file,request:f.request}),/read-back mismatch/);
  assert.equal(JSON.parse(fs.readFileSync(file)).verified,false);
});
test('duplicate remote IDs are detected',async()=>{
  const f=fixture({pages:[page(buildVent(input)),page(buildVent(input))]});
  await assert.rejects(writeVent({input,ids,receiptFile:receipt(),request:f.request}),/Duplicate/);
  assert.equal(posts(f).length,0);
});
test('follow-up appends, validates prior journal row, and never PATCHes original',async()=>{
  const prior=page(buildVent(input)); const original=JSON.stringify(prior);
  const f=fixture({pages:[prior]}); const wrapped=async(method,url,body)=>{
    if (url.endsWith('/query')) return {results:[]};
    if (url==='/v1/pages'&&method==='POST') {const p=page(body.properties,'33333333-3333-4333-8333-333333333333');f.pages.push(p);f.calls.push({method,url,body});return p;}
    return f.request(method,url,body);
  };
  await writeVent({input:{...input,entry_id:'44444444-4444-4444-8444-444444444444',body:'まだ腹が立つ。',follow_up_to:prior.id},
    ids,receiptFile:receipt(),request:wrapped});
  assert.equal(JSON.stringify(prior),original);
  assert.ok(f.calls.every(x=>x.method!=='PATCH'&&x.method!=='DELETE'));
  assert.equal(decodeVent(f.pages[1]).follow_up_to,prior.id);
});
test('recall searches only vent lane, keeps historical subjectivity, exposes truncation',async()=>{
  const f=fixture({pages:[page(buildVent(input))],more:true});
  const r=await recallVents({ids,query:'面倒',limit:2,request:f.request});
  assert.equal(r.complete,false); assert.equal(r.has_more,true); assert.equal(r.results[0].body,input.body);
  const q=f.calls.find(c=>c.url.endsWith('/query')).body;
  assert.equal(q.page_size,2); assert.equal(q.filter.and[0].title.starts_with,'[vent:');
  assert.equal(q.filter.and[1].or.length,3);
  assert.equal(posts(f).length,0);
});
test('invalid/ordinary journal records do not masquerade as vents',async()=>{
  const f=fixture({pages:[page({Name:{title:[{text:{content:'ordinary'}}]},worklog:{rich_text:[]}})]});
  const r=await recallVents({ids,request:f.request});
  assert.equal(r.results.length,0); assert.equal(r.complete,false); assert.equal(r.diagnostics.length,1);
});
test('recall bound validates before API access',async()=>{
  const f=fixture();
  for (const limit of [0,11,NaN,1.5]) await assert.rejects(recallVents({ids,limit,request:f.request}));
  assert.equal(f.calls.length,0);
});
test('CLI help and dry-run need no Notion call or receipt',async()=>{
  const dir=fs.mkdtempSync(path.join(os.tmpdir(),'sis-vent-cli-'));
  const idfile=path.join(dir,'ids.json'),payload=path.join(dir,'payload.json');
  fs.writeFileSync(idfile,JSON.stringify(ids)); fs.writeFileSync(payload,JSON.stringify(input));
  const result=await main(['write','--ids-file',idfile,'--payload-file',payload,'--dry-run']);
  assert.equal(result.writes,0); assert.equal(result.dry_run,true);
  assert.match((await main(['--help'])).usage,/recall/);
  await assert.rejects(main(['recall','--invented','value']),/Invalid argument/);
  const script=fileURLToPath(new URL('./vent_journal.js',import.meta.url));
  const child=spawnSync(process.execPath,[script,'write','--ids-file',idfile,'--payload-file',payload,'--dry-run'],
    {encoding:'utf8',env:{PATH:process.env.PATH,NOTIONCTL_PATH:'/does/not/exist'},timeout:5000});
  assert.equal(child.status,0,child.stderr); assert.equal(JSON.parse(child.stdout).writes,0);
});
