// Offline test: every request is intercepted by a mocked fetch; nothing is sent to the network.
import test from 'node:test';
import assert from 'node:assert/strict';
import {thetaUrl,pathSegment} from '../../build/security.js';
import {postJson,putJson,deleteEmpty} from '../../build/clients/http.js';
import {onDemandApiClient} from '../../build/clients/ondemandApi.js';
import {thetaVideoClient} from '../../build/clients/thetaVideo.js';
import {edgecloudControllerClient} from '../../build/clients/edgecloudController.js';
import {deployments} from '../../build/commands/deployments.js';
import {redactObject} from '../../build/redaction.js';
import {sanitizeHttpErrorMessage} from '../../build/errors.js';

const cfg={dryRun:false,httpTimeoutMs:1000,httpMaxRetries:3,httpRetryBackoffMs:25,onDemandApiToken:'synthetic-token',edgecloudApiKey:'synthetic-controller',edgecloudProjectId:'test',videoSaId:'test',videoSaSecret:'synthetic-video'};
async function mockFetch(mock,fn){const old=globalThis.fetch;globalThis.fetch=mock;try{return await fn();}finally{globalThis.fetch=old;}}
const json=(body)=>new Response(JSON.stringify(body),{status:200,headers:{'content-type':'application/json'}});

test('rejects malicious origins, credentials, ports and URL suffix tricks',()=>{
  for(const url of ['http://ondemand.thetaedgecloud.com','https://127.0.0.1','https://ondemand.thetaedgecloud.com.attacker.invalid','https://evilthetaedgecloud.com','https://u:p@ondemand.thetaedgecloud.com','https://ondemand.thetaedgecloud.com:8443','https://ondemand.thetaedgecloud.com/path','https://ondemand.thetaedgecloud.com/?token=x','https://ondemand.thetaedgecloud.com/#x']){
    assert.throws(()=>thetaUrl(url,'ondemand'));
  }
  assert.equal(thetaUrl('https://node.thetaedgecloud.com','dedicated'),'https://node.thetaedgecloud.com');
  assert.throws(()=>thetaUrl('https://thetaedgecloud.com.attacker.invalid','dedicated'));
});
test('rejects arbitrary on-demand override before any fetch',async()=>{
  await mockFetch(()=>{assert.fail('must not send credential');},async()=>{
    await assert.rejects(async()=>onDemandApiClient.createInferRequest({...cfg,onDemandApiBaseUrl:'https://attacker.invalid'},'whisper',{}));
  });
});
test('resource IDs cannot inject paths, queries or dot segments',()=>{
  for(const id of ['', '.', '..', '\n', 'x\u0000y']) assert.throws(()=>pathSegment(id,'id'));
  assert.equal(pathSegment('x/../y?z=1#q','id'),'x%2F..%2Fy%3Fz%3D1%23q');
});
for(const method of ['POST','PUT','DELETE']) test(`${method} never retries and refuses redirects`,async()=>{
  let calls=0;
  await mockFetch(async(_url,opts)=>{calls++;assert.equal(opts.redirect,'error');return new Response('unavailable',{status:503});},async()=>{
    const opts={maxRetries:6};
    await assert.rejects(()=>method==='POST'?postJson('https://controller.thetaedgecloud.com/test',{},opts):method==='PUT'?putJson('https://controller.thetaedgecloud.com/test',{},opts):deleteEmpty('https://controller.thetaedgecloud.com/test',opts));
  });
  assert.equal(calls,1);
});
test('on-demand billable POST never retries even capacity rejection',async()=>{
  let calls=0;
  await mockFetch(async(_url,opts)=>{calls++;assert.equal(opts.redirect,'error');return new Response('No instances available',{status:409});},async()=>{
    await assert.rejects(()=>onDemandApiClient.createInferRequest(cfg,'whisper',{}));
  });
  assert.equal(calls,1);
});
test('Video IDs are encoded and query values cannot inject parameters',async()=>{
  await mockFetch(async(url,opts)=>{assert.equal(opts.redirect,'error');assert.equal(String(url),'https://api.thetavideoapi.com/video/a%2Fb%3Fx%3D1');return json({});},()=>thetaVideoClient.getVideo(cfg,'a/b?x=1'));
});
test('multipart controller refuses redirects and redacts error credentials',async()=>{
  await mockFetch(async(_url,opts)=>{assert.equal(opts.redirect,'error');return new Response('{"auth_password":"synthetic-hidden-value"}',{status:400});},async()=>{
    await assert.rejects(()=>edgecloudControllerClient.createChatbotDocument(cfg,'bot','test',{filename:'x.txt',content:'test'},undefined,true),err=>!String(err.message).includes('synthetic-hidden-value'));
  });
});
test('redacts nested keys and named environment secrets without revealing fragments',()=>{
  const value=redactObject({api_key:'abcdef',auth_password:'passwordvalue',env_vars:[{name:'API_TOKEN',value:'synthetic-hidden-value'}],nested:{private_key:'keyvalue'}});
  assert.equal(value.api_key,'[redacted]');assert.equal(value.auth_password,'[redacted]');assert.equal(value.env_vars[0].value,'[redacted]');assert.equal(value.nested.private_key,'[redacted]');
});
test('JSON error redaction handles punctuation and nested auth keys',()=>{
  const result=sanitizeHttpErrorMessage('{"auth_password":"synthetic-hidden-value","nested":{"x-tva-sa-secret":"synthetic-hidden-value"}}');
  assert.equal(result.includes('synthetic-hidden-value'),false);
});
test('redaction rejects prototype keys and tolerates cycles',()=>{
  const obj=JSON.parse('{"__proto__":{"polluted":true},"constructor":"x","safe":1}');obj.self=obj;
  const out=redactObject(obj);assert.equal(Object.hasOwn(out,'__proto__'),false);assert.equal(out.self,'[circular]');assert.equal({}.polluted,undefined);
});
test('disposable validation fails closed with no returned cleanup handles',async()=>{
  await mockFetch(async(url,opts)=>opts.method==='POST'?json({}):json({body:{deployments:[]}}),async()=>{
    const result=await deployments.validateDisposable(cfg,{payload:{},confirm:true});
    assert.equal(result.ok,false);assert.equal(result.deleteResult.ok,false);assert.equal(result.cleanupVerification.checked,false);assert.equal(result.cleanupVerification.deletedHandlesAbsent,false);assert.match(result.operationFailure,/endpoint/);
  });
});
test('disposable cleanup handles shard zero and reports deletion despite probe failure',async()=>{
  let deleted=false;
  await mockFetch(async(_url,opts)=>{
    if(opts.method==='POST')return json({body:{base_id:'base-1',shard:0,suffix:'suffix-1'}});
    if(opts.method==='DELETE'){deleted=true;return new Response(null,{status:204});}
    return json({body:{deployments:[]}});
  },async()=>{
    const result=await deployments.validateDisposable(cfg,{payload:{},confirm:true});
    assert.equal(deleted,true);assert.equal(result.deleteResult.ok,true);assert.equal(result.cleanupVerification.deletedHandlesAbsent,true);assert.equal(result.ok,false);
  });
});
test('unknown list shape never proves cleanup',async()=>{
  await mockFetch(async(_url,opts)=>opts.method==='POST'?json({body:{base_id:'base-1',shard:1,suffix:'suffix-1'}}):opts.method==='DELETE'?new Response(null,{status:204}):json({unexpected:[]}),async()=>{
    const result=await deployments.validateDisposable(cfg,{payload:{},confirm:true});assert.equal(result.ok,false);assert.equal(result.cleanupVerification.checked,false);assert.equal(result.cleanupVerification.deletedHandlesAbsent,false);
  });
});
test('unrecognized deployment-list row never proves cleanup',async()=>{
  await mockFetch(async(_url,opts)=>opts.method==='POST'?json({body:{base_id:'base-1',shard:1,suffix:'suffix-1'}}):opts.method==='DELETE'?new Response(null,{status:204}):json({body:{deployments:[{unknown_id:'suffix-1'}]}}),async()=>{
    const result=await deployments.validateDisposable(cfg,{payload:{},confirm:true});assert.equal(result.ok,false);assert.equal(result.cleanupVerification.checked,false);assert.equal(result.cleanupVerification.deletedHandlesAbsent,false);
  });
});
for(const stream of [
  'data: {"choices":[{"delta":{"content":"partial"}}]}\n',
  'data: {broken json}\ndata: [DONE]\n',
  'data: [DONE]\n'
]) test(`invalid event stream is not accepted: ${stream.slice(0,25)}`,async()=>{
  let calls=0;
  await mockFetch(async()=>{calls++;return new Response(stream,{headers:{'content-type':'text/event-stream'}});},async()=>{
    await assert.rejects(()=>onDemandApiClient.createInferRequest(cfg,'qwen3',{messages:[{role:'user',content:'test'}],stream:true}));
  });
  assert.equal(calls,1);
});
