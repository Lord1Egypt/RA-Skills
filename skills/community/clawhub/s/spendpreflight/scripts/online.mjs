import { createHash, randomUUID } from 'node:crypto';
import { createSpendPolicy, parseSpendPolicy } from 'spendpreflight';
import * as offline from './offline.mjs';

export const SERVICE = Object.freeze({
  origin: 'https://api.spendpreflight.com', network: 'eip155:8453',
  asset: '0x833589fcd6edb6e08f4c7c32d4f71b54bda02913',
  payee: '0xbf4164e07552e4c1b1b1597e72c7acaa3f0a1c58',
});
const paid = { preflight_payment: ['/v1/preflight', '0.02', '20000'], check_payee: ['/v1/check', '0.01', '10000'] };
const object = x => x !== null && typeof x === 'object' && !Array.isArray(x);
const keys = (x, allowed) => object(x) && Object.keys(x).every(k => allowed.includes(k));
const copy = x => JSON.parse(JSON.stringify(x));
const hash = x => createHash('sha256').update(JSON.stringify(x)).digest('hex');
const frozen = x => { if (object(x) || Array.isArray(x)) { Object.values(x).forEach(frozen); Object.freeze(x); } return x; };
const base = (mode, tool, reasons, extra = {}) => ({ decision: 'hold', mode, tool, reasons,
  payment_authorized: false, signer: null, ...extra });
function publicUrl(value) {
  if (typeof value !== 'string' || value.length > 2048) throw Error('Public HTTPS URL required');
  const u = new URL(value);
  if (u.protocol !== 'https:' || u.username || u.password || u.hash ||
      !u.hostname.includes('.') || /[:\[\]]|^[\d.]+$/.test(u.hostname) ||
      /(?:^|\.)(?:localhost|local|internal|onion)$/.test(u.hostname) ||
      [...u.searchParams.keys()].some(k => /token|secret|password|api.?key|authorization|signature/i.test(k))) throw Error('Public HTTPS URL required');
  return u.href;
}
function address(value) { return typeof value === 'string' && /^[A-Za-z0-9]{14,256}$/.test(value) && (!/^0x/i.test(value) || /^0x[\da-f]{40}$/i.test(value)); }
async function jsonBody(response, limit = 262144) {
  const reader = response.body?.getReader();
  if (!reader) throw Error('Missing response');
  const chunks = []; let size = 0;
  try { for (;;) { const {done, value} = await reader.read(); if (done) break; size += value.length;
    if (size > limit) throw Error('Oversized response'); chunks.push(value); } }
  finally { await reader.cancel().catch(() => {}); }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}
function rulesFor(policy) {
  const p = parseSpendPolicy(copy(policy));
  return {max_per_payment_usd:p.maxPerCallUsd, hold_above_usd:p.holdAboveUsd, daily_cap_usd:p.dailyCapUsd,
    allowed_networks:p.networkAllowlist, usdc_only:true, strict_allowlist:true,
    payto_allowlist:p.merchantAllowlist, payto_blocklist:p.merchantBlocklist};
}

/** Runtime callbacks are supplied by the trusted host, never by request JSON. No signer/key is accepted. */
export function createClient(options = {}) {
  if (!keys(options, ['mode','fetch','approve','paymentTool','now']) || !['offline','online'].includes(options.mode ?? 'offline')) throw Error('Invalid client options');
  const mode = options.mode ?? 'offline', fetcher = options.fetch ?? globalThis.fetch;
  const now = options.now ?? Date.now;
  const used = new Set();
  return Object.freeze({ async run(request) {
    let tool = request?.tool;
    if (!keys(request, ['tool','input','policy','operation_id']) || !['preflight_payment','check_payee','ofac_address_check','lint_endpoint'].includes(tool))
      return base(mode, tool, ['Invalid request fields or tool.'], {decision:'block'});
    if (mode === 'offline') {
      if (paid[tool]) return offline[tool](request.input, request.policy);
      return base(mode, tool, ['Offline: no remote observation was made.'], {network_requests:0, remote_evidence:'not_observed'});
    }
    let input;
    try { if (JSON.stringify(request).length > 60000) throw Error(); input = copy(request.input); }
    catch { return base(mode, tool, ['Invalid or oversized input.'], {decision:'block'}); }
    const operationId = request.operation_id ?? randomUUID();
    if (typeof operationId !== 'string' || !/^[\w-]{1,100}$/.test(operationId) || used.has(operationId))
      return base(mode, tool, ['Operation already attempted or invalid; do not retry unknown outcomes.']);
    const requestOnce = (url, init, timeout) => fetcher(url, {...init, redirect:'error', credentials:'omit', signal:AbortSignal.timeout(timeout)});
    if (!paid[tool]) {
      try {
        if (tool === 'ofac_address_check') {
          if (!keys(input, ['address','addresses']) || Object.keys(input).length !== 1 ||
              !(address(input.address) || (Array.isArray(input.addresses) && input.addresses.length >= 1 && input.addresses.length <= 10 && input.addresses.every(address)))) throw Error();
        } else {
          if (!keys(input, ['url']) || Object.keys(input).length !== 1) throw Error();
          input.url = publicUrl(input.url);
        }
      } catch { return base(mode, tool, ['Invalid public screening input.'], {decision:'block'}); }
      used.add(operationId);
      try {
        const path = tool === 'ofac_address_check' ? '/v1/ofac-address-check' : '/v1/lint';
        const response = await requestOnce(SERVICE.origin + path, {method:'POST', headers:{'Content-Type':'application/json','Accept':'application/json'}, body:JSON.stringify(input)}, tool === 'lint_endpoint' ? 65000 : 15000);
        if (response.status !== 200) return base(mode, tool, ['Free check unavailable; no determination and no paid fallback.'], {http_status:response.status, operation_id:operationId, remote_evidence:'not_observed'});
        const data = await jsonBody(response);
        const ofacRows = input.addresses ? data.results : [data];
        if (tool === 'ofac_address_check' ? (!Array.isArray(ofacRows) || ofacRows.length !== (input.addresses?.length ?? 1) || ofacRows.some(r => typeof r.address_match !== 'boolean' || !r.snapshot_built_at)) : (!object(data) || typeof data.outcome !== 'string' || !Array.isArray(data.findings) || !data.checked_at)) throw Error();
        return base(mode, tool, [tool === 'ofac_address_check' ? 'Exact OFAC address fields only; a non-match is not clearance.' : 'Unpaid Lint observation; not paid-delivery or safety proof.'],
          {operation_id:operationId, remote_evidence:'observed', data});
      } catch { return base(mode, tool, ['Free check outcome unavailable or malformed; no automatic retry.'], {operation_id:operationId, remote_evidence:'not_observed'}); }
    }

    // Apply the original SDK gates before any network or paid tool dispatch.
    const local = await offline[tool](input, request.policy);
    if (local.decision === 'block') return {...local, mode};
    let body;
    try {
      if (tool === 'preflight_payment') {
        const preview = createSpendPolicy(copy(request.policy)).evaluate(input.challenge, input.selected_requirement);
        if (preview.decision !== 'allow') return base(mode, tool, preview.reasons, {decision:preview.decision});
        publicUrl(input.challenge.resource.url);
        body = {challenge:{...input.challenge, accepts:[input.selected_requirement]}, resource_url:input.challenge.resource.url, rules:rulesFor(request.policy)};
      } else {
        if (input.address && !address(input.address)) throw Error();
        if (input.domain) publicUrl(input.domain.includes('://') ? input.domain : 'https://' + input.domain);
        body = input;
      }
    } catch { return base(mode, tool, ['Invalid public input or local policy.'], {decision:'block'}); }
    const [path, price, amount] = paid[tool], url = SERVICE.origin + path;
    used.add(operationId);
    let requirement;
    try {
      // Inert HEAD: read the current quote without running the paid check or a trial.
      const response = await requestOnce(url, {method:'HEAD',headers:{Accept:'application/json'}},15000);
      const header = response.headers.get('payment-required');
      if (response.status !== 402 || !header || header.length > 32768) throw Error();
      const challenge = JSON.parse(Buffer.from(header,'base64').toString('utf8'));
      if (challenge.x402Version !== 2 || challenge.resource?.url !== url || !Array.isArray(challenge.accepts)) throw Error();
      requirement = challenge.accepts.find(r => r.scheme === 'exact' && r.network === SERVICE.network && r.asset?.toLowerCase() === SERVICE.asset && r.payTo?.toLowerCase() === SERVICE.payee && r.amount === amount);
      if (!requirement) throw Error();
    } catch { return base(mode, tool, ['Current service quote is unavailable or differs from the expected price/payee/network/asset; no spend.'], {operation_id:operationId}); }
    const proposal = frozen({request_id:randomUUID(), operation_id:operationId, tool, url, method:'POST', body:copy(body),
      price_usd:price, maxPayment:price, amount_atomic:amount, payee:requirement.payTo, network:SERVICE.network, asset:SERVICE.asset,
      input_digest:hash(body), created_at:now(), expires_at:now()+120000,
      disclosure:'SpendPreflight is our paid external service. This approval covers only its screening fee, never payment to the screened merchant.'});
    if (typeof options.approve !== 'function' || typeof options.paymentTool?.execute !== 'function')
      return base(mode, tool, ['Human approval and an existing bounded x402 payment tool are required. No keys are requested.'], {approval_required:true, proposal});
    let approval;
    try { approval = await options.approve(proposal); } catch { /* no approval */ }
    if (!object(approval) || approval.approved !== true || approval.request_id !== proposal.request_id || now() > proposal.expires_at)
      return base(mode, tool, ['No current human approval for this exact call; no spend.'], {operation_id:operationId});
    try {
      const response = await options.paymentTool.execute(frozen({url,method:'POST',body:copy(body),maxPayment:price,
        expectedPayment:{scheme:'exact',network:SERVICE.network,asset:SERVICE.asset,payTo:requirement.payTo,amount},
        approval_id:proposal.request_id, input_digest:proposal.input_digest}));
      if (response?.pending) return base(mode, tool, ['Existing payment tool requires wallet approval; do not start another request.'], {operation_id:operationId,payment_pending:response});
      if (response?.status !== 200 || !object(response.body) || JSON.stringify(response.body).length > 262144) throw Error();
      const data = copy(response.body);
      if (tool === 'preflight_payment' ? (!['allow','hold','block'].includes(data.decision) || !Array.isArray(data.reasons)) : !['low','medium','high','unknown'].includes(data.risk)) throw Error();
      return base(mode, tool, tool === 'preflight_payment' ? data.reasons : ['Standalone payee screening is not permission to pay.'],
        {decision:tool === 'preflight_payment' ? data.decision : data.risk === 'high' ? 'block' : 'hold', operation_id:operationId,remote_evidence:'observed',data,
          service_fee:{price_usd:price,payee:requirement.payTo,transport:'existing_x402_payment_tool',settlement_independently_verified:false}});
    } catch { return base(mode, tool, ['Paid tool outcome unknown or invalid. No automatic retry; preserve the operation ID.'], {operation_id:operationId,paid_outcome:'unknown'}); }
  }});
}

function toolData(result) {
  if (result?.isError) throw Error('Payment tool error');
  if (object(result?.structuredContent)) return result.structuredContent;
  if (Array.isArray(result?.content)) {
    const text = result.content.filter(c => c.type === 'text').map(c => c.text).join('\n');
    if (text.length > 262144) throw Error('Oversized tool result');
    return JSON.parse(text);
  }
  return result;
}

/** Existing Coinbase Wallet MCP two-step API. Host supplies its native tool bridge, not credentials. */
export function createWalletMcpPaymentTool({callTool, confirmWallet, readResponse = x => x}) {
  if (typeof callTool !== 'function') throw Error('Existing native MCP tool bridge required');
  return Object.freeze({ async execute(request) {
    const started = toolData(await callTool('initiate_x402_request', {url:request.url,method:'POST',body:request.body,maxPayment:request.maxPayment}));
    if (typeof started?.requestId !== 'string' || typeof started?.approvalUrl !== 'string' || new URL(started.approvalUrl).protocol !== 'https:') throw Error('Expected wallet approval request');
    const review = frozen({requestId:started.requestId,approvalUrl:started.approvalUrl,expectedPayment:request.expectedPayment,maxPayment:request.maxPayment,
      instruction:'The human must review the actual wallet payee, Base USDC amount and request, then approve in the existing wallet. Reject changed terms.'});
    if (typeof confirmWallet !== 'function' || await confirmWallet(review) !== true) return {pending:true,...review};
    // Exactly one completion; no signing code, payment headers, retries or wallet setup.
    return readResponse(toolData(await callTool('complete_x402_request', {requestId:started.requestId})));
  }});
}
