import {centeredState,finiteNumber} from './emotion_math.js';
import {readText,richText,atomicJson} from './soul_io.js';
export function planScaleMigration(rows){
 const operations=[];
 for(const lane of ['state','emotions'])for(const page of rows[lane]||[]){
  const p=page.properties;
  if(lane==='state'){
   const raw=JSON.parse(readText(p.state_json));
   if(raw.__meta?.version===2)continue;
   if(raw.__meta?.version!==undefined&&raw.__meta.version!==1)throw Error('Unknown state version: '+page.id);
   const converted=centeredState(raw);
   operations.push({id:page.id,lane,before:{state_json:richText(readText(p.state_json))},after:{state_json:richText(JSON.stringify(converted))}});
  }else{
   const version=p.scale_version?.number;
   if(version===2)continue;
   if(version!==undefined&&version!==null&&version!==1)throw Error('Unknown emotion version: '+page.id);
   const old=p.level?.number,n=finiteNumber(old);
   if(n!==null&&(n<0||n>10))throw Error('Out-of-range legacy emotion: '+page.id);
   const before={level:{number:old??null},scale_version:{number:version??null}};
   const after={level:{number:n===null?null:n-5},scale_version:{number:2}};
   const axis=p.axis?.select?.name,name=readText(p.Name);
   if(n!==null&&axis&&name===axis+'='+n){
    before.Name={title:[{type:'text',text:{content:name}}]};
    after.Name={title:[{type:'text',text:{content:axis+'='+(n-5)}}]};
   }
   operations.push({id:page.id,lane,before,after});
  }
 }
 return {version:1,kind:'soul-centered-scale',operations};
}
export function propertyMatches(page,patch){
 for(const [name,value] of Object.entries(patch)){
  const prop=page.properties?.[name];
  if(value.rich_text||value.title){if(readText(prop)!==(value.rich_text||value.title).map(x=>x.text.content).join(''))return false;}
  else if('number' in value){if((prop?.number??null)!==value.number)return false;}
  else throw Error('Unsupported migration property');
 }
 return true;
}
export async function applyScalePlan(plan,{request,progressFile,direction='forward',onProgress=()=>{}}){
 if(plan.kind!=='soul-centered-scale'||!['forward','rollback'].includes(direction))throw Error('Invalid migration plan/direction');
 const done=[];
 for(const op of plan.operations){
  const from=direction==='forward'?op.before:op.after,to=direction==='forward'?op.after:op.before;
  const live=await request('GET','/v1/pages/'+op.id);
  if(!propertyMatches(live,to)){
   if(!propertyMatches(live,from))throw Error('Concurrent/conflicting modification: '+op.id);
   await request('PATCH','/v1/pages/'+op.id,{properties:to});
   const verified=await request('GET','/v1/pages/'+op.id);
   if(!propertyMatches(verified,to))throw Error('Post-write verification failed: '+op.id);
  }
  done.push(op.id);
  if(progressFile)atomicJson(progressFile,{direction,completed:done.length,total:plan.operations.length,ids:done});
  onProgress(done.length,plan.operations.length);
 }
 return {ok:true,direction,completed:done.length,total:plan.operations.length};
}
