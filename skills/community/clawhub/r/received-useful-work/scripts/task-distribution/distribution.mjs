import { spawn } from 'node:child_process';
import { mkdtemp, mkdir, writeFile, rm } from 'node:fs/promises';
import { join } from 'node:path';
import { budget, sourceAdapter, CURRENT, ROOT, hash, fail } from './source.mjs';
import { members, extract } from './archive.mjs';

export const PIN = Object.freeze({ version: '0.4.1', archive: '64dbe1ee7f69dd40ebf71741eed92f1f3f893c44af8eadf18b71c0fac82227b8',
  license: 'c9e2795d29bf1008cbd36ac045bd3c77d537438a51d8dda34e158f4e82a6a27c',
  notice: 'b8581bef3ffe7354f1cdf38f0cdbd78f468d4addafefa21c92aa34725ce8bc3a', bytes: 40891 });
const CAPS = ['seller-useful-output', 'seller-method-binding'];
const PURPOSE = 'integration-command-referral';
const COMMAND = ['node', 'package/bin/caller-deliver.mjs', 'deliver', '--request', 'request.json'];
const stable = value => JSON.stringify(value, (_, item) => item && !Array.isArray(item) && typeof item === 'object'
  ? Object.fromEntries(Object.keys(item).sort().map(k => [k, item[k]])) : item);
const digest = value => hash(stable(value));
const scope = request => { const input = { ...request.input }; delete input.callerId; return digest({ task: request.task, requirements: request.requirements, input }); };
function secretKeys(value) {
  if (!value || typeof value !== 'object') return false;
  return Object.entries(value).some(([k, v]) => /^(authorization|credentials?|privateKey|paymentSignature|wallet|token|apiKey|grant)$/i.test(k) || secretKeys(v));
}
export function qualify(request) {
  if (!request || request.schema !== 'task-distribution.request.v1' || typeof request.task !== 'string' || !request.task.trim() || request.task.length > 2000 ||
      !Array.isArray(request.requirements) || !request.requirements.length) return 'missing_task_or_requirements';
  if (request.requirements.some(c => !CAPS.includes(c))) return 'no_compatible_capability';
  const input = request.input;
  if (!input || typeof input !== 'object' || typeof input.callerId !== 'string' || typeof input.origin !== 'string' ||
      typeof input.operation !== 'string' || typeof input.sdk !== 'string' || typeof input.runtime !== 'string' ||
      typeof input.task !== 'string' || input.task.trim().length < 40 || !input.expect || !input.limits) return 'missing_caller_input';
  if (input.task !== request.task) return 'task_text_mismatch';
  if (typeof input.expect.path !== 'string' || !Object.hasOwn(input.expect, 'value') ||
      ['probes', 'bodyBytes', 'deadlineMs', 'totalBodyBytes', 'totalResponseMs', 'outputBytes'].some(k => !Object.hasOwn(input.limits, k))) return 'missing_caller_input';
  if (input.observed && input.probeConsent) return 'ambiguous_caller_evidence';
  if (secretKeys(input) || input.paidIntent === true) return 'credentials_or_paid_intent_refused';
  if (request.requirements.includes('seller-method-binding') && !input.methodBinding) return 'missing_method_binding';
  if (!input.observed && input.probeConsent?.confirmed !== true) return 'missing_observation_or_probe_consent';
  return null;
}
function negative(code, extra = {}) {
  return { schema: 'task-distribution.result.v1', decision: 'rejected', reason: code, executed: false, useful: null,
    paymentAuthority: 'none', paymentSent: false, ...extra };
}
export async function discover(read, allowance) {
  const result = await allowance.wait(read(CURRENT, allowance));
  let d; try { d = JSON.parse(result.bytes); } catch { throw fail('descriptor_invalid_json'); }
  if (d.schema !== 'samedaydesk.seller-repair.current.v1' || d.packageName !== 'seller-repair-external-consumer') throw fail('descriptor_mismatch');
  if (d.version !== PIN.version || d.sha256 !== PIN.archive || d.bytes !== PIN.bytes) throw fail('version_requires_source_review');
  const expectedPath = `${ROOT}${PIN.version}/seller-repair-external-consumer-${PIN.version}.tar.gz`;
  if (d.archive !== expectedPath || d.license !== 'MIT' || stable(d.coldCommand?.argv) !== stable(COMMAND)) throw fail('descriptor_mismatch');
  const license = await allowance.wait(read(`${ROOT}${PIN.version}/LICENSE`, allowance, 16384));
  const notice = await allowance.wait(read(`${ROOT}${PIN.version}/SOURCE-NOTICE.txt`, allowance, 16384));
  if (hash(license.bytes) !== PIN.license || hash(notice.bytes) !== PIN.notice) throw fail('terms_changed');
  return { descriptor: d, descriptorSha256: hash(result.bytes), termsSha256: digest([hash(license.bytes), hash(notice.bytes)]),
    date: result.observedAt, coverage: result.coverage, currentUrl: result.url, license: 'MIT', source: d.source,
    command: COMMAND, prerequisites: ['Node.js >=22.22.2', 'caller-owned JSON task, observed evidence or explicit bounded probe consent'],
    hostedClaim: d.hostedAcquisitionVerified === true, outsideUsefulness: 'unknown' };
}
export function recheck(packet, request, source, now) {
  if (packet?.schema !== 'task-distribution.referral.v1' || packet.purpose !== PURPOSE || packet.authority !== 'none' ||
      !Array.isArray(packet.capabilities) || !packet.capabilities.length || packet.capabilities.some(c => !CAPS.includes(c))) return 'packet_scope_invalid';
  if (!Number.isFinite(Date.parse(packet.createdAt)) || !Number.isFinite(Date.parse(packet.expiresAt)) || Date.parse(packet.createdAt) > now ||
      Date.parse(packet.expiresAt) <= now || Date.parse(packet.expiresAt) - Date.parse(packet.createdAt) > 86400000) return 'packet_expired_or_invalid_clock';
  if (source.descriptorSha256 !== packet.descriptorSha256 || source.termsSha256 !== packet.termsSha256) return 'source_or_terms_changed';
  if (request.requirements.some(c => !packet.capabilities.includes(c)) || scope(request) !== packet.taskScopeSha256) return 'changed_task_requires_requalification';
  return null;
}
export function executionEnv() {
  return {};
}
function runChild(root, allowance, outputBytes) {
  const timeoutMs = allowance.left();
  return new Promise((resolve, reject) => {
    const child = spawn(process.execPath, COMMAND.slice(1), { cwd: root, env: executionEnv(), detached: process.platform !== 'win32', stdio: ['ignore', 'pipe', 'pipe'] });
    const out = [], err = []; let count = 0, failure = null;
    const kill = () => { try { if (process.platform === 'win32') child.kill('SIGKILL'); else process.kill(-child.pid, 'SIGKILL'); } catch {} };
    const stop = code => { if (!failure) failure = fail(code); kill(); };
    const timer = setTimeout(() => stop('deadline'), timeoutMs);
    for (const [stream, target] of [[child.stdout, out], [child.stderr, err]]) stream.on('data', chunk => {
      if (failure) return;
      if (count + chunk.length > outputBytes - 512) { stop('output_oversized'); return; }
      try { allowance.output.charge(chunk); } catch { stop('output_oversized'); return; }
      count += chunk.length; target.push(chunk);
    });
    child.on('error', error => { clearTimeout(timer); reject(error); });
    child.on('close', (code, signal) => { clearTimeout(timer); kill(); if (failure) return reject(failure);
      if (signal || code === null) return reject(fail('child_failed'));
      let received; try { received = JSON.parse(Buffer.concat(out).toString()); } catch { return reject(fail('child_output_invalid')); }
      resolve({ exitCode: code, received, stderr: Buffer.concat(err).toString() });
    });
  });
}
export async function distribute(request, { directory = null, read = sourceAdapter({ directory }), execute = false, share = false,
    packet = null, now = Date.now(), timeoutMs = 15000, maxBytes = 262144, outputBytes = 131072, allowance: admittedAllowance = null, work = null } = {}) {
  const refusal = qualify(request); if (refusal) return negative(refusal, { nextAction: 'Supply your task, required capabilities, and complete repair request; no example is substituted.' });
  if (!Number.isFinite(now) || !Number.isInteger(outputBytes) || outputBytes < 1024 || outputBytes > 1048576) return negative('invalid_budget_or_clock');
  if (execute && (typeof work !== "string" || work.length === 0 || work.includes("\0"))) {
    return negative("output_scope_required", { nextAction: "Pass --work. Execution files are written only in that directory." });
  }
  let root, allowance;
  try {
    if (request.input.methodBinding?.freshness && Date.parse(request.input.methodBinding.freshness.expiresAt) <= now) throw fail('task_evidence_expired');
    allowance = admittedAllowance || budget(timeoutMs, maxBytes, outputBytes);
    allowance.left();
    const source = await discover(read, allowance);
    if (packet) { const refusal = recheck(packet, request, source, now); if (refusal) return negative(refusal, { source, nextAction: 'Qualify a fresh supplied request. This packet cannot transfer its prior recommendation.' }); }
    const archive = await allowance.wait(read(source.descriptor.archive, allowance, 131072));
    if (archive.bytes.length !== PIN.bytes || hash(archive.bytes) !== PIN.archive) throw fail('archive_mismatch');
    const files = members(archive.bytes);
    if (!files.has('package/bin/caller-deliver.mjs') || hash(files.get('package/LICENSE') || '') !== PIN.license ||
        hash(files.get('package/SOURCE-NOTICE.txt') || '') !== PIN.notice) throw fail('archive_terms_or_command_mismatch');
    const result = { schema: 'task-distribution.result.v1', decision: 'accepted', source, exactCommand: COMMAND,
      executed: false, useful: null, laterReuse: packet ? 'freshly-rechecked' : null, paymentAuthority: 'none', paymentSent: false };
    if (execute) {
      const [major, minor, patch] = process.versions.node.split('.').map(Number);
      if (major < 22 || (major === 22 && (minor < 22 || (minor === 22 && patch < 2)))) throw fail('runtime_requires_node_22_22_2');
      await allowance.wait(mkdir(work, { recursive: true, mode: 0o700 }));
      root = await allowance.wait(mkdtemp(join(work, ".execute-")));
      await extract(files, root, allowance);
      const freshInput = structuredClone(request.input);
      if (freshInput.methodBinding?.freshness) freshInput.methodBinding.freshness.evaluatedAt = new Date(now).toISOString();
      await allowance.wait(writeFile(join(root, 'request.json'), JSON.stringify(freshInput), { mode: 0o600 }));
      const child = await runChild(root, allowance, outputBytes); allowance.left();
      result.execution = child; result.executed = true;
      // A meaningful negative from the owning client is retained as its decision.
      // Neither its exit code nor output is upgraded to caller-asserted usefulness.
      if (child.exitCode !== 0) { result.decision = 'received_negative'; result.reason = child.received.reason || 'client_refused'; }
    }
    if (share && result.decision === 'accepted') result.referral = {
      schema: 'task-distribution.referral.v1', purpose: PURPOSE, authority: 'none', capabilities: [...request.requirements],
      taskScopeSha256: scope(request), descriptorSha256: source.descriptorSha256, termsSha256: source.termsSha256,
      createdAt: new Date(now).toISOString(), expiresAt: new Date(now + 86400000).toISOString(),
      currentUrl: source.currentUrl, version: PIN.version, license: 'MIT', priorUseful: null,
      sharing: 'caller-explicit-command-reference-only', nextAction: 'Supply your own complete request and recheck current source/terms; execute only with your own explicit consent.'
    };
    return result;
  } catch (error) { return negative(error.code || 'source_or_execution_failed', { observation: error.observation || null, nextAction: 'Recheck the owning current descriptor and exact licensed bytes. Root owns publication; source failures are not useful execution.' }); }
  finally { if (root) await allowance.wait(rm(root, { recursive: true, force: true })); }
}
