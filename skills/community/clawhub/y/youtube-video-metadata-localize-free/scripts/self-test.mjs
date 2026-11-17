#!/usr/bin/env node
import {mkdtemp,readFile,writeFile,rm} from 'node:fs/promises';
import {tmpdir} from 'node:os';
import {join} from 'node:path';
import {spawnSync} from 'node:child_process';
const temp=await mkdtemp(join(tmpdir(),'youtube-localize-'));
const run=async(input,translations,name)=>{
 const output=join(temp,name+'.json');
 const r=spawnSync(process.execPath,['scripts/compose-draft.mjs','--input',input,'--translations',translations,'--output',output],{encoding:'utf8'});
 if(r.status!==0)throw new Error(r.stderr);
 return JSON.parse(await readFile(output,'utf8'));
};
try{
 const a=await run('fixtures/new-input-beginner.json','fixtures/agent-translations-beginner.json','beginner');
 const b=await run('fixtures/new-input-experienced.json','fixtures/agent-translations-experienced.json','experienced');
 if(a.chinese_draft.title===b.chinese_draft.title||a.audience_adaptation===b.audience_adaptation)throw new Error('audience expression differentiation missing');
 if(JSON.stringify(a.original)!==JSON.stringify(b.original))throw new Error('audience variants changed original facts');
 for(const p of a.chinese_draft.description_points)if(!p.source_url||!p.original||!p.source_field)throw new Error('point provenance absent');
 const f=await run('fixtures/new-input-failure.json','fixtures/agent-translations-failure.json','hidden');
 if(f.chinese_draft.description||f.chinese_draft.description_points.length||!f.missing_items.some(x=>x.includes('简介不可见')))throw new Error('unseen description invented');
 if(!f.missing_items.some(x=>x.includes('TrailPack X')&&x.includes('title')))throw new Error('title-only unconfirmed brand was not retained from visible title');
 const original=JSON.parse(await readFile('fixtures/agent-translations-beginner.json','utf8'));
 for(const mutate of [x=>x.points.pop(),x=>x.points[0].original='unprovided',x=>x.points[0].source_url='https://example.org/other',x=>x.chinese_audience='other']){
  const tr=structuredClone(original);mutate(tr);const path=join(temp,'bad.json');await writeFile(path,JSON.stringify(tr));
  const r=spawnSync(process.execPath,['scripts/compose-draft.mjs','--input','fixtures/new-input-beginner.json','--translations',path,'--output',join(temp,'bad-output.json')],{encoding:'utf8'});
  if(r.status===0)throw new Error('invalid translation contract accepted');
 }
 await run('fixtures/success-page.json','fixtures/success-translations.json','oldsuccess');
 const oldFailure=await run('fixtures/failure-page.json','fixtures/failure-translations.json','oldfailure');
 if(JSON.stringify(oldFailure).includes('30% faster'))throw new Error('failure translation invents an unseen performance claim');
 if(!oldFailure.missing_items.some(x=>x.includes('GlowBake')&&x.includes('title')))throw new Error('failure fixture does not report GlowBake as an unresolved title term');
 for(const changed of ['厨房灯：体验评测','Glow Bake：厨房灯体验评测']){
  const tr=JSON.parse(await readFile('fixtures/failure-translations.json','utf8'));
  tr.title.chinese=changed;
  const path=join(temp,'changed-glowbake.json');await writeFile(path,JSON.stringify(tr));
  const r=spawnSync(process.execPath,['scripts/compose-draft.mjs','--input','fixtures/failure-page.json','--translations',path,'--output',join(temp,'changed-glowbake-output.json')],{encoding:'utf8'});
  if(r.status===0)throw new Error(`changed or removed unresolved title term accepted: ${changed}`);
 }
 const hidden=JSON.parse(await readFile('fixtures/failure-page.json','utf8'));
 hidden.unresolved_terms=[{term:'claims up to 30% faster',source_field:'description_points[0]'}];
 const hiddenPath=join(temp,'unseen-claim.json');await writeFile(hiddenPath,JSON.stringify(hidden));
 const rejected=spawnSync(process.execPath,['scripts/compose-draft.mjs','--input',hiddenPath,'--translations','fixtures/failure-translations.json','--output',join(temp,'unseen-claim-output.json')],{encoding:'utf8'});
 if(rejected.status===0)throw new Error('unresolved term without visible source accepted');
 const badTitle=JSON.parse(await readFile('fixtures/new-input-failure.json','utf8'));
 badTitle.unresolved_terms=[{term:'Unseen Brand',source_field:'title'}];
 const badTitlePath=join(temp,'unseen-title.json');await writeFile(badTitlePath,JSON.stringify(badTitle));
 const rejectedTitle=spawnSync(process.execPath,['scripts/compose-draft.mjs','--input',badTitlePath,'--translations','fixtures/agent-translations-failure.json','--output',join(temp,'unseen-title-output.json')],{encoding:'utf8'});
 if(rejectedTitle.status===0)throw new Error('title term absent from visible title accepted');
 const visible=JSON.parse(await readFile('fixtures/success-page.json','utf8'));
 visible.unresolved_terms=[{term:'hot-water dough',source_field:'description_points[0]'}];
 const visiblePath=join(temp,'visible-claim.json');await writeFile(visiblePath,JSON.stringify(visible));
 const visibleTr=JSON.parse(await readFile('fixtures/success-translations.json','utf8'));
 visibleTr.points[0].chinese+='（hot-water dough）';
 const visibleTranslationsPath=join(temp,'visible-claim-translations.json');await writeFile(visibleTranslationsPath,JSON.stringify(visibleTr));
 const visibleOut=await run(visiblePath,visibleTranslationsPath,'visible-claim');
 if(!visibleOut.missing_items.some(x=>x.includes('hot-water dough')))throw new Error('visible unresolved term was not retained as a missing item');
 const dropped=structuredClone(visibleTr);dropped.points[0].chinese='用热水面团做出有层次的葱油饼。';
 const droppedPath=join(temp,'dropped-visible-term.json');await writeFile(droppedPath,JSON.stringify(dropped));
 const rejectedDropped=spawnSync(process.execPath,['scripts/compose-draft.mjs','--input',visiblePath,'--translations',droppedPath,'--output',join(temp,'dropped-visible-term-output.json')],{encoding:'utf8'});
 if(rejectedDropped.status===0)throw new Error('unresolved description term removed from Chinese point was accepted');
 console.log('PASS: assembly of independent agent translations, two audiences, per-item provenance, invisible-description stop, exact retention of unresolved terms in corresponding Chinese fields, and invalid-contract rejection. Translation quality is reviewed by Agent; no online run claimed.');
}finally{await rm(temp,{recursive:true,force:true});}
