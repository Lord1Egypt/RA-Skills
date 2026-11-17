// Offline test: every request is intercepted by a mocked fetch; nothing is sent to the network.
import assert from 'node:assert/strict';
import test from 'node:test';
import { executeThetaRuntimeCommand as run } from '../../dist/index.js';

test('video inspection uses service-account auth and fixed Theta host', async () => {
 const prior=globalThis.fetch;globalThis.fetch=async(url,init)=>{assert.equal(String(url),'https://api.thetavideoapi.com/video/test-video');assert.equal(new Headers(init?.headers).get('x-tva-sa-id'),'test-account');return new Response('{}');};
 try{await run({command:'theta.video.get',videoId:'test-video'},{env:{THETA_VIDEO_SA_ID:'test-account',THETA_VIDEO_SA_SECRET:'test-secret'}});}finally{globalThis.fetch=prior;}
});
