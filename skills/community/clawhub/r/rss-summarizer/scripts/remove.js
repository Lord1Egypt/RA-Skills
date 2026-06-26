import { removeSubscription } from './_lib.js';

const input = JSON.parse(await (async () => {
  const chunks = [];
  for await (const chunk of process.stdin) {
    chunks.push(chunk);
  }
  return Buffer.concat(chunks).toString();
})());

const result = await removeSubscription(input.id);
console.log(JSON.stringify(result));