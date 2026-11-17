import { createSpendPolicy, parseSpendPolicy } from 'spendpreflight';
import { pathToFileURL } from 'node:url';

const object = x => x !== null && typeof x === 'object' && !Array.isArray(x);
const exactKeys = (x, keys) => object(x) && Object.keys(x).every(k => keys.includes(k));
const clone = x => JSON.parse(JSON.stringify(x));
const result = (decision, reasons, extra = {}) => ({
  decision, reasons, mode: 'offline', payment_authorized: false,
  signer: null, network_requests: 0, ...extra,
});
const blocked = reason => result('block', [reason]);
const normalized = s => /^0x[0-9a-f]{40}$/i.test(s) ? s.toLowerCase() : s;

/** Free offline SDK check. There is deliberately no remote/approval/signer option. */
export async function preflight_payment(input, policy) {
  if (!exactKeys(input, ['challenge', 'selected_requirement']) || !input.challenge || !input.selected_requirement) {
    return blocked('Provide an actual challenge and selected_requirement; offline options cannot enable payment.');
  }
  try {
    const controller = createSpendPolicy(clone(policy)); // remote omitted: SDK holds.
    const verdict = await controller.check(clone(input.challenge), clone(input.selected_requirement));
    return result(verdict.decision === 'block' ? 'block' : 'hold', verdict.reasons, {
      tool: 'preflight_payment', sdk_version: '0.4.0',
      amount_usd: verdict.amountUsd, remote_evidence: 'not_observed',
    });
  } catch {
    return blocked('Invalid Spend Policy or challenge. No remote check or payment was attempted.');
  }
}

/** Validate public screening input; never fabricate a remote screening result. */
export async function check_payee(input, policy) {
  if (!exactKeys(input, ['address', 'domain', 'name']) || Object.keys(input).length === 0 ||
      Object.values(input).some(v => typeof v !== 'string' || !v.trim() || v !== v.trim() || v.length > 256)) {
    return blocked('Provide at least one bounded public address, domain or name.');
  }
  if (input.domain) {
    try {
      const u = new URL(input.domain.includes('://') ? input.domain : `https://${input.domain}`);
      if (!['https:', 'http:'].includes(u.protocol) || u.username || u.password || u.hash || !u.hostname) throw Error();
    } catch { return blocked('Invalid public domain or URL.'); }
  }
  try {
    const p = parseSpendPolicy(clone(policy));
    if (input.address && p.merchantBlocklist.some(a => normalized(a) === normalized(input.address))) {
      return blocked('Payee address is on the supplied local merchant blocklist.');
    }
  } catch { return blocked('Invalid Spend Policy.'); }
  return result('hold', ['Offline: payee screening has not been performed. Human approval is required before any paid remote check.'], {
    tool: 'check_payee', address_match: null, screening_status: 'unknown', remote_evidence: 'not_observed',
  });
}

async function main() {
  let text = '';
  for await (const chunk of process.stdin) {
    text += chunk;
    if (Buffer.byteLength(text) > 65536) throw Error('Input exceeds 64 KiB');
  }
  const request = JSON.parse(text);
  if (!exactKeys(request, ['tool', 'input', 'policy']) || !['preflight_payment', 'check_payee'].includes(request.tool)) {
    throw Error('Supported tools: preflight_payment, check_payee. Offline mode only.');
  }
  const fn = request.tool === 'preflight_payment' ? preflight_payment : check_payee;
  console.log(JSON.stringify(await fn(request.input, request.policy), null, 2));
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main().catch(() => { console.error('Invalid offline request; no network or payment attempted.'); process.exitCode = 1; });
}
