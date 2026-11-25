// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import {executeThetaRuntimeCommand as run} from '../../dist/index.js';
import {characterRoutes} from '../../build/commands/characters.js';

// Valid synthetic arguments for every route; IDs contain '/' to prove percent-encoding.
const ids={gameId:'g/id',characterId:'c/id',sessionId:'s/id',groupingId:'grp/id',messageId:'m/id',storylineId:'sl/id',dialogId:'d/id'};
const payloads={
  create:{name:'River',speaking_style:{formality:'casual',gesture_frequency:'low',verbosity:'concise'}},
  update:{name:'River'},
  'session.create':{game_id:'g',participants:{npcs:['c'],users:['u']}},
  'session.context':{context:{situation:'x',location:'y',time_of_day:'evening'}},
  'session.message':{type:'chat',from_id:'u',content:'Hello'},
  'grouping.create':{name:'The Lowtown Fire',description:'d',order_index:1},
  'grouping.update':{name:'Renamed'},
  'library.create':{type:'event',content:'Saved 20 villagers.',metadata:{outcome:'saved'}},
  'library.update':{content:'Saved 21 villagers.'},
  'storyline.create':{name:'Aria',npc_id:'char_1',grouping_ids:['grp_a','grp_b']},
  'storyline.update':{grouping_ids:['grp_a']},
  'dialog.create':{name:'Hero',npc_id:'char_1',message_refs:[{grouping_id:'grp_a',message_id:'msg_1'}]}
};
function expectedPath(route){let p=route.path;for(const f of route.fields)p=p.replace(`{${f}}`,encodeURIComponent(ids[f]));return p;}

for(const [name,route]of Object.entries(characterRoutes))test(`Characters ${name}: fixed route, auth, body and dry-run`,async()=>{
  const prior=globalThis.fetch;const calls=[];
  const args={command:`theta.characters.${name}`,...ids,...(payloads[name]?{payload:payloads[name]}:{})};
  globalThis.fetch=async(url,init)=>{calls.push({url:String(url),init});return route.method==='DELETE'?new Response(null,{status:204}):new Response('{}');};
  try{
    if(route.method!=='GET'){
      const r=await run(args,{env:{THETA_DRY_RUN:'1',THETA_CHARACTERS_API_KEY:'test-game'}});assert.equal(r.dryRun,true);assert.equal(calls.length,0);
      await assert.rejects(run(args,{env:{THETA_CHARACTERS_API_KEY:'test-game'}}),/confirm:true/);assert.equal(calls.length,0);
    }
    await run({...args,confirm:true},{env:{THETA_CHARACTERS_API_KEY:'test-game'}});
    assert.equal(calls.length,1);
    const {url,init}=calls[0];
    assert.equal(url,'https://ai-chars-api.thetaedgecloud.com'+expectedPath(route));
    assert.equal(init.method,route.method);assert.equal(init.redirect,'error');
    assert.equal(new Headers(init.headers).get('authorization'),'Bearer test-game');
    if(route.fixedBody)assert.deepEqual(JSON.parse(init.body),route.fixedBody);
    else if(payloads[name])assert.deepEqual(JSON.parse(init.body),payloads[name]);
  }finally{globalThis.fetch=prior;}
});

test('Characters rejects missing game key without on-demand credential fallback',async()=>{
  await assert.rejects(run({command:'theta.characters.list',gameId:'test'},{env:{THETA_ONDEMAND_API_TOKEN:'test'}}),/game-scoped key/);
});
