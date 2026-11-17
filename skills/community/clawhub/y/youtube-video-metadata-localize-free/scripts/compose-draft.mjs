#!/usr/bin/env node
// Assemble agent-authored translations, never pretend a glossary is a translator.
import {readFile,writeFile} from 'node:fs/promises';
const args=process.argv.slice(2);
const value=k=>{const i=args.indexOf(k);return i<0?null:args[i+1];};
const input=value('--input'), translated=value('--translations'), output=value('--output');
if(!input||!translated||!output) throw new Error('Usage: node scripts/compose-draft.mjs --input <page.json> --translations <agent-translations.json> --output <draft.json>');
const page=JSON.parse(await readFile(input,'utf8')), tr=JSON.parse(await readFile(translated,'utf8'));
const require=(ok,msg)=>{if(!ok)throw new Error(msg);};
require(/^https?:\/\//.test(page.source_url||''),'source_url must be http(s)');
require(typeof page.title==='string'&&page.title.trim(),'title is required');
require(typeof page.chinese_audience==='string'&&page.chinese_audience.trim(),'chinese_audience is required');
require(Array.isArray(page.description_points),'description_points must be an array');
require(page.description_points.length<=100,'description_points exceeds100; split input');
require(page.unresolved_terms===undefined||Array.isArray(page.unresolved_terms),'unresolved_terms must be an array');
if(page.unresolved_terms?.length){
 for(const item of page.unresolved_terms){
  require(item&&typeof item.term==='string'&&item.term.trim(),'each unresolved term must include its text');
  require(typeof item.source_field==='string'&&item.source_field.trim(),'each unresolved term must include source_field');
  if(item.source_field==='title') require(page.title.includes(item.term),'unresolved title term must occur in the visible title');
  else {
   require(page.description_visible===true,'unresolved description terms require visible supporting material');
   const match=/^description_points\[(\d+)\]$/.exec(item.source_field);
   require(match&&page.description_visible===true&&Number(match[1])<page.description_points.length,'unresolved description term must reference a visible description point');
   require(page.description_points[Number(match[1])].includes(item.term),'unresolved term must occur in its visible source text');
  }
 }
}
require(tr.chinese_audience===page.chinese_audience,'translation audience must exactly match request');
require(typeof tr.audience_adaptation==='string'&&tr.audience_adaptation.trim(),'explain audience wording adaptation');
require(tr.title?.original===page.title&&typeof tr.title?.chinese==='string'&&tr.title.chinese.trim(),'title translation must retain matching original');
require(Array.isArray(tr.points),'points translations must be an array');
const originalPoints=page.description_visible===true?page.description_points:[];
require(tr.points.length===originalPoints.length,'each visible point must have exactly one translation; invisible descriptions must have none');
const localized=tr.points.map((p,i)=>{
 require(p.index===i&&p.original===originalPoints[i],'point index/original mismatch');
 require(typeof p.chinese==='string'&&p.chinese.trim(),'Chinese point translation required');
 return {index:i,original:p.original,chinese:p.chinese,source_url:page.source_url,source_field:`description_points[${i}]`};
});
for(const item of page.unresolved_terms||[]){
 if(item.source_field==='title') require(tr.title.chinese.includes(item.term),`unresolved title term "${item.term}" must be preserved verbatim in the Chinese title`);
 else {
  const match=/^description_points\[(\d+)\]$/.exec(item.source_field);
  const index=Number(match[1]);
  require(localized[index].chinese.includes(item.term),`unresolved term "${item.term}" must be preserved verbatim in its Chinese description point`);
 }
}
const missing=[];
if(page.description_visible!==true)missing.push('简介不可见：未推断或补写简介内容。');
if(Array.isArray(page.unresolved_terms)&&page.unresolved_terms.length)missing.push(`待确认术语/主张：${page.unresolved_terms.map(x=>`${x.term}（来源：${x.source_field}）`).join('、')}；保留原词，不升级为已核实事实。`);
require(tr.title.source_url===page.source_url&&tr.title.source_field==='title','title source attribution mismatch');
for(const p of tr.points) require(p.source_url===page.source_url&&p.source_field===`description_points[${p.index}]`,'point source attribution mismatch');
const result={kind:'youtube-video-metadata-localization-draft',translation_method:'agent-authored; script validates and assembles only',collection_scope:page.fixture_notice||page.collection_scope||'Provided visible-page extract; online access not established by assembler',chinese_audience:page.chinese_audience,audience_adaptation:tr.audience_adaptation,original:{title:page.title,description_points:originalPoints},chinese_draft:{title:tr.title.chinese,description:localized.map(p=>p.chinese).join('\n'),title_source:{original:page.title,url:page.source_url,field:'title'},description_points:localized},sources:[{url:page.source_url,field:'title',original:page.title},...localized.map(p=>({url:p.source_url,field:p.source_field,original:p.original}))],missing_items:missing,no_backend_changes:true};
await writeFile(output,JSON.stringify(result,null,2)+'\n');
