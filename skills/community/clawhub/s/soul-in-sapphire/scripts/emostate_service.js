import fs from 'node:fs';
import crypto from 'node:crypto';
import {AXES,finiteNumber,initialState,advanceState} from './emotion_math.js';
import {nowIso,atomicJson,assertTarget,readText,richText} from './soul_io.js';
const title=s=>({title:[{type:'text',text:{content:String(s)}}]});
const select=s=>({select:s?{name:String(s)}:null});
const number=s=>({number:finiteNumber(s)});
const relation=id=>({relation:[{id}]});
const multi=xs=>({multi_select:(xs||[]).filter(Boolean).map(name=>({name}))});
const canonical=value=>JSON.stringify(value,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))):v);
export function payloadHash(payload,ids){return crypto.createHash('sha256').update(canonical({payload,ids})).digest('hex');}
export async function writeTick(payload,ids,{request,receiptFile,mirrorFile}={}){
 if(!payload||typeof payload!=='object'||Array.isArray(payload))throw Error('Expected a payload object');
 if(payload.scale_version!==2)throw Error('Specify scale_version:2; emotion level uses -5..5, neutral 0');
 for(const field of ['event','state'])if(field in payload&&(!payload[field]||typeof payload[field]!=='object'||Array.isArray(payload[field])))throw Error(field+' must be an object');
 const event=payload.event||{},emotions=payload.emotions||[],st=payload.state||{};
 if(!Array.isArray(emotions)||typeof event!=='object'||typeof st!=='object')throw Error('Invalid event/emotions/state shape');
 if(![event.title,event.context,event.trigger,st.title,st.reason,st.mood_label,...emotions.map(e=>e?.comment)].some(v=>typeof v==='string'&&v.trim()))throw Error('Meaningless payload');
 for(const e of emotions){
  if(!e||!AXES.includes(e.axis))throw Error('Unsupported emotion axis');
  if(e.level!==undefined&&e.level!==null&&(typeof e.level!=='number'||!Number.isFinite(e.level)))throw Error('Emotion level must be a finite number or null');
  const n=finiteNumber(e.level);
  if(n!==null&&(n<-5||n>5))throw Error('Emotion level must be -5..5');
 }
 for(const item of [...emotions,st])for(const field of ['body_signal','avoid'])if(field in item&&(!Array.isArray(item[field])||item[field].some(x=>typeof x!=='string')))throw Error(field+' must be an array of strings');
 // Validate every select option before any API or receipt mutation. Do not rewrite text:
 // a replacement character can silently change meaning or collide with another option.
 for(const [item,fields] of [[event,['importance','trigger','source']],[st,['source','mood_label','intent','need_stack']],...emotions.map(e=>[e,['axis','need','coping']])]){
  for(const field of fields){const value=item[field];if(value===undefined||value===null||value==='')continue;
   if((typeof value!=='string'&&typeof value!=='number')||String(value).includes(',')||!String(value).trim()||String(value).length>100)throw Error('Invalid Notion select '+field+': use a nonempty option without ASCII commas (max 100 characters); keep full wording in context, comment, or reason');
  }
 }
 for(const [item,field] of [[st,'avoid'],...emotions.map(e=>[e,'body_signal'])])for(const value of item[field]||[]){
  if(!value.trim()||value.includes(',')||value.length>100)throw Error('Invalid Notion multi_select '+field+': each option must be nonempty, without ASCII commas (max 100 characters); keep full wording in context, comment, or reason');
 }
 for(const [item,fields] of [[event,['control','uncertainty']],[st,['need_level']],...emotions.map(e=>[e,['weight']])]){
  for(const field of fields)if(item[field]!==undefined&&item[field]!==null&&finiteNumber(item[field])===null)throw Error('Invalid numeric field: '+field);
 }
 if(event.when&&!/T.*(?:Z|[+-]\d{2}:\d{2})$/.test(event.when))throw Error('event.when must include a time and explicit timezone');
 if(!receiptFile)throw Error('A durable --receipt-file is required for safe retries');
 const hash=payloadHash(payload,ids);
 let r=fs.existsSync(receiptFile)?JSON.parse(fs.readFileSync(receiptFile,'utf8')):null;
 if(r&&r.hash!==hash)throw Error('Receipt belongs to a different payload/target');
 if(r?.pending)throw Error('Ambiguous prior write ('+r.pending+'); reconcile the saved receipt before retry, never repeat blindly');
 const save=()=>atomicJson(receiptFile,r);
 const mirror=()=>{
  if(!mirrorFile)return;
  let old={};try{old=JSON.parse(fs.readFileSync(mirrorFile,'utf8'));}catch{}
  if(Date.parse(old.updated_at)>Date.parse(r.when))return; // A historical retry must not roll the live mirror back.
  atomicJson(mirrorFile,{...old,mood:st.mood_label||'quiet',intent:st.intent||'',stress:r.state_json.stress,
   updated_at:r.when,source:st.source||event.source||'soul:tick',note:st.reason||event.context||'',
   event_id:r.event?.id||null,state_id:r.complete?r.state?.id||null:null,durable:r.complete===true,
   scale_version:2,state_json:r.state_json,state_when:r.when});
 };
 if(r?.complete){mirror();return {ok:true,...r,replayed:true};}
 let stage='preflight';
 try{
  const ev=await assertTarget(request,'events',ids.events.database_id,ids.events.data_source_id,{Name:'title',when:'date',context:'rich_text'});
  const em=await assertTarget(request,'emotions',ids.emotions.database_id,ids.emotions.data_source_id,{axis:'select',level:'number',scale_version:'number',event:'relation'});
  const ss=await assertTarget(request,'state',ids.state.database_id,ids.state.data_source_id,{state_json:'rich_text',when:'date',event:'relation'});
  for(const target of [em,ss]){
   const relation=target.schema.properties.event.relation;
   if(relation?.data_source_id!==ev.dsid)throw Error('event relation targets another data source');
  }
  if(!r){
   const when=event.when||nowIso();
   if(!Number.isFinite(Date.parse(when)))throw Error('Invalid event.when');
   // Read/compute before the first mutation; fix historical writes separately.
   const q=await request('POST','/v1/data_sources/'+ss.dsid+'/query',{page_size:1,sorts:[{property:'when',direction:'descending'}]});
   const base=q.results?.[0];
   const baseJson=base?JSON.parse(readText(base.properties.state_json)):initialState();
   const baseWhen=base?readText(base.properties.when)||base.properties.when?.date?.start:null;
   const stateJson=advanceState(baseJson,baseWhen,when,emotions,{...event,when});
   r={version:1,hash,when,base_id:base?.id||null,state_json:stateJson,event:null,emotions:[],state:null,complete:false,pending:null};
   save();
  }
  const post=async(label,dbid,props)=>{
   stage=label;r.pending=label;save();
   try{
    const page=await request('POST','/v1/pages',{parent:{database_id:dbid},properties:props});
    if(!page?.id)throw Error('Write returned no page ID; receipt requires reconciliation');
    return page;
   }catch(err){
    // Validation/auth rejection means no page was accepted. Transport failures remain ambiguous.
    if(/validation_error|unauthorized|object_not_found|restricted_resource/.test(String(err.message))){r.pending=null;save();}
    throw err;
   }
  };
  if(!r.event){
   const page=await post('event',ev.dbid,{Name:title(event.title||'(event)'),when:{date:{start:r.when}},
    importance:select(event.importance),trigger:select(event.trigger),context:richText(event.context||''),
    source:select(event.source||'other'),link:{url:event.link||null},uncertainty:number(event.uncertainty),control:number(event.control)});
   r.event={id:page.id,url:page.url};r.pending=null;save();
  }
  for(let i=r.emotions.length;i<emotions.length;i++){
   const e=emotions[i],page=await post('emotion:'+i,em.dbid,{Name:title(e.title||e.axis+'='+e.level),axis:select(e.axis),
    level:number(e.level),scale_version:{number:2},comment:richText(e.comment||''),weight:number(e.weight),body_signal:multi(e.body_signal),
    need:select(e.need),coping:select(e.coping),event:relation(r.event.id)});
   r.emotions.push({id:page.id,url:page.url});r.pending=null;save();
  }
  if(!r.state){
   const page=await post('state',ss.dbid,{Name:title(st.title||'state@'+r.when),when:{date:{start:r.when}},
    state_json:richText(JSON.stringify(r.state_json)),reason:richText(st.reason||'event tick'),source:select(st.source||'event'),
    mood_label:select(st.mood_label),intent:select(st.intent),need_stack:select(st.need_stack),need_level:number(st.need_level),
    avoid:multi(st.avoid),event:relation(r.event.id)});
   r.state={id:page.id,url:page.url};r.pending=null;save();
  }
  r.complete=true;save();stage='mirror';mirror();
  return {ok:true,...r};
 }catch(error){
  const details={ok:false,stage,receipt_file:receiptFile,partial:r?{event:r.event,emotions:r.emotions,state:r.state,pending:r.pending}:null};
  if(r&&!r.complete){try{mirror();}catch{details.local_mirror_failed=true;}}
  error.details=details;throw error;
 }
}
