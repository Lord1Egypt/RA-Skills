/**
 * Subgraph store path — writes facts on-chain via ERC-4337 UserOps.
 *
 * Used when the managed service is active (TOTALRECLAW_SELF_HOSTED is not
 * "true"). Replaces the HTTP POST to /v1/store with an on-chain transaction
 * flow.
 *
 * Uses @totalreclaw/core WASM for calldata encoding, UserOp hashing, and
 * ECDSA signing. Raw fetch() for all JSON-RPC calls to the relay bundler
 * and chain RPCs. No viem, no permissionless.
 */
// Lazy-load WASM via createRequire — the shipped bundle is ESM-only and
// the bare `require` global is undefined there (issue #124). Same pattern
// as crypto / lsh / claims-helper / consolidation / digest-sync.
import { createRequire } from 'node:module';
const requireWasm = createRequire(import.meta.url);
let _wasm = null;
function getWasm() {
    if (!_wasm)
        _wasm = requireWasm('@totalreclaw/core');
    return _wasm;
}
import { CONFIG } from './config.js';
import { buildRelayHeaders } from './relay-headers.js';
// ---------------------------------------------------------------------------
// Pimlico 429 retry helper
// ---------------------------------------------------------------------------
/**
 * Wrap a fetch-based JSON-RPC call with exponential backoff for HTTP 429
 * (rate limit) responses from Pimlico. Max 5 retries with 5s base delay,
 * doubling each attempt, capped at 60s, plus random jitter (0-1000ms).
 * Total retry window: ~135s (5+10+20+40+60 plus jitter).
 * All other HTTP errors throw immediately.
 */
async function rpcWithRetry(url, headers, method, params) {
    const maxRetries = 5;
    const baseDelay = 5000; // 5 seconds
    const maxDelay = 60_000; // 60 seconds cap
    const body = JSON.stringify({ jsonrpc: '2.0', id: 1, method, params });
    for (let attempt = 1; attempt <= maxRetries + 1; attempt++) {
        const resp = await fetch(url, { method: 'POST', headers, body });
        if (resp.ok) {
            const json = await resp.json();
            if (json.error) {
                // Check if the RPC-level error message indicates a rate limit
                if (attempt <= maxRetries && /429|rate limit/i.test(json.error.message)) {
                    const delay = Math.min(Math.pow(2, attempt - 1) * baseDelay, maxDelay) + Math.floor(Math.random() * 1000);
                    console.error(`Pimlico rate limited, retrying in ${delay}ms (attempt ${attempt}/${maxRetries})...`);
                    await new Promise(r => setTimeout(r, delay));
                    continue;
                }
                throw new Error(`RPC ${method}: ${json.error.message}`);
            }
            return json.result;
        }
        // HTTP-level 429 — retry with backoff
        if (resp.status === 429 && attempt <= maxRetries) {
            const delay = Math.min(Math.pow(2, attempt - 1) * baseDelay, maxDelay) + Math.floor(Math.random() * 1000);
            console.error(`Pimlico rate limited, retrying in ${delay}ms (attempt ${attempt}/${maxRetries})...`);
            await new Promise(r => setTimeout(r, delay));
            continue;
        }
        throw new Error(`Relay returned HTTP ${resp.status} for ${method}`);
    }
    // Should not be reached, but satisfies TypeScript
    throw new Error(`RPC ${method}: max retries exceeded`);
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
const DUMMY_SIGNATURE = '0xfffffffffffffffffffffffffffffff0000000000000000000000000000000007aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa1c';
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
export function encodeFactProtobuf(fact) {
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
function getDefaultRpcUrl(chainId) {
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
export async function deriveSmartAccountAddress(mnemonic, chainId) {
    const eoa = getWasm().deriveEoa(mnemonic);
    const resolvedChainId = chainId ?? 84532;
    // SimpleAccountFactory.getAddress(address owner, uint256 salt) — view function
    // Selector: 0x8cb84e18 = keccak256("getAddress(address,uint256)")[0:4]
    const factoryAddress = getWasm().getSimpleAccountFactory();
    const ownerPadded = eoa.address.slice(2).toLowerCase().padStart(64, '0');
    const saltPadded = '0'.repeat(64);
    const selector = '8cb84e18';
    const calldata = `0x${selector}${ownerPadded}${saltPadded}`;
    const rpcUrl = CONFIG.rpcUrl || getDefaultRpcUrl(resolvedChainId);
    const response = await fetch(rpcUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            jsonrpc: '2.0',
            id: 1,
            method: 'eth_call',
            params: [{ to: factoryAddress, data: calldata }, 'latest'],
        }),
    });
    const json = await response.json();
    if (json.error) {
        throw new Error(`Failed to resolve Smart Account address: ${json.error.message}`);
    }
    if (!json.result || json.result === '0x') {
        throw new Error('Failed to resolve Smart Account address: empty result');
    }
    // Result is a 32-byte ABI-encoded address — take last 20 bytes
    return `0x${json.result.slice(-40)}`.toLowerCase();
}
// ---------------------------------------------------------------------------
// Smart Account deployment check (with session cache)
// ---------------------------------------------------------------------------
/**
 * Session-level cache for account deployment status.
 * Once an account is deployed (first successful UserOp), we skip the
 * eth_getCode check and omit factory/factoryData for all subsequent calls.
 * This prevents AA10 "duplicate deployment" errors when multiple facts
 * are stored in rapid succession for a first-time user.
 */
const deployedAccounts = new Set();
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
const _senderSubmissionLocks = new Map();
async function withSenderLock(sender, fn) {
    const key = sender.toLowerCase();
    const prev = _senderSubmissionLocks.get(key) ?? Promise.resolve();
    let release = () => { };
    const thisCallGate = new Promise((resolve) => { release = resolve; });
    _senderSubmissionLocks.set(key, prev.then(() => thisCallGate));
    try {
        await prev; // wait for previous submission to settle (success OR failure)
    }
    catch {
        // Prior submission threw — that's the caller's problem, not ours.
        // The lock is still released below; we re-enter the chain.
    }
    try {
        return await fn();
    }
    finally {
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
export function __resetSenderLocksForTests() {
    _senderSubmissionLocks.clear();
}
/**
 * Check if a Smart Account is deployed and return factory/factoryData if not.
 *
 * For ERC-4337 v0.7, undeployed accounts need `factory` and `factoryData`
 * in the UserOp so the EntryPoint can deploy them during the first transaction.
 */
async function getInitCode(sender, eoaAddress, rpcUrl) {
    // Session cache: if we already deployed this account, skip the RPC check
    if (deployedAccounts.has(sender.toLowerCase())) {
        return { factory: null, factoryData: null };
    }
    // Check if the Smart Account contract is deployed
    const codeResp = await fetch(rpcUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            jsonrpc: '2.0', id: 1, method: 'eth_getCode',
            params: [sender, 'latest'],
        }),
    });
    const codeJson = await codeResp.json();
    const isDeployed = codeJson.result && codeJson.result !== '0x' && codeJson.result !== '0x0';
    if (isDeployed) {
        deployedAccounts.add(sender.toLowerCase());
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
// On-chain submission (ERC-4337 UserOps via raw fetch)
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
 * All JSON-RPC calls go through raw fetch() to the relay bundler endpoint.
 */
export async function submitFactOnChain(protobufPayload, config) {
    if (!config.relayUrl) {
        throw new Error('Relay URL (TOTALRECLAW_SERVER_URL) is required for on-chain submission');
    }
    if (!config.mnemonic) {
        throw new Error('Recovery phrase (TOTALRECLAW_RECOVERY_PHRASE) is required for on-chain submission');
    }
    // Resolve sender up-front so we can serialize concurrent submissions for
    // the SAME Smart Account (rc.3 AA25 fix). Derivation is CREATE2, so we
    // don't need to hit the chain — WASM does it.
    const eoa = getWasm().deriveEoa(config.mnemonic);
    const sender = config.walletAddress || await deriveSmartAccountAddress(config.mnemonic, config.chainId);
    return withSenderLock(sender, () => submitFactOnChainLocked(protobufPayload, config, eoa, sender));
}
async function submitFactOnChainLocked(protobufPayload, config, eoa, sender) {
    const bundlerUrl = `${config.relayUrl}/v1/bundler`;
    const overrides = {
        'Content-Type': 'application/json',
    };
    if (config.authKeyHex)
        overrides['Authorization'] = `Bearer ${config.authKeyHex}`;
    if (config.walletAddress)
        overrides['X-Wallet-Address'] = config.walletAddress;
    const headers = buildRelayHeaders(overrides);
    // Helper for JSON-RPC calls to relay bundler (with 429 retry)
    async function rpc(method, params) {
        return rpcWithRetry(bundlerUrl, headers, method, params);
    }
    const entryPoint = config.entryPointAddress || getWasm().getEntryPointAddress();
    // 2. Encode calldata (SimpleAccount.execute → DataEdge fallback)
    const calldataBytes = getWasm().encodeSingleCall(protobufPayload);
    const callData = `0x${Buffer.from(calldataBytes).toString('hex')}`;
    // 3. Get gas prices from Pimlico
    const gasPrices = await rpc('pimlico_getUserOperationGasPrice', []);
    const fast = gasPrices.fast;
    const rpcUrl = config.rpcUrl || CONFIG.rpcUrl || getDefaultRpcUrl(config.chainId);
    // 4. Check if Smart Account is deployed (needed for factory/factoryData)
    const { factory, factoryData } = await getInitCode(sender, eoa.address, rpcUrl);
    // 5. Get nonce from EntryPoint via bundler RPC.
    //    Routing through the bundler lets Pimlico account for pending mempool
    //    UserOps, preventing AA25 nonce conflicts on rapid submissions.
    //    Requires relay allowlist to include eth_call (added in relay v1.x).
    //    Fallback: if bundler rejects eth_call (403/method_not_allowed), use public RPC.
    //    getNonce(address sender, uint192 key) — selector 0x35567e1a
    const senderPadded = sender.slice(2).toLowerCase().padStart(64, '0');
    const keyPadded = '0'.repeat(64);
    const nonceCalldata = `0x35567e1a${senderPadded}${keyPadded}`;
    let nonce;
    try {
        const nonceResult = await rpc('eth_call', [{ to: entryPoint, data: nonceCalldata }, 'latest']);
        nonce = nonceResult || '0x0';
    }
    catch {
        // Fallback to public RPC if bundler doesn't support eth_call
        const nonceResp = await fetch(rpcUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0', id: 1, method: 'eth_call',
                params: [{ to: entryPoint, data: nonceCalldata }, 'latest'],
            }),
        });
        const nonceJson = await nonceResp.json();
        nonce = nonceJson.result || '0x0';
    }
    // 6. Build unsigned UserOp (v0.7 fields, camelCase for Rust JSON serde)
    const unsignedOp = {
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
    const sponsorResult = await rpc('pm_sponsorUserOperation', [unsignedOp, entryPoint]);
    Object.assign(unsignedOp, sponsorResult);
    // 8. Hash and sign the UserOp via WASM
    const opJson = JSON.stringify(unsignedOp);
    const hashHex = getWasm().hashUserOp(opJson, entryPoint, BigInt(config.chainId));
    const sigHex = getWasm().signUserOp(hashHex, eoa.private_key);
    unsignedOp.signature = `0x${sigHex}`;
    // 9. Submit the signed UserOp (with AA25 nonce conflict retry)
    let userOpHash;
    try {
        userOpHash = await rpc('eth_sendUserOperation', [unsignedOp, entryPoint]);
    }
    catch (err) {
        const msg = err?.message || '';
        if (/AA25|AA10|invalid account nonce|already being processed/i.test(msg)) {
            console.error('AA25/AA10 nonce conflict detected, rebuilding UserOp with fresh nonce...');
            // Bust deployment cache so getInitCode re-checks on-chain
            deployedAccounts.delete(sender.toLowerCase());
            // Wait for previous UserOp to mine before retrying with fresh nonce.
            // Public RPC won't reflect the new nonce until the tx is on-chain.
            await new Promise(r => setTimeout(r, 15000));
            // Re-fetch initCode and nonce
            const { factory: retryFactory, factoryData: retryFactoryData } = await getInitCode(sender, eoa.address, rpcUrl);
            let retryNonce;
            try {
                const retryNonceResult = await rpc('eth_call', [{ to: entryPoint, data: nonceCalldata }, 'latest']);
                retryNonce = retryNonceResult || '0x0';
            }
            catch {
                const retryNonceResp = await fetch(rpcUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0', id: 1, method: 'eth_call',
                        params: [{ to: entryPoint, data: nonceCalldata }, 'latest'],
                    }),
                });
                const retryNonceJson = await retryNonceResp.json();
                retryNonce = retryNonceJson.result || '0x0';
            }
            // Rebuild unsigned UserOp with fresh nonce and initCode
            const retryOp = {
                sender,
                nonce: retryNonce,
                callData,
                callGasLimit: '0x0',
                verificationGasLimit: '0x0',
                preVerificationGas: '0x0',
                maxFeePerGas: fast.maxFeePerGas,
                maxPriorityFeePerGas: fast.maxPriorityFeePerGas,
                signature: DUMMY_SIGNATURE,
            };
            if (retryFactory) {
                retryOp.factory = retryFactory;
                retryOp.factoryData = retryFactoryData;
            }
            // Re-sponsor and re-sign
            const retrySponsor = await rpc('pm_sponsorUserOperation', [retryOp, entryPoint]);
            Object.assign(retryOp, retrySponsor);
            const retryOpJson = JSON.stringify(retryOp);
            const retryHashHex = getWasm().hashUserOp(retryOpJson, entryPoint, BigInt(config.chainId));
            const retrySigHex = getWasm().signUserOp(retryHashHex, eoa.private_key);
            retryOp.signature = `0x${retrySigHex}`;
            userOpHash = await rpc('eth_sendUserOperation', [retryOp, entryPoint]);
        }
        else {
            throw err;
        }
    }
    // 10. Wait for receipt (poll up to 120s)
    let receipt = null;
    for (let i = 0; i < 60; i++) {
        await new Promise(r => setTimeout(r, 2000));
        try {
            receipt = await rpc('eth_getUserOperationReceipt', [userOpHash]);
            if (receipt)
                break;
        }
        catch { /* not mined yet */ }
    }
    const success = receipt?.success ?? false;
    // Mark account as deployed after first successful submission
    if (success) {
        deployedAccounts.add(sender.toLowerCase());
    }
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
export async function submitFactBatchOnChain(protobufPayloads, config) {
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
    const eoa = getWasm().deriveEoa(config.mnemonic);
    const sender = config.walletAddress || await deriveSmartAccountAddress(config.mnemonic, config.chainId);
    return withSenderLock(sender, () => submitFactBatchOnChainLocked(protobufPayloads, config, eoa, sender));
}
async function submitFactBatchOnChainLocked(protobufPayloads, config, eoa, sender) {
    const bundlerUrl = `${config.relayUrl}/v1/bundler`;
    const overrides = {
        'Content-Type': 'application/json',
    };
    if (config.authKeyHex)
        overrides['Authorization'] = `Bearer ${config.authKeyHex}`;
    if (config.walletAddress)
        overrides['X-Wallet-Address'] = config.walletAddress;
    const headers = buildRelayHeaders(overrides);
    // Helper for JSON-RPC calls to relay bundler (with 429 retry)
    async function rpc(method, params) {
        return rpcWithRetry(bundlerUrl, headers, method, params);
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
    // Check if Smart Account is deployed (needed for factory/factoryData)
    const { factory, factoryData } = await getInitCode(sender, eoa.address, rpcUrl);
    // Get nonce via bundler (accounts for pending mempool UserOps) with public RPC fallback
    const senderPadded = sender.slice(2).toLowerCase().padStart(64, '0');
    const keyPadded = '0'.repeat(64);
    const nonceCalldata = `0x35567e1a${senderPadded}${keyPadded}`;
    let nonce;
    try {
        const nonceResult = await rpc('eth_call', [{ to: entryPoint, data: nonceCalldata }, 'latest']);
        nonce = nonceResult || '0x0';
    }
    catch {
        const nonceResp = await fetch(rpcUrl, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0', id: 1, method: 'eth_call',
                params: [{ to: entryPoint, data: nonceCalldata }, 'latest'],
            }),
        });
        const nonceJson = await nonceResp.json();
        nonce = nonceJson.result || '0x0';
    }
    // Build unsigned UserOp
    const unsignedOp = {
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
            if (gasEstimate.callGasLimit)
                unsignedOp.callGasLimit = gasEstimate.callGasLimit;
            if (gasEstimate.verificationGasLimit)
                unsignedOp.verificationGasLimit = gasEstimate.verificationGasLimit;
            if (gasEstimate.preVerificationGas)
                unsignedOp.preVerificationGas = gasEstimate.preVerificationGas;
        }
        catch {
            // If estimation fails, let the paymaster handle it (default behavior)
        }
    }
    // Paymaster sponsorship (uses gas limits from estimation above for batches)
    const sponsorResult = await rpc('pm_sponsorUserOperation', [unsignedOp, entryPoint]);
    Object.assign(unsignedOp, sponsorResult);
    // Hash and sign via WASM
    const opJson = JSON.stringify(unsignedOp);
    const hashHex = getWasm().hashUserOp(opJson, entryPoint, BigInt(config.chainId));
    const sigHex = getWasm().signUserOp(hashHex, eoa.private_key);
    unsignedOp.signature = `0x${sigHex}`;
    // Submit (with AA25 nonce conflict retry)
    let userOpHash;
    try {
        userOpHash = await rpc('eth_sendUserOperation', [unsignedOp, entryPoint]);
    }
    catch (err) {
        const msg = err?.message || '';
        if (/AA25|AA10|invalid account nonce|already being processed/i.test(msg)) {
            console.error('AA25/AA10 nonce conflict detected (batch), rebuilding UserOp with fresh nonce...');
            // Bust deployment cache so getInitCode re-checks on-chain
            deployedAccounts.delete(sender.toLowerCase());
            // Wait for previous UserOp to mine before retrying with fresh nonce.
            // Public RPC won't reflect the new nonce until the tx is on-chain.
            await new Promise(r => setTimeout(r, 15000));
            // Re-fetch initCode and nonce
            const { factory: retryFactory, factoryData: retryFactoryData } = await getInitCode(sender, eoa.address, rpcUrl);
            let retryNonce;
            try {
                const retryNonceResult = await rpc('eth_call', [{ to: entryPoint, data: nonceCalldata }, 'latest']);
                retryNonce = retryNonceResult || '0x0';
            }
            catch {
                const retryNonceResp = await fetch(rpcUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        jsonrpc: '2.0', id: 1, method: 'eth_call',
                        params: [{ to: entryPoint, data: nonceCalldata }, 'latest'],
                    }),
                });
                const retryNonceJson = await retryNonceResp.json();
                retryNonce = retryNonceJson.result || '0x0';
            }
            // Rebuild unsigned UserOp with fresh nonce and initCode
            const retryOp = {
                sender,
                nonce: retryNonce,
                callData,
                callGasLimit: '0x0',
                verificationGasLimit: '0x0',
                preVerificationGas: '0x0',
                maxFeePerGas: fast.maxFeePerGas,
                maxPriorityFeePerGas: fast.maxPriorityFeePerGas,
                signature: DUMMY_SIGNATURE,
            };
            if (retryFactory) {
                retryOp.factory = retryFactory;
                retryOp.factoryData = retryFactoryData;
            }
            // Re-sponsor and re-sign
            const retrySponsor = await rpc('pm_sponsorUserOperation', [retryOp, entryPoint]);
            Object.assign(retryOp, retrySponsor);
            const retryOpJson = JSON.stringify(retryOp);
            const retryHashHex = getWasm().hashUserOp(retryOpJson, entryPoint, BigInt(config.chainId));
            const retrySigHex = getWasm().signUserOp(retryHashHex, eoa.private_key);
            retryOp.signature = `0x${retrySigHex}`;
            userOpHash = await rpc('eth_sendUserOperation', [retryOp, entryPoint]);
        }
        else {
            throw err;
        }
    }
    // Wait for receipt (poll up to 120s)
    let receipt = null;
    for (let i = 0; i < 60; i++) {
        await new Promise(r => setTimeout(r, 2000));
        try {
            receipt = await rpc('eth_getUserOperationReceipt', [userOpHash]);
            if (receipt)
                break;
        }
        catch { /* not mined yet */ }
    }
    const batchSuccess = receipt?.success ?? false;
    // Mark account as deployed after first successful submission
    if (batchSuccess) {
        deployedAccounts.add(sender.toLowerCase());
    }
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
export function isSubgraphMode() {
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
export function getSubgraphConfig() {
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
