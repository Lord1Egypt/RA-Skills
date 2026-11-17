// Offline: every request is intercepted by a mocked fetch or dry-run; nothing is sent to the network.
import assert from 'node:assert/strict';
import test from 'node:test';
import { executeThetaRuntimeCommand as run } from '../../dist/index.js';

test('base ID restart uses documented PUT endpoint and encoded identifiers', async () => {
  const prior=globalThis.fetch;
  globalThis.fetch=async (url,init)=>{assert.equal(String(url),'https://controller.thetaedgecloud.com/deployments/base/base%2Fid/start?project_id=project');assert.equal(init?.method,'PUT');return new Response(null,{status:204});};
  try {await run({command:'theta.deployments.startByBaseId',projectId:'project',baseId:'base/id',confirm:true},{env:{THETA_EC_API_KEY:'test'}});}finally{globalThis.fetch=prior;}
});
