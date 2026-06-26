import { fetchSubscriptions } from './_lib.js';

const input = JSON.parse(await (async () => {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString();
})());

const { id, format = 'markdown', notify = false } = input;
// Notification is handled by AI if needed, so we default notify=false
const result = await fetchSubscriptions(id, format, false);
console.log(JSON.stringify(result));