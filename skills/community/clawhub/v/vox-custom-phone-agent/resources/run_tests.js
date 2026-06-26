#!/usr/bin/env node
'use strict';

const fs = require('fs');
const path = require('path');
const { handlePrompt } = require('./index');
const { CallJobStore } = require('./call_job_store');
const { callVoxOutbound } = require('./hmac_outbound_client');
const { turnsToTranscript } = require('./vox_call_result_client');

async function main() {
  const filePath = path.join(__dirname, 'test_prompts.json');
  const tests = JSON.parse(fs.readFileSync(filePath, 'utf8'));
  let failed = 0;

  for (const test of tests) {
    const result = await handlePrompt(test.prompt, { noCall: true });
    const errors = [];
    if (result.status !== test.expectedStatus) {
      errors.push(`status expected ${test.expectedStatus}, got ${result.status}`);
    }
    if (test.expectedVoiceType && result.voiceType !== test.expectedVoiceType) {
      errors.push(`voiceType expected ${test.expectedVoiceType}, got ${result.voiceType}`);
    }
    if (test.workflowIncludes && result.agentProfile) {
      for (const fragment of test.workflowIncludes) {
        if (!result.agentProfile.workflow.includes(fragment)) {
          errors.push(`workflow missing ${fragment}`);
        }
      }
    }

    if (errors.length) {
      failed += 1;
      console.error(`FAIL ${test.name}: ${errors.join('; ')}`);
      console.error(result.message);
    } else {
      console.log(`PASS ${test.name}`);
    }
  }

  await runPostCallCallbackTests();

  if (failed) process.exit(1);
}

async function runPostCallCallbackTests() {
  const outboundResult = await callVoxOutbound({
    credentials: { appId: 'app_test', secret: 'secret_test', baseUrl: 'https://vox.example.com', trialMode: false },
    payload: { appId: 'app_test', callee: '13800138000', requestId: 'req_test' },
    fetchImpl: async () => jsonResponse(202, {
      code: 0,
      msg: 'success',
      data: { requestId: 'req_test', callId: 'call_test', status: 'accepted' }
    })
  });
  assert(outboundResult.callId === 'call_test', 'callVoxOutbound should expose data.callId');

  const transcript = turnsToTranscript([
    { turnIndex: 1, userText: '', botText: '您好', playbackCompletedAt: '2026-05-20T10:30:15' },
    { turnIndex: 2, userText: '好的', botText: '谢谢', playbackCompletedAt: '2026-05-20T10:30:28' }
  ]);
  assert(transcript.length === 3, 'turnsToTranscript should split userText and botText');
  assert(transcript[1].role === 'callee', 'userText should become callee transcript');

  const store = new CallJobStore();
  const result = await handlePrompt('使用正式账号。给 13800138000 打电话，作为会议通知助理通知对方明天下午三点开会，地点在 A 座 2 楼会议室，只需确认对方是否知晓，使用知言音色。', {
    credentials: { appId: 'app_test', secret: 'secret_test', botId: '', baseUrl: 'https://vox.example.com', trialMode: false },
    postCallCallbackUrl: 'https://customer.example.com/callback',
    callJobStore: store,
    fetchImpl: async (url) => {
      if (String(url).includes('/vox/v1/outbound')) {
        return jsonResponse(202, { code: 0, msg: 'success', data: { requestId: 'req_formal', callId: 'call_formal', status: 'accepted' } });
      }
      return jsonResponse(200, { code: 0, msg: 'success', data: { callId: 'call_formal', appId: 'app_test', status: 'started' } });
    },
    requestId: 'req_formal'
  });
  assert(result.status === 'accepted', 'formal post-call prompt should still return accepted');
  assert(result.postCallCallback.enabled === true, 'formal callback should be enabled');
  assert(result.postCallCallback.status === 'polling', 'formal callback should start polling');
  assert(store.getJobByRequestId('req_formal').callId === 'call_formal', 'call job should store callId');

  const trial = await handlePrompt('先试用。给 13800138000 打电话，作为会议通知助理通知对方明天下午三点开会，地点不变，使用知言音色。', {
    noCall: true,
    postCallCallbackUrl: 'https://customer.example.com/callback'
  });
  assert(!trial.postCallCallback, 'trial preview should not add postCallCallback field');

  const queryResult = await handlePrompt('查询通话内容 callId：4e0c4ecf-1ad6-42c3-b343-e1eb90ee18c6', {
    credentials: { appId: 'app_test', secret: 'secret_test', botId: '', baseUrl: 'https://vox.example.com', trialMode: false },
    fetchImpl: async (url) => {
      if (String(url).includes('/vox/v1/get/call/status')) {
        return jsonResponse(200, { code: 0, msg: 'success', data: { callId: '4e0c4ecf-1ad6-42c3-b343-e1eb90ee18c6', appId: 'app_test', status: 'completed' } });
      }
      return jsonResponse(200, { code: 0, msg: 'success', data: [
        { turnIndex: 1, userText: '', botText: '您好', playbackCompletedAt: '2026-05-20T10:30:15' },
        { turnIndex: 2, userText: '好的', botText: '谢谢', playbackCompletedAt: '2026-05-20T10:30:28' }
      ] });
    }
  });
  assert(queryResult.status === 'call_result', 'call result query should return call_result');
  assert(queryResult.transcript.length === 3, 'call result query should return transcript');
  assert(queryResult.message.includes('调试信息'), 'call result query should include debug output');

  const waitedResult = await handlePrompt('使用正式账号。给 13800138000 打电话，作为会议通知助理通知对方明天下午三点开会，地点在 A 座 2 楼会议室，只需确认对方是否知晓，使用知言音色。挂断后直接总结通话内容。', {
    credentials: { appId: 'app_test', secret: 'secret_test', botId: '', baseUrl: 'https://vox.example.com', trialMode: false },
    requestId: 'req_wait',
    callResultTimeoutMs: 1000,
    callResultPollIntervalMs: 0,
    fetchImpl: async (url) => {
      if (String(url).includes('/vox/v1/outbound')) {
        return jsonResponse(202, { code: 0, msg: 'success', data: { requestId: 'req_wait', callId: 'call_wait', status: 'accepted' } });
      }
      if (String(url).includes('/vox/v1/get/call/status')) {
        return jsonResponse(200, { code: 0, msg: 'success', data: { callId: 'call_wait', appId: 'app_test', status: 'completed' } });
      }
      return jsonResponse(200, { code: 0, msg: 'success', data: [
        { turnIndex: 1, userText: '', botText: '您好', playbackCompletedAt: '2026-05-20T10:30:15' },
        { turnIndex: 2, userText: '好的，我知道了', botText: '谢谢，再见', playbackCompletedAt: '2026-05-20T10:30:28' }
      ] });
    }
  });
  assert(waitedResult.callResult.status === 'completed', 'wait mode should fetch completed call result');
  assert(waitedResult.message.includes('简单总结'), 'wait mode response should include summary');
  assert(waitedResult.message.includes('状态查询 #1'), 'wait mode response should include status debug output');

  const defaultWaitResult = await handlePrompt('使用正式账号。给 13800138000 打电话，作为朋友问候对方最近近况，围绕工作和生活聊天，使用景珩音色。', {
    credentials: { appId: 'app_test', secret: 'secret_test', botId: '', baseUrl: 'https://vox.example.com', trialMode: false },
    requestId: 'req_default_wait',
    callResultTimeoutMs: 1000,
    callResultPollIntervalMs: 0,
    fetchImpl: async (url) => {
      if (String(url).includes('/vox/v1/outbound')) {
        return jsonResponse(202, { code: 0, msg: 'success', data: { requestId: 'req_default_wait', callId: 'call_default_wait', status: 'accepted' } });
      }
      if (String(url).includes('/vox/v1/get/call/status')) {
        return jsonResponse(200, { code: 0, msg: 'success', data: { callId: 'call_default_wait', appId: 'app_test', status: 'completed' } });
      }
      return jsonResponse(200, { code: 0, msg: 'success', data: [
        { turnIndex: 1, userText: '', botText: '最近怎么样？', playbackCompletedAt: '2026-05-20T10:30:15' },
        { turnIndex: 2, userText: '还可以，工作有点忙', botText: '注意休息', playbackCompletedAt: '2026-05-20T10:30:28' }
      ] });
    }
  });
  assert(defaultWaitResult.callResult.status === 'completed', 'formal calls should wait by default without callbackUrl');
  console.log('PASS post_call_callback_helpers');
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

function jsonResponse(status, body) {
  return {
    ok: status >= 200 && status < 300,
    status,
    text: async () => JSON.stringify(body)
  };
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
