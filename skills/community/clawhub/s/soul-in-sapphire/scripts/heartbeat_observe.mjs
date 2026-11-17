import fs from 'node:fs';
import path from 'node:path';
import {atomicJson} from './soul_io.js';

const results = new Set(['changed', 'no_change', 'unavailable', 'failed']);
const isObject = value => value !== null && typeof value === 'object' && !Array.isArray(value);
const hasId = value => typeof value === 'string' && value.trim().length > 0;

function readObject(file) {
  const value = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!isObject(value)) throw new Error('Expected a JSON object: ' + file);
  return value;
}

function main() {
  const args = {};
  for (let i = 2; i < process.argv.length; i++) {
    const flag = process.argv[i];
    if (flag === '--help') {
      console.log('heartbeat_observe.mjs --workspace <agent-workspace> --observation-file <json> [--receipt-file <completed-tick.json>] [--apply | --dry-run]\nDefault: preview only. Observation: {"result":"no_change","reason":"grounded reason","evidence_references":{"source":"path or tool reference"}}');
      return;
    }
    if (flag === '--apply' || flag === '--dry-run') {
      args[flag] = true;
      continue;
    }
    if (!['--workspace', '--observation-file', '--receipt-file'].includes(flag)) {
      throw new Error('Unknown argument: ' + flag);
    }
    const value = process.argv[++i];
    if (!value || value.startsWith('--') || args[flag] !== undefined) {
      throw new Error('Missing or duplicate argument: ' + flag);
    }
    args[flag] = value;
  }
  if (args['--apply'] && args['--dry-run']) throw new Error('Choose --apply or --dry-run, not both');
  if (!args['--workspace']) throw new Error('--workspace is required');
  if (!args['--observation-file']) throw new Error('--observation-file is required');
  const observation = readObject(args['--observation-file']);
  if (!results.has(observation.result)) throw new Error('Invalid observation result');
  if (typeof observation.reason !== 'string' || !observation.reason.trim()) {
    throw new Error('A grounded observation reason is required');
  }
  const references = observation.evidence_references;
  if (!isObject(references) || Object.values(references).some(value => typeof value !== 'string')) {
    throw new Error('evidence_references must be an object of strings');
  }
  if ('event_id' in references || 'state_id' in references) {
    throw new Error('Event/state IDs must come from a completed tick receipt, not observation input');
  }
  const durableIds = {};
  if (observation.result === 'changed') {
    if (!args['--receipt-file']) throw new Error('changed requires --receipt-file');
    const receipt = readObject(args['--receipt-file']);
    if (receipt.complete !== true || receipt.pending || !hasId(receipt.event?.id) || !hasId(receipt.state?.id)) {
      throw new Error('Tick receipt is incomplete or ambiguous; reconcile before recording changed');
    }
    durableIds.event_id = receipt.event.id;
    durableIds.state_id = receipt.state.id;
  } else if (args['--receipt-file']) {
    throw new Error('--receipt-file applies only to changed observations');
  }
  const file = path.resolve(args['--workspace'], 'memory/heartbeat-state.json');
  let prior = {};
  try {
    prior = readObject(file);
  } catch (error) {
    if (error.code !== 'ENOENT') throw error;
  }
  if (prior.evidence_references !== undefined && !isObject(prior.evidence_references)) {
    throw new Error('Existing evidence_references must be an object');
  }
  const checkedAt = new Date().toISOString();
  const next = {
    ...prior,
    last_soul_check: checkedAt,
    last_soul_result: observation.result,
    last_soul_reason: observation.reason.trim(),
    evidence_references: {...prior.evidence_references, ...references, ...durableIds},
  };
  const applied = args['--apply'] === true;
  if (applied) atomicJson(file, next);
  console.log(JSON.stringify({ok: true, applied, dry_run: !applied, heartbeat_file: file,
    last_soul_check: checkedAt, last_soul_result: observation.result,
    last_soul_reason: next.last_soul_reason, evidence_references: next.evidence_references}));
}

try {
  main();
} catch (error) {
  console.error(JSON.stringify({ok: false, stage: 'observation', error: error.message}));
  process.exitCode = 1;
}
