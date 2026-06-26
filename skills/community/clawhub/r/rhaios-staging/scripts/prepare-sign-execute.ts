import { PrivyClient } from '@privy-io/node';
import {
  createPublicClient,
  formatGwei,
  http,
  keccak256,
  parseGwei,
  type Address,
  type Hex,
} from 'viem';
import { callApi } from '../src/client.ts';
import { runPreparePreflight } from '../src/preflight.ts';
import { createSigner, getPrepareGasInfo, signPreparedPayload } from '../src/signing.ts';
import { isRecord, type PrepareSignExecuteRequest, type ResolvedChain } from '../src/types.ts';
import { PreflightError } from '../src/types.ts';

const ADDRESS_RE = /^0x[a-fA-F0-9]{40}$/;
const HEX_RE = /^0x[0-9a-fA-F]*$/;
const HEX32_RE = /^0x[a-fA-F0-9]{64}$/;
type StageStatus = 'PASS' | 'WARN' | 'FAIL';

interface SetupPayload {
  to: Address;
  initCalldata: Hex;
  setupType: 'full' | 'modules';
  authorization: {
    contractAddress: Address;
    chainId: number;
  } | null;
  gasLimit?: bigint;
}

interface SetupTicket {
  version: 1;
  walletAddress: Address;
  chainId: number;
  implementation: Address;
  initCalldataHash: Hex;
  setupType?: 'full' | 'modules';
  expiresAt: string;
}

interface IntentIdentity {
  intentId: Hex;
}

interface SignedAuthorization {
  address: Address;
  nonce: number;
  chainId: number;
  yParity: 0 | 1;
  r: Hex;
  s: Hex;
}

type ExecuteClassification = 'EXECUTED' | 'DEDUP';

function logStage(stage: string, status: StageStatus, lines: string[] = []): void {
  console.log(`\n${stage}: ${status}`);
  for (const line of lines) {
    console.log(`  - ${line}`);
  }
}

function toRpcQuantity(value: bigint | number): string {
  const normalized = typeof value === 'number' ? BigInt(value) : value;
  return `0x${normalized.toString(16)}`;
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function rpcTransport(chainRpcUrl?: string) {
  return chainRpcUrl ? http(chainRpcUrl) : http();
}

function normalizeSignedTransactionHex(raw: string): Hex {
  if (/^0x[0-9a-fA-F]+$/.test(raw)) return raw as Hex;
  if (/^[0-9a-fA-F]+$/.test(raw)) return `0x${raw}` as Hex;
  throw new Error(`Privy eth_signTransaction returned invalid signed_transaction: ${raw}`);
}

async function signType2ViaPrivyRpc(params: {
  appId: string;
  appSecret: string;
  walletId: string;
  chainId: number;
  nonce: bigint;
  to: Address;
  data: Hex;
  gas: bigint;
  maxFeePerGas?: bigint;
  maxPriorityFeePerGas?: bigint;
}): Promise<Hex> {
  const client = new PrivyClient({ appId: params.appId, appSecret: params.appSecret });
  const signed = await client.wallets().ethereum().signTransaction(params.walletId, {
    params: {
      transaction: {
        type: 2,
        chain_id: params.chainId,
        nonce: toRpcQuantity(params.nonce),
        to: params.to,
        data: params.data,
        gas_limit: toRpcQuantity(params.gas),
        ...(params.maxFeePerGas ? { max_fee_per_gas: toRpcQuantity(params.maxFeePerGas) } : {}),
        ...(params.maxPriorityFeePerGas ? { max_priority_fee_per_gas: toRpcQuantity(params.maxPriorityFeePerGas) } : {}),
      },
    },
  });
  return normalizeSignedTransactionHex(String(signed.signed_transaction ?? ''));
}

async function signType4ViaPrivyRpc(params: {
  appId: string;
  appSecret: string;
  walletId: string;
  chainId: number;
  nonce: bigint;
  to: Address;
  data: Hex;
  gas: bigint;
  maxFeePerGas?: bigint;
  maxPriorityFeePerGas?: bigint;
  auth: SignedAuthorization;
}): Promise<Hex> {
  const client = new PrivyClient({ appId: params.appId, appSecret: params.appSecret });
  const signed = await client.wallets().ethereum().signTransaction(params.walletId, {
    params: {
      transaction: {
        type: 4,
        chain_id: params.chainId,
        nonce: toRpcQuantity(params.nonce),
        to: params.to,
        data: params.data,
        gas_limit: toRpcQuantity(params.gas),
        ...(params.maxFeePerGas ? { max_fee_per_gas: toRpcQuantity(params.maxFeePerGas) } : {}),
        ...(params.maxPriorityFeePerGas ? { max_priority_fee_per_gas: toRpcQuantity(params.maxPriorityFeePerGas) } : {}),
        authorization_list: [{
          chain_id: params.auth.chainId,
          contract: params.auth.address,
          nonce: params.auth.nonce,
          y_parity: params.auth.yParity,
          r: params.auth.r,
          s: params.auth.s,
        }],
      },
    },
  });
  return normalizeSignedTransactionHex(String(signed.signed_transaction ?? ''));
}

async function signAndBroadcastPrivyTransactionViaCustomRpc(params: {
  client: PrivyClient;
  walletId: string;
  chain: ResolvedChain['chain'];
  chainRpcUrl: string;
  transaction: {
    type?: 0 | 1 | 2 | 4;
    from?: Address;
    to?: Address;
    data?: Hex;
    value?: string;
    chain_id?: number;
    nonce?: string;
    gas_limit?: string;
    max_fee_per_gas?: string;
    max_priority_fee_per_gas?: string;
    authorization_list?: Array<{
      chain_id: number;
      contract: Address;
      nonce: number;
      y_parity: 0 | 1;
      r: Hex;
      s: Hex;
    }>;
  };
}): Promise<Hex> {
  const { client, walletId, chain, chainRpcUrl, transaction } = params;
  const signed = await client.wallets().ethereum().signTransaction(walletId, {
    params: {
      transaction,
    },
  });
  const signedRawTx = normalizeSignedTransactionHex(String(signed.signed_transaction ?? ''));
  const rpcClient = createPublicClient({
    chain,
    transport: rpcTransport(chainRpcUrl),
  });
  const txHash = await rpcClient.request({
    method: 'eth_sendRawTransaction',
    params: [signedRawTx],
  });
  if (typeof txHash !== 'string' || !/^0x[0-9a-fA-F]{64}$/.test(txHash)) {
    throw new Error(`Custom RPC eth_sendRawTransaction returned invalid hash: ${String(txHash)}`);
  }
  return txHash as Hex;
}

function failStage(stage: string, what: string, why: string, fix: string): never {
  logStage(stage, 'FAIL', [
    `What: ${what}`,
    `Why: ${why}`,
    `Fix: ${fix}`,
  ]);
  process.exit(1);
}

function classifyExecuteResult(payload: Record<string, unknown>): {
  classification: ExecuteClassification;
  resultField: string | null;
  receiptSource: string | null;
} {
  const resultField = typeof payload.result === 'string' ? payload.result : null;
  const receipt = isRecord(payload.receipt) ? payload.receipt : null;
  const receiptSource = receipt && typeof receipt.source === 'string' ? receipt.source : null;

  if (resultField === 'already_executed' || receiptSource === 'cached') {
    return {
      classification: 'DEDUP',
      resultField,
      receiptSource,
    };
  }

  return {
    classification: 'EXECUTED',
    resultField,
    receiptSource,
  };
}

async function readAllStdin(): Promise<string> {
  const chunks: Buffer[] = [];
  for await (const chunk of process.stdin) {
    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
  }
  return Buffer.concat(chunks).toString('utf8').trim();
}

async function readJsonStdin<T>(scriptName: string): Promise<T> {
  const raw = await readAllStdin();
  if (!raw) {
    throw new Error(
      `${scriptName} requires a JSON payload on stdin. Example: echo '{"operation":"deposit",...}' | bun run ...`,
    );
  }

  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch (error) {
    throw new Error(
      `Invalid JSON payload: ${error instanceof Error ? error.message : String(error)}`,
    );
  }

  if (!isRecord(parsed)) {
    throw new Error('JSON payload must be an object.');
  }

  return parsed as T;
}

function buildPrepareArgs(
  input: PrepareSignExecuteRequest,
  walletAddress: string,
  chain: string,
): Record<string, unknown> {
  if (input.operation === 'deposit') {
    return {
      operation: 'deposit',
      chain,
      agentAddress: walletAddress,
      asset: input.deposit!.asset,
      amount: input.deposit!.amount,
      vaultId: input.deposit!.vaultId,
    };
  }
  if (input.operation === 'redeem') {
    const amountSelection = input.redeem!.shares
      ? { shares: input.redeem!.shares }
      : { percentage: input.redeem!.percentage! };
    return {
      operation: 'redeem',
      chain,
      agentAddress: walletAddress,
      vaultId: input.redeem!.vaultId,
      ...amountSelection,
    };
  }
  const amountSelection = input.rebalance!.shares
    ? { shares: input.rebalance!.shares }
    : { percentage: input.rebalance!.percentage! };
  return {
    operation: 'rebalance',
    chain,
    agentAddress: walletAddress,
    vaultId: input.rebalance!.vaultId,
    asset: input.rebalance!.asset,
    ...amountSelection,
  };
}

function enforceGasCapIfConfigured(
  maxGasGwei: string | undefined,
  preparePayload: Record<string, unknown>,
): void {
  if (!maxGasGwei) return;
  const gas = getPrepareGasInfo(preparePayload);
  if (!gas?.maxFeePerGas) return;

  const maxAllowedWei = parseGwei(maxGasGwei);
  const txMaxWei = BigInt(gas.maxFeePerGas);
  if (txMaxWei > maxAllowedWei) {
    failStage(
      'Prepare',
      'Gas cap exceeded',
      `prepare maxFeePerGas=${formatGwei(txMaxWei)} gwei is above controls.maxGasGwei=${maxGasGwei}.`,
      'Raise controls.maxGasGwei or retry when base fees are lower.',
    );
  }
}

function parseSetupPayload(
  preparePayload: Record<string, unknown>,
  expectedWalletAddress: Address,
): SetupPayload {
  const setup = preparePayload.setup;
  if (!isRecord(setup)) {
    throw new Error('yield_prepare needsSetup=true but setup payload is missing.');
  }

  const toRaw = setup.to;
  if (typeof toRaw !== 'string' || !ADDRESS_RE.test(toRaw)) {
    throw new Error('setup.to is missing or invalid.');
  }
  if (toRaw.toLowerCase() !== expectedWalletAddress.toLowerCase()) {
    throw new Error(
      `setup.to (${toRaw}) does not match wallet address (${expectedWalletAddress}).`,
    );
  }

  const initCalldata = setup.initCalldata;
  if (typeof initCalldata !== 'string' || !HEX_RE.test(initCalldata)) {
    throw new Error('setup.initCalldata is missing or invalid.');
  }

  // setupType: 'full' (default) requires authorization, 'modules' does not
  const setupType = setup.setupType === 'modules' ? 'modules' : 'full';

  let authorization: SetupPayload['authorization'] = null;
  if (setupType === 'full') {
    const authRaw = setup.authorization;
    if (!isRecord(authRaw)) {
      throw new Error('setup.authorization is missing (required for full setup).');
    }
    const contractAddress = authRaw.contractAddress;
    if (typeof contractAddress !== 'string' || !ADDRESS_RE.test(contractAddress)) {
      throw new Error('setup.authorization.contractAddress is missing or invalid.');
    }
    const chainId = authRaw.chainId;
    if (typeof chainId !== 'number' || !Number.isInteger(chainId) || chainId <= 0) {
      throw new Error('setup.authorization.chainId is missing or invalid.');
    }
    authorization = { contractAddress: contractAddress as Address, chainId };
  }

  let gasLimit: bigint | undefined;
  if (isRecord(setup.gas) && typeof setup.gas.gasLimit === 'string') {
    try {
      gasLimit = BigInt(setup.gas.gasLimit);
    } catch {
      throw new Error('setup.gas.gasLimit must be a valid integer string.');
    }
  }

  return {
    to: toRaw as Address,
    initCalldata: initCalldata as Hex,
    setupType,
    authorization,
    gasLimit,
  };
}

function parseSetupTicket(
  preparePayload: Record<string, unknown>,
  expectedWalletAddress: Address,
  expectedChainId: number,
): SetupTicket {
  const ticket = preparePayload.setupTicket;
  if (!isRecord(ticket)) {
    throw new Error('yield_prepare needsSetup=true but setupTicket is missing.');
  }

  if (ticket.version !== 1) {
    throw new Error('setupTicket.version must be 1.');
  }

  const walletAddress = ticket.walletAddress;
  if (typeof walletAddress !== 'string' || !ADDRESS_RE.test(walletAddress)) {
    throw new Error('setupTicket.walletAddress is missing or invalid.');
  }
  if (walletAddress.toLowerCase() !== expectedWalletAddress.toLowerCase()) {
    throw new Error(
      `setupTicket.walletAddress (${walletAddress}) does not match wallet address (${expectedWalletAddress}).`,
    );
  }

  const chainId = ticket.chainId;
  if (typeof chainId !== 'number' || !Number.isInteger(chainId) || chainId <= 0) {
    throw new Error('setupTicket.chainId is missing or invalid.');
  }
  if (chainId !== expectedChainId) {
    throw new Error(`setupTicket.chainId (${chainId}) does not match selected chain (${expectedChainId}).`);
  }

  const implementation = ticket.implementation;
  if (typeof implementation !== 'string' || !ADDRESS_RE.test(implementation)) {
    throw new Error('setupTicket.implementation is missing or invalid.');
  }

  const initCalldataHash = ticket.initCalldataHash;
  if (typeof initCalldataHash !== 'string' || !HEX32_RE.test(initCalldataHash)) {
    throw new Error('setupTicket.initCalldataHash is missing or invalid.');
  }

  const expiresAt = ticket.expiresAt;
  if (typeof expiresAt !== 'string' || Number.isNaN(Date.parse(expiresAt))) {
    throw new Error('setupTicket.expiresAt is missing or invalid.');
  }

  const setupType = ticket.setupType === 'modules' ? 'modules' as const : 'full' as const;

  return {
    version: 1,
    walletAddress: walletAddress as Address,
    chainId,
    implementation: implementation as Address,
    initCalldataHash: initCalldataHash as Hex,
    setupType,
    expiresAt,
  };
}

function buildFallbackSetupTicket(
  setupPayload: SetupPayload,
  walletAddress: Address,
  chainId: number,
): SetupTicket {
  if (!setupPayload.authorization) {
    throw new Error('Cannot build fallback setup ticket without authorization (module-only setup requires explicit setupTicket from server).');
  }
  return {
    version: 1,
    walletAddress,
    chainId,
    implementation: setupPayload.authorization.contractAddress,
    initCalldataHash: keccak256(setupPayload.initCalldata),
    setupType: setupPayload.setupType,
    expiresAt: new Date(Date.now() + 15 * 60 * 1000).toISOString(),
  };
}

function extractIntentIdentity(preparePayload: Record<string, unknown>): IntentIdentity {
  const preparedEnvelope = preparePayload.intentEnvelope as Record<string, unknown> | undefined;
  const merkleRoot = typeof preparedEnvelope?.merkleRoot === 'string'
    ? preparedEnvelope.merkleRoot
    : '';
  const responseIntentId = typeof preparePayload.intentId === 'string'
    ? preparePayload.intentId
    : '';

  if (!HEX32_RE.test(merkleRoot)) {
    failStage(
      'Prepare',
      'Missing intent merkleRoot',
      'yield_prepare did not return a valid intentEnvelope.merkleRoot.',
      'Retry and verify API returns an executable intentEnvelope.',
    );
  }

  if (responseIntentId && responseIntentId !== merkleRoot) {
    failStage(
      'Prepare',
      'Intent ID mismatch',
      `intentId=${responseIntentId} does not match intentEnvelope.merkleRoot=${merkleRoot}.`,
      'Use the exact response from yield_prepare and retry.',
    );
  }

  return { intentId: merkleRoot as Hex };
}

function extractStrategyVaultAddress(preparePayload: Record<string, unknown>): Address | null {
  const strategy = preparePayload.strategy;
  if (!isRecord(strategy)) return null;
  const vault = strategy.vault;
  if (typeof vault !== 'string' || !ADDRESS_RE.test(vault)) return null;
  return vault as Address;
}

/** Fork-only relay mode. Hardcoded true for staging — cannot be disabled. */
function isForkOnlyModeEnabled(): boolean {
  return true;
}


async function main(): Promise<void> {
  let input: PrepareSignExecuteRequest;
  try {
    input = await readJsonStdin<PrepareSignExecuteRequest>('prepare-sign-execute');
  } catch (error) {
    failStage(
      'Input',
      'Invalid request payload',
      error instanceof Error ? error.message : String(error),
      'Provide valid JSON on stdin that matches the script schema.',
    );
  }

  let preflight;
  try {
    preflight = await runPreparePreflight(input!);
  } catch (error) {
    if (error instanceof PreflightError) {
      failStage('Preflight', error.what, error.why, error.fix);
    }
    failStage(
      'Preflight',
      'Unexpected preflight failure',
      error instanceof Error ? error.message : String(error),
      'Inspect the error and retry.',
    );
  }

  logStage('Preflight', 'PASS', [
    `chain: ${preflight.chain.slug} (${preflight.chain.chainId})`,
    `wallet: ${preflight.walletAddress}`,
    `signerBackend: ${preflight.signerBackend}`,
    `chainRpcUrl: ${preflight.chainRpcUrl ?? 'default'}`,
    `health: ${preflight.health.status ?? 'unknown'}/${preflight.health.freshnessStatus ?? 'unknown'}`,
    ...preflight.warnings.map((warning) => `warning: ${warning}`),
  ]);

  // Require vaultId for deposits — agents should call yield_discover first,
  // present results to the user, and let them choose a vault.
  if (input!.operation === 'deposit' && !input!.deposit?.vaultId) {
    failStage(
      'Prepare',
      'Missing deposit.vaultId',
      'deposit.vaultId is required. Call yield_discover first to browse vaults, present results to the user, and pass their chosen vaultId.',
      'Run yield_discover, let the user pick a vault, then include deposit.vaultId in the request.',
    );
  }

  const prepareArgs = buildPrepareArgs(input!, preflight.walletAddress, preflight.chain.slug);
  const { payload: firstPreparePayload, isError: firstPrepareIsError } = await callApi(
'yield_prepare',
    prepareArgs,
  );

  if (firstPrepareIsError || firstPreparePayload.error) {
    failStage(
      'Prepare',
      'yield_prepare failed',
      String(firstPreparePayload.error ?? firstPreparePayload.detail ?? JSON.stringify(firstPreparePayload)),
      'Fix request parameters, server oracle config, or snapshot freshness and retry.',
    );
  }

  enforceGasCapIfConfigured(preflight.controls.maxGasGwei, firstPreparePayload);
  let preparePayload = firstPreparePayload;
  let needsSetup = preparePayload.needsSetup === true;
  logStage('Prepare', 'PASS', [
    `operation: ${input!.operation}`,
    `needsSetup: ${String(needsSetup)}`,
    `merkleRoot: ${needsSetup ? 'n/a (setup required)' : extractIntentIdentity(preparePayload).intentId}`,
  ]);

  const publicClient = createPublicClient({
    chain: preflight.chain.chain,
    transport: rpcTransport(preflight.chainRpcUrl),
  });

  const signer = createSigner({
    signerBackend: preflight.signerBackend,
    walletAddress: preflight.walletAddress,
    ...(preflight.privy ? { privy: preflight.privy } : {}),
    ...(preflight.privateKey ? { privateKey: preflight.privateKey } : {}),
  });
  let resolvedIntentId: Hex | null = needsSetup
    ? null
    : extractIntentIdentity(preparePayload).intentId;

  if (needsSetup) {
    if (input!.operation !== 'deposit') {
      failStage(
        'Setup',
        'Setup is only supported for deposit',
        `operation=${input!.operation} returned needsSetup=true.`,
        'Run an initial deposit flow first to initialize the wallet.',
      );
    }

    if (preflight.controls.dryRun) {
      logStage('Setup', 'WARN', [
        'Dry run detected a wallet that needs setup.',
        'Run live mode (dryRun=false) to execute setup + re-prepare + sign + execute.',
      ]);
      return;
    }

    let setupPayload: SetupPayload;
    try {
      setupPayload = parseSetupPayload(preparePayload, preflight.walletAddress);
    } catch (error) {
      failStage(
        'Setup',
        'Invalid setup payload',
        error instanceof Error ? error.message : String(error),
        'Retry and inspect yield_prepare setup response fields.',
      );
    }

    let setupTicket: SetupTicket;
    try {
      setupTicket = parseSetupTicket(preparePayload, preflight.walletAddress, preflight.chain.chainId);
    } catch (error) {
      const detail = error instanceof Error ? error.message : String(error);
      const missingTicket = detail.includes('setupTicket is missing');
      if (!missingTicket) {
        failStage(
          'Setup',
          'Invalid setup ticket',
          detail,
          'Retry and inspect yield_prepare setupTicket response fields.',
        );
      }
      setupTicket = buildFallbackSetupTicket(
        setupPayload,
        preflight.walletAddress,
        preflight.chain.chainId,
      );
      logStage('Setup', 'WARN', [
        'yield_prepare setupTicket is missing (older API response).',
        'Using derived setupTicket fallback from setup payload for relay compatibility.',
      ]);
    }

    let setupTxHash: Hex;
    let setupReceipt: { status: string; blockNumber: string };
    try {
      const txNonce = BigInt(await publicClient.getTransactionCount({ address: preflight.walletAddress }));

      // Gas estimation: trust yield_prepare's server-side values (already fork-aware via
      // resolveRpcUrl) but apply a 2x buffer and enforce a minimum floor of 1 gwei.
      const serverMaxFee = setupPayload.gas?.maxFeePerGas ? BigInt(setupPayload.gas.maxFeePerGas) : 0n;
      const serverPriorityFee = setupPayload.gas?.maxPriorityFeePerGas ? BigInt(setupPayload.gas.maxPriorityFeePerGas) : 0n;
      const GAS_FLOOR = parseGwei('1');
      const PRIORITY_FLOOR = parseGwei('0.1');
      let maxFeePerGas = serverMaxFee * 2n;
      if (maxFeePerGas < GAS_FLOOR) maxFeePerGas = GAS_FLOOR;
      let maxPriorityFeePerGas = serverPriorityFee > 0n ? serverPriorityFee : PRIORITY_FLOOR;
      try {
        const fee = await publicClient.estimateFeesPerGas();
        if (fee.maxFeePerGas && fee.maxFeePerGas > maxFeePerGas) {
          maxFeePerGas = fee.maxFeePerGas;
        }
        if (fee.maxPriorityFeePerGas && fee.maxPriorityFeePerGas > maxPriorityFeePerGas) {
          maxPriorityFeePerGas = fee.maxPriorityFeePerGas;
        }
      } catch {
        // Client-side estimate failed — server values with buffer are sufficient
      }

      let signedRawTx: Hex;

      if (setupPayload.setupType === 'modules') {
        // Module-only: sign a regular Type-2 (EIP-1559) self-call transaction.
        // Delegation is already active — only initializeAccount() needs to run.
        if (preflight.signerBackend === 'privy' && preflight.privy) {
          signedRawTx = await signType2ViaPrivyRpc({
            appId: preflight.privy.appId,
            appSecret: preflight.privy.appSecret,
            walletId: preflight.privy.walletId,
            chainId: preflight.chain.chainId,
            nonce: txNonce,
            to: setupPayload.to,
            data: setupPayload.initCalldata,
            gas: setupPayload.gasLimit ?? 2_000_000n,
            maxFeePerGas,
            maxPriorityFeePerGas,
          });
        } else {
          signedRawTx = await signer.signTransaction({
            type: 'eip1559',
            chainId: preflight.chain.chainId,
            nonce: txNonce,
            to: setupPayload.to,
            data: setupPayload.initCalldata,
            gas: setupPayload.gasLimit ?? 2_000_000n,
            ...(maxFeePerGas ? { maxFeePerGas } : {}),
            ...(maxPriorityFeePerGas ? { maxPriorityFeePerGas } : {}),
          });
        }
      } else {
        // Full setup: sign a Type-4 (EIP-7702) transaction with authorization_list.
        if (!setupPayload.authorization) {
          throw new Error('Full setup requires authorization but it is null.');
        }
        const auth = await signer.signAuthorization({
          contractAddress: setupPayload.authorization.contractAddress,
          chainId: setupPayload.authorization.chainId,
          // EIP-7702 setup auth nonce must be the post-tx account nonce for self-call setup txs.
          nonce: Number(txNonce + 1n),
        }) as SignedAuthorization;

        if (preflight.signerBackend === 'privy' && preflight.privy) {
          signedRawTx = await signType4ViaPrivyRpc({
            appId: preflight.privy.appId,
            appSecret: preflight.privy.appSecret,
            walletId: preflight.privy.walletId,
            chainId: preflight.chain.chainId,
            nonce: txNonce,
            to: setupPayload.to,
            data: setupPayload.initCalldata,
            gas: setupPayload.gasLimit ?? 2_000_000n,
            maxFeePerGas,
            maxPriorityFeePerGas,
            auth,
          });
        } else {
          signedRawTx = await signer.signTransaction({
            type: 'eip7702',
            chainId: preflight.chain.chainId,
            nonce: txNonce,
            to: setupPayload.to,
            data: setupPayload.initCalldata,
            gas: setupPayload.gasLimit ?? 2_000_000n,
            ...(maxFeePerGas ? { maxFeePerGas } : {}),
            ...(maxPriorityFeePerGas ? { maxPriorityFeePerGas } : {}),
            authorizationList: [auth],
          });
        }
      }

      const { payload: relayPayload, isError: relayIsError } = await callApi(
        'yield_setup_relay',
        {
          setupTicket,
          signedRawTx,
          confirmations: 2,
        },
        180_000, // Setup relay broadcasts tx + waits for receipt — needs extended timeout
      );

      if (relayIsError || relayPayload.error) {
        throw new Error(
          String(relayPayload.error ?? relayPayload.detail ?? JSON.stringify(relayPayload)),
        );
      }

      if (relayPayload.delegationVerified !== true) {
        throw new Error(
          `yield_setup_relay did not verify delegation: ${JSON.stringify(relayPayload)}`,
        );
      }

      const txHash = relayPayload.txHash;
      if (typeof txHash !== 'string' || !/^0x[0-9a-fA-F]{64}$/.test(txHash)) {
        throw new Error(`yield_setup_relay returned invalid txHash: ${JSON.stringify(relayPayload)}`);
      }

      setupTxHash = txHash as Hex;
      setupReceipt = {
        status: String(relayPayload.receiptStatus ?? 'unknown'),
        blockNumber: String(relayPayload.blockNumber ?? 'unknown'),
      };
    } catch (error) {
      const detail = error instanceof Error ? error.message : String(error);
      failStage(
        'Setup',
        'Failed to relay setup transaction',
        detail,
        'Verify yield_setup_relay availability and signed transaction correctness, then retry.',
      );
    }
    if (setupReceipt.status !== 'success') {
      failStage(
        'Setup',
        'Setup transaction reverted',
        `txHash=${setupTxHash}`,
        'Fix chain/wallet permissions and retry the setup flow.',
      );
    }

    logStage('Setup', 'PASS', [
      `setupType: ${setupPayload.setupType}`,
      `txHash: ${setupTxHash}`,
      `status: ${setupReceipt.status}`,
      `block: ${setupReceipt.blockNumber}`,
    ]);

    let secondPreparePayload: Record<string, unknown> | null = null;
    const maxPrepareAttempts = 6;
    for (let attempt = 1; attempt <= maxPrepareAttempts; attempt++) {
      const { payload, isError } = await callApi(
        'yield_prepare',
        prepareArgs,
      );

      const hasError = isError || Boolean(payload.error);
      const stillNeedsSetup = payload.needsSetup === true;
      const envelope = payload.intentEnvelope as Record<string, unknown> | undefined;
      const hasMerkleRoot = typeof envelope?.merkleRoot === 'string' && HEX32_RE.test(envelope.merkleRoot);

      if (!hasError && !stillNeedsSetup && hasMerkleRoot) {
        secondPreparePayload = payload;
        break;
      }

      const detail = hasError
        ? String(payload.error ?? payload.detail ?? JSON.stringify(payload))
        : stillNeedsSetup
          ? 'needsSetup still true'
          : 'intentEnvelope.merkleRoot missing';
      if (attempt < maxPrepareAttempts) {
        logStage('Prepare', 'WARN', [
          `post-setup attempt ${attempt}/${maxPrepareAttempts} not ready: ${detail}`,
          'waiting 3s before retry',
        ]);
        await sleep(3_000);
        continue;
      }

      failStage(
        'Prepare',
        'yield_prepare failed after setup',
        detail,
        'Wait for setup tx indexing and retry.',
      );
    }
    enforceGasCapIfConfigured(preflight.controls.maxGasGwei, secondPreparePayload!);
    const secondIntent = extractIntentIdentity(secondPreparePayload!);

    preparePayload = secondPreparePayload!;
    resolvedIntentId = secondIntent.intentId;
    logStage('Prepare', 'PASS', [
      'phase: post-setup re-prepare',
      `operation: ${input!.operation}`,
      `needsSetup: false`,
      `merkleRoot: ${resolvedIntentId}`,
    ]);
  }

  let signed;
  try {
    signed = await signPreparedPayload({
      preparePayload,
      signer,
      chain: preflight.chain,
      publicClient,
    });
  } catch (error) {
    failStage(
      'Sign',
      'Failed to sign transaction',
      error instanceof Error ? error.message : String(error),
      'Validate wallet permissions and retry signing.',
    );
  }

  logStage('Sign', 'PASS', [
    `signature: ${String(signed.intentSignature).slice(0, 14)}...`,
    ...(signed.included7702AuthRequest ? ['7702AuthRequest: included'] : []),
  ]);

  if (preflight.controls.dryRun) {
    logStage('Execute', 'WARN', [
      'Dry run enabled: signed successfully, skipped yield_execute.',
    ]);
    return;
  }

  const { payload: executePayload, isError: executeIsError } = await callApi(
'yield_execute',
    {
      intentEnvelope: signed.intentEnvelope,
      intentSignature: signed.intentSignature,
      intentId: resolvedIntentId ?? undefined,
    },
    180_000, // Execute submits UserOp + waits for receipt — needs extended timeout
  );

  if (executeIsError || executePayload.error) {
    failStage(
      'Execute',
      'yield_execute failed',
      String(executePayload.error ?? executePayload.detail ?? JSON.stringify(executePayload)),
      'Inspect transaction validation errors and retry.',
    );
  }

  const executeClassification = classifyExecuteResult(executePayload);
  const receipt = (executePayload.receipt ?? {}) as Record<string, unknown>;
  logStage('Execute', 'PASS', [
    `classification: ${executeClassification.classification}`,
    `result: ${String(executeClassification.resultField ?? 'unknown')}`,
    `receipt.source: ${String(executeClassification.receiptSource ?? 'unknown')}`,
    `userOpHash: ${String(executePayload.userOpHash ?? '')}`,
    `txHash: ${String(executePayload.txHash ?? '')}`,
    `status: ${String(receipt.status ?? 'unknown')}`,
    `gasUsed: ${String(receipt.gasUsed ?? 'unknown')}`,
    `explorer: ${String(executePayload.explorerUrl ?? 'unknown')}`,
  ]);

  try {
    const { payload: statusPayload } = await callApi('yield_status', {
      userAddress: preflight.walletAddress,
    });
    const positionCount = Array.isArray(statusPayload.positions) ? statusPayload.positions.length : 0;
    logStage('Post-check', 'PASS', [
      `positions: ${positionCount}`,
      `totalValueUsd: ${String(statusPayload.totalValueUsd ?? 'n/a')}`,
    ]);
  } catch (error) {
    logStage('Post-check', 'WARN', [
      `status fetch failed: ${error instanceof Error ? error.message : String(error)}`,
    ]);
  }
}

await main();
