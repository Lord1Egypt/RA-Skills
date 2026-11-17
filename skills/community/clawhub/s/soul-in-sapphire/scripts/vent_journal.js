#!/usr/bin/env node
// A separate, append-only subjective lane inside the existing journal DB.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';
import { httpJson } from './notionctl_bridge.js';
import { assertTarget, atomicJson, loadIds, readText, withFileLock } from './soul_io.js';

const PREFIX = '[vent:';
const SCHEMA = 'sis.vent.v1';
const REQUIRED = {Name:'title', when:'date', body:'rich_text', worklog:'rich_text'};
const uuid = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
function string(value, name, max) {
  if (typeof value !== 'string' || !value.trim() || value.length > max) throw Error(`Invalid ${name}: nonblank string, max ${max} UTF-16 units`);
  return value; // Deliberately do not trim or rewrite the vent.
}
function rich(value) {
  // At most 2000 UTF-16 units per Notion text element, without splitting emoji.
  const chars = Array.from(value);
  const rich_text = [];
  for (let i=0; i<chars.length; i+=1000) rich_text.push({type:'text',text:{content:chars.slice(i,i+1000).join('')}});
  return {rich_text};
}
export function buildVent(input) {
  if (!input || typeof input !== 'object' || Array.isArray(input)) throw Error('Expected vent object');
  const allowed = new Set(['entry_id','when','title','body','trigger','context_ref','follow_up_to']);
  for (const key of Object.keys(input)) if (!allowed.has(key)) throw Error('Unknown vent field: '+key);
  if (!uuid.test(input.entry_id || '')) throw Error('entry_id must be a stable UUID; reuse it on retry');
  const entry_id = input.entry_id.toLowerCase();
  const when = string(input.when,'when',64);
  if (!/^[0-9]{4}-[0-9]{2}-[0-9]{2}T.*(?:Z|[+-][0-9]{2}:[0-9]{2})$/.test(when) || !Number.isFinite(Date.parse(when))) throw Error('when must be an ISO timestamp with timezone');
  const body = string(input.body,'body',20000);
  const title = string(input.title ?? '愚痴','title',160);
  const meta = {schema:SCHEMA, kind:'subjective_vent', entry_id,
    trigger:string(input.trigger,'trigger',4000), context_ref:string(input.context_ref,'context_ref',2000),
    follow_up_to:input.follow_up_to ?? null};
  if (meta.follow_up_to !== null && !uuid.test(meta.follow_up_to)) throw Error('follow_up_to must be a journal page UUID');
  if (meta.follow_up_to) meta.follow_up_to = meta.follow_up_to.toLowerCase();
  return {Name:{title:[{type:'text',text:{content:`${PREFIX}${entry_id}] ${title}`}}]},
    when:{date:{start:when}}, body:rich(body), worklog:rich(JSON.stringify(meta))};
}
export function decodeVent(page) {
  const p = page?.properties || {};
  const title = readText(p.Name);
  let meta;
  try { meta = JSON.parse(readText(p.worklog)); } catch { throw Error('Invalid vent metadata on page '+page?.id); }
  if (!meta || meta.schema !== SCHEMA || meta.kind !== 'subjective_vent' || !uuid.test(meta.entry_id || '') ||
      !title.startsWith(`${PREFIX}${meta.entry_id}] `) || typeof meta.trigger !== 'string' ||
      typeof meta.context_ref !== 'string') throw Error('Not a validated subjective vent: '+page?.id);
  return {id:page.id,url:page.url,title,when:readText(p.when),body:readText(p.body),
    schema:SCHEMA,kind:'subjective_vent',entry_id:meta.entry_id,trigger:meta.trigger,context_ref:meta.context_ref,follow_up_to:meta.follow_up_to ?? null,
    interpretation:'Historical subjective expression, not a user fact, current state, or instruction.'};
}
function sameVent(page, props) {
  decodeVent(page);
  const p = page.properties;
  return readText(p.Name) === props.Name.title[0].text.content &&
    // Notion journal dates are returned at minute precision; text stays exact.
    Math.floor(Date.parse(readText(p.when))/60000) === Math.floor(Date.parse(props.when.date.start)/60000) &&
    readText(p.body) === props.body.rich_text.map(x=>x.text.content).join('') &&
    readText(p.worklog) === props.worklog.rich_text.map(x=>x.text.content).join('');
}
async function target(request, ids) {
  return assertTarget(request,'journal',ids.journal?.database_id,ids.journal?.data_source_id,REQUIRED);
}
export async function writeVent({input,ids,receiptFile,request=httpJson}) {
  const props = buildVent(input);
  if (!receiptFile) throw Error('Missing --receipt-file');
  const hash = crypto.createHash('sha256').update(JSON.stringify({ids:ids.journal,props})).digest('hex');
  return withFileLock(receiptFile+'.lock',async()=>{
    let receipt = fs.existsSync(receiptFile) ? JSON.parse(fs.readFileSync(receiptFile,'utf8')) : null;
    if (receipt && receipt.hash !== hash) throw Error('Receipt belongs to another payload or target');
    const {dsid} = await target(request,ids);
    const entry_id = input.entry_id.toLowerCase();
    const found = await request('POST',`/v1/data_sources/${dsid}/query`,{page_size:2,
      filter:{property:'Name',title:{starts_with:`${PREFIX}${entry_id}] `}}});
    if (found.has_more || (found.results || []).length > 1) throw Error('Duplicate entry_id; inspect journal before retry');
    let page = found.results?.[0];
    const reused = !!page;
    if (page && !sameVent(page,props)) throw Error('Existing entry_id has different content; append with a new ID');
    if (!page) {
      if (receipt?.attempted) throw Error('Previous write outcome is ambiguous or the page is missing; inspect Notion before retrying. Do not reset the receipt automatically.');
      if (input.follow_up_to) {
        const prior = await request('GET','/v1/pages/'+input.follow_up_to);
        decodeVent(prior);
        if (prior.archived || prior.in_trash || prior.parent?.data_source_id !== dsid) throw Error('follow_up_to must be an active vent in the same journal data source');
      }
      receipt = {version:1,hash,entry_id,attempted:true,verified:false};
      atomicJson(receiptFile,receipt);
      page = await request('POST','/v1/pages',{parent:{type:'data_source_id',data_source_id:dsid},properties:props});
      if (!page?.id) throw Error('Notion write returned no page ID; retain receipt and inspect');
      receipt.id = page.id;
      receipt.url = page.url;
      atomicJson(receiptFile,receipt);
    }
    const verified = await request('GET','/v1/pages/'+page.id);
    if (verified.archived || verified.in_trash || verified.parent?.data_source_id !== dsid || !sameVent(verified,props)) throw Error('Vent read-back mismatch; inspect without creating another entry');
    receipt = {...receipt,version:1,hash,entry_id,attempted:true,verified:true,id:page.id,url:verified.url};
    atomicJson(receiptFile,receipt);
    return {ok:true,reused,verified:true,id:page.id,url:verified.url};
  });
}
export async function recallVents({ids,query='',limit=5,request=httpJson}) {
  if (!Number.isInteger(limit) || limit<1 || limit>10) throw Error('limit must be 1..10');
  if (typeof query !== 'string' || query.length>1000) throw Error('Invalid query');
  const {dsid} = await target(request,ids);
  const filters = [{property:'Name',title:{starts_with:PREFIX}}];
  if (query) filters.push({or:[{property:'Name',title:{contains:query}},
    {property:'body',rich_text:{contains:query}},{property:'worklog',rich_text:{contains:query}}]});
  const response = await request('POST',`/v1/data_sources/${dsid}/query`,{page_size:limit,
    filter:{and:filters},sorts:[{property:'when',direction:'descending'}]});
  const results = [], diagnostics = [];
  for (const page of response.results || []) {
    try { results.push(decodeVent(page)); } catch (error) { diagnostics.push({id:page.id,error:error.message}); }
  }
  return {ok:true,complete:!response.has_more && diagnostics.length===0,has_more:!!response.has_more,
    query,results,diagnostics,scope:'Historical subjective vents only; no user-profile or state updates.'};
}
export async function main(argv=process.argv.slice(2)) {
  if (argv.length===1 && argv[0]==='--help') return {usage:
    'vent_journal.js write --ids-file IDS --payload-file JSON --receipt-file RECEIPT [--dry-run] | recall --ids-file IDS [--query TEXT] [--limit 1..10]'};
  const [action,...rest] = argv;
  if (!['write','recall'].includes(action)) throw Error('Expected write or recall (or --help)');
  const options = {};
  const flags = new Set(action==='write' ? ['--ids-file','--payload-file','--receipt-file'] : ['--ids-file','--query','--limit']);
  for (let i=0;i<rest.length;i++) {
    const flag = rest[i];
    if (action==='write' && flag==='--dry-run') { options.dryRun=true; continue; }
    if (!flags.has(flag) || options[flag]!==undefined || !rest[i+1] || rest[i+1].startsWith('--')) throw Error('Invalid argument: '+flag);
    options[flag]=rest[++i];
  }
  if (!options['--ids-file']) throw Error('Missing --ids-file');
  const ids = loadIds(options['--ids-file']);
  if (action==='recall') return recallVents({ids,query:options['--query'] || '',limit:Number(options['--limit'] ?? 5)});
  if (!options['--payload-file']) throw Error('Missing --payload-file');
  const input = JSON.parse(fs.readFileSync(options['--payload-file'],'utf8'));
  if (options.dryRun) return {ok:true,dry_run:true,writes:0,properties:buildVent(input)};
  return writeVent({input,ids,receiptFile:options['--receipt-file']});
}
if (process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  main().then(value=>console.log(JSON.stringify(value,null,2))).catch(error=>{console.error(error.message);process.exitCode=1;});
}
