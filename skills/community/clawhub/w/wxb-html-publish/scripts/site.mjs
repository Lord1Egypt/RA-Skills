// 保留页面功能与目录布局，只转换资源路径；不执行页面代码。
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {digest,upload,safeURL,timeout} from './publish.mjs';
import {htmlPaths,cssPaths} from './paths.mjs';
const MIME={'.html':'text/html','.htm':'text/html','.css':'text/css','.js':'application/javascript','.mjs':'application/javascript','.json':'application/json','.svg':'image/svg+xml','.woff':'font/woff','.woff2':'font/woff2','.ttf':'font/ttf','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.gif':'image/gif','.webp':'image/webp','.ico':'image/x-icon','.mp4':'video/mp4','.pdf':'application/pdf'};
const mime=f=>MIME[path.extname(f).toLowerCase()]||'application/octet-stream';
const inside=(root,file)=>{const r=path.relative(root,file);return r!=='..'&&!r.startsWith(`..${path.sep}`)&&!path.isAbsolute(r);};
function regular(root,file){
 if(!inside(root,file))throw Error(`资源超出站点根目录：${file}`);
 let p=root;if(fs.lstatSync(p).isSymbolicLink())throw Error('拒绝符号链接根目录');
 for(const part of path.relative(root,file).split(path.sep).filter(Boolean)){p=path.join(p,part);if(fs.lstatSync(p).isSymbolicLink())throw Error(`符号链接须单独确认：${p}`);}
 if(!fs.statSync(file).isFile())throw Error(`不是普通文件：${file}`);
}
export function prepare(entry,siteRoot,output){
 const root=path.resolve(siteRoot);entry=path.resolve(entry);regular(root,entry);
 output=path.resolve(output);if(fs.existsSync(output))throw Error('输出目录已存在，不覆盖');
 if(inside(root,output))throw Error('发布副本目录必须放在源站点之外');
 const collected=new Map(),changes=[],warnings=[];
 const target=file=>path.relative(root,file).split(path.sep).join('/');
 function reference(raw,owner){
  const value=raw.replace(/&amp;/g,'&');
  if(!value||value.startsWith('#')||value.startsWith('//')||(/^[a-z][a-z0-9+.-]*:/i.test(value)&&!/^file:/i.test(value)&&!path.isAbsolute(value)))return raw;
  const at=value.search(/[?#]/);const suffix=at<0?'':value.slice(at);let pathname=at<0?value:value.slice(0,at);
  try{pathname=decodeURIComponent(pathname);}catch{throw Error(`路径编码无法解析：${raw}`);}
  let file;
  if(/^file:/i.test(pathname))file=fileURLToPath(pathname);
  else if(path.isAbsolute(pathname)){
   if(inside(root,pathname))file=pathname;
   else if(fs.existsSync(pathname))throw Error(`本机绝对路径位于根外：${raw}`);
   else file=path.join(root,pathname.replace(/^[/\\]+/,''));
  }else file=path.resolve(path.dirname(owner),pathname);
  regular(root,file);collect(file);
  let rel=path.posix.relative(path.posix.dirname(target(owner)),target(file));if(!rel.startsWith('.'))rel='./'+rel;
  rel=rel.split('/').map(s=>s==='..'||s==='.'?s:encodeURIComponent(s)).join('/')+suffix;
  if(rel!==raw)changes.push({from:raw,to:rel});return rel;
 }
 function collect(file){
  if(collected.has(file))return;
  let bytes=fs.readFileSync(file);collected.set(file,null);
  const ext=path.extname(file).toLowerCase();
  if(['.html','.htm','.css'].includes(ext)){
   const text=new TextDecoder('utf-8',{fatal:true}).decode(bytes);
   bytes=Buffer.from(ext==='.css'?cssPaths(text,v=>reference(v,file)):htmlPaths(text,v=>reference(v,file)));
  }
  if(['.html','.htm','.js','.mjs','.css'].includes(ext)){
   const text=bytes.toString('utf8');
   if(text.includes(root)||/file:\/\/|[A-Za-z]:\\/.test(text))warnings.push(`${target(file)}：可能存在脚本、注释或转义语法中的本地路径，请逐处核对；脚本未被自动改写。`);
   if(ext==='.js'||ext==='.mjs')warnings.push(`${target(file)}：JS动态路径保持原文；请核对站点根内资源是否齐全。`);
  }
  collected.set(file,{target:target(file),mime:mime(file),bytes});
 }
 // 用户声明的站点目录作为发布集合，支持运行时动态读取的静态资源。
 function walk(dir){for(const item of fs.readdirSync(dir,{withFileTypes:true})){
  if(item.name.startsWith('.')||['node_modules','credentials','secrets'].includes(item.name)||/\.(?:pem|key|p12|pfx)$/i.test(item.name)){warnings.push(`未自动纳入：${path.relative(root,path.join(dir,item.name))}`);continue;}
  const file=path.join(dir,item.name);if(item.isSymbolicLink())throw Error(`符号链接须单独确认：${file}`);
  if(item.isDirectory())walk(file);else{regular(root,file);collect(file);}
 }}
 collect(entry);walk(root);
 fs.mkdirSync(output);
 const files=[...collected.values()].map(({target,mime,bytes})=>{const dest=path.join(output,...target.split('/'));fs.mkdirSync(path.dirname(dest),{recursive:true});fs.writeFileSync(dest,bytes,{flag:'wx'});return{target,mime,size:bytes.length,sha256:digest(bytes)};});
 return{version:2,entry:target(entry),files,changes,warnings};
}
function validate(manifest,directory){
 const seen=new Set();return manifest.files.map(f=>{
  if(typeof f.target!=='string'||f.target.split('/').some(s=>!s||s==='.'||s==='..')||/[\\\x00]/.test(f.target)||path.isAbsolute(f.target)||seen.has(f.target))throw Error('非法清单路径');seen.add(f.target);
  if(mime(f.target)!==f.mime)throw Error('清单MIME不一致');
  const file=path.resolve(directory,f.target);regular(path.resolve(directory),file);const bytes=fs.readFileSync(file);if(digest(bytes)!==f.sha256)throw Error('审核后文件发生变化');return{...f,bytes};
 });
}
export async function publishSite(directory,manifestFile,approvedHash,receiptFile,fetcher=fetch,clock=Date.now){
 const raw=fs.readFileSync(manifestFile);if(digest(raw)!==approvedHash)throw Error('清单审核哈希不匹配');
 const manifest=JSON.parse(raw),entry=manifest.entry||'index.html',files=validate(manifest,directory);if(!files.some(f=>f.target===entry))throw Error('缺少入口');
 const stamp=String(clock());if(!/^\d{13}$/.test(stamp))throw Error('无效时间戳');const base='/wxb-published/'+stamp;
 const fd=fs.openSync(receiptFile,'wx',0o600),state={base,files:[],status:'in_progress',browser:'not_checked'};
 const save=()=>{fs.ftruncateSync(fd,0);fs.writeSync(fd,JSON.stringify(state,null,2),0,'utf8');fs.fsyncSync(fd);};save();
 try{
  for(const f of files.sort((a,b)=>(a.target===entry)-(b.target===entry))){
   const item={target:f.target,upload:'unknown',verification:'not_checked'};state.files.push(item);save();
   const parent=path.posix.dirname(f.target),group=base+(parent==='.'?'':'/'+parent);
   const result=await upload(f.bytes,fetcher,{group,name:path.posix.basename(f.target),mime:f.mime});item.upload='succeeded';item.url=result.url;save();
   const url=safeURL(result.url),expected='https://s2.wangxiaobao.com'+base+'/'+f.target.split('/').map(encodeURIComponent).join('/');if(url!==expected)throw Error('服务端未保留目录或原名');
   const r=await fetcher(url,{redirect:'manual',signal:timeout(30000)});if(r.status!==200)throw Error('文件访问失败');
   const chunks=[];let size=0;for await(const c of r.body){size+=c.length;if(size>f.bytes.length)throw Error('返回内容大于上传文件');chunks.push(Buffer.from(c));}
   if(digest(Buffer.concat(chunks))!==f.sha256)throw Error('返回内容与上传文件不一致');
   item.contentType=r.headers.get('content-type');item.contentDisposition=r.headers.get('content-disposition');
   item.verification='http_verified';if(/attachment/i.test(item.contentDisposition||'')||(item.contentType||'').split(';')[0].trim().toLowerCase()!==f.mime)item.warning='响应MIME或下载头不同，请检查浏览器实际加载';save();
  }
  state.status='http_verified';state.url=state.files.find(f=>f.target===entry).url;save();return state;
 }catch(e){state.status='partial_or_unknown';state.error=e.message;save();throw e;}finally{fs.closeSync(fd);}
}
if(process.argv[1]&&path.resolve(process.argv[1])===fileURLToPath(import.meta.url)){
 const [cmd,...a]=process.argv.slice(2);
 try{
  if(cmd==='prepare'&&a.length===3){const m=prepare(...a),mf=a[2]+'.manifest.json';fs.writeFileSync(mf,JSON.stringify(m,null,2),{flag:'wx',mode:0o600});console.log(JSON.stringify({directory:a[2],manifest:mf,sha256:digest(fs.readFileSync(mf)),warnings:m.warnings}));}
  else if(cmd==='publish'&&a.length===5&&a[4]==='--allow-public-upload')console.log(JSON.stringify(await publishSite(...a.slice(0,4)),null,2));
  else throw Error('用法：site.mjs prepare <入口HTML> <站点根目录> <新输出目录> | publish <发布目录> <manifest> <审核SHA256> <新回执路径> --allow-public-upload');
 }catch(e){console.error(e.message);process.exitCode=1;}
}
