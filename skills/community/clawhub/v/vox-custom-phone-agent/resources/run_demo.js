#!/usr/bin/env node
'use strict';

const { handlePrompt } = require('./index');
const { maskPhone } = require('./phone_validator');

async function main() {
  const args = process.argv.slice(2);
  const noCallIndex = args.indexOf('--no-call');
  const noCall = noCallIndex >= 0;
  if (noCall) args.splice(noCallIndex, 1);

  const prompt = args.join(' ').trim() || '帮我给 13800138000 打电话，作为课程顾问介绍周末 AI 编程体验课，目标是确认是否愿意预约试听，语气专业但不要强推。';
  const result = await handlePrompt(prompt, { noCall });

  console.log(result.message);
  if (result.status === 'ready') {
    console.log('\nPayload:');
    console.log(JSON.stringify(maskPayload(result.payload), null, 2));
  }
  if (result.status === 'needs_input') {
    console.log('\nPending intent:');
    console.log(JSON.stringify(result.intent, null, 2));
  }
}

function maskPayload(payload = {}) {
  return {
    ...payload,
    callee: maskPhone(payload.callee)
  };
}

main().catch((error) => {
  console.error(error.stack || error.message);
  process.exit(1);
});
