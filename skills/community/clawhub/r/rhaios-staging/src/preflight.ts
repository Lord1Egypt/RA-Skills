import { PrivyClient } from '@privy-io/node';
import type { Address, Hex } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';
import { HEALTH_URL } from './client.ts';
import {
  type HealthSnapshot,
  type PrepareSignExecuteRequest,
  type RpcOverrideConfig,
  type RequiredRunControls,
  type ResolvedChain,
  type SignerBackend,
  PreflightError,
  normalizeControls,
  resolveChain,
} from './types.ts';

const ADDRESS_RE = /^0x[a-fA-F0-9]{40}$/;
const PRIVATE_KEY_RE = /^0x[a-fA-F0-9]{64}$/;

function asAddress(value: string, label: string): Address {
  if (!ADDRESS_RE.test(value)) {
    throw new PreflightError(
      `${label} is not a valid EVM address`,
      `${label} must be a 20-byte hex string.`,
      `Provide a valid ${label} value (example: 0x...).`,
    );
  }
  return value as Address;
}

function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) {
    throw new PreflightError(
      `Missing ${name}`,
      `${name} is required for this flow.`,
      `Set ${name} in your environment or secret manager.`,
    );
  }
  return value;
}

function resolveChainRpcUrl(): string | undefined {
  // Staging uses managed forks via the API — no client-side RPC needed.
  return undefined;
}

function resolveSignerBackend(): SignerBackend {
  const backend = (process.env.SIGNER_BACKEND ?? 'privy').toLowerCase();
  if (backend === 'privy') return 'privy';
  if (backend === 'private-key' || backend === 'local') return 'private-key';
  throw new PreflightError(
    'Unsupported SIGNER_BACKEND',
    `SIGNER_BACKEND=${backend} is not supported.`,
    'Use SIGNER_BACKEND=privy or SIGNER_BACKEND=private-key.',
  );
}

function requirePrivateKeyEnv(name: string): Hex {
  const value = requireEnv(name).trim();
  if (!PRIVATE_KEY_RE.test(value)) {
    throw new PreflightError(
      `Invalid ${name}`,
      `${name} must be a 32-byte hex private key.`,
      `Set ${name}=0x<64 hex chars>.`,
    );
  }
  return value as Hex;
}

function parsePositiveNumber(value: string, label: string): number {
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed <= 0) {
    throw new PreflightError(
      `${label} must be positive`,
      `${label} received "${value}" but expected a positive number.`,
      `Set ${label} to a positive decimal value.`,
    );
  }
  return parsed;
}

async function fetchHealth(): Promise<HealthSnapshot> {
  const res = await fetch(HEALTH_URL);
  if (!res.ok) {
    throw new PreflightError(
      'API health endpoint is unreachable',
      `GET ${HEALTH_URL} returned HTTP ${res.status}.`,
      'Verify RHAIOS_API_URL/reachability before executing transactions.',
    );
  }
  const raw = await res.json() as Record<string, unknown>;
  const freshness = (raw.freshness ?? {}) as Record<string, unknown>;
  const latestSnapshotAt = freshness.latestSnapshotAt;
  return {
    status: typeof raw.status === 'string' ? raw.status : undefined,
    sessions: typeof raw.sessions === 'number' ? raw.sessions : undefined,
    tools: typeof raw.tools === 'number' ? raw.tools : undefined,
    freshnessStatus: typeof freshness.snapshotFreshnessStatus === 'string'
      ? freshness.snapshotFreshnessStatus
      : undefined,
    latestSnapshotAt: typeof latestSnapshotAt === 'string' || latestSnapshotAt === null
      ? latestSnapshotAt
      : undefined,
  };
}

function applyHealthRules(
  health: HealthSnapshot,
  controls: RequiredRunControls,
  warnings: string[],
): void {
  if (!health.status) {
    warnings.push('health.status missing in response');
  } else if (health.status !== 'ok') {
    warnings.push(`health.status is "${health.status}"`);
  }

  if (health.freshnessStatus === 'critical') {
    throw new PreflightError(
      'Snapshot freshness is critical',
      'Indexer snapshots are not ready, so vault discovery/prepare may fail.',
      'Wait for indexer snapshots to recover, then retry.',
    );
  }
  if (health.freshnessStatus && health.freshnessStatus !== 'healthy') {
    warnings.push(`snapshot freshness is "${health.freshnessStatus}"`);
  }

  if (controls.strictMode && warnings.length > 0) {
    throw new PreflightError(
      'Strict mode blocked warnings',
      warnings.join(' | '),
      'Resolve warnings or set controls.strictMode=false for this run.',
    );
  }
}

function ensureConfirmation(controls: RequiredRunControls): void {
  if (!controls.requireConfirm || controls.dryRun) return;
  if (controls.confirm !== 'yes') {
    throw new PreflightError(
      'Live execution confirmation missing',
      'controls.requireConfirm is true and this is not a dry run.',
      'Set controls.confirm to "yes" for live execution.',
    );
  }
}

function validatePreparePayload(input: PrepareSignExecuteRequest): void {
  if (input.operation === 'deposit') {
    if (!input.deposit?.asset || !input.deposit?.amount) {
      throw new PreflightError(
        'Deposit payload incomplete',
        'Deposit requires deposit.asset and deposit.amount.',
        'Provide {"deposit":{"asset":"USDC","amount":"1"}}.',
      );
    }
    parsePositiveNumber(input.deposit.amount, 'deposit.amount');
  }

  if (input.operation === 'redeem') {
    if (!input.redeem?.vaultId) {
      throw new PreflightError(
        'Redeem payload incomplete',
        'Redeem requires redeem.vaultId.',
        'Provide redeem.vaultId from yield_status.',
      );
    }
    const hasPercentage = typeof input.redeem.percentage === 'number';
    const hasShares = typeof input.redeem.shares === 'string' && input.redeem.shares.length > 0;
    if (hasPercentage === hasShares) {
      throw new PreflightError(
        'Redeem requires exactly one amount selector',
        'Provide percentage OR shares, but not both.',
        'Set either redeem.percentage or redeem.shares.',
      );
    }
    if (hasPercentage && (input.redeem.percentage! <= 0 || input.redeem.percentage! > 100)) {
      throw new PreflightError(
        'redeem.percentage out of range',
        'percentage must be > 0 and <= 100.',
        'Set redeem.percentage to a value between 1 and 100.',
      );
    }
  }

  if (input.operation === 'rebalance') {
    if (!input.rebalance?.vaultId || !input.rebalance?.asset) {
      throw new PreflightError(
        'Rebalance payload incomplete',
        'Rebalance requires rebalance.vaultId and rebalance.asset.',
        'Provide rebalance.vaultId and rebalance.asset.',
      );
    }
    const hasPercentage = typeof input.rebalance.percentage === 'number';
    const hasShares = typeof input.rebalance.shares === 'string' && input.rebalance.shares.length > 0;
    if (hasPercentage === hasShares) {
      throw new PreflightError(
        'Rebalance requires exactly one amount selector',
        'Provide percentage OR shares, but not both.',
        'Set either rebalance.percentage or rebalance.shares.',
      );
    }
    if (hasPercentage && (input.rebalance.percentage! <= 0 || input.rebalance.percentage! > 100)) {
      throw new PreflightError(
        'rebalance.percentage out of range',
        'percentage must be > 0 and <= 100.',
        'Set rebalance.percentage to a value between 1 and 100.',
      );
    }
  }
}

function enforceMaxAmountIfConfigured(
  input: PrepareSignExecuteRequest,
  controls: RequiredRunControls,
): void {
  if (!controls.maxAmount || input.operation !== 'deposit' || !input.deposit?.amount) return;
  const max = parsePositiveNumber(controls.maxAmount, 'controls.maxAmount');
  const amount = parsePositiveNumber(input.deposit.amount, 'deposit.amount');
  if (amount > max) {
    throw new PreflightError(
      'Deposit amount exceeds controls.maxAmount',
      `Requested ${amount} > max ${max}.`,
      'Lower deposit.amount or raise controls.maxAmount.',
    );
  }
}

function validateChainRules(chain: ResolvedChain, warnings: string[]): void {
  if (chain.slug !== 'base') {
    warnings.push(`chain is "${chain.slug}" (default is "base")`);
  }
}

async function verifyOwnerlessPrivyWallet(
  appId: string,
  appSecret: string,
  walletId: string,
  expectedAddress: Address,
): Promise<void> {
  let wallet: { address?: string; owner_id?: string | null };
  try {
    const client = new PrivyClient({ appId, appSecret });
    wallet = await client.wallets().get(walletId);
  } catch (error) {
    throw new PreflightError(
      'Failed to fetch Privy wallet metadata',
      error instanceof Error ? error.message : String(error),
      'Verify PRIVY_APP_ID/PRIVY_APP_SECRET/PRIVY_WALLET_ID are correct and retry.',
    );
  }

  if (!wallet.address || !ADDRESS_RE.test(wallet.address)) {
    throw new PreflightError(
      'Privy wallet has an invalid address',
      `wallet ${walletId} returned address "${String(wallet.address)}".`,
      'Use a valid EVM wallet ID and retry.',
    );
  }

  if (wallet.address.toLowerCase() !== expectedAddress.toLowerCase()) {
    throw new PreflightError(
      'PRIVY_WALLET_ID and PRIVY_WALLET_ADDRESS do not match',
      `wallet ${walletId} is ${wallet.address}, but configured address is ${expectedAddress}.`,
      'Set PRIVY_WALLET_ADDRESS to the wallet address returned by Privy for PRIVY_WALLET_ID.',
    );
  }

  if (wallet.owner_id) {
    throw new PreflightError(
      'Privy wallet is owner-protected',
      `wallet ${walletId} has owner_id=${wallet.owner_id}, so signing requires privy-authorization-signature.`,
      'Use an ownerless wallet (owner_id=null) for this skill, then set PRIVY_WALLET_ID and PRIVY_WALLET_ADDRESS to that wallet.',
    );
  }
}

export interface PreparePreflightContext extends RpcOverrideConfig {
  controls: RequiredRunControls;
  chain: ResolvedChain;
  walletAddress: Address;
  signerBackend: SignerBackend;
  privy?: {
    appId: string;
    appSecret: string;
    walletId: string;
  };
  privateKey?: Hex;
  warnings: string[];
  health: HealthSnapshot;
}

export async function runPreparePreflight(input: PrepareSignExecuteRequest): Promise<PreparePreflightContext> {
  const signerBackend = resolveSignerBackend();
  const controls = normalizeControls(input.controls);
  const chain = resolveChain(input.chain);
  const chainRpcUrl = resolveChainRpcUrl();
  const warnings: string[] = [];
  let walletAddress: Address;
  let privy: PreparePreflightContext['privy'];
  let privateKey: Hex | undefined;

  ensureConfirmation(controls);
  validatePreparePayload(input);
  enforceMaxAmountIfConfigured(input, controls);

  if (signerBackend === 'privy') {
    const appId = requireEnv('PRIVY_APP_ID');
    const appSecret = requireEnv('PRIVY_APP_SECRET');
    const walletId = requireEnv('PRIVY_WALLET_ID');

    walletAddress = asAddress(
      input.agentAddress ?? requireEnv('PRIVY_WALLET_ADDRESS'),
      'agentAddress/PRIVY_WALLET_ADDRESS',
    );
    await verifyOwnerlessPrivyWallet(appId, appSecret, walletId, walletAddress);
    privy = { appId, appSecret, walletId };
  } else {
    privateKey = requirePrivateKeyEnv('SIGNER_PRIVATE_KEY');
    const account = privateKeyToAccount(privateKey);
    walletAddress = asAddress(
      input.agentAddress ?? account.address,
      'agentAddress',
    );
    if (walletAddress.toLowerCase() !== account.address.toLowerCase()) {
      throw new PreflightError(
        'agentAddress does not match SIGNER_PRIVATE_KEY',
        `derived address is ${account.address} but provided agentAddress is ${walletAddress}.`,
        'Set agentAddress to the private key address or omit agentAddress.',
      );
    }
  }

  const health = await fetchHealth();
  applyHealthRules(health, controls, warnings);
  validateChainRules(chain, warnings);

  return {
    controls,
    chain,
    ...(chainRpcUrl ? { chainRpcUrl } : {}),
    walletAddress,
    signerBackend,
    ...(privy ? { privy } : {}),
    ...(privateKey ? { privateKey } : {}),
    warnings,
    health,
  };
}
