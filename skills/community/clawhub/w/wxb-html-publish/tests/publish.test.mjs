import { test } from 'node:test';
import assert from 'node:assert/strict';
import { upload, safeURL, ENDPOINT } from '../scripts/publish.mjs';
const html = Buffer.from('<!doctype html><html><body>synthetic</body></html>');
const options = {group:'/wxb-published/1794799499975',name:'index.html',mime:'text/html'};
test('一次POST，使用目录发布原名及明确group，multipart正确', async () => {
 let calls=0;
 const result=await upload(html, async (url,request)=>{
  calls++; assert.equal(url,ENDPOINT); assert.equal(request.redirect,'manual');
  assert.equal(request.body.get('name'),'index.html');
  assert.equal(request.body.get('group'),options.group);
  assert.equal(request.body.get('file').name,'index.html');
  return Response.json({code:0,data:`https://s2.wangxiaobao.com${options.group}/index.html`});
 },options);
 assert.equal(calls,1); assert.ok(result.url);
});
test('HTTP、业务失败、错误JSON、网络超时不重试',async()=>{
 for(const response of [()=>new Response('',{status:403}),()=>Response.json({code:1}),()=>new Response('invalid'),()=>{throw new Error('timeout');}]){
  let calls=0; await assert.rejects(upload(html,async()=>{calls++; return response();},options)); assert.equal(calls,1);
 }
});
test('存储回执拒绝任意主机、端口和用户名',()=>{
 for(const url of ['http://s2.wangxiaobao.com/a','https://127.0.0.1/a','https://evil.test/a','https://user@s2.wangxiaobao.com/a','https://s2.wangxiaobao.com:444/a']) assert.throws(()=>safeURL(url));
});
