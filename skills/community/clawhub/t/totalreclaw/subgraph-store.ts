/**
 * Subgraph store path — writes facts on-chain via ERC-4337 UserOps.
 *
 * Used when the managed service is active (TOTALRECLAW_SELF_HOSTED is not
 * "true"). Replaces the HTTP request to /v1/store with an on-chain transaction
 * flow.
 *
 * Uses @totalreclaw/core WASM for calldata encoding and UserOp hashing;
 * `signUserOp` (ECDSA) lives in `vault-crypto.ts`. All JSON-RPC calls to
 * the relay bundler and chain RPCs go through `relay.ts` (the plugin's
 * single network site). No viem, no permissionless.
 */

// Lazy-load WASM via createRequire — the shipped bundle is ESM-only and
// the bare `require` global is undefined there (issue #124). Same pattern
// as crypto / lsh / claims-helper / consolidation / digest-sync.
import { createRequire } from 'node:module';
const requireWasm = createRequire(import.meta.url);
let _wasm: typeof import('@totalreclaw/core') | null = null;
function getWasm() {
  if (!_wasm) _wasm = requireWasm('@totalreclaw/core');
  return _wasm;
}
import { CONFIG } from './config.js';
import { buildRelayHeaders } from './relay-headers.js';
import { rpcRequest, rpcWithRetry } from './relay.js';
import { signUserOp } from './vault-crypto.js';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

export interface SubgraphStoreConfig {
  relayUrl: string;           // TotalReclaw relay server URL (proxies bundler + subgraph)
  mnemonic: string;           // BIP-39 mnemonic for key derivation
  cachePath: string;          // Hot cache file path
  chainId: number;            // 100 for Gnosis mainnet, 84532 for Base Sepolia
  dataEdgeAddress: string;    // EventfulDataEdge contract address
  entryPointAddress: string;  // ERC-4337 EntryPoint v0.7
  authKeyHex?: string;        // HKDF auth key for relay server Authorization header
  rpcUrl?: string;            // Override chain RPC URL for public client reads
  walletAddress?: string;     // Smart Account address for billing (X-Wallet-Address header)
}

export interface FactPayload {
  id: string;
  timestamp: string;
  owner: string;           // Smart Account address (hex)
  encryptedBlob: string;   // Hex-encoded XChaCha20-Poly1305 ciphertext
  blindIndices: string[];   // SHA-256 hashes (word + LSH)
  decayScore: number;
  source: string;
  contentFp: string;
  agentId: string;
  encryptedEmbedding?: string;
  /**
   * Outer protobuf schema version. Plugin v3.0.0 writes Memory Taxonomy v1
   * JSON inner blobs, so this defaults to `PROTOBUF_VERSION_V4` (4). Omitting
   * the field (or passing 0) yields the legacy `DEFAULT_PROTOBUF_VERSION`
   * (3), which is retained so tombstone rows stay wire-compatible with
   * pre-v3 readers if ever needed.
   */
  version?: number;
}

/** Legacy protobuf wrapper schema version (v0/v1-binary inner blob). */
export const PROTOBUF_VERSION_LEGACY = 3;

/** Memory Taxonomy v1 protobuf wrapper schema version. */
export const PROTOBUF_VERSION_V4 = 4;

// Stub 65-byte signature for gas estimation (pm_sponsorUserOperation).
// Must be a structurally valid ECDSA signature (r,s,v) so that ecrecover does
// NOT revert inside SimpleAccount._validateSignature.  All-zeros causes
// OpenZeppelin ECDSA.recover() to revert with ECDSAInvalidSignature() (0xf645eedf),
// which the EntryPoint surfaces as AA23.
// This matches the stub used by permissionless/viem — ecrecover returns a
// non-owner address, so validateUserOp returns SIG_VALIDATION_FAILED (1)
// instead of reverting, which is what bundlers expect during simulation.
const DUMMY_SIGNATURE =
  '0xfffffffffffffffffffffffffffffff0000000000000000000000000000000007aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1c';

// ---------------------------------------------------------------------------
// Protobuf encoding (WASM)
// ---------------------------------------------------------------------------

/**
 * Encode a fact payload as a minimal Protobuf wire format via WASM core.
 *
 * Field numbers match server/proto/totalreclaw.proto.
 *
 * As of plugin v3.0.0 the outer protobuf `version` field is written as 4
 * when the caller passes `version: PROTOBUF_VERSION_V4`. Omitting the field
 * preserves legacy v3 semantics (e.g. for tombstone tombstone rows that
 * should round-trip through pre-v3 readers).
 */
export function encodeFactProtobuf(fact: FactPayload): Buffer {
  const json = JSON.stringify({
    id: fact.id,
    timestamp: fact.timestamp,
    owner: fact.owner,
    encrypted_blob_hex: fact.encryptedBlob,
    blind_indices: fact.blindIndices,
    decay_score: fact.decayScore,
    source: fact.source,
    content_fp: fact.contentFp,
    agent_id: fact.agentId,
    encrypted_embedding: fact.encryptedEmbedding || null,
    version: fact.version ?? PROTOBUF_VERSION_LEGACY,
  });
  return Buffer.from(getWasm().encodeFactProtobuf(json));
}

// ---------------------------------------------------------------------------
// Chain helpers
// ---------------------------------------------------------------------------

/** Get the default public RPC URL for a chain ID */
function getDefaultRpcUrl(chainId: number): string {
  switch (chainId) {
    case 100:
      return 'https://rpc.gnosischain.com';
    case 84532:
      return 'https://sepolia.base.org';
    default:
      return 'https://sepolia.base.org';
  }
}

// ---------------------------------------------------------------------------
// Smart Account address derivation
// ---------------------------------------------------------------------------

/**
 * Derive the Smart Account address from a BIP-39 mnemonic.
 *
 * Uses the SimpleAccountFactory's getAddress(owner, salt=0) view function
 * via a raw eth_call to the chain RPC. The address is deterministic (CREATE2).
 */
export async function deriveSmartAccountAddress(mnemonic: string, chainId?: number): Promise<string> {
  const eoa = getWasm().deriveEoa(mnemonic) as { private_key: string; address: string };
  const resolvedChainId = chainId ?? 84532;

  // SimpleAccountFactory.getAddress(address owner, uint256 salt) — view function
  // Selector: 0x8cb84e18 = keccak256("getAddress(address,uint256)")[0:4]
  const factoryAddress = getWasm().getSimpleAccountFactory();
  const ownerPadded = eoa.address.slice(2).toLowerCase().padStart(64, '0');
  const saltPadded = '0'.repeat(64);
  const selector = '8cb84e18';
  const calldata = `0x${selector}${ownerPadded}${saltPadded}`;

  const rpcUrl = CONFIG.rpcUrl || getDefaultRpcUrl(resolvedChainId);
  const json = await rpcRequest({
    url: rpcUrl,
    headers: { 'Content-Type': 'application/json' },
    method: 'eth_call',
    params: [{ to: factoryAddress, data: calldata }, 'latest'],
  });
  if (json.error) {
    throw new Error(`Failed to resolve Smart Account address: ${json.error.message}`);
  }
  if (!json.result || json.result === '0x') {
    throw new Error('Failed to resolve Smart Account address: empty result');
  }
  // Result is a 32-byte ABI-encoded address — take last 20 bytes
  return `0x${(json.result as string).slice(-40)}`.toLowerCase();
}

// ---------------------------------------------------------------------------
// Smart Account deployment check
// ---------------------------------------------------------------------------
//
// NOTE on the removed session cache (2026-06-28, AA10 fix):
//
// A module-level `Set<string>` of "already deployed" accounts used to skip
// the `eth_getCode` RPC after the first successful submission. That cache
// was the single largest source of AA10 "sender already constructed"
// failures in production:
//
//   - A process restart emptied the cache → the next submission relied on
//     ONE `eth_getCode` read that could return stale `0x` from a lagging
//     RPC node (the deploy tx was mined but the node hadn't caught up) →
//     initCode was re-added → the EntryPoint rejected with AA10.
//   - A receipt poll that timed out (success undetected within the 120s
//     window) left the cache unpopulated → the next submission hit the
//     same stale-`eth_getCode` path → AA10.
//   - The AA25 retry path (`deployedAccounts.delete(...)`) existed ONLY to
//     paper over the cache; with no cache there is nothing to invalidate.
//
// Fix: `getInitCode` calls `eth_getCode` on EVERY invocation. The
// per-sender submission mutex (`withSenderLock`) already serializes
// submissions per account, so the extra RPC cannot introduce a nonce
// race. The cost is one extra RPC read per submission — negligible
// against a relay round-trip — and the behavior is correct by
// construction: the plugin asserts on-chain state at submit time rather
// than trusting an in-memory guess that can be invalidated by anything
// the plugin doesn't observe (relayer retries, parallel clients, node
// reorgs, process restarts).

/**
 * Test-only RPC probe counter. Incremented each time `getInitCode` issues
 * an `eth_getCode` read. The lifecycle test uses this to assert the cache
 * is truly gone (every call hits the wire). Not part of the public API.
 */
let _ethGetCodeProbeCount = 0;

/** Test-only seam: drive the private `getInitCode` logic. */
export async function __getInitCodeForTests(
  sender: string,
  eoaAddress: string,
  rpcUrl: string,
): Promise<{ factory: string | null; factoryData: string | null }> {
  return getInitCode(sender, eoaAddress, rpcUrl);
}

/** Test-only seam: read the RPC probe counter. */
export function __getRpcProbeCountForTests(): number {
  return _ethGetCodeProbeCount;
}

/** Test-only seam: reset the RPC probe counter. */
export function __resetRpcProbeCountForTests(): void {
  _ethGetCodeProbeCount = 0;
}

/**
 * Test-only seam: previously reset the deployment cache. The cache was
 * removed in the AA10 fix; this function is retained as a no-op so the
 * lifecycle test (and any future test that imports it) doesn't break.
 */
export function __resetDeployedAccountsForTests(): void {
  /* no-op: session cache removed; getInitCode always re-checks eth_getCode */
}

// ---------------------------------------------------------------------------
// Per-account submission mutex — 3.3.1-rc.3 AA25 serialization
// ---------------------------------------------------------------------------
//
// Concurrent `submitFactOnChain` / `submitFactBatchOnChain` calls for the
// SAME Smart Account used to race at the nonce-fetch step:
//   - Call A: getNonce()=5, build UserOp, submit, wait for receipt.
//   - Call B: getNonce()=5 (A not mined yet), build UserOp, submit → AA25.
//
// The fix: chain submissions per `sender` address through a single promise.
// Each call awaits the previous in-flight submission before starting its
// own nonce fetch. Fallback to public RPC for getNonce continues to work
// because by the time B fetches, A's UserOp has been bundled AND mined.
//
// 16 AA25 occurrences were logged in rc.2 QA; this lock eliminates the
// race condition at the plugin layer. Subsequent AA25s would indicate
// nonce rot from another process (e.g. relay retrying the same UserOp)
// and are handled by the existing single-retry with fresh-nonce path.
const _senderSubmissionLocks = new Map<string, Promise<unknown>>();

async function withSenderLock<T>(sender: string, fn: () => Promise<T>): Promise<T> {
  const key = sender.toLowerCase();
  const prev = _senderSubmissionLocks.get(key) ?? Promise.resolve();
  let release: () => void = () => {};
  const thisCallGate = new Promise<void>((resolve) => { release = resolve; });
  _senderSubmissionLocks.set(key, prev.then(() => thisCallGate));
  try {
    await prev; // wait for previous submission to settle (success OR failure)
  } catch {
    // Prior submission threw — that's the caller's problem, not ours.
    // The lock is still released below; we re-enter the chain.
  }
  try {
    return await fn();
  } finally {
    release();
    // If we're the tail of the chain, clean up to avoid unbounded memory.
    // Use `===` to ensure we don't clobber a newer lock that joined while
    // we were running.
    const current = _senderSubmissionLocks.get(key);
    // The lock we set above was `prev.then(() => thisCallGate)` — when
    // `thisCallGate` resolves, the whole promise resolves. If nothing
    // queued behind us, remove the entry.
    if (current) {
      current.then(() => {
        if (_senderSubmissionLocks.get(key) === current) {
          _senderSubmissionLocks.delete(key);
        }
      }).catch(() => {
        if (_senderSubmissionLocks.get(key) === current) {
          _senderSubmissionLocks.delete(key);
        }
      });
    }
  }
}

/** Exposed for tests — reset the per-account lock map. */
export function __resetSenderLocksForTests(): void {
  _senderSubmissionLocks.clear();
}

// ---------------------------------------------------------------------------
// Test-only WASM mock seams (AA10 submit-path retry test)
// ---------------------------------------------------------------------------

/**
 * Test-only seam: inject a mock WASM module.
 *
 * The AA10 submit-path retry test needs to drive the real submitFactBatchOnChain
 * while controlling WASM behavior (deriveEoa, encodeBatchCall, hashUserOp,
 * signUserOp, getEntryPointAddress). This seam swaps the module-level _wasm
 * reference so the test can provide stubs.
 *
 * MUST be followed by __clearWasmForTests() in teardown.
 */
export function __setWasmForTests(mock: any): void {
  _wasm = mock;
}

/**
 * Test-only seam: restore the real WASM module.
 *
 * Clears a test-injected mock WASM and resets the module to null so the next
 * getWasm() call reloads the real @totalreclaw/core.
 */
export function __clearWasmForTests(): void {
  _wasm = null;
}

/**
 * Check if a Smart Account is deployed and return factory/factoryData if not.
 *
 * For ERC-4337 v0.7, undeployed (counterfactual) accounts need `factory`
 * and `factoryData` in the UserOp so the EntryPoint deploys the SA + runs
 * signature validation in one transaction.
 *
 * Re-checks `eth_getCode` on EVERY call — no session cache. The previous
 * in-memory cache was the source of AA10 "sender already constructed"
 * errors: it could be stale (process restart, missed receipt, lagging RPC
 * node) and re-add initCode to a UserOp whose sender was already
 * constructed. Each submission now pays one extra RPC read to assert the
 * on-chain deployment state at submit time, which is the only source of
 * truth the EntryPoint will enforce. See the note above on the removed
 * cache for the full failure taxonomy.
 */
async function getInitCode(
  sender: string,
  eoaAddress: string,
  rpcUrl: string,
): Promise<{ factory: string | null; factoryData: string | null }> {
  // Check if the Smart Account contract is deployed. Always re-read — never
  // cache. The per-sender submission mutex serializes calls for the same
  // account, so this cannot race a nonce fetch.
  _ethGetCodeProbeCount++;
  const codeJson = await rpcRequest({
    url: rpcUrl,
    headers: { 'Content-Type': 'application/json' },
    method: 'eth_getCode',
    params: [sender, 'latest'],
  });
  const codeResult = codeJson.result as string | undefined;
  const isDeployed = codeResult && codeResult !== '0x' && codeResult !== '0x0';

  if (isDeployed) {
    return { factory: null, factoryData: null };
  }

  // Account not deployed — build factory + factoryData for first-time deployment.
  // createAccount(address owner, uint256 salt) — state-changing function
  // Selector: 0x5fbfb9cf = keccak256("createAccount(address,uint256)")[0:4]
  const factory = getWasm().getSimpleAccountFactory();
  const ownerPadded = eoaAddress.slice(2).toLowerCase().padStart(64, '0');
  const saltPadded = '0'.repeat(64);
  const selector = '5fbfb9cf';
  const factoryData = `0x${selector}${ownerPadded}${saltPadded}`;

  return { factory, factoryData };
}

// ---------------------------------------------------------------------------
// On-chain submission (ERC-4337 UserOps via relay.ts network site)
// ---------------------------------------------------------------------------

/**
 * Submit a fact on-chain via ERC-4337 UserOp through the relay server.
 *
 * Uses @totalreclaw/core WASM for:
 * 1. EOA derivation from mnemonic (BIP-39 + BIP-44)
 * 2. Calldata encoding (SimpleAccount.execute)
 * 3. UserOp hashing (ERC-4337 v0.7)
 * 4. ECDSA signing (EIP-191 prefixed)
 *
 * All JSON-RPC calls go through `relay.ts` to the relay bundler endpoint.
 */
export async function submitFactOnChain(
  protobufPayload: Buffer,
  config: SubgraphStoreConfig,
): Promise<{ txHash: string; userOpHash: string; success: boolean }> {
  if (!config.relayUrl) {
    throw new Error('Relay URL (TOTALRECLAW_SERVER_URL) is required for on-chain submission');
  }

  if (!config.mnemonic) {
    throw new Error('Recovery phrase (TOTALRECLAW_RECOVERY_PHRASE) is required for on-chain submission');
  }

  // Resolve sender up-front so we can serialize concurrent submissions for
  // the SAME Smart Account (rc.3 AA25 fix). Derivation is CREATE2, so we
  // don't need to hit the chain — WASM does it.
  const eoa = getWasm().deriveEoa(config.mnemonic) as { private_key: string; address: string };
  const sender = config.walletAddress || await deriveSmartAccountAddress(config.mnemonic, config.chainId);

  return withSenderLock(sender, () => submitFactOnChainLocked(
    protobufPayload, config, eoa, sender,
  ));
}

async function submitFactOnChainLocked(
  protobufPayload: Buffer,
  config: SubgraphStoreConfig,
  eoa: { private_key: string; address: string },
  sender: string,
): Promise<{ txHash: string; userOpHash: string; success: boolean }> {
  const bundlerUrl = `${config.relayUrl}/v1/bundler`;
  const overrides: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (config.authKeyHex) overrides['Authorization'] = `Bearer ${config.authKeyHex}`;
  if (config.walletAddress) overrides['X-Wallet-Address'] = config.walletAddress;
  const headers = buildRelayHeaders(overrides);

  // Helper for JSON-RPC calls to relay bundler (with 429 retry)
  async function rpc(method: string, params: unknown[]): Promise<any> {
    return rpcWithRetry({ url: bundlerUrl, headers, method, params });
  }

  const entryPoint = config.entryPointAddress || getWasm().getEntryPointAddress();

  // 2. Encode calldata (SimpleAccount.execute → DataEdge fallback)
  const calldataBytes = getWasm().encodeSingleCall(protobufPayload);
  const callData = `0x${Buffer.from(calldataBytes).toString('hex')}`;

  // 3. Get gas prices from Pimlico
  const gasPrices = await rpc('pimlico_getUserOperationGasPrice', []);
  const fast = gasPrices.fast;

  const rpcUrl = config.rpcUrl || CONFIG.rpcUrl || getDefaultRpcUrl(config.chainId);

  // 5. Get nonce from EntryPoint via bundler RPC.
  //    Routing through the bundler lets Pimlico account for pending mempool
  //    UserOps, preventing AA25 nonce conflicts on rapid submissions.
  //    Requires relay allowlist to include eth_call (added in relay v1.x).
  //    Fallback: if bundler rejects eth_call (403/method_not_allowed), use public RPC.
  //    getNonce(address sender, uint192 key) — selector 0x35567e1a
  const senderPadded = sender.slice(2).toLowerCase().padStart(64, '0');
  const keyPadded = '0'.repeat(64);
  const nonceCalldata = `0x35567e1a${senderPadded}${keyPadded}`;

  // Helper to fetch nonce (with bundler fallback)
  async function fetchNonce(): Promise<string> {
    try {
      const nonceResult = await rpc('eth_call', [{ to: entryPoint, data: nonceCalldata }, 'latest']);
      return nonceResult || '0x0';
    } catch {
      // Fallback to public RPC if bundler doesn't support eth_call
      const nonceJson = await rpcRequest({
        url: rpcUrl,
        headers: { 'Content-Type': 'application/json' },
        method: 'eth_call',
        params: [{ to: entryPoint, data: nonceCalldata }, 'latest'],
      });
      return (nonceJson.result as string) || '0x0';
    }
  }

  // Track force-deployed senders for AA10 retry (local to this submission attempt)
  const forceDeployed = new Set<string>();

  // Single retry loop: getInitCode → build UserOp → sponsor → sign → send
  // On AA10 "sender already constructed", mark sender as force-deployed and retry.
  // AA10 can occur at pm_sponsorUserOperation (initCode present on deployed sender)
  // or eth_sendUserOperation (same root cause). This loop handles both.
  let userOpHash: string;
  let attempt = 0;
  const maxAttempts = 2;

  while (attempt < maxAttempts) {
    attempt++;

    try {
      // 4. Check if Smart Account is deployed (needed for factory/factoryData)
      // If force-deployed, skip eth_getCode and return null initCode.
      let factory: string | null = null;
      let factoryData: string | null = null;
      if (!forceDeployed.has(sender.toLowerCase())) {
        const initCode = await getInitCode(sender, eoa.address, rpcUrl);
        factory = initCode.factory;
        factoryData = initCode.factoryData;
      }

      // Fetch fresh nonce for each attempt
      const nonce = await fetchNonce();

      // 6. Build unsigned UserOp (v0.7 fields, camelCase for Rust JSON serde)
      const unsignedOp: Record<string, any> = {
        sender,
        nonce,
        callData,
        callGasLimit: '0x0',
        verificationGasLimit: '0x0',
        preVerificationGas: '0x0',
        maxFeePerGas: fast.maxFeePerGas,
        maxPriorityFeePerGas: fast.maxPriorityFeePerGas,
        signature: DUMMY_SIGNATURE,
      };
      if (factory) {
        unsignedOp.factory = factory;
        unsignedOp.factoryData = factoryData;
      }

      // 7. Get paymaster sponsorship (fills gas limits + paymaster fields)
      // This is where AA10 "sender already constructed" can occur if initCode
      // is present but the sender is already deployed.
      const sponsorResult = await rpc('pm_sponsorUserOperation', [unsignedOp, entryPoint]);
      Object.assign(unsignedOp, sponsorResult);

      // 8. Hash and sign the UserOp via WASM
      const opJson = JSON.stringify(unsignedOp);
      const hashHex = getWasm().hashUserOp(opJson, entryPoint, BigInt(config.chainId));
      const sigHex = signUserOp(hashHex, eoa.private_key);
      unsignedOp.signature = `0x${sigHex}`;

      // 9. Submit the signed UserOp
      userOpHash = await rpc('eth_sendUserOperation', [unsignedOp, entryPoint]);
      // Success — break out of retry loop
      break;
    } catch (err: any) {
      const msg = err?.message || '';
      // AA10 "sender already constructed" or AA25 invalid nonce → retry
      if (/AA25|AA10|invalid account nonce|already being processed/i.test(msg)) {
        console.error(`AA25/AA10 detected (attempt ${attempt}/${maxAttempts}), retrying...`);
        // On AA10, force-mark sender as deployed so next retry omits initCode
        if (/AA10/i.test(msg)) {
          forceDeployed.add(sender.toLowerCase());
          console.error('AA10: force-marking sender as deployed, retrying without initCode');
        }
        // Wait for previous UserOp to mine before retrying with fresh nonce.
        // Public RPC won't reflect the new nonce until the tx is on-chain.
        await new Promise(r => setTimeout(r, 15000));
        // Continue to next iteration of retry loop
        continue;
      }
      // Not a retryable error — re-throw
      throw err;
    }
  }

  // 10. Wait for receipt (poll up to 120s)
  let receipt = null;
  for (let i = 0; i < 60; i++) {
    await new Promise(r => setTimeout(r, 2000));
    try {
      receipt = await rpc('eth_getUserOperationReceipt', [userOpHash]);
      if (receipt) break;
    } catch { /* not mined yet */ }
  }

  const success = receipt?.success ?? false;

  // No session-deployment cache to update — getInitCode always re-checks
  // eth_getCode on the next submission, so a successful receipt needs no
  // bookkeeping here. (Previous cache removed in the AA10 fix — see note
  // at the top of this section.)

  return {
    txHash: receipt?.receipt?.transactionHash || '',
    userOpHash,
    success,
  };
}

/**
 * Submit multiple facts on-chain in a single ERC-4337 UserOp (batched).
 *
 * Each protobuf payload becomes one call in a multi-call UserOp. The
 * DataEdge contract emits a separate Log(bytes) event per call, and the
 * subgraph indexes each event independently (by txHash + logIndex).
 *
 * Falls back to single-fact path for batches of 1 (no multicall overhead).
 */
export async function submitFactBatchOnChain(
  protobufPayloads: Buffer[],
  config: SubgraphStoreConfig,
): Promise<{ txHash: string; userOpHash: string; success: boolean; batchSize: number }> {
  if (!protobufPayloads.length) {
    return { txHash: '', userOpHash: '', success: true, batchSize: 0 };
  }

  // Single fact — use standard path (avoids multicall overhead)
  if (protobufPayloads.length === 1) {
    const result = await submitFactOnChain(protobufPayloads[0], config);
    return { ...result, batchSize: 1 };
  }

  if (!config.relayUrl) {
    throw new Error('Relay URL (TOTALRECLAW_SERVER_URL) is required for on-chain submission');
  }
  if (!config.mnemonic) {
    throw new Error('Recovery phrase (TOTALRECLAW_RECOVERY_PHRASE) is required for on-chain submission');
  }

  // Resolve sender up-front for the per-account mutex (rc.3 AA25 fix).
  const eoa = getWasm().deriveEoa(config.mnemonic) as { private_key: string; address: string };
  const sender = config.walletAddress || await deriveSmartAccountAddress(config.mnemonic, config.chainId);

  return withSenderLock(sender, () => submitFactBatchOnChainLocked(
    protobufPayloads, config, eoa, sender,
  ));
}

async function submitFactBatchOnChainLocked(
  protobufPayloads: Buffer[],
  config: SubgraphStoreConfig,
  eoa: { private_key: string; address: string },
  sender: string,
): Promise<{ txHash: string; userOpHash: string; success: boolean; batchSize: number }> {
  const bundlerUrl = `${config.relayUrl}/v1/bundler`;
  const overrides: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (config.authKeyHex) overrides['Authorization'] = `Bearer ${config.authKeyHex}`;
  if (config.walletAddress) overrides['X-Wallet-Address'] = config.walletAddress;
  const headers = buildRelayHeaders(overrides);

  // Helper for JSON-RPC calls to relay bundler (with 429 retry)
  async function rpc(method: string, params: unknown[]): Promise<any> {
    return rpcWithRetry({ url: bundlerUrl, headers, method, params });
  }
  const entryPoint = config.entryPointAddress || getWasm().getEntryPointAddress();

  // Encode batch calldata (SimpleAccount.executeBatch)
  // encodeBatchCall expects a JSON array of hex-encoded payload strings
  const payloadsHex = protobufPayloads.map(p => p.toString('hex'));
  const calldataBytes = getWasm().encodeBatchCall(JSON.stringify(payloadsHex));
  const callData = `0x${Buffer.from(calldataBytes).toString('hex')}`;

  // Get gas prices
  const gasPrices = await rpc('pimlico_getUserOperationGasPrice', []);
  const fast = gasPrices.fast;

  const rpcUrl = config.rpcUrl || CONFIG.rpcUrl || getDefaultRpcUrl(config.chainId);

  // Get nonce via bundler (accounts for pending mempool UserOps) with public RPC fallback
  const senderPadded = sender.slice(2).toLowerCase().padStart(64, '0');
  const keyPadded = '0'.repeat(64);
  const nonceCalldata = `0x35567e1a${senderPadded}${keyPadded}`;

  // Helper to fetch nonce (with bundler fallback)
  async function fetchNonce(): Promise<string> {
    try {
      const nonceResult = await rpc('eth_call', [{ to: entryPoint, data: nonceCalldata }, 'latest']);
      return nonceResult || '0x0';
    } catch {
      const nonceJson = await rpcRequest({
        url: rpcUrl,
        headers: { 'Content-Type': 'application/json' },
        method: 'eth_call',
        params: [{ to: entryPoint, data: nonceCalldata }, 'latest'],
      });
      return (nonceJson.result as string) || '0x0';
    }
  }

  // Track force-deployed senders for AA10 retry (local to this submission attempt)
  const forceDeployed = new Set<string>();

  // Single retry loop: getInitCode → build UserOp → estimate → sponsor → sign → send
  // On AA10 "sender already constructed", mark sender as force-deployed and retry.
  let userOpHash: string;
  let attempt = 0;
  const maxAttempts = 2;

  while (attempt < maxAttempts) {
    attempt++;

    try {
      // Check if Smart Account is deployed (needed for factory/factoryData)
      // If force-deployed, skip eth_getCode and return null initCode.
      let factory: string | null = null;
      let factoryData: string | null = null;
      if (!forceDeployed.has(sender.toLowerCase())) {
        const initCode = await getInitCode(sender, eoa.address, rpcUrl);
        factory = initCode.factory;
        factoryData = initCode.factoryData;
      }

      // Fetch fresh nonce for each attempt
      const nonce = await fetchNonce();

      // Build unsigned UserOp
      const unsignedOp: Record<string, any> = {
        sender,
        nonce,
        callData,
        callGasLimit: '0x0',
        verificationGasLimit: '0x0',
        preVerificationGas: '0x0',
        maxFeePerGas: fast.maxFeePerGas,
        maxPriorityFeePerGas: fast.maxPriorityFeePerGas,
        signature: DUMMY_SIGNATURE,
      };
      if (factory) {
        unsignedOp.factory = factory;
        unsignedOp.factoryData = factoryData;
      }

      // Gas estimation for batch operations — get accurate gas limits from Pimlico
      // before paymaster sponsorship (can't bump after sponsorship as it invalidates
      // the paymaster's signature, causing AA34).
      if (protobufPayloads.length > 1) {
        try {
          const gasEstimate = await rpc('eth_estimateUserOperationGas', [unsignedOp, entryPoint]);
          if (gasEstimate.callGasLimit) unsignedOp.callGasLimit = gasEstimate.callGasLimit;
          if (gasEstimate.verificationGasLimit) unsignedOp.verificationGasLimit = gasEstimate.verificationGasLimit;
          if (gasEstimate.preVerificationGas) unsignedOp.preVerificationGas = gasEstimate.preVerificationGas;
        } catch {
          // If estimation fails, let the paymaster handle it (default behavior)
        }
      }

      // Paymaster sponsorship (uses gas limits from estimation above for batches)
      // This is where AA10 "sender already constructed" can occur if initCode
      // is present but the sender is already deployed.
      const sponsorResult = await rpc('pm_sponsorUserOperation', [unsignedOp, entryPoint]);
      Object.assign(unsignedOp, sponsorResult);

      // Hash and sign via WASM
      const opJson = JSON.stringify(unsignedOp);
      const hashHex = getWasm().hashUserOp(opJson, entryPoint, BigInt(config.chainId));
      const sigHex = signUserOp(hashHex, eoa.private_key);
      unsignedOp.signature = `0x${sigHex}`;

      // Submit the signed UserOp
      userOpHash = await rpc('eth_sendUserOperation', [unsignedOp, entryPoint]);
      // Success — break out of retry loop
      break;
    } catch (err: any) {
      const msg = err?.message || '';
      // AA10 "sender already constructed" or AA25 invalid nonce → retry
      if (/AA25|AA10|invalid account nonce|already being processed/i.test(msg)) {
        console.error(`AA25/AA10 detected (batch, attempt ${attempt}/${maxAttempts}), retrying...`);
        // On AA10, force-mark sender as deployed so next retry omits initCode
        if (/AA10/i.test(msg)) {
          forceDeployed.add(sender.toLowerCase());
          console.error('AA10: force-marking sender as deployed, retrying without initCode');
        }
        // Wait for previous UserOp to mine before retrying with fresh nonce.
        // Public RPC won't reflect the new nonce until the tx is on-chain.
        await new Promise(r => setTimeout(r, 15000));
        // Continue to next iteration of retry loop
        continue;
      }
      // Not a retryable error — re-throw
      throw err;
    }
  }

  // Wait for receipt (poll up to 120s)
  let receipt = null;
  for (let i = 0; i < 60; i++) {
    await new Promise(r => setTimeout(r, 2000));
    try {
      receipt = await rpc('eth_getUserOperationReceipt', [userOpHash]);
      if (receipt) break;
    } catch { /* not mined yet */ }
  }

  const batchSuccess = receipt?.success ?? false;

  // No session-deployment cache to update — getInitCode always re-checks
  // eth_getCode on the next submission, so a successful receipt needs no
  // bookkeeping here. (Previous cache removed in the AA10 fix — see note
  // at the top of the Smart Account deployment-check section.)

  return {
    txHash: receipt?.receipt?.transactionHash || '',
    userOpHash,
    success: batchSuccess,
    batchSize: protobufPayloads.length,
  };
}

// ---------------------------------------------------------------------------
// Configuration
// ---------------------------------------------------------------------------

/**
 * Check if subgraph mode is enabled (i.e. using the managed service).
 *
 * Returns true when TOTALRECLAW_SELF_HOSTED is NOT set to "true".
 * The managed service (subgraph mode) is the default.
 */
export function isSubgraphMode(): boolean {
  return !CONFIG.selfHosted;
}

/**
 * Get subgraph configuration from environment variables.
 *
 * After the v1 env var cleanup, clients only need:
 *   - TOTALRECLAW_RECOVERY_PHRASE -- BIP-39 mnemonic
 *   - TOTALRECLAW_SERVER_URL -- relay server URL (default: https://api.totalreclaw.xyz; staging via override: https://api-staging.totalreclaw.xyz)
 *   - TOTALRECLAW_SELF_HOSTED -- set "true" to use self-hosted server (default: managed service)
 *
 * Chain ID is no longer configurable via env — it is auto-detected from the
 * relay billing response (free = Base Sepolia, Pro = Gnosis mainnet).
 */
export function getSubgraphConfig(): SubgraphStoreConfig {
  return {
    // 3.3.12-rc.1 (F flip): production default for both release-types.
    relayUrl: CONFIG.serverUrl || 'https://api.totalreclaw.xyz',
    mnemonic: CONFIG.recoveryPhrase,
    cachePath: CONFIG.cachePath,
    chainId: CONFIG.chainId,
    dataEdgeAddress: CONFIG.dataEdgeAddress || getWasm().getDataEdgeAddress(),
    entryPointAddress: CONFIG.entryPointAddress || getWasm().getEntryPointAddress(),
    rpcUrl: CONFIG.rpcUrl || undefined,
  };
}
