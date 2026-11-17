// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import {executeThetaRuntimeCommand as run} from '../../dist/index.js';
import {characterRoutes} from '../../build/commands/characters.js';

for(const [name,route]of Object.entries(characterRoutes))test(`Characters ${name}: fixed route, auth and dry-run`,async()=>{
 const prior=globalThis.fetch;let calls=0;
 const args={command:`theta.characters.${name}`,gameId:'g/id',characterId:'c/id',sessionId:'s/id',payload:{message:'synthetic'}};
 globalThis.fetch=async(url,init)=>{calls++;assert.equal(String(url),'https://ai-chars-api.thetaedgecloud.com'+route.path.replace('{gameId}','g%2Fid').replace('{characterId}','c%2Fid').replace('{sessionId}','s%2Fid'));assert.equal(init.method,route.method);assert.equal(new Headers(init.headers).get('authorization'),'Bearer test-game');return route.method==='DELETE'?new Response(null,{status:204}):new Response('{}');};
 try{
  if(route.method!=='GET'){const r=await run(args,{env:{THETA_DRY_RUN:'1'}});assert.equal(r.dryRun,true);assert.equal(calls,0);}
  await run({...args,confirm:true},{env:{THETA_CHARACTERS_API_KEY:'test-game'}});assert.equal(calls,1);
 }finally{globalThis.fetch=prior;}
});
test('Characters rejects missing game key without on-demand credential fallback',async()=>{
 await assert.rejects(run({command:'theta.characters.list',gameId:'test'},{env:{THETA_ONDEMAND_API_TOKEN:'test'}}),/game-scoped key/);
});
