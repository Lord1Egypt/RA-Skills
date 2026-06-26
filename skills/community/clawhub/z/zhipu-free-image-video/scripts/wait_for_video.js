#!/usr/bin/env node
const { readJsonArg, getJson, sleep, print } = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.task_id) throw new Error('task_id is required');
  const maxWait = Number(input.max_wait_time || 300000);
  const poll = Number(input.poll_interval || 5000);
  const start = Date.now();

  while (Date.now() - start < maxWait) {
    const data = await getJson(`/paas/v4/async-result/${input.task_id}`);
    const status = data.task_status;
    if (status === 'SUCCESS') {
      return print({ success: true, action: 'wait_for_video', task_id: input.task_id, data });
    }
    if (status === 'FAIL') {
      throw new Error(data.error || 'video generation failed');
    }
    await sleep(poll);
  }

  print({
    success: false,
    action: 'wait_for_video',
    task_id: input.task_id,
    error: 'timeout',
    max_wait_time: maxWait,
  });
  process.exit(1);
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
