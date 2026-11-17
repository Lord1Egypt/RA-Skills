#!/usr/bin/env node
// Reading/offering context is NOT proof that a conversation used it.
// A consumer acknowledges only after actual use, with the exact candidate id.
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { ambientEnabled } from './memory_policy.js';
import { recallExperiences } from './experience_recall.js';

async function main() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--help') {
      console.log('read_ambient_recall.js --file <staged.json> [--resolve --events-dsid <uuid> --emotions-dsid <uuid> --state-dsid <uuid>] [--ack <candidate-id> --used-in <turn-reference>]');
      return;
    }
    if (args[i] === '--resolve') { opts.resolve = true; continue; }
    if (!['--file', '--ack', '--used-in', '--events-dsid', '--emotions-dsid', '--state-dsid'].includes(args[i]) || !args[i + 1] || args[i + 1].startsWith('--')) {
      throw new Error('Expected --file, or --ack with --used-in');
    }
    opts[args[i].slice(2)] = args[++i];
  }
  if (!ambientEnabled()) {
    console.log(JSON.stringify({ ok: true, status: 'disabled', consumed: false }));
    return;
  }
  if (!opts.file) throw new Error('Missing --file');
  if (opts.resolve && opts.ack) throw new Error('Resolve context before use; acknowledge in a separate call after use');
  if (Boolean(opts.ack) !== Boolean(opts['used-in'])) throw new Error('--ack and --used-in are required together');
  if (!fs.existsSync(opts.file)) {
    if (opts.ack) throw new Error('Cannot acknowledge a missing candidate');
    console.log(JSON.stringify({ ok: true, status: 'missing', consumed: false }));
    return;
  }
  const raw = fs.readFileSync(opts.file, 'utf8');
  const recall = JSON.parse(raw);
  if (recall.kind !== 'ambient_recall' || recall.version !== 1 || !recall.content ||
      !Number.isFinite(Date.parse(recall.expires_at))) throw new Error('Invalid staged recall');
  const id = recall.id || crypto.createHash('sha256').update(raw).digest('hex');
  const receiptFile = opts.file + '.consumption.json';
  let receipt = null;
  if (fs.existsSync(receiptFile)) receipt = JSON.parse(fs.readFileSync(receiptFile, 'utf8'));
  const consumed = receipt?.candidate_id === id;
  const expired = Date.parse(recall.expires_at) <= Date.now();
  if (opts.ack) {
    if (opts.ack !== id) throw new Error('Candidate changed; acknowledgment rejected');
    if (expired) throw new Error('Candidate expired; acknowledgment rejected');
    if (!opts['used-in'].trim()) throw new Error('Missing turn reference');
    if (!consumed) {
      // Detect replacement before writing; receipt id also prevents a stale
      // acknowledgment from marking a newer candidate consumed.
      if (fs.readFileSync(opts.file, 'utf8') !== raw) throw new Error('Candidate changed during acknowledgment');
      receipt = { version: 1, candidate_id: id, consumed_at: new Date().toISOString(),
        used_in: opts['used-in'], evidence: 'consumer_acknowledgment' };
      const tmp = receiptFile + '.' + crypto.randomUUID() + '.tmp';
      fs.mkdirSync(path.dirname(receiptFile), { recursive: true });
      fs.writeFileSync(tmp, JSON.stringify(receipt, null, 2) + '\n', { mode: 0o600, flag: 'wx' });
      fs.renameSync(tmp, receiptFile);
    }
    console.log(JSON.stringify({ ok: true, status: 'consumed', consumed: true, receipt }));
    return;
  }
  let resolution = null;
  if (opts.resolve && !expired && !consumed) {
    if (recall.source?.type === 'notion_state') {
      resolution = await recallExperiences({ stateId: recall.source.id, eventsDsid: opts['events-dsid'],
        emotionsDsid: opts['emotions-dsid'], stateDsid: opts['state-dsid'], limit: 1 });
    } else {
      resolution = { ok: true, status: 'no_verified_event_route', complete: false,
        source: recall.source || null, results: [] };
    }
    if (fs.readFileSync(opts.file, 'utf8') !== raw) throw new Error('Candidate changed during resolution; read the current candidate without rerolling');
    if (Date.parse(recall.expires_at) <= Date.now()) throw new Error('Candidate expired during resolution');
  }
  console.log(JSON.stringify({ ok: resolution?.ok !== false,
    status: expired ? 'expired' : consumed ? 'consumed' : 'available',
    consumed, receipt: consumed ? receipt : null,
    recall: expired || consumed ? null : { ...recall, id }, ...(resolution ? { resolution } : {}) }));
  if (resolution?.ok === false) process.exitCode = 1;
}
try { await main(); } catch (error) {
  console.error(JSON.stringify({ ok: false, status: 'error', error: error.message }));
  process.exitCode = 1;
}
