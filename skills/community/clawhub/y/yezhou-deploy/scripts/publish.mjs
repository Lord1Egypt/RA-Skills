#!/usr/bin/env node

import { chmod, mkdir, readFile, readdir, stat, unlink, writeFile } from "node:fs/promises";
import { homedir, hostname, platform } from "node:os";
import { basename, dirname, join, resolve } from "node:path";
import { spawn } from "node:child_process";

const commandArguments=process.argv.slice(2),positionals=[];let listOnly=false,siteArgument="";
for(let index=0;index<commandArguments.length;index+=1){
  const argument=commandArguments[index];
  if(argument==="--list")listOnly=true;
  else if(argument==="--site"){
    siteArgument=commandArguments[index+1]||"";index+=1;
    if(!siteArgument)fail("--site requires a site ID or public URL.");
  }else if(argument.startsWith("--site=")){
    siteArgument=argument.slice(7);if(!siteArgument)fail("--site requires a site ID or public URL.");
  }
  else if(argument.startsWith("--"))fail(`Unknown option: ${argument}`);
  else positionals.push(argument);
}
const [inputArgument,title=""] = positionals;
if (!inputArgument&&!listOnly) fail("Usage: node publish.mjs <html-file|directory|zip-file> [title] [--site <id|url>]\n       node publish.mjs --list");
if(listOnly&&(inputArgument||siteArgument))fail("--list cannot be combined with an input or --site.");

const inputPath = inputArgument?resolve(inputArgument):"";
let inputStats;
if(inputPath){try { inputStats = await stat(inputPath); }
catch (error) { fail(`Unable to read ${inputPath}: ${error instanceof Error ? error.message : String(error)}`); }}
const inputKind = inputStats?.isDirectory() ? "directory" : /\.zip$/i.test(inputPath) ? "zip" : "html";
const projectDirectory = inputKind === "directory" ? inputPath : dirname(inputPath||resolve("."));
const stateFile = join(projectDirectory,".yezhou.json");
const sourceName = inputKind === "directory" ? "." : basename(inputPath);
const bindingKey = `${inputKind}:${platform()==="win32"?sourceName.toLowerCase():sourceName}`;
const baseUrl = (process.env.YEZHOU_BASE_URL || "https://yz.gbfeng.com").replace(/\/$/, "");
const configRoot = process.env.YEZHOU_CONFIG_DIR || (platform() === "win32"
  ? join(process.env.APPDATA || join(homedir(), "AppData", "Roaming"), "yezhou")
  : join(process.env.XDG_CONFIG_HOME || join(homedir(), ".config"), "yezhou"));
const credentialFile = join(configRoot, "credentials");
const systemName=({darwin:"macOS",win32:"Windows",linux:"Linux"})[platform()]||platform();
const deviceName=Array.from(hostname()).filter(character=>character.charCodeAt(0)>=32&&character.charCodeAt(0)!==127).join("").trim()||"未知设备";
const authorizationLabel=`页舟 Deploy · ${systemName} · ${deviceName}`.slice(0,40);

function fail(message) {
  console.error(message);
  process.exit(1);
}

async function api(path, options = {}) {
  let response;
  try { response = await fetch(`${baseUrl}${path}`, options); }
  catch (error) { fail(`Unable to connect to 页舟: ${error instanceof Error ? error.message : String(error)}`); }
  const body = await response.json().catch(() => ({}));
  return { response, body };
}

function openBrowser(url) {
  const command = platform() === "win32" ? "cmd" : platform() === "darwin" ? "open" : "xdg-open";
  const args = platform() === "win32" ? ["/c", "start", "", url] : [url];
  try {
    const child = spawn(command, args, { detached:true, stdio:"ignore", windowsHide:true });
    child.unref();
    return true;
  } catch { return false; }
}

const sleep = (milliseconds) => new Promise((resolvePromise) => setTimeout(resolvePromise, milliseconds));

async function authorize() {
  const { response, body } = await api("/api/agent/device/code", {
    method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({label:authorizationLabel}),
  });
  if (!response.ok || !body.deviceCode || !body.verificationUriComplete) fail(body.error || "Unable to start browser authorization.");
  console.log(`Authorization code: ${body.userCode}`);
  console.log(`Open this page to authorize 页舟: ${body.verificationUriComplete}`);
  if (!openBrowser(body.verificationUriComplete)) console.log("The browser could not be opened automatically. Open the URL above manually.");
  const interval = Math.max(2, Number(body.interval) || 2) * 1000;
  const deadline = Date.now() + Math.max(60, Number(body.expiresIn) || 600) * 1000;
  while (Date.now() < deadline) {
    const tokenResult = await api("/api/agent/device/token", {
      method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({deviceCode:body.deviceCode}),
    });
    if (tokenResult.response.ok && tokenResult.body.accessToken) {
      await mkdir(configRoot, {recursive:true,mode:0o700});
      await writeFile(credentialFile, `${tokenResult.body.accessToken}\n`, {encoding:"utf8",mode:0o600});
      if (platform() !== "win32") await Promise.all([chmod(configRoot,0o700),chmod(credentialFile,0o600)]);
      console.log("Authorized successfully.");
      return tokenResult.body.accessToken;
    }
    if (tokenResult.body.error !== "authorization_pending") fail(`Authorization failed: ${tokenResult.body.error || "unknown_error"}`);
    await sleep(interval);
  }
  fail("Authorization timed out. Run the publish command again to retry.");
}

async function savedCredential() {
  try { return (await readFile(credentialFile,"utf8")).trim(); }
  catch { return ""; }
}

function siteIdFrom(value){
  const trimmed=value.trim();
  if(/^[a-f0-9]{12}$/i.test(trimmed))return trimmed.toLowerCase();
  try{const match=new URL(trimmed).pathname.match(/^\/p\/([a-f0-9]{12})(?:\/|$)/i);if(match)return match[1].toLowerCase();}catch{/* The value may be an ID rather than a URL. */}
  fail(`Invalid site ID or public URL: ${value}`);
}

async function listSites(accessToken){
  return api("/api/agent/sites",{headers:{Authorization:`Bearer ${accessToken}`}});
}

async function directoryFiles(directory,prefix="") {
  const entries=await readdir(directory,{withFileTypes:true}),files=[];
  for(const entry of entries){
    if(entry.name.startsWith(".")||entry.name==="node_modules")continue;
    const absolute=join(directory,entry.name),relative=prefix?`${prefix}/${entry.name}`:entry.name;
    if(entry.isDirectory())files.push(...await directoryFiles(absolute,relative));
    else if(entry.isFile())files.push({absolute,relative});
  }
  return files;
}

async function projectPayload() {
  const form=new FormData();if(title)form.set("title",title);
  if(inputKind==="zip"){form.set("archive",new Blob([await readFile(inputPath)],{type:"application/zip"}),inputPath.split(/[\\/]/).pop()||"project.zip");return form;}
  const files=await directoryFiles(inputPath);if(!files.length)fail("The project directory is empty.");
  const svgFiles=files.filter(file=>/\.svg$/i.test(file.relative));if(svgFiles.length)fail(`页舟暂不支持 SVG 文件，请转换为 PNG、WebP 或安全的 HTML/CSS 图标：\n${svgFiles.map(file=>`- ${file.relative}`).join("\n")}`);
  for(const file of files)form.append("files",new Blob([await readFile(file.absolute)]),file.relative.split("/").pop());
  form.set("paths",JSON.stringify(files.map(file=>file.relative)));return form;
}

async function publish(accessToken, payload, siteId) {
  const project=inputKind!=="html",basePath=project?"/api/agent/projects":"/api/agent/sites";
  return api(siteId ? `${basePath}/${encodeURIComponent(siteId)}` : basePath, {
    method:siteId ? "PUT" : "POST",
    headers:{Authorization:`Bearer ${accessToken}`,...(project?{}:{"Content-Type":"application/json; charset=utf-8"})},
    body:project?payload:JSON.stringify(payload),
  });
}

let accessToken = await savedCredential();
if (!accessToken) accessToken = await authorize();

if(listOnly){
  let result=await listSites(accessToken);
  if(result.response.status===401){await unlink(credentialFile).catch(()=>{});accessToken=await authorize();result=await listSites(accessToken);}
  if(!result.response.ok||!Array.isArray(result.body.sites))fail(result.body.error||`Unable to list sites (HTTP ${result.response.status}).`);
  if(!result.body.sites.length)console.log("No published sites found for this account.");
  else for(const site of result.body.sites)console.log(`${site.id}\t${site.projectType||"single"}\t${site.title||"未命名页面"}\t${site.url}`);
}else{
  let payload;
  if(inputKind==="html"){
    let html;try{html=await readFile(inputPath,"utf8");}catch(error){fail(`Unable to read ${inputPath}: ${error instanceof Error?error.message:String(error)}`);}
    payload={html,title};
  }else payload=await projectPayload();

  let state = {};
  try { state = JSON.parse(await readFile(stateFile,"utf8")); } catch { /* A first publish has no project state yet. */ }
  const manifest=state&&typeof state==="object"&&!Array.isArray(state)?state:{};
  const bindings=manifest.bindings&&typeof manifest.bindings==="object"&&!Array.isArray(manifest.bindings)?manifest.bindings:{};
  const legacyBinding=typeof manifest.siteId==="string"?{siteId:manifest.siteId,url:manifest.url}:null;
  const savedBinding=bindings[bindingKey],binding=savedBinding&&typeof savedBinding==="object"?savedBinding:legacyBinding||{};
  const selectedSiteId=siteArgument?siteIdFrom(siteArgument):(typeof binding.siteId==="string"?binding.siteId:"");
  let result = await publish(accessToken,payload,selectedSiteId);
  if (result.response.status === 401) {
    await unlink(credentialFile).catch(()=>{});
    accessToken = await authorize();
    result = await publish(accessToken,payload,selectedSiteId);
  }
  if (!result.response.ok || !result.body.url || !result.body.id) fail(result.body.error || `Publish failed with HTTP ${result.response.status}.`);
  const nextState={version:2,bindings:{...bindings,[bindingKey]:{source:sourceName,type:inputKind,siteId:result.body.id,url:result.body.url}}};
  await writeFile(stateFile,`${JSON.stringify(nextState,null,2)}\n`,"utf8");
  console.log(`${result.body.created ? "Published" : "Updated"}: ${result.body.url}`);
}
