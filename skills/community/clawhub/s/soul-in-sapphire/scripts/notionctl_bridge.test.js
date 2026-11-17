import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

test('validation errors do not masquerade as auth failures and known tokens stay redacted', () => {
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'sis-error-hint-'));
 const mock=path.join(root,'notionctl.mjs'),probe=path.join(root,'probe.mjs');
 const bridge=new URL('./notionctl_bridge.js',import.meta.url).href;
 fs.writeFileSync(mock,"console.log(JSON.stringify({ok:false,error:process.env.SIS_FIXTURE_FAILURE,details:'fixture-secret-value'}));");
 fs.writeFileSync(probe,"import {httpJson} from "+JSON.stringify(bridge)+";try{httpJson('GET','/users/me')}catch(e){console.log(e.message)}");
 for(const code of ['validation_error','unauthorized']){
  const env={...process.env,NOTIONCTL_PATH:mock,NOTION_API_KEY:'fixture-secret-value',SIS_FIXTURE_FAILURE:code};
  delete env.NOTION_TOKEN;delete env.NOTION_API_TOKEN;
  const r=spawnSync(process.execPath,[probe],{encoding:'utf8',env,timeout:5000});
  assert.equal(r.status,0,r.stderr);assert.doesNotMatch(r.stdout,/fixture-secret-value/);
  if(code==='validation_error'){assert.match(r.stdout,/target database/);assert.doesNotMatch(r.stdout,/Configure Notion auth/);}
  else assert.match(r.stdout,/Configure Notion auth/);
 }
});


test('dependency discovery works for unscoped and owner-qualified installed snapshots', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'sis-install-path-'));
  const source = path.join(path.dirname(fileURLToPath(import.meta.url)), 'notionctl_bridge.js');
  const env = { ...process.env };
  for (const name of ['NOTIONCTL_PATH','NOTION_API_KEY','NOTION_TOKEN','NOTION_API_TOKEN']) delete env[name];
  for (const relative of ['skills/soul-in-sapphire', 'skills/@fixture/soul-in-sapphire']) {
    const workspace = path.join(root, relative.includes('@') ? 'scoped' : 'unscoped');
    const installed = path.join(workspace, relative);
    const dependency = path.join(workspace, 'skills/notion-api-automation/scripts');
    fs.mkdirSync(path.join(installed, 'scripts'), { recursive:true });
    fs.mkdirSync(dependency, { recursive:true });
    fs.writeFileSync(path.join(installed, 'package.json'), '{"type":"module"}');
    fs.copyFileSync(source, path.join(installed, 'scripts/notionctl_bridge.js'));
    fs.writeFileSync(path.join(dependency, 'notionctl.mjs'), 'console.log(JSON.stringify({ok:true,result:{fixture:true}}));');
    fs.writeFileSync(path.join(installed, 'probe.mjs'), "import {httpJson} from './scripts/notionctl_bridge.js'; console.log(JSON.stringify(httpJson('GET','/users/me')));");
    const result = spawnSync(process.execPath, [path.join(installed, 'probe.mjs')], { env, encoding:'utf8', timeout:5000 });
    assert.equal(result.status, 0, result.stderr);
    assert.deepEqual(JSON.parse(result.stdout), {fixture:true});
  }
});

test('calls outside the documented Notion scope are refused before notionctl starts', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'sis-api-scope-'));
  const mock = path.join(root, 'notionctl.mjs');
  const probe = path.join(root, 'probe.mjs');
  const calls = path.join(root, 'calls.log');
  const bridge = new URL('./notionctl_bridge.js', import.meta.url).href;
  fs.writeFileSync(mock, `import fs from 'node:fs';
const arg = name => process.argv[process.argv.indexOf(name) + 1];
fs.appendFileSync(${JSON.stringify(calls)}, arg('--method') + ' ' + arg('--path') + '\\n');
console.log(JSON.stringify({ok:true,result:{}}));`);
  fs.writeFileSync(probe, `import {httpJson} from ${JSON.stringify(bridge)};
const attempts = JSON.parse(process.argv[2]);
console.log(JSON.stringify(attempts.map(([method, apiPath, body]) => {
  try { httpJson(method, apiPath, body); return 'ok'; } catch (error) { return error.message; }
})));`);
  const id = '0123456789abcdef0123456789abcdef';
  const allowed = [
    ['GET', '/users/me'], ['GET', `/blocks/${id}/children?page_size=100`], ['POST', '/databases', {}],
    ['GET', `/databases/${id}`], ['GET', `/data_sources/${id}`], ['PATCH', `/data_sources/${id}`, {properties:{}}],
    ['POST', `/data_sources/${id}/query`, {}], ['POST', '/pages', {}], ['GET', `/pages/${id}`],
    ['PATCH', `/pages/${id}`, {properties:{}}],
  ];
  const refused = [
    ['DELETE', `/blocks/${id}`], ['POST', '/search', {}], ['GET', '/users'], ['POST', '/comments', {}],
    ['PATCH', `/blocks/${id}`, {}], ['PATCH', `/blocks/${id}/children`, {}], ['GET', `/pages/${id}/properties/title`],
    ['PATCH', `/pages/${id}`, {archived:true}], ['PATCH', `/pages/${id}`, {properties:{}, in_trash:true}],
    ['PATCH', `/databases/${id}`, {}],
  ];
  const env = { ...process.env, NOTIONCTL_PATH: mock };
  const result = spawnSync(process.execPath, [probe, JSON.stringify([...allowed, ...refused])], { env, encoding:'utf8', timeout:20000 });
  assert.equal(result.status, 0, result.stderr);
  const outcomes = JSON.parse(result.stdout);
  assert.deepEqual(outcomes.slice(0, allowed.length), allowed.map(() => 'ok'));
  for (const message of outcomes.slice(allowed.length)) assert.match(message, /outside this skill's scope/);
  const started = fs.readFileSync(calls, 'utf8').trim().split('\n');
  assert.equal(started.length, allowed.length);
  assert.ok(started.every(line => line.startsWith('GET /v1/') || line.startsWith('POST /v1/') || line.startsWith('PATCH /v1/')));
});
