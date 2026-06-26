#!/usr/bin/env node
const { readJsonArg, getJson, print } = require('./lib');

async function main() {
  const input = readJsonArg(2, 'input');
  if (!input.task_id) throw new Error('task_id is required');
  const data = await getJson(`/paas/v4/async-result/${input.task_id}`);
  print({ success: true, action: 'query_video_result', task_id: input.task_id, data });
}

main().catch((error) => {
  console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
  process.exit(1);
});
