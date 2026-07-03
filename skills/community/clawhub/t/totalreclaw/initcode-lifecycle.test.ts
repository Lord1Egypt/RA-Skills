// scanner-sim: allow
/**
 * Tests for the initCode lifecycle (AA10 "sender already constructed" fix).
 *
 * Root cause this test locks in: after the first successful on-chain
 * submission deploys the counterfactual Smart Account via initCode, every
 * subsequent submission for the SAME sender MUST omit `factory` /
 * `factoryData`. If initCode is present on a UserOp whose sender is
 * already constructed, the EntryPoint rejects with AA10.
 *
 * The previous implementation cached "deployed" in a module-level Set.
 * That cache was the only thing preventing AA10 across submissions within
 * a session, and it was fragile:
 *   - A process restart emptied the cache → the next submission relied on
 *     a single eth_getCode that could return stale `0x` from a lagging
 *     RPC node → initCode was re-added → AA10.
 *   - A receipt poll that timed out (success undetected) left the cache
 *     empty → same staleness path.
 *
 * The fix: `getInitCode` re-checks `eth_getCode` on EVERY call — no
 * session cache. This test exercises the resulting contract by mocking
 * the RPC layer (`rpcRequest` via the relay module's fetch site) and
 * driving the real `getInitCode` through both states (undeployed →
 * deployed).
 *
 * The test also asserts the cache reset helper is a no-op-safe seam and
 * that repeated calls all hit the RPC layer (proving no caching).
 *
 * Run with: npx tsx initcode-lifecycle.test.ts
 */

import {
  __resetDeployedAccountsForTests,
  __getInitCodeForTests,
  __getRpcProbeCountForTests,
  __resetRpcProbeCountForTests,
  __setWasmForTests,
  __clearWasmForTests,
} from './subgraph-store.js';

let passed = 0;
let failed = 0;

function check(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.error(`not ok ${n} - ${name}`);
    failed++;
    process.exitCode = 1;
  }
}

// ---------------------------------------------------------------------------
// RPC probe instrumentation
// ---------------------------------------------------------------------------
//
// The production `getInitCode` calls `rpcRequest({ method: 'eth_getCode', ... })`
// on every invocation. To observe (and control) those calls without pulling
// in the live network, we monkey-patch global fetch. The probe counter is
// exported test-only from subgraph-store.ts so we can assert how many RPC
// reads happened across a sequence of getInitCode calls.
//
// `rpcRequest` POSTs a JSON-RPC envelope and reads `res.json()`. We decode
// the request body to find the method + params, then return the canned
// `eth_getCode` result the caller configured.

interface FetchController {
  codeResponses: string[];   // queued eth_getCode results (consumed in order)
  requests: Array<{ method: string; params: unknown[] }>;
  // Extended for Scenario 5: map of method → queued responses
  responseQueue: Map<string, Array<{ result?: any; error?: { message: string } }>>;
}

let controller: FetchController | null = null;

function installFetchMock(): FetchController {
  const ctl: FetchController = { codeResponses: [], requests: [], responseQueue: new Map() };
  controller = ctl;
  const original = globalThis.fetch;

  globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
    const bodyStr = typeof init?.body === 'string' ? init.body : '';
    let parsed: any = {};
    try { parsed = JSON.parse(bodyStr); } catch { /* not JSON-RPC */ }
    if (parsed.method) {
      ctl.requests.push({ method: parsed.method, params: parsed.params ?? [] });
    }
    // Look for an eth_getCode call and drain the next queued response (legacy path for Scenarios 1-4).
    if (parsed.method === 'eth_getCode') {
      // Check responseQueue first (Scenario 5), fall back to codeResponses (Scenarios 1-4)
      const methodQueue = ctl.responseQueue.get('eth_getCode');
      if (methodQueue && methodQueue.length > 0) {
        const response = methodQueue.shift()!;
        const responseBody = JSON.stringify({ jsonrpc: '2.0', id: parsed.id ?? 1, result: response.result, error: response.error });
        return new Response(responseBody, {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any;
      }
      const code = ctl.codeResponses.shift() ?? '0x';
      const responseBody = JSON.stringify({ jsonrpc: '2.0', id: parsed.id ?? 1, result: code });
      return new Response(responseBody, {
        status: 200,
        headers: { 'Content-Type': 'application/json' },
      }) as any;
    }
    // Check responseQueue for other methods (Scenario 5)
    if (parsed.method && ctl.responseQueue.has(parsed.method)) {
      const methodQueue = ctl.responseQueue.get(parsed.method)!;
      if (methodQueue.length > 0) {
        const response = methodQueue.shift()!;
        const responseBody = JSON.stringify({ jsonrpc: '2.0', id: parsed.id ?? 1, result: response.result, error: response.error });
        return new Response(responseBody, {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
        }) as any;
      }
    }
    // Default: empty success envelope for any other method.
    const responseBody = JSON.stringify({ jsonrpc: '2.0', id: parsed.id ?? 1, result: null });
    return new Response(responseBody, {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    }) as any;
  }) as typeof globalThis.fetch;

  // Attach a restore for teardown.
  (ctl as any)._restore = () => { globalThis.fetch = original; };
  return ctl;
}

function restoreFetch(ctl: FetchController): void {
  (ctl as any)._restore?.();
  controller = null;
}

// ---------------------------------------------------------------------------
// Scenario 1: undeployed → deployed transition omits initCode on the 2nd call
// ---------------------------------------------------------------------------
//
// First call  : eth_getCode → '0x'      → factory + factoryData returned.
// Second call : eth_getCode → '0x1234'  → factory + factoryData are NULL.
// This is the exact AA10 regression: if the second call still returned
// initCode, the entrypoint would reject with "sender already constructed".

{
  __resetDeployedAccountsForTests();
  __resetRpcProbeCountForTests();
  const ctl = installFetchMock();
  // Queue two eth_getCode responses: first undeployed, second deployed.
  ctl.codeResponses.push('0x');            // 1st call: SA not yet on-chain
  ctl.codeResponses.push('0x1234abcd');    // 2nd call: SA constructed

  const sender = '0xaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa';
  const eoa    = '0xbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb';
  const rpcUrl = 'http://localhost:0/rpc';

  const first = await __getInitCodeForTests(sender, eoa, rpcUrl);
  check(
    first.factory !== null && first.factoryData !== null,
    '1st call (undeployed): returns factory + factoryData (initCode present)',
  );
  check(
    typeof first.factory === 'string' && first.factory.startsWith('0x'),
    '1st call: factory is a hex string',
  );
  check(
    typeof first.factoryData === 'string' && first.factoryData.startsWith('0x'),
    '1st call: factoryData is a hex string',
  );

  const second = await __getInitCodeForTests(sender, eoa, rpcUrl);
  check(
    second.factory === null && second.factoryData === null,
    '2nd call (deployed): returns null factory + factoryData (no initCode → no AA10)',
  );

  restoreFetch(ctl);
}

// ---------------------------------------------------------------------------
// Scenario 2: getInitCode re-checks eth_getCode on EVERY call (no caching)
// ---------------------------------------------------------------------------
//
// The session-cache optimization used to skip the RPC after a "deployed"
// result. That meant a process restart (empty cache) fell back to a single
// stale eth_getCode. After the fix, every call MUST hit eth_getCode — we
// assert this via the RPC probe counter.

{
  __resetDeployedAccountsForTests();
  __resetRpcProbeCountForTests();
  const ctl = installFetchMock();
  // All deployed.
  ctl.codeResponses.push('0xdeadbeef', '0xdeadbeef', '0xdeadbeef');

  const sender = '0xcccccccccccccccccccccccccccccccccccccccc';
  const eoa    = '0xdddddddddddddddddddddddddddddddddddddddd';
  const rpcUrl = 'http://localhost:0/rpc';

  const probesBefore = __getRpcProbeCountForTests();
  check(probesBefore === 0, `probe counter starts at 0 (got ${probesBefore})`);

  await __getInitCodeForTests(sender, eoa, rpcUrl);
  await __getInitCodeForTests(sender, eoa, rpcUrl);
  await __getInitCodeForTests(sender, eoa, rpcUrl);

  const probesAfter = __getRpcProbeCountForTests();
  check(
    probesAfter === 3,
    `3 getInitCode calls → 3 eth_getCode RPC reads (no caching) (got ${probesAfter})`,
  );

  restoreFetch(ctl);
}

// ---------------------------------------------------------------------------
// Scenario 3: a stale-then-fresh sequence converges to "no initCode"
// ---------------------------------------------------------------------------
//
// Mirrors the field failure mode: receipt poll times out on the deploying
// UserOp, so the cache never gets marked. The next submission calls
// eth_getCode, which on a lagging node may STILL return '0x' once, then
// '0x<code>' once the node catches up. With the cache removed, the
// per-submission re-check self-heals as soon as the node reflects the
// deployment. This test asserts the second call returns no initCode even
// when the first call (post-deployment) saw stale empty code.

{
  __resetDeployedAccountsForTests();
  __resetRpcProbeCountForTests();
  const ctl = installFetchMock();
  ctl.codeResponses.push('0x');          // stale: node hasn't seen the deploy tx
  ctl.codeResponses.push('0xcafe');      // fresh: node caught up

  const sender = '0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee';
  const eoa    = '0xffffffffffffffffffffffffffffffffffffffff';
  const rpcUrl = 'http://localhost:0/rpc';

  const stale = await __getInitCodeForTests(sender, eoa, rpcUrl);
  // Stale read legitimately returns initCode (the plugin can't know better).
  check(
    stale.factory !== null,
    'stale eth_getCode=0x still returns initCode (plugin cannot detect staleness)',
  );

  const fresh = await __getInitCodeForTests(sender, eoa, rpcUrl);
  check(
    fresh.factory === null && fresh.factoryData === null,
    'fresh eth_getCode=0xcafe → no initCode (self-heals once node catches up)',
  );

  restoreFetch(ctl);
}

// ---------------------------------------------------------------------------
// Scenario 4: factory address is the canonical SimpleAccountFactory
// ---------------------------------------------------------------------------
//
// When initCode IS returned, the factory field must be the address the
// EntryPoint expects (from @totalreclaw/core getSimpleAccountFactory).
// We assert it is a 20-byte hex address — not the EOA, not the sender.

{
  __resetDeployedAccountsForTests();
  __resetRpcProbeCountForTests();
  const ctl = installFetchMock();
  ctl.codeResponses.push('0x');

  const sender = '0x1111111111111111111111111111111111111111';
  const eoa    = '0x2222222222222222222222222222222222222222';
  const rpcUrl = 'http://localhost:0/rpc';

  const { factory, factoryData } = await __getInitCodeForTests(sender, eoa, rpcUrl);

  check(factory !== null && factory!.length === 42, 'factory is a 0x + 20-byte address');
  check(
    factory!.toLowerCase() !== sender.toLowerCase() &&
      factory!.toLowerCase() !== eoa.toLowerCase(),
    'factory is neither the sender nor the EOA',
  );
  check(
    factoryData !== null && factoryData!.length > 10,
    'factoryData is non-empty calldata',
  );
  // createAccount(address,uint256) selector is 0x5fbfb9cf — first 10 chars.
  check(
    factoryData!.toLowerCase().startsWith('0x5fbfb9cf'),
    'factoryData encodes createAccount(address,uint256) selector',
  );

  restoreFetch(ctl);
}

// ---------------------------------------------------------------------------
// Scenario 5: AA10 'sender already constructed' at pm_sponsorUserOperation → retry succeeds
// ---------------------------------------------------------------------------
//
// This test drives the REAL submitFactBatchOnChain through a simulated AA10
// failure at the pm_sponsorUserOperation RPC call. The root cause being fixed:
//   - eth_getCode returns stale '0x' (Smart Account already deployed but RPC hasn't caught up)
//   - getInitCode returns factory + factoryData
//   - pm_sponsorUserOperation is called WITH initCode on a deployed sender
//   - Bundler simulation rejects with AA10 "sender already constructed"
//   - Current code: NO retry (pm_sponsorUserOperation is outside the AA10 try/catch)
//   - Fixed code: wrap pm_sponsorUserOperation in retry, force-deploy sender, rebuild UserOp without initCode
//
// This test:
//   1. Mocks WASM (deriveEoa, encodeBatchCall, hashUserOp, signUserOp, getEntryPointAddress)
//   2. Mocks global fetch to record all RPC calls and return staged responses
//   3. Calls submitFactBatchOnChain with a real mnemonic
//   4. First pm_sponsorUserOperation returns AA10 error
//   5. Second pm_sponsorUserOperation succeeds (initCode omitted)
//   6. Asserts: result.success===true, exactly 2 pm_sponsorUserOperation calls, 2nd UserOp has no factory field

{
  __resetDeployedAccountsForTests();
  __resetRpcProbeCountForTests();

  // Install fetch mock to record all RPC requests and return staged responses
  const ctl = installFetchMock();

  // Mock WASM module with minimal stubs
  const mockWasm = {
    deriveEoa: () => ({ private_key: '0x' + 'a'.repeat(64), address: '0xbbbb' + 'b'.repeat(36) }),
    encodeBatchCall: () => new Uint8Array([1, 2, 3]), // dummy batch calldata
    getEntryPointAddress: () => '0x5FF137D4b0FD9490299197e9fB6f7936EF32a416',
    hashUserOp: () => '0x' + 'c'.repeat(64),
    signUserOp: () => 'd'.repeat(128),
    getSimpleAccountFactory: () => '0x9406Cc6185a346906296840746125A0E4493a848',
    getDataEdgeAddress: () => '0x' + 'e'.repeat(40),
  };

  // Inject mock WASM
  __setWasmForTests(mockWasm);

  // Helper to stage a response for a specific RPC method
  function stageResponse(method: string, result: any, error?: { message: string }) {
    if (!ctl.responseQueue.has(method)) {
      ctl.responseQueue.set(method, []);
    }
    ctl.responseQueue.get(method)!.push({ result, error });
  }

  // First eth_getCode: stale '0x' (SA deployed but RPC hasn't caught up)
  stageResponse('eth_getCode', '0x');

  // Gas price
  stageResponse('pimlico_getUserOperationGasPrice', { fast: { maxFeePerGas: '0x1', maxPriorityFeePerGas: '0x1' } });

  // eth_call for nonce
  stageResponse('eth_call', '0x0');

  // eth_estimateUserOperationGas (batch estimation)
  stageResponse('eth_estimateUserOperationGas', { callGasLimit: '0x10000', verificationGasLimit: '0x10000', preVerificationGas: '0x10000' });

  // First pm_sponsorUserOperation: AA10 error (sender already constructed)
  stageResponse('pm_sponsorUserOperation', null, { message: 'AA10 sender already constructed' });

  // Second eth_getCode (retry path): now returns deployed code
  stageResponse('eth_getCode', '0x1234');

  // Second pm_sponsorUserOperation: success (no AA10 because initCode is omitted)
  stageResponse('pm_sponsorUserOperation', { callGasLimit: '0x10000', verificationGasLimit: '0x10000', preVerificationGas: '0x10000', paymaster: '0x' + 'f'.repeat(40), paymasterData: '0x' });

  // eth_call for nonce (retry)
  stageResponse('eth_call', '0x0');

  // eth_sendUserOperation
  stageResponse('eth_sendUserOperation', '0x' + 'g'.repeat(64));

  // eth_getUserOperationReceipt
  stageResponse('eth_getUserOperationReceipt', { success: true, receipt: { transactionHash: '0xabc' } });

  // Import submitFactBatchOnChain and call it
  const { submitFactBatchOnChain } = await import('./subgraph-store.js');

  const config = {
    relayUrl: 'http://dummy-relay/v1',
    mnemonic: 'test test test test test test test test test test test junk',
    walletAddress: '0xaaaa' + 'a'.repeat(36),
    chainId: 100,
    entryPointAddress: '0x5FF137D4b0FD9490299197e9fB6f7936EF32a416',
    cachePath: '',
    dataEdgeAddress: '0x' + 'e'.repeat(40),
  };

  const payloads = [Buffer.from([1]), Buffer.from([2])];

  try {
    const result = await submitFactBatchOnChain(payloads, config);

    // Assert success
    check(result.success === true, 'AA10 retry path: batch submission succeeds after retry');

    // Assert exactly 2 pm_sponsorUserOperation calls (first AA10, second success)
    const sponsorCalls = ctl.requests.filter(r => r.method === 'pm_sponsorUserOperation');
    check(sponsorCalls.length === 2, `AA10 retry path: 2 pm_sponsorUserOperation calls (got ${sponsorCalls.length})`);

    // Assert second pm_sponsorUserOperation UserOp has NO factory field (initCode omitted)
    if (sponsorCalls.length >= 2) {
      const secondUserOp = sponsorCalls[1].params?.[0];
      const hasFactory = secondUserOp && 'factory' in secondUserOp && secondUserOp.factory !== null;
      check(!hasFactory, 'AA10 retry path: 2nd pm_sponsorUserOperation UserOp has NO factory field');
    } else {
      check(false, 'AA10 retry path: need 2 sponsor calls to check factory field');
    }
  } catch (err: any) {
    // Current code will fail here — expected before fix
    check(false, `AA10 retry path: should succeed after retry, got error: ${err.message}`);
  } finally {
    // Cleanup
    restoreFetch(ctl);
    __clearWasmForTests();
  }
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
