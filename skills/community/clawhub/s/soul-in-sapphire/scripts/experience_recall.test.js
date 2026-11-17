import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { recallExperiences, parseRecallArgs } from './experience_recall.js';

const uuid = n => `00000000-0000-4000-8000-${String(n).padStart(12,'0')}`;
const ids = {events:uuid(1),emotions:uuid(2),state:uuid(3),mem:uuid(4),journal:uuid(5)};
const cfg = {eventsDsid:ids.events,emotionsDsid:ids.emotions,stateDsid:ids.state};
function property(type, value) {
  if (['title','rich_text'].includes(type)) return {type,[type]:[{plain_text:value,text:{content:value}}]};
  if (type === 'select') return {type,select:value === null ? null : {name:value}};
  if (type === 'date') return {type,date:{start:value}};
  if (type === 'multi_select') return {type,multi_select:value.map(name=>({name}))};
  if (type === 'relation') return {type,relation:value.map(id=>({id})),has_more:false};
  return {type,[type]:value};
}
function scene() {
  const p = (lane, n, fields) => ({object:'page',id:uuid(n),url:`https://example.invalid/${n}`,parent:{type:'data_source_id',data_source_id:ids[lane]},
    created_time:'2026-01-01T00:00:00Z',last_edited_time:'2026-01-01T00:00:00Z',properties:Object.fromEntries(Object.entries(fields).map(([k,[t,v]])=>[k,property(t,v)]))});
  const event = p('events',10,{Name:['title','A synthetic repair'],context:['rich_text','I repaired a fictional relay.'],when:['date','2026-01-01T00:00:00Z'],
    source:['select','manual'],link:['url',null],trigger:['select','progress'],importance:['select','4'],uncertainty:['number',2],control:['number',7],emotions:['relation',[]],state:['relation',[]]});
  const emotion = p('emotions',20,{Name:['title','relief'],axis:['select','stress'],level:['number',0],comment:['rich_text','The fictional relay works again.'],
    weight:['number',null],body_signal:['multi_select',['relief']],need:['select','progress'],coping:['select','act'],event:['relation',[event.id]]});
  const state = p('state',30,{Name:['title','Historical state'],when:['date','2026-01-01T00:00:00Z'],mood_label:['select','clear'],intent:['select','build'],
    need_stack:['select','growth'],need_level:['number',6],avoid:['multi_select',['noise']],reason:['rich_text','A synthetic reason'],state_json:['rich_text','{"stress":0}'],source:['select','event'],event:['relation',[event.id]]});
  const mem = p('mem',40,{Name:['title','Synthetic memory'],Content:['rich_text','Remembered relief in my own words.'],Tags:['multi_select',['relief']],
    Source:['url','https://example.invalid/source'],CreatedAt:['date','2026-01-01T00:00:00Z'],Confidence:['select','high']});
  const rows = {events:[event],emotions:[emotion],state:[state],mem:[mem]};
  const schemas = Object.fromEntries(Object.entries(rows).map(([lane,[row]])=>[lane,{object:'data_source',id:ids[lane],properties:Object.fromEntries(Object.entries(row.properties).map(([name,v])=>[name,{type:v.type,
    ...(v.type === 'relation' ? {relation:{data_source_id:ids[name === 'event' ? 'events' : name],type:'single_property',single_property:{}}} : {})}]))}]));
  const calls = [];
  const request = async (method, apiPath, body) => {
    calls.push({method,apiPath,body});
    assert.ok(method === 'GET' || (method === 'POST' && apiPath.endsWith('/query')), 'reader must not mutate');
    if (apiPath.startsWith('/pages/')) {
      const row = Object.values(rows).flat().find(r=>r.id === apiPath.split('/')[2]);
      if (!row) throw new Error('not found'); return structuredClone(row);
    }
    const lane = Object.keys(ids).find(k=>apiPath.split('/')[2] === ids[k]);
    if (method === 'GET') return structuredClone(schemas[lane]);
    let matches = rows[lane] || [];
    if (body.filter?.relation) matches = matches.filter(r=>r.properties.event?.relation.some(x=>x.id === body.filter.relation.contains));
    const pageSize = body.page_size;
    return {object:'list',results:structuredClone(matches.slice(0,pageSize)),has_more:matches.length>pageSize};
  };
  return {rows,schemas,calls,request,event,emotion,state,mem};
}
const codes = out => out.diagnostics.map(d=>d.code);

test('empty forward links still recover actual reverse-linked affect, zero level and historical state', async () => {
  const s = scene();
  const out = await recallExperiences({...cfg,query:'relay'},{request:s.request});
  assert.equal(out.status,'complete');
  assert.equal(out.budget.requests,6);
  assert.equal(out.results[0].emotions[0].fields.level,0);
  assert.equal(out.results[0].states[0].fields.mood_label,'clear');
  assert.equal(out.results[0].experience.fields.context,'I repaired a fictional relay.');
  assert.deepEqual(out.results[0].emotions[0].relation_evidence.via,['reverse:event']);
  assert.equal(out.results[0].temporal_scope,'recorded_at_experience_not_current');
  assert.equal(out.mem_join,'not_inferred');
  assert.ok(s.calls.filter(c=>c.apiPath.endsWith('/query')).every(c=>c.body.filter));
});
test('state-id follows only its stored event and returns the same experience', async () => {
  const s = scene();
  const out = await recallExperiences({...cfg,stateId:s.state.id},{request:s.request});
  assert.equal(out.status,'complete');
  assert.equal(out.origin.id,s.state.id);
  assert.equal(out.results[0].experience.id,s.event.id);
  assert.equal(out.budget.requests,7);
});
test('missing event link is partial, with no guessed date/text join', async () => {
  const s = scene(); s.state.properties.event.relation = [];
  const out = await recallExperiences({...cfg,stateId:s.state.id},{request:s.request});
  assert.equal(out.status,'partial'); assert.equal(out.complete,false);
  assert.ok(codes(out).includes('missing_event_link')); assert.deepEqual(out.results,[]);
  assert.equal(s.calls.length,4);
});
test('legacy forward-only records remain retrievable but schema gaps are explicit', async () => {
  const s = scene(); delete s.schemas.emotions.properties.event; delete s.emotion.properties.event;
  s.event.properties.emotions.relation = [{id:s.emotion.id}];
  const out = await recallExperiences({...cfg,eventId:s.event.id},{request:s.request});
  assert.equal(out.status,'partial'); assert.ok(codes(out).includes('missing_relation_schema'));
  assert.equal(out.results[0].emotions[0].id,s.emotion.id);
  assert.deepEqual(out.results[0].emotions[0].relation_evidence.via,['forward:emotions']);
  assert.equal(s.calls.filter(c=>c.apiPath === `/data_sources/${ids.emotions}/query`).length,0);
});
test('forward and reverse edges deduplicate; conflicting edges are not silently endorsed', async () => {
  const s = scene(); s.event.properties.emotions.relation = [{id:s.emotion.id}];
  let out = await recallExperiences({...cfg,eventId:s.event.id},{request:s.request});
  assert.equal(out.results[0].emotions.length,1);
  assert.deepEqual(out.results[0].emotions[0].relation_evidence.via,['reverse:event','forward:emotions']);
  s.emotion.properties.event.relation = [{id:uuid(99)}];
  out = await recallExperiences({...cfg,eventId:s.event.id},{request:s.request});
  assert.equal(out.status,'partial'); assert.ok(codes(out).includes('conflicting_relation'));
});
test('wrong relation target and wrong page parent are withheld without following unrelated data', async () => {
  const s = scene(); s.schemas.emotions.properties.event.relation.data_source_id = ids.mem;
  let out = await recallExperiences({...cfg,eventId:s.event.id},{request:s.request});
  assert.ok(codes(out).includes('incompatible_relation_schema'));
  assert.equal(s.calls.filter(c=>c.apiPath === `/data_sources/${ids.emotions}/query`).length,0);
  s.event.parent.data_source_id = ids.mem;
  out = await recallExperiences({...cfg,eventId:s.event.id},{request:s.request});
  assert.deepEqual(out.results,[]); assert.ok(codes(out).includes('source_unavailable_or_wrong_parent'));
});
test('one failing lane returns partial evidence and never echoes private error text', async () => {
  const s = scene();
  const out = await recallExperiences({...cfg,eventId:s.event.id},{request:async(...args)=>{
    if (args[1] === `/data_sources/${ids.emotions}/query`) throw new Error('PRIVATE PAYLOAD');
    return s.request(...args);
  }});
  assert.equal(out.ok,false); assert.equal(out.status,'partial');
  assert.equal(out.results[0].states.length,1); assert.equal(out.results[0].emotions.length,0);
  assert.doesNotMatch(JSON.stringify(out),/PRIVATE PAYLOAD/);
});
test('request, result, inline relation and total text bounds are reported, never hidden', async () => {
  const s = scene();
  let out = await recallExperiences({...cfg,eventId:s.event.id,maxRequests:4},{request:s.request});
  assert.equal(out.ok,false); assert.equal(out.budget.requests,4); assert.ok(codes(out).includes('request_budget_exhausted'));
  s.rows.emotions.push({...structuredClone(s.emotion),id:uuid(21)});
  s.event.properties.state.has_more = true;
  out = await recallExperiences({...cfg,eventId:s.event.id,linkedLimit:1,totalTextLimit:50},{request:s.request});
  assert.ok(codes(out).includes('result_limit')); assert.ok(codes(out).includes('relation_limit'));
  assert.ok(codes(out).includes('text_limit')); assert.equal(out.budget.text_characters,50);
  assert.equal(out.complete,false);
});
test('null emotion axis/level and old missing fields are not complete affect recall', async () => {
  const s = scene(); s.emotion.properties.axis.select = null; s.emotion.properties.level.number = null;
  delete s.state.properties.state_json;
  const out = await recallExperiences({...cfg,eventId:s.event.id},{request:s.request});
  assert.equal(out.status,'partial'); assert.ok(codes(out).includes('empty_recorded_value'));
  assert.ok(out.results[0].states[0].missing_fields.includes('state_json'));
});
test('invalid CLI limits/selectors fail before requests', async () => {
  let calls = 0; const request = async()=>{calls++;};
  for (const extra of [{limit:NaN},{limit:0},{limit:6},{maxRequests:1000},{query:'   '},{eventId:'../wrong'},{stateId:uuid(30)}]) {
    await assert.rejects(recallExperiences({...cfg,query:'relay',...extra},{request}));
  }
  assert.equal(calls,0);
  assert.throws(()=>parseRecallArgs(['--unknown','x']));
  assert.throws(()=>parseRecallArgs(['--query','a','--query','b']));
});

test('ambient state context resolves through real CLI boundary; read/resolve do not acknowledge', () => {
  const s = scene();
  const dir = fs.mkdtempSync(path.join(os.tmpdir(),'sis-experience-'));
  const scripts = path.dirname(fileURLToPath(import.meta.url));
  const fixture = path.join(dir,'fixture.json'); const mock = path.join(dir,'notionctl.mjs');
  fs.writeFileSync(fixture,JSON.stringify({ids,rows:s.rows,schemas:s.schemas}));
  fs.writeFileSync(mock,`import fs from 'node:fs';
const {ids,rows,schemas}=JSON.parse(fs.readFileSync(${JSON.stringify(fixture)},'utf8'));
const a=process.argv.slice(2);const get=k=>a[a.indexOf(k)+1];const p=get('--path');const b=a.includes('--body-json')?JSON.parse(get('--body-json')):{};
const lane=Object.keys(ids).find(k=>ids[k]===p.split('/').at(-2)||ids[k]===p.split('/').at(-1));
let result;
if(p.includes('/pages/'))result=Object.values(rows).flat().find(r=>r.id===p.split('/').at(-1));
else if(p.endsWith('/query'))result={results:(rows[lane]||[]).slice(0,b.page_size),has_more:false};
else result=schemas[lane];
console.log(JSON.stringify({ok:true,result}));`);
  const env = {...process.env,NOTIONCTL_PATH:mock,SIS_AMBIENT_RECALL:'1'};
  for (const name of ['NOTION_API_KEY','NOTION_TOKEN','NOTION_API_TOKEN']) delete env[name];
  const run = (script,args) => {
    const r = spawnSync(process.execPath,[path.join(scripts,script+'.js'),...args],{env,encoding:'utf8',timeout:10000});
    assert.equal(r.status,0,r.stderr); return JSON.parse(r.stdout);
  };
  const staged = run('stage_ambient_recall',['--workspace',dir,'--force-roll','1','--state-dsid',ids.state]);
  assert.equal(staged.recall.affect_context.fields.mood_label,'clear');
  assert.equal(staged.recall.affect_context.fields.state_json,'{"stress":0}');
  assert.deepEqual(staged.recall.affect_context.event_ids,[s.event.id]);
  const file = staged.stagedFile;
  const resolved = run('read_ambient_recall',['--file',file,'--resolve','--events-dsid',ids.events,'--emotions-dsid',ids.emotions,'--state-dsid',ids.state]);
  assert.equal(resolved.status,'available'); assert.equal(resolved.resolution.status,'complete');
  assert.equal(resolved.resolution.results[0].emotions[0].fields.level,0);
  assert.equal(fs.existsSync(file+'.consumption.json'),false);
  const ack = run('read_ambient_recall',['--file',file,'--ack',resolved.recall.id,'--used-in','synthetic:test-turn']);
  assert.equal(ack.receipt.evidence,'consumer_acknowledgment');
  assert.equal(ack.receipt.used_in,'synthetic:test-turn');
  const durable = run('stage_ambient_recall',['--workspace',dir,'--force-roll','5','--mem-dsid',ids.mem,'--mem-dbid',uuid(100)]);
  assert.deepEqual(durable.recall.affect_context.fields.Tags,['relief']);
  assert.equal(durable.recall.affect_context.status,'mem_only_no_verified_event_join');
  assert.equal(run('read_ambient_recall',['--file',durable.stagedFile,'--resolve']).resolution.status,'no_verified_event_route');
});
