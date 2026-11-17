import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
export const nowIso=()=>new Date().toISOString();
export function atomicJson(file,value){
 fs.mkdirSync(path.dirname(file),{recursive:true,mode:0o700});
 const tmp=file+'.'+crypto.randomUUID()+'.tmp';
 fs.writeFileSync(tmp,JSON.stringify(value,null,2)+'\n',{mode:0o600,flag:'wx'});
 fs.renameSync(tmp,file);
}
export function loadIds(file){return file?JSON.parse(fs.readFileSync(file,'utf8')):{};}
export async function withFileLock(file,work){
 fs.mkdirSync(path.dirname(file),{recursive:true,mode:0o700});
 let fd;
 try{fd=fs.openSync(file,'wx',0o600);}catch(e){
  if(e.code==='EEXIST')throw Error('Writer lock already exists; check its owner before recovery: '+file);
  throw e;
 }
 try{fs.writeFileSync(fd,JSON.stringify({pid:process.pid,created_at:nowIso()}));return await work();}
 finally{fs.closeSync(fd);fs.unlinkSync(file);}
}
export function readText(prop){
 if(prop?.type==='date')return prop.date?.start||'';
 return (prop?.[prop.type]||[]).map(x=>x.plain_text??x.text?.content??'').join('');
}
export const richText=value=>({rich_text:String(value).match(/[\s\S]{1,2000}/gu)?.map(content=>({type:'text',text:{content}}))||[]});
export async function assertTarget(request,lane,id,dsid,required){
 if(!id)throw Error('Missing '+lane+' database ID');
 const db=await request('GET','/v1/databases/'+id);
 const ds=dsid||db.data_sources?.[0]?.id;
 if(!ds||!db.data_sources?.some(x=>x.id===ds))throw Error(lane+' database/data source mismatch');
 const schema=await request('GET','/v1/data_sources/'+ds);
 if(schema.parent?.database_id&&schema.parent.database_id!==id)throw Error(lane+' data source parent mismatch');
 for(const [name,type] of Object.entries(required))if(schema.properties?.[name]?.type!==type)throw Error(lane+' schema missing '+name+' ('+type+')');
 return {dbid:id,dsid:ds,schema};
}
