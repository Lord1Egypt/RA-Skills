import { createClient } from './online.mjs';

// No arbitrary module/command loading, environment credentials or yes/approve flag.
async function main() {
  const args = process.argv.slice(2);
  if (args.length > 1 || (args.length === 1 && args[0] !== '--online')) throw Error();
  let text = '';
  for await (const chunk of process.stdin) { text += chunk; if (Buffer.byteLength(text) > 65536) throw Error(); }
  console.log(JSON.stringify(await createClient({mode:args[0] === '--online' ? 'online' : 'offline'}).run(JSON.parse(text)),null,2));
}
main().catch(() => { console.error('Invalid request. No automatic retry or payment approval.'); process.exitCode = 1; });
