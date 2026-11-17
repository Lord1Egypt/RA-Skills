#!/usr/bin/env node
import { durableReplace } from './delivery-contracts/durable.mjs';
import { readFileBounded, budget } from './source.mjs';
import { distribute } from './distribution.mjs';
const args = process.argv.slice(2);
let allowance;
const get = name => { const i = args.indexOf(name); return i < 0 ? null : args[i + 1]; };
if (!['qualify', 'run', 'reuse'].includes(args[0])) {
  process.stdout.write('Commands: qualify|run|reuse --request FILE [--source-directory SNAPSHOT] [--packet FILE] [--execute yes --work DIR] [--share yes --out PACKET]\n'); process.exit(2);
}
try {
  if (args.length > 64 || args.reduce((n, value) => n + Buffer.byteLength(value), 0) > 65536) throw new Error('caller_input_limit');
  const timeoutMs = get('--timeout-ms') ? Number(get('--timeout-ms')) : 15000;
  const maxBytes = get('--max-bytes') ? Number(get('--max-bytes')) : 262144;
  const outputBytes = get('--output-bytes') ? Number(get('--output-bytes')) : 131072;
  allowance = budget(timeoutMs, maxBytes, outputBytes);
  const request = get('--request') ? JSON.parse(await readFileBounded(get('--request'), 65536, allowance)) : null;
  const packet = get('--packet') ? JSON.parse(await readFileBounded(get('--packet'), 65536, allowance)) : null;
  if (args[0] === 'reuse' && !packet) throw new Error('packet_required');
  if (args[0] === 'run' && get('--execute') !== 'yes') throw new Error('explicit_execution_required');
  if (get('--share') === 'yes' && !get('--out')) throw new Error('packet_output_required');
  const result = await distribute(request, { packet, directory: get('--source-directory'),
    execute: get('--execute') === 'yes', share: get('--share') === 'yes', work: get('--work'),
    timeoutMs, maxBytes, outputBytes, allowance });
  const output = JSON.stringify(result) + '\n';
  const referral = result.referral ? JSON.stringify(result.referral) + '\n' : null;
  allowance.left();
  allowance.output.charge(output);
  if (referral) {
    allowance.output.charge(referral);
    await allowance.wait(durableReplace(get('--out'), referral, { exclusive: true }));
  }
  process.stdout.write(output);
  process.exitCode = result.decision === 'accepted' ? 0 : 2;
} catch (error) {
  const failure = JSON.stringify({ decision: 'rejected', reason: error.code || 'invalid_input', executed: false, useful: null,
    commitOutcome: error.outcome || null }) + '\n';
  // The bounded failure response uses the reserved control allowance.
  process.stdout.write(failure); process.exitCode = 2;
}
