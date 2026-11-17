// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import assert from 'node:assert/strict';
import test from 'node:test';
import { executeThetaRuntimeCommand as run } from '../../dist/index.js';

test('dryrun blocks paid deployment and inference network calls', async () => {
 const prior=globalThis.fetch;globalThis.fetch=async()=>{throw new Error('Dryrun attempted network');};
 try{for(const args of [{command:'theta.deployments.create',projectId:'test',payload:{}},{command:'theta.ondemand.chat',service:'glm_5_3',messages:[{role:'user',content:'test'}]}]){
 const r=await run(args,{env:{THETA_DRY_RUN:'1'}}) as {dryRun:boolean};assert.equal(r.dryRun,true);
 }}finally{globalThis.fetch=prior;}
});
