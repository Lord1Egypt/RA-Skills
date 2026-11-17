import test from 'node:test';
import assert from 'node:assert/strict';
import {planScaleMigration,applyScalePlan,propertyMatches} from './emotion_scale_migration.js';
const rich=s=>({type:'rich_text',rich_text:[{plain_text:s,text:{content:s}}]});
test('migration preserves neutral/zero/null, narratives and imprint severity; already migrated rows skip',async()=>{
 const state={id:'state',properties:{state_json:rich(JSON.stringify({joy:5,stress:0,pain:null,imprints:[{severity:9,notes:'keep'}],__meta:{version:1}})),reason:rich('unchanged')}};
 const emotion={id:'emotion',properties:{level:{number:0}}};
 const unknown={id:'missing',properties:{level:{number:null}}};
 const plan=planScaleMigration({state:[state],emotions:[emotion,unknown]});
 const converted=JSON.parse(plan.operations[0].after.state_json.rich_text[0].text.content);
 assert.equal(converted.joy,0);assert.equal(converted.stress,-5);assert.equal(converted.pain,null);assert.equal(converted.imprints[0].severity,9);
 assert.equal(plan.operations[1].after.level.number,-5);assert.equal(plan.operations[2].after.level.number,null);
 const pages=new Map([state,emotion,unknown].map(p=>[p.id,structuredClone(p)]));let patches=0;
 const request=async(method,p,body)=>{
  const row=pages.get(p.split('/').at(-1));if(method==='PATCH'){
   patches++;for(const [k,v]of Object.entries(body.properties))row.properties[k]=v.rich_text?rich(v.rich_text.map(x=>x.text.content).join('')):v;
  }return structuredClone(row);
 };
 await applyScalePlan(plan,{request});assert.equal(patches,3);
 await applyScalePlan(plan,{request});assert.equal(patches,3);
 assert.equal(planScaleMigration({state:[pages.get('state')],emotions:[pages.get('emotion'),pages.get('missing')]}).operations.length,0);
 assert.equal(pages.get('state').properties.reason.rich_text[0].plain_text,'unchanged');
 await applyScalePlan(plan,{request,direction:'rollback'});
 for(const op of plan.operations)assert.ok(propertyMatches(pages.get(op.id),op.before));
});
test('concurrent edits and unknown versions stop before overwrite',async()=>{
 const row={id:'x',properties:{level:{number:7}}},plan=planScaleMigration({emotions:[row]});
 let writes=0;
 await assert.rejects(applyScalePlan(plan,{request:async(method)=>{if(method==='PATCH')writes++;return {properties:{level:{number:8}}};}}),/Conflicting|conflicting/);
 assert.equal(writes,0);
 assert.throws(()=>planScaleMigration({emotions:[{id:'x',properties:{level:{number:1},scale_version:{number:99}}}]}),/Unknown/);
});


test('only generated numeric titles follow coordinate migration; authored titles stay',()=>{
 const p=(id,name)=>({id,properties:{Name:{type:'title',title:[{plain_text:name}]},axis:{select:{name:'joy'}},level:{number:7}}});
 const plan=planScaleMigration({emotions:[p('a','joy=7'),p('b','A moment of joy')]});
 assert.equal(plan.operations[0].after.Name.title[0].text.content,'joy=2');
 assert.equal('Name' in plan.operations[1].after,false);
});
